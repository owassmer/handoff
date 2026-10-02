"""Apply the owner's eight-topic scope review; preserve evidence and unrelated selections."""
from pathlib import Path
import copy
import json
import shutil

BASE = Path(__file__).resolve().parents[2]
REVIEW = 'j1/reassessment/workflow-scope-review.json'
BACKUP = BASE / 'j1/history/before-workflow-scope-integration'

def read(path):
    return json.loads((BASE / path).read_text())

def write(path, value):
    target = BASE / path
    backup = BACKUP / path
    if target.exists() and not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup)
    text = value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False) + '\n'
    target.write_text(text)

def append_unique(rows, value, key='unit'):
    if not any(x.get(key) == value.get(key) for x in rows):
        rows.append(value)

def exclude(instrument, unit, reason):
    unit = copy.deepcopy(unit)
    unit['prior_selection_reason'] = unit.get('prior_selection_reason', unit.get('reason'))
    unit['reason'] = reason
    unit['scope_review'] = REVIEW
    append_unique(instrument.setdefault('units_out', []), unit)

review = read(REVIEW)
items = {x['item']: x for x in review['items']}
water = items['Water fees']
water['remaining_j1'] = 'Establish the filed edition/status for selected repair-discharge fee section2200, including applicable (a)(4), (b)(4) construction and (b)(10) dewatering/maintenance branches. Exclude cannabis-cultivation section2200.7; retain the mixed section2200 for downstream provision review.'
water['register_change'] = 'Replace the broad Division3 selector with its child branches, split Chapter9 Article1 into explicit leaves excluding2200.7, and select only2200 within the mixed2026 amendment package.'
ids = dict(zip(['GoGreen','FPPC','Part 7','HOME 2025 Exhibit A','OEHHA','Water fees','Drinking-water correction','SBSD named resolutions'], ['CA:CCR4','CA:CCR2','CA:CCR24','CA-HB:HOME-TBRA-PROVIDER-AGREEMENTS','CA:CCR27','CA:CCR23','CA:CCR22','CA-HB:SBSD:FINAL-ACTION-EVIDENCE']))
data = read('j1/register_updates.json')
byid = {x['id']: x for x in data['instruments']}
for name, identity in ids.items():
    instrument = byid[identity]
    item = items[name]
    instrument['remaining_item_operating_connection'] = copy.deepcopy(item)
    if item['remaining_j1']:
        instrument['j1_unresolved_selection'] = {'item': name, 'reason': item['remaining_j1'], 'status': 'open', 'audit': REVIEW, 'next_action': 'Resolve the stated selection question online; no external messages.'}
    else:
        instrument.pop('j1_unresolved_selection', None)
        instrument['scope_exclusion_decision'] = {'item': name, 'reason': item['reason'], 'review': REVIEW, 'meaning': 'Outside the undertaken workflow; excluded action legal status has not been resolved.'}

ccr4 = byid['CA:CCR4']
new = []
for unit in ccr4['units_in_scope']:
    if unit['unit'].startswith('GoGreen'):
        exclude(ccr4, unit, items['GoGreen']['reason'])
    elif unit.get('toc_url', '').endswith('/title-4/division-13'):
        names = ['Procedures Relating to the Authority of Officers and Members','Manufacturing Sales and Use Tax Exclusion Program','Clean Energy Upgrade Financing Program','Pace Loss Reserve Program','GoGreen Home','Commercial Energy Efficiency Financing','GoGreen Affordable Multifamily']
        for n, name in enumerate(names, 1):
            child = copy.deepcopy(unit)
            child.update(unit=f'Division 13 Article {n} - {name}', heading=name, toc_url=unit['toc_url']+f'/article-{n}', scope_review=REVIEW)
            if n <= 4:
                child['reason'] = 'Preserved inherited selection while excluding Articles5–7; this bounded integration does not newly adjudicate unrelated financing selections.'
                new.append(child)
            else:
                exclude(ccr4, child, items['GoGreen']['reason'])
    else:
        new.append(unit)
ccr4['units_in_scope'] = new
for version in ccr4.get('version_records', []):
    archived = copy.deepcopy(version)
    archived['scope_review'] = REVIEW
    archived['compilation_required'] = False
    if archived not in ccr4.setdefault('excluded_version_records', []):
        ccr4['excluded_version_records'].append(archived)
ccr4['version_records'] = []

