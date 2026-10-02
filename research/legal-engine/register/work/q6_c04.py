"""q6 chunk 4: Reg F remainder, FDCPA remainder, CFPA (12 USC 55xx)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q6_lib import D, P, q, save, tf

fh = tf("US:15 USC 1692h")
f36 = tf("US:12 USC 5536")
f31 = tf("US:12 USC 5531")
f17 = tf("US:12 USC 5517")
CFPA = "Consumer Financial Protection Act of 2010, 12 U.S.C. 5481-5603"

r_h = P("US:15USC1692h-multiple-debts", "15 U.S.C. 1692h", "debt collector", "must",
        "A debt collector (for Handoff by configuration, US:HANDOFF-config-*) collects more than one debt from the same "
        "former tenant (for example balances from two leases or units, or a lease balance and another placed debt) and "
        "receives a single payment.",
        "It may not apply any of the payment to a debt the tenant disputes, and where the tenant directs how the payment "
        "is applied it must follow that direction.",
        fh, q(fh, "such debt collector may not apply such payment to any debt which is disputed by the consumer and, where applicable, shall apply such payment in accordance with the consumer’s directions."),
        "major", "8.3", instrument="Fair Debt Collection Practices Act, 15 U.S.C. 1692-1692p",
        dependencies=["US:15USC1692a(5)", "US:15USC1692a(6)-regularly-another"])

r_reach = P("US:12USC5536-cfpa-udaap-reach", "12 U.S.C. 5536(a); 5531(c)-(d); 5481(15)(A)(ii)", "landlord; managing agent; Handoff; collector",
            "scope",
            "Deciding whether the federal ban on unfair, deceptive or abusive acts in the Consumer Financial Protection Act "
            "reaches conduct in settling or collecting a former tenant's account.",
            "It binds only a covered person or service provider in connection with a consumer financial product or service. "
            "(1) An ordinary residential lease is not a consumer financial product (US:12USC5481(15)(A)(ii)), so the landlord "
            "or manager settling the account, and anyone collecting the lease balance, including Handoff or a collection "
            "agency, is not covered by it for that activity; New York's own unfair and abusive practices ban "
            "(NY:GBL-349-unfair-abusive) and the FDCPA still apply. (2) A payment plan for the balance is an extension of "
            "credit; the landlord offering it is covered only in the branches US:12USC5517(a)(2)-landlord-credit leaves "
            "open, and then may not engage in an act that is unfair (substantial injury not reasonably avoidable and not "
            "outweighed by benefits) or abusive (materially interfering with understanding a term, or taking unreasonable "
            "advantage of a lack of understanding, inability to protect interests, or reasonable reliance). (3) Anyone who "
            "knowingly or recklessly gives substantial assistance to a covered person's violation is liable to the same "
            "extent. Enforcement is by the CFPB and state attorneys general; the Act gives the tenant no private action.",
            f36, q(f36, "any covered person or service provider—", "to engage in any unfair, deceptive, or abusive act or practice;"),
            "critical", "5.10", determinacy="MIXED", judgment_terms=["unfair", "abusive", "substantial assistance"],
            instrument=CFPA, dependencies=["US:12USC5481(15)(A)(ii)", "US:12USC5517(a)(2)-landlord-credit", "US:15USC1602(f)"],
            construction=[(f31, q(f31, "the act or practice causes or is likely to cause substantial injury to consumers which is not reasonably avoidable by consumers; and")),
                          (f31, q(f31, "materially interferes with the ability of a consumer to understand a term or condition of a consumer financial product or service; or")),
                          (f36, q(f36, "any person to knowingly or recklessly provide substantial assistance to a covered person or service provider in violation of the provisions of section 5531 of this title"))],
            reasoning="5536(a)(1) confines the prohibition to covered persons and service providers; 5481(15)(A)(ii) takes an "
                      "ordinary lease out of 'financial product or service', so neither the lease nor collection of its "
                      "balance is a covered activity; a payment plan is credit and is governed by the 5517(a)(2) merchant "
                      "exclusion. The Act provides CFPB and state enforcement (12 U.S.C. 5552, 5564), not a consumer action.")

r_merch = P("US:12USC5517(a)(2)-landlord-credit", "12 U.S.C. 5517(a)(2)(A)-(C)", "landlord; managing agent", "scope",
            "The landlord (a seller of a nonfinancial service, the tenancy) gives a former tenant a payment plan or other "
            "deferral for rent or move-out charges it is owed.",
            "The CFPA does not reach that credit or the landlord's collection of it (directly or through an agent), or its "
            "sale of the plan once in default, unless: (i) the landlord assigns or sells the plan debt before default; (ii) "
            "the credit significantly exceeds the market value of the tenancy or is a subterfuge; or (iii) the landlord "
            "regularly extends credit subject to a finance charge. Even under (iii), the exclusion stands if the landlord "
            "is not significantly engaged in consumer financial products, which it is deemed not to be if it only extends "
            "credit for its own tenancies, keeps the credit on its own books (except selling defaulted debt) and is a "
            "small business under the Small Business Act size standard. Where the exclusion stands, state attorneys "
            "general also cannot bring CFPA claims about it.",
            f17, q(f17, "extends credit directly to a consumer, in a case in which the good or service being provided is not itself a consumer financial product or service",
                   "exclusively for the purpose of enabling that consumer to purchase such nonfinancial good or service directly from the merchant, retailer, or seller;"),
            "major", "8.1b", determinacy="MIXED", judgment_terms=["significantly exceeds the market value", "regularly extends credit"],
            instrument=CFPA, dependencies=["US:15USC1602(f)", "US:12USC5481(15)(A)(ii)"],
            construction=[(f17, q(f17, "in which the merchant, retailer, or seller of nonfinancial goods or services regularly extends credit and the credit is subject to a finance charge.")),
                          (f17, q(f17, "retains such credit on its own accounts (except to sell or convey such debt that is delinquent or otherwise in default); and"))],
            reasoning="5517(a)(2)(A) excludes merchant credit for its own nonfinancial service; (B) lists the exceptions; (C)(i)-(ii) "
                      "and (D)(ii) restore the exclusion for a small merchant-creditor; (E) bars state CFPA claims where it holds.")

save([
    D("US:12 CFR 1006.104", "stated", "US:15USC1692n states the same relation to state law: state rules apply unless "
      "inconsistent, and greater protection is not inconsistent.", ["US:15USC1692n"]),
    D("US:12 CFR Appendix_B_to_Part_1006", "stated", "Model Form B-1 safe harbor is stated by US:12CFR1006.34(d)(2); the "
      "register text holds only the form's title.", ["US:12CFR1006.34(d)(2)"]),
    D("US:12 CFR Appendix_C_to_Part_1006", "no_decision", "Advisory-opinion procedure; the only listed opinion concerns "
      "mortgage servicing, not a tenancy balance."),
    D("US:12 CFR Appendix_A_to_Part_1006", "no_decision", "Procedure for a State to apply for a 1692o exemption; New York "
      "has none (US:15USC1692o-NY-VA-none), so the procedure decides nothing for an NYC unit."),
    D("US:15 USC 1692h", "new_rule", "A collector receiving one payment on several debts may not apply it to a disputed "
      "debt and must follow the tenant's direction.", proposed=[r_h]),
    D("US:15 USC 1692l", "no_decision", "Allocates administrative enforcement among agencies; the tenant's remedies are "
      "stated in US:15USC1692k(a)."),
    D("US:15 USC 1692p", "no_decision", "Excludes private operators of prosecutor-run bad-check diversion programs; no "
      "landlord, manager, Handoff or collector in the chain runs one."),
    D("US:15 USC 1692", "no_decision", "Congressional findings and purpose; decides nothing."),
    D("US:12 USC 5536", "new_rule", "Decides whether the federal UDAAP ban reaches the landlord, Handoff or a collector: "
      "not for the lease balance, only for a payment plan outside the merchant exclusion.", proposed=[r_reach]),
    D("US:12 USC 5517", "new_rule", "The merchant exclusion decides whether a landlord's payment plan brings it under "
      "the CFPA; the other exclusions (brokers, accountants, auto dealers, etc.) do not reach the chain.", proposed=[r_merch]),
    D("US:12 USC 5531", "no_decision", "Grants CFPB authority and sets the unfairness and abusiveness tests, which bind "
      "only covered persons; their content is carried in the branch stated at proposed US:12USC5536-cfpa-udaap-reach."),
    D("US:12 USC 5533", "no_decision", "Data-access duty of covered persons for consumer financial products; a lease "
      "balance is not one (US:12USC5481(15)(A)(ii))."),
    D("US:12 USC 5518", "no_decision", "CFPB authority to restrict pre-dispute arbitration in consumer financial products; "
      "no rule under it binds a lease."),
    D("US:12 USC 5532", "no_decision", "CFPB disclosure rulemaking for consumer financial products; no rule under it "
      "reaches a lease balance."),
    D("US:12 USC 5534", "no_decision", "Complaint-response duties of large insured depository institutions and covered "
      "persons; not a landlord or its lease balance."),
    D("US:12 USC 5511", "no_decision", "Purpose and functions of the CFPB; decides nothing."),
    D("US:12 USC 5514", "no_decision", "CFPB supervision of nondepository covered persons; supervisory, and a lease-balance "
      "collector is not a covered person for that activity."),
    D("US:12 USC 5538", "no_decision", "Mortgage-loan modification and foreclosure-rescue rulemaking; no tenancy decision."),
    D("US:12 USC 5512", "no_decision", "CFPB general rulemaking authority; decides nothing in the chain."),
])
