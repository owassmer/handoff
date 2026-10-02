import sys; sys.path.insert(0, 'register/work'); from q4_lib import *
MH = 'NY Mental Hygiene Law art. 81 (guardianship)'
G = 'NY:MHL 81.21'
add([{'section_id': G, 'decision': 'new_rule', 'reason': 'Decides who receives the statement and refund, who may settle or pay the balance, and who is sued, when the tenant has a property-management guardian; no rule covers an incapacitated tenant beyond CPLR 1203 defaults.', 'proposed': [rule(G,
  id='NY:MHL-81.21-guardian-property-powers', instrument=MH, provision='MHL 81.21(a)(5), (13), (15), (17), (19), (20); 81.29(a), (c)', actor='landlord, managing agent, Handoff or collector', modality='obligation',
  condition='The departing tenant (or a co-tenant) has a guardian appointed under MHL article 81 whose commission grants powers over property management.',
  effect='Deal with the guardian within the powers its commission lists (NY:MHL-81.27-commission): (a) with power to marshal assets, send the itemized statement to the guardian as well as the tenant and pay the refund to the guardian for the tenant; title to the refund stays the tenant\'s, and payment to the guardian within its powers discharges the landlord; (b) with power to pay bills or enter contracts, the guardian may pay or settle the balance and agree a payment plan or release; (c) with power to lease the primary residence, the guardian may enter or end the lease (up to three years); (d) the guardian may defend or maintain a suit on the deposit or balance; a suit against the tenant is brought against the tenant with the guardian appearing (NY:CPLR-1203-1015-5208-parties). Where the commission does not grant the power in question, the tenant keeps it and deals for itself (NY:MHL-81.29-retained-rights). After the tenant\'s death the guardian may pay bills it was authorized to pay and continue a pending suit only until an executor or temporary administrator is appointed (NY:MHL-81.44-death-of-ward).',
  dependencies=['NY:CPLR-1203-1015-5208-parties', 'NY:GOL-7-108(1-a)(e)'],
  quote=q(G, 'the court may authorize the guardian to exercise those powers necessary and sufficient to manage the property and financial affairs of the incapacitated person'),
  construction=[{'source_file': 'register/texts/NY_MHY/81.21.txt', 'quote': q(G, 'pay bills after the death of the incapacitated person provided the authority existed to pay such bills prior to death until a temporary administrator or executor is appointed')},
                {'source_file': 'register/texts/NY_MHY/81.21.txt', 'quote': q(G, 'defend or maintain any judicial action or proceeding to a conclusion until an executor or administrator is appointed.')}],
  reasoning='Article 81 guardians hold only the powers the court grants and the commission lists; property of the incapacitated person stays titled in that person.',
  severity='critical', walk_step='6.5')]}])
R = 'NY:MHL 81.29'
add([{'section_id': R, 'decision': 'new_rule', 'reason': 'Decides that an incapacitated tenant keeps every right not granted to the guardian, and that a court may revoke contracts the tenant made while incapacitated (a lease, move-out agreement or release).', 'proposed': [rule(R,
  id='NY:MHL-81.29-retained-rights', instrument=MH, provision='MHL 81.29(a)-(d)', actor='landlord, managing agent, Handoff or collector', modality='applicability',
  condition='The departing tenant has an article 81 guardian, or is later found incapacitated and a guardian is appointed.',
  effect='(a) The tenant keeps every power and right the order does not give the guardian: where the guardian has only personal-needs powers, the tenant receives the statement and refund, settles and is dealt with directly. (b) Title to the tenant\'s property (the deposit refund included) stays in the tenant; the guardian possesses it only as the order directs. (c) The appointment is not conclusive proof that the tenant lacks capacity for other purposes. (d) If the court finds a contract, power of attorney or disposition the tenant made before the appointment was made while incapacitated, it may modify, amend or revoke it; a lease surrender, move-out agreement, payment plan or release the tenant signed while incapacitated can therefore be undone by the guardianship court, and the agent under a revoked power accounts to the guardian.',
  dependencies=['NY:MHL-81.21-guardian-property-powers'],
  quote=q(R, 'An incapacitated person for whom a guardian has been appointed retains all powers and rights except those powers and rights which the guardian is granted.'),
  construction=[{'source_file': 'register/texts/NY_MHY/81.29.txt', 'quote': q(R, 'or any contract, conveyance, or disposition during lifetime or to take effect upon death, made by the incapacitated person prior to the appointment of the guardian if the court finds that the previously executed appointment, power, delegation, contract, conveyance, or disposition during lifetime or to take effect upon death, was made while the person was incapacitated')}],
  reasoning='81.29 limits the guardian to granted powers, keeps title in the person, and lets the court revoke pre-appointment contracts made during incapacity.',
  severity='critical', walk_step='6.5')]}])
