"""Assemble tracker evidence from actual research; this is not a research chronology replay."""
import json
import re
from datetime import datetime
from pathlib import Path
from pipeline import core, coverage as c

HERE = Path(__file__).resolve().parent
FRESH = HERE / 'fresh_research'

def build():
    selection = json.loads((FRESH / 'source_selection.json').read_text())
    manifest = json.loads((FRESH / 'retrieval_manifest.json').read_text())
    selected = {s['source_id']: s for s in selection['sources']}
    other = {s['source_id']: s for s in selection['other_retrieved_sources']}
    ids = [s['source_id'] for s in manifest]
    inventory = {'source_ids': ids, 'method': selection['method'] + ' All retrieved sources accounted for, including conditional/redundant material; bounded by the fee decision, not all abandoned-property work.',
        'evidence': [c.artifact(FRESH / 'sources/CIV_TITLE5_CH5.html', 'complete enclosing chapter'),
                     c.artifact(FRESH / 'source_selection.json', 'source selection and exclusions'),
                     c.artifact(FRESH / 'discovery_log.json', 'actual fresh discovery sequence')]}
    inventory_path = FRESH / ('coverage-inventory.' + c.digest(inventory)[:16] + '.json')
    core.write_json(inventory_path, inventory)
    doc = {'schema': 1, 'scope_id': 'timely-property-recovery', 'jurisdiction': 'CA',
        'purpose': 'Return former-tenant belongings promptly and avoid unsupported storage charges while preserving lawful recovery.',
        'scope': 'Current ordinary California residential tenancy already terminated/vacated; two-day on-premises reclamation storage fee, including scope, timing and obstruction predicates. No full disposal authorization or determination of an offsite fee amount.',
        'author': 'root', 'as_of': '2026-10-01', 'next_action': 'Resolve identified source/interpretation gaps and obtain independent review.',
        'items': [], 'boundaries': [{'id': 'fee-decision-sources', 'description': 'Sources and exclusions needed for this bounded fee decision',
            'author': 'reference_evaluation_author', 'source_ids': ids, 'enumeration_complete': True,
            'next_action': 'Reconcile newly discovered sources and exclusions against authoritative enumeration and operating consequences.',
            'inventory': c.artifact(inventory_path, 'source_ids, method and authority evidence')}],
        'dependencies': [], 'reviews': []}
    for capture in manifest:
        sid = capture['source_id']; source = selected.get(sid)
        reason = source['selection_reason'] if source else other.get(sid, {}).get('reason', 'Newly retrieved source requires interpretation and dependency investigation')
        ref = c.artifact(FRESH / capture['text_path'], source['pinpoint'] if source else reason)
        footer = source.get('version_footer') if source else None
        if not footer and sid.startswith(('CIV_', 'CCP_', 'GOV_')) and sid != 'CIV_TITLE5_CH5':
            footers = re.findall(r'\((?:Amended by|Added by|Enacted)[^\n]*', (FRESH / capture['text_path']).read_text())
            footer = footers[-1].strip() if footers else None
        version = {'id': capture['text_sha256'], 'url': capture['resolved_url'], 'retrieved_at': capture['retrieved_at'],
            'effective_from': None, 'effective_to': None,
            'temporal_basis': footer or ('Current enclosing chapter snapshot; individual section versions determine operative dates.' if sid == 'CIV_TITLE5_CH5' else 'Dated legislative material; selection identifies its historical interpretive role, not an operative statutory rule.'), 'evidence': ref}
        match = re.search(r'Effective ([A-Za-z]+ \d{1,2}, \d{4})', footer or '')
        if match:
            version['effective_from'] = datetime.strptime(match.group(1), '%B %d, %Y').date().isoformat()
        version['id'] = c.digest({k:v for k,v in version.items() if k != 'id'})
        doc['items'].append({'id': sid, 'kind': 'source', 'title': sid, 'author': 'reference_evaluation_author',
            'status': 'resolved' if source else ('excluded' if sid in other else 'open'), 'decisions': [doc['purpose']],
            'next_action': 'Reinvestigate a changed source, legal date or factual branch.', 'conclusion': reason,
            'evidence': [ref, c.artifact(FRESH / 'FINDINGS.md', 'bounded fee decision, conditions, contrary authority and timing'),
                         c.artifact(FRESH / 'source_selection.json', sid)],
            'source': {'selected_version': version['id'], 'versions': [version], 'applies_on': '2026-10-01',
                'checked_through': '2026-10-01', 'recheck_on': '2026-10-02',
                'currentness_evidence': c.artifact(FRESH / 'source_selection.json', sid + ': current footer or dated historical authority')}})
    q = {'id': 'storage-fee-decision', 'kind': 'question', 'title': selection['question'], 'author': 'reference_evaluation_author',
        'status': 'resolved', 'decisions': [doc['purpose']], 'next_action': 'Establish actual timing, location, claimant and applicable route; reinvestigate changed facts.',
        'conclusion': 'Apply the independently reviewed FINDINGS decision, including the CIV1987 dwelling and CIV1990 premises distinction and every applicable alternative-route, timing and obstruction condition.',
        'evidence': [c.artifact(FRESH / 'FINDINGS.md', 'complete bounded interpretation and predicates')]}
    doc['items'].append(q)
    for sid in selected:
        doc['dependencies'].append({'id': 'fee->'+sid, 'from': q['id'], 'to': sid, 'status': 'required', 'reason': selected[sid]['selection_reason']})
    for a,b,reason in [('CIV_1987','CIV_1990','Separate premises fee bar'), ('CIV_1990','CIV_1980','Premises includes common areas'),
                      ('CIV_1980.5','CIV_1954.26','Commercial definition'),('CIV_1954.26','CIV_1940','Residential distinction'),
                      ('CIV_1987','CCP_12a','Terminal holiday rule'),('CCP_12a','CCP_135','Incorporated judicial holidays'),
                      ('CIV_1965','CIV_1940','Residential occupancy exclusion'),('CIV_1965','CIV_1981','Chapter5 initiation prevents alternative route'),
                      ('CCP_1174','CIV_1965','Express alternative return procedure'),('CCP_1174','CIV_1990','Express storage-cost incorporation'),
                      ('CCP_1174','CIV_1980','Express premises definition'),('CIV_1989','CIV_1981','Express override of chapter exclusion'),
                      ('CIV_7','GOV_6700','General holiday incorporation'),('CIV_7','GOV_6701','Observed general holidays'),
                      ('CIV_1987','CIV_10','First/last day count'),('CIV_1987','CIV_1983','Notice and chapter predicates'),
                      ('CIV_1990','CIV_10','Count two-day period'),('CIV_1990','CCP_12a','Extend final statutory holiday'),
                      ('CIV_1965','CIV_3517','No wrongful obstruction to manufacture storage costs'),
                      ('CIV_1987','CIV_1980','Claimant and premises definitions'),('CIV_1987','CIV_1981','Scope and chapter exclusions'),
                      ('CIV_1987','CIV_1980.5','Residential/commercial distinction'),('CIV_1987','CIV_1986','Storage location and safekeeping'),
                      ('CIV_1987','AB2521_2012_CH560','Enacted version and effective context'),
                      ('CIV_1990','AB2521_2012_CH560','Enacted independent premises restriction')]:
        doc['dependencies'].append({'id':a+'->'+b,'from':a,'to':b,'status':'required','reason':reason})
    return doc

if __name__ == '__main__':
    doc = build()
    core.write_json(HERE / 'fresh-candidate.json', doc)
    print(f"Prepared {len(doc['items'])} items and {len(doc['dependencies'])} dependencies; no reviews inserted.")
