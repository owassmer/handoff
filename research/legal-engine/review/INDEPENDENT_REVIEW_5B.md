# Independent review 5B: correctness of the market-rate NYC walk

Reviewer 5B, 2026-09-29/30. Report only; no rule file, walk, source or skill was edited. Evidence script: `python3 review/ir5b_verify.py` (all quotes verbatim, all ids exist, self-test passes).

## Summary

- Rules checked: 455 (every id the walk cites: 453 in scope plus 2 cited from outside scope), each read beside its walk sentence; sources opened in context where the effect goes beyond the quote.
- Findings: 10. By severity: critical 4, major 2, minor 4. By kind: contradiction 2, error 1, hedging 1, misread-authority 1, missing-exception 2, misstatement-in-walk 3.
- Judgment: **accept after the listed corrections.** The four critical findings change who is paid or how much: the prepaid rent after an owner-caused vacate order (R5B-01), the scope of RPL 227 (R5B-02), pre-sale rent arrears after a building sale (R5B-03), and the tenant's extended time to sue and the file-retention period (R5B-04). Everything else checked is confirmed below; the interpretive rulings re-decided (willfulness, address and dispatch, RPL 232, co-tenants, forfeiture survival, fee retention, lease balance not consumer credit, 2% interest, broker and DCWP licensing, FDCPA configurations, SHIELD dates, bankruptcy payee and setoff) hold.
- T-vacate open branch: decided. The tenant recovers the per-day share of the prepaid installment for the days after the ouster (apportioned on failure of consideration); see the ruling below.

## Findings (most severe first)

### R5B-01 (critical, misread-authority)

- Rules: `NY:ADJ-vacate-order-rent` (round 4), `NY:RPL-227`
- Walk step: 3.6; test case T-vacate
- What is wrong: T-vacate states that the March installment due 2026-03-01 'is not barred by the order' and leaves the prepaid days after the 2026-03-10 ouster unresolved, and NY:ADJ-vacate-order-rent says only that the order 'does not bar rent that fell due before it'. That is half the rule. New York law makes the eviction no defense to an installment already due, but a tenant who leaves because of the eviction recovers the proportionate part of the rent paid in advance for the rest of the period, on failure of consideration (Appellate Term, First Department, Kennedy v Peterart Realty, citing Matter of Strasburger, Court of Appeals). Read as written, the walk lets the landlord keep 21 days of March rent (or apply the deposit to them if March is unpaid) that the tenant is entitled to recover. The rule also cites Younger (App Div 1917) for the timing point, but in Younger the eviction came before the rent fell due, so Younger does not decide an installment that straddles the ouster.
- Correct rule: Tenant ousted by a government vacate order issued for conditions the owner was bound, wholly or in part, to correct: (1) rent that fell due after the ouster is not owed (Younger; Barash). (2) An installment that fell due before the ouster is owed as an installment, but a tenant who vacated because of the ouster recovers the part of it covering the days after the ouster (per-day share of the period) on failure of consideration; on the move-out account the landlord credits that share, so the rent retained or claimed for the period is only the per-day share up to and including the day of the ouster. If the installment was paid, the unearned share is refunded; if unpaid, only the earned share is charged. (3) Because the owner was at fault, the tenant also has a damages claim for the value of the rest of the term less the rent reserved (Strasburger, stating the Mack v Patchin measure where the lessor is at fault), which offsets any landlord claim. (4) Where the untenantability came from a sudden casualty (fire, collapse, flood), RPL 227 reaches the same apportionment by statute: rent paid in advance is adjusted to the surrender date. (5) A tenant who stays in possession of any part recovers no proportionate share (Kennedy). T-vacate: March rent is earned for 2026-03-01 to 2026-03-10 (10/31 of the installment); 21/31 is refunded or credited.
- Evidence:
  - `sources/REVIEW5B_NY_CASE_Kennedy_v_Peterart_1939_AppTerm.txt`: "it was no defense to the rent which had become due in advance September first"
  - `sources/REVIEW5B_NY_CASE_Kennedy_v_Peterart_1939_AppTerm.txt`: "If by reason of the eviction plaintiff had vacated the premises she would have been entitled to recover the proportionate part of the rent paid in advance for the balance of the month of September on the ground of failure of consideration"
  - `sources/REVIEW5B_NY_CASE_Kennedy_v_Peterart_1939_AppTerm.txt`: "Supreme Court, Appellate Term, First Department,"
  - `sources/REVIEW5B_NY_CASE_Matter_of_Strasburger_1892_CoA.txt`: "But the general rule is, in the absence of fault in the lessor, that the lessee can recover only such rent as he has advanced, and such mesne profits as he is liable to pay over."
  - `sources/REVIEW5B_NY_CASE_Matter_of_Strasburger_1892_CoA.txt`: "This would be so if the breach of the covenants for quiet enjoyment resulted from the fault of Strasburger."
  - `sources/SWEEP_NY_CASE_Younger_v_Campbell_1917_1stDept.txt`: "The defendant resisted payment upon the ground that he was evicted before the day the rent would have become due under the lease."
  - `sources/NY_RPL_227.txt`: "Any rent paid in advance or which may have accrued by the terms of a lease or any other hiring shall be adjusted to the date of such surrender."

### R5B-02 (critical, missing-exception)

