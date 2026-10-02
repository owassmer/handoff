"""Build bounded OAL quarterly source-screen ledger from saved web observations."""
import json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
rows=json.loads((HERE/'quarter-rows.json').read_text())
select={
'2025-1121-04SR':('CA:CCR16','Provider qualification and application continuity for architectural repair/design work.'),
'2026-0212-07S':('CA:CCR16','Retired architect reinstatement affects who can perform authorized design work.'),
'2026-0601-06S':('CA:CCR16','Architect application review affects provider qualification.'),
'2026-0601-04S':('CA:CCR16','Structural pest provider examinations and license qualification.'),
'2026-0217-01S':('CA:CCR16','Engineering/geology licensing fees affect qualified repair providers.'),
'2026-0213-03S':('CA:CCR10','Appraisal-review standards for property valuation/recovery evidence.'),
'2026-0520-04S':('CA:CCR10','Real-estate appraiser qualification standards.'),
'2026-0402-01S':('CA:CCR3','Pesticide application and groundwater restrictions during landscaping/pest work.'),
'2026-0410-03S':('CA:CCR3','Pesticide worker protection during residential pest/landscape work.'),
'2026-0330-01S':('CA:CCR14','Waste compliance hearing rules, including SB1383 enforcement, affect work and contested charges.'),
'2026-0506-01S':('CA:CCR22','Retain candidate-chemical framework dependency for materials/cleaning products; listing alone is not a product prohibition.'),
'2026-0521-05S':('CA:CCR22','Retain candidate-chemical framework dependency; do not infer product prohibition.'),
'2026-0417-04S':('CA:CCR22','Safer-consumer-product regulatory response framework can govern selected work products.'),
'2026-0202-01SR':('CA:CCR2','Housing discrimination conciliation procedures.'),
'2026-0127-01SR':('CA:CCR13','DMV record request rules support lawful abandoned-vehicle identification and resolution.'),
'2026-0112-02N':('CA:CCR13','Conditional work-provider vehicle safety and transport standards.'),
'2026-0126-02S':('CA:CCR1','General rulemaking filing procedure supports authoritative regulatory provenance; OAL title4 label appears erroneous.'),
'2026-0202-02S':('CA:CCR22','Conditional employer payroll/voluntary disability plan reporting for directly employed work crews.'),
'2025-1126-04S':('CA:CCR2','Retain compensation application/procedure changes because crime-related relocation/property reimbursement can affect account resolution; distinguish clinical-only units.'),
'2026-0410-02SR':('CA:CCR3','Conditional landscape plant movement and pest eradication controls.'),
'2026-0410-04S':('CA:CCR3','Conditional landscape plant import/movement controls.'),
'2026-0729-01SR':('CA:CCR3','Conditional tree/plant disease treatment and movement controls.'),
'2026-0803-02S':('CA:CCR3','Conditional landscape eradication-area rules; geographic application remains a fact.'),
'2026-0804-02S':('CA:CCR3','Conditional palm landscape disease/movement controls.'),
'2025-1212-02S':('CA:CCR10','Conditional payment-provider licensing; retained division dependency, not landlord money-transmitter status.'),
'2026-0717-01':('CA:CCR10','Conditional entity/securities filings within retained DFPI division; verify applicability before imposing duties.'),
'2026-0316-04EE':('CA:CCR13/CCR17','Conditional work vehicles/equipment; emergency history and titles require agency reconciliation before operative version assertion.'),
}
exclude={
'2026-0730-01S':'Final text confines this package to healthcare/mental-health provider payments and treatment benefits; does not amend relocation or residential account benefits.',
'2026-0807-01S':'Pink bollworm cotton quarantine repeal governs agricultural crop material, not residential landscape work in current scope.',
'2025-1202-01SR':'Seed-container commercial labeling, rather than use of landscaping seed by operator; retain plant quarantine rules separately.',
'2026-0721-01SR':'Animal blood-bank penalty administration, separate veterinary industry.',
'2026-0526-01E':'Metal-shredding facility fee, not waste-generator duties for residential repairs; retain waste disposal/generator rules separately.',
'2025-1031-02S':'Nail-product MMA priority-product designation; cosmetology product activity outside physical residential work.',
'2026-0417-03S':'Nail-product TPhP designation; distinct from generally applicable chemicals framework.',
'2026-0707-02S':'Energy supplier gas-data reporting, not building energy benchmarking or residential service account rule.',
'2026-0720-01S':'Publicly owned utility capacity payment administration, not customer billing/service rule.',
'2026-0701-01':'Skilled nursing facility financial reporting due date; clinical-institution accounting outside residential physical work.',
'2026-0508-02':'Adoption/resource-family approval procedures; no physical housing work or outgoing-account rule identified.',
'2026-0629-03S':'Oil-transfer operations/inspection for marine facilities and vessels; separate industrial operation.',
'2026-0102-01':'State fire-service training certification updates, not building fire standards or repair-provider qualification.',
'2026-0224-02SR':'Volunteer/employee criminal history exchange for care-service roles, not general dwelling work-provider selection.',
'2025-1024-04S':'Child Abuse Central Index reporting/review, separate child-protection administration.',
'2026-0310-02SR':'CalWORKs home-visiting service program; does not govern dwelling repair or departing-account disposition.',
'2026-0220-01S':'CalWORKs income/eligibility reporting; no specific housing-work/account dependency established.',
'2026-0403-01SR':'Interstate vehicle-sale taxation; does not determine residential work or outgoing account amounts.',
}
agency_exclusions={
'Commission on Peace Officer Standards and Training':'Police training and employment administration.',
'California Gambling Control Commission':'Gaming license/fee administration.',
'Commission on Teacher Credentialing':'Teacher qualification administration.',
'Department of Managed Health Care':'Health-plan provider-directory administration.',
'Board of Behavioral Sciences':'Clinical mental-health professional licensing/advertising.',
'Board of Pharmacy':'Pharmacy clinical dispensing practice.',
'Acupuncture Board':'Acupuncture clinical practice/licensing.',
'Veterinary Medical Board':'Veterinary drug practice.',
'New Motor Vehicle Board':'Motor-vehicle dealership/franchise board fees.',
'Bureau for Private Postsecondary Education':'Educational institution authorization/enforcement.',
'Board of Registered Nursing':'Nursing educational program approvals.',
'Bureau of Automotive Repair':'Vehicle emissions inspection equipment administration.',
'State Teachers Retirement System':'Public teacher pension administration.',
'Department of Cannabis Control':'Licensed commercial cannabis cultivation/testing, separate commercial industry.',
'San Francisco Bay Conservation and Development Commission':'San Francisco Bay geographic jurisdiction outside CA-OC/HB.',
'Board of Chiropractic Examiners':'Clinical chiropractic licensing administration.',
'Board of Barbering and Cosmetology':'Cosmetology professional discipline.',
'Public Employees Retirement System':'Public employee pension risk-pool administration.',
'Public Employment Relations Board':'Public employment bargaining/case administration, outside private residential work employment.',
'Board of Pilot Commissioners':'Maritime pilot rate proceedings.',
'State Lands Commission':'Marine invasive-species vessel enforcement, not residential shore property permitting.',
'Emergency Medical Services Authority':'Clinical emergency medical practice/program standards.',
'Board of Parole Hearings':'Criminal sentence review.',
'Department of Public Health':'Commercial cannery processing rules in this specific row; lead/housing health rules retained elsewhere.',
'California Correctional Training and Rehabilitation Board':'Correctional employee conduct.',
'ScholarShare Investment Board':'Education savings incentive program.',
}
for key,row in rows.items():
 if key in select:
  row.update(decision='retain_version_dependency',instrument_id=select[key][0],reason=select[key][1])
 elif key in exclude: row.update(decision='exclude_this_action',reason=exclude[key])
 elif row['agency'] in agency_exclusions:row.update(decision='exclude_this_action',reason=agency_exclusions[row['agency']])
 elif row['agency']=='Department of Justice':row.update(decision='exclude_this_action',reason='This action concerns firearms commercial/loan rules, gaming, or police accountability rather than residential work or account resolution; abandoned firearm handling remains governed by separately retained authorities.')
 else:row.update(decision='unresolved',reason='Requires substantive review; not excluded by lack of immediate keyword match.')
