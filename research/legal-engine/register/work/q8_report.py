"""Write register/work/report_8.md from decisions_8.jsonl (reviewer q8, set-aside batch B)."""
import json, pathlib, collections, sys
sys.path.insert(0, "register/work")
from q8_lib import SEC, load
rows = load()
cnt = collections.Counter(r["decision"] for r in rows.values())
inst = collections.Counter(SEC[s]["instrument"] for s in rows)
sev_order = {"critical": 0, "major": 1, "minor": 2}
props = [(p, r) for r in rows.values() for p in r["proposed"]]
props.sort(key=lambda x: (sev_order[x[0]["severity"]], x[0]["id"]))
L = []
L.append("# Report 8: set-aside reviewer B (NY MDL through federal FRBP)\n")
L.append("Reviewer q8, 2026-09-30. Batch `register/work/batch_8.json`: 420 sections Jev set aside as deciding nothing "
         "(NY 221, NYC 109, US 90; 905,152 characters). Every section was read in full from its register text; decisions "
         "are in `register/work/decisions_8.jsonl`, written by the idempotent scripts `register/work/q8_c*.py` "
         "(helpers `q8_lib.py`, this report `q8_report.py`). Report only: no rule file, walk, skill or source was edited.\n")
L.append("## Counts\n")
L.append(f"- Decided: {len(rows)}/420. no_decision {cnt['no_decision']}, new_rule {cnt['new_rule']}, partial {cnt['partial']}, "
         f"stated {cnt['stated']}, excluded_regime {cnt['excluded_regime']}.")
L.append(f"- Proposed rules: {len(props)} ({', '.join(f'{k} {v}' for k, v in collections.Counter(p['severity'] for p, _ in props).items())}).")
L.append("- `python3 register/work/check_decisions.py 8`: 420/420 decided, 0 errors. `check_decisions.py all`: no id collisions "
         "(batch 7's 45 undecided sections belong to set-aside reviewer A, still running).\n")
L.append("## Sections decided other than no_decision (Jev's misses)\n")
L.append("| Section | Heading | Decision | Jev p_decides | Jev chain_duty | Proposed rule |")
L.append("|---|---|---|---|---|---|")
for sid, r in rows.items():
    if r["decision"] != "no_decision":
        s = SEC[sid]
        L.append(f"| {sid} | {s['heading'][:60]} | {r['decision']} | {s['jev_p_decides']} | {s['jev_chain_duty']} | "
                 + ", ".join(f"`{p['id']}`" for p in r["proposed"]) + " |")
L.append("\nAll seven scored at or below 0.01 on p_decides and 0.04-0.08 on chain_duty: Jev read entity-filing and licensing "
         "boilerplate as internal governance and missed the suspension, winding-up and penalty clauses inside it. Six of the "
         "seven are owner-capacity or owner-status rules of the same family the queue reviewers already opened (LLC 206, BCL 1312, "
         "N-PCL 1313, Partnership Law 121-902/907/1500/1502/104-A); the set-aside list held the remaining branches of that family.\n")
L.append("## Proposed rules, most severe first\n")
for p, r in props:
    L.append(f"### `{p['id']}` ({p['severity']}, walk step {p['walk_step']}, {p['determinacy']})")
    L.append(f"- Section: {r['section_id']}; provision {p['provision']}" + (f"; amends `{p['amends']}`" if p.get("amends") else ""))
    L.append(f"- If: {p['condition']}")
    L.append(f"- Then: {p['effect']}")
    L.append(f"- Quote ({p['source_file']}): \"{p['quote'][:400]}{'...' if len(p['quote']) > 400 else ''}\"")
    if p.get("reasoning"):
        L.append(f"- Reasoning: {p['reasoning']}")
    L.append(f"- Depends on: {', '.join(p['dependencies']) or 'none'}\n")
L.append("## Notes for adjudication\n")
L.append("- Dependencies on queue proposals. The capacity rules above rest on the queue's proposed "
         "`NY:NPCL-1313-foreign-authority`, `NY:PTR-121-1502-foreign-llp` and `NY:PTR-121-104-a-process-address-suspension`, "
         "which are not yet in the rule files; the checker accepts only existing ids in `dependencies`, so those names appear in "
         "the effect or reasoning text and the existing analogues (`NY:LLC-206-publication-suspension`, `NY:BCL-1312(a)-foreign-authority`, "
         "`NY:LLC-808(a)-foreign-authority`) are listed as dependencies. If Owen rejects a queue proposal, the dependent rule here "
         "falls with it.")
L.append("- Suspension bars suit. `NY:PTR-121-201-lp-publication` and `NY:PTR-121-1506-llp-process-address-suspension` read "
         "'authority ... suspended' as barring the entity from maintaining an action, on the Appellate Division's reading of the "
         "identical LLC Law 206 words (Small Step Day Care, the construction behind `NY:LLC-206-publication-suspension`). "
         "`NY:NPCL-1309(b)-name-change-suspension` applies N-PCL 1313(a), whose text bars a corporation 'conducting activities "
         "... without authority'.")
L.append("- Boundary calls decided no_decision, stated here so Owen can overrule them in one line each:")
L.append("  - Partnership Law 121-303 and 121-403 (limited and general partners' personal liability for the owner partnership's debts): "
         "reaching an owner's principals to enforce a tenant's judgment is not a step any chain actor takes; consistent with the "
         "queue's 121-1001 decision. If Owen wants the tenant's enforcement against principals in scope, both become rules "
         "(general partners liable as partners in a general partnership; limited partners not liable unless they take part in control "
         "and the tenant reasonably relied on it).")
L.append("  - RPL 442-A (salespersons paid only through their broker for 'leasing, renting'): decided on the construction already in "
         "`NY:RPL-442-fee-split` (Kreuter, strict construction; 'renting' excludes rent collection). If that construction falls, 442-A "
         "would bar Handoff from paying its own salesperson-employees for rent collection under Configuration 3.")
L.append("  - SCPA 2108 (court-authorized continuation of a decedent's business): the existing owner-death and fiduciary rules decide "
         "who collects and who is paid; a continuation decree adds no settlement step.")
L.append("  - 6 RCNY 5-42 (price gouging, 'merchant' includes a lessor): a move-out charge passes on the landlord's repair or cleaning "
         "cost under the deposit rules and is not a sale of covered goods or services by the landlord.")
L.append("  - MHL 81.03, N-PCL 1301, Partnership Law 121-101 and 121-1507, 24 CFR 982.2, 28 RCNY 12-05 (definitions and applicability): "
         "each read against the rules that use its terms; none widens or narrows a stated or proposed rule.")
L.append("\n## Existing rules that look wrong\n")
L.append("None found in the rules this batch touched (`NYC:ADC-20-490`, `NY:RPL-223`, `NY:GBL-130-assumed-name`, "
         "`NY:HMC-27-2045-detector-charge`, `NY:HANDOFF-broker-config-under-broker`, `NY:RPL-442-fee-split`, "
         "`NY:LLC-206-publication-suspension`, `NY:GOL-7-103(1)-trust`). One incompleteness, proposed above: `NYC:ADC-20-490` lists "
         "the 20-494 penalties but not the separate 20-105 per-day fine, stop order and sealing for unlicensed activity.")
pathlib.Path("register/work/report_8.md").write_text("\n".join(L) + "\n")
print("wrote report_8.md", len(L), "lines")
