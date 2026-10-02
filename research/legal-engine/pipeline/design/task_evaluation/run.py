"""Frozen-request execution with transport-body verification and incremental records."""
from __future__ import annotations

import argparse
import hashlib
import asyncio
from datetime import datetime, timezone
from decimal import Decimal
import json
from pathlib import Path
import time

from pipeline import jev, jev_results
from .tasks import diagnostic, answer_diagnostic


def save(path, value):
    jev_results.atomic_write(path, json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n')


async def execute(requests, output, cap):
    import httpx2
    from pydantic import BaseModel, ConfigDict
    from typesafe_sdk import AsyncTypeSafeClient, RetryPolicy

    class Raw(BaseModel):
        model_config = ConfigDict(extra='allow')

    if cap <= 0 or not cap.is_finite():
        raise ValueError('Positive finite cost cap required')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    save(output / 'requests.json', requests)
    spent = Decimal(0)
    results = []
    stopped = None
    for request in requests:
        if stopped:
            results.append({'case_id': request['case_id'], 'status': 'not_sent', 'reason': stopped})
            save(output / 'results.json', results)
            continue
        # Reserve $0.01 per request. Stop if actual cost exceeds reservation.
        if spent + Decimal('.01') > cap:
            stopped = 'Cost reservation would exceed cap'
            results.append({'case_id': request['case_id'], 'status': 'not_sent', 'reason': stopped})
            save(output / 'results.json', results)
            continue
        record = {'case_id': request['case_id'], 'request_hash': request['request_hash'],
                  'started_at': datetime.now(timezone.utc).isoformat(), 'transport': []}
        start = time.monotonic()

        async def capture(http_request):
            body = json.loads(http_request.content)
            record['transport'].append({'url': str(http_request.url), 'body': body,
                'body_text': http_request.content.decode('utf-8'),
                'body_sha256': hashlib.sha256(http_request.content).hexdigest()})
            # Persist before transmission, without credentials or headers.
            save(output / 'inflight.json', record)
            if body != request['expected_wire']:
                raise ValueError('Actual serialized body differs from frozen request')
            if len(record['transport']) != 1:
                raise ValueError('Unexpected repeated transport attempt')

        try:
            if jev_results.fingerprint(request['identity']) != request['request_hash']:
                raise ValueError('Request identity mismatch')
            identity = request['identity']
            async with httpx2.AsyncClient(timeout=45, event_hooks={'request': [capture]}) as http:
                async with AsyncTypeSafeClient(api_key=jev.api_key(), base_url=identity['base_url'],
                        retry=RetryPolicy(max_retries=0), http_client=http) as client:
                    raw = await client.system_one(state=identity['state'],
                        questions=jev.sdk_questions(identity['questions']), model=identity['model'],
                        response_model=Raw)
            record['raw'] = raw.model_dump(mode='json')
            cost = jev_results.usage_cost(record['raw'])
            if cost is None:
                raise ValueError('Provider did not report cost')
            spent += cost
            answers = jev_results.validate(record['raw'], request['identity'])
            record['diagnostics'] = {key: answer_diagnostic(value) for key, value in answers.items()}
            if set(answers) == {'judgment'}:
                record['diagnostic'] = record['diagnostics']['judgment']
            record['status'] = 'answered'
            if cost > Decimal('.01'):
                stopped = 'Actual cost exceeded request reservation'
        except Exception as exc:
            record['status'] = 'invalid_response' if 'raw' in record else 'execution_error'
            record['error'] = jev.redact(f'{type(exc).__name__}: {exc}')
            stopped = 'Investigate failed request before further dispatch'
        record['seconds'] = time.monotonic() - start
        results.append(record)
        save(output / 'results.json', results)
    save(output / 'summary.json', {'requests': len(requests), 'answered': sum(r['status'] == 'answered' for r in results),
         'reported_cost': str(spent), 'stopped': stopped})
    return results


def read_frozen(bundle, root, *, include_evidence=False):
    bundle = Path(bundle)
    manifest = json.loads((bundle / 'manifest.json').read_bytes())
    mandatory = {'cases.json', 'review.json', 'contracts.json', 'requests.json'}
    implementation = {'pipeline/design/task_evaluation/' + name for name in
                      ('tasks.py', 'run.py', 'freeze.py', 'evaluate.py')} | {'pipeline/jev.py', 'pipeline/jev_results.py'}
    if set(manifest.get('files', {})) != mandatory or set(manifest.get('implementation', {})) != implementation:
        raise ValueError('Incomplete frozen manifest')
    snapshots = {}
    for name, expected in manifest['files'].items():
        if Path(name).name != name:
            raise ValueError('Invalid bundle member')
        data = (bundle / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError('Frozen input changed: ' + name)
        snapshots[name] = data
    for name, expected in manifest['implementation'].items():
        path = (Path(root) / name).resolve()
        if not path.is_relative_to(Path(root).resolve()) or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen implementation changed: ' + name)
    decoded = {name: json.loads(data) for name, data in snapshots.items()}
    return decoded if include_evidence else decoded['requests.json']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bundle', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--cap', type=Decimal, default=Decimal('1'))
    args = parser.parse_args()
    from pipeline import core
    asyncio.run(execute(read_frozen(args.bundle, core.ROOT), args.output, args.cap))
