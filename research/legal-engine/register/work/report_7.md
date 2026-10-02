# Report 7: set-aside reviewer A (batch 7)

Reviewer q7. 456 sections Jev set aside as deciding nothing (NY instruments 16 NYCRR through LLC Law). Each was decided from its saved text; decisions in `register/work/decisions_7.jsonl`, chunk scripts `q7_c01.py`-`q7_c23.py`, helpers `q7_lib.py`, this report from `q7_report.py`. Report only: no rule file, walk or register file was edited.

## Counts

| decision | count |
|---|---|
| no_decision | 436 |
| excluded_regime | 10 |
| stated | 3 |
| partial | 5 |
| new_rule | 2 |
| total | 456 |

By instrument:

| instrument | sections | not no_decision |
|---|---|---|
| NY:16NYCRR | 1 | 0 |
| NY:18NYCRR | 16 | 0 |
| NY:19NYCRR | 20 | 1 |
| NY:22NYCRR | 34 | 0 |
| NY:9NYCRR | 16 | 10 |
| NY:ABP | 6 | 0 |
| NY:BCL | 16 | 3 |
| NY:CCA | 8 | 1 |
| NY:CPLR | 28 | 1 |
| NY:EPTL | 28 | 0 |
| NY:EXEC | 4 | 0 |
| NY:GBL | 166 | 1 |
| NY:GCN | 39 | 0 |
| NY:GOL | 29 | 0 |
| NY:JUD | 25 | 0 |
| NY:LLC | 20 | 3 |

## Sections decided other than no_decision (Jev's misses)

Jev scores are p_decides / chain_duty. Every section below was set aside by Jev; `stated` and `excluded_regime` sections change or route something, `partial` and `new_rule` sections carry law no rule states.

| section | heading | decision | Jev p_decides | Jev chain_duty | atoms / proposed |
|---|---|---|---|---|---|
| NY:19 NYCRR 175.21 | Supervision of salesman by broker | partial | 0 | 0.04 | NY:HANDOFF-broker-config-under-broker, NY:RPL-441-c-licence-discipline, NY:19NYCRR-175.21-broker-supervision |
| NY:9 NYCRR 2200.1 | Statutory authority | excluded_regime | 0 | 0.07 | Statutory authority of the City Rent and Eviction Regulation |
| NY:9 NYCRR 2200.5 | Amendment or revocation | excluded_regime | 0 | 0.06 | Administrator may amend the City Rent and Eviction Regulatio |
| NY:9 NYCRR 2200.6 | Filing of amendments | excluded_regime | 0 | 0.06 | Filing of amendments to the City Rent and Eviction Regulatio |
| NY:9 NYCRR 2200.7 | Separability | excluded_regime | 0.06 | 0.09 | Separability clause of the City Rent and Eviction Regulation |
| NY:9 NYCRR 2200.8 | District rent office designations and descriptions | excluded_regime | 0 | 0.08 | District rent offices under the City Rent and Eviction Regul |
| NY:9 NYCRR 2520.1 | Statutory authority | excluded_regime | 0 | 0.05 | Statutory authority of the Rent Stabilization Code; regime:  |
| NY:9 NYCRR 2520.10 | Separability | excluded_regime | 0.09 | 0.09 | Separability clause of the Rent Stabilization Code; regime:  |
| NY:9 NYCRR 2520.5 | Designations | excluded_regime | 0 | 0.08 | Designations (RSL, ETPA, DHCR, Loft Board, TPU) used in the  |
| NY:9 NYCRR 2520.7 | Effective date | excluded_regime | 0.01 | 0.09 | Effective date of the Rent Stabilization Code; regime: NYC r |
| NY:9 NYCRR 2520.9 | Filing of amendments | excluded_regime | 0.01 | 0.07 | Filing of amendments to the Rent Stabilization Code; regime: |
| NY:BCL 1301 | Authorization of foreign corporations | partial | 0 | 0.06 | NY:BCL-1312(a)-foreign-authority, NY:GBL-130-assumed-name, NY:BCL-1301-doing-business-and-fictitious-name |
| NY:BCL 1305 | Application for authority | stated | 0 | 0.05 | NY:BCL-1312(a)-foreign-authority |
| NY:BCL 1309 | Certificate of amendment | partial | 0 | 0.05 | NY:BCL-1312(a)-foreign-authority, NY:BCL-1309(c)-authority-suspension |
| NY:CCA 2101 | Definitions | partial | 0 | 0.09 | NY:ADJ-lease-balance-not-consumer-credit, NY:S9760-venue, NY:CCA-2101(g)-balance-venue-current |
| NY:CPLR 1208 | Settlement procedure | new_rule | 0.04 | 0.08 | NY:CPLR-1208-incapacitated-settlement-papers |
| NY:GBL 136 | Exhibition or display of the flag | new_rule | 0.05 | 0.08 | NY:GBL-136(c)-no-flag-on-business-stationery |
| NY:LLC Law 204 | Limited liability company name | stated | 0 | 0.05 | NY:GBL-130-assumed-name |
| NY:LLC Law 803 | Activities not constituting doing business | partial | 0.01 | 0.06 | NY:LLC-808(a)-foreign-authority, NY:LLC-803-doing-business-exclusions |
| NY:LLC Law 805 | Issuance of certificate of authority | stated | 0 | 0.05 | NY:LLC-808(a)-foreign-authority |

