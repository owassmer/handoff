"""Apply root's October 2 operator-scope decisions; not a relevance classifier.

The named selections below are human-readable decisions, not keyword rules for
future sources. Backups are taken once. Running again produces the same result.
"""
from pathlib import Path
import copy
import json
import shutil

BASE = Path(__file__).resolve().parents[2]
ROOT = BASE.parents[1]
REVIEW = 'j1/reassessment/operator-scope.json'
BACKUP = BASE / 'j1/history/before-operator-scope'

def backup(path):
    relative = path.relative_to(ROOT)
    target = BACKUP / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not target.exists():
        shutil.copy2(path, target)

def write(path, value):
    backup(path)
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(text)
    temp.replace(path)

path = BASE / 'j1/register_updates.json'
backup(path)
doc = json.loads(path.read_text())
entries = {i['id']: i for i in doc['instruments']}
changes = []

def exclude(iid, names, reason):
    entry = entries[iid]
    # Recover the original selected objects on a repeat run, for a stable ledger.
    original = json.loads((BACKUP / path.relative_to(ROOT)).read_text())
    original = next(i for i in original['instruments'] if i['id'] == iid)
    selected = original['units_in_scope']
    targets = selected if names is None else [u for u in selected if u['unit'] in names]
    if names is not None:
        assert {u['unit'] for u in targets} == set(names), (iid, names)
    keys = {u['unit'] for u in targets}
    entry['units_in_scope'] = [u for u in entry['units_in_scope'] if u['unit'] not in keys]
    entry['units_out'] = [u for u in entry.get('units_out', []) if u['unit'] not in keys]
    for unit in targets:
        unit = copy.deepcopy(unit)
        unit['prior_selection_reason'] = unit.get('reason')
        unit['reason'] = reason
        unit['scope_review'] = REVIEW
        entry['units_out'].append(unit)
    changes.append({'instrument': iid, 'decision': 'exclude named units from this operating scope',
                    'units': sorted(keys), 'reason': reason,
                    'sources': sorted({u.get('toc_url') or entry['toc_source_url'] for u in targets})})
    entry['operator_scope_review'] = REVIEW

def select_names(iid, prefixes):
    original = json.loads((BACKUP / path.relative_to(ROOT)).read_text())
    original = next(i for i in original['instruments'] if i['id'] == iid)
    return [u['unit'] for u in original['units_in_scope']
            if any(u['unit'].startswith(p) for p in prefixes)]

# Whole instruments whose undertaking is different from multifamily turnover.
exclude('CA-OC:SHELTER-MODEL2027', None,
        'County shelter-operation contract: participant admission/exit, shelter belongings and care standards govern running the shelter. Handoff is undertaking apartment readiness and tenancy-account resolution, not shelter operation. Apartment assistance and survivor protections remain selected in their own authorities.')
exclude('CA:HCD-CALHOME', None,
        'CalHome funds homeownership assistance, counseling and owner rehabilitation. Administering that assistance or a homeownership development is a separate undertaking from managing institutional rental apartments. An ADU or manufactured home reference does not establish a multifamily turnover obligation. HOME rental assistance, rental-project restrictions and general repair law remain selected.')
exclude('CA:HCD-TAY-2025-26', None,
        'These county/provider award exhibits fund transitional-age-youth housing/navigation services. Handoff does not undertake county award administration or service delivery. A young tenant receiving assistance still has the ordinary tenancy, payment and protection sources; an actual apartment landlord agreement remains operating evidence.')

# Financial program administration is not made relevant merely by funding work.
exclude('CA:CCR4', [
    'Division 9.6 - California Debt and Investment Advisory Commission',
    'Division 12 - California Educational Facilities Authority',
    'Division 13 Article 1 - Procedures Relating to the Authority of Officers and Members',
    'Division 13 Article 2 - Manufacturing Sales and Use Tax Exclusion Program',
    'Division 13 Article 3 - Clean Energy Upgrade Financing Program',
    'Division 13 Article 4 - Pace Loss Reserve Program'],
    'Public debt administration, education-facility financing, manufacturing tax incentives and optional financing/lender reserves are separate undertakings. They do not establish how apartment work must be performed or how an outgoing tenancy is settled. Preserve selected tax-credit/bond rental restrictions, repair standards, payment law and obligations of an existing property agreement.')
