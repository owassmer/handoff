"""Named program documents and temporal instruments identified in the J1 source review."""
from build_register import instrument,HERE
import re

def supplement(items):
    def add(*a,**k):
        x=instrument(*a,**k);items.append(x);return x
    def get(ident):return next(x for x in items if x['id']==ident)
    for ident,name,url,units,fn in [
      ('24CFR236','HUD rental housing mortgage interest reduction','https://www.ecfr.gov/current/title-24/subtitle-B/chapter-II/subchapter-B/part-236',['Complete Part 236, all subparts and appendices'],['housing_assistance','rent_regulation','early_termination']),
      ('24CFR574','Housing Opportunities for Persons With AIDS','https://www.ecfr.gov/current/title-24/subtitle-B/chapter-V/subchapter-C/part-574',['Complete Part 574, all subparts and appendices'],['housing_assistance','rent_regulation','preconditions']),
      ('15USC9058','CARES Act covered-property eviction protections','https://www.govinfo.gov/content/pkg/PLAW-116publ136/pdf/PLAW-116publ136.pdf',['Section 4024, complete section and defined scope'],['housing_assistance','early_termination','courts_procedure']),
      ('15USC-FTC','Federal Trade Commission Act','https://www.law.cornell.edu/uscode/text/15/chapter-2/subchapter-I',['Chapter 2, Subchapter I, all sections and notes'],['consumer_protection','data_security','communications']),
      ('42USC82','Solid Waste Disposal Act','https://www.law.cornell.edu/uscode/text/42/chapter-82',['Chapter 82, all subchapters and notes'],['preconditions']),
      ('42USC85','Clean Air Act','https://www.law.cornell.edu/uscode/text/42/chapter-85',['Chapter 85, all subchapters and notes'],['preconditions']),
      ('33USC26','Federal Water Pollution Control Act','https://www.law.cornell.edu/uscode/text/33/chapter-26',['Chapter 26, all subchapters and notes'],['preconditions']),
      ('40CFR82','Protection of Stratospheric Ozone','https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-82',['Part 82, all subparts and appendices'],['preconditions'])]:
        if any(i['id']=='US:'+ident for i in items):continue
        x=add('US',ident,name,'regulation' if 'CFR' in ident else 'statute',fn,url,units)
        x['selection_reason']='Program coverage or physical-work authority: read complete mixed unit to preserve definitions, exemptions, duties and remedies.'
        if 'law.cornell.edu/uscode' in url:
            x['toc_mirror_url']=url
            x['text_source']='Office of the Law Revision Counsel USLM or GovInfo official US Code, with enacted amendments; LII is the browse index.'
    # Replace the draft chapter-number list with the actually observed Title 28 TOC.
    x=get('US:28USC');x['units_in_scope']=[]
    for roman,name in [('I','Organization of courts'),('II','Department of Justice'),('III','Court officers and employees'),('IV','Jurisdiction and venue'),('V','Procedure'),('VI','Particular proceedings')]:
        x['units_in_scope'].append({'unit':'Part '+roman,'heading':name,'toc_url':'https://www.law.cornell.edu/uscode/text/28/'+roman,'reason':'Civil and bankruptcy jurisdiction, representation, process and remedies; mixed units retained for section review.'})
    x['toc_mirror_url']='https://www.law.cornell.edu/uscode/text/28'
    x['source_capture']='j1/sources/usc28-toc.txt'
    for i in items:
        if i['id']=='US:26USC6050W':
            i['units_in_scope']=[]
            i['units_out']=[{'unit':'26 USC 6050W','reason':'Duplicate acquisition: included within the existing federal information-reporting instrument; retain this pointer for payment-settlement reporting.'}]
    # Actual OCHA document links, rather than the document-directory page.
    links={
      'OCHA-PHA2026':'https://ochousing.org/sites/ocha/files/2026-04/Annual%20PHA%20Plan%20FY2026.pdf',
      'OCHA-PHA2025-29':'https://www.ochousing.org/sites/ocha/files/2025-07/Accepted%20-%20Orange%20County%20Housing%20Authority%205-Year%20PHA%20Plan%20for%20FY%202025-2029_.pdf',
      'OCHA-VAWA':'https://www.ochousing.org/sites/ocha/files/2022-09/9-21-22%20VAWA%20PIH%20Notices.pdf',
      'OCHA-PAY2026':'https://housingauthority.oc.gov/sites/ocha/files/2025-10/2025-2026%20Payment%20Standard%20Public.pdf',
      'OCHA-UTILITY2026':'https://www.ochousing.org/sites/ocha/files/2025-10/2026%20Utility%20Allowance%20Schedule%20-%20Public%20Use.pdf',
      'OCHA-INCOME2026':'https://www.ochousing.org/sites/ocha/files/2026-05/2026%20HUD%20Income%20Limits%20-%20Public.pdf',
      'OCHA-FSS':'https://housingauthority.oc.gov/sites/ocha/files/import/data/files/68805.pdf'}
    for ident,url in links.items():
        x=get('CA-OC:'+ident);x['toc_source_url']=url;x['source_capture']='j1/sources/o-cha-files.txt'
        for u in x['units_in_scope']:u['toc_url']=url
    add('CA-OC','OCHA-TRANSFER','OCHA Emergency Transfer Plan','agency rule',['housing_assistance','anti_discrimination','early_termination'],'https://housingauthority.oc.gov/sites/ocha/files/2022-12/OCHA%20Emergency%20Transfer%20Plan%206-2017.pdf',['Complete plan and appendices'])
    for ident,name,url,chapters,fn in [
      ('HUD4350.3','HUD 4350.3 REV-1: Occupancy Requirements of Subsidized Multifamily Housing Programs','https://www.hud.gov/hudclips/handbooks/housing-4350-3',['Chapter 1 Introduction','Chapter 2 Civil Rights and Nondiscrimination','Chapter 3 Eligibility for Assistance and Occupancy','Chapter 4 Waiting List and Tenant Selection','Chapter 5 Determining Income and Calculating Rent','Chapter 6 Lease Requirements and Leasing Activities','Chapter 7 Recertification, Unit Transfers, and Gross Rent Changes','Chapter 8 Termination','Chapter 9 Enterprise Income Verification','Appendices, exhibits and change transmittals'],['housing_assistance','deposit','rent_regulation','early_termination','payments','anti_discrimination']),
      ('HUD-NSPIRE','NSPIRE final rule, standards and implementation notices','https://www.hud.gov/reac/nspire-notices',['Final rule FR-6086-F-03','Inspection standards FR-6086-N-05','Scoring notice FR-6086-N-06 and January 17 2025 correction','Administrative notice PIH 2023-16/H 2023-07','HCV implementation notice PIH 2024-26 REV-1','Compliance extension FR-6086-N-12','Affirmative-requirement scoring extension PIH 2025-27','Superseded transition notices FR-6086-N-07, N-08, N-09 and PIH 2024-39/H 2024-11'],['housing_assistance','preconditions','landlord_tenant']),
      ('HUD-HOTMA','HOTMA implementation and transition notices','https://www.hud.gov/hud-partners/multifamily-hotma',['Final rule 88 FR 9600','Joint implementation notice H 2023-10/PIH 2023-27','H 2024-04','H 2025-03','H 2025-07'],['housing_assistance','rent_regulation','payments'])]:
        x=add('US',ident,name,'agency rule',fn,url,chapters)
        x['legal_use']='Read with enabling statute/regulation and applicable program agreement; guidance does not independently override a statute or regulation.'
    get('US:HUD-NSPIRE')['temporal_note']='FR-6086-N-12 sets HCV/PBV/Mod Rehab compliance for 2027-02-01. PIH 2025-27 sets public/multifamily affirmative-defect scoring for 2026-10-01. Preserve separate program clocks.'
    get('US:HUD-HOTMA')['temporal_note']='H 2025-07 extends multifamily full compliance to 2027-01-01; early adoption remains a distinct configuration. Read PIH program implementation separately.'
    x=add('US','RULES-2026-12','Adopted federal rules and forms amendments for December 1 2026','court rule',['courts_procedure'],'https://www.uscourts.gov/forms-rules/pending-rules-and-forms-amendments',['Appellate Form 4','Bankruptcy Rules 1007, 3018, 5009, 7043, 9006, 9014, 9017','Evidence Rule 801','Official Forms 101 and 106C'],note='Acquire promulgation orders and amended text with committee notes. Separate December 2026 amendments from later proposals.')
    x['effective_from']='2026-12-01';x['source_capture']='j1/sources/pending-rules-tail.txt'
    x['units_out']=[{'unit':'Proposed December 2027/2028 rule amendments','reason':'Proposal/committee-stage materials, not adopted operative rules as of this intake. The separately adopted December 2026 forms remain included.'}]
    add('US','SCOTUS-RULES','Supreme Court rules','court rule',['courts_procedure'],'https://www.supremecourt.gov/filingandrules/rules_guidance.aspx',['Complete rules, appendices and 2026 revision orders'])
    for ident,name,url,units,fn in [
      ('CTCAC-COMPLIANCE','CTCAC compliance manual, operative notices and schedules','https://website-prod.treasurer.ca.gov/ctcac/compliance',['2026 compliance manual, all chapters and appendices','2026 compliance policy memoranda','2026 income and rent limit schedules','Utility allowance and rent-increase policies','HOTMA implementation and veteran income notices'],['housing_assistance','rent_regulation','payments','preconditions']),
      ('HCD-PORTFOLIO','HCD rental housing portfolio rules and administrative notices','https://www.hcd.ca.gov/funding/reporting-and-compliance-loan',['Uniform Multifamily Regulations and applicable award-vintage program guidelines','Rent increase limit notice 25-06 as amended June 4 2026','2026 rent adjustment notice 25-05','Wildfire displaced-household priority notice 25-03 as amended June 10 2026','NSPIRE implementation notice January 10 2025','Asset Management and Compliance notice 26-01','Operating budget, reserve, management and reporting requirements incorporated by program agreements'],['housing_assistance','rent_regulation','preconditions','payments']),
      ('CALHFA-ASSET','CalHFA multifamily asset management requirements','https://www.calhfa.ca.gov/multifamily/asset/forms/',['Asset management handbook and amendments','Combined HCD/CalHFA budget and reserve-disbursement requirements','Management agreement and tenant-selection plan requirements','MHSA/SNHP program requirements','Rent limit, operating subsidy and wildfire-priority notices'],['housing_assistance','rent_regulation','preconditions','payments']),
      ('SCO-HOLDER','SCO unclaimed property holder reporting instructions','https://sco.ca.gov/Files-UPD/guide_rptg_holderhandbook2.pdf',['Complete holder handbook, reporting specifications and due-diligence instructions'],['unclaimed_property','payments']),
      ('WATER-CGP2022','Construction General Permit Order 2022-0057-DWQ','agency-placeholder',['Complete order and all attachments'],['preconditions'])]:
        if ident=='WATER-CGP2022':url='https://www.waterboards.ca.gov/water_issues/programs/stormwater/construction.html'
        x=add('CA',ident,name,'agency rule',fn,url,units)
        x['application']='Program/permit and applicable version are determined from the governing authority and operating facts; no program is inferred from the demonstration property.'
    url='https://www.waterboards.ca.gov/santaana/water_issues/programs/stormwater/regional_ms4_permit.html'
    old=add('CA-OC','MS4-2009','Orange County MS4 Order R8-2009-0030 as amended by R8-2010-0062','agency rule',['preconditions'],url,['Complete order, attachments, Model WQMP and Technical Guidance Document'])
    old['text_source_url']='https://www.waterboards.ca.gov/santaana/board_decisions/adopted_orders/orders/2009/09_030_oc_ms4_as_amended_by_10_062.pdf'
    new=add('CA-OC','MS4-2026','Santa Ana Regional MS4 Order R8-2026-0034','agency rule',['preconditions'],url,['Complete order, all attachments and appendices'])
    new['adopted_on']='2026-09-11';new['effective_from']='2027-03-10'
    new['text_source_url']='https://www.waterboards.ca.gov/santaana/board_decisions/adopted_orders/orders/2026/r8-2026-0034_signed.pdf'
    for x in [old,new]:
        x['source_capture']='j1/sources/current-ms4-and-history.txt'
        x['application']='Regional permit binds the named permittees; operator duties must be traced through applicable local implementation and site/permit conditions.'
        x['transition']='Prior permit remains effective until 2027-03-10, then retained for prior violations; existing post-construction requirements continue under the separate application/technical-guidance transition stated in the new order.'
    add('CA-HB','ORD4350','Huntington Beach Ordinance 4350','ordinance',['preconditions','fees','abandoned_property'],'https://ecode360.com/HU4937/laws/LF2803862.pdf',['Complete ordinance, all amending and commencement sections'],note='Uncodified amendment to selected Title 10; parking/access/towing dependencies require section review.')
    x=add('CA-HB','ORD4351','Huntington Beach Ordinance 4351','ordinance',[],'https://ecode360.com/HU4937/laws/LF2803863.pdf',[])
    x['units_out']=[{'unit':'Complete ordinance','reason':'Amends public beach/park operations in Chapter 13.08; standalone recreation management is outside residential turn and account decisions.'}]
    x=add('CA','ZONE0-2026','Board of Forestry Zone 0 rule package, August 2026','regulatory action',['preconditions'],'https://bof.fire.ca.gov/projects-and-programs/defensible-space-zones-0-1-and-2',['August 19 board decision and approved rule package','September 2026 guidance and OAL submission 2026-0828-03'])
    x['legal_status']='Board package proceeding through OAL review; the current Board page says final review/publication is not complete. No operative date is asserted from the proposed schedule.'
    x['source_capture']='j1/sources/fire-zone-text.txt'
