import csv, json
from collections import Counter
from pathlib import Path

p=Path(__file__).parent
records=json.loads((p/'competitors.json').read_text())
columns=list(records[0])
extra=[
['APM Help','Managed accounting + software consulting','Residential property managers','accounting;payments;compliance',
'Trust bookkeeping with AP/AR and daily reconciliations; corporate books, cleanup, consulting and 1099 services.',
'Vendor service/pricing documentation; audit-success claims unverified',
'Cleanup depends on book condition; recurring pricing scales with unit count; numeric quote not published on reviewed pages.',
'Teams specialize in AppFolio, Buildium, Rentvine and Propertyware; corporate QuickBooks Online.',
'Payment-release responsibilities and guarantee exclusions need contract verification.',
'Competes on completed accounting work; future AI savings must beat outsourced service economics.',
'https://www.apmhelp.com/|https://www.apmhelp.com/services','Undated live pages'],
['OJO Bookkeeping','Managed property bookkeeping','Residential; commercial; HOA managers','accounting;payments;compliance',
'Dedicated bookkeeping, supervision and audit support; trust/management books and three-way reconciliation cleanup.',
'Vendor service/pricing documentation; savings and quality unverified',
'$34/hour ongoing; $45/hour cleanup/software setup; cancel-anytime and 30-day guarantee advertised.',
'AppFolio, Buildium, Rentvine, QuickBooks and Xero expertise; customer permissions require confirmation.',
'Hours needed, responsibility split and guarantee terms unverified; this is OJO Bookkeeping, not unrelated OJO businesses.',
'Visible outsourced labor rate gives a real comparator for accounting automation ROI.',
'https://ojobookkeeping.com/','Undated live page'],
['Second Nature','Managed resident services + onboarding','Rental property managers','move_in;resident_service;maintenance;compliance',
'Resident onboarding and configurable benefits; filter delivery, credit building, insurance and identity protection; Maestro workflow personalization.',
'Vendor product/service documentation; savings and resident outcomes unverified',
'No universal numeric wholesale or resident package price verified; packages are configurable.',
'Managed setup of leases, ledgers and benefits; exact external API rights not verified.',
'Resident fee, choice, exclusions and actual use must be assessed; manager revenue alone does not establish resident value.',
'Can replace administrative work and prevent some requests; competes through service bundling, not standalone AI.',
'https://www.secondnature.com/|https://www.secondnature.com/benefits','Undated live pages'],
['Mezo (now Property Meld)','Acquired maintenance AI lineage','Residential maintenance','maintenance',
'MAX intake, triage and mitigation technology acquired by Property Meld; now presented within Meld/MAX On-Call.',
'Acquirer announcement and current integration page; not an additional independent competitor',
'No separate current Mezo price; refer to current Property Meld packages.',
'Property Meld product integration; no separate new-vendor access established.',
'Acquired January 2025; legacy Mezo case studies are not independent current competition or verified outcomes.',
'Count as lineage showing specialist acquisition by an operating platform, not an extra independent market participant.',
'https://propertymeld.com/property-meld-mezo/|https://propertymeld.com/blog/property-meld-acquires-mezo-advancing-ai-driven-property-maintenance-operations/','2025-01-14 acquisition; current product page undated'],
['Conservice','Managed utility operations + software','Multifamily; commercial; SFR; student; manufactured; military','utilities;accounting;payments;compliance;procurement',
'Utility invoice administration, expense recovery, meters, analysis, contracts, energy procurement and sustainability services.',
'Vendor service documentation; savings and guarantee performance unverified',
'Numeric price not published on reviewed pages; quote needed.',
'PMS integrations and reporting portal advertised; exact interfaces not verified.',
'Reduced consumption/cost and shifting bills to residents are different outcomes; validate authorized allocation and service contract.',
'Utility management has a substantive people-plus-software competitor, not just PMS billing modules.',
'https://www.conservice.com/|https://www.conservice.com/solutions/expense-management/|https://www.conservice.com/solutions/expense-recovery/','Undated live pages'],
['AvidXchange','AP automation + managed payment infrastructure','Real estate managers; community associations; other industries','procurement;accounting;payments',
'Purchase orders, invoice processing, approvals, two/three-way matching and supplier payments; embedded AP infrastructure offered to ERPs.',
'Vendor product/integration documentation; performance unverified',
'Numeric quote not published on reviewed pages.',
'API or file integrations depending on accounting system; exchanges invoices, GL codes, suppliers, receipts, payments and POs.',
'Confirm actual integration method and latency; approval controls and fee allocation vary by agreement.',
'An invoice agent competes with mature workflow/payment infrastructure and existing supplier networks.',
'https://www.avidxchange.com/|https://www.avidxchange.com/solutions/avidsuite-for-real-estate/','Undated live pages'],
['Vendoroo','Maintenance AI + managed human support','Residential property managers; own-vendor and onsite-tech models','resident_service;maintenance;procurement;accounting',
'AI intake/dispatch/scheduling/invoice collection; Command adds human vendor failover and owner communication/approvals.',
'Vendor pricing/product and PMS-partner documentation; performance unverified',
'Coordinators/vendors plans: Engage $3/unit/month, Direct $6; each $400 minimum with annual billing; Command custom.',
'Own vendors supported; Rent Manager partner listing confirms integration offering; exact write guarantees not tested.',
'Smart estimates marked coming soon; marketed guarantees require contract review; full turn-date accountability not established.',
'Direct comparator for AI service using customer vendors and human exception support; must enter buy-versus-build test.',
'https://www.vendoroo.ai/|https://www.vendoroo.ai/pricing-vendors|https://www.rentmanager.com/integrations/vendoroo/','Undated live pages'],
['Proper','AI-assisted managed property accounting','Residential and commercial property/asset managers','accounting;payments;move_in;move_out;compliance',
'Staffed property accounting with AI; AP/AR, trust reconciliation, move-in/out accounting and process/control setup.',
'Vendor service documentation; cost-savings claims unverified',
'Quote; service page references residential units, commercial square footage and asset class; no numeric rate.',
'Works in property accounting systems; detailed permissions and API arrangements unverified.',
'AI-enabled staffing claim does not establish automation share, margins or error rates.',
'AI plus an accountable service team is already an operating accounting business model.',
'https://www.proper.ai/|https://www.proper.ai/how-it-works','Undated live pages'],
]
by_name={x['provider']:x for x in records}
for row in extra:by_name[row[0]]=dict(zip(columns,row+['2026-09-15']))
records=list(by_name.values())
assert len(records)==38
for record in records:
 if record['provider'] in {'Yardi','RealPage','Rent Manager','Zego'} and 'utilities' not in record['lifecycle_coverage'].split(';'):
  record['lifecycle_coverage'] += ';utilities'
(p/'competitors.json').write_text(json.dumps(records,indent=2)+'\n')
with (p/'competitors.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(records)
audit=list(csv.DictReader((p/'market_source_audit.csv').open()))
urls={x['url'] for x in audit}
for row in extra:
 for url in row[10].split('|'):
  if url not in urls:
   audit.append({'url':url,'provider':row[0],'access_result':'Opened successfully with web tool; public page text available','checked_date':'2026-09-15','evidence_limit':'Vendor source; advertised offering or acquisition status, not independently tested performance'})
   urls.add(url)
with (p/'market_source_audit.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=audit[0]);w.writeheader();w.writerows(audit)
current=[x for x in records if not x['provider'].startswith('Mezo')]
counts=Counter()
for r in current:counts.update(r['lifecycle_coverage'].split(';'))
(p/'market_coverage_counts.json').write_text(json.dumps({'entries':38,'current_provider_entries':37,'excluded_from_counts':'Mezo acquired lineage','counts':dict(counts.most_common())},indent=2)+'\n')
print(json.dumps({'entries':len(records),'source_pages':len(audit),'current_provider_entries':len(current),'counts':dict(counts.most_common())}))
