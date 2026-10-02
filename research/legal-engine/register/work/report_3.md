# Review queue, batch 3 (NYC Administrative Code and RCNY): reviewer q3

Decisions: `register/work/decisions_3.jsonl` (422 of 422). Built by `register/work/q3_d01.py` … `q3_d29.py` on
`q3_lib.py` (quotes copied mechanically from the register text by start/end markers; `source_url` read from each
file's SOURCE header). `python3 register/work/check_decisions.py 3` → `422/422 decided … 0 errors`; the all-batch run
shows no cross-batch id collision with the proposals filed so far.

## Counts

| decision | sections |
|---|---|
| stated | 36 |
| partial | 13 |
| new_rule | 28 |
| no_decision | 297 |
| excluded_regime | 48 |
| **total** | **422** |

42 proposed rules: 6 critical, 23 major, 13 minor. Every dependency and `amends` resolves to an existing rule or a
rule proposed in this file.

## Proposed rules, most severe first

Critical
- `NYC:ADC-26-3402-vacating-fee-cap`: when a tenant leaves in breach of the lease (the RPL 227-e duty to mitigate
  applies), the landlord may recover no vacating-related amount above the fair market cost of preparing the unit for
  rental. Whenever it seeks that amount it must give an itemized calculation. Rent damages under 227-e are outside the
  cap. No rule or walk step states this city law (in force 2022-06-22).
- `NYC:ADC-8-502-private-action`: the tenant can sue in court under city law over a discriminatory settlement or
  collection: damages including punitive, fees, a three-year limit with tolling, and election of remedies.
- `NYC:HMC-27-2148-lien-receiver-rents` (amends `NYC:HMC-27-2135(c)-receiver-rents`): once HPD repair liens reach
  $5,000, HPD can take over as receiver of the rents. This works on any premises, and the owner, manager and
  collector then stop collecting rent.
- `NYC:RCNY68-9-06-HOME-TBRA-payments`: HRA pays HOME TBRA only during the lease and while the household lives in the
  unit. Payments continue while an eviction is pending, until judgment.
- `NYC:RCNY68-9-10(e)-HOME-TBRA-moveout-month`: payments stop the month after the move, and the landlord keeps the
  move-out month.
- `NYC:RCNY68-9-14-HOME-TBRA-charges`: the landlord may charge only the lease rent and fees (customary fees need HRA
  approval). Overpayments go back to HRA. The sanction is being barred from HRA programs.

Major
- `NYC:HMC-27-2004(48)-buyout-offers`: an owner-initiated offer of money or other value to leave requires eight
  written disclosures. A written refusal bars new offers for 180 days, and no offer may come with threats or abusive
  contact. Any of these breaches is harassment (27-2005(d)).
- `NYC:HMC-27-2004(48)-ending-harassment`: while the person is still a lawful occupant, the following are harassment
  by the owner and its agents: false or misleading information about the occupancy, repeated baseless proceedings,
  removing belongings or locks, contact on weekends or outside 9 a.m.–5 p.m., status-based threats, and citizenship
  document demands.
- `NYC:ADC-26-2403-buyout-filing` and `NYC:ADC-26-2402-buyout-definition`: a tenancy ended by a buyout must be filed
  with HPD within 90 days. Any market-rate unit counts, including an owner-induced early termination that gives the
  tenant value.
- `NYC:ADC-26-3401-mitigation-definition`: the 26-3402 cap applies exactly when RPL 227-e applies.
- `NYC:ADC-27-2105-rent-receipt-agent`: every rent bill or receipt, including final arrears, must name the registered
  managing agent or owner and any separate rent-collection agent. A change of collection agent needs mailed notice 15
  days before the next rent payment is collected.
- `NYC:HMC-27-2005(c)-1-2-family-allocation` (amends `NYC:HMC-27-2013(a)`): in a one- or two-family house, a written
  lease may put repairs, including painting, on the tenant. The deposit is still limited to damage beyond wear and
  tear.
- `NYC:HMC-27-2009.1-pet-clause-waiver`: in a multiple dwelling, a no-pet clause is waived after three months of open
  harboring the owner knew about, so no pet-violation charge may be made. Actual pet damage stays chargeable.
- `NYC:HMC-27-2017.1-pest-owner-duty` (amends `NYC:HMC-27-2017.5-turnover`): pest and mold remediation is the owner's
  duty in every dwelling, one- and two-family houses included. The tenant is charged only for conditions it caused.
- `NYC:HMC-27-2017.12-waiver-void`: a lease clause shifting pest or mold remediation to the tenant is void, and
  seeking one is a misdemeanor plus a $500 civil penalty.
- `NYC:ADC-8-109-commission-complaint`, `NYC:ADC-8-120-commission-remedies`, `NYC:ADC-8-126-civil-penalty`: the
  Commission route (one-year limit), its remedies, and penalties of $125,000, or $250,000 for willful practices.
- `NYC:RCNY47-2-06-self-identified-name`: deliberately refusing the tenant's self-identified name, pronoun or title
  in the statement or collection letters violates 8-107.
- `NYC:RCNY31-5-07-SOTA-withholding`: SOTA payments HRA withheld for conditions are released only if the problem was
  resolved while the household still lived there.
- `NYC:RCNY68-9-09-HOME-TBRA-abatement`: HQS abatement months are not paid by HRA and are not the tenant's debt.
- `NYC:ADC-20-493(d)-agency-vicarious`: a licensed agency answers for its employees' and agents' acts within the scope
  of their authority.
- `NYC:ADC-20-106-unlicensed-sanctions` (amends `NYC:ADC-20-490`): criminal fines and escalating civil penalties for
  unlicensed collection.
- `NYC:ADC-20-703-CPL-remedies` (amends `NYC:CPL-20-700`): $350–$2,500 per violation, restitution, and no private
  action.
- `NYC:RCNY6-6-62-collection-penalties` (amends `NYC:ADC-20-490`): DCWP penalty amounts for 5-77 and 5-78 ($525,
  $1,050, $3,500) and for licensee duties.
- `NYC:RCNY6-5-78-deceptive-forms`: the city ban on flat-rating reaches any person, including Handoff when it is not
  really participating.
- `NYC:RCNY6-1-05-licence-number`: a licensee's letters, emails and receipts carry its DCWP licence number.
- `NYC:RCNY6-2-194-callback-person`: an agency's call-back number must be answered by a person within the 60/60-second
  standard.

Minor
- `NYC:ADC-26-2401-buyout-scope`, `NYC:ADC-26-2405-buyout-penalty`: buyout agreements from 2020-07-01; a late filing
  is a non-hazardous violation.
- `NYC:ADC-27-2103-registration-extension` (amends `NYC:ADC-27-2107(b)-rent-stay`): an HPD extension waives the city
  stay but not the MDL 325(2) bar.
- `NYC:ADC-27-2106-registration-proof`: without the HPD receipt, failure to register is proved prima facie.
- `NYC:RCNY28-12-03-classB-smoke`, `NYC:RCNY28-12-09-classB-CO` (amend `NYC:HMC-27-2045-detector-charge`): in a class
  B building the owner maintains and replaces detectors, and there is no reimbursement charge.
- `NYC:ADC-20-117-breach-copy-to-DCWP` and `NYC:RCNY6-6-85-breach-copy-penalty`: a DCWP licensee sends DCWP a copy
  of its breach notice ($175–$500 penalty).
- `NYC:RCNY6-1-15-licensee-judgment`: a licensee pays a consumer's judgment within 30 days.
- `NYC:RCNY6-5-24-card-payments`: taking the balance by card means disclosing card limitations and following GBL 518.
- `NYC:RCNY6-6-11-licence-number-penalty`, `NYC:RCNY6-6-47-CPL-penalties`, `NYC:RCNY6-6-89-FARE-penalties`: penalty
  amounts.

## Existing rules that look wrong or incomplete

1. `NYC:HMC-27-2135(c)-receiver-rents`. Its reasoning reads: "Section 27-2130 limits HPD receiverships to multiple
   dwellings, so a one- or two-family house is not subject to one." That holds only for article 6. Under 27-2148, a
   lien-based HPD receiver of "the rent and profits of the premises" can be appointed on any premises carrying
   $5,000 or more of HPD liens ("the department may issue an order appointing the commissioner … receiver of the rent
   and profits of the premises"). See `NYC:HMC-27-2148-lien-receiver-rents`.
2. `NY:ADJ-lease-break-charge`, walk 3.3, 5.2 and 5.4. None of them mentions Admin. Code 26-3402 ("such landlord may
   not recover from a tenant any amount in excess of the fair market cost necessary to prepare the physical
   conditions of the premises for rental"). Re-rental, broker, processing and lease-break fees above that ceiling are
   not recoverable after an early departure, and the itemized calculation is a condition of seeking the amount.
3. `NYC:HMC-27-2017.5-turnover` says "One- and two-family houses are not covered by this section." That is correct
   for 2017.5. But 27-2017.1 ("An owner of a dwelling shall keep the premises free from pests") puts the same cost on
   the owner of a house, so a pest or mold charge there is no freer than in a multiple dwelling.
4. `NYC:HMC-27-2013(a)` and `NYC:PAINT-wear-and-tear`. For a one- or two-family house they state the owner paints
   with no exception. 27-2005(c) makes that duty the owner's "except to the extent otherwise agreed between such owner
   and any tenant of such dwelling by lease or other contract in writing."
5. Walk deferral of `US:24CFR92.253(b)(2)` under "public housing and project-based or other subsidized housing". HRA
   HOME TBRA (68 RCNY ch. 9) is tenant-based assistance in a private unit, the same class as CityFHEPS and SOTA, which
   the aperture keeps in. I decided the HRA HOME TBRA landlord rules as in aperture (9-06, 9-09, 9-10, 9-14). The
   HOME lease protections in 24 CFR 92.253 reach TBRA leases through 92.209, so that deferral should be revisited in
   the batch that holds 24 CFR part 92.
6. `NYC:HMC-27-2045-detector-charge` covers class A multiple dwellings and private dwellings only. Class B is missing
   (28 RCNY 12-03 and 12-09 put maintenance and replacement on the owner).
7. Walk 8.4 and 8.6 state DCWP duties but not the penalty and restitution exposure (20-703, 6-47, 6-62, 20-106). That
   is not wrong, but the consequence of a miss is missing.

## no_decision where Jev had P(DECIDES) >= 0.9

- 6 RCNY 6-90 (0.90): self-storage penalty schedule. No chain party runs a self-storage facility.
- Admin. Code 26-1201 and 26-1202 (0.98): conditioning occupancy on medical treatment. No settlement or collection
  step turns on medical treatment, and the setoff in 26-1202(b) arises only in a suit on that violation.
- Admin. Code 26-3004 (0.92): the smart-access privacy policy given during the tenancy. The move-out data rules are
  stated elsewhere (26-3002(c), 26-3003/3006).
- Admin. Code 26-527 (0.91): the city is not liable for costs. No chain party is affected.
- Admin. Code 27-2009 (0.99): grounds for a summary proceeding after a tenant's code conviction. These are grounds to
  begin an ending, not a step in settling one.
- Admin. Code 27-2018.1 (0.90): bedbug history notice with a vacancy lease. Move-in paperwork that fixes no amount.
- Admin. Code 27-2129 (0.98): HPD's statement of account to the owner. The tenant-side rule is stated at
  `NYC:HMC-27-2128-owner-debt`.
- 28 RCNY Appendix A (allergen lease notice, English 0.90 and Spanish 0.91) and Appendix A (lead child-inquiry notice,
  0.94): forms that restate stated owner duties or move-in duties.

## Recall notes for Jev (sections below "likely" that decide something)

Of the 77 deciding sections (stated, partial, new_rule), 19 were in the "possible" tier and 10 in "low_confidence".
The low_confidence ones are mostly definition and applicability sections that set a rule's reach (26-2401, 26-2402,
26-3401, 26-3001, 26-522, 27-2003, 27-2017, 27-2056.2) plus 6 RCNY 5-24 and 6-11. The possible-tier ones include the
HOME TBRA payment rules (9-09 and 9-10, P = 0.01) and the SOTA withholding rule (5-07, 0.29). Jev's weakest area was
landlord-side payment rules inside rental-assistance programs.

## Notes

- LINC VI (68 RCNY ch. 7) expired and was repealed on 2024-12-31 (7-08), so its sections are no_decision.
- The city rental assistance voucher (Admin. Code tit. 26 ch. 39, in force 2027-01-26) is no_decision for now. Its
  landlord and move-out rules are delegated to HPD rulemaking under 26-3907, and HPD has adopted none.
- 28 RCNY ch. 1 (Article VIII rehabilitation-loan buildings) is excluded_regime, consistent with walk 0.6.
