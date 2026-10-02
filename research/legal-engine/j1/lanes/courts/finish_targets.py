import json,re,runpy
from pathlib import Path
P=Path(__file__).parent
runpy.run_path(str(P/'expand_proposals.py'))
p=P/'proposed_instruments.json';data=json.loads(p.read_text());E={x['id']:x for x in data['instruments']}
def urlblock(b):
 m=re.search(r'^.*?\((https://[^\n]+)\)$',b.strip(),re.M)
 if m:return m[1]
 m=re.search(r'Failed to fetch (https://\S+?)(?:: |: OK|$)',b)
 return m[1] if m else None
def add(x,n,h,url):x['units_in_scope'].append({'unit':n,'heading':h,'toc_url':url,'reason':'Court procedure and access dependency.','source_unit_kind':'document','section_list':[{'number':n,'heading':h,'ref':url}]})
forms={};dest={};alias={}
for f in P.glob('cacbforms*.json'):
 for b in json.loads(f.read_text()).split('--------------------------------------------------------------------------------'):
  m=re.search(r'cite(turn\d+view\d+)',b)
  if m:forms[m[1]]={'heading':b.strip().split(' | Central District')[0],'record_url':urlblock(b)}
for f in P.glob('cacbform-recover*.json'):
 s=json.loads(f.read_text());m=re.search(r'cite(turn\d+view\d+)',s);old=re.search(r'open\(\{"ref_id":"([^"]+)',s)
 if m and old:alias[m[1]]=old[1]
for glob in ['cacbpdf*.json','cacbfinal*.json']:
 for f in P.glob(glob):
  for b in json.loads(f.read_text()).split('--------------------------------------------------------------------------------'):
   m=re.search(r'click\(\{"ref_id":"([^"]+)',b);url=urlblock(b)
   if m and url and re.search(r'\.(?:pdf|docx?)(?:$|\?)',url,re.I):dest[alias.get(m[1],m[1])]=url
u=next(u for u in E['CA:CACB']['units_in_scope'] if u['unit']=='LBR-forms');u['section_list']=[];unresolved=[]
for ref,v in forms.items():
 if ref not in dest:unresolved.append(v);continue
 url=dest[ref];u['section_list'].append({'number':url.split('/')[-1],'heading':v['heading'],'ref':url,'form_record_url':v['record_url']})
u['source_unit_kind']='document';u['unresolved_form_records']=unresolved
print('CACB forms',len(forms),'resolved',len(u['section_list']),'unresolved',len(unresolved))
if unresolved:print(unresolved)
u=next(u for u in E['US:SCOTUS-RULES']['units_in_scope'] if u['unit']=='Filing-guidance-2026');u['section_list']=[]
heads=['Electronic filing guidelines March2026','Paid cases guide March2026','In forma pauperis guide March2026','Amicus guide May2026','Scheduling guidance March2026','Oral argument counsel guide OctoberTerm2024','Booklet format specifications March2026','Delivery of documents','Waiver form','Oral argument form','Circuit assignment order2022','Circuit map2022','Case distribution schedule']
for h,b in zip(heads,json.loads((P/'scotus.json').read_text()).split('--------------------------------------------------------------------------------')):
 url=urlblock(b);assert url;u['section_list'].append({'number':url.split('/')[-1],'heading':h,'ref':url})
for h,url in [('Complex civil department guidelines','https://www.occourts.org/system/files/department-guidelines.pdf'),('Probate continuance policy February2021','https://www.occourts.org/system/files/statement_on_continuances.pdf'),('Probate hearing and trial guidelines December2021','https://www.occourts.org/system/files/trial-hearing-rules-probate.pdf'),('CM03 standing order','https://www.occourts.org/system/files/general/cm03_standing_order.pdf'),('CM05 standing order','https://www.occourts.org/system/files/general/cm05_standing_order.pdf'),('CM06 standing order','https://www.occourts.org/system/files/general/cm06_standing_order.pdf'),('CM08 standing order','https://www.occourts.org/system/files/general/cm08-standing-order.pdf')]:add(E['CA-OC:SUPERIOR-ORDERS'],url.split('/')[-1],h,url)
for x in data['instruments']:
 for u in x['units_in_scope']:
  if u.get('source_unit_kind')=='publication':u['source_unit_kind']='document'
  if u.get('source_unit_kind')=='individual_rules' or u['unit'].startswith('Ethics'):u['source_unit_kind']='section'
