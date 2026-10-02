import sys; sys.path.insert(0, 'register/work'); from q4_lib import *
FCRA = 'NY General Business Law art. 25 (Fair Credit Reporting Act)'
add([
 nd('NY:GBL 349-C', 'Supplemental civil penalty in Attorney General proceedings for consumer fraud against persons 65 or older; AG enforcement changes no settlement action beyond NY:GBL-349-unfair-abusive, which already tests every charge and message.'),
 nd('NY:GBL 350-E', 'Private action for false advertising under GBL 350 and 350-a; advertising a unit is leasing, outside the settlement chain.'),
 nd('NY:GBL 380-C', 'Notice and authorization before an investigative consumer report (character and reputation from interviews); such reports are screening and employment tools, not a step in settling or collecting a tenancy.'),
 nd('NY:GBL 380-D', 'Duties of consumer reporting agencies to disclose files to consumers; binds the agency only.'),
 nd('NY:GBL 380-E', 'Methods and charges for an agency\'s file disclosure; binds the agency only.'),
 nd('NY:GBL 380-F', 'The agency\'s reinvestigation of a disputed item; binds the agency. The landlord\'s duties when a dispute reaches it through an agency are stated by US:15USC1681s-2(b)(1).'),
 nd('NY:GBL 380-G', 'Agency procedures for public-record items; binds the agency only.'),
 nd('NY:GBL 380-H', 'Limits on reuse of investigative-report information by the agency; binds the agency only.'),
 nd('NY:GBL 380-J', 'Lists what a consumer reporting agency may keep or report (including the age limits for collection accounts and judgments); binds the agency, not the landlord or collector that furnishes, whose furnishing duties are stated by US:15USC1681s-2(a)(1)(A) and US:15USC1681b-1681c-report-limits.'),
 nd('NY:GBL 380-K', 'Agency compliance procedures and user certification to the agency; the permitted purposes the user certifies are proposed at GBL 380-B.'),
 nd('NY:GBL 380-P', 'Criminal penalty for agency officers or employees who disclose files; binds agency staff only.'),
 nd('NY:GBL 380-Q', 'Medical information in disclosures goes only to a physician; applies to agency disclosures and adverse-action reasons, not to settling or collecting.'),
 nd('NY:GBL 380-R', 'Lets an agency give identifying information to government agencies; binds the agency only.'),
 nd('NY:GBL 380-S', 'Prohibits obtaining credit or goods in another person\'s name with intent to defraud; binds the impostor. A former tenant\'s claim that someone else incurred the balance is handled under NY:GBL-399-ddd-604-a and the federal and city dispute rules.'),
 nd('NY:GBL 380-U', 'Security freezes for protected minors placed by credit agencies; binds the agency only.'),
 nd('NY:GBL 390-E', 'Consent and 30-day notice before installing keyless entry in common areas, and no rent increase for it; conduct during the tenancy that fixes no move-out charge or credit.'),
 nd('NY:GBL 393-F', 'Third-party billing notices for telephone, cable and municipal utility customers; binds those providers only.'),
 nd('NY:GBL 394-A', 'Proof at trial of a lost negotiable instrument on which an action is founded; a deposit or balance claim is founded on the lease and GOL 7-108, not on an instrument.'),
 nd('NY:GBL 399-E*2', 'Bars denying or raising the cost of credit because the consumer is an identity-theft victim; a lease balance is not credit (NY:ADJ-lease-balance-not-consumer-credit) and settlement denies no credit.'),
 nd('NY:GBL 604-FF', 'Attorney General injunction and civil penalty for coerced-debt violations; AG enforcement is not a step the landlord or collector takes, and the duties it enforces are stated by NY:GBL-604-bb-coerced-debt.'),
 {'section_id': 'NY:GBL 604-GG', 'decision': 'stated', 'atom_ids': ['NY:GBL-604-bb-coerced-debt', 'NY:GBL-604-cc-coerced-defense'], 'reason': 'The article reaches the creditor (including a collector) once a debt is asserted to be coerced, adds no other duty, and leaves recourse for fraudulent claims; the rules are drawn to that scope.'},
])
I = 'NY:GBL 380-I'
add([{'section_id': I, 'decision': 'new_rule', 'reason': 'Subdivision (c) decides whether a landlord may pass a former tenant\'s consumer report to Handoff, a collector or anyone else at hand-off; (a)-(b) are adverse action on applications and outside the chain.', 'proposed': [rule(I,
  id='NY:GBL-380-i(c)-report-redisclosure', instrument=FCRA, provision='GBL 380-i(c)', actor='landlord, managing agent, Handoff or collector holding a consumer report on the tenant', modality='prohibition',
  condition='The landlord or manager holds a consumer report or investigative report on the former tenant (for example from the rental application) and considers passing it on at settlement or hand-off.',
  effect='It may give the report only to a person with a legitimate business need for the information in connection with a business transaction involving the tenant: Handoff settling the tenant\'s account, or a collector or attorney collecting the tenant\'s balance, qualify. It may not give the report to anyone else (for example the next occupant, a co-tenant about the other co-tenant, a family member or heir, or a buyer of the building for its marketing). Liability: NY:GBL-380-l-willful, NY:GBL-380-m-negligent.',
  dependencies=['NY:GBL-380-b-permissible-purpose'],
  quote=q(I, 'Every user of a consumer report or an investigative consumer report shall be prohibited from disseminating any such report to any other person unless such other person has a legitimate business need for the information in connection with a business transaction involving the consumer.'),
  determinacy='MIXED', judgment_terms=['legitimate business need for the information in connection with a business transaction involving the consumer'],
  severity='major', walk_step='6.10')]}])
