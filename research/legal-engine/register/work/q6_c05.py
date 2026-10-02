"""q6 chunk 5: FCRA (15 USC 1681-1681x) and Regulation V (12 CFR 1022)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q6_lib import D, P, q, save, tf

FCRA = "Fair Credit Reporting Act, 15 U.S.C. 1681-1681x"
REGV = "Regulation V, 12 CFR part 1022 (CFPB)"
S2 = "sources/US_15USC_1681s-2.txt"
T = {k: tf(k) for k in ["US:15 USC 1681t", "US:15 USC 1681c–2", "US:15 USC 1681m", "US:15 USC 1681n", "US:15 USC 1681o",
                        "US:15 USC 1681p", "US:15 USC 1681q", "US:15 USC 1681h", "US:15 USC 1681s", "US:15 USC 1681i",
                        "US:15 USC 1681c–1", "US:15 USC 1681d", "US:15 USC 1681a", "US:12 CFR 1022.82", "US:12 CFR 1022.3",
                        "US:15 USC 1681w", "US:15 USC 1681g"]}

ft = T["US:15 USC 1681t"]
r_pre = P("US:15USC1681t(b)(1)(F)-furnisher-preemption", "15 U.S.C. 1681t(a), (b)(1)(F), (b)(5)(C), (H), (I)",
          "landlord; managing agent; Handoff; collector (as furnisher)", "scope",
          "A landlord, manager, Handoff or collector reports (furnishes) a former tenant's balance to a consumer reporting "
          "agency, or holds consumer-report information, and a New York State or New York City rule would impose a "
          "requirement or prohibition on that furnishing or disposal.",
          "(1) No state or city requirement or prohibition applies with respect to any subject matter regulated under "
          "1681s-2 (the furnisher's accuracy duties, dispute notation, notice to the consumer of negative furnishing, "
          "identity-theft refurnishing, delinquency date, investigation of disputes). In the chain this means: (a) the NYC "
          "SHIELD pre-reporting notice and 14-day wait (NYC:SHIELD-5-77(e)(10)-credit-report-notice) does not bind a "
          "furnisher; (b) the GBL 604-bb(3)(a) duty to tell a consumer reporting agency that a coerced-debt account is "
          "disputed does not bind; the rest of 604-bb (stopping collection, review, determinations) stands; (c) RPL "
          "227-c(5)(b) does not govern what is furnished to a consumer reporting agency, where the federal accuracy duty "
          "(US:15USC1681s-2(a)(1)(A)) already bars reporting a lawful 227-c termination as an early termination; it still "
          "governs communications to prospective landlords, collectors and other third parties. The federal rules then "
          "govern alone, including the FDCPA and Regulation F rule that a debt collector first communicate with the "
          "tenant before furnishing (US:12CFR1006.30(a)). (2) State or city law on other subjects (collection conduct, "
          "deposit law, the content of collection letters) still applies unless inconsistent (1681t(a)). (3) For "
          "information derived from consumer reports (for example the move-in screening report), disposal is governed by "
          "the 1681w disposal regulations, not by state disposal law; NY:GBL-399-h-disposal governs the rest of the file.",
          ft, q(ft, "No requirement or prohibition may be imposed under the laws of any State—"),
          "critical", "8.7", determinacy="MIXED", judgment_terms=["subject matter regulated under section 1681s-2"],
          instrument=FCRA,
          dependencies=["US:15USC1681s-2(a)(1)(A)", "US:15USC1681s-2(a)(3)", "US:12CFR1006.30(a)",
                        "NYC:SHIELD-5-77(e)(10)-credit-report-notice", "NY:GBL-604-bb-coerced-debt", "NY:RPL-227-c(5)(b)",
                        "NY:GBL-399-h-disposal"],
          construction=[(ft, q(ft, "section 1681s–2 of this title, relating to the responsibilities of persons who furnish information to consumer reporting agencies, except that this paragraph shall not apply—")),
                        (ft, q(ft, "with respect to the conduct required by the specific provisions of—")),
                        (S2, q(S2, "If any financial institution that extends credit and regularly and in the ordinary course of business furnishes information to a consumer reporting agency described in section 1681a(p) of this title furnishes negative information to such an agency regarding credit extended to a customer, the financial institution shall provide a notice of such furnishing of negative information, in writing, to the customer.")),
                        (S2, q(S2, "the person may not furnish the information to any consumer reporting agency without notice that such information is disputed by the consumer."))],
          reasoning="1681t(b)(1)(F) bars any state-law requirement 'with respect to any subject matter regulated under' 1681s-2; "
                    "the exceptions are only two named Massachusetts and California provisions. Notice to the consumer of "
                    "negative furnishing is regulated by 1681s-2(a)(7), dispute notation by 1681s-2(a)(3) and (a)(8), and "
                    "accuracy by 1681s-2(a)(1), so a city pre-reporting notice and a state duty to report a dispute are "
                    "within that subject matter. Preemption is by subject matter, not by conflict, so DCWP's exemption for "
                    "collectors bound by 1681s-2(a)(7) does not save the rest of 5-77(e)(10). The city rule is a "
                    "requirement 'imposed under the laws of' New York, because the city acts under legislative power the "
                    "State confers; the FCRA's definition of 'State' names jurisdictions, not the source of the rule. "
                    "1681t(b)(5)(I) similarly displaces state rules on the disposal conduct 1681w requires.")

fc2 = T["US:15 USC 1681c–2"]
r_idt = P("US:15USC1681c-2-furnisher-identity-theft", "15 U.S.C. 1681c-2(b); 1681s-2(a)(6)", "landlord; managing agent; Handoff; collector (as furnisher)",
          "must / must not",
          "The landlord or its agent furnishes a former tenant's balance to a consumer reporting agency, and either (a) the "
          "agency notifies it that the information may result from identity theft and a block has been requested, or (b) "
          "the consumer sends an identity theft report to the address the furnisher specified for such reports, stating "
          "that the account resulted from identity theft (for example a lease signed in the consumer's name by someone "
          "else).",
          "(a) It must have reasonable procedures to respond to the agency's notice so that it does not refurnish the "
          "blocked information. (b) It may not furnish that information to any consumer reporting agency unless it later "
          "knows, or is told by the consumer, that the information is correct. In either case, once notified under "
          "1681c-2 it may not sell the balance, transfer it for consideration, or place it for collection "
          "(US:15USC1681m(f)-(g)-identity-theft-debt).",
          fc2, q(fc2, "A consumer reporting agency shall promptly notify the furnisher of information identified by the consumer under subsection (a)—"),
          "critical", "8.7", instrument=FCRA,
          dependencies=["US:15USC1681m(f)-(g)-identity-theft-debt", "US:12CFR1022.3(i)-identity-theft-report"],
          construction=[(S2, q(S2, "A person that furnishes information to any consumer reporting agency shall have in place reasonable procedures to respond to any notification that it receives from a consumer reporting agency under section 1681c–2 of this title")),
                        (S2, q(S2, "the person may not furnish such information that purports to relate to the consumer to any consumer reporting agency, unless the person subsequently knows or is informed by the consumer that the information is correct."))],
          reasoning="1681c-2(b) triggers the furnisher duties in 1681s-2(a)(6)(A)-(B) and the transfer ban in 1681m(f).")

fm = T["US:15 USC 1681m"]
r_mfg = P("US:15USC1681m(f)-(g)-identity-theft-debt", "15 U.S.C. 1681m(f), (g)", "landlord; managing agent; Handoff; collector",
          "must not / must",
          "The landlord or anyone collecting for it has been notified under 1681c-2 that a former tenant's balance "
          "resulted from identity theft, or a debt collector collecting it for the landlord is told that information "
          "about the balance may be fraudulent or the result of identity theft.",
          "(f) No one may sell the balance, transfer it for consideration or place it for collection after the "
          "1681c-2 notice; this binds everyone collecting it after the notice. A transfer in a merger or sale of "
          "substantially all assets, or a required repurchase by the assignor, is not barred. (g) A debt collector "
          "collecting for the landlord must tell the landlord that the information may be fraudulent or the result of "
          "identity theft, and on the consumer's request give the consumer all the information it would be entitled to if "
          "it were disputing the balance (for a lease balance, the verification items of US:12CFR1006.38(d)(2)).",
          fm, q(fm, "No person shall sell, transfer for consideration, or place for collection a debt that such person has been notified under section 1681c–2 of this title has resulted from identity theft."),
          "critical", "8.2", instrument=FCRA, dependencies=["US:12CFR1006.38(d)(2)", "US:15USC1681c-2-furnisher-identity-theft"],
          construction=[(fm, q(fm, "notify the third party that the information may be fraudulent or may be the result of identity theft; and"))],
          reasoning="1681m(f)(1)-(3) bar placement after a 1681c-2 notice with three transfer exceptions; 1681m(g) sets the "
                    "collector's duties.")

fa = T["US:15 USC 1681a"]
r_adv = P("US:15USC1681m(a)-adverse-action", "15 U.S.C. 1681m(a); 1681a(k)", "landlord; managing agent; Handoff", "must",
          "The landlord, manager or Handoff denies a former tenant's request for a payment plan (or grants one on less "
          "favorable terms than requested), or takes another action adverse to the tenant in a transaction the tenant "
          "initiated, based in whole or in part on information in a consumer report it obtained.",
          "It must give the tenant notice of the adverse action; any numerical credit score it used with its key factors; "
          "the name, address and telephone number of the consumer reporting agency that supplied the report and a "
          "statement that the agency did not make the decision; and notice of the right to a free report from that agency "
          "within 60 days and to dispute its accuracy. Oral, written or electronic delivery is allowed, except that the "
          "credit score disclosure is written or electronic.",
          fm, q(fm, "If any person takes any adverse action with respect to any consumer that is based in whole or in part on any information contained in a consumer report, the person shall—"),
          "major", "8.1b", determinacy="MIXED", judgment_terms=["based in whole or in part on"], instrument=FCRA,
          dependencies=["US:15USC1681b-1681c-report-limits", "US:15USC1602(f)"],
          construction=[(fa, q(fa, "an action taken or determination that is—", "adverse to the interests of the consumer."))],
          reasoning="1681a(k) makes a denial of requested credit (ECOA 1691(d)(6)) and any adverse determination in a "
                    "consumer-initiated transaction an adverse action; a payment plan is credit (US:15USC1602(f)).")

fn = T["US:15 USC 1681n"]
r_n = P("US:15USC1681n-willful", "15 U.S.C. 1681n(a)-(c)", "landlord; managing agent; Handoff; collector", "liable",
        "A landlord, manager, Handoff or collector willfully fails to comply with an FCRA duty toward a former tenant that "
        "is privately enforceable (for example investigating a dispute after notice from an agency, 1681s-2(b); obtaining "
        "a report only for a permissible purpose, 1681b(f); adverse action notice, 1681m(a)). Violations of 1681s-2(a) "
        "are not privately enforceable (US:15USC1681s-2(c)).",
        "It is liable to the tenant for actual damages or statutory damages of $100 to $1,000; where a natural person "
        "obtained a report under false pretenses or knowingly without a permissible purpose, actual damages or $1,000, "
        "whichever is greater; punitive damages as the court allows; and costs and reasonable attorney's fees. Anyone who "
        "obtains a report under false pretenses or knowingly without a permissible purpose also owes the agency its "
        "actual damages or $1,000, whichever is greater. A bad-faith or harassing filing earns the other side its fees.",
        fn, q(fn, "Any person who willfully fails to comply with any requirement imposed under this subchapter with respect to any consumer is liable to that consumer"),
        "critical", "8.7", determinacy="MIXED", judgment_terms=["willfully"], instrument=FCRA,
        dependencies=["US:15USC1681s-2(b)(1)", "US:15USC1681s-2(c)", "US:15USC1681b-1681c-report-limits"],
        construction=[(fn, q(fn, "any actual damages sustained by the consumer as a result of the failure or damages of not less than $100 and not more than $1,000; or"))],
        reasoning="1681n(a) sets willful liability for 'any person'; 1681s-2(c) removes 1681s-2(a) from its reach.")

fo = T["US:15 USC 1681o"]
r_o = P("US:15USC1681o-negligent", "15 U.S.C. 1681o", "landlord; managing agent; Handoff; collector", "liable",
        "A landlord, manager, Handoff or collector negligently fails to comply with a privately enforceable FCRA duty "
        "toward a former tenant (same scope as US:15USC1681n-willful).",
        "It is liable for the tenant's actual damages plus costs and reasonable attorney's fees; no statutory or punitive "
        "damages. A bad-faith or harassing filing earns the other side its fees.",
        fo, q(fo, "Any person who is negligent in failing to comply with any requirement imposed under this subchapter with respect to any consumer is liable to that consumer"),
        "critical", "8.7", determinacy="MIXED", judgment_terms=["negligent"], instrument=FCRA,
        dependencies=["US:15USC1681s-2(c)", "US:15USC1681n-willful"])

fp = T["US:15 USC 1681p"]
r_p = P("US:15USC1681p-limitations", "15 U.S.C. 1681p", "former tenant; landlord", "deadline",
        "A former tenant sues the landlord, manager, Handoff or a collector on FCRA liability (1681n, 1681o).",
        "The action must be brought by the earlier of 2 years after the tenant discovered the violation or 5 years after "
        "the violation occurred, in federal district court regardless of amount or any other court of competent "
        "jurisdiction. Records needed to defend a furnishing or report-pull decision are kept at least that long.",
        fp, q(fp, "not later than the earlier of—", "5 years after the date on which the violation that is the basis for such liability occurs."),
        "critical", "8.7", instrument=FCRA, dependencies=["US:15USC1681n-willful", "US:15USC1681o-negligent"])

fq = T["US:15 USC 1681q"]
r_q = P("US:15USC1681q-false-pretenses", "15 U.S.C. 1681q", "landlord; managing agent; Handoff; collector", "must not",
        "Anyone in the chain obtains information on a former tenant (or a co-tenant, guarantor or new occupant) from a "
        "consumer reporting agency by misstating its purpose or identity, for example certifying collection of an "
        "account for a person who owes nothing.",
        "Knowingly and willfully doing so is a federal crime punishable by a fine, up to 2 years' imprisonment, or both, "
        "in addition to civil liability (US:15USC1681n-willful).",
        fq, q(fq, "Any person who knowingly and willfully obtains information on a consumer from a consumer reporting agency under false pretenses shall be fined under title 18, imprisoned for not more than 2 years, or both."),
        "major", "8.7", determinacy="MIXED", judgment_terms=["knowingly and willfully", "false pretenses"], instrument=FCRA,
        dependencies=["US:15USC1681b-1681c-report-limits", "US:15USC1681n-willful"])

fh = T["US:15 USC 1681h"]
r_h = P("US:15USC1681h(e)-furnisher-immunity", "15 U.S.C. 1681h(e)", "landlord; managing agent; Handoff; collector", "immune except",
        "A former tenant sues a landlord, manager or collector that furnished the balance to a consumer reporting agency "
        "(or used a report and gave an adverse action notice) for defamation, invasion of privacy or negligence about "
        "the reporting, based on information the tenant learned through an agency disclosure (1681g, 1681h) or an "
        "adverse action notice (1681m).",
        "No such action lies unless the information was false and furnished with malice or willful intent to injure the "
        "tenant; FCRA liability under 1681n and 1681o is unaffected.",
        fh, q(fh, "no consumer may bring any action or proceeding in the nature of defamation, invasion of privacy, or negligence with respect to the reporting of information against any consumer reporting agency, any user of information, or any person who furnishes information to a consumer reporting agency",
              "except as to false information furnished with malice or willful intent to injure such consumer."),
        "major", "8.7", determinacy="MIXED", judgment_terms=["malice or willful intent to injure"], instrument=FCRA,
        dependencies=["US:15USC1681n-willful", "US:15USC1681t(b)(1)(F)-furnisher-preemption"])

fs = T["US:15 USC 1681s"]
r_s = P("US:15USC1681s-public-enforcement", "15 U.S.C. 1681s(a)(2), (c)(1)", "landlord; managing agent; Handoff; collector", "liable",
        "A landlord, manager, Handoff or collector violates the FCRA as a furnisher or user, including the 1681s-2(a) "
        "duties that tenants cannot enforce privately.",
        "The FTC may recover a civil penalty of up to $2,500 per violation (as adjusted for inflation) for a knowing "
        "violation that is a pattern or practice, but no penalty for a 1681s-2(a)(1) accuracy violation unless the person "
        "first violated an FTC injunction or order. The New York Attorney General may sue to enjoin, and on behalf of "
        "residents for their 1681n/1681o damages, for damages a 1681s-2(a) violation would cause but for 1681s-2(c), or "
        "for up to $1,000 per willful or negligent violation, plus costs and attorney's fees.",
        fs, q(fs, "in the event of a knowing violation, which constitutes a pattern or practice of violations of this subchapter",
              "such person shall be liable for a civil penalty of not more than $2,500 per violation."),
        "major", "8.7", determinacy="MIXED", judgment_terms=["knowing violation", "pattern or practice"], instrument=FCRA,
        dependencies=["US:15USC1681s-2(c)", "US:15USC1681s-2(a)(1)(A)"],
        construction=[(fs, q(fs, "damages of not more than $1,000 for each willful or negligent violation; and")),
                      (fs, q(fs, "a court may not impose any civil penalty on a person for a violation of section 1681s–2(a)(1) of this title, unless the person has been enjoined"))],
        reasoning="1681s(a)(2) sets FTC penalties with the (C) limit for accuracy violations; 1681s(c)(1)(B) gives the State "
                  "damages actions, including for 1681s-2(a) violations otherwise shielded by 1681s-2(c).")

fi = T["US:15 USC 1681i"]
r_i = P("US:15USC1681i-furnisher-deadline", "15 U.S.C. 1681i(a)(1)-(2), (a)(5); 1681j(a)(3)", "landlord; managing agent; Handoff; collector (as furnisher)",
        "deadline",
        "The former tenant disputes the reported balance with a consumer reporting agency, and the agency sends the "
        "furnisher notice of the dispute (it must do so within 5 business days of receiving it).",
        "The furnisher's investigation and report back (US:15USC1681s-2(b)(1)) must be completed within the agency's "
        "reinvestigation period: 30 days from the agency's receipt of the dispute, extended by up to 15 days if the "
        "tenant sends the agency relevant information during the 30 days (no extension once the item is found inaccurate "
        "or unverifiable), and 45 days where the dispute follows the tenant's free annual report. If the furnisher does "
        "not verify in time, the agency deletes or modifies the item and notifies the furnisher; the item may be "
        "reinserted only if the furnisher certifies it is complete and accurate.",
        fi, q(fi, "before the end of the 30-day period beginning on the date on which the agency receives the notice of the dispute from the consumer or reseller."),
        "critical", "8.7", instrument=FCRA, amends="US:15USC1681s-2(b)(1)", dependencies=["US:15USC1681s-2(b)(1)"],
        construction=[(fi, q(fi, "may be extended for not more than 15 additional days if the consumer reporting agency receives information from the consumer during that 30-day period that is relevant to the reinvestigation.")),
                      (fi, q(fi, "Before the expiration of the 5-business-day period beginning on the date on which a consumer reporting agency receives notice of a dispute")),
                      (fi, q(fi, "the information may not be reinserted in the file by the consumer reporting agency unless the person who furnishes the information certifies that the information is complete and accurate.")),
                      (tf("US:15 USC 1681j"), q(tf("US:15 USC 1681j"), "shall be completed not later than 45 days after the date on which the request is received."))],
        reasoning="1681s-2(b)(2) ties the furnisher's deadline to the 1681i(a)(1) period; 1681i(a)(1)(A)-(C), (a)(2), "
                  "(a)(5) and 1681j(a)(3) fix its length and the consequences.")

fc1 = T["US:15 USC 1681c–1"]
r_c1 = P("US:15USC1681c-1-freeze-alerts", "15 U.S.C. 1681c-1(h), (i)(4)(A)", "landlord; managing agent; Handoff; collector", "may / must",
         "The landlord or its agent (Handoff, a collector, an assignee of the balance) pulls a former tenant's consumer "
         "report to review or collect the lease account, and the tenant's file carries a security freeze, or an initial, "
         "extended or active-duty fraud alert.",
         "A security freeze does not block a report pulled by the landlord, its agent or assignee, or a prospective buyer "
         "of the balance, for reviewing or collecting the account or contract. If the report shows an initial or "
         "active-duty alert, the user may not establish a payment plan or other extension of credit in the tenant's name "
         "unless it uses reasonable procedures to form a reasonable belief that it knows who is asking (and, where the "
         "tenant gave a phone number for verification, calls it or takes reasonable steps to verify); with an extended "
         "alert, it must contact the tenant in person or by the contact method in the alert first.",
         fc1, q(fc1, "for the purposes of reviewing the account or collecting the financial obligation owed for the account, contract, or negotiable instrument."),
         "minor", "8.7", determinacy="MIXED", judgment_terms=["reasonable belief that the user knows the identity"], instrument=FCRA,
         dependencies=["US:15USC1681b-1681c-report-limits", "US:15USC1602(f)"],
         construction=[(fc1, q(fc1, "No prospective user of a consumer report that includes an initial fraud alert or an active duty alert in accordance with this section may establish a new credit plan or extension of credit"))],
         reasoning="1681c-1(i)(4)(A) excepts account review and collection by the person the consumer contracted with and its "
                   "agents and assignees; 1681c-1(h) limits new extensions of credit to a consumer with an alert.")

fd = T["US:15 USC 1681d"]
r_d = P("US:15USC1681d-investigative-report", "15 U.S.C. 1681d(a)-(c)", "landlord; managing agent; Handoff; collector", "must",
        "Anyone in the chain procures an investigative consumer report on a former tenant (character, reputation, "
        "personal characteristics or mode of living gathered by interviews with neighbors, friends or associates), for "
        "example to locate or assess the tenant for collection.",
        "It must disclose in writing, mailed or delivered within 3 days after first requesting the report, that such a "
        "report may be made, with the right to request the nature and scope of the investigation and the summary of "
        "rights; certify this to the agency; and on the tenant's written request disclose the nature and scope in "
        "writing within 5 days. It is not liable if it shows it kept reasonable procedures to comply.",
        fd, q(fd, "A person may not procure or cause to be prepared an investigative consumer report on any consumer unless—"),
        "minor", "8.7", instrument=FCRA, dependencies=["US:15USC1681b-1681c-report-limits"],
        construction=[(fd, q(fd, "is made in a writing mailed, or otherwise delivered, to the consumer, not later than three days after the date on which the report was first requested"))],
        reasoning="1681d(a) binds any person procuring the report; (b) sets the 5-day disclosure; (c) the procedures defense.")

r_own = P("US:15USC1681a(d)-(f)-own-experience-CRA", "15 U.S.C. 1681a(d)(1), (d)(2)(A)(i), (f)", "landlord; managing agent; Handoff",
          "scope",
          "The landlord, manager or Handoff communicates information about a former tenant's tenancy, balance or payment "
          "history to someone else. Branches: (a) the landlord (or its agent) states only its own experience with the "
          "tenant, to a collector, a consumer reporting agency, or a prospective landlord; (b) Handoff, for fees, "
          "regularly assembles or evaluates tenants' settlement or payment information from several owners and provides "
          "it to third parties (for example to other owners screening applicants).",
          "(a) A report containing only the landlord's own transactions or experiences with the tenant is not a consumer "
          "report, and the landlord is not a consumer reporting agency; when it sends that information to a consumer "
          "reporting agency it is a furnisher under 1681s-2 and Regulation V subpart E. (b) Handoff is then a consumer "
          "reporting agency and every communication used for eligibility is a consumer report, with the full agency "
          "duties (permissible purpose, accuracy procedures, disclosures, disputes). Handoff settling or collecting a "
          "tenancy for one owner, and reporting that owner's account to an agency, is branch (a).",
          fa, q(fa, "report containing information solely as to transactions or experiences between the consumer and the person making the report;"),
          "critical", "8.7", determinacy="MIXED", judgment_terms=["regularly engages in assembling or evaluating"], instrument=FCRA,
          dependencies=["US:15USC1681s-2(a)(1)(A)", "US:12CFR1022.42(a)"],
          construction=[(fa, q(fa, "The term “consumer reporting agency” means any person which, for monetary fees, dues, or on a cooperative nonprofit basis, regularly engages in whole or in part in the practice of assembling or evaluating consumer credit information or other information on consumers for the purpose of furnishing consumer reports to third parties"))],
          reasoning="1681a(d)(2)(A)(i) excludes first-party experience reports; 1681a(f) makes a regular fee-based assembler of "
                    "consumer information for third parties a consumer reporting agency. Which branch applies to Handoff is "
                    "an operating choice.")

f82 = T["US:12 CFR 1022.82"]
r_82 = P("US:12CFR1022.82-address-discrepancy", "12 CFR 1022.82(a)-(d)", "landlord; managing agent; Handoff; collector", "must",
         "The landlord or its agent requests a nationwide agency's report on a former tenant (for example to review or "
         "collect the account) and receives a notice of address discrepancy because the address it gave differs "
         "substantially from the agency's file.",
         "It must have and follow reasonable policies to form a reasonable belief that the report relates to the tenant "
         "(for example comparing the report with the lease application and its own records, or verifying with the "
         "tenant). The duty to furnish a confirmed address back to the agency arises only when the user establishes a "
         "continuing relationship with the consumer and regularly furnishes to that agency, which a collection pull on a "
         "former tenant does not.",
         f82, q(f82, "A user must develop and implement reasonable policies and procedures designed to enable the user to form a reasonable belief that a consumer report relates to the consumer about whom it has requested the report"),
         "minor", "8.7", determinacy="MIXED", judgment_terms=["reasonable belief"], instrument=REGV,
         dependencies=["US:15USC1681b-1681c-report-limits"],
         construction=[(f82, q(f82, "(ii) Establishes a continuing relationship with the consumer; and"))],
         reasoning="1022.82(c) binds every user receiving a discrepancy notice; (d)(1)(ii) limits the address-furnishing "
                   "duty to new continuing relationships.")

f3 = T["US:12 CFR 1022.3"]
r_3i = P("US:12CFR1022.3(i)-identity-theft-report", "12 CFR 1022.3(h), (i)", "landlord; managing agent; Handoff; collector (as furnisher)", "may / must",
         "A former tenant (or a person billed for a tenancy) gives the furnisher an identity theft report to stop it "
         "furnishing the balance (US:15USC1681c-2-furnisher-identity-theft).",
         "An identity theft report is a copy of an official report filed with a law enforcement agency (false filing "
         "being a crime) alleging identity theft as specifically as the consumer can. The furnisher may ask for "
         "additional information reasonably needed to judge validity within 15 days of receiving the report, make any "
         "supplemental request and final determination within another 15 days (5 days if the information arrives on the "
         "11th day or later); a detailed report bearing the officer's identification is sufficient on its face without "
         "an identifiable concern, while an automated report with a bare allegation may be supplemented by the "
         "CFPB identity theft affidavit and identification.",
         f3, q(f3, "(i)(1) Identity theft report means a report:", "if, in fact, the information in the report is false; and"),
         "major", "8.7", determinacy="MIXED", judgment_terms=["reasonably requests"], instrument=REGV,
         dependencies=["US:15USC1681c-2-furnisher-identity-theft"],
         construction=[(f3, q(f3, "Makes such request not later than fifteen days after the date of receipt of the copy of the report form"))],
         reasoning="1022.3(i)(1)(iii) sets the furnisher's windows for requesting more information; (i)(3) gives the examples.")

fw = T["US:15 USC 1681w"]
r_w = P("US:15USC1681w-disposal", "15 U.S.C. 1681w(a)(1), (b)", "landlord; managing agent; Handoff; collector", "must",
        "The landlord, manager, Handoff or a collector holds consumer information derived from a consumer report on the "
        "tenant (the move-in screening report, or a report pulled to collect) and disposes of the closed tenancy file.",
        "It must dispose of that information properly under the disposal regulations issued under 1681w (for non-bank "
        "persons, the FTC's rule); the section imposes no duty to keep or destroy records that other law does not.",
        fw, q(fw, "requiring any person that maintains or otherwise possesses consumer information, or any compilation of consumer information, derived from consumer reports for a business purpose to properly dispose of any such information or compilation."),
        "minor", "6.10", instrument=FCRA, dependencies=["US:15USC1681t(b)(1)(F)-furnisher-preemption", "NY:GBL-399-h-disposal"])

fg = T["US:15 USC 1681g"]
r_g = P("US:15USC1681g(e)-victim-records", "15 U.S.C. 1681g(e)", "landlord; managing agent; Handoff", "must",
        "A person claims that the tenancy (lease application, lease or payments) billed to them was made by someone who "
        "used their identity without authority, and sends the landlord a written request for the records, at any "
        "address the landlord specified.",
        "Within 30 days of the request, and after verifying identity and the claim (government ID or matching "
        "identifying information, plus, at the landlord's election, a police report and the CFPB affidavit or an "
        "acceptable affidavit of fact) unless it already has high confidence in the requester's identity, the landlord "
        "provides free copies of the application and transaction records it controls, including records kept for it by "
        "a manager or Handoff, to the victim or the law enforcement agency the victim names. It may decline in good "
        "faith if not required, if identity remains doubtful, if the request rests on a misrepresentation, or for web "
        "navigation data. Good-faith disclosure carries no civil liability; tenants cannot sue under 1681n/1681o for "
        "violations, which are enforced publicly.",
        fg, q(fg, "not later than 30 days after the date of receipt of a request from a victim in accordance with paragraph (3)",
              "evidencing any transaction alleged to be a result of identity theft to—"),
        "major", "8.1", determinacy="MIXED", judgment_terms=["high degree of confidence", "good faith"], instrument=FCRA,
        dependencies=["US:15USC1681c-2-furnisher-identity-theft"],
        construction=[(fg, q(fg, "Except as provided in section 1681s of this title, sections 1681n and 1681o of this title do not apply to any violation of this subsection."))],
        reasoning="1681g(e)(1)-(5) set the duty, verification and grounds to decline; (e)(6)-(7) limit liability.")

save([
    D("US:15 USC 1681t", "new_rule", "Preemption of state and city furnisher rules decides whether the NYC SHIELD "
      "pre-reporting notice and the GBL 604-bb credit-agency notice bind at all; the existing rules apply them without "
      "addressing 1681t(b)(1)(F).", proposed=[r_pre]),
    D("US:15 USC 1681c–2", "new_rule", "An identity-theft block notice triggers furnisher duties not to refurnish and bars "
      "placing the balance for collection.", proposed=[r_idt]),
    D("US:15 USC 1681m", "new_rule", "(f)-(g) bar placing an identity-theft balance for collection and set collector "
      "duties; (a) adverse action notice when a payment plan is refused on a report. (b)-(e), (h) concern credit "
      "applications, prescreening and risk-based pricing outside the chain.", proposed=[r_mfg, r_adv]),
    D("US:15 USC 1681n", "new_rule", "Willful FCRA liability of furnishers and users, with statutory and punitive damages.", proposed=[r_n]),
    D("US:15 USC 1681o", "new_rule", "Negligent FCRA liability of furnishers and users.", proposed=[r_o]),
    D("US:15 USC 1681p", "new_rule", "Two-year/five-year limit on FCRA suits.", proposed=[r_p]),
    D("US:15 USC 1681q", "new_rule", "Criminal liability for obtaining a tenant's report under false pretenses.", proposed=[r_q]),
    D("US:15 USC 1681h", "new_rule", "1681h(e) limits a tenant's state tort claims against a furnisher or user to false "
      "information furnished with malice; (a)-(d) bind agencies only.", proposed=[r_h]),
    D("US:15 USC 1681s", "new_rule", "Public enforcement and penalty amounts, including State damages actions for 1681s-2(a) "
      "violations that tenants cannot sue on.", proposed=[r_s]),
    D("US:15 USC 1681i", "partial", "US:15USC1681s-2(b)(1) states the furnisher's investigation duty 'within the agency's "
      "reinvestigation period' without the period; 1681i fixes 30 days, the 15-day extension, 45 days after a free "
      "report, and deletion/reinsertion.", ["US:15USC1681s-2(b)(1)"], [r_i]),
    D("US:15 USC 1681c–1", "new_rule", "Security freezes do not block collection pulls; fraud and active-duty alerts limit "
      "extending a payment plan without identity verification.", proposed=[r_c1]),
    D("US:15 USC 1681d", "new_rule", "Disclosure duties of anyone procuring an investigative consumer report on a former "
      "tenant.", proposed=[r_d]),
    D("US:15 USC 1681a", "new_rule", "Definitions decide whether the landlord's own-experience report is a consumer report "
      "and whether Handoff becomes a consumer reporting agency by configuration; the other definitions are carried by "
      "stated rules.", proposed=[r_own]),
    D("US:12 CFR 1022.82", "new_rule", "A user receiving an address-discrepancy notice on a former tenant's report needs "
      "reasonable identity-matching procedures.", proposed=[r_82]),
    D("US:12 CFR 1022.3", "new_rule", "The identity theft report definition and the furnisher's 15-day windows govern how "
      "a furnisher handles an identity-theft claim; the other definitions do not change a stated rule.", proposed=[r_3i]),
    D("US:15 USC 1681w", "new_rule", "Disposal of consumer-report information in the closed tenancy file.", proposed=[r_w]),
    D("US:15 USC 1681g", "new_rule", "1681g(e) obliges a business that dealt with an identity thief to give the victim "
      "application and transaction records within 30 days; the rest of 1681g binds agencies.", proposed=[r_g]),
    D("US:12 CFR Appendix_E_to_Part_1022", "stated", "The furnisher accuracy and integrity guidelines are the appendix E "
      "that US:12CFR1022.42(a) requires furnishers to consider.", ["US:12CFR1022.42(a)"]),
    D("US:12 CFR 1022.40", "stated", "Scope of subpart E (any furnisher) is the reach US:12CFR1022.42(a) and "
      "US:12CFR1022.43(a) already state.", ["US:12CFR1022.42(a)", "US:12CFR1022.43(a)"]),
    D("US:12 CFR 1022.41", "no_decision", "Definitions of accuracy, integrity, direct dispute and furnisher used by the "
      "stated furnisher rules; a landlord or collector reporting a balance is a furnisher and a dispute sent to it is a "
      "direct dispute, so they do not change those rules' reach."),
    D("US:12 CFR Appendix_B_to_Part_1022", "no_decision", "Model notices for financial institutions that extend credit "
      "under 1681s-2(a)(7); a landlord or collector reporting a lease balance is not one."),
    D("US:12 CFR 1022.1", "no_decision", "Purpose and scope of Regulation V; the operative scope sections decide reach."),
    D("US:12 CFR 1022.54", "no_decision", "Prescreened firm offers of credit or insurance; not used in the chain."),
    D("US:12 CFR Appendix_H_to_Part_1022", "no_decision", "Risk-based pricing model forms for creditors; no tenancy decision."),
    D("US:12 CFR Appendix_K_to_Part_1022", "no_decision", "Form of the summary of consumer rights that agencies and "
      "employers supply; no landlord duty in the chain."),
    D("US:12 CFR Appendix_M_to_Part_1022", "no_decision", "Notice agencies give furnishers; the furnisher's own duties are "
      "stated in the 1681s-2 rules."),
    D("US:12 CFR Appendix_N_to_Part_1022", "no_decision", "Notice agencies give users; the user duties are stated in the "
      "1681b and 1681m rules."),
    D("US:12 CFR Appendix_O_to_Part_1022", "no_decision", "Maximum charge an agency may impose for consumer disclosures."),
    D("US:12 CFR Appendix_C_to_Part_1022", "no_decision", "Affiliate-marketing opt-out model forms; no marketing in the chain."),
    D("US:12 CFR Appendix_I_to_Part_1022", "no_decision", "Identity theft rights summary that agencies provide."),
    D("US:12 CFR Appendix_L_to_Part_1022", "no_decision", "Form for requesting annual file disclosures from agencies."),
    D("US:15 USC 1681c–3", "no_decision", "Agency duty not to report adverse items caused by trafficking; the furnisher's "
      "duties are unchanged."),
    D("US:15 USC 1681e", "no_decision", "Agency compliance procedures and resale rules; Handoff as a reseller or agency is "
      "covered by US:15USC1681a(d)-(f)-own-experience-CRA."),
    D("US:15 USC 1681f", "no_decision", "Agency disclosures to government agencies."),
    D("US:15 USC 1681j", "no_decision", "Charges agencies may impose on consumers; the 45-day period in (a)(3) is carried in "
      "US:15USC1681i-furnisher-deadline."),
    D("US:15 USC 1681l", "no_decision", "Agency restriction on reusing investigative report information."),
    D("US:15 USC 1681r", "no_decision", "Crime by agency officers or employees."),
    D("US:15 USC 1681s–1", "no_decision", "Agency reporting of overdue child support."),
    D("US:15 USC 1681", "no_decision", "Findings and purpose; decides nothing."),
    D("US:15 USC 1681k", "no_decision", "Agency duties for public-record information in employment reports."),
    D("US:15 USC 1681s–3", "no_decision", "Affiliate marketing solicitations; no marketing in the chain."),
    D("US:15 USC 1681v", "no_decision", "Agency disclosures for counterterrorism."),
    D("US:15 USC 1681x", "no_decision", "Rulemaking against agency circumvention."),
    D("US:15 USC 1681u", "no_decision", "Agency disclosures to the FBI."),
])
