import sys; sys.path.insert(0, 'register/work'); from q4_lib import *
SS = {'source_file': 'sources/REVIEW4B_NY_CASE_SmallStep_v_BroadwayBushwick_2016_2dDept.txt', 'quote': 'Failure to comply with these requirements precludes a limited liability company from maintaining any action or special proceeding in New York'}
REASON = 'The publication-suspension clause uses the same words as LLC Law 206, which the Appellate Division reads as barring the entity from maintaining an action while suspended (NY:LLC-206-publication-suspension); the savings clause preserves contracts, the other party\'s suits and the entity\'s defense, and filing proof annuls the suspension.'
N = 'NY:N-PCL 1313'
add([{'section_id': N, 'decision': 'partial', 'atom_ids': ['NY:BCL-1312(a)-foreign-authority'], 'reason': 'The BCL rule covers business corporations; a foreign not-for-profit corporation owner is under the parallel N-PCL bar, which also requires paying back fees and taxes and binds successors.', 'proposed': [rule(N,
  id='NY:NPCL-1313-foreign-authority', instrument='NY Not-for-Profit Corporation Law', provision='N-PCL 1313(a)-(b)', actor='owner (foreign not-for-profit corporation) or a collector suing in its name', modality='precondition',
  determinacy='MIXED', judgment_terms=['conducting activities in this state'],
  condition='The owner is a not-for-profit corporation formed outside New York that conducts activities in New York (for example regularly leasing NYC units) without New York authority, and it or a collector in its name sues a former tenant.',
  effect='It cannot maintain the suit until it is authorized to conduct activities in New York and has paid all fees, penalties and franchise taxes for the unauthorized period; the bar also binds a successor in interest (for example an assignee of the claim). The lack of authority does not impair the lease or the deposit statement, the tenant\'s right to sue it, or its defense of the tenant\'s suit.',
  dependencies=['NY:BCL-1312(a)-foreign-authority'],
  quote=q(N, 'A foreign corporation conducting activities in this state without authority shall not maintain any action or special proceeding in this state unless and until such corporation has been authorized to conduct activities in this state'),
  severity='critical', walk_step='8.10', amends='NY:BCL-1312(a)-foreign-authority')]}])
L = 'NY:LLC Law 802'
add([{'section_id': L, 'decision': 'partial', 'atom_ids': ['NY:LLC-808(a)-foreign-authority', 'NY:LLC-206-publication-suspension'], 'reason': 'A foreign LLC with authority but no proof of publication within 120 days has its authority suspended, the same bar the files state for New York LLCs under 206.', 'proposed': [rule(L,
  id='NY:LLC-802-foreign-publication-suspension', instrument='NY Limited Liability Company Law', provision='LLC Law 802(b)', actor='owner (foreign LLC) or a collector suing in its name', modality='precondition',
  condition='The owner is a foreign LLC that obtained New York authority but did not file proof of publication with the Department of State within 120 days after filing its application (or, for older companies, within the period the section sets), and it or a collector in its name sues a former tenant.',
  effect='Its authority to do business in New York is suspended, and while suspended it cannot maintain the action; the suit is dismissed on motion unless cured. Filing proof of publication at any time annuls the suspension. The suspension does not impair the lease, the deposit statement, the tenant\'s right to sue it, or its defense of the tenant\'s suit, and does not make members or managers liable. Operator step: confirm the publication filing before suing.',
  dependencies=['NY:LLC-808(a)-foreign-authority', 'NY:LLC-206-publication-suspension'],
  quote=q(L, 'the authority of such foreign limited liability company to carry on, conduct or transact any business in this state shall be suspended, effective as of the expiration of such one hundred twenty day period.'),
  construction=[SS], reasoning=REASON, severity='critical', walk_step='8.10', amends='NY:LLC-808(a)-foreign-authority')]}])
P7 = 'NY:Partnership Law 121-907'
add([{'section_id': P7, 'decision': 'new_rule', 'reason': 'Capacity bar for a foreign limited partnership owner, parallel to the LLC and corporation rules, which no rule states.', 'proposed': [rule(P7,
  id='NY:PTR-121-907-foreign-lp-authority', instrument='NY Partnership Law art. 8-A (Revised Limited Partnership Act)', provision='Partnership Law 121-907(a)-(c)', actor='owner (foreign limited partnership) or a collector suing in its name', modality='precondition',
  determinacy='MIXED', judgment_terms=['doing business in this state'],
  condition='The owner is a limited partnership formed outside New York that does business in New York (for example regularly leasing NYC units) without a New York certificate of authority, and it or a collector in its name sues a former tenant.',
  effect='It may not maintain the suit until it receives a certificate of authority. The lack of authority does not impair the lease, the deposit statement or its defense of the tenant\'s suit, and by doing business it appoints the Secretary of State to receive the tenant\'s process.',
  dependencies=['NY:LLC-808(a)-foreign-authority'],
  quote=q(P7, 'A foreign limited partnership doing business in this state without having received a certificate of authority to do business in this state may not maintain any action, suit or special proceeding in any court of this state unless and until such partnership shall have received a certificate of authority in this state.'),
  severity='critical', walk_step='8.10')]}])