ccr2 = byid['CA:CCR2']
new = []
excluded_numbers = {'18360.1','18360.2','18360.3'}
for unit in ccr2['units_in_scope']:
    if unit['unit'].startswith('Version source FPPC-18360.'):
        exclude(ccr2, unit, items['FPPC']['reason'])
        continue
    if unit['unit'] == 'FPPC conflicts advice, complaints and remedies':
        for section in unit['section_list']:
            if section['number'] in excluded_numbers:
                exclude(ccr2, {'unit': 'FPPC section '+section['number'], 'section_list': [section], 'adapter': 'generic'}, items['FPPC']['reason'])
        unit['section_list'] = [s for s in unit['section_list'] if s['number'] not in excluded_numbers]
        unit['reason'] = 'Preserve inherited advice, complaint and remedy selections; exclude optional streamlined political-enforcement settlement sections18360.1–.3 under the reviewed workflow boundary.'
    if unit['unit'] == 'FPPC permit and covered-contract contribution restrictions':
        unit['reason'] = 'Disclosure, disqualification and cure requirements for actual covered nonministerial permit or contract proceedings needed for readiness work; section18438.2 excludes purely ministerial decisions.'
    new.append(unit)
ccr2['units_in_scope'] = new
retained = []
for version in ccr2.get('version_records', []):
    if version.get('action_id', '').startswith('FPPC-18360.'):
        archived = copy.deepcopy(version)
        archived.update(scope_review=REVIEW, compilation_required=False)
        append_unique(ccr2.setdefault('excluded_version_records', []), archived, 'action_id')
    else:
        retained.append(version)
ccr2['version_records'] = retained

ccr23 = byid['CA:CCR23']
new = []
for unit in ccr23['units_in_scope']:
    if unit.get('toc_url', '').endswith('/title-23/division-3'):
        chapters = '1 1.5 2 2.5 2.7 2.8 3 3.5 4 4.5 4.6 5 6 7 8 9.1 9.2 10 11 12 13 14 15 16 17 18 19 20 20.1 21 22 23 24 25 26 27 28 29 30'.split()
        suffixes = ['chapter-'+n for n in chapters] + ['chapter-9/article-'+n for n in ['2','3','5','6']]
        for suffix in suffixes:
            child = copy.deepcopy(unit)
            child.update(unit='Division 3 / '+suffix, heading='Division 3 / '+suffix, toc_url=unit['toc_url']+'/'+suffix, scope_review=REVIEW)
            child['reason'] = 'Preserved inherited branch while excluding Chapter9 Article1 section2200.7; unrelated scope is not newly adjudicated.'
            new.append(child)
        child = copy.deepcopy(unit)
        child.update(unit='Division 3 Chapter 9 Article 1 - selected fee sections', heading='Selected fee sections excluding cannabis cultivation', toc_url=unit['toc_url']+'/chapter-9/article-1', scope_review=REVIEW)
        child['section_list'] = [{'number': n, 'heading': 'Section '+n, 'ref': 'https://www.law.cornell.edu/regulations/california/23-CCR-'+n} for n in ['2200','2200.1','2200.2','2200.3','2200.4','2200.5','2200.6','2200.8','2200.9','2201']]
        child['reason'] = 'Keep mixed2200 including applicable construction and dewatering branches; preserve other inherited leaves. Exclude cannabis-cultivation2200.7.'
        new.append(child)
        exclude(ccr23, {'unit': 'Section 2200.7 - Annual Fee Schedule for Cannabis Cultivation', 'toc_url': 'https://www.law.cornell.edu/regulations/california/23-CCR-2200.7'}, 'Cannabis cultivation fees govern a separate business activity, not the undertaken readiness or outgoing-account work.')
    else:
        if 'SWRCB-2026-0038' in json.dumps(unit):
            unit['internal_units_in_scope'] = ['2200']
            unit['internal_units_out'] = [{'unit': '2200.7', 'reason': 'Cannabis cultivation fee schedule outside undertaken workflows.'}]
            unit['reason'] = 'Mixed amendment carrier retained to establish selected section2200 edition/status; cannabis section2200.7 is excluded from compilation.'
        new.append(unit)
ccr23['units_in_scope'] = new
for version in ccr23['version_records']:
    if version.get('id') == 'SWRCB-2026-0038':
        version.update(selected_sections=['2200'], excluded_sections=['2200.7'], remaining_j1=water['remaining_j1'])
for version in byid['CA:CCR22'].get('version_records', []):
    if '2026-0827-01N' in json.dumps(version):
        version['remaining_j1'] = items['Drinking-water correction']['remaining_j1']

sbsd = byid['CA-HB:SBSD:FINAL-ACTION-EVIDENCE']
sbsd['acquisition']['status'] = items['SBSD named resolutions']['remaining_j1']
for identity in sbsd.get('selected_instrument_identities', []):
    general = '2024-03-01' in identity['identity']
    identity['record_role'] = 'general fee instrument' if general else 'property application; adoption evidence preserved'
    identity['body_route_required_for_j1'] = general
    if not general:
        exclude(sbsd, {'unit': identity['identity']+' individualized schedule'}, items['SBSD named resolutions']['reason'])
for unit in sbsd['units_in_scope']:
    if any(s in unit['unit'] for s in ['waiver','final-roll','BOE']):
        unit['document_role'] = 'Adoption evidence retained for application; individualized schedules are not J1 prerequisites.'
