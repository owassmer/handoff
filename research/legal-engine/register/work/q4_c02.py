import sys; sys.path.insert(0, 'register/work'); from q4_lib import *
S = 'NY:SSL 143-C'
a1 = rule(S, id='NY:SSL-143-c-agency-deposit-refund', instrument='NY Social Services Law', provision='SSL 143-c(1)-(3), (5); 18 NYCRR 352.6(b)(3)',
  actor='landlord or managing agent', modality='obligation',
  condition='The former tenant received public assistance (or SSI or additional state payments, 143-c(5)) and the deposit was secured for the landlord by a local social services official (HRA/DSS in NYC). Branch (a): the official gave a security agreement (a voucher) or an escrow deposit not under the landlord\'s control (143-c(1)). Branch (b): the official paid a cash deposit to the landlord, or issued the recipient a grant for it (143-c(3)).',
  effect='(a) There is no cash deposit in the landlord\'s hands to refund; the landlord claims against the agreement or escrow on its terms (NYC:HRA-voucher-claim-window, NYC:HRA-voucher-proof). (b) The cash deposit is subject to GOL article 7 like any deposit (trust, bank notice, interest, 14-day statement and forfeiture). The recipient is required by 18 NYCRR 352.6(b)(3) to assign to the social services official its right to the return of the deposit and interest; once the landlord has notice of the assignment, the refund (deposit and interest less lawful deductions) is paid to the social services official, not to the former tenant, and the itemized statement still goes to the tenant. Without an assignment the refund is paid to the tenant.',
  dependencies=['NY:GOL-7-103(1)-trust', 'NY:GOL-7-108(1-a)(e)', 'NYC:HRA-voucher-claim-window'],
  quote=q(S, 'Landlords receiving such security deposits shall comply with the provisions of article seven of the general obligations law. Such cash security deposits shall be subject to assignment to the local social services official by the recipients of public assistance or care.'),
  construction=[{'source_file': 'register/texts/NY_18NYCRR/352.6.txt', 'quote': q('NY:18 NYCRR 352.6', 'The recipient is required to assign to the social services official any right the recipient may have to the return of the security deposit and interest accrued thereon.')}],
  reasoning='The statute makes the cash deposit assignable to the official and the regulation requires the recipient to assign it; an assignee with notice is the payee of the refund.',
  severity='critical', walk_step='5.8')
add([{'section_id': S, 'decision': 'new_rule', 'reason': 'Decides who is paid the refund of a deposit that a social services official funded in cash (the official, by required assignment) and confirms GOL art. 7 governs it; voucher and escrow branches route to the existing HRA rules.', 'proposed': [a1]}])
R = 'NY:18 NYCRR 352.6'
a2 = rule(R, id='NY:18NYCRR-352.6(c)(2)-damage-verification', instrument='18 NYCRR Part 352 (public assistance)', provision='18 NYCRR 352.6(c)(2)',
  actor='landlord or managing agent claiming against a social-services security agreement or keeping a social-services cash deposit', modality='precondition',
  condition='The landlord claims payment for the former tenant\'s damage under a social services security agreement (voucher), or keeps a cash deposit funded by the social services official for damage.',
  effect='The district pays for damage only if it has verified that the recipient caused it: by a pre-tenancy and a post-tenancy inspection or survey that it conducted or arranged, with the move-in and move-out condition documented and signed by the landlord and the recipient, or by some other means of verification. If verification does not confirm tenant-caused damage, no cash is issued under the agreement, and where a cash deposit was kept for the alleged damage the district seeks to recover it from the landlord. Operator step: record the move-in and move-out condition on a form both the landlord and the tenant sign. Rent claims under the agreement are unaffected by this paragraph.',
  dependencies=['NYC:HRA-voucher-proof', 'NY:SSL-143-c-agency-deposit-refund'],
  quote=q(R, 'The condition of the premises when the recipient moves in and when the recipient moves out must be documented and agreed to by signature of the landlord and the recipient.'),
  severity='major', walk_step='5.8', amends='NYC:HRA-voucher-proof')
