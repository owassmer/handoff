import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *

R = "register/texts/NYC_RCNY_T68/"
st("NYC:RCNY 68 10-09", ["NYC:RCNY68-10-14(e)", "NYC:RCNY68-10-14(h)"],
   "HRA may stop CityFHEPS payments when the household leaves the unit; the landlord's duties to notify HRA and "
   "return payments for months the household did not live there are stated. Income recalculation and program "
   "termination change no settlement step.")
nd("NYC:RCNY 68 10-12", "Duties the CityFHEPS household owes HRA (information, direct payment, paying its share, "
   "reporting arrears and a move); the landlord's limits on what it may demand are stated at NYC:RCNY68-10-14(a).")
nd("NYC:RCNY 68 7-07", "LINC VI program rules; the whole chapter expired and was repealed on 2024-12-31 "
   "(68 RCNY 7-08), so it decides nothing for a current settlement.")
dec("NYC:RCNY 68 9-06", "new_rule",
    "HRA HOME TBRA (tenant-based assistance in a private unit) pays the landlord only during the lease and while the "
    "household lives there; this decides whose share of the final months' rent is owed. Not stated.",
    proposed=[rule("NYC:RCNY68-9-06-HOME-TBRA-payments", "68 RCNY 9-06(c)(3)-(6)", "owner; manager", "who is paid",
                   "The departing household received HRA HOME TBRA rental assistance under a Rental Assistance "
                   "Contract between HRA and the landlord for an NYC unit.",
                   "HRA's payments are owed to the landlord only during the lease term and while the household resides "
                   "in the unit; the contract ends when the lease ends. When the landlord terminates the lease the "
                   "payments end, but while an eviction is pending and the household still lives there HRA keeps "
                   "paying until the landlord obtains a judgment or other process to evict, the household moves or "
                   "is evicted, or the contract term ends. The landlord may not terminate or refuse to renew the lease "
                   "except as 24 CFR 92.253(c) allows. So on the final account no HRA share is due for any period "
                   "after the household left, and any HRA payment received for such a period is returned to HRA "
                   "(NYC:RCNY68-9-14-HOME-TBRA-charges).",
                   R + "9-06.txt", q(R + "9-06.txt", "HRA HOME TBRA rental assistance payments shall be paid to the landlord",
                                     "while the household is residing in the assisted unit."),
                   "critical", "0.6; 5.7", dependencies=["NYC:RCNY68-9-14-HOME-TBRA-charges"])])
dec("NYC:RCNY 68 9-14", "new_rule",
    "Limits what a landlord of an HRA HOME TBRA household may demand (lease rent and fees only; customary fees with "
    "HRA approval) and requires return of overpayments after a move or eviction. Not stated.",
    proposed=[rule("NYC:RCNY68-9-14-HOME-TBRA-charges", "68 RCNY 9-14(i)-(k)", "owner; manager; Handoff; collector",
                   "prohibition + duty",
                   "The departing household received HRA HOME TBRA rental assistance for an NYC unit.",
                   "The landlord may not demand, request or receive any amount above the rent or fees stipulated in the "
                   "lease, whatever the change in household composition; fees customarily charged in rental housing "
                   "under 24 CFR 92.214(b)(3) are allowed only with HRA's prior approval. A landlord that does so is "
                   "barred from HRA rental assistance programs after notice and a chance to object in writing, and may "
                   "be barred from other city programs. When the household moves or is evicted, the landlord returns "
                   "any HRA overpayment to HRA (except as 68 RCNY 9-10 provides for moves); the overpayment is a "
                   "payable to HRA on the final account, not a credit to the tenant. On the sole member's death, "
                   "assistance ends and is not transferred. Deductions for rent and damage the tenant owes remain "
                   "governed by GOL 7-108.",
                   R + "9-14.txt", q(R + "9-14.txt", "A landlord who signs a lease with a household participating in HRA HOME TBRA is prohibited",
                                     "regardless of any changes in household composition,"),
                   "critical", "5.8", dependencies=["NY:GOL-7-108(1-a)(b)-refundable"],
                   construction=[{"source_file": R + "9-14.txt",
                                  "quote": q(R + "9-14.txt", "If a program participant moves or is evicted from an assisted unit",
                                             "except as otherwise provided in 68 RCNY § 9-10.")}],
                   reasoning="Subdivision (i) sets the charge ceiling and its sanction; (j) the overpayment return; "
                             "(k) ends assistance on the sole member's death. HOME TBRA is tenant-based assistance in a "
                             "private unit, the same class as CityFHEPS and SOTA, so it is inside the aperture.")])
commit()