Substantive misses (partial or new_rule): 7 of 456, all with p_decides of 0.09 or below.

## Proposed rules, most severe first

critical 0, major 4, minor 3.

### NY:19NYCRR-175.21-broker-supervision (major, RULE)
- Section: NY:19 NYCRR 175.21 (partial, amends NY:HANDOFF-broker-config-under-broker)
- Provision: 19 NYCRR 175.21(a), (b); actor: licensed broker; associated salesperson; walk step: Step 8.6a state licensing of whoever collects rent
- If: Configuration 3 applies: individuals (for example Handoff's people) collect or attempt to collect a rent balance as real estate salespersons associated with a licensed broker (for example the manager's brokerage).
- Then: The broker supervises each such salesperson by regular, frequent and consistent personal guidance, instruction, oversight and superintendence of the brokerage business the salesperson conducts, including the collection work; a broker whose name the salespersons use without that supervision does not meet the association RPL 441(1)(d) requires, and the broker's licence is exposed under NY:RPL-441-c-licence-discipline. The broker and the salesperson each keep written records of every transaction the salesperson effects or assists with, sufficient to identify it and showing its dates.
- Source: `register/texts/NY_19NYCRR/175.21.txt` (https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.21)
- Quote: "(a) The supervision of a real estate salesman by a licensed real estate broker, required by subdivision 1(d) of section 441 of the Real Property Law, shall consist of regular, frequent and consistent personal guidance, instruction, oversight and superintendence by the real estate broker with respect to the general real estate brokerage business conducted by the broker, and all matters relating thereto."

