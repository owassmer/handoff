import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *
R6 = "register/texts/NYC_RCNY_T6/"
for s, why in (("1-01", "fingerprinting of licence applicants"), ("1-01.1", "truthful licence applications"),
               ("1-03", "posting the DCWP licence sign"), ("1-07", "liability insurance notices"),
               ("1-08", "licensee change of address"), ("1-09", "late licence renewal"),
               ("1-10", "lost or mutilated licences"), ("1-21", "licensee conduct toward DCWP staff")):
    nd(f"NYC:RCNY 6 {s}", f"Licence administration ({why}); no settlement or collection step with a former tenant.")
nd("NYC:RCNY 6 1-12", "Repealed (City Record 2/24/2020).")
nd("NYC:RCNY 6 1-19", "Evidentiary presumption in DCWP proceedings that unlicensed activity continued daily; it "
   "affects only the count of penalty days, whose amount is in the proposed NYC:RCNY6-6-62-collection-penalties.")
nd("NYC:RCNY 6 5-01", "Definitions for DCWP's general consumer protection rules (consumer includes a co-obligor or "
   "surety); the debt-collection rules carry their own definitions in 5-76, which the stated rules apply.")
dec("NYC:RCNY 6 5-24", "new_rule",
    "A landlord, manager or collector that takes a former tenant's balance by credit card is a seller of consumer "
    "services accepting cards and must disclose card limitations and follow GBL 518. Not stated.",
    proposed=[rule("NYC:RCNY6-5-24-card-payments", "6 RCNY 5-24(a)-(b) (with 5-01 'consumer')",
                   "owner; manager; Handoff; collector", "duty",
                   "The landlord, manager, Handoff or a collector accepts credit cards for rent or a former tenant's "
                   "balance (a lease is a consumer service; the tenant and any surety are consumers).",
                   "It must conspicuously disclose every limitation it imposes on card use (minimums, surcharges, "
                   "excluded card types), at or near every entrance to its business premises and in any advertising "
                   "or payment page that says cards are accepted, and must comply with GBL 518 (including its "
                   "surcharge rules). DCWP penalty $150 first, $250 second, $350 third (6 RCNY 6-47).",
                   R6 + "5-24.txt", q(R6 + "5-24.txt", "A seller who accepts credit cards must conspicuously disclose",
                                      "New York General Business Law § 518."),
                   "minor", "8.1b", dependencies=["NY:RPL-235-g"])])
dec("NYC:RCNY 6 6-11", "new_rule", "Penalty for a licensee omitting its licence number from letters, emails and "
    "receipts to a former tenant.",
    proposed=[rule("NYC:RCNY6-6-11-licence-number-penalty", "6 RCNY 6-11 (6 RCNY 1-05 line)", "DCWP licensee",
                   "consequence",
                   "A DCWP-licensed collector's letter, email, receipt or website to a former tenant omits its licence "
                   "number (NYC:RCNY6-1-05-licence-number).",
                   "$175 first violation (curable on first offense where marked), $300 second, $500 third and later; "
                   "each item charged is a separate violation.",
                   R6 + "6-11.txt", q(R6 + "6-11.txt", "Failure to contain license number in advertisements and other printed and electronic matter", None),
                   "minor", "8.6", dependencies=["NYC:RCNY6-1-05-licence-number"])])
for s, why in (("6-24", "repealed sales penalty schedule"), ("6-30", "process servers"),
               ("6-35", "repealed electronic stores schedule"), ("6-48", "truth-in-pricing for retail goods"),
               ("6-50", "advertising representations"), ("6-63", "air conditioning systems"),
               ("6-64", "carpet emissions"), ("6-70", "polystyrene items"), ("6-73", "hotel service disruptions"),
               ("6-87", "ticket price advertising")):
    nd(f"NYC:RCNY 6 {s}", f"DCWP penalty schedule for {why}; no chain party or settlement step.")
commit()
