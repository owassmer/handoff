"""Build the bounded 100-form supplement from observed official source identities."""
import json,re
from pathlib import Path
from datetime import datetime
P=Path(__file__).parent
rows=json.loads((P/'jc_priority_selected.json').read_text())
assert len(rows)==100
mapping=json.loads((P/'jc_priority_pdf_map.json').read_text())
# URLs below were recovered from official search results or official reference links;
# filenames are not synthesized from form IDs.
fixed={
'WG-002':('https://courts.ca.gov/system/files/2025-07/wg002.pdf','wg002_resolved_search.json'),
'DAL-012':('https://courts.ca.gov/sites/default/files/courts/default/2024-11/dal012.pdf','jc_final_dal_recovery.json'),
'MIL-020':('https://courts.ca.gov/sites/default/files/courts/default/2024-11/mil020.pdf','jc_recover_search_MIL-020.json'),
'CP10':('https://courts.ca.gov/sites/default/files/courts/default/2024-11/cp10.pdf','jc_recover_search_CP10.json'),
'MC-013-INFO':('https://courts.ca.gov/sites/default/files/courts/default/2024-11/mc013info.pdf','jc_final_recovery.json'),
'MC-025':('https://courts.ca.gov/sites/default/files/courts/default/2024-11/mc025.pdf','jc_recover_search_MC-025.json'),
'DAL-001':('https://www.courts.ca.gov/documents/dal001.pdf','jc_leaf_recover.json'),
'WG-017':('https://courts.ca.gov/system/files/2025-12/ej137.pdf','jc_wg017_current.json'),
'MC-031':('https://www.courts.ca.gov/documents/mc031.pdf','jc_recover_search_MC-031.json'),
'MC-120':('https://www.courts.ca.gov/documents/mc120.pdf','jc_leaf_recover.json'),
'MC-356':('https://courts.ca.gov/sites/default/files/courts/default/2024-11/mc356.pdf','https://courts.ca.gov/system/files/itc/sp26-08.pdf'),
'EFS-050':('https://www.courts.ca.gov/documents/pos050.pdf','jc_recover_search_EFS-050.json'),
'WG-035':('https://courts.ca.gov/sites/default/files/courts/default/2024-11/wg035.pdf','jc_recover_search_WG-035.json'),
'WG-015':('https://courts.ca.gov/system/files/2025-12/ej135.pdf','jc_edition_resolved_WG-015.json'),
'WG-010':('https://courts.ca.gov/sites/default/files/courts/default/2024-11/ej175.pdf','jc_edition_WG-010.json'),
'WG-030':('https://courts.ca.gov/system/files?file=2025-07%2Fwg030.pdf','jc_edition_WG-030.json'),
'SUM-130':('https://courts.ca.gov/sites/default/files/courts/default/2024-11/sum130.pdf','jc_edition_resolved_SUM-130.json')}
reasons={
'WG':'Judgment recovery, protected earnings, exemption hearings and stays; includes financial-abuse garnishment conditionally where a covered residential account dispute produces that judgment.',
'VL':'Prefiling restrictions and their variation govern access to courts in residential disputes.',
'MC':'Civil filing, representation, costs, interest, protected-person settlements and court-access accommodations.',
'SUM':'Commencing civil, eviction, joint-debtor and State Housing Law proceedings; summons attachments and lost summons.',
'SER':'Sheriff service and execution instructions across residential dispute and recovery remedies.',
'RA':'Remote participation in civil proceedings, objections and court orders.',
'INT':'Civil language access and qualifications of interpreters used in proceedings.',
'JUD':'General civil judgment form governing adjudicated account resolution.',
'CP':'Prejudgment or postjudgment claims of possession by occupants in eviction proceedings.',
'CD':'Claim-and-delivery remedies for residential personal property; distinct from unlawful-detainer possession.',
'EFS':'Electronic filing, consent, exemption and service in civil cases.',
'DAL':'Construction-related access litigation where covered public-facing residential facilities are implicated; no automatic applicability to every residential unit.',
'MIL':'Servicemember petitions and orders relieving financial obligations can affect residential rent and recovery.',
'CLETS':'Law-enforcement identification supporting protective orders that affect access, contact and occupancy.',
'EPO':'Emergency protective orders affecting occupancy, contact and protected household members.'}
aliases={'WG-007':'EJ-165','WG-010':'EJ-175','WG-015':'EJ-135','WG-017':'EJ-137','WG-018':'EJ-138','EFS-050':'POS-050','EFS-050(D)':'POS-050(D)','EFS-050(P)':'POS-050(P)'}
units=[];unresolved=[]
for x in rows:
 n=x['number'];family=re.match('[A-Z]+',n)[0]
 if n in fixed:url,evidence=fixed[n]
 else:
  candidates=[u for u in mapping[n] if re.match(r'https://(?:[A-Za-z0-9-]+\.)*courts\.ca\.gov/',u)]
  assert candidates,n
  url=next((u for u in candidates if '/sites/default/files/' in u or '/system/files' in u),candidates[0]);evidence='jc_leaf_search_'+re.sub('[^A-Za-z0-9-]','_',n)+'.json'
 date=re.match(r'[A-Za-z]+ \d{1,2}, \d{4}',x['effective_label'])[0]
 unit={'unit':n,'heading':x['heading'],'toc_url':url,'reason':reasons[family],'source_unit_kind':'document','section_list':[{'number':n,'heading':x['heading'],'ref':url}],'effective_from':datetime.strptime(date,'%B %d, %Y').date().isoformat(),'index_mandatory_mark':x['mandatory_in_index'],'form_record_url':'https://selfhelp.courts.ca.gov/jcc-form/'+n,'target_evidence':evidence,'index_evidence':x['source_capture'],'edition_note':'Current effective date is the official form-index label. J2 must compare acquired footer to this date; search-result publication and URL directory dates are not edition dates.'}
 if n=='WG-002':unit['edition_note']='Official PDF search capture displays Rev. January 1, 2026, Mandatory Form and updated 30-day withholding text, agreeing with current official form record and July21 2026 Appendix A. The July2025 path is not the effective date. Direct open remained unavailable; J2 whole-document acquisition has not been performed.'
 if n in aliases:unit['also_numbered']=aliases[n]
 if n=='MIL-020':unit['edition_note']+=' Index prints July24 2022; verify footer against publisher list rather than silently normalizing to July1.'
 if n=='MC-356':unit['edition_note']+=' Current draft handbook is used only as evidence of an existing official form URL; handbook proposal is not treated as adopted authority.'
 units.append(unit)
