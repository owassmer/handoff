"""IR5B: build review/independent_review_5b.json from the findings below (run, then ir5b_render.py, then ir5b_verify.py).

Every evidence quote is copied from the saved source named with it; ir5b_verify.py checks each one verbatim
(whitespace-normalized) and checks every rule id against stage-a/{NY,NYC,US}.json.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
S = "sources/"

FINDINGS = [
    {
        "id": "R5B-01",
        "kind": "misread-authority",
        "severity": "critical",
        "rule_ids": ["NY:ADJ-vacate-order-rent", "NY:RPL-227"],
        "step": "3.6; test case T-vacate",
        "finding": (
            "T-vacate states that the March installment due 2026-03-01 'is not barred by the order' and leaves the prepaid "
            "days after the 2026-03-10 ouster unresolved, and NY:ADJ-vacate-order-rent says only that the order 'does not bar "
            "rent that fell due before it'. That is half the rule. New York law makes the eviction no defense to an "
            "installment already due, but a tenant who leaves because of the eviction recovers the proportionate part of the "
            "rent paid in advance for the rest of the period, on failure of consideration (Appellate Term, First Department, "
            "Kennedy v Peterart Realty, citing Matter of Strasburger, Court of Appeals). Read as written, the walk lets the "
            "landlord keep 21 days of March rent (or apply the deposit to them if March is unpaid) that the tenant is entitled "
            "to recover. The rule also cites Younger (App Div 1917) for the timing point, but in Younger the eviction came "
            "before the rent fell due, so Younger does not decide an installment that straddles the ouster."
        ),
        "correct_rule": (
            "Tenant ousted by a government vacate order issued for conditions the owner was bound, wholly or in part, to "
            "correct: (1) rent that fell due after the ouster is not owed (Younger; Barash). (2) An installment that fell "
            "due before the ouster is owed as an installment, but a tenant who vacated because of the ouster recovers the "
            "part of it covering the days after the ouster (per-day share of the period) on failure of consideration; on "
            "the move-out account the landlord credits that share, so the rent retained or claimed for the period is only "
            "the per-day share up to and including the day of the ouster. If the installment was paid, the unearned share "
            "is refunded; if unpaid, only the earned share is charged. (3) Because the owner was at fault, the tenant "
            "also has a damages claim for the value of the rest of the term less the rent reserved (Strasburger, stating "
            "the Mack v Patchin measure where the lessor is at fault), which offsets any landlord claim. (4) Where the "
            "untenantability came from a sudden casualty (fire, collapse, flood), RPL 227 reaches the same apportionment by "
            "statute: rent paid in advance is adjusted to the surrender date. (5) A tenant who stays in possession of any "
            "part recovers no proportionate share (Kennedy). T-vacate: March rent is earned for 2026-03-01 to 2026-03-10 "
            "(10/31 of the installment); 21/31 is refunded or credited."
        ),
        "evidence": [
            {"source_file": S + "REVIEW5B_NY_CASE_Kennedy_v_Peterart_1939_AppTerm.txt",
             "quote": "it was no defense to the rent which had become due in advance September first"},
            {"source_file": S + "REVIEW5B_NY_CASE_Kennedy_v_Peterart_1939_AppTerm.txt",
             "quote": "If by reason of the eviction plaintiff had vacated the premises she would have been entitled to recover the proportionate part of the rent paid in advance for the balance of the month of September on the ground of failure of consideration"},
            {"source_file": S + "REVIEW5B_NY_CASE_Kennedy_v_Peterart_1939_AppTerm.txt",
             "quote": "Supreme Court, Appellate Term, First Department,"},
            {"source_file": S + "REVIEW5B_NY_CASE_Matter_of_Strasburger_1892_CoA.txt",
             "quote": "But the general rule is, in the absence of fault in the lessor, that the lessee can recover only such rent as he has advanced, and such mesne profits as he is liable to pay over."},
            {"source_file": S + "REVIEW5B_NY_CASE_Matter_of_Strasburger_1892_CoA.txt",
             "quote": "This would be so if the breach of the covenants for quiet enjoyment resulted from the fault of Strasburger."},
            {"source_file": S + "SWEEP_NY_CASE_Younger_v_Campbell_1917_1stDept.txt",
             "quote": "The defendant resisted payment upon the ground that he was evicted before the day the rent would have become due under the lease."},
            {"source_file": S + "NY_RPL_227.txt",
             "quote": "Any rent paid in advance or which may have accrued by the terms of a lease or any other hiring shall be adjusted to the date of such surrender."},
        ],
    },
    {
        "id": "R5B-02",
        "kind": "missing-exception",
        "severity": "critical",
        "rule_ids": ["NY:RPL-227", "NY:ADJ-vacate-order-rent"],
        "step": "2.6; 3.6",
        "finding": (
            "NY:RPL-227 (walk 2.6) ends rent whenever the building is 'destroyed or so injured ... as to be untenantable' "
            "without tenant fault. The Commission of Appeals confined the statute to injury from a sudden and unexpected "
            "cause, not gradual deterioration (Suydam v Jackson), so a tenant who leaves over conditions that developed "
            "through wear and neglect cannot invoke RPL 227; that tenant needs constructive eviction (landlord's wrongful "
            "act, abandonment) or the habitability offset. Walk 2.6 also omits the section's last sentence (prepaid rent "
            "adjusted to the surrender date). Separately, NY:ADJ-vacate-order-rent reads Younger (Municipal Court) as "
            "holding RPL 227 inapplicable to vacate orders; the court's words keep RPL 227 where the untenantability "
            "'arises from direct injury or destruction', and the First Department applied RPL 227 to a physical condition "
            "cured under a municipal order (Warrin v Haverty)."
        ),
        "correct_rule": (
            "RPL 227 applies only where the building is destroyed or physically injured by a sudden, unexpected cause "
            "(fire, storm, collapse, flood or a kindred casualty), the injury leaves it untenantable, the tenant was not at "
            "fault, no written agreement provides otherwise, and the tenant quits and surrenders. Then no rent is owed "
            "after the surrender and rent paid in advance or accrued is adjusted to the surrender date. Gradual "
            "deterioration is outside RPL 227. A vacate order issued because of such a physical casualty is within RPL "
            "227; a vacate order for missing equipment, an unlawful occupancy or other non-physical noncompliance is "
            "governed by the eviction rule in NY:ADJ-vacate-order-rent as corrected by R5B-01."
        ),
        "evidence": [
            {"source_file": S + "REVIEW5B_NY_CASE_Suydam_v_Jackson_1873_CoA.txt",
             "quote": "The leaking was not caused by any sudden, unusual, or fortuitous circumstance, but seems to have been caused' by gradual wear and decay. The courts below held that the case was not within the statute, and that the lessee remained liable for the rent."},
            {"source_file": S + "REVIEW5B_NY_CASE_Suydam_v_Jackson_1873_CoA.txt",
             "quote": "New York Commission of Appeals"},
            {"source_file": S + "SWEEP_NY_CASE_Younger_v_Campbell_1916_MunCt.txt",
             "quote": "except where the condition of untenantability arises from direct injury or destruction."},
            {"source_file": S + "REVIEW5B_NY_CASE_Warrin_v_Haverty_1913_1stDept.txt",
             "quote": "All that the statute requires in this respect is that the injury shall be of a physical nature and that the premises are thereby rendered untenantable and unfit for occupancy"},
            {"source_file": S + "NY_RPL_227.txt",
             "quote": "Any rent paid in advance or which may have accrued by the terms of a lease or any other hiring shall be adjusted to the date of such surrender."},
        ],
    },
    {
        "id": "R5B-03",
        "kind": "error",
        "severity": "critical",
        "rule_ids": ["NY:RPL-223"],
        "step": "2.1; test case C10",
        "finding": (
            "Walk 2.1 says 'The buyer can collect the departing tenant's balance under the lease', and NY:RPL-223's effect "
            "says a successor landlord 'may pursue the departing tenant's balance under the lease'. RPL 223 gives the "
            "grantee the grantor's remedies going forward; rent that fell due before title passed stays the seller's unless "
            "the seller assigned it, and even an assignee of those arrears cannot use the summary remedies (Appellate Term, "
            "First Department, Getty Realty). Who is paid is wrong for every pre-sale arrear."
        ),
        "correct_rule": (
            "After a conveyance of the building mid-tenancy: rent and other lease charges that fell due before title "
            "passed belong to the seller and are collected by or for the seller, not the buyer, unless the seller assigned "
            "them to the buyer in writing; rent and charges falling due after title passed belong to the buyer, who has "
            "the seller's remedies under RPL 223. The buyer, holding the deposit under GOL 7-105, may not keep it for "
            "pre-sale arrears it does not own; the statement itemizes only amounts owed to the buyer and returns the rest. "
            "An assignee of pre-sale arrears sues on them as an assignee, not in a summary proceeding."
        ),
        "evidence": [
            {"source_file": S + "REVIEW5B_NY_CASE_Getty_Realty_v_2East61st_1939_AppTerm.txt",
             "quote": "There is no provision in the deed purporting to transfer the arrearage of rents to the grantee, and in the absence of such transfer the present landlord had no right to rents which had become due at the time of the passing of title."},
            {"source_file": S + "REVIEW5B_NY_CASE_Getty_Realty_v_2East61st_1939_AppTerm.txt",
             "quote": "the reference in section 223 of the Real Property Law to assignees of rents is to assignees of rents accruing after the grants therein referred to."},
            {"source_file": S + "REVIEW5B_NY_CASE_Getty_Realty_v_2East61st_1939_AppTerm.txt",
             "quote": "Supreme Court, Appellate Term, First Department, May 2, 1939."},
            {"source_file": S + "NY_RPL_223.txt",
             "quote": "has the same remedies, by entry, action or otherwise, for the nonperformance of any agreement contained in the assigned lease for the recovery of rent"},
        ],
    },
    {
        "id": "R5B-04",
        "kind": "contradiction",
        "severity": "critical",
        "rule_ids": ["NY:ADJ-tenant-deposit-claim-limitations", "US:11USC108(c)-extension", "US:50USC3936-tolling",
                     "NY:CPLR-210-death"],
        "step": "7.6; 8.10 (time limits)",
        "finding": (
            "NY:ADJ-tenant-deposit-claim-limitations lists US:11USC108(c)-extension as tolling the former tenant's own "
            "deposit claims. Section 108(c) extends periods for suing on a claim against the debtor (the landlord's "
            "claim); the debtor-tenant's own claim passes to the trustee and is extended by 108(a) instead, to the later of "
            "the period's end or two years after the order for relief. The walk then tells the operator to 'Keep the "
            "settlement file six years', which contradicts the extensions the same rule lists: military service is "
            "excluded from the period without limit (3936), 108(a) can run two years past the order for relief, and a "
            "tenant's estate has one year after death (CPLR 210(a))."
        ),
        "correct_rule": (
            "The former tenant's deposit claims run three years (punitive damages, forfeiture-only recovery) or six years "
            "(deposit kept without lawful basis) from the end of the 14 days, extended by: the tenant's military service "
            "(50 USC 3936, not counted); the tenant's bankruptcy, where the trustee may sue until the later of the period's "
            "end or two years after the order for relief (11 USC 108(a)); and the tenant's death, where the representative "
            "may sue within one year after death if the period had not run (CPLR 210(a)). 11 USC 108(c) extends only the "
            "landlord's time to sue the tenant. Operator step: keep the settlement file until the latest of those dates, "
            "not a flat six years."
        ),
        "evidence": [
            {"source_file": S + "REVIEW5B_US_11USC_108_uscode.txt",
             "quote": "(a) If applicable nonbankruptcy law, an order entered in a nonbankruptcy proceeding, or an agreement fixes a period within which the debtor may commence an action, and such period has not expired before the date of the filing of the petition, the trustee may commence such action only before the later of-"},
            {"source_file": S + "REVIEW5B_US_11USC_108_uscode.txt", "quote": "(2) two years after the order for relief."},
            {"source_file": S + "REVIEW5B_US_11USC_108_uscode.txt",
             "quote": "fixes a period for commencing or continuing a civil action in a court other than a bankruptcy court on a claim against the debtor"},
            {"source_file": S + "REVIEW4A_US_50USC_3936_uscode.txt",
             "quote": "The period of a servicemember's military service may not be included in computing any period limited by law, regulation, or order for the bringing of any action or proceeding in a court"},
            {"source_file": S + "REVIEW4A_NY_CPLR_210_nysenate.txt",
             "quote": "an action may be commenced by his representative within one year after his death."},
        ],
    },
    {
        "id": "R5B-05",
        "kind": "missing-exception",
        "severity": "major",
        "rule_ids": ["NY:RPAPL-1305-successor"],
        "step": "0.5 (who is owed the rent)",
        "finding": (
            "The rule and walk 0.5 state the foreclosure successor takes subject to the market-rate tenant's right to stay "
            "for the greater of 90 days or the rest of the lease 'on the same terms', without the section's limits: a "
            "successor that will occupy one unit as its primary residence may cut that one unit to 90 days; the lease "
            "qualifies only if the tenant is not the owner and the rent is not substantially below fair market rent; and "
            "a tenant who moved in after the foreclosure began keeps the rest of the lease only under a good-faith lease "
            "and for at most three years. Each limit moves the date the tenancy can end and so the rent owed."
        ),
        "correct_rule": (
            "RPAPL 1305(2): a tenant of a unit not rent-controlled or stabilized may stay for the greater of 90 days from "
            "the successor's notice or (b) the rest of the lease if it occupied at the start of the foreclosure or got the "
            "1303 notice, or (c) the rest of a good-faith lease, up to three years, if it moved in later; the lease counts "
            "only if the tenant is not the owner and the rent is not substantially below fair market rent; a successor "
            "that will occupy a single unsubsidized unit as its primary residence may limit that one unit to 90 days. The "
            "tenancy continues on the terms in effect at the judgment or transfer."
        ),
        "evidence": [
            {"source_file": S + "REVIEW4A_NY_RPAPL_1305_nysenate.txt",
             "quote": "provided that if a successor in interest who acquires title to such residential real property intends to occupy a single unit as his or her primary residence"},
            {"source_file": S + "REVIEW4A_NY_RPAPL_1305_nysenate.txt",
             "quote": "For a lease to qualify under this subdivision, the tenant under such lease may not be the owner of the residential real property, and such lease must require the payment of rent for such unit that is not substantially less than the fair market rent for the unit"},
            {"source_file": S + "REVIEW4A_NY_RPAPL_1305_nysenate.txt", "quote": "up to a maximum of three years"},
        ],
    },
    {
        "id": "R5B-06",
        "kind": "misstatement-in-walk",
        "severity": "major",
        "rule_ids": ["NY:ADJ-provide-address-branches", "NY:GOL-7-108(1-a)(e)"],
        "step": "6.5; test case C3",
        "finding": (
            "C3 gives the tenant only a forwarding email and then says the refund goes 'by a payment that reaches the "
            "tenant, such as a transfer to her account or a check to a postal address'. NY:ADJ-provide-address-branches "
            "branch (a) sends the refund 'to the forwarding address or by a payment the tenant can receive' but gives no "
            "compliant act where the landlord holds an email or phone number and neither a postal address (other than the "
            "unit) nor payment details. Waiting for an address forfeits (Prando), so the operator needs the act."
        ),
        "correct_rule": (
            "Within the 14 days the landlord sends the statement to the known email or phone number and dispatches the "
            "refund by a means directed to the tenant: an electronic payment to an account or payment address the "
            "landlord holds for the tenant, or, if it holds none, a check mailed to the last known postal address (the "
            "vacated unit), with the emailed statement saying where and how the refund was sent. It does not hold the "
            "refund for an address."
        ),
        "evidence": [
            {"source_file": S + "NY_GOL_7-108_nysenate.txt", "quote": "shall return any remaining portion of the deposit to the tenant"},
            {"source_file": S + "NY_CASE_Prando_v_Kelly_2021.txt",
             "quote": "Defendant Renee Kelly asserted that she had delayed returning plaintiff's security deposit because, among other things, she had not known his new address."},
        ],
    },
    {
        "id": "R5B-07",
        "kind": "contradiction",
        "severity": "minor",
        "rule_ids": ["NY:HANDOFF-broker-config-collection-agency", "NY:RPL-440(1)-rent-collection"],
        "step": "8.6a",
        "finding": (
            "NY:HANDOFF-broker-config-collection-agency is conditioned on handing off 'a former tenant's balance that "
            "includes rent or use and occupancy', while NY:RPL-440(1)-rent-collection holds that collecting use and "
            "occupancy owed after the tenancy ended is not collecting rent and needs no broker licence."
        ),
        "correct_rule": (
            "The broker licence is needed only for the rent part (rent that fell due under the tenancy, including rent "
            "reserved for months after an early departure); use and occupancy for occupancy after the tenancy ended, "
            "damage, fees and utilities need none."
        ),
        "evidence": [
            {"source_file": S + "SWEEP_NY_RPL_440_nysenate.txt", "quote": "collects or offers or attempts to collect rent for the use of real estate"},
            {"source_file": S + "NY_RPL_220.txt",
             "quote": "The landlord may recover a reasonable compensation for the use and occupation of real property"},
        ],
    },
    {
        "id": "R5B-08",
        "kind": "hedging",
        "severity": "minor",
        "rule_ids": ["NY:ADJ-willful-standard"],
        "step": "7.5",
        "finding": (
            "The rule's judgment terms label the standard 'willfully (knew or should have known)', the single-part test "
            "its own effect and reasoning reject (knowing, intentional or deliberate failure; should-have-known goes only "
            "to knowledge of the law). The label will be read as the test."
        ),
        "correct_rule": (
            "Judgment term: 'willfully: knowing, intentional or deliberate failure (not negligence or inadvertence), with "
            "knowledge of the law charged to an experienced landlord or managing agent'."
        ),
        "evidence": [
            {"source_file": S + "NY_CASE_Karole_v_340WEnd_2022.txt", "quote": "requires more than inadvertence"},
            {"source_file": S + "NY_CASE_Prando_v_Kelly_2021.txt", "quote": "not willful, and, thus, that punitive damages were not warranted"},
        ],
    },
    {
        "id": "R5B-09",
        "kind": "misstatement-in-walk",
        "severity": "minor",
        "rule_ids": ["NYC:HMC-27-2045-detector-charge"],
        "step": "5.5a; test case T-lead",
        "finding": (
            "The rule says a device 'replaced because its useful life expired ... is the owner's cost and is not charged'. "
            "27-2045(e) makes the occupant of the unit in which a device is installed reimburse the owner, within the "
            "caps, including for a device installed to replace one past its useful life. The departed tenant is not that "
            "occupant for a turnover replacement, so the move-out result holds, but a (e) reimbursement for a device "
            "installed during the tenancy and left unpaid is a lawful charge. T-lead also omits that the $50 cap is for "
            "a battery-operated combination device; a hardwired one is charged under the damage rule."
        ),
        "correct_rule": (
            "At move-out: a battery-operated device the tenant removed or disabled is charged within $25/$50/$75; a "
            "device replaced at turnover for age or defect is not charged to the departed tenant; a (e) reimbursement "
            "for a device installed during the tenancy (including a useful-life replacement) and unpaid may be claimed "
            "within the caps, separately from the deposit."
        ),
        "evidence": [
            {"source_file": S + "SWEEP_NYC_ADC_27-2045.txt",
             "quote": "or installed to replace a device that has exceeded the manufacturer's useful life or that has been lost or damaged by such occupant"},
            {"source_file": S + "SWEEP_NYC_ADC_27-2045.txt",
             "quote": "shall reimburse the owner for the cost of providing and installing such device"},
        ],
    },
    {
        "id": "R5B-10",
        "kind": "misstatement-in-walk",
        "severity": "minor",
        "rule_ids": ["NY:RPL-227-e"],
        "step": "3.3",
        "finding": (
            "Walk 3.3 says 'A new lease ends the old one.' The statute ends the old lease only when the landlord re-lets at "
            "fair market value or the agreed rate; the rule states this correctly, the walk drops the condition."
        ),
        "correct_rule": "A new tenant's lease at fair market value or the agreed rate, once in effect, ends the departed tenant's lease.",
        "evidence": [
            {"source_file": S + "NY_RPL_227-E.txt",
             "quote": "If the landlord rents the premises at fair market value or at the rate agreed to during the term of the tenancy, the new tenant's lease shall, once in effect, terminate the previous tenant's lease"},
        ],
    },
]

T_VACATE = {
    "rule": (
        "When an owner-caused government vacate order ousts a market-rate NYC tenant mid-month after that month's rent "
        "fell due and was paid, the rent for the days after the ouster is recoverable by the tenant: the landlord refunds "
        "or credits the per-day share of the installment for the days after the ouster (apportionment on failure of "
        "consideration), and rent earned is only the share up to and including the day of the ouster. If the installment "
        "is unpaid, only the earned share is charged or kept from the deposit. Because the owner caused the order, the "
        "tenant also has a damages claim for the value of the rest of the term less the rent reserved. Where the order "
        "follows a sudden physical casualty, RPL 227 imposes the same adjustment to the surrender date. A tenant who keeps "
        "possession of any part recovers no proportionate share. Controlling authority: Matter of Strasburger (Court of "
        "Appeals 1892: an evicted lessee recovers the rent it advanced, and the full loss of bargain where the lessor is at "
        "fault), applied to a mid-month eviction by Kennedy v Peterart Realty (Appellate Term, First Department 1939, "
        "binding on the New York and Bronx County Civil Courts; Peerless Candy, Appellate Term, Second Department 1925, "
        "states the same measure for Kings, Queens and Richmond). It prevails over the reading that the pre-ouster "
        "installment is simply 'not barred': that reading states only the first half of Kennedy (no defense to rent "
        "already due) and ignores its holding on recovery, and Younger (App Div 1917) is not contrary because there the "
        "eviction preceded the due date. No later decision found limits Kennedy or Strasburger (CourtListener searches "
        "for citing cases and for the rule's terms, 2026-09-29)."
    ),
    "evidence": [
        {"source_file": S + "REVIEW5B_NY_CASE_Kennedy_v_Peterart_1939_AppTerm.txt",
         "quote": "If by reason of the eviction plaintiff had vacated the premises she would have been entitled to recover the proportionate part of the rent paid in advance for the balance of the month of September on the ground of failure of consideration"},
        {"source_file": S + "REVIEW5B_NY_CASE_Kennedy_v_Peterart_1939_AppTerm.txt",
         "quote": "but her retention of possession to the end of the term prevents any such recovery."},
        {"source_file": S + "REVIEW5B_NY_CASE_Matter_of_Strasburger_1892_CoA.txt",
         "quote": "But the general rule is, in the absence of fault in the lessor, that the lessee can recover only such rent as he has advanced, and such mesne profits as he is liable to pay over."},
        {"source_file": S + "REVIEW5B_NY_CASE_Peerless_Candy_v_Halbreich_1925.txt",
         "quote": "If he does not remain in possession and vacates the premises treating the partial eviction as one from the entire demise and the relationship of landlord and tenant ceases, his damages would be: (a) The proportionate part of the rent due or paid"},
        {"source_file": S + "SWEEP_NY_CASE_Younger_v_Campbell_1917_1stDept.txt",
         "quote": "the landlord cannot recover any rent for the period after the eviction occurred."},
        {"source_file": S + "SWEEP_NY_CASE_Barash_v_PennTerminal_1970_CoA.txt",
         "quote": "In the case of actual eviction, even where the tenant is only partially evicted, liability for all rent is suspended"},
        {"source_file": S + "NY_RPL_227.txt",
         "quote": "Any rent paid in advance or which may have accrued by the terms of a lease or any other hiring shall be adjusted to the date of such surrender."},
    ],
}

if __name__ == "__main__":
    import ir5b_text  # noqa: E402  (confirmed list, test cases, method)
    out = {
        "review": "Independent review 5B (correctness), market-rate NYC walk",
        "date": "2026-09-29",
        "findings": FINDINGS,
        "confirmed": ir5b_text.CONFIRMED,
        "rules_checked_count": ir5b_text.RULES_CHECKED,
        "t_vacate_ruling": T_VACATE,
        "test_cases": ir5b_text.TEST_CASES,
    }
    (ROOT / "review/independent_review_5b.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print("findings", len(FINDINGS), "confirmed", len(ir5b_text.CONFIRMED))
