import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
S = "NY:GOL 5-1504"
rows.append(D(S, "new_rule",
  "Governs the landlord's handling of a statutory short-form POA presented to receive the refund or settle: it must "
  "honor or reject in writing within ten business days, may not refuse without reasonable cause, and is held harmless "
  "when it relies in good faith.",
  proposed=[R("NY:GOL-5-1504-accept-poa", S, "GOL 5-1504(1)-(5), (7)", "landlord, manager, Handoff", "must",
  "An agent presents the landlord (or its manager or Handoff) with an original or attorney-certified copy of the "
  "former tenant's statutory short-form power of attorney properly executed under GOL 5-1501B (or the law in force "
  "when executed), to receive the statement or refund, dispute charges or settle.",
  "Within ten business days after presentation the landlord either honors it, rejects it in a writing stating the "
  "reasons sent to the principal and agent at the addresses on the power, or asks the agent for an acknowledged "
  "affidavit that the power is in full force; after a written response to a rejection it honors or finally rejects "
  "within seven business days, and honors within seven business days after a compliant affidavit. It may not refuse "
  "without reasonable cause (for example knowledge of the principal's death, incapacity under a non-durable power, "
  "fraud, a report to adult protective services, or notice of revocation); refusal only because the form is not the "
  "landlord's own, or because time has passed, is unreasonable, and a court in a GOL 5-1510 proceeding may award "
  "damages, fees and costs. Once reasonably accepted, the landlord is held harmless for transactions in reliance, and "
  "absent actual knowledge of incapacity, fraud or duress, or actual notice of revocation or termination, it incurs no "
  "liability for acting on it; the agent's affidavit is conclusive for the landlord. Where the refund falls due during "
  "the review, the 14-day statement still goes out on time and the refund is held in trust until the payee is settled "
  "(NY:GOL-7-103(1)-trust).",
  Q(S, "(a) Once reasonably accepted, if a third party conducts a transaction in reliance on a properly executed statutory short form power of attorney",
    "the third party shall be held harmless from liability for the transaction."),
  "major", "Step 6 refund payee", determinacy="MIXED",
  judgment_terms=["reasonable cause", "good faith", "actual knowledge", "reasonably accepted"],
  dependencies=["NY:GOL-5-1501B-poa-validity", "NY:GOL-7-103(1)-trust"],
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S, "Not later than the tenth business day after presentation of an original or attorney certified copy",
                  "such third party shall either (a) honor the statutory short form power of attorney, or")}],
  reasoning="Subdivision 3(a) fixes the ten-business-day response; subdivision 4(a) the hold-harmless.")]))

rows.append(D("NY:GOL 5-1513", "no_decision",
  "The statutory short-form POA text; what the form's grants authorize in the settlement, and its validity and "
  "acceptance, are proposed at GOL 5-1501B, 5-1502A, 5-1502H and 5-1504."))
save(rows)