write('j1/register_updates.json', data)

review['integration_status'] = 'Applied to canonical selections and dependent metadata. Broad selectors narrowed to prevent excluded units returning during acquisition. J1 remains reopened with six retained questions; J2 has not begun.'
review['integration_script'] = 'j1/reassessment/apply_workflow_scope.py'
write(REVIEW, review)
remaining = [x['remaining_j1'] for x in review['items'] if x['remaining_j1']]
moved = read('j1/reassessment/moved-items.json')
moved['as_of'] = '2026-10-02'
moved['criterion'] = 'First establish the connection to undertaken readiness/account work. Within that scope, resolve any fact that could change registered identity, scope, status or acquisition route in J1.'
moved['open'] = [{'item': n, 'instrument': ids[n], 'reason': x['remaining_j1'], 'next_action': 'Resolve this selection question online; no external messages.'} for n,x in items.items() if x['remaining_j1']]
moved['scope_exclusions'] = [copy.deepcopy(x) for x in review['items'] if not x['remaining_j1']]
moved['scope_review'] = REVIEW
write('j1/reassessment/moved-items.json', moved)
connections = read('j1/reassessment/operating-connections.json')
connections['status'] = 'Eight-topic scope review integrated. Six source-selection questions remain; excluded action statuses are not claimed resolved.'
connections['items'] = [dict(copy.deepcopy(x), instrument=ids[n]) for n,x in items.items()] + [dict(x, remaining='Resolved through recovered replacement ArticleV and unchanged-adoption minutes.') for x in connections['items'] if x['item'] == 'SBSD organics amendment']
connections['review'] = REVIEW
write('j1/reassessment/operating-connections.json', connections)
completion = read('j1/completion.json')
completion.update(status='reopened', open_selection_questions=remaining, current_review=REVIEW)
completion['scope_review'] = {'source': REVIEW, 'status': 'Integrated', 'meaning': 'Six retained selection questions remain. Exclusions reflect undertaken workflows, not resolved legal status or retrieval difficulty.'}
completion['basis'] = ['Reviewed scope decisions applied to actual acquisition selectors. Six selection-changing source questions remain; J1 is incomplete.']
write('j1/completion.json', completion)
work = read('j1/WORK.json')
work['remaining'] = remaining
work['tasks'][1]['status'] = 'complete'
work['tasks'][1]['evidence'] = REVIEW
work['coordination'] = 'Root integrated the reviewed decisions; one bounded reviewer verified child selectors. No retrieval expansion.'
work['current_scope_review']['state'] = 'Integrated into canonical register, parent selectors and active queue.'
work['latest_turn_assessment'] = {'classification': 'progress', 'reason': review['integration_status'], 'evidence': [REVIEW]}
work['active_goal'] = 'Resolve the six retained workflow-relevant J1 selection questions; preserve jurisdiction-first construction.'
write('j1/WORK.json', work)
plan = (BASE/'PLAN.md').read_text()
plan = plan.replace('- [ ] Apply the [workflow-scope review](j1/reassessment/workflow-scope-review.json) to register selections and dependent metadata. This bounded integration precedes further retrieval; the register has not yet been changed by the review.', '- [x] Apply the [workflow-scope review](j1/reassessment/workflow-scope-review.json) to register selections and dependent metadata, including parent selectors that could reintroduce excluded subjects.')
plan = plan.replace('After register integration, online recovery follows', 'Register integration is complete. Next, online recovery follows')
plan = plan.replace('Current execution status: **blocked after three consecutive turns without selection progress**. The open requirements above remain unchanged.', 'Historical recovery status, superseded by resumed work and the scope review: blocked after three consecutive turns without selection progress.')
plan = plan.replace('Current work uses direct public-document and archive scraping, with root plus two workers.', 'That recovery round used direct public-document and archive scraping. Current work is recorded above.')
plan = plan.replace('No completion requirement was removed.', 'That recovery round did not remove requirements; the subsequent workflow review above narrowed them for substantive scope reasons.')
write('PLAN.md', plan)
progress = (BASE/'pipeline/PROGRESS.md').read_text()
heading = '## J1 workflow scope integrated — October 2, 2026'
if heading not in progress:
    progress = progress.replace('# Pipeline build progress\n', '# Pipeline build progress\n\n'+heading+'\n\nThe eight-topic review is applied to the register and acquisition selectors. GoGreen optional financing and FPPC streamlined-settlement amendments are excluded; cannabis cultivation fees and individualized district schedules are outside the retained requirements. Six source-selection questions remain. J1 is incomplete; J2 has not begun. See [current plan](../PLAN.md).\n', 1)
write('pipeline/PROGRESS.md', progress)
print('Applied eight-topic scope review; six retained questions remain.')
