"""Shared paths, file helpers and the layer model.

Every path the pipeline records (text_file, source_file) is relative to ROOT, the research/legal-engine folder.
Set PIPELINE_ROOT to run the package against another copy of that folder (tests and scratch runs do this).

A jurisdiction is a folder jurisdictions/<CODE>/ with a profile.json. Its profile names its direct parents;
layers(code) is the jurisdiction followed by every ancestor (NYC -> NY -> US). The family of a jurisdiction is its
layers plus every descendant, which is where a rule id named in its files may legally live.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import pathlib
import re
import shutil

PKG = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(os.environ.get("PIPELINE_ROOT") or PKG.parent).resolve()
JUR = ROOT / "jurisdictions"
VENV_PYTHON = PKG.parent / ".venv" / "bin" / "python"

DETERMINACY = {"RULE", "STANDARD", "MIXED"}
DECISIONS = {"stated", "partial", "new_rule", "no_decision", "excluded_regime"}
DECIDING = {"stated", "partial", "new_rule"}
# Hedging and weight words banned from rules, reasons and walks. The first line is stage_a_check.py's list; the
# second adds the words the skill and the reviewer checker also ban.
HEDGE = re.compile(
    r"\b(unclear|unsettled|open question|working position|conservative position|arguabl\w*|"
    r"consult counsel|needs counsel|not yet known|bounded unknown|undetermined|uncertain whether|"
    r"may or may not|it is possible that|"
    r"in practice|typically|persuasive only|weight label|weight:\s*\w+)\b", re.I)
# stage_a_check.py's list alone (rules --legacy-hedge compares with the legacy checker; the skill's list is HEDGE).
HEDGE_LEGACY = re.compile(
    r"\b(unclear|unsettled|open question|working position|conservative position|arguabl\w*|"
    r"consult counsel|needs counsel|not yet known|bounded unknown|undetermined|uncertain whether|"
    r"may or may not|it is possible that)\b", re.I)
RULE_REQUIRED = ["id", "jurisdiction", "instrument", "provision", "effective_from", "effective_to", "actor",
                 "modality", "condition", "effect", "determinacy", "judgment_terms", "dependencies", "source_file",
                 "source_url", "quote"]


def set_root(path):
    """Point the package at another legal-engine folder (tests and scratch runs). Modules read core.ROOT and
    core.JUR at call time, so this takes effect everywhere."""
    global ROOT, JUR
    ROOT = pathlib.Path(path).resolve()
    JUR = ROOT / "jurisdictions"
    _verbatim_cache.clear()


class PipelineError(Exception):
    """A failure the command reports and exits non-zero on."""


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def today():
    return datetime.date.today().isoformat()


def now():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()


# ---------- file helpers ----------

def read_json(p, default=None):
    p = pathlib.Path(p)
    if not p.exists():
        if default is not None:
            return default
        raise PipelineError(f"missing file {rel(p)}")
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError as e:
        raise PipelineError(f"{rel(p)} is not valid JSON: {e}")


def dumps(obj):
    return json.dumps(obj, indent=1, ensure_ascii=False) + "\n"


def write_json(p, obj):
    """Write only when the content changes; return True when the file changed."""
    p = pathlib.Path(p)
    s = dumps(obj)
    if p.exists() and p.read_text() == s:
        return False
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s)
    return True


def read_jsonl(p):
    p = pathlib.Path(p)
    if not p.exists():
        return []
    out = []
    for i, line in enumerate(p.read_text().splitlines(), 1):
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise PipelineError(f"{rel(p)} line {i} is not valid JSON: {e}")
    return out


def write_jsonl(p, rows):
    p = pathlib.Path(p)
    s = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    if p.exists() and p.read_text() == s:
        return False
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s)
    return True


def rel(p):
    p = pathlib.Path(p).resolve()
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    return sha256_bytes(pathlib.Path(p).read_bytes())


def body_of(text):
    """Text below the SOURCE/RETRIEVED header (the header ends at the first blank line)."""
    return text.split("\n\n", 1)[1] if "\n\n" in text else text


def text_hash(text):
    """Hash of a saved text's body, whitespace-normalized, so a new RETRIEVED date or rewrapping is no change."""
    return sha256_bytes(norm(body_of(text)).encode())


