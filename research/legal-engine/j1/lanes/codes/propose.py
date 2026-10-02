"""Materialize researched CA source selections; writes only this lane's proposal.

Explicit decisions below are research judgments, not relevance classification.
Root integrates replacement entries by id; baseline.json preserves the starting draft.
"""
from pathlib import Path
from urllib.parse import urlencode
import copy, json, re

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2]
LI = 'https://leginfo.legislature.ca.gov/faces/'

def url(code, path):
    return LI + 'codes_displayText.xhtml?' + urlencode({'lawCode':code, **{k:v + ('' if code=='CONS' else '.') for k,v in path}})

def captures(code):
    lines={}
    for f in sorted((HERE/'sources').glob(code.lower()+'-*.txt')):
        # Only expanded TOCs supply structure, never a section page's navigation headings.
        t=f.read_text()
        if 'codedisplayexpand.xhtml' not in t and 'codes_displayexpandedbranch.xhtml' not in t:continue
        document=t.splitlines()[0]
        for n,s in re.findall(r'L(\d+): (.*?)(?=L\d+: |\n|$)',t):lines[(document,int(n))]=(s,str(f.relative_to(BASE)))
    return lines

def tree(code):
    order={'EDC':'title division part chapter article','GOV':'title division part chapter article','PEN':'part title division chapter article'}.get(code,'division part title chapter article').split()
    roots=[]; stack=[];previous=None
    for (document,line),(s,source) in sorted(captures(code).items()):
        if document!=previous:stack=[];previous=document
        for heading in re.findall(r'†([^]+)',s):
            heading=heading.strip()
            m=re.match(r'(TITLE|DIVISION|PART|CHAPTER|ARTICLE) ([0-9A-Za-z.]+)\. (.+)',heading)
            if not m:continue
            kind=m[1].lower(); number=m[2].rstrip('.');rank=order.index(kind)
            while stack and stack[-1]['rank']>=rank:stack.pop()
            path=(stack[-1]['path'] if stack else ())+((kind,number),)
            node={'path':path,'rank':rank,'heading':heading,'source_capture':source,'source_line':line,'children':[]}
            (stack[-1]['children'] if stack else roots).append(node);stack.append(node)
    return roots

def select_tree(i, rules, default_reason):
    code=i['id'].split(':')[1]; ins=[]; outs=[]
    roots=tree(code)
    paths=set()
    def record(n):
        paths.add(n['path'])
        for c in n['children']:record(c)
    for n in roots:record(n)
    missing=set(rules)-paths
    if missing:raise ValueError((code,'Decision path absent from captured TOC',sorted(missing)))
    def visit(n, inherited=(False,default_reason)):
        decision=rules.get(n['path'],inherited)
        descendants=[p for p in rules if len(p)>len(n['path']) and p[:len(n['path'])]==n['path']]
        if descendants:
            for child in n['children']:visit(child,decision)
        else:
            keep,why=decision
            u={k:n[k] for k in ['heading','source_capture','source_line']}
            u.update(unit=' / '.join(k+' '+v for k,v in n['path']),toc_url=url(code,n['path']),reason=why)
            (ins if keep else outs).append(u)
    for n in roots:visit(n)
    assert ins and outs,code
    i['units_in_scope']=[u for u in i['units_in_scope'] if u['unit']=='preliminary']+ins
    i['units_out']=outs
    i['scope_granularity']='Official TOC parents retained where mixed; explicit narrower decisions partition their descendants.'

def p(**kw):return tuple(kw.items())

