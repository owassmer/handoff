"""Source-bound preparation for Goal 5; expected answers never enter requests."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pipeline import jev, jev_results

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare(case, root, registry, contracts=None):
    contracts = contracts or json.loads((HERE / 'contracts.json').read_text())
    contract = contracts['tasks'][case['task']]
    state = case['state']
    required = set(contract['fields'])
    if set(state) not in (required, required | {'context'}):
        raise ValueError('Unexpected or missing semantic fields')
    if any(not isinstance(v, str) or not v.strip() for v in state.values()):
        raise ValueError('Semantic fields must contain text')
    if 'use_expression' in state:
        expression = state['use_expression']
        if state['use_passage'].count(expression) != 1 or expression.count(state['term']) != 1:
            raise ValueError('Select a unique use expression containing the term')
    source_fields = set(contract['source_fields']) | ({'context'} if 'context' in state else set())
    if set(case['sources']) != source_fields:
        raise ValueError('Every evidence field needs an exact source selection')
    for field in source_fields:
        selection = case['sources'][field]
        path = (Path(root) / selection['path']).resolve()
        if not path.is_relative_to(Path(root).resolve()):
            raise ValueError('Source outside research root')
        captured = path.read_bytes()
        if hashlib.sha256(captured).hexdigest() != selection['sha256']:
            raise ValueError('Source changed')
        text = captured.decode("utf-8")
        start, end = selection['start'], selection['end']
        if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(text):
            raise ValueError('Invalid source offsets')
        if text[start:end] != state[field]:
            raise ValueError('Selected text differs from source')
    spec = {k: contract[k] for k in ('primitive', 'instructions')}
    if spec['primitive'] == 'choice':
        criteria = case.get('criteria')
        if not isinstance(criteria, dict) or len(criteria) < 2:
            raise ValueError('Choice requires distinct alternatives')
        if any(not isinstance(k, str) or not k or not isinstance(v, str) or not v.strip()
               for k, v in criteria.items()):
            raise ValueError('Choice alternatives require names and descriptions')
        if len(set(criteria.values())) != len(criteria):
            raise ValueError('Duplicate alternative descriptions')
        spec['criteria'] = criteria
    elif 'criteria' in case:
        raise ValueError('Case cannot override binary configuration')
    if 'criteria' in contract:
        spec['criteria'] = contract['criteria']
    questions = {'judgment': spec}
    # Native construction is part of preparation, not deferred until inference.
    wire_questions = {k: v.model_dump(exclude_none=True) for k, v in jev.sdk_questions(questions).items()}
    identity = {'format': 'focused-judgment-1', 'assembly_version': contracts['version'],
                'base_url': registry['base_url'], 'model': registry['model'],
                'pinned_build': registry['pinned_build'], 'questions': questions,
                'state': state, 'task': case['task'],
                'contract_hash': jev_results.fingerprint(contract)}
    wire = {'model': registry['model'], 'state': state, 'questions': wire_questions}
    return {'case_id': case['id'], 'request_hash': jev_results.fingerprint(identity),
            'identity': identity, 'expected_wire': wire,
            'evidence_hash': jev_results.fingerprint(case['sources'])}


def answer_diagnostic(answer):
    if answer['type'] == 'choice':
        distribution = answer['probabilities']
        winners = [key for key, value in distribution.items() if value == max(distribution.values())]
        return winners[0] if len(winners) == 1 else 'UNDECIDED'
    p = answer['noul']
    return 'YES' if p > .5 else 'NO' if p < .5 else 'UNDECIDED'


def diagnostic(raw, request):
    return answer_diagnostic(jev_results.validate(raw, request['identity'])['judgment'])
