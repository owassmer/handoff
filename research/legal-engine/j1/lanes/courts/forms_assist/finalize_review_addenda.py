import json,re
from pathlib import Path
P=Path(__file__).parent
import runpy
runpy.run_path(str(P/'build_review_addenda.py'))
p=P/'fcc76_proposed_instrument.json';d=json.loads(p.read_text())
old='2026-09-28';new='2026-09-30';base=f'https://www.ecfr.gov/api/versioner/v1/full/{new}/title-47.xml?part=76'
d=json.loads(json.dumps(d).replace(old,new));d['version_date']=new
titles={'H':'General Operating Requirements','N':'Cable Rate Regulation','P':'Competitive Availability of Navigation Devices','T':'Notices'}
reasons={'H':'Operator as subscriber/master-account customer: installation/repair service standards, billing dispute/refund/termination handling and truthful price presentation. Duties owed by providers can govern the operator account.','N':'Conditional regulated cable rates, equipment/installation charges and refund remedies affect lawful master-account bills and allocation; preserve applicable definitions, jurisdiction and exemptions rather than assume all systems regulated.','P':'Subscriber rights to attach/use navigation devices, equipment availability, security interfaces and device sale/lease pricing govern covered equipment work and accounts.','T':'Provider notices of rate/service changes, customer charges and termination-related changes can control account correction and service continuity; retain complete mixed notice subpart for J2 applicability review.'}
for sub in titles:
 u={'unit':'Subpart '+sub,'heading':titles[sub],'toc_url':base+'&subpart='+sub,'reason':reasons[sub]}
 if sub=='H':u['section_list']=[{'number':'76.309','heading':'Customer service obligations','ref':base+'&section=76.309'},{'number':'76.310','heading':'Truth in billing and advertising','ref':base+'&section=76.310'}]
 d['units_in_scope'].append(u)
d['units_out']=[u for u in d['units_out'] if u['unit'] not in {'Subpart '+x for x in titles}]
heads={}
for f in ['fcc76_k_dependency_evidence.json','fcc76_k_exact_headings.json']:
 for m in re.finditer(r'#### § (76\.\d+) ([^\n]+)',json.loads((P/f).read_text())):heads[m[1]]=m[2].rstrip('.')
for n in ['76.605']+[f'76.{i}' for i in range(610,618) if i != 615]:
 assert n in heads,n
 d['units_in_scope'].append({'unit':n,'heading':heads[n],'toc_url':base+'&section='+n,'reason':'Full section retained as an express signal-leakage/capping technical dependency of selected cable wiring work; J2 retains relevant conditions and exceptions.','section_list':[{'number':n,'heading':heads[n],'ref':base+'&section='+n}]})
d['units_out'].append({'unit':'76.615','reason':'No operative76.615 heading appears in the current official K body between76.614 and76.616; do not synthesize a section from the incorporated610–617 range. This is not an asserted repeal date.'})
d['incorporated_dependencies']=[{'ref':'47 USC 522','target_instrument':'US:47USC-CABLE-DEFINITIONS-COMPETITION','reason':'Complete definition section;MVPD definition expressly incorporated in76.800(c). Existing47USC227 does not cover it.'},{'ref':'47 USC 548','target_instrument':'US:47USC-CABLE-DEFINITIONS-COMPETITION','reason':'Complete section determining covered MVPD entity and competition scope under76.2000. Existing47USC227 does not cover it.'}]
d['name']='FCC cable subscriber accounts, inside wiring and multiple-dwelling-unit provider access'
d['currency_note']='Official current title47 page, accessedOctober1 2026, displays up-to-date and last-amendedSeptember30 2026. All targets therefore use2026-09-30. Cached individual subpart pages displaySeptember24/28/29; those support identity/TOC, not proof that September30 text is unchanged. Dated API retrieval/comparison was unavailable in this pass; J2 must retrieve the selected current release rather than reuse cached older text.'
d['source_evidence']+=['fcc76_currentness.json','fcc76_customer_subparts.json','fcc76_latest_change_and_pt.json','fcc76_k_dependency_evidence.json','fcc76_k_exact_headings.json']
d['acquisition']['enumeration']='Expand complete selected H/M/N/P/T/X subparts and explicit76.605/610–617 full sections from datedSeptember30 official eCFR XML; deduplicate76.309 as already withinH. Preserve conditional regulated-rate and provider/subscriber scope.'
d['scope_note']='Conditional master-account/customer, wiring/property-work and MDU-provider-contract scope; do not exclude a duty merely because the provider owes it. Broadcast content, carrier franchise/ownership and reporting administration remain outside the covered operating function.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
zipurl='https://uscode.house.gov/download/releasepoints/us/pl/119/111/xml_usc47@119-111.zip'
stat={'id':'US:47USC-CABLE-DEFINITIONS-COMPETITION','jurisdiction':'US','name':'Cable statutory definitions and competition scope','level':'statute','adapter':'usc','functions':['provider_contracts','work_standards','payments','landlord_tenant'],'toc_source_url':zipurl,'units_in_scope':[{'unit':'47 USC '+n,'heading':h,'toc_url':zipurl,'uslm_identifier':'/us/usc/t47/s'+n,'reason':r} for n,h,r in [('522','Definitions','Complete cable definitions governing selected47CFR76 sources.'),('548','Development of competition and diversity in video programming distribution','Complete statutory competition and covered-MVPD scope incorporated by76.2000; retain conditions and exceptions.')]],'units_out':[],'acquisition':{'text_adapter':'usc','enumeration':'Acquire complete two identified sections with notes from the shared verified119-111 release.'},'version_note':'OLRC official section522 search record reports laws in effectSeptember18 2026; shared register release119-111 is the same publisher release. No XML bytes asserted.','source_evidence':'j1/lanes/courts/forms_assist/fcc_cable_statute_dependencies.json','existing_coverage_check':'US:47USC227 selects onlysection227; neither522 nor548 is covered. This addendum closes that exact gap, not a claim to select the whole Cable Act.'}
(P/'fcc_cable_statute_proposal.json').write_text(json.dumps(stat,indent=2,ensure_ascii=False)+'\n')
extra=P/'jc_omitted_family_selection.json';e=json.loads(extra.read_text());e['units_out']=[u for u in e['units_out'] if u['unit']!='FL-130(A)'];e['units_out'].append({'unit':'FL-130(A)','reason':'Standalone family-case SCRA declaration/conditional waiver associated with appearance and dissolution origination; ordinary civil servicemember protection and financial-relief forms are selected separately.','index_evidence':'jc_full_observed_rows.json'});extra.write_text(json.dumps(e,indent=2,ensure_ascii=False)+'\n')
print('FCC:',len(d['units_in_scope']),'units;',len(d['units_out']),'other TOC boundaries; two USC sections.')