exclude('CA:FIN', ['division 2 / chapter 6',
    'DIVISION 1.10. HIGHER-PRICED MORTGAGE LOANS [4995 - 4995.6]',
    'DIVISION 9.5. Commercial Financing Disclosures [22800 - 22807]',
    'DIVISION 20. CALIFORNIA RESIDENTIAL MORTGAGE LENDING ACT [50000 - 50706]'],
    'Savings-association investment operations and originating/disclosing mortgage or commercial financing are outside the undertaken account and repair workflows. Keep payment processing, escrow, consumer payment-plan rules, collection licensing, existing financing restrictions and tenant protections at foreclosure.')
exclude('US:12USC5481', [
    'part Part F— Transfer of Functions and Personnel; Transitional Provisions',
    'part Part G— Regulatory Improvements'],
    'Agency personnel/function transfer and interagency regulatory administration do not govern the operator account. Retain definitions, substantive financial protections, state-law interaction and enforcement affecting payment plans, collection or payments.')

# Educational institutions and clinical facilities are not inferred from tenants.
exclude('CA:CCR5', None,
    'Selected Title 5 units regulate educational institutions, student-aid administration and institution-billed education/housing refunds. A student renting an institutional multifamily apartment does not make its manager an educational institution. Preserve ordinary tenancy, fair housing and applicable recorded/project restrictions; this scope does not undertake campus institutional-housing administration.')
exclude('CA:EDC', select_names('CA:EDC', [
    'title 1 / division 1 / part 7', 'title 1 / division 1 / part 8',
    'title 1 / division 1 / part 10.5', 'title 2 / division 3 / part 21',
    'title 2 / division 3 / part 23', 'title 2 / division 3 / part 24',
    'title 2 / division 4 / part 32', 'title 3 / division 14 / part 66',
    'title 3 / division 14 / part 68', 'title 3 / division 14 / part 69',
    'title 3 / division 14 / part 70', 'title 3 / division 14 / part 72']),
    'School district administration, instructional facilities, school finance and education bonds concern operating/funding schools, not apartment turnover. Retain mixed higher-education housing/public-owner provisions where rental-project obligations may occur; student status alone does not import school administration.')
exclude('CA:HSC', [
    'division 1.5', 'division 2 / chapter 2.1', 'division 2 / chapter 2.3',
    'division 2 / chapter 2.35', 'division 2 / chapter 2.4',
    'division 2 / chapter 2.45', 'division 2 / chapter 2.5',
    'division 2 / chapter 3.15', 'division 2 / chapter 3.9',
    'division 2 / chapter 3.93', 'division 2 / chapter 3.95',
    'division 2 / chapter 4.9', 'division 2 / chapter 8.5',
    'division 2 / chapter 8.6', 'division 2.1'],
    'This unit concerns institutional treatment/care, nursing or hospice business, its admissions or clinical resident protections, or children’s camps. Those are separate operations from rental multifamily. Keep mixed community-care and family-day-care housing provisions because they can limit an apartment landlord’s conduct, and keep disability, capacity, habitability and safety law independently.')
exclude('CA:CCR22', [
    'Division 5 - Licensing and Certification of Health Facilities, Home Health Agencies, Clinics, and Referral Agencies',
    'Division 7 - Health Planning and Facility Construction',
    'Final package - Transitional Housing Placement Program final licensing revision'],
    'Health-facility planning/licensing and licensed THPP service-provider operation are outside rental multifamily turnover. Tenant disability, youth status or receipt of services does not confer those provider roles. Mixed community-care/day-care units remain for landlord-facing use protections; building, environmental-health and rental-assistance requirements remain selected.')
exclude('CA:ACT:202520260AB2562', None,
    'The enacted amendments impose licensed/certified drug-treatment program policies and suicide-prevention plans (HSC11832.8,11834.26). They concern treatment-service operation, not ordinary apartment management; tenant disability and other housing protections remain selected.')

