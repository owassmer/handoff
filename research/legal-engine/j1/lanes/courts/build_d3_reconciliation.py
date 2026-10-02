import json
from pathlib import Path
P=Path(__file__).parent
base=json.loads((P/'proposed_instruments.recovered.json').read_text())
i=next(x for x in base['instruments'] if x['id']=='CA:4DCA')
u=i['units_in_scope'][0]
u['section_list'][0]['ref']='https://appellate.courts.ca.gov/system/files/2025-10/4dca-local-rules%202025.pdf'
u['currentness_note']='Official current local-rules HTML and indexed October 2025 PDF identify Rule 5 repeal October 24, 2025. PDF identity resolved; direct retrieval returned tool error, HTML capture supplies current enumeration.'
for num,title,file in [
 ('4D-additional-efiling','Additional electronic filing guidelines for Fourth Appellate District','4DCA-eFiling-additional-eFiling-guidelines.pdf'),
 ('DCASC-bookmarks','Formatting guidelines: bookmarks and pagination','DCASC-Bookmarks-and-Pagination.pdf'),
 ('DCASC-bookmark-zoom','PDF bookmark zoom settings','DCASC-Adobe-PDF-Bookmark-Zoom-Settings.pdf'),
 ('DCASC-briefs','Formatting guidelines for briefs','DCASC-Formatting-Guidelines-Briefs.pdf'),
 ('DCASC-sample-brief','Sample appellant opening brief','DCASC-Sample-AOB.pdf'),
 ('DCASC-petitions','Formatting guidelines for petitions','DCASC-Formatting-Guidelines-Petitions.pdf'),
 ('DCASC-sample-writ','Sample writ petition','DCASC-Sample-Writ-Petition.pdf'),
 ('DCASC-sample-transfer','Sample petition for transfer','DCASC-Sample-Petition-for-transfer.pdf'),
 ('DCASC-appendix','Formatting guidelines for appendix','DCASC-Formatting-Guidelines-Appendix.pdf'),
 ('DCASC-sample-appendix','Sample appendix','DCASC-Sample-Appendix.pdf'),
 ('DCASC-sample-exhibits','Sample writ exhibits','DCASC-Sample-Writ-Exhibits.pdf'),
 ('DCASC-exhibits','Formatting guidelines for exhibits to petition','DCASC-Formatting-Guidelines-Exhibits.pdf')]:
 ref='https://www.courts.ca.gov/documents/'+file
 if num=='DCASC-exhibits': ref='https://appellate.courts.ca.gov/system/files/2026-04/'+file
 if num in ('DCASC-briefs','DCASC-petitions'): ref='https://appellate.courts.ca.gov/sites/default/files/appellate/default/2023-09/'+file.lower()
 i['units_in_scope'].append({'unit':num,'heading':title,'toc_url':ref,'reason':'Court-issued formatting/submission guide or template expressly named on current Fourth District electronic-filing page; preserves filing acceptance and access dependencies.','source_unit_kind':'document','section_list':[{'number':num,'heading':title,'ref':ref}],'currentness_note':'Legacy official link recovered from e-filing provider mirror and corroborated by current official list. Some direct fetches fail redirect/throttle; this is a named acquisition target, not a claim full text was saved or every PDF edition verified.'})
for num,title,ref,reason in [
 ('D3-Misc-2025-01','D3 Miscellaneous Order 2025-01, effective March 3, 2025','https://appellate.courts.ca.gov/system/files/local-rules/misc-order-2025-01.pdf','Recovered official indexed text confines email service protocol to OCPD writ petitions served on OCDA; criminal counsel-specific litigation, not general residential civil service. Rule 1 itself remains selected.'),
 ('D3-Misc-2025-02','D3 Miscellaneous Order 2025-02, acting presiding justice','https://appellate.courts.ca.gov/system/files/local-rules/misc-order-2025-02.pdf','Temporary court administration designation from July 31, 2025 until new confirmation. May 22, 2026 official announcement and current roster identify Motoike as presiding justice. Does not establish a current civil filing requirement.'),
 ('4D-Misc-011314','Exception to Rule 8.47(c)(1), January 13, 2014','https://appellate.courts.ca.gov/sites/default/files/appellate/default/2023-09/4dca-011314-exception-to-rule-8-47-c-1.pdf','Official indexed text concerns probation report material in criminal appellate records; outside residential civil aperture.'),
 ('D3-historical-local-forms','Historical D3 notice of settlement and stipulated dismissal forms','https://appellate.courts.ca.gov/district-courts/4dca/rules-forms-filing/forms','Current official Division 3 forms page expressly states no local forms are in use. Older publication-library forms and 2013/2015 guide attachments are not adopted current forms merely because PDFs remain indexed; statewide APP forms remain selected.')]:i['units_out'].append({'unit':num,'heading':title,'source_url':ref,'reason':reason})
i['source_review']='j1/lanes/courts/D3_RECONCILIATION.md'
i['currentness_note']='Current local rules and March 24, 2026 D3 IOPP selected with operative practice, filing, fee and argument pages. Named miscellaneous orders 2025-01/2025-02/011314 individually reviewed and excluded for recorded reasons. Current D3 forms page expressly reports no local forms in use. 2014-1 official rescission summary remains selected over old guide; signed artifact and division caption remain J2 verification. CRC1.6(9),10.1030 and8.72 support the generally applicable published-practice source boundary. Clerk-request availability does not itself identify another applicable civil source; archive is mixed, not asserted internal-only. Twelve named formatting PDFs now have exact targets, including Exhibits.'
for unit in i['units_in_scope']:
 if unit['unit']=='DCASC-exhibits': unit['currentness_note']='Exact migrated official PDF recovered from indexed official text, revised August 2023; direct open failed. URL folder date is not inferred as amendment date. J2 must obtain document and verify edition.'
(P/'d3_reconciled_instrument.json').write_text(json.dumps({'as_of':'2026-10-01','instruments':[i]},indent=2)+'\n')
print(len(i['units_in_scope']),len(i['units_out']))
