import sys; sys.path.insert(0, 'register/work'); from q4_lib import *
MIL = 'NY Military Law art. 13'
add([
 nd('NY:Military Law 311', 'Protects servicemembers under contracts to buy real or personal property, or leases with a view to purchase; a residential lease is not such a contract (dwelling leases: NY:MIL-310(2), NY:MIL-306-309).'),
 nd('NY:Military Law 312', 'Stays enforcement of mortgages on property a servicemember owns; the tenant\'s lease balance is not a mortgage obligation.'),
 nd('NY:Military Law 313', 'Appraisal and settlement in stayed foreclosure or repossession of personal property; not a lease balance.'),
 nd('NY:Military Law 314', 'Property-tax sales and interest on a servicemember\'s own property; not part of a tenancy settlement.'),
 nd('NY:Military Law 319', 'Lets a court disregard transfers made to exploit article 13; a court remedy that changes no landlord step or amount.'),
 nd('NY:Military Law 321', 'Evidence rules for proving military service (certificates, missing persons) in article 13 proceedings; the service status the rules depend on is a fact input, and the notice with orders the landlord relies on is stated in NY:MIL-310(2) and NY:MIL-323-a-6pct.'),
 nd('NY:Military Law 323-B', 'Waives court filing fees for militia members suing over their service; changes nothing the landlord owes or does.'),
 nd('NY:Military Law 326', 'Saving clause for rights based on service before 1948-04-01; no current tenancy is affected.'),
 nd('NY:SSL 131-S', 'Social services payments of arrears to gas and electric corporations and municipalities; the landlord is neither payee nor obligor.'),
 nd('NY:SSL 131-W', 'Eligibility and repayment agreements for district payment of rent arrears; binds the district and the recipient. Money the district pays the landlord is rent received and credited like any payment.'),
])
S = 'NY:Military Law 313-A'
add([{'section_id': S, 'decision': 'new_rule', 'reason': 'Bars basing an adverse credit report on the servicemember\'s having sought or obtained article 13 relief; changes what the landlord may report.', 'proposed': [rule(S,
  id='NY:MIL-313-a-no-adverse-report', instrument=MIL, provision='Military Law 313-a(1)-(3)', actor='landlord, managing agent or collector that reports to credit agencies', modality='prohibition',
  condition='A former tenant in military service applied for or received a stay, postponement or suspension of payment under article 13 (for example a stay of the landlord\'s suit, NY:MIL-304-stay-on-application, or relief under NY:MIL-323-further-relief).',
  effect='The application or the relief by itself may not be the basis for treating the tenant as unable to pay or for an adverse report to a consumer reporting agency. The landlord may still report the delinquency of the balance on its own facts, accurately (US:15USC1681s-2(a)(1)(A)), but may not report or characterize the stay or the application as a default or as evidence of inability to pay.',
  dependencies=['US:15USC1681s-2(a)(1)(A)'],
  quote=q(S, 'An adverse report relating to the creditworthiness of such person in military service by or to any person or entity engaged in the practice of assembling or evaluating consumer credit information.'),
  construction=[{'source_file': 'register/texts/NY_MIL/313-a.txt', 'quote': q(S, 'shall not itself, without regard to other considerations, provide the basis for any of the following:')}],
  reasoning='The section forbids the stay itself serving as the basis; other considerations (the unpaid balance) remain reportable.',
  severity='major', walk_step='8.7')]}])
