"""Explicit non-code source selections for J1; run before build_register.py."""
from build_register import BASE,HERE,instrument,save
import json,re,copy

items=[]
def add(*args,**kw):
    i=instrument(*args,**kw); items.append(i); return i

# Retain reusable parent sources, and reverse NYC/settlement-only exclusions.
legacy=json.loads((BASE/'register/instruments.json').read_text())
legacy_functions=json.loads((HERE/'legacy_functions.json').read_text())
reopen={'US:FRBP','US:15USC-ch41','US:12USC5481','US:34USC-VAWA','US:12CFR1022','US:24CFR100','US:24CFR982','US:24CFR5'}
for old in legacy['instruments']:
    if old['jurisdiction']!='US': continue
    i=copy.deepcopy(old)
    i['functions']=legacy_functions[i['id']]
    i['adapter']='generic'
    i['legacy_source']='register/instruments.json'
    i['acquisition']={'text_adapter':'generic','enumeration':'USLM XML for USC; eCFR dated XML/HTML for CFR; official court PDF for rules. Expand every selected unit, not just saved sections.'}
    if not i['units_in_scope'] or i['id'] in reopen:
        for u in i['units_out']:
            u['reason']='Included: prior exclusion rested on the NYC market-rate or settlement-only aperture, which does not apply here.'
        i['units_in_scope']+=i['units_out'];i['units_out']=[]
    if i['id']=='US:11USC':
        keep=[]
        for u in i['units_out']:
            if any(k in u['unit'] for k in ['CHAPTER 9','CHAPTER 12','CHAPTER 15']):
                u['reason']='Public-owner, individual farming-income or cross-border status does not remove residential debts from this aperture.'
                i['units_in_scope'].append(u)
            else: keep.append(u)
        i['units_out']=keep
    i['scope_review']='Reconciled against California physical-work and outgoing-account aperture; applicability remains conditional.'
    items.append(i)

cf={
 (24,8):('HUD disability nondiscrimination',['anti_discrimination','housing_assistance']),
 (24,35):('Residential lead-paint requirements',['preconditions','landlord_tenant']),
 (24,91):('Consolidated housing/community plans',['housing_assistance']),
 (24,93):('Housing Trust Fund',['housing_assistance','rent_regulation']),
 (24,200):('HUD mortgage insurance general requirements',['housing_assistance','preconditions']),
 (24,245):('Tenant participation in multifamily housing projects',['housing_assistance','landlord_tenant']),
 (24,247):('Evictions from subsidized and HUD-owned projects',['housing_assistance','early_termination']),
 (24,576):('Emergency Solutions Grants',['housing_assistance','landlord_tenant']),
 (24,578):('Continuum of Care',['housing_assistance','landlord_tenant']),
 (24,984):('Family Self-Sufficiency',['housing_assistance','payments']),
 (28,35):('ADA state/local services',['anti_discrimination','preconditions']),
 (28,36):('ADA public accommodations',['anti_discrimination','preconditions']),
 (40,61):('Hazardous air pollutants',['preconditions']),
 (40,745):('Residential lead paint',['preconditions','landlord_tenant']),
 (40,261):('Hazardous waste identification',['preconditions']),
 (40,262):('Hazardous waste generators',['preconditions']),
 (40,273):('Universal waste management',['preconditions']),
 (29,1910):('Workplace safety standards',['preconditions']),
 (29,1926):('Construction safety standards',['preconditions']),
 (29,1952):('Approved state safety plans',['preconditions','general_construction']),
 (12,1002):('Equal Credit Opportunity / Regulation B',['usury_payment_plans','anti_discrimination']),
 (12,1026):('Truth in Lending / Regulation Z',['usury_payment_plans','payments']),
 (16,313):('Financial information privacy',['data_security']),
 (16,314):('Customer information safeguards',['data_security']),
 (16,681):('Identity theft rules',['credit_reporting','data_security']),
}
for (t,p),(name,fn) in cf.items():
    add('US',f'{t}CFR{p}',f'{t} CFR {p}: {name}','regulation',fn,f'https://www.ecfr.gov/current/title-{t}/part-{p}',[f'Part {p}, all subparts and appendices'])

