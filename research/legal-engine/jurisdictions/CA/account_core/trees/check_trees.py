#!/usr/bin/env python3
"""Check the California account-core legal trees.

Exit status 1 if any tree breaks the format in design/legal-trees.md (with the additions listed in REVIEW.md),
if any quote is not verbatim in the saved text its citation names, or if a quote cited to a subdivision is not
inside that subdivision. Verbatim means identical after collapsing runs of whitespace, which is the convention of
pipeline/core.py: the saved captures are wrapped mechanically, so line breaks are not part of the text.

Usage: python3 check_trees.py [tree.json ...]     (no arguments: every *.json in this folder except JEV_CHECK.json)
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
CA = HERE.parent.parent                       # research/legal-engine/jurisdictions/CA
LE = CA.parent.parent                         # research/legal-engine
SECTIONS = CA / "sections.jsonl"

CODES = {"Civ": "CA_CIV", "CCP": "CA_CCP", "Gov": "CA_GOV", "PUC": "CA_PUC"}
CODE_CITE = re.compile(r"^(Civ|CCP|Gov|PUC) (\d+(?:\.\d+)*[a-z]?)((?:\([0-9A-Za-z]+\))*)$")

# Named sources other than code sections: citation prefix -> (file, class).
# Classes: statute (official leginfo code text), bill (official leginfo bill text), guidance (official agency
# guidance, not law), mirror (case text from an unofficial mirror), court (official court text, e.g. GovInfo),
# leghist (official legislative committee analysis, not law).
NAMED = [
    ("AB 2801", LE / "j1/lanes/enactments/sources/202320240AB2801.txt", "bill"),
    ("Granberry v. Islay Investments", CA / "account_core/sources/CASE_Granberry_v_Islay_1995_mirror.txt", "mirror"),
    ("DRE, California Tenants", CA / "account_core/sources/DRE_2026_Landlord_Tenant_Guide.txt", "guidance"),
    # Captured by the authorities agent (account_core/authorities/, its ownership); cited only once committed.
    ("Brooks v. Greystar", CA / "account_core/authorities/FED_Brooks_v_Greystar_SDCal_2025-08-07_ECF56.txt", "court"),
    ("Senate Judiciary Committee, analysis of AB 2801",
     CA / "account_core/authorities/LEGHIST_AB2801_SJUD_analysis_2024-06-11.txt", "leghist"),
]

LAYERS = {"US", "CA", "CA-OC", "CA-HB"}
KINDS = {"determinate", "semantic", "discretionary"}
QTYPES = {"yesno", "choice", "score"}
EFFECT_KINDS = {"permission", "prohibition", "duty"}
UNITS = {"calendarDays", "cents", "hours", "date", "multiplier", "months"}
FUNCS = {"min", "max", "sum", "round", "days", "count", "len", "exists", "holds", "amount", "date", "abs",
         "any", "all", "earliest", "latest", "hours"}
WORDS = {"and", "or", "not", "in", "true", "false", "null", "if", "else"}
DP = re.compile(r"^(DP\d+(\.\d+)?|PW\d+(\.\d+)?)$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NUMBER_TEXT = {14: ["two weeks", "14"], 2: ["twice", "two"], 48: ["48"], 21: ["21"], 60: ["60"], 5: ["five"], 7: ["seven"],
               30: ["30"], 15: ["15"], 18: ["18"]}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


# ---------------------------------------------------------------- saved texts and subdivisions

_official = None


def official_files():
    global _official
    if _official is None:
        _official = set()
        for line in SECTIONS.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                if "leginfo.legislature.ca.gov" in (row.get("source_url") or ""):
                    _official.add((LE / row["text_file"]).resolve())
    return _official


def resolve(citation: str):
    """(file, class, section, path) for a citation, or raise ValueError."""
    m = CODE_CITE.match(citation)
    if m:
        code, sec, subs = m.groups()
        f = (CA / "texts" / CODES[code] / f"{sec}.txt").resolve()
        if not f.is_file():
            raise ValueError(f"no saved text for {citation} ({f.relative_to(LE)})")
        if f not in official_files():
            raise ValueError(f"{citation}: saved text is not an indexed leginfo capture")
        return f, "statute", sec, tuple(re.findall(r"\(([0-9A-Za-z]+)\)", subs))
    for prefix, f, cls in NAMED:
        if citation.startswith(prefix):
            if not f.is_file():
                raise ValueError(f"no saved text for {citation}")
            return f.resolve(), cls, None, ()
    raise ValueError(f"unrecognized citation {citation!r}")


ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii"]
CHILD = {None: ("lower", "a"), "lower": ("digit", "1"), "digit": ("upper", "A"), "upper": ("rlower", "i"),
         "rlower": ("rupper", "I")}


def nxt(kind, label):
    if kind == "digit":
        return str(int(label) + 1)
    if kind in ("lower", "upper"):
        return chr(ord(label) + 1)
    if kind == "rlower":
        return ROMAN[ROMAN.index(label) + 1] if label in ROMAN[:-1] else None
    if kind == "rupper":
        up = [r.upper() for r in ROMAN]
        return up[up.index(label) + 1] if label in up[:-1] else None


_spans = {}


def section_lines(f: pathlib.Path, sec: str):
    """[(path, line)] for the body of a saved section, path being the subdivision labels in force."""
    if f in _spans:
        return _spans[f]
    lines = f.read_text().splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == f"{sec}." or l.strip().startswith(f"{sec}.\t")
                     or re.match(rf"^{re.escape(sec)}\.\s*$", l.strip()))
    except StopIteration:
        start = 0
    stack: list[tuple[str, str]] = []
    out = []
    for raw in lines[start + 1:]:
        line = raw.strip()
        rest = line
        numbered = re.match(r"^(\d+)\.\s", rest)
        if numbered and (not stack or (len(stack) == 1 and stack[0][0] == "digit")):
            lab = numbered.group(1)
            if (not stack and lab == "1") or (stack and nxt("digit", stack[0][1]) == lab):
                stack = [("digit", lab)]
        while True:
            m = re.match(r"^\(([0-9A-Za-z]{1,5})\)\s*", rest)
            if not m:
                break
            lab = m.group(1)
            placed = False
            parent = stack[-1][0] if stack else None
            ck, cl = CHILD.get(parent, (None, None))
            if cl == lab:
                stack.append((ck, lab))
                placed = True
            else:
                for depth in range(len(stack) - 1, -1, -1):
                    kind, cur = stack[depth]
                    if nxt(kind, cur) == lab:
                        stack = stack[:depth] + [(kind, lab)]
                        placed = True
                        break
            if not placed:
                break
            rest = rest[m.end():]
        out.append((tuple(l for _, l in stack), raw))
    _spans[f] = out
    return out


def span_text(f, sec, path):
    if not path:
        return None
    rows = [l for p, l in section_lines(f, sec) if p[:len(path)] == path]
    return "\n".join(rows) if rows else ""


def check_quote(citation, quote, allowed, where, errors):
    if not isinstance(quote, str) or len(norm(quote)) < 12:
        errors.append(f"{where}: quote missing or too short")
        return
    try:
        f, cls, sec, path = resolve(citation)
    except ValueError as exc:
        errors.append(f"{where}: {exc}")
        return
    if cls not in allowed:
        errors.append(f"{where}: {citation} is a {cls} source; only {sorted(allowed)} allowed here")
    body = norm(f.read_text(errors="ignore"))
    q = norm(quote)
    if q not in body:
        errors.append(f"{where}: quote not verbatim in {f.relative_to(LE)}: {q[:90]!r}")
        return
    if path:
        span = span_text(f, sec, path)
        if span == "":
            errors.append(f"{where}: subdivision {citation} not found in the saved text")
        elif q not in norm(span):
            errors.append(f"{where}: quote is in {sec} but not inside {citation}")


# ---------------------------------------------------------------- expressions

NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*")
STRING = re.compile(r"\"[^\"]*\"|'[^']*'")
REF = re.compile(r"\b(holds|amount)\(\s*\"([^\"]+)\"(?:\s*,\s*\"([^\"]+)\")?")


def check_expr(expr, tree, where, errors, refs):
    if not isinstance(expr, str) or not expr.strip():
        errors.append(f"{where}: empty expression")
        return
    for fn, tid, eid in REF.findall(expr):
        refs.append((where, fn, tid, eid))
    bare = STRING.sub(" ", expr)
    inputs = tree.get("inputs", [])
    params = {p.get("id") for p in tree.get("parameters", [])}
    for m in NAME.finditer(bare):
        name = m.group(0)
        if m.start() > 0 and (bare[m.start() - 1].isdigit() or bare[m.start() - 1] == "."):
            continue
        is_call = bare[m.end():].lstrip().startswith("(")
        if name in WORDS or (is_call and name in FUNCS):
            continue
        if name.startswith("parameters."):
            if name.split(".", 2)[1] not in params:
                errors.append(f"{where}: unknown parameter {name}")
            continue
        if any(name == i or name.startswith(i + ".") or i.startswith(name + ".") for i in inputs):
            continue
        errors.append(f"{where}: {name!r} is not a declared input, parameter or function")


# ---------------------------------------------------------------- trees

def walk(node, where, tree, errors, leaves, refs, contested_refs):
    if not isinstance(node, dict) or "type" not in node:
        errors.append(f"{where}: node without type")
        return
    t = node["type"]
    if t in ("all", "any"):
        kids = node.get("children")
        if not isinstance(kids, list) or len(kids) < 2:
            errors.append(f"{where}: {t} needs at least two children")
            kids = kids or []
        extra = set(node) - {"type", "children"}
        if extra:
            errors.append(f"{where}: unexpected fields {sorted(extra)}")
        for i, k in enumerate(kids):
            walk(k, f"{where}/{t}[{i}]", tree, errors, leaves, refs, contested_refs)
    elif t == "not":
        if set(node) - {"type", "child"}:
            errors.append(f"{where}: unexpected fields on not")
        walk(node.get("child"), f"{where}/not", tree, errors, leaves, refs, contested_refs)
    elif t == "unless":
        if set(node) - {"type", "rule", "exception"}:
            errors.append(f"{where}: unexpected fields on unless")
        walk(node.get("rule"), f"{where}/unless.rule", tree, errors, leaves, refs, contested_refs)
        walk(node.get("exception"), f"{where}/unless.exception", tree, errors, leaves, refs, contested_refs)
    elif t == "condition":
        lid = node.get("id")
        w = f"{where}:{lid}"
        if not isinstance(lid, str) or not re.match(r"^[a-z0-9][a-z0-9-]*$", lid or ""):
            errors.append(f"{w}: leaf id must be lower-case kebab")
        if lid in leaves:
            errors.append(f"{w}: duplicate leaf id")
        leaves[lid] = node
        st = node.get("statement")
        if not isinstance(st, str) or not st.strip().endswith(".") or len(st) > 400:
            errors.append(f"{w}: statement must be one plain sentence ending in a period")
        src = node.get("source") or {}
        if set(src) != {"citation", "quote"}:
            errors.append(f"{w}: source must be {{citation, quote}}")
        check_quote(src.get("citation", ""), src.get("quote"), {"statute"}, w, errors)
        kind = node.get("kind")
        allowed = {"type", "id", "statement", "source", "kind", "contested"}
        if kind not in KINDS:
            errors.append(f"{w}: kind must be one of {sorted(KINDS)}")
        if kind == "determinate":
            allowed.add("compute")
            check_expr(node.get("compute"), tree, f"{w}.compute", errors, refs)
        elif kind == "semantic":
            allowed.add("question")
            q = node.get("question") or {}
            if q.get("type") not in QTYPES:
                errors.append(f"{w}: question.type must be one of {sorted(QTYPES)}")
            if not isinstance(q.get("wording"), str) or not q["wording"].strip().endswith("?"):
                errors.append(f"{w}: question.wording must be a question ending in '?'")
            if q.get("type") == "choice" and not (isinstance(q.get("options"), list) and len(q["options"]) >= 2):
                errors.append(f"{w}: choice question needs options")
            ins = q.get("inputs")
            if not isinstance(ins, list) or not ins:
                errors.append(f"{w}: question.inputs (the evidence contract) must be a non-empty list")
            else:
                for i in ins:
                    if i not in tree.get("inputs", []):
                        errors.append(f"{w}: question input {i!r} is not a declared tree input")
            if set(q) - {"type", "wording", "options", "inputs", "basis"}:
                errors.append(f"{w}: unexpected question fields {sorted(set(q) - {'type', 'wording', 'options', 'inputs', 'basis'})}")
            for j, b in enumerate(q.get("basis", [])):
                if set(b) != {"citation", "quote"}:
                    errors.append(f"{w}: basis[{j}] must be {{citation, quote}}")
                check_quote(b.get("citation", ""), b.get("quote"), {"statute", "guidance", "bill"}, f"{w}.basis[{j}]", errors)
        elif kind == "discretionary":
            allowed.add("decision")
            d = node.get("decision") or {}
            if d.get("by") not in ("agent", "operator") or not isinstance(d.get("what"), str) or set(d) != {"by", "what"}:
                errors.append(f"{w}: decision must be {{by: agent|operator, what}}")
        if "contested" in node:
            contested_refs.append((w, node["contested"], lid))
        extra = set(node) - allowed
        if extra:
            errors.append(f"{w}: unexpected fields {sorted(extra)}")
    else:
        errors.append(f"{where}: unknown node type {t!r}")


def check_tree(path: pathlib.Path, errors, all_ids):
    try:
        tree = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"{path.name}: invalid JSON ({exc})")
        return None, []
    w = path.name
    required = ["id", "title", "decisionPoint", "layer", "effective", "inputs", "parameters", "root", "effects",
                "contested"]
    for k in required:
        if k not in tree:
            errors.append(f"{w}: missing {k}")
    extra = set(tree) - set(required)
    if extra:
        errors.append(f"{w}: unexpected top-level fields {sorted(extra)}")
    tid = tree.get("id", "")
    if not re.match(r"^CA\.[a-z0-9-]+$", tid) or path.stem != tid.split(".", 1)[-1]:
        errors.append(f"{w}: id must be CA.<file stem>")
    if not isinstance(tree.get("title"), str) or not tree["title"].endswith("?"):
        errors.append(f"{w}: title must be the plain question the tree answers")
    if not DP.match(tree.get("decisionPoint", "")):
        errors.append(f"{w}: decisionPoint must be a chain-map id")
    if tree.get("layer") not in LAYERS:
        errors.append(f"{w}: layer must be one of {sorted(LAYERS)}")
    eff = tree.get("effective") or {}
    if set(eff) != {"from", "to"} or not DATE.match(str(eff.get("from"))) or not (eff.get("to") is None or DATE.match(str(eff["to"]))):
        errors.append(f"{w}: effective must be {{from: date, to: date|null}}")
    ins = tree.get("inputs")
    if not isinstance(ins, list) or not all(isinstance(i, str) for i in ins) or len(set(ins)) != len(ins or []):
        errors.append(f"{w}: inputs must be a list of unique names")
    refs = []
    for j, p in enumerate(tree.get("parameters", [])):
        pw = f"{w}:parameters[{j}]"
        if set(p) != {"id", "value", "unit", "source"}:
            errors.append(f"{pw}: parameter must be {{id, value, unit, source}}")
        if p.get("unit") not in UNITS:
            errors.append(f"{pw}: unit must be one of {sorted(UNITS)}")
        if p.get("unit") == "cents" and not isinstance(p.get("value"), int):
            errors.append(f"{pw}: cents must be an integer")
        src = p.get("source") or {}
        check_quote(src.get("citation", ""), src.get("quote"), {"statute"}, pw, errors)
        v = p.get("value")
        if isinstance(v, (int, float)) and not isinstance(v, bool) and src.get("quote"):
            texts = list(NUMBER_TEXT.get(v, [str(v)]))
            if p.get("unit") == "cents":
                texts += [f"${v / 100:.2f}", f"${v // 100}" if v % 100 == 0 else f"${v / 100:.2f}"]
            if p.get("unit") == "multiplier" and isinstance(v, float):
                texts += [f"{round(v * 100):g} percent"]
            if not any(t in norm(src["quote"]) for t in texts):
                errors.append(f"{pw}: value {v} not stated in its quote")
        elif isinstance(v, str) and DATE.match(v) and src.get("quote"):
            import datetime
            d = datetime.date.fromisoformat(v)
            if f"{d.strftime('%B')} {d.day}, {d.year}" not in norm(src["quote"]):
                errors.append(f"{pw}: date {v} not stated in its quote")
    leaves, contested_refs = {}, []
    walk(tree.get("root"), f"{w}:root", tree, errors, leaves, refs, contested_refs)
    effects = tree.get("effects")
    if not isinstance(effects, list) or not effects:
        errors.append(f"{w}: effects must be a non-empty list")
        effects = []
    seen = set()
    for j, e in enumerate(effects):
        ew = f"{w}:effects[{j}]"
        allowed = {"id", "kind", "statement", "when", "amount", "due", "consequence", "source", "margin", "notBefore"}
        if set(e) - allowed:
            errors.append(f"{ew}: unexpected fields {sorted(set(e) - allowed)}")
        if e.get("id") in seen or not isinstance(e.get("id"), str):
            errors.append(f"{ew}: effect id missing or duplicate")
        seen.add(e.get("id"))
        if e.get("kind") not in EFFECT_KINDS:
            errors.append(f"{ew}: kind must be one of {sorted(EFFECT_KINDS)}")
        if e.get("when") not in ("holds", "fails"):
            errors.append(f"{ew}: when must be holds or fails")
        if not isinstance(e.get("statement"), str) or not e["statement"].strip().endswith("."):
            errors.append(f"{ew}: statement must be a sentence")
        for k in ("amount", "due", "margin", "notBefore"):
            if k in e:
                check_expr(e[k], tree, f"{ew}.{k}", errors, refs)
        if "consequence" in e:
            refs.append((ew, "consequence", e["consequence"], ""))
        if "source" in e:
            src = e["source"]
            if set(src) != {"citation", "quote"}:
                errors.append(f"{ew}: source must be {{citation, quote}}")
            check_quote(src.get("citation", ""), src.get("quote"), {"statute"}, ew, errors)
    issues = {}
    for j, c in enumerate(tree.get("contested", [])):
        cw = f"{w}:contested[{j}]"
        if set(c) != {"issue", "question", "branches", "exposureBranch"}:
            errors.append(f"{cw}: contested must be {{issue, question, branches, exposureBranch}}")
        issues[c.get("issue")] = c
        bids = []
        brs = c.get("branches") or []
        if len(brs) < 2:
            errors.append(f"{cw}: needs at least two branches")
        for k, b in enumerate(brs):
            bw = f"{cw}.branches[{k}]"
            if set(b) != {"id", "reading", "authority", "effect"}:
                errors.append(f"{bw}: branch must be {{id, reading, authority, effect}}")
            bids.append(b.get("id"))
            if not b.get("authority"):
                errors.append(f"{bw}: authority required")
            for a, au in enumerate(b.get("authority", [])):
                if set(au) != {"citation", "quote"}:
                    errors.append(f"{bw}.authority[{a}]: must be {{citation, quote}}")
                check_quote(au.get("citation", ""), au.get("quote"), {"statute", "bill", "mirror", "guidance", "court", "leghist"},
                            f"{bw}.authority[{a}]", errors)
            ef = b.get("effect") or {}
            if not isinstance(ef.get("statement"), str) or set(ef) - {"statement", "sets"}:
                errors.append(f"{bw}: effect must be {{statement, sets?}}")
            for lid, val in (ef.get("sets") or {}).items():
                if lid not in leaves or not isinstance(val, bool):
                    errors.append(f"{bw}: sets {lid!r} must name a leaf of this tree with true or false")
        if c.get("exposureBranch") not in bids:
            errors.append(f"{cw}: exposureBranch must name a branch")
    for where, issue, lid in contested_refs:
        if issue not in issues:
            errors.append(f"{where}: contested {issue!r} not defined in this tree")
        elif not any(lid in (b.get("effect", {}).get("sets") or {}) for b in issues[issue].get("branches", [])):
            errors.append(f"{where}: no branch of {issue} sets this leaf")
    for where, issue, _ in []:
        pass
    all_ids.add(tid)
    return tree, refs


def main(argv):
    files = [pathlib.Path(a) for a in argv] or sorted(p for p in HERE.glob("*.json") if p.name != "JEV_CHECK.json")
    errors, all_ids, refs, trees = [], set(), [], {}
    for f in files:
        tree, r = check_tree(f, errors, all_ids)
        if tree:
            trees[tree.get("id")] = tree
            refs.extend(r)
    known = all_ids | {t.get("id") for t in (json.loads(p.read_text()) for p in HERE.glob("*.json")
                                             if p.name != "JEV_CHECK.json")}
    for where, fn, tid, eid in refs:
        if tid not in known:
            errors.append(f"{where}: {fn} refers to unknown tree {tid!r}")
        elif fn == "amount" and eid:
            target = trees.get(tid) or json.loads((HERE / (tid.split('.', 1)[1] + ".json")).read_text())
            if eid not in {e.get("id") for e in target.get("effects", [])}:
                errors.append(f"{where}: amount refers to unknown effect {tid}/{eid}")
    leaf_count = sum(1 for t in trees.values() for _ in _leaves(t.get("root")))
    if errors:
        for e in errors:
            print("FAIL", e)
        print(f"{len(errors)} problem(s) in {len(files)} tree file(s)")
        return 1
    print(f"OK: {len(files)} trees, {leaf_count} leaves; every quote verbatim and inside its cited subdivision")
    return 0


def _leaves(node):
    if not isinstance(node, dict):
        return
    if node.get("type") == "condition":
        yield node
    for k in ("children",):
        for c in node.get(k, []) or []:
            yield from _leaves(c)
    for k in ("child", "rule", "exception"):
        if isinstance(node.get(k), dict):
            yield from _leaves(node[k])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
