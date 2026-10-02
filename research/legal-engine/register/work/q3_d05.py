import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *

A = "register/texts/NYC_ADC/"
nd("NYC:ADC 27-2041", "Owner provides a peephole; no settlement step or charge turns on it.")
nd("NYC:ADC 27-2043", "Owner provides the entrance lock and at least one key; key and lock charges at move-out are "
   "decided by NY:RPL-235-i and the damage rule.")
nd("NYC:ADC 27-2043.1", "Window guards where a young child lives; a guard the tenant removed or damaged is a damage "
   "question under the deposit rule, and no settlement step turns on this section.")
nd("NYC:ADC 27-2046.3", "Outlet covers in public parts; no settlement step.")
nd("NYC:ADC 27-2046.4", "Stove-knob covers on request where a young child lives; in-tenancy duty with no settlement "
   "effect.")
nd("NYC:ADC 27-2047", "Mail delivery arrangements in a multiple dwelling; decides nothing about where the move-out "
   "statement goes (NY:ADJ-provide-address-branches).")
nd("NYC:ADC 27-2056.3", "Lead hazard remediation during a tenancy where a young child lives; the turnover duty that "
   "bears on the settlement is stated at NYC:HMC-27-2056.8-lead-turnover.")
nd("NYC:ADC 27-2056.4", "Annual lead investigation, child-residence inquiry and lease notices; move-in and in-tenancy "
   "duties that fix no settlement amount.")
nd("NYC:ADC 27-2056.5", "Presumption that pre-1960 paint is lead-based and HPD exemptions; an exempt unit has no lead "
   "turnover work, so no charge question arises, and the cost allocation where work arises is stated at "
   "NYC:HMC-27-2056.8-lead-turnover.")
nd("NYC:ADC 27-2056.6", "Classifies peeling lead paint as a class C violation; HPD enforcement, no settlement step.")
nd("NYC:ADC 27-2084", "Occupancy standards for cellar and basement units in converted dwellings; the rent "
   "consequence of unlawful occupancy runs through the certificate-of-occupancy bar (NY:MDL-301(1), "
   "NY:MDL-302(1)(b)) and these standards set no settlement amount.")
nd("NYC:ADC 27-2086", "Occupancy standards for cellar and basement units in old law tenements; same as 27-2084.")
nd("NYC:ADC 27-2095", "How HPD serves its notices and orders; no settlement step.")
nd("NYC:ADC 27-2096", "Signing and certifying HPD applications and registrations; false statements are an offense. "
   "No settlement step.")
st("NYC:ADC 27-2099", ["NYC:ADC-27-2097-registration", "NY:MDL-325(2)"],
   "A buyer must file its registration within 5 days of taking title (30 days by operation of law); the settlement "
   "consequence (no rent recovery until registered, walk C10) is stated and runs from non-registration, not from "
   "the filing deadline.")
nd("NYC:ADC 27-2101", "Changing or terminating a managing agent's designation with HPD; the notice to tenants that "
   "matters for payment is 27-2105(b).")
st("NYC:ADC 27-2102", ["NYC:ADC-27-2097-registration", "NY:MDL-325(2)"],
   "A lessee of an entire multiple dwelling registers like an owner; the registration duty and its rent "
   "consequence are stated.")
dec("NYC:ADC 27-2105", "new_rule",
    "Every rent bill or receipt, including for arrears paid at move-out, must name the registered managing agent or "
    "owner and any separate rent-collection agent, and a change of collection agent needs 15 days' mailed notice; "
    "this decides the form of payment documents and who may be named to collect. Not stated.",
    proposed=[rule("NYC:ADC-27-2105-rent-receipt-agent", "Admin. Code 27-2105(a)-(b)",
                   "owner; managing agent; agent designated to collect rent (incl. Handoff or a collector when "
                   "designated)", "duty",
                   "A dwelling that must register with HPD (multiple dwelling, or non-owner-occupied one- or "
                   "two-family house); the tenant pays rent, including final rent or rent arrears at or after "
                   "move-out; or the owner designates a new managing agent or a new agent to collect rent.",
                   "At each rent payment a rent bill or receipt is issued stating the name and New York City address "
                   "of the managing agent (or the owner, as in the current HPD registration), and of the agent the "
                   "owner designated to collect rent if different, printed on the managing agent's letterhead or the "
                   "letterhead of the owner's NYC address; the owner's registered name and address may replace the "
                   "managing agent's if the owner lives or does business in the city; a new agent or owner must be "
                   "stated. When the managing agent or rent-collection agent changes (e.g. the owner designates "
                   "Handoff or a collector to receive a former tenant's rent balance), the owner mails each affected "
                   "tenant regular-mail notice, postmarked at least 15 days before the next rent payment is to be "
                   "collected, with the new agent's telephone number. Charges other than rent (damage, fees) are "
                   "outside the section.",
                   A + "27-2105.txt", q(A + "27-2105.txt", "At the time of each rental payment",
                                        "if different from the managing agent."),
                   "major", "8.6a; 1.8", dependencies=["NYC:ADC-27-2097-registration", "NY:RPL-235-e(a)"])])
dec("NYC:ADC 27-2106", "new_rule",
    "In a rent suit the owner's failure to produce HPD's registration receipt is prima facie evidence it did not "
    "register, which triggers the rent bar and stay; not stated.",
    proposed=[rule("NYC:ADC-27-2106-registration-proof", "Admin. Code 27-2106(a)-(b)", "owner; lessee of an entire "
                   "multiple dwelling; managing agent", "evidence",
                   "The owner (or lessee of an entire multiple dwelling) sues or counterclaims for rent, or defends a "
                   "former tenant's claim, and its registration is in issue.",
                   "Failure to produce the HPD receipt acknowledging the registration filing is prima facie evidence "
                   "of non-registration (so NY:MDL-325(2) and NYC:ADC-27-2107(b)-rent-stay apply unless rebutted); the "
                   "filed registration statement is prima facie proof of its contents in a tenant's action against "
                   "the owner or managing agent. Keep the receipt with the settlement file before suing.",
                   A + "27-2106.txt", q(A + "27-2106.txt", "The failure of the owner or lessee of an entire multiple",
                                        "prima facie evidence of failure to comply with the provisions of this article."),
                   "minor", "8.10", dependencies=["NY:MDL-325(2)", "NYC:ADC-27-2107(b)-rent-stay"])])
nd("NYC:ADC 27-2109.1", "A foreclosing mortgagee's notice to HPD; the tenant-facing foreclosure rules are stated at "
   "NY:RPAPL-1305-successor.")
commit()
