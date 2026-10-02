#!/usr/bin/env python3
"""Reproduce descriptive RHFS tabulations and explicitly hypothetical economics.

Standard-library only. Run from any directory. No credentials required. The raw
2024 RHFS CSV is retained alongside this script; --download refreshes it.
No causal savings estimate is inferred from the survey. No missing value is zero.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
RAW_URL = "https://www2.census.gov/programs-surveys/rhfs/data/public-use-files/2024/rhfspuf2024.csv"
METHOD_URL = "https://www.census.gov/programs-surveys/rhfs/technical-documentation/methodology.html"
SIZE_NAMES = {0:"1 unit",1:"2–4 units",2:"5–24 units",3:"25–49 units",4:"50+ units"}
MANAGER_NAMES = {-9:"Not reported",1:"Owner or unpaid agent",2:"Owner-employed manager",3:"Management company",4:"Other"}

def weighted_quantile(records, val, q=.5, unit_weight=False):
    pairs=sorted((val(r),r['WEIGHT']*(r['NUMUNITS_R'] if unit_weight else 1)) for r in records)
    threshold=q*sum(w for _,w in pairs)
    acc=0
    for v,w in pairs:
        acc+=w
        if acc>=threshold:return v
    return None

def weighted_sum(records, units=False, weight='WEIGHT'):
    return sum(r[weight]*(r['NUMUNITS_R'] if units else 1) for r in records)

def profile(records, universe):
    p=weighted_sum(records);u=weighted_sum(records,True)
    return {'records':len(records),'properties':p,'units_puf':u,
            'share_properties':p/weighted_sum(universe),
            'share_units_puf':u/weighted_sum(universe,True)}

def scenario(units=1000,items_per_unit=.30,eligible_fraction=.70,pm_minutes_saved=20,
             pm_hourly=45,cash_realization=.50,owner_cost_saved=20,owner_collected_revenue=10,
             pm_fee=.08,ownership_share=0,monthly_price=1000,item_price=5,
             routine_minutes=3,exception_fraction=.15,exception_extra_minutes=20,
             provider_hourly=35,model_comms_per_item=.50,support_monthly=400,
             implementation_hours=20,implementation_hourly=50,amort_months=12):
    n=units*items_per_unit*eligible_fraction
    capacity=n*pm_minutes_saved/60*pm_hourly
    cash=capacity*cash_realization
    owner_gross=n*(owner_cost_saved+owner_collected_revenue)
    marginal_pm_fee=n*owner_collected_revenue*pm_fee
    owner_after_pm=owner_gross-marginal_pm_fee
    buyer_value=cash+marginal_pm_fee+ownership_share*owner_after_pm
    revenue=monthly_price+n*item_price
    human_mins=routine_minutes+exception_fraction*exception_extra_minutes
    variable_cost=human_mins/60*provider_hourly+model_comms_per_item
    impl=implementation_hours*implementation_hourly/amort_months
    cost=n*variable_cost+support_monthly+impl
    pm_value_per_item=(pm_minutes_saved/60*pm_hourly*cash_realization
                       +owner_collected_revenue*pm_fee
                       +ownership_share*(owner_cost_saved+owner_collected_revenue*(1-pm_fee)))
    return {'eligible_items_month':n,'pm_capacity_value_month':capacity,
        'pm_realized_labor_value_month':cash,'owner_gross_value_month':owner_gross,
        'pm_incremental_fee_month':marginal_pm_fee,'owner_after_pm_fee_month':owner_after_pm,
        'buyer_value_month':buyer_value,'provider_revenue_month':revenue,
        'buyer_net_value_month':buyer_value-revenue,'buyer_benefit_cost_ratio':buyer_value/revenue,
        'provider_human_minutes_per_item':human_mins,'provider_variable_cost_per_item':variable_cost,
        'provider_cost_month':cost,'provider_contribution_month':revenue-cost,
        'provider_contribution_margin':(revenue-cost)/revenue,
        'buyer_break_even_eligible_items_month':monthly_price/(pm_value_per_item-item_price) if pm_value_per_item>item_price else None,
        'provider_max_human_minutes_per_item_for_60pct_margin':
          ((.4*revenue-support_monthly-impl)/n-model_comms_per_item)/provider_hourly*60}

def main():
    p=argparse.ArgumentParser();p.add_argument('--download',action='store_true');args=p.parse_args()
    raw=ROOT/'rhfspuf2024.csv'
    if args.download or not raw.exists():raw.write_bytes(urlopen(RAW_URL,timeout=45).read())
    rows=[{k:float(v) for k,v in r.items()} for r in csv.DictReader(raw.open())]
    assert len(rows)==4425, 'Unexpected revision; inspect methodology before trusting counts.'
    assert all(r['WEIGHT']>0 and r['NUMUNITS_R']>=1 for r in rows)
    assert all(abs(r['WEIGHT']-r['REPWGT0'])<.00001 for r in rows)
    result={'raw_url':RAW_URL,'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),
        'retrieved':'2026-09-15','records':len(rows),'methodology':METHOD_URL,
        'statistical_status':'Descriptive survey-weighted point estimates; no confidence intervals. Not Census-endorsed estimates.',
        'unit_note':'NUMUNITS_R has disclosure-modified components. PUF unit total differs from pre-disclosure unit controls. Both are retained.',
        'overall':profile(rows,rows),'size':{},'management':{},'management_within_size':{},'expenses':{},'scenarios':{}}
    official_properties=[15714000,2765915,329560,73768,81331]
    official_puf_units=[15714000,7704000,4091000,2708000,19678172]
    for size,name in SIZE_NAMES.items():
        sub=[r for r in rows if r['NUMCAT_R']==size]
        result['size'][name]=profile(sub,rows)
        # Census publishes these rounded PUF verification totals; verify every stratum.
        assert round(weighted_sum(sub))==official_properties[size]
        assert round(weighted_sum(sub,True))==official_puf_units[size]
        result['management_within_size'][name]={MANAGER_NAMES[k]:profile([r for r in sub if r['MNGMNT']==k],sub) for k in MANAGER_NAMES}
    for k,name in MANAGER_NAMES.items():result['management'][name]=profile([r for r in rows if r['MNGMNT']==k],rows)
    for field in ['OPREP','OPMNG','OPINSUR','OPPAY','OPEX_R','TOTCOLL']:
        valid=[r for r in rows if r[field]>=0]
        result['expenses'][field]={
          'valid_records':len(valid),'valid_property_weight_fraction':weighted_sum(valid)/weighted_sum(rows),
          'not_reported_property_weight_fraction':weighted_sum([r for r in rows if r[field]==-9])/weighted_sum(rows),
          'not_applicable_property_weight_fraction':weighted_sum([r for r in rows if r[field]==-8])/weighted_sum(rows),
          'annual_per_unit_property_weighted_median':weighted_quantile(valid,lambda r:r[field]/r['NUMUNITS_R']),
          'annual_per_unit_unit_weighted_median':weighted_quantile(valid,lambda r:r[field]/r['NUMUNITS_R'],unit_weight=True),
          'annual_per_unit_property_weighted_mean':sum(r['WEIGHT']*r[field]/r['NUMUNITS_R'] for r in valid)/weighted_sum(valid),
          'interpretation':'Conditional on nonnegative item response; excludes not reported and not applicable. Descriptive; not savings potential.'}
    turn_inputs={'items_per_unit':.35/12,'eligible_fraction':1,'pm_minutes_saved':60,
          'owner_cost_saved':0,'owner_collected_revenue':200,'monthly_price':0,'item_price':100,
          'routine_minutes':20,'exception_fraction':.25,'exception_extra_minutes':60,
          'model_comms_per_item':2}
    result['turn_scenario_assumptions']={**turn_inputs,'units':1000,'pm_hourly':45,
          'cash_realization':.5,'pm_fee':.08,'provider_hourly':35,'support_monthly':400,
          'implementation_hours':20,'implementation_hourly':50,'amort_months':12,
          'monthly_rent':2000,'days_per_month':30,'collected_rent_days_recovered':3,
          'annual_turnover_fraction':.35,'status':'Illustrative inputs, not observed effects or recommended market pricing'}
    for name,params in [('Third-party PM',{}),('Integrated owner-operator',{'ownership_share':1}),
        ('Low cash realization',{'cash_realization':.20}),('Heavy exception tail',{'exception_fraction':.40,'exception_extra_minutes':40}),
        ('No owner savings yet proven',{'ownership_share':1,'owner_cost_saved':0,'owner_collected_revenue':0}),
        ('Turn-only PM illustrative35pct',turn_inputs),
        ('Turn-only integrated illustrative35pct',{**turn_inputs,'ownership_share':1}),
        ('Turn-only integrated no rent recovery',{**turn_inputs,'ownership_share':1,'owner_collected_revenue':0})]:
        result['scenarios'][name]=scenario(**params)
    turn=result['scenarios']['Turn-only integrated illustrative35pct']
    result['turn_price_and_effect_bounds']={
        'provider_zero_contribution_price_per_turn':turn['provider_cost_month']/turn['eligible_items_month'],
        'provider_price_per_turn_for_60pct_contribution':turn['provider_cost_month']/turn['eligible_items_month']/.4,
        'third_party_buyer_zero_net_price_per_turn':result['scenarios']['Turn-only PM illustrative35pct']['buyer_value_month']/turn['eligible_items_month'],
        'integrated_buyer_zero_net_price_per_turn':turn['buyer_value_month']/turn['eligible_items_month'],
        'integrated_collected_rent_days_for_buyer_break_even':(100-60/60*45*.5)/(2000/30),
        'third_party_collected_rent_days_for_buyer_break_even':(100-60/60*45*.5)/(2000/30*.08),
        'interpretation':'Conditional bounds from assumed value and handling costs; not market prices, budgets or proven effects.'}
    result['vacancy_example']={'assumptions':'1000 units, 40% annual turnover, 3 collected-rent days recovered per turn, $2000 monthly rent, 30-day convention, 8% PM fee',
        'owner_gross_revenue_year':1000*.4*3*2000/30,
        'pm_fee_uplift_year':1000*.4*3*2000/30*.08,
        'owner_after_pm_fee_year':1000*.4*3*2000/30*.92,
        'caution':'Only days that genuinely shift rent commencement count; earlier readiness without demand creates no collected rent.'}
    (ROOT/'economic_outputs.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
    rows_out=[]
    for size,data in result['size'].items():
        for k in ['records','properties','units_puf','share_properties','share_units_puf']:
            rows_out.append({'group':'RHFS size','category':size,'measure':k,'value':data[k],'status':'Independent descriptive calculation','period':'2024 survey; financial reference 2023','source_url':RAW_URL,'notes':result['statistical_status']})
    for name,data in result['management'].items():
        for k in ['records','properties','units_puf','share_properties','share_units_puf']:
            rows_out.append({'group':'RHFS management','category':name,'measure':k,'value':data[k],'status':'Independent descriptive calculation','period':'2024 survey; financial reference 2023','source_url':RAW_URL,'notes':result['statistical_status']})
    for name,data in result['expenses'].items():
        for k,v in data.items():
            if isinstance(v,(int,float)):rows_out.append({'group':'RHFS expenses','category':name,'measure':k,'value':v,'status':'Independent descriptive calculation','period':'2023','source_url':RAW_URL,'notes':data['interpretation']})
    anchors=[
      ('HVS','US renter-occupied units',46827000,'units','2026 Q2','https://www.census.gov/housing/hvs/files/currenthvspress.pdf','Table 3; 90% MOE 580000 units; not RHFS population'),
      ('HVS','US rental vacancy',7.3,'percent','2026 Q2','https://www.census.gov/housing/hvs/files/currenthvspress.pdf','Table 1; 90% MOE 0.2 percentage points'),
      ('HVS','Median asking rent vacant for-rent units',1531,'USD/month','2026 Q2','https://www.census.gov/housing/hvs/files/currenthvspress.pdf','Not average occupied-unit rent'),
      ('BLS','Property real estate community association manager median wage',69990,'USD/year','2025 May','https://www.bls.gov/ooh/management/property-real-estate-and-community-association-managers.htm','Broad occupation; salary excludes employer benefit load and self-employment income'),
      ('BLS','Property real estate community association manager median wage',33.65,'USD/hour','2025 May','https://www.bls.gov/ooh/management/property-real-estate-and-community-association-managers.htm','Not the wage for every task role'),
      ('BLS','Property real estate community association managers jobs',460400,'jobs','2025','https://www.bls.gov/ooh/management/property-real-estate-and-community-association-managers.htm','Includes residential commercial association managers and self employed; not number of PM firms'),
      ('INVH','Same store homes',76819,'homes','FY2025','https://www.businesswire.com/news/home/20260218809149/en/Invitation-Homes-Reports-Fourth-Quarter-and-Full-Year-2025-Results','Single company SFR portfolio; not national'),
      ('INVH','Same store annual turnover',22.8,'percent','FY2025','https://www.businesswire.com/news/home/20260218809149/en/Invitation-Homes-Reports-Fourth-Quarter-and-Full-Year-2025-Results','Annual turnover; quarterly value 5.6% must not be treated as annual'),
      ('INVH','Same store occupancy',96.8,'percent','FY2025','https://www.businesswire.com/news/home/20260218809149/en/Invitation-Homes-Reports-Fourth-Quarter-and-Full-Year-2025-Results','Same store average occupancy'),
      ('AvalonBay','Same store annualized turnover',37.2,'percent annualized','H1 2026','https://investors.avalonbay.com/sec-filings/all-sec-filings/content/0000915912-26-000018/q22026ex-992.htm','Attachment 3; annualized H1 run rate not actual annual 2026 turnover; excludes third-party-managed communities'),
      ('Buildium','Survey respondents using AI',58,'percent','2025 survey reported for 2026','https://www.buildium.com/resource/2026-property-management-industry-report/','Vendor survey; not representative population estimate or causal impact'),
      ('Buildium','Companies fully automating any process',8,'percent','2025 survey reported for 2026','https://www.buildium.com/resource/2026-property-management-industry-report/','Current adoption outcome not technical automation ceiling'),
      ('England EPLS','Direct landlords with one property',45,'percent','2024','https://www.gov.uk/government/statistics/english-private-landlord-survey-2024-main-report/english-private-landlord-survey-2024-main-report','Landlords directly registering deposits only; not whole England landlord universe'),
      ('England EPLS','Tenancies owned by direct landlords with 5+ properties',49,'percent','2024','https://www.gov.uk/government/statistics/english-private-landlord-survey-2024-main-report/english-private-landlord-survey-2024-main-report','Same direct-landlord sample limitation'),
    ]
    for group,name,value,unit,period,url,notes in anchors:
        rows_out.append({'group':group,'category':name,'measure':unit,'value':value,'status':'Published source statistic','period':period,'source_url':url,'notes':notes})
    with (ROOT/'public_data.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows_out[0]));w.writeheader();w.writerows(rows_out)
    print(json.dumps({'records':result['records'],'total':result['overall'],'scenarios':result['scenarios']},indent=2))

if __name__=='__main__':main()
