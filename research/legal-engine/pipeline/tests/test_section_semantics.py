from copy import deepcopy
import hashlib
import json
import asyncio

import pytest

from pipeline import jev_results
from pipeline.semantics import plan, compose
from pipeline.semantics.replay import replay


@pytest.fixture
def work(tmp_path):
    text = 'A must give notice. An emergency waives advance notice.'
    (tmp_path / 'source.txt').write_text(text)
    evidence = {'id': 'section', 'path': 'source.txt', 'sha256': hashlib.sha256(text.encode()).hexdigest(),
                'start': 0, 'end': len(text), 'quote': text}
    job = {'id': 'notice', 'evidence': ['section'], 'question': {'primitive': 'noul',
           'instructions': 'Does the first sentence require A to give notice?'}, 'after': []}
    second = {'id': 'waiver', 'evidence': ['section'], 'question': {'primitive': 'noul',
              'instructions': 'Does the second sentence waive advance notice for an emergency?'},
              'after': ['notice'], 'when': [{'job': 'notice', 'answer': True}]}
    assertion = {'id': 'notice_duty', 'kind': 'duty', 'value': {'actor': 'A', 'action': 'give notice'},
                 'evidence': ['section'], 'established_by': [{'job': 'notice', 'answer': True}],
                 'field_licenses': {'$kind': ['notice'], 'actor': ['notice'], 'action': ['notice']}}
    return {'format': 'section-semantics-1', 'id': 'example', 'sources': [evidence],
            'jobs': [job, second], 'assertions': [assertion]}, tmp_path


def result(work, answer=True, status='answered'):
    return {'plan_hash': jev_results.fingerprint(work), 'status': status, 'answer': answer}


def registry():
    return {'base_url': 'https://example.invalid', 'model': 'model', 'pinned_build': 'build'}


def test_unlicensed_extra_semantics_rejected(work):
    value, root = work
    value['assertions'][0]['value']['conditions'] = {'operator': 'all', 'terms': ['emergency', 'absence']}
    with pytest.raises(ValueError, match='Every semantic field'):
        plan.validate(value, root)


def test_dependency_wait_and_negative_gate_differ(work):
    value, root = work
    first = plan.requests(value, root, registry(), {})
    assert len(first['requests']) == 1 and first['waiting'] == ['waiver']
    unknown = plan.requests(value, root, registry(), {'notice': result(value, status='uncertain')})
    assert unknown['waiting'] == ['waiver'] and not unknown['inapplicable']
    false = plan.requests(value, root, registry(), {'notice': result(value, False)})
    assert false['inapplicable'] == ['waiver'] and not false['requests']


def test_source_and_parent_change_invalidate(work):
    value, root = work
    outcome = result(value)
    value['jobs'][0]['question']['instructions'] += ' Consider the whole passage.'
    with pytest.raises(ValueError, match='stale predecessor'):
        plan.requests(value, root, registry(), {'notice': outcome})
    (root / 'source.txt').write_text('Changed law')
    with pytest.raises(ValueError, match='Source version changed'):
        plan.validate(value, root)


def test_independent_jobs_share_state_but_dependent_do_not(work):
    value, root = work
    value['jobs'][1]['after'] = []
    value['jobs'][1]['when'] = []
    wave = plan.requests(value, root, registry(), {})
    assert len(wave['requests']) == 1
    assert set(wave['requests'][0]['identity']['questions']) == {'notice', 'waiver'}
    assert wave['requests'][0]['expected_wire']['state'] == [value['sources'][0]['quote']]


def test_dependent_question_receives_selected_meaning(work):
    value, root = work
    value['jobs'][0]['question'] = {'primitive': 'choice', 'instructions': 'Which action is required?',
                                   'criteria': {'notice': 'Give notice', 'entry': 'Enter the dwelling'}}
    value['jobs'][1]['when'] = []
    value['jobs'][1]['context_from'] = [{'job': 'notice', 'name': 'required_action'}]
    value['assertions'][0]['established_by'][0]['answer'] = 'notice'
    request = plan.requests(value, root, registry(), {'notice': result(value, 'notice')})['requests'][0]
    context = request['expected_wire']['state']['prior_judgments']['required_action']
    assert context == {'question': 'Which action is required?', 'answer': 'notice',
                       'selected_meaning': 'Give notice'}
    value['jobs'][1]['context_from'][0]['job'] = 'waiver'
    with pytest.raises(ValueError, match='declared predecessor'):
        plan.validate(value, root)