M = 'NY:GBL 380-M'
add([{'section_id': M, 'decision': 'new_rule', 'reason': 'State civil liability for a user\'s negligent noncompliance with article 25; no rule states it.', 'proposed': [rule(M,
  id='NY:GBL-380-m-negligent', instrument=FCRA, provision='GBL 380-m', actor='landlord, managing agent, Handoff or collector as user of consumer reports', modality='liability',
  condition='A user of consumer report information (landlord, manager, Handoff or collector) negligently fails to comply with a requirement of GBL art. 25 toward a former tenant (for example obtaining a report for a purpose 380-b does not permit, or passing it to a person without a legitimate business need, 380-i(c)).',
  effect='The user is liable to the former tenant for actual damages and, if the tenant succeeds, costs and reasonable attorney\'s fees. No punitive damages for negligence (for willful violations see NY:GBL-380-l-willful). The action is brought within the period of NY:GBL-380-n-limitations.',
  dependencies=['NY:GBL-380-b-permissible-purpose', 'NY:GBL-380-i(c)-report-redisclosure'],
  quote=q(M, 'Any consumer reporting agency or user of information who or which is negligent in failing to comply with any requirement imposed under this article, other than a violation of section three hundred eighty-t of this article, with respect to any consumer is liable to that consumer'),
  severity='critical', walk_step='8.7')]}])
N = 'NY:GBL 380-N'
add([{'section_id': N, 'decision': 'new_rule', 'reason': 'Fixes how long a former tenant may sue the landlord or collector for an article 25 violation, which sets the exposure window and record retention.', 'proposed': [rule(N,
  id='NY:GBL-380-n-limitations', instrument=FCRA, provision='GBL 380-n', actor='landlord, managing agent, Handoff or collector', modality='limitation',
  condition='A former tenant sues a user of its consumer report (landlord, manager, Handoff or collector) under GBL 380-l or 380-m.',
  effect='The action must be brought within two years from the date the liability arises. If the defendant materially and willfully misrepresented information article 25 required it to disclose to the tenant, and the misrepresentation is material to its liability, the tenant has two years from discovering the misrepresentation.',
  dependencies=['NY:GBL-380-l-willful', 'NY:GBL-380-m-negligent'],
  quote=q(N, 'within two years from the date on which the liability arises'),
  severity='major', walk_step='8.7')]}])
O = 'NY:GBL 380-O'
add([{'section_id': O, 'decision': 'new_rule', 'reason': 'Makes it a crime to obtain a former tenant\'s report under false pretenses or to feed false information to a credit agency to damage the tenant\'s credit; changes what may be reported.', 'proposed': [rule(O,
  id='NY:GBL-380-o-false-pretenses', instrument=FCRA, provision='GBL 380-o(1)-(2)', actor='landlord, managing agent, Handoff or collector', modality='prohibition',
  determinacy='MIXED', judgment_terms=['knowingly and willfully', 'for the purpose of wrongfully damaging'],
  condition='Branch (a): a person obtains a former tenant\'s consumer report by a false statement of its purpose or identity. Branch (b): a person reports to a consumer reporting agency information about the former tenant that it knows is false (for example a balance the landlord knows is not owed, such as a deposit forfeited under NY:GOL-7-108(1-a)(e)-forfeiture reported as unpaid, or a charge the law bars) to wrongfully damage the tenant\'s credit.',
  effect='Either act, done knowingly and willfully, is a crime punishable on conviction by a fine of up to $5,000, imprisonment of up to one year, or both. A tenant\'s own dispute statement filed with the agency is not covered. The civil consequences are NY:GBL-380-l-willful and the federal furnisher rules (US:15USC1681s-2(a)(1)(A)).',
  dependencies=['NY:GBL-380-b-permissible-purpose', 'US:15USC1681s-2(a)(1)(A)'],
  quote=q(O, 'Any person who knowingly and willfully introduces, attempts to introduce or causes to be introduced, false information into a consumer reporting agency’s files for the purpose of wrongfully damaging or wrongfully enhancing the credit information of any individual shall, upon conviction, be fined not more than five thousand dollars or imprisoned not more than one year, or both.'),
  severity='critical', walk_step='8.7')]}])