add([{'section_id': R, 'decision': 'partial', 'atom_ids': ['NYC:HRA-voucher-proof', 'NYC:RCNY68-10-14(c)'], 'reason': 'Voucher claims are stated; (c)(2) adds the verification the district requires before paying for damage; the (b)(3) assignment of a cash deposit is proposed at SSL 143-C; (a), (e), (f) are grants to recipients and change nothing for the landlord.', 'proposed': [a2]}])
add([
 {'section_id': 'NY:EPTL 11-3.1', 'decision': 'stated', 'atom_ids': ['NY:ADJ-tenant-death-payee', 'NY:CPLR-1203-1015-5208-parties'], 'reason': 'Contract claims survive by and against the personal representative; the rules name the fiduciary as the party who pays and is paid and require substitution.'},
 {'section_id': 'NY:EPTL 11-3.2', 'decision': 'stated', 'atom_ids': ['NY:ADJ-tenant-death-payee', 'NY:CPLR-1203-1015-5208-parties'], 'reason': 'Damage claims survive against the tenant\'s representative and the estate\'s claims survive for it; the rules route both through the fiduciary. The punitive bar reaches personal-injury actions only.'},
])
E = 'NY:EPTL 11-4.6'
add([{'section_id': E, 'decision': 'partial', 'atom_ids': ['NY:CPLR-1203-1015-5208-parties'], 'reason': 'The existing rule covers a judgment debtor who dies after judgment; 11-4.6 covers a judgment recovered against the personal representative.', 'proposed': [rule(E,
  id='NY:EPTL-11-4.6-execution-leave', instrument='NY Estates, Powers and Trusts Law', provision='EPTL 11-4.6(a)-(b)', actor='landlord or its collector enforcing a judgment', modality='precondition',
  condition='The landlord holds a money judgment against the executor or administrator of a deceased former tenant in its representative capacity.',
  effect='No execution issues until the surrogate\'s court that issued letters grants an order stating the sum to be collected, on at least six days\' notice personally served on the representative. If the estate cannot pay all claims of the landlord\'s class after expenses and prior claims, the sum is limited to the landlord\'s just proportion of the assets. A judgment against the representative jointly with others (for example a co-tenant or guarantor) may be executed against the others without the order if the execution directs no levy on estate property.',
  dependencies=['NY:CPLR-1203-1015-5208-parties', 'NY:ADJ-tenant-death-payee'],
  quote=q(E, 'an execution shall not be issued upon a judgment for a sum of money against a personal representative, in his representative capacity, until an order permitting it to be issued has been made by the surrogate’s court from which letters were issued.'),
  severity='major', walk_step='8.12', amends='NY:CPLR-1203-1015-5208-parties')]}])
D = 'NY:EPTL 12-1.1'
add([{'section_id': D, 'decision': 'new_rule', 'reason': 'Decides whether a deceased tenant\'s balance may be recovered from heirs and beneficiaries after distribution, and the cap; no rule states it.', 'proposed': [rule(D,
  id='NY:EPTL-12-1.1-distributee-liability', instrument='NY Estates, Powers and Trusts Law', provision='EPTL 12-1.1', actor='landlord or its collector', modality='permission',
  condition='A former tenant died owing a lease balance, and the estate\'s property has passed to distributees (heirs) or beneficiaries under the will.',
  effect='The landlord may sue a distributee or beneficiary for the balance, up to the value of the property that person received from the estate, only if it shows it cannot be paid in full (1) from the estate property in the representative\'s hands, (2) from persons earlier in the order of liability (NY:EPTL-12-1.2-order), because they cannot be sued in New York, are insolvent or otherwise cannot answer, or (3) by enforcing a lien or security it holds. No beneficiary or heir owes the balance beyond that value, and no family member owes it personally (NY:GBL-601-a-family). Each defendant\'s final share is ratable (NY:EPTL-12-1.3-ratable).',
  dependencies=['NY:ADJ-tenant-death-payee', 'NY:GBL-601-a-family'],
  quote=q(D, 'distributees and testamentary beneficiaries are liable, in an action, to the extent of the value of any property received by them as such, for the debts'),
  severity='major', walk_step='8.1')]}])
O = 'NY:EPTL 12-1.2'
add([{'section_id': O, 'decision': 'new_rule', 'reason': 'Fixes whom the landlord pursues first among heirs and beneficiaries and when a prior unpaid claim is a defense.', 'proposed': [rule(O,
  id='NY:EPTL-12-1.2-order', instrument='NY Estates, Powers and Trusts Law', provision='EPTL 12-1.2(a), (c), (d)', actor='landlord or its collector', modality='procedure',
  condition='The landlord pursues heirs or beneficiaries of a deceased former tenant under NY:EPTL-12-1.1-distributee-liability.',
  effect='They are liable in this order: distributees; residuary beneficiaries; general beneficiaries; specific beneficiaries; a surviving spouse whose gift qualifies for the marital deduction; a testator\'s expressed intention may vary the order. An unpaid claim legally preferred to the landlord\'s is a defense unless the property passing to the defendant\'s class exceeds it, and then the landlord recovers only its ratable share of the excess.',
  dependencies=['NY:EPTL-12-1.1-distributee-liability'],
  quote=q(O, 'Distributees and testamentary beneficiaries are liable, as provided in 12-1.1, in the following order:'),
  severity='minor', walk_step='8.1')]}])
