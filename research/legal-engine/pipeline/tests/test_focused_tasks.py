import hashlib
import json

import pytest

from pipeline.design.task_evaluation.tasks import prepare, diagnostic


@pytest.fixture
def prepared(tmp_path):
    text = 'For this chapter, tenant means an occupant under a rental agreement.'
    path = tmp_path / 'source.txt'
    path.write_text(text)
    case = {'id': 'one', 'task': 'definition_present', 'state': {'passage': text},
            'sources': {'passage': {'path': 'source.txt', 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                                    'start': 0, 'end': len(text)}}}
    registry = {'model': 'test', 'pinned_build': 'test-build', 'base_url': 'https://example.invalid'}
    return case, registry, tmp_path


def test_source_mutation_and_metadata_rejected(prepared):
    case, registry, root = prepared
    request = prepare(case, root, registry)
    assert request['expected_wire']['questions']['judgment']['type'] == 'noul'
    assert 'sources' not in request['expected_wire']['state']
    case['state']['source_label'] = 'Section 3'
    with pytest.raises(ValueError, match='semantic fields'):
        prepare(case, root, registry)
    del case['state']['source_label']
    (root / 'source.txt').write_text('replacement')
    with pytest.raises(ValueError, match='Source changed'):
        prepare(case, root, registry)


def test_wrong_selection_rejected(prepared):
    case, registry, root = prepared
    case['sources']['passage']['start'] = 1
    with pytest.raises(ValueError, match='differs from source'):
        prepare(case, root, registry)


def test_response_failure_not_negative(prepared):
    case, registry, root = prepared
    request = prepare(case, root, registry)
    with pytest.raises(ValueError, match='answer IDs'):
        diagnostic({'model': 'test-build', 'answers': {}}, request)
    raw = {'model': 'test-build', 'answers': {'judgment': {'type': 'noul', 'noul': .5}}}
    assert diagnostic(raw, request) == 'UNDECIDED'
    raw['answers']['judgment']['noul'] = False
    with pytest.raises(ValueError, match='Invalid Noul'):
        diagnostic(raw, request)


def test_runner_captures_native_wire_and_charged_invalid_response(prepared, monkeypatch):
    import asyncio
    from decimal import Decimal
    import httpx2
    from pipeline.design.task_evaluation.run import execute
    from pipeline import jev

    case, registry, root = prepared
    request = prepare(case, root, registry)
    original = httpx2.AsyncClient
    received = []

    async def handler(http_request):
        received.append(json.loads(http_request.content))
        return httpx2.Response(200, json={'model': 'wrong-build', 'answers': {},
                                          'usage': {'cost': .002}})

    monkeypatch.setattr(httpx2, 'AsyncClient', lambda **kw: original(transport=httpx2.MockTransport(handler), **kw))
    monkeypatch.setattr(jev, 'api_key', lambda: 'test-placeholder')
    results = asyncio.run(execute([request, request], root / 'run', Decimal('.1')))
    assert received == [request['expected_wire']]
    assert results[0]['transport'][0]['body'] == request['expected_wire']
    assert results[0]['status'] == 'invalid_response'
    assert results[1]['status'] == 'not_sent'
    assert json.loads((root / 'run/summary.json').read_text())['reported_cost'] == '0.002'
    assert 'test-placeholder' not in (root / 'run/results.json').read_text()


def test_transport_mismatch_never_dispatched(prepared, monkeypatch):
    import asyncio
    from decimal import Decimal
    import httpx2
    from pipeline.design.task_evaluation.run import execute
    from pipeline import jev

    case, registry, root = prepared
    request = prepare(case, root, registry)
    request['expected_wire']['state'] = {'passage': 'tampered'}
    original = httpx2.AsyncClient
    received = []

    async def handler(http_request):
        received.append(http_request)
        raise AssertionError('Must not send mismatched body')

    monkeypatch.setattr(httpx2, 'AsyncClient', lambda **kw: original(transport=httpx2.MockTransport(handler), **kw))
    monkeypatch.setattr(jev, 'api_key', lambda: 'test-placeholder')
    results = asyncio.run(execute([request], root / 'run', Decimal('.1')))
    assert received == []
    assert results[0]['status'] == 'execution_error'


def test_freeze_binds_review_and_detects_mutation(prepared, monkeypatch):
    from pipeline.design.task_evaluation.freeze import freeze
    from pipeline.design.task_evaluation.run import read_frozen
    from pipeline.design.task_evaluation.tasks import HERE, digest
    from pipeline import core

    case, registry, root = prepared
    cases_path = root / 'cases.json'
    cases_path.write_text(json.dumps({'cases': [case]}))
    review = {'cases_sha256': digest(cases_path), 'contracts_sha256': digest(HERE / 'contracts.json'),
              'material_findings': [], 'cases': [{'id': 'one', 'expected': 'YES', 'reason': 'Express definition.'}]}
    review_path = root / 'review.json'
    review_path.write_text(json.dumps(review))
    monkeypatch.setattr(core, 'questions', lambda: registry)
    with pytest.raises(ValueError):
        altered = dict(review, cases_sha256='wrong')
        review_path.write_text(json.dumps(altered))
        freeze(cases_path, review_path, root / 'bad', core.ROOT)
    # Directly exercise runner integrity against a minimal bundle.
    bundle = root / 'bundle'
    bundle.mkdir()
    (bundle / 'requests.json').write_text('[]')
    manifest = {'files': {'requests.json': digest(bundle / 'requests.json')}, 'implementation': {}}
    (bundle / 'manifest.json').write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match='Incomplete frozen manifest'):
        read_frozen(bundle, root)
    (bundle / 'requests.json').write_text('[{}]')
    with pytest.raises(ValueError, match='Incomplete frozen manifest'):
        read_frozen(bundle, root)


