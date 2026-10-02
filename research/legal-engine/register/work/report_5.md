# Reviewer q5: batch 5 (federal bankruptcy and tax)

Scope: 264 queued sections of 11 U.S.C., the FRBP, 26 CFR 1 information-reporting and bad-debt regulations,
26 U.S.C. 6041A-6050X and 26 U.S.C. 166. Decisions: `register/work/decisions_5.jsonl` (reviewer `q5`). Builder
scripts: `register/work/q5_lib.py`, `q5_c1.py` to `q5_c18.py` (idempotent; rerunning replaces a section's row),
`q5_show.py`, `q5_verify.py`.

Checker: `python3 register/work/check_decisions.py 5` gives
`batch 5: 264/264 decided {'excluded_regime': 0, 'new_rule': 48, 'no_decision': 201, 'partial': 13, 'stated': 2}; 0 errors`.
`q5_verify.py` shows that every rule id cited in a reason, effect or dependency exists, either in stage-a or as a
batch-5 proposal. The checker's self-test passes.

## Counts

| decision | sections |
|---|---|
| new_rule | 48 |
| partial | 13 |
| stated | 2 (11 USC 301 and 501) |
| no_decision | 201 |
| excluded_regime | 0 |

- Proposed rules: 61 (16 critical, 31 major, 14 minor).
- Sections found to decide something (63), by Jev tier: likely 30, possible 21, long_or_unscored 11, low_confidence 1.
- No no_decision section had Jev P(DECIDES) >= 0.9. The highest were 11 USC 545 (0.81) and 525 (0.74).
  - 545: New York gives a residential landlord no lien or distress for rent, so there is no lien for the trustee to avoid.
  - 525: it binds only governmental units, private employers and student-loan programs.

## Proposed rules, most severe first

Critical
- `US:11USC101(5)-charge-timing` (partial, amends 362(a)(6)). Charges tied to time before the petition are pre-petition claims even if assessed later: they are stayed and dischargeable. Rent for time after the petition, and damage caused after it, are post-petition. A residential balance owed by an individual is a consumer debt.
- `US:11USC105-discharge-contempt` (partial, amends 524(a)(2)). Collecting a discharged balance is civil contempt under the Taggart "no fair ground of doubt" standard, with compensatory sanctions and fees.
- `US:11USC1141-owner-plan-confirmed` (partial). The owner's chapter 11 plan binds tenants and revests the estate in the owner.
  - An entity owner is discharged of untraceable refund claims at confirmation.
  - An individual owner is discharged only on completing the plan, and 523 debts are excepted.
- `US:11USC1328-ch13-discharge`. A completed-plan chapter 13 discharge covers willful and malicious damage to property but not fraud. A hardship discharge excepts all of 523(a). There is no discharge if the tenant had a prior discharge within 4 years (chapter 7) or 2 years (chapter 13); there is a revocation window.
- `US:11USC342-effective-notice`. Rules on notice addresses: the 90-day two-communications rule, a case-specific address, and a national address. A notice not sent as required is ineffective until it reaches the designated unit. There is no monetary penalty for a stay violation or 542 turnover failure before effective notice.
- `US:11USC348-conversion`. After conversion from 13 to 7, an unpaid refund goes to the chapter 7 trustee, and charges incurred during the chapter 13 become pre-petition claims. The 365(d) 60-day period restarts at conversion.
- `US:11USC507(a)(7)-deposit-priority` (partial, amends 541-704). In the owner's bankruptcy, a tenant's untraceable deposit refund is a seventh-priority claim.
  - The cap is $3,800 per individual (cases from 2025-04-01) and $3,350 before that.
  - Penalty damages are not priority claims.
  - The rule adjudicates the "not delivered or provided" split in favor of priority for residential deposits (Guarracino, River Village, Wise; Cimaglia rejected).
- `US:11USC522-refund-exemption`. A New York debtor elects either the state exemptions (DCL 282, which includes CPLR 5205(g), residential security deposits with no limit) or the federal ones (DCL 285, with the wildcard in (d)(5)).
  - An exempt refund is paid to the tenant, not the trustee.
  - The landlord keeps its 553 setoff right, but applying the deposit still needs stay relief.
  - A lease waiver of exemptions is void, and a judicial lien that impairs an exemption can be avoided.
- `US:11USC523-landlord-exceptions`. A balance survives discharge if it was obtained by fraud, if it rests on a false written rental application with reasonable reliance and intent (Appling), if it is for willful and malicious damage (Geiger), or if the landlord was not scheduled (Massa rule for no-asset cases).
  - The landlord must act by the 523(c) deadline.
  - 523(d) shifts fees to the landlord if its fraud claim on a consumer debt fails.
- `US:11USC547-preference`. The trustee can avoid payments made in the 90 days before the filing.
  - Floors: $600 in consumer cases, and $8,575 in non-consumer cases.
  - Defences: ordinary course, contemporaneous new value, subsequent new value, and full deposit coverage.
  - The landlord's own application of the deposit is a setoff, tested under 553(b).
  - Consequences for the landlord's claim: 502(h) and 502(d).
- `US:11USC554-abandoned-refund`. If the trustee abandons the refund, or it was scheduled and the case closes, it is paid to the tenant. An unscheduled refund stays estate property.
- `US:11USC727-ch7-discharge`. A tenant that is not an individual gets no discharge.
  - Also covered: the grounds for denial, the 8-year and 6-year bars, and the scope of the discharge (all debts that arose before the order for relief).
  - The landlord's objection and revocation rights and their windows.
- `US:FRBP4001-stay-relief-procedure`. Stay relief to apply the deposit:
  - It is sought by a contested-matter motion; the 362(e) 30-day rule applies.
  - The order is stayed 14 days after entry, so the deposit is applied on day 15.
  - A stipulation with the debtor needs court approval, with 14 days for objections.
- `US:FRBP4004-discharge-objection`. An objection to discharge is due 60 days after the first date set for the 341 meeting (chapter 7, and 1328(f) motions in chapter 13), or by the confirmation hearing in chapter 11. Extensions are allowed only on a motion filed before the deadline runs.
- `US:FRBP4007-523c-deadline`. A 523(c) complaint (fraud, false financial statement, willful and malicious injury) is due 60 days after the first date set for the 341 meeting, or the debt is discharged. In chapter 13, an (a)(6) complaint is due only when the debtor moves for a hardship discharge. Other 523 grounds may be raised at any time.
- `US:FRBP9006-time`. How bankruptcy deadlines are counted.
  - A deadline on a weekend or holiday rolls to the next business day, counting New York holidays for periods measured after an event.
  - Mail service adds 3 days.
  - The deadlines under 3002(c), 4003(b), 4004(a), 4007(c) and 4008(a) can be extended only as those rules allow and can never be shortened.

Major
- `US:11USC104-dollar-amounts`: use the amounts in effect when the case was commenced (2025 and 2022 values listed).
- `US:11USC1111-deemed-filed`: in the owner's chapter 11, a scheduled, undisputed tenant claim is deemed filed.
- `US:FRBP3003-ch11-bar-date`: in the owner's chapter 11, a tenant whose claim is unscheduled or scheduled as disputed must file by the bar date or receives nothing.
- `US:11USC1305-postpetition-claim`: in chapter 13, a claim for post-petition rent can be filed. It is lost if trustee approval was practicable and not obtained. Without one, the debt is not discharged.
- `US:11USC1322-plan-lease-codebtor`: a chapter 13 plan may assume or reject the lease and may pay a balance shared with a co-debtor in full.
- `US:11USC1327-plan-binds`: a confirmed chapter 13 plan binds the landlord whether or not it filed a claim or objected.
- `US:FRBP3015-plan-objection`: objections to a chapter 13 plan are due at least 7 days before the confirmation hearing. Confirmation fixes the secured amount and grants any stay termination the plan asks for.
- `US:11USC303-involuntary`: when a landlord alone may file an involuntary petition ($21,050, a claim not subject to bona fide dispute, fewer than 12 creditors), with 303(i) costs and bad-faith damages. In an involuntary case against the owner, the owner keeps operating until the order for relief.
- `US:11USC349-dismissal`: dismissal means no discharge; the refund revests in the tenant; 542 and 553 orders are vacated; 109(g) bars refiling for 180 days in some cases.
- `US:11USC363-owner-cash-collateral`: in the owner's case, rents and balances subject to an assignment of rents are cash collateral, to be segregated and used only with consent or a court order. The sale-order branch is included.
- `US:11USC552(b)(2)-postpetition-rents`: the lender's pre-filing lien on rents reaches rents collected after the filing.
- `US:11USC543-custodian-turnover`: a receiver or 7-A administrator stops disbursing and turns rents over to the trustee or debtor in possession.
- `US:11USC503-admin-expense-refund`: refunds of deposits the estate took after the filing are administrative expenses. A tenant's post-petition rent in chapter 7 is not an administrative expense.
- `US:11USC506-deposit-secured-claim` (amends FRBP-3002(c)): the landlord's claim is secured up to the deposit, and an excess deposit carries lease fees and interest.
- `US:11USC726-ch7-distribution-order` (amends FRBP-3002(c)): tardy claims are paid in third place, and penalty damages in fourth.
- `US:FRBP3001-claim-contents` (amends FRBP-3002(c)): Form 410, the lease, and an itemization in an individual's case. Omissions bring preclusion and fee sanctions. Also covers claim transfers.
- `US:11USC521-schedules-dismissal`: two ways to end the case early: a tax-return request, and automatic dismissal on day 46 with an order within 7 days.
- `US:11USC544(b)-state-lookback`: rent paid by a non-liable third party can be avoided for four years under New York's UVTA.
- `US:11USC548-constructive-fraud-third-party`: third-party payments are avoidable for 2 years; the tenant's own payments are for value.
- `US:11USC549-postpetition-payment`: payments made after the filing from estate property are avoidable.
  - In chapter 7, payments from post-filing wages are not.
  - In chapter 13, all post-filing earnings are estate property.
- `US:11USC550-transferee-liability`: the landlord is liable, not an agent without dominion over the money (Second Circuit test). A debt buyer is liable for what it kept. The recovery suit has a 1-year limit.
- `US:11USC546(a)-avoidance-deadline`: avoidance suits must be brought within 2 years after the order for relief, or 1 year after the trustee's appointment, and before the case is closed.
- `US:11USC558-estate-defenses`: the estate keeps the tenant's defences, including the GOL 7-108 forfeiture. A post-filing acknowledgment by the tenant does not bind the estate.
- `US:FRBP4003-exemption-objection`: objections to exemptions are due 30 days after the 341 meeting concludes; after that the exempt refund is paid to the tenant.
- `US:FRBP4008-reaffirmation`: reaffirmation terms (made before discharge, filed within 60 days, with the 524(c) conditions). Voluntary repayment may be accepted, not asked for. Co-tenants and guarantors stay liable (524(e)).
- `US:FRBP9010-agent-authority`: Handoff or the manager may file the proof of claim and vote. Other representation needs a Form 411 power of attorney. Motions and complaints for an entity owner need an attorney.
- `US:26CFR1.6041-1-agent-reports-rent` (amends 1.166-1(e)): the managing agent files a 1099-MISC for the owner's gross rents, including the deposit kept. The threshold is $2,000 for payments after 2025. Where Handoff and the manager both handle the money, the one closest to the owner files unless they agree otherwise in writing.
- `US:26CFR1.6041-6-filing-dates`: file by Feb 28 on paper or Mar 31 electronically; the owner's copy is due Jan 31.
- `US:26CFR1.6049-4-middleman-return` (amends 6049): the landlord is a middleman for deposit interest.
  - Interest counts as paid in the year it is credited.
  - Backup withholding applies if the tenant gives no TIN.
  - A corporate tenant is exempt; a nonresident-alien tenant gets a 1042-S.
- `US:26CFR1.6049-6-tenant-statement` (amends 6049): the tenant's statement is due between May 1 and Jan 31 and may be mailed to the tenant's last known address.
- `US:26USC166-writeoff-deduction` (amends 1.166-1(e)): the deduction is limited to basis and taken in the year the debt becomes worthless. Partial write-offs need a charge-off on the books. The nonbusiness-debt branch is included.

Minor
- `US:11USC1129(a)(9)-priority-cash`: a chapter 11 plan must pay the tenant's priority claim in cash.
- `US:11USC1192-subv-discharge`: subchapter V discharge after 3 to 5 years; 523 debts are excepted.
- `US:11USC707(b)-abuse-motion`: a creditor may move to dismiss only if the tenant's income is above the state median; fee risk if the motion fails.
- 166 regulations:
  - `US:26CFR1.166-2-worthlessness-evidence`: no suit is needed if a judgment would be uncollectible, and the deduction cannot be shifted to the year the bankruptcy ends.
  - `US:26CFR1.166-3-charge-off`: a partial write-off needs a charge-off.
  - `US:26CFR1.166-5-nonbusiness`: a nonbusiness debt is a short-term capital loss, only when wholly worthless.
- 6041 regulations:
  - `US:26CFR1.6041-3-exceptions`: tenants paying a rental agent file nothing; corporate owners get no 1099.
  - `US:26CFR1.6041-4-foreign-owner`: a documented foreign owner gets no 1099 and falls under chapter 3 withholding instead.
- 6049 regulations:
  - `US:26CFR1.6049-5-which-interest`: passed-through bank interest is 6049 interest; a landlord's own-funds interest is not.
  - `US:26CFR1.6049-8-nra-tenant`: a 1042-S for a nonresident-alien tenant in a listed country.
- 6050P regulations:
  - `US:26CFR1.6050P-2-debt-buyer`: a debt buyer in a significant lending business files a 1099-C; the landlord never does.
  - `US:26CFR1.6050P-1-identifiable-events`: the events and timing that trigger that filing.
- `US:FRBP4006-no-discharge-notice`: when a case closes without a discharge, the balance survives.
- `US:FRBP9037-redaction`: redact identifiers in the proof of claim and its attachments.

## Existing rules that look wrong or incomplete

None of the cited existing rules is wrong in what it states. Several are incomplete, and the partials above
address that:
- `US:11USC542-refund-payee` sends a chapter 7 refund to the trustee. It lacks two branches where the payee becomes the tenant: exemption, and abandonment or closing (`US:11USC522-refund-exemption`, `US:11USC554-abandoned-refund`). It also lacks the payee change on conversion (`US:11USC348-conversion`) and on dismissal (`US:11USC349-dismissal`).
- `US:11USC524(a)(2)` states the injunction, but not:
  - the contempt sanction (105);
  - that co-debtors stay liable, "discharge of a debt of the debtor does not affect the liability of any other entity on ... such debt" (524(e));
  - the reaffirmation and voluntary-repayment branches (524(c), (f)).
  These are proposed at 105 and FRBP 4008. The 524 section itself is outside this batch.
- `US:FRBP-3002(c)-claim-deadline` says a late claim "is disallowed except as tardy filing is permitted". In chapter 7 a tardy claim is allowed and paid in third place (726(a)(3)); proposed as `US:11USC726-ch7-distribution-order`.
- `US:11USC362(a)(6)` and `US:11USC362(a)(7)` (362 is outside this batch) have no rule for:
  - when the stay ends (362(c): closing, dismissal, grant or denial of discharge);
  - the 30-day rule for relief motions (362(e));
  - damages for a willful stay violation against an individual (362(k): actual damages, fees and punitive damages);
  - the repeat-filer limits (362(c)(3)-(4)).
  The proposed rules cite these provisions without a quote. The owner of the 362 section should state them.
- `US:26CFR1.166-1(e)-bad-debt` states the reporting threshold for 6041 but not that the agent must report rent to the owner. This is added by `US:26CFR1.6041-1-agent-reports-rent`.

## Boundary items (decided no_decision under this batch's tax scope; flagged for Owen)

The brief limits tax to three events: a deposit kept, interest passed through, and a balance written off. Under the
general test ("must file"), these sections would create filing duties in the chain:
- 26 U.S.C. 6050I: Form 8300 within 15 days if a former tenant pays more than $10,000 in cash, in one transaction or related ones.
- 26 U.S.C. 6050W: 1099-K reporting if balances are collected by card or third-party network and Handoff settles funds for several owners (it becomes an aggregating payee under 6050W(b)(4)(A)).
- 26 U.S.C. 6045(f) with 26 CFR 1.6041-1(a)(1)(iii): a landlord paying a former tenant's damages or settlement over $600 through the tenant's attorney files returns for both the attorney and the tenant.
  - The punitive part of a twice-the-deposit award is reportable income of the tenant.
  - The returned deposit itself is not reportable.

## Sources to save

These authorities are stated in rule effects or reasoning without a saved verbatim source. They should be saved under
`sources/` before acceptance.
- The Judicial Conference's 2025 adjustment notice (90 F.R. 8941; uscode.house.gov notes to 11 U.S.C. 104) for the $3,800, $8,575, $21,050 and $1,675/$15,800 figures.
- Cases:
  - Guarracino v. Hoffman, 246 B.R. 130 (D. Mass. 2000)
  - In re River Village Assocs., 161 B.R. 127 (Bankr. E.D. Pa. 1993)
  - Taggart v. Lorenzen, 587 U.S. 554 (2019)
  - Lamar, Archer & Cofrin v. Appling, 584 U.S. 709 (2018)
  - Kawaauhau v. Geiger, 523 U.S. 57 (1998)
  - In re Massa, 187 F.3d 292 (2d Cir. 1999)
  - Christy v. Alexander & Alexander (In re Finley, Kumble), 130 F.3d 52 (2d Cir. 1997)
- Statutes and rules: 11 U.S.C. 362(c), (e), (k); FRBP 1017(e); 26 CFR 301.6011-2; 26 CFR 1.6050I-1; NY DCL 278 (UVTA limitation).
