"""Build register/work/report_6.md from decisions_6.jsonl (reviewer q6). Rerun after any change to the decisions."""
import collections
import json
import pathlib
import subprocess

LE = pathlib.Path(__file__).resolve().parents[2]
W = LE / "register/work"
batch = {s["section_id"]: s for s in json.loads((W / "batch_6.json").read_text())["sections"]}
rows = [json.loads(l) for l in (W / "decisions_6.jsonl").read_text().splitlines() if l.strip()]
counts = collections.Counter(r["decision"] for r in rows)
props = [(r["section_id"], p) for r in rows for p in r["proposed"]]
order = {"critical": 0, "major": 1, "minor": 2}
props.sort(key=lambda x: (order[x[1]["severity"]], x[1]["id"]))
check = subprocess.run(["python3", "register/work/check_decisions.py", "6"], cwd=LE, capture_output=True, text=True).stdout.strip()

L = []
L.append("# Review queue batch 6 (reviewer q6): federal consumer, credit, housing and servicemember law\n")
L.append("Report only. Decisions: `register/work/decisions_6.jsonl`; builders `register/work/q6_c01.py`-`q6_c09.py` "
         "(idempotent, merge by section id); helpers `q6_lib.py`, `q6_read.py`; this report `q6_report.py`.\n")
L.append("## Counts\n")
L.append(f"Sections decided: {len(rows)}/{len(batch)}.\n")
for k in ["stated", "partial", "new_rule", "no_decision", "excluded_regime"]:
    L.append(f"- {k}: {counts.get(k, 0)}")
sev = collections.Counter(p["severity"] for _, p in props)
L.append(f"\nProposed rules: {len(props)} (critical {sev['critical']}, major {sev['major']}, minor {sev['minor']}); every quote "
         "copied by script and verified by the checker; every dependency resolves to an existing or proposed id.\n")
L.append("Checker output:\n\n```\n" + check + "\n```\n")

L.append("## Proposed rules, most severe first\n")
for sid, p in props:
    eff = p["effect"].split(". ")[0].rstrip(".")
    amend = f" (amends `{p['amends']}`)" if p.get("amends") else ""
    L.append(f"- **{p['severity']}** `{p['id']}`{amend} [{sid}; walk {p['walk_step']}]: {eff}.")

L.append("""
## Existing rules that look wrong or incomplete

1. `NYC:SHIELD-5-77(e)(10)-credit-report-notice` applies the city's pre-reporting notice and 14-day wait to every
   debt collector that furnishes. FCRA 1681t(b)(1)(F) bars any state-law requirement "with respect to any subject matter
   regulated under section 1681s–2 of this title, relating to the responsibilities of persons who furnish information to
   consumer reporting agencies" (register/texts/US_15USC-ch41/1681t.txt). Notice to the consumer of negative furnishing
   is regulated by 1681s-2(a)(7); preemption is by subject matter, so DCWP's exemption for (a)(7) filers does not save
   the rest. The rule is displaced for furnishing; the Reg F pre-furnishing contact rule (`US:12CFR1006.30(a)`) still
   binds federal debt collectors. Proposed: `US:15USC1681t(b)(1)(F)-furnisher-preemption` (critical). The walk (8.5)
   lists the SHIELD notice as a live duty.
2. `NY:GBL-604-bb-coerced-debt`, credit-agency branch: it requires the creditor to "notify such consumer reporting agency
   that the account is disputed" within ten business days. That is a state requirement on the subject matter of
   1681s-2(a)(3) and (a)(8) and is displaced by the same clause; the stop-collection, review and determination duties stand.
3. `NY:RPL-227-c(5)(b)` reaches communications with "a collector or credit bureau". As to what is furnished to a
   consumer reporting agency it is displaced by 1681t(b)(1)(F); the federal accuracy duty
   (`US:15USC1681s-2(a)(1)(A)`) gives the same result, since a lawful 227-c termination reported as early is inaccurate.
   The rule stands for prospective landlords, collectors and other third parties.
4. `US:15USC1681s-2(b)(1)` says the furnisher investigates "within the agency's reinvestigation period" without the
   period; `EXT:15USC1681i` is marked "Not read". 1681i fixes 30 days, +15, 45 after a free report
   (`US:15USC1681i-furnisher-deadline`, partial).
5. `US:24CFR100.65-terms` conditions on a dwelling "not exempt under 42 U.S.C. 3603(b)" but no rule states the exemption.
   For the target customer (scattered single-family rentals) the single-family exemption is lost whenever a manager or
   other person in the business of renting is used (`US:42USC3603(b)-exemptions`).
6. `US:15USC7001(c)-esign-consent` does not limit the consent duty to a "consumer" (an individual renting for personal,
   family or household purposes, 15 U.S.C. 7006(1)); a company tenant is outside (`US:15USC7006-esign-consumer`, partial).
7. `US:50USC4042` states the private SCRA action but not the Attorney General's civil penalties (4041: $55,000 / $110,000)
   or the preservation of consequential and punitive damages (4043) (proposed `US:50USC4041-ag-penalties`,
   `US:50USC4043-other-remedies`).
8. Register scope, not a rule: `register/instruments.json` sets TILA part B (15 U.S.C. 1631-1651) out of scope because "a
   residential lease is not a credit transaction". A landlord that regularly offers move-out payment plans with a finance
   charge or more than four installments is a TILA creditor (`US:15USC1602(g)`, `US:15USC1605-plan-finance-charge`), and
   each such plan is a closed-end consumer credit transaction that needs part B disclosures (15 U.S.C. 1638, Reg Z
   1026.17-18). Part B, and Reg Z, belong in the register for that branch. Likewise the FTC Disposal Rule (16 CFR part 682)
   that 1681w requires is not in the register.

## no_decision sections with Jev P(DECIDES) >= 0.9

- US:15 USC 1681l (0.92): restricts what a consumer reporting agency may reuse from an investigative report in a later
  report; it binds agencies only, and no landlord, manager, Handoff or collector act turns on it.

No excluded_regime section had Jev >= 0.9.

## Recall notes for Jev (sections decided as deciding although Jev scored them below 0.15)

US:24 CFR 982.308, 982.309, 982.310, 982.312, 982.403, 982.453, 982.454, 982.455, 982.510, 5.2001, 5.2007, 5.2009;
US:12 CFR 1005.2, 1022.3; US:15 USC 1605, 7006; US:34 USC 12494; US:42 USC 3602; US:50 USC 3920. Most are voucher-owner
duties (termination grounds, tenancy addendum, HAP end dates, other charges) and definitions that change a stated rule's
reach; Jev read them as PHA administration.

## Method notes

- Reg E: only 1005.3(b)(2)-(3), 1005.10(b), (d), (e), 1005.13 and 1005.20 bind a person other than the account-holding bank
  (1005.3(a)); those became rules (autopay authorization, 10-day notice of a varying debit, no compulsory autopay for
  payment plans, check conversion and returned-fee notices, records, liability). Everything else, including error
  resolution, is the bank's; remittance and interchange sections decide nothing.
- The payment-plan branch recurs across TILA, EFTA, CFPA and FCRA: a plan is credit (`US:15USC1602(f)`); it may not be
  conditioned on autopay; it can make the landlord a TILA creditor; it stays outside the CFPA unless the 5517(a)(2)
  exceptions apply; refusing one on a credit report is an adverse action.
- 24 CFR 982: PHA-internal administration is no_decision; the two project-based sections (982.504, 982.521) and CPD
  equal access (5.106) are excluded_regime.
""")
(W / "report_6.md").write_text("\n".join(L) + "\n")
print("wrote report_6.md;", len(props), "proposed rules")