def civil(i):
    excluded={
      'division 1 / part 2.6 / chapter 2.5':'Genetic-test disclosure by health-care service plans, a separate insurance/clinical relationship; ordinary information and housing discrimination protections remain selected.',
      'division 3 / part 4 / title 1.7 / chapter 1.5':'Motor-vehicle manufacturer warranty adjustment programs; source expressly excludes motor homes and concerns vehicle repair, not residential premises work.',
      'division 3 / part 4 / title 2.91 / chapter 3':'Employment counseling contracts and counseling-service bonds; no residential work or outgoing-tenancy account function.',
      'division 3 / part 4 / title 2.91 / chapter 4':'Job-listing service contracts; distinct from authority and obligations of engaged repair providers.',
      'division 3 / part 4 / title 5 / chapter 1.5':'Short-term passenger-car rental transactions are a separate consumer transport service; residential occupancy and goods-moving provider obligations remain selected.',
      'division 3 / part 4 / title 7 / chapter 5 / article 5':'Commercial space-flight participant liability and immunity; no residential work, goods disposition or outgoing-account connection.',
      'division 3 / part 4 / title 14 / chapter 2b':'Personal motor-vehicle purchase financing; section 2981 excludes business purchases and post-June-1981 mobilehome sales. This does not govern residential repair procurement or the occupancy account.',
      'division 4 / part 1 / title 3 / chapter 1.5':'Investment-adviser liability for compensated investment recommendations; separate from residential work commitments and occupancy-account resolution.',
      'division 4 / part 1 / title 7':'Managed-health-care duty of care, a clinical/health-plan obligation; not a residential repair or account duty.'}
    ins=[];outs=copy.deepcopy(i['units_out'])
    for u in i['units_in_scope']:
        if u['unit'] in excluded:
            u['reason']=excluded[u['unit']];outs.append(u)
        else:
            if u['unit']=='division 3 / part 4 / title 14 / chapter 2d':
                u['reason']='Section 2985.7 covers registered-vehicle leases exceeding four months for household use; retain conditionally for residential recreational-vehicle occupancy/termination, without treating ordinary auto rental as residential.'
                u['scope_evidence']='j1/lanes/codes/sources/civ-vehicle-definitions.txt'
            ins.append(u)
    i['units_in_scope']=ins;i['units_out']=outs

def constitution(i):
    i['units_in_scope']=[u for u in i['units_in_scope'] if u['unit']!='preliminary']
    old_out=i['units_out'];i['units_out']=[]
    for u in old_out:
        article=re.match(r'ARTICLE ([IVXLCDM]+(?: [A-D])?)\b',u['heading'])[1]
        if article=='VII':
            u['reason']='Public-service contracting boundary expressly referenced by Article XXII; retain the source dependency governing public architectural/engineering engagements.'
            i['units_in_scope'].append(u)
        else:
            if article=='X A':u['reason']='State water-project financing and bond allocation; separate from premise water service, work permissions and account charges.'
            elif article=='X B':u['reason']='Marine fisheries/protected fishing-zone constitutional regime; no residential work or outgoing-account function.'
            else:u['reason']='Allocation, borrowing and enforcement of transportation revenues; outside residential physical work and outgoing-account resolution.'
            i['units_out'].append(u)
    have={u['heading'] for k in ['units_in_scope','units_out'] for u in i[k]}
    for h in re.findall(r'†(ARTICLE [^]+)',(HERE/'sources'/'cons-root.txt').read_text()):
        if h in have:continue
        num=re.match(r'ARTICLE ([IVXLCDM]+(?: [A-D])?)\b',h)[1]
        keep=num in ['XXII','XXXIV']
        why={'XXII':'Authority to engage architectural and engineering providers for public-owner residential work.', 'XXXIV':'Conditional public-housing authority and scope; preserve its definitions and statutory dependencies.', 'XXI':'Electoral redistricting, outside residential work and account resolution.', 'XXXV':'Medical research funding, outside the residential operating functions.'}[num]
        i['units_in_scope' if keep else 'units_out'].append({'unit':'article '+num,'heading':h,'toc_url':url('CONS',[('article',num)]),'reason':why,'source_capture':str((HERE/'sources'/'cons-root.txt').relative_to(BASE))})

