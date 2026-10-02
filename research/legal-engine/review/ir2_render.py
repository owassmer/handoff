"""Independent review 2: render review/INDEPENDENT_REVIEW_2.md from review/independent_review_2.json
plus the fixed sections below. Run from research/legal-engine:  python3 review/ir2_render.py
"""
import collections
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "review/independent_review_2.json").read_text())
OUT = ROOT / "review/INDEPENDENT_REVIEW_2.md"

F = D["findings"]
sev = collections.Counter(f["severity"] for f in F)
kind = collections.Counter(f["kind"] for f in F)
order = {"critical": 0, "major": 1, "minor": 2}
F = sorted(F, key=lambda f: (order[f["severity"]], f["id"]))

L = []
L.append("# Independent review 2: settling a market-rate tenancy in New York City")
L.append("")
L.append("Reviewer: independent reviewer 2, 2026-09-29. Report only; no rule file, walk or existing source was edited. "
         "Findings are machine-checked by `python3 review/ir2_verify.py` (every evidence quote verbatim in its saved "
         "source, every rule id exists, self-test catches a planted bad quote and a planted bad id). The findings "
         "live in `review/independent_review_2.json`; this file is rendered from it by `review/ir2_render.py`.")
L.append("")
L.append("## Summary")
L.append("")
L.append(f"- Findings: {len(F)}. By severity: critical {sev['critical']}, major {sev['major']}, minor {sev['minor']}. "
         "By kind: " + ", ".join(f"{k} {v}" for k, v in sorted(kind.items())) + ".")
L.append(f"- Confirmed: {len(D['confirmed'])} rulings and high-consequence rule groups verified against source (listed below).")
L.append("- Judgment: **accept after the listed corrections.**")
L.append("")
L.append(
    "The walk is sound where it matters most for the 14-day settlement itself: the regime by lease date, the cap, "
    "the trust and interest rules, the count of the 14 days, what may be kept, the written statement and where to "
    "send it, forfeiture of the security but not the debt, co-tenants, belongings, and the federal and city "
    "collection layers all check out against their sources. What is wrong sits at the edges of the chain, where the "
    "manager decides whether rent can be recovered at all and for how long. The files never ask whether the building "
    "has a lawful certificate of occupancy, and without one no rent or use and occupancy can be recovered for that "
    "period (MDL 302, R2-01). That changes the amount on the statement and the pursue-or-write-off decision for "
    "exactly the small, often converted, buildings this customer manages. The six-year limit is current law, but a "
    "bill that makes it three years for lease balances passed both houses in June and is waiting on the Governor "
    "(R2-02). Two statements in the walk would mislead an operator: unregistered multiple-dwelling owners are barred, "
    "not merely stayable (R2-03), and the high-rent exemption from Good Cause Eviction is missing (R2-04). The walk's "
    "one-line definition of 'willful' overstates exposure on every managed account (R2-05). Lease-break charges and "
    "the rent a deposit may cover after an early departure have no rule (R2-06, R2-07). None of these reopens the "
    "core rules; each is a bounded addition or restatement.")
L.append("")
L.append("## Findings (most severe first)")
L.append("")
for f in F:
    L.append(f"### {f['id']} ({f['severity']}, {f['kind']})")
    L.append("")
    L.append(f"- Step: {f['step']}")
    if f["rule_ids"]:
        L.append("- Rules affected: " + ", ".join(f"`{r}`" for r in f["rule_ids"]))
    L.append(f"- What is wrong: {f['finding']}")
    L.append(f"- Correct law: {f['correct_rule']}")
    L.append("- Evidence:")
    for e in f["evidence"]:
        L.append(f"  - `{e['source_file']}`: \"{e['quote']}\"")
    L.append("")

L.append("## Confirmed")
L.append("")
L.append("Each item was checked against the saved source text (and, for rulings, against the cited decisions and a "
         "search for contrary or later authority). Rule ids in backticks.")
L.append("")
for c in D["confirmed"]:
    L.append(f"- {c['id']}: " + ", ".join(f"`{r}`" for r in c["rule_ids"]) + f". {c['basis']}")
