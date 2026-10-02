"""Persist and resume dependency waves using the verified native Jev transport."""
from __future__ import annotations

import fcntl
import hashlib
import json
from importlib.metadata import version
from decimal import Decimal
from pathlib import Path

from pipeline import jev_results
from pipeline.design.task_evaluation.run import execute, save
from .replay import replay


def implementation_identity():
    """Bind resumable work to the code and SDK that interpret its results."""
    pipeline = Path(__file__).resolve().parents[1]
    paths = sorted((pipeline / 'semantics').glob('*.py')) + [pipeline / name for name in
             ('jev.py', 'jev_results.py', 'design/task_evaluation/run.py',
              'design/task_evaluation/batching.py', 'design/task_evaluation/tasks.py')]
    return {'files': {str(path.relative_to(pipeline)): hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in paths},
            'typesafe_sdk': version('typesafe-sdk')}


def read_run(directory, root):
    """Read a quiescent run by replaying raw evidence, not its cached output."""
    directory = Path(directory)
    with (directory / 'lock').open('r') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError('Semantic run is still executing') from exc
        snapshot = json.loads((directory / 'inputs.json').read_bytes())
        if snapshot.get('implementation') != implementation_identity():
            raise ValueError('Semantic run implementation differs from current code')
        waves = []
        for i, call in enumerate(sorted(directory.glob('call-*'))):
            if call.name != f'call-{i:06d}':
                raise ValueError('Execution history has a missing or unexpected call')
            if not (call / 'requests.json').exists() or not (call / 'results.json').exists():
                raise ValueError('Interrupted call has an unknown outcome')
            waves.append({'requests': json.loads((call / 'requests.json').read_bytes()),
                          'results': json.loads((call / 'results.json').read_bytes())})
        state = replay(snapshot['plan'], root, snapshot['registry'], snapshot['policies'], waves)
        return snapshot, state


async def run(plan, root, registry, policies, directory, cap, *, dispatch=execute):
    """Resume completed calls; never resend a call with an unknown outcome.

    A cap covers the whole run, including earlier calls. Each call keeps its
    prepared request, exact wire capture, raw response and reported cost.
    """
    cap = Decimal(cap)
    if not cap.is_finite() or cap <= 0:
        raise ValueError('Positive finite total cost cap required')
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / 'lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError('Semantic run is already executing') from exc
        snapshot = {'plan': plan, 'registry': registry, 'policies': policies,
                    'implementation': implementation_identity()}
        snapshot_path = directory / 'inputs.json'
        replay(plan, root, registry, policies, [])
        if snapshot_path.exists():
            if json.loads(snapshot_path.read_bytes()) != snapshot:
                raise ValueError('Run inputs changed; preserve this run and start a new version')
        else:
            save(snapshot_path, snapshot)
        waves, spent = [], Decimal(0)
        reservation_exceeded = False
        calls = sorted(directory.glob('call-*'))
        for i, call in enumerate(calls):
            if call.name != f'call-{i:06d}':
                raise ValueError('Execution history has a missing or unexpected call')
            request_path, result_path = call / 'requests.json', call / 'results.json'
            if not request_path.exists() or not result_path.exists():
                raise ValueError('Interrupted call has an unknown outcome; reconcile before resending')
            requests = json.loads(request_path.read_bytes())
            results = json.loads(result_path.read_bytes())
            waves.append({'requests': requests, 'results': results})
            # Reject incomplete persisted results before treating a call as done.
            replay(plan, root, registry, policies, waves)
            for record in results:
                if 'raw' in record:
                    cost = jev_results.usage_cost(record['raw'])
                    if cost is None:
                        raise ValueError('Historical call cost is unknown')
                    spent += cost
                    reservation_exceeded |= cost > Decimal('.01')
        while True:
            state = replay(plan, root, registry, policies, waves)
            save(directory / 'output.json', state['output'])
            save(directory / 'pending.json', state['next'])
            failed = any(r['status'] in {'execution_error', 'invalid_response'}
                         for r in state['output']['jobs'].values())
            ready = state['next']['requests']
            if failed or reservation_exceeded or not ready or spent + Decimal('.01') > cap:
                reason = ('failed_request' if failed else 'reservation_exceeded' if reservation_exceeded
                          else 'no_ready_jobs' if not ready else 'cost_cap')
                save(directory / 'summary.json', {'reported_cost': str(spent), 'stop_reason': reason,
                     'prepared_work_complete': state['output']['complete']})
                return state

            # Persist one physical call at a time so finished work is resumable.
            request = ready[0]
            call = directory / f'call-{len(waves):06d}'
            results = await dispatch([request], call, cap - spent)
            waves.append({'requests': [request], 'results': results})
            for record in results:
                if 'raw' in record:
                    cost = jev_results.usage_cost(record['raw'])
                    if cost is None:
                        raise ValueError('Call cost is unknown; reconcile before continuing')
                    spent += cost
                    reservation_exceeded |= cost > Decimal('.01')
            if all(r['status'] == 'not_sent' for r in results):
                state = replay(plan, root, registry, policies, waves)
                save(directory / 'summary.json', {'reported_cost': str(spent), 'stop_reason': 'not_sent',
                     'prepared_work_complete': state['output']['complete']})
                return state


def main():
    import argparse
    import asyncio
    from pipeline import core

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('registry', type=Path)
    parser.add_argument('policies', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--cap', type=Decimal, required=True, help='Total run cost cap in USD')
    args = parser.parse_args()
    read = lambda path: json.loads(path.read_bytes())
    state = asyncio.run(run(read(args.plan), core.ROOT, read(args.registry),
                            read(args.policies), args.output, args.cap))
    print(json.dumps({'prepared_work_complete': state['output']['complete'],
                      'ready_requests': len(state['next']['requests']),
                      'waiting_jobs': state['next']['waiting']}))


if __name__ == "__main__":
    main()