def education(i):
    rules={}
    def keep(path,why):rules[path]=(True,why)
    base='Educational administration, instruction, staff benefits or education financing without a residential work/account obligation; selected housing, property, equity and authority units are retained separately.'
    for chapter in ['1','2']:
        keep(p(title='1',division='1',part='1',chapter=chapter),'General construction and educational equity can govern institutional residential housing; retain definitions, enforcement and exceptions with the applicable provisions.')
    for part in ['7','8','10.5','19']:
        keep(p(title='1',division='1',part=part),'Mixed public educational property, joint authority, facilities and safety provisions may govern conditional residential premises; retain whole part for section review.')
    for part in ['21','23','24']:
        keep(p(title='2',division='3',part=part),'School-district authority, property, maintenance, financing and replacement housing; school-owned housing is within the agreed conditional aperture.')
    keep(p(title='2',division='4',part='32'),'State special schools include residential institutions; retain their occupancy and property authority rather than excluding the institutional housing regime.')
    for division,parts in [('5',['40','40.5','42']),('7',['45','47','49','50']),('8',['55']),('9',['57']),('10',['59']),('14',['65','66','68','68.1','68.2','69','70','72'])]:
        for part in parts:keep(p(title='3',division=division,part=part),'Conditional student/employee housing, institutional authority, residential facilities and funding restrictions; mixed units retained with applicable definitions and remedies.')
    select_tree(i,rules,base)

def revenue(i):
    rules={}
    def keep(path,why):rules[path]=(True,why)
    base='Standalone tax assessment, return computation, revenue distribution or separate-industry tax; selected operating purchases, reporting, capacity, housing restrictions and environmental charges are retained.'
    for path in [p(division='1',part='1'),p(division='1',part='2',chapter='1'),p(division='1',part='4',chapter='2'),p(division='1',part='6'),p(division='1',part='13')]:
        keep(path,'Property exemptions and affordability conditions, tax liens/title changes, disaster provisions and manufactured-home transfer dependencies can affect residential authority and obligations; retain complete named unit.')
    for part in ['1','1.5','1.6','1.7']:
        keep(p(division='2',part=part),'Tax treatment of purchased work/materials, equipment use and occupancy charges can affect actual vendor commitments and outgoing-account amounts; retain definitions, exceptions and enforcement.')
    for chapter in ['1','2','3','10.5','10.6','10.7']:
        keep(p(division='2',part='10',chapter=chapter),'Mixed tax definitions, housing credits, settlement/debt-income treatment and entity-status provisions; retained for the operating connection, not general owner tax-return preparation.')
    for chapter in ['1','2','4','7','9']:
        keep(p(division='2',part='10.2',chapter=chapter),'Reporting/withholding of work payments and account settlements, applicable definitions, administration and consequences; mixed chapters retained for complete review.')
    for path in [p(division='2',part='11',chapter='1'),p(division='2',part='11',chapter='2',article='7'),p(division='2',part='11',chapter='2',article='8'),p(division='2',part='11',chapter='3.5'),p(division='2',part='11',chapter='4')]:
        keep(path,'Entity suspension/revivor and dissolution affect contracting and recovery; housing tax credits/exempt entities can impose continuing residential restrictions. Keep shared definitions and mixed tax-credit chapter.')
    for part in ['19','20','22','22.1','22.5','23','26','30']:
        keep(p(division='2',part=part),'Utility, hazardous-substance, waste and tank charges and fee procedures may enter residential work costs or utility accounts; retain scope, payer, exemptions and enforcement together.')
    select_tree(i,rules,base)