usc=[
 ('1USC','Construction and effective law','1','1 2 3',['general_construction']),
 ('9USC','Federal Arbitration Act','9','1 2 3',['courts_procedure']),
 ('28USC','Judiciary and judicial procedure','28','1 3 5 6 7 21 23 31 33 37 39 41 43 45 49 51 57 81 83 85 87 89 91 93 95 97 99 111 113 115 117 119 121 123 125 127 129 131 133 135 137 139 141 151 153 155 157 159 161 163 165 169 171 173 175 176',['courts_procedure','limitations','debt_collection']),
 ('42USC21','Civil rights','42','21',['anti_discrimination','courts_procedure']),
 ('42USC126','Americans with Disabilities Act','42','126',['anti_discrimination','preconditions']),
 ('29USC16','Rehabilitation Act','29','16',['anti_discrimination','housing_assistance']),
 ('42USC8','Low-income housing','42','8',['housing_assistance','rent_regulation']),
 ('42USC8A','Slum clearance and farm housing','42','8A',['housing_assistance']),
 ('42USC44','Housing and urban development','42','44',['housing_assistance']),
 ('42USC89','Congregate housing services','42','89',['housing_assistance']),
 ('42USC119','Homeless assistance','42','119',['housing_assistance']),
 ('42USC127','Residential lead hazard reduction','42','127',['preconditions']),
 ('42USC129','National Affordable Housing Act','42','129',['housing_assistance']),
 ('15USC53','Toxic Substances Control Act','15','53',['preconditions']),
 ('15USC94','Financial privacy / GLBA','15','94',['data_security']),
 ('29USC15','Occupational Safety and Health Act','29','15',['preconditions']),
]
for ident,name,title,chapters,fn in usc:
    add('US',ident,name,'statute',fn,f'https://uscode.house.gov/browse/prelim@title{title}&edition=prelim',[f'Chapter {n} (all subchapters)' for n in chapters.split()])
for ident,name,ref,fn in [
 ('26USC42','Low-income housing tax credit','42',['housing_assistance','rent_regulation']),
 ('26USC142','Exempt-facility housing bonds','142',['housing_assistance','rent_regulation']),
 ('26USC145','Qualified nonprofit bonds','145',['housing_assistance']),
 ('26USC6050W','Payment settlement reporting','6050W',['tax_reporting']),
 ('26USC3406','Backup withholding','3406',['tax_reporting'])]:
    add('US',ident,name,'statute',fn,f'https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title26-section{ref}&num=0&edition=prelim',[f'26 USC {ref}, complete section and notes'])
for ident,name,url in [
 ('FRCP','Federal Rules of Civil Procedure','federal-rules-civil-procedure'),
 ('FRE','Federal Rules of Evidence','federal-rules-evidence'),
 ('FRAP','Federal Rules of Appellate Procedure','federal-rules-appellate-procedure')]:
    add('US',ident,name,'court rule',['courts_procedure'],'https://www.uscourts.gov/forms-rules/current-rules-practice-procedure/'+url,['All titles/articles/parts, appendices and prescribed forms'])

CCR_SELECT={1:'1 2',2:'2 3 4 4.1 4.5 7',3:'1 2 3 4 6',4:'3 6 7 8 9 9.5 9.6 11 12 13 17',5:'4 5 6 7.5 10',7:'',8:'1',9:'1 4',10:'1 3 5 6 6.5 6.50 7.95 14',11:'1 4 6',12:'1 2',13:'1 2 3',14:'1 1.5 2 4 5 5.4 5.5 5.6 6 6.3 6.5 7 8 9 17',15:'',16:'2 5 7 8 19 22 24 26 27 29 35 36 38 41',17:'1 2 3 3.5',18:'1 2 2.1 2.4 2.5 3 4.1 5',19:'1 2 3 4 5',20:'1 2',21:'1 2 5',22:'1 1.8 2 4 4.5 5 6 7 8 11 12 13',23:'1 1.5 2 3 4 5 6 7',25:'1 2',26:'',27:'1 2 3 4',28:''}
CCR_FUNCTIONS={1:['general_construction','courts_procedure'],2:['anti_discrimination','entity_capacity','electronic_records','housing_assistance'],3:['preconditions'],4:['housing_assistance','preconditions','fees'],5:['housing_assistance','landlord_tenant'],7:[],8:['preconditions','payments'],9:['housing_assistance','estates_incapacity'],10:['broker_licensing','consumer_protection','debt_collection','payments','data_security'],11:['data_security','communications','consumer_protection','preconditions'],12:['military','housing_assistance'],13:['abandoned_property','preconditions'],14:['preconditions','housing_assistance'],15:[],16:['broker_licensing','preconditions','courts_procedure','estates_incapacity'],17:['preconditions','housing_assistance'],18:['tax_reporting','unclaimed_property','entity_capacity','housing_assistance'],19:['preconditions'],20:['payments','fees','preconditions'],21:['preconditions'],22:['preconditions','housing_assistance','anti_discrimination','estates_incapacity'],23:['preconditions','payments'],25:['landlord_tenant','housing_assistance','preconditions'],26:[],27:['preconditions'],28:[]}
for n,selection in CCR_SELECT.items():
    f=HERE/'sources'/f'ccr-title-{n}.txt'
    if n==10:f=HERE/'sources/agency-census-0.txt'
    raw=f.read_text()
    if n==10:raw=raw.split('Title 10 - Investment |')[1]
    raw=raw.split('State regulations are updated quarterly')[0]
    heads=list(dict.fromkeys(re.findall(r'†((?:Division|Chapter) [^]+)',raw)))
    i=add('CA',f'CCR{n}',f'California Code of Regulations, Title {n}','regulation',CCR_FUNCTIONS[n],'https://oal.ca.gov/publications/ccr/',[])
    i['toc_mirror_url']=f'https://www.law.cornell.edu/regulations/california/title-{n}'
    i['source_capture']=str(f.relative_to(BASE))
    i['currentness_note']='LII supplies the browse tree; official CCR and issuing-agency adoption texts determine legal version. LII quarterly update is not treated as current legal authority.'
    for h in heads:
        num=re.match(r'(?:Division|Chapter) ([0-9.]+)',h)[1]
        keep=num in selection.split()
        reason=('Complete mixed agency unit: retain duties, definitions, exceptions, enforcement and program conditions for section review.' if keep else
          ('Removed duplicate compilation; use the originating CCR titles listed in these headings.' if n==26 else f'{h.split(" (")[0]} governs a separate industry, institutional administration or program outside residential physical work and account resolution.'))
        i['units_in_scope' if keep else 'units_out'].append({'unit':h.split(' (')[0],'heading':h,'toc_url':i['toc_mirror_url'],'reason':reason})

