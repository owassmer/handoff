"""Bounded statutory-expression experiment; frozen inputs, native Noul, shared context."""
from __future__ import annotations
import argparse
import asyncio
import hashlib
import json
import math
from pathlib import Path
from pipeline import core, jev
from pipeline.design.agent_jev_code.prepare import digest
from pipeline.design.agent_jev_code.run import execute, write
from pipeline.design.legal_references.experiment import make_requests


def assemble(cases, question, batched=False):
    # Reuse existing exact source/span checks; the legacy Choice is never dispatched.
    check = {'version': 'span-check-only', 'question_id': 'check', 'primitive': 'choice',
             'instructions': 'Span validation', 'criteria': {'YES': 'Yes', 'NO': 'No', 'INSUFFICIENT': 'Unknown'}}
    verified = make_requests(cases, check)
    groups = {}
    config = core.questions()
    for case in verified:
        state = case['payload']['state']
        if 'expression' not in state:
            raise ValueError('An exact expression is required')
        context = {'passage': state['focus'], 'source_kind': state['source_kind']}
        group = digest(context) if batched else case['case_id']
        row = groups.setdefault(group, {'state': context, 'questions': {}})
        spec = {'primitive': question['primitive'], 'instructions': {
            'question': question['instructions'], 'expression': state['expression']}}
        if question.get('expression_in_question'):
            spec['instructions'] = question['instructions'].replace('this expression', json.dumps(state['expression'], ensure_ascii=False))
        if 'criteria' in question:
            spec['criteria'] = question['criteria']
        row['questions'][case['case_id']] = spec
    rows = []
    for group, payload in groups.items():
        payload['model'] = config['model']
        identity = {'assembler_version': 'statutory-expression-1', 'task_version': question['version'],
                    'pinned_build': config['pinned_build'], 'payload': payload}
        rows.append({'case_id': group, 'request_hash': digest(identity), **identity})
    return rows


def validate_response(row, raw):
    if raw.get('model') != row['pinned_build']:
        raise ValueError('Unexpected model build')
    answers = raw.get('answers')
    if not isinstance(answers, dict) or set(answers) != set(row['payload']['questions']):
        raise ValueError('Missing or unexpected answer IDs')
    for answer in answers.values():
        if not isinstance(answer, dict):
            raise ValueError('Invalid Noul answer')
        value = answer.get('noul')
        if (answer.get('type') != 'noul' or isinstance(value, bool)
            or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1):
            raise ValueError('Invalid Noul answer')
    return answers


def freeze(cases, question, labels, output, review=None):
    if {c['case_id'] for c in cases} != {r['case_id'] for r in labels} or len(labels) != len(cases):
        raise ValueError('Label coverage mismatch')
    if any(r['expected'] not in ('YES', 'NO') or not r.get('reason') for r in labels):
        raise ValueError('Invalid label')
    separate, batched = assemble(cases, question), assemble(cases, question, True)
    output.mkdir(parents=True, exist_ok=False)
    for name, value in [('cases', cases), ('question', question), ('labels', labels),
                        ('separate', separate), ('batched', batched)]:
        write(output / f'{name}.json', value)
    if review is not None:
        write(output/'review.json', review)
    write(output/'manifest.json', {'frozen_before_dispatch': True,
          'label_review': 'Independent input-bound review.' if review is not None else 'Preparing agent; no independent reviewer in this run.',
          'files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir()}})


def freeze_reviewed(cases_path, question_path, review_path, output):
    review = json.loads(review_path.read_text())
    for key, path in [('cases', cases_path), ('question', question_path)]:
        if review.get('reviewed_inputs', {}).get(key) != hashlib.sha256(path.read_bytes()).hexdigest():
            raise ValueError('Review does not bind current ' + key)
    if any(row.get('material_ambiguity') for row in review['cases']):
        raise ValueError('Unresolved review ambiguity')
    freeze(json.loads(cases_path.read_text()), json.loads(question_path.read_text()),
           review['cases'], output, review=review)


def check_bundle(bundle):
    manifest = json.loads((bundle/'manifest.json').read_text())
    for name, expected in manifest['files'].items():
        if hashlib.sha256((bundle/name).read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen file changed: ' + name)


def evaluate(bundle, output, mode):
    check_bundle(bundle)
    requests = json.loads((bundle/f'{mode}.json').read_text())
    if json.loads((output/'requests.json').read_text()) != requests:
        raise ValueError('Executed requests differ from frozen requests')
    recorded = json.loads((output/'results.json').read_text())
    results = {r['case_id']: r for r in recorded}
    if len(results) != len(recorded) or set(results) - {r['case_id'] for r in requests}:
        raise ValueError('Duplicate or unknown result IDs')
    answers = {}
    statuses = {}
    for row in requests:
        result = results.get(row['case_id'])
        if result and result['request_hash'] != row['request_hash']:
            raise ValueError('Result identity mismatch')
        for qid in row['payload']['questions']:
            statuses[qid] = result['status'] if result else 'missing_result'
        if result and result['status'] == 'answered':
            answers.update(validate_response(row, result['raw']))
    rows = []
    for label in json.loads((bundle/'labels.json').read_text()):
        value = answers.get(label['case_id'], {}).get('noul')
        actual = 'YES' if value is not None and value > .5 else 'NO' if value is not None and value < .5 else None
        rows.append({**label, 'noul': value, 'actual': actual, 'status': statuses[label['case_id']],
                     'agreement': actual == label['expected'] if actual is not None else None})
    report = {'cases': len(rows), 'answered': len(answers), 'agreements': sum(r['agreement'] is True for r in rows),
              'disagreements': [r['case_id'] for r in rows if r['agreement'] is False],
              'unanswered': sum(r['noul'] is None for r in rows),
              'undecided': sum(r['noul'] == .5 for r in rows), 'rows': rows,
              'interpretation': 'Development majority comparison, not production thresholds or probability calibration.'}
    write(output/'evaluation.json', report)
    print(json.dumps({k: v for k, v in report.items() if k != 'rows'}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--mode', choices=['separate', 'batched'], default='separate')
    args = parser.parse_args()
    check_bundle(args.bundle)
    rows = json.loads((args.bundle/f'{args.mode}.json').read_text())
    for row in rows:
        identity = {k: row[k] for k in ('assembler_version', 'task_version', 'pinned_build', 'payload')}
        if digest(identity) != row['request_hash']:
            raise ValueError('Request identity mismatch')
        if any(q['primitive'] != 'noul' for q in row['payload']['questions'].values()):
            raise ValueError('This experiment requires Noul questions')
        jev.sdk_questions(row['payload']['questions'])
    args.output.mkdir(parents=True, exist_ok=False)
    write(args.output/'requests.json', rows)
    asyncio.run(execute(rows, args.output, .25, 4, response_validator=validate_response))
    evaluate(args.bundle, args.output, args.mode)


if __name__ == '__main__':
    main()
