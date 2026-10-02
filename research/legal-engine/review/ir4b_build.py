"""IR4B builder: writes review/independent_review_4b.json and the findings part of review/INDEPENDENT_REVIEW_4B.md
from one data set, so the two cannot diverge. Idempotent: rerunning rewrites both files identically.
The prose sections (summary, confirmed, test cases, method, earlier rounds) live in ir4b_text.py.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REV = ROOT / "review"
WALK = "review/NYC_MARKET_RATE.md"

F = []


def add(**k):
    F.append(k)


# ---------------------------------------------------------------- critical
add(id="R4B-01", kind="missing-exception", severity="critical",
    rule_ids=["US:11USC541-704-owner-chapter7", "US:11USC1107-1306-owner-reorganization", "NY:GOL-7-103(1)-trust"],
    step="0.5 (who is owed the rent: 'In every case the deposit stays the tenant's money')",
    finding=("Both owner-bankruptcy rules, and the walk, state without condition that the deposit stays outside the "
             "estate and that the trustee may not keep it for creditors. Section 541(d) excludes only property the "
             "debtor holds by bare legal title, and in bankruptcy a beneficiary of a GOL 7-103 trust must identify or "
             "trace the trust money; if the deposit was commingled and cannot be traced, the tenant is a general "
             "unsecured creditor and the trustee (or debtor in possession) owes no turnover of it. The rules omit the "
             "tracing condition, so they state who is paid wrongly for the commingled-deposit branch."),
    correct_rule=("When the owner is a debtor (chapter 7, 11 or 13), a deposit the tenant can identify or trace (a "
                  "separate deposit account, or a commingled account whose balance never fell below the deposit since "
                  "the mingling) is held in trust outside the estate and is refunded with the 14-day statement by "
                  "whoever holds it. A deposit that was commingled and cannot be traced is not recoverable as trust "
                  "property: the tenant's refund is a pre-petition unsecured claim against the owner's estate, "
                  "filed as a proof of claim, and the manager may not pay it from estate funds without the trustee's "
                  "or the court's authority."),
    evidence=[
        {"source_file": "sources/REVIEW4B_US_CASE_In_re_Trafalgar_Associates_1985_BankrSDNY.txt",
         "quote": "Unless the beneficiary can, and does, trace the trust res he will be relegated to the status of a general unsecured creditor."},
        {"source_file": "sources/REVIEW4B_US_CASE_In_re_Trafalgar_Associates_1985_BankrSDNY.txt",
         "quote": "Savoy and Alpha essentially argue that section 7-103 of the New York General Obligations Law imposes a statutory trust on their security deposits and advances, removing them from the realm of estate assets."},
        {"source_file": "sources/REVIEW1_US_11USC_541.txt",
         "quote": "only to the extent of the debtor's legal title to such property"},
        {"source_file": WALK, "quote": "In every case the deposit stays the tenant's money."},
    ])

add(id="R4B-02", kind="misstatement-in-walk", severity="critical",
    rule_ids=["NYC:RSL-26-504(a)", "NYC:RS-status"],
    step="0.1 (Not stabilized)",
    finding=("The walk defines a stabilized unit as one 'in a non-co-op, non-condo building of six or more units'. "
             "The statute excepts GBL 352-eeee conversions from the co-op/condo carve-out, and the Code keeps "
             "co-op and condo buildings converted after 1974-06-30 within stabilization as 352-eeee provides, so a "
             "non-purchasing tenant in a converted building stays stabilized. Read as written, the walk classifies "
             "that tenant as market-rate and routes the deposit to GOL 7-108 instead of 7-107. The rule text "
             "(NYC:RSL-26-504(a)) carries the exception; the walk drops it, and 0.1 lists no RSC 2520.11(l) branch."),
    correct_rule=("A unit in a building owned as a cooperative or condominium is excluded from stabilization only if "
                  "the building was so owned on or before 1974-06-30, or as GBL 352-eeee provides for later "
                  "conversions: a non-purchasing tenant in possession under a conversion plan remains stabilized, and "
                  "the co-op/condo status of the building does not by itself make that tenancy market-rate. Step 0 "
                  "must route such a unit to Review 2."),
    evidence=[
        {"source_file": "sources/NYC_ADC_26-504.txt",
         "quote": "except as provided in section three hundred fifty-two-eeee of the general business law"},
        {"source_file": "sources/NYC_RSC_Part2520_NYCRR.txt",
         "quote": "housing accommodations contained in buildings owned as cooperatives or condominiums on or before June 30, 1974; or thereafter, as provided in section 352-eeee of the General Business Law"},
        {"source_file": "sources/NYC_RSC_Part2524_NYCRR.txt",
         "quote": "tenants in a noneviction conversion plan pursuant to section 352-eeee of the General Business Law may not be evicted on this ground"},
        {"source_file": WALK, "quote": "A unit is rent-stabilized when it is in a non-co-op, non-condo building of six or more units"},
    ])

add(id="R4B-03", kind="misread-authority", severity="critical",
    rule_ids=["NY:ADJ-willful-standard", "NY:ADJ-provide-address-branches", "NY:CASE-Prando-willful", "NY:CASE-Karole-willful"],
    step="6.5 and 7.5 (willfulness; holding the statement for an address)",
    finding=("The walk and both rules state as law that, for a manager or experienced landlord, holding the statement "
             "until the tenant supplies an address 'is willful'. No cited decision so holds. The only appellate "
             "decision on a wait for a new address (Prando, App Term 2d Dept) holds that willfulness is a factual "
             "determination with credibility a factor and affirmed a finding that such a wait was innocent; Karole "
             "(Civil Court) found willfulness where a management company sent no statement at all and gave a "
             "pretextual reason. The statute makes punitive damages turn on a person 'found to have willfully "
             "violated' and caps them 'up to' twice the deposit. Converting a fact finding into a per se rule for "
             "managers overstates the damages exposure rule the authorities support; the rules' own text also says "
             "willfulness is 'a finding of fact on the whole record', so the walk contradicts the rule it cites."),
    correct_rule=("Punitive damages of up to twice the deposit require a finding, on the whole record, that the "
                  "violation was willful: knowing, intentional or deliberate, not negligent or inadvertent. An "
                  "experienced landlord or managing agent is charged with knowing that the 14-day rule has no "
                  "missing-address exception, so its deliberate decision to hold the statement pending an address "
                  "satisfies the knowledge element and is evidence of willfulness; whether willfulness is found, and "
                  "the amount up to twice the deposit, is for the trier of fact (Prando). Forfeiture of the deposit "
                  "follows the missed deadline regardless of intent."),
    evidence=[
        {"source_file": "sources/NY_CASE_Prando_v_Kelly_2021.txt",
         "quote": "Willfulness is a factual determination with credibility being one of the factors"},
        {"source_file": "sources/NY_CASE_Prando_v_Kelly_2021.txt",
         "quote": "Defendant Renee Kelly asserted that she had delayed returning plaintiff's security deposit because, among other things, she had not known his new address."},
        {"source_file": "sources/NY_GOL_7-108_nysenate.txt",
         "quote": "a person found to have willfully violated this subdivision shall be liable for punitive damages of up to twice the amount of the deposit or advance"},
        {"source_file": WALK, "quote": "Holding the statement because the new address is unknown is a deliberate failure and willful for a manager."},
        {"source_file": "stage-a/NY.json", "quote": "Willfulness is a finding of fact on the whole record"},
    ])

# ---------------------------------------------------------------- major
add(id="R4B-04", kind="misread-authority", severity="major",
    rule_ids=["NY:LLC-206-publication-not-bar"],
    step="8.10 (capacity)",
    finding=("The rule says a New York LLC's missing publication 'is not a ground to dismiss its claim'. The cited "
             "Appellate Term, First Department decision held only that the defect is not jurisdictional. LLC Law "
             "206(a) suspends the LLC's authority to carry on business after 120 days without filed proof of "
             "publication, and the Appellate Division, Second Department (binding on the Kings, Queens and Richmond "
             "courts, and on every trial court that has no contrary Appellate Division authority) holds that an LLC "
             "that has not complied is precluded from maintaining any action and affirmed dismissal. The suspension "
             "is annulled once proof of publication is filed, which is why later compliance cures it."),
    correct_rule=("A New York owner LLC that has not filed proof of publication within 120 days of formation cannot "
                  "maintain an action against a former tenant while its authority is suspended, and the action is "
                  "dismissed on motion if it has not cured (Small Step Day Care, 2d Dept). Filing the proof of "
                  "publication at any time annuls the suspension; the defect is not jurisdictional, can be cured "
                  "after commencement, and never affects the lease, the deposit statement or the LLC's defense of "
                  "the tenant's suit. Operator step: confirm publication was filed before suing."),
    evidence=[
        {"source_file": "sources/REVIEW4B_NY_CASE_SmallStep_v_BroadwayBushwick_2016_2dDept.txt",
         "quote": "Failure to comply with these requirements precludes a limited liability company from maintaining any action or special proceeding in New York"},
        {"source_file": "sources/REVIEW3_NY_LLC_206_nysenate.txt",
         "quote": "such suspension of such limited liability company's authority to carry on, conduct or transact business shall be annulled."},
        {"source_file": "sources/REVIEW3_NY_CASE_1700FirstAve_v_ParsonsNovak_2014_AppTerm1st.txt",
         "quote": "constitute a jurisdictional defect requiring dismissal"},
        {"source_file": "sources/REVIEW4B_NY_CASE_Shoreview_v_Fernandez_2025_CivCtQueens.txt",
         "quote": "such suspension of such limited liability company's authority to carry on, conduct or transact business *shall be annulled*"},
    ])

add(id="R4B-05", kind="missing-exception", severity="major",
    rule_ids=["NY:CCA-1809(1)", "NY:CCA-1801-A(b)", "NY:CCA-1803-A(b)"],
    step="8.10 (where to sue a small balance)",
    finding=("The walk sends every entity owner to the commercial claims part. CCA 1801-A(a) admits a commercial "
             "claim only if the claimant has its principal office in New York State and the defendant resides, has "
             "an office or is regularly employed in New York City. An owner entity with its principal office "
             "outside the State, or a former tenant who has moved out of the City, cannot use that part; the claim "
             "goes to the regular civil part (or the court where the tenant can be sued). The rules also state that "
             "an LLC is barred from small claims, which CCA 1809(1) does not say; the Appellate Term, First "
             "Department, has treated an LLC as a proper commercial claims claimant, which supports the walk's "
             "result but is not cited."),
    correct_rule=("An owner that is a corporation, partnership, association or LLC may not sue in the small claims "
                  "part (CCA 1809(1); an LLC is treated as a corporation/association, National Arbitration & "
                  "Mediation, App Term 1st Dept 2018). It may use the commercial claims part only if its principal "
                  "office is in New York State and the former tenant resides, has an office or is regularly employed "
                  "in New York City when the claim is filed; then the 1803-A demand letter and five-a-month "
                  "certification apply. Otherwise it sues in the regular part of the Civil Court (within its "
                  "monetary limit) or the court where the tenant can be sued."),
    evidence=[
        {"source_file": "sources/REVIEW1_NY_CCA_1801-A_nysenate.txt",
         "quote": "the claimant is a corporation, partnership or association, which has its principal office in the state of New York and provided that the defendant either resides, or has an office for the transaction of business or a regular employment, within the city of New York."},
        {"source_file": "sources/REVIEW1_NY_CCA_1809_nysenate.txt",
         "quote": "no partnership, or association and no assignee of any small claim shall institute an action or proceeding under this article"},
        {"source_file": "sources/REVIEW4B_NY_CASE_NationalArbitration_v_Schwartzberg_2018_AppTerm.txt",
         "quote": "the action was properly commenced in the Commercial Claims Part of the Civil Court by plaintiff, a limited liability company that had its principal office in the State of New York"},
        {"source_file": WALK, "quote": "It uses the commercial claims part, and because the lease with a natural person is a consumer"},
    ])

add(id="R4B-06", kind="missing-exception", severity="major",
    rule_ids=["NY:MDL-301(1)", "NY:MDL-302(1)(b)"],
    step="0.5 (certificate of occupancy)",
    finding=("The rules test whether the building 'had none' (no certificate of occupancy). MDL 301(4) lets the "
             "department issue a temporary certificate of compliance or occupancy, and a dwelling occupied under a "
             "temporary certificate in force is not occupied in violation of 301. Many post-2000 NYC buildings "
             "operate on temporary certificates; without this branch an operator reading the DOB record could bar "
             "rent that is recoverable. 301(1)(b)'s second branch (old-law tenements where apartments were combined, "
             "the legal number of families decreased and bulk not increased) is also omitted from the rule's list "
             "of exceptions."),
    correct_rule=("No certificate is needed for the MDL 301(1)(a)-(b) buildings, including an old-law tenement or "
                  "qualifying 1901-1909 class A building altered only by combining apartments so that the legal "
                  "number of families decreases without increasing bulk. A multiple dwelling occupied while a "
                  "permanent certificate, or a temporary certificate issued under 301(4), is in force for the "
                  "residential use is lawfully occupied, and MDL 302(1)(b) does not bar rent for that period."),
    evidence=[
        {"source_file": "sources/REVIEW2_NY_MDL_301_nysenate.txt",
         "quote": "The head of the department may, on the request of the owner or his certified agent, issue a temporary certificate of compliance or occupancy for a multiple dwelling or a section or a part thereof for a period of ninety days or less"},
        {"source_file": "sources/REVIEW2_NY_MDL_301_nysenate.txt",
         "quote": "(1) two or more apartments are combined creating larger residential units, and"},
        {"source_file": "stage-a/NY.json", "quote": "it needed a certificate of occupancy for that residential use and had none"},
    ])

# ---------------------------------------------------------------- minor
add(id="R4B-07", kind="missing-exception", severity="minor",
    rule_ids=["NY:MDL-325(2)"],
    step="0.5 (registration)",
    finding=("MDL 325(2) has a voluntary-payment clause: a resident who voluntarily paid rent while the owner was "
             "unregistered cannot recover it back (payment under a judgment is not voluntary). The rule omits it, "
             "although the parallel MDL 302-a rule carries the same clause."),
    correct_rule=("Rent a tenant paid voluntarily while the owner was unregistered stays paid; the tenant has no "
                  "claim to recover it, and it is not refunded or credited on the move-out account."),
    evidence=[
        {"source_file": "sources/REVIEW2_NY_MDL_325_nysenate.txt",
         "quote": "If a resident of an unregistered dwelling voluntarily pays rent or an installment of rent when he had a right to withhold the same under this subdivision, he shall not thereafter have any claim or cause of action to recover back the rent or installment of rent so paid."},
    ])

add(id="R4B-08", kind="contradiction", severity="minor",
    rule_ids=["NYC:ADC-27-2097-registration", "NYC:ADC-27-2107(b)-rent-stay", "NY:MDL-325(2)"],
    step="0.5, 1.6 and 8.10 (registration)",
    finding=("NYC:ADC-27-2097-registration names the discretionary stay as the settlement consequence of "
             "non-registration for every registrable dwelling, while NY:MDL-325(2) says the stay 'governs only a one- "
             "or two-family house' and NYC:ADC-27-2107(b)-rent-stay says 'For a multiple dwelling, NY:MDL-325(2) "
             "governs instead'. Section 27-2107(b) applies to every owner required to register, multiple dwellings "
             "included; for a multiple dwelling both apply and the stricter MDL 325(2) bar controls."),
    correct_rule=("For a multiple dwelling, MDL 325(2) bars recovery of rent until registration (and 27-2107(b) also "
                  "applies, adding the loss of possession for nonpayment during non-compliance); for a one- or "
                  "two-family house that must register, only the 27-2107(b) discretionary stay applies. The "
                  "27-2097 rule should point to both."),
    evidence=[
        {"source_file": "sources/REVIEW1_NYC_ADC_27-2107.txt",
         "quote": "An owner who is required to file a statement of registration under this article and who fails to file as required shall be denied the right to recover possession of the premises for nonpayment of rent during the period of noncompliance"},
        {"source_file": "stage-a/NY.json",
         "quote": "The city's discretionary stay (NYC:ADC-27-2107(b)-rent-stay) governs only a one- or two-family house that must register."},
    ])

add(id="R4B-09", kind="misstatement-in-walk", severity="minor",
    rule_ids=["NY:MDL-302-a(3)"],
    step="0.5 (rent-impairing violations)",
    finding=("The walk says no rent is recovered 'for that unit'. The statute deems a condition in a common part, or "
             "a part under the owner's control, to exist in every resident's premises, so a common-area violation "
             "bars rent for every unit. The rule states this; the walk drops it."),
    correct_rule=("A rent-impairing violation uncorrected six months after notice bars rent for the unit where the "
                  "condition exists, and for every unit in the building when the condition is in a common part or a "
                  "part under the owner's control."),
    evidence=[
        {"source_file": "sources/NY_MDL_302-A_nysenate.txt",
         "quote": "the violation shall be deemed to exist in the respective premises of each resident of the multiple dwelling."},
        {"source_file": WALK, "quote": "no rent is recovered for that unit while it remains uncorrected."},
    ])

add(id="R4B-10", kind="misstatement-in-walk", severity="minor",
    rule_ids=["NYC:SHIELD-5-77(b)(5)(i)(B)"],
    step="8.5 (SHIELD electronic contact)",
    finding=("The walk says 'Email or text only with consent'. The rule text allows electronic collection also where "
             "the consumer used that address or number to communicate with the collector about a debt within the "
             "past 60 days and has not opted out."),
    correct_rule=("From 2027-01-01 a collector may use a private email address, text number or other electronic "
                  "medium only with the consumer's revocable written consent for the debt, or (for the original "
                  "creditor) consent for the account given before collection procedures began and not revoked, or "
                  "where the consumer used that medium to communicate with it about a debt within the past 60 days "
                  "and has not opted out."),
    evidence=[
        {"source_file": "sources/NYC_DCWP_SHIELD_NOA_2026.txt",
         "quote": "debt collector about a debt within the past 60 days and the consumer has not since"},
        {"source_file": WALK, "quote": "Email or text only with consent"},
    ])

add(id="R4B-11", kind="misstatement-in-walk", severity="minor",
    rule_ids=["NY:ADJ-vacate-order-rent"],
    step="T-vacate",
    finding=("T-vacate apportions the March rent (owed for March 1-9, refunded or credited for March 10-31). The "
             "cited authority decides rent falling due after the eviction (Younger: the tenant resisted a month's "
             "rent on the ground that he was evicted before the day it fell due) and suspension of rent (Barash); "
             "neither states that an installment already due before the order is apportioned by days. The "
             "apportionment branch needs its own authority or should be stated as the tenant's damages for the "
             "eviction."),
    correct_rule=("No rent or use and occupancy falling due after the tenant had to leave under a vacate order caused "
                  "by the owner's default is recoverable (Younger). For the installment already due on 2026-03-01, "
                  "the rule must state, with authority, whether the post-order days are refunded as apportioned "
                  "rent or recovered by the tenant as damages for the eviction; the walk's day count is not "
                  "supported by the cited cases."),
    evidence=[
        {"source_file": "sources/SWEEP_NY_CASE_Younger_v_Campbell_1917_1stDept.txt",
         "quote": "The defendant resisted payment upon the ground that he was evicted before the day the rent would have become due under the lease."},
        {"source_file": WALK, "quote": "any rent paid for March 10-31 is refunded or credited"},
    ])

add(id="R4B-12", kind="misstatement-in-walk", severity="minor",
    rule_ids=["NYC:ADC-27-2107(b)-rent-stay", "NY:MDL-325(2)"],
    step="C10",
    finding=("C10 says the buyer 'must register as the new owner before it can recover rent' without a building "
             "type. That is the MDL 325(2) rule for a multiple dwelling; for a one- or two-family house the court "
             "may stay the rent claim in its discretion."),
    correct_rule=("A buyer of a multiple dwelling recovers no rent until it files its registration (MDL 325(1) "
                  "requires a successor to file within 30 days); a buyer of a registrable one- or two-family house "
                  "faces only the discretionary stay of 27-2107(b)."),
    evidence=[
        {"source_file": "sources/REVIEW1_NYC_ADC_27-2107.txt",
         "quote": "shall, in the discretion of the court, suffer a stay of proceedings to recover rents, during such period."},
        {"source_file": WALK, "quote": "The buyer must register as the new owner before it can recover rent."},
    ])

add(id="R4B-13", kind="misstatement-in-walk", severity="minor",
    rule_ids=["NY:CPLR-214-i-consumer-debt-S9760"],
    step="8.1",
    finding=("The walk says the Consumer Debt Uniformity Act 'awaits the Governor'. The Assembly record as of "
             "2026-09-29 shows the last action 'returned to senate' on 2026-06-03; the bill has not been delivered to "
             "the Governor, whose time to act runs only from delivery. The rule's own effective_from states this "
             "correctly."),
    correct_rule=("S9760/A10182-A passed both houses (2026-06-02, 2026-06-03) and has not been delivered to the "
                  "Governor; it takes effect on the 90th day after it becomes law."),
    evidence=[
        {"source_file": "sources/REVIEW4B_NY_A10182_status_2026-09-29.txt", "quote": "06/03/2026 returned to senate"},
        {"source_file": WALK, "quote": "passed both houses in June 2026 and awaits the Governor"},
    ])

add(id="R4B-14", kind="misstatement-in-walk", severity="minor",
    rule_ids=["NYC:RSL-26-504(a)", "NYC:RSC-2520.11(p)"],
    step="0.1",
    finding=("The walk's positive list of stabilization routes names J-51 and Article 18 but not RPTL 421-a, which "
             "makes a unit stabilized during its benefit period in any building size; 421-a appears only in the "
             "exclusion bullet for units that have left. C4 relies on 421-a as a route ('no J-51 or 421-a')."),
    correct_rule=("A unit receiving RPTL 421-a benefits is stabilized during the restriction period whatever the "
                  "building size, and leaves only as RSC 2520.11(p) provides."),
    evidence=[
        {"source_file": "sources/NYC_RSC_Part2520_NYCRR.txt",
         "quote": "originally made subject to regulation solely as a condition of receiving tax benefits pursuant to section 421-a of the Real Property Tax Law"},
        {"source_file": WALK, "quote": "or receives J-51 or Article 18 benefits (any building size)"},
    ])

add(id="R4B-15", kind="hedging", severity="minor",
    rule_ids=["NY:ADJ-fee-retention-commonlaw", "US:15USC1692g(b)", "NYC:ADC-20-489(a)", "NY:CASE-Toporek-forfeiture-scope",
              "NY:CASE-Pickens-provide", "NY:CASE-Mihalow-rent-arrears", "NY:CASE-Masseroli-separate-claim"],
    step="0.4, 8.3, 8.6 and rule instrument fields",
    finding=("Soft hedges and weight labels remain: the walk's 'In practice this case is rare today' and 'which in "
             "practice is the lease and the itemized statement'; NYC:ADC-20-489(a) 'is typically one'; instrument "
             "fields reading 'trial-level; persuasive only' and 'binding in the First Department; statewide absent "
             "contrary appellate authority'. The owner's ruling bars weight warnings and possibility language; each "
             "should state the rule or be removed."),
    correct_rule=("Delete 'in practice' and 'typically'; state verification content as the rule (the documents that "
                  "establish each charge: the lease terms and the itemized statement); drop weight labels from "
                  "instrument fields (the adjudicating rules already state which authority controls)."),
    evidence=[
        {"source_file": WALK, "quote": "In practice this case is rare today."},
        {"source_file": WALK, "quote": "which in practice is the lease and the itemized statement"},
        {"source_file": "stage-a/NYC.json", "quote": "is typically one"},
        {"source_file": "stage-a/NY.json", "quote": "trial-level; persuasive only"},
    ])

OUT = {"review": "Independent review 4B (correctness), NYC market-rate walk", "date": "2026-09-29",
       "findings": F, "confirmed": [], "rules_checked_count": 414}

if __name__ == "__main__":
    import ir4b_text  # noqa: E402  (same folder)
    OUT["confirmed"] = ir4b_text.CONFIRMED
    (REV / "independent_review_4b.json").write_text(json.dumps(OUT, indent=1, ensure_ascii=False) + "\n")
    md = ir4b_text.render(OUT)
    (REV / "INDEPENDENT_REVIEW_4B.md").write_text(md)
    print(len(F), "findings;", len(OUT["confirmed"]), "confirmed lines written")