for title,path in [('Fourth District practices and procedures; DivisionThree portions','practices-procedures'),('Fourth District fees and payments; DivisionThree portions','fees-payments')]:add(E['CA:4DCA'],path,title,'https://appellate.courts.ca.gov/district-courts/4dca/rules-forms-filing/'+path)
add(E['CA:4DCA'],'oral-argument-instructions','Fourth District oral argument, courtroom devices and security; DivisionThree portions','https://appellate.courts.ca.gov/district-courts/4dca/oral-argument-calendar')
p.write_text(json.dumps(data,indent=2)+'\n')
# Final recovered CACB record variants with download links at nonstandard positions.
records={}
for name in ['cacbmissing.json','lastcacb.json']:
 for b in json.loads((P/name).read_text()).split('--------------------------------------------------------------------------------'):
  if 'Content type: text/html' not in b:continue
  m=re.search(r'cite(turn\d+view\d+)',b)
  if m:records[m[1]]={'heading':b.strip().split(' | Central District')[0],'record_url':urlblock(b)}
u=next(u for u in E['CA:CACB']['units_in_scope'] if u['unit']=='LBR-forms')
for name in ['lastcacb.json','lastcacbpdf.json','lastdoc.json']:
 for b in json.loads((P/name).read_text()).split('--------------------------------------------------------------------------------'):
  m=re.search(r'click\(\{"ref_id":"([^"]+)',b);url=urlblock(b)
  if not m or m[1] not in records or not url or not re.search(r'\.(pdf|docx?)$',url):continue
  v=records[m[1]]
  if any(s['ref']==url for s in u['section_list']):continue
  u['section_list'].append({'number':url.split('/')[-1],'heading':v['heading'],'ref':url,'form_record_url':v['record_url']})
u['unresolved_form_records']=[]
assert len(u['section_list'])==179,len(u['section_list'])
x=E['CA:CA9'];recs={}
for f in P.glob('ca9records*.json'):
 for b in json.loads(f.read_text()).split('--------------------------------------------------------------------------------'):
  m=re.search(r'cite(turn\d+view\d+)',b)
  if m:recs[m[1]]=b.strip().split(' | United States')[0]
rows=[]
for f in P.glob('ca9pdf*.json'):
 for b in json.loads(f.read_text()).split('--------------------------------------------------------------------------------'):
  m=re.search(r'click\(\{"ref_id":"([^"]+)',b);url=urlblock(b)
  if m and url and '.pdf' in url:rows.append({'number':recs[m[1]].split('. ')[0] if recs[m[1]].startswith('Form ') else url.split('/')[-1],'heading':recs[m[1]],'ref':url})
