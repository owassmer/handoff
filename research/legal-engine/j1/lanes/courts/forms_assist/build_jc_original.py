"""Adjudicate the original 22 candidate families using saved publisher index rows."""
import json,re
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
from collections import Counter
P=Path(__file__).parent
rows={}
for f in [*P.glob('jc_index_*.json'),*P.glob('jc_original_*.json')]:
    if f.name in {'jc_original_selection.json'}: continue
    body=json.loads(f.read_text())
    if not isinstance(body,str):continue
    for m in re.finditer(r'^  \* ([A-Z][A-Z0-9-]*(?:\([^)]*\))*(?:\.[0-9])?) (\* )?(.+?) Effective: (.*)$',body,re.M):
        rows[m[1]]={'number':m[1],'mandatory_in_index':bool(m[2]),'heading':m[3],'effective_label':m[4],'source_capture':f.name}
for n,title,date,capture in [
 ('AT-150','Order to Terminate, Modify, or Vacate Temporary Protective Order','July 1, 1983','jc_original_completion_search.json'),
 ('FL-140','Declaration of Disclosure','July 1, 2013','jc_original_gap_records.json')]:
    rows[n]={'number':n,'heading':title,'effective_label':date,'mandatory_in_index':None,'source_capture':capture}
families='APP AT CIV CM DISC EJ FW MC PLD POS SC SUBP UD ADR CH DV EA WV TH DE GC FL'.split()
reasons={
 'APP':'Appeal and writ procedure for limited and unlimited residential civil disputes, including record, fees, service and costs.',
 'AT':'Prejudgment attachment and exemption process where a covered account claim permits attachment; no assumption that every debt qualifies.',
 'CIV':'General civil pleadings, representation, protected-party authority, judgment, debt collection and property-lien procedure applicable conditionally to covered residential disputes.',
 'CM':'General civil case management, stays, service and settlement of covered residential disputes.',
 'DISC':'Civil discovery, construction-work evidence, account evidence and unlawful-detainer discovery.',
 'EJ':'Recognition, execution, exemptions, consumer-debt procedure, satisfaction and renewal of judgments arising from covered residential disputes.',
 'FW':'Court fee waivers and associated review, including wards, conservatees and appeals.',
 'MC':'General civil filing, costs, representation, access, privacy and protected-person settlement dependencies; selected leaves already recovered in supplement.',
 'PLD':'Contract, common counts, fraud, property damage, premises liability and related tort pleading for residential performance/account disputes. Vehicle and product allegations are conditional mechanisms of covered property damage, not a separate transport or product business.',
 'POS':'Civil service and proofs, including electronic and substituted service.',
 'SC':'Small-claims filing, party authority, service, hearing, judgment, appeal/writ and enforcement of covered residential accounts.',
 'SUBP':'Civil evidence process, including premises inspection, records and interstate discovery for covered disputes.',
 'UD':'Eviction complaint, answer, trial, settlement, judgment, rental-assistance verification and habitability/partial-eviction attachments.',
 'ADR':'Civil mediation, judicial/contractual arbitration and referee procedure for covered residential disputes.',
 'CH':'Civil harassment protection affecting property access, occupant contact and performance of residential work; retains ancillary service, confidentiality, variation and compliance documents.',
 'DV':'Domestic-violence protection affecting possession, contact, access and protected household members; retains ancillary process and compliance, excludes independent custody/parentage, treatment-program and wireless-account administration.',
 'EA':'Elder/dependent-adult protection and contact rights affecting occupancy, property/account authority and access; includes associated process and compliance.',
 'WV':'Workplace-violence protection where covered premises/work create the workplace; retains associated service, variation and compliance rather than unrelated employment litigation.',
 'TH':'Transitional-housing misconduct proceedings and operative instructions for the conditional covered housing regime.',
 'DE':'Decedent authority, estate property, creditor claims, transfer and residence succession affecting ownership, notices, performance authority and payment/refund recipient.',
 'GC':'Existing or proposed guardian/conservator authority, residence/property control, claim notices and fiduciary accounting of covered residential property/accounts; excludes independent custody, medical treatment and immigration administration.',
 'FL':'Property/financial disclosure, property orders, judgment evidence, service, joinder, representation and guardian-ad-litem authority needed when a residential asset/account is subject to family-court control. Not a general divorce, custody, parentage or support proceeding.'}