def test_structured_predecessor_fields_use_actual_answers(work):
    value, root = work
    value['jobs'][0]['licenses'] = [
        {'answer': True, 'target': 'conditions.notice.predicate', 'value': 'Notice is required',
         'operation': 'establish_field_only'},
        {'answer': False, 'target': 'conditions.notice.predicate', 'value': None,
         'operation': 'reject_only'}]
    value['jobs'][1]['when'] = []
    value['jobs'][1]['state_template'] = {
        'passage': {'evidence_ref': 'section'},
        'previous': {'from_actual_results': [{'job': 'notice', 'field': 'conditions.notice'}]}}
    request = plan.requests(value, root, registry(), {'notice': result(value, False)})['requests'][0]
    selected = request['expected_wire']['state']['previous'][0]['assignments']
    assert selected == [{'target': 'conditions.notice.predicate', 'operation': 'reject_only', 'value': None}]
    assert 'Notice is required' not in json.dumps(request['expected_wire']['state'])


def test_conflicting_field_assignments_remain_incomplete(work):
    value, root = work
    for i, job in enumerate(value['jobs']):
        job['licenses'] = [{'answer': True, 'target': 'records.notice.actor',
                            'value': ['landlord', 'tenant'][i], 'operation': 'establish_field_only'}]
    outcomes = {job['id']: result(value) for job in value['jobs']}
    output = compose.compose(value, root, outcomes)
    assert {row['status'] for row in output['field_assignments']} == {'conflicting'}
    assert not output['complete']


def test_consumer_computes_condition_groups_without_source_text():
    from pipeline.semantics.consumer import evaluate_conditions
    def assignment(target, value):
        return {'target': target, 'value': value, 'status': 'supported', 'job': target,
                'evidence': ['opaque-source-binding']}
    output = {'format': 'section-semantics-output-1', 'plan_hash': 'test', 'field_assignments': [
        assignment('conditions.return.timely.predicate', 'Claim is timely'),
        assignment('conditions.return.paid.predicate', 'Storage costs are paid'),
        assignment('conditions.return.waived.predicate', 'Storage costs are waived'),
        assignment('conditions.return.cost', {'operator': 'any', 'children': ['paid', 'waived']}),
        assignment('conditions.return.root', {'operator': 'all', 'children': ['timely', 'cost']}),
        assignment('relations.return.applies_under.root', 'branch_trigger')]}
    facts = {'conditions.return.timely.predicate': True, 'conditions.return.paid.predicate': False}
    assert evaluate_conditions(output, facts)['branches'][0]['condition']['value'] is None
    facts['conditions.return.waived.predicate'] = True
    assert evaluate_conditions(output, facts)['branches'][0]['condition']['value'] is True
    facts['conditions.return.timely.predicate'] = False
    assert evaluate_conditions(output, facts)['branches'][0]['condition']['value'] is False
    facts['conditions.return.timely.predicate'] = 'false'
    with pytest.raises(ValueError, match='Boolean or unknown'):
        evaluate_conditions(output, facts)


def test_consumer_does_not_select_a_conflicting_field():
    from pipeline.semantics.consumer import fields
    output = {'format': 'section-semantics-output-1', 'field_assignments': [
        {'target': 'records.notice.actor', 'value': actor, 'status': 'supported',
         'job': actor, 'evidence': ['opaque']} for actor in ['landlord', 'tenant']]}
    indexed = fields(output)
    assert indexed['values'] == {}
    assert indexed['open_items'][0]['status'] == 'conflicting'


