import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s, r in [
  ("NY:9 NYCRR 540.7", "Electronic recording of instruments by county recording officers; no settlement instrument is recorded."),
  ("NY:ABP 102", "Declaration of policy for the Abandoned Property Law; it states no operative rule."),
  ("NY:ABP 103", "Definitions of banking organizations, utility services, gift certificates and similar terms; none governs the ABP 1315 deposit-refund rules the settlement relies on."),
  ("NY:ABP 1313", "Refunds held by sales finance companies and premium finance agencies; not a landlord holder."),
  ("NY:ABP 1318", "Support payments held by support collection units; not a landlord holder."),
  ("NY:ABP 1414", "The Comptroller's rulemaking power; the holder reporting guidance relied on is stated (NY:OSC-MS11-refunds-due)."),
  ("NY:ABP 1417", "The Comptroller's reciprocal agreements with other states; no landlord act turns on it."),
  ("NY:GCN 10", "Meaning of 'acknowledgment' for instruments other than deeds; no settlement instrument must be acknowledged beyond what the stated rules require."),
  ("NY:GCN 15", "Definition of 'chattels'; the rules on belongings left behind do not turn on it."),
  ("NY:GCN 22", "Gendered words in statutes refer to persons of any gender; it confirms, and changes nothing in, rules applied without regard to sex."),
  ("NY:GCN 23", "Meaning of 'heretofore' and 'hereafter'; each stated rule carries its own effective dates."),
  ("NY:GCN 25-B", "Definition of 'injury to property'; the settlement's damage claims arise under the lease, not a statute using this term."),
  ("NY:GCN 26-A", "Definition of 'judgment creditor'; enforcement limits are stated (NY:CPLR-5205-5231-enforcement-limits)."),
  ("NY:GCN 32", "References to municipal officers; not a settlement matter."),
  ("NY:GCN 34", "Meaning of 'now' in statutes; no stated rule turns on it."),
  ("NY:GCN 37", "'Person' includes a corporation; each stated rule names its actors, and none turns on this default."),
  ("NY:GCN 39", "Definition of 'personal property'; the belongings rules do not turn on it."),
  ("NY:GCN 42", "Acts of a county register satisfy county-clerk requirements; not a settlement matter."),
  ("NY:GCN 43", "Form of seals of courts and corporations; seals have no effect on any settlement instrument."),
  ("NY:GCN 44", "Form of a private seal; seals have no effect (GCN 44-A)."),
  ("NY:GCN 48", "Present tense includes the future; a construction rule no stated rule turns on."),
  ("NY:GCN 49", "'Territory' includes the District of Columbia; not a settlement matter."),
  ("NY:GCN 60", "What counts as a newspaper for required publication; no settlement notice is published."),
]:
    rows.append(D(s, "no_decision", r))

rows.append(D("NY:GCN 56", "stated",
  "'Writing' includes every legible representation of letters on a material substance; the written-statement and "
  "electronic-record rules already fix what counts as a writing in the settlement.",
  ["NY:ADJ-provide-written-dispatch", "NY:CASE-Bogom-Shanon-written", "NY:STT-305(3)"]))

S = "NY:GCN 46"
rows.append(D(S, "partial",
  "Several stated rules require a writing 'subscribed' or 'signed' by a party (early termination, guaranty, "
  "modification, release); GCN 46 decides what counts as that signature.",
  ["NY:GOL-5-703-15-301-early-termination", "NY:GOL-5-701(a)(2)-guaranty", "NY:STT-307"], [R(
  "NY:GCN-46-signature", S, "GCN 46", "landlord; former tenant", "may",
  "A settlement step depends on a writing signed by a party or its agent (an agreed early end date, a guaranty, a "
  "release, a modification or discharge, a written acknowledgment of the balance, a settlement offer).",
  "Any memorandum, mark or sign, written, printed, stamped, photographed, engraved or otherwise placed on the writing "
  "with intent to execute or authenticate it is a signature, including a typed name or printed letterhead adopted "
  "with that intent; an electronic signature has the same force (NY:STT-307). Whether a mark was placed with that "
  "intent is a finding on the facts; an email signature block or typed name the sender adopted for that message is "
  "sufficient when the intent to authenticate that writing is shown.",
  Q(S, "The term signature includes any memorandum, mark or sign", "with intent to execute or authenticate such instrument or writing."),
  "major", "Step 3.3 leaving early; Step 8.1b payments and settlements", determinacy="MIXED",
  judgment_terms=["intent to execute or authenticate"],
  dependencies=["NY:GOL-5-703-15-301-early-termination", "NY:STT-307"])]))
save(rows)