P2 = 'NY:Partnership Law 121-902'
add([{'section_id': P2, 'decision': 'new_rule', 'reason': 'A foreign limited partnership with authority but no proof of publication is suspended and cannot sue, like the LLC rules.', 'proposed': [rule(P2,
  id='NY:PTR-121-902-foreign-lp-publication', instrument='NY Partnership Law art. 8-A (Revised Limited Partnership Act)', provision='Partnership Law 121-902', actor='owner (foreign limited partnership) or a collector suing in its name', modality='precondition',
  condition='The owner is a foreign limited partnership authorized in New York that did not file proof of publication within 120 days after its application for authority (or within the period the section sets for older partnerships), and it or a collector in its name sues a former tenant.',
  effect='Its authority is suspended and while suspended it cannot maintain the action; filing proof of publication at any time annuls the suspension. The lease, the deposit statement, the tenant\'s suits and the partnership\'s defense are unaffected, and partners do not become liable.',
  dependencies=['NY:PTR-121-907-foreign-lp-authority', 'NY:LLC-206-publication-suspension'],
  quote=q(P2, 'the authority of such foreign limited partnership to carry on, conduct or transact any business in this state shall be suspended, effective as of the expiration of such one hundred twenty day period.'),
  construction=[SS], reasoning=REASON, severity='critical', walk_step='8.10')]}])
P0 = 'NY:Partnership Law 121-1500'
add([{'section_id': P0, 'decision': 'new_rule', 'reason': 'A New York registered LLP owner that did not file proof of publication is suspended and cannot sue until cured.', 'proposed': [rule(P0,
  id='NY:PTR-121-1500-llp-publication', instrument='NY Partnership Law art. 8-B (limited liability partnerships)', provision='Partnership Law 121-1500(a)(II)', actor='owner (New York registered LLP) or a collector suing in its name', modality='precondition',
  condition='The owner is a New York registered limited liability partnership that did not file proof of publication within 120 days after its registration took effect (or within the period the section sets for older partnerships), and it or a collector in its name sues a former tenant.',
  effect='Its authority to do business is suspended and while suspended it cannot maintain the action; filing proof of publication at any time annuls the suspension. The lease, the deposit statement, the tenant\'s suits and the partnership\'s defense are unaffected, and partners do not become liable by reason of it.',
  dependencies=['NY:LLC-206-publication-suspension'],
  quote=q(P0, 'the authority of such registered limited liability partnership to carry on, conduct or transact any business in this state shall be suspended, effective as of the expiration of such one hundred twenty day period.'),
  construction=[SS], reasoning=REASON, severity='critical', walk_step='8.10')]}])
P1 = 'NY:Partnership Law 121-1502'
add([{'section_id': P1, 'decision': 'new_rule', 'reason': 'A foreign LLP doing business without its New York notice, or with its authority suspended for want of publication, cannot sue until cured.', 'proposed': [rule(P1,
  id='NY:PTR-121-1502-foreign-llp', instrument='NY Partnership Law art. 8-B (limited liability partnerships)', provision='Partnership Law 121-1502', actor='owner (foreign LLP) or a collector suing in its name', modality='precondition',
  determinacy='MIXED', judgment_terms=['carrying on or conducting or transacting business or activities in this state'],
  condition='The owner is a limited liability partnership formed outside New York that carries on business in New York (for example regularly leasing NYC units), and it or a collector in its name sues a former tenant. Branch (a): it has not filed the New York notice. Branch (b): it filed the notice but did not file proof of publication within 120 days.',
  effect='(a) It may not maintain the suit until it files the notice, pays all fees it would have owed, and files proof of publication. (b) Its authority is suspended and it cannot maintain the suit until proof of publication is filed, which annuls the suspension. In both branches the lease, the deposit statement and its defense of the tenant\'s suit are unaffected.',
  dependencies=['NY:LLC-808(a)-foreign-authority', 'NY:LLC-206-publication-suspension'],
  quote=q(P1, 'may not maintain any action, suit or special proceeding in any court of this state unless and until such foreign limited liability partnership shall have filed such notice and paid all fees'),
  construction=[SS], reasoning=REASON, severity='critical', walk_step='8.10')]}])
