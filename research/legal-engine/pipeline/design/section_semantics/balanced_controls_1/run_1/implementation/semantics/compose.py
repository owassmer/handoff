"""Compose only answer-licensed candidate assertions; never infer a negative from absence."""
from __future__ import annotations

from pipeline import jev_results
from .plan import validate


def validate_policy(kind, policy):
    keys = {'false_at_most', 'true_at_least'} if kind == 'noul' else {'choice_min_probability'}
    if kind not in {'noul', 'choice'} or not isinstance(policy, dict) or not keys <= policy.keys():
        raise ValueError('Missing decision policy for the question primitive')
    for key in keys:
        jev_results.number(policy[key], 0, 1, key)
    if kind == 'noul' and policy['false_at_most'] >= policy['true_at_least']:
        raise ValueError('Decision regions must not overlap')


def outcome(answer, policy):
    """Policy is explicit evaluation input, not a claim of calibrated reliability."""
    validate_policy(answer['type'], policy)
    if answer['type'] == 'noul':
        low, high = policy['false_at_most'], policy['true_at_least']
        value = answer['noul']
        if value <= low:
            return {'status': 'answered', 'answer': False, 'raw': answer}
        if value >= high:
            return {'status': 'answered', 'answer': True, 'raw': answer}
        return {'status': 'uncertain', 'raw': answer}
    probabilities = answer['probabilities']
    winners = [k for k,v in probabilities.items() if v == max(probabilities.values())]
    minimum = policy['choice_min_probability']
    if len(winners) != 1 or probabilities[winners[0]] < minimum:
        return {'status': 'uncertain', 'raw': answer}
    return {'status': 'answered', 'answer': winners[0], 'raw': answer}


def compose(plan, root, outcomes):
    checked = validate(plan, root)
    if not set(outcomes) <= checked['jobs'].keys():
        raise ValueError('Unknown semantic outcome')
    for key, result in outcomes.items():
        if result.get('plan_hash') != jev_results.fingerprint(plan):
            raise ValueError('Stale semantic outcome')
    records = {}
    for key, assertion in checked['assertions'].items():
        required = assertion['established_by']
        evidence = [outcomes.get(c['job'], {'status': 'unanswered'}) for c in required]
        if any(r['status'] == 'not_applicable' for r in evidence):
            status = 'not_applicable'
        elif any(r['status'] != 'answered' for r in evidence):
            status = 'unresolved'
        elif all(outcomes[c['job']]['answer'] == c['answer'] for c in required):
            status = 'supported'
        else:
            status = 'not_supported'
        records[key] = {'id': key, 'kind': assertion['kind'], 'status': status,
                        'candidate_value': assertion['value'], 'evidence': assertion['evidence'],
                        'established_by': required, 'field_licenses': assertion['field_licenses'], 'links': assertion.get('links', [])}
    # A supported assertion is incomplete while a required semantic target is unresolved/rejected.
    changed = True
    while changed:
        changed = False
        for row in records.values():
            if row['status'] == 'supported' and any(records[k]['status'] != 'supported' for k in row['links']):
                row['status'] = 'unresolved_relationship'
                changed = True
    assignments = []
    for key, job in checked['jobs'].items():
        if not job.get('licenses'):
            continue
        result = outcomes.get(key, {'status': 'unanswered'})
        if result['status'] != 'answered':
            assignments.append({'job': key, 'status': result['status'],
                                'candidate_targets': sorted({r['target'] for r in job['licenses']})})
            continue
        selected = [row for row in job['licenses'] if row['answer'] == result['answer']]
        if not selected:
            assignments.append({'job': key, 'status': 'unmapped_answer'})
        for row in selected:
            status = ('unresolved' if row['operation'] == 'retain_open' else
                      'not_supported' if row['operation'] == 'reject_only' else 'supported')
            assignments.append({'job': key, 'status': status, 'target': row['target'],
                                'value': row['value'], 'operation': row['operation'],
                                'evidence': job['evidence']})
    values = {}
    for row in assignments:
        if row['status'] == 'supported':
            values.setdefault(row['target'], set()).add(jev_results.fingerprint(row['value']))
    for row in assignments:
        if row['status'] == 'supported' and len(values[row['target']]) > 1:
            row['status'] = 'conflicting'
    return {'format': 'section-semantics-output-1', 'plan_id': plan['id'],
            'plan_hash': jev_results.fingerprint(plan), 'records': list(records.values()),
            'field_assignments': assignments,
            'jobs': outcomes, 'complete': set(outcomes) == set(checked['jobs']) and
            all(r.get('status') in {'answered', 'not_applicable'} for r in outcomes.values()) and
            all(r['status'] in {'supported', 'not_supported', 'not_applicable'} for r in assignments) and
            all(r['status'] in {'supported', 'not_supported', 'not_applicable'} for r in records.values()),
            'scope': 'Prepared jobs and candidates only; full-unit semantic completeness requires independent coverage validation.'}
