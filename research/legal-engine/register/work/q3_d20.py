import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *
R31 = "register/texts/NYC_RCNY_T31/"
R6 = "register/texts/NYC_RCNY_T6/"
dec("NYC:RCNY 31 5-07", "new_rule",
    "HRA may withhold SOTA rent payments for conditions, and releases them only if the problem is resolved while the "
    "household still lives there; this decides whether withheld months are ever paid once the household leaves. Not "
    "stated.",
    proposed=[rule("NYC:RCNY31-5-07-SOTA-withholding", "31 RCNY 5-07(a)-(c)", "owner; manager", "who is paid",
                   "HRA granted a SOTA household's request to withhold SOTA payments because of housing conditions (a "
                   "housing court action, or a DOB or HPD violation for an NYC unit), and the household later moves "
                   "out.",
                   "Withheld payments are released only if the condition was resolved while the household still lived "
                   "in the unit, and only for periods it lived there; a landlord seeking release must give HRA a court "
                   "order or inspection report showing the condition cleared, within 60 days of resolution. If the "
                   "condition was not resolved before the household left, HRA never pays the withheld months. The "
                   "move-out account shows withheld months as HRA-withheld, not as rent the household failed to pay; "
                   "any claim against the tenant for rent in those months is decided under the lease and the warranty "
                   "of habitability (NY:RPL-235-b).",
                   R31 + "5-07.txt", q(R31 + "5-07.txt", "Withheld payments will only be released if the issue was resolved",
                                       "for periods of time when the program participant resided in the unit."),
                   "major", "5.8", determinacy="MIXED", judgment_terms=["issue resolved"],
                   dependencies=["NYC:RCNY31-5-06(a)(10)", "NY:RPL-235-b"])])
nd("NYC:RCNY 47 2-03", "Sex-restricted rooming houses and lodging facilities are exempt from the public "
   "accommodations provision; the chain's equal-treatment rule is the housing provision 8-107(5).")
nd("NYC:RCNY 47 2-10", "Employment discrimination based on reproductive health decisions; no housing settlement "
   "decision.")
nd("NYC:RCNY 6 1-04", "False statements to DCWP by licensees; licence administration.")
dec("NYC:RCNY 6 1-05", "new_rule",
    "A licensed collector's letterhead, receipts, website and emails to a former tenant must carry its DCWP licence "
    "number; not stated for the current rules.",
    proposed=[rule("NYC:RCNY6-1-05-licence-number", "6 RCNY 1-05", "DCWP-licensed debt collection agency (incl. "
                   "Handoff when licensed)", "form",
                   "A DCWP licensee (e.g. a licensed debt collection agency) sends a former NYC tenant a letter, receipt, "
                   "email or other printed or electronic matter, or maintains a website or advertisement.",
                   "Each must show the licensee's DCWP licence number, clearly identified as a New York City "
                   "Department of Consumer Affairs licence number; every email to a consumer must contain it. A "
                   "telephone listing of only name, address and number is exempt. An owner or manager that holds no "
                   "DCWP licence has no licence number to show.",
                   R6 + "1-05.txt", q(R6 + "1-05.txt", "Any advertisement, letterhead, receipt, online media, website",
                                      "must contain the license number assigned to the licensee by the Department."),
                   "major", "8.6", dependencies=["NYC:ADC-20-490"])])
nd("NYC:RCNY 6 1-06", "Proof of surety bond for licensing; licence administration.")
nd("NYC:RCNY 6 1-11", "Fee for a check dishonored in paying DCWP; licence administration.")
nd("NYC:RCNY 6 1-13", "Licensee must answer DCWP complaints within 20 days; agency procedure arising only on a "
   "complaint.")
nd("NYC:RCNY 6 1-14", "Licensee responses to DCWP subpoenas and document requests; agency procedure.")
commit()