rows.append({'number':'AO291','heading':'Application for Fees and Other Expenses under the Equal Access to Justice Act','ref':'https://www.ca9.uscourts.gov/forms/EAJA-Fees.pdf','retrieval_note':'Linked from current form record; web cache miss. Acquire direct file in J2.'})
x['units_in_scope'].append({'unit':'CA9-forms','heading':'Civil, bankruptcy and non-immigration agency appeal forms','toc_url':'https://www.ca9.uscourts.gov/filing/forms/','source_unit_kind':'document','reason':'Complete selected numbered forms and civil supplemental forms.','section_list':rows})
x['units_out'].append({'unit':'Forms2,12,23,33; criminal questionnaire; immigration informal opening brief; pro bono signup','reason':'Tax Court merits appeal, habeas/criminal, incarcerated-only and immigration litigation; program recruiting outside operating aperture.'})
add(E['CA:BAP9'],'BAP-Litigant-Manual-2026','BAP litigants manual January2026; procedural guide, not holdings authority','https://cdn.ca9.uscourts.gov/datastore/bap/2026/Litigants_Manual_2026_01_Final.pdf')
add(E['CA:4DCA'],'MiscOrder2014-1','Miscellaneous Order2014-1: rescinds2007-3 automatic rehearing-answer invitation','https://appellate.courts.ca.gov/district-courts/4dca/publication/petition-hearing-miscellaneous-order-no-2014-1')
E['CA:4DCA']['units_in_scope'][-1]['currentness_note']='Official publication summary identifies rescission effectiveMarch1,2014. Underlying signedPDF and division heading remain retrieval dependency; old2013 D3 guide is not operative evidence.'
E['CA:4DCA']['currentness_note']+=' Alternate official publication library recovered named2014-1 rehearing rescission; current practices, fees and oral-argument pages retained. D3 miscellaneous-order inventory remains unresolved, not established absent.'
p.write_text(json.dumps(data,indent=2)+'\n')
print('Final CACB179; CA9forms',len(rows))
# A shared Chapter11 tutorial is supplementary, not the disclosure/exhibits form.
u=next(u for u in E['CA:CACB']['units_in_scope'] if u['unit']=='LBR-forms')
for s in u['section_list']:
 if s['heading']=='Chapter 11 Disclosure Statement':
  s['number']='F3017-1.CH11DISCLSRSTMT.doc';s['ref']='https://www.cacb.uscourts.gov/sites/cacb/files/documents/forms/'+s['number']
 if s['heading']=='Exhibits to Chapter 11 Disclosure Statement and Chapter 11 Plan':
  s['number']='F3018.CH11.PLAN.DS.EXHIBITS.xls';s['ref']='https://www.cacb.uscourts.gov/sites/cacb/files/documents/forms/'+s['number']
E['CA:CACB']['currentness_note']+=' Disclosure statement DOC and plan-exhibits XLS are exact official links; rendering needs native document/spreadsheet handling in J2.'
p.write_text(json.dumps(data,indent=2)+'\n')

for b in (P/'root-bap-forms.txt').read_text().split('--------------------------------------------------------------------------------'):
 url=urlblock(b)
 if url:
  from urllib.parse import unquote
  add(E['CA:BAP9'],unquote(url.split('/')[-1]),unquote(url.split('/')[-1]).removesuffix('.pdf'),url)
add(E['CA-OC:SUPERIOR-ORDERS'],'CX102-Melzer-2025-04-23','Standing order for complex cases assigned to Judge Melzer, Department CX102','https://www.occourts.org/system/files/civil/civilremotehearinrules.pdf')
E['CA-OC:SUPERIOR-ORDERS']['units_in_scope'][-1]['currentness_note']='Actual PDF revised April23,2025 applies generally to cases assigned to this judge. Current department inventory and separate policies referenced inside remain unresolved.'
for ident,title,url in [('AppendixB','Liability limits for torts of minors, July1,2025','https://courts.ca.gov/system/files?file=rules-court%2Fappendix_b.pdf'),('AppendixH','Proposition65 warning cure civil penalty, April1,2024','https://courts.ca.gov/system/files?file=rules-court%2Froc-appendix-h.pdf')]:
 add(E['CA:CRC'],ident,title,url)
E['CA:CRC']['currentness_note']+=' AppendixB legacy /documents/ file is superseded2023; selected rules-court PDF is2025. AppendixH actualPDF says April1,2024 despite January2024 landing label.'
for entry in data['instruments']:
 numbers=[s['number'] for u in entry['units_in_scope'] for s in u.get('section_list',[])]
 assert len(numbers)==len(set(numbers)),entry['id']
p.write_text(json.dumps(data,indent=2)+'\n')

for entry in data['instruments']:
 for unit in entry['units_in_scope']:
  if unit.get('source_unit_kind')=='unexpanded_finite_collection':
   unit['source_unit_kind']='document'
   if not unit.get('section_list'):unit['enumeration_status']='unexpanded_finite_collection'
p.write_text(json.dumps(data,indent=2)+'\n')
