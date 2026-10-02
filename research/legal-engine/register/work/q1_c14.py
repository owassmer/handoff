import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s, r in [
  ("NY:ABP 1317", "Security deposits held by title insurers in real property transfers; not a tenant deposit."),
  ("NY:ABP 1319", "Unclaimed virtual currency held by virtual-currency businesses; not a landlord holder."),
  ("NY:ABP 1401", "The Comptroller's public record of abandoned property; no landlord act turns on it."),
  ("NY:ABP 1402", "The Comptroller's online publication of abandoned property; no landlord act turns on it."),
  ("NY:ABP 1406", "How an owner claims abandoned property from the Comptroller; after reporting, the landlord is discharged (proposed NY:ABP-1404-holder-discharged) and the tenant's claim runs against the State."),
  ("NY:ABP 1407", "Payment of allowed claims by the Comptroller; no landlord act turns on it."),
  ("NY:ABP 1410", "Newspapers for notices the chapter requires; a 1315 refund carries no holder publication."),
  ("NY:ABP 1418", "The Comptroller's recovery of New York residents' property held by other states; no landlord act turns on it."),
  ("NY:DCL 253", "Citation to a judicial settlement of a committee's or conservator's accounts; court procedure after the claim is presented under DCL 250."),
  ("NY:DCL 254", "Service of that citation; court procedure."),
  ("NY:DCL 255", "Court powers on the citation's return; court procedure."),
  ("NY:GCN 11", "Who may take an acknowledgment required by law; no instrument in the settlement must be acknowledged beyond what the rules already state."),
  ("NY:GCN 12", "Before whom an affidavit may be sworn; it fixes no settlement amount, date or payee, and the affidavits the chain requires are stated with their own rules."),
]:
    rows.append(D(s, "no_decision", r))

S = "NY:DCL 250"
rows.append(D(S, "new_rule",
  "Where the former tenant's property is managed by a committee (incompetent person) or conservator, the landlord's "
  "balance is collected by presenting a verified claim to it by the advertised date; no rule states this incapacity "
  "branch.",
  proposed=[R("NY:DCL-250-committee-claim", S, "DCL 250", "landlord", "must",
  "The former tenant has a court-appointed committee of the property (incompetent person) or conservator of the "
  "property (conservatee), and the court authorized it to advertise for creditors.",
  "The landlord presents its claim for the balance to the committee or conservator, with vouchers, verified, and "
  "naming a post-office address for service, on or before the day the advertisement sets (at least 30 days after the "
  "last of four weekly publications; the committee mails the notice to creditors known from the tenant's papers at "
  "least 30 days before). A claim not so presented may go unpaid from the estate (NY:DCL-252-good-faith-payment). A "
  "suit against a person with a committee or conservator also proceeds against that representative "
  "(NY:CPLR-1203-1015-5208-parties).",
  Q(S, "authorize him to advertise for creditors and other persons interested in such estate, to present to him their claims with the vouchers thereof, duly verified",
    "on or before a day to be specified in such advertisement"),
  "major", "Step 8.10 before suing: capacity", dependencies=["NY:CPLR-1203-1015-5208-parties"])]))

S = "NY:DCL 252"
rows.append(D(S, "new_rule",
  "Consequence of not presenting the claim under DCL 250: the committee's court-directed good-faith payments discharge "
  "it and its sureties as to creditors who did not present.",
  proposed=[R("NY:DCL-252-good-faith-payment", S, "DCL 252", "landlord", "must",
  "The former tenant's committee or conservator advertised for claims (NY:DCL-250-committee-claim) and, under the "
  "court's direction, pays the claims presented and proved (pro rata if the estate is insufficient).",
  "Payment made in good faith under the court's direction relieves the committee or conservator and its sureties of "
  "liability to creditors who failed to present their claims as the article provides; the landlord that did not "
  "present its balance cannot recover it from them for funds so paid.",
  Q(S, "and such payment, when so made in good faith and under direction of such court",
    "to creditors who have failed to present their claims as in this article provided."),
  "major", "Step 8.10 before suing: capacity", dependencies=["NY:DCL-250-committee-claim"])]))

S = "NY:DCL 251"
rows.append(D(S, "new_rule",
  "A committee or conservator may compromise the former tenant's own claims (the deposit claim) only with court "
  "authority; this decides whether a settlement with it binds.",
  proposed=[R("NY:DCL-251-committee-compromise", S, "DCL 251", "landlord", "must",
  "The landlord settles the former tenant's deposit claim, or buys or compounds it, with the tenant's committee or "
  "conservator.",
  "The committee or conservator may sell, compromise or compound a claim belonging to the estate only with the "
  "authority of the court having jurisdiction over the estate, on the terms the court directs; the landlord obtains "
  "or sees that authority before relying on the compromise. A good-faith sale made without prior authority is valid "
  "subject to the court's approval.",
  Q(S, "authorize the committee or conservator to sell, compromise or compound any claim or debt belonging to the estate"),
  "minor", "Step 8.1b payments and settlements", dependencies=["NY:DCL-250-committee-claim"])]))

save(rows)
