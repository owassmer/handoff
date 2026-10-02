"""Build lane proposals only; canonical integration belongs to the coordinator."""
import copy
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEGAL = HERE.parents[2]
SOURCE = HERE / 'sources'

def instrument(ident, name, url, functions, level='agency rule', documents=None):
    documents = documents or [(ident.split(':', 1)[1], name, url)]
    return {
        'id': ident, 'jurisdiction': ident.split(':')[0], 'name': name,
        'level': level, 'functions': functions, 'adapter': 'generic',
        'toc_source_url': url,
        'units_in_scope': [{'unit': number, 'heading': title, 'toc_url': ref,
                            'source_unit_kind': 'document',
                            'section_list': [{'number':number,'heading':title,'ref':ref}],
                            'reason': 'Complete named instrument, including definitions, conditions, exceptions and appendices; residential work, account or program dependency.'}
                           for number, title, ref in documents],
        'units_out': [],
        'acquisition': {'text_adapter': 'generic', 'enumeration': 'Explicit document references; harvest complete documents in J2.',
                        'status': 'Source identity established; J2 text completeness not asserted.'},
    }

def build():
    original = json.loads((LEGAL / 'jurisdictions/CA-OC/instruments.json').read_text())['instruments']
    ocha = [copy.deepcopy(i) for i in original if i['id'].startswith('CA-OC:OCHA-') and i['id'] != 'CA-OC:OCHA-OWNER']
    for item in ocha:
        ident = item['id']
        if ident == 'CA-OC:OCHA-FSS':
            item['toc_source_url'] = 'https://www.ochousing.org/sites/ocha/files/import/data/files/74034.pdf'
            item['source_capture'] = 'j1/lanes/local_agency/sources/ocha_identity.txt'
            chapters = ['The Family Self-Sufficiency (FSS) Program and the FSS Action Plan',
                        'Purpose, Scope, and Applicability of the Family Self-Sufficiency Program',
                        'Program Administration', 'Selecting and Serving FSS Families',
                        'Contract of Participation', 'Escrow Account',
                        'Portability in Housing Choice Voucher FSS Program',
                        'Family Unification Program (FUP) and Family Self Sufficiency Demonstration']
            item['units_in_scope'] = [{'unit': f'Chapter {n}', 'heading': title, 'toc_url': item['toc_source_url'],
                                      'reason': 'Local FSS policy affects program termination, portability and escrow-account treatment; retain complete chapter.'}
                                     for n, title in enumerate(chapters, 1)]
            item['temporal_note'] = 'Published OCHA directory labels this HUD Approved FSS Action Plan. Cover is undated. Retain alongside April 14 2026 Administrative Plan Chapter 18 and operative 24 CFR Part 984; publication does not establish that every federal-rule quotation in the plan is current.'
        elif ident == 'CA-OC:OCHA-COC':
            item['toc_source_url'] = 'https://housingauthority.oc.gov/sites/ocha/files/import/data/files/68805.pdf'
            item['source_capture'] = 'j1/sources/coc-real.txt'
            item['effective_from'] = '2017-10-01'
            item['temporal_note'] = 'Effective date is printed on the guidebook. It remains the guide linked by the OCHA directory on review; apply federal amendments and governing program agreements separately.'
        elif ident == 'CA-OC:OCHA-VAWA':
            item['name'] = 'OCHA VAWA policy, occupancy-rights notice and certification packet'
            item['temporal_note'] = 'Directory packet contains older policy and HUD forms; Emergency Transfer Plan is acquired separately as OCHA-TRANSFER. Operative federal requirements and April 2026 Administrative Plan control over obsolete form language.'
        if ident == 'CA-OC:OCHA-ADMIN':
            item['adopted_on'] = '2026-04-14'
            item['temporal_note'] = 'Cover states approval April 14 2026 despite stale Word metadata title. Read Chapter 8 with OCHA landlord-page NSPIRE notice and the federal implementation notices; retain Chapter 18/FSS and HOTMA conditional definitions.'
        for unit in item['units_in_scope']:
            unit['toc_url'] = item['toc_source_url']
        if ident == 'CA-OC:OCHA-FSS' or 'internal_units_in_scope' not in item:
            item['internal_units_in_scope'] = item['units_in_scope']
        item['units_in_scope'] = [{'unit':ident.split(':')[1], 'heading':item['name'],
            'toc_url':item['toc_source_url'], 'source_unit_kind':'document',
            'reason':'One complete program publication; preserve internal chapter selections and perform J2 subdivision without duplicate whole-document acquisition.',
            'section_list':[{'number':ident.split(':')[1], 'heading':item['name'], 'ref':item['toc_source_url']}]}]
        item['acquisition'] = {'text_adapter': 'generic', 'enumeration': 'One explicitly identified complete document; no directory-page substitution.', 'status': 'J1 source selection, not complete J2 harvest.'}
        item['legal_use'] = 'Local program policy/terms, conditional on program participation. Read with governing federal/state law, award-vintage agreements and later amendments; a posted summary does not override superior authority.'
    owner = instrument('CA-OC:OCHA-OWNER', 'OCHA owner implementation notices and briefing materials',
        'https://housingauthority.oc.gov/landlordowner',
        ['housing_assistance','deposit','payments','early_termination','work_standards','communications'], documents=[
        ('OWNER-NOTICES','OCHA Landlord/Owner notices','https://housingauthority.oc.gov/landlordowner'),
        ('OWNER-BRIEFING-2022','OCHA owner briefing packet, April 27 2022','https://www.ochousing.org/sites/ocha/files/2022-04/Owner%20Briefing%20Packet%20-%204-27-22_1.pdf'),
        ('OWNER-INSPECTION-2020','OCHA owner inspection checklist, January 2020','https://housingauthority.oc.gov/sites/ocha/files/import/data/files/17290.pdf'),
        ('OWNER-INCENTIVE-2024','Landlord Signing Bonus and Tenant Move-in Assistance Program terms and forms','https://housingauthority.oc.gov/sites/ocha/files/2024-10/Landlord%20Signing%20Bonus%20and%20Tenant%20Move-in%20Assistance%20Program%20Flyer-2024.pdf')])
    owner['source_capture'] = 'j1/lanes/local_agency/sources/owner_terms_more.txt'
    owner['legal_use'] = 'Separate local administrative actions and award/payment terms from informational summaries of California/federal law. Administrative Plan and superior law must resolve obsolete claims. Incentive availability is expressly funding-limited; no present award entitlement inferred.'
    owner['temporal_note'] = 'Landlord webpage announces NSPIRE implementation October 1 2025. This is a local implementation announcement, not proof of completed operational transition. Posted owner packet and checklist predate the announcement; retain for prior events and reconcile with April 2026 Administrative Plan and HUD notices. Two-month deposit language in the incentive flyer does not displace Civil Code 1950.5.'
    owner['units_out'] = [{'unit':'Owner newsletter archive 2018-2019; listing/marketing instructions and portal tutorials','reason':'No independent current legal requirement identified; marketing is outside the agreed aperture and current program duties are selected in the plan/notices.'}]
    hmis_docs = [
        ('POLICIES-2025','OC HMIS Policies and Procedures, May 2025','https://ochmis.org/wp-content/uploads/2025/07/OC-HMIS-Policies-Procedures-05-2025.pdf'),
        ('USER-AGREEMENT-2021','OC HMIS User Agreement','https://ochmis.org/wp-content/uploads/2021/02/OC-HMIS-User-Agreement-Reference-02-2021.pdf'),
        ('CLIENT-CONSENT-2026','OC HMIS Client Consent, May 2026','https://ochmis.org/wp-content/uploads/2026/05/HMIS-Client-Consent_05-2026_Updated.pdf'),
        ('COLLECTION-NOTICE-2022','Notice Regarding Collection of Personal Information','https://ochmis.org/wp-content/uploads/2022/01/01-2022-Notice-Regarding-Collection-of-Personal-Information-English.pdf'),
        ('PRIVACY-NOTICE-2025','OC HMIS Privacy Notice, October 2025','https://ochmis.org/wp-content/uploads/2025/11/10-2025-Privacy-Notice-English.pdf'),
        ('GRIEVANCE-2025','OC HMIS Grievance Form, May 2025','https://ochmis.org/wp-content/uploads/2025/06/Grievance-05-2025-English.pdf'),
        ('REVOCATION-2022','OC HMIS Client Revocation of Consent','https://ochmis.org/wp-content/uploads/2022/12/01-2022-Client-Revocation-of-Consent-English.pdf')]
    hmis = instrument('CA-OC:HMIS-POLICIES', 'Orange County CoC HMIS policies, agreements and privacy forms',
                      'https://ochmis.org/privacy-forms/', ['housing_assistance','data_security','communications'], documents=hmis_docs)
    hmis['application'] = 'Conditional on participating agency/program and actual handling of HMIS records; not a blanket duty on residential landlords.'
    hmis['source_capture'] = 'j1/lanes/local_agency/sources/hmis_documents.txt'
    hmis['temporal_note'] = 'Publisher directory selects May 2025 policies, October 2025 privacy notice and May 2026 consent; OCHA directory links an older May 2025 privacy notice. Use administering HMIS publisher for these versions.'
    hmis['units_out'] = [{'unit':'Participating agencies meeting schedule','reason':'Meeting dates are operational scheduling, not the rules for access or disclosure.'},
                         {'unit':'Translations of listed English originals','reason':'Duplicate language versions; preserve availability for actual notices and communications without treating each as an independent rule instrument.'}]

    # Source-owned link labels are matched to the actual clicked target, never guessed from titles.
    index = (SOURCE / 'state_emergency_index.txt').read_text()
    names = {int(n): title for n, title in re.findall(r'(\d+)†([^†]+)', index) if 31 <= int(n) <= 93}
    refs = {}
    for path in sorted(SOURCE.glob('caloes-links-*.txt')):
        for block in path.read_text().split('--------------------------------------------------------------------------------'):
            matched = re.search(r'Source: click\(\{"ref_id":"turn1011view0","id":(\d+)\}\)', block)
            url = re.search(r'\((https://[^\n]+)\)\n', block)
            if matched and url:
                refs[int(matched.group(1))] = url.group(1)
    assert len(refs) == 63, (len(refs), sorted(refs))
    assert set(refs) <= set(names)
    official_readable_counterparts = {
        66: 'https://www.gov.ca.gov/wp-content/uploads/2025/01/EO-1.10.25_-LA-Fires-N-3-25_signed_v2.pdf',
        82: 'https://www.gov.ca.gov/wp-content/uploads/2025/02/State-Permitting-and-Housing-Laws-EO-ATTESTED.pdf'}
    original_refs = dict(refs)
    refs.update(official_readable_counterparts)
    excluded_orders = {
        49: 'N-2-26 directs CalOES disaster assistance toImperialCounty forAugust2025storms. Full operative paragraph concerns intergovernmental funding, with no private residential work/account condition; underlying event proclamation remains selected.',
        69: 'N-6-25 concerns educational-agency instruction, school facilities and school administration; it does not regulate the selected residential work or outgoing account.',
        70: 'N-7-25 restricts unsolicited below-market property purchase offers; acquisition/disposition of real estate is outside this residential-work/outgoing-occupant-account aperture. Official Governor summary and DRE notice identify this scope; underlying attested scan remains a retrieval dependency if scope changes.',
        73: 'N-10-25 suspends penalties on owner property-tax payment; ownership taxation is outside this aperture. Official Governor summary identifies the relief; no residential tenant-account duty inferred.',
        81: 'N-19-25 directs CDSS/EDD outreach for childcare-worker disaster unemployment benefits; official Governor-hosted text contains no residential work or outgoing-account requirement.',
        86: 'N-26-25 extends the N-7-25 unsolicited real-property purchase-offer restrictions; same property-acquisition scope exclusion. Official Governor summary and DRE notice establish the connection.',
        83: 'N-21-25 concerns independent study, school audit and charter administration, and CalWORKs donation/resource treatment; no residential work or outgoing-account requirement identified in its four operative paragraphs.'}
    docs = [(f'CALOES-{n}', names[n], refs[n]) for n in sorted(refs) if n not in excluded_orders]
    docs.append(('TERMINATIONS-2026-09-21','September 21 2026 proclamation terminating 34 states of emergency',
                 'https://www.gov.ca.gov/wp-content/uploads/2026/09/FINAL-SOE-Termination-Proclamation-9.21.26-1.pdf'))
    docs.extend([
        ('EO-N-28-25','Executive Order N-28-25 hotel-tenancy extension','https://www.gov.ca.gov/wp-content/uploads/2025/06/EO-N-28-25-Hotel-Tenancy-_GGN-signed.pdf'),
        ('EO-N-32-25','Executive Order N-32-25 SB9 fire-area restrictions','https://www.gov.ca.gov/wp-content/uploads/2025/07/SB-9-EO_Formatted.FINAL_ATTESTED.pdf'),
        ('EO-N-35-25','Executive Order N-35-25 beneficial fire and permitting','https://www.gov.ca.gov/wp-content/uploads/2025/10/Executive-Order-Beneficial-Fire.pdf')])
    emergency = instrument('CA:EMERGENCY-PROCLAMATIONS','California open emergency proclamations, associated orders and September 2026 terminations',
        'https://www.caloes.ca.gov/office-of-the-director/policy-administration/legal-affairs/emergency-proclamations/',
        ['preconditions','work_standards','provider_contracts','rent_regulation','early_termination','consumer_protection'],
        level='executive order', documents=docs)
    event_rows = {}
    for n,title,territory,date in re.findall(r'(\d+)†([^†]+)\s*\|\s*([^|]+)\|\s*([^|]+)\|', index):
        if 31 <= int(n) <= 93:
            event_rows[int(n)] = {'event':title.strip(), 'territory':territory.strip(), 'event_proclamation_date':date.strip(),
                                  'source_basis':'CalOES event table; individual operative paragraphs can narrow or change application.'}
    for unit in emergency['units_in_scope']:
        if unit['unit'].startswith('CALOES-'):
            number = int(unit['unit'].split('-')[1])
            parent = max(n for n in event_rows if n <= number)
            unit['event_context'] = event_rows[parent]
            unit['source_role'] = 'event proclamation' if number in event_rows else 'associated executive order; date is event date, not order issuance'
        elif unit['unit'] in ['EO-N-28-25','EO-N-32-25']:
            unit['event_context'] = event_rows[64]
        elif unit['unit'] == 'EO-N-35-25':
            unit['event_context'] = event_rows[60]
    emergency['selection_reason'] = 'Emergency declarations and associated suspensions can change repair permits, housing protections, temporary occupancy and price restrictions; retain complete mixed instruments so geography, event, exceptions, durations and dependencies can be decided together. California parent scope includes conditional events outside Orange County.'
    emergency['source_capture'] = 'j1/lanes/local_agency/sources/state_emergency_index.txt'
    emergency['alternate_source_records'] = [{'unit':f'CALOES-{n}', 'index_target':original_refs[n], 'selected_readable_counterpart':url, 'evidence':'j1/lanes/local_agency/sources/emergency_alternate_text.txt'} for n,url in official_readable_counterparts.items()]
    emergency['units_out'] = [{'unit':names[n], 'toc_url':refs[n], 'reason':reason} for n,reason in excluded_orders.items()]
    emergency['units_out'].append({'unit':'N-34-25','toc_url':'https://www.gov.ca.gov/wp-content/uploads/2025/09/SEP-30_SIGNED_EO_N-34-25.pdf','reason':'Official Governor action summary identifies commissioning a climate/resilience/insurance study. No operative private residential work or occupant-account rule identified; scan body not recovered, so this is bounded by the source-summary evidence.'})
    emergency['enumeration_note'] = 'CalOES event table is not an exhaustive associated-order register: Governor January 6 2026 action summary supplies omitted N-28-25 and N-32-25, separately selected; October29 2025 Governor source supplies N-35-25 beneficial-fire order, whose body is only partly text-readable. N-34-25 study order excluded with stated evidence. Governor executive-orders archive pages1-3 screened: first page current through September21 2026, page3 cached four months earlier and jumps over known Jan2026/late2025 entries. This mixed-cache gap prevents complete chronological census; targeted official search is supplementary, not proof of absence.'
    emergency['acquisition']['status'] = 'Exact documents enumerated; several attested PDFs are scanned. Associated-order scope and temporal reconciliation remains incomplete where contents could not be recovered; source titles and an open-event index alone do not prove relevance or operation.'
    emergency['temporal_note'] = 'CalOES list is dated September 21 2026. An open event does not mean every associated executive-order provision remains operative. N-10-23 is expressly marked sunset November 1 2023 and retained only for historical/dependency reading. September 21 2026 termination proclamation ends the listed 2023/2024 emergencies and related executive-order provisions; it does not end all emergencies.'
    emergency['material_version_relationships'] = [
        {'unit':'CALOES-31','date':'2026-09-21','detail':'Statewide developing El Nino proclamation paragraph 18 suspends Penal Code396 restrictions for this event; paragraph9 concerns coastal emergency permitting. Preserve event-specific effect rather than a universal emergency flag.'},
        {'unit':'CALOES-38','date':'2026-05-23','detail':'CalOES final Orange County chemical-incident proclamation has six ordered paragraphs, including shelter property authorities. Earlier Governor-hosted 5-22-26_2120-23rd-version differs and is not the selected final source.'},
        {'unit':'TERMINATIONS-2026-09-21','date':'2026-09-21','detail':'Includes Airport/Bridge Fires, Hilary and earlier Orange County storm emergencies; local and state termination dates are distinct.'}]
    emergency['event_chain_register'] = 'j1/lanes/local_agency/emergency-chains.json'
    emergency['current_price_gouging_source'] = 'https://www.caloes.ca.gov/office-of-the-director/policy-administration/legal-affairs/price-gouging/'
    emergency['material_version_relationships'].extend([
        {'unit':'CALOES-89','date':'2026-01-06','detail':'N1-26 paragraph1 replaces N4-25 paragraph3 and extends396(b)/(c) only toFebruary7 2026 forLosAngelesCounty; open-event status does not extend that deadline.'},
        {'unit':'CALOES-88','date':'2025-11-24','detail':'N37-25 replaces N29-25 solar/building-code paragraphs with event-specific2022/2025code and insurance distinctions; replaces N23-25 HCDpriority paragraph adding imminent homelessness and omitting priorMarch2026sunset.'},
        {'unit':'EO-N-28-25','date':'2025-06-30','detail':'Readable Governor counterpart extends only N23paragraph4 hotel transient treatment toOctober1 2025. AB299(2025)chapter531 urgencyOctober10 provides separate conditional270day lodging rule; do not import tax suspension or infer gapless extension.'},
        {'unit':'CALOES-62','date':'2025-12-31','detail':'N38-25 initiation cutoffMay1 2026 subjectapproval/conditions differs from a universal completion sunset. SB1370(2026)chapter777 is futureJanuary2027 statutory successor.'}])
    local_emergency = instrument('CA-OC:LOCAL-EMERGENCIES', 'Orange County local emergency proclamations and status actions',
        'https://ocagendaext.oc.gov/',
        ['preconditions','work_standards','provider_contracts','rent_regulation','consumer_protection'],
        level='executive order', documents=[
        ('CHEMICAL-PROCLAMATION-2026-05-22','May 22 2026 chemical-incident local emergency proclamation','https://ocagendaext.oc.gov/ExtDocViewer/15f76c8b-b4da-42f2-b491-6942aaf959b4'),
        ('CHEMICAL-RATIFICATION-2026-05-27','May 27 2026 Board minutes: Resolution 26-039 ratification','https://ocagendaext.oc.gov/ExtDocViewer/9f5cd73a-94d6-4df0-9d65-d8fa6920f72e'),
        ('CHEMICAL-CONTINUATION-2026-08-11','August 11 2026 Board minutes: item 28 emergency continuation','https://ocagendaext.oc.gov/ExtDocViewer/9d0278fc-3d67-4c88-9bd5-226c7fe0f145'),
        ('COASTAL-PROCLAMATION-2026-09-17','September 17 2026 Hurricane Marie and El Nino local emergency proclamation','https://ocagendaext.oc.gov/ExtDocViewer/1cb12612-730f-43f1-86cd-3f928aa27334'),
        ('AIRPORT-HEALTH-TERMINATION-2026-06-09','June 9 2026 Board minutes: item 3 Airport Fire health emergency termination','https://ocagendaext.oc.gov/ExtDocViewer/d778a9c0-cf96-4d2e-b80a-231c9fb558f2'),
        ('AIRPORT-LOCAL-TERMINATION-2026-06-23','June 23 2026 Board minutes: item 62 Airport Fire local emergency termination','https://ocagendaext.oc.gov/ExtDocViewer/afa634c2-827c-44f6-8a3c-7306a2197a07')])
    local_emergency['units_in_scope'].append({'unit':'AIRPORT-HEALTH-DECLARATIONS-2024','heading':'September 13 and September 20 2024 Airport Fire local health declarations',
        'toc_url':'https://www.ochealthinfo.com/services-programs/disease-prevention/diseases-conditions/covid-19-resources/oc-health-officers',
        'source_unit_kind':'document','reason':'Two named declaration blocks on official Health Officer publisher page; J2 select both complete blocks and subdivide, preserving their distinct dates and wording.',
        'section_list':[{'number':'AIRPORT-HEALTH-DECLARATIONS-2024','heading':'September 13 and September 20 2024 Airport Fire local health declarations','ref':'https://www.ochealthinfo.com/services-programs/disease-prevention/diseases-conditions/covid-19-resources/oc-health-officers'}],
        'source_capture':'j1/lanes/local_agency/sources/airport_original.txt'})
    local_emergency['application'] = 'County instruments require their own territorial and event conditions. State, county, city and local-health declarations and terminations are distinct. No general extension of unincorporated county rules into Huntington Beach is inferred.'
    local_emergency['source_capture'] = 'j1/lanes/local_agency/sources/emergency_adoption.txt'
    local_emergency['temporal_note'] = 'May 27 actual minutes establish ratification; August 11 actual minutes establish continuation. September 17 proclamation is supported by the official press record and staff report, but September 24 ratification and September 29 chemical continuation are unresolved because the minute bodies could not be recovered. Preserve these as adoption/status dependencies, not approved resolutions. Airport health, county-local and state emergencies ended on different dates.'
    local_emergency['acquisition']['status'] = 'Chemical and coastal proclamation PDFs are scanned; generic text extraction does not establish contents. Obtain an image/OCR route in J2 and inspect operative text before deriving consequences. Minute bodies selected are readable.'
    local_emergency['unresolved_dependencies'] = [
        {'decision':'September 24 coastal ratification final action','source_url':'https://ocagendaext.oc.gov/ExtDocViewer/c4c226e7-f94c-4965-9111-b05e180fa4e0','cause':'Official minutes link returned retrieval failure. Posted draft resolution has blank resolution number and is not adoption proof.'},
        {'decision':'September 29 chemical emergency continuation final action','source_url':'https://ocagendaext.oc.gov/ExtDocViewer/e72cfa76-5fed-4cde-b846-a3d6c3b598e5','cause':'Official minutes link returned retrieval failure. September 23 memo recommends continuation; recommendation is not a Board action.'},
        {'decision':'Original Airport Fire declarations and debris-removal orders','cause':'Termination dates established, but original instruments and intervening debris measures need their full source chain retained for surviving or historical effects.'}]
    ces = instrument('CA-OC:CES-POLICY', 'Orange County Coordinated Entry System Policies and Procedures, October 2025',
        'https://ceo.oc.gov/sites/ceo/files/2025-10/CES%20P%26Ps%20Oct%202025.pdf',
        ['housing_assistance','early_termination','communications','data_security'])
    ces['adopted_on'] = '2025-10-22'
    ces['source_capture'] = 'j1/lanes/local_agency/sources/ces_policy.txt'
    ces['application'] = 'Conditional on CoC, ESG, HHAP or other required/voluntary CES program participation. Emergency transfer, housing-provider, grievance and privacy duties affect continuing/exiting assisted occupancy; unrelated initial-referral context retained in the same small mixed instrument.'
    ces['temporal_note'] = 'Cover states CoC Board approval October 22 2025; current County CES publisher links this version. Sections I-XIII and attachment retained. Later committee/Board action census and annual participating-agency agreement remain separate dependencies; a strategic-plan commitment to update standards is not an adopted replacement.'
    proposal = {'as_of':'2026-10-01','status':'source_proposals_ready; local_action_currentness_still_under_reconciliation',
                'replace_instruments': ocha, 'add_instruments':[owner,hmis,emergency,local_emergency,ces],
                'integration_note':'Generic section_list is explicit and bypasses directory guessing. Other local_agency child proposals are separate; root merges canonical sources.'}
    (HERE / 'proposal.json').write_text(json.dumps(proposal, indent=2)+'\n')
    print(f'{len(ocha)} replacements; {len(proposal["add_instruments"])} new source families; {len(docs)} named state emergency documents')

if __name__ == '__main__':
    build()