### NY:BCL-1301-doing-business-and-fictitious-name (major, MIXED)
- Section: NY:BCL 1301 (partial, amends NY:BCL-1312(a)-foreign-authority)
- Provision: BCL 1301(a), (b), (d); actor: owner (foreign corporation); collector in its name; walk step: Step 8.10 before suing: capacity
- If: The owner is a corporation formed outside New York, and it or a collector in its name is about to sue a former tenant or settle the tenancy account.
- Then: Only activity other than the acts listed in 1301(b) counts toward 'doing business' for the BCL 1312 bar: maintaining or defending an action or proceeding, settling it or settling claims or disputes (including the tenant's deposit claim or the balance), holding directors' or shareholders' meetings, keeping bank accounts (including the deposit account), and securities-transfer offices are not doing business. Owning and leasing New York units is weighed under NY:BCL-1312(a)-foreign-authority; a corporation whose only New York acts are those listed may sue without authority. A foreign corporation authorized under a fictitious name because its own name was unavailable must use that fictitious name in its New York business, including leases, statements and suits, and GBL 130 does not apply to that name: no assumed-name certificate is needed before suing on a lease made in it, and a GBL 130 filing does not adopt a fictitious name. A lease made in any other name than the corporate or filed fictitious name stays subject to NY:GBL-130-assumed-name.
- Judgment terms: doing business in this state
- Source: `register/texts/NY_BCL/1301.txt` (https://newyork.public.law/laws/n.y._business_corporation_law_section_1301)
- Quote: "(b) Without excluding other activities which may not constitute doing business in this state, a foreign corporation shall not be considered to be doing business in this state, for the purposes of this chapter, by reason of carrying on in this state any one or more of the following activities: (1) Maintaining or defending any action or proceeding, whether judicial, administrative, arbitrative or otherwise, or effecting settlement thereof or the settlement of claims or disputes."

### NY:CCA-2101(g)-balance-venue-current (major, RULE)
- Section: NY:CCA 2101 (partial, amends NY:ADJ-lease-balance-not-consumer-credit)
- Provision: CCA 2101(g); CCA 301(a); actor: landlord (plaintiff); collector suing in its name; walk step: Step 8.10 where to sue a small balance
- If: The landlord or its collector sues a former tenant in the NYC Civil Court for a residential lease balance (rent, use and occupancy, damage or other lease charges), and the action is commenced before NY:S9760-venue takes effect.
- Then: The action does not arise out of a 'consumer credit transaction' as CCA 2101(g) defines it (credit extended to an individual), so the tenant-county rule of CCA 301(a) for consumer credit actions does not apply. The action is brought in the county within the city where one of the parties resides when it is commenced: the tenant's county, or the owner's county, an entity owner residing in any county where it transacts business or keeps an office (CCA 305). If no party resides in the city, CCA 301(b) governs. For actions commenced on or after NY:S9760-venue takes effect, that rule controls instead. The added consumer-credit filing fee does not apply (NY:CCA-1911-clerk-fees).
- Source: `register/texts/NY_CCA/2101.txt` (https://www.nysenate.gov/legislation/laws/CCA/2101)
- Quote: "(g) "Consumer credit transaction" means a transaction wherein credit is extended to an individual"

### NY:LLC-803-doing-business-exclusions (major, MIXED)
- Section: NY:LLC Law 803 (partial, amends NY:LLC-808(a)-foreign-authority)
- Provision: LLC Law 803(a); actor: owner (foreign LLC); collector in its name; walk step: Step 8.10 before suing: capacity
- If: The owner is a limited liability company formed outside New York, and it or a collector in its name is about to sue a former tenant or settle the tenancy account.
- Then: Only activity other than the acts listed in 803(a) counts toward 'doing business' for the LLC Law 808 bar: maintaining or defending an action or proceeding, settling it or settling claims or disputes (including the tenant's deposit claim or the balance), holding members' or managers' meetings, keeping bank accounts (including the deposit account), and offices only for membership-interest transfers are not doing business. Owning and regularly leasing New York units is weighed under NY:LLC-808(a)-foreign-authority; a foreign LLC whose only New York acts are those listed may sue without a certificate of authority. The list does not decide whether the LLC may be served with process in New York.
- Judgment terms: doing business in this state
- Source: `register/texts/NY_LLC/803.txt` (https://newyork.public.law/laws/n.y._limited_liability_company_law_section_803)
- Quote: "(a) Without excluding other activities that may not constitute doing business in this state, a foreign limited liability company shall not be considered to be doing business in this state for the purposes of this chapter, by reason of carrying on in this state any one or more of the following activities: (1) maintaining or defending any action or proceeding, whether judicial, administrative, arbitrative or otherwise or effecting settlement thereof or the settlement of claims or disputes;"

### NY:BCL-1309(c)-authority-suspension (minor, RULE)
- Section: NY:BCL 1309 (partial, amends NY:BCL-1312(a)-foreign-authority)
- Provision: BCL 1309(c); actor: owner (foreign corporation); collector in its name; walk step: Step 8.10 before suing: capacity
- If: An authorized foreign corporation owning the unit changed its corporate name or its jurisdiction of incorporation in its home jurisdiction and did not deliver a certificate of amendment to the Department of State within 20 days after the change took effect there.
- Then: From the 21st day its New York authority is suspended, so while suspended it is not authorized and cannot maintain a suit against a former tenant (NY:BCL-1312(a)-foreign-authority). If the Department of State files the amendment within 120 days after the change, the suspension is annulled and authority continues as if never suspended. The Secretary of State remains its agent for process on liabilities incurred before the filing, so the tenant's suit on the deposit is served there. Operator step: before suing, confirm the owner's New York authority is not suspended and the name on the suit matches the name on file.
- Source: `register/texts/NY_BCL/1309.txt` (https://newyork.public.law/laws/n.y._business_corporation_law_section_1309)
- Quote: "If an authorized foreign corporation has changed its name in the jurisdiction of its incorporation, or has changed its jurisdiction of incorporation, it shall deliver to the department of state within twenty days after the change became effective in that jurisdiction a certificate of amendment under paragraph (a) of this section. Upon its failure to deliver such certificate, its authority to do business in this state shall upon the expiration of said twenty days be suspended."

### NY:CPLR-1208-incapacitated-settlement-papers (minor, RULE)
- Section: NY:CPLR 1208 (new_rule)
- Provision: CPLR 1208(a)-(f); actor: landlord and its attorney; tenant's representative; walk step: Step 8.1b payments and settlements; Step 7.6 the tenant's claims
- If: The landlord settles a claim with a former tenant who is an infant, adjudicated incompetent or conservatee (the tenant's deposit claim or the landlord's balance claim), so the settlement needs court approval under CPLR 1207.
- Then: The application includes an affidavit of the tenant's representative stating his name, residence and relationship; the tenant's name, age and residence; the circumstances of the claim; the nature and extent of the damages; the settlement terms and proposed distribution and his approval of both; any other settlement application on the same claim; any reimbursement received; and any related family claim. If the tenant or representative has an attorney, that attorney's affidavit states the reasons for recommending the settlement, that he is not concerned in it at the landlord's instance and takes no compensation from the landlord, and his services. At the hearing the moving party, the tenant and his attorney attend unless excused for good cause. No attorney with an interest conflicting with the tenant's may represent him, so the landlord's attorney never represents the tenant; if the tenant has no attorney, the landlord's attorney may prepare the papers and they must say so. A settlement without this approval does not bind (dependency).
- Source: `register/texts/NY_CPLR/1208.txt` (https://newyork.public.law/laws/n.y._civil_practice_law_&_rules_section_1208)
- Quote: "(e) Representation. No attorney having or representing any interest conflicting with that of an infant or incompetent may represent the infant or incompetent. (f) Preparation of papers by attorney for adverse party. If the infant or incompetent is not represented by an attorney the papers may be prepared by the attorney for an adverse party or person and shall state that fact."

### NY:GBL-136(c)-no-flag-on-business-stationery (minor, RULE)
- Section: NY:GBL 136 (new_rule)
- Provision: GBL 136(c); actor: landlord; managing agent; Handoff; collector; walk step: Step 6.4 what the statement must be; Step 8 collecting a balance
- If: A landlord, manager, Handoff or collector prepares or sends business stationery in the settlement chain: the itemized statement, a refund check, a balance or demand letter, an invoice, or their envelopes.
- Then: The stationery may not carry a representation of the flag, standard, color, shield or ensign of the United States or of New York (including any picture showing the stars and stripes that a reader would take for the flag), and stationery so marked may not be used for business correspondence; either act is a misdemeanor. The exception for stationery for private correspondence does not reach a landlord's or collector's business letters. The rule governs only the form of the document; a statement sent on such stationery is still a written statement for NY:GOL-7-108(1-a)(e).
- Source: `register/texts/NY_GBL/136.txt` (https://newyork.public.law/laws/n.y._general_business_law_section_136)
- Quote: "c. Shall print, engrave, or otherwise place or cause to be printed, engraved or otherwise placed on any blank check, bill head, letter head, envelope or other business stationery, a representation of any such flag, standard, color, shield or ensign, or shall use any such blank check, bill head, letter head, envelope or other stationery for business purposes or correspondence, or"

## Existing rules that look wrong or incomplete

- `NY:BCL-1312(a)-foreign-authority` and `NY:LLC-808(a)-foreign-authority` leave 'doing business' wholly to judgment. BCL 1301(b) and LLC Law 803(a) fix part of it by statute: suing, settling claims and keeping bank accounts are not doing business. The judgment should run only over what is left (leasing and managing units). Proposed: `NY:BCL-1301-doing-business-and-fictitious-name`, `NY:LLC-803-doing-business-exclusions`.
- `NY:GBL-130-assumed-name` does not carve out a foreign corporation's fictitious name filed with its application for authority; BCL 1301(d) says GBL 130 does not apply to that name. A lease made in the filed fictitious name needs no assumed-name certificate before suit.
- Current Civil Court venue for a lease-balance suit is stated nowhere. The register matched CCA 301 to `NY:S9760-venue`, which states only the pending bill's tenant-county rule. Under today's law (CCA 2101(g), 301(a)) the balance is not a consumer credit transaction, so suit lies in any city county where a party resides. The queue proposal `NY:CCA-305-venue-residence` assumes this without a rule behind it. Proposed: `NY:CCA-2101(g)-balance-venue-current`.
- `NY:HANDOFF-broker-config-under-broker` (Configuration 3) states only the licence condition. 19 NYCRR 175.21 makes the configuration lawful only with the broker's regular, frequent and consistent personal supervision and transaction records. Proposed: `NY:19NYCRR-175.21-broker-supervision`.

No existing rule was found stating the law incorrectly; the four items above are gaps in reach, not errors in what the rules say.

## Checker

```
$ python3 register/work/check_decisions.py 7
batch 7: 456/456 decided {'excluded_regime': 10, 'new_rule': 2, 'no_decision': 436, 'partial': 5, 'stated': 3}; 0 errors

$ python3 register/work/check_decisions.py all
batch 1: 499/499 decided {'excluded_regime': 49, 'new_rule': 55, 'no_decision': 340, 'partial': 40, 'stated': 15}; 0 errors
batch 2: 560/560 decided {'excluded_regime': 1, 'new_rule': 193, 'no_decision': 341, 'partial': 23, 'stated': 2}; 0 errors
batch 3: 422/422 decided {'excluded_regime': 48, 'new_rule': 28, 'no_decision': 297, 'partial': 13, 'stated': 36}; 0 errors
batch 4: 496/496 decided {'excluded_regime': 0, 'new_rule': 48, 'no_decision': 402, 'partial': 32, 'stated': 14}; 0 errors
batch 5: 264/264 decided {'excluded_regime': 0, 'new_rule': 48, 'no_decision': 201, 'partial': 13, 'stated': 2}; 0 errors
batch 6: 257/257 decided {'excluded_regime': 3, 'new_rule': 78, 'no_decision': 158, 'partial': 6, 'stated': 12}; 0 errors
batch 7: 456/456 decided {'excluded_regime': 10, 'new_rule': 2, 'no_decision': 436, 'partial': 5, 'stated': 3}; 0 errors
batch 8: 420/420 decided {'excluded_regime': 0, 'new_rule': 6, 'no_decision': 413, 'partial': 1, 'stated': 0}; 0 errors
```
