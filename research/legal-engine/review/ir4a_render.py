"""Independent review 4A: write the universe coverage map (review/ir4a_coverage.json) and render
review/INDEPENDENT_REVIEW_4A.md from review/independent_review_4a.json and review/review4a_universe.json.
Run after ir4a_build_findings.py: python3 review/ir4a_render.py
"""
import json
import pathlib
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent

# Universe item -> (status, rules or finding). Status: covered | gap | partial | deferred | no-decision.
C = {
 "U001": ("covered", "NY:GOL-7-108(1)"), "U002": ("covered", "NY:GOL-7-108(1-a)-exclusions"), "U003": ("covered", "NY:RPL-214"),
 "U004": ("covered", "NY:RPL-215"), "U005": ("covered", "NY:GOL-7-108(1-a)(a)"), "U006": ("covered", "NY:GOL-7-108(1-a)(c)-offer NY:GOL-7-108(1-a)(c)-bar"),
 "U007": ("covered", "NY:GOL-7-103(1)-trust"), "U008": ("covered", "NY:GOL-7-103(2)-bank-notice"), "U009": ("covered", "NY:GOL-7-103(2)-admin-fee"),
 "U010": ("covered", "NY:GOL-7-103(2-a)"), "U011": ("covered", "NY:GOL-7-103(3)"), "U012": ("gap", "R4A-15"), "U013": ("gap", "R4A-16"),
 "U014": ("gap", "R4A-14"), "U015": ("gap", "R4A-33"), "U016": ("covered", "NY:GOL-5-905"), "U017": ("partial", "R4A-01"),
 "U018": ("covered", "NY:RPL-232-c"), "U019": ("covered", "NY:RPL-232-a"), "U020": ("covered", "NY:RPL-226-c(1)(a) NY:RPL-226-c(2)"),
 "U021": ("covered", "NY:RPL-229"), "U022": ("covered", "NY:RPL-227-e"),
 "U023": ("covered", "NY:RPL-227-e (applies by the date the action is commenced, so the Holy Properties no-mitigation rule no longer governs a suit brought after 2019-06-14)"),
 "U024": ("covered", "NY:CASE-Toporek-forfeiture-scope"), "U025": ("partial", "R4A-09"),
 "U026": ("covered", "NY:ADJ-lease-break-charge NY:RPL-227-e-waiver (JMD Holding states the same penalty test)"),
 "U027": ("covered", "NY:ADJ-lease-break-charge"), "U028": ("covered", "NY:RPL-226-b(1)"), "U029": ("covered", "NY:RPL-226-b(2)"),
 "U030": ("covered", "NY:RPL-227"), "U031": ("covered", "NY:RPL-227-a(2)"), "U032": ("covered", "NY:RPL-227-c(2)"), "U033": ("covered", "NY:RPL-236"),
 "U034": ("covered", "NY:RPL-236-a"), "U035": ("covered", "NY:RPL-236-a"), "U036": ("covered", "US:50USC3955(e)(1)-prorate US:50USC3955(e)(1)-no-etf"),
 "U037": ("covered", "NY:MIL-310(2)"), "U038": ("gap", "R4A-22"), "U039": ("gap", "R4A-22"),
 "U040": ("covered", "NY:GOL-7-105(1) NY:GOL-7-105(2)-transfer-effect"), "U041": ("covered", "NY:GOL-7-108(2)(a) NY:GOL-7-108(2)(c)"),
 "U042": ("covered", "NY:RPL-223"), "U043": ("covered", "NY:RPL-440(1)-rent-collection"), "U044": ("covered", "NY:RPL-442-d-442-e-unlicensed"),
 "U045": ("covered", "NY:BCL-1312(a)-foreign-authority"), "U046": ("covered", "NY:LLC-808(a)-foreign-authority"), "U047": ("covered", "NY:MDL-325(2)"),
 "U048": ("covered", "NYC:ADC-27-2107(b)-rent-stay"), "U049": ("covered", "NY:MDL-302(1)(b)"), "U050": ("covered", "NY:MDL-301(1)"),
 "U051": ("covered", "NY:MDL-302-a(3)"), "U052": ("covered", "NY:RPAPL-776-778-administrator"), "U053": ("covered", "NY:CPLR-6401-foreclosure-receiver"),
 "U054": ("covered", "US:15USC1692a(6)-regularly-another (any person who regularly collects for another, lawyers included)"),
 "U055": ("covered", "US:15USC1692a(6)-regularly-another US:15USC1692a(6)(F)(iii)"), "U056": ("covered", "US:CASE-Romea-1998"),
 "U057": ("covered", "NY:GOL-7-103(2-b)"), "U058": ("covered", "NY:CASE-Paterno-commingling-forfeiture NY:CASE-Paterno-bank-notice-inference"),
 "U059": ("partial", "R4A-28"), "U060": ("covered", "NY:GOL-7-108(1-a)(b)-refundable NY:GOL-7-108(1-a)(b)-excluded-costs"),
 "U061": ("covered", "NY:GOL-7-108(1-a)(d)-notice NY:GOL-7-108(1-a)(d)-inspection"), "U062": ("covered", "NY:GOL-7-108(1-a)(f)"),
 "U063": ("covered", "NY:RPL-238-a(2)"), "U064": ("covered", "NY:RPL-238-a(2-a) NY:GOL-5-328(3)(b)"), "U065": ("covered", "NY:RPL-235-g"),
 "U066": ("covered", "NY:RPL-234"), "U067": ("partial", "R4A-29"), "U068": ("covered", "NY:RPL-234-a"), "U069": ("covered", "NY:RPL-235-i"),
 "U070": ("covered", "NY:RPL-235-b"), "U071": ("covered", "NY:RPL-235-a"), "U072": ("covered", "NYC:HMC-27-2013(b)(2) NYC:PAINT-wear-and-tear"),
 "U073": ("covered", "NYC:HMC-27-2056.8-lead-turnover"), "U074": ("covered", "NYC:HMC-27-2017.5-turnover"),
 "U075": ("covered", "US:24CFR982.313(c) US:24CFR982.313(d)"), "U076": ("covered", "US:24CFR982.311(d)(1)"), "U077": ("covered", "NYC:RCNY68-10-14(c)"),
 "U078": ("covered", "NYC:RCNY68-10-14(e)"), "U079": ("covered", "NYC:HRA-voucher-claim-window NYC:HRA-voucher-proof"),
 "U080": ("covered", "NY:GOL-7-108(1-a)(e) NY:GOL-7-108(1-a)(e)-forfeiture"), "U081": ("covered", "NY:GCN-25-a(1)"), "U082": ("covered", "NY:GCN-20"),
 "U083": ("covered", "NY:STT-305(3)"), "U084": ("covered", "NY:CASE-Levine-counterclaim"), "U085": ("covered", "NY:GOL-7-108(1-a)(g)"),
 "U086": ("gap", "R4A-05"), "U087": ("gap", "R4A-05"), "U088": ("deferred", "NY:GOL-7-109 (deferred as not a manager's decision; agreed)"),
 "U089": ("gap", "R4A-27"), "U090": ("gap", "R4A-26"), "U091": ("covered", "NY:CCA-1809(1)"), "U092": ("covered", "NY:CCA-1803-A(b)"),
 "U093": ("covered", "NY:CCA-1803-A(b) (five-per-month certification)"), "U094": ("covered", "NY:CPLR-3215(g)(3)"), "U095": ("gap", "R4A-13"),
 "U096": ("covered", "NY:ADJ-lease-balance-not-consumer-credit NY:S9760-pleading-service (no current application to a lease balance)"),
 "U097": ("covered", "NY:CPLR-3015(e)-licence-pleading"), "U098": ("covered", "US:50USC3931(b)(1)"), "U099": ("gap", "R4A-34"), "U100": ("gap", "R4A-17"),
 "U101": ("no-decision", "clerk's discretion over repeat claims; changes no manager decision"), "U102": ("covered", "NY:CPLR-213(2)"),
 "U103": ("covered", "NY:CPLR-214-i"), "U104": ("covered", "NY:ADJ-lease-balance-not-consumer-credit"),
 "U105": ("covered", "NY:ADJ-lease-balance-not-consumer-credit (agrees with DCWP's reading)"),
 "U106": ("no-decision", "accrual rule is implicit in every limitation rule; no separate decision"), "U107": ("gap", "R4A-04"), "U108": ("gap", "R4A-03 R4A-04"),
 "U109": ("gap", "R4A-03"), "U110": ("gap", "R4A-04"), "U111": ("gap", "R4A-04"), "U112": ("gap", "R4A-04"), "U113": ("covered", "NY:CPLR-5001(a)-(b)"),
 "U114": ("covered", "NY:CPLR-5004(a)-consumer-2pct"), "U115": ("gap", "R4A-08"), "U116": ("gap", "R4A-08"), "U117": ("covered", "US:15USC1692g(a)"),
 "U118": ("covered", "US:12CFR1006.34(a)(1) US:12CFR1006.34(c)"), "U119": ("covered", "US:12CFR1006.30(a)"),
 "U120": ("covered", "US:15USC1692c(a) US:15USC1692d US:15USC1692e(2)(A) US:15USC1692f(1)"), "U121": ("covered", "US:15USC1692i(a)"),
 "U122": ("covered", "US:15USC1692k(a)"), "U123": ("gap", "R4A-12"),
 "U124": ("partial", "NY:ADJ-lease-balance-not-consumer-credit (the state statute does not reach a lease balance; my universe line overstated it) and R4A-10 (the city rule imports its conduct)"),
 "U125": ("gap", "R4A-30"), "U126": ("deferred", "NY:GBL-602"), "U127": ("covered", "NY:23NYCRR-1.1(d)-not-lease"),
 "U128": ("covered", "NYC:ADC-20-489(a) NYC:ADC-20-490 NYC:DCA-owner-own-staff NYC:DCA-manager-for-owners"), "U129": ("covered", "NYC:ADC-20-493.1(b) NYC:ADC-20-493.2(a)"),
 "U130": ("covered", "NYC:RCNY6-2-190(b)"), "U131": ("covered", "NYC:RCNY6-2-191(a)"), "U132": ("gap", "R4A-21"), "U133": ("gap", "R4A-21"),
 "U134": ("covered", "NYC:RCNY6-5-76-debt-collector"), "U135": ("partial", "NYC:RCNY6-5-77(e)(1) NYC:RCNY6-5-77(b)(1)(iv) and R4A-10"),
 "U136": ("partial", "NYC:SHIELD-5-76-debt-collector NYC:SHIELD-5-77(f)(1) and R4A-11"), "U137": ("covered", "NYC:SHIELD-5-76-procedures"),
 "U138": ("covered", "NYC:SHIELD-effective-date NYC:SHIELD-operative-date"), "U139": ("covered", "NYC:CPL-20-700"), "U140": ("gap", "R4A-02"),
 "U141": ("gap", "R4A-02"), "U142": ("covered", "NY:L2019-c36-PartM-s29"), "U143": ("covered", "NY:ABP-1315(2)"),
 "U144": ("partial", "NY:OSC-MS11-refunds-due and R4A-31"), "U145": ("covered", "NY:ABP-1422"), "U146": ("covered", "US:11USC362(a)(6) US:11USC362(a)(7)"),
 "U147": ("covered", "US:11USC542-refund-payee"), "U148": ("covered", "US:11USC362(a)(7)-deposit-is-setoff"), "U149": ("covered", "US:11USC524(a)(2)"),
 "U150": ("gap", "R4A-07"), "U151": ("gap", "R4A-06"), "U152": ("gap", "R4A-24"), "U153": ("gap", "R4A-03"), "U154": ("gap", "R4A-03"),
 "U155": ("gap", "R4A-03"), "U156": ("gap", "R4A-03"), "U157": ("partial", "NY:COMMONLAW-owner-death-agency (owner's death only) and R4A-03 (tenant's death)"),
 "U158": ("deferred", "US:50USC3951(a)(1)(B) (deferred; agreed: eviction protection decides nothing once the tenant has left)"),
 "U159": ("deferred", "US:FR-2026-04689"), "U160": ("covered", "US:42USC3604(f)(3)(A)"), "U161": ("covered", "US:42USC3604(f)(3)(A)"),
 "U162": ("gap", "R4A-18"), "U163": ("gap", "R4A-18"), "U164": ("gap", "R4A-18"), "U165": ("gap", "R4A-18"), "U166": ("gap", "R4A-18"),
 "U167": ("gap", "R4A-25"), "U168": ("gap", "R4A-19"), "U169": ("gap", "R4A-25"),
 "U170": ("covered", "US:15USC1681s-2(a)(1)(A) US:15USC1681s-2(a)(3) US:15USC1681s-2(a)(5)(A)"), "U171": ("covered", "US:12CFR1022.42(a) US:12CFR1022.43(a)"),
 "U172": ("gap", "R4A-32"), "U173": ("gap", "R4A-20"), "U174": ("gap", "R4A-23"), "U175": ("gap", "R4A-23"),
 "U176": ("covered", "NY:CPLR-214-i-consumer-debt-S9760 NY:S9760-default-judgment"),
}