def test_conditional_waiver_uses_explicit_paths_and_preserves_facts():
    from pipeline.semantics.consumer import evaluate_conditions
    def assignment(target, value):
        return {'target': target, 'value': value, 'status': 'supported', 'job': target, 'evidence': ['source']}
    output = {'format': 'section-semantics-output-1', 'plan_hash': 'test', 'field_assignments': [
        assignment('conditions.base.paid.predicate', 'Payment made'),
        assignment('conditions.waiver.eligible.predicate', 'Waiver applies'),
        assignment('conditions.scope.covered.predicate', 'Regime covers case'),
        assignment('conditions.base.root', {'operator': 'all', 'children': ['paid']}),
        assignment('relations.base.applies_under.root', 'branch_trigger'),
        assignment('relations.waiver', {'execution': {'operation': 'set_predicate',
                   'when': 'conditions.waiver.eligible', 'target': 'conditions.base.paid', 'value': True}}),
        assignment('relations.scope', {'execution': {'operation': 'require_condition',
                   'condition': 'conditions.scope.covered', 'target': 'conditions.base.root'}})]}
    facts = {'conditions.base.paid.predicate': False, 'conditions.scope.covered.predicate': True}
    def condition():
        return evaluate_conditions(output, facts)['branches'][0]['condition']
    assert condition()['value'] is None
    facts['conditions.waiver.eligible.predicate'] = True
    assert condition()['value'] is True
    assert facts['conditions.base.paid.predicate'] is False
    facts['conditions.scope.covered.predicate'] = False
    assert condition()['value'] is False
    facts['conditions.scope.covered.predicate'] = True
    facts['conditions.waiver.eligible.predicate'] = False
    assert condition()['value'] is False
    facts['conditions.waiver.eligible.predicate'] = True
    output['field_assignments'].append(assignment('relations.contradictory_effect', {'execution': {
        'operation': 'set_predicate', 'when': 'conditions.waiver.eligible',
        'target': 'conditions.base.paid', 'value': False}}))
    assert condition()['value'] is None


def test_descriptive_relationship_name_is_not_executed():
    from pipeline.semantics.consumer import evaluate_conditions
    output = {'format': 'section-semantics-output-1', 'plan_hash': 'test', 'field_assignments': [
        {'status': 'supported', 'target': 'relations.exception', 'job': 'j', 'evidence': ['s'],
         'value': {'execution': {'operation': 'apply_exception_somehow'}}}]}
    result = evaluate_conditions(output, {})
    assert result['open_items'][0]['status'] == 'unsupported_relationship_operation'


def test_cure_blocks_condition_without_reversing_it_into_a_requirement():
    from pipeline.semantics.consumer import evaluate_conditions
    def row(target, value):
        return {'status': 'supported', 'target': target, 'value': value, 'job': target, 'evidence': ['s']}
    output = {'format': 'section-semantics-output-1', 'plan_hash': 'test', 'field_assignments': [
        row('conditions.termination.notice.predicate', 'Required notice completed'),
        row('conditions.termination.root', {'operator': 'all', 'children': ['notice']}),
        row('conditions.cure.timely.predicate', 'Timely sufficient cure completed'),
        row('relations.termination.applies_under.root', 'branch_trigger'),
        row('relations.cure_blocks', {'execution': {'operation': 'block_condition',
            'when': 'conditions.cure.timely', 'target': 'conditions.termination.root'}})]}
    facts = {'conditions.termination.notice.predicate': True}
    def value():
        return evaluate_conditions(output, facts)['branches'][0]['condition']['value']
    assert value() is None
    facts['conditions.cure.timely.predicate'] = True
    assert value() is False
    facts['conditions.cure.timely.predicate'] = False
    assert value() is True
    facts['conditions.termination.notice.predicate'] = False
    assert value() is False


