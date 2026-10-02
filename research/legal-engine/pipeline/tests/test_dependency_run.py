"""Reject invalid build/answer/request results before reporting model agreement."""
import copy
import math

import pytest

from pipeline.design.agent_jev_code import prepare, run


def request():
    return prepare.assemble()[0][0]


def response(row):
    qid = next(iter(row['payload']['questions']))
    return {'model': row['pinned_build'], 'answers': {qid: {
        'choice': 'YES', 'probabilities': {'YES': 0.8, 'NO': 0.1, 'INSUFFICIENT': 0.1}}}}


def test_intact_frozen_request_and_response():
    row = request()
    run.validate_request(row)
    assert run.validate_response(row, response(row))['choice'] == 'YES'


@pytest.mark.parametrize('defect', ['build', 'missing_answer', 'choice', 'nan', 'sum', 'extra_answer'])
def test_invalid_response_rejected(defect):
    row = request()
    raw = response(row)
    answer = next(iter(raw['answers'].values()))
    if defect == 'build': raw['model'] = 'other-build'
    elif defect == 'missing_answer': raw['answers'] = {}
    elif defect == 'choice': answer['choice'] = 'LIKELY'
    elif defect == 'nan': answer['probabilities']['YES'] = math.nan
    elif defect == 'sum': answer['probabilities']['YES'] = 0.1
    else: raw['answers']['unexpected'] = copy.deepcopy(answer)
    with pytest.raises(ValueError):
        run.validate_response(row, raw)


def test_changed_payload_cannot_reuse_request_identity():
    row = request()
    row['payload']['state']['focus']['text'] += 'changed'
    with pytest.raises(ValueError, match='hash mismatch'):
        run.validate_request(row)