# Concrete separate businesses; retain the mixed parent where it has dependencies.
exclude('CA:BPC', ['division 8 / chapter 21.5'],
    'Operating a money exchange house is a distinct financial business. Apartment receipts, refunds, transfers, installment agreements and collection remain covered by selected payments/consumer/financial authorities.')
exclude('US:15USC-ch41', ['subchapter SUBCHAPTER II–A— CREDIT REPAIR ORGANIZATIONS'],
    'Selling credit-repair services is outside account resolution. Correcting the operator’s furnished information and handling resident credit-report disputes remain governed by the retained FCRA/Regulation V sources; this exclusion does not remove those duties.')

# Remove a duplicate whole-parent acquisition, retaining every selected child.
exclude('US:11USC', ['chapter CHAPTER 15— ANCILLARY AND OTHER CROSS-BORDER CASES'],
    'Redundant parent selector: all five Chapter15 subchapters remain selected. This changes acquisition duplication, not bankruptcy coverage. Farmer/fisherman and cross-border debtor protections remain because they can change an apartment creditor’s actions.')

# Current court source identified in existing review, now expressed as a selection.
exclude('CA-OC:DEPARTMENT-PROCEDURES', ['C21-policies'],
    'Servino-captioned publication is retained as recovered material but is not established as Arthur’s current departmental policy. No rescission is asserted. Select the currently published Arthur general instructions separately; do not treat case-specific tentative rulings as general rules.')
c21 = entries['CA-OC:DEPARTMENT-PROCEDURES']
url = 'https://www.occourts.org/sites/default/files/oc/default/tentative-rulings/carthurrulings.pdf'
c21['units_in_scope'] = [u for u in c21['units_in_scope'] if u['unit'] != 'C21-Arthur-general-instructions']
c21['units_in_scope'].append({
    'unit': 'C21-Arthur-general-instructions',
    'heading': 'C21 Arthur general law-and-motion instructions, publication September18,2026',
    'toc_url': url, 'source_unit_kind': 'document', 'locator': 'PDF page1 only',
    'reason': 'Current official departmental publication supplies general submission, appearance and reporter instructions. Following case-specific rulings are not general procedural rules.',
    'section_list': [{'number': 'C21-Arthur-general-instructions',
                      'heading': 'General departmental instructions, page1', 'ref': url}],
    'acquisition_note': 'J2 must extract page1 and enumerate its general instructions; downloading the carrier PDF does not select the individual cases on later pages.',
    'scope_review': REVIEW})
changes.append({'instrument': c21['id'], 'decision': 'select current general instructions',
                'units': ['C21-Arthur-general-instructions'], 'sources': [url],
                'reason': 'Current court publication names Arthur; page1 is general procedure, following pages are individual cases.'})

