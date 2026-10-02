"""IR4B prose: confirmed list, test cases, method, and the markdown renderer used by ir4b_build.py."""

# Basis codes: T = statute/regulation text read in the saved source in context; C = cited decision read in the
# saved source; Q = quote and effect read side by side in the full dump (quote supports the whole effect).
CONFIRMED = [
    # Step 0: status and regime
    "NY:GOL-7-108(1), NY:GOL-7-108(1-a)-exclusions: 7-108 reaches every non-7-107 dwelling unit; 1-a excludes rent-controlled units and licensed senior/care facilities (T).",
    "NY:L2019-c36-PartM-s29: s.25 applies to leases, rental agreements and renewals entered on or after 2019-07-14 (30th day after 2019-06-14); ss.3, 6, 7 from 2019-10-12 (T; dates computed).",
    "NY:RPL-232-c, NY:CASE-Case-v-575Classon, NY:CASE-Bogom-Shanon-month-to-month: rent accepted after the term creates a month-to-month renewal tenancy entered after 2019-07-14, so 1-a applies; Case also fixes actual damages at the retained deposit (C). Chery v Richards (App Term 2d 2019) fn 1 reads s.29 as action-date based; it is dicta and Case (same court, later) states the lease-date rule the statute prescribes.",
    "NY:GOL-7-108(1)-pre2019, NY:COMMONLAW-deposit-return, NYC:CASE-Pezzo-lease-return-term, NY:ADJ-fee-retention-commonlaw: old scope and common-law return rule for unrenewed pre-2019-07-14 leases (T, C).",
    "NYC:RSL-26-520: RSL chapter expires 2027-04-01, so stabilization atoms end 2027-03-31 (T).",
    "NYC:RC-status, NYC:RCL-26-403(e)(2)(i)(4), NYC:RCL-26-403(e)(2)(i)(9), NYC:RER-2211.8(a): no six-unit floor; 1-2 family vacancy since 1953-04-01 and any vacancy since 1971-06-30 exempt; pre-2019 high-income deregulation stands (T/Q).",
    "NYC:RSC-2520.11(a), (b), (c), (d), (e), (k), (p), (r)(1), (s)(1): exclusions quoted from the official NYCRR and the 2023 amendment text (Q).",
    "NY:MDL-4(7)-multiple-dwelling: three or more families counted as let or occupied (T).",
    "NY:MDL-302(1)(b): no rent or use and occupancy for the period of unlawful occupancy, no revival by a later certificate, deposit not kept for it; Chatsworth interference exception only (T, C: Caldwell, Chazon quotes). Subject to R4B-06.",
    "NY:MDL-325(2): suspension, not forfeiture; recovery of accrued rent on registration (T; C: 9 Montague Terrace; Chan v Adossa, App Term 2d, cited in Shoreview, same compliance purpose). Subject to R4B-07.",
    "NY:MDL-302-a(3): six-month rule, plans proviso, four exceptions, plead-and-deposit, voluntary payment (T). Walk wording: R4B-09.",
    "NY:ADJ-MDL-rent-bar-not-1-2-family: MDL forfeitures confined to multiple dwellings (C: Pickering; Thomas).",
    "NY:MDL-285(1)-loft-law, NYC:HMC-27-2087-cellar-basement: routing and cellar rule (T/Q).",
    "NY:RPAPL-776-778-administrator, NYC:HMC-27-2135(c)-receiver-rents, NYC:HMC-27-2147-rent-levy, NY:CPLR-6401-foreclosure-receiver, NY:COMMONLAW-mortgagee-assignment-of-rents, NY:COMMONLAW-owner-death-agency: who holds the rent claim (T/C quotes).",
    "US:11USC541-704-owner-chapter7, US:11USC1107-1306-owner-reorganization: who collects the owner's claims is right; the deposit branch needs the tracing condition (R4B-01).",
    "NYC:RCNY68-10-14(c), NYC:RCNY31-5-06(a)(1), NYC:RCNY28-1-01, NYC:RCNY28-1-12(b)-cap: voucher and Article VIII deposit rules (Q).",
    "US:15USC1692a(3), US:50USC3911(1)-(2), US:50USC3911(4): definitions (T).",
    # Step 1
    "NY:GOL-7-108(1-a)(a), NY:GOL-7-108(4), NY:GOL-7-108(6), NY:L2021-c428, NY:L2022-c111, NY:L2021-c789-s7, NY:L2022-c93: one-month cap including advances; first month's rent is not an advance; seasonal and co-op exceptions and their dates (T).",
    "NY:GOL-7-103(1)-scope, NY:GOL-7-103(1)-trust, NY:GOL-7-103(3), NY:GOL-7-108(3), NY:GOL-7-103(2)-bank-notice, NY:GOL-7-103(2-a), NY:GOL-7-103(2)-admin-fee, NY:GOL-7-103(2)-interest-owed, NY:GOL-7-103(2-b): trust, bank notice, six-unit interest account, 1% fee, interest to tenant (T).",
    "NY:ADJ-7103-2a-building-count, NY:CASE-Gihon-7-103(2-a)-building: building test, owner's buildings not combined (C: Gihon; Holmes; State v Parker; Lefkowitz quotes).",
    "NY:CASE-Paterno-bank-notice-inference: no bank notice permits a commingling inference (C).",
    "NY:GOL-7-108(1-a)(c)-offer, NY:GOL-7-108(1-a)(c)-bar: move-in inspection and bar (T).",
    "NYC:FARE-20-699.22(b), NYC:FARE-20-699.20-fee, NYC:DCWP-FARE-FAQ-disclosure: signed itemized disclosure, 3-year retention, fee = charge for services, leases signed from 2025-06-11 (T).",
    "NYC:HMC-27-2013(a), (b)(2), (c), (g), NYC:PAINT-wear-and-tear: three-year repaint and records in multiple dwellings; painting charge only for proven damage beyond wear (T; C: Bohl).",
    "NYC:ADC-27-2097-registration (duty) (T); consequence wording R4B-08.",
    "NY:STT-305(3), NY:STT-307, NY:RPL-235-g, NY:RPL-235-e(a): e-records, payment method, receipts (T).",
    # Step 2-3
    "NY:GOL-7-105(1), (2), (3), NY:GOL-7-108(2)(a)-(e), NY:RPL-223: transfer turnover in 5 days by registered/certified mail, successor liability, receiver cap (T).",
    "NY:RPL-226-b(1)-(3), NY:RPL-235-f, NY:RPL-236, NY:RPL-236-a, US:12CFR1006.2(e), NY:RPL-227: assignment, occupants, death, destruction (T).",
    "NY:ADJ-cotenants-vacated, NY:ADJ-cotenants-payee: clock from the last co-tenant's departure; joint vs recorded shares (C: Holmes majority and dissent; Lasky; GCN 35).",
    "NY:RPL-226-c(2), NY:RPL-226-c(1)(a): 30/60/90-day notice and extension of the tenancy (T).",
    "NY:RPL-212, NY:RPL-214, NY:RPL-214(15)-high-rent, NY:RPL-211(3)-small-landlord, NY:RPL-215: Good Cause scope, all fifteen exemptions including the 2009 certificate for thirty years and 245% of FMR, sunset 2034-06-15 (T).",
    "NY:GOL-5-905: automatic renewal binds only with the 15-30 day personal or registered/certified notice (T).",
    "NY:RPL-232-a, NY:RPL-228, NY:RPL-232-b, NY:COMMONLAW-NYC-monthly-tenant-surrender, NY:ADJ-NYC-monthly-agreed-notice: NYC monthly tenant may leave at any month end without notice (C: T.I.B. affirmed 261 App Div 813; Srinivasan, App Term 2d, 2008, Kings), landlord needs 226-c notice (T).",
    "NY:RPL-232, NY:ADJ-RPL-232-monthly-letting, NY:ADJ-RPL-232-indefinite-term, NY:ADJ-RPL-232-after-october, NY:ADJ-RPL-232-agreement-sets-end, NY:ADJ-RPL-232-oral-term-over-one-year: general monthly letting presumed month to month (C: Gerolemou, App Term 2d, Queens); RPL 232 to the first October 1 only where a longer stay was contemplated (C: Spies); City of New York v State controls over Adina (T/C).",
    "NY:GCN-30, NY:GCN-25(1), NY:GCN-25-a(1)-contract-carveout: month and contract-date counting (T).",
    "NY:RPL-227-e, NY:CASE-Toporek-227-e, NY:RPL-227-e-waiver: mitigation duty, landlord's burden, no actual re-letting required, waiver void (T, C).",
    "NY:ADJ-lease-break-charge: JMD Holding test; never retained from the deposit; not a FARE fee (C).",
    "NY:RPL-227-a(1)-(3), NY:RPL-227-c(1)-(6)(a), NY:MIL-310(2): senior/disabled, domestic violence and NY military terminations with their dates, refunds and penalties (T).",
    "US:50USC3955(a)-(i), US:50USC3917(a), US:50USC3918, US:50USC4042, US:50USC3955(a)(1)-all-parties: SCRA termination, effective dates, proration, no early-termination charge, 30-day prepaid-rent refund, crime to hold deposit for later rent; termination ends the lease for all parties (T; House report quote).",
    "NY:RPL-229, NY:RPL-220: double rent after notice; use and occupancy (T).",
    "NY:ADJ-vacate-order-rent, NY:COMMONLAW-constructive-eviction, US:24CFR982.404(d)(3)-(4): no rent after an owner-caused vacate order or eviction; abated HAP never the family's debt (C: Younger, Barash; T). Apportionment wording in T-vacate: R4B-11.",
    # Step 4-6
    "NY:GOL-7-108(1-a)(d)-notice, NY:GOL-7-108(1-a)(d)-inspection, NY:CASE-Toporek-forfeiture-scope, NY:GOL-7-108(1-a)(g): pre-vacate inspection; only (e) forfeits; actual damages and up to twice the deposit (T, C).",
    "NY:GOL-7-108(1-a)(b)-refundable, NY:GOL-7-108(1-a)(b)-excluded-costs, NY:ADJ-no-fee-retention: four retention categories only; fees refunded (T; C: Colon; RPAPL 702; Freeland).",
    "NY:RPL-238-a(2), (2-a), (3), NY:GOL-5-328(3)(b): late fee after 5 days, lesser of $50 or 5%; returned check only if in lease, greater of actual cost or $20 (T).",
    "NY:RPL-234-a, NY:L2021-c695-s6, NY:L2022-c162, NY:RPL-234, NY:RPL-235-i, NY:RPL-235-c: no legal fees without court order from 2021-12-21; reciprocal fees; keys 110% (T).",
    "NYC:FARE-moveout-service-fee, NYC:FARE-20-699.23(c), NYC:FARE-damages-rent-not-fees: undisclosed move-out service fee may not be charged; rent and damages are not fees (T).",
    "NY:CASE-Mihalow-rent-arrears, NY:CASE-Gelbart-rent-offset, NY:ADJ-early-departure-rent-retention: rent retained only through a timely statement and only rent due and unpaid, up to a new tenant's lease (C: Kunik).",
    "NY:RPL-235-b, NY:RPL-235-a: habitability offset; tenant-paid utility credit (T).",
    "NYC:HMC-27-2056.8-lead-turnover, NYC:HMC-27-2017.5-turnover, NYC:HMC-27-2128-owner-debt: statutory turnover work and HPD charges are the owner's (T).",
    "NYC:HMC-27-2045-detector-charge: occupant reimbursement capped $25/$50/$75 per battery device; private-dwelling smoke exclusions read from (b)(1)(a), (b)(3)(a); combined smoke/CO device in a private dwelling capped at $50 by (e) (T).",
    "US:24CFR982.313(c)-(e), US:24CFR982.451(b)(4), US:24CFR982.311(d)(1), US:24CFR982.313(d)-promptly, US:24CFR982.452(b)(5), US:24CFR983.259(c)-(e), US:24CFR983.352(a), US:24CFR983.353(b): voucher deposit and HAP rules (T).",
    "NYC:HRA-voucher-claim-window, NYC:HRA-voucher-proof, NYC:DSS-SOTA-voucher-claim, NYC:RCNY68-10-14(a), (e), (h), NYC:RCNY31-5-06(a)(10), NYC:RCNY28-1-12(b)-escrow, NYC:HPD-ESCROW-no-owner-draw, NYC:HPD-ESCROW-regulatory-agreement: voucher and escrow deposits (Q).",
    "US:42USC3604(f)(3)(A)-(B) and the two animal rules: accommodation standard; actual damage chargeable (T; C: Goldmark).",
    "NY:GOL-7-108(1-a)(e), NY:GCN-110, NY:GCN-19, NY:GCN-20, NY:GCN-20-event-day, NY:GCN-25-a(1), NY:GCN-24, NY:CASE-Cohen-deadline-count: 14 calendar days excluding the vacate day, next business day after a Saturday, Sunday or public holiday; GCN 24 list read (T, C).",
    "NY:CASE-Urban-vacatur, NYC:CASE-Pezzo-surrender, US:50USC3955-deposit-clock-NY: vacatur date is a fact question informed by the lease; SCRA does not move the NY clock (C/T).",
    "NY:CASE-Bogom-Shanon-written, NY:ADJ-provide-written-dispatch, NY:CASE-Toporek-estimate, NY:CASE-Pickens-provide: written statement, dated by sending (C: Cohen, Urban, Freeland); estimates allowed (C: Toporek). Address/willfulness branch: R4B-03.",
    "US:11USC362(a)(7), US:11USC362(a)(7)-deposit-is-setoff, US:CASE-Strumpf-hold, US:11USC542-refund-payee: tenant bankruptcy setoff stay, temporary hold, refund payee by chapter (T, C).",
    "NY:OSC-MS11-refunds-due, NY:ABP-1315(2), NY:ABP-1422: 3-year dormancy under 1315(2); 90/60-day notices excused where the only address is not current; certified-mail cost deductible (T). ABP 1310 correctly deferred (voluntary disposition only).",
    "NY:COMMONLAW-belongings-owner-keeps, NY:CASE-Facey-belongings, NY:COMMONLAW-belongings-abandonment, NYC:ABANDONED-city-layer, US:50USC3958(a), US:50USC3958-lien-enforcement, US:50USC3951-distress-NY: belongings rules (C: Cretaro, 8902 Corp, Henryka; T).",
    # Step 7
    "NY:GOL-7-108(1-a)(e)-forfeiture, NY:ADJ-forfeiture-claims-survive, NY:CASE-Levine-counterclaim, NY:CASE-Masseroli-separate-claim, NY:CASE-Paterno-commingling-forfeiture, NY:CASE-Paterno-rent-survives, NY:GOL-7-108(1-a)(f): forfeiture of the security only; claims survive; commingling forfeits; landlord's burden (T, C).",
    # Step 8
    "NY:ADJ-lease-balance-not-consumer-credit, NY:CASE-Lefferts-rent-not-consumer-credit, NY:23NYCRR-1.1(d)-not-lease, NY:CPLR-213(2), NY:CPLR-214-i: no appellate decision; text of CPLR 105(f) and GBL 600(1) and Romea support six years today (C/T).",
    "NY:CPLR-214-i-consumer-debt-S9760 and NY:S9760-*: pending act; status re-read 2026-09-29 (not delivered to the Governor); wording in walk R4B-13.",
    "US:15USC1692a(2)-(6) family, US:CASE-Henson-2017, US:CASE-Romea-1998, US:12CFR1006-cmt-2(i)-1, US:12CFR1006.1(c)(1), US:15USC1692a(6)(A), (B), (F)(i), (F)(iii) and their construction rules, US:15USC1692j(a), US:15USC1692o, US:15USC1692o-NY-VA-none, US:15USC1692n: debt and debt-collector coverage by configuration (T; C quotes: Alibrandi, Franceschi, Goldstein, Vincent, Barbato, Wilson, Harris).",
    "US:HANDOFF-config-pre-default, -post-default, -owner-name-only, -principal-purpose, -owns-balance: consistent with each other and with the city and broker configurations (Q).",
    "US:15USC1692b-1692k conduct rules and Regulation F sections cited in 8.3: text matches effect (T).",
    "NYC:CPL-20-700, NYC:CPL-tenant-balance-consumer-debt, NYC:ADC-20-489(d), NYC:RCNY6-5-76-debt-collector (no creditor-employee exclusion in the current definition, read), NYC:RCNY6-5-77(g), NYC:RCNY6-5-76-procedures, NYC:RCNY6-5-77(b)(1)(iv), (e)(1), (f)(1), NYC:RCNY6-5-77(f)(1)-landlord-not-TILA-creditor, US:15USC1602(f), (g) (T).",
    "NYC:SHIELD-effective-date, NYC:SHIELD-operative-date, NYC:SHIELD-penalty-effective-date and SHIELD 5-76/5-77 rules: in force 2027-01-01 (T: City Record notices). Walk wording on electronic consent: R4B-10.",
    "NYC:ADC-20-489(a), (a)(1), (a)(7), NYC:ADC-20-490, NYC:DCA-* configurations: principal-purpose test; city (a)(7)(iii) is limited to secured parties, so no pre-default exclusion in the city licence (T).",
    "NYC:ADC-20-493.2(a), (b), NYC:RCNY6-2-190(b), NYC:RCNY6-2-191(a), NYC:ADC-20-493.1(b) (T).",
    "NY:RPL-440(1)-rent-collection, NY:ADJ-broker-owner-and-staff, NY:RPL-442-f-exemptions, NY:RPL-442-d-442-e-unlicensed, NY:RPL-442-fee-split, NY:HANDOFF-broker-config-*: collecting rent for another for a fee is the licensed act; exemptions closed; penalties (T; C: Weingast, Fields, G.C. Fortune, Futersak).",
    "US:15USC1681s-2 and Regulation V rules, US:12CFR1006.30(a), (b), US:11USC362(a)(6), US:11USC524(a)(2), US:50USC3931(b)(1), NY:CPLR-3215(g)(3) (T).",
    "NY:LLC-808(a)-foreign-authority, NY:BCL-1312(a)-foreign-authority: curable bar to suing (T). LLC 206: R4B-04.",
    "NY:CPLR-5001(a)-(b), NY:CASE-NML-contract-rate, NY:ADJ-lease-interest-on-rent, NY:CPLR-5004(a)-consumer-2pct: interest as of right; contract rate to judgment; lease interest on rent within 238-a; 2% consumer-debt rate for natural-person defendants on judgments from 2022-04-30 and unpaid parts of earlier judgments (T).",
    "NYC:ADC-27-2107(b)-rent-stay, NY:CPLR-3015(e)-licence-pleading: discretionary stay; licence pleading (T). Scope wording: R4B-08.",
]