def business(i):
    rules={}
    def keep(path,why):rules[path]=(True,why)
    base='Separate professional/industry business or commercial activity, without a residential work, provider, payment, information or account-resolution function.'
    for d in ['1','1.5']:
        keep(p(division=d),'Shared license authority, discipline and dispute remedies for selected providers.')
    for c in ['1','2','2.5','2.6','3','3.5','3.9','4','5','5.5','5.6','6','7','8.5','9','9.3','9.4','9.5','11','11.3','11.4','11.5','11.6','12.5','13','14','14.5','15','20','21.5']:
        keep(p(division='3',chapter=c),'Authority, qualification, contracts and remedies of relevant work, security, information, fiduciary or dispute providers; includes premises signs and assistance-animal provisions.')
    keep(p(division='4'),'Real-estate/property-management authority, appraisers and common-interest managers; conditional housing transaction regimes remain included.')
    rules[p(division='4',part='1',chapter='7')]=(False,'Mineral/oil/gas brokerage is a separate commercial brokerage activity; residential property-management authority remains selected.')
    for c in ['1','2','3','5','5.5','6','6.5','7']:
        keep(p(division='5',chapter=c),'Utility meters, measurement services, quantities and purchased material representations affect work and account charges.')
    keep(p(division='6',chapter='3'),'Trade names and designations can identify the contracting/provider party and prevent misleading business identity.')
    keep(p(division='7'),'Business licensing, competition, representations and independent contracting can govern provider commitments, consumer charges and communications.')
    rules[p(division='7',part='2',chapter='2.5')]=(False,'Obstruction of livestock sales is a separate agricultural trade.')
    for c in ['3','3.1','6','7','9','10','13','16','17.5','18','18.5','19','20','21.5','22','22.1','22.3','22.7','26','27','27.5','28','29','30','32','33','34','35','35.5']:
        keep(p(division='8',chapter=c),'Residential goods, movers/storage, work standards, service/notice providers, payments, communications or data/device protection; retain the whole identified operating subject.')
    for c in ['1','20']:
        keep(p(division='10',chapter=c),'Cannabis definitions and local/private-property control can affect lawful residential use; licensed cannabis-business operations are excluded separately.')
    select_tree(i,rules,base)

def government(i):
    rules={}
    def keep(path,why):rules[path]=(True,why)
    base='Separate government personnel/benefit administration, political administration, general fiscal operations or nonresidential public program; housing/work, agency powers, claims and public contracting units retained separately.'
    for d in ['1','3','3.5','3.6','4','4.5','5','6','7','9','10']:
        keep(p(title='1',division=d),'General government authority, public-owner claims/contracts, public records, remedies and construction applicable to residential operations; mixed division retained.')
    for d in ['1','2']:
        keep(p(title='2',division=d),'Statewide emergency, administrative and lawmaking authorities affect applicability, agency action and housing/work restrictions; retain mixed provisions.')
    for part in ['1','2','2.5','2.8','3','4','5.1','5.5','6','6.5','6.6','7.2','7.3','8.5','8.7','9','9.5','10','10.2','10.5','10b','11','14']:
        keep(p(title='2',division='3',part=part),'Public-owner/provider authority, civil rights, administrative remedies, housing programs, work/payment or environmental powers; retain full named agency part and its conditions.')
    for part in ['4','6','7']:
        keep(p(title='2',division='4',part=part),'Public payment instruments and mandated local costs may affect actual public-owner payment and local fee authority.')
    for title,ds in [('3',['1','2','3','5']),('4',['1','2','3','4']),('5',['1','2','3']),('6',['1','3','4','5','6','8'])]:
        for d in ds:keep(p(title=title,division=d),'Local authority, property, services, fees, public contracts and housing powers relevant to residential work/account resolution; territorial and program applicability remain conditional.')
    keep(p(title='6.7',division='1'),'Mixed infrastructure financing authority may govern funded residential work and continuing project conditions; separate transportation finance excluded.')
    titles=['6.5','6.8','6.9','7','7.2','7.25','7.3','7.4','7.41','7.42','7.43','7.5','7.75','7.86','7.97','8','13','21.1']
    for t in titles:keep(p(title=t),'Housing, land-use/work authority, courts, resource/utility or account services within the state layer; regional provisions are fact-filtered, not automatically applied to Huntington Beach.')
    select_tree(i,rules,base)

