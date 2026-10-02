"""Durable agent-authored research coverage; model routing never grants closure.

Records reference existing files relative to core.ROOT. SQLite transactions retain
immutable revisions and compare-and-swap updates. Review digests include the actual
research content and its dependencies; status also verifies the referenced bytes.
The checker establishes consistency, not the truth of an agent's legal conclusion.
"""
from __future__ import annotations

import contextlib
import datetime as dt
import hashlib
import json
import re
import sqlite3
from pathlib import Path

from . import core

SCHEMA = 1
STATES = {"open", "investigating", "resolved", "excluded"}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def date(value):
    try:
        return dt.date.fromisoformat(value)
    except (TypeError, ValueError):
        raise core.PipelineError(f"invalid ISO date: {value!r}")


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", value):
        raise core.PipelineError(f"invalid coverage identifier: {value!r}")
    return value


def artifact(path, locator):
    p = Path(path)
    if not p.is_absolute():
        p = core.ROOT / p
    p = p.resolve()
    try:
        relative = str(p.relative_to(core.ROOT))
    except ValueError:
        raise core.PipelineError("coverage evidence must be inside PIPELINE_ROOT")
    if not p.is_file() or not locator.strip():
        raise core.PipelineError(f"missing evidence or precise locator: {relative}")
    return {"path": relative, "sha256": core.sha256_file(p), "locator": locator}


def evidence_bytes(ref):
    if not isinstance(ref, dict) or not all(isinstance(ref.get(k), str) and ref[k].strip()
                                          for k in ("path", "sha256", "locator")):
        raise core.PipelineError("evidence requires path, sha256 and locator")
    p = (core.ROOT / ref["path"]).resolve()
    if not p.is_relative_to(core.ROOT) or Path(ref["path"]).is_absolute():
        raise core.PipelineError(f"evidence path outside research root: {ref['path']}")
    try:
        data = p.read_bytes()
    except OSError:
        raise core.PipelineError(f"missing/unreadable evidence: {ref['path']}")
    if core.sha256_bytes(data) != ref["sha256"]:
        raise core.PipelineError(f"changed evidence: {ref['path']}")
    return data


def evidence_errors(ref):
    try:
        evidence_bytes(ref)
        return []
    except core.PipelineError as e:
        return [str(e)]


