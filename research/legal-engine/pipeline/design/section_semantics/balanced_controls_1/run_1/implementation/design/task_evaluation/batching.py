"""Batch only independently prepared questions with byte-equivalent semantic state."""
from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from pipeline import jev, jev_results
from .tasks import answer_diagnostic


def group_requests(requests):
    groups = defaultdict(list)
    for row in requests:
        identity = row['identity']
        shared = {key: identity[key] for key in ('base_url', 'model', 'pinned_build', 'state')}
        groups[jev_results.fingerprint(shared)].append(row)
    batches = []
    for group in groups.values():
        if len(group) < 2:
            continue
        if len({r['case_id'] for r in group}) != len(group):
            raise ValueError('Repeated case in shared context')
        first = group[0]['identity']
        questions = {r['case_id']: r['identity']['questions']['judgment'] for r in group}
        identity = {key: first[key] for key in ('base_url', 'model', 'pinned_build', 'state')}
        identity.update({'format': 'focused-shared-context-1', 'questions': questions,
                         'parents': {r['case_id']: r['request_hash'] for r in group}})
        batches.append({'case_id': '+'.join(r['case_id'] for r in group),
            'request_hash': jev_results.fingerprint(identity), 'identity': identity,
            'expected_wire': {'state': identity['state'], 'model': identity['model'],
                'questions': {key: value.model_dump(exclude_none=True)
                              for key, value in jev.sdk_questions(questions).items()}}})
    return batches


def compare(batches, batch_results, separate_results, labels):
    by_result = {r['case_id']: r for r in batch_results}
    separate = {r['case_id']: r for r in separate_results}
    expected = {r['id']: r['expected'] for r in labels}
    rows = []
    if len(separate) != len(separate_results) or len(expected) != len(labels) or len({r['case_id'] for r in batches}) != len(batches):
        raise ValueError('Duplicate comparison records')
    if len(by_result) != len(batch_results) or set(by_result) != {r['case_id'] for r in batches}:
        raise ValueError('Batch result coverage mismatch')
    for batch in batches:
        result = by_result[batch['case_id']]
        if result['status'] != 'answered':
            for key in batch['identity']['questions']:
                rows.append({'id': key, 'status': result['status']})
            continue
        if result['request_hash'] != batch['request_hash']:
            raise ValueError('Batch identity mismatch')
        check_transport(result, batch['expected_wire'])
        answers = jev_results.validate(result['raw'], batch['identity'])
        for key, answer in answers.items():
            earlier = separate[key]
            if earlier['request_hash'] != batch['identity']['parents'][key]:
                raise ValueError('Separate request identity differs')
            separate_answer = None
            if earlier['status'] == 'answered':
                single = {'pinned_build': batch['identity']['pinned_build'], 'questions': {'judgment': batch['identity']['questions'][key]}}
                wire = {'model': batch['identity']['model'], 'state': batch['identity']['state'],
                        'questions': {'judgment': batch['expected_wire']['questions'][key]}}
                check_transport(earlier, wire)
                separate_answer = answer_diagnostic(jev_results.validate(earlier['raw'], single)['judgment'])
            rows.append({'id': key, 'status': 'answered', 'expected': expected[key],
                'batched': answer_diagnostic(answer),
                'separate': separate_answer})
    return {'rows': rows, 'physical_batched_requests': len(batches),
            'judgments': len(rows), 'note': 'Matched development comparison; independent questions share identical state. No whole-process performance claim.'}


def check_transport(result, expected):
    attempts = result['transport']
    if len(attempts) != 1 or attempts[0]['body'] != expected:
        raise ValueError('Comparison transport mismatch')
    attempt = attempts[0]
    raw = attempt['body_text'].encode('utf-8')
    if hashlib.sha256(raw).hexdigest() != attempt['body_sha256'] or json.loads(raw) != expected:
        raise ValueError('Comparison transport bytes mismatch')


if __name__ == '__main__':
    import argparse
    import asyncio
    from decimal import Decimal
    from pathlib import Path
    from pipeline import core
    from .run import read_frozen, execute, save
    parser = argparse.ArgumentParser()
    parser.add_argument('bundle', type=Path)
    parser.add_argument('separate_run', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    frozen = read_frozen(args.bundle, core.ROOT, include_evidence=True)
    requests = frozen['requests.json']
    if json.loads((args.separate_run / 'requests.json').read_text()) != requests:
        raise ValueError('Separate run differs from parent freeze')
    batches = group_requests(requests)
    if not batches:
        raise ValueError('No identical-state independent question groups')
    plan_path = args.output.with_suffix('.plan.json')
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan = {'parent_manifest_sha256': hashlib.sha256((args.bundle / 'manifest.json').read_bytes()).hexdigest(),
            'batching_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'requests': batches}
    with plan_path.open('x') as stream:
        json.dump(plan, stream, indent=2, ensure_ascii=False, allow_nan=False)
    results = asyncio.run(execute(batches, args.output, Decimal('1')))
    separate = json.loads((args.separate_run / 'results.json').read_text())
    save(args.output / 'comparison.json', compare(batches, results, separate, frozen['review.json']['cases']))
