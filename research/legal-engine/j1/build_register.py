"""Materialize the J1 scope decisions. This script does not decide legal relevance or completion.

Source headings are transcribed from saved TOCs. The explicit selections below are
the researcher's decisions. Running this preserves the previous registers once.
"""
from pathlib import Path
import json, re, shutil

BASE = Path(__file__).resolve().parents[1]
HERE = BASE / 'j1'
def save(path, obj):
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')
    temporary.replace(path)

def root_census():
    out = {}
    for f in sorted((HERE/'sources').glob('*.txt')):
        for block in f.read_text().split('--------------------------------------------------------------------------------'):
            m = re.search(r'codesTOCSelected.xhtml\?tocCode=([A-Z]+)', block)
            if not m: continue
            code = m[1]
            headings = list(dict.fromkeys(re.findall(r'†((?:DIVISION|TITLE|PART|ARTICLE) [^]+)', block)))
            if len(headings) > len(out.get(code, {}).get('headings', [])):
                out[code] = {'source_capture': str(f.relative_to(BASE)), 'headings': headings}
    return out

# Full parent units are retained when their headings cover both relevant and
# irrelevant provisions. Section review, not a title-only guess, resolves those.
SELECT = {
 'WAT': '1 2 4 5 6 7 11 12 13 16 17 18 20 20.5 21 28 30 31 33',
 'CIV': None, 'CCP': None, 'EVID': None,
 'BPC': '1 1.5 3 4 5 6 7 8',
 'COM': '1 2 3 4 5 7 9 10 11 12 13 14 15 16 17',
 'CORP': '1 2 2.6 3 10',
 'CONS': 'I II III IV V VI IX X XI XII XIII XIII A|XIII B|XIII C|XIII D|XIV XV XVI XVIII XX',
 'EDC': '3', 'ELEC': '',
 'FAC': '1 2 4 5 6 7 9 13 14 14.5 14.8 23',
 'FAM': '1 2 2.5 3 4 6 7 9 10 11 12',
 'FGC': '0.5 1 2 3 4 5 6 7 8 9',
 'FIN': '1 1.1 1.2 1.25 1.3 1.4 1.5 1.7 1.10 3 4.5 6 9 9.5 10 11.5 13 19 20 24 25',
 'GOV': '1 2 3 4 5 6 6.5 6.7 6.8 6.9 7 7.2 7.25 7.3 7.4 7.41 7.42 7.43 7.5 7.75 7.86 7.97 8 13 21.1',
 'HNC': '1 1.5 2 3 6 7 8',
 'HSC': '1 2 2.1 2.8 3 5 6 10.5 10.7 11 12 12.5 13 20 24 25.5 26 28 31 32 37 37.5 45 101 102 103 104 105 112 118 119 119.1',
 'INS': None,
 'LAB': '1 2 3 4 5',
 'MVC': '1 2 4 5 7 8',
 'PCC': None,
 'PEN': '1 2 4',
 'PRC': '1 2 3 4 6 7.7 7.8 8 9 10 11 12.1 12.2 12.3 12.4 12.7 12.9 13 13.5 15 16 16.3 17 18 19 19.5 20 20.4 20.6.5 20.6.9 21 22 25 26.5 27 30 31 33 34 38 43 44 45 46 47 50',
 'PROB': '1 2 3 4 4.5 5 6 7 8 9 11',
 'PUC': '1 1.5 1.7 2 2.5 3 3.5 4 4.1 4.8 4.9 5 6 7',
 'RTC': None,
 'SHC': '1 2 2.5 4 4.5 7 9 12 13 14 15 18',
 'UIC': '1 6',
 'VEH': '1 2 3 3.5 4 5 6.5 6.7 7 9 10 11 12 13 14.1 14.3 14.7 14.8 14.85 14.9 15 16.7 17 18',
 'WIC': '1 2 3.5 4 4.1 4.5 4.7 5 6 8 8.5 9 11.5 15',
}
WHY = {
 'WAT':'Water service, conservation, metering, discharge, drainage and site-work requirements.',
 'BPC':'Professional authority, vendor licensing, property management, meters, business practices and consumer charges.',
 'CIV':'Capacity, property rights, contracts, tenancy, payments, privacy, remedies and work obligations; complete mixed units retained for section review.',
 'CCP':'Civil claims, possession, provisional remedies, judgments, limitations, abandoned/unclaimed property and evidence procedures.',
 'COM':'Payment instruments, transfers, vendor goods and equipment contracts, security interests and transition law.',
 'CONS':'Rights, lawmaking, government powers, judicial remedies, housing authority, taxes/fees and usury.',
 'CORP':'Entity authority, representation, dissolution and surviving claims.',
 'EDC':'Student residential housing and educational public landlords; educational operations must be distinguished at section review.',
 'ELEC':'Election administration and political campaigns are outside tenancy, physical work and account resolution.',
 'EVID':'Proof of agreements, condition, work, charges, communications and settlement; civil applicability determined at section review.',
 'FAC':'Pest control, chemical use, landscape restrictions, animals and enforcement.',
 'FAM':'Household legal status, liability for debts, protective orders, contracting capacity and authority.',
 'FGC':'Pest/wildlife removal, nesting species, protected habitat and site-work permissions.',
 'FIN':'Collection licensing, financial consumer protections, payment handling, escrow, financing and foreclosure dependencies.',
 'GOV':'Public entity duties, claims, fair housing, local authority, land-use/repair permission, housing programs and courts.',
 'HNC':'Floating-home/marina residential classifications, premises authority and liens; operational commercial shipping excluded.',
 'HSC':'Habitability, residential classifications, fire, sanitation, remediation, environmental hazards, housing programs and enforcement.',
 'INS':'Property damage and liability claims, surety coverage, adjusting authority and fair claims handling.',
 'LAB':'Safe work, contractor responsibilities, classification and payment obligations incident to residential work.',
 'MVC':'Military tenancy protections, civil procedure and veterans housing programs.',
 'PCC':'Conditional public-owner repair procurement and payment; public ownership was not excluded at intake.',
 'PEN':'Lockouts, trespass, fraud, privacy/recording, protective orders and enforcement consequences affecting residential work.',
 'PRC':'Repair permissions, coastal/location requirements, fire clearance, environmental quality, materials, energy and waste.',
 'PROB':'Death, capacity, representatives, ownership and enforceability of tenancy/account obligations.',
 'PUC':'Utility service, shutoff, metering, customer protections and charges.',
 'RTC':'Entity suspension/capacity, information reporting and housing tax-credit restrictions; mixed divisions require section review.',
 'SHC':'Adjacent sidewalks, access, work permits, assessments, landscaping and parking.',
 'UIC':'Worker classification and withholding obligations incident to engaging or paying repair labor.',
 'VEH':'Private-property parking, towing, stored vehicles and lawful transport of property/materials.',
 'WIC':'Supported housing, assistance, capacity, elder protection and household protections.',
}
OUT = {
 'WAT':'Standalone district finance, major water infrastructure or energy procurement; premise service and discharge duties retained.',
 'BPC':'Licensing and operation of a separate medical, tobacco, alcohol or cannabis business; residential-use and nuisance effects remain in CIV/HSC/local code.',
 'COM':'Bulk business sales or investment securities, outside operating payments and vendor contracts.',
 'CONS':'Public employment or transport-revenue allocation, outside the operating decisions in this aperture.',
 'CORP':'Securities issuance and franchise-investment regulation, not entity capacity to operate or pursue an account.',
 'EDC':'Elementary/secondary education administration; housing and public-owner duties retained in generally applicable housing/procurement sources.',
 'ELEC':WHY['ELEC'],
 'FAC':'Agricultural production, commodity marketing or standalone food/vessel business, not residential pest and grounds work.',
 'FAM':'Standalone family-court services, custody/adoption proceedings or pilot administration, not household debt/capacity/protection.',
 'FGC':'Commercial fisheries/aquaculture or internal revenue/expenditure administration, not residential wildlife/site work.',
 'FIN':'Institutional organization, securities or unrelated education/enterprise lending programs, not residential account processing.',
 'GOV':'Transport administration, unrelated public programs, internal finance or political regulation outside residential operating decisions.',
 'HNC':'Commercial crews/cargoes and pilotage, not floating-home occupation or residential marina premises.',
 'HSC':'Clinical treatment, medical-business administration or unrelated health funding; housing/sanitation and protection provisions retained separately.',
 'LAB':'Standalone state-employee rehabilitation or business/workforce programs, not performing and paying for residential work.',
 'MVC':'Decorations and memorial/cemetery administration, not servicemember rights or residential assistance.',
 'PEN':'Prison/death-penalty administration, memorials or weapons regulation as a standalone criminal subject.',
 'PRC':'Standalone resource acquisition/conservancy administration, commercial mining, park or agricultural grant operations, outside residential maintenance.',
 'PROB':'Medical treatment decisions or allocation of death taxes, not authority to act on property and tenancy debts.',
 'PUC':'Transportation/airport agency operations, not utility services to premises.',
 'SHC':'Transport funding, bond-refinancing or toll/highway-district administration, not property access or maintenance duties.',
 'UIC':'Standalone employment-service and workforce programs or agency automation, outside contracting for residential work.',
 'VEH':'Driving-license/criminal sentencing or specialized vehicle industry operations, outside parking/towing and work transport.',
 'WIC':'Institutional corrections, healthcare coverage or standalone service administration, outside housing/household legal protections.',
}
FUN = {
 'WAT':['preconditions','landlord_tenant','payments'],
 'CIV':['deposit','landlord_tenant','fees','rent_regulation','early_termination','preconditions','abandoned_property','debt_collection','credit_reporting','consumer_protection','usury_payment_plans','anti_discrimination','electronic_records','data_security','communications','payments','general_construction'],
 'CCP':['courts_procedure','limitations','unclaimed_property','abandoned_property','debt_collection','entity_capacity'],
 'BPC':['broker_licensing','consumer_protection','preconditions','fees'],
 'COM':['payments','electronic_records','debt_collection'], 'CORP':['entity_capacity'],
 'CONS':['general_construction','courts_procedure','anti_discrimination','usury_payment_plans'],
 'EDC':['housing_assistance','landlord_tenant'], 'ELEC':[], 'EVID':['courts_procedure','electronic_records'],
 'FAC':['preconditions','landlord_tenant'], 'FAM':['estates_incapacity','early_termination','debt_collection'],
 'FGC':['preconditions'], 'FIN':['debt_collection','payments','usury_payment_plans','data_security'],
 'GOV':['anti_discrimination','courts_procedure','entity_capacity','housing_assistance','preconditions','fees'],
 'HNC':['landlord_tenant','abandoned_property'], 'HSC':['landlord_tenant','preconditions','housing_assistance','rent_regulation'],
 'INS':['consumer_protection','preconditions','debt_collection'], 'LAB':['preconditions','payments'],
 'MVC':['military','early_termination','courts_procedure','housing_assistance'], 'PCC':['preconditions','payments'],
 'PEN':['communications','consumer_protection','preconditions','data_security'], 'PRC':['preconditions','housing_assistance'],
 'PROB':['estates_incapacity','debt_collection','entity_capacity'], 'PUC':['payments','fees','landlord_tenant'],
 'RTC':['tax_reporting','entity_capacity','housing_assistance'], 'SHC':['preconditions','fees'],
 'UIC':['preconditions','tax_reporting'], 'VEH':['abandoned_property','preconditions','fees'],
 'WIC':['estates_incapacity','housing_assistance','anti_discrimination'],
}

