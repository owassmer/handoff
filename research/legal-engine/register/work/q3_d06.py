import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *

A = "register/texts/NYC_ADC/"
nd("NYC:ADC 27-2112", "The city is not liable for costs in HMC proceedings; no chain party is affected.")
nd("NYC:ADC 27-2114", "Public-nuisance declarations and stockholder liability for injury in a nuisance multiple "
   "dwelling; a tort route against owners that changes no settlement step.")
nd("NYC:ADC 27-2129", "HPD's statement of account to the owner for its repair costs and the owner's objection "
   "window; the tenant-side rule (those costs are the owner's debt, never a move-out charge) is stated at "
   "NYC:HMC-27-2128-owner-debt.")
st("NYC:ADC 27-2134", ["NYC:HMC-27-2135(c)-receiver-rents"],
   "On the order to show cause the court appoints HPD receiver of the rents; the receiver's collection of accrued "
   "and accruing rents is stated.")
nd("NYC:ADC 27-2138", "Receivership does not relieve the owner of prior liabilities, taxes or mortgages; no "
   "settlement step turns on it.")
st("NYC:ADC 27-2139", ["NY:ADJ-vacate-order-rent"],
   "HPD's power to vacate a dwelling unfit for habitation is the trigger of the vacate-order rent rule, which cites "
   "it.")
st("NYC:ADC 27-2140", ["NY:ADJ-vacate-order-rent"],
   "The order requires every occupant to leave within 24 hours to 10 days; the rent consequence is stated. The "
   "civil penalty on class B and SRO owners and lien provisions change no market-rate settlement step.")
nd("NYC:ADC 27-2141", "Service of a vacate order on owner and occupants; the rent consequence runs from the ouster, "
   "stated at NY:ADJ-vacate-order-rent.")
st("NYC:ADC 27-2142", ["NY:ADJ-vacate-order-rent"],
   "No one may occupy a unit under a vacate order; the vacate-order rent rule rests on this section.")
nd("NYC:ADC 27-2143", "HPD may sue the owner for its expenses; the owner-debt rule is stated at "
   "NYC:HMC-27-2128-owner-debt.")
nd("NYC:ADC 27-2146", "Limits challenges to HPD's repair-expense lien; owner and lienor matter only.")
dec("NYC:ADC 27-2148", "partial",
    "The receiver-collects-rents rule covers receivers under 27-2130 ff. and MDL 309 only; a lien-based HPD receiver "
    "of rents under 27-2148 is a separate route (any premises with $5,000 or more of HPD repair liens, houses "
    "included) and also displaces the owner as collector.",
    ["NYC:HMC-27-2135(c)-receiver-rents"],
    [rule("NYC:HMC-27-2148-lien-receiver-rents", "Admin. Code 27-2148(a)-(d)", "owner; manager; Handoff; collector",
          "who is paid",
          "HPD repair-expense liens on the premises total $5,000 or more and HPD has issued an order, on 30 days' "
          "notice to the owner, mortgagees and lienors, appointing the HPD commissioner receiver of the rents and "
          "profits; the receivership is in effect when the departing tenant's rent balance is collected. Applies to "
          "any premises carrying such liens (the section is not limited to multiple dwellings).",
          "The receiver has the powers of a receiver in a mortgage foreclosure and collects the rents and profits "
          "until the liens and commissions are fully paid; the owner, its manager, Handoff and any collector may not "
          "collect rent from the tenant or the former tenant for the period the receivership covers, and rent the "
          "tenant pays the receiver counts as paid. The owner may avoid the order within the notice period by paying "
          "the liens or contracting with HPD for their payment. When the receivership ends, the owner receives an "
          "accounting and any excess. The security deposit is not rent and profits; its return stays governed by "
          "GOL 7-103 and 7-108 and by NY:GOL-7-108(2)(e) for a receiver that holds it.",
          A + "27-2148.txt", q(A + "27-2148.txt", "the department may issue an order appointing the commissioner",
                               "receiver of the rent and profits of the premises."),
          "critical", "0.5",
          dependencies=["NYC:HMC-27-2135(c)-receiver-rents", "NY:CPLR-6401-foreclosure-receiver",
                        "NY:GOL-7-108(2)(e)"],
          amends="NYC:HMC-27-2135(c)-receiver-rents")])
nd("NYC:ADC 27-@0-0-0-60027", "Integrated pest management work practices for correcting pest violations; the cost "
   "allocation at move-out is decided by the owner-duty and turnover rules, not by the work standard.")
commit()
