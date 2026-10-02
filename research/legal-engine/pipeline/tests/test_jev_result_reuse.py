"""Request identity and consumer checks use real prepared requests and isolated caches."""
import copy
import json

import pytest

from pipeline import core, jev, jev_results as reuse, triage, registercheck
from .conftest import write_register


def saved_answer():
    write_register('T', n_undecided=1)
    sec = core.sections('T')[1]
    item = (sec['section_id'], sec, core.profile('T'), triage.inst_names(core.family('T')))
    request = jev.prepare(*item, core.questions())
    criteria = request['questions']['role']['criteria']
    choice = next(k for k in criteria if k != 'DECIDES')
    raw = {'model': request['pinned_build'], 'answers': {
        'role': {'type': 'choice', 'choice': choice, 'confidence': 1,
                 'probabilities': {k: int(k == choice) for k in criteria}},
        'chain_duty': {'type': 'noul', 'noul': 0}}}
    entry = reuse.envelope(request, raw, core.now())
    path = core.jdir('T') / 'jev/cache' / (reuse.fingerprint(request) + '.json')
    reuse.atomic_write(path, reuse.serialized(entry))
    return item, request, entry, path


def test_compatible_reuse_and_changed_source(root):
    item, request, entry, path = saved_answer()
    answers = jev.cached_answers('T', [item])
    assert answers[item[0]]['cache_hit'] is True
    assert answers[item[0]]['registry_version'] == request['registry_version']
    assert reuse.fingerprint(dict(reversed(list(request.items())))) == entry['request_hash']
    (core.ROOT / item[1]['text_file']).write_text('A different operative passage.')
    assert not jev.cached_answers('T', [item])
    assert json.loads(path.read_text()) == entry


@pytest.mark.parametrize('field', ['base_url', 'model', 'pinned_build', 'registry_version',
                                   'assembly_version', 'state', 'questions', 'question_versions'])
def test_identity_changes_reject_old_entry(root, field):
    _, request, entry, _ = saved_answer()
    changed = copy.deepcopy(request)
    changed[field] = {'changed': True} if isinstance(changed[field], dict) else changed[field] + '-changed'
    with pytest.raises(ValueError, match='identity mismatch'):
        reuse.validate_entry(entry, changed)


@pytest.mark.parametrize('defect', ['build', 'missing', 'extra', 'nan', 'bool', 'choice', 'probability', 'hash'])
def test_invalid_cache_never_becomes_an_answer(root, defect):
    item, _, entry, path = saved_answer()
    raw = entry['raw']
    if defect == 'build': raw['model'] = 'wrong'
    if defect == 'missing': del raw['answers']['chain_duty']
    if defect == 'extra': raw['answers']['unexpected'] = {}
    if defect == 'nan': raw['answers']['chain_duty']['noul'] = float('nan')
    if defect == 'bool': raw['answers']['chain_duty']['noul'] = False
    if defect == 'choice': raw['answers']['role']['choice'] = 'DECIDES'
    if defect == 'probability': del raw['answers']['role']['probabilities']['DECIDES']
    if defect == 'hash': entry['request_hash'] = 'wrong'
    path.write_text(json.dumps(entry))
    answers = jev.cached_answers('T', [item])
    assert not answers
    assert answers.outcomes[0]['status'] == 'cache_rejected'


def test_embedded_projection_cannot_override_current_cache(root):
    item, _, entry, path = saved_answer()
    rows = core.triage('T')
    triage.reroute('T', rows)
    valid = copy.deepcopy(rows[1]['jev'])
    assert valid['cache_key'] == entry['request_hash']
    rows[1]['jev']['chain_duty'] = .99
    triage.reroute('T', rows, {item[0]: rows[1]['jev']})
    assert rows[1]['jev'] == valid
    assert rows[1]['jev_history'][-1]['jev']['chain_duty'] == .99
    path.write_text('{broken')
    triage.reroute('T', rows)
    assert rows[1]['jev'] is None
    assert rows[1]['review_decision'] is None
    assert rows[1]['jev_history'][-1]['jev'] == valid