# These are deliberate keeps, not omissions from a pruning exercise.
keeps = {
    'US:11USC': 'Bankruptcy limits action against residents and counterparties. Do not discard Chapter12/15 or specialized debtor branches on rarity; code selects them by the actual proceeding. Duplicate Chapter15 parent alone removed.',
    'US:24CFR960': 'Retain conditional public-housing occupancy rules: a multifamily manager can manage covered apartments. This does not undertake PHA funding/admissions administration as a new product.',
    'US:24CFR966': 'Retain covered apartment lease/grievance requirements. Public housing and public-agency administration are not interchangeable categories.',
    'CA-OC:HMIS-POLICIES': 'Retain conditional project-program data obligations where an actual participating rental project/operator must use HMIS; do not infer that every recipient’s private landlord is a participating agency.',
    'CA-OC:CES-POLICY': 'Retain participation/coordination conditions that can govern covered rental-project vacancy or transfer handling. Operating the county referral system is outside the undertaking.',
    'CA-OC:SCAQMD': 'Retain mixed air-quality units at J1. Building equipment, asbestos, coatings, permits, offsets and contractors can connect these rules to actual repair obligations. No rule is applied merely because the source is selected; specialized facility/credit-market operations are outside semantic compilation unless needed by a selected repair requirement.',
    'CA:CCR3': 'Retain mixed pesticide/plant/animal units and applicable amendments: grounds work, treatment, quarantine and neighboring application restrictions can govern apartment work. Do not equate agricultural terminology with no apartment consequence.',
    'CA:CCR9': 'Retain mixed mental-health program source for housing-use, resident rights and authority dependencies; clinical treatment and program service delivery are outside the undertaking.',
    'CA:CCR12': 'Retain mixed military/veterans source for housing and occupant-status dependencies; running a veterans institution is not inferred.',
    'CA:DTSC-PERMIT-CORRECTIONS-2026': 'Retain the identified package as a conditional disposal-provider dependency in the hazardous-waste source family. It imposes no ordinary dwelling facility permit by inference. No further administrative-history retrieval is required.',
    'CA:SWRCB-DW-OP-FEES-2026': 'Retain identified conditional operator-certification source for a property water-system/provider role when legally triggered; not a municipal water-customer charge and not a new research chase.',
    'CA:HCD-HOME': 'Rental-project operating restrictions, repair standards and assistance-account conditions remain within institutional multifamily even without proof Holland participates in HOME.',
    'CA:CTCAC-COMPLIANCE': 'Restricted apartments fit the profile; LIHTC participation remains a distinct condition, not inferred from a BMR designation.',
    'CA-HB:HOME-TBRA-PROVIDER-AGREEMENTS': 'Keep landlord-facing refund recipient, assistance credits/end dates, mandatory tenancy forms and inspections. Provider grant administration is not an independent supported workflow.',
    'CA-HB:MHTBRA-GUIDELINES-2022': 'Keep identified local assistance source for correct program boundaries and resident-payment/inspection conditions; it is not evidence that Holland operates mobilehome parks. No expansion into homeowner loan administration is authorized.',
    'CA-HB:REHAB-HQS-POLICIES-2022': 'Keep the identified incorporated MHTBRA inspection-correction dependency, not a standalone homeowner lending workflow.',
    'CA-OC:RAINSMART-2026': 'Participant terms can govern eligible landscape work and reimbursement. Keep that actual work agreement branch; do not expand into administering the county grant program.'
}
for iid, reason in keeps.items():
    entries[iid]['operator_scope_decision'] = {'review': REVIEW, 'decision': 'keep conditionally', 'reason': reason}
    if iid in ['US:24CFR960', 'US:24CFR966']:
        for unit in entries[iid]['units_in_scope']:
            unit['reason'] = reason
write(path, doc)

included = ('Institutional rental multifamily unit readiness and departing-tenancy account resolution: investigation, '
            'access, physical work and provider commitments, lawful charges, rent/utilities/deposits/credits, payments, '
            'disputes, recovery, settlement and completion. Include restricted apartments, resident assistance and '
            'actual rental-project operating obligations. Derive US/state/local sources from these functions, '
            'not Breakwater facts or an exact Holland property roster.')
excluded = ('Separate educational, clinical-care or shelter operations; originating optional financing; independent '
            'government/program administration; unrelated businesses. Preserve any provisions in those source '
            'families that actually constrain apartment work, payments, resident rights or the operator’s legal '
            'authority. Rarity, tenant identity and absence from the demo do not justify exclusion. Mixed units '
            'remain selected when needed to preserve such dependencies.')
for code in ['US', 'CA', 'CA-OC', 'CA-HB']:
    p = BASE / 'jurisdictions' / code / 'profile.json'
    profile = json.loads(p.read_text())
    profile['aperture']['included'] = included
    profile['aperture']['exclusions'] = excluded
    profile['aperture']['scope_review'] = REVIEW
    profile['aperture']['regime_units_note'] = 'Unit-specific applicability is applied later; a customer roster is not a prerequisite for jurisdiction-first research.'
    profile['aperture']['time'] = 'Current law as of October2,2026 and identified adopted future changes. Retain older instruments only for a live transition, incorporation or continuing obligation; no historical-corpus reconstruction.'
    profile.setdefault('walk', {})['scope_exclude'] = excluded
    profile.setdefault('jev', {})['scope'] = 'institutional rental multifamily physical work and tenancy-account resolution'
    profile['jev']['chain_description'] = included
    write(p, profile)