SEV = {"critical": 0, "major": 1, "minor": 2}


def main():
    R = json.loads((HERE / "independent_review_4a.json").read_text())
    U = json.loads((HERE / "review4a_universe.json").read_text())
    assert set(C) == {u["id"] for u in U}, "coverage map must list every universe item"
    cov = [{"universe_id": u["id"], "citation": u["citation"], "status": C[u["id"]][0], "rules_or_finding": C[u["id"]][1]} for u in U]
    (HERE / "ir4a_coverage.json").write_text(json.dumps(cov, indent=1, ensure_ascii=False))
    nsrc = len(list((HERE.parent / "sources").glob("REVIEW4A_*")))
    F = sorted(R["findings"], key=lambda f: (SEV[f["severity"]], f["id"]))
    sev = Counter(f["severity"] for f in F)
    st = Counter(c["status"] for c in cov)
    L = []
    w = L.append
    w("# Independent Review 4A: completeness of the law for settling a market-rate NYC tenancy\n")
    w("2026-09-29. Reviewer 4A (fresh context, report only). Scope: NYC market-rate units (not stabilized, not controlled;")
    w("public and project-based housing out), NY State + NYC + federal law, from the facts fixed at move-in to the account")
    w("closed. Machine-readable: `review/independent_review_4a.json`; universe: `review/review4a_universe.json`; coverage:")
    w("`review/ir4a_coverage.json`; evidence check: `python3 review/ir4a_verify.py`.\n")
    w("## Summary\n")
    w(f"- Universe enumerated blind from primary sources: **{R['universe_count']} items** "
      f"({Counter(u['level'] for u in U)['state']} state, {Counter(u['level'] for u in U)['city']} city, {Counter(u['level'] for u in U)['federal']} federal; "
      f"{Counter(u['kind'] for u in U)['case']} controlling decisions, {Counter(u['kind'] for u in U)['pending']} pending or future-dated).")
    w(f"- Diff against NY.json, NYC.json and US.json (604 rules, 507 in the market-rate scope): {st['covered']} items fully stated, "
      f"{st['partial']} stated in part, {st['gap']} with no rule, {st['deferred']} deferred by the walk with a reason I accept, "
      f"{st['no-decision']} that change no decision.")
    w(f"- Findings: **{len(F)}** - {sev['critical']} critical, {sev['major']} major, {sev['minor']} minor. Over-scope: "
      f"{len(R['over_scope'])} group ({sum(len(o['rule_ids']) for o in R['over_scope'])} rules), minor.")
    w("- All findings are new against rounds 1-3. One (R4A-10) also narrows a round-1 correction (R1-15).")
    w("- Judgment: the core of the chain (deposit cap, trust, interest, inspection, 14-day statement, forfeiture, willfulness,")
    w("  charges, mitigation, payees for co-tenants and bankruptcy, building preconditions, collection licensing, SHIELD, FDCPA)")
    w("  is complete and precise. The universe is **not yet complete**. The gaps again sit at the edges, in five clusters the")
    w("  earlier sweeps did not reach: (1) the tenant's personal status after move-out - death, military service, bankruptcy of a")
    w("  co-obligor, coerced debt; (2) time - every tolling and extension rule, and the tenant's own limitation period;")
    w("  (3) who is a 'landlord's agent' under FARE; (4) city rules that import state conduct rules (GBL 601 via 6 RCNY 5-77) or")
    w("  add new ones (SHIELD credit-reporting notice); (5) cross-cutting duties outside landlord-tenant law (anti-discrimination,")
    w("  information returns, tenant data). Of the nine critical findings, one corrects an accepted rule (R4A-01 adds a branch")
    w("  that reverses NYC:FARE-moveout-service-fee for a manager who is the landlord's agent); the other eight add rules the")
    w("  files do not have. After these are resolved, a round limited to these clusters should come back clean.\n")
    w("## Gaps and partial statements (most severe first)\n")
    for f in F:
        w(f"### {f['id']} ({f['kind']}, {f['severity']})\n")
        w(f"- Decision point: {f['step']}")
        if f["rule_ids"]:
            w("- Rules concerned: " + ", ".join(f"`{i}`" for i in f["rule_ids"]))
        w(f"- What is missing: {f['finding']}")
        w(f"- Correct law, as a rule: {f['correct_rule']}")
        if f.get("earlier_rounds"):
            w(f"- Earlier rounds: {f['earlier_rounds']}")
        w("- Evidence:")
        for e in f["evidence"]:
            w(f"  - `{e['source_file']}`: \"{e['quote']}\"")
        w("")
    w("## Over-scope\n")
    for o in R["over_scope"]:
        w("- " + ", ".join(f"`{i}`" for i in o["rule_ids"]) + f" ({o['severity']}): {o['why']}")
    w("\nNo other in-scope rule is over-scope. The routing rules for stabilized and controlled status (RSL 26-504, RSC")
    w("2520.11, RCL 26-403), the loft-law rule and the seasonal and co-op exceptions to the one-month cap decide whether the")
    w("unit is market-rate at all, so they belong in Step 0. The deferred list is right except where R4A-10 says otherwise.\n")
    w("## Universe coverage\n")
    w("| Item | Citation | Status | Rules or finding |")
    w("|---|---|---|---|")
    for c in cov:
        w(f"| {c['universe_id']} | {c['citation'].replace('|', '/')} | {c['status']} | {c['rules_or_finding'].replace('|', '/')} |")
    w("\n## New versus earlier rounds\n")
    w("Read only after the findings above were saved. Rounds 1-3 (INDEPENDENT_REVIEW_1-3 and their dispositions) raised none")
    w("of R4A-01 to R4A-34. Specific overlaps checked:")
    w("- R4A-10 narrows R1-15: round 1 moved every GBL 601 rule to the deferred list as deciding nothing. That is right for")
    w("  the state statute, but for NYC units it is over-corrected, because the city rule imports GBL 601's conduct.")
    w("- R4A-13 is separate from R2-11 (the small-claims exception to 3215(g)(3)); 3215(j) was not raised.")
    w("- R4A-03 is separate from R1-08 (RPL 236 silence); the payee and estate-claim rules were not raised.")
    w("- R4A-17: guarantors appear earlier only as defendants for the 2% judgment rate (R1-01).")
    w("- R4A-27 is separate from R1-14 (the landlord's small and commercial claims).")
    w("A parallel reviewer's file (INDEPENDENT_REVIEW_4B.md) exists in the folder; I did not read it, so this review stays")
    w("independent of it.\n")
    w("## Method\n")
    w("1. Blind phase. Read only APERTURE.md and STAGE_A.md 'Chain' and 'Discovery method'. Walked tables of contents on")
    w("   nysenate.gov (RPL arts. 6-A, 7, 12-A; GOL art. 5 title 9, art. 7 title 1; RPAPL arts. 7, 7-A; CPLR arts. 2, 50;")
    w("   CCA arts. 18, 18-A; SCPA arts. 13, 18; ABP arts. 13, 14; Military Law art. 13; GBL arts. 25, 29-H, 29-HHH, 39-F) and")
    w("   the American Legal bulk XML for the NYC Admin Code (titles 8, 20, 26, 27) and RCNY (titles 6, 28, 68). Federal text")
    w("   from uscode.house.gov and eCFR; IRS Pub. 527; controlling decisions from CourtListener and nycourts.gov; bill actions")
    w("   from assembly.state.ny.us; DCWP rule status from the City Record and rules.cityofnewyork.us. Existing saved sources")
    w(f"   were used where present, never refetched; {nsrc} new sources were saved mechanically with prefix REVIEW4A_ (via")
    w("   web_extract, `review/ir4a_fetch.py` and `review/ir4a_aml.py`). Every universe quote is cut from a saved file by")
    w("   anchors (`review/ir4a_lib.py`, `review/ir4a_build_universe.py`), never retyped. The universe was saved before any rule")
    w("   file, the walk or a review file was opened.")
    w("2. Diff phase. Dumped all 604 rules; matched each universe item by source file, provision and keyword, then read the")
    w("   candidate rules in full (`review/show.py`). An item is 'partial' when the rule lacks a branch, exception, date or")
    w("   consequence. Over-scope was tested on every cited in-scope rule against the aperture.")
    w("3. Corrections to my own universe made in the diff phase, and why: U124 (GBL 601) overstated the state statute, which")
    w("   needs an extension of credit; the correct city-rule route is R4A-10. U144 first named Comptroller code AC06, which")
    w("   the table places under banks; corrected to MS11 or TR04 after re-reading the table.")
    w("4. Checked and not included, because they are not law in force or passed: NY bills on deposit return within 30 days")
    w("   (S4856/A2652, S4087, A4355, A8078), deposit installments (S3164), deposit alternatives (S6397/A1431) and rent")
    w("   reporting (A2729-A/S10477-A), all in committee; NYC Int. 249-2026 (documentation of deposit deductions), in")
    w("   committee. The FTC fee rule (16 CFR 464) covers short-term lodging only. Neither CFPB nor FTC has adopted a 2026-2027")
    w("   rule that reaches a residential landlord's settlement.")
    w("5. Tools: `python3 review/ir4a_build_universe.py`, `python3 review/ir4a_build_findings.py`, `python3 review/ir4a_render.py`,")
    w("   `python3 review/ir4a_verify.py` (every quote verbatim in its source, whitespace-normalized; every rule id exists;")
    w("   self-test with a planted bad quote and a planted bad id).")
    (HERE / "INDEPENDENT_REVIEW_4A.md").write_text("\n".join(L) + "\n")
    print("rendered", len(F), "findings;", dict(st))


if __name__ == "__main__":
    main()
