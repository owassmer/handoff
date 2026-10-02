import sys; sys.path.insert(0, 'register/work'); from q4_lib import *
# convert 349-C from no_decision to partial
rows = [json.loads(l) for l in DEC.read_text().splitlines() if l.strip()]
rows = [r for r in rows if r['section_id'] != 'NY:GBL 349-C']
DEC.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
C = 'NY:GBL 349-C'
add([{'section_id': C, 'decision': 'partial', 'atom_ids': ['NY:GBL-349-unfair-abusive'], 'reason': 'The rule states the private remedy and that the Attorney General enforces; 349-c adds a supplemental penalty where the deceptive or unfair practice targets a tenant 65 or older.', 'proposed': [rule(C,
  id='NY:GBL-349-c-elderly-penalty', instrument='NY General Business Law art. 22-A', provision='GBL 349-c(1)-(2), (4)', actor='landlord, managing agent, Handoff or collector', modality='liability',
  determinacy='MIXED', judgment_terms=['knew the conduct was directed to elderly persons or willful disregard of their rights', 'substantially more vulnerable because of age, poor health, infirmity, impaired understanding, restricted mobility, or disability'],
  condition='A practice in settling or collecting violates GBL 349 or 350 (NY:GBL-349-unfair-abusive) and is directed at one or more former tenants aged 65 or older.',
  effect='In addition to damages and the GBL 350-d penalty (NY:GBL-350-d-civil-penalty), the court may impose a supplemental civil penalty of up to $10,000, weighing whether the violator knew its conduct was directed at elderly persons or willfully disregarded their rights, and whether they suffered loss of a residence, income or retirement or benefit money, or were substantially more vulnerable and actually harmed. Restitution to the tenant is ordered before any penalty.',
  dependencies=['NY:GBL-349-unfair-abusive'],
  quote=q(C, 'may be liable for an additional civil penalty not to exceed ten thousand dollars, if the factors in paragraph (b) of this subdivision are present.'),
  severity='critical', walk_step='5.10', amends='NY:GBL-349-unfair-abusive')]}])
D = 'NY:GBL 350-D'
add([{'section_id': D, 'decision': 'partial', 'atom_ids': ['NY:GBL-349-unfair-abusive'], 'reason': 'Sets the civil penalty per violation for practices article 22-A makes unlawful, including GBL 349; the rule states only that the Attorney General enforces.', 'proposed': [rule(D,
  id='NY:GBL-350-d-civil-penalty', instrument='NY General Business Law art. 22-A', provision='GBL 350-d(a)', actor='landlord, managing agent, Handoff or collector, and their agents and employees', modality='liability',
  condition='A charge, statement, collection message or other practice toward a former tenant is unlawful under GBL 349 (NY:GBL-349-unfair-abusive) or 350.',
  effect='The violator, including an agent or employee who engages in the practice, is liable to a civil penalty of up to $5,000 for each violation, recovered by the Attorney General for the State; each deceptive statement or charge sent is a separate violation. Compliance with FTC or New York agency rules governing the practice is a complete defense. The penalty is in addition to the tenant\'s own damages.',
  dependencies=['NY:GBL-349-unfair-abusive'],
  quote=q(D, 'shall be liable to a civil penalty of not more than five thousand dollars for each violation, which shall accrue to the state of New York and may be recovered in a civil action brought by the attorney general.'),
  severity='critical', walk_step='5.10', amends='NY:GBL-349-unfair-abusive')]}])
N = 'NY:GBL 133'
add([{'section_id': N, 'decision': 'partial', 'atom_ids': ['US:15USC1692a(6)-false-name'], 'reason': 'The federal rule makes a creditor using a third-party-sounding name a debt collector; GBL 133 independently makes a name used with intent to mislead as to identity or connection a misdemeanor, which binds the choice of name on statements and collection letters.', 'proposed': [rule(N,
  id='NY:GBL-133-deceptive-name', instrument='NY General Business Law art. 9-B', provision='GBL 133', actor='landlord, managing agent, Handoff or collector', modality='prohibition',
  determinacy='MIXED', judgment_terms=['intent to deceive or mislead the public', 'may deceive or mislead the public as to the identity or connection'],
  condition='A statement, demand or collection letter goes out under a name or address other than the sender\'s own (for example a collection-department name for the owner, a name implying a law firm, court or government connection, or Handoff\'s name for an owner letter).',
  effect='Using a name, style, symbol or address with intent to mislead the tenant as to who the sender is, or its connection with another person, is a misdemeanor and may be enjoined without proof that anyone was misled. A name that truthfully identifies the sender and its role (for example the owner\'s legal or filed assumed name, NY:GBL-130-assumed-name, or Handoff as the owner\'s agent) does not violate it.',
  dependencies=['US:15USC1692a(6)-false-name', 'NY:GBL-130-assumed-name'],
  quote=q(N, 'which may deceive or mislead the public as to the identity of such person, firm or corporation or as to the connection of such person, firm or corporation with any other person, firm or corporation'),
  severity='major', walk_step='8.2', amends='US:15USC1692a(6)-false-name')]}])
