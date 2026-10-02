# Batch 2 review (reviewer q2): NY procedure and courts

Report only. Decisions: `register/work/decisions_2.jsonl` (560 lines). Builders: `register/work/q2_c01.py`-`q2_c24.py` (idempotent; each rewrites its own rows), helpers `q2_lib.py`, checks `q2_verify.py`. `python3 register/work/check_decisions.py 2` passes: 560/560 decided, 0 errors.

## Counts

| decision | sections |
|---|---|
| stated | 2 |
| partial | 23 |
| new_rule | 193 |
| no_decision | 341 |
| excluded_regime | 1 |
| total | 560 |

Proposed rules: 217 (13 critical, 79 major, 125 minor). All ids use the `NY:` prefix; none collides with an existing rule or with another batch's decisions file at the time of the check.

| instrument | stated | partial | new_rule | no_decision | excluded_regime |
|---|---|---|---|---|---|
| NY:22NYCRR | 0 | 1 | 18 | 83 | 0 |
| NY:CCA | 1 | 5 | 63 | 31 | 0 |
| NY:CPLR | 0 | 14 | 103 | 217 | 1 |
| NY:JUD | 1 | 3 | 9 | 10 | 0 |

## Where the line was drawn

Every section was decided from its text. For court rules and the CPLR the test applied was the brief's: a section
counts when it changes how a landlord sues a former tenant for a balance, or a tenant sues over the deposit, in NYC
Civil Court (regular, small claims, commercial claims) or Supreme Court. In practice:

- Rules: whether, where, when, by whom and against whom a claim can be brought (jurisdiction, long-arm, venue,
  capacity, limitations, accrual, interposition, borrowing, tolling); what must be done to commence and serve;
  what makes a default judgment available, and how long it stays open to vacatur; how the charges are proved (business
  records, paid-invoice presumptions, the dead man's statute, agent admissions); every amount a judgment adds
  (interest, costs, disbursements, fees); enforcement against a natural person (execution, levy, subpoenas,
  turnover, installment orders, attachment, liens, exemptions); settlement devices (stipulations, tender, offers,
  confession, interpleader, attorney's liens); and the landlord's duties when it is itself the garnishee of a former
  tenant's refund.
- No decision: in-suit calendar, conference, discovery, motion, trial and papers mechanics with no forfeiture;
  sheriff and clerk internal duties; appellate practice; matrimonial, malpractice, personal injury, foreclosure,
  tax review, public-entity and support rules; consumer-credit-only rules (a lease balance is not consumer credit:
  `NY:ADJ-lease-balance-not-consumer-credit`). Where an in-suit rule carries a deadline whose miss ends the claim
  (22 NYCRR 202.48/208.33 60-day submission, CPLR 306-b and CCA 411 120-day service, CPLR 3216, 208.14 one-year
  restoration, CPLR 8502), it was treated as a rule.
- Parallel sections (small claims and commercial claims counterparts, Supreme Court and Civil Court counterparts) each
  carry their own rule quoting their own text, cross-referenced, so each fact has one owner section.

Severity convention: critical = decides whether a claim exists or survives, its deadline, or who is paid (limitations,
accrual, interposition, borrowing, long-arm reach, service validity, small-claims preclusion, landlord as garnishee,
judgment interest); major = an operator step or a recoverable amount in a judgment; minor = court-mechanics detail
with a small cost or a narrow branch.

## Adjudications made in the proposed rules (read these first)

- A lease clause shortening the tenant's time to sue over the deposit is void (GOL 7-108 anti-waiver, quoted as
  construction), while other agreed shorter periods stand if reasonable: `NY:CPLR-201-agreed-shorter-period`.
- Borrowing statute: an economic-loss claim accrues where the plaintiff resides; an out-of-state owner entity, or a
  tenant who moved away before the 14 days ended, gets the shorter of New York's and its home state's period:
  `NY:CPLR-202-borrowing` (Global Fin. Corp. v Triarc Corp., 93 NY2d 525; Portfolio Recovery v King, 14 NY3d 410).
- Small-claims and commercial-claims judgments have no issue preclusion but full transactional claim preclusion, so an
  owner cannot split a balance between small claims and a later action: `NY:CCA-1808-preclusion`,
  `NY:CCA-1808-A-preclusion` (Simmons v Trans Express Inc., 37 NY3d 107 [2021], on a certified question).
- The vacated unit is not the former tenant's "dwelling place or usual place of abode", so substituted or
  nail-and-mail service there is void: `NY:CPLR-308-natural-person`; defaults on non-personal service stay open up to
  five years (`NY:CPLR-317-defend-after-default`).
- A former tenant who moved out of state can be sued in NYC for the balance (use and possession of NYC real property):
  `NY:CPLR-302-long-arm`, `NY:CCA-404-long-arm`.
- When a creditor of the former tenant levies on, restrains or attaches the refund, the landlord pays the officer as
  directed and is discharged; paying the tenant instead is contempt: `NY:CPLR-5209-landlord-as-garnishee`,
  `NY:CPLR-5251-disobedience-contempt`, `NY:CPLR-6204-landlord-garnishee-attachment`, `NY:CPLR-6219-garnishee-statement`.
- A judgment for a deposit the landlord held in trust and willfully withheld or commingled is enforceable by contempt as
  well as execution: `NY:CPLR-5105-fiduciary-contempt`.
- Handoff and managers may not take referral fees or fee shares from collection lawyers, solicit retainers for them, or
  run suits in a lawyer's name; an owner may transfer a balance in payment of services or an existing debt without
  champerty: `NY:JUD-491-no-fee-sharing`, `NY:JUD-479-no-solicitation`, `NY:JUD-476-lending-name`,
  `NY:JUD-490-champerty-exception`.
- A settlement with a represented tenant is paid subject to the attorney's lien: `NY:JUD-475-attorney-lien`,
  `NY:JUD-475-a-notice-of-lien`.
- A tenant deposit held by a landlord's attorney cannot sit in IOLA; GOL 7-103 controls: `NY:JUD-497-attorney-escrow-deposit`.

## Correctness findings on existing rules

1. `NY:CPLR-5205-5231-enforcement-limits` states the bank exemption as a fixed "$2,500". CPLR 5253 adjusts the CPLR 5205
   and 5206 dollar exemptions every three years: "Beginning on April first, two thousand twelve, and at each three-year
   interval ending on April first thereafter, the dollar amount of the exemption provided in sections fifty-two hundred
   five and fifty-two hundred six of this article and sections two hundred eighty-two and two hundred eighty-three of
   the debtor and creditor law shall be adjusted" (register/texts/NY_CPLR/5253.txt). The rule should state the
   statutory base as adjusted by the published amount in force when the restraint or execution is served
   (proposed amendment `NY:CPLR-5253-exemption-adjustment`). Severity: major (amount in the pursue estimate).
2. `NY:ADJ-tenant-deposit-claim-limitations` and `NY:CPLR-213(2)` state New York's periods only. CPLR 202: "An action
   based upon a cause of action accruing without the state cannot be commenced after the expiration of the time limited
   by the laws of either the state or the place without the state where the cause of action accrued, except that where
   the cause of action accrued in favor of a resident of the state the time limited by the laws of the state shall
   apply" (register/texts/NY_CPLR/202.txt). A non-resident plaintiff (out-of-state owner entity; tenant resident
   elsewhere at accrual) can be held to a shorter foreign period. Both rules should point to `NY:CPLR-202-borrowing`.
   Severity: critical.