def validate(doc):
    """Reject malformed records, while allowing honest incomplete investigation."""
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        raise core.PipelineError("unsupported coverage schema")
    for field in ("scope_id", "jurisdiction"):
        identifier(doc.get(field))
    for field in ("purpose", "scope", "author", "next_action"):
        if not isinstance(doc.get(field), str) or not doc[field].strip():
            raise core.PipelineError(f"scope requires {field}")
    date(doc.get("as_of"))
    for table in ("items", "boundaries", "dependencies", "reviews"):
        rows = doc.get(table)
        if not isinstance(rows, list) or any(not isinstance(r, dict) for r in rows):
            raise core.PipelineError(f"{table} must be a list of objects")
        ids = [r.get("id") for r in rows]
        if any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(ids)) != len(ids):
            raise core.PipelineError(f"{table} requires unique nonempty IDs")
    for item in doc["items"]:
        if item.get("kind") not in {"source", "question"} or item.get("status") not in STATES:
            raise core.PipelineError(f"{item['id']}: invalid kind/status")
        for field in ("title", "author"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise core.PipelineError(f"{item['id']}: missing {field}")
        if not isinstance(item.get("decisions"), list) or not item["decisions"] or any(
                not isinstance(x, str) or not x.strip() for x in item["decisions"]):
            raise core.PipelineError(f"{item['id']}: affected operating decisions required")
        if item["status"] in {"open", "investigating"} and not (
                isinstance(item.get("next_action"), str) and item["next_action"].strip()):
            raise core.PipelineError(f"{item['id']}: unfinished work needs next_action")
        if not isinstance(item.get("conclusion", ""), str):
            raise core.PipelineError(f"{item['id']}: conclusion must be text")
        if not isinstance(item.get("evidence", []), list):
            raise core.PipelineError(f"{item['id']}: evidence must be a list")
        if item["kind"] == "source":
            source = item.get("source")
            if not isinstance(source, dict):
                raise core.PipelineError(f"{item['id']}: source metadata required")
            if source.get("selected_version") is not None and not isinstance(source["selected_version"], str):
                raise core.PipelineError(f"{item['id']}: selected_version must identify a version")
            versions = source.get("versions")
            if not isinstance(versions, list) or any(not isinstance(v, dict) for v in versions):
                raise core.PipelineError(f"{item['id']}: malformed source versions")
            ids = [v.get("id") for v in versions]
            if any(not isinstance(x, str) or not x for x in ids) or len(ids) != len(set(ids)):
                raise core.PipelineError(f"{item['id']}: source versions need unique IDs")
    for b in doc["boundaries"]:
        if not isinstance(b.get("source_ids"), list) or any(not isinstance(x, str) for x in b["source_ids"]):
            raise core.PipelineError(f"{b['id']}: source_ids required")
        if len(set(b["source_ids"])) != len(b["source_ids"]):
            raise core.PipelineError(f"{b['id']}: duplicate boundary members")
        if not all(isinstance(b.get(k), str) and b[k].strip() for k in ("description", "author", "next_action")):
            raise core.PipelineError(f"{b['id']}: description, author and next_action required")
    for edge in doc["dependencies"]:
        if edge.get("status") not in {"required", "dismissed"} or not all(
                isinstance(edge.get(k), str) and edge[k].strip() for k in ("from", "to", "reason")):
            raise core.PipelineError(f"{edge['id']}: dependency endpoints, status and reason required")
        if not isinstance(edge.get("evidence", []), list):
            raise core.PipelineError(f"{edge['id']}: dependency evidence must be a list")
    for review in doc["reviews"]:
        if review.get("target_kind") not in {"item", "boundary", "scope"}:
            raise core.PipelineError(f"{review['id']}: invalid review target kind")
        if not isinstance(review.get("target_id"), str):
            raise core.PipelineError(f"{review['id']}: missing review target ID")
    for table in ("imports", "completed_research"):
        rows = doc.get(table, [])
        if not isinstance(rows, list) or any(not isinstance(r, dict) for r in rows):
            raise core.PipelineError(f"{table} must be a list of records")
        keys = [r.get("id") if table == "imports" else r.get("finding", {}).get("path") for r in rows]
        if any(not isinstance(k, str) or not k for k in keys) or len(keys) != len(set(keys)):
            raise core.PipelineError(f"{table} requires stable unique identities")


def target_content(doc, kind, target_id):
    """Bind a work item to the whole reachable dependency graph, including cycles."""
    if kind == "scope":
        if target_id != doc["scope_id"]:
            raise core.PipelineError("unknown review scope")
        return {k: v for k, v in doc.items() if k != "reviews"}
    table = {x["id"]: x for x in doc["boundaries" if kind == "boundary" else "items"]}
    if target_id not in table:
        raise core.PipelineError(f"unknown {kind}: {target_id}")
    if kind == "boundary":
        return table[target_id]
    visited, todo = set(), [target_id]
    while todo:
        key = todo.pop()
        if key in visited:
            continue
        visited.add(key)
        todo.extend(e["to"] for e in doc["dependencies"] if e["from"] == key and e["status"] == "required")
    return {"items": [table.get(k, {"missing": k}) for k in sorted(visited)],
            "dependencies": sorted((e for e in doc["dependencies"] if e["from"] in visited), key=lambda e: e["id"]),
            "as_of": doc["as_of"]}


def review_digest(doc, kind, target_id):
    return digest(target_content(doc, kind, target_id))


def review_errors(doc, kind, target_id, authors, check_evidence=evidence_errors):
    expected = review_digest(doc, kind, target_id)
    candidates = [r for r in doc["reviews"] if r["target_kind"] == kind and r["target_id"] == target_id
                  and r.get("target_sha256") == expected]
    # A later challenge for the same content supersedes an earlier pass.
    if not candidates:
        return ["no independent review bound to current research and dependencies"]
    r = candidates[-1]
    if r.get("result") != "pass" or r.get("unresolved_findings") != []:
        return ["independent review has unresolved findings"]
    if not r.get("reviewer") or r["reviewer"] in authors:
        return ["reviewer must be distinct from the research authors"]
    if not isinstance(r.get("summary"), str) or not r["summary"].strip() or not isinstance(r.get("checked"), list) or not r["checked"] or any(
            not isinstance(x, str) or not x.strip() for x in r["checked"]):
        return ["independent review must describe substantive checks"]
    return check_evidence(r.get("evidence"))


def assess(doc, as_of=None):
    validate(doc)
    when = date(as_of or doc["as_of"])
    items = {i["id"]: i for i in doc["items"]}
    problems = []

    def add(kind, key, message, decisions=None, next_action=None):
        problems.append({"kind": kind, "id": key, "problem": message,
                         "decisions": decisions or [doc["purpose"]],
                         "next_action": next_action or doc["next_action"]})

    if when < date(doc["as_of"]):
        add("scope", doc["scope_id"], "assessment predates research; use an appropriate historical revision")
    if not doc["boundaries"] or not items:
        add("scope", doc["scope_id"], "scope requires enumerated boundaries and investigation items")
    observed, evidence_bodies = {}, {}

    def check_evidence(ref):
        try:
            if isinstance(ref, dict) and ref.get("path") in evidence_bodies:
                if observed[ref["path"]] != ref.get("sha256"):
                    return [f"conflicting evidence versions at one path: {ref['path']}"]
                if not isinstance(ref.get("locator"), str) or not ref["locator"].strip():
                    return ["evidence requires precise locator"]
                return []
            data = evidence_bytes(ref)
            observed[ref["path"]] = ref["sha256"]
            evidence_bodies[ref["path"]] = data
            return []
        except core.PipelineError as e:
            return [str(e)]

    for imported in doc.get("imports", []):
        for err in check_evidence(imported.get("evidence")):
            add("import", imported.get("id", "unknown"), err,
                next_action="Reconcile changed upstream research without overwriting prior judgments.")
    for completed in doc.get("completed_research", []):
        for field in ("finding", "review", "verification"):
            for err in check_evidence(completed.get(field)):
                add("completed_research", completed.get("finding", {}).get("path", "unknown"), err,
                    next_action="Reconcile the changed completed research and its original independent review.")

    covered = set()
    for b in doc["boundaries"]:
        def bad(msg):
            add("boundary", b["id"], msg, next_action=b["next_action"])
        covered.update(b["source_ids"])
        if b.get("enumeration_complete") is not True:
            bad("source enumeration remains open")
        if not b["source_ids"] and not b.get("empty_reason"):
            bad("empty source boundary needs an investigated explanation")
        for key in b["source_ids"]:
            if key not in items or items[key]["kind"] != "source":
                bad(f"enumerated source missing: {key}")
        ref = b.get("inventory")
        errs = check_evidence(ref)
        for err in errs:
            bad(err)
        if not errs:
            try:
                inventory = json.loads(evidence_bodies[ref["path"]])
                if sorted(inventory["source_ids"]) != sorted(b["source_ids"]):
                    bad("boundary differs from retained enumeration membership")
                for authority in inventory.get("evidence", []):
                    for err in check_evidence(authority):
                        bad(err)
                if not inventory.get("evidence") or not inventory.get("method"):
                    bad("enumeration needs authoritative evidence and agent method")
            except (core.PipelineError, KeyError, TypeError, ValueError, AttributeError):
                bad("invalid enumeration artifact")
        selector = b.get("register_selector")
        if selector is not None:
            if not isinstance(selector, dict) or not isinstance(selector.get("units"), list):
                bad("invalid register selector")
            else:
                register_path = core.jdir(doc["jurisdiction"]) / "sections.jsonl"
                if register_path.is_file():
                    register_bytes = register_path.read_bytes()
                    observed[core.rel(register_path)] = core.sha256_bytes(register_bytes)
                    try:
                        register_rows = [json.loads(line) for line in register_bytes.decode().splitlines() if line.strip()]
                    except (ValueError, UnicodeError):
                        raise core.PipelineError("malformed current source register")
                else:
                    register_rows = []
                live = {s["section_id"] for s in register_rows
                        if s.get("instrument") == selector.get("instrument") and s.get("unit") in selector["units"]}
                if live != set(b["source_ids"]):
                    bad("current register membership differs from reviewed boundary")
                selected_rows = [s for s in register_rows if s.get("instrument") == selector.get("instrument")
                                 and s.get("unit") in selector["units"]]
                if len(selected_rows) != len(live):
                    bad("duplicate current register source identity")
                for row in selected_rows:
                    item = items.get(row["section_id"], {})
                    if item.get("register_record_sha256") != digest(row):
                        bad(f"current register source/version differs: {row['section_id']}")
        for err in review_errors(doc, "boundary", b["id"], {b["author"]}, check_evidence):
            bad(err)
    for edge in doc["dependencies"]:
        if edge["from"] not in items or edge["to"] not in items:
            add("dependency", edge["id"], "untracked dependency endpoint", next_action=edge.get("next_action"))
        elif edge["status"] == "required" and items[edge["to"]]["status"] == "excluded":
            add("dependency", edge["id"], "required dependency cannot be satisfied by excluded work",
                items[edge["from"]]["decisions"], edge.get("next_action"))
        if edge["status"] == "dismissed":
            if not edge.get("evidence"):
                add("dependency", edge["id"], "dismissed dependency needs reasoned evidence")
            for ref in edge.get("evidence", []):
                for err in check_evidence(ref):
                    add("dependency", edge["id"], err)
    for key, item in items.items():
        def bad(msg):
            add("item", key, msg, item["decisions"], item.get("next_action"))
        if item["kind"] == "source" and key not in covered:
            bad("source is outside all declared enumeration boundaries")
        if item["status"] not in {"resolved", "excluded"}:
            bad(f"investigation {item['status']}")
        if not item.get("conclusion", "").strip() or not item.get("evidence"):
            bad("substantive conclusion and supporting evidence required")
        for ref in item.get("evidence", []):
            for err in check_evidence(ref):
                bad(err)
        if item["kind"] == "source":
            src = item["source"]
            versions = {v["id"]: v for v in src["versions"]}
            selected = versions.get(src.get("selected_version"))
            if not selected:
                bad("no selected source version")
            else:
                for err in check_evidence(src.get("currentness_evidence")):
                    bad("currentness investigation: " + err)
                for field in ("url", "retrieved_at", "temporal_basis"):
                    if not selected.get(field):
                        bad(f"source version lacks {field}")
                for err in check_evidence(selected.get("evidence")):
                    bad(err)
                try:
                    applies = date(src.get("applies_on"))
                    start, end = selected.get("effective_from"), selected.get("effective_to")
                    if (start and applies < date(start)) or (end and applies >= date(end)):
                        bad("selected version does not apply on the declared legal date")
                    if date(src.get("checked_through")) < when:
                        bad("source currentness not investigated through scope date")
                    if date(src.get("recheck_on")) <= when:
                        bad("source currentness recheck due")
                except core.PipelineError as e:
                    bad(str(e))
        content = target_content(doc, "item", key)
        authors = {i.get("author") for i in content["items"]}
        for err in review_errors(doc, "item", key, authors, check_evidence):
            bad(err)
    authors = {doc["author"]} | {i["author"] for i in items.values()} | {b["author"] for b in doc["boundaries"]}
    for err in review_errors(doc, "scope", doc["scope_id"], authors, check_evidence):
        add("scope", doc["scope_id"], err)
    for path, sha in observed.items():
        p = core.ROOT / path
        if not p.is_file() or core.sha256_file(p) != sha:
            add("scope", doc["scope_id"], f"external evidence changed during assessment: {path}; rerun against stable files")
    return {"scope_id": doc["scope_id"], "jurisdiction": doc["jurisdiction"], "as_of": str(when),
            "complete": not problems, "items": len(items), "boundaries": len(doc["boundaries"]),
            "dependencies": len(doc["dependencies"]), "problems": problems, "observed_artifacts": observed,
            "meaning": "Evidence-bound recorded research coverage; not independent proof of legal truth or undiscovered-source absence."}


def database(code):
    identifier(code)
    core.profile(code)
    return core.jdir(code) / "coverage.sqlite3"


@contextlib.contextmanager
def connect(code):
    db = sqlite3.connect(database(code), timeout=10)
    db.execute("PRAGMA synchronous=FULL")
    db.execute("CREATE TABLE IF NOT EXISTS revisions (scope TEXT, revision INTEGER, parent TEXT, sha256 TEXT, payload TEXT, saved_at TEXT, PRIMARY KEY(scope, revision))")
    try:
        with db:
            yield db
    except sqlite3.Error as e:
        raise core.PipelineError(f"coverage database error: {e}") from e
    finally:
        db.close()


def load(code, scope_id, revision=None):
    identifier(scope_id)
    if not database(code).exists():
        raise core.PipelineError("no coverage records; initialize a scope")
    with connect(code) as db:
        rows = db.execute("SELECT revision,parent,sha256,payload FROM revisions WHERE scope=? ORDER BY revision", (scope_id,)).fetchall()
    if not rows:
        raise core.PipelineError(f"unknown coverage scope: {scope_id}")
    previous = None
    expected_number = 1
    chosen = None
    for number, parent, sha, payload in rows:
        try:
            doc = json.loads(payload)
        except ValueError:
            raise core.PipelineError("corrupt coverage revision")
        if number != expected_number or parent != previous or digest(doc) != sha:
            raise core.PipelineError("coverage revision history failed integrity check")
        previous = sha
        expected_number += 1
        if revision is None or number == revision:
            chosen = (number, doc)
    if chosen is None:
        raise core.PipelineError(f"missing coverage revision {revision}")
    return chosen


def save(code, doc, expected_revision):
    validate(doc)
    if type(expected_revision) is not int or expected_revision < 0:
        raise core.PipelineError("expected_revision must be a nonnegative integer")
    if doc["jurisdiction"] != code:
        raise core.PipelineError("coverage jurisdiction mismatch")
    with connect(code) as db:
        db.execute("BEGIN IMMEDIATE")
        previous = None
        for expected_number, (number, parent, sha, payload) in enumerate(db.execute(
                "SELECT revision,parent,sha256,payload FROM revisions WHERE scope=? ORDER BY revision", (doc["scope_id"],)), 1):
            try:
                historical = json.loads(payload)
            except ValueError:
                raise core.PipelineError("corrupt coverage revision")
            if number != expected_number or parent != previous or digest(historical) != sha:
                raise core.PipelineError("coverage revision history failed integrity check")
            previous = sha
        row = db.execute("SELECT revision,sha256,payload FROM revisions WHERE scope=? ORDER BY revision DESC LIMIT 1", (doc["scope_id"],)).fetchone()
        current = row[0] if row else 0
        if current != expected_revision:
            raise core.PipelineError(f"stale update: expected revision {expected_revision}, current {current}; reload and reconcile")
        if row:
            old = json.loads(row[2])
            if digest(old) != row[1]:
                raise core.PipelineError("corrupt current revision")
            if doc["reviews"][:len(old["reviews"])] != old["reviews"]:
                raise core.PipelineError("reviews are immutable and ordered; append new reviews after the existing prefix")
            for table in ("imports", "completed_research"):
                key = (lambda x: x["id"]) if table == "imports" else (lambda x: x["finding"]["path"])
                before = {key(x): x for x in old.get(table, [])}
                after = {key(x): x for x in doc.get(table, [])}
                if before.keys() - after.keys():
                    raise core.PipelineError(f"cannot remove {table}; retain upstream research links")
                if any(after[k] != v and not after[k].get("reconciliation_reason") for k, v in before.items()):
                    raise core.PipelineError(f"changed {table} requires explicit reconciliation_reason")
            for table in ("items", "boundaries", "dependencies", "reviews"):
                prior = {x["id"]: x for x in old[table]}
                present = {x["id"]: x for x in doc[table]}
                if prior.keys() - present.keys():
                    raise core.PipelineError(f"cannot remove {table}; retain explicit exclusions/challenges and history")
                if table == "reviews" and any(present[k] != v for k, v in prior.items()):
                    raise core.PipelineError("reviews are immutable; append a new review")
            for table in ("items", "dependencies"):
                present = {x["id"]: x for x in doc[table]}
                fields = ("kind",) if table == "items" else ("from", "to")
                for prior in old[table]:
                    if any(present[prior["id"]].get(k) != prior.get(k) for k in fields):
                        raise core.PipelineError("stable work identities cannot change kind or dependency endpoints")
            old_boundaries = {b["id"]: b for b in old["boundaries"]}
            shrink = any(set(old_boundaries[b["id"]]["source_ids"]) - set(b["source_ids"])
                         or old_boundaries[b["id"]].get("register_selector") != b.get("register_selector")
                         for b in doc["boundaries"] if b["id"] in old_boundaries)
            if (shrink or old["scope"] != doc["scope"] or old["purpose"] != doc["purpose"]) and not doc.get("scope_change_reason"):
                raise core.PipelineError("scope changes require an explicit scope_change_reason and fresh review")
            for old_item in old["items"]:
                if old_item["kind"] != "source":
                    continue
                new_item = next(i for i in doc["items"] if i["id"] == old_item["id"])
                versions = {v["id"]: v for v in new_item.get("source", {}).get("versions", [])}
                if any(versions.get(v["id"]) != v for v in old_item["source"]["versions"]):
                    raise core.PipelineError("source versions are immutable; append a new version")
        sha = digest(doc)
        if row and row[1] == sha:
            return current
        db.execute("INSERT INTO revisions VALUES (?,?,?,?,?,?)", (doc["scope_id"], current + 1,
                   row[1] if row else None, sha, json.dumps(doc, ensure_ascii=False, allow_nan=False), core.now()))
    return current + 1


def seed(code, scope_id, purpose, author):
    """Import registry evidence without importing its routes as research acceptance."""
    core.profile(code)
    doc = {"schema": SCHEMA, "scope_id": identifier(scope_id), "jurisdiction": code,
           "purpose": purpose, "scope": "All currently registered source units; broader discovery remains open.",
           "author": author, "as_of": core.today(), "next_action": "Investigate and independently review source coverage and consequential legal questions.",
           "items": [], "boundaries": [], "dependencies": [], "reviews": []}
    groups = {}
    doc["imports"] = []
    register_rows = []
    instrument_doc = None
    for name in ("sections.jsonl", "instruments.json"):
        path = core.jdir(code) / name
        if not path.is_file():
            continue
        raw = path.read_bytes()
        doc["imports"].append({"id": "register-" + name, "evidence": {
            "path": core.rel(path), "sha256": core.sha256_bytes(raw),
            "locator": "complete registered inventory at scope initialization"}})
        if name == "sections.jsonl":
            try:
                register_rows = [json.loads(line) for line in raw.decode().splitlines() if line.strip()]
            except (ValueError, UnicodeError):
                raise core.PipelineError("malformed source register")
        else:
            try:
                instrument_doc = json.loads(raw)
            except ValueError:
                raise core.PipelineError("malformed instrument register")
    for sec in register_rows:
        sid = sec["section_id"]
        groups.setdefault((sec["instrument"], sec["unit"]), []).append(sid)
        item = {"id": sid, "kind": "source", "title": sec.get("heading") or sid, "status": "open",
                "author": author, "decisions": [purpose], "next_action": "Read source, establish applicable version and investigate its operating consequences and dependencies.",
                "evidence": [], "conclusion": "", "register_section": sid,
                "register_record_sha256": digest(sec),
                "source": {"selected_version": None, "versions": []}}
        path = sec.get("text_file")
        if path and (core.ROOT / path).is_file():
            ref = artifact(path, "complete saved section; registration is not substantive review")
            item["source"]["versions"] = [{"id": ref["sha256"], "evidence": ref,
                "url": core.source_url_of(core.ROOT / path), "retrieved_at": "see retained source header",
                "effective_from": None, "effective_to": None, "temporal_basis": "Not yet investigated"}]
            item["source"]["selected_version"] = ref["sha256"]
        doc["items"].append(item)
    if instrument_doc is not None:
        for inst in instrument_doc.get("instruments", []):
            for unit in inst.get("units_in_scope", []):
                groups.setdefault((inst["id"], unit["unit"]), [])
        leads = [("source-discovery", "Establish the complete applicable source universe", {
            "discovery_status": instrument_doc.get("discovery_status"),
            "functions_without_instrument": instrument_doc.get("functions_without_instrument", [])})]
        for field in ("pending_source_families", "non_code_sources"):
            for value in instrument_doc.get(field, []):
                leads.append((field + ":" + digest(value)[:16], str(value), value))
        for field in ("section_gaps", "instrument_gaps"):
            for value in instrument_doc.get("fetch_gaps", {}).get(field, []):
                leads.append((field + ":" + digest(value)[:16], str(value), value))
        instrument_ref = next(i["evidence"] for i in doc["imports"] if i["id"] == "register-instruments.json")
        for key, title, observation in leads:
            doc["items"].append({"id": key, "kind": "question", "title": title, "author": author,
                "status": "open", "decisions": [purpose], "conclusion": "", "evidence": [instrument_ref],
                "next_action": "Investigate this recorded source-discovery lead, reconcile the applicable universe and record a supported conclusion with independent review.",
                "observation": observation})
    for (inst, unit), ids in groups.items():
        doc["boundaries"].append({"id": f"{inst}/{unit}", "description": f"Registered {inst} {unit}; authoritative enumeration still required",
            "author": author, "source_ids": ids, "enumeration_complete": False,
            "next_action": "Reconcile full authoritative enumeration and retained exclusions; independently review source boundary.",
            "register_selector": {"instrument": inst, "units": [unit]}})
    return doc


def import_followup(doc, path, author):
    """Retain prepared-task observations and all broad leads as unfinished work.

    This adapter consumes the existing fresh.followup.json contract. It preserves
    occurrence, preparation identity, model observation, targets and agent notes.
    No inference result, including NO, promotes an item to resolved/excluded.
    """
    result = copy_document(doc)
    ref = artifact(path, "complete prepared-task follow-up; rows and next_dependencies")
    raw = (core.ROOT / ref["path"]).read_bytes()
    if core.sha256_bytes(raw) != ref["sha256"]:
        raise core.PipelineError("follow-up changed during import")
    try:
        data = json.loads(raw)
    except ValueError:
        raise core.PipelineError("invalid prepared follow-up JSON")
    if not isinstance(data, dict) or not isinstance(data.get("rows"), list) or not isinstance(data.get("next_dependencies"), list):
        raise core.PipelineError("prepared follow-up requires rows and next_dependencies")
    import_id = "followup-" + digest(ref["path"])[:16]
    imports = result.setdefault("imports", [])
    if any(i["id"] == import_id for i in imports):
        raise core.PipelineError("follow-up already imported; reconcile changed evidence explicitly")
    imports.append({"id": import_id, "evidence": ref, "source_scope": data.get("scope")})
    known = {i["id"] for i in result["items"]}
    for index, row in enumerate(data["rows"] + data["next_dependencies"]):
        key = import_id + ":" + (row.get("case_id") or f"broad-{index}")
        if key in known:
            raise core.PipelineError("duplicate prepared follow-up identity")
        known.add(key)
        result["items"].append({"id": key, "kind": "question", "title": row.get("expression") or ", ".join(row.get("targets", [])),
            "author": author, "status": "open", "decisions": [result["purpose"]],
            "next_action": row.get("followup") or row.get("cause") or "Investigate the prepared research lead.",
            "conclusion": "", "evidence": [ref], "observation": row})
        for target in row.get("targets", []):
            # Preserve unresolved target strings without guessing a legal identity.
            target_id = import_id + ":target:" + digest(target)[:16]
            if target_id not in known:
                known.add(target_id)
                result["items"].append({"id": target_id, "kind": "question", "title": target,
                    "author": author, "status": "open", "decisions": [result["purpose"]],
                    "next_action": "Resolve the target's precise source/version, retrieve and investigate its effect on the originating question.",
                    "conclusion": "", "evidence": [ref], "unresolved_target": target})
            result["dependencies"].append({"id": key + "->" + target_id, "from": key, "to": target_id,
                "status": "required", "reason": row.get("followup") or row.get("cause") or "Agent-identified target requires investigation"})
    validate(result)
    return result


def link_completed_research(doc, verification_path):
    """Retain exact previously accepted findings, without accepting a larger scope.

    The Goal 3 verification contract supplies finding/review pairs. These receipts
    preserve that completed work as reusable evidence; the current investigation
    still determines which conclusions apply and whether its dependencies are closed.
    """
    result = copy_document(doc)
    ref = artifact(verification_path, "review_bindings: exact accepted finding/review identities")
    data = json.loads(evidence_bytes(ref))
    parent = (core.ROOT / ref["path"]).parent
    bindings = data.get("review_bindings")
    if not isinstance(bindings, list) or not bindings:
        raise core.PipelineError("research verification has no reviewed findings")
    links = result.setdefault("completed_research", [])
    known = {x["finding"]["path"] for x in links}
    for row in bindings:
        finding = artifact(parent / row["finding"], "complete accepted finding; scope retained in report")
        review = artifact(parent / row["review"], "independent acceptance of the exact finding hash")
        if finding["sha256"] != row["sha256"] or row.get("review_contains_current_hash") is not True:
            raise core.PipelineError("completed finding no longer matches its recorded review")
        if finding["sha256"] not in (core.ROOT / review["path"]).read_text():
            raise core.PipelineError("independent review does not bind the finding")
        if finding["path"] in known:
            raise core.PipelineError("finding already linked; reconcile changes explicitly")
        known.add(finding["path"])
        links.append({"finding": finding, "review": review, "verification": ref,
                      "meaning": "Prior accepted research with its original scope; not automatic closure of this scope."})
    return result


def copy_document(doc):
    return json.loads(json.dumps(doc, ensure_ascii=False, allow_nan=False))


def main(args):
    action, code, scope = args.action, args.code, args.scope
    if action == "seed":
        doc = seed(code, scope, args.purpose, args.author)
        revision = save(code, doc, 0)
        print(f"{scope}: revision {revision}; {len(doc['items'])} sources, none automatically accepted")
    elif action == "save":
        doc = core.read_json(args.file)
        if doc.get("scope_id") != scope:
            raise core.PipelineError("scope/file mismatch")
        print(f"{scope}: revision {save(code, doc, args.expected_revision)}")
    elif action in ("followup", "link-research"):
        revision, doc = load(code, scope)
        if revision != args.expected_revision:
            raise core.PipelineError("stale follow-up import; reload current revision")
        updated = (import_followup(doc, args.file, args.author) if action == "followup"
                   else link_completed_research(doc, args.file))
        print(f"{scope}: revision {save(code, updated, revision)}; upstream evidence linked without automatic scope closure")
    else:
        revision, doc = load(code, scope, args.revision)
        if action == "export":
            print(json.dumps({"revision": revision, "document": doc}, indent=2, ensure_ascii=False))
        elif action == "digest":
            print(review_digest(doc, args.kind, args.target))
        else:
            report = assess(doc, args.as_of or core.today())
            report["revision"] = revision
            print(json.dumps(report, indent=2, ensure_ascii=False))
            return 0 if action == "status" or report["complete"] else 1
    return 0


def jurisdiction_summary(code):
    """All declared scopes, including open broader work; no scope means untracked."""
    if not database(code).exists():
        return {"complete": False, "message": "research coverage untracked", "scopes": []}
    with connect(code) as db:
        scopes = [r[0] for r in db.execute("SELECT DISTINCT scope FROM revisions ORDER BY scope")]
    reports = []
    for scope in scopes:
        revision, doc = load(code, scope)
        report = assess(doc, core.today())
        reports.append({"scope_id": scope, "revision": revision, "complete": report["complete"],
                        "problems": len(report["problems"])})
    return {"complete": bool(reports) and all(r["complete"] for r in reports),
            "message": "declared research scopes only; broader discovery must be explicitly tracked",
            "scopes": reports}
