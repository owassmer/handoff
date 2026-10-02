"""J1 explicit source selection only; does not fetch or change canonical registers."""
import json
from pathlib import Path

OUT = Path(__file__).parent
def unit(number, heading, ref, version, reason):
    return {'unit':number,'heading':heading,'toc_url':ref,'source_unit_kind':'document','section_list':[{'number':number,'heading':heading,'ref':ref,'source_unit_kind':'document'}],'version':version,'reason':reason}

sco = [
 ('NAUPA-II','NAUPA II codes and dormancy periods','https://www.sco.ca.gov/Files-UPD/upd_naupa_II_codes_dormancy_periods.pdf','Current linked edition; printed revision not established'),
 ('DUE-DILIGENCE','Due diligence instructions','https://sco.ca.gov/Files-UPD/upd_duediligence.pdf','Current linked edition; undated'),
 ('CYCLE-2026','General holders property reporting cycle 2026','https://sco.ca.gov/Files-UPD/upd_general_holders_prc_2026.pdf','2026'),
 ('REMIT','Remitting unclaimed property to the State','https://sco.ca.gov/Files-UPD/upd_remitting_property_factsheet.pdf','Rev. 4/2026'),
 ('UFS-1','Universal Holder Face Sheet and instructions','https://www.sco.ca.gov/Files-UPD/form_rptg_ufs-1.pdf','Rev. 04/2024'),
 ('HCR-1','Holder Claim for Reimbursement and instructions','https://www.sco.ca.gov/Files-UPD/form_rptg_hcr-1.pdf','Current linked edition; revision not established'),
 ('DUE-DILIGENCE-MODEL','Sample due diligence letter','https://sco.ca.gov/Files-UPD/outreach_rptg_notice_duediligencesample.pdf','Current linked model; undated'),
]
records=[{'id':'CA:SCO-HOLDER','aliases':['CA:SCO-UNCLAIMED'],'operation':'replace_units','name':'SCO holder reporting publications for landlord-held outgoing credits','level':'agency rule','instrument_kind':'agency reporting instructions and forms','functions':['unclaimed_property','payments'],'adapter':'generic','toc_source_url':'https://www.sco.ca.gov/upd_how_to_report.html','units_in_scope':[unit(n,h,u,v,'Reporting and return of abandoned landlord-held credits; includes security deposits, overpayments, refunds and credit balances. Classify each credit under the statute and applicable NAUPA code; do not classify every credit as security deposit.') for n,h,u,v in sco],'reason':'Legacy guide_rptg_holderhandbook2.pdf returns not-found HTML. Replace generic handbook target with current individually named publications. These implement rather than replace CCP unclaimed-property law and Title 2 regulations. Securities and safe-deposit details are not default landlord-credit requirements.','acquisition':{'text_adapter':'generic','enumeration':'Explicit whole-document references','status':'explicit_targets_verified'}}]
waters=[
 ('CA:WATER-CGP2022','Construction General Permit Order 2022-0057-DWQ','https://www.waterboards.ca.gov/board_decisions/adopted_orders/water_quality/2022/wqo_2022-0057-dwq.pdf','Adopted 2022-09-08; effective 2023-09-01','Complete 471-page order, fact sheet and attachments. Conditional construction/common-plan threshold; retain for larger residential work.'),
 ('CA-OC:MS4-2009','Orange County MS4 Order R8-2009-0030 as amended by R8-2010-0062','https://www.waterboards.ca.gov/santaana/board_decisions/adopted_orders/orders/2009/09_030_oc_ms4_as_amended_by_10_062.pdf','2009 order as amended 2010; operative until 2027-03-10 transition','Retain complete 93-page operative permit. Supersession does not erase past-violation enforcement or transitional project requirements.'),
 ('CA-OC:MS4-2026','Santa Ana Regional MS4 Order R8-2026-0034','https://www.waterboards.ca.gov/santaana/board_decisions/adopted_orders/orders/2026/r8-2026-0034_signed.pdf','Adopted 2026-09-11; effective 2027-03-10','Retain adopted future complete 394-page signed order and attachments. Preserve VIII.C.4–5 WQMP/TGD transition tied to future Executive Officer approval, not an invented automatic 2029 replacement date.'),
]
for id,name,url,version,reason in waters:
 records.append({'id':id,'operation':'replace_units','name':name,'level':'regulation','instrument_kind':'water quality control board order','functions':['work_standards'],'adapter':'generic','toc_source_url':url,'units_in_scope':[unit('complete',name,url,version,reason)],'reason':reason,'acquisition':{'text_adapter':'generic','enumeration':'Explicit complete PDF with attachments','status':'explicit_targets_verified'}})
records[2]['units_in_scope'].append(unit('MODEL-WQMP-2011','Model Water Quality Management Plan, North Orange County','https://pwer.oc.gov/sites/ocpwocer/files/2026-04/Model%20WQMP%20May%202011.pdf','May 19, 2011; April 2026 URL is upload date','Retain actual 2011 Model WQMP during regional permit transition.'))
records[2]['remaining_dependencies']=[{'target':'North Orange County Technical Guidance Document, December 2013','source':'https://pwer.oc.gov/service-areas/oc-environmental-resources/regional-stormwater-program/water-quality-requirements','cause':'Official link returned internal fetch error on repeated attempts; precise downloadable PDF remains to recover. Do not treat this directory as executable.'}]
for record in records:
 record['jurisdiction'] = record['id'].split(':')[0]
 record['units_out'] = []
payload={'as_of':'2026-10-01','stage':'J1 selection; no J2 harvesting','replacements':records,'remaining_families':[{'family':'CCR retained divisions','decision':'Retain selected division scope pending actual leaf enumeration','cause':'Existing generic adapter does not recursively traverse Westlaw/Cornell division indexes. Currentness decisions in proposal.json do not close section enumeration.'},{'family':'SCAQMD','decision':'Retain selected regulation scope; explicit rule PDFs handled separately','cause':'Regulation TOCs alone are not executable generic targets.'}]}
(OUT/'existing-agency-targets.json').write_text(json.dumps(payload,indent=2)+'\n')