- Rules: `NY:RPL-227`, `NY:ADJ-vacate-order-rent` (round 4)
- Walk step: 2.6; 3.6
- What is wrong: NY:RPL-227 (walk 2.6) ends rent whenever the building is 'destroyed or so injured ... as to be untenantable' without tenant fault. The Commission of Appeals confined the statute to injury from a sudden and unexpected cause, not gradual deterioration (Suydam v Jackson), so a tenant who leaves over conditions that developed through wear and neglect cannot invoke RPL 227; that tenant needs constructive eviction (landlord's wrongful act, abandonment) or the habitability offset. Walk 2.6 also omits the section's last sentence (prepaid rent adjusted to the surrender date). Separately, NY:ADJ-vacate-order-rent reads Younger (Municipal Court) as holding RPL 227 inapplicable to vacate orders; the court's words keep RPL 227 where the untenantability 'arises from direct injury or destruction', and the First Department applied RPL 227 to a physical condition cured under a municipal order (Warrin v Haverty).
- Correct rule: RPL 227 applies only where the building is destroyed or physically injured by a sudden, unexpected cause (fire, storm, collapse, flood or a kindred casualty), the injury leaves it untenantable, the tenant was not at fault, no written agreement provides otherwise, and the tenant quits and surrenders. Then no rent is owed after the surrender and rent paid in advance or accrued is adjusted to the surrender date. Gradual deterioration is outside RPL 227. A vacate order issued because of such a physical casualty is within RPL 227; a vacate order for missing equipment, an unlawful occupancy or other non-physical noncompliance is governed by the eviction rule in NY:ADJ-vacate-order-rent as corrected by R5B-01.
- Evidence:
  - `sources/REVIEW5B_NY_CASE_Suydam_v_Jackson_1873_CoA.txt`: "The leaking was not caused by any sudden, unusual, or fortuitous circumstance, but seems to have been caused' by gradual wear and decay. The courts below held that the case was not within the statute, and that the lessee remained liable for the rent."
  - `sources/REVIEW5B_NY_CASE_Suydam_v_Jackson_1873_CoA.txt`: "New York Commission of Appeals"
  - `sources/SWEEP_NY_CASE_Younger_v_Campbell_1916_MunCt.txt`: "except where the condition of untenantability arises from direct injury or destruction."
  - `sources/REVIEW5B_NY_CASE_Warrin_v_Haverty_1913_1stDept.txt`: "All that the statute requires in this respect is that the injury shall be of a physical nature and that the premises are thereby rendered untenantable and unfit for occupancy"
  - `sources/NY_RPL_227.txt`: "Any rent paid in advance or which may have accrued by the terms of a lease or any other hiring shall be adjusted to the date of such surrender."

### R5B-03 (critical, error)

- Rules: `NY:RPL-223`
- Walk step: 2.1; test case C10
- What is wrong: Walk 2.1 says 'The buyer can collect the departing tenant's balance under the lease', and NY:RPL-223's effect says a successor landlord 'may pursue the departing tenant's balance under the lease'. RPL 223 gives the grantee the grantor's remedies going forward; rent that fell due before title passed stays the seller's unless the seller assigned it, and even an assignee of those arrears cannot use the summary remedies (Appellate Term, First Department, Getty Realty). Who is paid is wrong for every pre-sale arrear.
- Correct rule: After a conveyance of the building mid-tenancy: rent and other lease charges that fell due before title passed belong to the seller and are collected by or for the seller, not the buyer, unless the seller assigned them to the buyer in writing; rent and charges falling due after title passed belong to the buyer, who has the seller's remedies under RPL 223. The buyer, holding the deposit under GOL 7-105, may not keep it for pre-sale arrears it does not own; the statement itemizes only amounts owed to the buyer and returns the rest. An assignee of pre-sale arrears sues on them as an assignee, not in a summary proceeding.
- Evidence:
  - `sources/REVIEW5B_NY_CASE_Getty_Realty_v_2East61st_1939_AppTerm.txt`: "There is no provision in the deed purporting to transfer the arrearage of rents to the grantee, and in the absence of such transfer the present landlord had no right to rents which had become due at the time of the passing of title."
  - `sources/REVIEW5B_NY_CASE_Getty_Realty_v_2East61st_1939_AppTerm.txt`: "the reference in section 223 of the Real Property Law to assignees of rents is to assignees of rents accruing after the grants therein referred to."
  - `sources/REVIEW5B_NY_CASE_Getty_Realty_v_2East61st_1939_AppTerm.txt`: "Supreme Court, Appellate Term, First Department, May 2, 1939."
  - `sources/NY_RPL_223.txt`: "has the same remedies, by entry, action or otherwise, for the nonperformance of any agreement contained in the assigned lease for the recovery of rent"

### R5B-04 (critical, contradiction)

- Rules: `NY:ADJ-tenant-deposit-claim-limitations` (round 4), `US:11USC108(c)-extension` (round 4), `US:50USC3936-tolling` (round 4), `NY:CPLR-210-death` (round 4)
- Walk step: 7.6; 8.10 (time limits)
- What is wrong: NY:ADJ-tenant-deposit-claim-limitations lists US:11USC108(c)-extension as tolling the former tenant's own deposit claims. Section 108(c) extends periods for suing on a claim against the debtor (the landlord's claim); the debtor-tenant's own claim passes to the trustee and is extended by 108(a) instead, to the later of the period's end or two years after the order for relief. The walk then tells the operator to 'Keep the settlement file six years', which contradicts the extensions the same rule lists: military service is excluded from the period without limit (3936), 108(a) can run two years past the order for relief, and a tenant's estate has one year after death (CPLR 210(a)).
- Correct rule: The former tenant's deposit claims run three years (punitive damages, forfeiture-only recovery) or six years (deposit kept without lawful basis) from the end of the 14 days, extended by: the tenant's military service (50 USC 3936, not counted); the tenant's bankruptcy, where the trustee may sue until the later of the period's end or two years after the order for relief (11 USC 108(a)); and the tenant's death, where the representative may sue within one year after death if the period had not run (CPLR 210(a)). 11 USC 108(c) extends only the landlord's time to sue the tenant. Operator step: keep the settlement file until the latest of those dates, not a flat six years.
- Evidence:
  - `sources/REVIEW5B_US_11USC_108_uscode.txt`: "(a) If applicable nonbankruptcy law, an order entered in a nonbankruptcy proceeding, or an agreement fixes a period within which the debtor may commence an action, and such period has not expired before the date of the filing of the petition, the trustee may commence such action only before the later of-"
  - `sources/REVIEW5B_US_11USC_108_uscode.txt`: "(2) two years after the order for relief."
  - `sources/REVIEW5B_US_11USC_108_uscode.txt`: "fixes a period for commencing or continuing a civil action in a court other than a bankruptcy court on a claim against the debtor"
  - `sources/REVIEW4A_US_50USC_3936_uscode.txt`: "The period of a servicemember's military service may not be included in computing any period limited by law, regulation, or order for the bringing of any action or proceeding in a court"
  - `sources/REVIEW4A_NY_CPLR_210_nysenate.txt`: "an action may be commenced by his representative within one year after his death."

### R5B-05 (major, missing-exception)

- Rules: `NY:RPAPL-1305-successor` (round 4)
- Walk step: 0.5 (who is owed the rent)
- What is wrong: The rule and walk 0.5 state the foreclosure successor takes subject to the market-rate tenant's right to stay for the greater of 90 days or the rest of the lease 'on the same terms', without the section's limits: a successor that will occupy one unit as its primary residence may cut that one unit to 90 days; the lease qualifies only if the tenant is not the owner and the rent is not substantially below fair market rent; and a tenant who moved in after the foreclosure began keeps the rest of the lease only under a good-faith lease and for at most three years. Each limit moves the date the tenancy can end and so the rent owed.
- Correct rule: RPAPL 1305(2): a tenant of a unit not rent-controlled or stabilized may stay for the greater of 90 days from the successor's notice or (b) the rest of the lease if it occupied at the start of the foreclosure or got the 1303 notice, or (c) the rest of a good-faith lease, up to three years, if it moved in later; the lease counts only if the tenant is not the owner and the rent is not substantially below fair market rent; a successor that will occupy a single unsubsidized unit as its primary residence may limit that one unit to 90 days. The tenancy continues on the terms in effect at the judgment or transfer.
- Evidence:
  - `sources/REVIEW4A_NY_RPAPL_1305_nysenate.txt`: "provided that if a successor in interest who acquires title to such residential real property intends to occupy a single unit as his or her primary residence"
  - `sources/REVIEW4A_NY_RPAPL_1305_nysenate.txt`: "For a lease to qualify under this subdivision, the tenant under such lease may not be the owner of the residential real property, and such lease must require the payment of rent for such unit that is not substantially less than the fair market rent for the unit"
  - `sources/REVIEW4A_NY_RPAPL_1305_nysenate.txt`: "up to a maximum of three years"

### R5B-06 (major, misstatement-in-walk)

