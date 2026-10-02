import json,re
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
from collections import Counter
P=Path(__file__).parent
rows={};headings=set()
for f in P.glob('jc_*.json'):
 try:s=json.loads(f.read_text())
 except:continue
 if not isinstance(s,str):continue
 headings.update(re.findall(r'^## \[Button: (.*?)\]',s,re.M))
 for m in re.finditer(r'^  \* ([A-Z][A-Z0-9-]*(?:\([^)]*\))*(?:\.[0-9])?) (\* )?(.+?) Effective: (.*)$',s,re.M):rows[m[1]]={'number':m[1],'heading':m[3],'mandatory_in_index':bool(m[2]),'effective_label':m[4],'source_capture':f.name}
rows['CARE-060-INFO']={'number':'CARE-060-INFO','heading':'Information for Respondents—About the CARE Act','mandatory_in_index':None,'effective_label':'July 1, 2026 汉语 فارسی 한국어 español Tiếng Việt','source_capture':'jc_care_rights_record.json'}
reasons={'RC':'Receiver appointment and rents/issues/profits authority determine who may direct property work and collect/pay residential accounts.','SH':'Safe at Home protected-party identity and sealing procedure applies to covered civil proceedings and notices.','REC':'Preserving/accessing court records that establish covered judgments, orders and authority; notice, transfer and retention procedures.','JURY':'Civil and expedited-jury selection procedure in covered litigation; no independent juror sanctions or criminal jury process.','EJT':'Mandatory/voluntary expedited civil trial procedure, opt-out, agreements and orders in covered residential disputes.','EM':'Minor emancipation changes capacity to contract and administer residential accounts; retain authority proceedings and financial showing, not DMV licensing.','MD':'Dangerous-dog premises safety proceedings can determine lawful access, animal conditions and safety-related work at covered property.','GDC':'Conditional gender-based pricing discrimination notice for covered work/services; not a generic all-defendants advisory.','LA':'Language assistance for court-ordered services and requests/orders to change inaccessible court requirements; preserve conditions affecting compliance.','SV':'School-violence protection where covered campus/student housing or associated residential work is implicated; all related procedural forms retained conditionally.','CR':'Victim restitution recovery/credit against covered property losses and operative criminal protective-order/termination documents affecting occupancy/contact; no independent prosecution procedure.','CARE':'Respondent rights, existing CARE order changes, notice and related-proceeding information where a covered housing arrangement depends on an existing CARE plan; independent clinical initiation/evaluation is excluded.'}
select={'JURY':{'JURY-001','JURY-003'},'EM':{'EM-100-INFO','EM-100','EM-109','EM-115','EM-130'},'CR':{'CR-110','CR-111','CR-112','CR-115','CR-160','CR-161','CR-165'},'CARE':{'CARE-060-INFO','CARE-103','CARE-113','CARE-115','CARE-116','CARE-118','CARE-119','CARE-120'}}
chosen=[]
for n,x in sorted(rows.items()):
 fam=n.split('-')[0]
 if fam not in reasons or (fam in select and n not in select[fam]):continue
 date=datetime.strptime(re.match(r'[A-Za-z]+ \d{1,2}, \d{4}',x['effective_label'])[0],'%B %d, %Y').date().isoformat()
 url='https://selfhelp.courts.ca.gov/jcc-form/'+quote(n,safe='-')
 chosen.append({'unit':n,'heading':x['heading'],'toc_url':url,'source_unit_kind':'document','section_list':[{'number':n,'heading':x['heading'],'ref':url}],'reason':reasons[fam],'effective_from':date,'index_mandatory_mark':x['mandatory_in_index'],'index_evidence':x['source_capture'],'acquisition':{'method':'judicial_council_form_record','record_url':url,'expected_form_id':n,'download_link_text':'Get form '+n,'expected_effective_date':date},'edition_note':'Publisher current-index/record label; downloaded PDF footer must be reconciled at J2.'})