def test_register_rejects_embedded_only_answer_on_stated_row(root):
    saved_answer()
    d = registercheck.load('T')
    d['triage'][0]['jev'] = {'model': 'jev-1.13', 'cache_key': 'unverified'}
    assert any('embedded Jev record' in e for e in registercheck.check(d, strict=False))


def fake_provider(monkeypatch, response):
    sdk = pytest.importorskip('typesafe_sdk')
    calls = []

    class Client:
        def __init__(self, **kwargs):
            self.http = kwargs['http_client']

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            await self.http.aclose()

        async def system_one(self, **kwargs):
            calls.append(kwargs)
            for hook in self.http.event_hooks['request']:
                await hook(None)
            if isinstance(response, Exception):
                raise response
            return kwargs['response_model'].model_validate(copy.deepcopy(response))

    monkeypatch.setattr(sdk, 'AsyncTypeSafeClient', Client)
    monkeypatch.setattr(jev, 'api_key', lambda: 'test-key')
    return calls


def test_live_then_offline_reuse_retains_origin(root, monkeypatch):
    item, request, entry, path = saved_answer()
    path.unlink()
    calls = fake_provider(monkeypatch, entry['raw'])
    answers, usage = jev.run('T', [item])
    assert len(calls) == usage['requests'] == usage['physical_attempts'] == 1
    assert usage['unanswered'] == 0
    assert not answers[item[0]]['cache_hit']
    assert calls[0]['state'] == request['state']
    for qid, spec in request['questions'].items():
        wire = calls[0]['questions'][qid].model_dump(mode='json')
        assert wire['type'] == spec['primitive']
        assert wire['instructions'] == spec['instructions']
        assert wire['criteria'] == spec['criteria']
    monkeypatch.setattr(jev, 'api_key', lambda: pytest.fail('Cache hit requested credentials'))
    cached, hit_usage = jev.run('T', [item])
    assert len(calls) == 1
    assert hit_usage['requests'] == 0 and hit_usage['cache_hits'] == 1
    assert cached[item[0]]['created_at'] == answers[item[0]]['created_at']
    assert cached[item[0]]['origin'] == answers[item[0]]['origin']
    assert jev.cached_answers('T', [item])[item[0]] == cached[item[0]]
    assert len(core.read_jsonl(jev.paths('T')['dir'] / 'result-history.jsonl')) == 2
    assert len(list((jev.paths('T')['dir'] / 'result-snapshots').glob('*.jsonl'))) == 1


@pytest.mark.parametrize('defect', ['build', 'shape', 'cost', 'network'])
def test_failed_live_refresh_preserves_rejected_cache(root, monkeypatch, defect):
    item, _, entry, path = saved_answer()
    rejected = b'{broken old record'
    path.write_bytes(rejected)
    raw = entry['raw']
    if defect == 'build': raw['model'] = 'wrong-build'
    if defect == 'shape': raw['answers']['role']['probabilities'] = {}
    if defect == 'cost': raw['usage'] = {'cost': 'NaN'}
    response = RuntimeError('provider unavailable') if defect == 'network' else raw
    calls = fake_provider(monkeypatch, response)
    answers, usage = jev.run('T', [item])
    assert not answers and len(calls) == 1
    assert usage['errors'] == usage['unanswered'] == 1
    assert float(usage['spent_usd']) > 0
    assert usage['outcomes'][0]['lookup']['status'] == 'cache_rejected'
    assert path.read_bytes() == rejected
    exchange = core.read_jsonl(jev.paths('T')['exchanges'])[0]
    assert exchange['outcome']['status'] in {'execution_error', 'invalid_response'}
    assert not jev.cached_answers('T', [item])


def test_successful_recovery_archives_exact_corrupt_bytes(root, monkeypatch):
    item, _, entry, path = saved_answer()
    previous = b'\xffpartial write'
    path.write_bytes(previous)
    fake_provider(monkeypatch, entry['raw'])
    answers, usage = jev.run('T', [item])
    assert usage['answered'] == 1
    archived = list((jev.paths('T')['dir'] / 'replaced-cache').glob('*.json'))
    assert len(archived) == 1 and archived[0].read_bytes() == previous
    assert jev.cached_answers('T', [item])[item[0]]['cache_key'] == answers[item[0]]['cache_key']