def test_uncertainty_is_per_task_and_does_not_treat_gaps_as_answers():
    from pipeline.design.task_evaluation.evaluate import upper_error_bound, evaluate
    assert upper_error_bound(0, 60) == pytest.approx(1 - .05**(1/60))
    cases = [{'id': 'x', 'task': 'definition_present', 'family': 'statute', 'source_cluster': 'a'}]
    result = evaluate(cases, [{'id': 'x', 'expected': 'YES'}], [{'case_id': 'x'}],
                      [{'case_id': 'x', 'status': 'execution_error'}])
    metric = result['metrics']['definition_present']
    assert metric['answered'] == 0 and metric['execution_gaps'] == 1
    assert metric['conditional_independent_case_upper_error_95'] is None


def test_complete_freeze_roundtrip_and_source_manifest_integrity(prepared, monkeypatch):
    import importlib
    import shutil
    from pipeline.design.task_evaluation.tasks import HERE, digest
    from pipeline.design.task_evaluation.run import read_frozen
    from pipeline import core
    freeze_module = importlib.import_module('pipeline.design.task_evaluation.freeze')
    case, registry, root = prepared
    copied_here = root / 'pipeline/design/task_evaluation'
    copied_here.mkdir(parents=True)
    for name in ['tasks.py', 'run.py', 'freeze.py', 'evaluate.py', 'contracts.json']:
        shutil.copyfile(HERE / name, copied_here / name)
    for name in ['jev.py', 'jev_results.py']:
        shutil.copyfile(core.ROOT / 'pipeline' / name, root / 'pipeline' / name)
    monkeypatch.setattr(freeze_module, 'HERE', copied_here)
    monkeypatch.setattr(core, 'questions', lambda: registry)
    cases = root / 'cases.json'
    cases.write_text(json.dumps({'cases': [case]}))
    review = root / 'review.json'
    review.write_text(json.dumps({'cases_sha256': digest(cases), 'contracts_sha256': digest(copied_here / 'contracts.json'),
        'reviewer': 'independent-test', 'author_labels_seen': False, 'model_responses_seen': False,
        'material_findings': [], 'cases': [{'id': 'one', 'expected': 'YES', 'reason': 'Explicit means clause.'}]}))
    requests = freeze_module.freeze(cases, review, root / 'bundle', root)
    assert read_frozen(root / 'bundle', root) == requests
    assert (root / 'bundle/cases.json').read_bytes() == cases.read_bytes()
    (root / 'bundle/contracts.json').write_text('{}')
    with pytest.raises(ValueError, match='Frozen input changed'):
        read_frozen(root / 'bundle', root)


def test_batch_comparison_recomputes_raw_and_rejects_bad_transport(prepared):
    from copy import deepcopy
    from pipeline.design.task_evaluation.batching import group_requests, compare
    from pipeline import jev_results
    case, registry, root = prepared
    one = prepare(case, root, registry)
    second_case = deepcopy(case)
    second_case['id'] = 'two'
    two = prepare(second_case, root, registry)
    batches = group_requests([one, two])
    assert len(batches) == 1

    def record(request, answers):
        wire = request['expected_wire']
        body = json.dumps(wire)
        return {'case_id': request['case_id'], 'request_hash': request['request_hash'],
                'status': 'answered', 'diagnostic': 'NO',
                'raw': {'model': 'test-build', 'answers': answers},
                'transport': [{'body': wire, 'body_text': body,
                               'body_sha256': hashlib.sha256(body.encode()).hexdigest()}]}
    separate = [record(r, {'judgment': {'type': 'noul', 'noul': .8}}) for r in [one, two]]
    batched = [record(batches[0], {k: {'type': 'noul', 'noul': .2} for k in ['one', 'two']})]
    labels = [{'id': k, 'expected': 'NO'} for k in ['one', 'two']]
    result = compare(batches, batched, separate, labels)
    assert all(r['separate'] == 'YES' and r['batched'] == 'NO' for r in result['rows'])
    with pytest.raises(ValueError, match='Duplicate'):
        compare(batches, batched, separate + [separate[0]], labels)
    separate[0]['transport'] = []
    with pytest.raises(ValueError, match='transport mismatch'):
        compare(batches, batched, separate, labels)