L = 'NY:Military Law 316-A'
add([{'section_id': L, 'decision': 'partial', 'atom_ids': ['US:50USC3958(a)', 'US:50USC3958-lien-enforcement'], 'reason': 'The federal rule states the court-order requirement for SCRA servicemembers; subdivision 2 extends it to New York state active duty and fixes a three-month tail and a return notice. Subdivision 1 (life-insurance assignments) changes nothing.', 'proposed': [rule(L,
  id='NY:MIL-316-a(2)-storage-lien', instrument=MIL, provision='Military Law 316-a(2)', actor='landlord or managing agent holding a former tenant\'s belongings', modality='prohibition',
  determinacy='MIXED', judgment_terms=['ability to pay the storage charges materially affected by reason of military service'],
  condition='A former tenant in military service as defined by Military Law 301(1) (federal active duty, or New York state active duty or national guard state duty) left household goods, furniture or personal effects that the landlord stores, and the landlord claims a lien for the storage charges.',
  effect='During the service and for three months after, the landlord may not foreclose or enforce the storage lien (sell, keep or apply the goods for the charges) without a prior court order and an approved return. The court must, on the tenant\'s application, stay the proceeding or make an equitable disposition unless the service did not materially affect the tenant\'s ability to pay. Within thirty days of returning from service the tenant must notify whoever stores the goods. Keeping the reasonable storage cost from the deposit (NY:GOL-7-108(1-a)(b)-refundable) does not foreclose the lien; holding the goods for the charges does (US:50USC3958-lien-enforcement).',
  dependencies=['US:50USC3958(a)', 'NY:COMMONLAW-belongings-owner-keeps'],
  quote=q(L, 'No person shall exercise any right to foreclose or enforce any lien for storage of household goods, furniture, or personal effects of a person in military service during such person’s period of military service and for three months thereafter except upon an order previously granted by a court'),
  severity='major', walk_step='6.9', amends='US:50USC3958(a)')]}])
W = 'NY:Military Law 318'
add([{'section_id': W, 'decision': 'partial', 'atom_ids': ['US:50USC3918'], 'reason': 'The federal rule limits waivers of SCRA rights; 318 forbids even asking a New York servicemember to waive article 13 rights, voids the waiver and sets criminal and civil penalties.', 'proposed': [rule(W,
  id='NY:MIL-318-no-waiver-request', instrument=MIL, provision='Military Law 318(2)', actor='landlord, managing agent, Handoff or collector', modality='prohibition',
  condition='A lease, move-out agreement, settlement, payment plan or release with a tenant who is or may become a person in military service (Military Law 301(1)).',
  effect='No one may solicit, require, demand or request that the tenant waive any article 13 right, present or future (for example the 310 termination, the 323-a 6% cap, stays and penalty relief). A waiver obtained in violation does not bind the servicemember. A knowing violation is a misdemeanor (up to one year, up to $1,000, or both) and carries a civil penalty of up to $5,000 per occurrence, recovered by the Attorney General. Standard lease or settlement forms therefore carry no article 13 waiver.',
  dependencies=['US:50USC3918', 'NY:MIL-310(2)', 'NY:MIL-323-a-6pct'],
  quote=q(W, 'No person shall solicit, require, demand or otherwise request that a person waive any of his or her rights under this article, whether existing at that time or thereafter to accrue.'),
  severity='critical', walk_step='3.4', amends='US:50USC3918')]}])
F = 'NY:Military Law 323'
add([{'section_id': F, 'decision': 'new_rule', 'reason': 'Lets a servicemember obtain a court-ordered stay and installment schedule on a pre-service lease balance, with no penalties accruing; changes when and how the balance may be collected.', 'proposed': [rule(F,
  id='NY:MIL-323-further-relief', instrument=MIL, provision='Military Law 323(1)(b), (2)', actor='landlord or its collector', modality='procedure',
  determinacy='MIXED', judgment_terms=['ability to comply materially affected by reason of military service', 'such other terms as may be just'],
  condition='A former tenant who incurred the lease obligation before entering military service applies to a court during service or within six months after it for relief from the balance.',
  effect='Unless the court finds the service did not materially affect the tenant\'s ability to pay, it may stay enforcement during service and, from the end of service (or the application, if later), for a period up to the length of the service, conditioned on payment of the balance and accrued interest in equal periodic installments at the rate that applies to the obligation when paid on time, on other just terms. While the tenant complies with the stay, no fine or penalty (for example a late fee) accrues. Interest is still capped at 6% during service (NY:MIL-323-a-6pct).',
  dependencies=['NY:MIL-323-a-6pct', 'NY:MIL-305-penalty-relief'],
  quote=q(F, 'In the case of any other obligation, liability, tax, or assessment, a stay of the enforcement thereof during the applicant’s period of military service'),
  severity='major', walk_step='8.10')]}])
