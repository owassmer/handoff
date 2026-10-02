"""Flag reference-bearing passages for J1 researchers using one repeated Jev question."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from decimal import Decimal
from pathlib import Path

from pipeline import core, jev, jev_results
from pipeline.design.task_evaluation.run import execute, save

VERSION = 'j1-passage-reference-2'
QUESTION = 'Does this passage cite or refer to another document or provision?'


def selected(text, span):
    start, end = span['start'], span['end']
    if not (isinstance(start, int) and isinstance(end, int) and 0 <= start < end <= len(text)):
        raise ValueError('Invalid source span')
    return text[start:end]


def prepare(preparation, root, registry):
    requests = []
    ids = set()
    for source in preparation['sources']:
        if source['id'] in ids:
            raise ValueError('Duplicate source ID')
        ids.add(source['id'])
        path = (Path(root) / source['file']).resolve()
        if not path.is_relative_to(Path(root).resolve()):
            raise ValueError('Source outside research root')
        text = path.read_text()
        if hashlib.sha256(text.encode()).hexdigest() != source['sha256']:
            raise ValueError('Source changed since partitioning')
        selected(text, source['body'])
        cursor = source['body']['start']
        questions = {}
        for passage in source['passages']:
            if passage['id'] in questions or passage['start'] != cursor:
                raise ValueError('Duplicate passage or gap/overlap in source partition')
            instructions = {'question': QUESTION, 'passage': selected(text, passage)}
            context = [selected(text, span) for span in passage.get('context', [])]
            if context:
                instructions['context'] = context
            questions[passage['id']] = {'primitive': 'noul', 'instructions': instructions}
            cursor = passage['end']
        if not questions or cursor != source['body']['end']:
            raise ValueError('Partition does not cover the complete selected body')
        identity = {key: registry[key] for key in ('base_url', 'model', 'pinned_build')}
        # Each independent question carries its own passage. Source bookkeeping
        # is saved in identity but never put in the semantic request body.
        identity.update(format=VERSION, state=[], questions=questions, source=source)
        requests.append({'case_id': source['id'], 'identity': identity,
            'request_hash': jev_results.fingerprint(identity),
            'expected_wire': {'model': identity['model'], 'state': [],
                'questions': {key: value.model_dump(exclude_none=True)
                              for key, value in jev.sdk_questions(questions).items()}}})
    return requests


def report(requests, results):
    by_id = {r['case_id']: r for r in results}
    rows = []
    for request in requests:
        result = by_id.get(request['case_id'])
        answers = {}
        if result and result['status'] == 'answered':
            if result['request_hash'] != request['request_hash']:
                raise ValueError('Result belongs to a different input')
            answers = jev_results.validate(result['raw'], request['identity'])
        source = request['identity']['source']
        for passage in source['passages']:
            answer = answers.get(passage['id'])
            rows.append({'source': source['id'], 'file': source['file'],
                'passage': passage['id'], 'start': passage['start'], 'end': passage['end'],
                'text': request['identity']['questions'][passage['id']]['instructions']['passage'],
                'status': result['status'] if result else 'not_run',
                'reference_probability': answer['noul'] if answer else None})
    return {'passages': rows, 'use': 'Researchers inspect flagged passages, locate the cited text, '
            'retrieve it and reconcile coverage. Scores do not establish source completeness. '
            'All passages remain visible; unexecuted passages have no score.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('preparation', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--cap', type=Decimal, default=Decimal('.10'))
    args = parser.parse_args()
    requests = prepare(json.loads(args.preparation.read_text()), core.ROOT, core.questions())
    args.output.mkdir(parents=True, exist_ok=False)
    save(args.output / 'requests.json', requests)
    results = asyncio.run(execute(requests, args.output / 'calls', args.cap)) if args.run else []
    result = report(requests, results)
    save(args.output / 'passages.json', result)
    print(json.dumps({'passages': len(result['passages']),
                      'answered': sum(r['status'] == 'answered' for r in result['passages']),
                      'output': str(args.output)}))


if __name__ == '__main__':
    main()
