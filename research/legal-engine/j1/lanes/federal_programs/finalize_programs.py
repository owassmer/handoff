"""Additional lane proposals, executed by build_proposals with its document helpers."""
calhome_reason='Conditional shared-housing tenancies, ADU/JADU rehabilitation and manufactured housing on rented spaces; use the applicable award vintage and amendment terms, not a blanket ownership-program exclusion.'
x=document_set('CA','HCD-CALHOME','HCD CalHome operating and rehabilitation guidelines',[
 ('CALHOME-2004','CalHome approved regulatory text (2004)','https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/calhome/calhome-regs-approved-text.pdf',calhome_reason),
 ('CALHOME-2019','CalHome Final Guidelines (2019)','https://www.hcd.ca.gov/grants-funding/active-no-funding/calhome/docs/calhome-final-guidelines.pdf',calhome_reason),
 ('CALHOME-2022','CalHome Final Guidelines, December 30, 2022','https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/CalHome-Final-Guidelines-2022.pdf',calhome_reason),
 ('CALHOME-2024-AMENDED-2025','CalHome 2024 Program Guidelines, amended October 2, 2025','https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/hosn/2024-amended-calhome-guidelines.pdf',calhome_reason),
 ('HCD-AN24-02','HCD Administrative Notice 24-02, May 30, 2024: Homeownership program guideline amendments','https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/hosn-omnibus-amendments-admin-memo.pdf','Amends specified CalHome/Serna requirements across active contracts; apply its express affected editions and provisions.')],work+['housing_assistance','landlord_tenant'])
x['source_capture']='j1/lanes/federal_programs/home-calhome-documents.txt'
x['edition_note']='Current resources link has stale 2022 metadata but actual CalHome cover states 2024 guidelines amended October 2, 2025. Historical editions remain conditional on the award and later amendments.'
x=document_set('CA','HCD-HOME','HCD state-administered HOME award conditions',[
 ('HOME-2022-23','HOME 2022-2023 NOFA','https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/home/home-2022-2023-nofa.pdf','Prior award-vintage tenancy, affordability and rehabilitation conditions survive funding closure.'),
 ('HOME-2024-AMENDED','HOME 2024 NOFA, second amended edition','https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/home/home-2024-nofa.pdf','Program activity rental assistance and rehabilitation terms where state HOME award applies.'),
 ('HOME-2025-PROJECTS','HOME 2025 Project Activities NOFA','https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/home/home-2025-projects-nofa.pdf','Covered rental acquisition/rehabilitation project operating and affordability conditions.'),
 ('HOME-2025-OVERLAYS','HOME 2025 Appendix A: Federal and State Overlays','https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/home/appendix-a-federal-and-state-overlays.pdf','Identifies applicable work, displacement, accessibility and assistance dependencies.'),
 ('HOME-2025-JURISDICTIONS','HOME 2025 Appendix B: Eligible State HOME Jurisdictions','https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/home/appendix-b-eligible-jurisdictions.pdf','Territorial eligibility limits state HOME awards; federal HOME recipient status and tribal-land exceptions must be checked.')],work+['housing_assistance','rent_regulation','early_termination'])
x['source_capture']='j1/lanes/federal_programs/home-calhome-documents.txt'
x['recovery_limit']='Current contract-management-manual page says it is being updated and supplies no manual file. A manual was not recovered; directory is not treated as an instrument. 2026 draft program guidelines remain a proposal, not adopted authority. State HOME territorial eligibility is narrower than federal HOME applicability.'
# Replace the original portfolio placeholders rather than leave duplicate browse roots.
for old,new in [('CA:HCD-PROGRAM-INSTRUMENTS','CA:HCD-PORTFOLIO'),('CA:CALHFA-ASSET-INSTRUMENTS','CA:CALHFA-ASSET')]:
 x=proposals.pop(old);x['id']=new;proposals[new]=x

