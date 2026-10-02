"""Reviewer q1 helpers (batch 1). Run from research/legal-engine.

show(start, end)       print section texts for batch entries [start, end) (index in batch order), skipping decided ones
Q(src, a, b)           verbatim quote: normalized text of src from anchor a through anchor b (inclusive)
R(...)                 build a proposed rule (source_url taken from the file's SOURCE header)
D(sid, decision, reason, atom_ids=(), proposed=())   one decision row
save(rows)             append rows to decisions_1.jsonl (replacing rows for the same section)
"""
import json
import pathlib
import re

LE = pathlib.Path(__file__).resolve().parents[2]
WORK = LE / "register/work"
OUT = WORK / "decisions_1.jsonl"
BATCH = json.loads((WORK / "batch_1.json").read_text())["sections"]
BY_ID = {s["section_id"]: s for s in BATCH}
norm = lambda s: re.sub(r"\s+", " ", s).strip()


def decided():
    if not OUT.exists():
        return {}
    return {json.loads(l)["section_id"]: json.loads(l) for l in OUT.read_text().splitlines() if l.strip()}


def body(path):
    t = (LE / path).read_text(errors="ignore")
    lines = t.splitlines()
    out = [l for l in lines if not re.match(r"^(SOURCE|OFFICIAL|RETRIEVED):", l)]
    t = "\n".join(out)
    t = re.sub(r"\nSource:\nSection .*$", "", t, flags=re.S)
    return t.strip()


def show(start, end, skip_decided=True, maxchars=None):
    d = decided()
    for i, s in enumerate(BATCH[start:end], start):
        if skip_decided and s["section_id"] in d:
            continue
        b = body(s["text_file"])
        if maxchars and len(b) > maxchars:
            b = b[:maxchars] + f"\n...[truncated {len(b) - maxchars}]"
        print(f"=== [{i}] {s['section_id']} | {s['heading']} | tier={s['tier']} p={s['jev_p_decides']} | {s['text_file']}")
        print(re.sub(r"\n(?=[a-z(])", " ", b) if False else b)
        print()


def compact(b):
    b = re.sub(r"\nNOTES \(LII amendment history\):.*$", "", b, flags=re.S)
    b = re.sub(r"^N\.Y\.\n\n", "", b)
    b = re.sub(r"\n+(?!\(|\d+(-[a-z])?\.|[a-z]\.\n|\*)", " ", b)
    return b


def showc(start, budget=38000, heads_only=False):
    d = decided()
    used, i = 0, start
    while i < len(BATCH):
        s = BATCH[i]
        if s["section_id"] in d:
            i += 1
            continue
        b = compact(body(s["text_file"]))
        if used and used + len(b) > budget:
            break
        print(f"=== [{i}] {s['section_id']} | {s['heading']} | {s['tier']} p={s['jev_p_decides']}")
        print(b if not heads_only else b[:300])
        print()
        used += len(b)
        i += 1
    print(f"NEXT {i}")


def src_of(sid_or_path):
    return BY_ID[sid_or_path]["text_file"] if sid_or_path in BY_ID else sid_or_path


def Q(src, a, b=None):
    src = src_of(src)
    t = norm((LE / src).read_text(errors="ignore"))
    a, b = norm(a), norm(b) if b else None
    i = t.find(a)
    if i < 0:
        raise ValueError(f"anchor a not found in {src}: {a[:60]}")
    if b is None:
        return a
    j = t.find(b, i)
    if j < 0:
        raise ValueError(f"anchor b not found after a in {src}: {b[:60]}")
    return t[i:j + len(b)]


def url_of(src):
    for l in (LE / src).read_text(errors="ignore").splitlines()[:5]:
        if l.startswith("SOURCE:"):
            return l.split(":", 1)[1].strip()
    raise ValueError(f"no SOURCE header in {src}")


def R(id, sid, provision, actor, modality, condition, effect, quote, severity, walk_step, determinacy="RULE",
      judgment_terms=(), dependencies=(), amends=None, instrument=None, reasoning=None, construction=None,
      jurisdiction="NY", effective_from=None):
    src = src_of(sid)
    r = {"id": id, "jurisdiction": jurisdiction, "instrument": instrument or BY_ID.get(sid, {}).get("instrument", ""),
         "provision": provision, "actor": actor, "modality": modality, "condition": condition, "effect": effect,
         "determinacy": determinacy, "judgment_terms": list(judgment_terms), "dependencies": list(dependencies),
         "source_file": src, "source_url": url_of(src), "quote": quote, "severity": severity, "walk_step": walk_step}
    if amends:
        r["amends"] = amends
    if reasoning:
        r["reasoning"] = reasoning
    if construction:
        r["construction"] = construction
    if effective_from:
        r["effective_from"] = effective_from
    return r


def D(sid, decision, reason, atom_ids=(), proposed=()):
    assert sid in BY_ID, sid
    row = {"section_id": sid, "decision": decision, "reason": reason, "reviewer": "q1"}
    if atom_ids:
        row["atom_ids"] = list(atom_ids)
    if proposed:
        row["proposed"] = list(proposed)
    return row


def save(rows):
    d = decided()
    for r in rows:
        d[r["section_id"]] = r
    order = {s["section_id"]: i for i, s in enumerate(BATCH)}
    OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in sorted(d.values(), key=lambda r: order.get(r["section_id"], 1e9))) + "\n")
    print(f"saved {len(rows)}; total decided {len(d)}/{len(BATCH)}")
