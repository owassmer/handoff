"""q6 chunk 7: SCRA (50 USC ch. 50) remainder."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q6_lib import D, P, q, save, tf

SCRA = "Servicemembers Civil Relief Act, 50 U.S.C. 3901-4043"
f = {k: tf(f"US:50 USC {k}") for k in ["3914", "3919", "3932", "3935", "3952", "3956", "3959", "4011", "4012", "4021",
                                        "4022", "3920", "4026", "4041", "4043"]}


def R(id, prov, actor, mod, cond, eff, sec, quote, sev, step, **kw):
    return P(id, prov, actor, mod, cond, eff, f[sec], quote, sev, step, instrument=SCRA, **kw)


r3914 = R("US:50USC3914-allied-forces", "50 U.S.C. 3914", "landlord", "scope",
          "A tenant is a U.S. citizen serving with the forces of a nation allied with the United States in a war or military "
          "action, in service similar to U.S. military service.",
          "The tenant has the same SCRA relief and protections as a servicemember (for example lease termination under "
          "US:50USC3955(a)(1), the 6% cap, stays), ending on discharge or release from that service.",
          "3914", q(f["3914"], "is entitled to the relief and protections provided under this chapter if that service with the allied force is similar to military service as defined in this chapter."),
          "minor", "3.4", determinacy="MIXED", judgment_terms=["similar to military service"],
          dependencies=["US:50USC3911(1)-(2)", "US:50USC3955(a)(1)"])

r3919 = R("US:50USC3919-no-adverse-report", "50 U.S.C. 3919", "landlord; managing agent; Handoff; collector", "must not",
          "A servicemember former tenant applied for or received an SCRA stay, postponement or suspension of an obligation "
          "(for example a stay of the landlord's suit, or relief under 3933 or 4021).",
          "That application or relief may not by itself be the basis for treating the tenant as unable to pay, for denying "
          "or changing the terms of a payment plan or refusing one on the terms requested, for an adverse report to a "
          "consumer reporting agency, or for annotating the tenant's record as a reservist or National Guard member. The "
          "underlying balance may still be reported accurately on its own facts.",
          "3919", q(f["3919"], "shall not itself (without regard to other considerations) provide the basis for any of the following:"),
          "major", "8.7", dependencies=["US:15USC1681s-2(a)(1)(A)", "US:50USC3933-penalties"])

r3932 = R("US:50USC3932-stay-with-notice", "50 U.S.C. 3932(a)-(e)", "court; landlord", "shall on application",
          "The landlord sues a former tenant for the balance (or the tenant sues the landlord for the deposit), and the "
          "tenant, at the time of applying, is in military service or within 90 days after release, and has notice of the "
          "action.",
          "At any stage before final judgment the court may stay the action on its own motion and must stay it for at least "
          "90 days on the servicemember's application containing a statement of how duty materially affects the ability to "
          "appear with a date of availability, and a commanding officer's letter that duty prevents appearance and leave is "
          "not authorized. Applying is not an appearance and waives no defense. Further stays may be sought on the same "
          "showing; if refused, the court appoints counsel. A servicemember denied a 3932 stay cannot then use the 3931 "
          "default protections.",
          "3932", q(f["3932"], "the court may on its own motion and shall, upon application by the servicemember, stay the action for a period of not less than 90 days"),
          "major", "8.9", determinacy="MIXED", judgment_terms=["materially affect the servicemember's ability to appear"],
          dependencies=["US:50USC3931(b)(1)", "US:50USC3911(1)-(2)"],
          construction=[(f["3932"], q(f["3932"], "A letter or other communication from the servicemember’s commanding officer stating that the servicemember’s current military duty prevents appearance"))],
          reasoning="3932(b)(1)-(2) make the 90-day stay mandatory on a complete application; (c)-(e) set its effects.")

r3935 = R("US:50USC3935-stay-term-codefendants", "50 U.S.C. 3935(a)-(c)", "court; landlord", "may",
          "A court stays the landlord's action, an attachment or an execution against a servicemember former tenant under "
          "the SCRA (other than a 3932 or 4021 stay), and co-tenants or guarantors not in service are also defendants.",
          "The stay may run for the period of military service plus 90 days, or any part of it, and the court may set "
          "reasonable installment payments. The landlord may proceed against the co-defendants who are not in service only "
          "with the court's approval (US:50USC3913-guarantor-cotenant may extend the stay to them).",
          "3935", q(f["3935"], "the plaintiff may proceed against those other defendants with the approval of the court."),
          "major", "8.9", determinacy="MIXED", judgment_terms=["reasonable installment payments"],
          dependencies=["US:50USC3913-guarantor-cotenant"],
          construction=[(f["3935"], q(f["3935"], "may be ordered for the period of military service and 90 days thereafter, or for any part of that period."))],
          reasoning="3935(a) sets the maximum stay and installment power; (b) conditions proceeding against co-defendants; (c) "
                    "excludes 3932 and 4021 stays.")

r3952 = R("US:50USC3952-lease-no-termination-without-order", "50 U.S.C. 3952(a)-(c)", "landlord", "must not",
          "The tenant signed the lease and paid a deposit or rent installment before entering military service, and the "
          "landlord wants to terminate the lease or retake the unit for a breach occurring before or during the service.",
          "The landlord may not terminate the lease or retake possession for that breach without a court order; knowingly "
          "resuming or attempting to resume possession otherwise is a misdemeanor (fine, up to one year's imprisonment). In "
          "the hearing the court may condition termination on repaying the tenant all or part of the deposit or "
          "installments paid, must stay the proceeding on the servicemember's application when service materially affects "
          "the ability to comply, and may make any other equitable disposition.",
          "3952", q(f["3952"], "may not be rescinded or terminated for a breach of terms of the contract occurring before or during that person’s military service, nor may the property be repossessed for such breach without a court order."),
          "major", "3.4", determinacy="MIXED", judgment_terms=["materially affected by military service", "equitable"],
          dependencies=["US:50USC3911(1)-(2)", "US:50USC3918"],
          construction=[(f["3952"], q(f["3952"], "may order repayment to the servicemember of all or part of the prior installments or deposits as a condition of terminating the contract and resuming possession of the property;")),
                        (f["3952"], q(f["3952"], "This section applies only to a contract for which a deposit or installment has been paid by the servicemember before the servicemember enters military service."))],
          reasoning="3952(a)(1)(B) reaches the lease of 'real or personal property'; (a)(2) limits it to contracts with a deposit "
                    "or installment paid before service; (b)-(c) set the crime and the court's powers, including return of "
                    "deposits.")

r3956 = R("US:50USC3956-landlord-service-contracts", "50 U.S.C. 3956(a), (b), (e), (f)", "landlord; managing agent", "must",
          "The landlord (or its manager) provides the tenant internet access, home security services, or a gym or fitness "
          "program under a contract or lease addendum separate from the tenancy, entered before the tenant received orders, "
          "and the servicemember tenant (or a covered spouse or dependent) receives orders to relocate for 90 days or more "
          "to a place the contract cannot serve, or a qualifying stop-movement order.",
          "The tenant may terminate that contract by written or electronic notice with a copy of the orders and the "
          "termination date; the provider gives written or electronic notice of these rights. No early termination charge "
          "may be imposed; amounts already due under the contract remain owed. Advance payments for periods after the "
          "termination date (beyond the current billing period) are refunded within 60 days. Provider-owned equipment is "
          "returned within 10 days of disconnection.",
          "3956", q(f["3956"], "For any contract terminated under this section, the service provider under the contract may not impose an early termination charge"),
          "major", "3.4", dependencies=["US:50USC3955(a)(1)", "US:50USC3911(4)"],
          construction=[(f["3956"], q(f["3956"], "Not later than 60 days after the effective date of the termination of a contract under this section, the service provider under the contract shall refund to the servicemember any fee or other amount to the extent paid for a period extending until after such date"))],
          reasoning="3956(b) lists covered service contracts; (e)-(f) bar early termination charges and require refunds.")

r3959 = R("US:50USC3959-dependents", "50 U.S.C. 3959", "court; landlord", "scope",
          "A dependent of a servicemember (spouse, child, or person supported more than half) is the tenant or co-tenant and "
          "applies to a court for relief because the servicemember's military service materially affects the dependent's "
          "ability to comply with the lease or other obligation.",
          "The dependent is entitled to the protections of SCRA subchapter III (50 U.S.C. 3951-3959: eviction and distress "
          "protections, installment-contract and lease protections, lien enforcement), as the court applies them.",
          "3959", q(f["3959"], "Upon application to a court, a dependent of a servicemember is entitled to the protections of this subchapter if the dependent’s ability to comply with a lease, contract, bailment, or other obligation is materially affected by reason of the servicemember’s military service."),
          "major", "3.4", determinacy="MIXED", judgment_terms=["materially affected by reason of the servicemember's military service"],
          dependencies=["US:50USC3911(4)", "US:50USC3958(a)"])

r4011 = R("US:50USC4011-abuse", "50 U.S.C. 4011", "court; landlord", "may",
          "In the landlord's action to recover a balance, the court finds that the former tenant transferred or acquired an "
          "interest, property or contract with intent to use the SCRA to delay just enforcement.",
          "The court enters whatever judgment or order it lawfully could concerning that transfer or acquisition, so the "
          "SCRA does not shelter it.",
          "4011", q(f["4011"], "the court shall enter such judgment or make such order as might lawfully be entered or made concerning such transfer or acquisition."),
          "minor", "8.12", determinacy="MIXED", judgment_terms=["intent to delay the just enforcement"])

r4012 = R("US:50USC4012-certificates", "50 U.S.C. 4012", "landlord", "may",
          "The landlord must establish a former tenant's military service status or dates (for the 3931 affidavit, a stay, "
          "the 3936 tolling period or the 3937 cap).",
          "A certificate signed by the Secretary concerned (including one appearing so signed) is prima facie evidence of "
          "whether and when the person served, residence on entry, rank and unit, pay and release or death; the Secretary "
          "issues one on application. A servicemember reported missing is presumed still in service until accounted for.",
          "4012", q(f["4012"], "In any proceeding under this chapter, a certificate signed by the Secretary concerned is prima facie evidence as to any of the following facts stated in the certificate:"),
          "minor", "8.9", dependencies=["US:50USC3931(b)(1)", "US:50USC3936-tolling"])

r4021 = R("US:50USC4021-anticipatory-relief", "50 U.S.C. 4021(a), (b)(2), (c)", "court; landlord", "may",
          "A servicemember former tenant, during service or within 180 days after release, applies to a court for relief "
          "from a lease obligation incurred before the service began, and service materially affects the ability to pay.",
          "After notice and hearing the court may stay enforcement during service and for a period equal to the service "
          "after release (or after application if made later), conditioned on paying the unpaid balance and accrued "
          "interest in equal periodic installments at the rate that would apply if paid when due. While the servicemember "
          "complies with the stay, no fine or penalty (late fees included) accrues.",
          "4021", q(f["4021"], "In the case of any other obligation, liability, tax, or assessment, the court may grant a stay of enforcement—"),
          "major", "8.10", determinacy="MIXED", judgment_terms=["materially affected by reason of military service"],
          dependencies=["US:50USC3933-penalties", "US:50USC3937-6pct"],
          construction=[(f["4021"], q(f["4021"], "When a court grants a stay under this section, a fine or penalty shall not accrue on the obligation, liability, tax, or assessment for the period of compliance with the terms and conditions of the stay."))],
          reasoning="4021(a) lets the servicemember seek relief before default; (b)(2) sets the stay and installment terms; (c) "
                    "stops penalties during compliance.")

r3920 = R("US:50USC3920-representatives", "50 U.S.C. 3920; 4022", "landlord; managing agent; Handoff", "must accept",
          "An attorney for the servicemember tenant, or a person holding the servicemember's power of attorney, gives the "
          "landlord an SCRA notice or request (for example lease termination with orders, a 6% cap request) or claims "
          "SCRA relief.",
          "The representative is treated as the servicemember, so the notice or request has the same effect as the "
          "servicemember's own. A power of attorney naming a spouse, parent or other relative, executed during service or "
          "after orders or notice of possible orders, is extended automatically while the servicemember is missing, unless "
          "its terms fix an expiry regardless of missing status.",
          "3920", q(f["3920"], "Whenever the term “servicemember” is used in this chapter, such term shall be treated as including a reference to a legal representative of the servicemember."),
          "major", "3.4", dependencies=["US:50USC3955(c)", "US:50USC3937-6pct"],
          construction=[(f["4022"], q(f["4022"], "A power of attorney of a servicemember shall be automatically extended for the period the servicemember is in a missing status"))],
          reasoning="3920(a)-(b) define the legal representative and equate it with the servicemember; 4022 keeps a qualifying "
                    "power of attorney alive during missing status.")

r4026 = R("US:50USC4026-business-obligations", "50 U.S.C. 4026", "landlord", "must not",
          "The tenant is a company or trade name of a servicemember, and the servicemember is personally liable for the "
          "lease balance (for example as guarantor), during the servicemember's military service.",
          "The servicemember's assets not held in connection with the business may not be used to satisfy that balance "
          "during military service, unless a court on the landlord's application modifies the relief as justice and "
          "equity require.",
          "4026", q(f["4026"], "the assets of the servicemember not held in connection with the trade or business may not be available for satisfaction of the obligation or liability during the servicemember’s military service."),
          "minor", "8.12", determinacy="MIXED", judgment_terms=["as justice and equity require"],
          dependencies=["US:50USC3911(1)-(2)"])

r4041 = R("US:50USC4041-ag-penalties", "50 U.S.C. 4041", "landlord; managing agent; Handoff; collector", "liable",
          "A person in the chain engages in a pattern or practice of SCRA violations (for example charging early "
          "termination fees on 3955 terminations, withholding prepaid rent, suing without the 3931 affidavit) or a "
          "violation raising an issue of significant public importance.",
          "The Attorney General may sue; the court may grant equitable and declaratory relief, monetary damages to "
          "aggrieved persons, and civil penalties of up to $55,000 for a first violation and $110,000 for any subsequent "
          "violation (as adjusted for inflation). Aggrieved persons may intervene for their own relief with costs and "
          "attorney's fees.",
          "4041", q(f["4041"], "in an amount not exceeding $55,000 for a first violation; and", "in an amount not exceeding $110,000 for any subsequent violation."),
          "critical", "7", determinacy="MIXED", judgment_terms=["pattern or practice", "significant public importance"],
          dependencies=["US:50USC4042"])

r4043 = R("US:50USC4043-other-remedies", "50 U.S.C. 4043", "landlord; managing agent; Handoff; collector", "liable",
          "A tenant sues over an SCRA violation (US:50USC4042) or the Attorney General sues (US:50USC4041-ag-penalties).",
          "Those remedies do not limit any remedy under other law, including consequential and punitive damages (for "
          "example under state law or the lease).",
          "4043", q(f["4043"], "Nothing in section 4041 or 4042 of this title shall be construed to preclude or limit any remedy otherwise available under other law, including consequential and punitive damages."),
          "major", "7", amends="US:50USC4042", dependencies=["US:50USC4042"])

save([
    D("US:50 USC 3914", "new_rule", "Extends SCRA protections (including lease termination) to U.S. citizens serving with "
      "allied forces; changes who may use them.", proposed=[r3914]),
    D("US:50 USC 3919", "new_rule", "Using SCRA relief may not itself ground an adverse credit report or refusal of a "
      "payment plan.", proposed=[r3919]),
    D("US:50 USC 3932", "new_rule", "Mandatory 90-day stay of the landlord's suit on a servicemember's application; no "
      "rule states it.", proposed=[r3932]),
    D("US:50 USC 3935", "new_rule", "Length of SCRA stays with installment terms, and proceeding against non-military "
      "co-defendants only with court approval.", proposed=[r3935]),
    D("US:50 USC 3952", "new_rule", "A lease with a pre-service deposit cannot be terminated for breach without a court "
      "order, and the court may order deposits repaid as a condition.", proposed=[r3952]),
    D("US:50 USC 3956", "new_rule", "Where the landlord supplies internet, home security or gym services under a contract, "
      "a relocating servicemember may end it without charge and with refunds.", proposed=[r3956]),
    D("US:50 USC 3959", "new_rule", "Dependents may obtain subchapter III protections by court application.", proposed=[r3959]),
    D("US:50 USC 4011", "new_rule", "Court relief against transfers made to exploit the SCRA; affects recovery.", proposed=[r4011]),
    D("US:50 USC 4012", "new_rule", "Service certificates are prima facie evidence for the affidavit, stays and tolling; "
      "missing servicemembers presumed in service.", proposed=[r4012]),
    D("US:50 USC 4021", "new_rule", "A servicemember may obtain a stay with installments on a pre-service lease obligation, "
      "with no penalties accruing.", proposed=[r4021]),
    D("US:50 USC 3920", "new_rule", "An attorney or power-of-attorney holder exercises the servicemember's SCRA rights, so "
      "their notices bind the landlord.", proposed=[r3920]),
    D("US:50 USC 4022", "new_rule", "Automatic extension of a servicemember's power of attorney during missing status decides "
      "whether the representative's notice is valid; carried with 3920.",
      proposed=[R("US:50USC4022-poa-missing", "50 U.S.C. 4022(a)-(b)", "landlord; managing agent; Handoff", "must accept",
                  "A relative acting under a servicemember tenant's power of attorney gives the landlord an SCRA notice or "
                  "request after the power's stated expiry, while the servicemember is in missing status.",
                  "The power is extended automatically for the missing period if executed during service (or after orders or "
                  "notice of possible orders), naming a spouse, parent or other relative, and expiring by its terms after "
                  "missing status began; it is not extended if its terms say it expires on the stated date even if the "
                  "servicemember goes missing.",
                  "4022", q(f["4022"], "A power of attorney executed by a servicemember may not be extended under subsection (a) if the document by its terms clearly indicates that the power granted expires on the date specified"),
                  "minor", "3.4", dependencies=["US:50USC3920-representatives"])]),
    D("US:50 USC 4026", "new_rule", "Shields a servicemember's personal assets from a business tenant's lease balance during "
      "service.", proposed=[r4026]),
    D("US:50 USC 4041", "new_rule", "Attorney General enforcement with civil penalties of $55,000/$110,000; "
      "US:50USC4042 mentions AG suits but states no penalty amounts.", proposed=[r4041]),
    D("US:50 USC 4043", "partial", "US:50USC4042 states the private action; 4043 adds that other remedies, including "
      "consequential and punitive damages, remain.", ["US:50USC4042"], [r4043]),
    D("US:50 USC 3953", "no_decision", "Protects servicemember mortgagors against foreclosure of their own property; a "
      "tenant's lease balance is not a mortgage obligation, and a foreclosure successor's duties to tenants are stated in "
      "NY:RPAPL-1305-successor."),
    D("US:50 USC 3902", "no_decision", "Statement of purpose."),
    D("US:50 USC 3912", "no_decision", "Applies the Act to state courts and proceedings, which every stated SCRA rule "
      "already assumes; excludes criminal cases."),
    D("US:50 USC 3954", "no_decision", "Appraisal and equity payments when repossessing personal property or foreclosing on "
      "it; not a tenancy settlement."),
    D("US:50 USC 4013", "no_decision", "Courts may revise their own interlocutory SCRA orders; no act by the landlord."),
    D("US:50 USC 4025", "no_decision", "Residence for voting purposes of absent servicemembers and spouses."),
    D("US:50 USC 4027", "no_decision", "Spouse's election of the servicemember's residence for residency purposes; it does "
      "not change the tenancy or its settlement."),
    D("US:50 USC 3915", "no_decision", "Duty of the military Secretaries to notify servicemembers of benefits."),
    D("US:50 USC 4023", "no_decision", "Suspension of professional liability insurance for called-up professionals."),
    D("US:50 USC 4024", "no_decision", "Reinstatement of health insurance after service."),
    D("US:50 USC 3957", "no_decision", "Assigned life insurance policies; no life policy secures a lease balance in the "
      "chain."),
])
