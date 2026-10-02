import copy
import json
from pathlib import Path
import pytest
from pipeline.design.prepared_tasks.statutory import assemble, validate_response

P=Path(__file__).parents[1]/'design/prepared_tasks'


def test_batch_changes_only_grouping_not_question_or_evidence():
    cases=json.loads((P/'statutory-fresh-corrected-frozen/cases.json').read_text())
    question=json.loads((P/'statutory.question.json').read_text())
    separate=assemble(cases,question);batched=assemble(cases,question,True)
    assert len(separate)==27 and len(batched)==4
    def flatten(rows):
        return {key:(row['payload']['state'],value) for row in rows for key,value in row['payload']['questions'].items()}
    assert flatten(separate)==flatten(batched)
    assert all('SOURCE:' not in r['payload']['state']['passage'] for r in batched)


def test_batch_requires_every_typed_answer_and_pinned_build():
    row={'pinned_build':'pinned','payload':{'questions':{'a':{},'b':{}}}}
    raw={'model':'pinned','answers':{'a':{'type':'noul','noul':.9},'b':{'type':'noul','noul':.1}}}
    assert set(validate_response(row,raw))=={'a','b'}
    for broken in [dict(raw,model='other'), dict(raw,answers={'a':raw['answers']['a']}),
                   dict(raw,answers={**raw['answers'],'extra':raw['answers']['a']})]:
        with pytest.raises(ValueError):validate_response(row,broken)
    for value in [True,float('nan'),1.1,'0.9']:
        broken=copy.deepcopy(raw);broken['answers']['a']['noul']=value
        with pytest.raises(ValueError):validate_response(row,broken)


def test_corrected_local_occurrence_is_in_remedy_clause():
    cases=json.loads((P/'statutory-fresh-corrected-frozen/cases.json').read_text())
    case=next(c for c in cases if c['case_id']=='fresh-1942-07')
    a,b=case['expression_span']
    assert case['text'][a:b]=='subdivision (a)'
    assert case['text'][:a].endswith('The tenant’s remedy under ')


def test_direct_question_and_governing_clause_preserve_exact_expression():
    cases=json.loads((P/'statutory-clause-frozen/cases.json').read_text())
    question=json.loads((P/'statutory-pointer.question.json').read_text())
    row=assemble(cases,question,True)[0]
    spec=next(iter(row['payload']['questions'].values()))
    assert spec['instructions']=='Is "a declaration of COVID-19-related financial distress" a pointer to statutory text?'
    assert row['payload']['state']['passage']=='who has submitted a declaration of COVID-19-related financial distress'
    # The other reference still has its own source-backed selection in the parent set.
    parent=json.loads((P/'statutory-confirmation-frozen/cases.json').read_text())
    assert sum(c['case_id'].startswith('confirm-1942.9') and c['text'][slice(*c['expression_span'])]=='Section 1179.02 of the Code of Civil Procedure' for c in parent)==2


def test_independent_review_binds_inputs_and_rejects_ambiguity(tmp_path):
    import hashlib
    from pipeline.design.prepared_tasks.statutory import freeze_reviewed
    cases=[{'case_id':'a','text':'This section applies.','authored':True,'source_kind':'statute','expression_span':[0,12],'strata':[]}]
    paths={name:tmp_path/f'{name}.json' for name in ['cases','question','review']}
    paths['cases'].write_text(json.dumps(cases))
    paths['question'].write_text((P/'statutory-pointer.question.json').read_text())
    review={'reviewed_inputs':{k:hashlib.sha256(paths[k].read_bytes()).hexdigest() for k in ['cases','question']},
            'cases':[{'case_id':'a','expected':'YES','reason':'Enclosing section.', 'material_ambiguity':True}]}
    paths['review'].write_text(json.dumps(review))
    with pytest.raises(ValueError,match='ambiguity'):
        freeze_reviewed(paths['cases'],paths['question'],paths['review'],tmp_path/'bad')
    review['cases'][0]['material_ambiguity']=False;paths['review'].write_text(json.dumps(review))
    freeze_reviewed(paths['cases'],paths['question'],paths['review'],tmp_path/'good')
    assert json.loads((tmp_path/'good/manifest.json').read_text())['label_review']=='Independent input-bound review.'
    assert json.loads((tmp_path/'good/review.json').read_text())==review
    paths['cases'].write_text(json.dumps(cases)+'\n')
    with pytest.raises(ValueError,match='bind current cases'):
        freeze_reviewed(paths['cases'],paths['question'],paths['review'],tmp_path/'stale')


def test_execution_failure_is_not_a_semantic_disagreement(tmp_path):
    from pipeline.design.prepared_tasks.statutory import freeze, evaluate
    cases=[{'case_id':'a','text':'This section applies.','authored':True,'source_kind':'statute','expression_span':[0,12],'strata':[]}]
    bundle=tmp_path/'bundle';output=tmp_path/'run';output.mkdir()
    freeze(cases,json.loads((P/'statutory-pointer.question.json').read_text()),
           [{'case_id':'a','expected':'YES','reason':'Enclosing section.'}],bundle)
    requests=json.loads((bundle/'batched.json').read_text())
    (output/'requests.json').write_text(json.dumps(requests))
    failure={'case_id':requests[0]['case_id'],'request_hash':requests[0]['request_hash'],'status':'execution_error'}
    (output/'results.json').write_text(json.dumps([failure]))
    evaluate(bundle,output,'batched')
    report=json.loads((output/'evaluation.json').read_text())
    assert report['unanswered']==1 and not report['disagreements']
    assert report['rows'][0]['agreement'] is None
    (output/'results.json').write_text(json.dumps([failure,failure]))
    with pytest.raises(ValueError,match='Duplicate or unknown'):
        evaluate(bundle,output,'batched')
