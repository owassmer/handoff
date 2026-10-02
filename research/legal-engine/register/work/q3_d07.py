import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *

A = "register/texts/NYC_ADC/"
T = "NYC:ADC-8-107(5)(a)-terms"
dec("NYC:ADC 8-502", "new_rule",
    "The tenant's city-law court action for discriminatory settlement or collection: damages including punitive, "
    "fees, three-year limit with tolling, election of remedies. Only the state remedy is stated.",
    proposed=[rule("NYC:ADC-8-502-private-action", "Admin. Code 8-502(a), (b), (d), (g), (h)",
                   "owner; manager; Handoff; collector (defendants); former tenant (plaintiff)", "liability",
                   "A settlement or collection decision on an NYC tenancy (deduction, strictness of damage review, "
                   "pursuit, credit reporting or write-off of a balance) is an unlawful discriminatory practice under "
                   "NYC:ADC-8-107(5)(a)-terms, whether done by the owner or by its agent or employee acting within the "
                   "scope of the agency (manager, Handoff, collector).",
                   "The tenant may sue in any court of competent jurisdiction for damages, including punitive damages, "
                   "injunctive and other relief, and the court may award the prevailing party reasonable attorney's "
                   "fees, expert fees and costs. The action must be commenced within three years after the practice; "
                   "the period is tolled while a complaint on the same practice is pending before the NYC Commission "
                   "on Human Rights or the State Division of Human Rights and during court review of its dismissal. "
                   "The court route is closed if the tenant filed such an agency complaint, unless the agency "
                   "dismissed it for administrative convenience, untimeliness, or on annulment of the election of "
                   "remedies. A deprivation of the right alone makes the tenant aggrieved, with no further injury "
                   "required.",
                   A + "8-502.txt", q(A + "8-502.txt", "shall have a cause of action in any court of competent jurisdiction",
                                      "such other remedies as may be appropriate,"),
                   "critical", "5.10; 7.6", dependencies=[T, "NY:EXC-297(9)-remedies"],
                   construction=[{"source_file": A + "8-502.txt",
                                  "quote": q(A + "8-502.txt", "A civil action commenced under this section must be commenced within three years",
                                             "such three-year limitations period shall be tolled.")},
                                 {"source_file": A + "8-502.txt",
                                  "quote": q(A + "8-502.txt", "the court, in its discretion, may award the prevailing party reasonable attorney's fees",
                                             "expert fees and other costs.")}],
                   reasoning="Subdivision (a) creates the action and its election-of-remedies bar, (b) restores the "
                             "action after the listed dismissals, (d) fixes the three-year period and its tolling, (g) "
                             "fees, and (h) makes conduct of an agent within the scope of the agency the covered "
                             "entity's.")])
dec("NYC:ADC 8-109", "new_rule",
    "The Commission complaint route for the same practice: one-year limit (three for gender-based harassment) and "
    "the bar where the tenant already sued or went to the State Division. Not stated.",
    proposed=[rule("NYC:ADC-8-109-commission-complaint", "Admin. Code 8-109(a), (e), (f)", "former tenant; owner; "
                   "manager; Handoff; collector", "limitation",
                   "A former tenant claims a settlement or collection decision was discriminatory under "
                   "NYC:ADC-8-107(5)(a)-terms and chooses the Commission on Human Rights.",
                   "The tenant may file a verified complaint with the Commission; the Commission has no jurisdiction "
                   "over a complaint filed more than one year after the practice (three years for gender-based "
                   "harassment), or where the tenant already started a court action on the same grievance (unless "
                   "dismissed or withdrawn without prejudice), has a pending State Division proceeding on it, or "
                   "obtained a final State Division determination on it. The Commission may also file its own "
                   "complaint.",
                   A + "8-109.txt", q(A + "8-109.txt", "The commission shall not have jurisdiction over any complaint that has been filed more than one year",
                                      "within three years after the alleged harassing conduct occurred."),
                   "major", "7.6", dependencies=[T, "NYC:ADC-8-502-private-action"])])
dec("NYC:ADC 8-120", "new_rule",
    "What the Commission may order against a landlord, manager or collector found to have discriminated in the "
    "settlement: compensatory damages, fees and costs, affirmative relief. Not stated.",
    proposed=[rule("NYC:ADC-8-120-commission-remedies", "Admin. Code 8-120(a)", "owner; manager; Handoff; collector",
                   "liability",
                   "After a hearing the Commission finds a settlement or collection practice on an NYC tenancy was an "
                   "unlawful discriminatory practice.",
                   "It orders the respondent to cease and desist and to take affirmative action, including payment of "
                   "compensatory damages to the tenant and of the tenant's reasonable attorney's fees, expert fees and "
                   "costs, and reports on compliance; civil penalties may be added under Admin. Code 8-126. Punitive "
                   "damages are a court remedy (NYC:ADC-8-502-private-action), not a Commission remedy.",
                   A + "8-120.txt", q(A + "8-120.txt", "Payment of compensatory damages to the person aggrieved by such practice or act;", None),
                   "major", "5.10; 7.6", dependencies=[T])])
nd("NYC:ADC 8-116", "Commission probable-cause procedure and posting; agency procedure with no settlement step.")
nd("NYC:ADC 8-122", "Commission may seek a TRO during its proceeding; agency procedure.")
nd("NYC:ADC 8-124", "Penalty for violating a Commission order already issued; arises only after an adjudication and "
   "changes no settlement step.")
nd("NYC:ADC 8-125", "Enforcement of Commission orders in court; agency procedure.")
dec("NYC:ADC 8-126", "new_rule", "Civil penalty exposure for a discriminatory settlement or collection practice; not "
    "stated.",
    proposed=[rule("NYC:ADC-8-126-civil-penalty", "Admin. Code 8-126(a)-(c)", "owner; manager; Handoff; collector",
                   "consequence",
                   "The Commission finds a settlement or collection practice on an NYC tenancy was an unlawful "
                   "discriminatory practice.",
                   "In addition to damages and fees, the Commission may impose a civil penalty of up to $125,000, or up "
                   "to $250,000 where the practice was willful, wanton or malicious; the respondent may plead and prove "
                   "mitigating factors. A knowingly false material statement in a Commission proceeding or in a record "
                   "the chapter requires carries a further penalty of up to $10,000.",
                   A + "8-126.txt", q(A + "8-126.txt", "impose a civil penalty of not more than $125,000.",
                                      "impose a civil penalty of not more than $250,000."),
                   "major", "5.10; 7.6", determinacy="MIXED",
                   judgment_terms=["willful, wanton or malicious", "mitigating factor"], dependencies=[T])])
nd("NYC:ADC 8-129", "Criminal penalty for obstructing the Commission or willfully violating its order; arises only "
   "after an order.")
nd("NYC:ADC 8-402", "City's pattern-or-practice action through corporation counsel; the city's enforcement choice, "
   "not a chain party's step.")
nd("NYC:ADC 8-404", "Civil penalty in the city's pattern-or-practice action; same as 8-402.")
nd("NYC:ADC 8-602", "City's action to enjoin bias-motivated threats, intimidation or coercion; no settlement or "
   "collection step involves such conduct and the tenant-facing rule is 8-107.")
nd("NYC:ADC 8-603", "Bars bias-motivated injury or threats by force and property destruction; no settlement or "
   "collection step involves force, and collection conduct limits are stated in Step 8.")
commit()
