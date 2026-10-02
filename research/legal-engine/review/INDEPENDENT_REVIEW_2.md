# Independent review 2: settling a market-rate tenancy in New York City

Reviewer: independent reviewer 2, 2026-09-29. Report only; no rule file, walk or existing source was edited. Findings are machine-checked by `python3 review/ir2_verify.py` (every evidence quote verbatim in its saved source, every rule id exists, self-test catches a planted bad quote and a planted bad id). The findings live in `review/independent_review_2.json`; this file is rendered from it by `review/ir2_render.py`.

## Summary

- Findings: 13. By severity: critical 2, major 5, minor 6. By kind: alignment 1, gap 6, misstatement-in-review 4, stale-source 2.
- Confirmed: 27 rulings and high-consequence rule groups verified against source (listed below).
- Judgment: **accept after the listed corrections.**

The walk is sound where it matters most for the 14-day settlement itself: the regime by lease date, the cap, the trust and interest rules, the count of the 14 days, what may be kept, the written statement and where to send it, forfeiture of the security but not the debt, co-tenants, belongings, and the federal and city collection layers all check out against their sources. What is wrong sits at the edges of the chain, where the manager decides whether rent can be recovered at all and for how long. The files never ask whether the building has a lawful certificate of occupancy, and without one no rent or use and occupancy can be recovered for that period (MDL 302, R2-01). That changes the amount on the statement and the pursue-or-write-off decision for exactly the small, often converted, buildings this customer manages. The six-year limit is current law, but a bill that makes it three years for lease balances passed both houses in June and is waiting on the Governor (R2-02). Two statements in the walk would mislead an operator: unregistered multiple-dwelling owners are barred, not merely stayable (R2-03), and the high-rent exemption from Good Cause Eviction is missing (R2-04). The walk's one-line definition of 'willful' overstates exposure on every managed account (R2-05). Lease-break charges and the rent a deposit may cover after an early departure have no rule (R2-06, R2-07). None of these reopens the core rules; each is a bounded addition or restatement.

## Findings (most severe first)

### R2-01 (critical, gap)

- Step: 0, 1.8, 5.5, 8.10; test cases C4, C7, C14
- Rules affected: `NY:GOL-7-108(1-a)(b)-refundable`, `NY:CASE-Mihalow-rent-arrears`, `NY:CPLR-5001(a)-(b)`, `NYC:ADC-27-2107(b)-rent-stay`, `NY:RPL-220`
- What is wrong: No rule states Multiple Dwelling Law 301-302. In New York City a multiple dwelling (three or more families, including a house certified for one or two families that is actually occupied by three or more, a 'de facto multiple dwelling') may not be occupied without a residential certificate of occupancy, and while it is so occupied the owner recovers no rent and no use and occupancy for that period. The walk treats unpaid rent as always retainable from the deposit (5.5) and always suable (8.10, C14), and never asks the certificate-of-occupancy question, although illegal third units in two-family houses are common in the scattered small-multifamily segment Handoff serves. The coverage note in NYC.json says 'MDL is state, not read', and NY.json has no MDL atom, so the gap is in both files.
- Correct law: NY:MDL-302(1)(b) (new, RULE with a STANDARD exception). Condition: the unit is in a multiple dwelling (MDL 4(7): occupied or let as the residence of three or more families living independently), including a de facto multiple dwelling, and during the period claimed the dwelling was occupied without a certificate of occupancy permitting that residential use (MDL 301(1)); the unit is not in an interim multiple dwelling whose owner is in compliance with the Loft Law (MDL 285(1)). Effect: the owner may not recover rent or use and occupancy for that period by action, counterclaim, setoff or by applying the deposit to it; on the 14-day statement no amount may be retained for rent of that period; damage and other non-rent claims are unaffected. The bar is absolute (Caldwell, 2d Dept 2008; followed by 49 Bleecker, 1st Dept 2018; Chazon, Court of Appeals 2012, reads the text as it stands); the only exception is a tenant who actually prevented the owner from legalizing (Chatsworth 72nd St. v Rigai, Court of Appeals 1975, as stated in Caldwell). Obtaining a certificate later does not revive rent for the period of unlawful occupancy. Order of authority: MDL 302 is a state statute and controls over any lease term; the Appellate Division rule binds the Civil Court in both departments.
- Evidence:
  - `sources/REVIEW2_NY_MDL_302_nysenate.txt`: "No rent shall be recovered by the owner of such premises for said period, and no action or special proceeding shall be maintained therefor, or for possession of said premises for nonpayment of such rent."
  - `sources/REVIEW2_NY_MDL_4_nysenate.txt`: "is occupied as the residence or home of three or more families living independently of each other."
  - `sources/REVIEW2_NY_CASE_Caldwell_v_AmericanPackage_2008_2dDept.txt`: "The command of Multiple Dwelling Law § 302 (1) (b) is, by its terms, absolute."
  - `sources/REVIEW2_NY_CASE_Caldwell_v_AmericanPackage_2008_2dDept.txt`: "An owner of a de facto multiple dwelling who fails to obtain a proper certificate of occupancy or comply with the registration requirements of the Multiple Dwelling Law cannot recover for rent or money for use and occupancy"
  - `sources/REVIEW2_NY_CASE_Caldwell_v_AmericanPackage_2008_2dDept.txt`: "where the tenant actually interfered with the owner's"
  - `sources/REVIEW2_NY_CASE_49Bleecker_v_Gatien_2018_1stDept.txt`: "was precluded from charging respondents rent or other remuneration while the building lacked a certificate of occupancy for residential use"
  - `sources/REVIEW2_NY_CASE_Chazon_v_Maugenest_2012_CoA.txt`: "In the absence of compliance, the law's command is quite clear"