add('CA','CCR24','2025 California Building Standards Code','regulation',['preconditions','landlord_tenant','anti_discrimination'],'https://www.dgs.ca.gov/BSC/Codes',[
 'Part 1 Administrative','Part 2 Building (Volumes 1 and 2)','Part 2.5 Residential','Part 3 Electrical','Part 4 Mechanical','Part 5 Plumbing','Part 6 Energy','Part 7 Wildland-Urban Interface','Part 8 Historical Building','Part 9 Fire','Part 10 Existing Building','Part 11 Green Building','Part 12 Referenced Standards'],note='Entire part and incorporated standards; 2025 edition effective 2026-01-01. Retain prior edition where event/permit date makes it applicable; read local amendments separately.')

# Court sources attach by forum, not by where a litigant happens to live.
add('CA','CRC','California Rules of Court','court rule',['courts_procedure','electronic_records','estates_incapacity'],'https://courts.ca.gov/forms-rules/rules-court',[
 'Title 1 All courts','Title 2 Trial courts','Title 3 Civil','Title 5 Family and juvenile (protective orders/capacity dependencies)','Title 7 Probate and mental health','Title 8 Appeals','Title 9 Law practice','Title 10 Judicial administration','Standards of Judicial Administration','Ethics Standards for Neutral Arbitrators','Appendices and mandatory forms'],outs=[('Title 4 Criminal','Standalone criminal proceedings are outside the aperture; protective-order dependencies retained in Title 5 and statutes.'),('Title 6 Reserved','No operative rules.')])
add('CA-OC','SUPERIOR-RULES','Orange County Superior Court local rules','court rule',['courts_procedure','estates_incapacity'],'https://www.occourts.org/forms-filing/rules-court',[
 'Preface/Civility Guidelines','Division 1 Court organization','Division 3 Civil rules','Division 4 Civil over $35,000','Division 5 Appellate division','Division 6 Probate','Division 7 Family law (protective orders/authority dependencies)','Division 10 Local Emergency Rule 1','Appendices and incorporated forms'],outs=[('Division 2 Personnel','Internal court employment administration.'),('Division 8 Criminal','Standalone criminal proceedings.'),('Division 9 Juvenile','Standalone juvenile proceedings.')])
for ident,name,url in [
 ('4DCA','Fourth District Court of Appeal rules and Division Three operating procedures','https://appellate.courts.ca.gov/district-courts/4dca/rules-forms-filing'),
 ('CACD','Central District civil local rules and general orders','https://www.cacd.uscourts.gov/court-procedures/local-rules'),
 ('CACB','Central District bankruptcy local rules, forms and general orders','https://www.cacb.uscourts.gov/the-central-guide/complete-sets-general-orders-lbr-lbr-forms-tcg-supplements'),
 ('CA9','Ninth Circuit rules','https://www.ca9.uscourts.gov/rules/'),
 ('BAP9','Ninth Circuit Bankruptcy Appellate Panel rules','https://www.bap9.uscourts.gov/rules')]:
    i=add('CA',ident,name,'court rule',['courts_procedure'],'%s'%url,['Complete civil/bankruptcy rule set and operative general orders; appendices/forms'])
    i['attachment']='Forum overlay: current Orange County/Huntington Beach proceedings. Does not purport to supply other California local trial court rules.'

