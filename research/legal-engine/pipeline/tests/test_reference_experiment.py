"""Reference experiments must preserve input identity, sources, and missing-result accounting."""
import copy
import hashlib
import json
from pathlib import Path

import pytest

from pipeline.design.legal_references import experiment

HERE = Path(experiment.__file__).parent


def dataset():
    return [{'case_id':'a','text':'This section applies.','authored':True,'source':None,'strata':['self']},
            {'case_id':'b','text':'The title to the goods.','authored':True,'source':None,'strata':['lookalike']}]


def bind_review(tmp_path):
    review=experiment.load(tmp_path/'review.json')
    review['reviewed_inputs']={name:hashlib.sha256((tmp_path/(name+'.json')).read_bytes()).hexdigest() for name in ['cases','question']}
    experiment.save(tmp_path/'review.json',review)


def frozen(tmp_path):
    cases=dataset();question=experiment.load(HERE/'question.v1-dev2.json')
    labels={'cases':[{'case_id':'a','expected':'YES','reason':'self'}, {'case_id':'b','expected':'NO','reason':'ordinary title'}]}
    for name,obj in [('cases',cases),('question',question),('review',labels)]:experiment.save(tmp_path/(name+'.json'),obj)
    bind_review(tmp_path)
    out=tmp_path/'frozen';experiment.freeze(tmp_path/'cases.json',tmp_path/'question.json',tmp_path/'review.json',out)
    return out


def test_only_focus_enters_model_state():
    cases=dataset();q=experiment.load(HERE/'question.v1-dev2.json');before=experiment.make_requests(cases,q)
    for c in cases:
        c['expected']='ORACLE';c['wrapper_metadata']={'citation':'CIV 99','review':'ORACLE'};c['strata']=['ORACLE']
    after=experiment.make_requests(cases,q)
    assert before==after
    assert 'ORACLE' not in json.dumps(after)


def test_empty_unattributed_and_duplicate_examples_fail():
    q=experiment.load(HERE/'question.v1-dev2.json')
    for cases in [[],dataset()+[dataset()[0]], [dict(dataset()[0],text='')], [dict(dataset()[0],authored=False)]]:
        with pytest.raises(ValueError):experiment.make_requests(cases,q)


def test_source_change_and_span_mismatch_fail(tmp_path):
    import hashlib
    (tmp_path/'pipeline').mkdir();experiment.save(tmp_path/'pipeline/jev_questions.json',{'model':'m','pinned_build':'b'})
    p=tmp_path/'source.txt';p.write_text('This section applies.')
    c=dataset()[0];c['source']={'path':'source.txt','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'start':0,'end':len(c['text'])};c['authored']=False
    q=experiment.load(HERE/'question.v1-dev2.json');experiment.make_requests([c],q,tmp_path)
    c['source']['start']=1
    with pytest.raises(ValueError,match='excerpt'):experiment.make_requests([c],q,tmp_path)
    c['source']['start']=0;p.write_text('This chapter applies.')
    with pytest.raises(ValueError,match='Changed source'):experiment.make_requests([c],q,tmp_path)


def test_unanswered_case_stays_in_denominator(tmp_path):
    out=frozen(tmp_path);requests=[json.loads(s) for s in (out/'requests.jsonl').read_text().splitlines()];run=tmp_path/'run';run.mkdir()
    experiment.save(run/'requests.json',requests)
    qid=next(iter(requests[0]['payload']['questions']))
    experiment.save(run/'results.json',[{'case_id':'a','request_hash':requests[0]['request_hash'],'status':'answered','raw':{'model':requests[0]['pinned_build'],'answers':{qid:{'choice':'YES'}}}}])
    result=experiment.evaluate(out,run)
    assert result['cases']==2 and result['answered']==1 and result['unanswered']==1 and result['agreements']==1
    # Mutating frozen labels must not retroactively improve a score.
    labels=experiment.load(out/'labels.json');labels[0]['expected']='NO';experiment.save(out/'labels.json',labels)
    with pytest.raises(ValueError,match='Frozen file changed'):experiment.evaluate(out,run)


def test_unresolved_review_blocks_freeze(tmp_path):
    for name,obj in [('cases',dataset()),('question',experiment.load(HERE/'question.v1-dev2.json')),('review',{'cases':[{'case_id':'a','expected':'YES','reason':'x','material_ambiguity':True},{'case_id':'b','expected':'NO','reason':'x'}]})]:experiment.save(tmp_path/(name+'.json'),obj)
    bind_review(tmp_path)
    with pytest.raises(ValueError,match='Unresolved review ambiguity'):
        experiment.freeze(tmp_path/'cases.json',tmp_path/'question.json',tmp_path/'review.json',tmp_path/'frozen')


@pytest.mark.parametrize('changed', ['cases', 'question'])
def test_stale_independent_review_cannot_label_changed_input(tmp_path, changed):
    frozen(tmp_path)
    path=tmp_path/(changed+'.json');value=experiment.load(path)
    if changed=='cases':value[0]['text']='The title to the goods.'
    else:value['instructions']='Use a different meaning of reference.'
    experiment.save(path,value)
    with pytest.raises(ValueError,match='Review does not bind current '+changed):
        experiment.freeze(tmp_path/'cases.json',tmp_path/'question.json',tmp_path/'review.json',tmp_path/'new-frozen')