### R2-02 (critical, stale-source)

- Step: 8.1, 8.5, 8.6; test cases C7, C14
- Rules affected: `NY:ADJ-lease-balance-not-consumer-credit`, `NY:CPLR-213(2)`, `NY:CPLR-214-i`, `NY:CASE-Lefferts-rent-not-consumer-credit`, `NYC:SHIELD-5-77(i)`, `NYC:ADC-20-493.2(b)`
- What is wrong: The walk states flatly that the landlord has six years to sue because a lease balance is not consumer credit. That is the law today, but the Consumer Debt Uniformity Act (S9760 / A10182-A) passed the Senate on 2026-06-02 and the Assembly on 2026-06-03 and awaits delivery to the Governor. It adds CPLR 105(f-1) 'consumer debt' (a purpose test, like CPLR 5004(b)) and rewrites CPLR 214-i to 'actions arising out of consumer debt'. A residential lease balance sued for in a plenary action is a consumer debt under that definition (only obligations sought in an RPAPL article 7 summary proceeding are excluded), so on the 90th day after the bill becomes law the limit for suing a former tenant who is a natural person becomes three years, and the consumer-credit pleading, default and affidavit rules (CPLR 3016(j), 3215(j)) follow. No rule records this point-in-time change; the files' family-5 check was run before passage and nothing flags it.
- Correct law: NY:CPLR-214-i-consumer-debt (new, point-in-time). Effective_from: the 90th day after S9760/A10182-A becomes law (not yet law on 2026-09-29; the Governor acts after delivery, 10 days excluding Sundays, or 30 days if delivered after adjournment). Condition: an action (not a summary proceeding) against a natural person for a residential lease balance commenced on or after that date. Effect: must be commenced within three years of accrual; CPLR 105(f-1) displaces NY:ADJ-lease-balance-not-consumer-credit for the limitations period; collectors' limitations procedures (SHIELD 5-77(i), Admin Code 20-493.2(b)) then measure time-barred status by three years. Until then CPLR 213(2) (six years) governs. The rule file should carry both versions with dates, and the walk should state the six-year rule as current law with the enacted-but-unsigned change named.
- Evidence:
  - `sources/REVIEW2_NY_S9760_A10182A_ConsumerDebtUniformityAct_2026.txt`: "consumer debt to be commenced within three years. An action arising out"
  - `sources/REVIEW2_NY_S9760_A10182A_ConsumerDebtUniformityAct_2026.txt`: "include an obligation or alleged obligation to pay money when sought"
  - `sources/REVIEW2_NY_S9760_A10182A_ConsumerDebtUniformityAct_2026.txt`: "This act shall take effect on the ninetieth day after it shall"
  - `sources/REVIEW2_NY_S9760_A10182A_ConsumerDebtUniformityAct_2026.txt`: "PASSED SENATE"
  - `sources/REVIEW2_NY_S9760_A10182A_ConsumerDebtUniformityAct_2026.txt`: "passed assembly"
  - `review/NYC_MARKET_RATE.md`: "and the landlord has six years to sue, not three"

### R2-03 (major, misstatement-in-review)

- Step: 1.8, 8.10; test cases C7, C14
- Rules affected: `NYC:ADC-27-2107(b)-rent-stay`, `NYC:ADC-27-2097-registration`
- What is wrong: The walk says an unregistered owner's rent claim 'can be stayed' at the court's discretion. That is the city rule (Admin Code 27-2107(b)). For a multiple dwelling the state rule is mandatory: MDL 325(2) says no rent shall be recovered by an owner who has not complied with the city's registration requirement until he complies. Only a one- or two-family house that must register because neither the owner nor a family member lives there falls under the discretionary city stay alone. The state statute is the higher authority and the stricter one, so it governs multiple dwellings.
- Correct law: NY:MDL-325(2) (new, RULE). Condition: the unit is in a multiple dwelling in New York City and the owner has not filed the HPD registration Admin Code 27-2097 requires. Effect: the owner recovers no rent, by action or proceeding, until it registers; registration is a precondition, not a discretionary stay. A non-owner-occupied one- or two-family house remains under NYC:ADC-27-2107(b)-rent-stay (discretionary stay). In both cases the operator registers before suing or referring for suit; damage claims are not claims for rent.
- Evidence:
  - `sources/REVIEW2_NY_MDL_325_nysenate.txt`: "no rent shall be recovered by the owner of a multiple dwelling who fails to comply with such registration requirements until he complies with such requirements."
  - `sources/REVIEW1_NYC_ADC_27-2107.txt`: "in the discretion of the court, suffer a stay of proceedings to recover rents, during such period"
  - `review/NYC_MARKET_RATE.md`: "If the owner had to register and has not, the court may stay its claim for rent until it registers."

### R2-04 (major, misstatement-in-review)

