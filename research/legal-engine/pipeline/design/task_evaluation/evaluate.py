"""Diagnostic agreement with all execution outcomes retained; no routing calibration."""
from __future__ import annotations

import math
import hashlib
import json


def binomial_cdf(k, n, p):
    return sum(math.comb(n, i) * p**i * (1-p)**(n-i) for i in range(k+1))


def upper_error_bound(errors, n, alpha=.05):
    """One-sided Clopper-Pearson bound conditional on independent Bernoulli draws."""
    if not 0 <= errors <= n or n < 1:
        raise ValueError('Invalid binomial counts')
    if errors == n:
        return 1.0
    low, high = 0.0, 1.0
    for _ in range(70):
        mid = (low + high) / 2
        if binomial_cdf(errors, n, mid) > alpha:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def evaluate(cases, labels, requests, results):
    def index(rows, field):
        mapped = {row[field]: row for row in rows}
        if len(mapped) != len(rows):
            raise ValueError('Duplicate case records')
        return mapped
    source = index(cases, 'id')
    expected = index(labels, 'id')
    prepared = index(requests, 'case_id')
    actual = index(results, 'case_id')
    if not set(source) == set(expected) == set(prepared) == set(actual):
        raise ValueError('Incomplete or unexpected evaluation records')
    ledger = []
    for key, case in source.items():
        response = actual[key]
        if response['status'] == 'answered':
            from .tasks import diagnostic
            if response['request_hash'] != prepared[key]['request_hash']:
                raise ValueError('Result request identity differs')
            transport = response['transport']
            if len(transport) != 1 or transport[0]['body'] != prepared[key]['expected_wire']:
                raise ValueError('Transport evidence differs')
            captured = transport[0]['body_text'].encode('utf-8')
            if hashlib.sha256(captured).hexdigest() != transport[0]['body_sha256'] or json.loads(captured) != transport[0]['body']:
                raise ValueError('Captured transport bytes differ')
            answer = diagnostic(response['raw'], prepared[key])
            outcome = 'agreement' if answer == expected[key]['expected'] else 'disagreement'
        else:
            answer = None
            outcome = response['status']
        ledger.append({'id': key, 'task': case['task'], 'family': case['family'],
                       'source_cluster': case['source_cluster'], 'expected': expected[key]['expected'],
                       'answer': answer, 'outcome': outcome})
    groups = {}
    for row in ledger:
        for name in [row['task'], row['task'] + '/' + row['family']]:
            groups.setdefault(name, []).append(row)
    metrics = {}
    for name, rows in groups.items():
        answered = [r for r in rows if r['outcome'] in ('agreement', 'disagreement')]
        errors = sum(r['outcome'] == 'disagreement' for r in answered)
        clusters = {}
        for row in rows:
            clusters.setdefault(row['source_cluster'], []).append(row)
        metrics[name] = {'total': len(rows), 'answered': len(answered), 'disagreements': errors,
            'execution_gaps': len(rows)-len(answered), 'source_clusters': len(clusters),
            'clusters_with_disagreement': sum(any(r['outcome'] == 'disagreement' for r in rs) for rs in clusters.values()),
            'conditional_independent_case_upper_error_95': upper_error_bound(errors, len(answered)) if answered else None}
    return {'ledger': ledger, 'metrics': metrics,
            'interpretation': 'Purposive clustered challenge set. Binomial bounds are conditional reference calculations, not population reliability or authorization thresholds. All execution gaps and disagreements require investigation.'}


if __name__ == '__main__':
    import argparse
    from pathlib import Path
    from pipeline import core
    from .run import read_frozen, save
    parser = argparse.ArgumentParser()
    parser.add_argument('bundle', type=Path)
    parser.add_argument('run', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    frozen = read_frozen(args.bundle, core.ROOT, include_evidence=True)
    requests = frozen['requests.json']
    if json.loads((args.run / 'requests.json').read_text()) != requests:
        raise ValueError('Executed requests differ from frozen bundle')
    cases = frozen['cases.json']['cases']
    labels = frozen['review.json']['cases']
    results = json.loads((args.run / 'results.json').read_text())
    if args.output.exists():
        raise ValueError('Preserve existing evaluation; select a new output path')
    save(args.output, evaluate(cases, labels, requests, results))
