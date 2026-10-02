"""Lane-local, repeatable J1 proposals. Does not write canonical registers."""
import copy, json, re, sys
from urllib.parse import unquote
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2]
sys.path.insert(0, str(BASE/'j1'))
from build_register import instrument

def save(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')

current = {i['id']: i for i in json.loads((BASE/'jurisdictions/US/instruments.json').read_text())['instruments']}
manifest = json.loads((HERE/'document_manifest.json').read_text())
proposals = {}

functions = {
 '11USC':['bankruptcy','debt_collection','payments','landlord_tenant'],
 'FRBP':['bankruptcy','courts_procedure'],
 '15USC-ch41':['debt_collection','credit_reporting','payments','usury_payment_plans','anti_discrimination'],
 '15USC-ch96':['electronic_records','communications','provider_contracts'],
 '42USC-ch45':['anti_discrimination','landlord_tenant','work_standards'],
 '50USC-ch50':['military','early_termination','courts_procedure','debt_collection'],
 '47USC227':['communications','debt_collection'],
 '26USC-6041-6050':['tax_reporting','payments'],
 '26USC166':['tax_reporting','debt_collection'],
 '12USC5481':['consumer_protection','debt_collection','usury_payment_plans','payments'],
 '12USC5220note':['landlord_tenant','early_termination'],
 '34USC-VAWA':['housing_assistance','anti_discrimination','early_termination','landlord_tenant'],
 '12CFR1006':['debt_collection','communications','credit_reporting'],
 '12CFR1005':['payments','consumer_protection'],
 '12CFR1022':['credit_reporting','data_security'],
 '24CFR100':['anti_discrimination','landlord_tenant','work_standards'],
 '24CFR982':['housing_assistance','deposit','rent_regulation','early_termination','payments','work_standards'],
 '24CFR5':['housing_assistance','anti_discrimination','rent_regulation','work_standards','early_termination'],
 '47CFR64L':['communications','debt_collection'],
 '26CFR1-info':['tax_reporting','payments','debt_collection'],
 '24CFR966':['housing_assistance','deposit','early_termination','courts_procedure','landlord_tenant'],
 '24CFR960':['housing_assistance','rent_regulation','anti_discrimination'],
 '24CFR880':['housing_assistance','rent_regulation','payments','work_standards','early_termination'],
 '24CFR881':['housing_assistance','rent_regulation','payments','work_standards','early_termination'],
 '24CFR882':['housing_assistance','rent_regulation','payments','work_standards','early_termination'],
 '24CFR883':['housing_assistance','rent_regulation','payments','work_standards','early_termination'],
 '24CFR884':['housing_assistance','rent_regulation','payments','work_standards','early_termination'],
 '24CFR886':['housing_assistance','rent_regulation','payments','work_standards','early_termination'],
 '24CFR891':['housing_assistance','rent_regulation','payments','work_standards','early_termination'],
 '24CFR983':['housing_assistance','rent_regulation','payments','work_standards','early_termination'],
 '24CFR92':['housing_assistance','rent_regulation','payments','work_standards','early_termination'],
 '7CFR3560':['housing_assistance','rent_regulation','payments','work_standards','early_termination'],
 '16CFR682':['data_security','credit_reporting'],
}
save('legacy_functions.json', {'US:'+k:v for k,v in functions.items()})

def put(x):
    x.pop('scope_review',None)
    proposals[x['id']]=x
    return x

def cfr_sections(ident, name, refs, funcs, reason):
    x=instrument('US',ident,name,'regulation',funcs,'https://www.ecfr.gov/current/title-26/part-1',[],adapter='ecfr')
    x['as_of']='2026-09-30'
    x['units_in_scope']=[{'unit':'26 CFR '+n,'heading':n,'reason':reason,'toc_url':'https://www.ecfr.gov/api/versioner/v1/full/2026-09-30/title-26.xml?part=1&section='+n} for n in refs]
    x['source_capture']='j1/lanes/federal_programs/federal-details.txt'
    return put(x)

# The old register's 33 rows were not a reasoned boundary: they included gambling
# returns yet omitted service-provider reporting and the current 1.6041-9.
refs=[f'1.166-{n}' for n in range(1,11)]+[f'1.6041-{n}' for n in range(1,10)]+['1.6041A-1']+[f'1.6049-{n}' for n in range(1,11)]+[f'1.6050P-{n}' for n in range(3)]+['1.6050W-1']
x=cfr_sections('26CFR1-info','Treasury: bad debts, provider payments, interest and debt/payment reporting',refs,functions['26CFR1-info'],'Complete identified reporting/debt provision, including definitions, exceptions and cross-references; historical variants remain for event-date selection.')
x['units_out']=[{'unit':'26 CFR 1.6041-10','reason':'Bingo, keno and slot-machine winnings reporting has no residential work/account connection.'},{'unit':'Remainder of 26 CFR Part 1 outside the separately registered 1.42 family','reason':'Standalone income-tax computation and unrelated businesses are outside this workflow; reporting, bad-debt closeout and housing-program requirements are separately selected.'}]
cfr_sections('26CFR1-LIHTC','Treasury low-income housing credit regulations',['1.42-0','1.42-0T','1.42-1','1.42-1T']+[f'1.42-{n}' for n in range(3,20) if n!=7],['housing_assistance','rent_regulation','work_standards','payments'],'Entire LIHTC regulatory family: retain rental eligibility, utility allowances, available-unit treatment, monitoring, program duration and construction provisions together.').update({'units_out':[{'unit':'1.42-2 and 1.42-7','reason':'Reserved entries; no operative sections.'}]})

DOC_NAMES={
 ('ctcac',44):('CTCAC-HOTMA-2026-08-04','CTCAC HOTMA Guidance Memo, August 4, 2026','Determines income and asset treatment, early adoption and January 2027 implementation for assisted units.'),
 ('ctcac',45):('CTCAC-policy-2026-07','CTCAC Compliance Policy Updates, July 2026, with attachments','Updates tenant/program compliance treatment and prescribed attachments.'),
 ('ctcac',46):('CTCAC-waiver-2026-06-09','CTCAC Rent Increase Limit Waiver Memorandum, June 9, 2026','Constrains rent increases and the waiver process affecting outgoing rent balances.'),
 ('ctcac',48):('CTCAC-waiver-tenant-notice','CTCAC Tenant Notice of Intent to Request Rent Increase Limit Waiver','Prescribed tenant notice accompanying the selected rent-limit waiver process.'),
 ('ctcac',49):('CTCAC-rent-cap-2026-07-15','CTCAC 2026/2027 Rent Increase Limit Update, July 15, 2026','Sets period-specific rent increase limits affecting lawful account charges.'),
 ('ctcac',51):('CTCAC-veteran-income','CTCAC VA Service-Connected Disability Benefits Exclusion for Veterans','Changes covered household income and resulting program rent calculations.'),
 ('ctcac',52):('CTCAC-secondary-tenants','CTCAC Secondary Tenants Policy and HUD-VASH Special Rule','Determines continuing occupancy and remaining household treatment after a departure.'),
 ('ctcac',54):('CTCAC-AIT','CTCAC Final Average Income Targeting Guidance','Determines unit restrictions and permissible rent in average-income projects.'),
 ('ctcac',55):('CTCAC-casualty-loss','CTCAC Casualty Loss Memorandum','Connects casualty repairs, restoration periods and assisted-unit compliance.'),
 ('ctcac',57):('CTCAC-exempt-unit-change','CTCAC Exempt Unit Change Policy','Determines treatment of exempt/resident-manager units and unit designation changes.'),
 ('ctcac',58):('CTCAC-rehabilitation-vacancies','CTCAC Policy Regarding Vacancies Pending a Rehabilitation','Constrains vacancy and work sequencing during rehabilitation.'),
 ('ctcac-appendix',37):('CTCAC-manual-2026','CTCAC Compliance Monitoring Manual, 2026 edition','Training/reference map for rental restrictions, unit condition, files and compliance; operative authority is traced separately.'),
 ('ctcac-appendix',44):('IRS-P5913-2024','IRS Publication 5913, Guide for Completing Form 8823, January 2024','Explains reporting and correction of LIHTC noncompliance, including condition and rent violations.'),
}
def docs(ident, name, code, captures, funcs, selection=None):
    selected=[d for d in manifest if d['capture'] in captures and d['ref'] and (selection is None or d['link_id'] in selection.get(d['capture'],[]))]
    unique={d['ref']:d for d in selected}
    x=instrument(code,ident,name,'agency rule',funcs,next(iter(unique),''),[])
    for d in unique.values():
        heading=d['heading'].strip() or d['ref'].split('/')[-1]
        number=re.sub(r'[^A-Za-z0-9_.-]+','-',unquote(d['ref'].split('/')[-1]).removesuffix('.pdf'))
        reason='LIHTC administrative interpretation concerning covered unit/rent treatment, program restrictions or correction; retain effective-date and supersession clauses.' if ident=='IRS-LIHTC-GUIDANCE' else 'Program-specific conditions governing repairs, tenant charges, remaining occupancy or disputed account treatment.'
        number,heading,reason=DOC_NAMES.get((d['capture'],d['link_id']),(number,heading,reason))
        x['units_in_scope'].append({'unit':heading,'heading':heading,'toc_url':d['ref'],'reason':reason,'section_list':[{'number':number,'heading':heading,'ref':d['ref']}],'source_capture':'j1/lanes/federal_programs/'+d['capture']+('-documents.txt' if d['capture'] in ['ctcac','hcd','calhfa'] else '.txt')})
    x['legal_use']='Agency guidance, prescribed contractual terms and regulations retain their different force. Read underlying authority and actual program agreement; a handbook is not an independent substitute for controlling law.'
    return put(x)

x=docs('CTCAC-COMPLIANCE','CTCAC current compliance manual and operative policy documents','CA',['ctcac','ctcac-appendix'],['housing_assistance','rent_regulation','payments','work_standards','early_termination'],{'ctcac':[44,45,46,48,49,51,52,54,55,57,58], 'ctcac-appendix':[37]})
x['edition_note']='Current directory resolves to ctcac/2026%20Compliance%20Manual.pdf. Earlier saved 2026-01/manual.pdf is an April 2023 manual, not this edition. Manual describes itself as training material; register operative policy documents separately within this set.'
x['temporal_note']='August 4, 2026 CTCAC HOTMA memo requires implementation January 1, 2027, with stated early-adoption and income-definition distinctions. This is a CTCAC transition, not automatic importation of every HUD program rule.'
docs('IRS-LIHTC-GUIDANCE','IRS LIHTC administrative interpretations and compliance guide','US',['ctcac-appendix'],['housing_assistance','rent_regulation','payments','work_standards'],{'ctcac-appendix':[44,49,50,51,52,55,56,58,59,63,64,65,66,67,68,69,70]})

x=copy.deepcopy(current['US:HUD-HOTMA'])
x['units_in_scope']=[]
hotma=[('Final rule 88 FR 9600','https://www.govinfo.gov/content/pkg/FR-2023-02-14/pdf/2023-01617.pdf'),('Joint implementation guidance H 2023-10/PIH 2023-27, Revision 3','https://www.hud.gov/sites/dfiles/OCHCO/documents/2023-10hsgn.pdf'),('H 2024-04 TSP/EIV timing','https://www.hud.gov/sites/dfiles/OCHCO/documents/2024-04hsgn.pdf'),('H 2024-09 prior multifamily timing','https://www.hud.gov/sites/dfiles/OCHCO/documents/2024-09hsgn.pdf'),('H 2025-03 prior multifamily timing','https://www.hud.gov/sites/dfiles/OCHCO/documents/2025-03hsgn.pdf'),('H 2025-07 multifamily compliance','https://www.hud.gov/sites/dfiles/hudclips/documents/HSGN-07.pdf'),('PIH 2024-38 partial PHA implementation','https://www.hud.gov/sites/dfiles/OCHCO/documents/2024-38pihn.pdf'),('PIH 2026-15 PHA compliance and reporting','https://www.hud.gov/sites/default/files/hudclips/documents/PIH-2026-15.pdf'),('H 2026-05 / PIH 2026-09 interim reexaminations','https://www.hud.gov/sites/default/files/hudclips/documents/PIH-2026-09.pdf')]
for n,(name,url) in enumerate(hotma,1):x['units_in_scope'].append({'unit':name,'heading':name,'toc_url':url,'reason':'Complete notice/rule with attachments; current or explicitly historical transition source.','section_list':[{'number':f'HOTMA-{n}','heading':name,'ref':url}]})
x['temporal_note']='MFH: H 2025-07 January 1, 2027 full compliance. PIH: PIH 2026-15 January 1, 2027 except MTW/exclusive FRS agencies, whose systems conditions remain separate; PIH 2024-38 July 1, 2025 requirements are not postponed. H 2026-05/PIH 2026-09 amends Attachment I; use Revision 3. Early adoption and actual PHA policy remain distinct.'
x['source_capture']='j1/lanes/federal_programs/resolved_currentness.txt';put(x)
x=copy.deepcopy(current['US:HUD-NSPIRE'])
for u in x['units_in_scope']:
    if 'Superseded transition' in u['unit']:
        u['unit']=u['heading']='Earlier transition notices FR-6086-N-07, N-08, N-09 and PIH 2024-39/H 2024-11'
        u['reason']='Retain program-specific historical transitions; later voucher extensions do not themselves extend CPD deadlines.'
name='PIH 2026-18 voucher-program NSPIRE administrative procedures';url='https://www.hud.gov/sites/default/files/PIH/documents/PIH-2026-18.pdf'
x['units_in_scope'].append({'unit':name,'heading':name,'toc_url':url,'reason':'July 15, 2026 notice supersedes PIH 2023-28 and 2024-26 and clarifies precisely which requirements are delayed.','section_list':[{'number':'PIH-2026-18','heading':name,'ref':url}]})
x['temporal_note']='Separate CPD, voucher and public/multifamily clocks. FR-6086-N-12 extends specified HCV/PBV/Mod Rehab compliance to February 1, 2027; PIH 2026-18 identifies delayed versus unaffected provisions. PIH 2025-27/H 2025-06 public/multifamily scoring date is October 1, 2026. Earlier adoption is possible; OCHA local implementation evidence belongs in its own layer.'
put(x)

# Published state program instruments: dates follow document contents, not URL paths.
DOC_NAMES.update({
 ('hcd',23):('HCD-25-04','HCD Administrative Notice 25-04: Replacement Reserve Guidelines (April 21, 2025)','Controls reserve-funded repair work, bids, eligible costs and withdrawals; supersedes Notice 16-02 despite legacy filename.'),
 ('hcd',26):('HCD-Management-Contract','HCD Residential Management Contract','Prescribed allocation of owner/agent maintenance, contracting, collection and record duties.'),
 ('hcd',28):('HCD-Management-Plan','HCD Management Plan Checklist','Required operating policies for maintenance, tenant charges, notices and grievance handling.'),
 ('hcd',30):('HCD-Lease-Addendum','HCD Lease Addendum','Program lease conditions affecting rent, occupancy, termination and tenant account rights.'),
 ('hcd',43):('HCD-25-06','HCD Notice 25-06: Rent Increase Limit Policy and Waiver','Program rent-increase limit and waiver conditions affect lawful charges.'),
 ('hcd',44):('HCD-Co-Regulated-Monitoring','HCD Streamlining of Long-Term Monitoring for Co-Regulated Developments','Determines which agency monitoring requirements control a multiply regulated property.'),
 ('hcd',45):('HCD-AB2240','HCD Farmworker Housing Grant Marketing to OMS','Conditional farmworker program occupancy and waiting-list rules affect ability to lease a returned unit.'),
 ('hcd',46):('HCD-24-07','HCD Notice 24-07: Veterans Income Exclusions','Income exclusions affect assistance and lawful tenant rent where the designated program applies.'),
 ('hcd',47):('HCD-NSPIRE-2025-01-10','HCD NSPIRE Memorandum (January 10, 2025)','HCD inspection standard and implementation conditions for covered properties.'),
 ('hcd',49):('HCD-Transition-Reserve-2023-08-08','HCD Transition Reserve Policy, amended August 8, 2023','Reserve availability and conditions may fund continued operations or repair work.'),
 ('hcd',51):('HCD-Utility-Allowances','HCD Utility Allowance Notice','Utility allowance treatment affects permissible tenant rent and account amounts.'),
 ('umr',2):('UMR-2017','Uniform Multifamily Regulations, 2017 edition','Award-vintage rules for management, rents, reserves, budgets and property operation; use applicability provisions.'),
 ('umr',13):('UMR-2010','Uniform Multifamily Regulations, July 11, 2010 edition','Older award-vintage operational and reserve conditions remain conditional dependencies.'),
 ('umr',14):('UMR-2003','Uniform Multifamily Regulations, September 29, 2003 edition','Older award-vintage operational and reserve conditions remain conditional dependencies.'),
 ('calhfa',13):('CalHFA-Bid-Reserve-Guide','CalHFA Bid, Change Order and Replacement Reserve Guide','Controls approval and funding of covered repair contracts.'),
 ('calhfa',16):('CalHFA-Change-Order-Policy','CalHFA Change Order Policy','Controls modifications to covered work commitments.'),
 ('calhfa',20):('CalHFA-Reserve-Items-2026-04','CalHFA Combined Replacement Reserve Eligible and Ineligible Items (April 2026)','Determines which repair/replacement expenses may be paid from the reserve.'),
 ('calhfa',25):('CalHFA-Model-Lease-2008','CalHFA Model Form of Lease (2008)','Prescribed lease conditions govern rent, deposits, maintenance and termination where incorporated.'),
 ('calhfa',26):('CalHFA-Grievance','CalHFA Appeal and Grievance Procedure','Tenant dispute process can condition termination and charge enforcement.'),
 ('calhfa',28):('CalHFA-Eviction-2010','CalHFA Model Lease Attachment 4: Eviction Hearing Procedure (January 2010)','Required procedural dependency for covered termination decisions.'),
 ('calhfa',33):('CalHFA-HUD-Addendum-2013','CalHFA Addendum to HUD Lease Agreements (2013)','Additional state program terms apply to the covered HUD lease.'),
 ('calhfa',34):('CalHFA-811-Lease','Section 811 PRA Model Lease','Disability housing program lease terms include rent, deposits, maintenance and termination.'),
 ('pra811',9):('HUD-90173A-CA','Section 811 PRA Rental Assistance Contract Part I','Project contractual identification, assistance and term conditions.'),
 ('pra811',10):('HUD-90173B-CA','Section 811 PRA Rental Assistance Contract Part II','Owner duties, assistance payment conditions and remedies for noncompliance.'),
 ('pra811',13):('CalHFA-811-Eviction-F','Section 811 PRA Lease Addendum F: Eviction Hearing Procedure','Program procedural restriction on recovering possession.'),
})
x=docs('HCD-PROGRAM-INSTRUMENTS','HCD operating, reserve and tenancy program instruments','CA',['hcd','umr','hcd-program'],['housing_assistance','rent_regulation','payments','work_standards','provider_contracts','early_termination'],{'hcd':[23,26,28,30,43,44,45,46,47,49,51],'umr':[2,13,14],'hcd-program':[31,34]})
x['units_out']=[{'unit':'LA County wildfire waitlist priority notice, March 16, 2026 revision','heading':'LA County wildfire waitlist priority','reason':'Its operative property-location condition expressly covers developments in Los Angeles County; Huntington Beach is outside that territorial condition.'}]
x=docs('CALHFA-ASSET-INSTRUMENTS','CalHFA repair, management and tenancy instruments','CA',['calhfa','pra811'],['housing_assistance','rent_regulation','payments','work_standards','provider_contracts','early_termination'],{'calhfa':[13,16,20,25,26,28,33,34],'pra811':[9,10,13]})
x['retrieval_note']='Bid/reserve guide and change-order policy direct targets were recovered from the official directory, but their content fetch failed; no substantive edition assertion is made for those two documents.'

# Narrow work authorities. Procurement is conditional on the award/contract and implementing program.
def cfr(ident,title,part,name,reason,funcs,date='2026-09-30'):
 url=f'https://www.ecfr.gov/api/versioner/v1/full/{date}/title-{title}.xml?part={part}'
 x=instrument('US',ident,name,'regulation',funcs,url,[f'Part {part}'],adapter='ecfr',note=reason)
 x['version_date']=date
 return put(x)
work=['work_standards','provider_contracts','payments']
cfr('2CFR200',2,200,'Uniform Administrative Requirements, Cost Principles and Audit Requirements for Federal Awards','Covered repair procurement, allowable costs, payment, records and contract clauses depend on award applicability; retain definitions, exceptions and Appendix II.',work+['housing_assistance'])
for part,name,reason in [(1,'Davis-Bacon wage determination procedures','Wage determinations incorporated into covered housing repair/construction contracts.'),(3,'Copeland Act contractor and subcontractor requirements','Covered work payroll, deductions, statements and anti-kickback requirements.'),(5,'Labor standards for federally financed and assisted construction','Covered contracts require labor clauses, wage compliance, withholding and dispute procedures.'),(4,'Labor standards for federal service contracts','Conditional direct federal service contracts for maintenance can trigger service-contract wage duties; ordinary private repair contracts do not trigger this part.'),(516,'FLSA records','Required records when the operating model employs covered workers.'),(531,'FLSA wage payments and facilities','Permitted credits and deductions matter to worker payment obligations.'),(541,'FLSA executive, administrative and professional exemptions','Actual role and compensation determine exemptions for covered employed personnel.'),(778,'FLSA overtime compensation','Overtime computation where covered workers perform operational or repair work.'),(785,'FLSA hours worked','Working time and compensable activity for covered personnel.'),(791,'FLSA joint employment','Conditional shared-worker arrangement affects responsibility for wage obligations.'),(795,'FLSA employee or independent contractor classification','Worker classification determines direct payment duties; a contract label does not settle status.')]:
 cfr(f'29CFR{part}',29,part,name,reason,work)
proposals['US:29CFR795']['temporal_note']='DOL identifies the February 26, 2026 rulemaking as a proposal; do not substitute it for an adopted rule. Enforcement policy and court effects require their own evidence.'


for part,name,reason in [(42,'Displacement, relocation assistance and real property acquisition for HUD programs','Covered federally assisted rehabilitation can displace occupants or trigger relocation payments.'),(50,'HUD environmental review responsibilities','HUD review and conditions before committing to covered repair/rehabilitation work.'),(51,'HUD environmental criteria and standards','Noise, hazards and siting requirements when applicable to a covered rehabilitation project.'),(55,'Floodplain management and protection of wetlands','Covered work requires floodplain/wetland evaluation and conditions.'),(58,'Environmental review by responsible entities','Responsible-entity review, exemptions and choice-limiting action restrictions affect when work may proceed.'),(75,'Economic opportunities for low- and very low-income persons','Section 3 duties attach to covered public housing and housing/community-development assistance.'),(570,'Community Development Block Grants','Covered rehabilitation, public services, property standards, labor and program-income conditions depend on the funded activity.')]:
 cfr(f'24CFR{part}',24,part,name,reason,work+['housing_assistance'])
cfr('49CFR24',49,24,'Uniform Relocation Assistance and Real Property Acquisition','Covered assisted work can require displacement notices, replacement housing assistance and relocation payment procedures.',work+['housing_assistance','early_termination'])
cfr('7CFR3565',7,3565,'Guaranteed Rural Rental Housing Program','Conditional guarantee program includes project operation, tenant rents, property management and servicing requirements.',work+['housing_assistance','rent_regulation'],date='2026-09-29')
cfr('7CFR1970',7,1970,'USDA environmental policies and procedures','Covered USDA-financed work must satisfy environmental classification and review before commitment.',work+['housing_assistance'],date='2026-09-29')
for part,name,reason in [(260,'Hazardous waste management definitions and general provisions','Definitions and determination procedures support selected waste-generator and disposal rules.'),(263,'Hazardous waste transporters','Conditional removal of regulated repair debris triggers transporter and manifest obligations.'),(268,'Land disposal restrictions','Generator handling of covered waste requires treatment and notification conditions before disposal.'),(279,'Used oil management','Maintenance-generated used oil handling and disposal duties.'),(302,'Hazardous substance release notification','Reportable release from work or property conditions can trigger immediate federal notification.'),(761,'PCB use, cleanup and disposal','PCB-containing building materials/equipment can trigger marking, storage, remediation and disposal requirements.'),(84,'Hydrofluorocarbon restrictions and management','HVAC and refrigerant work can trigger technology-transition, servicing and disposal conditions.')]:
 cfr(f'40CFR{part}',40,part,name,reason,work)

# Correct inherited categorical exclusions without relying on customer type.
for ident in ['11USC','15USC-ch96','50USC-ch50','26USC166']:
 x=copy.deepcopy(current['US:'+ident]);x['functions']=functions[ident]
 retained=[]
 for u in x.get('units_out',[]):
  reopen=ident=='11USC' or (ident=='15USC-ch96' and 'TRANSFERABLE' in u['unit']) or (ident=='50USC-ch50' and 'TAXES AND PUBLIC' in u['unit'])
  if reopen:
   u=copy.deepcopy(u);u['reason']={'11USC':'Special debtor regimes can affect recovery from an owner/provider or enforcement of a tenancy claim; industry identity alone does not remove that dependency.','15USC-ch96':'Electronic transferable records may be used in secured settlement or provider payment obligations.','50USC-ch50':'Servicemember tax-sale protections can affect possession and property interests.'}[ident];x['units_in_scope'].append(u)
  else:retained.append(u)
 x['units_out']=retained
 if ident=='26USC166':
  for u in x['units_out']:u['reason']='Standalone computation of other tax deductions is outside account writeoff/reporting; this exclusion does not remove separately selected payment, withholding or program-tax authorities.'
 put(x)

# Direct, edition-specific program documents whose operative conditions can affect work or tenancy.
def document_set(code,ident,name,items,funcs):
 x=instrument(code,ident,name,'agency rule',funcs,items[0][2],[])
 for num,heading,url,reason in items:
  x['units_in_scope'].append({'unit':heading,'heading':heading,'toc_url':url,'reason':reason,'source_unit_kind':'document','section_list':[{'number':num,'heading':heading,'ref':url,'source_unit_kind':'document'}]})
 return put(x)
document_set('CA','HCD-PROGRAM-GUIDELINES','HCD program-specific operating guideline dependencies',[
 ('MHP-2025','MHP Final Guidelines, February 13, 2025','https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/supernofa/2025-mhp-guidelines.pdf','Body identifies Final Guidelines dated February 13, 2025, notwithstanding stale PDF title metadata. Nonretroactive Round 3 applicability. Covers operating income, rent, management, supportive services and construction requirements.'),
 ('FWHG-2025','2025 Joe Serna Jr. Farmworker Housing Grant Guidelines','https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/supernofa/2025-fwhg-guidelines.pdf','Conditional farmworker program adds population and operating conditions to common MHP rules.'),
 ('NPLH-2020-amended','No Place Like Home 2020 Amended Guidelines','https://www.hcd.ca.gov/grants-funding/active-funding/nplh/docs/NPLH-2020-Amended-Guidelines-Clean-Version.pdf','Current Round 4 directory links this amended edition; operating subsidy, management, rent and occupancy conditions survive award selection.'),
 ('MHP-2019','MHP Final Guidelines effective June 19, 2019, tracked edition','https://www.hcd.ca.gov/grants-funding/active-funding/mhp/docs/Round-1-MHP-Final-Guidelines-with-Tracked-Changes.pdf','Older award-vintage operation and rehabilitation duties; tracked deletions must not be read as operative text.'),
 ('VHHP-TOD-amendment','Notice of Amendment to TOD Rounds 1-3 and VHHP Rounds 1-4 Guidelines','https://www.hcd.ca.gov/grants-funding/active-funding/vhhp/docs/Notice-of-Amendment-to-TOD-%28Rounds-1-3%29-and-VHHP-Guidelines-%28Rounds-1-4%29.pdf','Specific amendment of retained award-vintage conditions; direct official target found, fetch failed.')],work+['housing_assistance','rent_regulation'])
document_set('US','HUD-HOME-TRANSITIONS','HOME rule effective-date transitions',[
 ('2026-08339','HOME Further Program Updates and Streamlining: indefinite delay (April 29, 2026)','https://www.govinfo.gov/content/pkg/FR-2026-04-29/pdf/2026-08339.pdf','Delays revised 92.250 and 92.253 indefinitely; do not treat the April 30 supplemental proposal as an adopted replacement.')],['housing_assistance','rent_regulation','early_termination','work_standards'])

# All these named policy/manual entries are document units, not invented section leaves.
for x in proposals.values():
 if x.get('adapter')=='generic' and x.get('level')=='agency rule':
  for u in x['units_in_scope']:
   if u.get('section_list'):
    u['source_unit_kind']='document'
    for entry in u['section_list']:entry['source_unit_kind']='document'

proposals.pop('US:29CFR791',None) # Reserved since 2021; 2026 proposal is not an operative part.
# Existing whole-part scopes receive dated API targets without changing their extent.
for ident,old in current.items():
 m=re.fullmatch(r'US:(7|12|16|24|28|29|40|47)CFR(\d+)',ident)
 if not m or ident in proposals:continue
 title,part=map(int,m.groups());x=copy.deepcopy(old)
 date='2026-09-29' if title==7 else '2026-09-30'
 url=f'https://www.ecfr.gov/api/versioner/v1/full/{date}/title-{title}.xml?part={part}'
 x['adapter']='ecfr';x['acquisition']['text_adapter']='ecfr';x['toc_source_url']=url;x['version_date']=date
 # The inherited whole-part units sometimes have subpart labels; preserve selection rather than duplicate the full part per label.
 for u in x['units_in_scope']:
  u['toc_url']=url
  sub=re.search(r'(?i)subpart ([A-Z]+)\b',u['unit'])
  if sub:u['toc_url']+='&subpart='+sub.group(1)
 put(x)

document_set('US','HUD-30DAY-TRANSITIONS','HUD nonpayment termination notice transition instruments',[
 ('2026-03921','Revocation of the 30-Day Notification Requirement, February 26, 2026','https://www.govinfo.gov/content/pkg/FR-2026-02-26/pdf/2026-03921.pdf','Adopted interim rule whose effectiveness was later delayed; retain for temporal reconciliation.'),
 ('2026-04990','Indefinite delay of HUD 30-day notice revocation, March 13, 2026','https://www.govinfo.gov/content/pkg/FR-2026-03-13/pdf/2026-04990.pdf','Indefinitely postpones revocation pending final action; agency now treats revocation as proposed.')],['housing_assistance','early_termination','landlord_tenant'])

selected_notices={
 'pih-relevant':{22:('PIH-2026-08','Federal procurement and single-audit threshold changes','Covered work procurement thresholds and streamlined requirements.'),57:('PIH-2025-06','Build America, Buy America implementation for public housing','Domestic-content conditions on covered infrastructure expenditures.'),85:('PIH-2024-20','Responding to Extreme Heat in Public Housing','Eligible cooling expenses and individual excess-utility relief affect work and tenant charges.'),137:('PIH-2023-06','Remedies for Poor Performing HCV/PBV Owners','PHA repair enforcement and owner payment remedies.'),163:('PIH-2022-20','FSS Escrow Accounts and Forfeited Escrow','Ownership and permissible use of escrow affect account closeout.'),183:('PIH-2022-01','Carbon Monoxide Alarms or Detectors in HUD-Assisted Housing','Required alarm work and inspection conditions.')},
 'housing-relevant':{5:('H-2026-06','Emergency Call Systems: Revisions to Handbook 4910.1','Changes applicable equipment standards for covered housing.'),9:('H-2026-02','Suspension of CNA eTool Submission and HUD Review','Changes approval process for capital needs assessments.'),22:('H-2024-10','Environmental Review for Multifamily Housing','Environmental review prerequisites for covered work.'),48:('H-2022-04','Reserve for Replacement Lender Delegation','Allocation of approval authority for reserve withdrawals funding repairs.'),62:('H-2020-10','Electronic Signature, Transmission and Storage','Requirements for electronically executed and retained program documents.')},
 'cpd-relevant':{11:('JOINT-LEAD-2026','Reduced Elevated Blood Lead Level Triggering Response','Covered assisted target housing requires hazard response at revised threshold.'),17:('CPD-2025-01','CPD Build America, Buy America Implementation','Covered CPD-funded work domestic-content conditions.'),38:('CPD-2022-13','HOME-ARP Revised Requirements','Special HOME-ARP tenancy and operating terms differ from baseline HOME.'),39:('HOME-ARP-Appendix','HOME-ARP Appendix','Companion alternative requirements and waivers for HOME-ARP.'),56:('CPD-2021-10','HOME-ARP Requirements','Foundational HOME-ARP requirements, read with subsequent amendments.'),42:('CPD-2022-10','HOPWA Rent Standards','HOPWA rent conditions affect lawful tenant charges.'),101:('CPD-2017-11','CoC Rent Contribution, Occupancy Charge and Utility Reimbursement','Utility responsibility determines participant charges and reimbursements.'),103:('CPD-2017-09','Management of CDBG-Assisted Real Property','Continued property use and management conditions for funded premises.')}
}
for cap,items in selected_notices.items():
 for link,(num,title,reason) in items.items():DOC_NAMES[(cap,link)]=(num,title,reason)
docs('HUD-OPERATING-NOTICES','HUD conditional work, reserve, tenancy and payment notices','US',list(selected_notices),work+['housing_assistance','rent_regulation','electronic_records'],{cap:list(v) for cap,v in selected_notices.items()})
for x in proposals.values():
 if x.get('adapter')=='generic' and x.get('level')=='agency rule':
  for u in x['units_in_scope']:
   if u.get('section_list'):
    u['source_unit_kind']='document'
    for entry in u['section_list']:entry['source_unit_kind']='document'

def usc(ident,title,name,units,reason,funcs):
 # Retain the shared register release pointer, explicitly without asserting fresh verification.
 url=f'https://uscode.house.gov/download/releasepoints/us/pl/119/111/xml_usc{title:02d}@119-111.zip'
 x=instrument('US',ident,name,'statute',funcs,url,[],adapter='usc')
 for label,selector in units:x['units_in_scope'].append({'unit':label,'heading':label,'toc_url':url,'uslm_identifier':selector,'reason':reason})
 x['version_note']='119-111 is the existing shared-register release pointer. Fresh OLRC release-page verification failed during maintenance; this pointer requires validation before claiming acquisition/currentness closure.'
 return put(x)
usc('29USC8',29,'Fair Labor Standards Act',[('Chapter 8','/us/usc/t29/ch8')],'Covered employed personnel and classification affect wages, overtime, deductions, records and remedies.',work)
usc('29USC9',29,'Portal-to-Portal Act',[('Chapter 9','/us/usc/t29/ch9')],'Compensable time, limitations and defenses are direct dependencies of FLSA work-payment claims.',work)
usc('40USC31',40,'Federal public works bonds and labor standards',[('Chapter 31','/us/usc/t40/stII/ptA/ch31')],'Covered public work requires payment/security and Davis-Bacon/Copeland labor terms; applicability is conditional on contract or funding authority.',work)
usc('40USC37',40,'Contract Work Hours and Safety Standards',[('Chapter 37','/us/usc/t40/stII/ptA/ch37')],'Covered federal/assisted construction contracts carry work-hour and safety obligations.',work)
usc('18USC874',18,'Kickbacks from public works employees',[('Section 874','/us/usc/t18/s874')],'Anti-kickback restriction applies to covered publicly financed construction or repair payroll.',work)
usc('41USC67',41,'Service Contract Labor Standards',[('Chapter 67','/us/usc/t41/stII/ch67')],'Direct covered federal maintenance service contracts can require prescribed wage and benefit terms.',work)
usc('42USC61',42,'Uniform Relocation Assistance and Real Property Acquisition',[('Chapter 61','/us/usc/t42/ch61')],'Federally assisted rehabilitation may cause displacement and compensation obligations.',work+['housing_assistance','early_termination'])
usc('42USC103',42,'CERCLA release response and liability',[('Chapter 103','/us/usc/t42/ch103')],'Hazardous-substance release, removal and cleanup can affect safe work, response costs and responsible-party obligations.',work)

x=document_set('US','PL119-101','21st Century ROAD to Housing Act, July 11, 2026',[
 ('PL119-101','Public Law 119-101: selected housing operation and physical-work provisions','https://www.govinfo.gov/content/pkg/PLAW-119publ101/html/PLAW-119publ101.htm','Acquire the enactment document; selected statutory units and exclusions below determine substantive extent. Do not infer program implementation dates merely from enactment.')],work+['housing_assistance','rent_regulation','early_termination'])
x['level']='statute'
x['selected_statutory_units']=[
 {'unit':'Sections 102, 103, 106, 202, 204-206, 210, 212','reason':'Building/repair standards, environmental review, whole-home repair assistance, conversion rehabilitation and RAD operating transitions.'},
 {'unit':'Sections 301-304','reason':'Manufactured/modular housing definitions, construction/rehabilitation and PRICE conditions may apply to covered residential work.'},
 {'unit':'Sections 404-405','reason':'FSS escrow and voucher inspection/owner participation changes directly affect account and repair decisions.'},
 {'unit':'Sections 501-505','reason':'HOME, rural housing, homelessness, disaster and MTW reforms affect conditional program operations and tenant/work requirements.'},
 {'unit':'Section 602','reason':'Disabled-veteran income treatment affects program eligibility and tenant rent.'},
 {'unit':'Sections 801-805','reason':'Interagency coordination, rural alignment and PHA/MTW accountability can alter implementation; study-only duties must remain distinguished from current operator mandates.'},
 {'unit':'Section 1001','reason':'Subsection (c)(5) requires covered institutional owners to provide initial and annual renter-outreach notices, update dispute-contact information within 30 days, and post resource information; retain definitions, exceptions and timing dependencies.'},
 {'unit':'Sections 1, 1201-1202','reason':'Interpretation, severability and funding context.'}]
x['units_out']=[{'unit':'Sections 101,104-105,107,201,203,207-209,211,213,401-403,601,603,701-704,901-909,1101','reason':'Counseling, land inventories, standalone mortgage origination/appraisal, planning/supply studies, banking supervision and central-bank currency are outside residential work and tenancy-account decisions; specific operating exceptions are selected separately.'}]
x['source_capture']='j1/lanes/federal_programs/transition-docs.txt'

# Bound 40 USC chapter 31 to work bonds/labor and related exceptions, not unrelated public-building administration.
x=proposals['US:40USC31'];url=x['toc_source_url'];x['units_in_scope']=[]
for sec in list(range(3131,3135))+list(range(3141,3149))+[3161,3162,3172]:
 x['units_in_scope'].append({'unit':f'Section {sec}','heading':f'40 USC {sec}','toc_url':url,'uslm_identifier':f'/us/usc/t40/s{sec}','reason':'Payment bonds, wage standards, volunteer exception or state workers-compensation applicability for covered federal work.'})
x['units_out']=[{'unit':'Other Chapter 31 sections','reason':'Federal building administration, land acquisition and unrelated internal services do not govern the selected work-contract decision.'}]

x=document_set('US','ACCESSIBILITY-STANDARDS','Federal accessibility standards and HUD adoption conditions',[
 ('UFAS-1984','Uniform Federal Accessibility Standards (1984), Access Board publisher','https://www.access-board.gov/files/ufas/ufas.pdf','Concrete technical standard used by HUD under Section 504/ABA; application comes from governing agency rules.'),
 ('ADA-2010','DOJ 2010 ADA Standards for Accessible Design','https://www.ada.gov/assets/pdfs/2010-design-standards.pdf','Technical/scoping standards for covered Title II/III work, including residential facilities where applicable.'),
 ('ADA-1991','DOJ 1991 ADA Standards for Accessible Design','https://www.ada.gov/assets/pdfs/1991-design-standards.pdf','Historical design and safe-harbor analysis requires the actual prior edition, not automatic retroactive use of 2010 standards.'),
 ('HUD-2014-11844','HUD alternative accessibility standard notice, 79 FR 29671, May 23, 2014','https://www.govinfo.gov/content/pkg/FR-2014-05-23/pdf/2014-11844.pdf','Permits specified use of 2010 Title II standards instead of UFAS for Section 504, with express exceptions; not a wholesale replacement.'),
 ('ABA-2004-2013','ABA Accessibility Standards, Access Board compilation with 2013 outdoor-developed-area supplement','https://www.access-board.gov/files/aba/ABAstandards.pdf','Conditional GSA/DOD/USPS adoption differs from HUD, which continues to use UFAS; retain responsible-agency applicability.'),
 ('FHA-DESIGN-MANUAL','HUD Fair Housing Act Design Manual','https://www.huduser.gov/portal/publications/PDF/FAIRHOUSING/fairfull.pdf','Named HUD safe-harbor design guidance informs restoration/alteration of covered multifamily accessible features; does not replace statutory design requirements.')],['work_standards','anti_discrimination','housing_assistance'])
x['adoption_note']='The Access Board states HUD has not adopted the newer ABA standards. Agency, facility, construction/alteration date and governing rule select the applicable standard; document availability does not establish universal applicability.'
cfr('24CFR40',24,40,'HUD accessibility standards under the Architectural Barriers Act','HUD ABA applicability and adopted technical standard govern covered federally financed residential construction and alteration.',['work_standards','anti_discrimination','housing_assistance'])

hb=json.loads((HERE/'handbook_manifest.json').read_text())
chapter_labels={9:(1,'Introduction'),11:(2,'Basic Documents'),15:(4,'Reserve Fund for Replacements'),27:(7,'Processing Budgeted Rent Increases'),29:(8,'Enforcement of Mortgagor Requirements'),41:(12,'Energy Conservation'),48:(16,'Partial Release of Security; Alterations'),54:(19,'Environmental Issues'),56:(20,'Historic Preservation'),58:(21,'Insurance and Loss Drafts'),62:(23,'Real Estate Assessment and Appeal'),66:(25,'Residual Receipts'),68:(26,'General Operating Reserve'),72:(28,'Special Escrows'),78:(31,'Mandatory Meals'),80:(32,'Pets'),82:(33,'Special Management and Servicing of SRO Projects'),84:(34,'Calculating Rents Using Annual Adjustment Factors'),86:(35,'Smoke Detectors')}
items=[]
for d in hb:
 if d['parent']=='turn1443view0' and d['url'] and d['link'] in chapter_labels:
  n,label=chapter_labels[d['link']];items.append((f'4350.1-ch{n}',f'HUD 4350.1 Chapter {n}: {label}',d['url'],'Chapter-specific operating, reserve, repair, safety or tenant-charge conditions for covered multifamily projects; read later rules and notices for supersession.'))
for n,label,url in [(6,'Project Monitoring','https://archives.hud.gov/offices/adm/hudclips/handbooks/hsgh/DOC_35338.DOC'),(9,'Enforcement of Civil Rights Requirements','https://archives.hud.gov/offices/adm/hudclips/handbooks/hsgh/DOC_35344.DOC'),(27,'Section 202 Debt Service Reserve','https://archives.hud.gov/offices/adm/hudclips/handbooks/hsgh/DOC_35313.PDF'),(38,'Multifamily Emergency/Disaster Guidance','https://archives.hud.gov/offices/adm/hudclips/handbooks/hsgh/DOC_24956.DOC')]:
 items.append((f'4350.1-ch{n}',f'HUD 4350.1 Chapter {n}: {label}',url,'Selected monitoring, reserve or emergency conditions; direct official archival target recovered, content fetch unsupported or timed out.'))
x=document_set('US','HUD4350.1','HUD 4350.1 Multifamily Asset Management and Project Servicing',items,work+['housing_assistance','rent_regulation','anti_discrimination'])
x['units_out']=[{'unit':'Chapters 3,5,10-11,13-15,17-18,22,24,29-30','reason':'Standalone mortgage origination, servicing/workout, financing, ownership conversion or loan restructuring; specific operating and repair requirements are retained in selected chapters and controlling program regulations.'},{'unit':'Chapters 36-37','reason':'Official directory says Coming soon; no published chapter was identified.'}]
labels=['Transmittal','Introduction','Approval of Management Agents','Allowable Management Fees from Project Funds','Working with Residents','Encouraging Training and Employment Opportunities','Program Monitoring','Program Compliance','Service Coordinator']
items=[]
for d in hb:
 if d['parent']=='turn1454view0' and d['url']:
  n=0 if d['link']==4 else d['link']-6;items.append((f'4381.5-ch{n}',f'HUD 4381.5: {labels[n]}',d['url'],'Management responsibility, fees, resident participation, compliance and service duties where the covered program agreement applies.'))
x=document_set('US','HUD4381.5','HUD 4381.5 Management Agent Handbook, REV-2 published chapters',items,work+['housing_assistance','landlord_tenant'])
x['edition_note']='Official HUD archive supplies published chapter files; later notices/program agreements may amend them. Chapter 9 Neighborhood Networks is excluded as standalone technology/community-service initiative administration.'
x=document_set('US','HUD4350.3',current['US:HUD4350.3']['name'],[('4350.3-REV1-CHG4','HUD 4350.3 REV-1 Change 4, complete published handbook','https://www.hud.gov/sites/documents/43503hsgh.pdf','Complete occupancy, lease, deposits, rent, termination and prescribed forms source; controlling HOTMA and later notices amend the older handbook.')],current['US:HUD4350.3']['functions'])
x['retrieval_note']='Official current handbook index identifies complete PDF and November 2013 Change 4 revision; direct full PDF fetch timed out. Internal-section harvesting remains J2.'
document_set('US','USDA-MFH-HANDBOOKS','USDA Rural Housing Service multifamily operating and servicing handbooks',[
 ('HB2-3560-2026-08-31','HB-2-3560 Multifamily Housing Asset Management Handbook, portal issued August 31, 2026','https://www.usda.gov/sites/default/files/guidance-documents/RHS%20HB-2-3560%20Consolidated.pdf','Covered direct-loan properties require maintenance, management, rent, reserve and tenant grievance/account procedures.'),
 ('HB3-3560-2026-03-10','HB-3-3560 Multifamily Housing Project Servicing Handbook, portal issued March 10, 2026','https://www.usda.gov/sites/default/files/guidance-documents/RHS%20HB-3-3560%20MFH%20Project%20Servicing%20Handbook.pdf','Servicing actions can change assistance, preservation duties, tenant protections and repair funding; use actual chapter effective dates.')],work+['housing_assistance','rent_regulation','early_termination'])
exec((HERE/'finalize_programs.py').read_text())
save('replacements.json',list(proposals.values()))
print(f'{len(proposals)} stable replacements/additions; {len(functions)} legacy function mappings')
