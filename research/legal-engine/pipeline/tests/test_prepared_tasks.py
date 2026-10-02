import hashlib
import json
from pathlib import Path
import pytest
from pipeline.design.prepared_tasks.prepare import prepare
from pipeline.design.prepared_tasks.scope import contains
from pipeline import core
from pipeline.design.legal_references.experiment import make_requests

QUESTION=json.loads((Path(__file__).parents[1]/'design/prepared_tasks/reference.question.json').read_text())


def selection(case, status='ready', **extra):
    return dict(case_id=case['case_id'],input_sha256=hashlib.sha256(case['text'].encode()).hexdigest(),status=status,reason='Agent inspected source structure.',**extra)


def test_excludes_locator_but_keeps_body_reference():
    c={'case_id':'a','text':'Section 8. This section governs notice.','authored':True,'strata':[]}
    rows,outcomes,requests=prepare([c],[selection(c,start=len('Section 8. '),end=len(c['text']))],QUESTION,core.ROOT)
    assert rows[0]['text']=='This section governs notice.'
    assert requests[0]['payload']['state']=={'focus':'This section governs notice.'}
    assert 'Agent inspected' not in json.dumps(requests)


def test_unready_material_stays_accounted_without_model_answer():
    c={'case_id':'a','text':'Section','authored':True,'strata':[]}
    rows,outcomes,requests=prepare([c],[selection(c,'needs_context',next_action='Recover adjacent text.')],QUESTION,core.ROOT)
    assert not rows and not requests
    assert outcomes[0]['status']=='needs_context' and 'expected' not in outcomes[0]
    with pytest.raises(ValueError,match='Every input'):
        prepare([c],[],QUESTION,core.ROOT)


def test_stale_selection_and_unready_dispatch_rejected():
    c={'case_id':'a','text':'This section applies.','authored':True,'strata':[]}
    s=selection(c,start=0,end=len(c['text']));c['text']='This chapter applies.'
    with pytest.raises(ValueError,match='changed input'):prepare([c],[s],QUESTION,core.ROOT)
    s=selection(c,'needs_context',start=0,end=len(c['text']),next_action='Recover.')
    with pytest.raises(ValueError,match='Unready'):prepare([c],[s],QUESTION,core.ROOT)


def test_scope_containment_uses_full_ancestry_and_requires_known_units():
    assert contains(['CA','CIV','Title1.6C'],['CA','CIV','Title1.6C','1788.16'])
    assert not contains(['CA','CIV','Title1.6C'],['CA','CIV','Title5','1950.5'])
    assert not contains(['CA','CIV'],['CA','GOV','12955'])
    with pytest.raises(ValueError):contains(['CA',''],['CA','CIV'])
    with pytest.raises(ValueError):contains([],['CA','CIV'])


def test_expression_keeps_context_and_exact_target_without_source_identifier():
    c={'case_id':'a','text':'This section applies.','authored':True,'strata':[],
       'expression_span':[0,12],'source_kind':'statute','source_identifier':'CIV 999'}
    request=make_requests([c],QUESTION)[0]
    assert request['payload']['state']=={'focus':'This section applies.',
                                        'expression':'This section','source_kind':'statute'}
    assert 'CIV 999' not in json.dumps(request)
    c['expression_span']=[0,999]
    with pytest.raises(ValueError,match='expression span'):make_requests([c],QUESTION)
    c['expression_span']=[0,12];del c['source_kind']
    with pytest.raises(ValueError,match='source context'):make_requests([c],QUESTION)