C = 'NY:MHL 81.27'
add([{'section_id': C, 'decision': 'new_rule', 'reason': 'The commission is the document that shows a guardian\'s specific powers and end date; dealing with a guardian outside it does not bind the tenant.', 'proposed': [rule(C,
  id='NY:MHL-81.27-commission', instrument=MH, provision='MHL 81.27; 81.26', actor='landlord, managing agent or Handoff', modality='precondition',
  condition='A person presents itself as the guardian of a departing or former tenant and asks for the statement or refund, or offers to pay or settle the balance.',
  effect='Before paying or settling, obtain the guardian\'s commission issued by the court clerk. It states the proceeding, the tenant, the guardian\'s name and contact details, the guardian\'s specific powers, the appointment date and any termination date. Act only within the listed powers and before the termination date (NY:MHL-81.21-guardian-property-powers); no commission issues until the guardian designates the clerk to receive process, so process in a suit may be served on the clerk when the guardian cannot be served in the state.',
  dependencies=['NY:MHL-81.21-guardian-property-powers'],
  quote=q(C, 'the name, address, and telephone number of the guardian and the specific powers of such guardian'),
  severity='major', walk_step='6.5')]}])
T = 'NY:MHL 81.23'
add([{'section_id': T, 'decision': 'new_rule', 'reason': 'A temporary guardian may be the payee or party for a tenant during a pending proceeding, and an injunction may bar anyone from taking property or a confession of judgment from the tenant.', 'proposed': [rule(T,
  id='NY:MHL-81.23-temporary-guardian', instrument=MH, provision='MHL 81.23(a)-(b)', actor='landlord, managing agent, Handoff or collector', modality='obligation',
  condition='A guardianship proceeding for the departing or former tenant is pending.',
  effect='(a) A temporary guardian acts only with the powers its appointment order enumerates, from the issuance of its commission until a guardian\'s commission issues; within those powers it receives the refund or settles as NY:MHL-81.21-guardian-property-powers describes. (b) The court may enjoin any person (the landlord or collector included) from receiving property from the tenant, arranging for another to receive it, or taking a confession of judgment that may become a lien; while such an order is in force, the landlord takes no payment, settlement or confession of judgment from the tenant, and deals only as the order allows.',
  dependencies=['NY:MHL-81.21-guardian-property-powers', 'NY:MHL-81.27-commission'],
  quote=q(T, 'The powers and duties of the temporary guardian shall be specifically enumerated in the order of appointment and are limited in the same manner as are the powers of a guardian appointed pursuant to this article.'),
  severity='major', walk_step='6.5')]}])
S = 'NY:MHL 81.16'
add([{'section_id': S, 'decision': 'new_rule', 'reason': 'A court may, without a guardian, authorize or ratify a single transaction for an incapacitated tenant through a special guardian, who is then the party the landlord deals with for it.', 'proposed': [rule(S,
  id='NY:MHL-81.16-special-guardian', instrument=MH, provision='MHL 81.16(b), (c)', actor='landlord, managing agent, Handoff or collector', modality='obligation',
  condition='A court has found the tenant incapacitated and, instead of appointing a general guardian, authorized, directed or ratified a transaction concerning the tenant\'s property (for example ending the lease, settling the account or receiving the refund), possibly appointing a special guardian for it.',
  effect='The transaction is carried out as the order authorizes: the special guardian has only the authority its order confers, and the refund, settlement or lease termination is dealt with through it on those terms. Any matter outside the order stays with the tenant (NY:MHL-81.29-retained-rights).',
  dependencies=['NY:MHL-81.29-retained-rights'],
  quote=q(S, 'The special guardian shall have the authority conferred by the order of appointment'),
  severity='major', walk_step='6.5')]}])
V = 'NY:MHL 81.38'
add([{'section_id': V, 'decision': 'new_rule', 'reason': 'Decides who acts for an incapacitated tenant when the guardian dies, resigns or is removed mid-settlement: an interim or standby guardian.', 'proposed': [rule(V,
  id='NY:MHL-81.38-interim-standby', instrument=MH, provision='MHL 81.38(a)-(b); 81.37', actor='landlord, managing agent, Handoff or collector', modality='obligation',
  condition='The tenant\'s guardian dies, is removed, discharged, suspended or resigns, or becomes incapacitated, before the statement, refund or balance is settled.',
  effect='The former guardian may no longer act. A standby guardian (or alternate) named in the original order assumes the office at once, subject to court confirmation after sixty days; otherwise the court appoints an interim guardian for ninety days or until a successor is appointed, with the powers its order enumerates. Pay or settle with the standby, interim or successor guardian within its powers (NY:MHL-81.27-commission).',
  dependencies=['NY:MHL-81.21-guardian-property-powers', 'NY:MHL-81.27-commission'],
  quote=q(V, 'shall without further proceedings be empowered to immediately assume the duties of office immediately upon resignation, death, removal, discharge, suspension or adjudication of incapacity, of the guardian'),
  severity='critical', walk_step='6.5')]}])