3. `NY:CPLR-321-JUD-495-appearance` is conditioned only on "The owner sues a former tenant". When the tenant sues a
   corporate owner in small claims, CCA 1809(2) applies: "A corporation may appear in the defense of any small claim
   action brought pursuant to this article by an attorney as well as by any authorized officer, director or employee
   of the corporation" (register/texts/NY_CCA/1809.txt). The defense branch (the corporation's own officer or employee,
   never an outside manager or Handoff) is missing. CCA 1809 is not in this batch; flagged for its owner. The housing
   part branch is proposed here (`NY:CCA-110-housing-part-appearance`). Severity: major.
4. `NY:CCA-1801-A(a)-eligibility` is correct against the statute ("principal office in the state of New York"); the
   court rule 22 NYCRR 208.41-a(a)(1) still says "principal office in the City of New York". The statute prevails;
   recorded in `NY:22NYCRR-208.41-a-commercial-claims-procedure` with a construction quote. No change to the existing rule.

## Sources an applier must save before adopting

The quotes of every proposed rule are from register texts and pass the verbatim check. Three effects also cite cases
that are not saved under sources/ (web search result pages only, no saved text): Simmons v Trans Express Inc., 37 NY3d
107 (2021) (`NY:CCA-1808-preclusion`, `NY:CCA-1808-A-preclusion`); Global Fin. Corp. v Triarc Corp., 93 NY2d 525 (1999)
and Portfolio Recovery Assoc., LLC v King, 14 NY3d 410 (2010) (`NY:CPLR-202-borrowing`). Save them and add construction
quotes when applying; do not carry the case statements on this report's word. Two other adjudications rest on statutory
text only and name no case: `NY:CPLR-3213-summary-judgment-in-lieu` (a lease is not an instrument for the payment of
money only) and `NY:CPLR-4545-collateral-source` (reaches a property-damage claim however pleaded); a B reviewer should
check each against controlling decisions.

## Seams with other batches

Proposed rules here reference sections outside this batch that I did not decide: CPLR 3215 (default judgment; only
(g)(3) and (j) are stated), CPLR 503 and CCA 301 (venue), CCA 1809(2) (above), CPLR 5222 and 5231 (stated in the
enforcement-limits rule). No proposed id here is used by another batch's decisions file at the time of the check.


## Proposed rules, most severe first

