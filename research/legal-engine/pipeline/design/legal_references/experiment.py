"""Freeze and evaluate the legal-reference task without leaking review labels into input.

Run as python3 -m pipeline.design.legal_references.experiment from legal-engine.
Jev execution uses the existing atomic runner; this module makes no model calls.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path

from pipeline import core
from pipeline.design.agent_jev_code import prepare as identity
from pipeline.design.agent_jev_code.run import validate_request, validate_response

VERSION = 'reference-focus-1'


def load(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def index(rows, key='case_id'):
    indexed = {r[key]:r for r in rows}
    if len(indexed) != len(rows):raise ValueError('Duplicate IDs')
    return indexed


def make_requests(cases, question, root=core.ROOT):
    index(cases)
    if not cases:raise ValueError('Empty dataset')
    model = load(root/'pipeline/jev_questions.json')
    requests = []
    for case in cases:
        text = case['text']
        if not isinstance(text,str) or not text.strip():raise ValueError('Missing readable focus')
        source = case.get('source')
        if source:
            path = (root/source['path']).resolve()
            if not path.is_relative_to(root.resolve()):raise ValueError('Source outside research root')
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != source['sha256']:raise ValueError('Changed source')
            a,b = source['start'],source['end'];full = raw.decode('utf-8')
            if not 0 <= a < b <= len(full) or full[a:b] != text:raise ValueError('Incorrect source excerpt')
        elif not case.get('authored'):
            raise ValueError('Unattributed example must be explicitly authored')
        state = {'focus':text}
        if 'expression_span' in case:
            a,b = case['expression_span']
            if not 0 <= a < b <= len(text) or not text[a:b].strip():
                raise ValueError('Invalid expression span')
            if not case.get('source_kind'):
                raise ValueError('Expression judgment needs source context')
            state.update(expression=text[a:b],source_kind=case['source_kind'])
        payload = {'model':model['model'], 'questions':{question['question_id']:{k:question[k] for k in ['primitive','instructions','criteria']}}, 'state':state}
        ident = {'assembler_version':VERSION,'task_version':question['version'],'pinned_build':model['pinned_build'],'payload':payload}
        row = {'case_id':case['case_id'],'request_hash':identity.digest(ident),**ident}
        validate_request(row);requests.append(row)
    return requests


def freeze(cases_path, question_path, review_path, output):
    cases = load(cases_path);question = load(question_path);review = load(review_path)
    reviewed = review.get('reviewed_inputs', {})
    for name, path in [('cases', cases_path), ('question', question_path)]:
        if reviewed.get(name) != hashlib.sha256(path.read_bytes()).hexdigest():
            raise ValueError('Review does not bind current ' + name)
    labels = index(review['cases']);requests = make_requests(cases,question)
    if set(labels) != {r['case_id'] for r in requests}:raise ValueError('Review coverage differs from dataset')
    frozen = []
    for req in requests:
        label = labels[req['case_id']]
        if label['expected'] not in question['criteria'] or not label.get('reason'):raise ValueError('Invalid review label')
        if label.get('material_ambiguity'):raise ValueError(f"Unresolved review ambiguity: {req['case_id']}")
        frozen.append({'case_id':req['case_id'],'request_hash':req['request_hash'],'expected':label['expected'],'reason':label['reason']})
    output.mkdir(parents=True,exist_ok=False)
    save(output/'cases.json',cases);save(output/'question.json',question);save(output/'review.json',review)
    save(output/'labels.json',frozen)
    (output/'requests.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in requests))
    save(output/'manifest.json',{'assembler_version':VERSION,'cases':len(cases),'source_backed':sum(bool(c.get('source')) for c in cases),'authored':sum(bool(c.get('authored')) for c in cases),'frozen_before_model_run':True,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file()}})
    return {'frozen_cases':len(cases),'output':str(output)}


def evaluate(bundle, run):
    manifest = load(bundle/'manifest.json')
    for name,digest in manifest['files'].items():
        if hashlib.sha256((bundle/name).read_bytes()).hexdigest() != digest:raise ValueError('Frozen file changed: '+name)
    requests = index([json.loads(s) for s in (bundle/'requests.jsonl').read_text().splitlines()])
    labels = index(load(bundle/'labels.json'));cases = index(load(bundle/'cases.json'))
    results = index(load(run/'results.json'));executed = index(load(run/'requests.json'))
    if set(results)-set(requests) or set(executed)-set(requests):raise ValueError('Unknown executed case')
    for sid,req in executed.items():
        if req != requests[sid]:raise ValueError('Executed request differs from frozen request')
    rows=[];strata={}
    for sid,req in requests.items():
        label=labels[sid];result=results.get(sid)
        if label['request_hash'] != req['request_hash']:raise ValueError('Label identity mismatch')
        row={'case_id':sid,'request_hash':req['request_hash'],'expected':label['expected'],'actual':None,'agreement':None,'status':'missing_result','strata':cases[sid]['strata']}
        if result:
            if result['request_hash'] != req['request_hash']:raise ValueError('Result identity mismatch')
            row['status']=result['status']
            if result['status']=='answered':
                if sid not in executed:raise ValueError('Answer has no executed request')
                answer=validate_response(req,result['raw']);row.update(actual=answer['choice'],agreement=answer['choice']==label['expected'],confidence=answer.get('confidence'))
        rows.append(row)
        for stratum in row['strata']:
            stat=strata.setdefault(stratum,{'cases':0,'answered':0,'agreements':0})
            stat['cases']+=1;stat['answered']+=row['actual'] is not None;stat['agreements']+=row['agreement'] is True
    report={'cases':len(rows),'answered':sum(r['actual'] is not None for r in rows),'agreements':sum(r['agreement'] is True for r in rows),'unanswered':sum(r['actual'] is None for r in rows),'disagreements':[r['case_id'] for r in rows if r['agreement'] is False],'by_stratum':strata,'rows':rows,'interpretation':'Agreement on a deliberately constructed benchmark; strata overlap. Not probability calibration or complete dependency recall.'}
    save(run/'evaluation.json',report)
    return {k:v for k,v in report.items() if k not in ['rows','by_stratum']}


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    f=sub.add_parser('freeze')
    for name in ['cases','question','review','output']:f.add_argument('--'+name,type=Path,required=True)
    e=sub.add_parser('evaluate');e.add_argument('--bundle',type=Path,required=True);e.add_argument('--run',type=Path,required=True)
    args=parser.parse_args()
    result=freeze(args.cases,args.question,args.review,args.output) if args.command=='freeze' else evaluate(args.bundle,args.run)
    print(json.dumps(result))


if __name__=='__main__':main()
