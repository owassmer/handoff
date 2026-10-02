"""Gold negatives for calibration: sections from IN-scope units whose headings are plainly outside the chain, each
checked by hand (heading read against the chain; text read where the heading alone was not conclusive) with a
one-line reason. Writes register/calibration_negatives.json after verifying every id exists, is not a gold
positive, and is short enough to be sent to Jev (<= 12,000 characters)."""
import json
import pathlib

REG = pathlib.Path(__file__).resolve().parent.parent
N = {}


def add(prefix, items):
    for sid, reason in items:
        N[f"{prefix} {sid}"] = reason


add("NY:GBL", [
    ("390", "Sale of substitute motor oils; no tenancy or collection subject."),
    ("390-A", "Identification marks on optical discs (manufacturing)."),
    ("390-C", "Admission of minors to certain facilities."),
    ("390-D", "Trafficking-help notices at truck stops."),
    ("391", "Marking of retreaded tires."),
    ("391-A", "Adulteration and labeling of liquid fuels and oils."),
    ("391-B", "Sale of dangerous clothing articles."),
    ("391-C", "Sale of bicycles."),
    ("391-D", "Sale of matchbooks."),
    ("391-E", "Promotion of camps by organizations."),
    ("391-F", "Promotion of private schools by organizations."),
    ("391-H", "Sale of lubricating oils."),
    ("391-I", "Sale of urea-formaldehyde foam insulation."),
    ("391-J", "Sale of fire extinguishers."),
    ("391-M", "Manufacture and sale of in-line skates."),
    ("391-N", "Sale of reptiles."),
    ("391-P", "Rental of previously worn clothing."),
    ("391-S", "Sale of novelty lighters."),
    ("391-T", "Sale of small animals."),
    ("391-X", "Labeling of hair relaxers."),
    ("392", "Sale of second-hand watches."),
    ("392-A", "Sale of new computers (disclosures)."),
    ("392-C", "Obliteration of marks of origin on goods."),
    ("392-D", "False marks as to manufacture."),
    ("392-F", "Taximeters."),
    ("392-G", "Sale of ultraviolet tanning devices."),
    ("392-J", "Sale of sparkling devices (fireworks)."),
    ("393", "Sale of lime by weight."),
    ("393-A", "Sale of non-fire-rated wood paneling."),
    ("394", "Replacement of lost stock certificates."),
    ("396-C", "Advertising of dentures and bridges."),
    ("396-DD", "Renting of horses."),
    ("396-E", "Marking of linen articles."),
    ("396-F", "Sale of blind-made products."),
    ("396-H", "Fraudulent sale of patriotic flowers and flags."),
    ("396-J", "Master keys for motor vehicles."),
    ("396-KK", "Sale of video game consoles."),
    ("396-L", "Shopping carts."),
    ("396-V", "Public blood pressure machines."),
    ("396-W", "Soliciting transportation passengers at terminals."),
])
add("NY:22 NYCRR", [
    ("202.15", "Videotape recording of depositions in Supreme Court."),
    ("202.16-a", "Automatic orders in matrimonial actions."),
    ("202.16-b", "Written applications in contested matrimonial actions."),
    ("202.17", "Exchange of medical reports in personal injury actions."),
    ("202.18", "Court-appointed experts in matrimonial actions."),
    ("202.50", "Proposed judgments in matrimonial actions."),
    ("202.51", "Proof required in dissolution proceedings."),
    ("202.54", "Guardians for patients in facilities (Mental Hygiene)."),
    ("202.56", "Medical malpractice actions."),
    ("202.59", "Tax assessment review outside New York City."),
    ("202.60", "Tax assessment review proceedings in New York City."),
    ("202.61", "Appraisal reports in eminent domain proceedings."),
    ("202.62", "Payment of eminent domain awards."),
    ("202.64", "Election Law proceedings."),
    ("202.66", "Workers' compensation settlements."),
    ("202.68", "Custody of an Indian child."),
])
add("NYC:RCNY 6", [
    ("6-12", "Tobacco retail dealer penalty schedule."),
    ("6-12.1", "Electronic cigarette retail dealer penalty schedule."),
    ("6-13", "Amusement arcade penalty schedule."),
    ("6-16", "Sidewalk stand penalty schedule."),
    ("6-17", "Sightseeing guide penalty schedule."),
    ("6-18", "Pedicab penalty schedule."),
    ("6-20", "Pawnbroker penalty schedule."),
    ("6-22", "Laundry penalty schedule."),
    ("6-23", "Locksmith penalty schedule."),
    ("6-25", "Garage and parking lot penalty schedule."),
    ("6-26", "Bingo licensing penalty schedule."),
    ("6-28", "Sightseeing bus and horse-drawn cab penalty schedule."),
    ("6-33", "Games of chance penalty schedule."),
    ("6-36", "Towing penalty schedule."),
    ("6-37", "Vehicle booting penalty schedule."),
    ("6-38", "Weights and measures penalty schedule."),
    ("6-40", "Etching acid penalty schedule."),
    ("6-44", "Prepackaged meat penalty schedule."),
    ("6-55", "Motorized scooter penalty schedule."),
    ("6-64", "Carpet VOC emissions penalty schedule."),
])
add("US:26 USC", [
    ("6042", "Information returns on dividends."),
    ("6043A", "Information returns on taxable mergers and acquisitions."),
    ("6044", "Information returns on patronage dividends of cooperatives."),
    ("6045A", "Broker statements on transfers of covered securities."),
    ("6045B", "Issuer returns on actions affecting securities basis."),
    ("6046", "Returns on organization of foreign corporations."),
    ("6046A", "Returns on interests in foreign partnerships."),
    ("6047", "Information on certain trusts and annuity plans."),
    ("6050A", "Reporting by fishing boat operators."),
    ("6050B", "Returns on unemployment compensation."),
    ("6050F", "Returns on social security benefits."),
    ("6050G", "Returns on railroad retirement benefits."),
    ("6050L", "Returns on donated property."),
    ("6050R", "Returns on purchases of fish."),
    ("6050S", "Returns on higher education tuition."),
])
add("US:26 CFR", [
    ("1.6041-2", "Information returns on payments to employees (wages)."),
    ("1.6041-9", "Coordination with widely held fixed investment trust reporting."),
    ("1.166-7", "Worthless bonds issued by an individual (bond investors)."),
])
add("US:11 USC", [
    ("322", "Qualification and bonding of bankruptcy trustees."),
    ("324", "Removal of a trustee or examiner."),
    ("1110", "Aircraft equipment and vessels in chapter 11."),
    ("1113", "Rejection of collective bargaining agreements."),
    ("1114", "Retiree insurance benefits in chapter 11 (long text but plainly outside)."),
    ("1145", "Exemption of plan securities from securities laws."),
    ("1146", "Special tax provisions for chapter 11 plans."),
    ("1188", "Status conference in small business chapter 11 cases."),
    ("1195", "Employment of professionals in small business cases."),
])
add("US:FRBP", [
    ("9003", "Ex parte contacts with the court prohibited."),
    ("9005.1", "Notice of constitutional challenges to statutes."),
    ("9015", "Jury trials in bankruptcy."),
    ("9028", "Judge's disability."),
    ("9029", "Adoption of local bankruptcy rules."),
    ("9031", "Masters not authorized."),
    ("9032", "Effect of amendments to the civil rules."),
    ("9035", "Application of the rules in Alabama and North Carolina districts."),
])
add("US:15 USC", [
    ("1693i", "Issuance of debit cards by financial institutions."),
    ("1693l–1", "Gift cards and general-use prepaid cards."),
    ("1693p", "Reports to Congress on electronic fund transfers."),
    ("1693o", "Administrative enforcement of EFTA by banking agencies."),
    ("1693h", "Liability of financial institutions to account holders."),
    ("1681f", "Consumer reporting agency disclosures to governmental agencies."),
    ("1681k", "Public record information in employment screening."),
    ("1681r", "Unauthorized disclosures by agency officers or employees."),
    ("1681s–1", "Reporting of overdue child support obligations."),
    ("1681v", "Disclosures to government for counterterrorism."),
    ("1681x", "Corporate circumvention by consumer reporting agencies."),
])
add("US:42 USC", [
    ("3601", "Declaration of national fair housing policy (no operative duty)."),
    ("3608a", "HUD collection of fair housing data."),
    ("3609", "HUD education, conciliation and reports."),
    ("3618", "Authorization of appropriations."),
    ("3619", "Separability clause."),
])
add("NY:SSL", [
    ("131-AA", "Monthly statistical reports by social services districts."),
    ("131-AAA", "Availability of adverse childhood experience services."),
    ("131-D", "Substance abuse rehabilitation services for recipients."),
    ("131-E", "Family planning services."),
    ("131-G", "Authority of districts to accept gifts."),
    ("131-H", "Authority to operate family homes for adults."),
    ("131-L", "Exclusion of Agent Orange benefits from income."),
    ("131-P", "Group health insurance benefits of recipients."),
    ("131-Q", "Electronic payment file transfer pilot project."),
    ("131-X", "Reverse mortgage loans and eligibility."),
    ("142-A", "Federal Economic Opportunity Act grants."),
    ("142-B", "Federal manpower training act payments."),
    ("147", "Misuse of food stamps."),
    ("152-C", "Menstrual products for recipients."),
])
add("NY:EPTL", [
    ("11-1.2", "Tax elections by personal representatives."),
    ("11-1.9", "Deposit of estate securities in a clearing corporation."),
    ("11-1.10", "Employment of a broker-dealer as custodian."),
    ("11-1.11", "Amending trusts for tax purposes."),
    ("11-2.3-A", "Judicial control of a trustee's power to adjust."),
])
add("NY:MHL", [
    ("81.27", "Issuance of a commission to a guardian."),
    ("81.28", "Compensation of guardians."),
    ("81.39", "Guardian education requirements."),
    ("81.40", "Court evaluator education requirements."),
    ("81.41", "Court examiner education requirements."),
])
add("NY:CPLR", [
    ("4502", "Spousal privilege."),
    ("4504", "Physician privilege."),
    ("4505", "Clergy privilege."),
    ("4507", "Psychologist privilege."),
    ("4508", "Social worker privilege."),
    ("4509", "Library records privilege."),
    ("4516", "Proof of age of a child."),
    ("4519-A", "Evidence of possession of opioid antagonists."),
    ("4522", "Ancient maps and surveys of real property."),
    ("4526", "Marriage certificates as evidence."),
    ("4528", "Weather reports as evidence."),
    ("4529", "USDA inspection certificates as evidence."),
])
add("NY:Judiciary Law", [
    ("460", "Examination and admission of attorneys."),
    ("460-B", "Special arrangements for bar examination applicants."),
    ("461", "Compensation of the state board of law examiners."),
    ("462", "Annual account of the board of law examiners."),
    ("463", "Times and places of bar examinations."),
    ("464", "Certification of successful bar candidates."),
    ("465", "Bar examination and credential review fees."),
    ("469", "Continuance where an attorney is a legislator."),
    ("471", "Attorney practicing before a partner who is a judge."),
    ("473", "Court officers prohibited from practicing law."),
    ("474-A", "Contingent fees in medical malpractice claims."),
    ("499", "Lawyer assistance committees."),
])
add("US:12 CFR", [
    ("Appendix_C_to_Part_1022", "Model opt-out forms for affiliate marketing."),
    ("Appendix_D_to_Part_1022", "Model forms for prescreened firm offers of credit."),
    ("Appendix_H_to_Part_1022", "Model risk-based pricing and credit score notices."),
])
add("US:50 USC", [
    ("3938", "Child custody protections for servicemembers."),
    ("3938a", "Annual notice of child custody protections."),
    ("4023", "Professional liability insurance protection."),
    ("4024", "Health insurance reinstatement."),
    ("4025a", "Portability of professional licenses."),
])