fl=set(('140 141 142 144 145 150 155 158 160 161 180 190 300 300-INFO 303 304-INFO 305 306 307 308 309 310 315 316 319 320 320-INFO 321 330 330-INFO 335 335-INFO 336 337 338 340 344 345 346 371 373 375 410 411 412 415 935 936 950 955 955-INFO 956 957 958 960 980 982 985').split())
gc_ex=set(('010 070 110(P) 120 120(A) 205-INFO 207-INFO 210(CA) 210(P) 210(PE) 212 220 224 251 312 313 314 325 330 331 333 334 335 335A 336 356 380 385 505').split())
gc_account_ex={'GC-400(A)(1)','GC-400(A)(2)','GC-400(A)(3)','GC-400(A)(5)','GC-400(C)(1)','GC-400(C)(3)','GC-400(C)(6)','GC-400(C)(8)'}
dv_ex=set(('105 105(A) 105-INFO 108 125 140 145 150 180 305 325 805 815 900 901').split())
out_specific={
 'APP-060':'Standalone civil commitment/mental-health appeal; selected civil authority and conservatorship documents capture the residential authority boundary.',
 'CM-011':'Independent government False Claims Act litigation is outside the residential work/account dispute procedure.',
 'DISC-002':'Employment-law discovery for an independent employment dispute; general civil and construction discovery retained.',
 'CIV-160':'Special lien process restricted to government employees; not the general property-lien remedy.',
 'CIV-161':'Companion government-employee special lien proceeding, outside covered residential-account remedy.',
 'ADR-103':'Independent attorney-client fee arbitration dispute rather than covered residential-account arbitration.',
 'ADR-104':'Independent attorney-client fee arbitration dispute rather than covered residential-account arbitration.',
 'ADR-105':'Independent attorney-client fee arbitration instructions rather than covered residential-account arbitration.',
 'SC-101':'Independent attorney-client fee dispute attachment.',
 'SC-132':'Independent attorney-client fee dispute judgment attachment.',
 'SC-202A':'Independent attorney-client fee dispute decision.',
 'DE-270':'Independent securities-sale permission; real/personal property and representative authority retained.'}
supp=json.loads((P/'jc_supplement.json').read_text())
supp_by={u['unit']:u for u in supp['units_in_scope']}
mc_out={u['unit']:u['reason'] for u in supp['units_out'] if u['unit'].startswith('MC-')}
out_specific.update(mc_out)
aliases={'UD-106':'DISC-003','EJ-165':'WG-007','EJ-175':'WG-010','EJ-135':'WG-015','EJ-137':'WG-017','EJ-138':'WG-018','FW-015-INFO':'APP-015-INFO','FW-016':'APP-016','FW-016-GC':'APP-016-GC','FL-935':'CIV-010','FL-936':'CIV-011','DE-350':'GC-100','DE-351':'GC-101','POS-050':'EFS-050','POS-050(D)':'EFS-050(D)','POS-050(P)':'EFS-050(P)','GC-310(A-PF)':'GC-210(A-PF)'}
selected=[];excluded=[]
for n,x in sorted(rows.items()):
    fam=n.split('-')[0]
    if fam not in families:continue
    suffix=n[len(fam)+1:];why=out_specific.get(n)
    if fam=='FL' and suffix not in fl:why='Standalone marital-status, custody, parentage, support, retirement-plan, immigration or governmental support administration; no selected residential property/control/authority function. The selected FL list is deliberately finite.'
    if fam=='GC' and (suffix in gc_ex or n in gc_account_ex):why='Independent personal guardianship/custody, screening/investigation, medical, immigration, securities or unrelated income/expense subledger; property/residence authority and covered-account accounting retained.'
    if fam=='DV' and suffix in dv_ex:why='Standalone custody/parentage/abduction, treatment-program or wireless-account component, rather than possession/contact/property protection and associated procedure.'
    if why:
        excluded.append({'unit':n,'heading':x['heading'],'reason':why,'index_evidence':x['source_capture']});continue
    if n in supp_by:
        u=dict(supp_by[n]);u['original_family']=fam;selected.append(u);continue
    date=re.match(r'[A-Za-z]+ \d{1,2}, \d{4}',x['effective_label'])
    assert date,(n,x)
    date=datetime.strptime(date[0],'%B %d, %Y').date().isoformat()
    record='https://selfhelp.courts.ca.gov/jcc-form/'+quote(n,safe='-')
    acquisition={'method':'judicial_council_form_record','form_number':n,'record_url':record,'expected_form_id':n,'expected_effective_date':date,'download_link_text':'Get form '+n,'language':'en','publisher_index_url':'https://selfhelp.courts.ca.gov/find-forms/all-by-category','record_url_basis':'Official per-form jcc-form route applied to publisher-listed stable ID; resolve actual record and validate its heading/ID. If route differs, locate exact ID in publisher index and follow its actual See form info link. Never synthesize a PDF filename.','on_missing_or_ambiguous_download':'Fail acquisition; do not save HTML guidance as the form.'}
    u={'unit':n,'heading':x['heading'],'toc_url':record,'reason':reasons[fam],'source_unit_kind':'document','section_list':[{'number':n,'heading':x['heading'],'ref':record,'acquisition':acquisition}],'acquisition':acquisition,'effective_from':date,'index_mandatory_mark':x['mandatory_in_index'],'index_evidence':x['source_capture'],'edition_note':'Publisher current-index effective label, not a claim of acquired PDF bytes. J2 must validate downloaded form number and edition footer and subdivide instruction-bearing documents as needed.','original_family':fam}
    if n in aliases:u['also_numbered']=aliases[n]
    direct_alias={'CIV-010':'fl935.pdf','FL-935':'fl935.pdf','GC-210(A-PF)':'gc210apf.pdf','GC-310(A-PF)':'gc210apf.pdf','APP-016':'fw016.pdf','FW-016':'fw016.pdf'}
    if n in direct_alias:
        u['observed_direct_pdf']='https://courts.ca.gov/sites/default/files/courts/default/2024-11/'+direct_alias[n]
        u['direct_pdf_evidence']='jc_alias_evidence.json'
    other=supp_by.get(aliases.get(n,''))
    if other:u['observed_direct_pdf']=other['section_list'][0]['ref'];u['direct_pdf_evidence']=other.get('target_evidence')
    selected.append(u)