@pytest.mark.parametrize('limit', [{'cap': 0}, {'ceiling': 0}])
def test_budget_refusal_is_explicitly_unanswered(root, monkeypatch, limit):
    item, _, entry, path = saved_answer()
    path.unlink()
    calls = fake_provider(monkeypatch, entry['raw'])
    answers, usage = jev.run('T', [item], **limit)
    assert not calls and not answers and usage['unanswered'] == 1
    assert usage['outcomes'][0]['status'] == 'not_sent'
    assert usage['stopped']


def test_atomic_failure_leaves_original_and_cleans_temp(tmp_path, monkeypatch):
    path = tmp_path / 'cache.json'
    path.write_bytes(b'original')
    def fail(*args):
        raise OSError('interrupted replacement')
    monkeypatch.setattr(reuse.os, 'replace', fail)
    with pytest.raises(OSError):
        reuse.atomic_write(path, 'replacement')
    assert path.read_bytes() == b'original'
    assert list(tmp_path.iterdir()) == [path]


def test_legacy_file_remains_explicitly_rejected(root):
    item, request, entry, path = saved_answer()
    path.unlink()
    old_key = jev.canonical_sha256({k: request[k] for k in ('model', 'questions', 'state')})
    old = path.with_name(old_key + '.json')
    old.write_text(json.dumps(entry['raw']))
    before = old.read_bytes()
    answers = jev.cached_answers('T', [item])
    assert not answers
    assert answers.outcomes[0]['legacy_cache_key'] == old_key
    assert old.read_bytes() == before


@pytest.mark.parametrize('size', [1, 3, 11])
def test_native_score_legend_matches_ordered_criteria(size):
    criteria = [{'level': i} for i in range(size)]
    request = {'pinned_build': 'pinned', 'questions': {'score': {'primitive': 'score', 'criteria': criteria}}}
    answer = {'type': 'score', 'score': 0, 'confidence': 1,
              'legend': {str(i): value for i, value in enumerate(criteria)},
              'probabilities': {str(i): int(i == 0) for i in range(size)}}
    raw = {'model': 'pinned', 'answers': {'score': answer}}
    reuse.validate(raw, request)
    del answer['legend']
    with pytest.raises(ValueError, match='legend'):
        reuse.validate(raw, request)
    answer['legend'] = {'0': 'different rubric'}
    with pytest.raises(ValueError, match='legend'):
        reuse.validate(raw, request)


@pytest.mark.parametrize('change', ['heading', 'instrument', 'scope', 'chain', 'exclusions', 'instructions',
                                   'criteria', 'question_version', 'global_rules'])
def test_prepared_input_change_invalidates_actual_lookup(root, change):
    item, _, _, _ = saved_answer()
    sid, sec, prof, names = copy.deepcopy(item)
    reg = copy.deepcopy(core.questions())
    if change == 'heading': sec['heading'] += ' changed'
    if change == 'instrument': names[sec['instrument']] += ' changed'
    if change == 'scope': prof.setdefault('jev', {})['scope'] = 'changed scope'
    if change == 'chain': prof.setdefault('jev', {})['chain_description'] = 'changed chain'
    if change == 'exclusions': prof.setdefault('aperture', {})['exclusions'] = ['changed regime']
    if change == 'instructions': reg['questions'][0]['prompt']['instructions'] += ' changed'
    if change == 'criteria': reg['questions'][0]['prompt']['criteria']['DECIDES'] += ' changed'
    if change == 'question_version': reg['questions'][0]['version'] += '-changed'
    if change == 'global_rules': reg['global_rules'].append('Changed rule')
    answers = jev.cached_answers('T', [(sid, sec, prof, names)], reg)
    assert not answers and answers.outcomes[0]['status'] == 'cache_miss'


def test_failed_rerun_drops_stale_projection_and_preserves_decision(root, monkeypatch):
    item, _, entry, path = saved_answer()
    rows = core.triage('T')
    triage.reroute('T', rows)
    rows[1]['review_decision'] = 'no_decision'
    core.write_jsonl(core.jdir('T') / 'triage.jsonl', rows)
    path.write_text('broken')
    fake_provider(monkeypatch, RuntimeError('unavailable'))
    assert triage.triage_main('T', rerun=True) == 1
    current = core.triage('T')[1]
    assert current['jev'] is None
    assert current['review_decision'] == 'no_decision'
    assert current['jev_history'][-1]['jev'] == rows[1]['jev']


