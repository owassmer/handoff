import json,re
from pathlib import Path
from urllib.parse import quote
P=Path(__file__).parent
rows=json.loads((P/'cacd_inventory_rows.json').read_text())
excluded={'G-096':'Bar association educational-event transportation funding; actual PDF is internal/event administration.','ADR-019':'Mediator recruitment; not party procedure.','ADR-023':'Panel mediator vendor expense authorization.','ADR-024':'Panel mediator vendor reimbursement.','CV-010':'Admiralty in-rem arrest outside residential work/accounts.','CV-046':'Admiralty judicial sale writ outside aperture.','CV-011B':'Habeas consent.','CV-027':'Habeas petition.','CV-027A':'Immigration custody habeas.','CV-060P':'Prisoner fee waiver.','CV-066A':'Prisoner civil-rights instructions.','CV-066B':'Prisoner pilot instructions.','CV-067':'Criminal sentence collateral attack.','CV-069':'State custody habeas.','CV-138':'Death sentence execution notice.','G-004':'Criminal arrest warrant.','G-005':'Media workroom administration.','G-030':'Federal agency records request; public request selected separately.','G-058':'Court-facility use agreement; not litigation procedure.','G-127':'Lawyer representative travel administration.','G-128':'Lawyer representative travel reimbursement.','G-129':'Conference representative recruitment.'}
selected=[];out=[];aliases=[]
for n,title,raw,date in rows:
 date=re.match(r'\d\d/\d{4}',date).group() if re.match(r'\d\d/\d{4}',date) else ''
 filename=re.sub(r'^Image: \S+\s+','',raw).strip()
 if n in {'AO-0078','AO-0078B','AO-0110','AO-0196A','AO-0336','AO-0443','AO-0455'}:
  out.append({'unit':n,'heading':title,'reason':'Personnel, court-vendor or criminal procedure outside residential civil aperture.'});continue
 if n.startswith('AO-') and n!='AO-0436':
  aliases.append({'number':n,'heading':title,'reason':'National forms register owns civil AO document; obsolete AO-0133 is replaced by selected CV-059. Local summons example is explanatory, not an independent operative form.','observed_file_label':filename});continue
 reason=excluded.get(n)
 if n.startswith('Pro Se Packet') and n!='Pro Se Packet 5':reason='Criminal, prisoner or immigration custody packet outside aperture.'
 if n.startswith('G-009'):reason='Custody transport/habeas witness process outside ordinary residential civil litigation.'
 if 'replaced by' in title:aliases.append({'number':n,'heading':title,'reason':'Publisher expressly replaces local form with stated national/Judicial Council form.'});continue
 if n.endswith(('wpd','docx')):reason='Alternate editable version of selected PDF legal form; PDF governs acquisition of same form content.'
 if reason:out.append({'unit':n,'heading':title,'reason':reason});continue
 if not filename.lower().endswith(('.pdf','.docx')):raise ValueError((n,filename))
 selected.append({'number':n,'heading':title,'ref':'https://apps.cacd.uscourts.gov/cm-api/dwwwroot/'+quote(filename),'publisher_filename':filename,'publisher_revision':date,'source_unit_kind':'document','acquisition_identity_status':'publisher filename joined to observed official public store; per-target verification recorded separately'})
for row in selected:
 if row['number']=='G-101 ORDER': row['ref']='https://www.cacd.uscourts.gov/sites/default/files/forms/G-101/G-101%20ORDER.pdf'
 if row['number']=='AO-0436': row['ref']='https://www.cacd.uscourts.gov/sites/default/files/forms/AO-436/AO-436.pdf'
 row['acquisition_identity_status']='direct official PDF verified' if row['number'] not in {'G-002','CV-059'} else 'publisher filename mapped to verified public file store; binary response unverified'
 if row['number']=='CV-066': row['scope_note']='General section1983/Bivens pleading template; prisoner-oriented questions do not make every use prisoner-only. Conditional public-enforcement/civil-rights dependency; no prisoner instructions or packets selected.'
i={'id':'CA:CACD-FORMS','name':'Central District of California civil, general, appeal and ADR forms','level':'court rule','instrument_kind':'court forms','source_url':'https://apps.cacd.uscourts.gov/cm-api/form/','adapter':'generic','source_unit_kind':'document','units_in_scope':[{'unit':'Forms','heading':'Applicable published local forms','toc_url':'https://apps.cacd.uscourts.gov/cm-api/form/','source_unit_kind':'document','reason':'Federal civil filing, attachment, enforcement, counsel, access, appeal and dispute-resolution dependencies for residential physical work and outgoing accounts.','section_list':selected}],'units_out':out,'cross_register_dependencies':aliases,'source_review':'j1/lanes/courts/CACD_FORMS_ACQUISITION.md'}
(P/'cacd_forms_addition.json').write_text(json.dumps({'instruments':[i]},indent=2)+'\n')
print(len(selected),'selected',len(out),'excluded',len(aliases),'cross-register')