- Rules: `NY:ADJ-provide-address-branches` (round 4), `NY:GOL-7-108(1-a)(e)`
- Walk step: 6.5; test case C3
- What is wrong: C3 gives the tenant only a forwarding email and then says the refund goes 'by a payment that reaches the tenant, such as a transfer to her account or a check to a postal address'. NY:ADJ-provide-address-branches branch (a) sends the refund 'to the forwarding address or by a payment the tenant can receive' but gives no compliant act where the landlord holds an email or phone number and neither a postal address (other than the unit) nor payment details. Waiting for an address forfeits (Prando), so the operator needs the act.
- Correct rule: Within the 14 days the landlord sends the statement to the known email or phone number and dispatches the refund by a means directed to the tenant: an electronic payment to an account or payment address the landlord holds for the tenant, or, if it holds none, a check mailed to the last known postal address (the vacated unit), with the emailed statement saying where and how the refund was sent. It does not hold the refund for an address.
- Evidence:
  - `sources/NY_GOL_7-108_nysenate.txt`: "shall return any remaining portion of the deposit to the tenant"
  - `sources/NY_CASE_Prando_v_Kelly_2021.txt`: "Defendant Renee Kelly asserted that she had delayed returning plaintiff's security deposit because, among other things, she had not known his new address."

### R5B-07 (minor, contradiction)

- Rules: `NY:HANDOFF-broker-config-collection-agency`, `NY:RPL-440(1)-rent-collection`
- Walk step: 8.6a
- What is wrong: NY:HANDOFF-broker-config-collection-agency is conditioned on handing off 'a former tenant's balance that includes rent or use and occupancy', while NY:RPL-440(1)-rent-collection holds that collecting use and occupancy owed after the tenancy ended is not collecting rent and needs no broker licence.
- Correct rule: The broker licence is needed only for the rent part (rent that fell due under the tenancy, including rent reserved for months after an early departure); use and occupancy for occupancy after the tenancy ended, damage, fees and utilities need none.
- Evidence:
  - `sources/SWEEP_NY_RPL_440_nysenate.txt`: "collects or offers or attempts to collect rent for the use of real estate"
  - `sources/NY_RPL_220.txt`: "The landlord may recover a reasonable compensation for the use and occupation of real property"

### R5B-08 (minor, hedging)

- Rules: `NY:ADJ-willful-standard` (round 4)
- Walk step: 7.5
- What is wrong: The rule's judgment terms label the standard 'willfully (knew or should have known)', the single-part test its own effect and reasoning reject (knowing, intentional or deliberate failure; should-have-known goes only to knowledge of the law). The label will be read as the test.
- Correct rule: Judgment term: 'willfully: knowing, intentional or deliberate failure (not negligence or inadvertence), with knowledge of the law charged to an experienced landlord or managing agent'.
- Evidence:
  - `sources/NY_CASE_Karole_v_340WEnd_2022.txt`: "requires more than inadvertence"
  - `sources/NY_CASE_Prando_v_Kelly_2021.txt`: "not willful, and, thus, that punitive damages were not warranted"

### R5B-09 (minor, misstatement-in-walk)

- Rules: `NYC:HMC-27-2045-detector-charge`
- Walk step: 5.5a; test case T-lead
- What is wrong: The rule says a device 'replaced because its useful life expired ... is the owner's cost and is not charged'. 27-2045(e) makes the occupant of the unit in which a device is installed reimburse the owner, within the caps, including for a device installed to replace one past its useful life. The departed tenant is not that occupant for a turnover replacement, so the move-out result holds, but a (e) reimbursement for a device installed during the tenancy and left unpaid is a lawful charge. T-lead also omits that the $50 cap is for a battery-operated combination device; a hardwired one is charged under the damage rule.
- Correct rule: At move-out: a battery-operated device the tenant removed or disabled is charged within $25/$50/$75; a device replaced at turnover for age or defect is not charged to the departed tenant; a (e) reimbursement for a device installed during the tenancy (including a useful-life replacement) and unpaid may be claimed within the caps, separately from the deposit.
- Evidence:
  - `sources/SWEEP_NYC_ADC_27-2045.txt`: "or installed to replace a device that has exceeded the manufacturer's useful life or that has been lost or damaged by such occupant"
  - `sources/SWEEP_NYC_ADC_27-2045.txt`: "shall reimburse the owner for the cost of providing and installing such device"

### R5B-10 (minor, misstatement-in-walk)

- Rules: `NY:RPL-227-e`
- Walk step: 3.3
- What is wrong: Walk 3.3 says 'A new lease ends the old one.' The statute ends the old lease only when the landlord re-lets at fair market value or the agreed rate; the rule states this correctly, the walk drops the condition.
- Correct rule: A new tenant's lease at fair market value or the agreed rate, once in effect, ends the departed tenant's lease.
- Evidence:
  - `sources/NY_RPL_227-E.txt`: "If the landlord rents the premises at fair market value or at the rate agreed to during the term of the tenancy, the new tenant's lease shall, once in effect, terminate the previous tenant's lease"

## T-vacate ruling

When an owner-caused government vacate order ousts a market-rate NYC tenant mid-month after that month's rent fell due and was paid, the rent for the days after the ouster is recoverable by the tenant: the landlord refunds or credits the per-day share of the installment for the days after the ouster (apportionment on failure of consideration), and rent earned is only the share up to and including the day of the ouster. If the installment is unpaid, only the earned share is charged or kept from the deposit. Because the owner caused the order, the tenant also has a damages claim for the value of the rest of the term less the rent reserved. Where the order follows a sudden physical casualty, RPL 227 imposes the same adjustment to the surrender date. A tenant who keeps possession of any part recovers no proportionate share. Controlling authority: Matter of Strasburger (Court of Appeals 1892: an evicted lessee recovers the rent it advanced, and the full loss of bargain where the lessor is at fault), applied to a mid-month eviction by Kennedy v Peterart Realty (Appellate Term, First Department 1939, binding on the New York and Bronx County Civil Courts; Peerless Candy, Appellate Term, Second Department 1925, states the same measure for Kings, Queens and Richmond). It prevails over the reading that the pre-ouster installment is simply 'not barred': that reading states only the first half of Kennedy (no defense to rent already due) and ignores its holding on recovery, and Younger (App Div 1917) is not contrary because there the eviction preceded the due date. No later decision found limits Kennedy or Strasburger (CourtListener searches for citing cases and for the rule's terms, 2026-09-29).

Evidence:
- `sources/REVIEW5B_NY_CASE_Kennedy_v_Peterart_1939_AppTerm.txt`: "If by reason of the eviction plaintiff had vacated the premises she would have been entitled to recover the proportionate part of the rent paid in advance for the balance of the month of September on the ground of failure of consideration"
- `sources/REVIEW5B_NY_CASE_Kennedy_v_Peterart_1939_AppTerm.txt`: "but her retention of possession to the end of the term prevents any such recovery."
- `sources/REVIEW5B_NY_CASE_Matter_of_Strasburger_1892_CoA.txt`: "But the general rule is, in the absence of fault in the lessor, that the lessee can recover only such rent as he has advanced, and such mesne profits as he is liable to pay over."
- `sources/REVIEW5B_NY_CASE_Peerless_Candy_v_Halbreich_1925.txt`: "If he does not remain in possession and vacates the premises treating the partial eviction as one from the entire demise and the relationship of landlord and tenant ceases, his damages would be: (a) The proportionate part of the rent due or paid"
- `sources/SWEEP_NY_CASE_Younger_v_Campbell_1917_1stDept.txt`: "the landlord cannot recover any rent for the period after the eviction occurred."
- `sources/SWEEP_NY_CASE_Barash_v_PennTerminal_1970_CoA.txt`: "In the case of actual eviction, even where the tenant is only partially evicted, liability for all rent is suspended"
- `sources/NY_RPL_227.txt`: "Any rent paid in advance or which may have accrued by the terms of a lease or any other hiring shall be adjusted to the date of such surrender."