add('CA-HB','MUNICIPAL','Huntington Beach municipal and zoning codes','local code',['landlord_tenant','preconditions','fees','consumer_protection','entity_capacity','payments'],'https://ecode360.com/HU4937',[
 'Charter','Title 1 General Provisions','Title 2 Administration and Personnel','Title 3 Revenue and Finance','Title 5 Business Licenses and Regulations','Title 7 Animals','Title 8 Health and Safety','Title 9 Public Peace, Morals and Welfare','Title 10 Vehicles and Traffic','Title 12 Streets and Sidewalks','Title 14 Water and Sewers','Title 15 Oil Code','Title 17 Buildings and Construction','Title 20 Zoning General','Title 21 Base Districts','Title 22 Overlay Districts','Title 23 District Provisions','Title 24 Administration','Title SR Statutory References','Title OL Ordinance history'],adapter='ecode360',outs=[(f'Title {n} Reserved','No operative provisions.') for n in [4,6,11,16,18,19]]+[('Title 13 Public Property','Public beach/park conduct outside residential premises; work access is retained in Titles 12, 14 and zoning.'),('Title 25 Subdivisions','Creation/subdivision of parcels is outside turn/repair work; existing parcel and permit conditions remain inputs.')])
add('CA-OC','CODE','Orange County codified ordinances','local code',['preconditions','fees','landlord_tenant','consumer_protection','entity_capacity'],'https://library.municode.com/ca/orange_county/codes/code_of_ordinances',[
 'Charter','Title 1 Government and Administration','Title 2 Public Facilities','Title 3 Public Morals, Safety and Welfare','Title 4 Health, Sanitation and Animal Regulations','Title 5 Business and Special Licenses, Regulations','Title 6 Highways, Bridges, Rights-of-Way, Vehicles','Title 7 Land Use and Building Regulations','Title 8 Fees','Title 9 Water Quality—Orange County Flood Control District','Supplement/ordinance history'],adapter='municode',note='Preserve territorial/application clauses. Unincorporated-only rules do not automatically apply inside Huntington Beach; countywide and district duties remain separately applicable.')
add('CA-OC','OCHA-ADMIN','OCHA Housing Choice Voucher Administrative Plan, approved 2026-04-14','agency rule',['housing_assistance','deposit','rent_regulation','early_termination','preconditions','payments','anti_discrimination'],'https://www.ochousing.org/sites/ocha/files/2026-04/Final%20-%20Orange%20County%20Housing%20Authority%20Administrative%20Plan%204-14-2026.pdf',['Complete plan, all chapters/exhibits and definitions'])
for ident,name in [('OCHA-PHA2026','Annual PHA Plan FY 2026'),('OCHA-PHA2025-29','PHA 5-Year Plan FY 2025-2029'),('OCHA-VAWA','VAWA Policy and Emergency Transfer Plan'),('OCHA-PAY2026','2026 Payment Standards'),('OCHA-UTILITY2026','2026 Utility Allowance Schedule'),('OCHA-INCOME2026','2026 HUD Income Limits'),('OCHA-FSS','HUD Approved FSS Action Plan'),('OCHA-COC','CoC Program PSH Guidebook')]:
    add('CA-OC',ident,name,'agency rule',['housing_assistance','payments','rent_regulation'],'https://housingauthority.oc.gov/documents-forms',['Complete named document and incorporated schedules'],note='Program-specific administrative material; applicability depends on the program, not on a generic affordable-housing label.')

regs={'I':'General','II':'Permits','III':'Fees','IV':'Prohibitions','V':'Hearing Board','VI':'Repealed','VII':'Emergencies','VIII':'Abatement','IX':'Stationary source performance','X':'Hazardous air pollutants','XI':'Source-specific standards','XII':'Practice and procedure','XIII':'New source review','XIV':'Toxics','XV':'Trip reduction','XVI':'Mobile offsets','XVII':'Significant deterioration','XVIII':'Reserved','XIX':'Federal conformity','XX':'RECLAIM','XXI':'Portable equipment','XXII':'Mobile mitigation','XXIII':'Facility mobile measures','XXIV':'In-use mobile reductions','XXV':'Trading','XXVII':'Climate change','XXX':'Title V permits','XXXI':'Acid rain','XXXV':'Railroads'}
omit={'VI','XVIII','XXXI','XXXV'}
add('CA-OC','SCAQMD','South Coast Air Quality Management District rule book','agency rule',['preconditions'],'https://www.aqmd.gov/home/rules-compliance/rules/scaqmd-rule-book',[f'Regulation {n}: {h}' for n,h in regs.items() if n not in omit],outs=[(f'Regulation {n}: {regs[n]}','Reserved/repealed or standalone power-generation/railroad program outside residential work.') for n in regs if n in omit],note='Regional overlay, not a county ordinance. Includes asbestos, coatings, dust, equipment and combustion; source/threshold exceptions require section review.')

from supplemental_sources import supplement
supplement(items)
save(HERE/'additional_instruments.json',items)
print(f'{len(items)} additional source entries prepared')