- Step: 3.1
- Rules affected: `NY:RPL-214`, `NY:RPL-215`, `NY:RPL-211(3)-small-landlord`
- What is wrong: The walk and NY:RPL-214 list Good Cause Eviction exemptions as 'include' and omit the one most likely to decide a market-rate NYC unit: a unit whose monthly rent exceeds 245 percent of HUD fair market rent (RPL 214(15)). They also omit units regulated under other law or income-restricted by regulatory agreement (214(5)-(6)), an owner-occupied unit sublet under 226-b recovered for personal use (214(3)) and employment housing (214(4)). An operator reading the list would treat a high-rent unit as covered and fail to treat a tenant who stays after a proper 226-c non-renewal as a holdover owing use and occupancy.
- Correct law: NY:RPL-214(15) (add to NY:RPL-214 as an exemption branch). Condition: NYC unit whose monthly rent is greater than 245 percent of the HUD fair market rent for its county and unit type, as DHCR publishes it by August 1 each year. Effect: article 6-A does not apply; the tenancy ends as RPL 226-c and the lease provide, and a tenant who stays after a proper non-renewal is a holdover (RPL 220 use and occupancy; RPL 229 only if the tenant gave notice). The complete exemption list is 214(1)-(15); the walk should name the high-rent test and say the list is complete in the rule.
- Evidence:
  - `sources/REVIEW1_NY_RPL_214_nysenate.txt`: "or two hundred forty-five percent of the fair market rent"
  - `sources/REVIEW1_NY_RPL_214_nysenate.txt`: "unit on or within a housing accommodation where such unit is otherwise subject to regulation of rents or evictions pursuant to local, state or federal law, rule, or regulation"
  - `review/NYC_MARKET_RATE.md`: "Exempt units include those of a small landlord (ten units or fewer in the state, counted through every natural-person owner)"

### R2-05 (major, misstatement-in-review)

- Step: 7.5
- Rules affected: `NY:ADJ-willful-standard`, `NY:CASE-Karole-willful`, `NY:CASE-Prando-willful`, `NY:CASE-Bogom-Shanon-willful`, `NY:GOL-7-108(1-a)(g)`
- What is wrong: The walk defines 'willful' as 'knew or should have known its conduct broke the law' and says any account a manager or Handoff handles cannot defend with ignorance. Read literally, every late statement on a managed account is willful and exposes the owner to up to twice the deposit, because a professional always 'should have known' the 14 days had run. That is not the law. The authority the rule adopts (Karole) starts from the settled meaning that willful conduct is 'not merely negligent' and 'requires more than inadvertence', and the Appellate Term upheld a finding that a late return was 'innocent', not willful (Prando). The 'should have known' formula in the prevailing-wage cases goes to knowledge of the law, not to accidental failures. The rule file's effect keeps 'more than inadvertence or accident'; the walk drops it.
- Correct law: NY:ADJ-willful-standard (restate). Willful = a knowing, intentional or deliberate failure, or reckless disregard of the statute; negligence and inadvertence are not willful (Karole, applying McLaughlin v Richland Shoe; Prando, App Term 2d). Knowledge of the law is charged to an experienced landlord or its managing agent and imputed to the owner, so a deliberate choice to keep the deposit without a timely written statement is willful whatever the landlord's reading of the law (Karole; Bogom-Shanon). A miss caused by an inadvertent error despite a working process (misdated send, a failed delivery, an unknown fact such as the tenant's new address) is not willful, even for a manager. The amount is discretionary 'up to' twice the deposit. The tenant proves willfulness; it is a finding of fact.
- Evidence:
  - `sources/NY_CASE_Karole_v_340WEnd_2022.txt`: "it is generally understood to refer to conduct that is not merely negligent"
  - `sources/NY_CASE_Karole_v_340WEnd_2022.txt`: "requires more than inadvertence"
  - `sources/NY_CASE_Prando_v_Kelly_2021.txt`: "not willful, and, thus, that punitive damages were not warranted"
  - `review/NYC_MARKET_RATE.md`: ""Willful" means the landlord knew or should have known its conduct broke the law"

### R2-06 (major, gap)

- Step: 3.3, 5.2; test case C6
- Rules affected: `NY:RPL-227-e`, `NY:RPL-227-e-waiver`, `NY:RPL-235-c`, `NY:ADJ-no-fee-retention`, `NY:GOL-7-108(1-a)(b)-refundable`
- What is wrong: Many NYC leases carry an early-termination ('lease break') charge or a liquidated-damages clause. The walk reaches such clauses only through unconscionability (RPL 235-c), which is the wrong primary test and gives the operator no rule. The Court of Appeals test for liquidated damages decides whether the charge is owed at all, and RPL 227-e decides whether it can displace mitigation.
- Correct law: NY:CASE-liquidated-damages-lease (new, MIXED). Condition: the lease fixes a sum payable on early departure. Effect: (a) the clause is enforceable only if, when the lease was made, the sum bore a reasonable proportion to the probable loss and the actual loss was difficult to estimate; a sum plainly disproportionate to the probable loss is a penalty and unenforceable, and the landlord is left to proven damages (Truck Rent-A-Center, as restated in JMD Holding, Court of Appeals 2005); (b) a clause that makes the tenant pay rent for the rest of the term whatever the landlord does to relet, or otherwise exempts the landlord from mitigation, is void (RPL 227-e); (c) an enforceable liquidated sum is damages, not rent, a utility charge or damage to the unit, so it is not retained from the deposit under 7-108(1-a)(b) and is pursued as a claim (NY:ADJ-no-fee-retention reasoning); (d) it is not a FARE Act 'fee' because it is not a charge for services (NYC:FARE-damages-rent-not-fees). Judgment on proportionality.
- Evidence:
  - `sources/REVIEW2_NY_CASE_JMD_Holding_v_Congress_2005_CoA.txt`: "A contractual provision fixing damages in the event of breach will be sustained if the amount liquidated bears a reasonable proportion to the probable loss and the amount of actual loss is incapable or difficult of precise estimation."
  - `sources/REVIEW2_NY_CASE_JMD_Holding_v_Congress_2005_CoA.txt`: "If, however, the amount fixed is plainly or grossly disproportionate to the probable loss, the provision calls for a penalty and will not be enforced"
  - `sources/NY_RPL_227-E.txt`: "Any provision in a lease that exempts a landlord's duty to mitigate damages under this section shall be void as contrary to public policy."
  - `review/NYC_MARKET_RATE.md`: "A court may refuse to enforce an unconscionable clause (for example a move-out fee or cleaning schedule)"

