"""Native yes/no diagnostic on identical reviewed inputs; not production routing."""
import argparse
import asyncio
import hashlib
import json
import math
import time
from decimal import Decimal
from pathlib import Path
from pydantic import BaseModel, ConfigDict
from typesafe_sdk import AsyncTypeSafeClient, Noul, RetryPolicy
from pipeline import core, jev
from pipeline.design.agent_jev_code.prepare import digest


def save(path, value):
    path.write_text(jev.redact(json.dumps(value, ensure_ascii=False, indent=2))+'\n')


async def run(bundle, output, structured=False, criteria=False):
    manifest=json.loads((bundle/'manifest.json').read_text())
    for name,h in manifest['files'].items():
        if hashlib.sha256((bundle/name).read_bytes()).hexdigest()!=h:raise ValueError('Frozen input changed')
    original=[json.loads(line) for line in (bundle/'requests.jsonl').read_text().splitlines()]
    labels={r['case_id']:r for r in json.loads((bundle/'labels.json').read_text())}
    requests=[]
    for row in original:
        qid,q=next(iter(row['payload']['questions'].items()))
        payload={'model':row['payload']['model'],'state':row['payload']['state'],
                 'questions':{qid:{'primitive':'noul','instructions':q['instructions']}}}
        if structured:
            state = payload['state']
            payload['questions'][qid]['instructions'] = {
                'question': 'Is this expression a textual cross-reference?',
                'expression': state['expression']}
            payload['state'] = {'passage': state['focus'], 'source_kind': state['source_kind']}
        if criteria:
            payload['questions'][qid]['criteria'] = {
                'true': 'The expression identifies a unit of legal text.',
                'false': 'The expression describes a thing, event, or duration.'}
        identity={'assembler_version'  :'structured-noul-1' if structured else 'native-noul-1','task_version':row['task_version']+('-structured-criteria-noul' if criteria else '-structured-noul' if structured else '-noul'),
                  'pinned_build':row['pinned_build'],'payload':payload}
        requests.append({'case_id':row['case_id'],'original_request_hash':row['request_hash'],
                         'request_hash':digest(identity),**identity})
    output.mkdir(exist_ok=False);save(output/'requests.json',requests)
    save(output/'comparison.json',{'source_bundle':str(bundle),'treatment':('Structured expression beside question; passage as shared context; textual cross-reference wording; native Noul without criteria.' if structured else 'Noul instead of Choice; omit Choice criteria. State and question wording identical.'),
                                  'criteria_added':criteria, 'scoring':'Diagnostic majority above/below 0.5; exactly 0.5 undecided. No production threshold or probability calibration claimed.'})
    class Raw(BaseModel):
        model_config=ConfigDict(extra='allow')
    results=[];started=time.monotonic()
    async with AsyncTypeSafeClient(api_key=jev.api_key(),base_url=core.questions()['base_url'],retry=RetryPolicy(max_retries=0)) as client:
        async def one(row):
            result={'case_id':row['case_id'],'request_hash':row['request_hash'],'status':'execution_error'}
            try:
                qid,q=next(iter(row['payload']['questions'].items()))
                response=await client.system_one(model=row['payload']['model'],state=row['payload']['state'],questions=jev.sdk_questions({qid:q}),response_model=Raw)
                raw=response.model_dump(mode='json');result['raw']=raw;result['status']='invalid_response'
                if raw.get('model')!=row['pinned_build'] or set(raw.get('answers',{}))!={qid}:raise ValueError('Response identity mismatch')
                answer=raw['answers'][qid];value=answer.get('noul')
                if answer.get('type')!='noul' or isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not 0<=value<=1:raise ValueError('Invalid Noul')
                result.update(status='answered',noul=value,actual='YES' if value>0.5 else 'NO' if value<0.5 else None)
            except Exception as exc:result['error']=jev.redact(str(exc))[:600]
            return result
        for start in range(0,len(requests),4):
            results.extend(await asyncio.gather(*(one(r) for r in requests[start:start+4])))
            save(output/'results.json',results)
    for r in results:
        r['expected']=labels[r['case_id']]['expected'];r['agreement']=r.get('actual')==r['expected'] if r['status']=='answered' else None
    save(output/'evaluation.json',results)
    costs=[r.get('raw',{}).get('usage',{}).get('cost') for r in results]
    summary={'requested':len(requests),'answered':sum(r['status']=='answered' for r in results),'agreements':sum(r['agreement'] is True for r in results),
             'disagreements':[r['case_id'] for r in results if r['agreement'] is False],
             'cost_usd':str(sum((Decimal(str(c)) for c in costs if c is not None),Decimal(0))),
             'missing_cost_records':sum(c is None for c in costs),'elapsed_seconds':round(time.monotonic()-started,4),'retries':0}
    save(output/'summary.json',summary);print(json.dumps(summary))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--bundle',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--structured', action='store_true')
    parser.add_argument('--criteria', action='store_true')
    args=parser.parse_args();asyncio.run(run(args.bundle,args.output,args.structured,args.criteria))