TEST_CASES = """\
All dates computed with Python's calendar; public holidays from GCN 24 as saved.

| Case | My answer (from the law) | Walk | Difference |
|---|---|---|---|
| C3 | 7-108(1-a) applies (lease 2023). Statement by email within 14 days after vacating (vacate day excluded; next business day if day 14 is a Saturday, Sunday or GCN 24 holiday). Refund in the same 14 days: deposit plus bank interest less 1% a year, less only unpaid rent due, tenant damage beyond wear, lease utilities, moving/storage; no fees retained; no painting for ordinary wear (multiple-dwelling 3-year cycle). | Same | None |
| C4 | Three-family house: fewer than six units, so no stabilization route unless J-51/421-a; controlled only if a tenancy continuous since before 1971-07; no interest account required (building test); bank notice and interest less 1% if banked; multiple dwelling: 3-year repaint and records, HPD registration, certificate of occupancy (no rent for any period occupied as a post-1929 conversion without a permanent or in-force temporary certificate), rent-impairing violations. | Same, but omits the temporary-certificate branch | R4B-06 |
| C5a | Rent accepted after the 2018 lease expired: month-to-month renewal tenancy entered after 2019-07-14; 7-108(1-a) applies; tenant may leave at any month end without notice; landlord needs 226-c notice. | Same | None |
| C6 | Rent after departure limited by the re-letting duty (landlord's burden); DV, senior, NY military and SCRA terminations end rent on their statutory dates and bar early-termination charges; auto-renewal binds only with GOL 5-905 notice; clock runs from vacating; statement keeps only rent due and unpaid before any new lease; a lease-break sum only if valid liquidated damages and never from the deposit. | Same | None |
| C7 | Timely statement itemizing estimates; excess is a separate claim surviving forfeiture; no legal fees without a court order; interest 2% (natural person) or the lease rate for non-rent amounts until judgment; rent barred for certificate/RIV periods and suspended while an MD owner is unregistered; six years to sue; entity owner may use commercial claims only if its principal office is in NY and the tenant is still in NYC; an unpublished NY LLC must cure before suing. | Same except the forum and LLC-publication branches | R4B-04, R4B-05 |
| C8 | No statement until the second co-tenant leaves; statement to each; joint refund if one undifferentiated deposit, proportional if records show shares. | Same | None |
| C9 | Statement and refund to the vacated unit within 14 days; refund stays trust money; reported under ABP 1315(2) after 3 years; ABP 1422 notice excused (only address is not current). | Same | None |
| C10 | Turnover within 5 days of the deed with registered/certified notice; buyer liable (and liable with actual knowledge even if not turned over); a multiple-dwelling buyer recovers no rent until registered (successor filing within 30 days, MDL 325(1)); a one- or two-family buyer faces only the discretionary stay. | Omits building type | R4B-12 |
| C11 | Belongings stay the tenant's; not held for rent; released on request; disposal only on abandonment; reasonable moving/storage retained under 1-a(b); servicemember: court order before enforcing a lien. | Same | None |
| C12 | Vacated Friday 2026-12-11; day 14 is Friday 2026-12-25 (Christmas, GCN 24); Saturday 26 and Sunday 27 skipped; due Monday 2026-12-28. | Same | None |
| C13 | Only the tenant share is charged; owner keeps the move-out month's HAP and nothing after; written list and refund within the 14 days. | Same | None |
| C14 | Agency: federal debt collector (post-default hand-off; regular collection); DCWP licence; broker licence for the rent part (or an attorney); validation notice within 5 days to an address where she receives mail; verification with lease and statement; six-year limit today; 2% interest; 23 NYCRR 1 inapplicable; before suit check certificate, registration, RIVs; SHIELD validation applies if the notice is first due on or after 2027-01-01. | Same | None |
| C15 | Filing on day 5: setoff of the deposit against pre-petition charges stayed; landlord may hold only the disputed amount while it promptly moves for relief; statement by day 14 (2 weeks from vacating) with no payment demand; the rest to the chapter 7 trustee (or the debtor in chapter 13), payment to the debtor after notice does not discharge. | Same | None |
| T-232 | (a) Monthly letting: month to month; she left at a month end; nothing after June; no July rent retained; vacated Tuesday 2026-06-30, statement due Tuesday 2026-07-14. (b) 'A long time': RPL 232 term to 2026-10-01; July rent (due Wednesday 2026-07-01, unpaid on the statement date) retainable if no new tenant's lease had begun; August and September are a later claim subject to 227-e. | Same | None |
| T-vacate | No rent falling due after 2026-03-10 (Tuesday); none retained for it; rent before the order owed subject to 235-b. Whether the post-order days of the March installment are refunded is not decided by the cited cases. | States a day-count refund | R4B-11 |
| T-lead | Pre-1960 two-family, one unit rented: a 'private dwelling' under art. 14 and 27-2045; lead turnover work is the owner's cost, not deductible; a combined smoke/CO device the tenant removed is charged at most $50 (and not above actual cost). No MDL rent bars, no HPD registration (owner-occupied), no 3-year repaint duty. | Same | None |
| T-collect | Handoff demanding or receiving rent for a fee needs a broker licence; settlement-only with the licensed manager demanding and receiving does not; a damage-only balance needs no broker licence. City licence and FDCPA follow their own configurations. | Same | None |
"""

