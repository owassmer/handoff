import sys; sys.path.insert(0, 'register/work'); from q4_lib import *
EP = 'NY Estates, Powers and Trusts Law'
add([
 nd('NY:UCC 1-108', 'Relates UCC article 1 to E-SIGN for UCC records; the electronic statement and notices in the chain are governed by NY:ADJ-statement-electronic and US:15USC7001(c)-esign-consent, which this section leaves untouched.'),
 nd('NY:UCC 1-301', 'Choice of law for UCC transactions; a check drawn or taken in settling an NYC lease is governed by New York law under either branch, so no settlement step changes.'),
 nd('NY:UCC 1-302', 'Freedom to vary UCC provisions except good faith; the lease is not a UCC transaction, and NY:UCC-1-308-full-payment-check turns on the reservation made at acceptance, not on a prior agreement.'),
 nd('NY:UCC 1-304', 'Good faith in contracts within the UCC; the lease is outside the UCC, and no settlement step on a check turns on it beyond NY:UCC-1-308-full-payment-check.'),
 nd('NY:UCC 1-305', 'Remedies under the UCC are compensatory; no lease or deposit remedy arises under the UCC.'),
 nd('NY:UCC 1-306', 'Discharge without consideration of a claim arising from breach of a UCC transaction; releasing or writing off a lease balance is governed by the General Obligations Law (NY:GOL-15-104-105-cotenant-release), not the UCC.'),
 nd('NY:UCC 3-307', 'Burden of proving signatures in a suit on an instrument; a deposit or balance claim is a suit on the lease.'),
 nd('NY:UCC 3-408', 'A check given for an existing balance needs no new consideration; the landlord\'s rights on a dishonored payment are decided under UCC 3-802 (decided there).'),
 {'section_id': 'NY:BCL 1313', 'decision': 'stated', 'atom_ids': ['NY:BCL-1312(a)-foreign-authority'], 'reason': 'A foreign corporation sues like a domestic one except as statute prescribes; the statutory bar that matters (authority to do business) is the stated rule.'},
 nd('NY:BCL 1314', 'Lists when non-residents may sue a foreign corporation in New York; a former tenant\'s claim on an NYC lease qualifies under (b)(1)-(3), so nothing in the landlord\'s decisions changes.'),
 nd('NY:EPTL 11-3.3', 'Damages when an injury causes death (wrongful death); not a tenancy settlement claim.'),
 nd('NY:EPTL 11-4.1', 'Suits by or against a personal representative are brought in the representative capacity; a pleading form. That claims run against the fiduciary is stated in NY:ADJ-tenant-death-payee.'),
 nd('NY:EPTL 11-4.2', 'Joinder of personal and representative claims against a fiduciary; pleading mechanics.'),
 nd('NY:EPTL 11-4.3', 'Separate docketing of the personal part of a judgment against a fiduciary; enforcement mechanics with no effect on the lease claim.'),
 nd('NY:EPTL 11-4.4', 'Service on one of several co-representatives gives jurisdiction over all; service mechanics.'),
 nd('NY:EPTL 11-4.5', 'A fiduciary may not plead want of assets against a money claim; recovery is limited at execution (proposed NY:EPTL-11-4.6-execution-leave), so the claim decision does not change.'),
 nd('NY:EPTL 13-1.3', 'Which estate assets pay estate debts and the order in which gifts abate; internal administration among beneficiaries. The landlord\'s claim rank is proposed at SCPA 1811.'),
 nd('NY:EPTL 13-3.5', 'Filing duties when a foreign representative sues in New York; the landlord\'s payment decision toward a foreign fiduciary is proposed at EPTL 13-3.4.'),
 nd('NY:EPTL 13-3.6', 'A fiduciary or a creditor with a claim over $100 against an insolvent estate may set aside fraudulent transfers; an extraordinary creditor remedy that changes no step in presenting or pricing the claim (NY:SCPA-1811-claim-priority).'),
 {'section_id': 'NY:EPTL 4-1.5', 'decision': 'stated', 'atom_ids': ['NY:ABP-1315(2)', 'NY:OSC-MS11-refunds-due'], 'reason': 'A refund owed to a decedent with no heir passes to the State as abandoned property; the unclaimed-refund rules already send it to the Comptroller.'},
])
E = 'NY:EPTL 11-1.1'
add([{'section_id': E, 'decision': 'partial', 'atom_ids': ['NY:COMMONLAW-owner-death-agency', 'NY:ADJ-tenant-death-payee'], 'reason': '(b)(5)(A) is the rent-collection power the owner-death rule relies on; (b)(11)-(13) add that a surviving or successor fiduciary may be paid and that any fiduciary may compromise the claim, which the rules do not say.', 'proposed': [rule(E,
  id='NY:EPTL-11-1.1-fiduciary-powers', instrument=EP, provision='EPTL 11-1.1(b)(5)(A), (11)-(13)', actor='landlord or managing agent dealing with an estate', modality='permission',
  condition='The deceased is the owner or the former tenant, and an executor or administrator (or several) holds letters, unless the will or the court order limits these powers.',
  effect='(a) Owner\'s estate: the fiduciary may take possession of, collect the rents from and manage a building that the will does not specifically dispose of; so rent, the departing tenant\'s balance and the deposit refund are dealt with through the fiduciary (NY:COMMONLAW-owner-death-agency). (b) Surviving and successor fiduciaries: if one of several fiduciaries stops acting, the survivor alone may collect, pay and settle; a successor or substitute fiduciary has all the original fiduciary\'s powers, so the refund or claim is dealt with through the successor. (c) Any fiduciary may contest, compromise or settle a claim for or against the estate, so the landlord may settle the balance, or the tenant\'s deposit claim, with the fiduciary alone.',
  dependencies=['NY:COMMONLAW-owner-death-agency', 'NY:ADJ-tenant-death-payee'],
  quote=q(E, 'To contest, compromise or otherwise settle any claim in favor of the estate, trust or fiduciary or in favor of third persons and against the estate, trust or fiduciary.'),
  construction=[{'source_file': 'register/texts/NY_EPTL/11-1.1.txt', 'quote': q(E, 'As successor or substitute fiduciary, to succeed to all of the powers, duties and discretion of the original fiduciary')},
                {'source_file': 'register/texts/NY_EPTL/11-1.1.txt', 'quote': q(E, 'In the case of the survivor of two or more fiduciaries, to continue to administer the property of the estate or trust without the appointment of a successor')}],
  reasoning='The powers apply to every fiduciary unless the will or order limits them.',
  severity='critical', walk_step='2.5', amends='NY:ADJ-tenant-death-payee')]}])
