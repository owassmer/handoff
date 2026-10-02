import sys; sys.path.insert(0, 'register/work'); from q4_lib import *
D = 'NY:Military Law 301'
add([{'section_id': D, 'decision': 'partial', 'atom_ids': ['NY:MIL-310(2)', 'NY:MIL-323-a-6pct', 'NY:MIL-306-309'], 'reason': 'The state article 13 rules depend on this definition, and it reaches New York state active duty and national guard state duty that the federal SCRA does not, so it widens who gets the state protections.', 'proposed': [rule(D,
  id='NY:MIL-301-military-service', instrument='NY Military Law art. 13', provision='Military Law 301(1)-(2)', actor='landlord, managing agent or collector', modality='definition',
  condition='Deciding whether a tenant, co-tenant or guarantor is a person in military service for a New York article 13 protection (lease termination 310, 6% cap 323-a, stays 304-309, penalty relief 305, relief 323, storage liens 316-a, no-waiver 318).',
  effect='Military service means: active military service of the United States; active duty in the state\'s military service on the Governor\'s order; and state active duty of national guard members activated by the Governor of New York or of another state. A guardsman on state active duty therefore has the article 13 protections even where the federal SCRA does not apply (US:50USC3911(1)-(2)). \'Person\' holding a right against the servicemember includes individuals, partnerships, corporations and other business associations, so an owner LLC or corporation is bound.',
  dependencies=['NY:MIL-310(2)', 'NY:MIL-323-a-6pct', 'US:50USC3911(1)-(2)'],
  quote=q(D, 'and state active duty by members of the national guard who are activated pursuant to a call of the governor of this state or of any other state as provided for by law.'),
  severity='critical', walk_step='0.6')]}])
add([
 nd('NY:Military Law 300', 'Legislative findings for article 13.'),
 nd('NY:Military Law 311-A', 'Termination of motor vehicle leases by servicemembers; not a residential lease.'),
 nd('NY:Military Law 311-C', 'Termination of telecom, internet, health club and TV contracts; not a residential lease.'),
 nd('NY:Military Law 315', 'Deferral of state income tax for servicemembers; not part of a tenancy settlement.'),
 nd('NY:Military Law 317', 'Reemployment rights of servicemembers; employment law.'),
 nd('NY:Military Law 325', 'Article 13 controls over inconsistent laws; the article\'s rules are stated to apply on their own terms, and no conflict with the deposit or collection rules changes a step.'),
 nd('NY:Military Law 308-A', 'Waiver of professional continuing education during service; licensing, not tenancy.'),
 nd('NY:Military Law 308-B', 'Extension of professional licences during active duty; licensing, not tenancy.'),
 nd('NY:Military Law 316', 'Life insurance policies of servicemembers do not lapse; not a tenancy matter.'),
 nd('NY:Military Law 316-B', 'Suspension of professional liability insurance during active duty; not a tenancy matter.'),
 nd('NY:Military Law 322', 'Courts may revoke or modify their interlocutory article 13 orders; court procedure.'),
 nd('NY:Military Law 324', 'Severability clause.'),
 nd('NY:Military Law 327', 'Article 13 stays in force until repealed, which is why its rules carry no end date; nothing else changes.'),
])
