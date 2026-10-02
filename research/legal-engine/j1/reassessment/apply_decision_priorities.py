"""Apply reviewed source sufficiency decisions; do not infer new legal outcomes."""
import json, shutil
from pathlib import Path
B=Path(__file__).resolve().parents[2]
H=B/'j1/history/before-decision-priorities'
def read(f): return json.loads((B/f).read_text())
def write(f,v):
 p=B/f;b=H/f
 if p.exists() and not b.exists():
  b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,b)
 p.write_text(v if isinstance(v,str) else json.dumps(v,indent=2,ensure_ascii=False)+'\n')
questions={
 'Part 7': 'Determine which Part7 provisions govern older-building alterations and exposed open-eave underside materials on the relevant dates. The emergency text removes the pre-July2008 remodel exception and ordinary two-inch lumber underside option; readoption changes no substance. Use sufficient authoritative edition/status evidence, not a required administrative form.',
 'Water fees': 'Establish authoritative applicable section2200 fee text and timing for covered fill/excavation, construction and dewatering work. Compare current text with the adopted amendment only where charges or continuing obligations differ; a sufficient official schedule/history can settle this without reconstructing each filing.',
 'HOME 2025 Exhibit A': 'Identify the operative local TBRA guidelines and mandatory landlord/tenant forms affecting refund recipient, subsidy credits, termination notices and inspection corrections. Authoritative common-edition evidence can suffice; do not require both physical ExhibitA copies or compile unrelated provider administration.',
 'OEHHA': 'Use the supplied official section25705 text, current through September18,2026, as the established baseline. Resolve only whether a later or future-effective action changes the two relevant safe-harbor entries used for actual covered cleaning/repair exposure decisions; do not infer outcome from absence or require a particular filing document.'}
closed={
 'Drinking-water correction': 'Remove the separate2026-0827-01N administrative-action hunt. User confirms current authoritative drinking-water text is already available. No concrete selected-provision, reference or required historical-version discrepancy has been identified. Retain applicable drinking-water law; no new approval/date or changed-section inventory is asserted.',
 'SBSD named resolutions': 'Published general charges, classifications, owner liability and tax-roll collection plus adoption/currentness evidence are sufficient for the selected fee framework. Assessment policy separately covers vacancy, construction dumpsters and erroneous assessments. No supported unknown requires the additional complete2024-03-01 copy. Defer that copy; preserve district requirements and distinguish owner assessments from tenant liability.'}
review=read('j1/reassessment/workflow-scope-review.json')
for item in review['items']:
 n=item['item']
 if n in questions:
  item['remaining_j1']=questions[n];item['decision']='keep narrowly defined operating decision'
 if n in closed:
  item['remaining_j1']=None;item['decision']='separate document recovery is not a J1 prerequisite';item['sufficiency_reason']=closed[n]
review['integration_status']='Latest decision priorities integrated. Four targeted questions remain; DDW action hunt removed and extra SBSD resolution copy deferred on source sufficiency. Applicable source selections preserved; no J1 completion claim.'
review['integration_script']='j1/reassessment/apply_decision_priorities.py'
write('j1/reassessment/workflow-scope-review.json',review)
r=read('j1/register_updates.json')
ids={'Part 7':'CA:CCR24','Water fees':'CA:CCR23','HOME 2025 Exhibit A':'CA-HB:HOME-TBRA-PROVIDER-AGREEMENTS','OEHHA':'CA:CCR27','Drinking-water correction':'CA:CCR22','SBSD named resolutions':'CA-HB:SBSD:FINAL-ACTION-EVIDENCE'}
byid={x['id']:x for x in r['instruments']}
for n,i in ids.items():
 obj=byid[i]
 obj['remaining_item_operating_connection']=next(x.copy() for x in review['items'] if x['item']==n)
 if n in closed:
  obj.pop('j1_unresolved_selection',None)
  obj['j1_source_sufficiency']={'reason':closed[n],'decision_date':'2026-10-02','basis':'User instruction and saved-source operating-decision reassessment','review':'j1/reassessment/workflow-scope-review.json'}
 else:
  obj['j1_unresolved_selection']={'item':n,'reason':questions[n],'status':'open','next_action':'Root evaluates established sources against this decision before targeted acquisition.','audit':'j1/reassessment/workflow-scope-review.json'}
sbsd=byid[ids['SBSD named resolutions']]
sbsd['acquisition']['status']='Selected published fee framework and adoption evidence have demonstrated public acquisition routes; additional complete resolution copy deferred. Do not represent notices as the complete resolution.'
for x in sbsd.get('selected_instrument_identities',[]):
 if '2024-03-01' in x.get('identity',''):
  x['body_route_required_for_j1']=False;x['record_role']='Identified adoption; selected substantive fee terms established through published general framework'
