"""Produce a reviewable complete replacement; never write canonical registers."""
import copy,hashlib,json,re
from pathlib import Path
from collections import defaultdict,Counter
P=Path(__file__).parent
root=P.parents[3]
canonical_path=root/'jurisdictions/CA/instruments.json'
canonical=next(x for x in json.loads(canonical_path.read_text())['instruments'] if x['id']=='CA:JUDICIAL-COUNCIL-FORMS')
extra=json.loads((P/'jc_omitted_family_selection.json').read_text())
translations=json.loads((P/'jc_translation_variants.json').read_text())
aliases=json.loads((P/'jc_alias_map.json').read_text())['alias_groups']
original=json.loads((P/'jc_original_selection.json').read_text())
supplement=json.loads((P/'jc_supplement.json').read_text())
# Current canonical fields/targets win for IDs already integrated. Lane entries fill additions.
base={}
for source in [original,supplement,extra,canonical]:
 for u in source['units_in_scope']:
  if 'language' not in u or not u.get('base_form_id'):base[u['unit']]=copy.deepcopy(u)
current_ids={u['unit'] for u in canonical['units_in_scope']}
def direct(u):return all('/jcc-form/' not in s['ref'] for s in u['section_list'])
representative={n:n for n in base};groups={n:[n] for n in base};group_evidence={}
for g in aliases:
 ids=g['form_ids'];assert all(n in base for n in ids),ids
 dates={base[n].get('effective_from') for n in ids};assert len(dates)==1,(ids,dates)
 # Preserve already selected concrete PDF rather than returning to a record route.
 rep=next((n for n in ids if n in current_ids and direct(base[n])),ids[0])
 for n in ids:representative[n]=rep;groups.pop(n,None)
 groups[rep]=ids;group_evidence[rep]=g
base_units=[]
for rep,ids in sorted(groups.items()):
 u=copy.deepcopy(base[rep]);members=[base[n] for n in ids]
 g=group_evidence.get(rep)
 if g and not direct(u) and g.get('observed_direct_pdf'):
  u['toc_url']=g['observed_direct_pdf'];u['section_list'][0]['ref']=g['observed_direct_pdf'];u['target_evidence']=g['evidence']
 u['unit']=rep;u['form_ids']=sorted(ids);u['variant_kind']='base_form';u['source_unit_kind']='document'
 u['section_list'][0]['number']=rep;u['section_list'][0]['source_unit_kind']='document'
 u['reasons_by_form_id']={n:base[n]['reason'] for n in ids}
 u['functions']=sorted(set(canonical.get('functions',[])+sum([m.get('functions',[]) for m in members],[])))
 if len(ids)>1:
  u['aliases']=[n for n in ids if n!=rep];u['alias_evidence']=g['evidence'];u['reason']=' '.join(dict.fromkeys(m['reason'] for m in members))
  u['alias_source_metadata']=[{k:m[k] for k in ['unit','heading','effective_from','index_evidence','index_mandatory_mark','edition_note','original_family'] if k in m} for m in members]
  u['alternate_acquisition_targets']=list(dict.fromkeys([s['ref'] for m in members for s in m['section_list']]+([g['observed_direct_pdf']] if g.get('observed_direct_pdf') else [])))
  u['alternate_acquisition_targets']=[r for r in u['alternate_acquisition_targets'] if r!=u['section_list'][0]['ref']]
 u.pop('also_numbered',None)
 base_units.append(u)
variant_groups=defaultdict(list)
for v in translations['units_in_scope']:
 assert v['base_form_id'] in representative,v['unit']
 variant_groups[(representative[v['base_form_id']],v['language'])].append(v)
variant_units=[]
for (rep,language),variants in sorted(variant_groups.items()):
 chosen=next((v for v in variants if v['base_form_id']==rep),variants[0]);u=copy.deepcopy(chosen)
 u['unit']=rep+'@'+language;u['base_form_id']=rep;u['source_base_form_id']=chosen['base_form_id'];u['form_ids']=sorted(groups[rep]);u['variant_kind']='translation';u['variant_ids']=[v['unit'] for v in variants]
 u['toc_url']=u['record_url'];u['section_list'][0]['number']=u['unit'];u['section_list'][0]['source_unit_kind']='document';u['functions']=list(canonical.get('functions',[]))
 u['alternate_variant_records']=[{'variant_id':v['unit'],'record_url':v['record_url'],'ref':v['section_list'][0]['ref'],'index_evidence':v['index_evidence']} for v in variants if v is not chosen]
 u['reasons_by_form_id']={n:base[n]['reason'] for n in groups[rep]}
 u['reason']+=' '+ ' '.join(dict.fromkeys(u['reasons_by_form_id'].values()))
 u['edition_note']+=' Shared alias-language records are alternate acquisition routes, not additional fetches. If actual downloads differ by revision, preserve a version conflict rather than collapse distinct editions.'
 variant_units.append(u)