excluded={
'WG-004':'Support-specific earnings withholding remedy; competing-order priority remains in selected ordinary garnishment forms.',
**{f'WG-0{i}':'State-tax-liability collection procedure; independent tax collection outside the residential account aperture.' for i in range(20,27)},
**{n:'Independent criminal/gang, forfeiture, media-coverage, voting-rights or court-signage administration rather than residential civil-account process.' for n in ['MC-1000','MC-200','MC-201','MC-202','MC-500','MC-510','MC-600','MC-600A','MC-800']},
**{n:'Criminal military diversion, dismissal or resentencing rather than relief from residential financial obligations.' for n in ['MIL-100','MIL-183','MIL-184','MIL-412']},
'CLETS-002':'Criminal-only confidential-law-enforcement form; shared civil protective-order identification retained as CLETS-001.',
'EPO-002':'Firearm-only emergency order does not itself govern tenancy possession or account resolution; EPO-001 protective occupancy/contact order retained.',
'RA-025':'Juvenile dependency remote appearance rather than civil operating dispute.',
'RA-030':'Juvenile dependency physical-presence request rather than civil operating dispute.',
'EFS-005-JV':'Juvenile-only electronic service consent; general civil service forms retained.',
'INT-001':'Court semiannual reporting administration; individual interpreter qualification and access forms retained.',
'INT-002(A)':'Attachment to court semiannual administrative reporting; individual qualification and access forms retained.'}
result={'instrument_id':'CA:JUDICIAL-COUNCIL-FORMS','as_of':'2026-10-01','merge_instruction':'Add the 100 document units to existing state forms selection. This is a bounded supplement, not a replacement for the original22 families. Deduplicate dual-numbered forms by leaf URL and also_numbered.','units_in_scope':units,'units_out':[{'unit':n,'reason':r} for n,r in excluded.items()],'unresolved_current_edition_targets':unresolved,'scope_note':'100 selected English-base forms in15 bounded families. All observed translations are enumerated in jc_translation_variants.json. Original families and omitted-family additions are separately adjudicated; language variants remain tied to actual publisher record links.','acquisition_note':'Official PDF identities recovered from indexed original form PDFs or official form references. Whole-document targets require J2 internal subdivision where instructions carry separate rules; this does not assert J2 text acquisition.','source_review':'j1/lanes/courts/forms_assist/REPORT.md'}
result['translation_variants']='j1/lanes/courts/forms_assist/jc_translation_variants.json'
(P/'jc_supplement.json').write_text(json.dumps(result,indent=2)+'\n')
print('Saved',len(units),'official leaf targets;',len(unresolved),'current-edition target unresolved')