P = 'NY:GBL 399-DD*3'
add([{'section_id': P, 'decision': 'new_rule', 'reason': 'Bars procuring a former tenant\'s telephone records from a carrier to locate the tenant without written authorization; locating the tenant is a step in delivering the statement and collecting.', 'proposed': [rule(P,
  id='NY:GBL-399-dd-phone-records', instrument='NY General Business Law', provision='GBL 399-dd (third section so numbered)(2)-(3)', actor='landlord, managing agent, Handoff or collector', modality='prohibition',
  condition='The landlord, manager, Handoff or a collector tries to locate a former tenant or verify its contact details.',
  effect='It may not knowingly and intentionally procure, or get another to procure, the tenant\'s telephone records (numbers called or received, message contents, call times and charges) from a telephone company without the tenant\'s written authorization; caller ID it received is not a telephone record and may be used. The Attorney General may enjoin a violation and the court may award the tenant\'s actual losses and fees and impose a civil penalty of $1,000 per violation, within two years of the act or its discovery.',
  quote=q(P, 'No person, firm, partnership, association, limited liability company, corporation, trust, business or other entity shall knowingly and intentionally procure, attempt to procure, solicit or conspire with another to procure'),
  severity='major', walk_step='6.5')]}])
D = 'NY:GBL 399-DDD*2'
add([{'section_id': D, 'decision': 'new_rule', 'reason': 'Decides when the landlord may require the former tenant\'s social security number (for example for the deposit-interest 1099-INT) and bars refusing the refund for want of it; NY:GBL-399-ddd-604-a covers only printing the number on mail.', 'proposed': [rule(D,
  id='NY:GBL-399-ddd2-ssn-demand', instrument='NY General Business Law', provision='GBL 399-ddd (second section so numbered)(2)-(5)', actor='landlord, managing agent, Handoff or collector', modality='prohibition',
  condition='The landlord, its manager, Handoff or a collector asks the former tenant for its social security number at settlement or collection.',
  effect='It may not require the number, or refuse any service, privilege or right (including the refund) because the tenant will not give it, unless an exception applies: the tenant consents; law requires it (for example the Form 1099-INT for $10 or more of deposit interest, US:26USC6049-deposit-interest, which is also the tax-compliance exception); internal verification or fraud investigation; a lawful request for a consumer report (NY:GBL-380-b-permissible-purpose); enforcement of a judgment by a sheriff or marshal. An exception permits the request; it never extends the 14-day statement and refund (NY:GOL-7-108(1-a)(e)). Violation: Attorney General injunction and restitution, civil penalty up to $500, and up to $1,000 for a second or later offense; no violation if the error was unintentional and bona fide despite procedures reasonably adopted to avoid it.',
  dependencies=['US:26USC6049-deposit-interest', 'NY:GOL-7-108(1-a)(e)'],
  quote=q(D, 'shall require an individual to disclose or furnish his or her social security account number, for any purpose in connection with any activity, or to refuse any service, privilege or right to an individual wholly or partly because such individual refuses to disclose or furnish such number'),
  severity='major', walk_step='6.10')]}])