X = 'NY:EPTL 12-1.3'
add([{'section_id': X, 'decision': 'new_rule', 'reason': 'Caps each heir\'s liability at its ratable share, which sets what the landlord may finally recover from each.', 'proposed': [rule(X,
  id='NY:EPTL-12-1.3-ratable', instrument='NY Estates, Powers and Trusts Law', provision='EPTL 12-1.3(a)', actor='landlord or its collector', modality='limit',
  condition='The landlord obtains judgment against an heir or beneficiary of a deceased former tenant under NY:EPTL-12-1.1-distributee-liability.',
  effect='The judgment may be for the full value of the property the defendant received, but the defendant\'s maximum liability is its ratable obligation: the proportion that the property passing to it bears to all property passing to persons in its order of liability. A defendant who pays more recovers the excess by contribution or indemnity from the others, not from the landlord.',
  dependencies=['NY:EPTL-12-1.1-distributee-liability', 'NY:EPTL-12-1.2-order'],
  quote=q(X, 'the maximum liability to which a distributee or testamentary beneficiary is subject under this article is his ratable obligation'),
  severity='major', walk_step='8.1')]}])
T = 'NY:EPTL 12-2.1'
add([{'section_id': T, 'decision': 'new_rule', 'reason': 'Decides that missing the claim presentation to the fiduciary does not bar suit against heirs, and that the limitation period is not extended.', 'proposed': [rule(T,
  id='NY:EPTL-12-2.1-unpresented-claim', instrument='NY Estates, Powers and Trusts Law', provision='EPTL 12-2.1', actor='landlord or its collector', modality='permission',
  condition='The landlord did not present its claim for a deceased former tenant\'s balance to the executor or administrator (NY:ADJ-tenant-death-payee), and the estate has been distributed.',
  effect='The failure to present does not bar a suit against the heirs or beneficiaries under NY:EPTL-12-1.1-distributee-liability, but the suit must still be brought within the limitation period for the lease claim (NY:CPLR-213(2), extended only by NY:CPLR-210-death).',
  dependencies=['NY:EPTL-12-1.1-distributee-liability', 'NY:CPLR-210-death'],
  quote=q(T, 'The failure of the plaintiff to present his claim to the personal representative as prescribed by law shall not impair his right to maintain an action against distributees or testamentary beneficiaries under this article; but nothing contained herein shall extend the time limited for the commencement of an action to enforce plaintiff’s claim.'),
  severity='major', walk_step='8.10')]}])
add([
 nd('NY:EPTL 12-2.2', 'Joinder and impleader among heirs; who is liable and for how much is proposed at EPTL 12-1.1 to 12-1.3.'),
 nd('NY:EPTL 12-2.3', 'Stays enforcement against a decedent\'s real property during an estate accounting; it changes neither liability nor amount of a lease balance.'),
 nd('NY:EPTL 12-2.4', 'Ranks a judgment against an heir ahead of that heir\'s personal creditors on the inherited property; priority among the heir\'s creditors changes nothing the landlord does or recovers.'),
 nd('NY:EPTL 12-2.5', 'Protects good-faith purchasers of inherited property; affects which asset a judgment reaches, not whether or how much the landlord recovers.'),
 nd('NY:Executive Law 296-D', 'Employer liability for discrimination against contractors in its workplace; employment law, outside the tenancy chain.'),
 nd('NY:Executive Law 298', 'Judicial review of Division of Human Rights orders; procedure after an agency ruling, not a decision in the settlement chain (liability is stated by NY:EXC-297(9)-remedies).'),
 nd('NY:Executive Law 298-A', 'Reaches discrimination committed outside the state against New York residents; settling an NYC unit is conduct within the state, already reached by NY:EXEC-296(5)(a)(2)-terms.'),
 nd('NY:Executive Law 300', 'Canon of liberal construction and election of remedies for the complainant; the housing exemptions in NY:EXEC-296(5)(a)(2)-terms are stated as fixed conditions, so their reach does not change.'),
])