def header(source_url, route, retrieved=None, extra=None):
    lines = [f"SOURCE: {source_url}"]
    for k, v in (extra or {}).items():
        lines.append(f"{k.upper()}: {v}")
    lines.append(f"RETRIEVED: {retrieved or today()} via {route}")
    return "\n".join(lines) + "\n\n"


def has_header(text):
    head = text[:800]
    return head.startswith("SOURCE:") and "RETRIEVED:" in head


def source_url_of(path):
    head = pathlib.Path(path).read_text(errors="ignore")[:800]
    m = re.search(r"SOURCE:\s*(\S+)", head) or re.search(r"(https?://\S+)", head)
    return m.group(1) if m else ""


_verbatim_cache = {}


def verbatim(src, quote):
    """None if the quote is verbatim (whitespace-normalized) in ROOT/src, else the error."""
    f = ROOT / (src or "")
    if not src or not f.is_file():
        return f"source file missing {src}"
    key = (str(f), f.stat().st_mtime_ns)
    if key not in _verbatim_cache:
        _verbatim_cache[key] = norm(f.read_text(errors="ignore"))
    return None if quote and norm(quote) in _verbatim_cache[key] else f"quote not verbatim in {src}"


def must(src, phrase):
    """Assert a figure or phrase stated beyond a rule's quote is present in its saved source."""
    e = verbatim(src, phrase)
    if e:
        raise PipelineError(f"source check failed: '{phrase[:80]}' ({e})")


def backup(path, backups_dir):
    """Copy a file into backups_dir named by its content hash; a backup of identical content is not taken twice."""
    path = pathlib.Path(path)
    if not path.exists():
        return None
    h = sha256_file(path)[:16]
    dst = pathlib.Path(backups_dir) / f"{path.stem}.{h}{path.suffix}"
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dst)
    return dst


# ---------- jurisdictions and layers ----------

def jdir(code):
    return JUR / code


def exists(code):
    return (jdir(code) / "profile.json").exists()


def codes():
    if not JUR.exists():
        return []
    return sorted(p.name for p in JUR.iterdir() if (p / "profile.json").exists())


def profile(code):
    if not exists(code):
        raise PipelineError(f"no jurisdiction {code} (expected {rel(jdir(code) / 'profile.json')}; run init)")
    return read_json(jdir(code) / "profile.json")


def parents(code):
    return list(profile(code).get("parents") or [])


def ancestors(code):
    out, todo = [], parents(code)
    while todo:
        c = todo.pop(0)
        if c in out or c == code:
            continue
        out.append(c)
        if exists(c):
            todo.extend(parents(c))
    return out


def layers(code):
    return [code] + ancestors(code)


def descendants(code):
    return [c for c in codes() if c != code and code in ancestors(c)]


def family(code):
    return layers(code) + [c for c in descendants(code) if c not in layers(code)]


def rules_file(code):
    return jdir(code) / "rules.json"


def load_rules(code):
    return read_json(rules_file(code), {"jurisdiction": code, "atoms": [], "external_references": {}})


def rule_index(codes_):
    """{rule id: rule} over the given jurisdictions that exist."""
    idx = {}
    for c in codes_:
        if exists(c):
            for a in load_rules(c).get("atoms", []):
                idx[a["id"]] = a
    return idx


def known_ids(codes_):
    """Rule ids plus declared external references over the given jurisdictions."""
    ids = set()
    for c in codes_:
        if exists(c):
            d = load_rules(c)
            ids |= {a["id"] for a in d.get("atoms", [])} | set(d.get("external_references", {}))
    return ids


def sections(code):
    return read_jsonl(jdir(code) / "sections.jsonl")


def triage(code):
    return read_jsonl(jdir(code) / "triage.jsonl")


def instruments(code):
    return read_json(jdir(code) / "instruments.json", {"instruments": []})


def chain_map():
    return read_json(PKG / "chain_map.json")


def routing():
    return read_json(PKG / "routing.json")


def questions():
    return read_json(PKG / "jev_questions.json")


def code_of(rule_or_section_id):
    return rule_or_section_id.split(":", 1)[0]