if __name__ == "__main__":
    secs = {json.loads(l)["section_id"]: json.loads(l) for l in (REG / "sections.jsonl").read_text().splitlines() if l.strip()}
    m = json.loads((REG / "match.json").read_text())["sections"]
    bad = [s for s in N if s not in secs]
    pos = [s for s in N if s in m and (m[s]["atom_ids"] or m[s]["gap_5a"])]
    longs = [s for s in N if s in secs and secs[s]["chars"] > 12000]
    if bad or pos:
        raise SystemExit(f"missing ids: {bad}\npositives: {pos}")
    neg = [{"section_id": s, "unit": secs[s]["unit"], "heading": secs[s]["heading"], "reason": r,
            "cited_by_universe": bool(m[s]["universe_4a"] or m[s]["universe_5a"])} for s, r in N.items() if s not in longs]
    (REG / "calibration_negatives.json").write_text(json.dumps({
        "method": "Hand-checked: heading read against the chain; section text read where the heading alone was not conclusive. "
                  "Drawn from in-scope units across 17 instruments; none is stated by a rule or cited in a 5A gap finding.",
        "count": len(neg), "excluded_as_long": longs, "negatives": neg}, indent=1))
    print(len(neg), "negatives;", len(longs), "excluded as LONG:", longs)
