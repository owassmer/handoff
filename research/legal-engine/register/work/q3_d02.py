import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *

A = "register/texts/NYC_ADC/"
dec("NYC:ADC 20-117", "partial",
    "GBL 899-aa breach notice is stated; the added duty of a DCWP licensee (a licensed collector, or Handoff if "
    "licensed) to send DCWP a copy is not.", ["NY:GBL-899-aa-breach-notice"],
    [rule("NYC:ADC-20-117-breach-copy-to-DCWP", "Admin. Code 20-117", "DCWP-licensed debt collection agency "
          "(including Handoff when licensed)", "duty",
          "A person required to hold a DCWP licence (e.g. a debt collection agency collecting a former tenant's "
          "balance) must notify affected residents of a security breach under GBL 899-aa(2) or (3).",
          "It must promptly submit a copy of that notification to DCWP, without delaying the notice to the affected "
          "individuals. An owner or manager that holds no DCWP licence has no duty under this section (its duty is "
          "NY:GBL-899-aa-breach-notice alone).",
          A + "20-117.txt", q(A + "20-117.txt", "shall promptly submit a copy of such notification to the department.",
                              None), "minor", "6.10", dependencies=["NY:GBL-899-aa-breach-notice", "NYC:ADC-20-490"],
          effective_from="2022-04-10")])
nd("NYC:ADC 20-119", "Penalties for the general licensing chapter (display, address, trade-name duties) that "
   "decide nothing in the settlement chain; debt-collection penalties are in 20-494.")
nd("NYC:ADC 20-492", "Licence application contents; whether a licence is required is stated (NYC:ADC-20-490), "
   "and the application form decides no settlement step.")
dec("NYC:ADC 20-493", "new_rule",
    "Subdivision (d) makes a licensed debt collection agency answerable for its employees' and agents' acts; this "
    "decides who is liable for collection conduct on a handed-off balance. Rulemaking and investigation powers "
    "decide nothing.",
    proposed=[rule("NYC:ADC-20-493(d)-agency-vicarious", "Admin. Code 20-493(d)",
                   "DCWP-licensed debt collection agency (incl. Handoff when licensed)", "liability",
                   "A licensed debt collection agency's employee or agent makes a statement, representation or promise "
                   "or does an act while collecting a former tenant's balance.",
                   "For the debt collection agency subchapter, the licensee may be held responsible for the act if it "
                   "was within the scope of the employee's or agent's authority. It is not responsible for acts "
                   "contrary to its instructions, or amounting to gross negligence or an intentional tort, unless it "
                   "specifically authorized them.",
                   A + "20-493.txt", q(A + "20-493.txt", "licensees may be held responsible for statements",
                                       "unless specifically authorized by the licensee."),
                   "major", "8.6", determinacy="MIXED",
                   judgment_terms=["within the scope of their authority", "contrary to instructions",
                                   "gross negligence or intentional torts"],
                   dependencies=["NYC:ADC-20-490"])])
nd("NYC:ADC 20-494.1", "Child support collection practices; no tenancy balance is child support.")
nd("NYC:ADC 20-704", "DCWP's power to accept assurances of discontinuance; an agency enforcement choice, not a "
   "step for the landlord, manager, collector or tenant in the settlement.")
nd("NYC:ADC 20-808", "Screening-report disclosures when application information is requested from a prospective "
   "tenant; happens before the lease and fixes nothing the settlement uses.")
nd("NYC:ADC 20-809", "Screening-report sign at rental offices; decides nothing in the settlement.")
nd("NYC:ADC 20-810", "Penalties for the screening disclosure and sign rules, which decide nothing in the chain.")
nd("NYC:ADC 20-811", "DCWP hearing authority for screening disclosure violations; no chain decision.")
nd("NYC:ADC 26-1103", "Posting a notice of the housing information guide in a multiple dwelling; no settlement "
   "step depends on it.")
nd("NYC:ADC 26-1104", "Penalty for the housing-guide posting duty, which decides nothing in the chain.")
nd("NYC:ADC 26-1201", "Bars conditioning occupancy or its terms on medical treatment; no settlement step "
   "(deposit, charges, statement, collection) turns on medical treatment.")
nd("NYC:ADC 26-1202", "Private action for a 26-1201 violation, with setoff of delinquent rent against the award; "
   "arises only on that violation, which no settlement step involves.")