def test_blocker_exception_preserves_base_prerequisites_and_unrelated_branches():
    from pipeline.semantics.consumer import evaluate_conditions
    def row(target, value):
        return {'status': 'supported', 'target': target, 'value': value, 'job': target, 'evidence': ['s']}
    output = {'format': 'section-semantics-output-1', 'plan_hash': 'test', 'field_assignments': [
        row('conditions.termination.notice.predicate', 'Required notice completed'),
        row('conditions.cure.timely.predicate', 'Timely sufficient cure'),
        row('conditions.repeat.qualifies.predicate', 'Repeat violation qualifies for no-cure route'),
        row('conditions.damages.loss.predicate', 'Recoverable loss established'),
        row('relations.termination.applies_under.notice', 'branch_trigger'),
        row('relations.damages.applies_under.loss', 'branch_trigger'),
        row('relations.cure', {'execution': {'operation': 'block_condition',
            'when': 'conditions.cure.timely', 'unless': 'conditions.repeat.qualifies',
            'target': 'conditions.termination.notice'}})]}
    # Exhaust all known/unknown combinations; the exception never supplies notice.
    for notice in (True, False, None):
        for cure in (True, False, None):
            for repeat in (True, False, None):
                facts = {'conditions.termination.notice.predicate': notice,
                         'conditions.cure.timely.predicate': cure,
                         'conditions.repeat.qualifies.predicate': repeat,
                         'conditions.damages.loss.predicate': True}
                result = evaluate_conditions(output, facts)
                possible = {n and not (c and not r)
                    for n in ([False, True] if notice is None else [notice])
                    for c in ([False, True] if cure is None else [cure])
                    for r in ([False, True] if repeat is None else [repeat])}
                expected = possible.pop() if len(possible) == 1 else None
                branches = {b['record']: b['condition']['value'] for b in result['branches']}
                assert branches == {'termination': expected, 'damages': True}
                assert facts['conditions.cure.timely.predicate'] is cure


def test_requirement_bundle_resolves_fields_not_case_compliance():
    from pipeline.semantics.consumer import evaluate_conditions
    def row(target, value):
        return {'status': 'supported', 'target': target, 'value': value, 'job': target, 'evidence': ['s']}
    output = {'format': 'section-semantics-output-1', 'plan_hash': 'test', 'field_assignments': [
        row('records.entry.action', 'Enter for work'),
        row('records.times.action', 'Use agreed time window'),
        row('conditions.entry.specified.predicate', 'An entry window was specified'),
        row('relations.times', {'execution': {'operation': 'attach_requirements', 'target': 'records.entry',
            'combine': 'all', 'requirements': [{'kind': 'permitted_time', 'path': 'records.times.action',
                                               'when': 'conditions.entry.specified'}]}})]}
    def item(facts):
        return evaluate_conditions(output, facts)['requirement_bundles'][0]['requirements'][0]
    assert item({})['status'] == 'unresolved'
    resolved = item({'conditions.entry.specified.predicate': True})
    assert resolved['status'] == 'required'
    assert resolved['selection']['fields'] == {'records.times.action': 'Use agreed time window'}
    assert resolved['case_compliance'] == 'not_evaluated'
    assert item({'conditions.entry.specified.predicate': False})['status'] == 'not_applicable'


def test_prefix_selection_does_not_claim_complete_record():
    from pipeline.semantics.requirements import select
    indexed = {'values': {'records.notice.actor': 'landlord'},
               'bindings': {'records.notice.actor': [{'job': 'j', 'evidence': ['s']}]}, 'open_items': []}
    assert select(indexed, 'records.notice')['selection_contract_missing']
    result = select(indexed, 'records.notice', ['records.notice.actor', 'records.notice.content'])
    assert result['status'] == 'unresolved' and result['missing_fields'] == ['records.notice.content']


def test_legal_relationship_cycles_are_not_execution_cycles(work):
    value, root = work
    other = deepcopy(value['assertions'][0])
    other['id'] = 'related'
    other['links'] = ['notice_duty']
    other['field_licenses']['$links'] = ['notice']
    value['assertions'][0]['links'] = ['related']
    value['assertions'][0]['field_licenses']['$links'] = ['notice']
    value['assertions'].append(other)
    assert plan.validate(value, root)
    value['jobs'][0]['after'] = ['waiver']
    with pytest.raises(ValueError, match='Cyclic semantic dependencies'):
        plan.validate(value, root)


def test_unanswered_never_promotes_candidate(work):
    value, root = work
    output = compose.compose(value, root, {})
    assert output['records'][0]['status'] == 'unresolved'
    assert not output['complete']
    output = compose.compose(value, root, {'notice': result(value, False),
                                         'waiver': result(value, status='not_applicable')})
    assert output['records'][0]['status'] == 'not_supported'
    assert output['complete']


