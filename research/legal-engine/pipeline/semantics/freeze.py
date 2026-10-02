"""Freeze reviewed preparation, independent expectations and executable inputs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pipeline import jev_results
from pipeline.design.task_evaluation.run import save
from .prepare import compile_proposal
from .plan import source_text
from .replay import replay
from .run import implementation_identity
from .evaluate import evaluate

FILES = {'preparation.json', 'expectations.json', 'review.json', 'registry.json', 'policies.json',
         'plan.json', 'evaluation_mapping.json'}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def source_selections(plan, expectations):
    evidence = expectations.get('evidence')
    if not isinstance(evidence, dict) or not evidence:
        raise ValueError('Independent expectations require exact source evidence')
    return plan['sources'] + [dict(row, quote=row['text']) for row in evidence.values()]


def create(preparation, expectations, review, registry, policies, root, destination, *, phase, rationale,
           evaluation_mapping):
    if phase not in {'development', 'heldout'} or not isinstance(rationale, str) or not rationale.strip():
        raise ValueError('Evaluation phase and policy rationale are required')
    paths = dict(zip(('preparation.json', 'expectations.json', 'review.json', 'registry.json', 'policies.json'),
                     (preparation, expectations, review, registry, policies)))
    paths['evaluation_mapping.json'] = evaluation_mapping
    raw = {key: Path(path).read_bytes() for key, path in paths.items()}
    data = {key: json.loads(value) for key, value in raw.items()}
    assessment = data['review.json']
    if (assessment.get('preparation_sha256') != digest(raw['preparation.json']) or
            assessment.get('expectations_sha256') != digest(raw['expectations.json'])):
        raise ValueError('Review does not bind these preparation and expectation versions')
    if (assessment.get('status') != 'ready_for_evaluation' or assessment.get('material_findings') != []
            or assessment.get('model_responses_seen') is not False):
        raise ValueError('Preparation review has open findings or response exposure')
    if not assessment.get('reviewer') or not assessment.get('coverage_assessment'):
        raise ValueError('Independent reviewer identity and coverage assessment are required')
    plan = compile_proposal(data['preparation.json'], root)
    initial = replay(plan, root, data['registry.json'], data['policies.json'], [])
    evaluate(initial['output'], data['expectations.json'], data['evaluation_mapping.json'])
    # Read every source before writing the bundle; avoid mixed versions.
    sources = {}
    for selection in source_selections(plan, data['expectations.json']):
        source_text(selection, root)
        path = selection['path']
        if Path(path).is_absolute() or '..' in Path(path).parts:
            raise ValueError('Frozen source paths must be relative within the research root')
        contents = (Path(root) / path).read_bytes()
        if digest(contents) != selection['sha256']:
            raise ValueError('Source changed while preparing freeze')
        sources[path] = contents
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    for name, contents in raw.items():
        (destination / name).write_bytes(contents)
    save(destination / 'plan.json', plan)
    for name, contents in sources.items():
        target = destination / 'sources' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)
    manifest = {'format': 'section-semantics-freeze-1', 'phase': phase,
                'policy_rationale': rationale, 'implementation': implementation_identity(),
                'files': {name: digest((destination / name).read_bytes()) for name in sorted(FILES)},
                'sources': {name: digest(value) for name, value in sources.items()}}
    save(destination / 'manifest.json', manifest)
    return manifest


def read(directory):
    directory = Path(directory)
    manifest = json.loads((directory / 'manifest.json').read_bytes())
    if manifest.get('format') != 'section-semantics-freeze-1' or set(manifest.get('files', {})) != FILES:
        raise ValueError('Invalid or incomplete frozen bundle')
    if manifest.get('implementation') != implementation_identity():
        raise ValueError('Frozen implementation differs from current code')
    data = {}
    for name, expected in manifest['files'].items():
        raw = (directory / name).read_bytes()
        if digest(raw) != expected:
            raise ValueError('Frozen input changed: ' + name)
        data[name] = json.loads(raw)
    source_root = (directory / 'sources').resolve()
    selections = source_selections(data['plan.json'], data['expectations.json'])
    expected_sources = {row['path']: row['sha256'] for row in selections}
    if manifest.get('sources') != expected_sources:
        raise ValueError('Frozen source coverage differs from plan')
    for name, expected in expected_sources.items():
        path = (source_root / name).resolve()
        if not path.is_relative_to(source_root) or digest(path.read_bytes()) != expected:
            raise ValueError('Frozen source changed or escaped bundle')
    for selection in selections:
        source_text(selection, source_root)
    if compile_proposal(data['preparation.json'], source_root) != data['plan.json']:
        raise ValueError('Frozen plan differs from preparation')
    initial = replay(data['plan.json'], source_root, data['registry.json'], data['policies.json'], [])
    evaluate(initial['output'], data['expectations.json'], data['evaluation_mapping.json'])
    return data, source_root