### R2-07 (major, gap)

- Step: 3.3, 5.5, 6.1; test case C6
- Rules affected: `NY:GOL-7-108(1-a)(b)-refundable`, `NY:GOL-7-108(1-a)(e)`, `NY:RPL-227-e`, `NY:CASE-Gelbart-rent-offset`
- What is wrong: When a tenant leaves before the lease ends, the operator must decide at day 14 how much rent the deposit may cover. No rule says. The walk (C6) says only that the clock runs from vacating. The statute lets the landlord retain the reasonable, itemized cost 'due to non-payment of rent' and return the rest within 14 days; rent for months that have not yet fallen due has not gone unpaid, and holding the deposit against it would defeat the 14-day return. The Appellate Term allowed an offset of rent that accrued after vacating up to the day the new tenant's lease began.
- Correct law: NY:ADJ-early-departure-rent-retention (new, RULE). Condition: tenant vacated before the lease ended; unit under 7-108(1-a). Effect: the 14-day statement may retain rent that fell due under the lease and was unpaid by the date the statement is sent, including rent falling due after vacating, but only for periods before a new tenant's lease took effect (RPL 227-e ends the old lease then; Kunik, App Term 2d 2023). Rent for periods not yet due on the statement date may not be retained; it is claimed later against the tenant, subject to mitigation and the landlord's burden (RPL 227-e). The balance of the deposit is returned within the 14 days.
- Evidence:
  - `sources/NY_GOL_7-108_nysenate.txt`: "shall return any remaining portion of the deposit to the tenant"
  - `sources/REVIEW2_NY_CASE_Kunik_v_ClubAtPearlRiver_2023_AppTerm2d.txt`: "plaintiffs remained liable for rent from July 1, 2021 to July 14, 2021, which amount defendant could offset from the security"
  - `review/NYC_MARKET_RATE.md`: "The deposit clock still runs from vacating."

### R2-08 (minor, gap)