| id | severity | section | decision basis (one line) |
|---|---|---|---|
| `NY:CCA-1808-A-preclusion` | critical | NY:CCA 1808-A | The commercial-claims counterpart of 1808: an entity owner's commercial-claims judgment has no issue preclusion, carries claim preclusion, and reduces a later judgment on the same facts. |
| `NY:CCA-1808-preclusion` | critical | NY:CCA 1808 | Fixes what a small-claims judgment between landlord and tenant does to later suits: no issue preclusion, claim preclusion as usual, and a later judgment on the same facts reduced by the small-claims award. |
| `NY:CCA-400-commencement` | critical | NY:CCA 400 | An NYC Civil Court action is commenced by filing the summons and complaint with the fee (the limitations interposition date) and jurisdiction is acquired by service. |
| `NY:CCA-404-long-arm` | critical | NY:CCA 404 | Gives the Civil Court personal jurisdiction over a non-resident of the city on a claim arising from its possession or use of real property in the city, served anywhere. |
| `NY:CPLR-201-agreed-shorter-period` | critical | NY:CPLR 201 | The limitation rules state the periods. |
| `NY:CPLR-202-borrowing` | critical | NY:CPLR 202 | The borrowing statute: where a claim over the tenancy accrues outside New York in favor of a non-resident (an owner entity based out of state, a tenant who moved away before its claim accrued), the shorter of New York's and that place's period applies. |
| `NY:CPLR-203(d)-counterclaim-offset` | critical | NY:CPLR 203 | Fixes when a limitation period starts and stops (accrual to interposition) for the landlord's balance suit and the tenant's deposit suit, and saves a time-barred counterclaim from the same lease as a setoff. |
| `NY:CPLR-203-accrual-interposition` | critical | NY:CPLR 203 | Fixes when a limitation period starts and stops (accrual to interposition) for the landlord's balance suit and the tenant's deposit suit, and saves a time-barred counterclaim from the same lease as a setoff. |
| `NY:CPLR-302-long-arm` | critical | NY:CPLR 302 | New York courts have personal jurisdiction over a non-domiciliary on a claim arising from its owning, using or possessing real property in New York, or transacting business here. |
| `NY:CPLR-304-commencement` | critical | NY:CPLR 304 | In Supreme Court an action is commenced by filing the summons and complaint (or summons with notice) with the county clerk and paying the index fee. |
| `NY:CPLR-308-natural-person` | critical | NY:CPLR 308 | The methods of serving a natural-person former tenant (personal delivery. |
| `NY:CPLR-5003-judgment-interest` | critical | NY:CPLR 5003 | The 2% rule names post-judgment interest but no rule states that a money judgment bears interest from entry (or a docketed money order from docketing). |
| `NY:CPLR-5209-landlord-as-garnishee` | critical | NY:CPLR 5209 | When a creditor of the former tenant levies on or restrains the deposit refund the landlord owes the tenant, paying the sheriff or creditor under the execution or order discharges the landlord to that extent. |
| `NY:22NYCRR-202.27-calendar-default` | major | NY:22 NYCRR 202.27 | Supreme Court default at a calendar call or conference: the absent tenant can be defaulted and the absent landlord's action dismissed. |
| `NY:22NYCRR-202.46-inquest-proof` | major | NY:22 NYCRR 202.46 | Sets how the landlord proves damages at a Supreme Court inquest after the tenant defaults (affidavits or sworn written statements). |
| `NY:22NYCRR-202.48-judgment-submission` | major | NY:22 NYCRR 202.48 | A proposed judgment the court directs to be settled or submitted must be submitted within 60 days or the action is deemed abandoned. |
| `NY:22NYCRR-202.5(e)-redaction` | major | NY:22 NYCRR 202.5 | Papers filed in Supreme Court must omit the tenant's taxpayer or social security number, birth date (except year), minors' names and account numbers (except last four). |
| `NY:22NYCRR-208.14-calendar-default` | major | NY:22 NYCRR 208.14 | NYC Civil Court calendar default, dismissal and one-year restoration window. |
| `NY:22NYCRR-208.32-inquest-proof` | major | NY:22 NYCRR 208.32 | Sets how the landlord proves damages at an NYC Civil Court inquest after the tenant defaults (affidavits permitted as of right). |
| `NY:22NYCRR-208.33-judgment-submission` | major | NY:22 NYCRR 208.33 | In NYC Civil Court a proposed judgment directed to be settled or submitted must be submitted within 60 days or the action is deemed abandoned. |
| `NY:22NYCRR-208.37-execution-precondition` | major | NY:22 NYCRR 208.37 | A precondition to enforcing an NYC Civil Court judgment: no execution until the judgment is served on the tenant's attorney, or on a pro se tenant who defaulted in answering personally or by certified mail. |
| `NY:22NYCRR-208.4(b)-redaction` | major | NY:22 NYCRR 208.4 | Papers the landlord files in NYC Civil Court must omit the tenant's taxpayer or social security number, birth date (except year) and account numbers (except last four). |
| `NY:22NYCRR-208.41-a-commercial-claims-procedure` | major | NY:22 NYCRR 208.41-a | The eligibility and consumer demand-letter rules are stated. |
| `NY:22NYCRR-208.41-small-claims-procedure` | major | NY:22 NYCRR 208.41 | The NYC small-claims procedure that governs a tenant's deposit suit and an individual owner's balance suit: what must be produced at the hearing, the one-hour default rule, counterclaims, jury demand costs, four-month service dismissal and binding arbitration. |
| `NY:22NYCRR-208.4a-efiling` | major | NY:22 NYCRR 208.4a | An action e-filed in NYC Civil Court is filed (and so interposed for limitations) on NYSCEF receipt with the fee. |
| `NY:CCA-1402-default-on-endorsed-summons` | major | NY:CCA 1402 | The 3215 rules state the default mailing and limitations affidavit. |
| `NY:CCA-1403-confession-civil-court` | major | NY:CCA 1403 | Makes a former tenant's confession of judgment (CPLR 3218) enterable and enforceable in NYC Civil Court for a balance within its jurisdiction. |
| `NY:CCA-1504-civil-court-execution` | major | NY:CCA 1504 | An NYC Civil Court execution reaches only the tenant's personal property, goes to a city marshal or the city sheriff, and may be levied anywhere in the city without docketing. |
| `NY:CCA-1507-no-levy-24h` | major | NY:CCA 1507 | Bars a levy on an evicted tenant's property for 24 hours after a nonpayment dispossess. |
| `NY:CCA-1803-small-claims-notice-counterclaim` | major | NY:CCA 1803 | Sets how a tenant's small-claims deposit suit reaches the landlord (mail to the rent-payment address, presumed received after 21 days) and the landlord's counterclaim window. |
| `NY:CCA-1804-A-commercial-claims-proof` | major | NY:CCA 1804-A | In the commercial claims part an itemized paid invoice, or two itemized estimates, is prima facie proof of the reasonable value and necessity of repairs. |
| `NY:CCA-1804-small-claims-proof` | major | NY:CCA 1804 | In small claims an itemized paid invoice, or two itemized estimates, is prima facie proof of the reasonable value and necessity of repairs. |
| `NY:CCA-1805-small-claims-remedies` | major | NY:CCA 1805 | Small-claims remedies: conditional judgments, pre-judgment examination and restraint of the defendant, transfer, and a bar on counterclaims beyond the small-claims limit. |
| `NY:CCA-1807-A-commercial-default` | major | NY:CCA 1807-A | In the commercial claims part the clerk mails notice of a default judgment and the defaulting tenant may seek vacatur in writing with a reasonable excuse under CPLR 5015. |
| `NY:CCA-1813-A-duty-to-pay` | major | NY:CCA 1813-A | The commercial-claims counterpart of 1813: a business judgment debtor in the commercial claims part must pay in any name it uses. |
| `NY:CCA-1813-duty-to-pay` | major | NY:CCA 1813 | A landlord business sued in small claims must pay the judgment in its true name or any business name. |
| `NY:CCA-1901-costs-amount` | major | NY:CCA 1901 | Fixes the costs a prevailing party recovers in an NYC Civil Court action (not small claims or summary proceedings): $50/$100/$150 stages, or $20/$35/$60 when the money judgment is $6,000 or less. |
| `NY:CCA-1906-A-summary-costs` | major | NY:CCA 1906-A | Fixes the only costs a landlord recovers in an NYC summary proceeding against the tenant. |
| `NY:CCA-1908-disbursements` | major | NY:CCA 1908 | Lists the disbursements a prevailing party (including a self-represented one) recovers in NYC Civil Court: court, sheriff and marshal fees, private process-server cost, witness fees, certified copies, transcript and execution fees. |
| `NY:CCA-1911-clerk-fees` | major | NY:CCA 1911 | Sets the NYC Civil Court fees the landlord pays to sue and enforce (summons or first paper $45, jury $70, satisfaction $6, notice of petition $45) and that the $95 consumer-credit surcharge does not apply to a lease balance. |
| `NY:CCA-202-money-limit` | major | NY:CCA 202 | Caps the NYC Civil Court's money jurisdiction at $50,000. |
| `NY:CCA-402-answer-time` | major | NY:CCA 402 | Fixes the tenant's time to answer a Civil Court summons (20 days after personal delivery in the city. |
| `NY:CCA-403-service-within-city` | major | NY:CCA 403 | A Civil Court summons is served as in Supreme Court (including mail under CPLR 312-a) but only within New York City unless a statute such as CCA 404 authorizes more. |
| `NY:CCA-411-120-days` | major | NY:CCA 411 | The summons and complaint must be served within 120 days after filing or the action is dismissed without prejudice unless the court extends. |
| `NY:CPLR-1006-interpleader` | major | NY:CPLR 1006 | A landlord facing conflicting claims to a deposit refund (co-tenants, an estate and a relative, a trustee and the tenant) may interplead the claimants, pay the refund into court and be discharged, owing interest only at the Federal Reserve discount rate absent agreement. |
| `NY:CPLR-1201-representation` | major | NY:CPLR 1201 | The parties rule bars a default against an infant or adjudicated incompetent. |
| `NY:CPLR-1206-proceeds-payee` | major | NY:CPLR 1206 | Money an infant, adjudicated incompetent or conservatee former tenant recovers (for example a deposit settlement or judgment) is paid to its guardian, committee or conservator, or as the court orders, not to the person. |
| `NY:CPLR-1207-incapacitated-settlement` | major | NY:CPLR 1207 | A settlement of a claim by an infant, adjudicated incompetent or conservatee (for example a deposit claim of a tenant under guardianship) binds only when the court approves it on the representative's motion or petition. |
| `NY:CPLR-1501-joint-obligors` | major | NY:CPLR 1501 | On a joint lease obligation the landlord may proceed against the co-tenants it has served and take judgment against all named. |
| `NY:CPLR-206-demand-accrual` | major | NY:CPLR 206 | Where a lease makes a sum payable only on the landlord's demand, the period runs from when the landlord could first demand, not from the demand. |
| `NY:CPLR-2103-a-confidential-address` | major | NY:CPLR 2103-A | A court may let a party keep its address confidential for safety, and the address of a domestic-violence program resident is never revealed. |
| `NY:CPLR-2104-stipulations` | major | NY:CPLR 2104 | A settlement with a former tenant in a pending case binds only if in a writing signed by the party or its attorney, made in open court, or so-ordered, and its terms are filed by the defendant with the county clerk. |
| `NY:CPLR-215(7)-retaliation-one-year` | major | NY:CPLR 215 | 215(7) sets a one-year limit on a tenant's RPL 223-b(3) retaliation action, which the retaliation rule does not state. |
| `NY:CPLR-3002-no-election` | major | NY:CPLR 3002 | Suing one co-tenant or the guarantor, or holding an unsatisfied judgment against one, does not bar an action against the others. |
| `NY:CPLR-3019-counterclaims` | major | NY:CPLR 3019 | A defendant may counterclaim any claim against the plaintiff, and counterclaims are permissive. |
| `NY:CPLR-306-b-120-days` | major | NY:CPLR 306-B | In Supreme Court the summons must be served within 120 days after filing or the action is dismissed without prejudice unless extended. |
| `NY:CPLR-312-a-mail-service` | major | NY:CPLR 312-A | Service by mail with acknowledgment: complete only when the tenant returns the signed acknowledgment (within 30 days), answer due 20 days later, and the tenant pays the cost of other service if it does not return it. |
| `NY:CPLR-313-service-outside-state` | major | NY:CPLR 313 | A former tenant domiciled in New York or subject to its long-arm jurisdiction (CPLR 302, for a claim arising from its lease of NYC property) may be served outside the state in the same manner as within. |
| `NY:CPLR-317-defend-after-default` | major | NY:CPLR 317 | A former tenant served other than by personal delivery who defaulted may reopen the judgment within one year after learning of it (at most five years after entry) if it did not receive the summons and has a meritorious defense, with restitution. |
| `NY:CPLR-320-appearance-time` | major | NY:CPLR 320 | In Supreme Court the former tenant must appear within 20 days after personal delivery, or 30 days after service is complete for substituted, affix-and-mail, out-of-state or publication service. |
| `NY:CPLR-3211-dismissal-grounds` | major | NY:CPLR 3211 | Lists the grounds on which the former tenant (or the landlord, when sued) can have a claim dismissed early (limitations, release, payment, lack of capacity, no personal jurisdiction, failure to state a claim) and when each is waived. |
| `NY:CPLR-3218-confession` | major | NY:CPLR 3218 | A former tenant may confess judgment by affidavit for the balance, filed within three years only in the county where the tenant resided, with the consumer-rate statement where it applies. |
| `NY:CPLR-3219-tender` | major | NY:CPLR 3219 | A landlord sued on the lease (for example for the deposit) may deposit a sum with the clerk and tender it. |
| `NY:CPLR-3221-offer-to-compromise` | major | NY:CPLR 3221 | An offer to allow judgment for a stated sum: if accepted within ten days judgment is entered. |
| `NY:CPLR-4518-business-records` | major | NY:CPLR 4518 | The landlord proves the balance and each charge through business records (ledger, move-in record, inspection reports, invoices, the itemized statement, electronic records) made in the regular course of business at or near the time. |
| `NY:CPLR-4533-a-repair-bill-proof` | major | NY:CPLR 4533-A | In any civil action an itemized, receipted repair bill of $2,000 or less, certified by the vendor and served with notice ten days before trial, is prima facie proof of the reasonable value and necessity of the repair. |
| `NY:CPLR-5002-decision-to-judgment` | major | NY:CPLR 5002 | The interest rules state pre-decision interest and the rate. |
| `NY:CPLR-5015-relief-from-judgment` | major | NY:CPLR 5015 | The grounds and deadlines on which a former tenant (or the landlord) can vacate a judgment: excusable default within one year after service with notice of entry, lack of jurisdiction at any time, fraud or misconduct, new evidence, and mass vacatur of improper defaults, with restitution. |
| `NY:CPLR-5020-a-deposit-with-clerk` | major | NY:CPLR 5020-A | A landlord that owes a former tenant a judgment, and whose certified-mail payment to the tenant's last known address came back, may deposit a certified check with the clerk to stop execution charges. |
| `NY:CPLR-5105-fiduciary-contempt` | major | NY:CPLR 5105 | A judgment requiring a trustee or fiduciary to pay money for a willful default may be enforced by contempt as well as by execution. |
| `NY:CPLR-5206-homestead` | major | NY:CPLR 5206 | The enforcement-limits rule covers bank and wage exemptions but not the homestead: a former tenant's owned and occupied home is exempt up to $150,000 of equity in NYC (adjusted under CPLR 5253), which caps recovery from real property. |
| `NY:CPLR-5224-enforcement-subpoenas` | major | NY:CPLR 5224 | The enforcement subpoenas the landlord may serve (deposition, documents, information subpoena by certified mail with 7-day answers), the reasonable-belief certification without which a third-party information subpoena is void, and the one-year bar on re-examining the tenant. |
| `NY:CPLR-5226-installment-order` | major | NY:CPLR 5226 | The court may order a former tenant with income to pay the judgment in installments fixed with regard to its and its dependents' reasonable needs. |
| `NY:CPLR-5230-execution` | major | NY:CPLR 5230 | The enforcement-limits rule covers exemptions. |
| `NY:CPLR-5232-levy` | major | NY:CPLR 5232 | The enforcement-limits rule states the bank exemption. |
| `NY:CPLR-5251-disobedience-contempt` | major | NY:CPLR 5251 | Disobeying an enforcement subpoena, restraining notice or order, or false swearing on an examination, is contempt. |
| `NY:CPLR-5253-exemption-adjustment` | major | NY:CPLR 5253 | The enforcement-limits rule states the exemptions at their statutory amounts. |
| `NY:CPLR-6201-attachment-grounds` | major | NY:CPLR 6201 | Grounds for a pre-judgment order of attachment against a former tenant: it lives outside New York, cannot be served despite diligence, or is hiding or moving assets to defeat a judgment. |
| `NY:CPLR-6204-landlord-garnishee-attachment` | major | NY:CPLR 6204 | When a creditor of the former tenant attaches the refund the landlord owes the tenant, paying the sheriff under the order of attachment discharges the landlord to that extent. |
| `NY:CPLR-6212-attachment-motion` | major | NY:CPLR 6212 | To attach, the landlord must show probable success and that its claim exceeds known counterclaims (for example the deposit), post an undertaking of at least $500, file within ten days, and is liable for all damages and attorney's fees if the attachment was wrongful. |
| `NY:CPLR-8012-poundage` | major | NY:CPLR 8012 | The sheriff takes 5% poundage in NYC on sums collected, and on a settlement after levy is owed poundage on the lesser of the judgment or the settlement. |
| `NY:CPLR-8101-costs-to-prevailing-party` | major | NY:CPLR 8101 | The party that wins judgment gets costs unless a statute says otherwise or the court finds it inequitable. |
| `NY:CPLR-8201-costs-amount` | major | NY:CPLR 8201 | Fixes Supreme Court costs ($200 before note of issue, $200 after, $300 per trial or inquest). |
| `NY:CPLR-8301-disbursements` | major | NY:CPLR 8301 | Lists the disbursements a party awarded costs taxes in Supreme Court (witness and officer fees, publication, certified copies, docketing, one execution's sheriff fees, deposition transcripts up to $250, searches), and allows disbursements to a party recovering $50 or more without costs. |
| `NY:CPLR-8303-a-frivolous-property-claim` | major | NY:CPLR 8303-A | In an action for injury to property, a frivolous claim, counterclaim or defense brings costs and attorney's fees up to $10,000 against the party or its attorney. |
| `NY:JUD-475-a-notice-of-lien` | major | NY:Judiciary Law 475-A | An attorney who serves a written notice of lien before suit (for example with a tenant's deposit demand) has a lien from that notice on any settlement or recovery, unaffected by a later direct settlement. |
| `NY:JUD-475-attorney-lien` | major | NY:Judiciary Law 475 | An attorney who appears for the former tenant (or the landlord) has a lien on the claim and on any settlement or judgment proceeds in whatever hands they come, unaffected by a settlement between the parties. |
| `NY:JUD-484-nonlawyer-preparation` | major | NY:Judiciary Law 484 | The appearance rule bars Handoff and managers from appearing or signing pleadings as attorney. |
| `NY:JUD-485-a-felony` | major | NY:Judiciary Law 485-A | The appearance rule makes unauthorized practice a misdemeanor. |
| `NY:JUD-488-attorney-buying-claims` | major | NY:Judiciary Law 488 | A collection attorney may not buy or take assignment of a former tenant's balance to sue on it, nor give value for having claims placed with it. |
| `NY:JUD-490-champerty-exception` | major | NY:Judiciary Law 490 | The champerty rule treats an assignment of a balance taken to sue on as void. |
| `NY:JUD-491-no-fee-sharing` | major | NY:Judiciary Law 491 | No person or company may receive any part of an attorney's fee or any reward for placing a claim with an attorney for collection or suit. |
| `NY:22NYCRR-202.28-notify-court` | minor | NY:22 NYCRR 202.28 | Parties, including self-represented ones, must promptly notify the court in writing when a case is settled or discontinued, or when a party dies or files for bankruptcy. |
| `NY:22NYCRR-202.5bb-mandatory-efiling` | minor | NY:22 NYCRR 202.5bb | In designated counties and case types a represented party must commence and litigate a Supreme Court action by NYSCEF e-filing (with a hard-copy exception on the last limitations day), while an unrepresented party is exempt. |
| `NY:22NYCRR-208.16-file-discontinuance` | minor | NY:22 NYCRR 208.16 | After an NYC Civil Court action is discontinued (for example on settlement with the former tenant), the plaintiff's attorney must file the stipulation or statement of discontinuance within 20 days, or before any scheduled court date. |
| `NY:22NYCRR-208.36-incapacitated-settlement` | minor | NY:22 NYCRR 208.36 | A settlement of a claim by an infant or adjudicated incapacitated person in NYC Civil Court must follow CPLR 1207-1208 court approval. |
| `NY:22NYCRR-208.39-enforcement-subpoenas` | minor | NY:22 NYCRR 208.39 | Governs subpoenas and examinations to enforce an NYC Civil Court money judgment (the step that finds the former tenant's assets). |
| `NY:22NYCRR-208.6-summons-form` | minor | NY:22 NYCRR 208.6 | Prescribes the NYC Civil Court summons form: county division and court location, the parties, the plaintiff's residence address, the basis of venue, the sum and interest-start date for default judgment, and the 20/30-day answer notice. |
| `NY:22NYCRR-208.8-wrong-county` | minor | NY:22 NYCRR 208.8 | The NYC Civil Court clerk rejects a summons whose face shows another county is proper, and a wrong-county summons delays the answer date. |
| `NY:CCA-110-housing-part-appearance` | minor | NY:CCA 110 | The housing part hears summary proceedings and rent judgments that may precede the move-out and HP actions. |
| `NY:CCA-1501-who-issues-execution` | minor | NY:CCA 1501 | Says who issues an execution on an NYC Civil Court judgment (the creditor's attorney, or the clerk if the creditor has no attorney) and that Supreme Court time limits apply. |
| `NY:CCA-1502-transcript` | minor | NY:CCA 1502 | To reach real property, or to enforce through county clerks and sheriffs outside the city, the landlord must obtain the Civil Court transcript and docket it with the county clerk. |
| `NY:CCA-1505-real-property` | minor | NY:CCA 1505 | A Civil Court execution cannot reach real property. |
| `NY:CCA-1506-attached-real-property` | minor | NY:CCA 1506 | Where the tenant's real property was attached before judgment, execution must issue out of Supreme Court after docketing. |
| `NY:CCA-1508-enforcement-powers` | minor | NY:CCA 1508 | Lets the NYC Civil Court grant injunctions, restraining notices and receivers in an enforcement proceeding within CPLR 5221, with statewide service. |
| `NY:CCA-1805-A-commercial-claims-remedies` | minor | NY:CCA 1805-A | Commercial-claims remedies: conditional judgment, pre-judgment examination and restraint, transfer, and counterclaims only within the part's limit. |
| `NY:CCA-1806-A-commercial-claims-jury` | minor | NY:CCA 1806-A | The commercial-claims counterpart: the former tenant sued in the commercial claims part may demand a jury with fee, affidavit and $50 undertaking. |
| `NY:CCA-1806-small-claims-jury` | minor | NY:CCA 1806 | A landlord sued in small claims may move the case to a jury part by demand, fee, affidavit and a $50 undertaking. |
| `NY:CCA-1810-A-harassing-refiling` | minor | NY:CCA 1810-A | The commercial-claims counterpart of 1810: an owner re-filing an adjudicated or harassing commercial claim may be denied the part. |
| `NY:CCA-1810-harassing-refiling` | minor | NY:CCA 1810 | The clerk and court may deny the small claims part to a claimant re-filing a claim already adjudicated or filed to harass. |
| `NY:CCA-1811(d)-satisfaction-proof` | minor | NY:CCA 1811 | 1811(d): a judgment debtor that pays must present proof of satisfaction to the court or the judgment stays indexed as unpaid, which feeds the CCA 1812 treble-damages count. |
| `NY:CCA-1811-A-satisfaction-proof` | minor | NY:CCA 1811-A | Unsatisfied commercial-claims judgments are indexed under the debtor's name. |
| `NY:CCA-1812-A-information-subpoenas` | minor | NY:CCA 1812-A | An unpaid commercial-claims judgment lets the owner get information subpoenas from the clerk at nominal cost with help preparing them. |
| `NY:CCA-1814-A-defendant-name` | minor | NY:CCA 1814-A | The commercial-claims counterpart of 1814: a business party may be named by its business name, the judge fixes the true name, and a judgment debtor seeking vacatur must disclose its names. |
| `NY:CCA-1814-defendant-name` | minor | NY:CCA 1814 | A tenant may sue the landlord in small claims under any business name it uses, and a landlord seeking to vacate a small-claims judgment must disclose its true and business names. |
| `NY:CCA-1815-relative-representative` | minor | NY:CCA 1815 | The appearance rule states who may appear for owners and bars Handoff. |
| `NY:CCA-1900-security-for-costs` | minor | NY:CCA 1900 | Applies CPLR article 85 security for costs in NYC Civil Court with a $200 minimum undertaking. |
| `NY:CCA-1903-cplr-costs-apply` | minor | NY:CCA 1903 | Makes the CPLR rules on who gets costs (8101 prevailing party, 8103 split issues, 8104 consolidated actions, 8105 multiple parties, 8106 motions) apply in NYC Civil Court. |
| `NY:CCA-1904-additional-allowances` | minor | NY:CCA 1904 | Adds to Civil Court costs the CPLR 8302/8303(a) allowances and the discretionary allowance on an enforcement motion (8303(b)). |
| `NY:CCA-1905-no-costs-bankruptcy-defense` | minor | NY:CCA 1905 | A former tenant who wins on a bankruptcy-discharge defense recovers no costs. |
| `NY:CCA-1906-discretionary-costs` | minor | NY:CCA 1906 | The court may impose up to $50 costs on a motion, amendment or trial adjournment. |
| `NY:CCA-1907-taxation` | minor | NY:CCA 1907 | The clerk taxes costs and clerk and execution fees into the judgment. |
| `NY:CCA-1908-A-unacknowledged-mail-service` | minor | NY:CCA 1908-A | If the tenant does not return a CPLR 312-a mail-service acknowledgment within 30 days, the landlord's cost of serving another way is taxed against the tenant. |
| `NY:CCA-1909-review-of-taxation` | minor | NY:CCA 1909 | The clerk's taxation of costs can be reviewed only on motion within ten days. |
| `NY:CCA-1915-marshal-fees` | minor | NY:CCA 1915 | New York City marshals and the city sheriff enforcing Civil Court judgments get the same fees as a Supreme Court sheriff (fixed fees and 5% poundage). |
| `NY:CCA-201-limit-excludes-interest` | minor | NY:CCA 201 | The Civil Court's $50,000 limit is measured exclusive of interest and costs, so a balance of $50,000 plus interest and costs stays in Civil Court. |
| `NY:CCA-204-summary-rent-judgment` | minor | NY:CCA 204 | In an NYC summary proceeding the court renders judgment for rent due without regard to amount. |
| `NY:CCA-205-interpleader` | minor | NY:CCA 205 | Gives the Civil Court interpleader jurisdiction up to $50,000. |
| `NY:CCA-206-compulsory-arbitration` | minor | NY:CCA 206 | Where the Chief Administrator has ordered it for the county, a Civil Court money action of $10,000 or less per claim (not small claims) is heard by an arbitration panel. |
| `NY:CCA-208-counterclaims` | minor | NY:CCA 208 | In NYC Civil Court a counterclaim for money is heard without regard to amount. |
| `NY:CCA-209-provisional-remedies` | minor | NY:CCA 209 | Allows an order of attachment out of the NYC Civil Court wherever Supreme Court could issue one, and limits injunctions and receivers. |
| `NY:CCA-211-joinder` | minor | NY:CCA 211 | Several claims each within the $50,000 limit may be joined and judgment may exceed $50,000. |
| `NY:CCA-305-venue-residence` | minor | NY:CCA 305 | For Civil Court venue an assignee is treated as the original owner, and a corporation or association resides in any county where it does business or has an office. |
| `NY:CCA-306-venue-objection` | minor | NY:CCA 306 | Suing in the wrong county is not fatal. |
| `NY:CCA-401-summons-form` | minor | NY:CCA 401 | Who issues the Civil Court summons and what it must contain (answer with the clerk, the plaintiff's residence address, the attorney's office address). |
| `NY:CCA-407-service-on-303-agent` | minor | NY:CCA 407 | In Civil Court, service on the attorney or clerk designated as agent under CPLR 303 (a moved-away tenant who sued the landlord) may be made anywhere. |
| `NY:CCA-408-service-outside-city` | minor | NY:CCA 408 | A Civil Court summons may be served anywhere on a defendant who is a New York domiciliary and city resident (for example a former tenant temporarily away) and on added parties. |
| `NY:CCA-409-proof-of-service` | minor | NY:CCA 409 | Proof of service must be filed with the Civil Court clerk by the marshal's or sheriff's certificate or the server's affidavit. |
| `NY:CCA-410-service-complete` | minor | NY:CCA 410 | Service of a Civil Court summons is complete on personal delivery, or otherwise on filing proof of service. |
| `NY:CCA-412-interest-from-service` | minor | NY:CCA 412 | The interest rule sets interest from each due date. |
| `NY:CCA-801-provisional-city-only` | minor | NY:CCA 801 | A Civil Court provisional remedy (such as attachment) runs only within New York City against persons or property there. |
| `NY:CCA-802-tender-offer` | minor | NY:CCA 802 | Applies CPLR tender and offer-to-compromise rules (3219-3221) in Civil Court, with the added duty to file a copy with the clerk. |
| `NY:CCA-902-pleading-form` | minor | NY:CCA 902 | In Civil Court a money-only claim may be pleaded by an endorsement on the summons (nature, substance and default amount). |
| `NY:CCA-907-counterclaim-reply` | minor | NY:CCA 907 | In Civil Court a plaintiff need not reply to a counterclaim, which is deemed denied. |
| `NY:CPLR-1021-substitution-deadline` | minor | NY:CPLR 1021 | The parties rule states substitution on death. |
| `NY:CPLR-1202-guardian-ad-litem-motion` | minor | NY:CPLR 1202 | The parties rule bars a default against an infant or incompetent until a guardian ad litem is appointed. |
| `NY:CPLR-1204-gal-compensation` | minor | NY:CPLR 1204 | A guardian ad litem appointed for an incapacitated or infant former tenant may be paid reasonable compensation by any other party, including the landlord that sued. |
| `NY:CPLR-1205-no-costs-against-incapacitated` | minor | NY:CPLR 1205 | An infant, incompetent, conservatee or guardian-ad-litem-represented former tenant (or its representative) is not liable for costs unless the court orders. |
| `NY:CPLR-1502-later-action-co-obligor` | minor | NY:CPLR 1502 | To reach an unserved co-tenant's own property after a joint judgment, the landlord must bring a second, verified action, in which the co-tenant keeps all its defenses. |
| `NY:CPLR-209-war-tolling` | minor | NY:CPLR 209 | Tolls limitation periods while a party cannot sue because of a war between the United States and the country where it resides or of which it is a national. |
| `NY:CPLR-2106-affirmation` | minor | NY:CPLR 2106 | Any person may sign a statement affirmed under penalty of perjury in the statutory form instead of a notarized affidavit. |
| `NY:CPLR-213-b-crime-victim` | minor | NY:CPLR 213-B | A crime victim may sue the convicted defendant within seven years of the crime. |
| `NY:CPLR-216-adverse-claimant-notice` | minor | NY:CPLR 216 | Where one person sues for a contract sum and another claims the same sum but cannot be served, the defendant may notify the other claimant and cut its time to sue to one year. |
| `NY:CPLR-2222-docket-order` | minor | NY:CPLR 2222 | On request the clerk dockets an order directing payment of money (including motion costs, a so-ordered payment) as a judgment, making it enforceable and interest-bearing. |
| `NY:CPLR-3018-affirmative-defenses` | minor | NY:CPLR 3018 | Defenses such as the statute of limitations, payment, release, bankruptcy discharge and res judicata must be pleaded or are lost. |
| `NY:CPLR-3020-verification` | minor | NY:CPLR 3020 | Says who may verify the landlord's pleading: the owner, an officer of a domestic corporation, or an agent (managing agent) where the owner is a foreign entity or out of county or the facts are within the agent's personal knowledge. |
| `NY:CPLR-303-plaintiff-designates-agent` | minor | NY:CPLR 303 | A party beyond New York's jurisdiction who sues here (a moved-away tenant suing for the deposit) designates its attorney, or the clerk, as agent to be served in the landlord's separate action on a claim that could have been a counterclaim. |
| `NY:CPLR-305-summons-contents` | minor | NY:CPLR 305 | A Supreme Court summons must state the basis of venue (and the plaintiff's address if venue rests on its residence), the index number and filing date. |
| `NY:CPLR-306-proof-of-service` | minor | NY:CPLR 306 | Sets what the proof of service must show (papers, person, date, time, address, manner, a physical description of the person served, and the prior attempts for nail-and-mail). |
| `NY:CPLR-309-infant-incompetent` | minor | NY:CPLR 309 | How to serve a former tenant who is an infant, an adjudicated incompetent or a conservatee (the parent, guardian, committee or conservator, and the person too). |
| `NY:CPLR-310-a-limited-partnership` | minor | NY:CPLR 310-A | How a limited partnership owner (or tenant) is served: its managing or general agent or general partner in New York, an authorized agent, or a designated person. |
| `NY:CPLR-310-partnership` | minor | NY:CPLR 310 | How a partnership owner (or partnership tenant) is served. |
| `NY:CPLR-311-a-llc` | minor | NY:CPLR 311-A | How a limited liability company is served (a member or manager in New York, an authorized or designated agent, or the Secretary of State under the LLC Law). |
| `NY:CPLR-311-corporation` | minor | NY:CPLR 311 | How a corporation is served (an officer, director, managing or general agent, or authorized agent, or the Secretary of State under BCL 306). |
| `NY:CPLR-3213-summary-judgment-in-lieu` | minor | NY:CPLR 3213 | An action on an instrument for the payment of money only, or on a judgment, may start with a summary-judgment motion instead of a complaint. |
| `NY:CPLR-3216-want-of-prosecution` | minor | NY:CPLR 3216 | A landlord that sues and then neglects the case for a year after joinder can be served a 90-day demand to file a note of issue, after which the action may be dismissed. |
| `NY:CPLR-3217-discontinuance` | minor | NY:CPLR 3217 | How a landlord (or tenant) discontinues its claim, and that a second discontinuance by notice is an adjudication on the merits. |
| `NY:CPLR-3220-conditional-offer` | minor | NY:CPLR 3220 | A party sued on the lease may offer to fix damages at a stated sum if it loses on liability. |
| `NY:CPLR-4519-dead-mans-statute` | minor | NY:CPLR 4519 | The dead man's statute: after a former tenant dies, the landlord and its interested witnesses cannot testify against the estate about personal transactions or communications with the tenant. |
| `NY:CPLR-4539-reproductions` | minor | NY:CPLR 4539 | A scanned or electronic copy the business made in its regular course is as admissible as the original, and an image stored by a process that records any change is admissible when its tamper-protection is shown. |
| `NY:CPLR-4545-collateral-source` | minor | NY:CPLR 4545 | In an action for injury to property, a loss replaced by a collateral source (such as the owner's property insurance) reduces the award, net of two years' premiums, except payments carrying a statutory right of reimbursement. |
| `NY:CPLR-4547-compromise-inadmissible` | minor | NY:CPLR 4547 | Settlement offers and statements made in compromise negotiations over a disputed balance or deduction are not admissible to prove liability or amount. |
| `NY:CPLR-4549-agent-statements` | minor | NY:CPLR 4549 | Statements by the landlord's authorized agent or employee (the managing agent, Handoff, a collector) on matters within the agency are admissible against the landlord. |
| `NY:CPLR-501-venue-clause` | minor | NY:CPLR 501 | A written venue clause agreed before suit (for example in the lease) is enforced on a motion to change venue. |
| `NY:CPLR-5013-dismissal-effect` | minor | NY:CPLR 5013 | A dismissal after the plaintiff has closed its evidence is on the merits unless it says otherwise, so the landlord (or tenant) cannot sue again. |
| `NY:CPLR-5014-renewal-judgment` | minor | NY:CPLR 5014 | An action on a New York money judgment is allowed only after ten years from docketing (to renew the lien, begun in the ninth year), after a default on non-personal service, or by leave. |
| `NY:CPLR-5018-docketing` | minor | NY:CPLR 5018 | Docketing of a money judgment (and by transcript in other counties) with the debtor's last known address. |
| `NY:CPLR-5019-assignee-of-judgment` | minor | NY:CPLR 5019 | A person other than the judgment creditor who becomes entitled to enforce the judgment (an assignee such as a collector or debt buyer) must file its acknowledged instrument with the clerk before enforcing. |
| `NY:CPLR-5021-entry-of-satisfaction` | minor | NY:CPLR 5021 | The satisfaction rule states the creditor's duty to file a satisfaction-piece. |
| `NY:CPLR-511-venue-demand` | minor | NY:CPLR 511 | In Supreme Court a former tenant who objects to the landlord's county must serve a written demand with or before its answer and move within 15 days. |
| `NY:CPLR-5201-reachable-property` | minor | NY:CPLR 5201 | The enforcement-limits rule states the exemptions. |
| `NY:CPLR-5203-real-property-lien` | minor | NY:CPLR 5203 | A docketed money judgment is a lien on the former tenant's real property in that county for ten years (extendable for stays or a pending sale). |
| `NY:CPLR-5221-enforcement-forum` | minor | NY:CPLR 5221 | An enforcement proceeding on an NYC Civil Court judgment against a tenant who lives or works in the city is brought in the Civil Court. |
| `NY:CPLR-5223-disclosure-subpoena` | minor | NY:CPLR 5223 | Until the judgment is satisfied, the landlord may compel disclosure of anything relevant to collecting it by a subpoena stating the parties, judgment and amount due, and warning of contempt. |
| `NY:CPLR-5225-turnover` | minor | NY:CPLR 5225 | Turnover: the court orders the former tenant, or a third party holding the tenant's money or property, to pay or deliver it to satisfy the landlord's judgment. |
| `NY:CPLR-5227-debts-owed-to-tenant` | minor | NY:CPLR 5227 | By special proceeding the court may order anyone who owes the former tenant money to pay it to the landlord up to the judgment, or enter judgment against that person. |
| `NY:CPLR-5228-receiver` | minor | NY:CPLR 5228 | The court may appoint a receiver to collect or sell the former tenant's property to satisfy the judgment, at up to 5% commission (none if the landlord itself is receiver). |
| `NY:CPLR-5229-pre-judgment-restraint` | minor | NY:CPLR 5229 | After a decision in the landlord's favor and before judgment is entered, the trial judge may order the former tenant examined and restrained as if a post-judgment restraining notice had been served. |
| `NY:CPLR-5234-distribution-priority` | minor | NY:CPLR 5234 | Proceeds of a levy go to the judgment creditor after fees, excess to the former tenant, not before 15 days after service. |
| `NY:CPLR-5239-adverse-claims` | minor | NY:CPLR 5239 | Anyone claiming an interest in levied property (a joint account holder, a spouse, the former tenant) may bring a proceeding to decide it, and the court may void the levy and award damages. |
| `NY:CPLR-5250-arrest-of-debtor` | minor | NY:CPLR 5250 | A court may order the arrest of a judgment debtor about to leave the state or in hiding with property, to bring it in for examination. |
| `NY:CPLR-6211-confirmation` | minor | NY:CPLR 6211 | An attachment granted without notice must be confirmed on motion within 5 days after levy (10 days for a nondomiciliary defendant), or it lapses. |
| `NY:CPLR-6213-serve-within-60-days` | minor | NY:CPLR 6213 | An attachment granted before the former tenant is served is valid only if the summons is served (or publication begun and completed) within 60 days. |
| `NY:CPLR-6214-attachment-levy` | minor | NY:CPLR 6214 | How an attachment levy binds a garnishee: it must hold and turn over the defendant's property or debts for 90 days. |
| `NY:CPLR-6219-garnishee-statement` | minor | NY:CPLR 6219 | A garnishee served with an order of attachment must within ten days serve the sheriff a statement of its debts to and property of the defendant. |
| `NY:CPLR-6223-vacate-burden` | minor | NY:CPLR 6223 | The former tenant, a garnishee or any interested person may move to vacate an attachment, and the landlord bears the burden of proving the grounds, the need for the levy and probable success. |
| `NY:CPLR-8001-witness-fees` | minor | NY:CPLR 8001 | A non-party subpoenaed to testify or produce records gets $15 a day plus mileage outside a city (and $3 more at an examination before trial). |
| `NY:CPLR-8010-court-fund-fee` | minor | NY:CPLR 8010 | The NYC Commissioner of Finance takes 2% of money paid out of court. |
| `NY:CPLR-8011-sheriff-fees` | minor | NY:CPLR 8011 | Sets the sheriff's fixed fees for executions, income executions, attachments and service, largely payable in advance. |
| `NY:CPLR-8014-fees-collected-on-execution` | minor | NY:CPLR 8014 | Sheriff's fees on a property execution not in the creditor's bill of costs are collected from the judgment debtor under the execution. |
| `NY:CPLR-8018-index-fee` | minor | NY:CPLR 8018 | Commencing a Supreme Court action costs a $190 index-number fee (plus $20 in surcharges), which covers later filings including judgment and satisfaction docketing. |
| `NY:CPLR-8020-court-fees` | minor | NY:CPLR 8020 | Supreme Court fees after filing: $95 request for judicial intervention (needed for any motion, including a default judgment motion), $45 per motion, $30 to calendar, $65 jury demand, and $35 paid by the defendant to file a settlement or discontinuance. |
| `NY:CPLR-8021-transcript-fees` | minor | NY:CPLR 8021 | County clerk fees outside court actions include $25 in New York City to file a transcript of a Civil Court judgment and $15 to issue a transcript of the docket. |
| `NY:CPLR-8102-costs-limit-higher-court` | minor | NY:CPLR 8102 | A landlord that sues in Supreme Court in NYC for what the Civil Court could hear gets no costs unless it recovers $6,000 or more. |
| `NY:CPLR-8103-split-costs` | minor | NY:CPLR 8103 | Where the landlord recovers on the balance but the tenant prevails on a distinct claim (for example its deposit counterclaim), the court may award costs to both. |
| `NY:CPLR-8110-costs-against-fiduciary` | minor | NY:CPLR 8110 | Costs awarded against a fiduciary (a deceased tenant's executor, or an owner's estate or receiver) are charged to the estate, not personally, unless for mismanagement or bad faith. |
| `NY:CPLR-8202-motion-costs` | minor | NY:CPLR 8202 | Motion costs are fixed by the court up to $100. |
| `NY:CPLR-8303-additional-allowance` | minor | NY:CPLR 8303 | The court may award up to 5% (max $3,000) in a difficult or extraordinary contested case, and on a motion to enforce a judgment the greater of 5% of the judgment or $50. |
| `NY:CPLR-8401-clerk-taxation` | minor | NY:CPLR 8401 | The clerk taxes costs and disbursements on application and strikes any disbursement not shown by affidavit to be necessary and reasonable. |
| `NY:CPLR-8501-security-for-costs` | minor | NY:CPLR 8501 | A defendant may obtain security for costs as of right against a plaintiff that is not a New York resident, domestic corporation or licensed foreign corporation (a former tenant who moved away, an unlicensed foreign owner), and in the court's discretion against executors, receivers and similar plaintiffs. |
| `NY:CPLR-8502-stay-dismissal` | minor | NY:CPLR 8502 | Until ordered security for costs is posted, the plaintiff's action is stayed, and after 30 days it may be dismissed with costs. |
| `NY:CPLR-8503-undertaking-amount` | minor | NY:CPLR 8503 | Security for costs is an undertaking of $500 in New York City counties (more if the court fixes it). |
| `NY:JUD-476-lending-name` | minor | NY:Judiciary Law 476 | An attorney who knowingly lets a non-partner prosecute an action in the attorney's name, and the person who does so, each forfeit $50 to the other side. |
| `NY:JUD-479-no-solicitation` | minor | NY:Judiciary Law 479 | No person may solicit legal business or retainers for an attorney. |
| `NY:JUD-487-attorney-deceit` | minor | NY:Judiciary Law 487 | An attorney who deceives a court or party (for example with a false affidavit of service or amount in a balance suit) is liable to the injured former tenant for treble damages. |
| `NY:JUD-492-use-of-attorney-name` | minor | NY:Judiciary Law 492 | An attorney who knowingly lets a non-partner prosecute an action in the attorney's name, and the person who uses the name, commit a misdemeanor. |
| `NY:JUD-497-attorney-escrow-deposit` | minor | NY:Judiciary Law 497 | Attorney escrow funds that are nominal or short-term go into an IOLA account whose interest goes to the state fund. |

## no_decision where Jev had P(DECIDES) >= 0.9

| section | Jev P | reason |
|---|---|---|
| NY:22 NYCRR 202.27-b | 0.91 | Applies only to actions arising from a consumer credit transaction (CPLR 105(f)); a residential lease balance is not one (NY:ADJ-lease-balance-not-consumer-credit). The pending S9760 mailing is stated at NY:S9760-notice-mailings. |
| NY:CPLR 5102 | 0.97 | Enforces a judgment awarding possession by execution; in this chain possession is back when the tenant leaves, and an NYC eviction is enforced by an RPAPL warrant, not a CPLR 5102 execution. |
| NY:CCA 1807 | 0.93 | Limits appeal from a small-claims judgment to substantial-justice review; appellate practice, which changes no settlement or collection step. |
| NY:CPLR 205-A | 0.93 | Recommencement rules only for actions on instruments under CPLR 213(4) (mortgages and other real-property secured instruments); a lease balance or deposit claim is not one (its recommencement is CPLR 205(a), stated). |
| NY:CPLR 218 | 0.90 | Transitional rules for claims that accrued before CPLR article 2 took effect in 1963; no current claim is affected. |
| NY:CPLR 3004 | 0.91 | Rescission of a transaction void or voidable for fraud, mistake, duress or incapacity without tendering back benefits first; rescinding a lease is not a step in settling the account of a tenancy that has ended. |