D = 'NY:MHL 81.44'
add([{'section_id': D, 'decision': 'partial', 'atom_ids': ['NY:ADJ-tenant-death-payee'], 'reason': 'Adds that when a tenant under guardianship dies, the guardian stops being the payee and delivers to the personal representative or public administrator.', 'proposed': [rule(D,
  id='NY:MHL-81.44-death-of-ward', instrument=MH, provision='MHL 81.44(a)-(d); 81.21(a)(19)-(20)', actor='landlord, managing agent or Handoff', modality='obligation',
  condition='A tenant who had an article 81 guardian dies before the refund is paid or the balance settled.',
  effect='The refund is paid to the personal representative of the tenant\'s estate on letters (NY:ADJ-tenant-death-payee), or, where none has been appointed, to the public administrator (or county chief fiscal officer), which holds guardianship property only as stakeholder; not to the guardian. The guardian must within twenty days serve a statement of death and within 150 days deliver guardianship property to the personal representative or public administrator, keeping only what secures known claims. The landlord\'s claim for a balance may be included in the guardian\'s statement of assets and notice of claim, and until an executor or temporary administrator is appointed the guardian may pay the landlord\'s bill if it was authorized to pay such bills before the death.',
  dependencies=['NY:ADJ-tenant-death-payee', 'NY:MHL-81.21-guardian-property-powers', 'NY:SCPA-1112-public-administrator'],
  quote=q(D, 'shall deliver all guardianship property to:'),
  construction=[{'source_file': 'register/texts/NY_MHY/81.44.txt', 'quote': q(D, 'The role of the public administrator under this section is that of a stake holder or escrowee only')}],
  reasoning='81.44 routes guardianship property to the personal representative or the public administrator after death; 81.21(a)(19)-(20) keeps only bill-paying and pending-suit authority until an executor is appointed.',
  severity='critical', walk_step='2.5', amends='NY:ADJ-tenant-death-payee')]}])
nds = {
 'NY:MHL 81.02': 'Standard for appointing a guardian; the landlord relies on the order, not the standard.',
 'NY:MHL 81.04': 'Which courts may appoint a guardian; guardianship jurisdiction.',
 'NY:MHL 81.05': 'Venue of a guardianship proceeding.',
 'NY:MHL 81.06': 'Who may petition for a guardian; the landlord\'s decisions follow the appointment, not the petition.',
 'NY:MHL 81.08': 'Contents of a guardianship petition.',
 'NY:MHL 81.09': 'Appointment and duties of the court evaluator.',
 'NY:MHL 81.11': 'Hearing procedure in a guardianship proceeding.',
 'NY:MHL 81.15': 'Findings the court makes when appointing; the powers that result are read from the commission (proposed NY:MHL-81.27-commission).',
 'NY:MHL 81.18': 'A foreign guardian may be appointed a New York guardian; until then, payment to a foreign fiduciary of a non-domiciliary incompetent is governed by EPTL 13-3.4 (proposed NY:EPTL-13-3.4-foreign-fiduciary).',
 'NY:MHL 81.19': 'Who may serve as guardian.',
 'NY:MHL 81.20': 'The guardian\'s own duties to the incapacitated person (care, reports, visits, delivery of property); they bind the guardian, not the landlord.',
 'NY:MHL 81.22': 'Personal-needs powers (care, abode, medical decisions); a guardian with only these powers does not receive the refund or settle the account, which stays with the tenant (proposed NY:MHL-81.29-retained-rights).',
 'NY:MHL 81.24': 'The petitioner files a notice of pendency when the proceeding affects real property; a tenant\'s leasehold settlement is not affected.',
 'NY:MHL 81.25': 'Guardian\'s bond.',
 'NY:MHL 81.26': 'Guardian designates the clerk to receive process; folded into the service note of proposed NY:MHL-81.27-commission, it changes no settlement step itself.',
 'NY:MHL 81.33': 'Guardian\'s intermediate and final reports to the court.',
 'NY:MHL 81.34': 'Court decree approving a guardian\'s accounts.',
 'NY:MHL 81.36': 'Discharge or modification of a guardian\'s powers; the powers in force at the time are read from the current commission or order (proposed NY:MHL-81.27-commission).',
 'NY:MHL 81.37': 'Resignation or suspension of a guardian; who then acts is proposed at MHL 81.38.',
 'NY:MHL 81.42': 'Technical defects do not defeat a guardianship proceeding, and an order releases the guardian and sureties; no landlord step changes.',
 'NY:MHL 81.43': 'A guardian\'s turnover proceeding to discover withheld property; a forum for the tenant\'s existing deposit claim that changes nothing the landlord owes or must send.',
}
add([nd(k, v) for k, v in nds.items()])
