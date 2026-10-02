"""Build court-register proposals; shared registers are integrated by coordinator."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent
existing={x['id']:x for j in ('US','CA','CA-OC') for x in json.loads((ROOT/'jurisdictions'/j/'instruments.json').read_text())['instruments']}
proposals={}
def base(id,name=None):
 x=json.loads(json.dumps(existing.get(id,{'id':id,'jurisdiction':id.split(':')[0],'name':name,'level':'court rule','functions':['courts_procedure'],'adapter':'generic','units_in_scope':[],'units_out':[]})))
 x['units_in_scope']=[];x['adapter']='generic'
 x['acquisition']={'text_adapter':'generic','enumeration':'section_list entries are whole named publications, not individual-rule enumeration. J2 must split rules and preserve headings, appendices, effective dates and amendment history before semantic work. Units with toc_url and no section_list require expansion of the stated finite source family.','status':'J1 publication and unit selection; J2 text acquisition and subdivision not performed.'}
 x['source_review']='j1/lanes/courts/REPORT.md';proposals[id]=x;return x
def doc(x,num,title,url,reason='Procedural conditions, evidence, participation, recovery or dispute resolution within the residential operating aperture.'):
 x['units_in_scope'].append({'unit':num,'heading':title,'toc_url':url,'reason':reason,'section_list':[{'number':num,'heading':title,'ref':url}]})
def family(x,num,title,url,reason):
 x['units_in_scope'].append({'unit':num,'heading':title,'toc_url':url,'reason':reason})
def excluded(x,u,reason):x['units_out'].append({'unit':u,'reason':reason})
for ident,label,scope in [('FRCP','civil-procedure','Titles I–XI, Rules 1–86; Supplemental Rules A–G; supplemental Social Security rules'),('FRE','evidence','Articles I–XI, Rules 101–1103'),('FRAP','appellate-procedure','Titles I–VII, Rules 1–48; Appendix of Forms and length limits'),('FRBP','bankruptcy-procedure','Rule 1001 and Parts I–IX, Rules 1002–9038; all bankruptcy chapters and adversary/appeal procedures')]:
 x=base('US:'+ident);x['units_out']=[]
 doc(x,ident+'-2025',scope,'https://www.uscourts.gov/sites/default/files/document/federal-rules-of-'+label+'.pdf','Complete rulebook retained: cross-rule references and owner/tenant/provider debtor or creditor roles make narrower litigation-stage selection unsafe. Criminal-only applications remain conditional rather than separate operating workflows.')
 x['currentness_note']='Official current-rules page checked October 1, 2026. Rulebook dated December 1, 2025; FRE last substantive amendments 2024. Future adopted changes separately registered in US:RULES-2026-12.'
x=base('US:RULES-2026-12','Adopted federal rules and forms amendments for December 1 2026')
x['toc_source_url']='https://www.uscourts.gov/forms-rules/pending-rules-and-forms-amendments'
doc(x,'2026-congressional-package','April 8, 2026 Supreme Court promulgation package: Appellate Form 4; Bankruptcy Rules 1007, 3018, 5009, 7043, 9006, 9014, 9017; Evidence Rule 801','https://www.uscourts.gov/sites/default/files/document/2026_congressional_package_final.pdf')
family(x,'Bankruptcy-forms-2026','Official Forms 101 and 106C, effective December 1, 2026','https://www.uscourts.gov/forms-rules/pending-rules-and-forms-amendments','Official pending page footnote places these forms in December 2026 despite listing under the 2027 rules heading; acquire approved clean forms and approval report, not 2027 proposed rule text.')
x['effective_from']='2026-12-01';x['units_out']=[]
excluded(x,'2027 proposed FRAP 15,29,32/length limits; FRBP2002; FRCP7.1,26,41,45,81; Criminal17','Not Supreme Court-promulgated future rules at October 1, 2026. Evidence609 withdrawn before September2026 Judicial Conference.')
x=base('US:SCOTUS-RULES','Supreme Court rules');x['toc_source_url']='https://www.supremecourt.gov/filingandrules/rules_guidance.aspx'
doc(x,'SCOTUS-2026','Rules of the Supreme Court, complete Rules 1–48, effective March 16, 2026','https://www.supremecourt.gov/filingandrules/2026RulesoftheCourt_WEB.pdf')
family(x,'Filing-guidance-2026','March2026 electronic filing guidelines, paid/IFP guides, scheduling guidance and booklet specifications; May2026 amicus guide; waiver and oral-argument forms',x['toc_source_url'],'Retained filing instructions and prescribed forms, distinct from merits authority; current linked documents enumerated at J2.')
x['currentness_note']='March 16, 2026 revision is operative, not future.'
x=base('CA:CACD');x['units_out']=[]
doc(x,'Chapter-I-2026-06','Chapter I Local Civil Rules (June 1, 2026)','https://www.cacd.uscourts.gov/sites/default/files/documents/2026-June-LRs-Chap-1.pdf')
doc(x,'Chapter-IV-2015-12','Chapter IV Local Rules Governing Bankruptcy Appeals, Cases and Proceedings (December 1, 2015)','https://www.cacd.uscourts.gov/sites/default/files/documents/LRs%20Effective%202015%20December%201%20-%20Chapter%204_0.pdf')
family(x,'Chapter-II','Chapter II Local Rules for Admiralty and Maritime Claims and Asset Forfeiture Actions',x['toc_source_url'],'Retain civil asset-forfeiture/property-claim procedure where premises or property are subject to forfeiture; maritime-only provisions are out at J2 subdivision. Exact chapter PDF linked from official local-rules page.')
excluded(x,'Chapter III Criminal rules','Standalone criminal prosecution outside aperture; civil forfeiture remains in Chapter II.')
ids=['11-10','25-05','23-07','13-05','26-11','25-07','25-04','23-06','06-01','05-07','11-15','24-01','17-08','23-08','22-05','16-04','13-15','11-09','356','235']
titles=['ADR program','Attorney admission, renewal and pro hac vice fees','Bankruptcy rulemaking','Bankruptcy reference and appeals','District judge case assignment','Voluntary magistrate consent','Direct assignment to magistrate judges','Magistrate judge duties amendment','Magistrate judge duties amendment','Magistrate judge duties','Court reporter plan','Grand and petit jury plan','Extended juror fees','Coronavirus emergency rescission','Vaccination/testing rescission','Registry funds','Interpreter plan','Information technology policy','Court discrimination policy','Custodian for seized property']
cap=json.loads((OUT/'capture-19.json').read_text());urls=re.findall(r'^.*?\((https://[^\n]+\.pdf)\)$',cap,re.M)
assert len(urls)==len(ids),(len(urls),len(ids))
for no,title,url in zip(ids,titles,urls):doc(x,'GO-'+no,title,url)
excluded(x,'Operative-index criminal counsel/sentencing/probation/criminal duty/Speedy Trial/naturalization/patent/library/personnel-appointment and security-equipment orders','Separate criminal, immigration, patent or internal court-management subjects; no residential civil claim procedure. Historical orders are not made current by index presence.')
x['currentness_note']='Checked operative by-subject index and June2026 rules October1. Index still repeats older voluntary/direct-assignment orders; latest 25-07/25-04 govern their stated replacements. General orders retained with promulgated date; archives only for event-time dependencies.'
x=base('CA:CACB');x['units_out']=[]
doc(x,'LBR-complete','Local Bankruptcy Rules 1001-1 through 9075-1, complete','https://www.cacb.uscourts.gov/sites/cacb/files/documents/local_rules/COMPLETE%20LBRS%20double-sided.pdf')
family(x,'LBR-forms','Complete current LBR forms, 1002-1 through 9075-1','https://www.cacb.uscourts.gov/forms/local_bankruptcy_rules_forms','Retain all debtor/creditor chapters and contested/adversary proceedings, including stay relief, proof of service, claims, default and judgment; official table gives exact form numbers and leaf links.')
family(x,'TCG-supplements','Central Guide supplements 1002-1(c),(d);1007-1;1071-1(a)(1),(2);2002-2(a);3007-1;3015-1;5003(a)-(b),(e);5005-2(d);5005-4;5010-1;5075-1;7054-1;9004-1;9006;9021-1,(c)(7);9075-1',x['toc_source_url'],'Named twenty-supplement collection is the court’s filing/service implementation, including address/venue and fee dependencies.')
for no,title,path in [('26-01','Sealed documents','GO%2026-01.pdf'),('23-02-amended-2026','Complex Chapter11 case and pre-filing procedure','Amended%20GO%2023-02.pdf'),('23-01','Phased reopening, judge copies and remote appearances','GO%2023-01.pdf'),('22-02','Order vacating obsolete or superseded orders','GO%2022-02.pdf')]:doc(x,'GO-'+no,title,'https://www.cacb.uscourts.gov/sites/cacb/files/documents/general-orders/'+path)
ids=['24-01','22-03','22-01','20-01-amended','96-05-sixth','19-01','16-01','13-01-amended','09-01-first-amended','11-02','11-01','95-01-third','09-01-vacatur','05-01','02-04','01-01','97-01','88-0']
titles=['Loan modification program','Vaccination/testing rescission','Recording prohibition','SBRA interim rules (event-time)','Attorney discipline','Appropriation lapse operations','Vacatur order','Registry funds','Interim1007-I amendment','Estate bank fees','Related cases and recusal','Mediation program','Vacatur order','Electronic fee refunds','Vacatur order','Fee payment','Vacatur order','Revocation order']
cap=json.loads((OUT/'capture-20.json').read_text());urls=re.findall(r'^.*?\((https://[^\n]+\.[pP][dD][fF])\)$',cap,re.M)
assert len(urls)==len(ids),(len(urls),len(ids))
for no,title,url in zip(ids,titles,urls):doc(x,'GO-'+no,title,url)
excluded(x,'GO23-03 student-loan Department-of-Education discharge guidelines','Distinct student-loan discharge litigation; ordinary residential claims use retained adversary rules.')
excluded(x,'GO20-02 variants;20-03;20-04;20-05;20-06 variants;20-07;20-09;20-11;20-12;21-01;21-02;21-03;21-04;21-05;21-06;original23-02','Vacatur/supersession established by 22-02,23-01,22-03 and amended23-02. Preserve archival recovery for historical events, do not treat directory entries as operative.')
excluded(x,'GO20-08 and20-10','Woodland Hills/Santa Barbara courthouse-entry overlays outside current Santa Ana forum; districtwide procedures retained.')
x['currentness_note']='Directory is mixed current/historical. GO22-02 vacates listed COVID orders; GO23-01 supersedes21-05. Amended23-02 is March10,2026 and26-01 is May2026. Interim rules must retain applicability period rather than override subsequent national rules.'
x=base('CA:CA9');x['units_out']=[]
doc(x,'Handbook-2026-06','FRAP, Ninth Circuit Rules and Circuit Advisory Committee Notes, June1,2026','https://cdn.ca9.uscourts.gov/datastore/uploads/frap-June%201%202026.pdf')
doc(x,'General-orders-2025-06','Ninth Circuit General Orders, June25,2025','https://cdn.ca9.uscourts.gov/datastore/uploads/rules/general_orders/general_orders_20250625.pdf','Complete finite internal-operating publication retained for en banc/assignment/processing dependencies; does not confer substantive rights merely because included.')
doc(x,'Admin-2023-06-16','Appellate Case Management System administrative order','https://cdn.ca9.uscourts.gov/datastore/general/2023/06/16/Admin-order-final-June-2023.pdf')
doc(x,'Admin-HSD-2021','Highly Sensitive Documents administrative order','https://cdn.ca9.uscourts.gov/datastore/general/2021/10/Draft_Adminorder_signed_1.16.21%20.pdf')
excluded(x,'Admin2022 prisoner e-filing;2021 name change;2019 CJA Unit and CJA paper-copy order','Prisoner-specific, judicial name or criminal appointment administration; no ordinary residential civil/bankruptcy filing duty.')
excluded(x,'September2026 proposed miscellaneous circuit-rule revisions','Public proposal, not adopted future law as of October1,2026.')
x=base('CA:BAP9');x['units_out']=[]
doc(x,'BAP-2015','BAP Rules adopted February24,2000, revised June15,2015, complete','https://cdn.ca9.uscourts.gov/datastore/bap/2015/06/18/baprules.pdf')
excluded(x,'September2026 proposed miscellaneous BAP revisions','Public proposal, not adopted future law as of October1,2026.')
x=base('CA:4DCA');x['units_out']=[]
family(x,'Local-Rules-1-3','Rule1 Writ Proceedings; Rule2 Automatic Extensions for Briefs in Omitted Records; Rule3 Original Superior Court File','https://appellate.courts.ca.gov/district-courts/4dca/rules-forms-filing/local-rules-orders','Rule1/3 civil procedures retained; Rule2 retained for scope qualification (references criminal record8.340). Current HTML records Rule5 repeal October24,2025, unlike old2024 PDF.')
doc(x,'D3-IOPP-2026-03','DivisionThree Internal Operating Practices and Procedures, March24,2026','https://appellate.courts.ca.gov/system/files/forms-filing/iop_district4_division3.pdf')
doc(x,'4D-Efiling','Fourth District electronic filing requirements','https://appellate.courts.ca.gov/district-courts/4dca/rules-forms-filing/electronic-filing')
excluded(x,'Rule4 Civil Settlement Conferences (DivisionTwo only)','Not DivisionThree current forum; attach if appeal transferred.')
excluded(x,'Former Rules5–10','Rule5 repealed October24,2025;6–9 repealed;10 renumbered3.')
x['currentness_note']='Current official HTML search capture recovered Rule5 repeal and Rules1–4. Direct open returned403. March24,2026 DivisionThree IOPP identified. DivisionThree miscellaneous orders are supplied by clerk request, not a public enumerable list; see REPORT outstanding dependency.'
x=base('CA-OC:SUPERIOR-RULES');x['units_out']=[]
for no,title,path in [('Preface','Civility Guidelines','civility_guidelines_-_preface_to_local_rules.pdf'),('Division1','Court organization','local_rule_180_d1d.pdf'),('Division3','Civil rules including limited, small claims and all civil cases; AppendixA','local-rules/12div3.pdf'),('Division4','Civil cases over $35,000','local-rules/09div4.pdf'),('Division5','Appellate division','20div5.pdf'),('Division6','Probate, creditors, estates, guardianship, conservatorship','local-rules/div6.pdf'),('Division7','Family law; protective/property authority dependencies','local-rules/div7.pdf')]:doc(x,no,title,'https://www.occourts.org/system/files/'+path)
for no,reason in [('Division2','Internal personnel administration; court-access emergency orders separately retained.'),('Division8','Standalone criminal prosecution.'),('Division9','Standalone juvenile proceedings.'),('Division10 EmergencyRule1','By its own text case-management suspension ended March31,2021; current index inclusion does not revive it.')]:excluded(x,no,reason)
x['currentness_note']='Official current-edition index says July1,2025. October5,2026 comment deadline covers proposed868/909/700.7/710.1/720; not adopted future rules. Division10 text expressly expired March31,2021.'
x=base('CA-OC:SUPERIOR-ORDERS','Orange County Superior Court civil, probate and appellate procedural orders');x['toc_source_url']='https://www.occourts.org/divisions/civil/civil-appearance-procedure-and-information'
for no,title,path in [('Appellate26-01','Use of Generative Artificial Intelligence (August6,2026)','local-rules/appellate-division-administrative-order-no-2601-use-generative-artificial-intelligence.pdf'),('23-06','Updated remote appearance guidelines for civil and probate','general/administrativeorder23_06_updatedremoteappearances.pdf'),('Appellate21-01','Appellate division videoconferencing','administrativeorder21_01appellatedivisionvideoconferencingorder.pdf'),('AC01-22','Small claims electronic evidence','adminorderac01-22.pdf')]:doc(x,no,title,'https://www.occourts.org/system/files/'+path)
cap=json.loads((OUT/'capture-21.json').read_text());urls=re.findall(r'^.*?\((https://[^\n]+\.pdf)\)$',cap,re.M)
for k,(title,url) in enumerate(zip(['SmallClaims','UD','ProtectiveOrders','RemoteGuidelines','UnlimitedComplex','Limited','ProbateMentalHealth','AppellateDivision'],urls[1:])):doc(x,'Appearance-'+title,title+' appearance and procedure instructions',url)
family(x,'Department-orders','Civil limited/unlimited/complex and probate courtroom requirements','https://www.occourts.org/divisions/civil/civil-calendar-information','Attach orders of assigned department at action time. J1 selects source family; no assumption that generic county rules displace department-specific scheduling/filing orders.')
x=base('CA-OC:UD-FORMS','Orange County local unlawful-detainer forms');x['toc_source_url']='https://www.occourts.org/forms-filing/forms/unlawful-detainer-local-forms'
for num,title,path in [('L690','Application and order for posting summons','l690.pdf'),('L1051','Application for writ of possession','l1051.pdf'),('L982','UD105 answer attachment3.t.a','civil/l982.pdf'),('L983','UD105 answer attachment3.t.b','civil/l983.pdf'),('OCSD5','Sheriff eviction instructions','ocsd5.pdf')]:doc(x,num,title,'https://www.occourts.org/system/files/'+path)
# CRC title selections remain broad, but each title gets its actual TOC. Forms are their own source family.
x=base('CA:CRC');old=existing['CA:CRC']['units_in_scope']
words={1:'one',2:'two',3:'three',5:'five',7:'seven',8:'eight',9:'nine',10:'ten'}
for n,w in words.items():
 title=next(u['heading'] for u in old if u['unit'].split(' ')[1]==str(n) if u['unit'].startswith('Title '))
 family(x,'Title '+str(n),title,'https://courts.ca.gov/cms/rules/index/'+w,'Retain complete title at J1 for civil, protective-order, representative-authority and court access dependencies; title-wide inclusion does not make independent family/juvenile litigation an operating workflow.')
family(x,'Standards','Standards of Judicial Administration','https://courts.ca.gov/cms/rules/index/standards','Court access, case management, ADR and appointment standards.')
for n in range(1,18):doc(x,'Ethics'+str(n),'Neutral arbitrator ethics standard '+str(n),'https://courts.ca.gov/cms/rules/index/ethics/ethics'+str(n))
x['currentness_note']='Official new/amended index recovered in capture8: latest listed adoption June17,2026 effectiveAugust1; April24 July1 and October24,2025 July1,2026 changes are operative. Index title headers saying July2025 are not a version guarantee: individual1.31/3.670/5.7 histories show2026 changes. October16,2026 committee recommendations are proposals as ofOctober1.'
x=base('CA:JUDICIAL-COUNCIL-FORMS','Judicial Council civil and authority-related forms');x['toc_source_url']='https://selfhelp.courts.ca.gov/find-forms/all'
for name in ['APP appellate','AT attachment','CIV civil','CM case management','DISC discovery','EJ enforcement','FW fee waivers','MC miscellaneous civil','PLD pleadings','POS service','SC small claims','SUBP subpoenas','UD unlawful detainer','ADR alternative dispute resolution','CH civil harassment','DV domestic violence','EA elder abuse','WV workplace violence','TH transitional housing misconduct','DE decedents estates','GC guardianship/conservatorship','FL family property/authority and protective orders']:
 family(x,name,name+' forms',x['toc_source_url'],'Complete named form family selected including instructions, optional forms and mandatory alternatives. Follow numbered form record to current official PDF; revision/effective dates must be preserved. Forms are not all automatically mandatory.')
excluded(x,'ADOPT/SUR parentage/adoption-only;CR criminal;TR traffic;JV juvenile-only;child-support-only forms','Independent family/criminal/juvenile case work outside operating aperture; orders establishing authority, protection and property control retained through selected families/rules.')
(OUT/'proposed_instruments.json').write_text(json.dumps({'as_of':'2026-10-01','instruments':list(proposals.values())},indent=2)+'\n')
print('Wrote',len(proposals),'court instruments')
