"""Batches 7-8: the 878 sections Jev set aside as deciding nothing. The queue review showed 5 of 49 queued sections
with set-aside-like scores (P(DECIDES) < 0.15 and chain_duty < 0.10) do decide something, so every set-aside section
also gets a reviewer decision. Split by instrument into two batches of similar size."""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent; REG = HERE.parent
T = [json.loads(l) for l in open(REG / "triage.jsonl")]
S = {json.loads(l)["section_id"]: json.loads(l) for l in open(REG / "sections.jsonl")}
done = {x["section_id"] for n in range(1, 7) for x in json.loads((HERE / f"batch_{n}.json").read_text())["sections"]}
rows = []
for t in T:
    if t["status"] != "triaged_no_decision" or t["section_id"] in done: continue
    j = t.get("jev") or {}; s = S[t["section_id"]]
    rows.append({"section_id": t["section_id"], "instrument": t["instrument"], "unit": t["unit"], "heading": t["heading"],
                 "text_file": "register/" + s["text_file"], "chars": s["chars"], "tier": "set_aside",
                 "jev_p_decides": (j.get("role_probabilities") or {}).get("DECIDES"), "jev_chain_duty": j.get("chain_duty"),
                 "queue_reason": "Jev set aside as deciding nothing; reviewed for completeness"})
rows.sort(key=lambda r: (r["instrument"], r["section_id"]))
half = sum(r["chars"] for r in rows) / 2; acc = 0; split = len(rows)
for i, r in enumerate(rows):
    acc += r["chars"]
    if acc >= half and r["instrument"] != rows[min(i + 1, len(rows) - 1)]["instrument"]:
        split = i + 1; break
for n, part in ((7, rows[:split]), (8, rows[split:])):
    (HERE / f"batch_{n}.json").write_text(json.dumps({"batch": n, "family": "Set aside by Jev", "sections": part,
        "count": len(part), "chars": sum(r["chars"] for r in part)}, indent=1, ensure_ascii=False))
    print(n, len(part), sum(r["chars"] for r in part), part[0]["instrument"], "->", part[-1]["instrument"])
