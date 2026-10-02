"""Mechanical adaptation of reviewed preparation proposals; no legal inference."""
from copy import deepcopy

from pipeline import jev_results
from .plan import validate


def compile_proposal(proposal, root):
    if proposal.get('format') != 'section-semantics-preparation-proposal-1':
        raise ValueError('Unknown preparation proposal format')
    used = {key for job in proposal['jobs'] for key in job['evidence_refs']}
    sources = []
    for key in sorted(used):
        selection = proposal['evidence'][key]
        source = selection['source']
        sources.append({'id': key, 'path': source['path'], 'sha256': source['sha256'],
                        'start': source['start'], 'end': source['end'], 'quote': selection['text']})
    jobs = [{'id': job['id'], 'question': deepcopy(job['native']),
             'evidence': deepcopy(job['evidence_refs']), 'after': deepcopy(job['requires']),
             'state_template': deepcopy(job['state_template']), 'licenses': deepcopy(job['licenses'])}
            for job in proposal['jobs']]
    for job in jobs:
        if job['question']['primitive'] == 'noul':
            for license in job['licenses']:
                if license['answer'] not in {'YES', 'NO'}:
                    raise ValueError('Noul proposal licenses must name YES or NO')
                license['answer'] = license['answer'] == 'YES'
    plan = {'format': 'section-semantics-1', 'id': proposal['id'], 'sources': sources,
            'jobs': jobs, 'assertions': [], 'preparation_hash': jev_results.fingerprint(proposal),
            'source_occurrence_inventory': deepcopy(proposal['source_occurrence_inventory']),
            'candidate_inventory': {key: deepcopy(proposal[key]) for key in
                                    ('proposed_records', 'proposed_definitions', 'proposed_relationships')},
            'unit_boundary': deepcopy(proposal['unit_boundary'])}
    validate(plan, root)
    return plan