METHOD = """\
- Grounding read: APERTURE.md, STAGE_A.md, the whole walk (814 lines).
- Script review/ir4b_dump.py wrote a side-by-side dump of all 414 cited rules (walk lines, every field, construction
  quotes, reasoning); all 9,530 lines were read.
- Sources read in context for the rules that decide amounts, dates, forfeiture, damages, payees and regime:
  GOL 7-103, 7-105, 7-108; MDL 301, 302, 302-a, 325; Admin. Code 27-2045, 27-2056.8, 27-2107, 20-489, 20-699.22;
  6 RCNY 5-76; SHIELD 5-77(b)(5); CPLR 5004; RPL 214, 232, 236; GCN 24; CCA 1801-A, 1809; ABP 1310, 1315, 1422;
  LLC Law 206. Decisions read in the saved text: Prando, Case v 575 Classon, Kunik, Holmes v Worthen, Gerolemou,
  Srinivasan, Younger, 1700 First Ave. Construction quotes of the other interpretive rules were read in the dump.
- Contrary and later authority searched through the CourtListener v4 search API (queries on 7-108 willfulness and
  delivery, CPLR 5004 and 214-i for rent, MDL 302/325, RPL 232, LLC 206, CCA 1809/1801-A, 7-103 trusts in
  bankruptcy). New sources saved with prefix REVIEW4B_ (Small Step Day Care; Shoreview; Reyes v Scherrer;
  In re Trafalgar Associates; 11 USC 507; National Arbitration v Schwartzberg; 2505 Victory; 49 Bleecker; the
  A10182 Assembly status page).
- Checks run: stage_a_check.py (0 errors in all four files), check_review.py (507 in scope; 412 cited; 95 deferred),
  review/ir4b_verify.py (every evidence quote verbatim, whitespace-normalized; every rule id exists; self-test
  with a planted bad quote and bad id).
- Findings were written before any earlier review, disposition or sweep file was opened.
"""


