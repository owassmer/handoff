"""Reviewer q8 helpers: read batch-8 sections, copy quotes mechanically, merge decisions idempotently.

Usage in chunk scripts (run from research/legal-engine):
    from q8_lib import D, P, q, save
    save([D(...), ...])      # replaces rows with the same section_id, keeps batch order
CLI:
    python3 register/work/q6_lib.py show '<section_id>' [start] [len]   # print a section's text
    python3 register/work/q6_lib.py todo                               # undecided section ids
"""
import json
import pathlib
import re
import sys

LE = pathlib.Path(__file__).resolve().parents[2]
WORK = LE / "register/work"
OUT = WORK / "decisions_8.jsonl"
BATCH = json.loads((WORK / "batch_8.json").read_text())["sections"]
SEC = {s["section_id"]: s for s in BATCH}
ORDER = {s["section_id"]: i for i, s in enumerate(BATCH)}
norm = lambda s: re.sub(r"\s+", " ", s).strip()


def text(path):
    return (LE / path).read_text(errors="ignore")


def tf(sid):
    return SEC[sid]["text_file"]


def src_url(path):
    for line in text(path).splitlines()[:5]:
        if line.startswith("SOURCE:"):
            return line.split(":", 1)[1].strip()
    raise ValueError(f"no SOURCE header in {path}")


def q(path, start, end=None):
    """Return the exact (whitespace-normalized) span of `path` from `start` through `end` (inclusive)."""
    t = norm(text(path))
    s = norm(start)
    i = t.find(s)
    if i < 0:
        raise ValueError(f"start not found in {path}: {start[:80]}")
    if t.find(s, i + 1) >= 0 and end is None:
        pass
    if end is None:
        return t[i:i + len(s)]
    e = norm(end)
    j = t.find(e, i)
    if j < 0:
        raise ValueError(f"end not found after start in {path}: {end[:80]}")
    return t[i:j + len(e)]


def P(id, provision, actor, modality, condition, effect, source_file, quote, severity, walk_step,
      determinacy="RULE", judgment_terms=None, dependencies=None, instrument=None, amends=None,
      construction=None, reasoning=None, jurisdiction="US"):
    r = {"id": id, "jurisdiction": jurisdiction, "instrument": instrument or provision, "provision": provision,
         "actor": actor, "modality": modality, "condition": condition, "effect": effect, "determinacy": determinacy,
         "judgment_terms": judgment_terms or [], "dependencies": dependencies or [], "source_file": source_file,
         "source_url": src_url(source_file), "quote": quote, "severity": severity, "walk_step": walk_step}
    if amends:
        r["amends"] = amends
    if construction:
        assert reasoning, f"{id}: construction needs reasoning"
        r["construction"] = [{"source_file": f, "quote": qq} for f, qq in construction]
        r["reasoning"] = reasoning
    elif reasoning:
        r["reasoning"] = reasoning
    return r


def D(sid, decision, reason, atoms=None, proposed=None):
    assert sid in SEC, sid
    r = {"section_id": sid, "decision": decision, "reason": reason, "atom_ids": atoms or [],
         "proposed": proposed or [], "reviewer": "q8"}
    return r


def load():
    if not OUT.exists():
        return {}
    return {json.loads(l)["section_id"]: json.loads(l) for l in OUT.read_text().splitlines() if l.strip()}


def save(rows):
    cur = load()
    for r in rows:
        cur[r["section_id"]] = r
    OUT.write_text("".join(json.dumps(cur[k], ensure_ascii=False) + "\n" for k in sorted(cur, key=ORDER.get)))
    print(f"saved {len(rows)} rows; file has {len(cur)}/{len(SEC)}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "show":
        t = text(tf(sys.argv[2]))
        a = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        n = int(sys.argv[4]) if len(sys.argv) > 4 else 40000
        print(t[a:a + n])
    elif cmd == "todo":
        done = load()
        print([s for s in SEC if s not in done])


def chunks(limit=40000):
    """Split batch into consecutive chunks of about `limit` chars."""
    out, cur, n = [], [], 0
    for s in BATCH:
        if cur and n + s["chars"] > limit:
            out.append(cur); cur, n = [], 0
        cur.append(s); n += s["chars"]
    if cur:
        out.append(cur)
    return out


def dump(k, a=0, b=None, limit=40000):
    for s in chunks(limit)[k][a:b]:
        print(f"\n######## {s['section_id']} | {s['heading']} | jev p={s['jev_p_decides']} duty={s['jev_chain_duty']} | {s['text_file']}")
        t = text(s["text_file"])
        t = "\n".join(l for l in t.splitlines() if not l.startswith(("SOURCE:", "OFFICIAL:", "RETRIEVED:", "Source:", "N.Y.")) and l.strip())
        print(t)


def props(pat):
    """Print proposals in decisions_1-8 whose id or section matches regex pat."""
    import glob
    rx = re.compile(pat)
    for f in sorted(glob.glob(str(WORK / "decisions_*.jsonl"))):
        for l in open(f):
            r = json.loads(l)
            for p in r.get("proposed", []):
                if rx.search(p["id"]) or rx.search(r["section_id"]):
                    print(f"{f[-8:]} {r['section_id']} -> {p['id']}: IF {p['condition'][:200]} THEN {p['effect'][:400]}")
