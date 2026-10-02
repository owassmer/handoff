import sys; sys.path.insert(0, 'register/work'); from q4_lib import *
S = 'NY:GBL 380-B'
p1 = rule(S, id='NY:GBL-380-b-permissible-purpose', instrument='NY General Business Law art. 25 (Fair Credit Reporting Act)',
  provision='GBL 380-b(a)', actor='landlord, managing agent, Handoff or collector obtaining a consumer report', modality='permission/prohibition',
  condition='A landlord, its manager, Handoff or a collector wants a consumer report on a former tenant (for example to locate the tenant for the statement or refund, or to collect a balance).',
  effect='A New York consumer reporting agency may furnish the report only (1) on a court order, (2) on the former tenant\'s written instructions, or (3) to a person it has reason to believe will use it in connection with the rental or lease of a residence ((a)(3)(vi)), or in a business transaction involving the consumer where the user has a legitimate business need ((a)(3)(v)). Locating a former tenant to deliver the deposit statement or refund, and collecting the lease balance, are uses in connection with the lease of the residence, so the report may be requested for them. A report requested for any other purpose (for example curiosity about a former tenant, or marketing) is outside the permitted purposes. The federal permission runs alongside: US:15USC1681b-1681c-report-limits. Liability for a user\'s violations: NY:GBL-380-l-willful, NY:GBL-380-m-negligent.',
  dependencies=['US:15USC1681b-1681c-report-limits'],
  quote=q(S, 'A consumer reporting agency may furnish a consumer report under the following circumstances and no other:'),
  construction=[{'source_file': 'register/texts/NY_GBL/380-b.txt', 'quote': q(S, 'in connection with the rental or lease of a residence.')}],
  reasoning='(a)(3)(i) needs a credit transaction, which a lease is not (NY:ADJ-lease-balance-not-consumer-credit); (a)(3)(vi) and (v) reach a report used to settle or collect the lease of a residence.',
  severity='major', walk_step='8.7')
L = 'NY:GBL 380-L'
p2 = rule(L, id='NY:GBL-380-l-willful', instrument='NY General Business Law art. 25 (Fair Credit Reporting Act)', provision='GBL 380-l',
  actor='landlord, managing agent, Handoff or collector as user of consumer reports, or as a person giving information to a consumer reporting agency',
  modality='liability', determinacy='MIXED', judgment_terms=['willfully and knowingly fails to comply'],
  condition='A user of consumer report information (a landlord, manager, Handoff or collector who obtained a report on a former tenant) willfully and knowingly fails to comply with a requirement of GBL art. 25 toward that tenant (for example obtaining the report for a purpose 380-b does not permit, or under false pretenses, 380-o); or a person\'s knowing and willful violation of GBL 380-s (identity theft) caused information to be given to a consumer reporting agency that otherwise would not have been.',
  effect='The violator is liable to the former tenant for the sum of actual damages, punitive damages in the amount the court allows (no statutory cap), and, if the tenant succeeds, costs and reasonable attorney\'s fees. The action is brought within the period of GBL 380-n.',
  dependencies=['NY:GBL-380-b-permissible-purpose'],
  quote=q(L, 'any consumer reporting agency or user of information who or which willfully and knowingly fails to comply with any requirement imposed under this article with respect to any consumer is liable to that consumer'),
  severity='critical', walk_step='8.7')
add([
 {'section_id': S, 'decision': 'new_rule', 'reason': 'Fixes when a NY consumer report on a former tenant may be obtained (locating or collecting the lease balance is a permitted lease use); the (b) application notice is move-in screening and changes nothing at settlement.', 'proposed': [p1]},
 {'section_id': L, 'decision': 'new_rule', 'reason': 'State civil liability (actual, uncapped punitive, fees) for a landlord or collector that willfully misuses a consumer report on a former tenant; no rule states it.', 'proposed': [p2]},
])
S2 = 'NY:Military Law 301-B'
add([{'section_id': S2, 'decision': 'new_rule', 'reason': 'Extends the article 13 protections the files apply to the servicemember tenant (310 termination, 323-a 6% cap, stays) to dependents, and obliges the landlord to grant them on the dependent\'s direct application.', 'proposed': [rule(S2,
  id='NY:MIL-301-b-dependents', instrument='NY Military Law art. 13', provision='Military Law 301-b(1)-(2)', actor='landlord or its collector', modality='obligation',
  determinacy='MIXED', judgment_terms=['ability to comply materially impaired by reason of the military service'],
  condition='A tenant or co-tenant is a dependent (for example the spouse or child) of a person in military service (Military Law 301(1)), and claims a benefit of Military Law art. 13 (for example lease termination under 310, the 6% cap under 323-a, relief from penalties under 305). Branch (a): no court proceeding is pending, and the dependent applies to the landlord or collector. Branch (b): a proceeding is pending, and the dependent applies to the court.',
  effect='(a) The landlord or collector must grant the benefit unless the dependent\'s ability to comply with the lease has not been materially impaired by the service; the landlord carries the decision, and the dependent may still apply to a court. (b) The court grants it on the same test. A benefit granted applies to the dependent\'s account as it would to the servicemember\'s (NY:MIL-310(2), NY:MIL-323-a-6pct, NY:MIL-306-309).',
  dependencies=['NY:MIL-310(2)', 'NY:MIL-323-a-6pct', 'NY:MIL-306-309'],
  quote=q(S2, 'Such agency, private party, business or other entity shall grant such entitlement unless the ability of such dependents to comply with the terms of the obligation, contract, lease, or bailment has not been materially impaired by reason of the military service of the person upon whom the applicants are dependent.'),
  severity='critical', walk_step='3.4')]}])
