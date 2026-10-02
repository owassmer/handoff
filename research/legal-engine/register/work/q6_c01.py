"""q6 chunk 1: batch_6 items 0-5 (strong tier)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q6_lib import D, P, q, save, tf

S = "US:12 CFR 1006.18"
f18 = tf(S)
r18 = P("US:12CFR1006.18-other-representations", "12 CFR 1006.18(a)-(d), (e)(3), (f)", "debt collector", "must not",
        "A debt collector (FDCPA 1692a(6); for Handoff by configuration, US:HANDOFF-config-*) communicates about or "
        "collects a former tenant's move-out balance, by letter, email, text, call or court paper.",
        "It may not use any false, deceptive or misleading representation or means, including: implying government "
        "affiliation or bonding, that it is or works for a consumer reporting agency, that any individual is an "
        "attorney or a communication is from one, that the tenant committed a crime or disgraceful conduct, that a "
        "sale or referral of the balance makes the tenant lose a defense or become subject to a prohibited practice, "
        "that the account was turned over to innocent purchasers for value, that documents are legal process or that "
        "legal-process documents need no action; misstating the services rendered or the compensation it may "
        "lawfully receive; saying non-payment will lead to arrest, imprisonment, or seizure, garnishment, attachment "
        "or sale of property or wages unless that action is lawful and the collector or owner intends it; sending "
        "anything that simulates a court or agency document or misstates its source. The collector-identity "
        "disclosures (US:15USC1692e(11)) are not required in a formal pleading. An employee may use an assumed name "
        "only if used consistently and the collector can identify the employee. Amount, legal status, threats, "
        "credit information and business name are stated in US:15USC1692e(2)(A), (5), (8), (14).",
        f18, q(f18, "(b) False, deceptive, or misleading representations. (1) A debt collector must not falsely represent or imply that:",
               "(viii) Documents are not legal process forms or do not require action by the consumer."),
        "major", "8.3", determinacy="MIXED",
        judgment_terms=["false, deceptive, or misleading representation", "intends to take such action"],
        dependencies=["US:15USC1692e(2)(A)", "US:15USC1692e(5)", "US:15USC1692e(8)", "US:15USC1692e(11)",
                      "US:15USC1692e(14)"],
        instrument="Regulation F, 12 CFR part 1006 (CFPB)",
        construction=[(f18, q(f18, "(3) A debt collector must not represent or imply that nonpayment of any debt will result in the arrest",
                              "unless such action is lawful and the debt collector or creditor intends to take such action.")),
                      (f18, q(f18, "(f) Assumed names.", "can readily identify any employee using an assumed name."))],
        reasoning="1006.18(b)-(d) list the prohibited representations beyond those the existing 1692e atoms state; "
                  "(b)(3) conditions threats of garnishment or seizure on lawfulness and intent; (e)(3) exempts formal "
                  "pleadings from the disclosures; (f) permits consistent assumed names.")

f13 = tf("US:50 USC 3913")
r13 = P("US:50USC3913-guarantor-cotenant", "50 U.S.C. 3913(a), (b), (d)", "court; landlord", "may / effective only if",
        "The landlord sues for a move-out balance that a servicemember tenant owes jointly or that a guarantor, "
        "co-signer or co-tenant also owes, and the court stays, postpones or vacates the action or judgment against "
        "the servicemember under the SCRA (e.g. 50 U.S.C. 3931, 3932, 3934).",
        "The court may give the same stay, postponement or suspension to the guarantor, co-signer, co-tenant or other "
        "person primarily or secondarily liable, and may set aside a judgment against them when it sets aside the "
        "servicemember's. A written waiver of these protections by a guarantor or co-obligor is effective only if "
        "executed as an instrument separate from the lease or guaranty; a waiver signed before the signer (or the "
        "person whose dependent signed) entered military service is not valid after service begins unless signed "
        "during the 3917 period after receipt of orders. A waiver clause inside the lease or guaranty is not "
        "effective.",
        f13, q(f13, "the court may likewise grant such a stay, postponement, or suspension to a surety, guarantor, endorser",
               "the performance or enforcement of which is stayed, postponed, or suspended."),
        "major", "8.9", determinacy="MIXED", judgment_terms=["court discretion to extend the stay"],
        dependencies=["US:50USC3931(b)(1)", "US:50USC3917(a)", "US:50USC3918"],
        instrument="Servicemembers Civil Relief Act, 50 U.S.C. 3901-4043",
        construction=[(f13, q(f13, "Any such waiver is effective only if it is executed as an instrument separate from the obligation or liability with respect to which it applies."))],
        reasoning="3913(a)-(b) extend court relief to co-obligors at the court's discretion; 3913(d) sets the separate-"
                  "instrument waiver rule and voids pre-service waivers after service begins.")

f33 = tf("US:50 USC 3933")
r33 = P("US:50USC3933-penalties", "50 U.S.C. 3933(a), (b)", "landlord; court", "must not / may",
        "A servicemember tenant owes a lease obligation, and a penalty (late fee, lease-break penalty or other "
        "contractual penalty) would accrue or has accrued for non-performance.",
        "(a) While an action to enforce the lease is stayed under the SCRA, no penalty accrues for failure to comply "
        "with the lease during the stay, so late fees for that period are not charged on the account. (b) If the "
        "tenant was in military service when the penalty was incurred and service materially affected the ability to "
        "perform, a court may reduce or waive it.",
        f33, q(f33, "When an action for compliance with the terms of a contract is stayed pursuant to this chapter, a penalty shall not accrue",
               "during the period of the stay."),
        "major", "8.10", determinacy="MIXED", judgment_terms=["materially affected by such military service"],
        dependencies=["US:50USC3911(1)-(2)"], instrument="Servicemembers Civil Relief Act, 50 U.S.C. 3901-4043",
        construction=[(f33, q(f33, "If a servicemember fails to perform an obligation arising under a contract and a penalty is incurred",
                              "was materially affected by such military service."))],
        reasoning="(a) is a flat bar during a stay; (b) is a court power turning on material effect.")

f34 = tf("US:50 USC 3934")
r34 = P("US:50USC3934-execution-stay", "50 U.S.C. 3934(a), (b)", "court; landlord", "shall on application",
        "The landlord holds a judgment or order for the move-out balance against a servicemember, or attaches or "
        "garnishes the servicemember's property, wages or bank funds (before or after judgment), in an action begun "
        "before or during military service or within 90 days after it ends.",
        "If the servicemember's ability to comply is materially affected by military service, the court may on its "
        "own motion, and must on the servicemember's application, stay execution of the judgment and vacate or stay "
        "the attachment or garnishment. Enforcement plans for such a balance account for this stay.",
        f34, q(f34, "the court may on its own motion and shall on application by the servicemember", "whether before or after judgment."),
        "major", "8.12", determinacy="MIXED", judgment_terms=["materially affected by reason of military service"],
        dependencies=["US:50USC3911(1)-(2)"], instrument="Servicemembers Civil Relief Act, 50 U.S.C. 3901-4043",
        construction=[(f34, q(f34, "This section applies to an action or proceeding commenced in a court against a servicemember before or during"))],
        reasoning="3934(a) makes the stay mandatory on application once material effect is found; (b) limits it to actions "
                  "begun before, during or within 90 days after service.")

save([
    D("US:12 CFR 1006.10", "stated", "US:15USC1692b states location communications in full and names 12 CFR 1006.10 as "
      "its implementation: identity, no debt mention, once per person, no postcards or collection wording, attorney-only.",
      ["US:15USC1692b"]),
    D(S, "partial", "Existing 1692e atoms state amount/status, threats, credit information, disclosures and true name; "
      "the other Reg F representation bans, the pleading exception and assumed names are unstated.",
      ["US:15USC1692e(2)(A)", "US:15USC1692e(5)", "US:15USC1692e(8)", "US:15USC1692e(11)", "US:15USC1692e(14)"], [r18]),
    D("US:12 USC 5220 note", "stated", "NY:RPAPL-1305-successor states the foreclosure successor's duties and records "
      "that the state right (90 days or the lease remainder) meets the PTFA 90-day floor; PTFA preserves longer state "
      "protections.", ["NY:RPAPL-1305-successor"]),
    D("US:50 USC 3913", "new_rule", "Court stays and vacaturs for a servicemember may reach co-tenants and guarantors, "
      "and guarantor waivers need a separate instrument; this changes whom the landlord may recover from and when.",
      proposed=[r13]),
    D("US:50 USC 3933", "new_rule", "No penalty (late fee) accrues during an SCRA stay and a court may waive penalties; "
      "this changes what may be charged on the account.", proposed=[r33]),
    D("US:50 USC 3934", "new_rule", "Mandatory stay of execution, attachment and garnishment on the servicemember's "
      "application changes post-judgment recovery of the balance.", proposed=[r34]),
])