def render(o):
    F = o["findings"]
    sev = {s: sum(1 for f in F if f["severity"] == s) for s in ("critical", "major", "minor")}
    kinds = {}
    for f in F:
        kinds[f["kind"]] = kinds.get(f["kind"], 0) + 1
    L = []
    L.append("# Independent review 4B: correctness of the NYC market-rate walk\n")
    L.append("Reviewer 4B, 2026-09-29. Report only; no rule file, walk, source or skill was edited.\n")
    L.append("## Summary\n")
    L.append(f"- Rules checked: {o['rules_checked_count']} cited rules (all read side by side in the dump); 94 interpretive rules re-decided.")
    L.append(f"- Findings: {len(F)} ({sev['critical']} critical, {sev['major']} major, {sev['minor']} minor).")
    L.append("- By kind: " + ", ".join(f"{k} {v}" for k, v in sorted(kinds.items())) + ".")
    L.append("- Judgment: **accept after listed corrections.** The statutory core (cap, retention list, 14-day "
             "count, forfeiture, damages, interest rate, holidays, voucher, SCRA, FDCPA coverage, licensing) is "
             "stated correctly. Three critical corrections are needed before acceptance: the owner-bankruptcy "
             "deposit rule lacks the tracing condition (R4B-01); the walk's definition of a stabilized unit drops "
             "the co-op/condo conversion exception (R4B-02); and the walk states as law that a manager's wait for an "
             "address is willful, which no authority holds (R4B-03). Three major corrections concern suing: LLC "
             "publication (R4B-04), the commercial claims conditions (R4B-05) and temporary certificates of "
             "occupancy (R4B-06).\n")
    L.append("## Findings (most severe first)\n")
    for f in F:
        L.append(f"### {f['id']} ({f['severity']}, {f['kind']})\n")
        L.append(f"- Rules: " + ", ".join(f"`{r}`" for r in f["rule_ids"]))
        L.append(f"- Walk step: {f['step']}")
        L.append(f"- What is wrong: {f['finding']}")
        L.append(f"- Correct rule: {f['correct_rule']}")
        L.append("- Evidence:")
        for e in f["evidence"]:
            L.append(f"  - `{e['source_file']}`: \"{e['quote']}\"")
        L.append("")
    L.append("## Confirmed\n")
    L.append("Basis codes: T = statute or regulation text read in the saved source; C = cited decision read in the "
             "saved source; Q = quote and effect read side by side in the full dump.\n")
    for c in o["confirmed"]:
        L.append(f"- {c}")
    L.append("\n## Test cases\n")
    L.append(TEST_CASES)
    L.append("## New versus earlier rounds\n")
    L.append(EARLIER)
    L.append("\n## Method\n")
    L.append(METHOD)
    return "\n".join(L) + "\n"


