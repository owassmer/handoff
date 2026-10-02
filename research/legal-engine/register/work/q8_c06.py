import sys; sys.path.insert(0, "register/work")
from q8_lib import D, P, q, save
N = "no_decision"
F803 = "register/texts/NY_PTR/121-803.txt"
F804 = "register/texts/NY_PTR/121-804.txt"
r803 = P("NY:PTR-121-803-dissolved-owner-winding-up", "Partnership Law 121-803", "persons winding up a dissolved owner limited partnership; managing agent; collector", "may / must",
  "The owner is a New York limited partnership that is dissolved (121-801 or 121-802) before a departing tenant's account is closed.",
  "Dissolution does not end the settlement or the claim. The persons winding up act in the partnership's name: the general partners who did not wrongfully dissolve it, or if none the limited partners, or, where the Supreme Court winds up the affairs on a partner's application or after a judicial dissolution under 121-802 (to which the partners' own winding-up right does not extend), the receiver or liquidating trustee it appoints. They may send the statement and refund, settle, and prosecute or defend suits in the partnership's name, including a suit for the former tenant's balance; the manager and any collector take instructions and pay remittances only to them. The deposit stays the tenant's trust money (NY:GOL-7-103(1)-trust) and is returned or applied under the deposit rules, not distributed to partners.",
  F803, q(F803, "Upon dissolution of a limited partnership, the persons winding up the limited partnership’s affairs may, in the name of", "discharge the limited partnership’s liabilities"),
  "major", "0.5", jurisdiction="NY", instrument="NY Partnership Law art. 8-A (Revised Limited Partnership Act)", dependencies=["NY:GOL-7-103(1)-trust"])
r804 = P("NY:PTR-121-804-creditors-before-partners", "Partnership Law 121-804(a)", "persons winding up a dissolved owner limited partnership", "must",
  "A dissolved owner limited partnership winds up while a former tenant's refund, interest or damages claim (for example 7-108(1-a)(g) damages) is unpaid or in dispute.",
  "The partnership's assets go first to creditors, the former tenant included, by payment or by an adequate reserve for the claim, before any distribution to partners on their interests or contributions.",
  F804, q(F804, "to creditors, including partners who are creditors, to the extent permitted by law, in satisfaction of liabilities of the limited partnership, whether by payment or by establishment of adequate reserves"),
  "minor", "7.6", jurisdiction="NY", instrument="NY Partnership Law art. 8-A (Revised Limited Partnership Act)", dependencies=["NY:GOL-7-108(1-a)(g)"])
save([
 D("NY:Partnership Law 121-705", N, "Assignor and assignee liability for contributions after an assignment; internal partnership governance."),
 D("NY:Partnership Law 121-801", N, "Events that dissolve a limited partnership; the settlement consequence of dissolution is the winding-up rule proposed under 121-803."),
 D("NY:Partnership Law 121-802", N, "Judicial dissolution on a partner's application; the settlement consequence is in the winding-up rule proposed under 121-803."),
 D("NY:Partnership Law 121-803", "new_rule", "Decides who sends the statement and refund and who may sue for the balance in the owner's name after the owner limited partnership dissolves; no rule covers a dissolved owner entity.", proposed=[r803]),
 D("NY:Partnership Law 121-804", "new_rule", "On winding up, creditors including the former tenant are paid or reserved for before partners; decides that a tenant's unpaid refund or damages claim survives the owner's dissolution ahead of distributions.", proposed=[r804]),
 D("NY:Partnership Law 121-901", N, "Home-state law governs a foreign limited partnership's internal affairs and limited partners' liability; no settlement step turns on it."),
 D("NY:Partnership Law 121-903", N, "Amendment of a foreign LP's application for authority, including a name change within 90 days; unlike N-PCL 1309(b) no suspension attaches, so capacity is unaffected."),
 D("NY:Partnership Law 121-903-A", N, "Certificate of change of office, process address or agent for a foreign LP; filing mechanics."),
 D("NY:Partnership Law 121-904", N, "Effect of a foreign LP's authority and its powers; capacity is tested by whether authority exists under the proposed NY:PTR-121-907-foreign-lp-authority."),
 D("NY:Partnership Law 121-905", N, "Surrender of a foreign LP's authority and continued service on the Secretary of State; affects service of the tenant's process, and a partnership still doing business after surrender falls under the proposed 121-907 bar."),
 D("NY:Partnership Law 121-908", N, "Attorney General actions against unauthorized foreign LPs; an annulled partnership is without authority, which the proposed 121-907 bar already covers."),
 D("NY:RPAPL 101", N, "Short title of the RPAPL."),
 D("NY:RPAPL 1315", N, "Junior mortgage participant's foreclosure action; lender remedy, not a tenancy settlement step."),
 D("NY:RPAPL 1352", N, "Judgment foreclosing a right of redemption after a foreclosure sale; title matter, the tenant's position after foreclosure is in NY:RPAPL-1305-successor."),
 D("NY:RPAPL 1361", N, "Claims to surplus money after a foreclosure sale; lienholder procedure, no settlement step."),
 D("NY:RPAPL 611", N, "Actions that cannot be maintained (dower, six-inch strips, mortgagee ejectment); not a tenancy settlement matter."),
 D("NY:RPAPL 812", N, "Ward's waste action against a guardian; not a landlord-tenant matter."),
 D("NY:RPAPL 882", N, "Severability clause of an RPAPL article; decides nothing."),
 D("NY:RPL 1", N, "Short title of the Real Property Law."),
 D("NY:RPL 210", N, "Short title of the Good Cause Eviction Law with its 2034-06-15 repeal note; the sunset is already carried in the walk's Good Cause rules (NY:RPL-212 and related)."),
 D("NY:RPL 240-B", N, "Conveyances naming the grantor as a grantee; title form, no settlement consequence."),
 D("NY:RPL 241", N, "Abolishes ancient conveyance forms; decides nothing."),
 D("NY:RPL 242", N, "Seller disclosures to purchasers (no electric service, utility surcharges, gas wells, on-bill charges); runs between seller and buyer, not to the tenant or the account."),
 D("NY:RPL 246", N, "Bargain-and-sale deeds are grants; title form."),
 D("NY:RPL 249", N, "No implied covenant to pay in a mortgage; lender remedy."),
 D("NY:RPL 253", N, "Construction of deed covenants between grantor and grantee; no settlement consequence."),
 D("NY:RPL 255", N, "Construction of the deed clause granting appurtenances, rents and the grantor's rights; Getty Realty (the authority in NY:RPL-223) held a deed without an express transfer of arrears passes none, so this clause does not change who owns pre-sale rent."),
 D("NY:RPL 256", N, "Construction of an executor's or trustee's deed clause; title form, same reasoning as RPL 255."),
 D("NY:RPL 260", N, "Conveyance valid despite adverse possession; title matter."),
 D("NY:RPL 261", N, "No prescriptive right from utility wires; not a tenancy matter."),
])
