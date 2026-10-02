# Independent Review 4A: completeness of the law for settling a market-rate NYC tenancy

2026-09-29. Reviewer 4A (fresh context, report only). Scope: NYC market-rate units (not stabilized, not controlled;
public and project-based housing out), NY State + NYC + federal law, from the facts fixed at move-in to the account
closed. Machine-readable: `review/independent_review_4a.json`; universe: `review/review4a_universe.json`; coverage:
`review/ir4a_coverage.json`; evidence check: `python3 review/ir4a_verify.py`.

## Summary

- Universe enumerated blind from primary sources: **176 items** (117 state, 24 city, 35 federal; 13 controlling decisions, 6 pending or future-dated).
- Diff against NY.json, NYC.json and US.json (604 rules, 507 in the market-rate scope): 115 items fully stated, 9 stated in part, 46 with no rule, 4 deferred by the walk with a reason I accept, 2 that change no decision.
- Findings: **34** - 9 critical, 15 major, 10 minor. Over-scope: 1 group (3 rules), minor.
- All findings are new against rounds 1-3. One (R4A-10) also narrows a round-1 correction (R1-15).
- Judgment: the core of the chain (deposit cap, trust, interest, inspection, 14-day statement, forfeiture, willfulness,
  charges, mitigation, payees for co-tenants and bankruptcy, building preconditions, collection licensing, SHIELD, FDCPA)
  is complete and precise. The universe is **not yet complete**. The gaps again sit at the edges, in five clusters the
  earlier sweeps did not reach: (1) the tenant's personal status after move-out - death, military service, bankruptcy of a
  co-obligor, coerced debt; (2) time - every tolling and extension rule, and the tenant's own limitation period;
  (3) who is a 'landlord's agent' under FARE; (4) city rules that import state conduct rules (GBL 601 via 6 RCNY 5-77) or
  add new ones (SHIELD credit-reporting notice); (5) cross-cutting duties outside landlord-tenant law (anti-discrimination,
  information returns, tenant data). Of the nine critical findings, one corrects an accepted rule (R4A-01 adds a branch
  that reverses NYC:FARE-moveout-service-fee for a manager who is the landlord's agent); the other eight add rules the
  files do not have. After these are resolved, a round limited to these clusters should come back clean.

## Gaps and partial statements (most severe first)

### R4A-01 (partial, critical)

- Decision point: S5 charges and credits (move-out fees)
- Rules concerned: `NYC:FARE-moveout-service-fee`, `NYC:FARE-20-699.20-fee`, `NYC:FARE-20-699.22(b)`
- What is missing: The FARE atoms treat a move-out service fee as lawful if it was on the pre-lease disclosure. They miss Admin Code 20-699.21: a 'landlord's agent' (a licensed agent who found or obtained the tenant for the landlord) may not impose or collect ANY fee from the tenant related to the rental, disclosed or not, and the landlord is itself in violation when its agent does. Small managers who lease their own units are exactly this agent.
- Correct law, as a rule: Condition: a fee (a charge for services: move-out cleaning, repainting service, lock change service, processing or administration) related to the rental is imposed or collected on or after 2025-06-11. Branch (a): the person imposing or collecting it is a landlord's agent for this landlord (listing agent, cooperating agent, landlord's subagent or broker's agent who found or obtained this tenant; not a dual agent), or an agent who published the listing with the landlord's authorization (presumed). Effect: the fee is barred whether or not disclosed; the landlord is in violation (20-699.21(b)); the tenant may sue for compensatory relief (20-699.24); the final statement and any balance may not carry it. Branch (b): the landlord itself, or a manager who is not such an agent, imposes it: NYC:FARE-moveout-service-fee applies (disclosure governs). Rent and compensation for damage the tenant caused are not fees in either branch (NYC:FARE-20-699.20-fee).
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/NYC_ADC_20-699.21.txt`: "1. a landlord’s agent shall not impose any fee on, or collect any fee from, a tenant related to the rental of residential real property"
  - `sources/NYC_ADC_20-699.21.txt`: "b. A landlord is in violation of subdivision a of this section if: [ALP S-104] 1. a landlord’s agent of such landlord violates such subdivision"
  - `sources/NYC_ADC_20-699.20.txt`: "Landlord’s agent. The term “landlord's agent” means a listing agent who acts alone, or an agent who acts in cooperation with a listing agent, acts as a landlord's subagent, or acts as a broker's agent, to find or obtain a tenant for residential real property."
  - `sources/NYC_ADC_20-699.24.txt`: "Such court may order compensatory, injunctive and declaratory relief."

### R4A-02 (gap, critical)

- Decision point: S19 domestic violence; S9 pursuing a balance; S21 credit reporting
- Rules concerned: `NY:RPL-227-c(1)`, `US:15USC1681s-2(a)(3)`, `NY:ADJ-lease-balance-not-consumer-credit`
- What is missing: No atom states New York's coerced-debt law (GBL art. 29-HHH, 604-aa to 604-dd, in force 2026-06-17). Unlike GBL art. 29-H, its 'coerced debt' needs no extension of credit, only a household-purpose transaction, so it reaches a residential lease balance; the landlord, its manager and any collector are 'creditors'.
- Correct law, as a rule: Condition: a former tenant who is a natural person tells the landlord, manager or collector that all or part of a lease balance is coerced debt (incurred through duress, coercion or undue influence by an intimate partner, family or household member, trafficker, parent/caretaker, or caregiver of an elderly or protected person). Branch (a): the tenant supplies a sworn statement and adequate documentation (police report, law-enforcement report, court order, or sworn statement of a qualified third party). Effect: within 10 business days stop collection activity on that debt; within 10 business days tell any consumer reporting agency the landlord reports to that the account is disputed; within 30 business days complete a review without contacting the alleged abuser, using only the contact details the tenant gave, and without disclosing the documents; if collection resumes, within 5 business days send the written determination and its good-faith basis. Branch (b): the tenant notifies without documents: send the statutory 604-bb(2)(a) notice text. In any suit, coerced debt is an affirmative defense; a tenant who proves it gets a declaration of non-liability, an injunction, dismissal of the landlord's claim, deletion of reported data and fees. The 14-day deposit statement is still sent: it is a statutory duty, not collection. Exclusion: a creditor who itself did the coercing is not a 'creditor'.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NY_GBL_604-AA_nysenate.txt`: "3. "Coerced debt" means a debt arising out of a transaction primarily for personal, family or household purposes that was incurred because of duress, intimidation, threat, force, coercion, manipulation, or undue influence within the context of intimate relationships or relationships between family or household members"
  - `sources/REVIEW4A_NY_GBL_604-BB_nysenate.txt`: "1. Within ten business days of receipt of the following, a creditor shall cease collection activities until completion of the review under subdivision three of this section: (a) adequate documentation of coerced debt; and (b) the debtor's statement that a particular debt being collected, or portion thereof, is coerced debt."
  - `sources/REVIEW4A_NY_GBL_604-BB_nysenate.txt`: "3. (a) Within ten business days of receiving all the information required under subdivision one of this section, the creditor shall, if such creditor furnishes adverse information about the debtor to a consumer reporting agency, notify such consumer reporting agency that the account is disputed."
  - `sources/REVIEW4A_NY_GBL_604-CC_nysenate.txt`: "4. In any action by a creditor against a debtor to collect a debt, it shall be an affirmative defense to such action that all or a portion of the debt is coerced debt."

### R4A-03 (gap, critical)

- Decision point: S16 death of tenant (who is paid; claims against the estate)
- Rules concerned: `NY:RPL-236-a`, `NY:RPL-236`, `NY:GOL-7-103(1)-trust`, `NY:ADJ-provide-address-branches`, `NY:COMMONLAW-owner-death-agency`
- What is missing: The rules cover the estate's options to end the lease (RPL 236, 236-a) and the owner's death, but no atom says who receives the statement and refund when the tenant dies, or how the landlord preserves its claim against the estate.
- Correct law, as a rule: Condition: the tenant (or the last surviving co-tenant) dies before the refund is paid or the balance collected. Payee: the refund belongs to the estate. Pay it to the executor or administrator on letters, or, for an estate of personal property of $50,000 or less, to a voluntary administrator on the court's short-form certificate, which discharges the landlord (SCPA 1301, 1305). SCPA 1310's pay-without-administration list (bank deposits, wages, public payments and similar) does not include a landlord's refund, so payment to a relative without letters or a certificate does not discharge the landlord. Statement: still due within 14 days of vacatur; send it to the fiduciary if one is known, otherwise to the last known address addressed to the tenant's estate (NY:ADJ-provide-address-branches), and hold the refund in trust (NY:GOL-7-103(1)-trust) until a fiduciary presents authority. Claims against the estate: present the claim to the fiduciary within 7 months of letters (after that the fiduciary is not chargeable for good-faith distributions, SCPA 1802); the limitation period against the estate is extended by 18 months after death (CPLR 210(b)); the estate's own deposit claim may be brought within one year after death if not yet expired (CPLR 210(a)).
- Earlier rounds: new: round 1 (R1-08) addressed RPL 236 silence only; payee and estate claims were not raised
- Evidence:
  - `sources/REVIEW4A_NY_SCPA_1301_nysenate.txt`: "A small estate is the estate of a domiciliary or a non-domiciliary who dies leaving personal property having a gross value of $50,000 or less"
  - `sources/REVIEW4A_NY_SCPA_1305_nysenate.txt`: "The delivery by a voluntary administrator to a debtor, transfer agent, safe deposit company, bank, trust company or other person holding or having custody or possession or control of any personal property of the decedent, of the short form certificate of the court, the receipt of the administrator, and the surrender of any evidentiary document, shall constitute a complete release and discharge"
  - `sources/REVIEW4A_NY_SCPA_1310_nysenate.txt`: "(a) "Debt" means (i) money or securities payable on account of a deposit in a bank, national bank, trust company, branch of a foreign banking corporation"
  - `sources/REVIEW4A_NY_SCPA_1802_nysenate.txt`: "If any claim is not presented within 7 months from the date of issue of letters, the fiduciary shall not be chargeable for any assets or moneys that he may have paid in good faith in satisfaction of any lawful claims or of any legacies or distributions to the legatees or distributees of the decedent before such claim was presented."
  - `sources/REVIEW4A_NY_CPLR_210_nysenate.txt`: "(b) Death of person liable. The period of eighteen months after the death, within or without the state, of a person against whom a cause of action exists is not a part of the time within which the action must be commenced against his executor or administrator."

### R4A-04 (gap, critical)

- Decision point: S11 limitations (tolling and extension)
- Rules concerned: `NY:CPLR-213(2)`, `NY:CPLR-214-i`, `US:11USC362(a)(6)`, `US:50USC3911(1)-(2)`
- What is missing: The limitation atoms state the six-year and three-year periods but no tolling or extension: military service, the debtor's bankruptcy, the debtor's death, or a written acknowledgment. Each moves the last day to sue.
- Correct law, as a rule: Add to every limitation computation for a claim by or against a former tenant: (1) the tenant's period of military service is excluded, for claims by or against the servicemember, heirs or representatives (50 USC 3936(a); Military Law 308 to the same effect); (2) if the tenant filed bankruptcy before the period ran, the period ends no earlier than 30 days after notice that the stay (or the chapter 13 co-debtor stay) ended (11 USC 108(c)); (3) 18 months after the tenant's death are excluded (CPLR 210(b)); (4) for the six-year contract period, a written acknowledgment or promise signed by the tenant restarts it and a part payment keeps its common-law effect (GOL 17-101); for a claim that is a consumer credit transaction CPLR 214-i bars revival, and a lease balance is not one (NY:ADJ-lease-balance-not-consumer-credit).
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_US_50USC_3936_uscode.txt`: "The period of a servicemember's military service may not be included in computing any period limited by law, regulation, or order for the bringing of any action or proceeding in a court, or in any board, bureau, commission, department, or other agency of a State (or political subdivision of a State) or the United States by or against the servicemember or the servicemember's heirs, executors, administrators, or assigns."
  - `sources/REVIEW4A_US_11USC_108_uscode.txt`: "(c) Except as provided in section 524 of this title, if applicable nonbankruptcy law, an order entered in a nonbankruptcy proceeding, or an agreement fixes a period for commencing or continuing a civil action in a court other than a bankruptcy court on a claim against the debtor, or against an individual with respect to which such individual is protected under section 1201 or 1301 of this title, and such period has not expired before the date of the filing of the petition, then such period does not expire until the later of- (1) the end of such period, including any suspension of such period occurring on or after the commencement of the case; or (2) 30 days after notice of the termination or expiration of the stay under section 362, 922, 1201, or 1301 of this title, as the case may be, with respect to such claim."
  - `sources/REVIEW4A_NY_CPLR_210_nysenate.txt`: "(b) Death of person liable. The period of eighteen months after the death, within or without the state, of a person against whom a cause of action exists is not a part of the time within which the action must be commenced against his executor or administrator."
  - `sources/REVIEW4A_NY_GOL_17-101_nysenate.txt`: "An acknowledgment or promise contained in a writing signed by the party to be charged thereby is the only competent evidence of a new or continuing contract whereby to take an action out of the operation of the provisions of limitations of time for commencing actions under the civil practice law and rules other than an action for the recovery of real property. This section does not alter the effect of a payment of principal or interest."

### R4A-05 (gap, critical)

- Decision point: S8 consequences of a miss; S11 limitations (landlord's exposure window)
- Rules concerned: `NY:GOL-7-108(1-a)(g)`, `NY:GOL-7-108(1-a)(e)-forfeiture`, `NY:CPLR-213(2)`
- What is missing: No atom states how long a former tenant may sue the landlord over the deposit. The punitive damages in 7-108(1-a)(g) and a recovery that exists only because of the (1-a)(e) forfeiture are liabilities created by statute (CPLR 214(2), three years); a claim for a deposit wrongly kept at common law is contract/trust (six years).
- Correct law, as a rule: Condition: a former tenant's claim concerning the deposit. Branch (a): punitive damages for a willful violation, or recovery of amounts the landlord could have kept at common law but lost only by the 14-day forfeiture: three years from accrual (CPLR 214(2); Gaidon: 214(2) governs where liability would not exist but for the statute). Branch (b): return of a deposit kept without a lawful basis (no rent owed, no tenant damage, wear and tear), or actual damages for it: six years (CPLR 213(1), (2)), the claim existing at common law under the 7-103 trust. Accrual: the day after the 14-day deadline passes. Tolling per R4A-04. The operator keeps the settlement file at least six years after vacatur.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NY_CPLR_214_nysenate.txt`: "2\. an action to recover upon a liability, penalty or forfeiture created or imposed by statute except as provided in sections 213 and 215;"
  - `sources/REVIEW4A_NY_CASE_Gaidon_v_GuardianLife_2001_CoA.txt`: "CPLR 214 (2) does not automatically apply to all causes of action in which a statutory remedy is sought, but only where liability “would not exist but for a statute” * (Aetna. Life & Cas. Co. v Nelson,* [67 NY2d 169, 174](/opinion/5688138/aetna-life-casualty-co-v-nelson/#174)). Thus, CPLR 214 (2) “does not apply to liabilities existing at common law which have been recognized or implemented by statute"

### R4A-06 (gap, critical)

- Decision point: S15 bankruptcy (who may be pursued)
- Rules concerned: `US:11USC362(a)(6)`, `US:11USC524(a)(2)`, `US:11USC542-refund-payee`
- What is missing: No atom states the chapter 13 co-debtor stay. When one tenant files chapter 13, the landlord may not collect the lease balance (a consumer debt) from a co-tenant or guarantor who is liable with the debtor.
- Correct law, as a rule: Condition: a tenant has a chapter 13 case pending (order for relief entered) and another individual is liable on the same lease balance or secured it (co-tenant, individual guarantor). Effect: the landlord, its manager and collectors may not act or sue to collect any part of the balance from that individual until the case is closed, dismissed or converted to chapter 7 or 11, unless the court grants relief (e.g., the co-debtor received the consideration, the plan does not pay the claim, or the landlord would be irreparably harmed). Exception: an individual who became liable in the ordinary course of its business (a commercial guarantor) is not protected. Chapter 7 has no co-debtor stay. Limitation against the co-debtor runs until 30 days after notice the stay ended (11 USC 108(c)).
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_US_11USC_1301_uscode.txt`: "(a) Except as provided in subsections (b) and (c) of this section, after the order for relief under this chapter, a creditor may not act, or commence or continue any civil action, to collect all or any part of a consumer debt of the debtor from any individual that is liable on such debt with the debtor, or that secured such debt, unless- (1) such individual became liable on or secured such debt in the ordinary course of such individual's business; or (2) the case is closed, dismissed, or converted to a case under chapter 7 or 11 of this title."

### R4A-07 (gap, critical)

- Decision point: S15 bankruptcy (amount of the landlord's claim)
- Rules concerned: `US:11USC542-refund-payee`, `NY:RPL-227-e`
- What is missing: No atom states the cap on a lessor's claim for lease-termination damages in the tenant's bankruptcy.
- Correct law, as a rule: Condition: the landlord files a proof of claim in a former tenant's bankruptcy for damages from termination of the lease (future rent). Effect: the allowed claim is capped at the rent reserved, without acceleration, for the greater of one year or 15% (not over three years) of the remaining term, counted from the earlier of the petition date and the date the tenant surrendered or the landlord repossessed, plus unpaid rent due on that earlier date. The claim is further reduced by mitigation under RPL 227-e and by any deposit applied after stay relief.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_US_11USC_502_uscode.txt`: "(6) if such claim is the claim of a lessor for damages resulting from the termination of a lease of real property, such claim exceeds- (A) the rent reserved by such lease, without acceleration, for the greater of one year, or 15 percent, not to exceed three years, of the remaining term of such lease, following the earlier of- (i) the date of the filing of the petition; and (ii) the date on which such lessor repossessed, or the lessee surrendered, the leased property; plus (B) any unpaid rent due under such lease, without acceleration, on the earlier of such dates;"

### R4A-08 (gap, critical)

- Decision point: S17 military service (rate on the balance)
- Rules concerned: `NY:ADJ-lease-interest-on-rent`, `NY:RPL-238-a(2)`, `US:50USC3911(1)-(2)`
- What is missing: No atom states the 6% cap on interest and fees for obligations a servicemember incurred before entering service.
- Correct law, as a rule: Condition: the tenant (alone or jointly with a spouse) signed the lease before entering military service, the lease makes the balance bear interest or late fees or other charges above 6% a year, and the tenant gives written notice with the orders (or the landlord confirms service through the DMDC) no later than 180 days after release. Effect: during the period of service the balance may not bear interest above 6% a year, 'interest' including service charges, fees and other charges; the excess is forgiven, not deferred; the landlord may obtain relief only by court order showing the tenant's ability to pay was not materially affected. Military Law 323-a imposes the same cap for state and federal active duty.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_US_50USC_3937_uscode.txt`: "An obligation or liability bearing interest at a rate in excess of 6 percent per year that is incurred by a servicemember, or the servicemember and the servicemember's spouse jointly, before the servicemember enters military service shall not bear interest at a rate in excess of 6 percent- (A) during the period of military service and one year thereafter, in the case of an obligation or liability consisting of a mortgage, trust deed, or other security in the nature of a mortgage; or (B) during the period of military service, in the case of any other obligation or liability."
  - `sources/REVIEW4A_US_50USC_3937_uscode.txt`: "The term "interest" includes service charges, renewal charges, fees, or any other charges (except bona fide insurance) with respect to an obligation or liability."
  - `sources/REVIEW4A_NY_MIL_323-A_nysenate.txt`: "As used in this section the term "interest" includes service charges, renewal charges, fees and any other charges (except bona fide insurance) with respect to such obligation or liability."

### R4A-09 (partial, critical)

- Decision point: S2 when rent stops (fixed-term lease ended by the parties' conduct)
- Rules concerned: `NY:COMMONLAW-NYC-monthly-tenant-surrender`, `NYC:CASE-Pezzo-surrender`, `NY:RPL-227-e`
- What is missing: Surrender is covered for monthly tenancies and for keys kept past expiry, and RPL 227-e covers re-letting. No atom states the Court of Appeals rule on surrender by operation of law, which ends a fixed-term lease (and the rent) mid-term when both parties act inconsistently with its continuance, e.g. the landlord takes back possession for its own use or accepts the keys and treats the unit as its own.
- Correct law, as a rule: Condition: a tenant with a fixed term leaves early and the landlord's conduct, together with the tenant's, is so inconsistent with the landlord-tenant relationship that it shows intent to treat the lease as ended (for example: the landlord accepts the keys and occupies, renovates or combines the unit for its own account, or releases the tenant). Effect: the lease ends on that date and rent stops; the landlord recovers only rent accrued before it and proven damages. Standard, decided on all the facts. Mere acceptance of keys for re-letting on the tenant's account, or re-letting under 227-e, is not surrender by operation of law (227-e governs that branch).
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NY_CASE_Riverside_v_KMGA_1986_CoA.txt`: "A surrender by operation of law occurs when the parties to a lease both do some act so inconsistent with the landlord-*692tenant relationship that it indicates their intent to deem the lease terminated"
  - `sources/REVIEW4A_NY_CASE_Riverside_v_KMGA_1986_CoA.txt`: "As distinguished from an express surrender, a surrender by operation of law is inferred from the conduct of the parties *(Bedford v Terhune,* [30 NY 453, 463](/opinion/3616239/bedford-v-terhune/#463); Rasch, *op. cit.* § 859). Whether a surrender by operation of law has occurred is a determination to be made on the facts."

### R4A-10 (partial, major)

- Decision point: S13 collection conduct (NYC)
- Rules concerned: `NY:GBL-601(2)`, `NY:GBL-601(9)`, `NY:ADJ-lease-balance-not-consumer-credit`, `NYC:RCNY6-5-77(e)(1)`, `NYC:RCNY6-5-76-debt-collector`
- What is missing: The walk defers GBL 601 as deciding nothing because art. 29-H does not reach a lease balance. That is right for the state statute, but the current 6 RCNY 5-77 incorporates GBL 601's conduct into the city rule: (d)(17) makes conduct proscribed by GBL 601(1), (3), (5), (7), (8) or (9) deceptive, and (e)(8) makes conduct prohibited by 601(2) or (4) unconscionable. 5-77 reaches a landlord's own staff collecting NYC former-tenant balances. No atom states this.
- Correct law, as a rule: Condition: a debt collector under 6 RCNY 5-76 (including the landlord's or manager's staff who regularly collect) collects a NYC former tenant's balance after debt collection procedures begin (a final statement demanding the balance starts them). Effect: it may not (601(1)) pose as law enforcement or a government agency; (601(2)) knowingly collect or assert a collection fee, attorney's fee, court cost or expense not justly due and legally chargeable; (601(3)) disclose credit information it knows or should know is false; (601(4)) tell the tenant's employer about the claim before final judgment; (601(5)) disclose a debt it knows is disputed without saying so; (601(7)) threaten action it does not in fact take in the usual course; (601(8)) claim or threaten to enforce a right it knows or should know does not exist; (601(9)) use a communication that looks like legal process or like it comes from a government body or an attorney when it does not. Each is a DCWP violation charged to the employer (NYC:RCNY6-5-77(g)).
- Earlier rounds: new, and it narrows round 1: R1-15 (accepted) moved all GBL 601 rules to the deferred list as deciding nothing; for NYC units that is over-corrected, because 6 RCNY 5-77(d)(17) and (e)(8) import GBL 601's conduct into the city rule
- Evidence:
  - `sources/NYC_RCNY6_5-77.txt`: "(17) any conduct proscribed by New York General Business Law §§ 601(1), (3), (5), (7), (8), or (9);"
  - `sources/NYC_RCNY6_5-77.txt`: "(8) engaging in any conduct prohibited by New York General Business Law §§ 601(2) or (4); or"

### R4A-11 (gap, major)

- Decision point: S21 credit reporting (NYC, from 2027-01-01)
- Rules concerned: `NYC:SHIELD-5-76-debt-collector`, `NYC:SHIELD-operative-date`, `US:12CFR1006.30(a)`
- What is missing: The SHIELD atoms omit new 6 RCNY 5-77(e)(10): before furnishing a debt to a consumer reporting agency, a debt collector (which from 2027 includes a landlord that regularly collects its own balances) must send notice and wait 14 days.
- Correct law, as a rule: Condition: from 2027-01-01, a landlord, manager or collector that is a 'debt collector' under the SHIELD definition intends to report a NYC former tenant's balance to a consumer reporting agency. Effect: first send, in at least one medium used to collect and also by U.S. mail, a clear notice that the debt will be reported; wait 14 consecutive days; monitor for undeliverability notices and, if one arrives, do not report until the notice is re-sent properly. Exemption: furnishers subject to FCRA 623(a)(7) (financial institutions), which does not include a landlord.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/NYC_DCWP_SHIELD_NOA_2026.txt`: "(10) furnishing to a consumer reporting agency, as defined in section 603(f) of the Fair Credit Reporting Act (15 U.S.C. § 1681a(f)), information about a debt unless the debt collector has sent to the consumer in at least one medium of communication used to collect the debt, and sent a written copy to the consumer via U.S. mail or other delivery service, a notice that states, clearly and conspicuously, that the information about the debt will be reported to a consumer reporting agency and has waited 14 consecutive days after sending such notice."

### R4A-12 (gap, major)

- Decision point: S13 collection letters (balance that grows)
- Rules concerned: `US:15USC1692e(2)(A)`, `US:12CFR1006.34(c)`, `NY:ADJ-lease-interest-on-rent`
- What is missing: No atom states the controlling Second Circuit rule that a collection notice stating a current balance must disclose that the balance may increase when interest or fees are accruing.
- Correct law, as a rule: Condition: an FDCPA debt collector (a collector, a law firm, or a manager collecting a balance obtained after default) states a former tenant's balance while interest or fees accrue on it (lease interest, statutory prejudgment interest being claimed, late fees). Effect: the notice must say the balance may increase due to interest and fees; otherwise it is misleading under 1692e. If nothing accrues, no disclosure is needed.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_US_CASE_Avila_v_Riexinger_2016_2dCir.txt`: "We hold that Section 1692e of the FDCPA requires debt 8 collectors, when they notify consumers of their account balance, to disclose that 9 the balance may increase due to interest and fees."

### R4A-13 (gap, major)

- Decision point: S10 procedure before judgment
- Rules concerned: `NY:CPLR-3215(g)(3)`, `US:50USC3931(b)(1)`
- What is missing: The default-judgment atoms cover the additional mailing and the SCRA affidavit, not CPLR 3215(j): a clerk's default judgment needs an affidavit that the limitation period has not expired.
- Correct law, as a rule: Condition: the landlord or its collector asks the clerk for a default judgment on a former tenant's balance. Effect: attach an affidavit by the plaintiff or its attorney that, after reasonable inquiry, the plaintiff believes the limitation period has not expired (using the OCA form); without it the clerk cannot enter judgment.
- Earlier rounds: new: round 2 (R2-11) fixed the small-claims exception to 3215(g)(3); 3215(j) was not raised
- Evidence:
  - `sources/REVIEW4A_NY_CPLR_3215_nysenate.txt`: "(j) Affidavit. A request for a default judgment entered by the clerk, must be accompanied by an affidavit by the plaintiff or plaintiff's attorney stating that after reasonable inquiry, he or she has reason to believe that the statute of limitations has not expired."

### R4A-14 (gap, major)

- Decision point: S5 charges (what the lease can prove)
- Rules concerned: `NY:ADJ-lease-break-charge`, `NY:RPL-238-a(2)`, `NY:ADJ-lease-interest-on-rent`
- What is missing: No atom states CPLR 4544: lease text in print under 8 points (5.5 for upper case) cannot be received in evidence for the landlord who prepared it, so a charge resting only on that clause (late fee, lease-break fee, interest, fee clause) cannot be proved.
- Correct law, as a rule: Condition: a charge on the final account rests on a lease clause printed in type smaller than 8 points (5.5 for upper case) or not clear and legible, in a lease the landlord or its agent printed or prepared. Effect: the clause cannot be put in evidence by the landlord, so the charge is not kept from the deposit and is not pursued; the tenant may still rely on it. Waiver void.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NY_CPLR_4544_nysenate.txt`: "The portion of any printed contract or agreement involving a consumer transaction or a lease for space to be occupied for residential purposes where the print is not clear and legible or is less than eight points in depth or five and one-half points in depth for upper case type may not be received in evidence in any trial, hearing or proceeding on behalf of the party who printed or prepared such contract or agreement, or who caused said agreement or contract to be printed or prepared."

### R4A-15 (gap, major)

- Decision point: S4 custody of the deposit by a licensed managing agent
- Rules concerned: `NY:GOL-7-103(1)-trust`, `NY:HANDOFF-broker-config-collects-rent`, `NY:RPL-440(1)-rent-collection`
- What is missing: The broker-licence configuration atoms do not state the DOS escrow rule for a licensed broker who holds tenants' deposits for the owner.
- Correct law, as a rule: Condition: a licensed real estate broker (the managing agent, or Handoff in its broker configuration) receives or holds a tenant's deposit or other money of its principal. Effect: it may not commingle that money with its own and must keep it in a separate special bank account used only for such funds; a breach is a licensing violation in addition to the 7-103 trust breach (which forfeits use of the deposit, NY:CASE-Paterno-commingling-forfeiture).
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NY_19NYCRR_175.1_LII.txt`: "A real estate broker shall not commingle the money or other property of his principal with his own and shall at all times maintain a separate, special bank account"

### R4A-16 (gap, major)

- Decision point: S1 facts fixed at move-in; S5 credits
- Rules concerned: `NY:RPL-238-a(2)`, `NY:RPL-238-a(3)`, `NYC:FARE-20-699.22(b)`
- What is missing: RPL 238-a(1) has no atom: except background and credit checks (actual cost or $20, whichever is less), no payment, fee or charge may be demanded before or at the beginning of the tenancy. A move-in, amenity or application fee still on the ledger cannot be carried into the final account, and one paid is recoverable by the tenant.
- Correct law, as a rule: Condition: the ledger shows a fee or charge demanded before or at the start of the tenancy other than the deposit, the first rent and a background/credit check within the cap. Effect: do not charge it on the final account or keep it from the deposit; if the tenant paid it, it is a tenant claim that can be offset against any balance. Background/credit fees over the lesser of actual cost or $20, or charged without giving the tenant a copy of the check and receipt, are the same.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/NY_RPL_238-A.txt`: "or demand any other payment, fee or charge before or at the beginning of the tenancy, except background checks and credit checks as provided by paragraph (b) of this subdivision"

### R4A-17 (gap, major)

- Decision point: S9 pursuing a guarantor
- Rules concerned: `US:15USC1692a(3)`, `NY:RPL-236-a`
- What is missing: No atom states when a guarantor of a residential lease may be pursued for the former tenant's balance.
- Correct law, as a rule: Condition: the landlord seeks the balance from a person other than the tenant who promised to answer for it. Effect: only if the guaranty is in a writing signed by the guarantor (GOL 5-701(a)(2)); an oral guaranty is void. The guarantor is a consumer for FDCPA and city collection rules when the guaranty was personal. The chapter 13 co-debtor stay protects an individual guarantor (R4A-06).
- Earlier rounds: new: guarantors appear in earlier rounds only as defendants for the 2% interest rate (R1-01)
- Evidence:
  - `sources/REVIEW4A_NY_GOL_5-701_nysenate.txt`: "2\. Is a special promise to answer for the debt, default or miscarriage of another person;"

### R4A-18 (gap, major)

- Decision point: S22 anti-discrimination binding charges and settlement
- Rules concerned: `US:42USC3604(f)(3)(A)`, `US:42USC3604(f)(3)(B)-animal-fees`, `NY:RPL-227-c(1)`
- What is missing: No atom states the general anti-discrimination rules that bind terms of the tenancy, which include deposit handling, deductions and collection: the FHA terms-and-conditions rule, NY Executive Law 296(5)(a)(2), NYC Admin Code 8-107(5)(a)(1)(b) (including lawful source of income, which covers vouchers), and RPL 227-d (domestic-violence status).
- Correct law, as a rule: Condition: any settlement decision (what is deducted, how strictly damage is assessed, whether a balance is pursued or reported). Effect: apply the same standard to every tenant; do not vary it because of race, creed, color, national origin, citizenship or immigration status, gender, age, disability, sexual orientation, marital or partnership status, military or uniformed service, height, weight, familial status or children, domestic-violence victim status, or lawful source of income (a voucher or other assistance, whether paid to the landlord or the tenant). Exemption for the NYC and state housing provisions: owner-occupied two-family buildings not publicly advertised, and owner-occupied rooms. Violations carry damages and penalties before the city and state commissions and courts.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_US_24CFR_100.65_ecfr.txt`: "(1) Using different provisions in leases or contracts of sale, such as those relating to rental charges, security deposits and the terms of a lease and those relating to down payment and closing requirements, because of race, color, religion, sex, handicap, familial status, or national origin."
  - `sources/REVIEW4A_NY_EXEC_296_nysenate.txt`: "(2) To discriminate against any person because of race, creed, color, national origin, citizenship or immigration status, sexual orientation, gender identity or expression, military status, sex, age, disability, marital status, status as a victim of domestic violence, lawful source of income or familial status in the terms, conditions or privileges of the sale, rental or lease of any such housing accommodation or in the furnishing of facilities or services in connection therewith."
  - `sources/REVIEW4A_NYC_ADC_8-107.txt`: "(b) To discriminate against any such person or persons in the terms, conditions or privileges of the sale, rental or lease of any such housing accommodation or an interest therein or in the furnishing of facilities or services in connection therewith; or"
  - `sources/REVIEW4A_NYC_ADC_8-102.txt`: "Lawful source of income. The term "lawful source of income" includes, but is not limited to, child support, alimony, foster care subsidies, income derived from social security, or any form of federal, state, or local public assistance or housing assistance including, but not limited to, section 8 vouchers, whether or not such income or credit is paid or attributed directly to a landlord."
  - `sources/REVIEW4A_NY_RPL_227-D_nysenate.txt`: "(a) No person, firm or corporation owning or managing any building used for dwelling purposes, or the agent of such person, firm or corporation, shall, because of such person's or family member's domestic violence victim status, (1) refuse to rent a residential unit to any person or family, when, but for such status, rental would not have been refused, (2) discriminate in the terms, conditions, or privileges of any such rental"

### R4A-19 (gap, major)

- Decision point: S20 tax and information reporting (deposit interest)
- Rules concerned: `NY:GOL-7-103(2)-interest-owed`, `NY:GOL-7-103(2-a)`, `NY:GOL-7-103(2-b)`
- What is missing: No atom states the information-return duty when the landlord passes deposit interest to the tenant.
- Correct law, as a rule: Condition: the deposit is in an interest-bearing account (required in buildings of six or more units), the bank pays the interest to the landlord, and the landlord pays or credits $10 or more of it to the tenant in a calendar year (annually, or at termination under 7-103(2-b)). Effect: the landlord received it as nominee and must file an information return (Form 1099-INT) and furnish the tenant a statement, which requires the tenant's name, address and TIN. Below $10 a year, no return.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_US_26USC_6049_uscode.txt`: "(2) who receives payments of interest (as so defined) as a nominee and who makes payments aggregating $10 or more during any calendar year to any other person with respect to the interest so received, shall make a return according to the forms or regulations prescribed by the Secretary, setting forth the aggregate amount of such payments and the name and address of the person to whom paid."

### R4A-20 (gap, major)

- Decision point: S21 data at move-out (NYC smart-access buildings)
- What is missing: No atom states the NYC Tenant Data Privacy Act duty triggered by the tenant's move-out.
- Correct law, as a rule: Condition: the unit is in a class A multiple dwelling that uses a smart access system (key fob, app, biometric or other electronic entry). Effect: within 90 days after the tenant permanently vacates, remove the tenant's reference data from the system (or anonymize it where removal would disable the system); authentication data must in any case be destroyed within 90 days of collection. Private right of action and civil penalties apply.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NYC_ADC_26-3002.txt`: "c. Reference data for any tenant who has permanently vacated a smart access building shall be removed, or anonymized where removal of such data would render the smart access system inoperable, from the smart access system no later than 90 days after such tenant has permanently vacated such building."

### R4A-21 (gap, major)

- Decision point: S13 licensed collection-agency configuration
- Rules concerned: `NY:HANDOFF-broker-config-collection-agency`, `NYC:ADC-20-493.1(b)`, `NYC:ADC-20-490`
- What is missing: For the configuration in which the collector is a DCWP-licensed agency, the atoms cover 20-493.1(b) but not the rules that say what the written payment-plan confirmation must contain and what records must be kept.
- Correct law, as a rule: Condition: a DCWP-licensed debt collection agency agrees a payment schedule or settlement with a former tenant, or collects at all. Effect: the written confirmation must name the originating creditor, the agency, the employee (or supervisor), the consumer, the agreement date, each payment's amount and due date, where to pay, all other terms and the conditions for satisfying the balance (6 RCNY 2-192); the agency keeps a separate file for each debt with the records in 6 RCNY 2-193.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NYC_RCNY6_2-192.txt`: "(a) The written confirmation of the debt payment schedule or settlement agreement with a consumer that a debt collection agency is required to furnish pursuant to § 20-493.1 (b) shall identify the originating creditor of the debt, the debt collection agency, the employee of such agency who concluded the debt payment schedule or agreement or the employee's direct supervisor, the name and address of the consumer, the date on which the debt payment schedule or agreement was made, the specific amount and due date of each payment, the address where the payments are to be mailed or where payment may otherwise be transmitted, any other terms of the debt payment schedule or agreement, and the conditions for satisfying the outstanding balance."
  - `sources/REVIEW4A_NYC_RCNY6_2-193.txt`: "2-193 Records to be Maintained by Debt Collection Agency. (a) Unless otherwise prohibited by federal, state or local law, a debt collection agency shall maintain a separate file for each debt"

### R4A-22 (gap, major)

- Decision point: S3 who may collect after foreclosure
- Rules concerned: `NY:GOL-7-105(1)`, `NY:RPL-223`, `NY:CPLR-6401-foreclosure-receiver`
- What is missing: The rules cover the deposit's transfer on foreclosure and receivers, but not the successor's duties toward a market-rate tenant under RPAPL 1305, which decide who may collect rent and from when.
- Correct law, as a rule: Condition: the building is sold in foreclosure (or transferred during it) while a market-rate tenant is in occupancy. Effect: the successor takes subject to the tenant's right to stay for the rest of the lease (or 90 days after notice, whichever is greater) on the same terms, and must give written notice of that right and of its name and address; until the tenant has that notice, rent paid to the former landlord's representative is not a default. The federal Protecting Tenants at Foreclosure Act gives a 90-day floor where the mortgage was federally related; the longer state protection controls.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NY_RPAPL_1305_nysenate.txt`: "a successor in interest of residential real property shall provide written notice to all tenants in the same manner as required by subdivision four of section thirteen hundred three of this article: (a) that they are entitled to remain in occupancy of such property for the remainder of the lease term, or a period of ninety days from the date of mailing of such notice, whichever is greater, on the same terms and conditions as were in effect at the time of entry of the judgment of foreclosure and sale, or if no such judgment was entered, upon the terms and conditions as were in effect at the time of transfer of ownership of such property; and (b) of the name and address of the new owner."
  - `sources/REVIEW4A_US_12USC_5220_uscode_PTFA.txt`: "the provision, by such successor in interest of a notice to vacate to any bona fide tenant at least 90 days before the effective date of such notice"

### R4A-23 (gap, major)

- Decision point: S7 payment fees (pending bill)
- Rules concerned: `NY:RPL-235-g`
- What is missing: S947/A3121 (amending RPL 235-g) passed the Senate on 2026-03-18 and the Assembly on 2026-05-13 and has not been delivered to the Governor. No dated future atom records it.
- Correct law, as a rule: Pending, effective immediately upon becoming law: a landlord may not charge any fee for rent paid by ACH, and must offer at least one rent-payment method with no landlord fee (e.g., cash or personal check); any waiver is void. Until then NY:RPL-235-g governs. Any convenience fee on a former tenant's balance paid by ACH after enactment is barred.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NY_S00947_Assembly_2025-26.txt`: "2. A landlord shall not assess any fee or other charge for the use of 9 an automated clearing house payment for the payment of rent."
  - `sources/REVIEW4A_NY_S00947_Assembly_2025-26.txt`: "03/18/2026PASSED SENATE 03/18/2026DELIVERED TO ASSEMBLY 03/18/2026referred to housing 05/13/2026substituted for a3121 05/13/2026ordered to third reading cal.102 05/13/2026passed assembly"

### R4A-24 (gap, major)

- Decision point: S15 bankruptcy (lease still running when a chapter 7 is filed)
- Rules concerned: `US:11USC362(a)(6)`, `US:11USC542-refund-payee`
- What is missing: No atom states the deemed rejection of a residential lease in chapter 7, which fixes when post-petition rent becomes a pre-petition claim.
- Correct law, as a rule: Condition: a tenant files chapter 7 while the lease is unexpired. Effect: unless the trustee assumes it within 60 days of the order for relief (or a court-extended period), the lease is deemed rejected; rejection is a breach as of immediately before the petition, so the landlord's damages are a pre-petition unsecured claim (capped under R4A-07) and are dischargeable; the tenant's continued occupancy after the petition is claimed as use and occupancy.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_US_11USC_365_uscode.txt`: "(d)(1) In a case under chapter 7 of this title, if the trustee does not assume or reject an executory contract or unexpired lease of residential real property or of personal property of the debtor within 60 days after the order for relief, or within such additional time as the court, for cause, within such 60-day period, fixes, then such contract or lease is deemed rejected."
  - `sources/REVIEW4A_US_11USC_365_uscode.txt`: "the rejection of an executory contract or unexpired lease of the debtor constitutes a breach of such contract or lease- (1) if such contract or lease has not been assumed under this section or under a plan confirmed under chapter 9, 11, 12, or 13 of this title, immediately before the date of the filing of the petition;"

### R4A-25 (gap, minor)

- Decision point: S20 tax (owner income; write-off)
- What is missing: No atom states the federal tax treatment the owner meets at settlement: kept deposit is income in the year kept; no cancellation-of-debt return is due on a write-off by a non-financial landlord.
- Correct law, as a rule: A refundable deposit is not income when received; the part kept is income in the year kept; a deposit to be applied as last month's rent is advance rent, income when received (IRS Pub. 527). Writing off a former tenant's balance creates no Form 1099-C duty, because 6050P applies only to financial entities and government agencies.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_US_IRS_Pub527_2025.txt`: "Don’t include a security deposit in your income when you receive it if you plan to return it to your tenant at the end of the lease. But if you keep part or all of the security deposit during any year because your tenant doesn’t live up to the terms of the lease, include the amount you keep in your income in that year."
  - `sources/REVIEW4A_US_26USC_6050P_uscode.txt`: "The term "applicable entity" means- (A) an executive, judicial, or legislative agency (as defined in section 3701(a)(4) of title 31, United States Code), and (B) an applicable financial entity."

### R4A-26 (gap, minor)

- Decision point: S8 consequences (unpaid small-claims judgment)
- What is missing: No atom states CCA 1812: a business that leaves small-claims judgments unpaid faces a treble-damages action.
- Correct law, as a rule: Condition: a tenant holds an unpaid NYC small-claims judgment against the landlord arising from its business, there are at least two other unpaid small-claims judgments from the same business, and the landlord does not pay within 30 days of notice. Effect: the tenant may sue for three times the judgment plus fees; inability to pay is the only defense.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NY_CCA_1812_nysenate.txt`: "(b) Where each of the elements of subdivision (a) of this section are present the judgment creditor shall be entitled to commence an action against said judgment debtor for treble the amount of such unsatisfied judgment, together with reasonable counsel fees"

### R4A-27 (gap, minor)

- Decision point: S8 forum for the tenant's deposit claim
- Rules concerned: `NY:CCA-1809(1)`
- What is missing: No atom states that a tenant may sue a landlord in NYC small claims over a NYC tenancy regardless of where the landlord lives, up to $10,000.
- Correct law, as a rule: A former tenant's deposit claim up to $10,000 (exclusive of interest and costs) may be brought in NYC small claims when the property is in NYC, even if the landlord neither lives nor does business in NYC.
- Earlier rounds: new: round 1 (R1-14) added small/commercial claims for the landlord as plaintiff; the tenant's forum was not raised
- Evidence:
  - `sources/REVIEW4A_NY_CCA_1801_nysenate.txt`: "or where claimant is a tenant or lessee of real property owned by the defendant and the claim relates to such tenancy or lease, and such real property is situated within the city of New York."

### R4A-28 (partial, minor)

- Decision point: S4 commingling (First Department authority)
- Rules concerned: `NY:CASE-Paterno-commingling-forfeiture`, `NY:CASE-Paterno-bank-notice-inference`
- What is missing: The commingling forfeiture is grounded only on Second Department cases. The First Department holds the same (LeRoy v Sayers), and adds that the tenant's own lease breach is no defense; worth citing for New York and Bronx County.
- Correct law, as a rule: Commingling is a conversion: the tenant recovers the deposit at once, and the tenant's breach of the lease is no defense (1st Dept).
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NY_CASE_LeRoy_v_Sayers_1995_1stDept.txt`: "it has been uniformly held that a commingling constitutes a conversion and entitles the tenant to the immediate recovery of his deposit or advances."

### R4A-29 (partial, minor)

- Decision point: S9 fee exposure when pursuing
- Rules concerned: `NY:RPL-234`
- What is missing: NY:RPL-234 states reciprocity but not its breadth under Graham Court: a clause giving the landlord fees for retaking possession after the tenant's default triggers the tenant's reciprocal right.
- Correct law, as a rule: A lease clause letting the landlord recover attorneys' fees incurred in retaking possession after the tenant's default is within RPL 234, so a tenant who defeats the landlord's claim (or wins its own claim for the landlord's breach) recovers reasonable fees.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NY_CASE_GrahamCourt_v_Taylor_2015_CoA.txt`: "We hold that Real Property Law § 234, which imposes a covenant in favor of a tenant’s right to attorneys’ fees, applies to a lease that authorizes the landlord to cancel the lease upon tenant’s default, repossess the premises and then collect attorneys’ fees incurred in retaking possession."

### R4A-30 (gap, minor)

- Decision point: S13 statements about family members
- Rules concerned: `NY:GBL-601(2)`
- What is missing: GBL 601-a is not in the files. It is not limited to 'consumer claims', so it reaches a lease balance.
- Correct law, as a rule: No landlord, manager or collection agency may represent that a family member must pay the tenant's debt contrary to the FDCPA, or misrepresent a family member's obligation (e.g., telling a parent or the estate's heirs they owe the balance).
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NY_GBL_601-A_nysenate.txt`: "No principal creditors and/or debt collection agencies shall make any representation that a person is required to pay the debt of a family member in a way that contravenes with the Fair Debt Collection Practices Act (15 USC § 1692 et seq.). In addition, the principal creditors and/or debt collection agencies shall not make any misrepresentation about the family member's obligation to pay such debts."

### R4A-31 (partial, minor)

- Decision point: S14 unclaimed funds (reporting code)
- Rules concerned: `NY:OSC-MS11-refunds-due`
- What is missing: NY:OSC-MS11-refunds-due is right for an owner. A real-estate company holding deposits in escrow reports under TR04.
- Correct law, as a rule: Branch (a): the owner (or a non-broker manager) holds the unclaimed refund: MS11 Refunds Due, three years. Branch (b): a real-estate company (licensed managing agent) holds it in its escrow account: TR04 Escrow Accounts (held by real estate companies), three years. Same dormancy, different code.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/NY_OSC_unclaimed_property_type_table.txt`: "TR04 1315 Escrow Accounts (held by real estate companies) 3 years"

### R4A-32 (gap, minor)

- Decision point: S21 data security for refund data
- What is missing: No atom states the SHIELD Act safeguard duty for the bank-account data collected to pay refunds electronically.
- Correct law, as a rule: Anyone holding a New York resident's private information (e.g., account number with access code for an ACH refund) must keep reasonable administrative, technical and physical safeguards, including secure disposal.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NY_GBL_899-BB_nysenate.txt`: "reasonable safeguards to protect the security, confidentiality and integrity of the private information"

### R4A-33 (gap, minor)

- Decision point: S1 move-in disclosure (1-3 unit buildings)
- Rules concerned: `NY:MDL-301(1)`, `NY:ADJ-MDL-rent-bar-not-1-2-family`
- What is missing: RPL 235-bb has no atom: owners of three or fewer rental units must disclose in bold whether any required certificate of occupancy is valid before the lease is signed. The statute states no remedy; it is evidence in a later dispute over rent for an unlawful unit.
- Correct law, as a rule: Condition: owner of 3 or fewer rental units. Effect: before signing, a bold notice whether a required CO is valid (or a copy of the CO); waiver void.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NY_RPL_235-BB_nysenate.txt`: "Prior to executing a residential lease or rental agreement with a tenant, the owner of real property consisting of three or fewer rental units shall provide conspicuous notice in bold face type as to whether a certificate of occupancy, if such certificate is required by law, is currently valid for the dwelling unit subject to the lease or rental"

### R4A-34 (gap, minor)

- Decision point: S10 non-military affidavit (state law)
- Rules concerned: `US:50USC3931(b)(1)`
- What is missing: Military Law 303(3) is not in the files. It removes any state-law non-military affidavit requirement except where federal law requires one; federal law (50 USC 3931) does, so the practical rule is unchanged.
- Correct law, as a rule: State law adds no non-military affidavit; the SCRA affidavit remains required for every default judgment.
- Earlier rounds: new: not raised in rounds 1-3 or their dispositions
- Evidence:
  - `sources/REVIEW4A_NY_MIL_303_nysenate.txt`: "3\. Where a default judgment may properly be rendered in any action or proceeding in any court, the court shall not require the attorney for the plaintiff or petitioner to submit an affidavit or affirmation that the defendant or respondent is not in military service, provided that the court may impose such requirement where authorized by federal law."

## Over-scope

- `US:24CFR983.259(c)-(e)`, `US:24CFR983.352(a)`, `US:24CFR983.353(b)` (minor): Project-based voucher rules. A PBV contract unit is project-based assistance, which the aperture for this review excludes and which the walk itself sends to the later subsidized-housing review; yet Step 5 cites these three as applying ('Project-based vouchers follow the same rules'). They decide nothing for a market-rate unit and should be listed as deferred with the other public/project-based rules.

No other in-scope rule is over-scope. The routing rules for stabilized and controlled status (RSL 26-504, RSC
2520.11, RCL 26-403), the loft-law rule and the seasonal and co-op exceptions to the one-month cap decide whether the
unit is market-rate at all, so they belong in Step 0. The deferred list is right except where R4A-10 says otherwise.

## Universe coverage

| Item | Citation | Status | Rules or finding |
|---|---|---|---|
| U001 | GOL 7-108(1), (1-a) opening | covered | NY:GOL-7-108(1) |
| U002 | GOL 7-108(1-a) exclusions | covered | NY:GOL-7-108(1-a)-exclusions |
| U003 | RPL 214 (Good Cause Eviction, covered housing) | covered | NY:RPL-214 |
| U004 | RPL 215 (necessity for good cause) | covered | NY:RPL-215 |
| U005 | GOL 7-108(1-a)(a) | covered | NY:GOL-7-108(1-a)(a) |
| U006 | GOL 7-108(1-a)(c) | covered | NY:GOL-7-108(1-a)(c)-offer NY:GOL-7-108(1-a)(c)-bar |
| U007 | GOL 7-103(1) | covered | NY:GOL-7-103(1)-trust |
| U008 | GOL 7-103(2) | covered | NY:GOL-7-103(2)-bank-notice |
| U009 | GOL 7-103(2) administration fee | covered | NY:GOL-7-103(2)-admin-fee |
| U010 | GOL 7-103(2-a) | covered | NY:GOL-7-103(2-a) |
| U011 | GOL 7-103(3) | covered | NY:GOL-7-103(3) |
| U012 | 19 NYCRR 175.1 | gap | R4A-15 |
| U013 | RPL 238-a(1) | gap | R4A-16 |
| U014 | CPLR 4544 | gap | R4A-14 |
| U015 | RPL 235-bb | gap | R4A-33 |
| U016 | GOL 5-905 | covered | NY:GOL-5-905 |
| U017 | NYC Admin Code 20-699.21 (FARE Act) | partial | R4A-01 |
| U018 | RPL 232-c | covered | NY:RPL-232-c |
| U019 | RPL 232-a | covered | NY:RPL-232-a |
| U020 | RPL 226-c | covered | NY:RPL-226-c(1)(a) NY:RPL-226-c(2) |
| U021 | RPL 229 | covered | NY:RPL-229 |
| U022 | RPL 227-e | covered | NY:RPL-227-e |
| U023 | Holy Props. v Kenneth Cole Prods., 87 NY2d 130 (1995) | covered | NY:RPL-227-e (applies by the date the action is commenced, so the Holy Properties no-mitigation rule no longer governs a suit brought after 2019-06-14) |
| U024 | 14 E. 4th St. Unit 509 LLC v Toporek, 203 AD3d 17 (1st Dept 2022) | covered | NY:CASE-Toporek-forfeiture-scope |
| U025 | Riverside Research Inst. v KMGA, 68 NY2d 689 (1986) | partial | R4A-09 |
| U026 | 172 Van Duzer Realty v Globe Alumni, 24 NY3d 528 (2014) | covered | NY:ADJ-lease-break-charge NY:RPL-227-e-waiver (JMD Holding states the same penalty test) |
| U027 | Truck Rent-A-Center v Puritan Farms 2nd, 41 NY2d 420 (1977) | covered | NY:ADJ-lease-break-charge |
| U028 | RPL 226-b(1) | covered | NY:RPL-226-b(1) |
| U029 | RPL 226-b(2) | covered | NY:RPL-226-b(2) |
| U030 | RPL 227 | covered | NY:RPL-227 |
| U031 | RPL 227-a | covered | NY:RPL-227-a(2) |
| U032 | RPL 227-c | covered | NY:RPL-227-c(2) |
| U033 | RPL 236 | covered | NY:RPL-236 |
| U034 | RPL 236-a | covered | NY:RPL-236-a |
| U035 | RPL 236-a (liability and notice) | covered | NY:RPL-236-a |
| U036 | 50 USC 3955 | covered | US:50USC3955(e)(1)-prorate US:50USC3955(e)(1)-no-etf |
| U037 | NY Military Law 310 | covered | NY:MIL-310(2) |
| U038 | RPAPL 1305 | gap | R4A-22 |
| U039 | Protecting Tenants at Foreclosure Act (12 USC 5220 note) | gap | R4A-22 |
| U040 | GOL 7-105(1)-(2) | covered | NY:GOL-7-105(1) NY:GOL-7-105(2)-transfer-effect |
| U041 | GOL 7-108(2) | covered | NY:GOL-7-108(2)(a) NY:GOL-7-108(2)(c) |
| U042 | RPL 223 | covered | NY:RPL-223 |
| U043 | RPL 440 / 440-a | covered | NY:RPL-440(1)-rent-collection |
| U044 | RPL 442-d | covered | NY:RPL-442-d-442-e-unlicensed |
| U045 | BCL 1312 | covered | NY:BCL-1312(a)-foreign-authority |
| U046 | LLC Law 808 | covered | NY:LLC-808(a)-foreign-authority |
| U047 | MDL 325(2) | covered | NY:MDL-325(2) |
| U048 | NYC Admin Code 27-2107(b) | covered | NYC:ADC-27-2107(b)-rent-stay |
| U049 | MDL 302(1)(b) | covered | NY:MDL-302(1)(b) |
| U050 | MDL 301 | covered | NY:MDL-301(1) |
| U051 | MDL 302-a | covered | NY:MDL-302-a(3) |
| U052 | RPAPL 778 | covered | NY:RPAPL-776-778-administrator |
| U053 | CPLR 6401 | covered | NY:CPLR-6401-foreclosure-receiver |
| U054 | Heintz v Jenkins, 514 US 291 (1995) | covered | US:15USC1692a(6)-regularly-another (any person who regularly collects for another, lawyers included) |
| U055 | 15 USC 1692a(6) | covered | US:15USC1692a(6)-regularly-another US:15USC1692a(6)(F)(iii) |
| U056 | Romea v Heiberger, 163 F3d 111 (2d Cir 1998) | covered | US:CASE-Romea-1998 |
| U057 | GOL 7-103(2-b) | covered | NY:GOL-7-103(2-b) |
| U058 | Paterno v Carroll, 75 AD3d 625 (2d Dept 2010); Gihon v 501 Second St., 103 AD3d 840 (2d Dept 2013) | covered | NY:CASE-Paterno-commingling-forfeiture NY:CASE-Paterno-bank-notice-inference |
| U059 | LeRoy v Sayers, 217 AD2d 63 (1st Dept 1995) | partial | R4A-28 |
| U060 | GOL 7-108(1-a)(b) | covered | NY:GOL-7-108(1-a)(b)-refundable NY:GOL-7-108(1-a)(b)-excluded-costs |
| U061 | GOL 7-108(1-a)(d) | covered | NY:GOL-7-108(1-a)(d)-notice NY:GOL-7-108(1-a)(d)-inspection |
| U062 | GOL 7-108(1-a)(f) | covered | NY:GOL-7-108(1-a)(f) |
| U063 | RPL 238-a(2) | covered | NY:RPL-238-a(2) |
| U064 | RPL 238-a(2-a); GOL 5-328(3)(b) (L.2025 c.431) | covered | NY:RPL-238-a(2-a) NY:GOL-5-328(3)(b) |
| U065 | RPL 235-g | covered | NY:RPL-235-g |
| U066 | RPL 234 | covered | NY:RPL-234 |
| U067 | Graham Ct. Owner's Corp. v Taylor, 24 NY3d 742 (2015) | partial | R4A-29 |
| U068 | RPL 234-a | covered | NY:RPL-234-a |
| U069 | RPL 235-i | covered | NY:RPL-235-i |
| U070 | RPL 235-b | covered | NY:RPL-235-b |
| U071 | RPL 235-a | covered | NY:RPL-235-a |
| U072 | NYC Admin Code 27-2013 | covered | NYC:HMC-27-2013(b)(2) NYC:PAINT-wear-and-tear |
| U073 | NYC Admin Code 27-2056.8 | covered | NYC:HMC-27-2056.8-lead-turnover |
| U074 | NYC Admin Code 27-2017.5 | covered | NYC:HMC-27-2017.5-turnover |
| U075 | 24 CFR 982.313 | covered | US:24CFR982.313(c) US:24CFR982.313(d) |
| U076 | 24 CFR 982.311(b) | covered | US:24CFR982.311(d)(1) |
| U077 | 68 RCNY 10-14 (CityFHEPS) | covered | NYC:RCNY68-10-14(c) |
| U078 | 68 RCNY 10-14(e) (CityFHEPS move-out notice) | covered | NYC:RCNY68-10-14(e) |
| U079 | HRA W-147N security voucher | covered | NYC:HRA-voucher-claim-window NYC:HRA-voucher-proof |
| U080 | GOL 7-108(1-a)(e) | covered | NY:GOL-7-108(1-a)(e) NY:GOL-7-108(1-a)(e)-forfeiture |
| U081 | General Construction Law 25-a | covered | NY:GCN-25-a(1) |
| U082 | General Construction Law 20 | covered | NY:GCN-20 |
| U083 | State Technology Law 305 (ESRA) | covered | NY:STT-305(3) |
| U084 | Levine v Xu-Kehrli, 2026 NY Slip Op 50528(U) (App Term 1st Dept) | covered | NY:CASE-Levine-counterclaim |
| U085 | GOL 7-108(1-a)(g) | covered | NY:GOL-7-108(1-a)(g) |
| U086 | CPLR 214(2) | gap | R4A-05 |
| U087 | Gaidon v Guardian Life, 96 NY2d 201 (2001) | gap | R4A-05 |
| U088 | GOL 7-109 | deferred | NY:GOL-7-109 (deferred as not a manager's decision; agreed) |
| U089 | CCA 1801 | gap | R4A-27 |
| U090 | CCA 1812 | gap | R4A-26 |
| U091 | CCA 1809 | covered | NY:CCA-1809(1) |
| U092 | CCA 1803-A | covered | NY:CCA-1803-A(b) |
| U093 | CCA 1809-A | covered | NY:CCA-1803-A(b) (five-per-month certification) |
| U094 | CPLR 3215(g)(3) | covered | NY:CPLR-3215(g)(3) |
| U095 | CPLR 3215(j) | gap | R4A-13 |
| U096 | CPLR 3016(j) | covered | NY:ADJ-lease-balance-not-consumer-credit NY:S9760-pleading-service (no current application to a lease balance) |
| U097 | CPLR 3015(e) | covered | NY:CPLR-3015(e)-licence-pleading |
| U098 | 50 USC 3931 | covered | US:50USC3931(b)(1) |
| U099 | NY Military Law 303(3) | gap | R4A-34 |
| U100 | GOL 5-701(a)(2) | gap | R4A-17 |
| U101 | CCA 1810 / 1810-A | no-decision | clerk's discretion over repeat claims; changes no manager decision |
| U102 | CPLR 213(2) | covered | NY:CPLR-213(2) |
| U103 | CPLR 214-i | covered | NY:CPLR-214-i |
| U104 | CPLR 105(f) | covered | NY:ADJ-lease-balance-not-consumer-credit |
| U105 | DCWP SHIELD NOA (2026) statement on CPLR 214-i | covered | NY:ADJ-lease-balance-not-consumer-credit (agrees with DCWP's reading) |
| U106 | CPLR 203(a) | no-decision | accrual rule is implicit in every limitation rule; no separate decision |
| U107 | GOL 17-101 | gap | R4A-04 |
| U108 | CPLR 210(b) | gap | R4A-03 R4A-04 |
| U109 | CPLR 210(a) | gap | R4A-03 |
| U110 | 50 USC 3936 | gap | R4A-04 |
| U111 | NY Military Law 308 | gap | R4A-04 |
| U112 | 11 USC 108(c) | gap | R4A-04 |
| U113 | CPLR 5001 | covered | NY:CPLR-5001(a)-(b) |
| U114 | CPLR 5004 | covered | NY:CPLR-5004(a)-consumer-2pct |
| U115 | 50 USC 3937 | gap | R4A-08 |
| U116 | NY Military Law 323-a | gap | R4A-08 |
| U117 | 15 USC 1692g | covered | US:15USC1692g(a) |
| U118 | 12 CFR 1006.34 | covered | US:12CFR1006.34(a)(1) US:12CFR1006.34(c) |
| U119 | 12 CFR 1006.30(a) | covered | US:12CFR1006.30(a) |
| U120 | 15 USC 1692c / 1692d / 1692e / 1692f | covered | US:15USC1692c(a) US:15USC1692d US:15USC1692e(2)(A) US:15USC1692f(1) |
| U121 | 15 USC 1692i | covered | US:15USC1692i(a) |
| U122 | 15 USC 1692k | covered | US:15USC1692k(a) |
| U123 | Avila v Riexinger & Assocs., 817 F3d 72 (2d Cir 2016) | gap | R4A-12 |
| U124 | GBL 601 | partial | NY:ADJ-lease-balance-not-consumer-credit (the state statute does not reach a lease balance; my universe line overstated it) and R4A-10 (the city rule imports its conduct) |
| U125 | GBL 601-a | gap | R4A-30 |
| U126 | GBL 602 | deferred | NY:GBL-602 |
| U127 | 23 NYCRR 1.1 (DFS debt collection regulation) | covered | NY:23NYCRR-1.1(d)-not-lease |
| U128 | NYC Admin Code 20-489, 20-490 | covered | NYC:ADC-20-489(a) NYC:ADC-20-490 NYC:DCA-owner-own-staff NYC:DCA-manager-for-owners |
| U129 | NYC Admin Code 20-493.1, 20-493.2 | covered | NYC:ADC-20-493.1(b) NYC:ADC-20-493.2(a) |
| U130 | 6 RCNY 2-190 | covered | NYC:RCNY6-2-190(b) |
| U131 | 6 RCNY 2-191 | covered | NYC:RCNY6-2-191(a) |
| U132 | 6 RCNY 2-192 | gap | R4A-21 |
| U133 | 6 RCNY 2-193 | gap | R4A-21 |
| U134 | 6 RCNY 5-76 (definition in force until 2026-12-31) | covered | NYC:RCNY6-5-76-debt-collector |
| U135 | 6 RCNY 5-77 (in force until 2026-12-31) | partial | NYC:RCNY6-5-77(e)(1) NYC:RCNY6-5-77(b)(1)(iv) and R4A-10 |
| U136 | SHIELD Rule (6 RCNY 5-76/5-77 as amended, adopted 2026-02-26, effective 2027-01-01) | partial | NYC:SHIELD-5-76-debt-collector NYC:SHIELD-5-77(f)(1) and R4A-11 |
| U137 | SHIELD Rule: debt collection procedures definition | covered | NYC:SHIELD-5-76-procedures |
| U138 | SHIELD effective-date notice (City Record 2026-07-22) | covered | NYC:SHIELD-effective-date NYC:SHIELD-operative-date |
| U139 | NYC Admin Code 20-700 | covered | NYC:CPL-20-700 |
| U140 | GBL 604-aa, 604-bb (coerced debt, eff. 2026-06-17) | gap | R4A-02 |
| U141 | GBL 604-aa(3)-(4) definitions | gap | R4A-02 |
| U142 | L.2019 c.36 Part M, section 29 (effective dates) | covered | NY:L2019-c36-PartM-s29 |
| U143 | Abandoned Property Law 1315(2) | covered | NY:ABP-1315(2) |
| U144 | OSC property-type table (TR04 / MS11; AC06 is the banks' code) | partial | NY:OSC-MS11-refunds-due and R4A-31 |
| U145 | Abandoned Property Law 1422 | covered | NY:ABP-1422 |
| U146 | 11 USC 362(a) | covered | US:11USC362(a)(6) US:11USC362(a)(7) |
| U147 | 11 USC 541 / 542 | covered | US:11USC542-refund-payee |
| U148 | 11 USC 553 | covered | US:11USC362(a)(7)-deposit-is-setoff |
| U149 | 11 USC 524(a) | covered | US:11USC524(a)(2) |
| U150 | 11 USC 502(b)(6) | gap | R4A-07 |
| U151 | 11 USC 1301(a) | gap | R4A-06 |
| U152 | 11 USC 365(d)(1) | gap | R4A-24 |
| U153 | SCPA 1301 (small estate) | gap | R4A-03 |
| U154 | SCPA 1310(1)(a) (debts payable without administration) | gap | R4A-03 |
| U155 | SCPA 1305 | gap | R4A-03 |
| U156 | SCPA 1802 | gap | R4A-03 |
| U157 | EPTL 11-1.1 | partial | NY:COMMONLAW-owner-death-agency (owner's death only) and R4A-03 (tenant's death) |
| U158 | 50 USC 3951 | deferred | US:50USC3951(a)(1)(B) (deferred; agreed: eviction protection decides nothing once the tenant has left) |
| U159 | SCRA rent threshold 2026 (91 FR / FR 2026-04689) | deferred | US:FR-2026-04689 |
| U160 | 42 USC 3604(f)(3)(A) | covered | US:42USC3604(f)(3)(A) |
| U161 | 24 CFR 100.203 | covered | US:42USC3604(f)(3)(A) |
| U162 | 24 CFR 100.65(b)(1) | gap | R4A-18 |
| U163 | NYC Admin Code 8-107(5)(a)(1)(b) | gap | R4A-18 |
| U164 | NYC Admin Code 8-102 'lawful source of income' | gap | R4A-18 |
| U165 | Executive Law 296(5)(a)(2) | gap | R4A-18 |
| U166 | RPL 227-d | gap | R4A-18 |
| U167 | IRS Pub. 527 (security deposits) | gap | R4A-25 |
| U168 | 26 USC 6049(a)(2) | gap | R4A-19 |
| U169 | 26 USC 6050P(c) | gap | R4A-25 |
| U170 | 15 USC 1681s-2(a) | covered | US:15USC1681s-2(a)(1)(A) US:15USC1681s-2(a)(3) US:15USC1681s-2(a)(5)(A) |
| U171 | 12 CFR 1022.42 / 1022.43 | covered | US:12CFR1022.42(a) US:12CFR1022.43(a) |
| U172 | GBL 899-bb | gap | R4A-32 |
| U173 | NYC Admin Code 26-3002(c) (Tenant Data Privacy Act) | gap | R4A-20 |
| U174 | S947 / A3121 (2025-26): RPL 235-g amendment, passed Senate 2026-03-18 and Assembly 2026-05-13, not yet delivered | gap | R4A-23 |
| U175 | S947 actions | gap | R4A-23 |
| U176 | S9760 / A10182-A Consumer Debt Uniformity Act (passed both houses June 2026) | covered | NY:CPLR-214-i-consumer-debt-S9760 NY:S9760-default-judgment |

## New versus earlier rounds

Read only after the findings above were saved. Rounds 1-3 (INDEPENDENT_REVIEW_1-3 and their dispositions) raised none
of R4A-01 to R4A-34. Specific overlaps checked:
- R4A-10 narrows R1-15: round 1 moved every GBL 601 rule to the deferred list as deciding nothing. That is right for
  the state statute, but for NYC units it is over-corrected, because the city rule imports GBL 601's conduct.
- R4A-13 is separate from R2-11 (the small-claims exception to 3215(g)(3)); 3215(j) was not raised.
- R4A-03 is separate from R1-08 (RPL 236 silence); the payee and estate-claim rules were not raised.
- R4A-17: guarantors appear earlier only as defendants for the 2% judgment rate (R1-01).
- R4A-27 is separate from R1-14 (the landlord's small and commercial claims).
A parallel reviewer's file (INDEPENDENT_REVIEW_4B.md) exists in the folder; I did not read it, so this review stays
independent of it.

## Method

1. Blind phase. Read only APERTURE.md and STAGE_A.md 'Chain' and 'Discovery method'. Walked tables of contents on
   nysenate.gov (RPL arts. 6-A, 7, 12-A; GOL art. 5 title 9, art. 7 title 1; RPAPL arts. 7, 7-A; CPLR arts. 2, 50;
   CCA arts. 18, 18-A; SCPA arts. 13, 18; ABP arts. 13, 14; Military Law art. 13; GBL arts. 25, 29-H, 29-HHH, 39-F) and
   the American Legal bulk XML for the NYC Admin Code (titles 8, 20, 26, 27) and RCNY (titles 6, 28, 68). Federal text
   from uscode.house.gov and eCFR; IRS Pub. 527; controlling decisions from CourtListener and nycourts.gov; bill actions
   from assembly.state.ny.us; DCWP rule status from the City Record and rules.cityofnewyork.us. Existing saved sources
   were used where present, never refetched; 67 new sources were saved mechanically with prefix REVIEW4A_ (via
   web_extract, `review/ir4a_fetch.py` and `review/ir4a_aml.py`). Every universe quote is cut from a saved file by
   anchors (`review/ir4a_lib.py`, `review/ir4a_build_universe.py`), never retyped. The universe was saved before any rule
   file, the walk or a review file was opened.
2. Diff phase. Dumped all 604 rules; matched each universe item by source file, provision and keyword, then read the
   candidate rules in full (`review/show.py`). An item is 'partial' when the rule lacks a branch, exception, date or
   consequence. Over-scope was tested on every cited in-scope rule against the aperture.
3. Corrections to my own universe made in the diff phase, and why: U124 (GBL 601) overstated the state statute, which
   needs an extension of credit; the correct city-rule route is R4A-10. U144 first named Comptroller code AC06, which
   the table places under banks; corrected to MS11 or TR04 after re-reading the table.
4. Checked and not included, because they are not law in force or passed: NY bills on deposit return within 30 days
   (S4856/A2652, S4087, A4355, A8078), deposit installments (S3164), deposit alternatives (S6397/A1431) and rent
   reporting (A2729-A/S10477-A), all in committee; NYC Int. 249-2026 (documentation of deposit deductions), in
   committee. The FTC fee rule (16 CFR 464) covers short-term lodging only. Neither CFPB nor FTC has adopted a 2026-2027
   rule that reaches a residential landlord's settlement.
5. Tools: `python3 review/ir4a_build_universe.py`, `python3 review/ir4a_build_findings.py`, `python3 review/ir4a_render.py`,
   `python3 review/ir4a_verify.py` (every quote verbatim in its source, whitespace-normalized; every rule id exists;
   self-test with a planted bad quote and a planted bad id).
