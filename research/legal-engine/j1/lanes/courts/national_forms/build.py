import json
from pathlib import Path

P = Path(__file__).parent
rows = json.loads((P / 'observed_rows.json').read_text())
related = json.loads((P / 'related_documents.json').read_text())
excluded = {
    'B 423': 'Publisher expressly marks abrogated December 1, 2024.',
    'B 4100N': 'Replaced December 1, 2025 by B 410C13-N; stale national index retained as supersession evidence.',
    'B 4100R': 'Replaced December 1, 2025 by B 410C13-NR; stale national index retained as supersession evidence.',
    'B 4170': 'Inmate-specific filing declaration; independent incarcerated-party procedure outside operating aperture.',
    'B 2810': 'Independent child-support creditor appearance; ordinary competing-priority/debtor discharge forms remain selected.',
    'AO 241': 'Habeas proceeding outside aperture.',
    'AO 242': 'Habeas proceeding outside aperture.',
    'AO 243': 'Criminal sentence collateral attack outside aperture.',
    'Pro Se 13': 'Independent Social Security benefits appeal outside aperture.',
    'Pro Se 14': 'Prisoner civil-rights complaint outside aperture.',
}
other_selected = {'AO 30', 'AO 120', 'AO 121', 'AO 132', 'AO 133', 'AO 145', 'AO 187', 'AO 187A', 'AO 213R', 'AO 390', 'AO 393', 'AO 435', 'AO 436'}
other_numbers = {r['number'] for r in rows[182:]}
for number in other_numbers - other_selected:
    excluded[number] = 'Court personnel, internal accounting/record management, vendor/payment administration, judicial discipline or wiretap reporting; no independent civil-party filing dependency in this aperture.'

def instrument(bankruptcy):
    relevant = [r for r in rows if r['number'].startswith('B ') == bankruptcy]
    selected = [r for r in relevant if r['number'] not in excluded]
    source = 'https://www.uscourts.gov/forms-rules/forms/' + ('bankruptcy-forms' if bankruptcy else 'civil-forms')
    ident = 'US:BANKRUPTCY-FORMS' if bankruptcy else 'US:CIVIL-FORMS'
    units = []
    for row in selected:
        units.append({'number': row['number'], 'heading': row['heading'], 'ref': row['record_url'], 'source_unit_kind': 'document', 'form_document_role': 'primary', 'acquisition_identity_status': 'exact official form record; resolve primary Download pdf anchor'})
        if row['number'] == 'B 3180FH':
            units[-1].update(ref='https://www.uscourts.gov/sites/default/files/form_b3180fh_0.pdf', publisher_record_url=row['record_url'], acquisition_identity_status='exact official PDF observed in indexed publisher result; record direct-open transport failure')
    documents = {}
    selected_numbers = {r['number'] for r in selected}
    for link in related:
        if link['number'] not in selected_numbers:
            continue
        ref = link['pdf_url']
        role = link['role']
        if ref not in documents:
            documents[ref] = {'number': link['number'] + ('-NOTES' if role == 'committee_notes' else '-INSTRUCTIONS'), 'heading': ('Committee notes' if role == 'committee_notes' else 'Form instructions') + ' linked from ' + link['number'], 'ref': ref, 'source_unit_kind': 'document', 'form_document_role': role, 'related_form_numbers': [], 'publisher_record_urls': [], 'acquisition_identity_status': 'actual labelled publisher link resolved to official PDF', 'edition_note': 'Publisher-linked supporting publication, potentially cumulative or derived from predecessor form; distinguish historical commentary and current instructions during J2/J5.'}
        doc = documents[ref]
        if link['number'] not in doc['related_form_numbers']:
            doc['related_form_numbers'].append(link['number'])
            doc['publisher_record_urls'].append(link['record_url'])
    units.extend(documents.values())
    return {'id': ident, 'jurisdiction': 'US', 'name': 'National Official and Director Bankruptcy Forms' if bankruptcy else 'National civil and related court forms', 'level': 'court rule', 'instrument_kind': 'court forms', 'functions': ['courts_procedure'], 'source_url': source, 'adapter': 'usc_court_forms', 'text_adapter': 'usc_court_forms', 'source_unit_kind': 'document', 'units_in_scope': [{'unit': 'Forms', 'heading': 'Applicable national form documents', 'toc_url': source, 'source_unit_kind': 'document', 'section_list': units, 'reason': 'Civil filing, evidence, enforcement and appeals; bankruptcy debtor/creditor claims, assets, contracts, notices, discharge and distribution dependencies. Specialized bankruptcy chapters remain conditionally relevant where an account debtor enters that chapter.'}], 'exclusions': [{'number':r['number'], 'heading':r['heading'], 'ref':r.get('record_url'), 'reason':excluded[r['number']]} for r in relevant if r['number'] in excluded], 'acquisition_notes': 'Resolve primary form PDF before Form Number. Committee Notes and Form Instructions are separately labelled related publications, not alternate editions or substitutes for the primary form. Supporting publications are independently enumerated by exact PDF URL with form associations. Do not collapse them into the primary form. Local form requirements and Official versus Director form force must be reconciled during later analysis. Future B101/B106C December 2026 amendments are separately registered by root.', 'source_review': 'j1/lanes/courts/national_forms/README.md'}

out = {'instruments': [instrument(True), instrument(False)]}
(P / 'proposal.json').write_text(json.dumps(out, indent=2) + '\n')
for entry in out['instruments']:
    leaves = entry['units_in_scope'][0]['section_list']
    assert len(leaves) == len({r['number'] for r in leaves})
    assert all(r['ref'].startswith('https://www.uscourts.gov/') for r in leaves)
    print(entry['id'], len(leaves), 'selected;', len(entry['exclusions']), 'excluded')
