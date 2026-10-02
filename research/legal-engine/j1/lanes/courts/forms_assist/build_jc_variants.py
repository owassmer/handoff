"""Enumerate observed publisher language variants; no guessed download filenames."""
import json,re
from pathlib import Path
from urllib.parse import quote
from collections import Counter
P=Path(__file__).parent
units={u['unit']:u for fn in ['jc_original_selection.json','jc_supplement.json','jc_omitted_family_selection.json'] for u in json.loads((P/fn).read_text())['units_in_scope']}
rows={x['number']:x for x in json.loads((P/'jc_full_observed_rows.json').read_text())}
languages={'اَلْعَرَبِيَّةُ':('ar','Arabic'),'漢語':('zh-Hant','Chinese Traditional'),'汉语':('zh-Hans','Chinese Simplified'),'فارسی':('fa','Farsi'),'Hmong':('hmn','Hmong'),'한국어':('ko','Korean'),'ਪੰਜਾਬੀ':('pa','Punjabi'),'русский язык':('ru','Russian'),'español':('es','Spanish'),'Tagalog':('tl','Tagalog'),'Tiếng Việt':('vi','Vietnamese')}
variants=[]
for n,u in sorted(units.items()):
    if n not in rows:continue
    x=rows[n];tail=re.sub(r'^[A-Za-z]+ \d{1,2}, \d{4}','',x['effective_label']).strip()
    if not tail:continue
    leftover=tail
    for label,(code,name) in languages.items():
        if label not in tail:continue
        leftover=leftover.replace(label,'')
        record='https://selfhelp.courts.ca.gov/jcc-form/'+quote(n,safe='-')
        ref=record+'#language='+quote(name,safe='')
        variants.append({'unit':n+'@'+code,'base_form_id':n,'heading':u['heading']+' — '+name,'language':code,'language_name':name,'publisher_language_label':label,'source_unit_kind':'document','section_list':[{'number':n+'@'+code,'heading':u['heading']+' — '+name,'ref':ref}],'record_url':record,'resolver_selector_note':'Fragment is a local ca_court_forms selector, not a publisher PDF URL. Fetch the record without the fragment and follow the actual selected-language download href.','download_link_text':'Get form '+n+' in '+name,'index_evidence':x['source_capture'],'base_form_effective_from':u['effective_from'],'variant_effective_from':None,'edition_note':'The index effective date labels the base form record; it does not establish the translated PDF revision date. Preserve and reconcile each actual translation footer and any information-only/nonfiling restriction at acquisition.','reason':'Official language variant of a selected operating form or instruction. Included now so rights notices, service and language access are not implicitly restricted to English; exact legal use depends on the instrument and applicable notice/service rule.'})
    assert not leftover.strip(),(n,leftover)
result={'instrument_id':'CA:JUDICIAL-COUNCIL-FORMS','adapter':'ca_court_forms','text_adapter':'ca_court_forms','as_of':'2026-10-01','base_form_count':len({v['base_form_id'] for v in variants}),'variant_count':len(variants),'counts_by_language':dict(Counter(v['language_name'] for v in variants)),'units_in_scope':variants,'scope_decision':'All observed publisher-listed language variants of selected base forms are in J1 scope. They are variants of the same adopted form identity, not presumed independent regulations or automatically valid filed/service substitutes. A separately numbered required notice or instruction is its own base document, irrespective of language. Bilingual/multilingual content inside a selected PDF stays within that whole document; it must not be stripped as non-English.','resolver_contract':'The record URL plus local #language=<publisher English language name> selector identifies a concrete form-language pair. Fetch the record without fragment; select the unique anchor labeled Get form <base ID> in <language name>, allowing a matching parenthetical language display suffix; follow its actual href. Reject missing/ambiguous language, do not fallback to English, and require PDF. Deduplicate only by actual shared PDF identity while retaining all form aliases and language applicability.','completeness_limit':'This enumerates all non-English labels observed in saved current-index rows for selected forms. At record resolution also inventory actual publisher language links and reconcile any added/removed variants; missing labels in a search excerpt are not proof that no translation exists. The entry records publisher form/language identity now, not downloaded translated bytes or their individual revision dates.','evidence':['jc_translation_record_evidence.json','jc_translation_use_evidence.json'],'required_multilingual_dependency':{'form_id':'SUM-130','source':'https://courts.ca.gov/system/files/itc/spr26-07.pdf','status':'Proposal discusses AB863 requirement for a single-use multilingual summons byJanuary1 2027. Proposed layout is not represented as an adopted future form. Parent reviewing adopted statute and final council action separately.'}}
(P/'jc_translation_variants.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(result['base_form_count'],'base forms;',len(variants),'language variants;',result['counts_by_language'])