dec("NYC:ADC 26-2403", "new_rule",
    "A tenancy that ends by a buyout (owner pays the tenant to surrender and vacate) triggers an owner filing duty "
    "with HPD within 90 days; no rule states it.",
    proposed=[rule("NYC:ADC-26-2403-buyout-filing", "Admin. Code 26-2403", "owner (manager or Handoff filing for it)",
                   "duty",
                   "The tenancy ends by a buyout agreement (NYC:ADC-26-2402-buyout-definition) executed on or after "
                   "2020-07-01: the owner gave money or other consideration to induce a person lawfully entitled to "
                   "occupy the unit to surrender or waive occupancy rights, and the tenant vacated. Any NYC dwelling "
                   "unit, market-rate included.",
                   "Within 90 days after executing the agreement the owner must file electronically with HPD, as HPD "
                   "prescribes: the owner's name; the unit address; the amount of money or a description of other "
                   "consideration (including, where the consideration was dismissal of a pending action, its caption, "
                   "index number and county); the execution date; and the months remaining on the lease (unlimited "
                   "where the tenant had a legal right to renewal under state law). A consideration that is a waiver "
                   "or credit of the tenant's balance on the move-out account is 'other valuable consideration' and "
                   "is described in the filing. Late or missing filing: NYC:ADC-26-2405-buyout-penalty.",
                   A + "26-2403.txt", q(A + "26-2403.txt", "Within 90 days after the execution of a buyout agreement",
                                        "in a manner prescribed by the commissioner of the department:"),
                   "major", "3.3", dependencies=["NYC:ADC-26-2402-buyout-definition", "NYC:ADC-26-2401-buyout-scope"],
                   effective_from="2020-07-01")])
dec("NYC:ADC 26-2405", "new_rule", "Consequence of a missed buyout filing; not stated.",
    proposed=[rule("NYC:ADC-26-2405-buyout-penalty", "Admin. Code 26-2405", "owner", "consequence",
                   "An owner required to file a buyout agreement fails to file within the 90 days of 26-2403.",
                   "The owner is liable for a non-hazardous HMC violation under Admin. Code 27-2115. The failure does "
                   "not undo the buyout agreement or the surrender.",
                   A + "26-2405.txt", q(A + "26-2405.txt", "shall be liable for a non-hazardous violation",
                                        "pursuant to section 27-2115."),
                   "minor", "3.3", dependencies=["NYC:ADC-26-2403-buyout-filing"])])
dec("NYC:ADC 26-2401", "new_rule", "Sets the temporal reach of the buyout filing duty.",
    proposed=[rule("NYC:ADC-26-2401-buyout-scope", "Admin. Code 26-2401", "owner", "applicability",
                   "A buyout agreement for an NYC dwelling unit.",
                   "Chapter 24 (buyout filing) applies to every buyout agreement executed on or after its effective "
                   "date, 2020-07-01 (L.L. 2019/102); an agreement executed earlier needs no filing.",
                   A + "26-2401.txt", q(A + "26-2401.txt", "This chapter applies to all buyout agreements",
                                        "effective date of this chapter."), "minor", "3.3",
                   effective_from="2020-07-01")])
dec("NYC:ADC 26-2402", "new_rule", "Defines 'buyout agreement', which sets the reach of the filing duty.",
    proposed=[rule("NYC:ADC-26-2402-buyout-definition", "Admin. Code 26-2402 ('Buyout agreement')", "owner",
                   "definition",
                   "The owner of a dwelling unit gives money or other valuable consideration to a person lawfully "
                   "entitled to occupy it.",
                   "It is a buyout agreement if the consideration is exchanged to induce that person to surrender or "
                   "waive occupancy rights and it results in the tenant vacating. A mutual early-termination agreement "
                   "in which the owner gives anything of value (cash, a waiver of rent or charges owed, return of more "
                   "of the deposit than is owed) and the tenant vacates is one; an ordinary move-out at lease end with "
                   "no inducement is not.",
                   A + "26-2402.txt", q(A + "26-2402.txt", "The term \"buyout agreement\" means",
                                        "that results in the tenant vacating such unit."), "major", "3.3",
                   determinacy="MIXED", judgment_terms=["to induce ... to surrender or waive any rights"])])
nd("NYC:ADC 26-2404", "HPD's annual report to the Mayor and Council on buyouts; binds no party in the chain.")
dec("NYC:ADC 26-3401", "new_rule", "Defines the duty to mitigate by reference to RPL 227-e, which fixes when the "
    "26-3402 ceiling applies.",
    proposed=[rule("NYC:ADC-26-3401-mitigation-definition", "Admin. Code 26-3401", "landlord", "definition",
                   "Applying the vacating-fee ceiling of Admin. Code 26-3402.",
                   "The ceiling applies exactly when the landlord has the RPL 227-e duty to mitigate: the tenant "
                   "vacated in violation of the lease terms. It does not apply when the tenancy ended at its term, by "
                   "proper notice, or under a statutory termination right.",
                   A + "26-3401.txt", q(A + "26-3401.txt", "the term \"duty to mitigate damages\" means",
                                        "section 227-e of the real property law."), "major", "3.3",
                   dependencies=["NY:RPL-227-e", "NYC:ADC-26-3402-vacating-fee-cap"], effective_from="2022-06-22")])
nd("NYC:ADC 26-3004", "Smart-access privacy policy given to tenants during the tenancy; the move-out data duties "
   "that decide the chain are NYC:ADC-26-3002(c)-moveout-data and NYC:ADC-26-3003-3006-data-sale.")
commit()