source=B/'j1/delegation/oehha/user-official-25705.pdf'
if not source.exists():shutil.copy2('/Users/owenwassmer/Documents/View Document - California Code of Regulations.pdf',source)
byid['CA:CCR27']['user_supplied_current_text']={'path':str(source.relative_to(B)),'source':'User-supplied print of Barclays Official California Code of Regulations section25705','publisher_current_through':'2026-09-18','history_last_entry':'Amendment of(c)(2) filed2025-06-18, operative2025-10-01','scope':'Full supplied section; proposed1-bromopropane/diethanolamine additions absent','limit':'Does not independently establish the later action outcome or absence of a future-effective amendment.'}
write('j1/register_updates.json',r)
m=read('j1/reassessment/moved-items.json')
m['open']=[{'item':n,'instrument':ids[n],'reason':q,'next_action':'Evaluate sufficient authoritative evidence for this decision.'} for n,q in questions.items()]
for n,reason in closed.items():
 m['other_items']=[x for x in m['other_items'] if x['item']!=n]+[{'item':n,'decision':'Not a separate J1 document prerequisite','reason':reason}]
write('j1/reassessment/moved-items.json',m)
c=read('j1/completion.json');c['open_selection_questions']=list(questions.values());c['basis']=['Four specific operating-decision source questions remain. DDW administrative history and an additional SBSD resolution copy are not separate completion prerequisites.'];c['scope_review']['meaning']=review['integration_status'];write('j1/completion.json',c)
o=read('j1/reassessment/operating-connections.json')
for item in o['items']:
 if item['item'] in ids:
  item.update(next(x for x in review['items'] if x['item']==item['item']))
o['status']=review['integration_status'];write('j1/reassessment/operating-connections.json',o)
w=read('j1/WORK.json');w['remaining']=list(questions.values());w['coordination']='Root owns the four decision questions and integration. Delegated findings are available; no active scraping workers.'
w['tasks']=[{'task':'Apply DDW and SBSD sufficiency decisions and incorporate supplied OEHHA baseline','status':'complete'},*({'task':q,'owner':'root','status':'pending'} for q in questions.values()),{'task':'Reason through final instrument-selection sufficiency and record J1 completion when justified','owner':'root','status':'pending'}]
w['active_goal']='Finish applicable source selection for readiness and outgoing-account decisions using sufficient authoritative evidence.'
w['current_scope_review']['state']=review['integration_status'];w['current_scope_review']['narrowed_district_requirement']=closed['SBSD named resolutions']
w['latest_turn_assessment']={'classification':'decision priorities applied','reason':review['integration_status']}
w['latest_goal_turn_assessment']={'classification':'superseded retrieval objective','objective':w['active_goal']}
w['delegation']['round_status']='Historical research assignments; superseded by root-owned decision queue.'
w['delegation']['root']=list(questions.values())+['Integration and reasoned J1 completion']
write('j1/WORK.json',w)
write('PLAN.md', '''# Legal-engine plan and to-do list

Updated October 2, 2026. J0 complete. J1 remains open for four specific source decisions. J2 has not begun.

## Current work, owned by root

- [x] Remove the separate DDW no-regulatory-effect action hunt; preserve current applicable drinking-water law. Reopen only for a concrete discrepancy in a needed provision, reference or historical version.
- [x] Accept the supported SBSD general fee framework and adoption evidence as sufficient for J1 selection. Defer an additional complete resolution copy; preserve all applicable district requirements.
- [x] Save the user-supplied official section25705 baseline, current through September18,2026.
- [ ] Part7: determine the applicable older-building alteration exception and open-eave material rules using established candidate differences and authoritative edition/status evidence.
- [ ] Discharge fees: establish the authoritative applicable section2200 charges and timing for covered repair discharges.
- [ ] HOME: identify operative program guidelines and mandatory landlord/tenant forms for deposit, subsidy, notice and inspection decisions. A common-edition confirmation can suffice; individual execution choices are case evidence.
- [ ] OEHHA: reconcile only any subsequent/future-effective change to the two relevant safe-harbor entries against the supplied official baseline.
- [ ] Integrate supported answers and make the reasoned J1 completion decision.

## Working boundary

Start with the Handoff decision and assess existing authoritative evidence. Acquire more only for a demonstrated gap that could change instrument selection or applicable version. No particular administrative document is mandatory when sufficient authority establishes the answer. Neither rarity nor absence from Breakwater excludes applicable requirements. General law, conditional work requirements, local program standards and executed agreements remain distinct.

Root owns prioritization and synthesis. No new scraping round is active. Earlier delegated results support the decisions; their old retrieval lists are not current instructions. No external messages or records requests.

J1 identifies applicable sources, scope, status and routes. Full harvest and provision-level compilation follow. Structural checks support clerical consistency; source-backed reasoning establishes adequacy.

Current detail: [WORK](j1/WORK.json), [scope decisions](j1/reassessment/workflow-scope-review.json), [completion state](j1/completion.json). Prior plans and source findings are preserved under j1/history and j1/delegation.
''')
print('Applied decision priorities: four root-owned questions; DDW/SBSD document hunts removed; source selections preserved.')