def instrument(code, ident, name, level, functions, url, units, adapter='generic', outs=(), note=''):
    return {'id':f'{code}:{ident}','jurisdiction':code,'name':name,'level':level,
      'functions':functions,'toc_source_url':url,'adapter':adapter,
      'units_in_scope':[{'unit':u,'heading':u,'toc_url':url,'reason':note or 'Complete named unit; all sections, definitions, exceptions and appendices included.'} for u in units],
      'units_out':[{'unit':u,'heading':u,'reason':r} for u,r in outs],
      'acquisition':{'text_adapter':adapter,'enumeration':'Expand the named TOC units into individual section references in J2; retain edition and effective-date history.','status':'J1 identifies source and scope; section acquisition is J2.'}}

def build():
    census=root_census(); save(HERE/'code_root_census.json',census)
    docs={c:{'jurisdiction':c,'as_of':'2026-10-01','discovery_status':'open','instruments':[], 'functions_without_instrument':[]} for c in ['US','CA','CA-OC','CA-HB']}
    for code,x in sorted(census.items()):
        heads=x['headings']; selected=SELECT[code]
        i=instrument('CA',code,'California '+code,'statute',FUN[code],f'https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode={code}',[],'ca_leginfo',note=WHY[code])
        i['source_capture']=x['source_capture']
        i['units_in_scope']=[{'unit':'preliminary','heading':'Unnumbered title, preliminary provisions, definitions and construction','reason':'Preserve shared definitions and construction; do not orphan the selected units.','toc_url':i['toc_source_url']}] if code!='ELEC' else []
        for h in heads:
            m=re.match(r'(DIVISION|TITLE|PART|ARTICLE) (.*?)(?:\. | \[| [A-Z][A-Z])',h)
            if h in ['TITLE OF ACT','TITLE OF THE ACT']: continue
            number = re.match(r'(?:DIVISION|TITLE|PART) ([0-9.]+)',h)
            if code=='CONS':
                keep=not any(h.startswith('ARTICLE '+v+' ') for v in ['VII','X A','X B','XIX','XIX A','XIX B','XIX C','XIX D'])
            else:
                keep=selected is None or (number and number[1].rstrip('.') in selected.split())
            u={'unit':h,'heading':h,'toc_url':i['toc_source_url'],'reason':WHY[code] if keep else OUT[code]}
            i['units_in_scope' if keep else 'units_out'].append(u)
        docs['CA']['instruments'].append(i)
    extra=json.loads((HERE/'additional_instruments.json').read_text()) if (HERE/'additional_instruments.json').exists() else []
    for i in extra: docs[i['jurisdiction']]['instruments'].append(i)
    from refine_civil import refine
    refine(next(i for i in docs['CA']['instruments'] if i['id']=='CA:CIV'))
    # The coordinator integrates reasoned lane selections here after reviewing
    # their sources. Regenerating the baseline must not discard those decisions.
    updates=HERE/'register_updates.json'
    if updates.exists():
        for i in json.loads(updates.read_text())['instruments']:
            entries=docs[i['jurisdiction']]['instruments']
            existing=next((n for n,x in enumerate(entries) if x['id']==i['id']),None)
            if existing is None: entries.append(i)
            else: entries[existing]=i
    layer_decisions = HERE/'function_layer_decisions.json'
    if layer_decisions.exists():
        for c, reasons in json.loads(layer_decisions.read_text()).items():
            docs[c]['functions_without_instrument'] = reasons
    # Preserve the coordinator's explicit stage decision; generation is not its basis.
    completion = HERE/'completion.json'
    if completion.exists():
        decision = json.loads(completion.read_text())
        if decision.get('status') == 'complete':
            for c in decision['layers']:
                docs[c]['discovery_status'] = 'complete'
                docs[c]['j1_completion_decision'] = 'j1/completion.json'
    for c,doc in docs.items():
        target=BASE/'jurisdictions'/c/'instruments.json'
        backup=target.parent/'history'/'before-j1-register'/'instruments.json'
        backup.parent.mkdir(parents=True,exist_ok=True)
        if target.exists() and not backup.exists(): shutil.copy2(target,backup)
        save(target,doc)
    save(HERE/'COUNTS.json',{c:{'instruments':len(d['instruments']),'in_units':sum(len(i['units_in_scope']) for i in d['instruments']),'out_units':sum(len(i['units_out']) for i in d['instruments'])} for c,d in docs.items()})

if __name__=='__main__': build()