selected_ids={u['unit'] for u in chosen}
existing={u['unit'] for f in ['jc_original_selection.json','jc_supplement.json'] for u in json.loads((P/f).read_text())['units_in_scope']}
assert not existing&selected_ids
outside={'ADOPT':'Independent adoption/parentage establishment; existing representative authority and protected-minor civil representation are selected through GC/CIV/FL.','BMD':'Independent vital-record correction/establishment, not residential work/account procedure.','GV':'Firearm-only restraining orders; selected CH/DV/EA/WV/SV protections cover occupancy/contact orders rather than independent gun-possession adjudication.','HC':'Custody/habeas and criminal postconviction proceeding, not residential civil recovery or authority process.','ICWA':'Indian child-welfare proceedings rather than residential property/account operation; this is not a tribal housing exclusion.','JV':'Juvenile dependency/delinquency proceedings; existing civil authority/protection documents selected separately.','NC':'Independent name/gender identity-change proceeding; an existing identity record may be evidence without initiating this proceeding.','RT':'Retail crime protection concerns retail premises/crime operations, not the covered residential premises workflow.','SUR':'Gestational carrier/parentage proceeding, not residential property/account operation.','TR':'Traffic adjudication, not covered physical property work or residential account.'}
prior_decisions={}
for f in ['jc_original_selection.json','jc_supplement.json']:
 d=json.loads((P/f).read_text())
 for u in d['units_out']:prior_decisions[u['unit']]=u['reason']
screen=[]
for fam in sorted({re.match('[A-Z]+',n)[0] for n in rows}):
 observed=[n for n in rows if re.match('[A-Z]+',n)[0]==fam];included=[n for n in observed if n in existing or n in selected_ids]
 if fam in reasons:reason=reasons[fam];status='mixed' if len(included)<len(observed) else 'selected'
 elif fam in outside:reason=outside[fam];status='excluded'
 else:reason='Reviewed in original22 or bounded supplement; retain selected IDs and explicit per-form exclusions in those artifacts.';status='mixed' if len(included)<len(observed) else 'selected'
 screen.append({'family':fam,'status':status,'reason':reason,'observed_form_count':len(observed),'selected_form_ids':sorted(included),'observed_excluded_form_ids':sorted(set(observed)-set(included))})
extra_out=[]
for n,x in rows.items():
 fam=n.split('-')[0]
 if fam in select and n not in select[fam]:
  why={'JURY':'Criminal jury or independent juror-sanctions administration.','EM':'DMV licensing consequence rather than contractual/representative capacity.','CR':'Independent prosecution, bail, diversion, sentencing, criminal firearms-compliance or criminal appeal; restitution and operative occupancy/contact-order inputs are expressly selected.','CARE':'Independent clinical eligibility evaluation, origination/referral and investigative reporting rather than existing housing-plan rights/change procedure.'}[fam]
  extra_out.append({'unit':n,'heading':x['heading'],'reason':why,'index_evidence':x['source_capture']})
extra_out.append({'unit':'FL-130(A)','reason':'Standalone family-case SCRA conditional waiver associated with dissolution origination; ordinary civil servicemember protection and financial-relief forms are separately selected.','index_evidence':'jc_full_observed_rows.json'})
result={'instrument_id':'CA:JUDICIAL-COUNCIL-FORMS','adapter':'ca_court_forms','text_adapter':'ca_court_forms','as_of':'2026-10-01','units_in_scope':chosen,'units_out':extra_out,'family_screen':screen,'observed_category_headings':sorted(headings),'scope_note':'Source-led omitted-family review supplements—not merely restates—the original22 plus15. Selected mixed families are retained generously at document level with applicability conditions; J2 subdivides actual forms/instructions. Full observed category headings and per-prefix dispositions are saved; search-index excerpts are not represented as complete raw publisher HTML.','counts_by_family':dict(Counter(u['unit'].split('-')[0] for u in chosen)),'evidence':['jc_omitted_family_evidence.json','jc_omitted_record_recovery.json','jc_omitted_index_completion.json','jc_criminal_account_boundary.json','jc_care_boundary_evidence.json','jc_care_rights_record.json']}
P.joinpath('jc_omitted_family_selection.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
P.joinpath('jc_full_observed_rows.json').write_text(json.dumps(list(rows.values()),indent=2,ensure_ascii=False)+'\n')
print(len(chosen),'additionalforms;',len(screen),'observedfamilies;',result['counts_by_family'])