PA = 'NY:Partnership Law 121-104-A'
add([{'section_id': PA, 'decision': 'new_rule', 'reason': 'A limited partnership whose process address resigned and was not replaced has its authority suspended, which bars it from suing a former tenant until it files a new address.', 'proposed': [rule(PA,
  id='NY:PTR-121-104-a-process-address-suspension', instrument='NY Partnership Law art. 8-A (Revised Limited Partnership Act)', provision='Partnership Law 121-104-a', actor='owner (domestic or foreign limited partnership) or a collector suing in its name', modality='precondition',
  condition='The party whose address the owner limited partnership designated for service of process filed a certificate of resignation, and the partnership has not filed a certificate designating a new address, when it or a collector in its name sues a former tenant.',
  effect='The partnership\'s authority to do business in New York is suspended, so it cannot maintain the suit until it files the certificate designating a new address, which ends the suspension; process against it may meanwhile be served on the Secretary of State. The lease and deposit statement are unaffected.',
  dependencies=['NY:PTR-121-907-foreign-lp-authority'],
  quote=q(PA, 'Upon the failure of the designating limited partnership to file a certificate of amendment or change providing for the designation by the limited partnership of the new address after the filing of a certificate of resignation for receipt of process with the secretary of state, its authority to do business in this state shall be suspended.'),
  construction=[SS], reasoning='Suspension of authority to do business bars maintaining an action as with the publication suspensions (NY:LLC-206-publication-suspension); the section itself provides for service on the Secretary of State while suspended.',
  severity='major', walk_step='8.10')]}])
M = 'NY:Partnership Law 121-1104'
add([{'section_id': M, 'decision': 'new_rule', 'reason': 'Decides who owns the balance and owes the refund when the owner limited partnership merges mid-settlement.', 'proposed': [rule(M,
  id='NY:PTR-121-1104-merger-successor', instrument='NY Partnership Law art. 8-A (Revised Limited Partnership Act)', provision='Partnership Law 121-1104(a), (c), (d)', actor='landlord (surviving limited partnership)', modality='succession',
  condition='The owner limited partnership merges or consolidates into another limited partnership before the departing tenant\'s account is closed.',
  effect='The building, the deposit held in trust and the claim for the balance vest in the surviving or resulting partnership, which is liable for the refund, the statement and every deposit obligation as if it had incurred them; statements and suits proceed in its name, and a pending suit by or against the old partnership continues against or by the survivor.',
  dependencies=['NY:GOL-7-103(1)-trust', 'NY:GOL-7-108(1-a)(e)'],
  quote=q(M, 'the surviving or resulting limited partnership shall be liable for all debts, obligations, liabilities and penalties of each constituent limited partnership as though each such debt, obligation, liability or penalty had been originally incurred by such surviving or resulting limited partnership'),
  severity='major', walk_step='2.1')]}])
add([
 nd('NY:N-PCL 1315', 'When non-residents may sue a foreign not-for-profit corporation; a former tenant\'s claim on an NYC lease qualifies, so nothing changes.'),
 nd('NY:N-PCL 1312', 'Filing of a foreign not-for-profit corporation\'s termination and continued service on the Secretary of State; affects service of the tenant\'s process, not a settlement step.'),
 nd('NY:N-PCL 1314', 'A foreign not-for-profit corporation sues like a domestic one except as statute prescribes; the statutory bar is proposed at N-PCL 1313.'),
 nd('NY:N-PCL 1320', 'Lists internal-governance provisions (derivative suits, indemnification, mergers) applied to foreign not-for-profits.'),
 nd('NY:BCL 1311', 'Filing of a foreign corporation\'s termination and continued service on the Secretary of State; service of the tenant\'s process, not a settlement step.'),
 nd('NY:BCL 1319', 'Lists shareholder and governance provisions applied to foreign corporations; internal governance.'),
 nd('NY:LLC Law 202', 'General powers of an LLC to sue, hold and lease property; the limits that decide whether an owner LLC may sue are stated in NY:LLC-808(a)-foreign-authority and NY:LLC-206-publication-suspension.'),
 nd('NY:LLC Law 210', 'Liability for false statements in filed LLC articles; not a tenancy settlement matter.'),
 nd('NY:LLC Law 215', 'Beneficial ownership disclosure by LLCs (marked effective and repealed 2026-01-01); a past-due or delinquent status is a record notation and bars no suit or collection.'),
 nd('NY:LLC Law 807', 'Filing of a foreign LLC\'s termination and continued service on the Secretary of State; service of the tenant\'s process, not a settlement step.'),
 nd('NY:Partnership Law 121-1001', 'A limited partner is not a proper party to suits by or against the partnership; the owner partnership sues and is sued in its own name, which no rule contradicts.'),
 nd('NY:Partnership Law 121-703', 'Charging orders against a partner\'s interest for the partner\'s own creditors; not a tenancy matter.'),
 nd('NY:Partnership Law 121-706', 'A deceased or incompetent partner\'s representative exercises the partner\'s rights in the partnership; the owner partnership\'s claims and duties are unaffected.'),
 nd('NY:Partnership Law 121-906', 'Filing of a foreign limited partnership\'s termination; affects service of the tenant\'s process, not a settlement step.'),
 nd('NY:Partnership Law 121-109', 'How process is served on a limited partnership through the Secretary of State; service on the owner is the tenant\'s step, and the landlord\'s own capacity rules are proposed at 121-907 and 121-902.'),
 nd('NY:Partnership Law 121-109-A', 'Optional electronic service of process on partnerships; service mechanics.'),
 nd('NY:Partnership Law 121-1505', 'Service of process on registered LLPs through the Secretary of State; service mechanics.'),
 nd('NY:Partnership Law 121-1505-A', 'Optional electronic service of process on LLPs; service mechanics.'),
])