ledger = {
    'date': '2026-10-02', 'owner': 'root; no worker delegation',
    'deliverable': 'Applied operator-scope reconciliation across the J1 register families',
    'status': 'complete', 'scope': included, 'boundary': excluded,
    'basis': ['HANDOFF_CONTEXT.md', 'research/expansion/context/intent_notepad.md',
              'research/holland/portfolio.md', 'j1/reassessment/reconciled-next-steps.json',
              'j1/lanes/j1-selection-final-review.md', 'j1/lanes/j1-selection-final-exclusions.json',
              'j1/lanes/acquisition/boundary-scope-review-delta.json'],
    'changes': changes, 'deliberate_keeps': keeps,
    'review_depth': 'Whole register-family reconciliation against the operating purpose, with named unit corrections and targeted source review. Not a claim to have interpreted every selected provision; mixed units deliberately remain for full-text work.',
    'consumer_effect': 'Removed units no longer occur in units_in_scope. units_out preserves their source routes and reasons. Whole-document carriers and retained mixed parents still require J2 internal enumeration and section-level selection; narrative exclusions are not executable descendant filters.',
    'stage': 'J1 remains open for the existing four consequential current-source selections. This scope deliverable does not claim J1 completion.',
    'inventory': [{'id': i['id'], 'selected_units': len(i['units_in_scope']),
                   'decision': 'revised' if i['id'] in {c['instrument'] for c in changes} else 'existing selections retained under corrected operating boundary'}
                  for i in doc['instruments']]
}
write(BASE / REVIEW, ledger)

completion_path = BASE / 'j1/completion.json'
completion = json.loads(completion_path.read_text())
completion['as_of'] = '2026-10-02'
completion['scope'] = included
completion['current_review'] = REVIEW
completion['scope_review'] = {'source': REVIEW, 'status': 'applied',
                              'meaning': 'Root reconciled the operating scope across source families and changed actual selections. Four current-source questions remain; J1 completion not asserted.'}
completion['downstream_limits'] = [s for s in completion['downstream_limits'] if not s.startswith('Shelter model,')]
completion['downstream_limits'].append('RainSmart participant work agreement is retained conditionally; shelter operation model is excluded from the supported undertaking. Whole carrier capture and internal enumeration remain J2.')
write(completion_path, completion)
work_path = BASE / 'j1/WORK.json'
work = json.loads(work_path.read_text())
work['coordination'] = 'Root performs reconciliation and remaining research directly. Workers stopped at user instruction; do not restart.'
work['scope'] = included
work['execution'] = 'Operator scope integrated; remaining current-source selection decisions'
work['current_scope_review'] = completion['scope_review']
work['delegation']['round_status'] = 'Stopped by explicit user instruction; historical assignments only.'
work['integrated'] = [s for s in work['integrated'] if not s.startswith('Operator-scope reconciliation:')]
work['integrated'].append('Operator-scope reconciliation: actual financial, institutional, statutory and court selections corrected; assisted/restricted multifamily and conditional work dependencies preserved. See ' + REVIEW)
write(work_path, work)

context = ROOT / 'HANDOFF_CONTEXT.md'
text = context.read_text()
marker = '\nOctober 2 operator-scope reconciliation (root-owned):'
text = text.split(marker)[0].rstrip()
text += marker + ' ' + included + ' ' + excluded + ' Applied decisions are in research/legal-engine/' + REVIEW + '. These supersede earlier universal-residential inclusion language. Workers are stopped at Owen’s instruction.\n'
write(context, text)

for code in ['US', 'CA', 'CA-OC', 'CA-HB']:
    backup(BASE / 'jurisdictions' / code / 'instruments.json')
backup(BASE / 'j1/COUNTS.json')
print(f'Applied {len(changes)} named selection decisions; preserved {len(doc["instruments"])} instrument records.')
