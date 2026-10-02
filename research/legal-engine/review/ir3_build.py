"""Build review/independent_review_3.json and review/INDEPENDENT_REVIEW_3.md from the data below.

Run from research/legal-engine:  python3 review/ir3_build.py
Then:                             python3 review/ir3_verify.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
S = "sources/"
WALK = "review/NYC_MARKET_RATE.md"

FINDINGS = [
    {
        "id": "R3-01", "kind": "incorrect rule", "severity": "critical",
        "rule_ids": ["NY:ADJ-RPL-232-indefinite-term", "NY:ADJ-RPL-232-monthly-letting", "NY:RPL-232"],
        "step": "3.2a; T-232",
        "finding": (
            "The walk rules that an NYC agreement stating a monthly rent and nothing about duration is within RPL 232 "
            "and binds the tenant to the next October 1 ('A rent \"of $X a month\" is not a period'), calls Stauber v "
            "Antelo controlling, and rejects Spies v Voss. The authorities do not support that. (1) Stauber decided a "
            "sublet that began in September, so RPL 232 produced a one-month term, and the court held the occupancy "
            "month to month 'by any legal definition', citing as a separate ground that monthly acceptance of rent "
            "creates a month-to-month tenancy. It did not decide whether a bare monthly rent binds either party to a "
            "later October 1; on its facts every path gave the same result. (2) The Appellate Term, Second Department, "
            "later and directly on point, holds that a general letting at a monthly rent is presumed a month-to-month "
            "tenancy (Gerolemou v Soliz, 2000, a Queens oral tenancy; cited by the First Department in 2024 and 2025). "
            "(3) Spies, the sweep's own authority for applying RPL 232 to an open stay, states that a hiring at a "
            "monthly rent with nothing said about the term is a tenancy for a month; it applied the statute only because "
            "the parties spoke of staying 'a long time'. Gilfoyle (App Term 1896) inferred a monthly letting from a monthly "
            "rent paid monthly. T.I.B. v Repetto (App Term 1st, aff'd) treated a no-lease tenant renting month to month as a "
            "monthly tenant and set 'indefinite hirings' apart. (4) The 1920 committee note says the bill restored the law "
            "'substantially as it was previously', which carries forward the Spies and Gilfoyle constructions rather than "
            "overruling them. Result: T-232 keeps July rent from the deposit and claims August and September rent that "
            "the tenant does not owe, a wrongful retention that feeds the willful-damages exposure."
        ),
        "correct_rule": (
            "In New York City an agreement, oral or written, that fixes a monthly rent and says nothing about how long the "
            "occupancy lasts is presumed a month-to-month tenancy from the start, unless there is proof of a different "
            "agreement (Gerolemou; Spies; Gilfoyle; T.I.B.; Stauber's monthly-acceptance ground). The tenant may leave at the "
            "end of any monthly term without notice (NY:COMMONLAW-NYC-monthly-tenant-surrender). RPL 232 governs an agreement "
            "under which the parties contemplated an occupancy longer than one rental period but did not particularly specify "
            "its length ('a long time', 'indefinitely', 'for years' without a valid written term): that occupancy runs to the "
            "first October 1 after possession, and a tenant who leaves earlier without an accepted surrender owes rent through "
            "September 30, subject to RPL 227-e (Spies; Abbey). Which words were used is a Judgment. Gerolemou and T.I.B. "
            "prevail on the bare-monthly-rent case: Gerolemou is the latest appellate decision on the exact question and binds "
            "the Second Department's city courts; T.I.B. was affirmed by the First Department; Stauber is consistent with both "
            "because it did not decide the question. T-232 as written (oral, $2,400 a month, nothing said about length): nothing "
            "is owed after June 30; July rent may not be kept from the deposit."
        ),
        "evidence": [
            {"source_file": S + "REVIEW3_NY_CASE_Gerolemou_v_Soliz_2000_AppTerm2d.txt",
             "quote": "In the absence of contravening proof, the law presumes that where there is a general letting with a monthly rent reserved, an indefinite month-to-month tenancy is created"},
            {"source_file": S + "SWEEP_NY_CASE_Spies_v_Voss_1890_CommonPleasGT.txt",
             "quote": "If nothing had been said concerning the term, and the hiring had been at a certain monthly rent, a tenancy for a month only would have been created."},
            {"source_file": S + "SWEEP_NY_CASE_Spies_v_Voss_1890_CommonPleasGT.txt",
             "quote": "But in the present case the parties contemplated a longer occupation than a month, as is apparent from the conversation between them"},
            {"source_file": S + "SWEEP_NY_CASE_Stauber_v_Antelo_1990_1stDept.txt",
             "quote": "Moreover, the acceptance of rent on a monthly basis creates a month-to-month tenancy"},
            {"source_file": S + "SWEEP_NY_CASE_Stauber_v_Antelo_1990_1stDept.txt",
             "quote": "continued until October 1, 1980, a lease term of one month. Thus, by any legal definition, plaintiffs’ occupancy of the apartment involved a month-to-month subtenancy."},
            {"source_file": S + "NY_CASE_TIB_v_Repetto_1940_AppTerm1st.txt",
             "quote": "or the letting was *“* for no fixed period ”"},
            {"source_file": S + "SWEEP_NY_CASE_1239Madison_v_Neuburger_1922_MunCt.txt",
             "quote": "The present bill restores the law substantially as it was previously"},
            {"source_file": S + "REVIEW3_NY_CASE_Olympic_Galleria_v_Sitt_2025_1stDept.txt",
             "quote": "see Gerolemou v Soliz"},
            {"source_file": WALK,
             "quote": "A rent \"of $X a month\" is\nnot a period; a tenant who leaves before that October 1 owes rent to September 30"},
        ],
    },
    {
        "id": "R3-02", "kind": "incomplete rule", "severity": "critical",
        "rule_ids": ["NY:MDL-301(1)", "NY:MDL-302(1)(b)"],
        "step": "0.5; C4; C7; C14",
        "finding": (
            "NY:MDL-301(1) and Step 0.5 state without exception that a multiple dwelling may not be occupied without a "
            "certificate of occupancy, and MDL 302(1)(b) then bars all rent. MDL 301 itself exempts (a) a class B multiple "
            "dwelling existing on 1929-04-18 that needed no certificate before then and has not been altered except in "
            "compliance, and (b) an old-law tenement, or a class A multiple dwelling erected after 1901-04-12 and occupied for "
            "two years before 1909, not altered except in compliance; and 301(2) ties the certificate requirement to a dwelling "
            "constructed, altered or converted into a multiple dwelling after 1929-04-18. MDL 302 bars rent only for occupancy "
            "'in violation of section three hundred one'. As written, the operator would forfeit rent, and refund deposit "
            "money kept for rent, on lawful pre-1929 buildings that have no certificate, which are common among small NYC "
            "walk-ups."
        ),
        "correct_rule": (
            "MDL 302(1)(b) bars rent and use and occupancy only for a period when a multiple dwelling is occupied in violation of "
            "MDL 301: a building constructed as, or altered or converted into, a multiple dwelling after 1929-04-18 (including a "
            "one- or two-family house later occupied by three or more families) that lacks a certificate of occupancy for that "
            "use; or an older building outside the MDL 301(1)(a)-(b) exceptions. A building within those exceptions needs no "
            "certificate, and its owner recovers rent. Evidence input: construction or conversion date and alteration history "
            "(DOB record), not the mere absence of a certificate."
        ),
        "evidence": [
            {"source_file": S + "REVIEW2_NY_MDL_301_nysenate.txt",
             "quote": "except that no such certificate\nshall be required in the case of:"},
            {"source_file": S + "REVIEW2_NY_MDL_301_nysenate.txt",
             "quote": "Any old-law tenement, or any class A multiple dwelling erected\nafter April twelfth, nineteen hundred one, which was occupied for two\nyears immediately before January first, nineteen hundred nine"},
            {"source_file": S + "REVIEW2_NY_MDL_301_nysenate.txt",
             "quote": "no dwelling constructed as or altered or\nconverted into a multiple dwelling after April eighteenth, nineteen\nhundred twenty-nine, shall be occupied in whole or in part until the\nissuance of a certificate of compliance or occupancy."},
            {"source_file": S + "REVIEW2_NY_MDL_302_nysenate.txt",
             "quote": "occupied in whole or in part for human habitation in violation of section three hundred one"},
            {"source_file": WALK,
             "quote": "It may not be occupied without a certificate of occupancy for that use: `NY:MDL-301(1)`."},
        ],
    },
    {
        "id": "R3-03", "kind": "incorrect test case", "severity": "critical",
        "rule_ids": ["NY:MDL-325(2)", "NYC:ADC-27-2107(b)-rent-stay"],
        "step": "0.5; 8.10; C4; C10",
        "finding": (
            "C4 says 'No rent is recoverable for any period ... the owner was unregistered.' The registration bar is a "
            "suspension, not a forfeiture: MDL 325(2) bars recovery 'until he complies', and the Appellate Term, Second "
            "Department (9 Montague Terrace, 2001, overruling Davis v Priddie and agreeing with the First Department's Appellate "
            "Term in 128 E. 83rd St. Co. v Kagan) holds that once the owner registers it recovers the rent that accrued while it "
            "was unregistered. Step 0.5 files registration under 'Can rent be recovered at all?' and neither the atom nor the walk "
            "states the consequence that matters for the 14-day statement: an owner unregistered on the day it sends the statement "
            "cannot keep the deposit for rent, but can register and then keep or sue for all of it. The one- or two-family stay "
            "(27-2107(b)) is likewise only a stay 'during such period'."
        ),
        "correct_rule": (
            "An NYC multiple-dwelling owner that has not filed its HPD registration recovers no rent while unregistered, by suit, "
            "setoff or deposit retention. When it registers, the bar lifts and it recovers all rent that accrued during the "
            "unregistered period (9 Montague Terrace; MDL 325(2) 'until he complies'). Operator step: confirm current registration "
            "before the 14-day statement; if missing, file it before the statement goes out so the deposit may be applied to rent. "
            "For a one- or two-family house that must register, the court may stay the rent claim until registration "
            "(NYC:ADC-27-2107(b)-rent-stay); rent is not forfeited."
        ),
        "evidence": [
            {"source_file": S + "REVIEW3_NY_CASE_9MontagueTerrace_v_Feuerer_2001_AppTerm2d.txt",
             "quote": "hold that, upon registering, an owner is entitled to recover the rents which accrued during the period of noncompliance"},
            {"source_file": S + "REVIEW3_NY_CASE_9MontagueTerrace_v_Feuerer_2001_AppTerm2d.txt",
             "quote": "but does not [\\*20](https://www.courtlistener.com/opinion/6346103/9-montague-terrace-assoc-v-feuerer/#20) provide for an abatement of the rents which accrue during the period of noncompliance."},
            {"source_file": S + "REVIEW2_NY_MDL_325_nysenate.txt",
             "quote": "fails to comply with such registration requirements until he complies with such requirements."},
            {"source_file": WALK,
             "quote": "No rent is recoverable for any period the house\nlacked a certificate of occupancy for three families or the owner was unregistered."},
        ],
    },
    {
        "id": "R3-04", "kind": "incomplete rule", "severity": "critical",
        "rule_ids": ["NY:MDL-302-a(3)"],
        "step": "0.5; 5.5; C7; C14",
        "finding": (
            "NY:MDL-302-a(3) and the walk state the rent-impairing bar as absolute once a violation stays on HPD's record six "
            "months after notice. The statute's subparagraph 3(b) says the bar does not apply where (i) the condition did not in "
            "fact exist, (ii) it has in fact been corrected though HPD's record still shows it, (iii) it was caused by the resident "
            "sought against, the resident's family or guests, or another resident or that resident's family or guests, or (iv) "
            "the resident refused the owner entry to correct it. Subparagraph 3(d) bars the resident from recovering rent it "
            "voluntarily paid. Without these, the operator forgoes rent the owner is owed, for example where the tenant caused "
            "the condition or refused access, or the violation was cured but not cleared."
        ),
        "correct_rule": (
            "No rent is recovered for a unit (or for every unit, where the condition is in a common part or a part the owner "
            "controls) for the period a rent-impairing violation stays uncorrected after six months from HPD's mailed notice (or "
            "from plan approval), unless the condition did not exist, was in fact corrected, was caused by the departing tenant "
            "or its household or guests or by another resident or its household or guests, or the tenant refused entry to "
            "correct it. Rent the tenant voluntarily paid for the period is not recoverable by the tenant. Evidence inputs: HPD "
            "record, repair record, access refusals, cause of the condition."
        ),
        "evidence": [
            {"source_file": S + "NY_MDL_302-A_nysenate.txt",
             "quote": "the condition which is the subject of the violation has in fact been corrected, though the note thereof in the department has not been removed or cancelled"},
            {"source_file": S + "NY_MDL_302-A_nysenate.txt",
             "quote": "the violation has been caused by the resident from whom rent is sought to be collected or by members of his family or by his guests"},
            {"source_file": S + "NY_MDL_302-A_nysenate.txt",
             "quote": "the resident proceeded against for rent has refused entry to the owner for the purpose of correcting the condition giving rise to the violation"},
            {"source_file": S + "NY_MDL_302-A_nysenate.txt",
             "quote": "If a resident voluntarily pays rent or an installment of rent when he would be privileged to withhold the same under subparagraph a, he shall not thereafter have any claim or cause of action to recover back the rent"},
        ],
    },
    {
        "id": "R3-05", "kind": "incorrect test case", "severity": "critical",
        "rule_ids": ["NY:HANDOFF-broker-config-collection-agency", "NY:RPL-440(1)-rent-collection", "NY:RPL-442-f-exemptions"],
        "step": "C14",
        "finding": (
            "C14 hands a $2,400 balance to a collection agency and lists only its federal and city status (and cites Rules "
            "8.1-8.6, not 8.6a). Under the walk's own 8.6a and NY:HANDOFF-broker-config-collection-agency, which this review "
            "confirms on the text of RPL 440(1) and 442-f, an agency collecting the rent part for a fee also needs a New York "
            "broker's licence; only attorneys, court appointees and public officers are exempt. The test case answer omits a "
            "licence requirement that decides whether the hand-off is lawful."
        ),
        "correct_rule": (
            "C14: if any part of the $2,400 is rent (including rent for months after an early departure), the agency needs a "
            "New York real estate broker's licence as well as its DCWP licence, or the rent part must go to an attorney. A "
            "balance of damage and other non-rent charges needs no broker licence. Rules: add 8.6a."
        ),
        "evidence": [
            {"source_file": S + "SWEEP_NY_RPL_440_nysenate.txt",
             "quote": "collects or offers or attempts to collect rent for the use of real estate"},
            {"source_file": S + "SWEEP_NY_RPL_442-F_nysenate.txt",
             "quote": "or public officers while performing their official duties, or attorneys at law."},
            {"source_file": WALK,
             "quote": "The agency is a federal\ndebt collector and a licensed city agency."},
        ],
    },
    {
        "id": "R3-06", "kind": "incomplete rule", "severity": "critical",
        "rule_ids": ["NY:RPL-442-d-442-e-unlicensed", "NY:HANDOFF-broker-config-collects-rent"],
        "step": "8.6a",
        "finding": (
            "The consequence of unlicensed collection is stated as losing 'its fee' and paying the owner one to four times it. "
            "The Appellate Division applies the illegality to the whole engagement where the brokerage element is its dominant "
            "feature (G.C. Fortune, 3d Dept 1998: management agreement with occasional rent collection unenforceable, owner's "
            "counterclaim also dismissed) and to all property-management fees in a bundle that includes rent collection "
            "(Fields, 2d Dept 2025). RPL 442-e(3) gives the penalty to 'any person aggrieved', not only the owner. For Handoff "
            "in Configuration 1 the exposure is the compensation for the whole settlement engagement, not a collection fee."
        ),
        "correct_rule": (
            "An unlicensed business that collects rent for another for a fee commits a misdemeanor for each act; it cannot "
            "recover compensation for the services of which rent collection is part, and where the brokerage element is the "
            "dominant feature of the engagement the whole agreement is unenforceable (G.C. Fortune; Fields). It is liable to a "
            "penalty of one to four times the compensation received, recoverable by any person aggrieved. The owner's claim "
            "against the former tenant is unaffected. Which services form the tainted bundle is a Judgment on the engagement's "
            "terms (dominant-feature test: Dodge; G.C. Fortune)."
        ),
        "evidence": [
            {"source_file": S + "REVIEW3_NY_CASE_GC_Fortune_v_Stockade_1998_3dDept.txt",
             "quote": "the dominant or principal feature of the parties’ transaction was in the nature of a real estate broker wherein a license would be required"},
            {"source_file": S + "REVIEW3_NY_CASE_GC_Fortune_v_Stockade_1998_3dDept.txt",
             "quote": "delivered late notices to tenants who were in arrears on rent payments and occasionally collected rents and issued receipts"},
            {"source_file": S + "SWEEP_NY_CASE_Fields_v_Pinkney_2025_2dDept.txt",
             "quote": "including those related to home equity financing, lease generation, rental costs, and rent collection"},
            {"source_file": S + "SWEEP_NY_RPL_442-E_nysenate.txt",
             "quote": "which penalty may be sued for and recovered by any person aggrieved and for his use and benefit"},
        ],
    },
    {
        "id": "R3-07", "kind": "missing rule (pending law)", "severity": "major",
        "rule_ids": ["NY:CPLR-214-i-consumer-debt-S9760", "NY:CPLR-3215(g)(3)"],
        "step": "8.1; 8.9; C14",
        "finding": (
            "Status confirmed: the Assembly action list for A10182/S9760 ends at 06/03/2026 'returned to senate'; it has not been "
            "delivered to the Governor. But the act does more than shorten the limitations period. Because a lease balance becomes "
            "a 'consumer debt', a suit on it against a natural person will also fall under the consumer-credit procedure the act "
            "re-keys to consumer debt: the additional notice mailing (CPLR 306-d), attaching the lease to the complaint (CPLR "
            "3016(j)), the additional default-judgment proof (CPLR 3215(f), (j)), the summary-judgment notice (CPLR 3212(j)) and "
            "the NYC Civil Court summons and venue rules (CCA 301(a), 401(d)). Only the three-year period is recorded as a dated "
            "future atom."
        ),
        "correct_rule": (
            "Record dated future atoms (effective the 90th day after S9760/A10182-A becomes law) for each procedural amendment that "
            "reaches an action on a residential lease balance against a natural person: CPLR 306-d, 3016(j), 3212(j), 3215(f) and "
            "(j), 305(a), 3012(a), 3211(e), CCA 301(a) and 401(d); and reflect them in 8.9 and C14. Until the act becomes law, "
            "current law governs (CPLR 213(2); 3215(g)(3))."
        ),
        "evidence": [
            {"source_file": S + "REVIEW3_NY_A10182_S9760_Assembly_actions_2026-09-29.txt", "quote": "returned to senate"},
            {"source_file": S + "REVIEW2_NY_S9760_A10182A_ConsumerDebtUniformityAct_2026.txt",
             "quote": "Additional mailing of notice in [an action arising out of a consumer"},
            {"source_file": S + "REVIEW2_NY_S9760_A10182A_ConsumerDebtUniformityAct_2026.txt",
             "quote": "(j) [Consumer credit transactions] Consumer debts."},
            {"source_file": S + "REVIEW2_NY_S9760_A10182A_ConsumerDebtUniformityAct_2026.txt",
             "quote": "Subdivisions (f) and (j) of section 3215 of the civil practice"},
        ],
    },
    {
        "id": "R3-08", "kind": "missing rule (family 10)", "severity": "major",
        "rule_ids": ["NY:CPLR-3015(e)-licence-pleading", "NYC:ADC-27-2107(b)-rent-stay"],
        "step": "8.10",
        "finding": (
            "Family 10 omits the owner's own capacity to sue. Scattered-site owners are commonly LLCs, many formed outside New York. "
            "A foreign LLC doing business in New York without a certificate of authority may not maintain any action until it "
            "obtains one (LLC Law 808(a)); a foreign corporation likewise, and it must also pay its New York taxes (BCL 1312(a)). "
            "The Second Department applied 808(a) in 2026 to a landlord LLC suing former tenants for breach of the lease. Neither "
            "provision affects the lease, deposit retention or the tenant's right to sue. A domestic LLC's failure to publish "
            "under LLC Law 206 suspends its authority but is not a jurisdictional defect in a landlord's proceeding (1700 First "
            "Ave., App Term 1st)."
        ),
        "correct_rule": (
            "Before an owner that is a foreign LLC or foreign corporation sues a former tenant (or a collector sues in its name), "
            "it must hold New York authority to do business; otherwise the suit is dismissed on motion until it does (LLC Law "
            "808(a); BCL 1312(a), which also requires payment of New York taxes). Whether leasing NYC units is 'doing business' is "
            "a Judgment on the regularity of the owner's New York activity. The defect is curable and does not affect the lease, "
            "the deposit statement or the owner's defense of a tenant's suit (808(b); 1312(b)). A domestic LLC's unfiled "
            "publication is not a ground to dismiss its rent claim (1700 First Ave.). A nonresident owner may be required to post "
            "security for costs (CPLR 8501(a), cited in S. Garson)."
        ),
        "evidence": [
            {"source_file": S + "REVIEW3_NY_LLC_808_nysenate.txt",
             "quote": "may not maintain any action, suit or special proceeding in any court of this state unless and until such limited liability company shall have received a certificate of authority in this state."},
            {"source_file": S + "REVIEW3_NY_BCL_1312_nysenate.txt",
             "quote": "shall not maintain any action or special proceeding in this state unless and until such corporation has been authorized to do business in this state"},
            {"source_file": S + "REVIEW3_NY_CASE_SGarson_v_Luck_2026_2dDept.txt",
             "quote": "Since it is undisputed that the plaintiff is a foreign limited liability company authorized to do business in New York"},
            {"source_file": S + "REVIEW3_NY_CASE_1700FirstAve_v_ParsonsNovak_2014_AppTerm1st.txt",
             "quote": "Limited Liability Company Law § 206 constitute a jurisdictional defect requiring dismissal"},
        ],
    },
    {
        "id": "R3-09", "kind": "scope gate gap (family 7/10)", "severity": "major",
        "rule_ids": ["NY:MDL-302(1)(b)", "NY:MDL-325(2)"],
        "step": "0.1-0.5",
        "finding": (
            "The sweep marks Loft Law interim multiple dwellings 'out: not a market-rate apartment', but Step 0 routes out only "
            "stabilized, controlled and undetermined units. An IMD unit would be classed market-rate by default and run through "
            "MDL 302 and 325(2), which MDL 285(1) displaces: an IMD owner recovers rent from protected occupants only while in "
            "compliance with article 7-C."
        ),
        "correct_rule": (
            "Step 0 classifies a unit in a building registered with or covered by the Loft Board (MDL art. 7-C) as outside this "
            "engine and routes it to the operator. For such a unit, rent recovery from a protected occupant turns on the owner's "
            "article 7-C compliance (MDL 285(1)), not on MDL 302 or 325(2)."
        ),
        "evidence": [
            {"source_file": S + "REVIEW3_NY_MDL_285_nysenate.txt",
             "quote": "the owner of an interim multiple dwelling may recover rent payable from"},
            {"source_file": S + "REVIEW3_NY_MDL_285_nysenate.txt", "quote": "provided that he is in compliance with this article."},
            {"source_file": "review/SWEEP_BUILDING_OWNER.md",
             "quote": "| Loft Law IMDs, SROs, class B | read | out | not a market-rate apartment |"},
        ],
    },
    {
        "id": "R3-10", "kind": "inconsistent wording", "severity": "minor",
        "rule_ids": ["NY:ADJ-willful-standard"],
        "step": "7.5",
        "finding": (
            "The willfulness restatement is right in structure, but its example of an innocent miss, 'an unknown new address', "
            "conflicts with Step 6.5 (with no channel the statement goes to the vacated unit; waiting for an address forfeits) and "
            "with the atom's own first part: a manager that holds the statement because it has no address has made a deliberate "
            "choice on a wrong reading of the law, which the atom calls willful. Prando's 'innocent' finding concerned individual "
            "owners and was a deferential affirmance of a trial finding."
        ),
        "correct_rule": (
            "For an experienced landlord or managing agent, withholding the statement because the tenant's new address is unknown "
            "is willful. An honest process error remains not willful: a misdated send, a failed delivery, or missing a channel the "
            "tenant supplied that did not reach the manager's records."
        ),
        "evidence": [
            {"source_file": S + "NY_CASE_Prando_v_Kelly_2021.txt", "quote": "she had not known his new address"},
            {"source_file": WALK,
             "quote": "A miss from an honest process error (a misdated\nsend, a failed delivery, an unknown new address) is not willful, even for a manager."},
            {"source_file": WALK, "quote": "Waiting for an address forfeits"},
        ],
    },
    {
        "id": "R3-11", "kind": "incomplete test case", "severity": "minor",
        "rule_ids": ["NY:ADJ-vacate-order-rent"],
        "step": "T-vacate",
        "finding": "T-vacate states February rent stays owed but is silent on March 1-9, the part of the month before the 2026-03-10 order.",
        "correct_rule": (
            "Rent for the period before the order (March 1-9) is owed; no rent is owed from the order date (March 10) onward, "
            "while the order stands or after the tenant surrenders; any March rent paid for March 10-31 is refunded or credited."
        ),
        "evidence": [
            {"source_file": S + "SWEEP_NY_CASE_Younger_v_Campbell_1917_1stDept.txt",
             "quote": "the landlord cannot recover any rent for the period after the eviction occurred."},
        ],
    },
    {
        "id": "R3-12", "kind": "incomplete rule", "severity": "minor",
        "rule_ids": ["NYC:HMC-27-2045-detector-charge"],
        "step": "5.5a; T-lead",
        "finding": "The $25/$50/$75 reimbursement caps in 27-2045(e) apply to battery-operated devices; the atom and walk omit that limit.",
        "correct_rule": (
            "The caps govern a battery-operated smoke, CO or gas device (or combination) the tenant lost, removed or damaged. A "
            "hardwired device the tenant damaged is charged under the general damage rule at the reasonable cost of repair."
        ),
        "evidence": [
            {"source_file": S + "SWEEP_NYC_ADC_27-2045.txt",
             "quote": "The occupant of a dwelling unit within a class A multiple dwelling or private dwelling in which a battery-operated smoke detecting device"},
        ],
    },
    {
        "id": "R3-13", "kind": "incomplete rule", "severity": "minor",
        "rule_ids": ["NY:ABP-1422"],
        "step": "6.8",
        "finding": "ABP 1422 lets the holder deduct the certified-mail postage from the property and prescribes the notice's content; the atom states neither.",
        "correct_rule": (
            "The notice tells the tenant the refund will be reported and paid to the Comptroller unless claimed before the "
            "remittance date. The certified-mail cost for a refund over $1,000 may be deducted from it as a service charge."
        ),
        "evidence": [
            {"source_file": S + "REVIEW2_NY_ABP_1422_justia.txt",
             "quote": "Costs paid to the postal authorities by holders of unclaimed property to provide such written notice by certified mail, return receipt requested, may be deducted from the property as a service charge."},
        ],
    },
    {
        "id": "R3-14", "kind": "provenance", "severity": "minor",
        "rule_ids": ["NY:23NYCRR-1.1(d)-not-lease", "NY:COMMONLAW-owner-death-agency"],
        "step": "8.1; 0.5",
        "finding": (
            "NY:23NYCRR-1.1(d)-not-lease cites a Cornell URL while its saved text is the Justia compilation (current through "
            "2024-12-24). NY:COMMONLAW-owner-death-agency rests on a Court of Appeals decision saved from hallapproved.com, an "
            "unofficial mirror. The content supports both rules."
        ),
        "correct_rule": "Point source_url at the page actually saved; save Farmers' Loan & Trust v Wilson (139 NY 284) from CourtListener or the official reports.",
        "evidence": [
            {"source_file": S + "REVIEW2_NY_23NYCRR_1.1_justia.txt",
             "quote": "SOURCE: https://regulations.justia.com/states/new-york/title-23/chapter-i/part-1/section-1-1"},
            {"source_file": "stage-a/NY.json", "quote": "\"source_url\": \"https://www.law.cornell.edu/regulations/new-york/23-NYCRR-1.1\""},
            {"source_file": S + "SWEEP_NY_CASE_FarmersLoan_v_Wilson_1893_CoA.txt",
             "quote": "SOURCE: https://hallapproved.com/ny/cases/supreme/1893/3638763/"},
        ],
    },
]

CONFIRMED = [
    "NY:MDL-4(7)-multiple-dwelling: quote and effect match MDL 4(7); counting by actual letting or occupancy is right.",
    "NY:MDL-302(1)(b) (apart from R3-02's scope): bar on rent and use and occupancy, no revival by a later certificate, damage claims unaffected, Chatsworth exception; deposit retention is recovery (GOL 7-103 trust).",
    "NY:MDL-325(2) (apart from R3-03): bar applies to multiple dwellings only and is not discretionary.",
    "NYC:ADC-27-2107(b)-rent-stay: discretionary stay for one- and two-family houses; consistent with 9 Montague Terrace.",
    "NY:CPLR-214-i-consumer-debt-S9760: text, 90-day effective clause and pending status confirmed on the Assembly action list (last action 06/03/2026, returned to senate, not delivered).",
    "NY:RPL-214 and NY:RPL-214(15)-high-rent: fifteen exemptions and the 245% figure match the text; DHCR publishes the figure.",
    "NY:ADJ-willful-standard: two-part structure, factors and discretionary 'up to' amount are right (see R3-10 for one example); no Appellate Division or Appellate Term decision construing 'willfully' in 7-108 was found (CourtListener search, 2026-09-29).",
    "NY:ADJ-lease-break-charge: JMD Holding test, RPL 227-e waiver bar, not retained from the deposit, not a FARE fee.",
    "NY:ADJ-early-departure-rent-retention: only rent already due and unpaid, and only before a new tenant's lease (Kunik).",
    "NY:ABP-1422 (apart from R3-13): 90-day first-class and 60-day certified notices and both exceptions match the text.",
    "NY:23NYCRR-1.1(d)-not-lease: 'credit has been extended' definition supports the rule (provenance note R3-14).",
    "NY:CPLR-3215(g)(3): mailing, envelope, 20 days, small-claims exclusion.",
    "NY:ADJ-MDL-rent-bar-not-1-2-family: Pickering (App Term 2d) confines the rent forfeitures to multiple dwellings.",
    "NY:ADJ-RPL-232-after-october; NY:ADJ-RPL-232-agreement-sets-end (City of New York v State controls); NY:ADJ-RPL-232-oral-term-over-one-year (GOL 5-703, Darling, T.I.B.).",
    "RPL 232 interaction with T.I.B., Srinivasan and RPL 232-c: correctly stated in NY:COMMONLAW-NYC-monthly-tenant-surrender and NY:ADJ-RPL-232-after-october; the error is confined to R3-01.",
    "NY:RPL-440(1)-rent-collection: a former tenant's rent balance is rent; non-rent charges and use and occupancy are outside under strict construction (Weingast, Kreuter; RPL 220); statements and refunds without custody or demand are outside; the incidental-feature rule does not reach rent collection within services about the rental (Fields, Dodge; G.C. Fortune adds the 3d Dept).",
    "NY:ADJ-broker-owner-and-staff; NY:RPL-442-f-exemptions; NY:RPL-442-fee-split (442 lists leasing and renting, not rent collection).",
    "NY:HANDOFF-broker-config-collects-rent, -settlement-only, -under-broker, -collection-agency: each configuration's rule follows from 440(1), 440(3), 442-f and the DOS 'handling another person's money' line.",
    "NY:RPL-442-d-442-e-unlicensed (apart from R3-06): misdemeanor, DOS enforcement, owner's claim unaffected.",
    "NY:ADJ-vacate-order-rent; NY:COMMONLAW-constructive-eviction (Barash).",
    "NY:COMMONLAW-mortgagee-assignment-of-rents (Sullivan v Rosson); NY:CPLR-6401-foreclosure-receiver; NY:RPAPL-776-778-administrator; NYC:HMC-27-2135(c)-receiver-rents; NYC:HMC-27-2147-rent-levy; NY:COMMONLAW-owner-death-agency (content).",
    "NY:CPLR-3015(e)-licence-pleading; NY:RPL-235-a.",
    "NYC:HMC-27-2017.5-turnover; NYC:HMC-27-2056.8-lead-turnover; NYC:HMC-27-2087-cellar-basement; NYC:HMC-27-2128-owner-debt; NYC:HMC-27-2045-detector-charge (apart from R3-12).",
    "US:11USC541-704-owner-chapter7; US:11USC1107-1306-owner-reorganization; US:24CFR982.404(d)(3)-(4).",
    "Date arithmetic: T-232 vacate Tuesday 2026-06-30, day 14 Tuesday 2026-07-14 (no holiday); C12 Friday 2026-12-11, day 14 Friday 2026-12-25 (holiday), due Monday 2026-12-28.",
    "Mechanical checks: check_review.py 499 in scope, 0 not cited; stage_a_check.py 0 errors in all four files and cross-file.",
]

TEST_CASES = [
    ("C4", "Agree in part. Three-family house: multiple dwelling; no interest-bearing account; bank notice if banked; three-year repaint, painting records and HPD registration apply. Rent bar for no certificate only if the house was built or converted to three families after 1929-04-18 (or is outside the MDL 301(1) exceptions) and lacks a certificate for that use (R3-02). An unregistered owner recovers no rent until it registers, then recovers all of it (R3-03). Good Cause may be excluded if the owner is a small landlord (RPL 214(1))."),
    ("C6", "Agree."),
    ("C7", "Agree, with R3-03 (registration suspends, it does not forfeit) and R3-04 (302-a exceptions)."),
    ("C9", "Agree: the ABP 1422 notice is excused where the holder can show its only address is not the tenant's current one."),
    ("C10", "Agree: the buyer recovers no rent until it registers, and then recovers the rent that accrued meanwhile (R3-03)."),
    ("C14", "Agree in part. Add: the agency needs a New York broker's licence for any rent part (R3-05); if the owner is a foreign entity it must hold New York authority before suing (R3-08); once S9760 is law, the consumer-debt suit procedure applies as well as the three-year limit (R3-07)."),
    ("T-232", "Disagree (R3-01). Oral, $2,400 a month, nothing said about length: a month-to-month tenancy. The tenant leaving at the end of June owes nothing after June 30; July rent may not be kept from the deposit. Statement due Tuesday 2026-07-14. If the parties had agreed on 'a long time' or 'indefinitely', RPL 232 applies: term to 2026-10-01, July rent may be kept if unpaid and no new tenant, August and September a later claim subject to RPL 227-e."),
    ("T-vacate", "Agree, adding that March 1-9 rent is owed and nothing from March 10 (R3-11)."),
    ("T-lead", "Agree: lead turnover is the owner's cost; a battery-operated combination smoke/CO device the tenant removed is charged at most $50 (a hardwired one under the general damage rule, R3-12)."),
    ("T-collect", "Agree on all three branches."),
]


def md_escape(s):
    return s.replace("|", "\\|")


def build():
    sev_order = {"critical": 0, "major": 1, "minor": 2}
    findings = sorted(FINDINGS, key=lambda f: (sev_order[f["severity"]], f["id"]))
    data = {"findings": findings, "confirmed": CONFIRMED, "prior_rounds": []}
    pr = ROOT / "review/ir3_prior_rounds.json"
    if pr.exists():
        data["prior_rounds"] = json.loads(pr.read_text())
    (ROOT / "review/independent_review_3.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")

    by_sev, by_kind = {}, {}
    for f in findings:
        by_sev[f["severity"]] = by_sev.get(f["severity"], 0) + 1
        by_kind[f["kind"]] = by_kind.get(f["kind"], 0) + 1

    L = []
    L.append("# Independent review 3: round-2 corrections and the building, owner and collecting-agent sweep (NYC market-rate)")
    L.append("")
    L.append("2026-09-29. Limited scope: the atoms added or restated by build/apply_review2.py and build/sweep_building_owner.py, the walk")
    L.append("text that cites them (review/NYC_MARKET_RATE.md), and the completeness of discovery family 10. Report only; nothing else")
    L.append("was edited. Every quote below is checked verbatim against its saved source by review/ir3_verify.py.")
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append(f"Findings: {len(findings)} ({', '.join(f'{k} {v}' for k, v in sorted(by_sev.items(), key=lambda kv: sev_order[kv[0]]))}).")
    L.append("")
    L.append("By kind: " + "; ".join(f"{k} {v}" for k, v in sorted(by_kind.items())) + ".")
    L.append("")
    L.append("Overall judgment: **accept after listed corrections.** The sweep's structure is sound and most of its 34 atoms are right,")
    L.append("including all four broker-licensing configurations. Six corrections change amounts, forfeitures or licences: the RPL 232")
    L.append("ruling applies the October 1 term to a bare monthly rent, contrary to the Appellate Term's presumption of a monthly tenancy")
    L.append("(R3-01); the certificate-of-occupancy bar omits the statute's pre-1929 exceptions (R3-02); registration is treated as a")
    L.append("forfeiture in C4 when it only suspends recovery (R3-03); the rent-impairing bar omits its statutory exceptions (R3-04); C14")
    L.append("omits the agency's broker licence (R3-05); and the fee consequence of unlicensed collection is understated (R3-06). Family 10")
    L.append("still missed the owner's capacity to sue (R3-08) and the loft-law scope gate (R3-09).")
    L.append("")
    L.append("## Findings (most severe first)")
    L.append("")
    for f in findings:
        L.append(f"### {f['id']} ({f['severity']}, {f['kind']}): step {f['step']}")
        L.append("")
        L.append("Rules: " + ", ".join(f"`{r}`" for r in f["rule_ids"]))
        L.append("")
        L.append("What is wrong. " + f["finding"])
        L.append("")
        L.append("Correct rule. " + f["correct_rule"])
        L.append("")
        L.append("Evidence:")
        for e in f["evidence"]:
            q = " ".join(e["quote"].split())
            L.append(f"- `{e['source_file']}`: \"{q}\"")
        L.append("")
    L.append("## Confirmed")
    L.append("")
    for c in CONFIRMED:
        L.append(f"- {c}")
    L.append("")
    L.append("## Test cases in scope: this review's answers")
    L.append("")
    for k, v in TEST_CASES:
        L.append(f"- {k}. {v}")
    L.append("")
    L.append("## Earlier rounds (written after the findings above were saved)")
    L.append("")
    if data["prior_rounds"]:
        for p in data["prior_rounds"]:
            L.append(f"- {p['item']}: **{p['rating']}**. {p['note']}")
    else:
        L.append("- Pending.")
    L.append("")
    L.append("## Method")
    L.append("")
    L.append("- Read APERTURE.md, STAGE_A.md (family 10), HANDOFF_CONNECTION.md, the walk in full, and every in-scope atom in full")
    L.append("  (review/ir3_dump.py writes them to a scratch file), before opening any earlier review or disposition.")
    L.append("- Read the source text behind each ruling in scope; for RPL 232 read Stauber, T.I.B., Srinivasan, Spies, Gilfoyle, Hyacinth")
    L.append("  Green, Abbey and 1239 Madison, then searched CourtListener for later New York authority (found Gerolemou v Soliz and its")
    L.append("  2024-2026 Appellate Division citations). For registration, searched MDL 325 case law (found 9 Montague Terrace). For broker")
    L.append("  licensing, searched every New York decision quoting the 'collects or offers or attempts to collect rent' clause (found")
    L.append("  G.C. Fortune). For 'willful', searched 7-108 decisions through 2026 (none at appellate level construing it).")
    L.append("- Checked S9760 on the Assembly action list (curl, saved). Computed weekdays with Python.")
    L.append("- Family 10 re-enumerated independently: certificate of occupancy, registration, rent-impairing violations, vacate orders,")
    L.append("  receivers and administrators, levies, owner insolvency and death, mortgagees, agent licensing, owner-entity capacity,")
    L.append("  loft-law buildings, flood disclosure (RPL 231-b: notice duties only, no rent consequence), smoke and lead duties.")
    L.append("- New sources saved with prefix REVIEW3_ in sources/. Tools: review/ir3_dump.py, review/ir3_build.py, review/ir3_verify.py.")
    L.append("- Ran check_review.py and stage_a_check.py (both clean) and ir3_verify.py (all quotes verbatim, all rule ids exist, self-test")
    L.append("  catches a planted bad quote and a planted bad id).")
    L.append("")
    (ROOT / "review/INDEPENDENT_REVIEW_3.md").write_text("\n".join(L))
    print(f"wrote {len(findings)} findings, {len(CONFIRMED)} confirmed, {len(data['prior_rounds'])} prior-round items")


if __name__ == "__main__":
    build()