EARLIER = """\
Written after the findings above were saved and verified; the earlier reviews, dispositions and sweep files were
opened only then.

New (no earlier round raised them): R4B-01 (tracing of the deposit in an owner bankruptcy), R4B-02 (GBL 352-eeee
conversion exception dropped from the walk's definition of a stabilized unit), R4B-06 (temporary certificates of
occupancy; the 301(1)(b) combined-apartments branch), R4B-07 (MDL 325(2) voluntary-payment clause; round 3 added the
parallel 302-a clause only), R4B-10 (SHIELD 60-day own-use branch), R4B-14 (421-a route), R4B-15 (residual hedges).

Disagreements with earlier corrections:
- R3-10 (manager's wait for an address is willful): over-corrected. Round 3 rightly removed 'an unknown new address'
  from the examples of innocent misses, but restating the wait as willful as a matter of law goes past every cited
  authority; the correct rule states the charged knowledge and leaves the finding to the trier (R4B-03).
- R3-08 (LLC Law 206 'not a ground to dismiss'): incorrect in part. 1700 First Ave. holds only that the defect is
  not jurisdictional; Small Step Day Care (2d Dept 2016) holds an unpublished LLC cannot maintain an action until it
  cures (R4B-04).
- R1-14, rated 'correct and complete' by round 2: incomplete. The commercial claims part requires a New York
  principal office and a defendant in the City (R4B-05).
- R2-03 (27-2107(b) 'limited to one- and two-family houses'): over-limited. 27-2107(b) reaches every owner required
  to register; for a multiple dwelling MDL 325(2) is the stricter bar and both apply (R4B-08).
- R3-11 (T-vacate day-count refund of March rent): unsupported by the cited cases (R4B-11).

Carried over (corrected in the rules, not fully in the walk): R3-04's common-area branch of MDL 302-a is in the rule
but not in walk 0.5 (R4B-09); rounds 2 and 3 recorded that S9760/A10182-A was not delivered to the Governor, but walk
8.1 still says it 'awaits the Governor' (R4B-13); C10 still omits the building type after R3-03 (R4B-12).

Corrections this review confirms as correct: R3-03 (registration is a suspension), R3-04 (302-a exceptions), the
RPL 232 rulings (monthly letting presumed month to month; RPL 232 only for a contemplated longer stay), R1-14's CCA
1803-A demand-letter rule, R2-05's two-part willfulness structure, and R1-01 (2% CPLR 5004 rate; contract rate to judgment).
"""
