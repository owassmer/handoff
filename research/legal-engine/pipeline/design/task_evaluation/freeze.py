"""Freeze independently reviewed cases and exact requests before inference."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pipeline import core, jev_results
from .tasks import HERE, digest, prepare
from .run import save


def freeze(cases_path, review_path, destination, root, contracts_path=None):
    cases_path, review_path, destination = map(Path, (cases_path, review_path, destination))
    case_bytes = cases_path.read_bytes()
    review_bytes = review_path.read_bytes()
    contract_bytes = Path(contracts_path or HERE / 'contracts.json').read_bytes()
    cases = json.loads(case_bytes)['cases']
    review = json.loads(review_bytes)
    contracts = json.loads(contract_bytes)
    if review['cases_sha256'] != hashlib.sha256(case_bytes).hexdigest() or review['contracts_sha256'] != hashlib.sha256(contract_bytes).hexdigest():
        raise ValueError('Review does not bind current inputs')
    if not review.get('reviewer') or review.get('author_labels_seen') is not False or review.get('model_responses_seen') is not False:
        raise ValueError('Independent review identity and exposure disclosure required')
    if review.get('material_findings') != []:
        raise ValueError('Material findings remain')
    labels = review['cases']
    ids = [case['id'] for case in cases]
    if len(ids) != len(set(ids)) or len(labels) != len(cases) or {row['id'] for row in labels} != set(ids):
        raise ValueError('Case and independent expectation coverage differ')
    by_id = {row['id']: row for row in labels}
    for case in cases:
        expected = by_id[case['id']]['expected']
        valid = set(case['criteria']) if contracts['tasks'][case['task']]['primitive'] == 'choice' else {'YES', 'NO'}
        if expected not in valid or not by_id[case['id']].get('reason'):
            raise ValueError('Invalid or unexplained expectation')
    requests = [prepare(case, root, core.questions(), contracts) for case in cases]
    destination.mkdir(parents=True, exist_ok=False)
    for name, value in [('cases.json', case_bytes), ('review.json', review_bytes), ('contracts.json', contract_bytes)]:
        (destination / name).write_bytes(value)
    save(destination / 'requests.json', requests)
    implementation = {str(path.relative_to(root)): digest(path) for path in
                      [HERE / 'tasks.py', HERE / 'run.py', HERE / 'freeze.py', HERE / 'evaluate.py',
                       Path(root) / 'pipeline/jev.py', Path(root) / 'pipeline/jev_results.py']}
    save(destination / 'manifest.json', {
        'files': {name: digest(destination / name) for name in
                  ['cases.json', 'review.json', 'contracts.json', 'requests.json']},
        'implementation': implementation,
        'note': 'Labels frozen independently before inference; inspect review for reviewer identity and exposure disclosure.'})
    return requests


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cases', type=Path)
    parser.add_argument('review', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--contracts', type=Path)
    args = parser.parse_args()
    freeze(args.cases, args.review, args.destination, core.ROOT, args.contracts)