L.append("")
L.append("Also verified on fidelity (effect matches quote and walk sentence): Step 0 routing (RSL 26-504, RSC 2520.11, "
         "RCL 26-403(e)(2)(i)(4) and (9)); 7-108(1) and (1-a) exclusions; Part M s.29 dates (2019-07-14, 2019-10-12); "
         "232-c renewal by rent acceptance (Case v 575 Classon, App Term 2d); 7-105 turnover and its inconsistent-"
         "agreement clause (text confirmed); 7-108(2) successor liability; 226-b; 235-f; 236/236-a; 226-c notice "
         "periods; 227-a, 227-c, MIL 310, SCRA 3955 (incl. all-parties reading from the 2004 House report); 229 and "
         "220; the inspection rules and Toporek's forfeiture scope; 238-a(2)/(2-a); 234/234-a; 235-i; 235-b offset; "
         "7-103(2-b); HCV and PBV rules; HRA/SOTA voucher terms; Article VIII escrow; FHA assistance-animal rules; "
         "OSC MS11 and ABP 1315(2); SCRA 3958; FDCPA and Regulation F conduct, validation, delivery, dispute and "
         "liability rules; 6 RCNY 5-76/5-77 current rules; the SHIELD text; Admin Code 20-489/20-490/20-493.1/20-493.2; "
         "FCRA furnisher duties; 11 USC 362(a)(6), 524(a)(2).")
L.append("")

L.append("## Test cases")
L.append("")
L.append("Decided from the law before reading the walk's answers; differences stated.")
L.append("")
TC = [
    ("C3", "Same result. 7-108(1-a) applies (2023 lease). Statement by email within 14 days of vacating (vacate day "
           "excluded, weekend/holiday rolls). Refund within the same 14 days: deposit plus bank interest less 1% a year, "
           "less rent unpaid, damage beyond wear and tear, lease utilities and moving/storage; no fees; no charge for "
           "repainting after ordinary use. With only an email known, the money goes by a payment the tenant can receive "
           "(electronic transfer) or a check mailed to the last postal address the landlord has. Add: rent may be kept "
           "only if the building's certificate of occupancy covers the unit (R2-01)."),
    ("C4", "Differs. Same as C3 without the interest-bearing duty, with 3-year repaint, painting records and HPD "
           "registration. Missing from the walk: a three-family house must hold a certificate of occupancy for three "
           "families; a legal two-family with a third unit is a de facto multiple dwelling and no rent or use and "
           "occupancy is recoverable for the unlawful period (R2-01); an unregistered owner recovers no rent until it "
           "registers (MDL 325(2), R2-03). Good Cause does not reach it if the owner holds ten or fewer units or lives "
           "in the building."),
    ("C5a", "Same result. Rent accepted after 2019-07-14 created a new month-to-month tenancy (RPL 232-c; Case v 575 "
            "Classon), so 1-a applies; the tenant may leave at the end of any month without notice (T.I.B.; "
            "Srinivasan)."),
    ("C6", "Differs in completeness. Mitigation duty and burden on the landlord (227-e, Toporek); statutory "
           "terminations end rent on their dates and bar early-termination charges; auto-renewal binds only with the "
           "5-905 notice; the clock runs from vacating. Missing: at day 14 the deposit may cover only rent that has "
           "fallen due and is unpaid, up to the new tenant's lease (R2-07); a lease-break sum is owed only if it is a "
           "valid liquidated-damages clause, cannot displace mitigation, and is not kept from the deposit (R2-06)."),
    ("C7", "Same result with additions. Timely itemized estimates (Toporek); excess is a separate claim that survives "
           "forfeiture; no legal fees without a court order; interest at the lease post-maturity rate to judgment "
           "(rent interest capped by 238-a) or 2% statutory; registration: a multiple-dwelling owner is barred, not "
           "stayed, until it registers (R2-03); rent part barred if no valid certificate of occupancy (R2-01); six-year "
           "limit today, three years if S9760 becomes law (R2-02)."),
    ("C8", "Same result. No statement until the second co-tenant leaves; then a statement to each; refund split by "
           "the landlord's records of who paid what, else jointly."),
    ("C9", "Same result with one addition. Statement and refund to the vacated unit within 14 days; unclaimed money "
           "stays the tenant's and is reported after three years. The ABP 1422 due-diligence mailing is excused here "
           "because the only address is known not to be current (R2-09)."),
    ("C10", "Same result with one addition. Turnover within 5 days with registered or certified mail notice; the buyer "
            "settles; a buyer with actual knowledge is liable if not turned over. The buyer must register as the new "
            "owner (27-2097; MDL 325(1) within 30 days of succession) before it can recover rent (R2-03)."),
    ("C11", "Same result. Belongings stay the tenant's, cannot be held for rent, are released on request, may be "
            "disposed of only on abandonment; reasonable moving and storage costs may be kept; belongings may push "
            "back the vacate date where the lease so provides (Urban)."),
    ("C12", "Same result. 2026-12-11 is a Friday; day 14 is Friday 2026-12-25, Christmas, a public holiday; "
            "Saturday 26 and Sunday 27 follow; the statement and refund are due Monday 2026-12-28."),
    ("C13", "Same result. Only the tenant's share is charged; the owner keeps the move-out month's HAP and gets no "
            "later HAP; written list and refund within 14 days satisfy 'promptly'."),
    ("C14", "Differs. The agency is a federal debt collector (principal purpose; account taken after default) and a "
            "DCWP-licensed agency; validation notice within 5 days to an address where the tenant now receives mail; "
            "verification with the lease and the statement; the current 6 RCNY 5-77 rules apply until 2027-01-01, "
            "SHIELD after. 23 NYCRR Part 1 does not apply (R2-10). Limitation: six years today, three years for suits "
            "commenced from the 90th day after S9760 becomes law (R2-02). Interest 2% (natural person). Before suit: "
            "multiple-dwelling registration is a bar, not a stay (R2-03), and no rent is recoverable for any period "
            "without a valid certificate of occupancy (R2-01)."),
    ("C15", "Same result. Applying the deposit to pre-filing charges is a stayed setoff; hold only the disputed part "
            "while promptly moving for relief (Strumpf); statement by day 14 without a demand; the rest to the chapter "
            "7 trustee (or as the trustee directs) or to the debtor in chapter 13."),
]
for c, t in TC:
    L.append(f"- {c}: {t}")
