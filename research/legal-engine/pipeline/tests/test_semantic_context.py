from copy import deepcopy

import pytest

from pipeline.semantics.context import expand_condition_context
from pipeline.semantics.templates import render


def fixture():
    def producer(jid, target, value):
        return {'id': jid, 'requires': [], 'state_template': {}, 'licenses': [
            {'answer': True, 'target': target, 'value': value, 'operation': 'establish_field_only'},
            {'answer': False, 'target': target, 'value': 'rejected_candidate', 'operation': 'reject_only'}]}
    return {'jobs': [
        producer('p', 'conditions.notice.delivered.predicate', 'Notice delivered'),
        producer('g', 'conditions.notice.service', {'operator': 'all', 'children': ['delivered']}),
        producer('root', 'conditions.notice.root', {'operator': 'any', 'children': ['service']}),
        {'id': 'consumer', 'requires': ['root'], 'licenses': [], 'state_template': {
            'meaning': {'from_actual_results': [{'job': 'root', 'field': 'conditions.notice.root'}]}}}]}


def test_nested_context_contains_actual_meaning_and_does_not_promote_rejections():
    original = fixture()
    saved = deepcopy(original)
    proposal, changes = expand_condition_context(original)
    assert original == saved
    assert len(changes) == 2
    assert proposal['jobs'][-1]['requires'] == ['root', 'g', 'p']
    jobs = {j['id']: j for j in proposal['jobs']}
    outcomes = {jid: {'status': 'answered', 'answer': True} for jid in ('root', 'g', 'p')}
    state = render(jobs['consumer']['state_template'], {}, jobs, outcomes)
    assert state['meaning'][-1]['assignments'][0]['value'] == 'Notice delivered'
    outcomes['p']['answer'] = False
    state = render(jobs['consumer']['state_template'], {}, jobs, outcomes)
    assert state['meaning'][-1]['assignments'][0]['operation'] == 'reject_only'
    outcomes['p'] = {'status': 'uncertain'}
    with pytest.raises(ValueError, match='unanswered predecessor'):
        render(jobs['consumer']['state_template'], {}, jobs, outcomes)
    repeated, additions = expand_condition_context(proposal)
    assert repeated == proposal and additions == []


def test_missing_condition_producer_is_not_replaced_with_child_identifier():
    proposal = fixture()
    proposal['jobs'] = proposal['jobs'][1:]
    with pytest.raises(ValueError, match='no field producer: conditions.notice.delivered'):
        expand_condition_context(proposal)


def test_context_cannot_require_the_answer_it_is_preparing():
    proposal = fixture()
    proposal['jobs'][-1]['licenses'] = proposal['jobs'][0]['licenses']
    proposal['jobs'] = proposal['jobs'][1:]
    with pytest.raises(ValueError, match='own answer'):
        expand_condition_context(proposal)
