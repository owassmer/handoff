import json,re
from pathlib import Path
P=Path(__file__).parent
lines=json.loads((P/'oc_index_lines.json').read_text());rows=[];cat=''
civil_out={'L-0089','L-0249','L-0317','L-1179','L-3008','L-0693','L-0937','L-0274','L-0288','L-0115','L-0203','L-3011'}
family_in={'L-3034','L-3035','L-0842','L-1120','L-0015','L-1124','L-0771','L-0481','L-1018','L-0965','L-3048','L-0966','OCSD3','L-3052A','L-3052B','L-3052C','L-3047','L-0221','L-0967'}
for n,s in sorted(lines.items(),key=lambda x:int(x[0])):
 m=re.search(r'### \[Button: ([^]]+)',s)
 if m:cat=m[1]
 m=re.search(r'^(.+?)\s+\|\s+cite(\d+)†(.*?)(?:\s*\|\s*(.*))?',s)
 if not m:continue
 number=m[1].strip();fid=number.replace('*','').strip();link=int(m[2]);heading=m[3];date=m[4] or ''
 included=cat in ['Civil','Probate / Mental Health','Small Claims'] or fid in family_in or fid in ['OCSD1','OCSD2','L-0338','L-1348']
 reason='Civil process, residential disputes, money recovery, evidence, protection and court access.'
 if cat=='Probate / Mental Health':reason='Estate or fiduciary authority over residential property, protected-person tenancy/account interests, estate claims and related adjudication; relevance remains conditional.'
 if cat=='Family Law':reason='Property/account control, protection, evidence, service or settlement dependency; does not authorize independent marital-status or custody workflow.'
 if fid in civil_out:included=False;reason='Driving/parking license or citation, name-change/parent notice, or criminal-exhibit procedure outside residential physical work and outgoing accounts.'
 elif not included:reason='Independent criminal, traffic, juvenile, adoption, parental-status, custody, support or marriage-dissolution proceeding; shared civil forms retained separately.'
 if fid in ['L-0338','L-1348']:reason='Victim restitution can affect recovery of property damage and double recovery; conditional ancillary remedy.'
 rows.append(dict(number=fid,heading=heading,revision_label=date,mandatory_in_index='*' in number,category=cat,index_link=link,in_scope=included,reason=reason))
# Any included occurrence retains shared form; preserve all category/date listings rather than choose conflicting index dates.
selected={}
for row in rows:
 if row['in_scope']:selected.setdefault(row['index_link'],row)
(P/'oc_rows.json').write_text(json.dumps(rows,indent=2)+'\n');(P/'oc_selected.json').write_text(json.dumps(list(selected.values()),indent=2)+'\n')
print('index rows',len(rows),'selected leaf links',len(selected))
leaf=json.loads((P/'oc_leaf_map.json').read_text());units=[]
for row in selected.values():
 url=leaf[str(row['index_link'])]['url'];assert url and not leaf[str(row['index_link'])]['failed']
 units.append({'unit':row['number']+'-'+str(row['index_link']),'heading':row['heading'],'toc_url':url,'reason':row['reason'],'source_unit_kind':'document','section_list':[{'number':row['number'],'heading':row['heading'],'ref':url}],'index_revision_label':row['revision_label'],'index_mandatory_mark':row['mandatory_in_index'],'source_index_url':'https://www.occourts.org/forms-filing/forms','index_occurrences':[x for x in rows if x['index_link']==row['index_link']]})
x={'id':'CA-OC:LOCAL-FORMS','jurisdiction':'CA-OC','name':'Orange County Superior Court local civil, small claims and conditional authority/protection forms','level':'court forms','adapter':'generic','functions':['courts_procedure'],'toc_source_url':'https://www.occourts.org/forms-filing/forms','units_in_scope':units,'units_out':[{'unit':x['number']+'-'+str(x['index_link']),'heading':x['heading'],'reason':x['reason'],'index_category':x['category']} for x in rows if not x['in_scope'] and x['index_link'] not in selected],'currentness_note':'Official live forms table inspected October 1, 2026. Revision labels and mandatory marks are preserved by category occurrence because the table repeats shared forms with conflicting labels. J2 must read each PDF footer for actual edition and any changed mandatory status. Leaf links were resolved by clicking the official table; no whole-text harvest was performed.','acquisition':{'text_adapter':'generic','enumeration':'One complete document per section_list entry; J2 subdivides internal operative instructions where relevant. L-0690, L-1051, L-0982, L-0983 overlap CA-OC:UD-FORMS and should be deduplicated by official leaf URL.','status':'122 official leaf URLs enumerated; all click requests resolved without tool fetch error.'},'source_review':'j1/lanes/courts/forms_assist/REPORT.md'}
(P/'oc_proposed_instrument.json').write_text(json.dumps(x,indent=2)+'\n')