L.append("")

L.append("## First-round corrections (task 6)")
L.append("")
FR = D.get("first_round", [])
if not FR:
    L.append("Pending: written after tasks 1-5 were saved.")
else:
    for x in FR:
        L.append(f"- {x['id']}: **{x['verdict']}**. {x['reason']}")
    ov = D.get("overlap")
    if ov:
        L.append("")
        L.append(ov)
L.append("")

L.append("## Method")
L.append("")
L.append(
    "- Read APERTURE.md, STAGE_A.md and the CORDON design principles, then the walk in full. Scripted a side-by-side "
    "dump (`review/ir2_dump.py`) of all 361 rules the walk cites: the walk paragraph, condition, effect, quote, "
    "source, authorities and reasoning, and read all of it (about 450 KB). Opened sources in context where a quote "
    "was short or the effect went beyond it (RPL 214, GOL 7-105, CPLR 3215, CPLR 5004, Admin Code 27-2097/27-2107, "
    "Karole, Prando, Freeland, Srinivasan, Pickens, Caldwell). Ran `check_review.py` (359 in scope cited, 95 "
    "deferred, 0 missing) and `stage_a_check.py` (0 errors in all four files).")
L.append(
    "- Searched for contrary and later authority on each ruling (nycourts.gov reporter, Justia, CourtListener-backed "
    "mirrors, web search): 7-108 willfulness and delivery decisions 2021-2026; CPLR 214-i and rent; NYC month-to-"
    "month notice; MDL 302/325 and de facto multiple dwellings (Chazon, Caldwell, Jalinos, 49 Bleecker, Malden); "
    "liquidated damages (JMD Holding); DFS 23 NYCRR Part 1 and its unadopted amendment; FARE Act litigation (2d "
    "Cir. 2026-07-13); DCWP SHIELD status and the ACA International challenge to the superseded 2024 rule; the "
    "Consumer Debt Uniformity Act (S9760/A10182-A) actions; ABP 1422.")
L.append(
    "- Enumerated the chain through the nine families. New law not in the files: MDL 301/302/325(2) and MDL 4(7); "
    "RPL 214(15); RPL 232; ABP 1422; 23 NYCRR 1.1(d); the Court of Appeals liquidated-damages test; S9760. Considered "
    "and left out as not changing a decision in this chain: RPL 235-e(d) (defense in eviction only), CPLR 5205(g) "
    "(debtor's exemption; the trustee still directs payment), NYC Human Rights Law process rules, PSC submetering "
    "(no utility charge fact pattern in scope).")
L.append(
    "- Saved new sources mechanically (web_extract output or curl + pdftotext written by script, never retyped) with "
    "the REVIEW2_ prefix: MDL 4, 301, 302, 325; RPL 232; ABP 1422; 23 NYCRR 1.1; Chazon (CoA 2012), Caldwell (2d "
    "Dept 2008), 49 Bleecker (1st Dept 2018), JMD Holding (CoA 2005), Kunik (App Term 2d 2023); S9760/A10182-A with "
    "actions; REBNY v City of New York (2d Cir. 2026).")
L.append(
    "- Access: nycourts.gov and Justia returned a Cloudflare page to curl; web_extract retrieved them. write_file "
    "will not overwrite a file it did not read, so two stub files from the first curl attempt were deleted and "
    "re-saved. Google Scholar was not used.")
L.append("")
OUT.write_text("\n".join(L))
print("wrote", OUT, len("\n".join(L)))