Z = 'NY:GBL 399-ZZZ'
add([{'section_id': Z, 'decision': 'partial', 'atom_ids': ['NY:RPL-235-g'], 'reason': 'RPL 235-g binds the landlord on rent payments; 399-zzz bars any business, including a collector or Handoff, from charging a fee for paying the balance by mail or receiving a paper statement, and makes it a deceptive practice.', 'proposed': [rule(Z,
  id='NY:GBL-399-zzz-paper-fee', instrument='NY General Business Law', provision='GBL 399-zzz(1)-(3)', actor='landlord, managing agent, Handoff or collector', modality='prohibition',
  condition='A former tenant (a natural person) chooses to receive a paper statement or bill, or to pay the balance by United States mail.',
  effect='No one may charge the tenant an extra fee or a different rate for that choice (for example a paper-statement fee or a mail-payment processing fee added to the balance). A credit or other incentive for electing electronic delivery or payment is allowed. A violation is a deceptive act under article 22-A (NY:GBL-349-unfair-abusive), with its private remedy.',
  dependencies=['NY:RPL-235-g', 'NY:GBL-349-unfair-abusive'],
  quote=q(Z, 'no person, partnership, corporation, association or other business entity shall charge a consumer an additional rate or fee or a differential in the rate or fee associated with payment on an account when the consumer chooses to pay by United States mail or receive a paper billing statement.'),
  severity='major', walk_step='5.2', amends='NY:RPL-235-g')]}])
add([
 nd('NY:Executive Law 290', 'Title and legislative purposes of the Human Rights Law; the operative housing prohibition is stated by NY:EXEC-296(5)(a)(2)-terms.'),
 nd('NY:Executive Law 291', 'Declares equal opportunity in housing a civil right; the operative duties are in section 296, stated by NY:EXEC-296(5)(a)(2)-terms.'),
 nd('NY:GBL 350', 'Declares false advertising unlawful; advertising a unit is leasing, outside the settlement chain, and statements and demands are tested under NY:GBL-349-unfair-abusive.'),
 nd('NY:GBL 380-V', 'Severability clause.'),
 nd('NY:GBL 390-B', 'Bars soliciting identifying information online by impersonating a business without its authority; Handoff or a collector requesting refund bank details in the owner\'s name acts with the owner\'s authority, so no settlement step changes.'),
 nd('NY:GBL 390-BB', 'Third-party charges on cable-company telephone bills; not a tenancy matter.'),
 nd('NY:GBL 393-E', 'Disclosures by paid finders of funds held by the Comptroller; binds finders, not the landlord.'),
 nd('NY:GBL 394-H', 'Bars law enforcement from buying health data without a warrant; not a tenancy matter.'),
 nd('NY:GBL 394-I', 'Limits compliance with subpoenas about legally protected health activity; not a tenancy settlement matter.'),
 nd('NY:GBL 395-B', 'Two-way mirrors in fitting rooms, restrooms and hotel rooms; private dwellings are excluded.'),
 nd('NY:GBL 396', 'Bait advertising and unsolicited merchandise; not a tenancy matter.'),
 nd('NY:GBL 396-AA*2', 'Unsolicited fax advertising; not a settlement or collection communication.'),
 nd('NY:GBL 396-D', 'Naming the true locality when describing or leasing real property; a leasing and advertising rule that fixes nothing at settlement.'),
 nd('NY:GBL 396-II', 'Food stores and retail establishments must accept cash; a landlord collecting rent or a balance is not a retail establishment selling consumer commodities. Payment-method rules for rent are stated by NY:RPL-235-g.'),
 nd('NY:GBL 396-R', 'Price gouging on essential goods during declared emergencies; lease charges at settlement are governed by the deposit and lease rules.'),
 nd('NY:GBL 399-A', 'Prohibits pay toilets; not a tenancy settlement matter.'),
 nd('NY:GBL 399-C', 'Voids mandatory arbitration clauses in contracts for the sale of consumer goods; a lease of real property is not such a contract.'),
 nd('NY:GBL 399-CC', 'Bars building wireless-number directories from carriers without consent; not a settlement or collection step.'),
 nd('NY:GBL 399-CC*2', 'Attorneys pay for stenographic records they order; litigation cost between lawyer and reporter.'),
 nd('NY:GBL 399-P', 'Rules for automatic dialing-announcing devices and consumer telephone solicitation of sales; a settlement or collection call is not a sales solicitation. Collection calling is governed by US:47USC227-TCPA and the federal and city collection rules.'),
 nd('NY:GBL 399-W*2', 'Notices by businesses renting personal property; not a residential lease.'),
 nd('NY:GBL 399-ZZ', 'Large-print billing by telephone and cable companies; binds those providers only.'),
 nd('NY:GBL 399-ZZZZ', 'Bars early-termination fees on a deceased customer\'s utility service contract or motor vehicle lease; a residential lease is not covered (a deceased tenant\'s lease is governed by NY:RPL-236-a).'),
 nd('NY:MHL 81.12', 'Burden of proof in a guardianship proceeding; the landlord relies on the appointment order, not on the finding\'s proof.'),
])
