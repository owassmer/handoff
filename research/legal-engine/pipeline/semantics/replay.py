"""Rebuild semantic outcomes from request/response evidence, never cached labels."""
from __future__ import annotations

from pipeline import jev_results
from pipeline.design.task_evaluation.batching import check_transport
from . import plan as preparation
from .compose import outcome, compose, validate_policy


def replay(plan, root, registry, policies, waves):
    """Validate an ordered execution history and derive the next runnable wave.

    Policies are explicit per-job inputs. Replaying with a changed policy rebuilds
    every outcome; a previously dispatched dependent request must still match.
    Failed or uncertain jobs remain visible and are never silently retried.
    """
    checked = preparation.validate(plan, root)
    if set(policies) != set(checked['jobs']):
        raise ValueError('Every job requires an explicit decision policy')
    for key, job in checked['jobs'].items():
        validate_policy(job['question']['primitive'], policies[key])
    plan_hash = jev_results.fingerprint(plan)
    outcomes = {}

    def next_wave():
        # Propagate explicit inapplicability before evaluating another wave.
        while True:
            pending = preparation.requests(plan, root, registry, outcomes)
            if not pending['inapplicable']:
                return pending
            for key in pending['inapplicable']:
                outcomes[key] = {'status': 'not_applicable', 'plan_hash': plan_hash}

    for wave in waves:
        pending = next_wave()
        expected = {r['request_hash']: r for r in pending['requests']}
        supplied = wave['requests']
        if len({r['request_hash'] for r in supplied}) != len(supplied):
            raise ValueError('Repeated request in execution wave')
        for request in supplied:
            if expected.get(request['request_hash']) != request:
                raise ValueError('Execution request differs from ready prepared work')
        results = wave['results']
        by_id = {r['case_id']: r for r in results}
        if len(by_id) != len(results) or set(by_id) != {r['case_id'] for r in supplied}:
            raise ValueError('Execution result coverage mismatch')
        for request in supplied:
            record = by_id[request['case_id']]
            status = record['status']
            if status not in {'answered', 'execution_error', 'invalid_response', 'not_sent'}:
                raise ValueError('Unknown execution status')
            if status != 'not_sent' and record.get('request_hash') != request['request_hash']:
                raise ValueError('Response request binding mismatch')
            if status == 'not_sent':
                continue
            binding = {'plan_hash': plan_hash, 'request_hash': request['request_hash'],
                       'record_hash': jev_results.fingerprint(record)}
            if status != 'answered':
                for key in request['identity']['questions']:
                    outcomes[key] = dict(binding, status=status)
                continue
            check_transport(record, request['expected_wire'])
            answers = jev_results.validate(record['raw'], request['identity'])
            for key, answer in answers.items():
                outcomes[key] = dict(outcome(answer, policies[key]), **binding,
                                     policy_hash=jev_results.fingerprint(policies[key]))
    pending = next_wave()
    output = compose(plan, root, outcomes)
    output['decision_policy_hash'] = jev_results.fingerprint(policies)
    return {'output': output, 'next': pending}
