"""Known missing structure returns work to the agent; it is never a semantic NO."""
import copy

from pipeline.design.agent_jev_code import context, prepare


def test_missing_hierarchy_is_not_sent_and_input_is_unchanged():
    rows = prepare.assemble()[0]
    original = copy.deepcopy(rows)
    ready, work = context.prepare_dispatch(rows)
    assert rows == original
    assert len(ready) == 21
    assert [r['case_id'] for r in work] == ['dev13']
    assert work[0]['missing_fields'] == ['use_location.unit']
    assert work[0]['model_answer'] is None
    assert work[0]['status'] == 'needs_context'


def test_shape_checks_do_not_claim_semantic_context_sufficiency():
    rows = prepare.assemble()[0]
    ready, _ = context.prepare_dispatch(rows)
    # dev14 lacks the governing scope sentence. Its valid structure cannot prove semantic sufficiency.
    assert any(r['case_id'] == 'dev14' for r in ready)


def test_recovered_context_gets_a_different_request_identity():
    rows = prepare.assemble()[0]
    row = copy.deepcopy(next(r for r in rows if r['case_id'] == 'dev13'))
    previous = row['request_hash']
    row['payload']['state']['use_location']['unit'] = 'Division 3 Part 4 Title 5 Chapter 5'
    identity = {k: row[k] for k in ['assembler_version','task_version','pinned_build','payload']}
    row['request_hash'] = prepare.digest(identity)
    ready, work = context.prepare_dispatch([row])
    assert len(ready) == 1 and not work
    assert ready[0]['request_hash'] != previous
