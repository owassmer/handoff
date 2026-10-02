"""Build register/work/report_1.md from decisions_1.jsonl (reviewer q1). Run from research/legal-engine."""
import collections
import json
import pathlib
import sys

sys.path.insert(0, "register/work")
from q1_lib import BY_ID, OUT

rows = [json.loads(l) for l in OUT.read_text().splitlines() if l.strip()]
counts = collections.Counter(r["decision"] for r in rows)
props = [(r["section_id"], p) for r in rows for p in r.get("proposed", [])]
sev_order = {"critical": 0, "major": 1, "minor": 2}
props.sort(key=lambda x: (sev_order[x[1]["severity"]], x[1]["id"]))
by_sev = collections.Counter(p["severity"] for _, p in props)
high_nd = [r for r in rows if r["decision"] == "no_decision" and (BY_ID[r["section_id"]].get("jev_p_decides") or 0) >= 0.9]
high_ex = [r for r in rows if r["decision"] == "excluded_regime" and (BY_ID[r["section_id"]].get("jev_p_decides") or 0) >= 0.9]


def one_line(p):
    e = p["effect"]
    return (e[:230] + "...") if len(e) > 230 else e


L = []
L.append("# Review queue batch 1 (NY real property and deposits): reviewer q1 report\n")
L.append("Decisions: `register/work/decisions_1.jsonl` (499 of 499). Checker: `python3 register/work/check_decisions.py 1` "
         "-> 499/499 decided, 0 errors. Helper scripts: `register/work/q1_*.py` (q1_lib.py builds rows and copies quotes "
         "mechanically from the register text files; q1_c1..q1_c31.py are the chunk builders, rerunnable).\n")
L.append("## Counts\n")
for k in ["stated", "partial", "new_rule", "no_decision", "excluded_regime"]:
    L.append(f"- {k}: {counts.get(k, 0)}")
L.append(f"- proposed rules: {len(props)} (critical {by_sev['critical']}, major {by_sev['major']}, minor {by_sev['minor']})\n")
L.append("## Proposed rules, most severe first\n")
L.append("| id | severity | section | walk step | effect (one line) |")
L.append("|---|---|---|---|---|")
for sid, p in props:
    amend = f" (amends `{p['amends']}`)" if p.get("amends") else ""
    L.append(f"| `{p['id']}`{amend} | {p['severity']} | {sid} | {p['walk_step']} | {one_line(p).replace('|', '/')} |")
L.append("")
L.append("## Correctness findings on existing rules\n")
L.append("""1. `US:11USC542-refund-payee` omits the exemption branch. It pays a chapter 7 tenant's refund to the trustee once the
   landlord knows of the case. New York debtors may exempt CPLR 5205 property (DCL 282(i)), and CPLR 5205(g) exempts
   "Money deposited as security for the rental of real property to be used as the residence of the judgment debtor";
   11 USC 522(l): "Unless a party in interest objects, the property claimed as exempt on such list is exempt." An
   exempted refund leaves the estate and is paid to the debtor, not the trustee. Paying the trustee after the exemption
   stands is paying the wrong payee. Proposed fix: `NY:DCL-282-deposit-exemption-payee` (critical, amends the rule).
2. `NY:16NYCRR96-submetering` states only that submetering must be authorized. It does not state the charge ceiling,
   which 16 NYCRR 96.1(i) and 96.6(c) fix: the rate cap is "the rates and charges of the distribution utility for
   delivery and commodity in that billing period to similarly situated, direct metered residential customers", and
   "the submeterer shall not charge more than the applicable rate cap". So a submetered charge above the direct-metered
   utility rate is kept today when it may not be. It also omits 96.6(h): HEFPA protections "shall be provided to such
   resident prior to the commencement of any other civil enforcement, collection, or other proceeding based on such
   resident's overdue electric charges". Proposed: `NY:16NYCRR-96.1(i)-rate-cap`, `NY:16NYCRR-96.6-submeter-charge-limits`
   (both critical).
3. `NY:ADJ-tenant-death-payee` covers the sole or last surviving tenant only. When one of several co-tenants dies,
   GOL 15-106 says: "On the death of a joint obligor in contract, his estate shall be bound as such jointly and
   severally with the surviving obligor or obligors." The survivors stay liable for the full balance. Proposed
   `NY:GOL-15-106-cotenant-death`.
4. `NY:CASE-NML-contract-rate` applies "the lease rate" with no reading rule. GOL 5-1301 says that where a rate is stated
   "and no period of time is stated", it is computed "as if the words 'per annum' or 'by the year' had been added". A lease
   saying "interest at 1.5%" is therefore 1.5% a year, not a month. Proposed `NY:GOL-5-1301-rate-per-annum` (critical,
   amends).
5. The walk (Step 6.3) counts the 14 days in calendar days but never says which clock applies. GCN 53: "Any act required by
   or in pursuance of law to be performed at or within a prescribed time, shall be performed according to the standard
   time." An email statement sent after New York midnight on day 14 is late, whatever the sender's time zone. Proposed
   `NY:GCN-53-deadline-clock` (critical) with `NY:GCN-52-standard-time`. GCN 52(2) gives April/October daylight-saving
   dates, which are superseded by the federal Uniform Time Act (15 U.S.C. 260a; not in a saved source). The rule states
   that supersession in its reasoning. Verify against a saved copy of 260a before acceptance.

No stated rule was found to state the law wrongly on the text read. The five items above are omissions that change an
amount, payee or deadline.
""")
L.append("## no_decision or excluded_regime where Jev had P(DECIDES) >= 0.9\n")
L.append("| section | P | decision | reason |")
L.append("|---|---|---|---|")
for r in sorted(high_nd + high_ex, key=lambda r: -BY_ID[r["section_id"]]["jev_p_decides"]):
    L.append(f"| {r['section_id']} | {BY_ID[r['section_id']]['jev_p_decides']} | {r['decision']} | {r['reason'].replace('|', '/')} |")
L.append("")
L.append("## Notes on method\n")
L.append("""- Every section's text was read. The 18 long sections were read by structure, and their tenant, rent, lease and
  deposit passages were read in full.
- 23 NYCRR Part 1 (sections 1.2-1.7) was decided no_decision on the stated `NY:23NYCRR-1.1(d)-not-lease`. These sections
  scored 0.95-0.99 with Jev. If Owen ever reverses the lease-balance-not-credit adjudication, they become new rules for
  third-party collectors: initial disclosures, a time-barred debt notice, substantiation, payment-plan confirmation and
  email consent.
- The usury rules (GOL 5-501, 5-511, 5-513, 5-515, 5-519, 5-521) are proposed for payment plans or forbearance agreements
  on a balance. The branches state that lease late charges and statutory CPLR interest are not forbearance interest.
- Article 7-C (RPAPL 796 to 796-M) and 7-D (797 to 797-J) are excluded as outside NYC by their own terms (796-A(4), 797(3)).
  Article 7-A mechanics are no_decision because `NY:RPAPL-776-778-administrator` states their settlement effect.
- Rent-control regulations (9 NYCRR 2200.x) and RSC administration (2520.x) are excluded_regime. So are manufactured
  home parks, campgrounds, commercial leases, lodging houses, adult homes and Westchester/Putnam/outside-NYC Good Cause
  opt-in.
""")
pathlib.Path("register/work/report_1.md").write_text("\n".join(L) + "\n")
print(counts, len(props), by_sev, len(high_nd), len(high_ex))
