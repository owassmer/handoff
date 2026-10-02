# Review queue batch 6 (reviewer q6): federal consumer, credit, housing and servicemember law

Report only. Decisions: `register/work/decisions_6.jsonl`; builders `register/work/q6_c01.py`-`q6_c09.py` (idempotent, merge by section id); helpers `q6_lib.py`, `q6_read.py`; this report `q6_report.py`.

## Counts

Sections decided: 257/257.

- stated: 12
- partial: 6
- new_rule: 78
- no_decision: 158
- excluded_regime: 3

Proposed rules: 87 (critical 17, major 46, minor 24); every quote copied by script and verified by the checker; every dependency resolves to an existing or proposed id.

Checker output:

```
batch 6: 257/257 decided {'excluded_regime': 3, 'new_rule': 78, 'no_decision': 158, 'partial': 6, 'stated': 12}; 0 errors
```

## Proposed rules, most severe first

- **critical** `US:12CFR1005.10(d)-varying-debit-notice` [US:12 CFR 1005.10; walk 8.1b]: The payee (or the tenant's bank) must send the tenant written notice of the amount and date of the transfer at least 10 days before its scheduled date, so a varying debit is scheduled no earlier than the 10th day after the notice is sent.
- **critical** `US:12USC5536-cfpa-udaap-reach` [US:12 USC 5536; walk 5.10]: It binds only a covered person or service provider in connection with a consumer financial product or service.
- **critical** `US:15USC1605-plan-finance-charge` [US:15 USC 1605; walk 8.1b]: Each such charge is a finance charge, so the plan is consumer credit 'for which the payment of a finance charge is or may be required'.
- **critical** `US:15USC1681a(d)-(f)-own-experience-CRA` [US:15 USC 1681a; walk 8.7]: (a) A report containing only the landlord's own transactions or experiences with the tenant is not a consumer report, and the landlord is not a consumer reporting agency; when it sends that information to a consumer reporting agency it is a furnisher under 1681s-2 and Regulation V subpart E.
- **critical** `US:15USC1681c-2-furnisher-identity-theft` [US:15 USC 1681c–2; walk 8.7]: (a) It must have reasonable procedures to respond to the agency's notice so that it does not refurnish the blocked information.
- **critical** `US:15USC1681i-furnisher-deadline` (amends `US:15USC1681s-2(b)(1)`) [US:15 USC 1681i; walk 8.7]: The furnisher's investigation and report back (US:15USC1681s-2(b)(1)) must be completed within the agency's reinvestigation period: 30 days from the agency's receipt of the dispute, extended by up to 15 days if the tenant sends the agency relevant information during the 30 days (no extension once the item is found inaccurate or unverifiable), and 45 days where the dispute follows the tenant's free annual report.
- **critical** `US:15USC1681m(f)-(g)-identity-theft-debt` [US:15 USC 1681m; walk 8.2]: (f) No one may sell the balance, transfer it for consideration or place it for collection after the 1681c-2 notice; this binds everyone collecting it after the notice.
- **critical** `US:15USC1681n-willful` [US:15 USC 1681n; walk 8.7]: It is liable to the tenant for actual damages or statutory damages of $100 to $1,000; where a natural person obtained a report under false pretenses or knowingly without a permissible purpose, actual damages or $1,000, whichever is greater; punitive damages as the court allows; and costs and reasonable attorney's fees.
- **critical** `US:15USC1681o-negligent` [US:15 USC 1681o; walk 8.7]: It is liable for the tenant's actual damages plus costs and reasonable attorney's fees; no statutory or punitive damages.
- **critical** `US:15USC1681p-limitations` [US:15 USC 1681p; walk 8.7]: The action must be brought by the earlier of 2 years after the tenant discovered the violation or 5 years after the violation occurred, in federal district court regardless of amount or any other court of competent jurisdiction.
- **critical** `US:15USC1681t(b)(1)(F)-furnisher-preemption` [US:15 USC 1681t; walk 8.7]: (1) No state or city requirement or prohibition applies with respect to any subject matter regulated under 1681s-2 (the furnisher's accuracy duties, dispute notation, notice to the consumer of negative furnishing, identity-theft refurnishing, delinquency date, investigation of disputes).
- **critical** `US:15USC1693m-civil-liability` [US:15 USC 1693m; walk 7]: It is liable to the tenant for actual damages, plus statutory damages of $100 to $1,000 in an individual action (in a class action, no per-member minimum and a total cap of the lesser of $500,000 or 1% of net worth), plus costs and a reasonable attorney's fee.
- **critical** `US:24CFR982.312-absence` [US:24 CFR 982.312; walk 3.4]: The HAP payments, the HAP contract and the assisted lease terminate at that point, which fixes the end of the assisted tenancy for the settlement; the owner must repay the PHA any housing assistance payment received for the period after the termination, and that repayment is never charged to the family.
- **critical** `US:42USC3610-3612-hud-enforcement` [US:42 USC 3612; walk 5.10]: The complaint may be filed within one year after the practice occurred or ended; HUD serves the respondent within 10 days, and the respondent may answer within 10 days of notice.
- **critical** `US:42USC3613-private-action` [US:42 USC 3613; walk 5.10]: The person may sue in federal or state court within 2 years after the practice occurred or ended (the time a HUD or agency administrative proceeding is pending is excluded), whether or not an administrative complaint was filed, unless a conciliation agreement was reached (then only to enforce it) or an ALJ hearing on a HUD charge began.
- **critical** `US:42USC3614-ag-pattern` [US:42 USC 3614; walk 5.10]: The Attorney General may sue; the court may order injunctive relief, monetary damages to aggrieved persons, and a civil penalty of up to $50,000 for a first violation and $100,000 for any subsequent violation (as adjusted), with attorney's fees to the prevailing party other than the United States.
- **critical** `US:50USC4041-ag-penalties` [US:50 USC 4041; walk 7]: The Attorney General may sue; the court may grant equitable and declaratory relief, monetary damages to aggrieved persons, and civil penalties of up to $55,000 for a first violation and $110,000 for any subsequent violation (as adjusted for inflation).
- **major** `US:12CFR1005.3(a)-payee-duties` [US:12 CFR 1005.3; walk 6.5]: Regulation E binds it only through 1005.3(b)(2) (converting a check to an EFT), 1005.3(b)(3) (returned-item fees by EFT), 1005.10(b) (written authorization of recurring debits), 1005.10(d) (notice of varying debits), 1005.10(e) (no compulsory EFT repayment of credit), 1005.13 (two-year records) and 1005.20 (gift cards); every other Regulation E duty (disclosures, periodic statements, error resolution, unauthorized-transfer liability, stop-payment handling) is the account-holding bank's.
- **major** `US:12CFR1005.3(b)(2)-check-conversion` [US:12 CFR 1005.3; walk 8.1b]: The payee must give notice that the check will or may be processed as an EFT and obtain the tenant's authorization for each transfer; the tenant authorizes by receiving the notice and then sending the check.
- **major** `US:12CFR1005.3(b)(3)-returned-fee-eft` [US:12 CFR 1005.3; walk 5.3]: It may debit the fee electronically only with the tenant's authorization for that transfer: before the tenant made the underlying payment it received notice (for example on the invoice, statement or payment page) that the fee will be collected by EFT from the account if the payment is returned unpaid, stating the dollar amount of the fee (or, if the fee varies with the payment or other factors, how it is determined).
- **major** `US:12CFR1006.18-other-representations` [US:12 CFR 1006.18; walk 8.3]: It may not use any false, deceptive or misleading representation or means, including: implying government affiliation or bonding, that it is or works for a consumer reporting agency, that any individual is an attorney or a communication is from one, that the tenant committed a crime or disgraceful conduct, that a sale or referral of the balance makes the tenant lose a defense or become subject to a prohibited practice, that the account was turned over to innocent purchasers for value, that documents are legal process or that legal-process documents need no action; misstating the services rendered or the compensation it may lawfully receive; saying non-payment will lead to arrest, imprisonment, or seizure, garnishment, attachment or sale of property or wages unless that action is lawful and the collector or owner intends it; sending anything that simulates a court or agency document or misstates its source.
- **major** `US:12CFR1022.3(i)-identity-theft-report` [US:12 CFR 1022.3; walk 8.7]: An identity theft report is a copy of an official report filed with a law enforcement agency (false filing being a crime) alleging identity theft as specifically as the consumer can.
- **major** `US:12USC5517(a)(2)-landlord-credit` [US:12 USC 5517; walk 8.1b]: The CFPA does not reach that credit or the landlord's collection of it (directly or through an agent), or its sale of the plan once in default, unless: (i) the landlord assigns or sells the plan debt before default; (ii) the credit significantly exceeds the market value of the tenancy or is a subterfuge; or (iii) the landlord regularly extends credit subject to a finance charge.
- **major** `US:15USC1603-plan-exemptions` [US:15 USC 1603; walk 8.1b]: TILA does not apply to a plan with a tenant that is an organization (company, partnership, LLC), to credit primarily for business or commercial purposes, or to a plan whose amount financed exceeds the statutory threshold ($50,000 as adjusted), none of which is secured by real property or the tenant's dwelling.
- **major** `US:15USC1681g(e)-victim-records` [US:15 USC 1681g; walk 8.1]: Within 30 days of the request, and after verifying identity and the claim (government ID or matching identifying information, plus, at the landlord's election, a police report and the CFPB affidavit or an acceptable affidavit of fact) unless it already has high confidence in the requester's identity, the landlord provides free copies of the application and transaction records it controls, including records kept for it by a manager or Handoff, to the victim or the law enforcement agency the victim names.
- **major** `US:15USC1681h(e)-furnisher-immunity` [US:15 USC 1681h; walk 8.7]: No such action lies unless the information was false and furnished with malice or willful intent to injure the tenant; FCRA liability under 1681n and 1681o is unaffected.
- **major** `US:15USC1681m(a)-adverse-action` [US:15 USC 1681m; walk 8.1b]: It must give the tenant notice of the adverse action; any numerical credit score it used with its key factors; the name, address and telephone number of the consumer reporting agency that supplied the report and a statement that the agency did not make the decision; and notice of the right to a free report from that agency within 60 days and to dispute its accuracy.
- **major** `US:15USC1681q-false-pretenses` [US:15 USC 1681q; walk 8.7]: Knowingly and willfully doing so is a federal crime punishable by a fine, up to 2 years' imprisonment, or both, in addition to civil liability (US:15USC1681n-willful).
- **major** `US:15USC1681s-public-enforcement` [US:15 USC 1681s; walk 8.7]: The FTC may recover a civil penalty of up to $2,500 per violation (as adjusted for inflation) for a knowing violation that is a pattern or practice, but no penalty for a 1681s-2(a)(1) accuracy violation unless the person first violated an FTC injunction or order.
- **major** `US:15USC1692h-multiple-debts` [US:15 USC 1692h; walk 8.3]: It may not apply any of the payment to a debt the tenant disputes, and where the tenant directs how the payment is applied it must follow that direction.
- **major** `US:15USC1693e(a)-autopay-authorization` [US:15 USC 1693e; walk 8.1b]: The recurring debits may be authorized only by a writing signed or similarly authenticated by the tenant (an E-SIGN-compliant electronic signature, including a security code, suffices; the payee may not sign for the tenant on an oral authorization), which is readily identifiable as an authorization with clear terms, and the payee must give the tenant a copy of the terms, on paper or electronically.
- **major** `US:15USC1693j-malfunction-suspends` [US:15 USC 1693j; walk 5.3]: The tenant's obligation for that payment is suspended until the malfunction is corrected and the transfer can be completed, so the payment is not late for that period and no late fee or default follows from it, unless the payee afterwards demanded payment by another means in a written request, from which point the tenant owes payment by that other means.
- **major** `US:15USC1693k(1)-payment-plan-autopay` [US:15 USC 1693k; walk 8.1b]: It may not condition the plan on the tenant's repaying by preauthorized recurring electronic debits.
- **major** `US:15USC1693n(a)-criminal` [US:15 USC 1693n; walk 7]: It commits a federal crime punishable by a fine of up to $5,000, imprisonment of up to one year, or both, in addition to civil liability under US:15USC1693m-civil-liability.
- **major** `US:15USC7006-esign-consumer` (amends `US:15USC7001(c)-esign-consent`) [US:15 USC 7006; walk 6.4]: The consumer-consent requirements (US:15USC7001(c)-esign-consent) apply only where the tenant is a consumer: an individual who obtains the tenancy primarily for personal, family or household purposes, or that individual's legal representative.
- **major** `US:24CFR100.500-discriminatory-effect` [US:24 CFR 100.500; walk 5.10]: The policy is unlawful unless the landlord proves it is necessary to achieve a substantial, legitimate, nondiscriminatory interest, shown by evidence and not speculation, and the tenant does not prove that a less discriminatory practice would serve that interest.
- **major** `US:24CFR100.60(b)(5)-(7)-ending-tenancy` [US:24 CFR 100.60; walk 3.6]: Ending the tenancy for that reason, or harassment causing the tenant to leave, is a discriminatory housing practice; the tenant's damages claim (US:42USC3613-private-action) stands against the landlord's move-out claims, and charges flowing from the forced departure (lease-break or re-letting charges) are not owed as a matter of the tenant's damages.
- **major** `US:24CFR100.600-harassment` [US:24 CFR 100.600; walk 5.10]: Quid pro quo harassment is unlawful even if the tenant acquiesces; hostile-environment harassment is judged on the totality of circumstances from a reasonable person's view and needs no economic change or proven harm.
- **major** `US:24CFR5.2005-hcv-owner-limits` [US:24 CFR 5.2005; walk 3.4]: The owner may not evict or end the tenancy on the basis or as a direct result of that status.
- **major** `US:24CFR5.2007-documentation-confidentiality` [US:24 CFR 5.2007; walk 6.10]: The owner may, but need not, ask in writing for documentation; the tenant chooses among the HUD certification form, a professional's signed statement, a law-enforcement, court or agency record, or (at the owner's discretion) other evidence.
- **major** `US:24CFR5.2009-bifurcation-remaining-tenant` [US:24 CFR 5.2009; walk 3.4]: The bifurcation follows state and local eviction procedure.
- **major** `US:24CFR982.308-tenancy-addendum` [US:24 CFR 982.308; walk 5.7]: The tenancy addendum prevails over any other lease provision, and the tenant may enforce it against the owner; changes the owner and tenant agreed must be in writing with a copy given to the PHA at once.
- **major** `US:24CFR982.309-term-rent-freeze` [US:24 CFR 982.309; walk 5.7]: Rent to owner may not be raised during the initial term, so any increase billed in that term is not owed and is refunded or credited.
- **major** `US:24CFR982.310-owner-termination` [US:24 CFR 982.310; walk 3.4]: Only for a serious or repeated lease violation (including failure to pay the tenant's rent or other amounts due under the lease), a violation of law tied to occupancy, or other good cause; during the initial term, 'other good cause' must rest on something the family did or failed to do (not a refused renewal offer, owner use, sale, renovation or a higher rent).
- **major** `US:24CFR982.403-454-hap-ends` [US:24 CFR 982.403; walk 5.7]: For a too-small unit, the HAP contract ends at the end of the calendar month after the month the PHA notifies the owner; for insufficient funding, when the PHA terminates it.
- **major** `US:24CFR982.453-overpayment-recovery` [US:24 CFR 982.453; walk 5.7]: The PHA may recover the overpayment from the owner, abate or reduce payments, or terminate the contract.
- **major** `US:24CFR982.455-zero-hap` [US:24 CFR 982.455; walk 0]: The HAP contract has ended automatically; from then on the tenancy is not a voucher tenancy, and its settlement follows state and local law alone, without the part 982 deposit and charge rules (US:24CFR982.313(c), US:24CFR982.451(b)(4)).
- **major** `US:24CFR982.510-other-charges` [US:24 CFR 982.510; walk 5.7]: It may not charge extra for items customarily included in rent in the locality or provided at no extra cost to unsubsidized tenants in the building, and the lease may not require payment for meals or supportive services; such charges are not owed, may not be deducted from the deposit, and non-payment of meal or service charges is not a ground to end the tenancy.
- **major** `US:34USC12494-no-retaliation` [US:34 USC 12494; walk 5.10]: The owner or manager may not discriminate against, coerce, intimidate, threaten, interfere with or retaliate against that person for it (for example by adding charges, pressing collection or reporting because the tenant invoked VAWA).
- **major** `US:42USC3603(b)-exemptions` [US:42 USC 3603; walk 5.10]: They do not reach (1) a single-family house rented by a private individual owner who owns no more than three single-family houses (or interests in their proceeds), but only if rented without any broker, agent, salesperson or any person in the business of renting dwellings (including a manager or its employees; a person who took part as agent in two or more rentals in 12 months, as principal in three or more, or owns a building for five or more families is in that business) and without discriminatory advertising after notice; or (2) units in a building of at most four families in which the owner lives.
- **major** `US:42USC3610-complaint-period` [US:42 USC 3610; walk 5.10]: The complaint is timely if filed within one year after the practice occurred or ended; HUD serves the respondent within 10 days of filing, the respondent may answer within 10 days of notice, and HUD aims to finish investigating within 100 days.
- **major** `US:50USC3913-guarantor-cotenant` [US:50 USC 3913; walk 8.9]: The court may give the same stay, postponement or suspension to the guarantor, co-signer, co-tenant or other person primarily or secondarily liable, and may set aside a judgment against them when it sets aside the servicemember's.
- **major** `US:50USC3919-no-adverse-report` [US:50 USC 3919; walk 8.7]: That application or relief may not by itself be the basis for treating the tenant as unable to pay, for denying or changing the terms of a payment plan or refusing one on the terms requested, for an adverse report to a consumer reporting agency, or for annotating the tenant's record as a reservist or National Guard member.
- **major** `US:50USC3920-representatives` [US:50 USC 3920; walk 3.4]: The representative is treated as the servicemember, so the notice or request has the same effect as the servicemember's own.
- **major** `US:50USC3932-stay-with-notice` [US:50 USC 3932; walk 8.9]: At any stage before final judgment the court may stay the action on its own motion and must stay it for at least 90 days on the servicemember's application containing a statement of how duty materially affects the ability to appear with a date of availability, and a commanding officer's letter that duty prevents appearance and leave is not authorized.
- **major** `US:50USC3933-penalties` [US:50 USC 3933; walk 8.10]: (a) While an action to enforce the lease is stayed under the SCRA, no penalty accrues for failure to comply with the lease during the stay, so late fees for that period are not charged on the account.
- **major** `US:50USC3934-execution-stay` [US:50 USC 3934; walk 8.12]: If the servicemember's ability to comply is materially affected by military service, the court may on its own motion, and must on the servicemember's application, stay execution of the judgment and vacate or stay the attachment or garnishment.
- **major** `US:50USC3935-stay-term-codefendants` [US:50 USC 3935; walk 8.9]: The stay may run for the period of military service plus 90 days, or any part of it, and the court may set reasonable installment payments.
- **major** `US:50USC3952-lease-no-termination-without-order` [US:50 USC 3952; walk 3.4]: The landlord may not terminate the lease or retake possession for that breach without a court order; knowingly resuming or attempting to resume possession otherwise is a misdemeanor (fine, up to one year's imprisonment).
- **major** `US:50USC3956-landlord-service-contracts` [US:50 USC 3956; walk 3.4]: The tenant may terminate that contract by written or electronic notice with a copy of the orders and the termination date; the provider gives written or electronic notice of these rights.
- **major** `US:50USC3959-dependents` [US:50 USC 3959; walk 3.4]: The dependent is entitled to the protections of SCRA subchapter III (50 U.S.C.
- **major** `US:50USC4021-anticipatory-relief` [US:50 USC 4021; walk 8.10]: After notice and hearing the court may stay enforcement during service and for a period equal to the service after release (or after application if made later), conditioned on paying the unpaid balance and accrued interest in equal periodic installments at the rate that would apply if paid when due.
- **major** `US:50USC4043-other-remedies` (amends `US:50USC4042`) [US:50 USC 4043; walk 7]: Those remedies do not limit any remedy under other law, including consequential and punitive damages (for example under state law or the lease).
- **minor** `US:12CFR1005-cmt-2(k)-1-one-time-payments` [US:12 CFR Supplement_I_to_Part_1005; walk 6.5]: A payment the tenant initiates each time is not a preauthorized transfer: the 1005.10(b) written-authorization and 1005.10(d) varying-amount rules do not apply to it.
- **minor** `US:12CFR1005.13(b)-records` [US:12 CFR 1005.13; walk 8.1b]: It keeps evidence of compliance (the signed authorization and copy sent, the notices and their dates) for at least two years from when the disclosure or action was required; once it has actual notice of an investigation or has been served in an EFTA action, it keeps the related records until final disposition.
- **minor** `US:12CFR1005.2-reach` [US:12 CFR 1005.2; walk 8.1b]: It applies only where the tenant is a natural person and the account debited or credited is a checking, savings or other asset account (including a prepaid account) held primarily for personal, family or household purposes; a company tenant or a business account is outside.
- **minor** `US:12CFR1022.82-address-discrepancy` [US:12 CFR 1022.82; walk 8.7]: It must have and follow reasonable policies to form a reasonable belief that the report relates to the tenant (for example comparing the report with the lease application and its own records, or verifying with the tenant).
- **minor** `US:15USC1611-criminal` [US:15 USC 1611; walk 8.1b]: It is punishable by a fine of up to $5,000, imprisonment of up to one year, or both.
- **minor** `US:15USC1615-unearned-interest` [US:15 USC 1615; walk 8.1b]: The landlord promptly refunds the unearned part of the interest charge (not required if under $1); for a precomputed plan longer than 61 months the refund is computed by a method at least as favorable as the actuarial method.
- **minor** `US:15USC1681c-1-freeze-alerts` [US:15 USC 1681c–1; walk 8.7]: A security freeze does not block a report pulled by the landlord, its agent or assignee, or a prospective buyer of the balance, for reviewing or collecting the account or contract.
- **minor** `US:15USC1681d-investigative-report` [US:15 USC 1681d; walk 8.7]: It must disclose in writing, mailed or delivered within 3 days after first requesting the report, that such a report may be made, with the right to request the nature and scope of the investigation and the summary of rights; certify this to the agency; and on the tenant's written request disclose the nature and scope in writing within 5 days.
- **minor** `US:15USC1681w-disposal` [US:15 USC 1681w; walk 6.10]: It must dispose of that information properly under the disposal regulations issued under 1681w (for non-bank persons, the FTC's rule); the section imposes no duty to keep or destroy records that other law does not.
- **minor** `US:15USC1693l-no-waiver` [US:15 USC 1693l; walk 8.1b]: The waiver is void.
- **minor** `US:24CFR100.10(a)(3)-occupancy-limits` [US:24 CFR 100.10; walk 5.10]: Reasonable local, state or federal occupancy limits may be applied; a charge based on household size beyond such a limit is not saved by this exemption and is tested as familial-status discrimination.
- **minor** `US:24CFR100.70(d)(1)-agent-refusal` [US:24 CFR 100.70; walk 5.10]: The owner may not discharge, penalize or take other adverse action against the employee, broker or agent for refusing.
- **minor** `US:24CFR100.75-statements` [US:24 CFR 100.75; walk 6.4]: It may not indicate a preference, limitation or discrimination because of race, color, religion, sex, handicap, familial status or national origin (for example attributing a charge to 'the children' or to a disability as such); written notices and statements include any document used with respect to the rental.
- **minor** `US:24CFR982.454-funding-termination` [US:24 CFR 982.454; walk 5.7]: No housing assistance is paid after the termination, and the lost assistance is never charged to the family (US:24CFR982.451(b)(4)); the remaining tenancy and its settlement follow the lease and state law.
- **minor** `US:24CFR982.456-tenant-enforcement` [US:24 CFR 982.456; walk 7]: The tenant may enforce the lease, including the owner's obligations under the tenancy addendum, against the owner; it is not a party to or beneficiary of the HAP contract and cannot enforce the HAP contract itself.
- **minor** `US:24CFR982.5-written-notices` [US:24 CFR 982.5; walk 3.4]: The notice must be in writing.
- **minor** `US:42USC3602(h)-handicap` [US:42 USC 3602; walk 5.9]: Handicap means a physical or mental impairment substantially limiting one or more major life activities, a record of one, or being regarded as having one; it excludes current illegal use of or addiction to a controlled substance (recovered or treated addiction and alcoholism are included).
- **minor** `US:42USC3607-religious-older-persons` [US:42 USC 3607; walk 5.10]: The religious organization may prefer members of its religion (unless membership is restricted by race, color or national origin) and the club its members; familial-status protections do not apply to qualifying housing for older persons, and a person relying in good faith on a written claim of that exemption without knowledge that it fails owes no personal damages; conduct based on the drug-manufacture or distribution conviction is not prohibited; reasonable occupancy limits stand.
- **minor** `US:42USC3631-criminal` [US:42 USC 3631; walk 5.10]: It is a federal crime: fine or up to one year's imprisonment, up to ten years if bodily injury results or a dangerous weapon is used or threatened, and up to life if death results.
- **minor** `US:50USC3914-allied-forces` [US:50 USC 3914; walk 3.4]: The tenant has the same SCRA relief and protections as a servicemember (for example lease termination under US:50USC3955(a)(1), the 6% cap, stays), ending on discharge or release from that service.
- **minor** `US:50USC4011-abuse` [US:50 USC 4011; walk 8.12]: The court enters whatever judgment or order it lawfully could concerning that transfer or acquisition, so the SCRA does not shelter it.
- **minor** `US:50USC4012-certificates` [US:50 USC 4012; walk 8.9]: A certificate signed by the Secretary concerned (including one appearing so signed) is prima facie evidence of whether and when the person served, residence on entry, rank and unit, pay and release or death; the Secretary issues one on application.
- **minor** `US:50USC4022-poa-missing` [US:50 USC 4022; walk 3.4]: The power is extended automatically for the missing period if executed during service (or after orders or notice of possible orders), naming a spouse, parent or other relative, and expiring by its terms after missing status began; it is not extended if its terms say it expires on the stated date even if the servicemember goes missing.
- **minor** `US:50USC4026-business-obligations` [US:50 USC 4026; walk 8.12]: The servicemember's assets not held in connection with the business may not be used to satisfy that balance during military service, unless a court on the landlord's application modifies the relief as justice and equity require.

## Existing rules that look wrong or incomplete

1. `NYC:SHIELD-5-77(e)(10)-credit-report-notice` applies the city's pre-reporting notice and 14-day wait to every
   debt collector that furnishes. FCRA 1681t(b)(1)(F) bars any state-law requirement "with respect to any subject matter
   regulated under section 1681s–2 of this title, relating to the responsibilities of persons who furnish information to
   consumer reporting agencies" (register/texts/US_15USC-ch41/1681t.txt). Notice to the consumer of negative furnishing
   is regulated by 1681s-2(a)(7); preemption is by subject matter, so DCWP's exemption for (a)(7) filers does not save
   the rest. The rule is displaced for furnishing; the Reg F pre-furnishing contact rule (`US:12CFR1006.30(a)`) still
   binds federal debt collectors. Proposed: `US:15USC1681t(b)(1)(F)-furnisher-preemption` (critical). The walk (8.5)
   lists the SHIELD notice as a live duty.
2. `NY:GBL-604-bb-coerced-debt`, credit-agency branch: it requires the creditor to "notify such consumer reporting agency
   that the account is disputed" within ten business days. That is a state requirement on the subject matter of
   1681s-2(a)(3) and (a)(8) and is displaced by the same clause; the stop-collection, review and determination duties stand.
3. `NY:RPL-227-c(5)(b)` reaches communications with "a collector or credit bureau". As to what is furnished to a
   consumer reporting agency it is displaced by 1681t(b)(1)(F); the federal accuracy duty
   (`US:15USC1681s-2(a)(1)(A)`) gives the same result, since a lawful 227-c termination reported as early is inaccurate.
   The rule stands for prospective landlords, collectors and other third parties.
4. `US:15USC1681s-2(b)(1)` says the furnisher investigates "within the agency's reinvestigation period" without the
   period; `EXT:15USC1681i` is marked "Not read". 1681i fixes 30 days, +15, 45 after a free report
   (`US:15USC1681i-furnisher-deadline`, partial).
5. `US:24CFR100.65-terms` conditions on a dwelling "not exempt under 42 U.S.C. 3603(b)" but no rule states the exemption.
   For the target customer (scattered single-family rentals) the single-family exemption is lost whenever a manager or
   other person in the business of renting is used (`US:42USC3603(b)-exemptions`).
6. `US:15USC7001(c)-esign-consent` does not limit the consent duty to a "consumer" (an individual renting for personal,
   family or household purposes, 15 U.S.C. 7006(1)); a company tenant is outside (`US:15USC7006-esign-consumer`, partial).
7. `US:50USC4042` states the private SCRA action but not the Attorney General's civil penalties (4041: $55,000 / $110,000)
   or the preservation of consequential and punitive damages (4043) (proposed `US:50USC4041-ag-penalties`,
   `US:50USC4043-other-remedies`).
8. Register scope, not a rule: `register/instruments.json` sets TILA part B (15 U.S.C. 1631-1651) out of scope because "a
   residential lease is not a credit transaction". A landlord that regularly offers move-out payment plans with a finance
   charge or more than four installments is a TILA creditor (`US:15USC1602(g)`, `US:15USC1605-plan-finance-charge`), and
   each such plan is a closed-end consumer credit transaction that needs part B disclosures (15 U.S.C. 1638, Reg Z
   1026.17-18). Part B, and Reg Z, belong in the register for that branch. Likewise the FTC Disposal Rule (16 CFR part 682)
   that 1681w requires is not in the register.

## no_decision sections with Jev P(DECIDES) >= 0.9

- US:15 USC 1681l (0.92): restricts what a consumer reporting agency may reuse from an investigative report in a later
  report; it binds agencies only, and no landlord, manager, Handoff or collector act turns on it.

No excluded_regime section had Jev >= 0.9.

## Recall notes for Jev (sections decided as deciding although Jev scored them below 0.15)

US:24 CFR 982.308, 982.309, 982.310, 982.312, 982.403, 982.453, 982.454, 982.455, 982.510, 5.2001, 5.2007, 5.2009;
US:12 CFR 1005.2, 1022.3; US:15 USC 1605, 7006; US:34 USC 12494; US:42 USC 3602; US:50 USC 3920. Most are voucher-owner
duties (termination grounds, tenancy addendum, HAP end dates, other charges) and definitions that change a stated rule's
reach; Jev read them as PHA administration.

## Method notes

- Reg E: only 1005.3(b)(2)-(3), 1005.10(b), (d), (e), 1005.13 and 1005.20 bind a person other than the account-holding bank
  (1005.3(a)); those became rules (autopay authorization, 10-day notice of a varying debit, no compulsory autopay for
  payment plans, check conversion and returned-fee notices, records, liability). Everything else, including error
  resolution, is the bank's; remittance and interchange sections decide nothing.
- The payment-plan branch recurs across TILA, EFTA, CFPA and FCRA: a plan is credit (`US:15USC1602(f)`); it may not be
  conditioned on autopay; it can make the landlord a TILA creditor; it stays outside the CFPA unless the 5517(a)(2)
  exceptions apply; refusing one on a credit report is an adverse action.
- 24 CFR 982: PHA-internal administration is no_decision; the two project-based sections (982.504, 982.521) and CPD
  equal access (5.106) are excluded_regime.

