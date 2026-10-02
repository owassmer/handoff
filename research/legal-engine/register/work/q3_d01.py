import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *

st("NYC:ADC 20-494", ["NYC:ADC-20-490"],
   "Penalty for violating the debt collection agency subchapter ($700-$1,000 per violation, $100 per unlicensed "
   "contact) is stated in NYC:ADC-20-490; the investigation-cost add-on changes no chain decision.")

F = "register/texts/NYC_ADC/26-3402.txt"
dec("NYC:ADC 26-3402", "new_rule",
    "Caps what a landlord may recover from a tenant who vacated in breach of the lease (RPL 227-e duty) at the fair "
    "market cost of preparing the unit for rental and requires an itemized calculation; no rule states it.",
    proposed=[rule(
        "NYC:ADC-26-3402-vacating-fee-cap", "Admin. Code 26-3402 (with 26-3401)",
        "landlord; managing agent; Handoff or collector seeking the amount for the landlord", "prohibition + duty",
        "NYC residential tenancy; the tenant vacated in violation of the lease terms (before the term ended, without a "
        "lawful early-termination right), so the landlord has the RPL 227-e duty to mitigate; the landlord seeks from the "
        "tenant (by deduction on the move-out statement, by demand, through a collector or in suit) an amount arising "
        "from the vacating other than rent.",
        "The landlord may not recover from the tenant any amount in excess of the fair market cost necessary to prepare "
        "the physical condition of the unit for rental. Every other amount charged because the tenant vacated "
        "(re-letting or re-rental fee, broker commission or advertising for a new tenant, lease-break or "
        "early-termination fee, administrative or processing fee, turnover or preparation charge above fair market "
        "cost) is not recoverable above that ceiling, by deduction, demand or suit. Whenever the landlord seeks the "
        "amount it must give the tenant an itemized list demonstrating how the amount was calculated; a demand or "
        "statement line without that list does not meet the section. Rent for the period until the unit is re-let at "
        "fair market value or the lease rate, and a lease-break sum that is valid liquidated damages for lost rent "
        "(NY:ADJ-lease-break-charge), are rent damages governed by RPL 227-e and are outside this ceiling. The ceiling "
        "creates no charge: preparation costs are recoverable only to the extent state and city law already allow "
        "(damage caused by the tenant beyond normal wear and tear, NY:GOL-7-108(1-a)(b)-refundable; never the owner's "
        "statutory turnover work, NYC:HMC-27-2056.8-lead-turnover, NYC:HMC-27-2017.5-turnover). When the tenant left "
        "under a lawful termination right (RPL 227-a, 227-c, SCRA, month-to-month notice) there is no breach, no 227-e "
        "duty, and no vacating amount is owed at all under those rules.",
        F, q(F, "Where a landlord has a duty to mitigate damages", "demonstrating the calculation of such amount."),
        "critical", "3.3; 5.2; 5.4; 8.1", determinacy="MIXED",
        judgment_terms=["fair market cost necessary to prepare the physical conditions of the premises for rental",
                        "amount arising from the vacating versus rent damages"],
        dependencies=["NY:RPL-227-e", "NY:ADJ-lease-break-charge", "NY:GOL-7-108(1-a)(b)-refundable"],
        construction=[{"source_file": "register/texts/NYC_ADC/26-3401.txt",
                       "quote": q("register/texts/NYC_ADC/26-3401.txt", "the term \"duty to mitigate damages\" means",
                                  "section 227-e of the real property law.")},
                      {"source_file": "sources/NY_RPL_227-E.txt",
                       "quote": q("sources/NY_RPL_227-E.txt", "the new tenant's lease shall, once in effect, terminate",
                                  "because of such tenant's vacating the premises.")}],
        reasoning="26-3401 ties the section to the RPL 227-e duty, which arises when a tenant vacates in violation of "
                  "the lease. The chapter is titled 'Fees Associated with Vacating a Premises' and the section "
                  "'Limitation of fees'; the Council's summary of Int. 2312-2021 (L.L. 2021/169) says it limits 'the "
                  "resulting fees recoverable by the landlord' subject to the state mitigation provisions. State law "
                  "(227-e) expressly lets the landlord recover lost rent until re-letting, and a local law cannot "
                  "take that away, so 'any amount' reaches every vacating-related charge other than rent damages. "
                  "In force 2022-06-22 (L.L. 2021/169), renumbered 26-3402 by L.L. 2023/030.",
        effective_from="2022-06-22")])

DET = "NYC:HMC-27-2045-detector-charge"
st("NYC:RCNY 28 12-02", [DET], "Occupant duty and $25/$50/$75 reimbursement caps for smoke devices in class A "
   "multiple dwellings; stated by the detector-charge rule.")
st("NYC:RCNY 28 12-04", [DET], "Sample notice restating occupant replacement duty, manufacturing-defect exception "
   "and $25/$50/$75 caps; stated by the detector-charge rule.")
st("NYC:RCNY 28 12-07", [DET], "Private-dwelling CO alarm duties: owner replaces devices missing from prior "
   "occupancy before a new occupancy, $25 per alarm reimbursement; stated by the detector-charge rule.")
st("NYC:RCNY 28 12-08", [DET], "Occupant CO alarm duty and $25 reimbursement including useful-life replacement "
   "during the tenancy; stated by the detector-charge rule.")
st("NYC:RCNY 28 12-09.2", [DET], "Sample natural gas alarm notice with $25/$50/$75 amounts; stated by the "
   "detector-charge rule.")
st("NYC:RCNY 28 12-10", [DET], "Sample CO alarm notice with $25/$50/$75 amounts; stated by the detector-charge "
   "rule.")
dec("NYC:RCNY 6 2-194", "new_rule",
    "Licensed debt collection agency's call-back number must be answered by a natural person; binds a licensed "
    "collector (or Handoff if licensed) working a former tenant's balance; no rule states it.",
    proposed=[rule(
        "NYC:RCNY6-2-194-callback-person", "6 RCNY 2-194(a)-(b)", "licensed debt collection agency (incl. Handoff "
        "when it is one: NYC:DCA-handoff-principal-purpose)", "duty",
        "A debt collection agency (Admin. Code 20-489) collects a former NYC tenant's balance and must give the "
        "consumer a call-back number under Admin. Code 20-493.1(a)(i).",
        "The call-back number must be answered by a natural person qualified to address the consumer's inquiries "
        "about the agency's communications, or routed to such a person within 60 seconds after the call connects and "
        "answered by that person within 60 seconds after routing, at all times the agency conducts business with "
        "consumers. An owner, its staff, or a manager that is not a debt collection agency has no duty under this "
        "section.",
        "register/texts/NYC_RCNY_T6/2-194.txt",
        q("register/texts/NYC_RCNY_T6/2-194.txt", "shall be a number for a telephone for which a call to that number",
          "within 60 seconds after the call is routed."),
        "major", "8.6", dependencies=["NYC:ADC-20-489(a)", "NYC:ADC-20-490"])])
nd("NYC:RCNY 6 6-90", "Penalty schedule for self-storage facility licensing (Admin. Code 20-566.x); a tenant's "
   "belongings are not stored under a self-storage occupancy agreement in this chain.")
commit()