def health(i):
    rules={}
    def keep(path,why):rules[path]=(True,why)
    base='Clinical treatment, health-insurance administration, unrelated product/industry operations or public funding without a residential work/account function; conditional residential institutions and premises protections retained separately.'
    for part in ['0.5','1','2','3']:
        keep(p(division='1',part=part),'Environmental/public-health authority and applicable administrative provisions for premises health and safety.')
    for c in ['2','2.1','2.3','2.35','2.4','2.45','2.5','2.6','3','3.01','3.15','3.2','3.35','3.4','3.5','3.6','3.62','3.65','3.9','3.93','3.95','4.9','8.5','8.6','10','12','13','15']:
        keep(p(division='2',chapter=c),'Conditional residential care/continuing-care occupancy and account obligations, home-care access, or family-day-care premises rights; retain full scope and applicable protections.')
    for d in ['1.5','2.1','2.8','3','5','6','10.5','10.7','11','12','12.5','13','24','25.5','26','28','31','32','37','37.5','45','101','102','105','118','119','119.1']:
        keep(p(division=d),'Residential safety, access/occupancy, remediation, permitted work, housing/program conditions or protected-household treatment; mixed units retained for section review.')
    for c in ['1','2','3','3.7','4','5']:
        keep(p(division='7',part='1',chapter=c),'Death at premises, custody/removal authority and unclaimed remains affect lawful turnover; retain definitions, permits and duties without importing cemetery operations.')
    keep(p(division='7',part='2',chapter='1'),'Removal permits and consent are dependencies of lawful handling of remains at premises or discovered during work.')
    keep(p(division='7',part='2',chapter='5'),'Human-remains discoveries during physical work may trigger Native American handling/repatriation requirements.')
    for c in ['1','2','6','6.5','8','10','12','13']:
        keep(p(division='10',chapter=c),'Controlled-substance definitions, lawful use/property restrictions, seizure, drug-nuisance abatement and clandestine-lab consequences can govern premises occupancy and cleanup; clinical prescribing is excluded.')
    keep(p(division='20'),'Environmental hazards, waste, materials, remediation and fixtures directly affect safe work, responsibility and vendor commitments.')
    for c in ['1.2','1.3','1.4','1.6','2','3.5','5','12.8','13.4','13.5','13.6','13.8','14','24','25']:
        rules[p(division='20',chapter=c)]=(False,'Distinct clinical, food/animal-production or social-media business regulation; no residential premises-work/account relationship in this unit.')
    for part in ['2','3','4','5']:
        keep(p(division='103',part=part),'Injury prevention, residential smoke/exposure restrictions, older-household protections and environmental/occupational hazards affect occupancy and safe work.')
    for part in ['1','2','3','8','9','9.5','10','11','12','13','14','15']:
        keep(p(division='104',part=part),'Premises environmental health, hazardous products/radiation, excavations, pools, vectors, water, waste and residential cleanup requirements.')
    keep(p(division='112',part='1'),'Public-health powers and their general provisions; this is the Public Health division, not the separately numbered prescription-discount division.')
    select_tree(i,rules,base)
    # LegInfo contains two different Part 3 headings in Division 1. Hierarchy
    # parameters alone cannot identify which one is intended.
    for u in list(i['units_in_scope']):
        if u['unit']=='division 1 / part 3':
            if 'BINATIONAL' in u['heading']:
                i['units_in_scope'].remove(u)
                u['reason']='Binational border-health office administration, outside residential premises work/account functions.'
                u['toc_url']=LI+'codes_displaySection.xhtml?lawCode=HSC&sectionNum=475.'
                i['units_out'].append(u)
            else:
                u['unit']='division 1 / part 3 (Children environmental health; 900–901)'
                u['section_list']=[{'number':n,'heading':'','ref':'HSC '+n} for n in ['900','901']]

def penal(i):
    rules={}
    def keep(path,why):rules[path]=(True,why)
    base='Standalone criminal prosecution, prison administration, police staffing or separate weapons industry; provisions affecting residential access, property, information, protected households or remedies remain selected.'
    for t in ['1','2','7','8','9','10','11','11.5','11.6','13','14','15','16','17']:
        keep(p(part='1',title=t),'Conduct, victim/property protection and consequences affecting access, eviction, premises damage, agreements, privacy or account recovery; mixed offense titles retained with their scope.')
    for t in ['1','3','6','8','10','12']:
        keep(p(part='2',title=t),'Protective orders, victim remedies, restitution, property seizure/return and enforcement can affect residential occupancy and recovery; mixed procedural titles retained.')
    for t in ['1','5','5.3','7.5','8','10','10.6','11','13']:
        keep(p(part='4',title=t),'Premises nuisance, records, protection, domestic violence, building security, conflict resolution and environmental enforcement have residential operating connections.')
    keep(p(part='6',title='1'),'Definitions and construction for weapons found on premises and lawful handling/disposal.')
    for t in ['2','3','4']:
        keep(p(part='6',title=t),'Found/abandoned weapons require lawful possession, storage, transport, surrender and disposition; broad mixed title retained rather than assuming ordinary abandoned-property sale rules suffice.')
    rules[p(part='6',title='4',division='7')]=(False,'Manufacture of firearms is a separate industrial activity; found-property possession/transfer rules remain selected.')
    select_tree(i,rules,base)

