"""Build register/work/report_2.md from decisions_2.jsonl (tables) plus the reviewer's written sections."""
import json, collections
from q2_lib import OUT, WORK, BY_ID

rows = [json.loads(l) for l in OUT.read_text().splitlines() if l.strip()]
cnt = collections.Counter(r["decision"] for r in rows)
by_inst = collections.defaultdict(collections.Counter)
for r in rows:
    by_inst[BY_ID[r["section_id"]]["instrument"]][r["decision"]] += 1
props = [(r["section_id"], p, r["reason"]) for r in rows for p in r.get("proposed", [])]
sev_order = {"critical": 0, "major": 1, "minor": 2}
props.sort(key=lambda x: (sev_order[x[1]["severity"]], x[1]["id"]))
first = lambda s: s.split("; ")[0].split(". ")[0].rstrip(".") + "."

L = []
L.append("# Batch 2 review (reviewer q2): NY procedure and courts\n")
L.append("Report only. Decisions: `register/work/decisions_2.jsonl` (560 lines). Builders: `register/work/q2_c01.py`-`q2_c24.py` "
         "(idempotent; each rewrites its own rows), helpers `q2_lib.py`, checks `q2_verify.py`. "
         "`python3 register/work/check_decisions.py 2` passes: 560/560 decided, 0 errors.\n")
L.append("## Counts\n")
L.append("| decision | sections |\n|---|---|")
for k in ("stated", "partial", "new_rule", "no_decision", "excluded_regime"):
    L.append(f"| {k} | {cnt[k]} |")
L.append(f"| total | {sum(cnt.values())} |\n")
L.append(f"Proposed rules: {len(props)} ({sum(1 for _, p, _ in props if p['severity']=='critical')} critical, "
         f"{sum(1 for _, p, _ in props if p['severity']=='major')} major, {sum(1 for _, p, _ in props if p['severity']=='minor')} minor). "
         "All ids use the `NY:` prefix; none collides with an existing rule or with another batch's decisions file at the time of the check.\n")
L.append("| instrument | stated | partial | new_rule | no_decision | excluded_regime |\n|---|---|---|---|---|---|")
for inst, c in sorted(by_inst.items()):
    L.append(f"| {inst} | {c['stated']} | {c['partial']} | {c['new_rule']} | {c['no_decision']} | {c['excluded_regime']} |")
L.append("")
L.append(open(WORK / "q2_report_text.md").read())
L.append("\n## Proposed rules, most severe first\n")
L.append("| id | severity | section | decision basis (one line) |\n|---|---|---|---|")
for sid, p, reason in props:
    L.append(f"| `{p['id']}` | {p['severity']} | {sid} | {first(reason).replace('|', '/')} |")
L.append("\n## no_decision where Jev had P(DECIDES) >= 0.9\n")
L.append("| section | Jev P | reason |\n|---|---|---|")
for r in rows:
    s = BY_ID[r["section_id"]]
    if r["decision"] == "no_decision" and (s["jev_p_decides"] or 0) >= 0.9:
        L.append(f"| {r['section_id']} | {s['jev_p_decides']:.2f} | {r['reason'].replace('|', '/')} |")
(WORK / "report_2.md").write_text("\n".join(L) + "\n")
print("report written;", len(props), "proposed rules")