B = 'NY:GBL 604-B'
add([{'section_id': B, 'decision': 'partial', 'atom_ids': ['NY:GBL-601-a-family'], 'reason': 'Art. 29-H\'s conduct rules mostly do not reach a lease balance, but 601-a does (NY:GBL-601-a-family); 604-b sets the penalty and the principal creditor\'s cure and bona fide error defenses for it.', 'proposed': [rule(B,
  id='NY:GBL-604-b-penalty-cure', instrument='NY General Business Law art. 29-H', provision='GBL 604-b(a)-(c)', actor='landlord (principal creditor) or collector', modality='liability',
  condition='The landlord, its manager or a collector violates GBL 601-a by telling a family member or heir of a former tenant that it must pay the tenant\'s balance, or misrepresenting its obligation (NY:GBL-601-a-family).',
  effect='The Attorney General may obtain an injunction and restitution, and the court may impose a civil penalty of $500 to $1,000 per violation. The landlord as principal creditor has no civil liability if, within fifteen days after discovering a curable violation or receiving written notice of it, it notifies the person of the violation and makes the corrections needed to cure it (for example withdrawing the demand in writing); nor if it shows the violation was unintentional and a bona fide error despite procedures reasonably adopted to avoid it. The cure and bona fide error defenses are the principal creditor\'s; a collection agency has only the penalty exposure.',
  dependencies=['NY:GBL-601-a-family'],
  quote=q(B, 'A principal creditor shall have no civil liability under this article if, within fifteen days either after discovering a violation which is able to be cured, or after the receipt of a written notice of such violation, the principal creditor notifies the debtor of the violation, and makes whatever adjustments or corrections are necessary to cure the violation with respect to the debtor.'),
  severity='major', walk_step='8.4', amends='NY:GBL-601-a-family')]}])
DD = 'NY:GBL 604-DD'
add([{'section_id': DD, 'decision': 'partial', 'atom_ids': ['NY:GBL-604-bb-coerced-debt', 'NY:GBL-604-cc-coerced-defense'], 'reason': 'The secured-debt carve-outs could narrow the coerced-debt rules; they do not reach a lease balance, and the rules should say so.', 'proposed': [rule(DD,
  id='NY:GBL-604-dd-lease-balance-not-secured', instrument='NY General Business Law art. 29-HHH (coerced debt)', provision='GBL 604-dd(1)-(3)', actor='landlord, managing agent or collector', modality='applicability',
  condition='A former tenant asserts that all or part of a lease balance is coerced debt, and the landlord holds or held a security deposit.',
  effect='The carve-outs of 604-dd do not apply. A lease balance is not a debt secured by real property (the tenant gives no lien on real property), and it is not a debt secured by personal property: the carve-out for personal property addresses collateral under a financing and security agreement enforced under UCC article 9 (repossession, surrender), while a rental security deposit is the tenant\'s own money held in trust (NY:GOL-7-103(1)-trust), not collateral under such an agreement. So 604-bb (stop collection, review, notices) and both 604-cc remedies apply in full to the balance (NY:GBL-604-bb-coerced-debt, NY:GBL-604-cc-coerced-defense).',
  dependencies=['NY:GBL-604-bb-coerced-debt', 'NY:GOL-7-103(1)-trust'],
  quote=q(DD, 'the affirmative defense authorized by section six hundred four-cc of this article shall not affect the creditor’s right to enforce any security interest upon default of the financing and security agreement under article nine of the uniform commercial code'),
  construction=[{'source_file': 'register/texts/NY_GBL/604-dd.txt', 'quote': q(DD, 'Except with respect to section six hundred four-ee of this article, this article shall not apply to debts secured by real property.')}],
  reasoning='604-dd(3) shows the personal-property carve-out concerns article 9 collateral (repossession, deficiency); GOL 7-103 makes the deposit the tenant\'s trust money, not the landlord\'s collateral, and the balance claimed after move-out is unsecured.',
  severity='critical', walk_step='8.1a', amends='NY:GBL-604-bb-coerced-debt')]}])
EE = 'NY:GBL 604-EE'
add([{'section_id': EE, 'decision': 'new_rule', 'reason': 'Gives the landlord a claim against the person who coerced the tenant into the debt, with its own limitation period; changes whom the balance may be recovered from.', 'proposed': [rule(EE,
  id='NY:GBL-604-ee-claim-against-coercer', instrument='NY General Business Law art. 29-HHH (coerced debt)', provision='GBL 604-ee(1)-(2)', actor='landlord (creditor)', modality='permission',
  determinacy='MIXED', judgment_terms=['coerced debt'],
  condition='The landlord has determined under 604-bb, or a court has determined, that all or part of a former tenant\'s lease balance is coerced debt, caused by an identified person (for example an abusive co-occupant or partner).',
  effect='The landlord may sue the person who caused the coerced debt for the amount found coerced, plus its reasonable costs and attorney\'s fees in that action. A tenant who already paid part of the coerced debt has the same claim for what it paid. The action must be commenced within three years of the later of the landlord\'s determination or the court\'s determination that the debt is coerced. This claim applies whatever the debt\'s security.',
  dependencies=['NY:GBL-604-bb-coerced-debt', 'NY:GBL-604-cc-coerced-defense'],
  quote=q(EE, 'A person who causes another person to incur a coerced debt in violation of this section shall be civilly liable to the creditor and/or the debtor in whose name such coerced debt was incurred'),
  severity='critical', walk_step='8.1a')]}])