def insurance(i):
    other_in=[u for u in i['units_in_scope'] if not u['heading'].startswith('DIVISION 2.') and u['unit']!='preliminary']
    rules={}
    for part in ['1','3','4','6','7','8']:
        rules[p(division='2',part=part)]=(True,'Property, liability/workers compensation, surety, land, home-protection and service-contract coverage can fund work or change responsibility/recovery; retain applicable conditions and remedies.')
    select_tree(i,rules,'Life, personal health, motor-club or pet-insurance operations; separate from residential property/work liability and outgoing-tenancy resolution.')
    i['units_in_scope']+=other_in

def replace_branches(i, roots, rules, reason):
    original=copy.deepcopy(i)
    select_tree(i,rules,reason)
    for field in ['units_in_scope','units_out']:
        i[field]+=[u for u in original[field] if u['unit']!='preliminary' and not any(u['heading'].startswith('DIVISION '+d+'. ') for d in roots)]

def resources(i):
    rules={}
    for a in ['2','3','4','5']:
        rules[p(division='5',chapter='1',article=a)]=(True,'Historical-property work restrictions, conditional hostel occupancy and public park-property leases can govern residential work and account obligations.')
    for c in ['1.1.5','1.2','1.3','1.4','1.7','1.75','1.76','2.6','6','6.5','7']:
        rules[p(division='5',chapter=c)]=(True,'Historic/archeological resources, discovered remains, public-property occupancy, playground safety or protected site conditions affect lawful physical work; territorial/program conditions remain fact-dependent.')
    for a in ['1','2']:
        rules[p(division='5',chapter='2',article=a)]=(True,'Local historic-property/monument authority can restrict work on residential historic resources.')
    replace_branches(i,['5'],rules,'Standalone recreation/park administration, grants, trail networks or museum operations without a residential premises-work/account function; historic/site protections are retained explicitly.')

def utilities(i):
    rules={}
    for c in ['1','2','5','6']:
        rules[p(division='9',part='1',chapter=c)]=(True,'Definitions, authority, planning and enforcement support aviation-related restrictions on premises height, hazards and land use.')
    for a in ['2.6','2.7','3.5','5']:
        rules[p(division='9',part='1',chapter='4',article=a)]=(True,'Airport-adjacent hazard/obstruction and land-use restrictions, or relocation, can affect lawful residential work and occupancy.')
    replace_branches(i,['9'],rules,'Airport/aircraft business operation, district financing and aviation activities; selected land-use, obstruction and relocation provisions supply the residential work connection.')

def credit_unions(i):
    rules={}
    for c in ['1','4','5','6','7','8','10']:
        rules[p(division='2',chapter=c)]=(True,'Savings-association definitions, customer savings/investment services and oversight can affect tenancy funds and work financing; no bank-only assumption.')
    for c in ['1','3','5','6','7','11','12']:
        rules[p(division='5',chapter=c)]=(True,'Credit-union definitions, customer accounts, loans and enforcement can govern holding/disbursing tenancy funds and financing work; no bank-only assumption.')
    replace_branches(i,['2','5'],rules,'Savings-association/credit-union formation, internal governance, merger and central-institution organization; ordinary customer-account and payment protections retained separately.')

def water(i):
    rules={}
    for part in ['1','5','6','9','10']:
        rules[p(division='14',part=part)]=(True,'Water-storage-district services, property/work authority, maintenance assessments and territorial changes can affect premises; retain the complete applicable unit.')
    for part in ['1','5','6','7','8','9']:
        rules[p(division='15',part=part)]=(True,'Reclamation-district property/work powers, physical plans, service/maintenance charges and enforcement can affect premises; conditional district status is not excluded.')
    for part in ['1','2','3','4']:
        rules[p(division='35',part=part)]=(True,'Delta geography and consistency/planning requirements can constrain physical work; retained as conditional state law, not applied to Huntington Beach by default.')
    replace_branches(i,['14','15','35'],rules,'District formation, elections and internal organization/finance unrelated to the owner service/work obligation; operative property, service and assessment units retained.')

