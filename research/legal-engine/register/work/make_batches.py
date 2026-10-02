"""Split the review queue into six reviewer batches by instrument family (Owen, option a: every queued section gets a
reviewer decision). Adds two sections Ferro pulled back from Jev's set-aside list on spot check (MDL 9, RPL 442-C).

Run from research/legal-engine/register: python3 work/make_batches.py. Writes work/batch_<n>.json. Each batch lists
its sections in tier order (strong, likely, possible, low-confidence, long/unscored), then by instrument.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
REG = HERE.parent
T = [json.loads(l) for l in open(REG / "triage.jsonl")]
S = {json.loads(l)["section_id"]: json.loads(l) for l in open(REG / "sections.jsonl")}
REQUEUE = {"NY:MDL 9": "Converted buildings; bears on the MDL 301 certificate-of-occupancy rule (Ferro spot check).",
           "NY:RPL 442-C": "Salesperson violations; bears on the Handoff-under-a-broker configuration (Ferro spot check)."}

FAMILIES = {
    1: ("NY real property and deposits", ["NY:RPL", "NY:RPAPL", "NY:MDL", "NY:GOL", "NY:GCN", "NY:9NYCRR", "NY:16NYCRR",
                                           "NY:19NYCRR", "NY:23NYCRR", "NY:STT", "NY:ABP", "NY:DCL"]),
    2: ("NY procedure and courts", ["NY:CPLR", "NY:CCA", "NY:22NYCRR", "NY:JUD"]),
    3: ("NYC codes and rules", ["NYC:ADC", "NYC:RCNY"]),
    4: ("NY business, consumer, estates and status law", ["NY:GBL", "NY:SSL", "NY:18NYCRR", "NY:PTR", "NY:MHY", "NY:UCC",
                                                          "NY:MIL", "NY:EXEC", "NY:LLC", "NY:NPCL", "NY:BCL", "NY:SCPA",
                                                          "NY:EPTL"]),
    5: ("Federal bankruptcy and tax", ["US:11USC", "US:FRBP", "US:26CFR1-info", "US:26USC-6041-6050", "US:26USC166"]),
    6: ("Federal consumer, credit, housing and servicemember law",
        ["US:12CFR1005", "US:15USC-ch41", "US:15USC-ch96", "US:12USC5481", "US:12CFR1022", "US:12CFR1006", "US:24CFR982",
         "US:24CFR5", "US:24CFR100", "US:42USC-ch45", "US:50USC-ch50", "US:34USC-VAWA", "US:47CFR64L", "US:12USC5220note"]),
}


def tier(t):
    j = t.get("jev") or {}
    if not j:
        return 4, "long_or_unscored"
    pd = (j.get("role_probabilities") or {}).get("DECIDES", 0) or 0
    cd = j.get("chain_duty") or 0
    if pd >= .9 and cd >= .8:
        return 0, "strong"
    if pd >= .5 or cd >= .5:
        return 1, "likely"
    if pd >= .15 or cd >= .3:
        return 2, "possible"
    return 3, "low_confidence"


queue = [t for t in T if t["status"] == "review_queue" or t["section_id"] in REQUEUE]
fam_of = {inst: n for n, (_, insts) in FAMILIES.items() for inst in insts}
missing = sorted({t["instrument"] for t in queue} - set(fam_of))
assert not missing, missing
total = 0
for n, (name, _) in FAMILIES.items():
    rows = []
    for t in queue:
        if fam_of[t["instrument"]] != n:
            continue
        rank, label = tier(t)
        j = t.get("jev") or {}
        s = S[t["section_id"]]
        rows.append({"section_id": t["section_id"], "instrument": t["instrument"], "unit": t["unit"],
                     "heading": t["heading"], "text_file": "register/" + s["text_file"], "chars": s["chars"],
                     "tier": label, "_rank": rank,
                     "jev_p_decides": (j.get("role_probabilities") or {}).get("DECIDES"),
                     "jev_chain_duty": j.get("chain_duty"), "queue_reason": REQUEUE.get(t["section_id"], t["reason"])})
    rows.sort(key=lambda r: (r["_rank"], r["instrument"], r["section_id"]))
    for r in rows:
        del r["_rank"]
    out = {"batch": n, "family": name, "sections": rows, "count": len(rows), "chars": sum(r["chars"] for r in rows)}
    (HERE / f"batch_{n}.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    total += len(rows)
    print(n, name, len(rows), out["chars"])
print("total", total)