# Apply the acquisition lane's legacy XML grouping after substantive scope edits.
import importlib.util
spec=importlib.util.spec_from_file_location('lane_uslm',HERE.parent/'acquisition/propose_uslm.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
merged={**current,**proposals}
for route in module.propose(list(merged.values())):
 if 'units' not in route:continue
 x=copy.deepcopy(merged[route['instrument']]);x['adapter']='usc';x['acquisition']['text_adapter']='usc'
 routes={u['unit']:u for u in route['units']}
 for u in x['units_in_scope']:u.update(routes[u['unit']])
 x['version_note']=route['source_status'];put(x)
for ident,old in current.items():
 if ident in proposals or not old.get('units_in_scope') or 'USC' not in ident:continue
 m=re.match(r'US:(\d+)USC',ident)
 if not m:continue
 title=int(m.group(1));x=copy.deepcopy(old)
 url=f'https://uscode.house.gov/download/releasepoints/us/pl/119/111/xml_usc{title:02d}@119-111.zip'
 usable=True
 for u in x['units_in_scope']:
  label=u['unit'];chapter=re.search(r'Chapter (\d+[A-Z]?)',label);part=re.fullmatch(r'Part ([IVX]+)',label);section=re.search(r'USC (\d+[A-Z]?)',label)
  if ident=='US:12USC5220note':selector='/us/usc/t12/s5220';u['reason']='Preserve the complete enclosing section with statutory notes to acquire PTFA; base-section mortgage-program provisions do not become an independent selected operating rule.'
  elif ident=='US:15USC9058':selector='/us/usc/t15/s9058'
  elif ident=='US:15USC-FTC':selector='/us/usc/t15/ch2/schI'
  elif chapter:selector=f'/us/usc/t{title}/ch{chapter.group(1)}'
  elif part:selector=f'/us/usc/t{title}/pt{part.group(1)}'
  elif section:selector=f'/us/usc/t{title}/s{section.group(1)}'
  else:usable=False;break
  u['toc_url']=url;u['uslm_identifier']=selector
 if usable:
  x['adapter']='usc';x['acquisition']['text_adapter']='usc';x['toc_source_url']=url
  x['version_note']='Uses shared register asserted119-111 release pointer; publisher maintenance prevented independent release verification in this pass.'
  put(x)
additional=json.loads((HERE/'additional_program_manifest.json').read_text())
items=[]
for d in additional:
 url=d['url'];file=unquote(url.split('/')[-1])
 if 'Round_' in file:
  n=re.search(r'Round_(\d+)',file).group(1);label=f'AHSC Round {n} Guidelines, amended December 17, 2024'
 elif '06a_Attachment' in file:label='AHSC Round 9 Guidelines, amended February 25, 2026'
 elif '06b_Attachment' in file:label='AHSC Round 10 Guidelines, adopted February 25, 2026'
 elif d['parent']=='turn1609view2':label={22:'MHP Round 2 Guidelines (2023)',24:'FWHG Round 2 Guidelines (2023)',25:'VHHP Round 2 Guidelines (2023)',38:'MHP Round 1 Guidelines (2022), amended May 5, 2022',40:'FWHG Round 1 Guidelines (2022)',41:'VHHP Round 1 Guidelines (2022)'}[d['link']]
 elif d['parent']=='turn1609view0':label={4:'Homekey Round 3 NOFA, amended edition',5:'Homekey 2023 NOFA Amendment',7:'Homekey Round 3 Exhibit A: Authority, Purpose and Scope',9:'Homekey Round 3 Exhibit D: General Terms',10:'Homekey Round 3 Exhibit E: Interim Housing',11:'Homekey Round 3 Exhibit E: Permanent Housing'}[d['link']]
 else:label={2:'Homekey Round 2 NOFA, amended December 11, 2024',40:'Homekey Round 1 Amended NOFA'}[d['link']]
 reason='Award-vintage housing management, rent, affordability, repair, service and property-use conditions continue after initial funding; apply the agreement and amendment applicability clauses.'
 items.append((re.sub(r'[^A-Za-z0-9_.-]+','-',file),label,url,reason))
items.append(('HOMEKEYPLUS-2026-03-27','Homekey+ NOFA, amended March 27, 2026','https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/homekey/hk-plus-amendment.pdf','Supportive-housing rehabilitation and continuing tenancy/property conditions; preserve program-specific exceptions to incorporated UMR and other guidelines.'))
x=document_set('CA','HCD-AWARD-VINTAGE-GUIDELINES','HCD and SGC housing program award-vintage guidelines',items,work+['housing_assistance','rent_regulation','early_termination'])
x['recovery_limit']='SGC current archive supplies AHSC Rounds 3-10 and directs readers to contact the agency for Rounds 1-2; no Round 1-2 text was recovered from that route. No email contact was made.'
items=[]
for letter in ['a','b']:
 items.append((f'TAY-2025-26-Exhibit-{letter.upper()}',f'HCD FY2025-26 THP Round 7 / HNMP Round 4 / THPSUP Round 5 Exhibit {letter.upper()}, approved July 14, 2025',f'https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/tay/2025-2026-round-7-thp-round-4-hnmp-round-5-thpsup-standard-agreement-exhibit-{letter}-template.pdf','Template supplies program conditions affecting housing/service eligibility, tenancy, provider costs and payment; actual applicability depends on executed agreement.'))
x=document_set('CA','HCD-TAY-2025-26','HCD transitional-age-youth housing and navigation standard agreement exhibits',items,work+['housing_assistance','early_termination'])
x['applicability_note']='OC award list and Resolution25-098 establish participation; these blank templates are not Orange County executed STD213. Preserve Exhibit A inconsistent maintenance-of-effort baseline years for later adjudication.'
x['source_capture']='j1/lanes/local_agency/oc_enactments/hcd-tay-evidence.txt'

nspire=[
 ('2023-09693','NSPIRE Final Rule FR-6086-F-03','2023-05-11','Final standards framework and program applicability.'),
 ('2023-13293','NSPIRE Inspection Standards FR-6086-N-05','2023-06-22','Actual inspectable items, defect classifications and correction conditions.'),
 ('2023-14362','NSPIRE Scoring Notice FR-6086-N-06','2023-07-07','Scoring and defect treatment for covered inspections.'),
 ('2025-01116','NSPIRE Scoring Notice Correction','2025-01-17','Corrects the scoring notice.'),
 ('2023-20130','NSPIRE CPD initial extension FR-6086-N-07','2023-09-18','Historical CPD transition.'),
 ('2023-21141','NSPIRE voucher initial extension FR-6086-N-08','2023-09-28','Historical voucher transition.'),
 ('2024-14718','NSPIRE voucher and CPD extension FR-6086-N-09','2024-07-05','Historical extension subsequently amended by program-specific notices.'),
 ('2025-18988','NSPIRE CPD extension FR-6086-N-11','2025-09-30','CPD compliance to October 1, 2026, subject to later HOME/HTF-specific action.'),
 ('2025-19070','NSPIRE voucher extension FR-6086-N-12','2025-09-30','Specified voucher provisions extended to February 1, 2027; statutory alarm mandates remain distinct.'),
 ('2026-07176','NSPIRE HOME/HTF Implementation Guidance and Inspection Standards','2026-04-14','HOME/HTF compliance April 14, 2027; program-specific standards and prior-written-agreement treatment.')]
items=[(num,title,f'https://www.govinfo.gov/content/pkg/FR-{date}/pdf/{num}.pdf',reason) for num,title,date,reason in nspire]
items.extend([
 ('PIH-2023-16','NSPIRE Administrative Procedures','https://www.hud.gov/sites/dfiles/OCHCO/documents/2023-16pihn.pdf','Correction evidence, review and inspection administration.'),
 ('PIH-2025-27','NSPIRE Affirmative Requirements Scoring Extension','https://www.hud.gov/sites/dfiles/OCHCO/documents/PIH-2025-27.pdf','Public/multifamily scoring October 1, 2026.'),
 ('PIH-2026-18','NSPIRE Voucher Administrative Procedures','https://www.hud.gov/sites/default/files/PIH/documents/PIH-2026-18.pdf','Supersedes PIH2023-28 and2024-26; identifies delayed versus unaffected requirements.')])
x=document_set('US','HUD-NSPIRE','HUD NSPIRE standards and program-specific implementation instruments',items,['housing_assistance','work_standards','landlord_tenant','payments'])
x['temporal_note']='Public/MFH affirmative scoring October 1, 2026; CPD generally October 1, 2026 under N11; HOME/HTF April 14, 2027 under2026-07176 with agreement-date distinctions; vouchers specified provisions February 1, 2027. Actual early adoption remains separate, including OCHA October 1, 2025.'
x=proposals['US:HUD-HOTMA']
for num,title,url,reason in [('2025-23989','HOTMA CPD Compliance Extension to January 1, 2027','https://www.govinfo.gov/content/pkg/FR-2025-12-30/pdf/2025-23989.pdf','CPD-specific timing and voluntary earlier implementation, distinct from PIH and multifamily notices.'),('PIH-2024-19','HOTMA Voucher Final Rule Implementation','https://www.hud.gov/sites/dfiles/OCHCO/documents/2024-19pihn.pdf','Voucher implementation requirements are separate from income/assets rule implementation.')]:
 x['units_in_scope'].append({'unit':title,'heading':title,'toc_url':url,'reason':reason,'source_unit_kind':'document','section_list':[{'number':num,'heading':title,'ref':url,'source_unit_kind':'document'}]})
x['temporal_note']+=' CPD:2025-23989 January1 2027, with optional earlier implementation; voucher HOTMA amendments have separate PIH2024-19 requirements.'
document_set('US','USDA-30DAY-2026','USDA 2026 nonpayment notice regulation rescission',[
 ('2026-03716','RHS rescission of 30-day nonpayment notice regulation','https://www.govinfo.gov/content/pkg/FR-2026-02-25/pdf/2026-03716.pdf','RHS Section514/515 regulatory rescission is separate from HUD delayed action and does not itself repeal statutory CARES Act protections.')],['housing_assistance','early_termination','landlord_tenant'])

for x in proposals.values():
 if x.get('adapter')=='usc':
  x['version_note']='OLRC publisher download and currency search snapshots identify release 119-111, September 18, 2026 (remaining_currency.txt and targeted_recovery.txt). Direct publisher pages return maintenance/timeouts and ZIP retrieval failed; this verifies the publisher release assertion, not XML bytes or every selector.'
  x['release_evidence']='j1/lanes/federal_programs/remaining_currency.txt'
 if re.match(r'US:(16|28|47)CFR',x['id']):
  x['currency_evidence']='j1/lanes/federal_programs/currency_direct.txt; j1/lanes/federal_programs/api_currency.txt'
x=proposals['US:HUD4350.3']
x['retrieval_note']='Official complete-file target repeatedly times out, but current publisher directory and recovered November 27, 2013 revised transmittal establish REV-1 Change 4. Official Chapter 6 PDF recovered as an alternate component route. Full handbook content retrieval remains pending; no substituted third-party edition.'
x['alternate_component_targets']=[{'number':'4350.3-REV1-CHG4-TRANSMITTAL','heading':'Revised transmittal, November 27, 2013','ref':'https://www.hud.gov/sites/documents/43503rev-trn4hsgh.pdf'},{'number':'4350.3-CH6','heading':'Chapter 6: Lease Requirements and Leasing Activities','ref':'https://www.hud.gov/sites/documents/43503c6hsgh.pdf'}]
x['source_capture']='j1/lanes/federal_programs/recovery_alternatives.txt'

# Source-grounded headings avoid assuming USLM subtitle abbreviation conventions.
for ident,heading in [('US:40USC37','CONTRACT WORK HOURS AND SAFETY STANDARDS'),('US:41USC67','SERVICE CONTRACT LABOR STANDARDS')]:
 for u in proposals[ident]['units_in_scope']:
  u.pop('uslm_identifier',None);u['uslm_parent_heading']=heading
  u['selector_evidence']='Official OLRC chapter headings confirmed in preliminary title40 chapter37 and title41 subtitleII chapter67 publisher search results on October 1, 2026; XML hierarchy is selected by named heading, not an inferred subtitle identifier.'
x=proposals['CA:HCD-AWARD-VINTAGE-GUIDELINES']
for num,title,url in [
 ('AHSC-R1-2015-AMENDED-2018','AHSC Round 1 Guidelines, adopted January 20, 2015; technical amendments October 11, 2016 and September 25, 2018','https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/ahsc-round-1-fy1415-guidelines-ammendment-LOCKED-2022-09-21-remediated-final.pdf'),
 ('AHSC-R2-2015','AHSC Round 2 Guidelines, adopted December 17, 2015, with quantification appendix','https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/adopted-final-15-16-ahsc-guidelines-with-qm-LOCKED-2022-09-21-remediated-final.pdf')]:
 x['units_in_scope'].append({'unit':title,'heading':title,'toc_url':url,'reason':'Prior award-vintage affordability, housing work, legal agreement and prevailing-wage conditions; apply subsequent express amendments without substituting later-round guidelines.','source_unit_kind':'document','source_capture':'j1/lanes/federal_programs/ahsc12_covers.txt','section_list':[{'number':num,'heading':title,'ref':url,'source_unit_kind':'document'}]})
x.pop('recovery_limit',None)
x['edition_note']='Rounds 1-2 recovered from HCD preserved primary PDFs despite SGC archive directing agency contact. Filename 2022 remediation date is not adoption. Rounds 3-8 retain December 17, 2024 amendments; rounds 9-10 retain February 25, 2026 editions. Each award and express amendment controls applicability.'
x=proposals['CA:HCD-HOME']
for u in x['units_in_scope']:
 if u['section_list'][0]['number']=='HOME-2024-AMENDED':
  label='HOME 2024 NOFA, second amendment January 21, 2026';u['unit']=u['heading']=u['section_list'][0]['heading']=label
for num,title,url in [
 ('HOME-2017-18','HOME 2017-2018 NOFA, June 5, 2018','https://www.hcd.ca.gov/grants-funding/nofas/docs/HOME_NOFA_2018.pdf'),
 ('HOME-2017-18-AMEND1','HOME 2017-2018 NOFA Amendment 1','https://www.hcd.ca.gov/grants-funding/docs/HOME_nofamend1.pdf'),
 ('HOME-2020-21-RESTATED','HOME 2020-2021 NOFA, amended and restated February 24, 2022','https://www.hcd.ca.gov/grants-funding/active-funding/home/docs/Amended-and-Restated-HOME-2020-2021-NOFA-2-24-2022.pdf'),
 ('HOME-2019','HOME 2019 NOFA, October 31, 2019','https://www.hcd.ca.gov/grants-funding/active-funding/docs/2019_HOME_NOFA_signed.pdf')]:
 x['units_in_scope'].append({'unit':title,'heading':title,'toc_url':url,'reason':'Prior award-vintage rental-project affordability, rehabilitation and continuing agreement conditions; funding closure does not itself terminate operating restrictions.','source_unit_kind':'document','source_capture':'j1/lanes/federal_programs/home_prior_awards.txt','section_list':[{'number':num,'heading':title,'ref':url,'source_unit_kind':'document'}]})
x['edition_note']='Current published HOME project/program NOFAs and archive editions are selected by award vintage. The 2017-2018 Amendment 1 identity and direct URL are recovered from the publisher search snapshot in home_manual_closure.txt; its full text remains J2 fetch-pending. The 2026 draft guidelines do not supersede these adopted sources.'
for u in x['units_in_scope']:
 if u['section_list'][0]['number']=='HOME-2017-18-AMEND1':u['source_capture']='j1/lanes/federal_programs/home_manual_closure.txt'
for ident in ['US:40USC37','US:41USC67']:
 proposals[ident]['selector_evidence']='j1/lanes/federal_programs/nested_chapter_heading_snapshots.txt'