def execution(request, probability):
    body = json.dumps(request['expected_wire'])
    return {'case_id': request['case_id'], 'request_hash': request['request_hash'],
            'status': 'answered', 'transport': [{'body': request['expected_wire'],
            'body_text': body, 'body_sha256': hashlib.sha256(body.encode()).hexdigest()}],
            'raw': {'model': 'build', 'answers': {key: {'type': 'noul', 'noul': probability}
                    for key in request['identity']['questions']}}}


def test_replay_derives_answers_and_rejects_changed_transport(work):
    value, root = work
    policies = {j['id']: {'false_at_most': .1, 'true_at_least': .9} for j in value['jobs']}
    request = plan.requests(value, root, registry(), {})['requests'][0]
    record = execution(request, .99)
    # Cached interpretations must not establish the result.
    record['diagnostics'] = {'notice': False}
    waves = [{'requests': [request], 'results': [record]}]
    first = replay(value, root, registry(), policies, waves)
    assert first['output']['jobs']['notice']['answer'] is True
    assert first['next']['requests'][0]['case_id'] == 'waiver'
    record['transport'][0]['body_text'] = '{}'
    with pytest.raises(ValueError, match='transport bytes'):
        replay(value, root, registry(), policies, waves)


def test_invalid_policy_is_rejected_before_any_response(work):
    value, root = work
    policies = {j['id']: {'false_at_most': .9, 'true_at_least': .1} for j in value['jobs']}
    with pytest.raises(ValueError, match='must not overlap'):
        replay(value, root, registry(), policies, [])


def test_evaluation_counts_omissions_and_requires_actual_case_output():
    from pipeline.semantics.evaluate import evaluate, requirements
    expected = {'components': [{'id': 'C1', 'expected': {'actor': 'tenant', 'limit': None}}],
                'relationships': [{'from': 'C1', 'to': 'C2', 'type': 'exception'}],
                'operating_cases': [{'id': 'case1', 'expected_outputs': ['release']}],
                'negative_controls': ['No invented charge']}
    output = {'format': 'section-semantics-output-1', 'plan_hash': 'plan', 'field_assignments': [
        {'status': 'supported', 'target': 'records.return.actor', 'value': 'tenant', 'job': 'j', 'evidence': ['s']}]}
    mapping = {'format': 'section-semantics-evaluation-mapping-1', 'plan_hash': 'plan',
               'expectations_hash': jev_results.fingerprint(expected), 'requirements': {
                   'component:C1/actor': {'checks': [{'kind': 'field', 'target': 'records.return.actor', 'expected': 'tenant'}]},
                   'component:C1/limit': {'checks': [{'kind': 'field', 'target': 'records.return.limit', 'expected': None}]},
                   'case:case1/expected_outputs/0': {'checks': [{'kind': 'case', 'case_id': 'case1',
                                                               'pointer': '/release', 'expected': True}]}}}
    result = evaluate(output, expected, mapping)
    assert result['denominator'] == len(requirements(expected)) == 5
    assert result['counts'] == {'correct': 1, 'missing': 2, 'unmapped': 2}
    assert not result['all_requirements_met']
    result = evaluate(output, expected, mapping, case_outputs={'case1': {'release': True}})
    assert result['counts']['correct'] == 2 and not result['all_requirements_met']
    mapping['requirements']['case:case1/expected_outputs/0']['checks'] = [
        {'kind': 'field', 'target': 'records.return.actor', 'expected': 'tenant'}]
    with pytest.raises(ValueError, match='actual case'):
        evaluate(output, expected, mapping)


def test_replay_invalidates_dependent_dispatch_after_policy_change(work):
    value, root = work
    policies = {j['id']: {'false_at_most': .1, 'true_at_least': .8} for j in value['jobs']}
    request = plan.requests(value, root, registry(), {})['requests'][0]
    waves = [{'requests': [request], 'results': [execution(request, .85)]}]
    child = replay(value, root, registry(), policies, waves)['next']['requests'][0]
    waves.append({'requests': [child], 'results': [execution(child, .99)]})
    assert replay(value, root, registry(), policies, waves)['output']['complete']
    policies['notice']['true_at_least'] = .9
    with pytest.raises(ValueError, match='ready prepared work'):
        replay(value, root, registry(), policies, waves)


