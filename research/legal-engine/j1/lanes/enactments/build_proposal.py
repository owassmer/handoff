"""Transcribe saved official inventories and explicit author selections; no semantic classifier."""
from pathlib import Path
import json
import re
from collections import Counter

HERE = Path(__file__).resolve().parent
J1 = HERE.parent.parent
BASE = 'https://leginfo.legislature.ca.gov/faces/'

def read(name):
    return json.loads((HERE / name).read_text())

def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def billid(number):
    match = re.fullmatch(r'([AS]B)X(\d)(\d+)', number)
    return ('20252026' + match[2] + match[1] + match[3]) if match else '202520260' + number

inventory = read('session_inventory.json')
chapters = read('chapters_2025.json')
groups = read('selection_groups.json')
timing = read('timing_and_prior_selections.json')
exclusions = {}
for group in read('scope_exclusions.json'):
    for house in ['AB', 'SB']:
        for n in group[house].split():
            exclusions[house + n] = group['reason']
old = json.loads((J1 / 'bill_candidates.json').read_text())
early_ab = json.loads((J1 / 'assembly_early_2026.json').read_text())
early_sb = json.loads((J1 / 'senate_early_2026_ids.json').read_text())
membership = {}
for group_id, group in groups.items():
    numbers = [house + n for house in ['AB', 'SB'] for n in group[house].split()]
    numbers += group.get('extraordinary', '').split()
    for number in numbers:
        assert inventory[number]['status'] == 'Chaptered', number
        membership.setdefault(number, []).append(group_id)

decisions = []
instruments = []
for number, row in sorted(inventory.items(), key=lambda item: item[1]['line']):
    if not re.fullmatch(r'[AS]B(?:X\d)?\d+', number):
        continue
    decision = dict(row)
    decision['session_bill_id'] = billid(number)
    decision['text_url'] = BASE + 'billTextClient.xhtml?bill_id=' + billid(number)
    decision['history_url'] = BASE + 'billHistoryClient.xhtml?bill_id=' + billid(number)
    decision['official_status'] = row['status']
    if number in old:
        decision['governor_announcement'] = old[number]
        if old[number]['status'] == 'vetoed':
            decision['legal_status'] = 'vetoed'
    decision.setdefault('legal_status', 'chaptered' if row['status'] == 'Chaptered' else 'vetoed' if row['status'] == 'Vetoed' else row['status'])
    if row['status'] == 'Chaptered':
        if 'X' in number:
            decision['statutes_year'] = 2025
            decision['session_type'] = 'first_extraordinary'
            decision['year_evidence'] = 'sources/session-index-1.json'
        elif number in chapters:
            decision.update(chapters[number])
            decision['session_type'] = 'regular'
        else:
            decision['statutes_year'] = 2026
            decision['session_type'] = 'regular'
            decision['year_evidence'] = 'Official complete 2025–26 chaptered inventory minus all 790 regular-session 2025 chapters; extraordinary acts separated.'
        if number in membership and number not in exclusions:
            gs = membership[number]
            decision['scope'] = 'retain'
            decision['scope_groups'] = gs
            decision['functions'] = sorted({f for g in gs for f in groups[g]['functions']})
            decision['reason'] = ' '.join(groups[g]['reason'] for g in gs)
            unit = {'unit':number, 'heading':row['title'], 'reason':decision['reason'],
                    'toc_url':decision['text_url'],
                    'source_unit_kind':'document',
                    'section_list':[{'number':number, 'heading':row['title'], 'ref':decision['text_url'], 'source_unit_kind':'document'}]}
            instrument = {'id':'CA:ACT:' + billid(number), 'jurisdiction':'CA',
                          'name':number + ' — ' + row['title'], 'level':'statute',
                          'functions':decision['functions'], 'adapter':'ca_leginfo',
                          'toc_source_url':decision['text_url'], 'units_in_scope':[unit], 'units_out':[],
                          'legal_status':'chaptered', 'statutes_year':decision['statutes_year'],
                          'status_source':decision['source_capture'],
                          'history_url':decision['history_url'],
                          'temporal_selection':'Whole enactment preserves changes, savings, operative conditions and uncodified provisions; current-code units remain separately selected.',
                          'timing':'Chaptered status established. Do not equate signing, effective and operative dates. Individual operative branches remain part of selected text for J2/J4; no uniform January 1 date asserted.'}
            evidence = timing.get(billid(number))
            if evidence:
                instrument['temporal_evidence'] = evidence
                if evidence.get('ref'):
                    instrument['toc_source_url'] = evidence['ref']
                    unit['toc_url'] = evidence['ref']
                    unit['section_list'][0]['ref'] = evidence['ref']
            if decision['statutes_year'] == 2026:
                instrument['temporal_selection'] = '2026 enacted amendment: preserve the enacted text before its default 2027 effectiveness and any earlier urgency, deferred operation, uncodified or transition provisions. Current codified text alone may represent a different operative version.'
                instruments.append(instrument)
            decision['instrument_proposal'] = instrument
        else:
            decision['scope'] = 'exclude'
            decision['reason'] = exclusions.get(number, 'Heading reviewed: '+row['title']+' Its stated subject is outside residential physical work and outgoing-account resolution. Exclusion is of this enactment as an additional source, not of generally applicable code provisions or a later demonstrated cross-reference.')
    else:
        if decision['legal_status'] == 'vetoed':
            decision['scope'] = 'exclude_vetoed'
            decision['reason'] = 'Veto established by official session status or Governor action announcement; not an enacted or pending-Governor source.'
        elif number == 'SB1446':
            decision['legal_status'] = 'concurrence_pending'
            decision['scope'] = 'exclude_not_both_house_passed'
            decision['status_evidence'] = 'sources/sb1446-official-final-summary.txt, Senate final daily summary August 31, 2026, page 13, lines 545–547: concurrence in Assembly amendments pending.'
            decision['reason'] = 'The final official Senate summary resolves unfinished business as pending concurrence, not enrolled passage by both houses. Incarceration release/parole is also outside the residential work/account aperture.'
        else:
            decision['scope'] = 'exclude_not_both_house_passed'
            decision['reason'] = 'Official end-of-session location identifies committee, failed/died, inactive or chamber-floor business rather than enrollment or Governor consideration. No bill is converted to a both-house-passed measure from one-house passage.'
    decisions.append(decision)