def build():
    items=copy.deepcopy(json.loads((HERE/'baseline.json').read_text()))
    preliminary={x['instrument']:x for x in json.loads((HERE/'preliminary_units.json').read_text())}
    for i in items:
        code=i['id'].split(':')[1]
        # Concrete hierarchy URLs replace code-root indexes for existing numbered units.
        if code!='CIV':
            for u in i['units_in_scope']+i['units_out']:
                m=re.match(r'(DIVISION|TITLE|PART) ([0-9A-Za-z.]+)',u['heading'])
                if m:u['toc_url']=url(code,[(m[1].lower(),m[2].rstrip('.'))])
                elif code=='CONS' and u['heading'].startswith('ARTICLE '):
                    a=re.match(r'ARTICLE ([IVXLCDM]+(?: [A-D])?)\b',u['heading'])[1];u['toc_url']=url(code,[('article',a)])
        if code=='CIV':civil(i)
        if code=='CONS':constitution(i)
        if code=='EDC':education(i)
        if code=='RTC':revenue(i)
        if code=='BPC':business(i)
        if code=='GOV':government(i)
        if code=='HSC':health(i)
        if code=='PEN':penal(i)
        if code=='INS':insurance(i)
        if code=='PRC':resources(i)
        if code=='PUC':utilities(i)
        if code=='FIN':credit_unions(i)
        if code=='WAT':water(i)
        if code in ['WAT','VEH']:
            restore={'WAT':{'3':'Qualifying dams/reservoirs on or affecting residential premises can impose physical-work, inspection and safety duties; the structural thresholds decide applicability.', '19':'Levee-district powers and premises obligations are conditional sources for flood-related work and charges; district finance alone does not justify excluding the entire mixed division.'}, 'VEH':{'14':'Removal and transport of explosive hazards discovered during turnover must respect the applicable transport regime.', '14.5':'Radioactive-material removal/transport can be incident to remediation; retain the short specialized transport unit with other hazard controls.'}}[code]
            for u in list(i['units_out']):
                m=re.match(r'DIVISION ([0-9.]+)\. ',u['heading'])
                if m and m[1] in restore:
                    i['units_out'].remove(u);u['reason']=restore[m[1]];i['units_in_scope'].append(u)
        if code=='PROB':
            for u in list(i['units_out']):
                if u['heading'].startswith('DIVISION 4.7.'):
                    i['units_out'].remove(u)
                    u['reason']='Health-care decision authority includes selecting/discharging institutions (4617); relevant to conditional residential care transfers and who may direct them. Clinical decisions do not become ordinary residential functions.'
                    u['scope_evidence']='j1/lanes/codes/sources/prob-health-decision.txt'
                    i['units_in_scope'].append(u)
        if code in ['CONS','CIV','BPC','GOV','HSC','LAB','PCC','PRC','FAC','FGC','PUC','WAT','SHC','EDC','INS','PEN','HNC','WIC']:
            i['functions']=list(dict.fromkeys(i['functions']+['work_standards']))
        if code in ['CONS','CIV','BPC','GOV','LAB','PCC','COM','INS','EDC']:
            i['functions']=list(dict.fromkeys(i['functions']+['provider_contracts']))
        if i['id'] in preliminary:
            prep=preliminary[i['id']]
            i['units_in_scope']=[dict(u,source_capture=prep['source_capture']) for u in prep['with_units']]+[u for u in i['units_in_scope'] if u['unit']!='preliminary']
    (HERE/'replacement_instruments.json').write_text(json.dumps(items,indent=2,ensure_ascii=False)+'\n')
    print('Wrote replacement_instruments.json; J1 integration and substantive acceptance remain with coordinator.')

if __name__=='__main__':build()