P = 'NY:SCPA 1112'
add([{'section_id': P, 'decision': 'partial', 'atom_ids': ['NY:ADJ-tenant-death-payee', 'NY:COMMONLAW-owner-death-agency'], 'reason': 'The rules name the executor, administrator or voluntary administrator; where no one eligible for letters is known, the public administrator takes the tenant\'s property (refund, belongings) and collects a deceased owner\'s rents.', 'proposed': [rule(P,
  id='NY:SCPA-1112-public-administrator', instrument='NY Surrogate\'s Court Procedure Act art. 11', provision='SCPA 1112(1)-(3)', actor='landlord or managing agent', modality='obligation',
  condition='Branch (a): the former tenant died intestate with no known person eligible to receive letters, leaving a refund due or belongings in the unit. Branch (b): an individual owner died intestate with no known person eligible for letters, and the building\'s rents and the departing tenant\'s account remain open. In NYC the public administrator of the county acts.',
  effect='(a) The public administrator has authority to take charge of the tenant\'s personal property in the county: the refund is paid to it and the belongings are released to it, and the landlord\'s claim for the balance is presented to it (NY:ADJ-tenant-death-payee). (b) The public administrator has authority to take possession of the building, manage it and collect its rents, so rent and the departing tenant\'s balance are collected by or for it, and the deposit refund duty runs with the building it controls (NY:COMMONLAW-owner-death-agency).',
  dependencies=['NY:ADJ-tenant-death-payee', 'NY:COMMONLAW-owner-death-agency'],
  quote=q(P, 'The public administrator in his proper county shall have authority to take possession of, manage and collect the rents of the real property and take charge of the personal property of an intestate:'),
  severity='critical', walk_step='2.5')]}])
C = 'NY:SCPA 1803'
add([{'section_id': C, 'decision': 'partial', 'atom_ids': ['NY:ADJ-tenant-death-payee'], 'reason': 'The rule says to present the claim to the fiduciary within 7 months; 1803 fixes the claim\'s form and how it is delivered.', 'proposed': [rule(C,
  id='NY:SCPA-1803-claim-form', instrument='NY Surrogate\'s Court Procedure Act art. 18', provision='SCPA 1803(1)-(3)', actor='landlord or its collector', modality='procedure',
  condition='The landlord presents its claim for a deceased former tenant\'s balance to the executor or administrator (NY:ADJ-tenant-death-payee).',
  effect='The claim must be in writing and state the facts it rests on and the amount (the itemized statement and the lease supply both). The fiduciary may require an affidavit that the amount is justly due, all payments are credited, no offsets are known, and no security is held except as described (the deposit applied must be described). It is delivered to the fiduciary personally or by certified mail, return receipt requested, at the residence in the fiduciary\'s designation, or served on the court clerk if the fiduciary cannot be found in the state. A claim not presented this way, and not based on a judgment or court order, cannot be enforced in the surrogate\'s court.',
  dependencies=['NY:ADJ-tenant-death-payee'],
  quote=q(C, 'Every claim against the estate of a decedent other than claims for expenses of administration and claims of the United States or the state of New York must be in writing, contain a statement of the facts upon which it is based and the amount thereof.'),
  severity='major', walk_step='2.5', amends='NY:ADJ-tenant-death-payee')]}])