Branches the operator applies: (a) installment paid before the ouster, tenant leaves: refund or credit the days after the ouster; (b) installment unpaid: charge or keep only the earned days; (c) tenant keeps possession of part: no proportionate recovery, rent suspended for later periods only (Barash, actual eviction); (d) order caused only by conditions the tenant or its household created: no defence, the lease governs; (e) order after a sudden casualty without tenant fault: RPL 227, same adjustment to the surrender date.

## Confirmed

Each line was checked quote-to-effect in the dump and, where marked, against the statute text (T) or the decision (C) in context. Rules added or changed in round 4 are marked (round 4).

- NY:GOL-7-108(1), NY:GOL-7-108(1-a)-exclusions, NY:L2019-c36-PartM-s29, NY:GOL-7-108(1)-pre2019: 7-108 reaches every non-7-107 dwelling; 1-a from leases and renewals entered on or after 2019-07-14; rent-controlled and licensed care units outside 1-a (T; 30th day computed).
- NY:RPL-232-c, NY:CASE-Case-v-575Classon, NY:CASE-Bogom-Shanon-month-to-month: rent accepted after the term creates a month-to-month renewal tenancy, so 1-a reaches a pre-2019 lease continued after 2019-07-14 (T, C).
- NY:COMMONLAW-deposit-return, NYC:CASE-Pezzo-lease-return-term, NY:ADJ-fee-retention-commonlaw: common-law return rule and lease return term for unrenewed pre-2019 leases (C).
- NYC:RSL-26-504(a)-(c), NYC:RS-status, NYC:RSC-2520.11(a)-(e), (k), (p), (r)(1), (s)(1), NYC:RSL-26-520, NYC:RC-status, NYC:RCL-26-403(e)(2)(i)(4), (9), NYC:RER-2211.8(a): status routing and exclusions; RSL through 2027-03-31 (Q).
- NY:MDL-4(7)-multiple-dwelling, NY:MDL-301(1), NY:MDL-302(1)(b): de facto multiple dwelling; certificate rule with its exceptions; no rent or use and occupancy for the unlawful period, deposit not kept for it; only the Chatsworth interference exception (T; C: Caldwell, 49 Bleecker, Chazon). (round 4: NY:MDL-301(1), NY:MDL-302(1)(b))
- NY:MDL-325(2), NYC:ADC-27-2097-registration, NYC:ADC-27-2107(b)-rent-stay: suspension until registration, accrued rent then recoverable (9 Montague Terrace); city stay discretionary and the only consequence for a one- or two-family house (T, C). (round 4: NY:MDL-325(2), NYC:ADC-27-2097-registration, NYC:ADC-27-2107(b)-rent-stay)
- NY:MDL-302-a(3): six-month rent-impairing bar with plans proviso, four exceptions, voluntary-payment and plead-and-deposit rules (T).
- NY:ADJ-MDL-rent-bar-not-1-2-family, NYC:HMC-27-2087-cellar-basement, NY:MDL-285(1)-loft-law: MDL forfeitures confined to multiple dwellings (C: Pickering); cellar rule; loft routing (T).
- NY:RPL-235-bb-co-notice: three or fewer rental units, bold notice before signing, waiver void (T). (round 4: NY:RPL-235-bb-co-notice)
- NY:RPAPL-776-778-administrator, NYC:HMC-27-2135(c)-receiver-rents, NYC:HMC-27-2147-rent-levy, NY:CPLR-6401-foreclosure-receiver, NY:COMMONLAW-mortgagee-assignment-of-rents, NY:COMMONLAW-owner-death-agency: who holds the rent claim (T; C: Holmes, Sullivan v Rosson, Farmers' Loan).
- US:11USC541-704-owner-chapter7, US:11USC1107-1306-owner-reorganization: who collects in the owner's bankruptcy; deposit outside the estate only if traceable (T; C: Trafalgar). (round 4: US:11USC1107-1306-owner-reorganization, US:11USC541-704-owner-chapter7)
- NY:GOL-7-108(1-a)(a), (4), (6), NY:L2021-c428, NY:L2022-c111, NY:L2021-c789-s7, NY:L2022-c93: one-month cap including advances; seasonal and co-op exceptions and dates (T).
- NY:GOL-7-103(1)-scope, (1)-trust, (2)-bank-notice, (2-a), (2)-admin-fee, (2)-interest-owed, (2-b), (3), NY:GOL-7-108(3): trust, bank notice, six-unit interest account, 1% fee, interest paid over at termination, waivers void (T).
- NY:ADJ-7103-2a-building-count, NY:CASE-Gihon-7-103(2-a)-building: six units counted per building (C).
- NY:CASE-Paterno-bank-notice-inference, NY:CASE-Paterno-commingling-forfeiture, NY:CASE-Paterno-rent-survives: no bank notice permits the commingling inference; commingling forfeits at once; rent claim survives (C; LeRoy v Sayers, 1st Dept). (round 4: NY:CASE-Paterno-commingling-forfeiture)
- NY:19NYCRR-175.1-broker-escrow: broker's separate federally insured account within three business days (T). (round 4: NY:19NYCRR-175.1-broker-escrow)
- NY:GOL-7-108(1-a)(c)-offer, (c)-bar: move-in inspection offer and bar (T).
- NYC:FARE-20-699.20-fee, NYC:FARE-20-699.22(b), NYC:FARE-20-699.21-agent-fee-ban, NYC:FARE-20-699.23(c), NYC:FARE-moveout-service-fee, NYC:FARE-damages-rent-not-fees, NYC:DCWP-FARE-FAQ-disclosure: fee definition, disclosure, agent fee ban, restitution; rent and damages are not fees (T). (round 4: NYC:FARE-20-699.21-agent-fee-ban, NYC:FARE-moveout-service-fee)
- NY:RPL-238-a(1)-no-move-in-fees, NY:RPL-235-g, NY:RPL-235-e(a), NY:STT-305(3), NY:STT-307: move-in fee bar, payment method, receipts, e-records (T). (round 4: NY:RPL-238-a(1)-no-move-in-fees)
- NY:S947-ach-fee-ban: passed Senate 2026-03-18 and Assembly 2026-05-13, returned to Senate, not delivered to the Governor on 2026-09-29 (Assembly actions re-read 2026-09-29: REVIEW5B_NY_S00947_Assembly_actions_2026-09-29.txt). (round 4: NY:S947-ach-fee-ban)
- NY:GOL-7-105(1), (2)-transfer-effect, (2)-inconsistent-agreement, (3), NY:GOL-7-108(2)(a)-(e): deposit turnover within five days with registered or certified notice; successor and receiver liability (T). RPL 223 payee: R5B-03.
- NY:RPL-226-b(1)-(3), NY:RPL-235-f, NY:RPL-236, NY:RPL-236-a, US:12CFR1006.2(e), NY:ADJ-tenant-death-payee, NY:CPLR-210-death: assignment, occupants, tenant death and estate payee (T). (round 4: NY:ADJ-tenant-death-payee, NY:CPLR-210-death)
- NY:ADJ-cotenants-vacated, NY:ADJ-cotenants-payee: clock from last co-tenant's departure; joint versus recorded shares (C: Lasky; Holmes majority did not decide the split).
- NY:RPL-226-c(2), NY:RPL-226-c(1)(a), NY:GOL-5-905: notice periods and extension; auto-renewal notice (T).
- NY:RPL-212, NY:RPL-214, NY:RPL-214(15)-high-rent, NY:RPL-211(3)-small-landlord, NY:RPL-215: Good Cause scope, fifteen exemptions, sunset 2034-06-15 (T).
- NY:RPL-232-a, NY:RPL-228, NY:RPL-232-b, NY:COMMONLAW-NYC-monthly-tenant-surrender, NY:ADJ-NYC-monthly-agreed-notice: NYC monthly tenant may leave at month end without notice (C: T.I.B. affirmed; Srinivasan).
- NY:RPL-232, NY:ADJ-RPL-232-monthly-letting, NY:ADJ-RPL-232-indefinite-term, NY:ADJ-RPL-232-after-october, NY:ADJ-RPL-232-agreement-sets-end, NY:ADJ-RPL-232-oral-term-over-one-year: re-decided and confirmed. A bare monthly rent is a monthly letting (Gerolemou, Queens; Spies; and Mayer Meat v Heilman, App Term 1st 1923, doubting that a 'monthly rental of $200 a month' letting is 'any more than a letting by the month', REVIEW5B_NY_CASE_Mayer_Meat_v_Heilman_1923_AppTerm.txt). Stauber's application of RPL 232 to a September sublet was not needed for its result. 1239 Madison (App Div 1st 1924, REVIEW5B_NY_CASE_1239Madison_v_Neuburger_1924_1stDept.txt) held RPL 232 inapplicable to an emergency-rent statutory tenant and is consistent.
- NY:RPL-227-e, NY:CASE-Toporek-227-e, NY:RPL-227-e-waiver: mitigation duty, burden, waiver void (T, C). Walk wording: R5B-10.
- NY:CASE-Riverside-surrender-by-operation, NY:ADJ-lease-break-charge: surrender test (Court of Appeals) and JMD liquidated-damages test; lease-break sum never kept from the deposit (C). (round 4: NY:CASE-Riverside-surrender-by-operation)
- NY:RPL-227-a(1)-(3), NY:RPL-227-c(1), (2), (3)(a)-(d), (4)(b), (5)(b), (6)(a), NY:MIL-310(2), NY:RPL-227-d-dv-status: senior/disabled, domestic-violence and NY military terminations (T). (round 4: NY:RPL-227-d-dv-status)
- US:50USC3955(a)(1), (a)(1)-all-parties, (a)(2), (a)(3)-(4), (b)(1), (c), (d)(1)(A), (d)(1)(B), (e)(1)-prorate, -no-etf, -other, (f), (g), (h), (i), US:50USC3917(a), US:50USC3918, US:50USC4042, US:50USC3911(1)-(2), (4), US:50USC3955-deposit-clock-NY: SCRA termination (T; House report for all-parties).
- NY:RPL-229, NY:RPL-220: double rent after the tenant's own notice; use and occupancy (T).
- NY:COMMONLAW-constructive-eviction, US:24CFR982.404(d)(3)-(4): Barash conditions; abated HAP never the family's debt (C, T). Vacate-order rent: R5B-01, R5B-02.
- NY:GOL-7-108(1-a)(d)-notice, (d)-inspection, NY:CASE-Toporek-forfeiture-scope, NY:GOL-7-108(1-a)(g): pre-vacate inspection; only (e) forfeits; actual damages and up to twice the deposit (T, C). (round 4: NY:CASE-Toporek-forfeiture-scope)
- NY:GOL-7-108(1-a)(b)-refundable, (b)-excluded-costs, NY:ADJ-no-fee-retention, NY:RPL-238-a(2), (2-a), (3), NY:GOL-5-328(3)(b): four retention categories; fees refunded and pursued separately; late fee after five days at the lesser of $50 or 5% (T; C: Colon, Freeland).
- NY:RPL-234-a, NY:L2021-c695-s6, NY:L2022-c162, NY:RPL-234, NY:CPLR-4544-small-print, NY:RPL-235-i, NY:RPL-235-c: legal fees only by court order from 2021-12-21; reciprocal fees (Graham Court); small print; keys 110% (T, C). (round 4: NY:CPLR-4544-small-print, NY:RPL-234)
- NYC:HMC-27-2013(a), (b)(2), (c), (g), NYC:PAINT-wear-and-tear: repainting from ordinary occupancy is the owner's; painting bill alone proves nothing (T; C: Bohl).
- NY:CASE-Mihalow-rent-arrears, NY:CASE-Gelbart-rent-offset, NY:ADJ-early-departure-rent-retention: rent kept only through a timely statement and only rent due and unpaid, to the day before a new lease (C: Kunik). (round 4: NY:CASE-Mihalow-rent-arrears)
- NY:RPL-235-b, NY:RPL-235-a, NYC:HMC-27-2056.8-lead-turnover, NYC:HMC-27-2017.5-turnover, NYC:HMC-27-2128-owner-debt: habitability offset; utility credit; statutory turnover work and HPD charges are the owner's (T). Detector wording: R5B-09.
- US:24CFR982.313(c), (d), (d)-promptly, (e), US:24CFR982.451(b)(4), US:24CFR982.311(d)(1), US:24CFR982.452(b)(5): voucher deposit and HAP rules (T).
- NYC:RCNY68-10-14(a), (c), (e), (h), NYC:RCNY31-5-06(a)(1), (a)(10), NYC:HRA-voucher-claim-window, NYC:HRA-voucher-proof, NYC:DSS-SOTA-voucher-claim, NYC:RCNY28-1-01, NYC:RCNY28-1-12(b)-cap, (b)-escrow, NYC:HPD-ESCROW-no-owner-draw, NYC:HPD-ESCROW-regulatory-agreement: voucher and Article VIII escrow rules (T).
- US:42USC3604(f)(3)(A), (B), -animal-fees, -animal-damage, US:24CFR100.65-terms, NY:EXEC-296(5)(a)(2)-terms, NYC:ADC-8-107(5)(a)-terms: accommodation and equal-treatment rules with their exemptions (T). (round 4: NY:EXEC-296(5)(a)(2)-terms, NYC:ADC-8-107(5)(a)-terms, US:24CFR100.65-terms)
- NY:GOL-7-108(1-a)(e), NY:GCN-110, NY:GCN-19, NY:GCN-20, NY:GCN-20-event-day, NY:GCN-25-a(1), NY:GCN-24, NY:GCN-25(1), NY:GCN-25-a(1)-contract-carveout, NY:GCN-30, NY:CASE-Cohen-deadline-count: 14 days excluding the vacating day with weekend/holiday rollover (T; C: Cohen, July 24 to August 7).
- NY:CASE-Urban-vacatur, NYC:CASE-Pezzo-surrender: date vacated is a fact question shaped by the lease (C).
- NY:CASE-Bogom-Shanon-written, NY:ADJ-provide-written-dispatch, NY:CASE-Toporek-estimate, NY:ADJ-provide-address-branches, NY:CASE-Pickens-provide: written statement, timed by the send date, estimates allowed, known channel must be used (C: Cohen, Urban, Freeland, Pickens, Prando). Refund route gap: R5B-06. (round 4: NY:ADJ-provide-address-branches, NY:CASE-Pickens-provide)
- US:11USC362(a)(7), -deposit-is-setoff, US:CASE-Strumpf-hold, US:11USC542-refund-payee: stayed setoff, Strumpf hold with prompt motion, refund to the ch. 7 trustee after notice or the ch. 13 debtor (T, C).
- NY:OSC-MS11-refunds-due, NY:OSC-TR04-broker-escrow, NY:ABP-1315(2), NY:ABP-1422: three-year dormancy; pre-report notice excused where the only address is not current (T). (round 4: NY:OSC-TR04-broker-escrow)
- NY:COMMONLAW-belongings-owner-keeps, NY:CASE-Facey-belongings, NY:COMMONLAW-belongings-abandonment, NYC:ABANDONED-city-layer, US:50USC3958(a), US:50USC3958-lien-enforcement, US:50USC3951-distress-NY: belongings rules (C: 8902 Corp, Cretaro, Henryka; T).
- NYC:ADC-26-3002(c)-moveout-data, NY:GBL-899-bb-safeguards: data removal within 90 days; safeguards (T). (round 4: NY:GBL-899-bb-safeguards, NYC:ADC-26-3002(c)-moveout-data)
- NY:GOL-7-108(1-a)(e)-forfeiture, NY:ADJ-forfeiture-claims-survive, NY:CASE-Levine-counterclaim, NY:CASE-Masseroli-separate-claim: forfeiture takes the security, not the debt (C: Levine, App Term 1st; Paterno). (round 4: NY:CASE-Masseroli-separate-claim)
- NY:GOL-7-108(1-a)(f): landlord's burden on reasonableness (T).
- NY:ADJ-willful-standard, NY:CASE-Prando-willful, NY:CASE-Karole-willful, NY:CASE-Bogom-Shanon-willful: two-part willfulness standard re-decided and confirmed; label: R5B-08. (round 4: NY:ADJ-willful-standard)
- NY:ADJ-tenant-deposit-claim-limitations (three and six years, accrual at day 14, Gaidon), NY:CCA-1801-tenant-claim, NY:CCA-1812-treble: confirmed except the tolling list and file retention (R5B-04). (round 4: NY:ADJ-tenant-deposit-claim-limitations, NY:CCA-1801-tenant-claim, NY:CCA-1812-treble)
- NY:ADJ-lease-balance-not-consumer-credit, NY:CASE-Lefferts-rent-not-consumer-credit, NY:23NYCRR-1.1(d)-not-lease, NY:CPLR-213(2), NY:CPLR-214-i: lease balance is not consumer credit; six years (C: Romea, Lefferts).
- NY:CPLR-214-i-consumer-debt-S9760, NY:S9760-pleading-service, NY:S9760-notice-mailings, NY:S9760-venue, NY:S9760-default-judgment: pending; passed both houses 2026-06-02/03, returned to Senate, not delivered to the Governor on 2026-09-29 (REVIEW5B_NY_S09760_Assembly_actions_2026-09-29.txt).
- US:15USC1692a(2)-(6) and every (6) branch, US:CASE-Henson-2017, US:12CFR1006-cmt-2(i)-1, US:12CFR1006.1(c)(1), (c)(2), US:12USC5481(15)(A)(ii), US:CASE-Romea-1998, US:15USC1692a(5)-lease-charges, -non-party-tort, US:15USC1692a(6)(F)(i), -manager-incidental, -collection-only, (F)(iii), -moveout-branches, -default-meaning, US:HANDOFF-config-pre-default, -post-default, -owner-name-only, -principal-purpose, -owns-balance, US:15USC1692j(a), US:15USC1692o, -NY-VA-none, US:15USC1692n: FDCPA coverage by configuration (T; C: Henson, Alibrandi, Franceschi, Wilson, Goldstein, Vincent, Barbato). (round 4: US:15USC1692n)
- US:15USC1692b, c(a)-(d), d, e(2)(A), e(5), e(8), e(11), e(14), f(1), f(7)-(8), g(a), g(b), i(a), k(a), k(c), k(d), US:CASE-Avila-accruing-balance, US:12CFR1006.6(d)(3)-(4), 6(e), 14(b)(2), 22(f)(3)-(4), 26(b), 30(a), 30(b), 34(a)(1), 34(b)(3), 34(b)(5), 34(c), 34(d)(2), -cmt-34(c)(2)(viii)-2, 38(b), 38(d)(2), 42(a)(1), 42(b), 100(a): conduct, validation, disputes, delivery, suits, liability (T). (round 4: US:CASE-Avila-accruing-balance)
- NY:GOL-5-701(a)(2)-guaranty: guaranty only in a signed writing (T). (round 4: NY:GOL-5-701(a)(2)-guaranty)
- NYC:CPL-20-700, NYC:CPL-tenant-balance-consumer-debt, NYC:ADC-20-489(d): a tenant balance is a consumer debt under city law (T; C: Allen).
- NY:GBL-604-bb-coerced-debt, NY:GBL-604-cc-coerced-defense: effective 2026-06-17; ten, thirty and five business-day steps; purpose-based definition reaches a lease balance (T). (round 4: NY:GBL-604-bb-coerced-debt, NY:GBL-604-cc-coerced-defense)
- NYC:RCNY6-5-76-debt-collector, -procedures, NYC:RCNY6-5-77(b)(1)(iv), (d)(17)-GBL601, (e)(1), (e)(8)-GBL601, (f)(1), (f)(1)-landlord-not-TILA-creditor, (g), US:15USC1602(f), (g), NY:GBL-601-a-family: current city rules through 2026-12-31 (T). (round 4: NY:GBL-601-a-family)
- NYC:SHIELD-effective-date, -operative-date, -penalty-effective-date, -5-76-debt-collector, -5-76-procedures, NYC:DCWP-FAQ-procedures-trigger, -validation-scope, NYC:SHIELD-5-77(f)(1), (f)(1)(viii), (b)(1)(iii)-frequency, (b)(1)(iii)(D)(IX), (b)(4)-cease, (b)(5)(i)(B), (i), (e)(10)-credit-report-notice: SHIELD operative 2027-01-01 (T: City Record notices).
- NYC:ADC-20-489(a), (a)(1), (a)(7), NYC:ADC-20-490, NYC:DCA-owner-own-staff, -affiliate-collector, -manager-for-owners, -handoff-incidental, -handoff-principal-purpose, -debt-buyer, -originated-exclusion-scope, NYC:ADC-20-493.1(b), 20-493.2(a), (b), NYC:RCNY6-2-190(b), 2-191(a), 2-192-payment-plan, 2-193-records: DCWP licensing by configuration (T; C: Citibank v Yanling Wu). (round 4: NYC:ADC-20-489(a))
- NY:RPL-440(1)-rent-collection, NY:ADJ-broker-owner-and-staff, NY:RPL-442-f-exemptions, NY:RPL-442-d-442-e-unlicensed, NY:RPL-442-fee-split, NY:HANDOFF-broker-config-collects-rent, -settlement-only, -under-broker: broker licensing by configuration (T; C: Weingast, Fields, Futersak, G.C. Fortune). Collection-agency wording: R5B-07.
- US:15USC1681s-2(a)(1)(A), (a)(3), (a)(5)(A), (b)(1), (c), US:12CFR1022.42(a), 1022.43(a): furnisher duties (T).
- US:11USC362(a)(6), US:11USC524(a)(2), US:11USC1301-codebtor-stay, US:11USC365(d)(1)-ch7-rejection, US:11USC502(b)(6)-lessor-cap, US:11USC108(c)-extension: stay, discharge, co-debtor stay (chapter 13 only), deemed rejection in chapter 7, lessor cap, creditor's 30-day extension (T). (round 4: US:11USC108(c)-extension, US:11USC1301-codebtor-stay, US:11USC365(d)(1)-ch7-rejection, US:11USC502(b)(6)-lessor-cap)
- US:50USC3931(b)(1), NY:CPLR-3215(g)(3), NY:CPLR-3215(j)-sol-affidavit, NY:MIL-303(3): default-judgment affidavits and mailing; small claims excluded from the mailing (T). (round 4: NY:CPLR-3215(j)-sol-affidavit, NY:MIL-303(3))
- NY:LLC-808(a)-foreign-authority, NY:BCL-1312(a)-foreign-authority, NY:LLC-206-publication-suspension: capacity defects curable (T; C: Small Step). (round 4: NY:LLC-206-publication-suspension)
- NY:CCA-1809(1), NY:CCA-1801-A(a)-eligibility, NY:CCA-1801-A(b), NY:CCA-1803-A(b): entity owners barred from small claims; commercial claims conditions and demand letter (T; C: National Arbitration). (round 4: NY:CCA-1801-A(a)-eligibility, NY:CCA-1803-A(b), NY:CCA-1809(1))
- US:50USC3936-tolling, NY:GOL-17-101-acknowledgment: military tolling both ways; signed acknowledgment or part payment restarts the period (T). (round 4: NY:GOL-17-101-acknowledgment, US:50USC3936-tolling)
- NY:CPLR-5001(a)-(b), NY:CASE-NML-contract-rate, NY:ADJ-lease-interest-on-rent, NY:CPLR-5004(a)-consumer-2pct, US:50USC3937-6pct, NY:MIL-323-a-6pct: interest as of right; lease rate to judgment; lease interest on rent within the 238-a cap; 2% for a natural person from 2022-04-30 (T; C: NML, Allen). (round 4: NY:MIL-323-a-6pct, US:50USC3937-6pct)
- NY:CPLR-3015(e)-licence-pleading: licensed collector pleads licence (T).
- US:IRS-Pub527-deposit-income, US:26USC6050P-no-1099C, US:26USC6049-deposit-interest: tax treatment (T). (round 4: US:26USC6049-deposit-interest, US:26USC6050P-no-1099C, US:IRS-Pub527-deposit-income)

## Test cases (decided before reading the walk's answers)

| Case | 5B answer | Difference from the walk |
|---|---|---|
| C3 | 1-a applies (2023 lease). Statement by email within 14 days of vacating (rolled to the next business day if day 14 is a weekend or GCN 24 holiday). Refund in the same 14 days: deposit plus bank interest less the 1%/yr fee, less only unpaid rent, tenant damage beyond wear, lease utilities and moving/storage. Fees refunded; ordinary repainting not charged. Refund dispatched by a means directed to the tenant; with only an email known, by e-payment to a held account or a check to the last known postal address (R5B-06). 1099-INT if $10 or more of interest is paid in the year. | Refund route with only an email known is not stated in the walk (R5B-06). |
| C4 | Three families: a multiple dwelling (MDL 4(7)); not a 7-103(2-a) building; not stabilized absent J-51/421-a; not controlled (vacancy after 1971-06-30). Bank notice and net interest if banked in an interest-bearing account. Three-year repaint and records; HPD registration required; no rent for any period occupied without a required certificate (conversion after 1929-04-18); rent suspended until registration then recovered; rent-impairing bar if an uncorrected violation stands. | None. |
| C5a | Rent accepted monthly after 2019-07-14 created a month-to-month renewal tenancy (RPL 232-c; Case v 575 Classon), so 1-a applies. | None. |
| C6 | Rent after departure only as damages subject to the landlord's re-letting duty and burden (RPL 227-e); surrender by operation of law if both treat the lease as ended; statutory terminations (227-a, 227-c, SCRA 3955, Mil 310) end rent on their dates and bar early-termination charges; auto-renewal only with GOL 5-905 notice; at day 14 the deposit covers only rent due and unpaid, up to the day before a new lease; a lease-break sum only if valid liquidated damages and never from the deposit. | None. |
| C7 | Timely statement with itemized estimates; excess is a separate claim that survives any forfeiture; no legal fees without a court order; statutory interest 2% (natural person) or the lease rate to judgment, with lease interest on rent inside the 238-a cap; rent barred for periods without a required certificate or under a six-month rent-impairing violation, suspended while unregistered; six years to sue today. | Walk omits that lease interest on rent is capped with the late fee (stated in 8.10). |
| C8 | No statement until the second co-tenant leaves; then a statement to each; recorded shares paid pro rata, otherwise one joint refund. | None. |
| C9 | Statement and refund to the vacated unit within 14 days; unclaimed refund stays trust money and is reported under MS11 (TR04 if a real-estate company's escrow) after three years; ABP 1422 notice excused because the only address is not current. | None. |
| C10 | Seller turns the deposit over within five days of the deed with registered or certified notice; buyer settles the deposit. Rent that fell due before title passed is the seller's unless assigned; the buyer collects only later-falling rent and may not keep the deposit for the seller's arrears (R5B-03). Multiple dwelling: buyer recovers no rent until it registers; one- or two-family house: discretionary stay only. | Walk 2.1 lets the buyer collect the whole balance (R5B-03). |
| C11 | Belongings not held for rent; released on request; disposed of only when abandoned; reasonable moving and storage cost retainable. | None. |
| C12 | Vacated Friday 2026-12-11; day 14 is Friday 2026-12-25 (Christmas, GCN 24); due Monday 2026-12-28 (GCN 25-a). Weekdays computed. | None. |
| C13 | Only the tenant's share is charged; owner keeps the move-out month's HAP and gets none after; written list and refund within 14 days. | None. |
| C14 | Agency took the account after default: FDCPA debt collector; DCWP licence; broker licence for the rent part or refer the rent part to an attorney; validation notice within five days of first contact to an address where the tenant receives mail; verification with lease and statement; six years (three for suits from the 90th day after S9760 becomes law); 2% interest; 23 NYCRR 1 inapplicable; CO, registration and 302-a checked before suing for rent; licence pleaded (CPLR 3015(e)); suit only where the tenant signed or lives. | None. |
| C15 | Filing on day 5: applying the deposit to pre-filing charges is stayed setoff; hold only the disputed part with a prompt stay-relief motion; statement by day 14 without a demand; the rest paid to the chapter 7 trustee once the landlord knows of the case (to the debtor in chapter 13). | None. |
| T-232 | Bare monthly rent: month-to-month from the start; leaving at the end of June owes nothing after June; statement due Tuesday 2026-07-14 (vacated Tuesday 2026-06-30). 'A long time': RPL 232 term to 2026-10-01; July rent, due Wednesday 2026-07-01 and unpaid on the statement date, may be kept if no new lease began; August and September later, subject to RPL 227-e. | None. |
| T-vacate | No rent after the 2026-03-10 ouster; March rent (due Sunday 2026-03-01, payable Monday 2026-03-02 under GCN 25) is earned only for 2026-03-01 to 2026-03-10 (10/31); 21/31 of the installment is refunded or credited (Kennedy; Strasburger); if March was unpaid only 10/31 may be kept from the deposit or claimed; the tenant also holds a loss-of-bargain damages claim because the owner caused the order. If the order followed a sudden casualty, RPL 227 gives the same adjustment. | Walk says the March installment 'is not barred' without the apportionment (R5B-01). |
| T-lead | Owner-occupied pre-1960 two-family: the tenant's unit is within the lead article (27-2056.1), so turnover lead work is the owner's cost; not a multiple dwelling for the MDL rent bars; no HPD registration duty while the owner lives there; Good Cause exempt (owner-occupied, ten units or fewer). A removed battery-operated combination smoke/CO device is charged at no more than $50; a hardwired one at the reasonable repair cost. | Walk does not say the $50 cap is for a battery-operated device (R5B-09). |
| T-collect | Handoff demanding rent in its own name or taking payment: broker licence; manager demands and payment settles to the manager's account: none for Handoff; damage-only balance: no broker licence. | None. |

## New versus earlier rounds (written after the findings were saved)

- R5B-01: Partly earlier. Round 3 (R3-11) put a day-count refund in T-vacate without authority; round 4B (R4B-11) removed it as unsupported and sent the question here. 5B decides it with authority not cited before (Kennedy, App Term 1st; Strasburger, CoA; Peerless, App Term 2d). The rule changed in round 4.
- R5B-02: New. No earlier round tested RPL 227's sudden-casualty limit (Suydam) or the reading of Younger (Municipal Court) in the round-4 vacate-order rule.
- R5B-03: New. Review 4A listed RPL 223 as covered; no round addressed pre-sale arrears.
- R5B-04: New, and introduced by round 4: R4A-04 framed 11 USC 108(c) as extending 'a claim by or against a former tenant', and the round-4 rules applied it to the tenant's own claims; 108(a) was not cited in any round. The six-year file instruction came in with R4A-05.
- R5B-05: New. Round 4A (R4A-22) added the RPAPL 1305 rule; its limits were not stated then.
- R5B-06: Earlier in substance: round 2's test-case answer for C3 gave the same refund route (electronic payment or a check to the last postal address), but it never reached the rule or the walk.
- R5B-07: New.
- R5B-08: Partly earlier: rounds 1-4 settled the two-part test (R4B-03 last); the leftover 'knew or should have known' judgment-term label was not raised.
- R5B-09: Partly earlier: R3-12 added the battery-operated limit to the rule; T-lead still omits it. The 27-2045(e) useful-life reimbursement point is new.
- R5B-10: New.

Earlier corrections rated:

- R4B-11 (T-vacate day count): over-corrected. It rightly found the day count unsupported by Younger and Barash, but removing the apportionment left the walk stating less than the law; Kennedy and Strasburger support apportionment (R5B-01).
- R3-11 (T-vacate day-count refund): result correct in substance (March earned to the ouster, the rest refunded), unsupported when made.
- R4A-04 (tolling): correct for the landlord's claims; incorrect as applied to the former tenant's own claims, which 11 USC 108(a) governs (R5B-04).
- R4A-05 (tenant's time to sue): periods and Gaidon accrual correct; the six-year file instruction contradicts the tolling it lists (R5B-04).
- R4A-22 (foreclosure successor): correct gap; the added rule omits the section's limits (R5B-05). The disposition's narrowing (dropping the reviewer's unsupported pre-notice payment rule) was correct.
- R4B-03 (willfulness): correct; the rule's judgment-term label still carries the rejected test (R5B-08).
- R3-12 (battery-operated detector cap): correct; T-lead text not updated (R5B-09).
- Round 3 RPL 232 reversal (bare monthly rent is month to month): correct; additional support found in Mayer Meat v Heilman (App Term 1st 1923).
- R4B-01, R4B-02, R4B-04 to R4B-10, R4B-12 to R4B-15 and R4A-01 to R4A-03, R4A-06 to R4A-21, R4A-23 to R4A-34: correct as applied; every rule they produced was re-checked and appears in the Confirmed list.
- No earlier finding is rejected.

## Method

- Read grounding (APERTURE.md, STAGE_A.md) and the whole walk.
- review/ir5b_dump.py printed, for all 455 cited ids in walk order, the citing walk paragraph beside every rule field (condition, effect, determinacy, dates, quote, source, construction quotes, reasoning); all 42 chunks were read in full.
- Sources opened in context for every rule whose effect goes beyond its quote and for each flagged item; new sources fetched by review/ir5b_fetch.py (Harvard Caselaw Access Project static files for older NY reports; Assembly actions pages; uscode.house.gov) and saved as sources/REVIEW5B_*.txt. CourtListener pages were blocked (CloudFront 403); its search API was used to look for citing and contrary decisions.
- Dates computed with Python (weekday of every test-case date; GCN 24 holidays).
- Test cases decided from the rules and sources before comparing with the walk's answers.
- Findings, T-vacate ruling and this list written by review/ir5b_build.py; review/ir5b_verify.py checks every evidence quote verbatim (whitespace-normalized) in its source and every rule id, with a self-test that catches a planted bad quote and a planted bad id.
- Disclosure: before saving findings I opened review/ir4b_text.py (a round-4 helper script, not on the excluded list) looking for the fetch pattern; its confirmed list names an R4B-11 'apportionment wording in T-vacate'. I did not open the round-4 report or dispositions until my findings were saved, and the T-vacate ruling rests on sources I fetched and read (Kennedy, Strasburger, Peerless, Suydam, Warrin).

New sources saved (sources/REVIEW5B_*): Kennedy v Peterart Realty (App Term 1st 1939); Matter of Strasburger (CoA 1892); Peerless Candy v Halbreich (App Term 2d 1925); Suydam v Jackson (Commission of Appeals 1873); Warrin v Haverty (1st Dept 1913); Niles v Iroquois Realty (1st Dept 1909); Getty Realty v 2 East 61st Street (App Term 1st 1939); 1239 Madison Ave v Neuburger (1st Dept 1924); Mayer Meat v Heilman (App Term 1st 1923); 11 USC 108; Assembly actions for S947 and S9760 as of 2026-09-29.