revoked=['PLD-C-500','PLD-C-505','PLD-C-520','SC-500','SC-500A','SC-500-INFO','UD-101','UD-104','UD-104(A)','UD-125']
for n in revoked:excluded.append({'unit':n,'reason':'Revoked January 1, 2026 per official publisher list; retain as a historical dependency only when an earlier act/proceeding requires it. Not a current filing form.','effective_to':'2026-01-01','source':'https://courts.ca.gov/system/files/file/publisher-list-2026-01-01.pdf','evidence':'jc_original_revoked_UD-101.json'})
excluded.append({'unit':'APP-011','reason':'Official form record states revoked January 1, 2017; stale appellate library reference does not make it current.','effective_to':'2017-01-01','source':'https://selfhelp.courts.ca.gov/jcc-form/APP-011','evidence':'jc_original_temporal_records.json'})
result={'instrument_id':'CA:JUDICIAL-COUNCIL-FORMS','adapter':'ca_court_forms','text_adapter':'ca_court_forms','as_of':'2026-10-01','replaces_candidate_families':families,'units_in_scope':selected,'units_out':excluded,'family_selection_reasoning':reasons,'counts_by_family':dict(Counter(u['original_family'] for u in selected)),'merge_instruction':'Replace original22 family placeholders with these document units. Merge supplement100 by stable form ID, then deduplicate dual-numbered physical forms; MC overlaps intentionally. Preserve aliases and current-edition notes. HTML record refs require the specified resolver, not generic whole-page acquisition.','scope_note':'Current English-base form selection from observed official index and record evidence. Conditional regimes remain conditional. All observed translated variants are separately enumerated in jc_translation_variants.json. Explicit exclusions document actual family/function boundaries, not demo-case facts.','resolver_contract':'Get the actual official record (or exact-ID index record link), match its form ID, then follow the exact English Get form ID anchor. Save PDF bytes only after MIME/signature and form identity/edition checks. A 403, missing link or mismatched date is an acquisition failure, not form text.','source_limit':'Search captures expose publisher IDs, dates and Get form labels; direct record opens returned403, so no claim that raw HTML or all link hrefs were captured. The stable ID/index-to-record route is the repeatable J1 acquisition target; J2 retrieval remains unperformed.','resolver_evidence':['jc_original_completion_search.json','jc_original_gap_records.json','jc_resolver_record_evidence.json','jc_resolver_alternate_evidence.json','jc_record_check_APP-031A.json','jc_record_check_GC-400_A__4_.json','jc_record_check_UD-106.json','jc_record_check_FL-935.json']}
result['translation_variants']='j1/lanes/courts/forms_assist/jc_translation_variants.json'
(P/'jc_original_selection.json').write_text(json.dumps(result,indent=2)+'\n')
(P/'jc_rows_expanded.json').write_text(json.dumps(list(rows.values()),indent=2)+'\n')
print(len(selected),'selected;',len(excluded),'excluded;',result['counts_by_family'])