def test_limited_triage_reports_deferred_instead_of_success(root, capsys):
    item, _, _, path = saved_answer()
    path.unlink()
    assert triage.triage_main('T', cached_only=True, limit=0) == 1
    assert '1 eligible sections deferred' in capsys.readouterr().out


def test_calibration_preserves_prior_report_and_selected_origin(root, monkeypatch):
    item, _, _, _ = saved_answer()
    pos = [item[:3]]
    monkeypatch.setattr(triage, 'gold', lambda code: (pos, [], []))
    report = core.jdir('T') / 'calibration.json'
    previous = b'{"historical report": "unaltered"}\n'
    report.write_bytes(previous)
    assert triage.calibrate_main('T', cached_only=True) == 1  # No negative population.
    saved = json.loads(report.read_text())
    selected = saved['selected_answers'][item[0]]
    assert selected['created_at'] and selected['response_hash'] and selected['origin']
    archives = list((core.jdir('T') / 'calibration-history').glob('*.json'))
    assert len(archives) == 1 and archives[0].read_bytes() == previous


@pytest.mark.parametrize('value', ['null', '[]', '{', '{"format":"wrong","format":"jev-result-2"}'])
def test_corrupt_json_shapes_reject_without_exception(root, value):
    item, _, _, path = saved_answer()
    path.write_text(value)
    answers = jev.cached_answers('T', [item])
    assert not answers and answers.outcomes[0]['status'] == 'cache_rejected'


def test_valid_shape_response_edit_requires_matching_response_identity(root):
    item, _, entry, path = saved_answer()
    entry['raw']['answers']['chain_duty']['noul'] = .5
    path.write_text(json.dumps(entry))
    assert not jev.cached_answers('T', [item])


def test_question_metadata_outside_active_request_does_not_invalidate(root):
    item, _, _, _ = saved_answer()
    registry = copy.deepcopy(core.questions())
    registry['quote_check']['prompt']['instructions'] = 'Unrelated task changed'
    registry['history'] = []
    assert jev.cached_answers('T', [item], registry)[item[0]]['cache_hit']


def test_batch_cannot_use_stale_scores_without_triage(root):
    from pipeline import batch
    item, _, _, path = saved_answer()
    rows = core.triage('T')
    triage.reroute('T', rows)
    rows[1]['jev']['chain_duty'] = .99
    rows[1]['tier'] = 'high'
    core.write_jsonl(core.jdir('T') / 'triage.jsonl', rows)
    (core.jdir('T') / 'decisions/batch_1.json').unlink()
    path.unlink()
    planned = batch.plan('T')[0][0]
    assert planned['jev_p_decides'] is None and planned['jev_chain_duty'] is None
    # Read-only planning preserves the old observation for explicit later retirement.
    assert core.triage('T')[1]['jev']['chain_duty'] == .99


def test_duplicate_request_and_missing_text_are_explicit(root):
    item, _, _, _ = saved_answer()
    with pytest.raises(core.PipelineError, match='Duplicate'):
        jev.cached_answers('T', [item, item])
    (core.ROOT / item[1]['text_file']).unlink()
    answers = jev.cached_answers('T', [item])
    assert not answers and answers.outcomes[0]['status'] == 'preparation_error'


def test_legacy_execution_guard_never_requests_credentials():
    import asyncio
    import importlib.util
    module_path = core.PKG.parent / 'register/jev_triage.py'
    spec = importlib.util.spec_from_file_location('historical_jev', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with pytest.raises(RuntimeError, match='historical-only'):
        asyncio.run(module.run(['unrequested']))


def test_calibration_limit_preserves_population_accounting(root, monkeypatch):
    item, _, _, _ = saved_answer()
    monkeypatch.setattr(triage, 'gold', lambda code: ([item[:3]], [], []))
    assert triage.calibrate_main('T', cached_only=True, limit=0) == 1
    report = core.read_json(core.jdir('T') / 'calibration.json')
    assert report['population'] == {'positives': 1, 'negatives': 0}
    assert report['deferred_by_limit'] == 1 and report['answered'] == 0
