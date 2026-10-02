"""Reviewer q4 helpers (batch 4). Read-only on rule files."""
import json, pathlib, re, sys
LE = pathlib.Path(__file__).resolve().parents[2]
WORK = LE / "register/work"
ATOMS = {}
for k in ("NY", "NYC", "US", "VA"):
    for a in json.loads((LE / f"stage-a/{k}.json").read_text())["atoms"]:
        ATOMS[a["id"]] = a
BATCH = json.loads((WORK / "batch_4.json").read_text())["sections"]
DEC = WORK / "decisions_4.jsonl"
norm = lambda s: re.sub(r"\s+", " ", s).strip()

def brief(i):
    a = ATOMS[i]
    return f"{i} || IF {a['condition']} || THEN {a['effect']}"

def search(pat, fields=("id","provision","condition","effect","quote")):
    r = re.compile(pat, re.I)
    return [i for i, a in ATOMS.items() if any(r.search(str(a.get(f, ""))) for f in fields)]

def decided():
    if not DEC.exists(): return {}
    return {json.loads(l)["section_id"]: json.loads(l) for l in DEC.read_text().splitlines() if l.strip()}

def text(sid):
    s = next(x for x in BATCH if x["section_id"] == sid)
    return (LE / s["text_file"]).read_text()

def body(sid):
    t = text(sid)
    # strip header lines
    lines = t.splitlines()
    out = [l for l in lines if not l.startswith(("SOURCE:", "OFFICIAL:", "RETRIEVED:"))]
    return "\n".join(l for l in out if l.strip())

def src(sid):
    s = next(x for x in BATCH if x["section_id"] == sid)
    t = (LE / s["text_file"]).read_text()
    m = re.search(r"^SOURCE:\s*(\S+)", t, re.M)
    return s["text_file"], (m.group(1) if m else "")

def q(sid, start, end=None):
    """Mechanically copy a verbatim quote from the section text: from `start` through `end` (inclusive)."""
    t = norm(text(sid))
    i = t.find(norm(start))
    assert i >= 0, f"start not found in {sid}: {start}"
    if end is None:
        return norm(start)
    j = t.find(norm(end), i)
    assert j >= 0, f"end not found in {sid}: {end}"
    return t[i:j + len(norm(end))]

def rule(sid, **kw):
    f, u = src(sid)
    base = {"jurisdiction": "NY", "determinacy": "RULE", "judgment_terms": [], "dependencies": [],
            "source_file": f, "source_url": u}
    base.update(kw)
    return base

def add(rows):
    have = decided()
    with DEC.open("a") as fh:
        for r in rows:
            r.setdefault("reviewer", "q4")
            r.setdefault("atom_ids", [])
            r.setdefault("proposed", [])
            if r["section_id"] in have:
                print("SKIP already decided", r["section_id"]); continue
            assert any(x["section_id"] == r["section_id"] for x in BATCH), r["section_id"]
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            have[r["section_id"]] = r

def nd(sid, reason):
    return {"section_id": sid, "decision": "no_decision", "reason": reason}

def show_range(a, b, maxc=None):
    for k, s in enumerate(BATCH[a:b], a):
        t = body(s["section_id"])
        if maxc: t = t[:maxc]
        print(f"\n===== [{k}] {s['section_id']} | {s['heading']} | jev {s['jev_p_decides']}\n{t}")

def fix(sid, pid, field, old, new):
    rows = [json.loads(l) for l in DEC.read_text().splitlines() if l.strip()]
    n = 0
    for r in rows:
        if r["section_id"] != sid: continue
        if pid is None:
            assert old in r[field], (sid, field); r[field] = r[field].replace(old, new); n += 1
        for p in r.get("proposed", []):
            if p["id"] == pid:
                assert old in p[field], (sid, pid, field); p[field] = p[field].replace(old, new); n += 1
    assert n, (sid, pid)
    DEC.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
