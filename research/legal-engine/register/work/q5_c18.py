import sys
sys.path.insert(0, "register/work")
from q5_lib import add, nd, rule

add("US:FRBP 9010", "new_rule",
    "Decides what Handoff or the manager may do for the landlord in a tenant's bankruptcy without a lawyer (file the proof of claim, vote) and what needs a Form 411 power of attorney or an attorney.",
    proposed=[rule("US:FRBP 9010", "US:FRBP9010-agent-authority", "FRBP 9010(a), (c)", "Handoff; manager; landlord", "may",
                   "The landlord (owner) acts in a former tenant's bankruptcy through its manager or Handoff (per configuration) rather than personally.",
                   "An authorized agent may perform any act that is not the practice of law for the landlord; executing and filing the proof of claim (Form 410, signed as authorized agent, US:FRBP3001-claim-contents) and accepting or rejecting a plan need no power of attorney. Any other representation of the landlord as creditor by an agent (for example attending the 341 meeting or acting on the claim for other purposes) must be evidenced by a power of attorney substantially conforming to Form 411, acknowledged before an officer authorized to take acknowledgments. Motions, complaints and objections (stay relief, dischargeability, discharge objections, plan objections) are acts in the practice of law: an individual owner may file them personally, but an entity owner acts only through an attorney admitted in the court, and neither Handoff nor the manager may file them for it.",
                   "major", "8.8", "(a) In General. A debtor, creditor, equity security holder", "a person authorized to administer oaths under the state law where the oath is administered.",
                   dependencies=[])])

add("US:FRBP 9037", "new_rule",
    "A proof of claim or other filing the landlord or Handoff makes (with the lease and ledger attached) must redact the tenant's SSN, birth date and account numbers.",
    proposed=[rule("US:FRBP 9037", "US:FRBP9037-redaction", "FRBP 9037(a), (e)", "landlord; Handoff; manager", "shall",
                   "The landlord, its manager or Handoff files a proof of claim or other paper in a bankruptcy case with attachments (lease, rental application, ledger, move-out statement) containing personal identifiers.",
                   "Unless the court orders otherwise, the filing may show only the last four digits of a social-security or taxpayer-identification number, the year of birth, a minor's initials, and the last four digits of a financial-account number (including the tenant's bank or card number and, where it is a financial-account number, the landlord's account number for the tenant). An unredacted copy may also be filed under seal.",
                   "minor", "8.8", "(a) Redacted Filings.", "(4) the last four digits of the financial-account number.",
                   dependencies=[])])

L = "General litigation procedure in bankruptcy cases"
for sid, why in [
    ("US:FRBP 9001", "Definitions for the Rules; the terms the proposed rules use carry their ordinary Code meanings and none changes a chain outcome."),
    ("US:FRBP 9002", "Meaning of Civil Rules terms in bankruptcy; procedural."),
    ("US:FRBP 9003", "Bars ex parte contacts with the judge; procedural."),
    ("US:FRBP 9004", "Form of papers and captions; procedural."),
    ("US:FRBP 9005", "Harmless error; procedural."),
    ("US:FRBP 9005.1", "Notice of a constitutional challenge to a statute; procedural."),
    ("US:FRBP 9007", "The court's authority to regulate notices; the landlord's notice and address rights are proposed at 342 (US:11USC342-effective-notice)."),
    ("US:FRBP 9008", "Service or notice by publication; procedural."),
    ("US:FRBP 9009", "Use of Official Forms; the landlord's use of Form 410 is stated in US:FRBP3001-claim-contents."),
    ("US:FRBP 9011", L + ": signatures on papers and sanctions for unfounded filings; the fee exposure it creates for a failed abuse motion is carried in US:11USC707(b)-abuse-motion, and it adds no deadline, amount or payee."),
    ("US:FRBP 9012", "Oaths and affirmations; procedural."),
    ("US:FRBP 9013", L + ": form and service of motions; the stay-relief procedure is proposed at FRBP 4001."),
    ("US:FRBP 9014", L + ": contested-matter procedure used by the stay-relief motion proposed at FRBP 4001 (US:FRBP4001-stay-relief-procedure)."),
    ("US:FRBP 9015", L + ": jury trials."),
    ("US:FRBP 9016", L + ": subpoenas."),
    ("US:FRBP 9017", L + ": evidence."),
    ("US:FRBP 9018", L + ": protection of confidential or scandalous matter."),
    ("US:FRBP 9019", L + ": court approval of the trustee's compromises; a settlement the trustee makes with the landlord (for example of a preference claim) is approved on the trustee's motion, with no separate duty on the landlord."),
    ("US:FRBP 9020", L + ": procedure for contempt motions; the discharge-injunction contempt consequence is proposed at 105 (US:11USC105-discharge-contempt)."),
    ("US:FRBP 9021", L + ": when a judgment or order becomes effective (on docket entry)."),
    ("US:FRBP 9022", L + ": notice of judgments and orders."),
    ("US:FRBP 9023", L + ": motions for a new trial or to amend a judgment within 14 days."),
    ("US:FRBP 9024", L + ": relief from a judgment or order; the discharge-revocation time it cross-references is carried in US:11USC727-ch7-discharge."),
    ("US:FRBP 9025", L + ": proceedings against sureties."),
    ("US:FRBP 9026", L + ": objecting to rulings."),
    ("US:FRBP 9027", L + ": removal of claims to the bankruptcy court; a landlord's state-court suit against a debtor is already stayed (US:11USC362(a)(6))."),
    ("US:FRBP 9028", L + ": judge's disability."),
    ("US:FRBP 9029", "Local rules and judges' directives; procedural."),
    ("US:FRBP 9031", "Masters not authorized; procedural."),
    ("US:FRBP 9032", "Effect of amendments to the Civil Rules; procedural."),
    ("US:FRBP 9033", L + ": review of proposed findings in non-core proceedings."),
    ("US:FRBP 9034", "Copies of certain papers to the U.S. trustee; the landlord's plan-objection copy duty is carried in US:FRBP3015-plan-objection."),
    ("US:FRBP 9035", "Application of the Rules in Alabama and North Carolina bankruptcy-administrator districts; outside New York."),
    ("US:FRBP 9036", "Electronic notice and service channels; where court notices go and when notice is effective for the landlord is proposed at 342 (US:11USC342-effective-notice)."),
    ("US:FRBP 9038", "Bankruptcy Rules emergency declared by the Judicial Conference; no chain decision absent a declaration."),
]:
    nd(sid, why)