R = 'NY:EPTL 11-3.4'
add([{'section_id': R, 'decision': 'partial', 'atom_ids': ['NY:ADJ-tenant-death-payee'], 'reason': 'Decides who may not be paid when the tenant\'s fiduciary itself dies: the fiduciary\'s own representative has no authority over the first estate.', 'proposed': [rule(R,
  id='NY:EPTL-11-3.4-no-representative-of-representative', instrument=EP, provision='EPTL 11-3.4', actor='landlord or managing agent', modality='prohibition',
  condition='The executor or administrator of a deceased former tenant (or of a deceased owner) dies or leaves office before the refund is paid or the balance is settled.',
  effect='The personal representative of that fiduciary has no authority over the first estate: it may not collect the refund, sue on the tenant\'s deposit claim, or receive the balance, and paying it does not discharge the landlord. Deal instead with a surviving co-fiduciary (NY:EPTL-11-1.1-fiduciary-powers) or a successor appointed by the court (administrator de bonis non).',
  dependencies=['NY:ADJ-tenant-death-payee', 'NY:EPTL-11-1.1-fiduciary-powers'],
  quote=q(R, 'a personal representative of a personal representative has no authority to commence or maintain any action or proceeding relating to the estate, effects or rights of the decedent of the first representative, or to take any charge or control thereof, as such representative.'),
  severity='critical', walk_step='2.5', amends='NY:ADJ-tenant-death-payee')]}])