result=copy.deepcopy(canonical)
result['units_in_scope']=base_units+variant_units
outs={}
for d in [original,supplement,extra,canonical]:
 for u in d['units_out']:outs[u['unit']]=copy.deepcopy(u)
assert not set(outs)&set(base)
result['units_out']=list(outs.values())
result['functions']=sorted(set(result.get('functions',[])+['landlord_tenant','payments','debt_collection','work_standards','anti_discrimination','housing_assistance']))
result['scope_note']='Selected source-led civil, property/account, representative-authority and conditional housing/protection forms, including published language variants. Original family placeholders, omitted-family screen and explicit per-form exclusions are reconciled; no English-only scope exclusion. Translation identity is selected without asserting translation-specific effective dates or filing/service sufficiency.'
result['acquisition']={'text_adapter':'ca_court_forms','enumeration':'One explicit document target per confirmed physical base-form identity and per language variant. Direct publisher PDFs are preserved. Record references follow exact Get form ID or selected-language anchor; fragment language selectors are local adapter metadata. Never acquire record guidance as form content.','status':'J1 source selection; J2 PDF acquisition, edition reconciliation, internal subdivision and passage-level reference discovery remain pending.'}
result['resolver_contract']=translations['resolver_contract']
result['family_selection_reasoning']=copy.deepcopy(original['family_selection_reasoning'])
for u in supplement['units_in_scope']:
 fam=re.match('[A-Z]+',u['unit'])[0];result['family_selection_reasoning'].setdefault(fam,u['reason'])
for decision in extra['family_screen']:result['family_selection_reasoning'].setdefault(decision['family'],decision['reason'])
result['family_screen']=extra['family_screen'];result['alias_groups']=aliases
result['source_review']=list(dict.fromkeys(result.get('source_review',[])+['j1/lanes/courts/forms_assist/REPORT.md','j1/lanes/courts/forms_assist/INTEGRATED_REVIEW.md']))
result['source_inputs']=['jc_original_selection.json','jc_supplement.json','jc_omitted_family_selection.json','jc_translation_variants.json','jc_alias_map.json']
result['integration_counts']={'source_base_form_ids':len(base),'base_document_acquisitions':len(base_units),'source_language_variant_ids':len(translations['units_in_scope']),'language_document_acquisitions':len(variant_units),'total_document_acquisitions':len(result['units_in_scope']),'confirmed_alias_groups':len(aliases),'additions_vs_canonical_ids':len(set(base)-current_ids)}
result['canonical_input_sha256']=hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest()
result['language_variant_reconciliation_note']=translations['completeness_limit']
result['future_source_review']='j1/lanes/courts/forms_assist/future_form_dependencies.json'
result.pop('pending_source_variants',None);result.pop('translation_variants',None)
# Every current direct acquisition remains the chosen target or an explicit same-form alternate.
retained={r for u in base_units for r in [*[s['ref'] for s in u['section_list']],*u.get('alternate_acquisition_targets',[])]}
assert all(s['ref'] in retained for u in canonical['units_in_scope'] if direct(u) for s in u['section_list'])
assert {n for u in base_units for n in u['form_ids']}==set(base)
assert {v for u in variant_units for v in u['variant_ids']}=={u['unit'] for u in translations['units_in_scope']}
ids=[u['unit'] for u in result['units_in_scope']];assert len(ids)==len(set(ids))
refs=[s['ref'] for u in result['units_in_scope'] for s in u['section_list']];assert len(refs)==len(set(refs))
assert all(u['source_unit_kind']=='document' for u in result['units_in_scope'])
assert all(u['variant_effective_from'] is None for u in variant_units)
(P/'judicial_council_integrated_replacement.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(result['integration_counts'],indent=2))