O = 'NY:SCPA 1811'
add([{'section_id': O, 'decision': 'new_rule', 'reason': 'Fixes where a deceased tenant\'s lease balance ranks in the estate, which decides whether pursuing it recovers anything.', 'proposed': [rule(O,
  id='NY:SCPA-1811-claim-priority', instrument='NY Surrogate\'s Court Procedure Act art. 18', provision='SCPA 1811(1)-(3)', actor='landlord or its collector', modality='priority',
  condition='The landlord holds a claim for a deceased former tenant\'s balance against the tenant\'s estate.',
  effect='The fiduciary pays in this order: administration expenses and reasonable funeral expenses; debts preferred by federal or state law; taxes assessed before death; judgments docketed and decrees entered against the tenant before death, by their priority; then all other debts, including a lease balance not reduced to judgment, as one class paid ratably with no preference for suing first or for being due. Rent due or accruing on a lease the tenant held at death may be preferred over that last class if the court finds it benefits the estate. The pursue-or-write-off estimate uses the balance\'s class and the estate\'s assets.',
  dependencies=['NY:ADJ-tenant-death-payee', 'NY:SCPA-1803-claim-form'],
  quote=q(O, 'Preference may be given to rents due or accruing on leases held by the decedent at the time of his death over other debts specified in subdivision 2 (d) if it appears to the court\'s satisfaction that such preference will benefit the estate of the decedent.'),
  severity='major', walk_step='8.12')]}])
E = 'NY:SSL 137'
add([{'section_id': E, 'decision': 'partial', 'atom_ids': ['NY:CPLR-5205-5231-enforcement-limits'], 'reason': 'The enforcement-limits rule covers exempt direct deposits in bank accounts; SSL 137 exempts public assistance money itself from levy and bars its assignment.', 'proposed': [rule(E,
  id='NY:SSL-137-assistance-exempt', instrument='NY Social Services Law', provision='SSL 137', actor='landlord or its collector enforcing a judgment or taking payment', modality='limit',
  condition='A former tenant who receives public assistance or care under the Social Services Law owes a balance or a judgment.',
  effect='The assistance money and orders cannot be levied on or executed against, and the tenant cannot assign them, so an assignment of the tenant\'s assistance to the landlord for the balance is void and no restraint or execution reaches them. Payments the tenant voluntarily makes are unaffected. The pursue-or-write-off estimate excludes those funds.',
  dependencies=['NY:CPLR-5205-5231-enforcement-limits'],
  quote=q(E, 'All moneys or orders granted to persons as public assistance or care pursuant to this chapter shall be inalienable by any assignment or transfer and shall be exempt from levy and execution under the laws of this state.'),
  severity='major', walk_step='8.12', amends='NY:CPLR-5205-5231-enforcement-limits')]}])
A = 'NY:SSL 137-A'
add([{'section_id': A, 'decision': 'partial', 'atom_ids': ['NY:CPLR-5205-5231-enforcement-limits'], 'reason': 'Adds a full exemption of a public-assistance recipient\'s wages from income execution, beyond the 10% cap the existing rule states.', 'proposed': [rule(A,
  id='NY:SSL-137-a-wages-exempt', instrument='NY Social Services Law', provision='SSL 137-a(1)-(2)', actor='landlord or its collector enforcing a judgment', modality='limit',
  condition='The landlord enforces a judgment against a former tenant who, while employed, receives public assistance or care supplementing wages (including SSI and additional state payments), or would need it if the execution were enforced.',
  effect='The tenant\'s wages are exempt from income execution, installment payment order and assignment for as long as the assistance continues or would be needed; the judgment itself remains valid. An employer notified in writing by the social services official that withholds anyway is liable to the tenant for the amount. Execution may start or resume once the official notifies the employer that the need has ended.',
  dependencies=['NY:CPLR-5205-5231-enforcement-limits'],
  quote=q(A, 'shall be exempt from assignment, income execution or from an installment payment order under the laws of this state but only so long as such public assistance or care, shall continue or would be needed if the assignment, income execution or installment payment order were enforced.'),
  severity='major', walk_step='8.12', amends='NY:CPLR-5205-5231-enforcement-limits')]}])
