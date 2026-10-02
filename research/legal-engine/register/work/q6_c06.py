"""q6 chunk 6: TILA part A, CCPA garnishment, E-SIGN definitions/government."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q6_lib import D, P, q, save, tf

TILA = "Truth in Lending Act, 15 U.S.C. 1601-1667f"
f05, f03, f11, f15, f06 = (tf("US:15 USC 1605"), tf("US:15 USC 1603"), tf("US:15 USC 1611"), tf("US:15 USC 1615"),
                           tf("US:15 USC 7006"))

r_fc = P("US:15USC1605-plan-finance-charge", "15 U.S.C. 1605(a)", "landlord; managing agent; Handoff", "scope",
         "The landlord (or Handoff for it) offers a former tenant who is a natural person a payment plan for the move-out "
         "balance and charges, as an incident to the plan, interest, a time-price differential, a service or carrying "
         "charge, a plan set-up or similar fee, or a credit-report fee.",
         "Each such charge is a finance charge, so the plan is consumer credit 'for which the payment of a finance charge "
         "is or may be required'. A landlord that regularly offers such plans (or regularly offers plans payable in more "
         "than four installments) is a TILA creditor (US:15USC1602(g)) and each covered plan requires the TILA part B "
         "closed-end credit disclosures before consummation. Amounts that would be owed anyway in a comparable cash "
         "transaction (the rent, damage and lawful lease charges themselves) are not finance charges. A plan with no "
         "finance charge and at most four installments does not make the landlord a creditor.",
         f05, q(f05, "the amount of the finance charge in connection with any consumer credit transaction shall be determined as the sum of all charges, payable directly or indirectly by the person to whom the credit is extended, and imposed directly or indirectly by the creditor as an incident to the extension of credit. The finance charge does not include charges of a type payable in a comparable cash transaction."),
         "critical", "8.1b", determinacy="MIXED", judgment_terms=["incident to the extension of credit", "regularly extends"],
         instrument=TILA, dependencies=["US:15USC1602(f)", "US:15USC1602(g)", "US:15USC1603-plan-exemptions"],
         construction=[(f05, q(f05, "Interest, time price differential, and any amount payable under a point, discount, or other system or additional charges."))],
         reasoning="1605(a) defines the finance charge by charges imposed incident to the credit, excluding comparable cash "
                   "charges; 1602(g) makes a regular extender of credit with a finance charge a creditor.")

r_ex = P("US:15USC1603-plan-exemptions", "15 U.S.C. 1603(1), (3)", "landlord; managing agent; Handoff", "scope",
         "A landlord that is a TILA creditor (US:15USC1605-plan-finance-charge) gives a payment plan for a move-out balance.",
         "TILA does not apply to a plan with a tenant that is an organization (company, partnership, LLC), to credit "
         "primarily for business or commercial purposes, or to a plan whose amount financed exceeds the statutory "
         "threshold ($50,000 as adjusted), none of which is secured by real property or the tenant's dwelling. A plan with "
         "a natural-person tenant for a residential tenancy balance under the threshold is covered.",
         f03, q(f03, "Credit transactions involving extensions of credit primarily for business, commercial, or agricultural purposes, or to government or governmental agencies or instrumentalities, or to organizations."),
         "major", "8.1b", instrument=TILA, dependencies=["US:15USC1605-plan-finance-charge"],
         construction=[(f03, q(f03, "in which the total amount financed exceeds $50,000."))],
         reasoning="1603(1) and (3) exempt organization, business-purpose and large unsecured credit.")

r_cr = P("US:15USC1611-criminal", "15 U.S.C. 1611", "landlord; managing agent; Handoff", "liable",
         "A landlord that is a TILA creditor for a payment plan willfully and knowingly gives false information, omits "
         "required disclosures, or otherwise fails to comply with TILA.",
         "It is punishable by a fine of up to $5,000, imprisonment of up to one year, or both.",
         f11, q(f11, "otherwise fails to comply with any requirement imposed under this subchapter,", "shall be fined not more than $5,000 or imprisoned not more than one year, or both."),
         "minor", "8.1b", determinacy="MIXED", judgment_terms=["willfully and knowingly"], instrument=TILA,
         dependencies=["US:15USC1605-plan-finance-charge"])

r_78 = P("US:15USC1615-unearned-interest", "15 U.S.C. 1615(a), (b)", "landlord; managing agent; Handoff", "must",
         "A landlord that is a TILA creditor gives a payment plan with an interest charge, and the former tenant prepays "
         "the plan in full (including after acceleration or restructuring).",
         "The landlord promptly refunds the unearned part of the interest charge (not required if under $1); for a "
         "precomputed plan longer than 61 months the refund is computed by a method at least as favorable as the "
         "actuarial method.",
         f15, q(f15, "If a consumer prepays in full the financed amount under any consumer credit transaction, the creditor shall promptly refund any unearned portion of the interest charge to the consumer."),
         "minor", "8.1b", instrument=TILA, dependencies=["US:15USC1605-plan-finance-charge"])

f7001 = "sources/REVIEW5A_US_15USC_7001_ESIGN.txt"
r_es = P("US:15USC7006-esign-consumer", "15 U.S.C. 7006(1), (4), (5), (13)", "landlord; managing agent; Handoff", "scope",
         "The landlord sends electronically a record that law requires to be given in writing, or relies on an electronic "
         "signature (lease, autopay authorization, payment plan, settlement).",
         "The consumer-consent requirements (US:15USC7001(c)-esign-consent) apply only where the tenant is a consumer: an "
         "individual who obtains the tenancy primarily for personal, family or household purposes, or that individual's "
         "legal representative. A company tenant, or an individual renting for business use, is not; records to it may be "
         "sent electronically without the 7001(c) disclosures and consent. The lease of real property is a "
         "'transaction', and an electronic signature is any electronic sound, symbol or process attached to or logically "
         "associated with the record and executed or adopted with intent to sign.",
         f06, q(f06, "The term “consumer” means an individual who obtains, through a transaction, products or services which are used primarily for personal, family, or household purposes, and also means the legal representative of such an individual."),
         "major", "6.4", instrument="E-SIGN Act, 15 U.S.C. 7001-7031", amends="US:15USC7001(c)-esign-consent",
         dependencies=["US:15USC7001(c)-esign-consent"],
         construction=[(f06, q(f06, "the sale, lease, exchange, or other disposition of any interest in real property, or any combination thereof.")),
                       (f06, q(f06, "The term “electronic signature” means an electronic sound, symbol, or process, attached to or logically associated with a contract or other record and executed or adopted by a person with the intent to sign the record."))],
         reasoning="7001(c) protects a 'consumer' as 7006(1) defines it; 7006(13)(B) includes real-property leases.")

save([
    D("US:15 USC 1605", "new_rule", "Whether a payment plan's interest or fees are finance charges decides whether the "
      "landlord is a TILA creditor (the stated 1602(g) test) and whether TILA disclosures reach the plan.", proposed=[r_fc]),
    D("US:15 USC 1603", "new_rule", "Exempts plans with company tenants, business-purpose credit and large amounts; decides "
      "whether TILA reaches a payment plan.", proposed=[r_ex]),
    D("US:15 USC 1611", "new_rule", "Criminal liability of a landlord that is a TILA creditor for willful violations.", proposed=[r_cr]),
    D("US:15 USC 1615", "new_rule", "Refund of unearned interest when a creditor-landlord's payment plan is prepaid.", proposed=[r_78]),
    D("US:15 USC 1604", "no_decision", "CFPB disclosure rulemaking and model forms; the duty to disclose sits in part B, "
      "not in this section."),
    D("US:15 USC 1606", "no_decision", "APR computation method; it fixes a number within the part B disclosures a creditor-"
      "landlord gives (US:15USC1605-plan-finance-charge) and decides nothing on its own."),
    D("US:15 USC 1607", "no_decision", "Allocates administrative enforcement of TILA among agencies."),
    D("US:15 USC 1610", "no_decision", "Preserves consistent state disclosure and credit-charge laws and contract validity; "
      "changes no decision in the chain."),
    D("US:15 USC 1612", "no_decision", "Government credit programs and immunity of government agencies; no landlord in the "
      "chain is one."),
    D("US:15 USC 1673", "stated", "NY:CPLR-5205-5231-enforcement-limits states the income-execution cap, which CPLR 5231(b) "
      "sets at the stricter of ten percent of gross income and the federal 25%/thirty-times-minimum-wage limits (using the "
      "higher state minimum wage); 1677 preserves the stricter state rule.", ["NY:CPLR-5205-5231-enforcement-limits"]),
    D("US:15 USC 1677", "no_decision", "Preserves stricter state garnishment limits, which the stated NY rule already applies."),
    D("US:15 USC 1674", "no_decision", "Bars an employer from firing an employee over one garnishment; binds the tenant's "
      "employer, not anyone in the chain."),
    D("US:15 USC 1675", "no_decision", "Secretary of Labor exemptions for state garnishment laws; no decision for the landlord."),
    D("US:15 USC 1671", "no_decision", "Findings and purpose."),
    D("US:15 USC 1672", "no_decision", "Definitions of earnings and garnishment used by 1673, whose limit is applied through "
      "the stated NY income-execution rule."),
    D("US:15 USC 1676", "no_decision", "Department of Labor enforcement."),
    D("US:15 USC 7006", "partial", "US:15USC7001(c)-esign-consent does not state that consent is owed only to a 'consumer' "
      "(an individual for personal, family or household purposes); a company tenant is outside.",
      ["US:15USC7001(c)-esign-consent"], [r_es]),
    D("US:15 USC 7004", "no_decision", "Government filing requirements and agency interpretive authority under E-SIGN; no "
      "rule under it changes a landlord's electronic delivery in the chain."),
])