S3 = 'NY:Military Law 302'
add([{'section_id': S3, 'decision': 'partial', 'atom_ids': ['NY:MIL-306-309'], 'reason': 'NY:MIL-306-309 states the stay for the servicemember; 302 adds that a guarantor or co-obligor may be stayed too, and limits a guarantor\'s waiver.', 'proposed': [rule(S3,
  id='NY:MIL-302-guarantor-stay', instrument='NY Military Law art. 13', provision='Military Law 302(1)-(3)', actor='landlord or its collector suing a guarantor or co-obligor', modality='procedure',
  determinacy='MIXED', judgment_terms=['in the discretion of the court'],
  condition='Enforcement of a former tenant\'s balance, or a suit or judgment on it, is stayed, postponed or vacated under Military Law art. 13 because the tenant is in military service, and the landlord pursues a guarantor, surety, endorser or other person liable on the same obligation.',
  effect='The court may extend the stay, postponement or vacatur to the guarantor or other obligor. A guarantor\'s written waiver of that protection is valid only if it is an instrument separate from the lease or guaranty, and a waiver is never valid after the start of military service if the guarantor signed it and later entered service.',
  dependencies=['NY:MIL-306-309', 'NY:GOL-5-701(a)(2)-guaranty'],
  quote=q(S3, 'such stay, postponement or suspension may, in the discretion of the court, likewise be granted to sureties, guarantors, endorsers and others subject to the obligation or liability'),
  severity='major', walk_step='8.10', amends='NY:MIL-306-309')]}])
S4 = 'NY:Military Law 304'
add([{'section_id': S4, 'decision': 'partial', 'atom_ids': ['NY:MIL-306-309'], 'reason': 'NY:MIL-306-309 says a suit may be stayed; 304 makes the stay mandatory on the servicemember\'s application unless its ability to defend is not materially affected.', 'proposed': [rule(S4,
  id='NY:MIL-304-stay-on-application', instrument='NY Military Law art. 13', provision='Military Law 304', actor='landlord or its collector suing', modality='procedure',
  determinacy='MIXED', judgment_terms=['ability to conduct the defense materially affected by reason of military service'],
  condition='The landlord or a collector sues a former tenant (or pursues any court or agency proceeding) while the tenant is in military service or within sixty days after.',
  effect='The court may stay the action on its own motion at any stage, and must stay it on the tenant\'s application (or one made on its behalf) unless it finds the tenant\'s ability to defend is not materially affected by the service. Duration and terms: NY:MIL-307-stay-terms.',
  dependencies=['NY:MIL-306-309'],
  quote=q(S4, 'shall, on application to it by such person or some person on his behalf, be stayed as provided in this act, unless, in the opinion of the court'),
  severity='major', walk_step='8.10', amends='NY:MIL-306-309')]}])
S5 = 'NY:Military Law 305'
add([{'section_id': S5, 'decision': 'new_rule', 'reason': 'Stops late fees and other contract penalties accruing during a military stay and lets a court relieve penalties incurred during service; changes what may be charged.', 'proposed': [rule(S5,
  id='NY:MIL-305-penalty-relief', instrument='NY Military Law art. 13', provision='Military Law 305', actor='landlord or its collector', modality='prohibition',
  determinacy='MIXED', judgment_terms=['ability to pay or perform materially impaired by reason of such service', 'on such terms as may be just'],
  condition='A former tenant in military service owes a lease balance on which a fine or penalty (for example a late fee or a lease-break penalty) is claimed. Branch (a): an action on the lease is stayed under article 13. Branch (b): no stay, but the penalty was incurred while the tenant was in service.',
  effect='(a) No fine or penalty accrues for non-performance during the stay, so none is added to the account for that period. (b) A court may relieve the tenant of the penalty on just terms if the tenant was in service when it was incurred and the service materially impaired the ability to pay or perform.',
  dependencies=['NY:MIL-304-stay-on-application', 'NY:RPL-238-a(2)'],
  quote=q(S5, 'no fine or penalty shall accrue by reason of failure to comply with the terms of such contract during the period of such stay'),
  severity='major', walk_step='8.10')]}])
S6 = 'NY:Military Law 307'
add([{'section_id': S6, 'decision': 'partial', 'atom_ids': ['NY:MIL-306-309'], 'reason': 'Adds the stay\'s maximum length, installment terms and the right to proceed against co-defendants by leave.', 'proposed': [rule(S6,
  id='NY:MIL-307-stay-terms', instrument='NY Military Law art. 13', provision='Military Law 307', actor='landlord or its collector suing', modality='procedure',
  determinacy='MIXED', judgment_terms=['subject to such terms as may be just'],
  condition='A court stays the landlord\'s action, attachment or execution against a former tenant in military service under article 13.',
  effect='The stay may run for the period of service plus three months, or any part of it, on terms the court fixes, including payment of the balance in installments. If co-tenants or guarantors are co-defendants, the landlord may proceed against them with the court\'s leave.',
  dependencies=['NY:MIL-304-stay-on-application', 'NY:MIL-306-309'],
  quote=q(S6, 'Where the person in military service is a codefendant with others the plaintiff may nevertheless, by leave of court, proceed against the others.'),
  severity='major', walk_step='8.10', amends='NY:MIL-306-309')]}])
add([nd('NY:Military Law 311-B', 'Covers rental contracts for goods or services not otherwise addressed by article 13; a dwelling lease is addressed by Military Law 310 (NY:MIL-310(2)).')])
