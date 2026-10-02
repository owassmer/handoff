"""Produce reviewable full entries from lane decisions; canonical registers are read-only."""
import copy,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[3]
LANE=pathlib.Path(__file__).resolve().parent
def read(name): return json.loads((LANE/name).read_text())
canonical={x['id']:x for j in ['CA','CA-OC','CA-HB'] for x in json.loads((ROOT/f'jurisdictions/{j}/instruments.json').read_text())['instruments']}
result={}; deferred=[]
def base(id):
 if id not in result: result[id]=copy.deepcopy(canonical[id])
 return result[id]
def put(x,origin):
 x=copy.deepcopy(x); id=x['id']; aliases=x.get('aliases',[])
 if id not in canonical:
  for alias in aliases:
   if alias in canonical: id=alias; x['id']=id; break
 old=copy.deepcopy(canonical.get(id,{})); old.update(x)
 old.pop('operation',None);old.setdefault('units_out',[]);old.setdefault('jurisdiction',id.split(':')[0])
 old.setdefault('proposal_sources',[])
 if origin not in old['proposal_sources']: old['proposal_sources'].append(origin)
 result[id]=old; return old
for f,keys in [('proposal.json',['replace_instruments','add_instruments']),('utility-proposal.json',['add']),('hb/utility-proposal.json',['add_instruments']),('hb/proposal.json',['add_instruments']),('regulatory/solo-currentness.json',['add']),('regulatory/existing-agency-targets.json',['replacements'])]:
 for key in keys:
  for x in read(f).get(key,[]): put(x,f)
put(read('fuels-epp-proposal.json'),'fuels-epp-proposal.json')
hb=read('hb/proposal.json'); x=base(hb['target'])
x['units_out']=[u for u in x['units_out'] if u['unit'] not in hb['remove_units_out']]
for field,key in [('units_in_scope','add_units_in_scope'),('units_out','add_units_out')]:
 known={u['unit'] for u in x[field]}
 x[field].extend(u for u in hb[key] if u['unit'] not in known)
x['local_currentness_review']={k:hb[k] for k in ['building_currentness','currentness','version_conflicts','source_candidates']}
oc=read('oc_enactments/proposal.json')
for rec in oc['instruments']:
 rec=copy.deepcopy(rec);rec['level']='local code';rec['instrument_kind']='ordinance'
 rec['functions']=['preconditions','work_standards']
 if rec['id'].endswith('25-016'):rec['functions']=['estates_incapacity','payments']
 put(rec,'oc_enactments/proposal.json')
for rec in oc['resolutions']:
 if not rec.get('units_in_scope'):
  deferred.append({'family':'OC resolution','reason':'Adoption identified but actual operative document target/inventory is not yet established','record':rec});continue
 x=copy.deepcopy(rec);x.update(id='CA-OC:RES-'+rec['number'],jurisdiction='CA-OC',level='local code',instrument_kind='resolution',functions=['preconditions','work_standards','payments'],adapter='generic',toc_source_url=rec['source_url'],units_out=[])
 put(x,'oc_enactments/proposal.json')
def decision(d,origin):
 id=d['instrument_id']; op=d['operation']
 if op in ['add_instrument','add_dependency']:
  x=copy.deepcopy(d);url=x['source_url'];name=x.get('name',x['order'])
  x.update(id=id,jurisdiction=id.split(':')[0],name=name,level='agency rule',instrument_kind='water quality order',functions=x.pop('legal_functions'),adapter='generic',toc_source_url=url,units_out=[],units_in_scope=[{'unit':x['selected_unit'],'heading':name,'source_unit_kind':'document','section_list':[{'number':id,'heading':name,'ref':url,'source_unit_kind':'document'}]}]);x.pop('instrument_id');put(x,origin);return
 if id not in canonical and id not in result:
  deferred.append({'origin':origin,'record':d,'reason':'No canonical parent instrument'});return
 x=base(id)
 x['functions']=list(dict.fromkeys(x.get('functions',[])+d.get('legal_functions',[])))
 if op in ['append_version_record','append_version_records','amend_version_scope']:
  records=d.get('versions',[{k:v for k,v in d.items() if k not in ['operation','instrument_id','legal_functions']}])
  for r in records:
   r=copy.deepcopy(r);r['proposal_source']=origin
   if d.get('limitation'):r['limitation']=d['limitation']
   if d.get('source_url'):r.setdefault('source_url',d['source_url'])
   versions=x.setdefault('version_records',[])
   fingerprint=lambda a:(a.get('oal_file'),a.get('source_url'),a.get('name'),a.get('sections'),str(a.get('rules')))
   existing=next((i for i,v in enumerate(versions) if fingerprint(v)==fingerprint(r)),None)
   if existing is None:versions.append(r)
   else:versions[existing].update(r)
 else:
  x.update({k:v for k,v in d.items() if k not in ['operation','instrument_id','legal_functions']})
for f,key in [('regulatory/proposal.json','decisions'),('regulatory/quarterly-final-targets.json','decisions'),('regulatory/solo-currentness.json','version_records')]:
 for d in read(f)[key]:decision(d,f)
aq=read('regulatory/scaqmd-explicit-targets.json');x=base(aq['id'])
# Preserve unresolved selected regulation roots explicitly; do not pretend the known links close inventory.
roman=lambda u:re.match(r'Regulation\s+([IVX]+)',u['unit']).group(1)
known={roman(u) for u in aq['units_in_scope']}
x['units_in_scope']=[u for u in x['units_in_scope'] if roman(u) not in known]+aq['units_in_scope']
for k in ['excluded_inactive_entries','failed_rule_targets','unresolved_regulations','coverage_note']:x[k]=aq[k]
valid={x['id'] for x in json.loads((ROOT/'pipeline/chain_map.json').read_text())['functions']}
for x in result.values():
 if x['level']=='executive order':x.update(level='agency rule',instrument_kind='executive order')
 if x['id']=='CA:ZONE0-2026':x.update(level='regulation',instrument_kind='regulatory action')
 x['functions']=[{'notices':'communications','accounting':'payments','post_tenancy':'unclaimed_property'}.get(f,f) for f in x.get('functions',[])]
 assert not(set(x['functions'])-valid),(x['id'],set(x['functions'])-valid)
 for key in ['id','jurisdiction','name','level','functions','adapter','units_in_scope','units_out']:assert key in x,(x['id'],key)
(LANE/'consolidated-instruments.json').write_text(json.dumps({'as_of':'2026-10-01','status':'Reviewed full entries for coordinator integration; unresolved currentness and source dependencies remain expressly recorded','instruments':list(result.values())},indent=2)+'\n')
(LANE/'consolidation-deferred.json').write_text(json.dumps({'deferred':deferred,'remaining_files':['REMAINING_J1.md','regulatory/quarterly-final-targets.json','regulatory/proposal.json','utility-proposal.json'],'noninstrument_decisions':read('regulatory/solo-currentness.json')['decisions']},indent=2)+'\n')
print(len(result),'full entries;',len(deferred),'deferred records')