write('bill_decisions.json', decisions)
write('instruments_2026.json', instruments)
prior = []
representation = []
budget_ids = {'AB100', 'AB102', 'AB104', 'SB101', 'SB103', 'SB105'}
for decision in decisions:
    if decision.get('scope') != 'retain' or decision.get('statutes_year') != 2025:
        continue
    instrument = decision['instrument_proposal']
    ident = decision['session_bill_id']
    selected = ident in timing or decision['id'] in budget_ids
    if selected:
        instrument['temporal_selection'] = timing[ident]['selection_use'] if ident in timing else 'Uncodified budget appropriations and conditions for housing, residential recovery, enforcement and civil legal services are not reproduced in consolidated codes. Retain the budget document for those conditional authorities; unrelated state appropriations do not expand the operational scope.'
        prior.append(instrument)
    representation.append({'id':ident,'representation':'separate_enactment_and_current_code' if selected else 'current_code', 'reason':instrument['temporal_selection'] if selected else 'Ordinary codified amendment represented by complete selected current code units, including displayed future versions and annotations. No additional historical-act duplication selected from this heading review.'})
older_names = {'202320240AB1572':'Potable water: nonfunctional turf.', '202320240AB2579':'Inspections: exterior elevated elements.', '202320240AB2801':'Tenancy: security deposits.'}
for ident, name in older_names.items():
    evidence = timing[ident]
    number = ident[9:]
    ref = BASE + 'billTextClient.xhtml?bill_id=' + ident
    functions = ['work_standards'] if number != 'AB2801' else ['deposit']
    prior.append({'id':'CA:ACT:'+ident,'jurisdiction':'CA','name':number+' — '+name,'level':'statute','adapter':'ca_leginfo','functions':functions,'legal_status':'chaptered','statutes_year':evidence['statutes_year'],'toc_source_url':ref,'status_source':evidence['source_capture'],'temporal_selection':evidence['selection_use'],'temporal_evidence':evidence,'units_in_scope':[{'unit':number,'heading':name,'reason':evidence['selection_use'],'source_unit_kind':'document','toc_url':ref,'section_list':[{'number':number,'heading':name,'ref':ref,'source_unit_kind':'document'}]}],'units_out':[]})
write('instruments_prior.json', prior)
write('prior_representation.json', representation)
chaptered = {x['id'] for x in decisions if x['legal_status'] == 'chaptered' and x.get('statutes_year') == 2026}
existing = set(old) | {x['id'] for x in early_ab} | set(early_sb)
reconciliation = {
    'as_of':'2026-10-01',
    'official_source':'https://leginfo.legislature.ca.gov/faces/billSearchClient.xhtml?author=All&house=Both&lawCode=All&session_year=20252026',
    'source_rows':5065,'ordinary_measure_rows':len(inventory),'additional_row':'GRP-1 (source L3153; agency reorganization referred to local/agency lane)',
    'regular_2025_chaptered':len(chapters),'regular_2026_chaptered':len(chaptered),'extraordinary_2025_chaptered':4,
    'earlier_candidates':len(old),'early_assembly':len(early_ab),'early_senate':len(early_sb),'earlier_union':len(existing),
    'chaptered_2026_missing_from_earlier_union':sorted(chaptered-existing),
    'news_veto_table_unfinished':[x['id'] for x in decisions if x['legal_status']=='vetoed' and x['official_status']=='Senate - Unfinished Business'],
    'scope_counts':dict(Counter(x['scope'] for x in decisions)),
    'selected_2026_acts':len(instruments),
    'selected_prior_acts':len(prior),
    'nonchaptered_status_counts':dict(Counter(x['legal_status'] for x in decisions if x['official_status'] != 'Chaptered')),
    'both_house_pending_disposition':'No AB/SB entry is listed as enrolled, passed or pending Governor in the complete official table. Senate Unfinished Business comprises 30 Governor-vetoed measures and SB1446 pending concurrence, resolved from the final official daily summary. Passed rows in the table are resolutions rather than AB/SB bills.',
    'year_derivation':'2025 complete SOS numbered chapters 1–790; all remaining regular-session chaptered acts in complete 2025–26 official inventory belong to 2026. No introduced-year shortcut used.',
    'limitations':'Headline Governor 1160 total is corroboration only. Senate Unfinished Business can mean veto consideration or lack of concurrence. Record bill-specific history before treating it as enacted/passed both houses. Earlier-year separate-text selections are in a distinct proposal.'
}
write('reconciliation.json',reconciliation)
print(json.dumps({k:v for k,v in reconciliation.items() if not isinstance(v,list)},indent=2))
