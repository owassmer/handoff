"""q6 chunk 3: remaining Reg E / EFTA sections."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q6_lib import D, P, q, save, tf

SUP = tf("US:12 CFR Supplement_I_to_Part_1005")
fj = tf("US:15 USC 1693j")
fn = tf("US:15 USC 1693n")
EFTA = "Electronic Fund Transfer Act, 15 U.S.C. 1693-1693r"
REG_E = "Regulation E, 12 CFR part 1005 (CFPB)"

r_j = P("US:15USC1693j-malfunction-suspends", "15 U.S.C. 1693j", "landlord; managing agent; Handoff", "must not charge",
        "The landlord (or its manager or Handoff as payee) agreed to accept rent or a balance payment by electronic fund "
        "transfer, the tenant initiated the transfer from a consumer account, and a system malfunction prevented the "
        "transfer from being completed.",
        "The tenant's obligation for that payment is suspended until the malfunction is corrected and the transfer can be "
        "completed, so the payment is not late for that period and no late fee or default follows from it, unless the "
        "payee afterwards demanded payment by another means in a written request, from which point the tenant owes payment "
        "by that other means.",
        fj, q(fj, "the consumer’s obligation to the other person shall be suspended until the malfunction is corrected and the electronic fund transfer may be completed"),
        "major", "5.3", determinacy="MIXED", judgment_terms=["system malfunction"], instrument=EFTA,
        dependencies=["US:12CFR1005.2-reach", "NY:RPL-238-a(2)"])

r_n = P("US:15USC1693n(a)-criminal", "15 U.S.C. 1693n(a)", "landlord; managing agent; Handoff", "liable",
        "A payee knowingly and willfully fails to comply with an EFTA duty that binds it (US:12CFR1005.3(a)-payee-duties), "
        "for example debiting a tenant's account on recurring autopay without a written authorization, or gives false "
        "information it must disclose.",
        "It commits a federal crime punishable by a fine of up to $5,000, imprisonment of up to one year, or both, in "
        "addition to civil liability under US:15USC1693m-civil-liability.",
        fn, q(fn, "Whoever knowingly and willfully—", "shall be fined not more than $5,000 or imprisoned not more than one year, or both."),
        "major", "7", determinacy="MIXED", judgment_terms=["knowingly and willfully"], instrument=EFTA,
        dependencies=["US:12CFR1005.3(a)-payee-duties", "US:15USC1693m-civil-liability"])

r_portal = P("US:12CFR1005-cmt-2(k)-1-one-time-payments", "12 CFR part 1005, Supplement I, comments 2(k)-1, 20(b)(4)-2.iv",
             "landlord; managing agent; Handoff", "scope",
             "The tenant or former tenant pays through the landlord's or Handoff's portal by instructing each payment itself "
             "(no standing authorization), or the landlord pays a deposit refund by a prepaid card issued for that "
             "disbursement and not advertised to the public.",
             "A payment the tenant initiates each time is not a preauthorized transfer: the 1005.10(b) written-authorization "
             "and 1005.10(d) varying-amount rules do not apply to it. A refund paid on such a prepaid card is not a gift card "
             "or general-use prepaid card under 1005.20, so the gift-card fee and expiration rules do not bind the payer; the "
             "card's own account disclosures are the issuing bank's (1005.18).",
             SUP, q(SUP, "In contrast, if the consumer must take action each month to initiate a payment (such as by entering instructions on a touch-tone telephone or home computer), the payments are not preauthorized EFTs."),
             "minor", "6.5", instrument=REG_E, dependencies=["US:12CFR1005.2-reach", "US:12CFR1005.10(d)-varying-debit-notice"],
             construction=[(SUP, q(SUP, "iv. An insurance company settles a policyholder's claim and distributes the insurance proceeds to the consumer by means of a prepaid card.",
                                   "the exclusion in § 1005.20(b)(4) applies."))],
             reasoning="Comment 2(k)-1 limits 'preauthorized' to transfers needing no further action by the consumer; comment "
                       "20(b)(4)-2.iv excludes a prepaid card that is only the means of paying proceeds and is not marketed to "
                       "the public.")

FI = "binds the account-holding financial institution (or card issuer), not a landlord, manager, collector or Handoff; 1005.3(a) does not extend it to other persons"
save([
    D("US:12 CFR 1005.11", "no_decision", f"Error resolution {FI}. A tenant disputing a landlord debit uses its bank; the payee's own duties are in the proposed 1005.3/1005.10 rules."),
    D("US:12 CFR 1005.6", "no_decision", f"Consumer liability for unauthorized transfers {FI}."),
    D("US:12 CFR 1005.8", "no_decision", f"Change-in-terms and error-resolution notices {FI}."),
    D("US:12 CFR 1005.1", "no_decision", "Authority and purpose statement; decides nothing."),
    D("US:12 CFR 1005.17", "no_decision", f"Overdraft-service opt-in {FI}."),
    D("US:12 CFR 1005.4", "no_decision", f"General disclosure form rules {FI}."),
    D("US:12 CFR 1005.5", "no_decision", f"Issuance of access devices {FI}."),
    D("US:12 CFR 1005.7", "no_decision", f"Initial account disclosures {FI}."),
    D("US:12 CFR 1005.9", "no_decision", f"Terminal receipts and periodic statements {FI}."),
    D("US:12 CFR 1005.18", "no_decision", f"Prepaid-account disclosures, access and error rules {FI}; a refund paid on a prepaid card leaves the disclosures to the issuer (US:12CFR1005-cmt-2(k)-1-one-time-payments)."),
    D("US:12 CFR 1005.19", "no_decision", "Internet posting of prepaid account agreements binds issuers only."),
    D("US:12 CFR 1005.20", "no_decision", "Gift-card fee and expiration rules reach cards sold to consumers for payment and marketed to the public; a refund card issued only to disburse a deposit is excluded by 1005.20(b)(4) (comment 20(b)(4)-2.iv, carried in US:12CFR1005-cmt-2(k)-1-one-time-payments)."),
    D("US:12 CFR Appendix_A_to_Part_1005", "no_decision", "Model clauses; the only payee-relevant one (A-6 check conversion and returned-item fee notices) is a safe harbor already carried in proposed US:12CFR1005.3(b)(2)-check-conversion."),
    D("US:12 CFR Supplement_I_to_Part_1005", "new_rule", "Official interpretations: the payee-relevant comments (3(b)(1)-1.v, 3(b)(2), 3(b)(3), 3(c)(1)-1, 10(b), 10(d), 10(e)) are carried as construction in the rules proposed at 1005.3, 1005.10, 1693e and 1693k; comments 2(k)-1 and 20(b)(4)-2.iv add the portal-payment and refund-card branches proposed here; the rest bind banks, issuers and remittance providers.",
      proposed=[r_portal]),
    D("US:15 USC 1693d", "no_decision", f"Terminal receipts and periodic statements {FI}."),
    D("US:15 USC 1693f", "no_decision", f"Error resolution {FI}."),
    D("US:15 USC 1693g", "no_decision", "Limits the consumer's liability to its bank for unauthorized transfers; no landlord duty."),
    D("US:15 USC 1693h", "no_decision", "Liability of financial institutions and ATM operators; not a landlord or manager."),
    D("US:15 USC 1693i", "no_decision", "Issuance of cards and access devices by financial institutions."),
    D("US:15 USC 1693j", "new_rule", "A system malfunction in an EFT the landlord agreed to accept suspends the tenant's obligation, so no late fee or default for that period.", proposed=[r_j]),
    D("US:15 USC 1693n", "new_rule", "Knowing and willful EFTA violations by any person, including a payee, are crimes; a consequence in the chain.", proposed=[r_n]),
    D("US:15 USC 1693q", "no_decision", "Preserves consistent and more protective state EFT law; New York has no inconsistent EFT rule on a landlord's payee duties, so it changes nothing."),
    D("US:15 USC 1693b", "no_decision", "Rulemaking authority and ATM-operator fee notices; no landlord duty."),
    D("US:15 USC 1693c", "no_decision", f"Account terms disclosures {FI}."),
    D("US:15 USC 1693o", "no_decision", "Allocates administrative enforcement among agencies; the tenant's remedies against a payee are in 1693m."),
    D("US:15 USC 1693o–1", "no_decision", "Remittance transfers to foreign recipients by remittance providers; a refund to a US account or a rent payment is not a remittance and a landlord is not a remittance transfer provider."),
    D("US:15 USC 1693o–2", "no_decision", "Interchange fees and network rules bind card issuers and networks; the merchant freedoms it protects (discounts, minimums) impose nothing on a landlord."),
])
