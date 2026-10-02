"""Reviewer q2 helpers (batch 2). Import from register/work chunk scripts.

show(i, j)            print batch sections i..j-1 (body text, header stripped)
q(src, start, end)    mechanically copy the verbatim span of src that begins with `start` and ends with `end`
R(...)                build a proposed rule (source_url from the file's SOURCE header, quote copied by q)
D(sid, decision, reason, atoms=(), proposed=())   one decision row
write(rows)           append rows to decisions_2.jsonl, replacing rows for the same section_id (idempotent)
"""
import json
import pathlib
import re

LE = pathlib.Path(__file__).resolve().parents[2]
WORK = LE / "register/work"
OUT = WORK / "decisions_2.jsonl"
BATCH = json.loads((WORK / "batch_2.json").read_text())["sections"]
BY_ID = {s["section_id"]: s for s in BATCH}
norm = lambda s: re.sub(r"\s+", " ", s).strip()


def body(path):
    t = (LE / path).read_text(errors="ignore")
    lines = t.splitlines()
    k = 0
    while k < len(lines) and re.match(r"^(SOURCE|OFFICIAL|CAPTURE|PUBLISHED|RETRIEVED|NOTE)\b", lines[k]):
        k += 1
    return "\n".join(lines[k:]).strip()


def show(i, j, maxc=None):
    for n, s in enumerate(BATCH[i:j], i):
        b = body(s["text_file"])
        if maxc and len(b) > maxc:
            b = b[:maxc] + f"\n...[{len(b) - maxc} more chars]"
        print(f"\n######## [{n}] {s['section_id']} | {s['heading']} | P={s['jev_p_decides']} | {s['text_file']}")
        print(b)


def src_url(src):
    for line in (LE / src).read_text(errors="ignore").splitlines()[:6]:
        if line.startswith("SOURCE:"):
            return line.split("SOURCE:", 1)[1].strip()
    raise ValueError(f"no SOURCE header in {src}")


def q(src, start, end=None):
    t = norm((LE / src).read_text(errors="ignore"))
    start, end = norm(start), norm(end) if end else None
    i = t.find(start)
    if i < 0:
        raise ValueError(f"start not found in {src}: {start[:60]}")
    if end is None:
        return start
    j = t.find(end, i + len(start) - len(end) if len(end) < len(start) else i)
    if j < 0:
        raise ValueError(f"end not found in {src}: {end[:60]}")
    return t[i:j + len(end)]


def R(id, sid, provision, actor, modality, condition, effect, start, end=None, severity="major", walk_step="8.10",
      determinacy="RULE", judgment_terms=(), dependencies=(), amends=None, instrument=None, src=None,
      effective_from=None, construction=None, reasoning=None):
    s = BY_ID[sid]
    src = src or s["text_file"]
    p = {
        "id": id, "jurisdiction": "NY", "instrument": instrument or {
            "NY:CPLR": "NY Civil Practice Law and Rules", "NY:CCA": "New York City Civil Court Act",
            "NY:22NYCRR": "22 NYCRR (Uniform Rules of the Trial Courts)", "NY:JUD": "NY Judiciary Law"}[s["instrument"]],
        "provision": provision, "actor": actor, "modality": modality, "condition": condition, "effect": effect,
        "determinacy": determinacy, "judgment_terms": list(judgment_terms), "dependencies": list(dependencies),
        "source_file": src, "source_url": src_url(src), "quote": q(src, start, end), "severity": severity,
        "walk_step": walk_step,
    }
    if effective_from:
        p["effective_from"] = effective_from
    if amends:
        p["amends"] = amends
    if construction:
        p["construction"] = construction
        p["reasoning"] = reasoning
    return p


def D(sid, decision, reason, atoms=(), proposed=()):
    assert sid in BY_ID, sid
    return {"section_id": sid, "decision": decision, "reason": reason, "atom_ids": list(atoms),
            "proposed": list(proposed), "reviewer": "q2"}


def write(rows):
    old = [json.loads(l) for l in OUT.read_text().splitlines() if l.strip()] if OUT.exists() else []
    new_ids = {r["section_id"] for r in rows}
    assert len(new_ids) == len(rows), "duplicate section in chunk"
    keep = [r for r in old if r["section_id"] not in new_ids]
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in keep + rows))
    print(f"wrote {len(rows)} rows; file now {len(keep) + len(rows)} rows")
