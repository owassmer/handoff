"""Source-only repairs requested by independent preparation review; no labels/inference."""
from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).parent;R=B.parents[2];H=B/'history/expansion-before-preparation-review-v1'
H.mkdir(parents=True,exist_ok=True)
for name in ['expansion.cases.json','expansion.author_labels.json','expansion.coverage.json','expansion.recovery.json','build_expansion.py']:
 if not (H/name).exists():shutil.copy2(B/name,H/name)
if not (H/'source_manifest.json').exists():shutil.copy2(B/'expansion_sources/manifest.json',H/'source_manifest.json')
d=json.loads((B/'expansion.cases.json').read_bytes());cases={c['id']:c for c in d['cases']}
def selection(source,start,end):
 p=B/'expansion_sources'/(source+'.txt');t=p.read_bytes().decode('utf-8');a=t.index(start);b=t.index(end,a);text=t[a:b].strip();a=t.index(text,a)
 return text,{'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'start':a,'end':a+len(text)}
use,us=selection('ARTIS','   Turning from statutory texts to judicial decisions, only','\n                                     B')
definition,ds=selection('ARTIS','We there characterized a state statute providing','This atypical use of')
for cid in ['exp026','exp027','exp042','exp043']:
 c=cases[cid];c['state']['term']='tolling';c['state']['use_expression']='as “tolling”';c['state']['use_passage']=use;c['sources']['use_passage']=us;c['source_cluster']='ARTIS:Hardin-historical-grace-usage'
 if cid=='exp027':c['state']['definition_passage']=definition;c['sources']['definition_passage']=ds
context,ctx=selection('OREGON_90','90.155 Service\nor delivery of written notice.','90.160\nCalculation')
cases['exp077']['state']['context']=context;cases['exp077']['sources']['context']=ctx
text,src=selection('OREGON_90','90.155 Service\nor delivery of written notice.','(3) A landlord or\ntenant may utilize alternative')
cases['exp096']['state']['text']=text;cases['exp096']['sources']['text']=src
(B/'expansion.cases.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
report={'scope':'source-only preparation correction; no label or response disclosure','prior_cases_sha256':hashlib.sha256((H/'expansion.cases.json').read_bytes()).hexdigest(),'cases_sha256':hashlib.sha256((B/'expansion.cases.json').read_bytes()).hexdigest(),'contracts_sha256':hashlib.sha256((B/'configurations/proposed-v2.json').read_bytes()).hexdigest(),'changed_ids':['exp026','exp027','exp042','exp043','exp077','exp096'],'changes':[{'ids':['exp026','exp027','exp042','exp043'],'source_action':'Recovered complete majority paragraph reporting the actual Hardin historical tolling usage. Selected one affirmative as-tolling expression, replacing an unresolved interrogative. exp027 now supplies the complete declarative characterization of the historical meaning, not a question.'},{'ids':['exp077'],'source_action':'Added complete90.155 as source-bound context, including service modes, electronic-address cancellation, mail extension and tenancy-termination clause. Preserved original requirement and candidate for independently reassessing their relation.'},{'ids':['exp096'],'source_action':'Expanded contiguous evidence to90.155 lead-in through subsection2, recovering referenced(1)(b)first-class-mail rule.'}],'source_history':'Raw and derived primary captures unchanged. Prior96 cases, source manifest, author artifacts and generation script preserved under history/expansion-before-preparation-review-v1. Original author labels remain prior-version expectations, not newly independently validated labels.','no_inference':True}
(B/'expansion.preparation_corrections.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['cases_sha256'])