def test_replay_negative_and_failed_responses_do_not_become_missing(work):
    value, root = work
    policies = {j['id']: {'false_at_most': .1, 'true_at_least': .9} for j in value['jobs']}
    request = plan.requests(value, root, registry(), {})['requests'][0]
    record = execution(request, .01)
    waves = [{'requests': [request], 'results': [record]}]
    output = replay(value, root, registry(), policies, waves)['output']
    assert output['jobs']['waiver']['status'] == 'not_applicable'
    assert output['complete']
    record['status'] = 'invalid_response'
    failed = replay(value, root, registry(), policies, waves)
    assert failed['output']['jobs']['notice']['status'] == 'invalid_response'
    assert failed['next']['waiting'] == ['waiver']
    assert not failed['output']['complete']


def test_persistent_run_resumes_without_resending_completed_work(work):
    from pipeline.semantics.run import run
    from pipeline.design.task_evaluation.run import save
    value, root = work
    policies = {j['id']: {'false_at_most': .1, 'true_at_least': .9} for j in value['jobs']}
    calls = []

    async def dispatch(requests, directory, cap):
        directory.mkdir()
        calls.append(requests[0]['case_id'])
        records = [execution(requests[0], .99)]
        records[0]['raw']['usage'] = {'cost': .002}
        save(directory / 'requests.json', requests)
        save(directory / 'results.json', records)
        return records

    # The first cap permits one call; its cost leaves too little reservation for another.
    first = asyncio.run(run(value, root, registry(), policies, root / 'run', '.01', dispatch=dispatch))
    assert calls == ['notice'] and not first['output']['complete']
    second = asyncio.run(run(value, root, registry(), policies, root / 'run', '.1', dispatch=dispatch))
    assert calls == ['notice', 'waiver'] and second['output']['complete']
    third = asyncio.run(run(value, root, registry(), policies, root / 'run', '.1', dispatch=dispatch))
    assert third == second and calls == ['notice', 'waiver']
    assert json.loads((root / 'run' / 'summary.json').read_text())['reported_cost'] == '0.004'
    policies['notice']['true_at_least'] = .95
    with pytest.raises(ValueError, match='Run inputs changed'):
        asyncio.run(run(value, root, registry(), policies, root / 'run', '.1', dispatch=dispatch))


def test_persistent_run_rejects_unknown_dispatch_outcome(work):
    from pipeline.semantics.run import run
    value, root = work
    policies = {j['id']: {'false_at_most': .1, 'true_at_least': .9} for j in value['jobs']}
    (root / 'run' / 'call-000000').mkdir(parents=True)

    async def forbidden(*args):
        pytest.fail('An interrupted call must not be resent automatically')

    with pytest.raises(ValueError, match='unknown outcome'):
        asyncio.run(run(value, root, registry(), policies, root / 'run', '.1', dispatch=forbidden))


