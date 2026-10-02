import sys; sys.path.insert(0, 'register/work'); from q4_lib import *
s='NY:Executive Law 296-A'
add([{'section_id': s, 'decision': 'partial', 'atom_ids': ['NY:EXEC-296(5)(a)(2)-terms'], 'reason': 'The housing rule covers deductions and whether a balance is pursued; a payment plan on the balance is credit under Exec. Law 292, so 296-a adds its own bar on discriminatory plan decisions and a duty to give reasons on request.', 'proposed': [rule(s, instrument='NY Executive Law art. 15 (Human Rights Law)',
  id='NY:EXEC-296-a-payment-plan', provision='Exec. Law 296-a(1)(b), (2)-(4); 292 (credit, creditor)', actor='landlord, managing agent, Handoff or collector offering deferred payment', modality='prohibition',
  determinacy='MIXED', judgment_terms=['factually supportable, objective differences in overall credit worthiness'],
  condition='A former tenant owes a balance and asks for, or is offered, time to pay it (a payment plan, installment agreement or deferral), which is credit: a right conferred by a creditor to incur debt and defer its payment, with or without a finance charge.',
  effect='Whoever grants the plan is a creditor for this purpose. It may not grant, withhold, extend or set the terms of the plan (length, down payment, interest, co-signer) differently because of race, creed, color, national origin, citizenship or immigration status, sexual orientation, gender identity or expression, military status, age, sex, marital status, domestic-violence victim status, disability or familial status, nor ask about childbearing or birth control, nor refuse to consider, or discount, a source of the tenant\'s income for those reasons. Differences based on factually supportable, objective differences in overall creditworthiness (current income, assets, prior credit history) are lawful. On the tenant\'s request, a creditor that rejects a plan request gives the specific reasons. Remedies follow NY:EXC-297(9)-remedies.',
  dependencies=['NY:EXEC-296(5)(a)(2)-terms', 'NY:EXC-297(9)-remedies'],
  quote=q(s, 'To discriminate in the granting, withholding, extending or renewing, or in the fixing of the rates, terms or conditions of, any form of credit'),
  construction=[{'source_file': 'register/texts/NY_EXEC/292.txt', 'quote': 'The term “credit”, when used in this article means the right conferred upon a person by a creditor to incur debt and defer its payment, whether or not any interest or finance charge is made for the exercise of this right.'}],
  reasoning='A payment plan confers a right to defer payment of the balance, which is credit under 292, and the landlord granting it extends credit and so is a creditor.',
  severity='major', walk_step='5.10', amends='NY:EXEC-296(5)(a)(2)-terms')]}])
add([
 {'section_id': 'NY:Executive Law 292', 'decision': 'stated', 'atom_ids': ['NY:EXEC-296(5)(a)(2)-terms'], 'reason': 'The definitions (housing accommodation, lawful source of income including vouchers paid to the landlord, military status, familial status) give the stated rule its reach, and the rule already applies them to every market-rate unit; the credit definitions are used by the proposed 296-a rule.'},
 nd('NY:Executive Law 295', 'Powers and duties of the Division of Human Rights; agency administration.'),
 nd('NY:Executive Law 299', 'Crime of obstructing the Division or wilfully violating its order; changes no settlement step (substantive duties are in 296).'),
 nd('NY:Executive Law 301', 'Severability clause.'),
])
