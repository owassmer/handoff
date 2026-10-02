"""Materialize finite rule TOCs and direct publication targets; no J2 text harvest."""
import json,re,runpy
from pathlib import Path
P=Path(__file__).parent
runpy.run_path(str(P/'build_proposals.py'))
p=P/'proposed_instruments.json'; data=json.loads(p.read_text()); entries={x['id']:x for x in data['instruments']}
def source(x,number,heading,ref):
 x['units_in_scope'].append({'unit':number,'heading':heading,'toc_url':ref,'reason':'Operative court filing or procedure dependency.','source_unit_kind':'publication','section_list':[{'number':number,'heading':heading,'ref':ref}]})
for u in entries['CA:CRC']['units_in_scope']:
 if u['unit'].startswith('Ethics'):continue
 word=u['toc_url'].split('/')[-1]
 raw=json.loads((P/'capture-33.json').read_text()) if word=='one' else (P/f'crc-{word}.txt').read_text()
 block=next(b for b in raw.split('--------------------------------------------------------------------------------') if f'(https://courts.ca.gov/cms/rules/index/{word})' in b)
 rows=[]; seen=set()
 for m in re.finditer(r'(?:Rule|Standard) (\d+(?:\.\d+)+)\.\s*([^\n]+)',block):
  n,h=m.groups();h=re.split(r'\s*(?:\*|【||Rule \d)',h)[0].strip()
  if n in seen or h=='...':continue
  seen.add(n)
  if '[Repealed]' in h:
   entries['CA:CRC']['units_out'].append({'unit':('Standard ' if word=='standards' else 'Rule ')+n,'reason':'TOC expressly identifies repealed provision; recover only for historical event-time dependency.'});continue
  rows.append({'number':('Standard ' if word=='standards' else 'Rule ')+n,'heading':h,'ref':u['toc_url']+'/'+('standard' if word=='standards' else 'rule')+n.replace('.','_')})
 assert rows,word
 u['section_list']=rows;u['source_unit_kind']='individual_rules';u['enumeration_evidence']=f'j1/lanes/courts/'+('capture-33.json' if word=='one' else f'crc-{word}.txt')
 print(word,len(rows))
x=entries['CA:CACD'];u=next(u for u in x['units_in_scope'] if u['unit']=='Chapter-II');u['section_list']=[{'number':'Chapter-II-2018-12','heading':u['heading'],'ref':'https://www.cacd.uscourts.gov/sites/default/files/documents/LocalRules_Chap2.pdf'}]
x=entries['CA:CACB'];u=next(u for u in x['units_in_scope'] if u['unit']=='TCG-supplements')
cap=json.loads((P/'capture-33.json').read_text());urls=re.findall(r'^ \((https://[^\n]+\.pdf)\)$',cap,re.M);assert len(urls)==20,len(urls)
titles=re.findall(r'†(TCG Supplement [^]+)',json.loads((P/'capture-32.json').read_text()));assert len(titles)==20,len(titles)
u['section_list']=[{'number':t.split(':')[0],'heading':t,'ref':url} for t,url in zip(titles,urls)]
source(entries['CA:BAP9'],'BAP-ECF-2015','Administrative Order Regarding Electronic Filing in BAP Cases, February 2, 2015','https://cdn.ca9.uscourts.gov/datastore/bap/2015/02/02/GENORD_cmecf_Feb_2015.pdf')
u=entries['CA:4DCA']['units_in_scope'][0];u['section_list']=[{'number':'4D-local-rules-current','heading':u['heading'],'ref':u['toc_url']}]
x={'id':'US:COURT-FEES','jurisdiction':'US','name':'Federal district, appellate and bankruptcy miscellaneous fee schedules','level':'court rule','instrument_kind':'court fee schedule','adapter':'generic','functions':['courts_procedure'],'units_in_scope':[],'units_out':[],'source_review':'j1/lanes/courts/REPORT.md'}
for name in ['district-court','court-appeals','bankruptcy-court']:source(x,name+'-fee-schedule',name+' miscellaneous fee schedule','https://www.uscourts.gov/court-programs/fees/'+name+'-miscellaneous-fee-schedule')
source(x,'Adopted-fees-2026-12','Adopted miscellaneous fee amendments effective December 1, 2026','https://www.orb.uscourts.gov/sites/orb/files/documents/news/2026%20Fee%20Schedule%20Changes.pdf')
x['units_in_scope'][-1]['effective_from']='2026-12-01'
source(x,'JC-2026-03-fees','Judicial Conference March 2026 proceedings: fee amendment adoption evidence','https://www.uscourts.gov/sites/default/files/document/jcus-march-2026-proceedings.pdf')
data['instruments'].append(x)
for x in data['instruments']:
 for u in x['units_in_scope']:
  u.setdefault('source_unit_kind','publication' if u.get('section_list') else 'unexpanded_finite_collection')
 x['acquisition']={'text_adapter':'generic','enumeration':'Explicit section_list entries are acquisition identities. Individual CRC rule entries are rule-level targets; publication entries require J2 subdivision and do not assert one legal section. Unexpanded finite collections remain expressly unresolved.','status':'J1 selection only; J2 text acquisition and subdivision not performed.'}
p.write_text(json.dumps(data,indent=2)+'\n')