A = 'NY:EPTL 13-1.1'
add([{'section_id': A, 'decision': 'partial', 'atom_ids': ['NY:COMMONLAW-owner-death-agency', 'NY:RPL-236'], 'reason': 'Decides who owns rent accrued before an owner\'s death and that a deceased tenant\'s leasehold passes to its personal representative; the owner-death rule does not split accrued from later rent.', 'proposed': [rule(A,
  id='NY:EPTL-13-1.1-accrued-rent-leasehold', instrument=EP, provision='EPTL 13-1.1(a)(1), (6)', actor='landlord, managing agent, or the estate', modality='ownership',
  condition='Branch (a): an individual owner dies while the departing tenant owes rent. Branch (b): the tenant dies during the lease term.',
  effect='(a) Rent that had accrued (fallen due) before the owner\'s death is personal property that passes to the owner\'s personal representative, even if the building is specifically devised; rent falling due after the death goes with the building to the devisee or distributees, and the fiduciary collects it where the building is not specifically devised (NY:EPTL-11-1.1-fiduciary-powers). The statement\'s rent lines are therefore credited to the payee that owns each period. (b) The tenant\'s estate for years under the lease is personal property that passes to the tenant\'s personal representative, who exercises the lease rights on the estate\'s behalf (assignment request or termination: NY:RPL-236, NY:RPL-236-a).',
  dependencies=['NY:COMMONLAW-owner-death-agency', 'NY:RPL-236', 'NY:RPL-236-a'],
  quote=q(A, 'Rent reserved to the decedent which had accrued at the time of his death.'),
  construction=[{'source_file': 'register/texts/NY_EPTL/13-1.1.txt', 'quote': q(A, 'Estates for years in real property, estates from year to year and estates which were held by the decedent for the life of another person.')},
                {'source_file': 'register/texts/NY_EPTL/13-1.1.txt', 'quote': q(A, 'All other fixtures annexed to land or structures do not pass to the personal representative, but descend to the distributees or pass to the devisees.')}],
  reasoning='13-1.1 classes accrued rent and leaseholds as personal property passing to the personal representative; real property itself descends or passes to devisees, so rent accruing on it after death follows it, subject to the fiduciary\'s statutory rent-collection power over property not specifically devised.',
  severity='critical', walk_step='0.5', amends='NY:COMMONLAW-owner-death-agency')]}])
F = 'NY:EPTL 13-3.4'
add([{'section_id': F, 'decision': 'partial', 'atom_ids': ['NY:ADJ-tenant-death-payee'], 'reason': 'Adds who may be paid when the tenant was domiciled outside New York at death (a foreign fiduciary) and when that payment discharges.', 'proposed': [rule(F,
  id='NY:EPTL-13-3.4-foreign-fiduciary', instrument=EP, provision='EPTL 13-3.4(a)-(b)', actor='landlord or managing agent', modality='permission',
  condition='The former tenant (or a tenant who was an infant or incompetent) was domiciled outside New York, and a fiduciary appointed there (executor, administrator, guardian or similar) authorized by that jurisdiction\'s law to receive the tenant\'s personal property asks for the refund.',
  effect='The landlord may pay the refund to the foreign fiduciary without a court order, and its receipt is a complete discharge, unless before paying the landlord received written notice that a principal or ancillary representative was appointed in New York, or that the tenant has creditors in New York; in that case pay the New York representative (NY:ADJ-tenant-death-payee). The landlord\'s own claim for a balance makes it a New York creditor, so where it asserts one it sets it off in the statement before paying and presents any excess claim in New York.',
  dependencies=['NY:ADJ-tenant-death-payee'],
  quote=q(F, 'such person or fiduciary may pay or deliver the property to such foreign fiduciary without an order of the court, and the receipt and acquittance from such foreign fiduciary is a sufficient release and discharge of the person or fiduciary paying or delivering such property.'),
  severity='critical', walk_step='2.5', amends='NY:ADJ-tenant-death-payee')]}])