def test_existing_review_batch_consumes_replayed_semantic_fields(work, monkeypatch):
    from pipeline import batch, core, triage
    from pipeline.semantics.run import run
    from pipeline.design.task_evaluation.run import save
    value, root = work
    value['jobs'][0]['licenses'] = [{'answer': True, 'target': 'records.notice.actor',
                                   'value': 'A', 'operation': 'establish_field_only'}]
    policies = {j['id']: {'false_at_most': .1, 'true_at_least': .9} for j in value['jobs']}

    async def dispatch(requests, directory, cap):
        directory.mkdir()
        records = [execution(requests[0], .99)]
        records[0]['raw']['usage'] = {'cost': .001}
        save(directory / 'requests.json', requests)
        save(directory / 'results.json', records)
        return records

    asyncio.run(run(value, root, registry(), policies, root / 'run', '.1', dispatch=dispatch))
    save(root / 'run' / 'output.json', {'forged': 'cached legal conclusion'})
    section = {'section_id': 'TEST:1', 'text_file': 'source.txt'}
    registration = {'run': 'run', 'plan_hash': jev_results.fingerprint(value),
                    'section_source_sha256': value['sources'][0]['sha256'], 'section_evidence': ['section']}
    save(root / 'semantic_runs.json', {'TEST:1': registration})
    monkeypatch.setattr(core, 'ROOT', root)
    monkeypatch.setattr(core, 'jdir', lambda code: root)
    monkeypatch.setattr(core, 'sections', lambda code: [section])
    monkeypatch.setattr(core, 'instruments', lambda code: {})
    monkeypatch.setattr(core, 'chain_map', lambda: {'functions': []})
    monkeypatch.setattr(triage, 'current_rows', lambda code: [
        {'section_id': 'TEST:1', 'instrument': 'TEST', 'unit': '1'}])
    monkeypatch.setattr(batch, 'already_batched', lambda code: set())
    item = batch.plan('TEST')[0][0]
    assert item['semantic']['established_fields'] == {'records.notice.actor': 'A'}
    assert item['semantic']['prepared_work_complete']
    (root / 'source.txt').write_text('Changed section')
    with pytest.raises(ValueError, match='section source has changed'):
        batch.plan('TEST')


def test_freeze_preserves_sources_and_rejects_unreviewed_or_changed_inputs(work):
    from pipeline.semantics import freeze
    from pipeline.design.task_evaluation.run import save
    value, root = work
    source = value['sources'][0]
    proposal = {'format': 'section-semantics-preparation-proposal-1', 'id': 'fixture',
                'evidence': {'section': {'text': source['quote'], 'source': {
                    key: source[key] for key in ('path', 'sha256', 'start', 'end')}}},
                'source_occurrence_inventory': [], 'unit_boundary': {'test': True},
                'proposed_records': [], 'proposed_definitions': [], 'proposed_relationships': [],
                'jobs': [{'id': 'notice', 'native': value['jobs'][0]['question'],
                          'evidence_refs': ['section'], 'requires': [], 'licenses': [],
                          'state_template': {'passage': {'evidence_ref': 'section'}}}]}
    save(root / 'proposal.json', proposal)
    expectations = {'test_expectations': 'independent fixture', 'components': [],
                    'evidence': {'source': dict(source, text=source['quote'])}}
    save(root / 'expected.json', expectations)
    from pipeline.semantics.prepare import compile_proposal
    save(root / 'mapping.json', {'format': 'section-semantics-evaluation-mapping-1',
                                'expectations_hash': jev_results.fingerprint(expectations),
                                'plan_hash': jev_results.fingerprint(compile_proposal(proposal, root)),
                                'requirements': {}})
    assessment = {'preparation_sha256': freeze.digest((root / 'proposal.json').read_bytes()),
                  'expectations_sha256': freeze.digest((root / 'expected.json').read_bytes()),
                  'status': 'ready_for_evaluation', 'material_findings': ['missing condition'],
                  'model_responses_seen': False, 'reviewer': 'test reviewer',
                  'coverage_assessment': 'synthetic test unit'}
    save(root / 'review.json', assessment)
    save(root / 'registry.json', registry())
    save(root / 'policies.json', {'notice': {'false_at_most': .1, 'true_at_least': .9}})
    args = [root / name for name in ('proposal.json', 'expected.json', 'review.json', 'registry.json', 'policies.json')]
    with pytest.raises(ValueError, match='open findings'):
        freeze.create(*args, root, root / 'frozen', phase='development', rationale='Synthetic test only',
                      evaluation_mapping=root / 'mapping.json')
    assert not (root / 'frozen').exists()
    assessment['material_findings'] = []
    save(root / 'review.json', assessment)
    freeze.create(*args, root, root / 'frozen', phase='development', rationale='Synthetic test only',
                  evaluation_mapping=root / 'mapping.json')
    (root / 'source.txt').write_text('Live source later changed')
    data, source_root = freeze.read(root / 'frozen')
    assert (source_root / 'source.txt').read_text() == source['quote']
    assert data['preparation.json'] == proposal
    (root / 'frozen' / 'expectations.json').write_text('{}')
    with pytest.raises(ValueError, match='Frozen input changed'):
        freeze.read(root / 'frozen')