- Step: 3.2
- Rules affected: `NY:COMMONLAW-NYC-monthly-tenant-surrender`, `NY:RPL-232-c`
- What is wrong: RPL 232 is not atomized (it is absent from NY.json's read and out lists). In New York City an occupancy agreement that does not specify its duration runs until the next October 1. It fixes when an oral or open-ended tenancy (common with small owners) ends and how much rent is owed if the tenant leaves earlier; only after acceptance of rent past that date does the month-to-month rule of 232-c and T.I.B. take over.
- Correct law: NY:RPL-232 (new, RULE). Condition: NYC unit; the agreement for occupancy does not particularly specify its duration. Effect: the tenancy continues until the first October 1 after possession began; rent runs to that date, subject to mitigation if the tenant leaves early (RPL 227-e); a holdover after it with rent accepted is month to month (RPL 232-c).
- Evidence:
  - `sources/REVIEW2_NY_RPL_232_nysenate.txt`: "shall be deemed to continue until the first day of October next after the possession commences under the agreement."

### R2-09 (minor, gap)

- Step: 6.8; test case C9
- Rules affected: `NY:OSC-MS11-refunds-due`, `NY:ABP-1315(2)`
- What is wrong: Before an unclaimed refund is reported to the Comptroller, the holder must mail the owner a due-diligence notice, and a second one by certified mail when the amount exceeds $1,000. No rule states this. The notice is excused when the holder has no address or its only address is known not to be current, which is the C9 facts (vacated unit), but not when a refund check sent to a forwarding address goes uncashed.
- Correct law: NY:ABP-1422 (new, RULE). Condition: an unclaimed deposit refund is to be reported under ABP 1315. Effect: not less than 90 days before the reporting date, send the tenant written notice by first-class mail at the address in the holder's records; if the amount exceeds $1,000, send a second notice by certified mail, return receipt requested, not less than 60 days before the reporting date. Not required where the holder has no address or can show its only address is not the tenant's current address, or (second notice) where the tenant claimed or the first notice came back undeliverable.
- Evidence:
  - `sources/REVIEW2_NY_ABP_1422_justia.txt`: "not less than ninety days prior to the applicable reporting date for such unclaimed property, a written notice by first-class mail"
  - `sources/REVIEW2_NY_ABP_1422_justia.txt`: "send a second written notice to the owner by certified mail, return receipt requested"
  - `sources/REVIEW2_NY_ABP_1422_justia.txt`: "the holder can demonstrate that the only address that the holder has pertaining to the owner is not the current address of the owner"

### R2-10 (minor, gap)

- Step: 8.1, 8.3; test case C14
- Rules affected: `NY:ADJ-lease-balance-not-consumer-credit`, `NY:GBL-600(1)`
- What is wrong: The walk says GBL art. 29-H does not reach a lease balance but is silent on the DFS debt-collection regulation (23 NYCRR Part 1), which a third-party collector in C14 would otherwise follow. Its 'debt' definition also requires credit extended, so on the files' own ruling it does not apply to a lease balance. A proposed amendment (2021, revised 2022) has not been adopted; the current text governs.
- Correct law: NY:23NYCRR-1.1(d)-not-lease (new, RULE). Condition: a third-party collector or debt buyer collects a former tenant's lease balance. Effect: 23 NYCRR Part 1 does not apply, because 'debt' there means an obligation arising from a transaction in which credit was extended, and a lease balance is not credit (same reasoning as NY:ADJ-lease-balance-not-consumer-credit). The FDCPA, Regulation F and the city rules apply on their own terms.
- Evidence:
  - `sources/REVIEW2_NY_23NYCRR_1.1_justia.txt`: "which arises out of a transaction wherein credit has been extended to a consumer"

### R2-11 (minor, misstatement-in-review)

- Step: 8.9
- Rules affected: `NY:CPLR-3215(g)(3)`
- What is wrong: CPLR 3215(g)(3)(iii) exempts the small claims part from the additional-mailing requirement. The walk and the rule state the mailing as universal. It still applies in the commercial claims part and in plenary Civil Court actions.
- Correct law: NY:CPLR-3215(g)(3) (add branch). The 20-day 'personal and confidential' mailing and affidavit apply to a default judgment against a natural person on a contractual obligation, except in the small claims part of any court and in summary proceedings.
- Evidence:
  - `sources/REVIEW1_NY_CPLR_3215_justia.txt`: "This requirement shall not apply to cases in the small claims part of any court"

### R2-12 (minor, stale-source)

- Step: 1.8, 8.10
- Rules affected: `NYC:ADC-27-2107(b)-rent-stay`, `NYC:ADC-27-2097-registration`
- What is wrong: Provenance defect in rules added after review 1. The two HPD rules carry source_url codelibrary ...0-0-0-60000 while the saved files were cut from XML sections 0-0-0-61160 (27-2097) and 0-0-0-61209 (27-2107). The wording matches, so no rule changes. (CPLR 3215 and RPL 211 rest on Justia copies; nysenate.gov still returns 'not found' for both on 2026-09-29, so that choice stands, and the instrument field says so.)
- Correct law: Re-point each HPD rule's source_url to the section actually saved.
- Evidence:
  - `sources/REVIEW1_NYC_ADC_27-2107.txt`: "SOURCE: https://codelibrary.amlegal.com/codes/newyorkcity/latest/NYCadmin/0-0-0-61209"
  - `stage-a/NYC.json`: "https://codelibrary.amlegal.com/codes/newyorkcity/latest/NYCadmin/0-0-0-60000"

### R2-13 (minor, alignment)

- Step: front matter; 1.5-1.8
- What is wrong: The walk asks Owen to accept that the rules are the law 'with nothing missing'; R2-01, R2-02 and R2-06 to R2-10 show that is not yet true. It also still says the corrections were 'each verified against its source', which is provenance an operator does not need. Step 1 numbers run 1.5, 1.8, 1.6, 1.7. Otherwise the walk is plain, ordered by the decision chain and states rules without hedging.
- Correct law: Drop the provenance sentence, renumber Step 1, and state acceptance after the listed corrections are applied.
- Evidence:
  - `review/NYC_MARKET_RATE.md`: "That these rules are the law for this chain, stated correctly, with nothing missing."

## Confirmed

Each item was checked against the saved source text (and, for rulings, against the cited decisions and a search for contrary or later authority). Rule ids in backticks.

- C-forfeiture-debt: `NY:ADJ-forfeiture-claims-survive`, `NY:CASE-Levine-counterclaim`, `NY:CASE-Paterno-rent-survives`. Forfeiture takes the right to retain, not the claim: 7-108(1-a)(e) text; Levine (App Term 1st 2026) decided the damage counterclaim on the merits after full return; Paterno (2d Dept) rent survives the 7-103 forfeiture; no contrary decision found.
- C-14-day-count: `NY:GCN-20`, `NY:GCN-25-a(1)`, `NY:CASE-Cohen-deadline-count`. GCN 20 excludes the event day, 25-a rolls a weekend/holiday end; Cohen (2d Dept 2024) counts July 24 -> August 7.
- C-written-provide: `NY:ADJ-provide-written-dispatch`, `NY:CASE-Bogom-Shanon-written`. Statement must be written (email/text suffice, STT 305(3)); timeliness by date sent (Cohen, Urban counted the send date).
- C-address-branches: `NY:ADJ-provide-address-branches`, `NY:CASE-Pickens-provide`. Use a known forwarding address or electronic channel; with none, send to the vacated unit within 14 days; waiting for an address forfeits (Prando upheld forfeiture for an innocent wait).
- C-estimates: `NY:CASE-Toporek-estimate`. Toporek (1st Dept 2022): a timely statement itemizing estimated costs with photos complied; disputes go to trial on the landlord's burden.
- C-cotenants: `NY:ADJ-cotenants-vacated`, `NY:ADJ-cotenants-payee`. GCN 35 and 7-103(1): clock at last departure (Holmes, App Term 2d); joint refund discharges on payment to one unless records sever shares (Lasky).
- C-fees-not-retained: `NY:ADJ-no-fee-retention`, `NY:RPL-238-a(2)`, `NY:RPL-234-a`. 7-108(1-a)(b) lists four categories exclusively (Colon canon); Freeland (1st Dept 2026) approved retention only by naming rent and utilities; RPL 234-a bars legal fees without a court order.
- C-painting: `NYC:PAINT-wear-and-tear`, `NYC:HMC-27-2013(b)(2)`. Owner's 3-year repaint duty; Bohl and Blansett (App Term 2d) require proof beyond wear and tear.
- C-FARE: `NYC:FARE-moveout-service-fee`, `NYC:FARE-20-699.22(b)`. FARE Act in force: 2d Cir. affirmed denial of a preliminary injunction on 2026-07-13 (REBNY v City of New York); a move-out service fee is chargeable only if it was on the signed pre-lease disclosure.
- C-mtm-surrender: `NY:COMMONLAW-NYC-monthly-tenant-surrender`, `NY:RPL-232-b`. T.I.B. (App Term 1st, aff'd 1st Dept) and Srinivasan (App Term 2d) hold an NYC month-to-month tenant owes no notice; 232-b is limited to outside NYC.
- C-auto-renewal: `NY:GOL-5-905`. Statutory text: a renewal clause binds only with the landlord's 15-30 day notice by personal service or registered/certified mail.
- C-GCE-end: `NY:RPL-215`, `NY:RPL-212`. RPL 215/216: for a covered unit non-renewal without a court finding of good cause does not end the tenancy (subject to R2-04 on the exemption list).
- C-interest-rate: `NY:CPLR-5004(a)-consumer-2pct`, `NY:CASE-NML-contract-rate`, `NY:ADJ-lease-interest-on-rent`, `NY:CPLR-5001(a)-(b)`. CPLR 5004(b) purpose test covers rent (Allen v Whidbee); lease post-maturity rate governs to judgment (NML, Court of Appeals); interest on late rent is a 238-a(2) late charge.
- C-not-consumer-credit: `NY:ADJ-lease-balance-not-consumer-credit`. Current law: GBL 600(1) and CPLR 105(f) require credit extended; Romea's analysis; Lefferts over Kings & Queens; the NYC Bar's 2026 report treats rent arrears as outside 214-i (see R2-02 for the pending change).
- C-belongings: `NY:COMMONLAW-belongings-owner-keeps`, `NY:COMMONLAW-belongings-abandonment`. Conversion law: no holding for rent (Facey), no bailment without agreement (8902 Corp., 1st Dept), disposal only on abandonment (Cretaro 4th Dept; Henryka App Term 2d).
- C-FDCPA-default: `US:15USC1692a(6)(F)(iii)-default-meaning`, `US:15USC1692a(6)(F)(iii)-moveout-branches`. Alibrandi (2d Cir. 2003) rejects default-on-due-date; referral to a self-identified collector declares default; Franceschi applies 'obtained' to a managing agent.
- C-fiduciary: `US:15USC1692a(6)(F)(i)-manager-incidental`, `US:15USC1692a(6)(F)(i)-collection-only`. Wilson (4th Cir.) and Harris (11th Cir.) incidental-versus-central test; FTC staff commentary on firms collecting overdue rent.
- C-handoff-configs: `US:HANDOFF-config-pre-default`, `US:HANDOFF-config-post-default`, `US:HANDOFF-config-owner-name-only`, `US:HANDOFF-config-principal-purpose`, `US:HANDOFF-config-owns-balance`. Each configuration follows from 1692a(6) text, Henson, Barbato, Vincent and Maguire as cited.
- C-DCWP-licensing: `NYC:DCA-manager-for-owners`, `NYC:DCA-handoff-incidental`, `NYC:DCA-handoff-principal-purpose`, `NYC:DCA-debt-buyer`. Admin Code 20-489(a) joins principal purpose and regular collection for others; buyer clause; (a)(7)(i) fiduciary exclusion.
- C-SHIELD-date: `NYC:SHIELD-operative-date`, `NYC:SHIELD-effective-date`. City Record notice of 2026-07-22 and DCWP FAQ (2026-08-04) set 2027-01-01; the conforming amendment was still 'Proposed' after the 2026-09-17 hearing.
- C-bankruptcy: `US:11USC362(a)(7)-deposit-is-setoff`, `US:CASE-Strumpf-hold`, `US:11USC542-refund-payee`. Setoff stayed (Sweet N Sour; Malinowski), temporary hold with prompt motion (Strumpf), refund to the chapter 7 trustee under 542(b).
- C-small-claims: `NY:CCA-1809(1)`, `NY:CCA-1801-A(b)`, `NY:CCA-1803-A(b)`. CCA text: entities barred from small claims; commercial claims consumer-transaction demand letter and five-per-month certificate.
- C-default-mailing: `NY:CPLR-3215(g)(3)`, `US:50USC3931(b)(1)`. CPLR 3215(g)(3)(i)-(ii) text (subject to the small-claims exception in R2-11); SCRA affidavit.
- C-HPD-registration-duty: `NYC:ADC-27-2097-registration`. 27-2097(b)(1) and (3): multiple dwellings and non-owner-occupied one- and two-family houses register (consequence corrected in R2-03).
- C-cap-interest: `NY:GOL-7-108(1-a)(a)`, `NY:GOL-7-103(2-a)`, `NY:ADJ-7103-2a-building-count`, `NY:GOL-7-103(2)-admin-fee`. Statutory text; Gihon (2d Dept) building test; 1% administration fee in lieu of all others.
- C-HCV: `US:24CFR982.313(c)`, `US:24CFR982.451(b)(4)`, `US:24CFR982.311(d)(1)`. eCFR text: tenant share only; owner keeps move-out month HAP; no PHA reimbursement.
- C-C12-date: `NY:GCN-24`. Computed: 2026-12-11 is a Friday; day 14 is Friday 2026-12-25 (public holiday); Saturday and Sunday follow; due Monday 2026-12-28.

Also verified on fidelity (effect matches quote and walk sentence): Step 0 routing (RSL 26-504, RSC 2520.11, RCL 26-403(e)(2)(i)(4) and (9)); 7-108(1) and (1-a) exclusions; Part M s.29 dates (2019-07-14, 2019-10-12); 232-c renewal by rent acceptance (Case v 575 Classon, App Term 2d); 7-105 turnover and its inconsistent-agreement clause (text confirmed); 7-108(2) successor liability; 226-b; 235-f; 236/236-a; 226-c notice periods; 227-a, 227-c, MIL 310, SCRA 3955 (incl. all-parties reading from the 2004 House report); 229 and 220; the inspection rules and Toporek's forfeiture scope; 238-a(2)/(2-a); 234/234-a; 235-i; 235-b offset; 7-103(2-b); HCV and PBV rules; HRA/SOTA voucher terms; Article VIII escrow; FHA assistance-animal rules; OSC MS11 and ABP 1315(2); SCRA 3958; FDCPA and Regulation F conduct, validation, delivery, dispute and liability rules; 6 RCNY 5-76/5-77 current rules; the SHIELD text; Admin Code 20-489/20-490/20-493.1/20-493.2; FCRA furnisher duties; 11 USC 362(a)(6), 524(a)(2).

## Test cases

Decided from the law before reading the walk's answers; differences stated.

- C3: Same result. 7-108(1-a) applies (2023 lease). Statement by email within 14 days of vacating (vacate day excluded, weekend/holiday rolls). Refund within the same 14 days: deposit plus bank interest less 1% a year, less rent unpaid, damage beyond wear and tear, lease utilities and moving/storage; no fees; no charge for repainting after ordinary use. With only an email known, the money goes by a payment the tenant can receive (electronic transfer) or a check mailed to the last postal address the landlord has. Add: rent may be kept only if the building's certificate of occupancy covers the unit (R2-01).
- C4: Differs. Same as C3 without the interest-bearing duty, with 3-year repaint, painting records and HPD registration. Missing from the walk: a three-family house must hold a certificate of occupancy for three families; a legal two-family with a third unit is a de facto multiple dwelling and no rent or use and occupancy is recoverable for the unlawful period (R2-01); an unregistered owner recovers no rent until it registers (MDL 325(2), R2-03). Good Cause does not reach it if the owner holds ten or fewer units or lives in the building.
- C5a: Same result. Rent accepted after 2019-07-14 created a new month-to-month tenancy (RPL 232-c; Case v 575 Classon), so 1-a applies; the tenant may leave at the end of any month without notice (T.I.B.; Srinivasan).
- C6: Differs in completeness. Mitigation duty and burden on the landlord (227-e, Toporek); statutory terminations end rent on their dates and bar early-termination charges; auto-renewal binds only with the 5-905 notice; the clock runs from vacating. Missing: at day 14 the deposit may cover only rent that has fallen due and is unpaid, up to the new tenant's lease (R2-07); a lease-break sum is owed only if it is a valid liquidated-damages clause, cannot displace mitigation, and is not kept from the deposit (R2-06).
- C7: Same result with additions. Timely itemized estimates (Toporek); excess is a separate claim that survives forfeiture; no legal fees without a court order; interest at the lease post-maturity rate to judgment (rent interest capped by 238-a) or 2% statutory; registration: a multiple-dwelling owner is barred, not stayed, until it registers (R2-03); rent part barred if no valid certificate of occupancy (R2-01); six-year limit today, three years if S9760 becomes law (R2-02).
- C8: Same result. No statement until the second co-tenant leaves; then a statement to each; refund split by the landlord's records of who paid what, else jointly.
- C9: Same result with one addition. Statement and refund to the vacated unit within 14 days; unclaimed money stays the tenant's and is reported after three years. The ABP 1422 due-diligence mailing is excused here because the only address is known not to be current (R2-09).
- C10: Same result with one addition. Turnover within 5 days with registered or certified mail notice; the buyer settles; a buyer with actual knowledge is liable if not turned over. The buyer must register as the new owner (27-2097; MDL 325(1) within 30 days of succession) before it can recover rent (R2-03).
- C11: Same result. Belongings stay the tenant's, cannot be held for rent, are released on request, may be disposed of only on abandonment; reasonable moving and storage costs may be kept; belongings may push back the vacate date where the lease so provides (Urban).
- C12: Same result. 2026-12-11 is a Friday; day 14 is Friday 2026-12-25, Christmas, a public holiday; Saturday 26 and Sunday 27 follow; the statement and refund are due Monday 2026-12-28.
- C13: Same result. Only the tenant's share is charged; the owner keeps the move-out month's HAP and gets no later HAP; written list and refund within 14 days satisfy 'promptly'.
- C14: Differs. The agency is a federal debt collector (principal purpose; account taken after default) and a DCWP-licensed agency; validation notice within 5 days to an address where the tenant now receives mail; verification with the lease and the statement; the current 6 RCNY 5-77 rules apply until 2027-01-01, SHIELD after. 23 NYCRR Part 1 does not apply (R2-10). Limitation: six years today, three years for suits commenced from the 90th day after S9760 becomes law (R2-02). Interest 2% (natural person). Before suit: multiple-dwelling registration is a bar, not a stay (R2-03), and no rent is recoverable for any period without a valid certificate of occupancy (R2-01).
- C15: Same result. Applying the deposit to pre-filing charges is a stayed setoff; hold only the disputed part while promptly moving for relief (Strumpf); statement by day 14 without a demand; the rest to the chapter 7 trustee (or as the trustee directs) or to the debtor in chapter 13.

## First-round corrections (task 6)

- R1-01: **correct and complete**. CPLR 5001/5004 rules, the NML contract-rate rule and the 238-a cap on lease interest are applied and match the text; 2% for natural persons, 9% for companies. S9760 (R2-02) would add 'whether contingent or absolute' to 5004(b) and changes nothing for rent.
- R1-02: **correct and complete**. NY:GOL-5-905 matches the statute (15-30 days, personal or registered/certified service); walk 3.1 and C6 state it.
- R1-03: **correct and complete**. Two-branch payee rule rests on 7-103(1) as words of severance and Lasky for the joint branch; Holmes is no longer cited for the split.
- R1-04: **correct and complete**. US:11USC542-refund-payee applies 541(a)(1), 542(b)-(c) and 1306(b); walk 6.7 and C15 pay the trustee in chapter 7 and the debtor in chapter 13.
- R1-05: **correct but incomplete**. The city registration duty and discretionary stay are right for a non-owner-occupied one- or two-family house, but for a multiple dwelling MDL 325(2) bars recovery of rent until registration (R2-03), and the related MDL 302 certificate-of-occupancy bar was missed by both rounds (R2-01).
- R1-06: **correct but incomplete**. Covered-unit rule (RPL 212, 215) is right; the applied exemption list omits the 245%-of-FMR high-rent exemption (RPL 214(15)), the one most likely to reach a market-rate NYC unit, and three others (R2-04). The first-round correct-rule text had the same omission.
- R1-07: **correct and complete**. NYC:HMC-27-2013(a) added; walk 1.5 and 5.3 now condition the 3-year cycle and records on a multiple dwelling.
- R1-08: **correct and complete**. Walk 2.5 now says silence is consent and only an election to terminate or an unreasonable refusal ends the lease (RPL 236 text).
- R1-09: **correct and complete**. Cap reaches deposit plus rent paid ahead for a later period; first month's rent is not an advance; AG guide supports.
- R1-10: **over-corrected**. The wording fix is right for mistake of law, but the walk now leads with 'knew or should have known' and ties it to every managed account while dropping the rule's 'more than inadvertence or accident' limb, so an inadvertent miss by a manager reads as willful (R2-05). I reject the first round's confirmation that knew-or-should-have-known is the whole meaning: Karole, which the rule adopts, starts from 'not merely negligent'.
- R1-11: **correct and complete**. C3 now separates the emailed statement from a refund paid by a method that reaches the tenant within the 14 days.
- R1-12: **correct and complete**. Phone limb now rests on Bogom-Shanon (text is writing) plus Pickens; I accept the adjudication.
- R1-13: **correct but incomplete**. NY:CPLR-3215(g)(3) states the mailing, but not 3215(g)(3)(iii), which excludes the small claims part (R2-11).
- R1-14: **correct and complete**. CCA 1809(1), 1801-A(b), 1803-A(b) rules match the text; walk 8.10 states them.
- R1-15: **correct and complete**. The 17 rules are in the deferred list with one kept sentence each (29-H does not apply; no distress in New York); they remain in the files.
- R1-16: **correct and complete**. The 'lighter authority' section and 'No appellate court' sentence are gone from the walk; 8.1 states the controlling authority.
- R1-17: **correct and complete**. Gelbart, RPL 235-b, GCN 35, Mabe and Van Rensselaer now point to official or CourtListener copies. New review-1 sources introduced their own provenance slip (HPD source_url, R2-12).

Overlap with the first round: R2-03 extends R1-05; R2-04 extends R1-06; R2-05 reverses the emphasis of R1-10 and rejects part of the first round's confirmation of the willfulness standard; R2-11 completes R1-13; R2-12 is a provenance slip in sources added for R1-05. New in this round: R2-01 (MDL 302 certificate of occupancy), R2-02 (S9760, passed both houses after the first-round sources were read), R2-06 (liquidated damages and lease-break charges), R2-07 (rent a deposit may cover after an early departure), R2-08 (RPL 232), R2-09 (ABP 1422), R2-10 (23 NYCRR Part 1), R2-13 (walk alignment). First-round findings I would reject on the merits: none; R1-10 was right to narrow the mistake-of-law sentence, but its supporting confirmation overstated the standard.

## Method

- Read APERTURE.md, STAGE_A.md and the CORDON design principles, then the walk in full. Scripted a side-by-side dump (`review/ir2_dump.py`) of all 361 rules the walk cites: the walk paragraph, condition, effect, quote, source, authorities and reasoning, and read all of it (about 450 KB). Opened sources in context where a quote was short or the effect went beyond it (RPL 214, GOL 7-105, CPLR 3215, CPLR 5004, Admin Code 27-2097/27-2107, Karole, Prando, Freeland, Srinivasan, Pickens, Caldwell). Ran `check_review.py` (359 in scope cited, 95 deferred, 0 missing) and `stage_a_check.py` (0 errors in all four files).
- Searched for contrary and later authority on each ruling (nycourts.gov reporter, Justia, CourtListener-backed mirrors, web search): 7-108 willfulness and delivery decisions 2021-2026; CPLR 214-i and rent; NYC month-to-month notice; MDL 302/325 and de facto multiple dwellings (Chazon, Caldwell, Jalinos, 49 Bleecker, Malden); liquidated damages (JMD Holding); DFS 23 NYCRR Part 1 and its unadopted amendment; FARE Act litigation (2d Cir. 2026-07-13); DCWP SHIELD status and the ACA International challenge to the superseded 2024 rule; the Consumer Debt Uniformity Act (S9760/A10182-A) actions; ABP 1422.
- Enumerated the chain through the nine families. New law not in the files: MDL 301/302/325(2) and MDL 4(7); RPL 214(15); RPL 232; ABP 1422; 23 NYCRR 1.1(d); the Court of Appeals liquidated-damages test; S9760. Considered and left out as not changing a decision in this chain: RPL 235-e(d) (defense in eviction only), CPLR 5205(g) (debtor's exemption; the trustee still directs payment), NYC Human Rights Law process rules, PSC submetering (no utility charge fact pattern in scope).
- Saved new sources mechanically (web_extract output or curl + pdftotext written by script, never retyped) with the REVIEW2_ prefix: MDL 4, 301, 302, 325; RPL 232; ABP 1422; 23 NYCRR 1.1; Chazon (CoA 2012), Caldwell (2d Dept 2008), 49 Bleecker (1st Dept 2018), JMD Holding (CoA 2005), Kunik (App Term 2d 2023); S9760/A10182-A with actions; REBNY v City of New York (2d Cir. 2026).
- Access: nycourts.gov and Justia returned a Cloudflare page to curl; web_extract retrieved them. write_file will not overwrite a file it did not read, so two stub files from the first curl attempt were deleted and re-saved. Google Scholar was not used.
