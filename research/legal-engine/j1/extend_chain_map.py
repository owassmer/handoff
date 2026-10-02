"""Record the agreed physical-work aperture in the existing shared decision map.

This is an operating research map, not a set of legal conclusions or a runtime
sequence. Existing account point identities remain available to their consumers.
"""
import json
from pathlib import Path
import shutil

BASE = Path(__file__).resolve().parents[1]
target = BASE / 'pipeline/chain_map.json'
backup = BASE / 'j1/history/chain_map.before-physical-work.json'
backup.parent.mkdir(parents=True, exist_ok=True)
if not backup.exists():
    shutil.copy2(target, backup)
doc = json.loads(target.read_text())
doc['version'] = '1.1.0'
doc['date'] = '2026-10-01'
doc['derived_from'] = ('The original DP0-DP9 account map derives from review/NYC_MARKET_RATE.md. '
    'PW0-PW3 and the expanded function descriptions express the full residential physical-work '
    'and outgoing-account aperture agreed in HANDOFF_CONTEXT.md, the intent notepad and CA/J0_INTAKE.md.')
doc['chain'] = ('From learning that a tenancy is ending through two independently progressing outcomes: '
    'the property is ready for its next occupant, and the departing tenancy financial relationship is resolved. '
    'Earlier events, governing agreements and legal changes are included where they change either outcome.')
doc['ordering_note'] = ('Point order supports research presentation, not a compulsory operating sequence. '
    'Physical work and account duties can proceed concurrently; dependencies follow the actual decision.')

groups = [
 ('PW0', 'access_and_occupancy', 'Lawful access and control of the premises', [
  'When may the landlord or provider enter, inspect, secure or work on the premises; what notice, consent or emergency condition is required?',
  'Has the landlord lawfully recovered possession, and what protection remains for occupants, belongings, keys and access credentials?',
  'What conditions require immediate action, restrict occupancy or trigger relocation, accommodation or interruption of service?',
  'Who has authority to arrange work and act for the owner or household, including death, incapacity, public ownership and program restrictions?']),
 ('PW1', 'work_scope_and_standards', 'Required work, permitted scope and safe performance', [
  'What condition must be restored, what work is required, and which responsibility belongs to the landlord, tenant, association, utility or another party?',
  'Which permits, approvals, inspections and building, accessibility or fire standards govern the proposed repair or replacement on the relevant dates?',
  'What hazard assessment, containment, worker protection, environmental handling or waste-disposal requirements govern this work?',
  'Which location, building, program or emergency conditions change the work requirements, allowable methods or timing?']),
 ('PW2', 'provider_commitments', 'Selecting, commissioning and paying providers', [
  'Which licences, certifications, insurance, bonds or other qualifications are required for the work and contracting arrangement?',
  'What authority, procurement, agreement, disclosure, cancellation, deposit and payment requirements govern the proposed commitment?',
  'How do changes, delays, incomplete performance, warranties, indemnities and subcontracting affect the existing commitment and available remedies?',
  'What wage, classification, prompt-payment, withholding, lien, release and reporting obligations attach to performing and paying for this work?']),
 ('PW3', 'work_completion', 'Completion, defects and the connection to the account', [
  'What completion evidence, inspection, clearance, certificate or approval establishes compliance and lawful readiness for occupancy?',
  'What remains owed when work is defective, incomplete, disputed, cancelled or paid in advance, and what remedy or corrective action is available?',
  'Which photographs, notices, invoices and other records must be created, delivered or retained, by whom and when?',
  'How do actual work, lawful charges, timing, credits and third-party payments affect the outgoing account without equating provider cost with tenant liability?'])]
doc['decision_points'] = [g for g in doc['decision_points'] if not g['id'].startswith('PW')]
for n, (ident, key, name, questions) in enumerate(groups, 10):
    doc['decision_points'].append({'id':ident, 'key':key, 'name':name, 'walk_step':'Physical work',
      'order':n, 'points':[{'id':f'{ident}.{i}', 'question':q} for i,q in enumerate(questions,1)]})

additions = {
 'landlord_tenant':['PW0.1','PW0.2','PW0.3','PW1.1','PW3.4'],
 'preconditions':['PW1.2','PW3.1'],
 'abandoned_property':['PW0.2'],
 'broker_licensing':['PW0.4','PW2.2'],
 'consumer_protection':['PW2.2','PW2.3','PW3.2'],
 'courts_procedure':['PW0.2','PW3.2'],
 'entity_capacity':['PW0.4','PW2.2'],
 'estates_incapacity':['PW0.4'],
 'anti_discrimination':['PW0.1','PW0.3','PW1.2'],
 'electronic_records':['PW2.2','PW3.3'],
 'data_security':['PW0.2','PW3.3'],
 'communications':['PW0.1','PW2.2'],
 'tax_reporting':['PW2.4'],
 'general_construction':['PW1.4','PW2.4'],
 'housing_assistance':['PW0.3','PW1.1','PW1.2','PW1.4','PW3.1'],
 'payments':['PW2.2','PW2.4','PW3.2','PW3.4'],
 'deposit':['PW3.3','PW3.4'],
 'limitations':['PW3.2'],
 'bankruptcy':['PW2.3','PW3.2']}
expanded = {
 'housing_assistance': ('Federal, state and local assisted, public, regulated-affordability and special housing '
    'programs: scope, agreements, tenant and agency shares, physical standards, inspection, tenancy protections, '
    'termination, transfers, deposits and permitted charges. Program and version conditions are preserved.'),
 'entity_capacity': ('Business-entity law governing authority to contract, operate property and assert or respond '
    'to claims: representation, foreign qualification, assumed names, suspension, dissolution and cures.'),
 'tax_reporting': ('Tax and information-reporting consequences directly incident to residential work and account '
    'resolution: payments to providers, classification/withholding, deposits, credits, settlements, bad debts and '
    'applicable information returns. Standalone tax planning and unrelated business operations are outside the aperture.')}
for f in doc['functions']:
    f['decision_points'] = list(dict.fromkeys(f['decision_points'] + additions.get(f['id'],[])))
    if f['id'] in expanded:
        f['description'] = expanded[f['id']]
    if f['id']=='anti_discrimination':
        f['description'] = ('Fair-housing and applicable accessibility law throughout access, repairs, accommodations, '
            'relocation, account treatment and recovery, including protected statuses, equal treatment and retaliation.')
new_functions = [
 {'id':'work_standards','name':'Physical-work requirements and standards',
  'description':'Housing, building, fire, accessibility, worker-safety and environmental requirements governing residential repair, remediation, service interruption, permits, inspections and lawful completion; retain applicable local, program and emergency variations.',
  'decision_points':['PW0.1','PW0.3','PW1.1','PW1.2','PW1.3','PW1.4','PW3.1','PW3.3']},
 {'id':'provider_contracts','name':'Provider qualification, commitments and remedies',
  'description':'Provider licensing and qualification; authority and procurement; work agreements, changes, cancellation, advances, payment, performance, warranties, liens, worker classification and work-related claims. Public-owner or program conditions attach where applicable.',
  'decision_points':['PW0.4','PW2.1','PW2.2','PW2.3','PW2.4','PW3.2','PW3.4']}]
doc['functions'] = [f for f in doc['functions'] if f['id'] not in {x['id'] for x in new_functions}] + new_functions
target.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+'\n')
