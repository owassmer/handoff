"""q6 chunk 2: Reg E / EFTA sections that bind a payee (items 6, 7, 35, 36, 77, 113, 114, 147, 149, 168)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q6_lib import D, P, q, save, tf

SUP = tf("US:12 CFR Supplement_I_to_Part_1005")
f3 = tf("US:12 CFR 1005.3")
f10 = tf("US:12 CFR 1005.10")
f2 = tf("US:12 CFR 1005.2")
fe = tf("US:15 USC 1693e")
fk = tf("US:15 USC 1693k")
fl = tf("US:15 USC 1693l")
fm = tf("US:15 USC 1693m")
f13 = tf("US:12 CFR 1005.13")
fa = tf("US:15 USC 1693a")
REG_E = "Regulation E, 12 CFR part 1005 (CFPB)"
EFTA = "Electronic Fund Transfer Act, 15 U.S.C. 1693-1693r"

r_cov = P("US:12CFR1005.3(a)-payee-duties", "12 CFR 1005.3(a), (b)(1), (c)(1)", "landlord; managing agent; Handoff",
          "scope",
          "The landlord, managing agent or Handoff takes a payment from a tenant or former tenant, or pays a refund, by an "
          "electronic transfer that debits or credits the tenant's consumer account (ACH debit or credit, debit card, "
          "payment app pull or push), and is not itself the tenant's bank.",
          "Regulation E binds it only through 1005.3(b)(2) (converting a check to an EFT), 1005.3(b)(3) (returned-item "
          "fees by EFT), 1005.10(b) (written authorization of recurring debits), 1005.10(d) (notice of varying debits), "
          "1005.10(e) (no compulsory EFT repayment of credit), 1005.13 (two-year records) and 1005.20 (gift cards); every "
          "other Regulation E duty (disclosures, periodic statements, error resolution, unauthorized-transfer liability, "
          "stop-payment handling) is the account-holding bank's. A refund paid by ACH credit or other push transfer to the "
          "tenant's account therefore puts no Regulation E duty on the payer. A payment originated by paper check, and an "
          "electronic re-presentment of a returned check, is not an EFT; an EFT debiting a fee because a check was returned "
          "is. Where the tenant is a company, or the account is not held primarily for personal, family or household "
          "purposes, Regulation E does not apply (US:12CFR1005.2-reach).",
          f3, q(f3, "For purposes of §§ 1005.3(b)(2) and (3), 1005.10(b), (d), and (e), 1005.13, and 1005.20, this part applies to any person"),
          "major", "6.5", instrument=REG_E, dependencies=["US:12CFR1005.2-reach"],
          construction=[(f3, q(f3, "(1) Checks. Any transfer of funds originated by check, draft, or similar paper instrument;")),
                        (SUP, q(SUP, "1. Re-presented checks. The electronic re-presentment of a returned check is not covered by Regulation E",
                                "The person debiting the fee electronically must obtain the consumer's authorization."))],
          reasoning="1005.3(a) lists the only provisions that bind a person other than a financial institution; 1005.2(i) makes a "
                    "financial institution only one that holds the consumer's account or issues an access device under an EFT "
                    "agreement, which a landlord or manager does not; 1005.3(c)(1) and comment 3(c)(1)-1 exclude check-originated "
                    "transfers but not an electronic returned-check fee.")

r_ck = P("US:12CFR1005.3(b)(2)-check-conversion", "12 CFR 1005.3(b)(2); comments 3(b)(2)-2 to -4", "landlord; managing agent; Handoff",
         "must",
         "A tenant or former tenant pays rent or a move-out balance by paper check (mailed, dropped at a lockbox or office, "
         "or handed over) from a consumer account, and the payee or its bank uses the check's routing and account numbers "
         "to initiate a one-time ACH debit instead of collecting the check (accounts-receivable or back-office conversion).",
         "The payee must give notice that the check will or may be processed as an EFT and obtain the tenant's authorization "
         "for each transfer; the tenant authorizes by receiving the notice and then sending the check. For mailed payments "
         "the notice is given for each payment, for example on the invoice or statement demanding the balance (it covers "
         "every check sent for that invoice, by the tenant or another payer); a coupon book with set dates and amounts may "
         "carry one notice. Without notice, the check is processed as a check. The appendix A-6 model clauses satisfy the "
         "notice.",
         f3, q(f3, "(ii) The person initiating an electronic fund transfer using the consumer's check as a source of information for the transfer must provide a notice",
               "and obtain a consumer's authorization for each transfer."),
         "major", "8.1b", instrument=REG_E, dependencies=["US:12CFR1005.3(a)-payee-duties"],
         construction=[(SUP, q(SUP, "3. Notice for each transfer. Generally, a notice to authorize an electronic check conversion transaction must be provided for each transaction.")),
                       (SUP, q(SUP, "notice to a consumer listed on the billing account that a check provided as payment during a single billing cycle or after receiving an invoice or statement will be processed as a one-time EFT or as a check transaction constitutes notice for all checks provided in payment"))],
         reasoning="1005.3(b)(2)(ii) binds the person initiating the conversion; comments 3(b)(2)-3 and -4 set notice per "
                   "payment and per invoice.")

r_fee = P("US:12CFR1005.3(b)(3)-returned-fee-eft", "12 CFR 1005.3(b)(3); comments 3(b)(3)-2, 3(c)(1)-1", "landlord; managing agent; Handoff",
          "must",
          "The lease allows a returned-payment charge within NY:RPL-238-a(2-a), a tenant's rent or balance payment (check or "
          "EFT) is returned unpaid, and the payee wants to collect the charge by debiting the tenant's consumer account "
          "electronically.",
          "It may debit the fee electronically only with the tenant's authorization for that transfer: before the tenant "
          "made the underlying payment it received notice (for example on the invoice, statement or payment page) that the "
          "fee will be collected by EFT from the account if the payment is returned unpaid, stating the dollar amount of the "
          "fee (or, if the fee varies with the payment or other factors, how it is determined). Without that notice it "
          "collects the fee only by other means, such as the move-out statement or a separate demand. Fees the tenant's own "
          "bank charges are outside this rule.",
          f3, q(f3, "The person initiating an electronic fund transfer to collect a fee for the return of an electronic fund transfer or a check that is unpaid",
                "must obtain the consumer's authorization for each transfer."),
          "major", "5.3", instrument=REG_E, dependencies=["US:12CFR1005.3(a)-payee-duties", "NY:RPL-238-a(2-a)"],
          construction=[(f3, q(f3, "The notice must state that the fee will be collected by means of an electronic fund transfer from the consumer's account if the payment is returned unpaid and must disclose the dollar amount of the fee.")),
                        (SUP, q(SUP, "A consumer authorizes a person to electronically collect a returned item fee when the consumer receives notice, typically on an invoice or statement"))],
          reasoning="1005.3(b)(3)(i) makes notice before the underlying payment the authorization; comment 3(b)(3)-1 limits it "
                    "to the person initiating the fee debit.")

r_vary = P("US:12CFR1005.10(d)-varying-debit-notice", "12 CFR 1005.10(d); 15 U.S.C. 1693e(b); comments 10(d)(2)-1", "landlord; managing agent; Handoff (designated payee)",
           "must",
           "The tenant pays rent (or a payment-plan installment) by recurring debits that the landlord, manager or Handoff "
           "initiates under the tenant's standing authorization (payee-initiated ACH or card-on-file debit), and a debit "
           "will differ in amount from the previous debit under that authorization or from the authorized amount (for "
           "example a prorated last month, or last rent plus move-out charges). Transfers the tenant initiates from its own "
           "bank's bill-pay are the bank's, not the payee's.",
           "The payee (or the tenant's bank) must send the tenant written notice of the amount and date of the transfer at "
           "least 10 days before its scheduled date, so a varying debit is scheduled no earlier than the 10th day after the "
           "notice is sent. The payee must tell the tenant of the right to notice of every varying transfer, and may instead "
           "offer notice only when a debit falls outside a specified range, or differs from the last debit by more than an "
           "agreed amount, that the tenant could reasonably anticipate. A debit outside the authorization's terms is not "
           "authorized by it and needs the tenant's separate authorization.",
           f10, q(f10, "(d) Notice of transfers varying in amount—(1) Notice. When a preauthorized electronic fund transfer from the consumer's account will vary in amount",
                  "at least 10 days before the scheduled date of transfer."),
           "critical", "8.1b", instrument=REG_E,
           dependencies=["US:12CFR1005.3(a)-payee-duties", "US:15USC1693e(a)-autopay-authorization", "US:15USC1693m-civil-liability"],
           construction=[(f10, q(f10, "(2) Range. The designated payee or the institution shall inform the consumer of the right to receive notice of all varying transfers")),
                         (SUP, q(SUP, "must provide an acceptable range that could be anticipated by the consumer.")),
                         (fe, q(fe, "the financial institution or designated payee shall, prior to each transfer, provide reasonable advance notice to the consumer"))],
           reasoning="1005.10(d) applies to any person (1005.3(a)) and sets the 10-day advance written notice for the "
                     "designated payee; 1693e(b) is the statutory basis.")

r_auth = P("US:15USC1693e(a)-autopay-authorization", "15 U.S.C. 1693e(a); 12 CFR 1005.10(b); comments 10(b)-2, -3, -5, -6, -7", "landlord; managing agent; Handoff",
           "must",
           "The landlord, manager or Handoff debits a tenant's or former tenant's consumer account by transfers authorized in "
           "advance to recur at substantially regular intervals (rent autopay, or installments of a move-out balance "
           "payment plan).",
           "The recurring debits may be authorized only by a writing signed or similarly authenticated by the tenant (an "
           "E-SIGN-compliant electronic signature, including a security code, suffices; the payee may not sign for the tenant "
           "on an oral authorization), which is readily identifiable as an authorization with clear terms, and the payee "
           "must give the tenant a copy of the terms, on paper or electronically. The payee, not the tenant's bank, is in "
           "violation if it fails. If a tenant who called its card a credit card turns out to have given a debit card, the "
           "payee obtains a written authorization as soon as reasonably possible or stops debiting. The tenant may stop any "
           "preauthorized debit through its bank up to three business days before it is scheduled.",
           fe, q(fe, "A preauthorized electronic fund transfer from a consumer’s account may be authorized by the consumer only in writing, and a copy of such authorization shall be provided to the consumer when made."),
           "major", "8.1b", instrument=EFTA, dependencies=["US:12CFR1005.3(a)-payee-duties", "US:15USC1693m-civil-liability"],
           construction=[(f10, q(f10, "Preauthorized electronic fund transfers from a consumer's account may be authorized only by a writing signed or similarly authenticated by the consumer. The person that obtains the authorization shall provide a copy to the consumer.")),
                         (SUP, q(SUP, "rather, it is the third-party payee that is in violation of the regulation.")),
                         (SUP, q(SUP, "cannot be met by a payee's signing a written authorization on the consumer's behalf with only an oral authorization from the consumer.")),
                         (SUP, q(SUP, "The writing and signature requirements of this section are satisfied by complying with the Electronic Signatures in Global and National Commerce Act")),
                         (SUP, q(SUP, "must obtain a written and signed or (where appropriate) a similarly authenticated authorization as soon as reasonably possible, or cease debiting the consumer's account."))],
           reasoning="1693e(a) and 1005.10(b) set the writing-and-copy requirement; comments 10(b)-2 to -7 place the duty on "
                     "the payee and define 'similarly authenticated' by E-SIGN.")

r_comp = P("US:15USC1693k(1)-payment-plan-autopay", "15 U.S.C. 1693k(1); 12 CFR 1005.10(e)(1); comments 10(e)(1)-1, -4", "landlord; managing agent; Handoff; collector",
           "must not",
           "The landlord, manager, Handoff or a collector offers a former tenant (a natural person) a payment plan for a "
           "move-out balance, which gives a right to defer payment of a debt (US:15USC1602(f)).",
           "It may not condition the plan on the tenant's repaying by preauthorized recurring electronic debits. It may offer "
           "autopay as an option, and may give a cost incentive for autopay only if a plan without autopay is also offered. "
           "A plan conditioned on autopay violates 1693k and carries 1693m liability.",
           fk, q(fk, "condition the extension of credit to a consumer on such consumer’s repayment by means of preauthorized electronic fund transfers;"),
           "major", "8.1b", instrument=EFTA,
           dependencies=["US:15USC1602(f)", "US:15USC1693m-civil-liability", "US:12CFR1005.3(a)-payee-duties"],
           construction=[(f10, q(f10, "No financial institution or other person may condition an extension of credit to a consumer on the consumer's repayment by preauthorized electronic fund transfers")),
                         (SUP, q(SUP, "provided the program with the automatic payment feature is not the only loan program offered by the creditor for the type of credit involved.")),
                         (f2, q(f2, "(f) “Credit” means the right granted by a financial institution to a consumer to defer payment of debt"))],
           reasoning="1693k(1) binds any person and does not define credit; 1005.10(e)(1) extends the bar to 'other person[s]', "
                     "which the 1005.2(f) definition (credit granted by a financial institution) would make surplus if read "
                     "to exclude non-bank creditors. The statute controls over the regulation's definition, and 1005.3(a) "
                     "applies 1005.10(e) to any person. A payment plan defers payment of a debt, which is credit under "
                     "US:15USC1602(f), the definition of the same Consumer Credit Protection Act.")

r_liab = P("US:15USC1693m-civil-liability", "15 U.S.C. 1693m(a)-(g)", "landlord; managing agent; Handoff", "liable",
           "The landlord, manager or Handoff fails to comply with an EFTA or Regulation E duty that binds it "
           "(US:12CFR1005.3(a)-payee-duties) toward a tenant.",
           "It is liable to the tenant for actual damages, plus statutory damages of $100 to $1,000 in an individual action "
           "(in a class action, no per-member minimum and a total cap of the lesser of $500,000 or 1% of net worth), plus "
           "costs and a reasonable attorney's fee. No liability if it proves by a preponderance that the violation was "
           "unintentional and a bona fide error despite procedures reasonably adapted to avoid it; or if, before suit, it "
           "notifies the tenant of the failure, complies, adjusts the account and pays actual damages; or for acts in good "
           "faith conformity with a CFPB or Board rule or interpretation. Suit must be brought within one year of the "
           "violation; a bad-faith or harassing unsuccessful suit earns the defendant its fees.",
           fm, q(fm, "any person who fails to comply with any provision of this subchapter with respect to any consumer",
                 "an amount not less than $100 nor greater than $1,000; or"),
           "critical", "7", instrument=EFTA, dependencies=["US:12CFR1005.3(a)-payee-duties"],
           construction=[(fm, q(fm, "the person notifies the consumer concerned of the failure, complies with the requirements of this subchapter, and makes an appropriate adjustment to the consumer’s account and pays actual damages")),
                         (fm, q(fm, "within one year from the date of the occurrence of the violation."))],
           reasoning="1693m(a) reaches 'any person', so a payee that breaches 1693e or 1693k is liable; (c), (d), (e), (g) state "
                     "the defenses, cure and limitation.")

r_wv = P("US:15USC1693l-no-waiver", "15 U.S.C. 1693l", "landlord; managing agent; Handoff", "void",
         "A lease, autopay form, payment-plan agreement or settlement with a tenant contains a term waiving an EFTA or "
         "Regulation E right (for example, the 10-day notice of a varying debit, or the right to stop a preauthorized debit).",
         "The waiver is void. An agreement may give the tenant greater protection, and a waiver given in settlement of a "
         "dispute or action is valid.",
         fl, q(fl, "No writing or other agreement between a consumer and any other person may contain any provision which constitutes a waiver of any right conferred or cause of action created by this subchapter."),
         "minor", "8.1b", instrument=EFTA, dependencies=["US:12CFR1005.10(d)-varying-debit-notice"])

r_rec = P("US:12CFR1005.13(b)-records", "12 CFR 1005.13(b)", "landlord; managing agent; Handoff", "must",
          "The payee took an authorization, gave a check-conversion, returned-fee or varying-amount notice, or offered a "
          "payment plan subject to 1005.3(b)(2)-(3) or 1005.10(b), (d), (e).",
          "It keeps evidence of compliance (the signed authorization and copy sent, the notices and their dates) for at "
          "least two years from when the disclosure or action was required; once it has actual notice of an investigation "
          "or has been served in an EFTA action, it keeps the related records until final disposition.",
          f13, q(f13, "(1) Any person subject to the Act and this part shall retain evidence of compliance with the requirements imposed by the Act and this part for a period of not less than two years"),
          "minor", "8.1b", instrument=REG_E, dependencies=["US:12CFR1005.3(a)-payee-duties"])

r_reach = P("US:12CFR1005.2-reach", "12 CFR 1005.2(b)(1), (e), (k), (m)", "landlord; managing agent; Handoff", "scope",
            "Deciding whether a payee rule of Regulation E (US:12CFR1005.3(a)-payee-duties) applies to a transfer to or from a "
            "tenant.",
            "It applies only where the tenant is a natural person and the account debited or credited is a checking, savings "
            "or other asset account (including a prepaid account) held primarily for personal, family or household purposes; "
            "a company tenant or a business account is outside. A 'preauthorized' transfer is one authorized in advance to "
            "recur at substantially regular intervals, so a single one-time debit of a move-out balance is not governed by "
            "1005.10(b) or (d). A debit initiated without the tenant's actual authority is an 'unauthorized' EFT, which the "
            "tenant's bank must treat under 1005.6 and 1005.11 (the tenant's liability limits and error resolution).",
            f2, q(f2, "(k) “Preauthorized electronic fund transfer” means an electronic fund transfer authorized in advance to recur at substantially regular intervals."),
            "minor", "8.1b", instrument=REG_E,
            construction=[(f2, q(f2, "(b)(1) “Account” means a demand deposit (checking), savings, or other consumer asset account",
                                 "established primarily for personal, family, or household purposes.")),
                          (f2, q(f2, "(e) “Consumer” means a natural person."))],
            reasoning="The definitions fix the reach of each payee duty: consumer, account and preauthorized transfer.")

save([
    D("US:12 CFR 1005.10", "new_rule", "1005.10(d) (10-day notice of a varying preauthorized debit) binds any designated "
      "payee, including a landlord taking a prorated or move-out debit under rent autopay; no rule states it. 1005.10(b) "
      "and (e) are proposed under 15 USC 1693e and 1693k; (a) and (c) bind the bank.", proposed=[r_vary]),
    D("US:12 CFR 1005.3", "new_rule", "Coverage fixes which Reg E duties bind a landlord or manager that takes or pays money "
      "electronically, and 1005.3(b)(2)-(3) bind it directly for check conversion and electronic returned-payment fees.",
      proposed=[r_cov, r_ck, r_fee]),
    D("US:15 USC 1693e", "new_rule", "Recurring debits (rent autopay, payment-plan installments) need the tenant's signed or "
      "authenticated writing and a copy; the payee is the one in violation.", proposed=[r_auth]),
    D("US:15 USC 1693m", "new_rule", "Civil liability of any person, including a landlord payee, for EFTA violations, with "
      "the bona fide error, cure and one-year limits.", proposed=[r_liab]),
    D("US:12 CFR 1005.13", "new_rule", "1005.13 is one of the provisions 1005.3(a) applies to any person: the payee keeps "
      "evidence of compliance two years.", proposed=[r_rec]),
    D("US:15 USC 1693k", "new_rule", "No person may condition a payment plan (credit) on autopay repayment; changes how a "
      "move-out balance plan may be offered.", proposed=[r_comp]),
    D("US:15 USC 1693l", "new_rule", "Voids lease or autopay-form waivers of EFTA rights; changes what a payment agreement "
      "may contain.", proposed=[r_wv]),
    D("US:12 CFR 1005.12", "no_decision", "Relation to TILA covers card and overdraft features of bank accounts, and state "
      "preemption determinations and state exemptions; none alters a landlord's or manager's payee duties in NYC."),
    D("US:12 CFR 1005.2", "new_rule", "The definitions of consumer, account and preauthorized transfer decide whether each "
      "payee duty reaches a given tenant, account and debit.", proposed=[r_reach]),
    D("US:15 USC 1693a", "no_decision", "EFTA definitions are restated with the same reach in 12 CFR 1005.2-1005.3, whose "
      "reach rules are proposed there (US:12CFR1005.2-reach, US:12CFR1005.3(a)-payee-duties); the statutory text adds no "
      "term that changes a payee's duties."),
])
