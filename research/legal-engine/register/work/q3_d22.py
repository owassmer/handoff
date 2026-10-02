import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *
R6 = "register/texts/NYC_RCNY_T6/"
R68 = "register/texts/NYC_RCNY_T68/"
# consistency revision: HPD voucher split is an agency calculation, like CityFHEPS 10-06
nd("NYC:ADC 26-3905", "HPD's calculation of its monthly payment to the owner and the household contribution under "
   "the city rental assistance voucher (from 2027-01-26); the landlord requirements and move-out rules are left to "
   "HPD rules under 26-3907, none adopted, and the calculation itself fixes no settlement step (as with CityFHEPS, "
   "68 RCNY 10-06).")
dec("NYC:RCNY 6 6-47", "partial",
    "The Consumer Protection Law hook is stated; DCWP's penalty amounts for a 20-700 deceptive or unconscionable "
    "practice (e.g. a deceptive move-out charge or demand) are not.", ["NYC:CPL-20-700"],
    [rule("NYC:RCNY6-6-47-CPL-penalties", "6 RCNY 6-47", "owner; manager; Handoff; collector", "consequence",
          "DCWP finds that a settlement or collection practice toward a former NYC tenant is a deceptive or "
          "unconscionable trade practice under Admin. Code 20-700 (outside the 6 RCNY 5-77 and 5-78 rules, whose "
          "amounts are in 6 RCNY 6-62).",
          "$525 first, $1,050 second, $3,500 third and later violation within three years (same on default); a "
          "knowing violation carries $3,500; each statement, representation or omission is a separate violation, "
          "counted per 20-703(c).",
          R6 + "6-47.txt", q(R6 + "6-47.txt", "the knowing violation of any provision of Subchapter 1 of Chapter 5",
                             "is subject to a penalty of $3,500."),
          "minor", "8.4", dependencies=["NYC:CPL-20-700", "NYC:ADC-20-703-CPL-remedies"], amends="NYC:CPL-20-700")])
nd("NYC:RCNY 6 6-56", "Penalty schedule for immigration assistance services; no chain party.")
nd("NYC:RCNY 6 6-60", "Penalty schedule for domestic worker notices; no chain party.")
nd("NYC:RCNY 6 6-72", "Penalty schedule for cashless retail establishments; a landlord is not a retail food or "
   "retail establishment and rent-payment methods are governed by NY:RPL-235-g.")
nd("NYC:RCNY 6 6-82", "Penalty schedule for force-fed food products; no chain party.")
nd("NYC:RCNY 68 10-05", "HRA's maximum rents and utility allowance for CityFHEPS; decided at approval, no settlement "
   "step.")
nd("NYC:RCNY 68 10-06", "HRA's calculation of the CityFHEPS payment and participant contribution for apartments and "
   "SROs; the landlord's move-out duties (no extra charges, notice, return of payments for months not occupied) are "
   "stated at NYC:RCNY68-10-14(a), (e), (h).")
st("NYC:RCNY 68 10-07", ["NYC:RCNY68-10-14(h)"],
   "For a room HRA may pay the first four months in advance; payments covering months the household did not live "
   "there are returned under the stated rule. The calculation itself decides nothing further.")
nd("NYC:RCNY 68 10-15", "CityFHEPS program terms (no combining subsidies, no waitlist, landlord-incentive "
   "restrictions, relatives as landlords); none decides a settlement step.")
nd("NYC:RCNY 68 7-04", "LINC VI rent limits and payments to the primary occupant; the chapter expired and was repealed "
   "on 2024-12-31 (68 RCNY 7-08).")
nd("NYC:RCNY 68 9-08", "HRA's calculation of the HOME TBRA payment and household share; the settlement effect (which "
   "months HRA pays and what is returned) is decided by the rules proposed at 68 RCNY 9-06, 9-10 and 9-14.")
dec("NYC:RCNY 68 9-09", "new_rule",
    "HRA abates or ends HOME TBRA payments for an HQS failure the landlord does not cure; this decides whether HRA's "
    "share for those months is ever paid. Not stated.",
    proposed=[rule("NYC:RCNY68-9-09-HOME-TBRA-abatement", "68 RCNY 9-09(b)-(c)", "owner; manager", "who is paid",
                   "HRA found the HOME TBRA unit failed Housing Quality Standards and the landlord did not remedy the "
                   "failure within HRA's period, the landlord being responsible for it.",
                   "HRA abates its payments in full until the landlord remedies the failure, or terminates the Rental "
                   "Assistance Contract and stops paying; the household may move (68 RCNY 9-10). Abated months are "
                   "not paid by HRA, and nothing in the program makes the household liable for HRA's abated payment, "
                   "so the move-out account does not charge it to the tenant. If the household caused the failure "
                   "and does not remedy it, HRA ends the household's participation instead, and the lease governs "
                   "the household's liability. A landlord not responsible for the failure is outside the abatement.",
                   R68 + "9-09.txt", q(R68 + "9-09.txt", "HRA shall either abate HRA HOME TBRA rental assistance payments in their entirety",
                                       "This provision does not apply if the landlord is not responsible for the HQS failure."),
                   "major", "5.8", determinacy="MIXED", judgment_terms=["landlord responsible for the HQS failure"],
                   dependencies=["NYC:RCNY68-9-06-HOME-TBRA-payments"])])
dec("NYC:RCNY 68 9-10", "new_rule",
    "HOME TBRA payments stop the month after the household moves and the landlord keeps the move-out month's payment; "
    "this fixes HRA's share on the final account. Not stated.",
    proposed=[rule("NYC:RCNY68-9-10(e)-HOME-TBRA-moveout-month", "68 RCNY 9-10(e)", "owner; manager", "who is paid",
                   "A household receiving HRA HOME TBRA moves out of the assisted NYC unit.",
                   "HRA's payments for the unit stop as of the month after the month the household moves; the landlord "
                   "keeps HRA's payment for the move-out month. Any HRA payment for a later month is an overpayment "
                   "returned to HRA (NYC:RCNY68-9-14-HOME-TBRA-charges). A mutual termination that frees the household "
                   "to move requires the landlord to sign a release of the lease and the Rental Assistance Contract "
                   "(9-10(a)(3)).",
                   R68 + "9-10.txt", q(R68 + "9-10.txt", "If a household moves from an assisted unit",
                                       "during which the household moves from such unit."),
                   "critical", "5.8", dependencies=["NYC:RCNY68-9-06-HOME-TBRA-payments", "NYC:RCNY68-9-14-HOME-TBRA-charges"])])
commit()