# Bound every row to its actual observed index; membership is evidence, not section-text harvest.
for name in ['quarter_census','quarter_census2','agency_final_batch']:
 s=json.loads((HERE/(name+'-capture.json')).read_text())
 for block in s.split('--------------------------------------------------------------------------------'):
  match=re.search(r'https://oal.ca.gov/(?:october-1-2026-effective-date|july-1-effective_date|april_1_effective_date|january-1-2027-effective-date)/',block)
  if not match:continue
  for key in rows:
   if key in block:rows[key].setdefault('index_urls',[]);rows[key]['index_urls']=sorted(set(rows[key]['index_urls']+[match[0]]))
ledger={'as_of':'2026-10-01','scope':'Every posted row in OAL April/July/October2026 and January2027 quarterly tables, as retrieved October1. April table nominal filed interval Dec1 2025–Feb28 2026; July Mar1–May31; October June1–Aug31; Jan2027 Sept1–Nov30, only rows posted throughSept10 currently. Some tables include out-of-interval and emergency rows, retained as observed.','limitation':'Not a complete all-agency filing census. Agency cross-check found Architects103, CPUC and BES missing from these tables. January1 2026 baseline table and entire nonstandard-date table are outside this bounded ledger.','rows':rows}
(HERE/'quarterly-screen-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
print('Rows:',len(rows));print('Unresolved:',[k for k,v in rows.items() if v['decision']=='unresolved'])
