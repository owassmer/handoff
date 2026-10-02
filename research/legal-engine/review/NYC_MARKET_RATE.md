# Review 1: settling a market-rate tenancy in New York City

Prepared 2026-09-28 for Owen's review of Stage A; revised 2026-09-30. It walks one departing tenancy from the unit's status to the
closed account, and names the rules that govern each step. It covers New York State law, the city rules that reach a
unit that is not rent-stabilized or rent-controlled, and federal law. Stabilized and controlled units are Review 2.

How to read it
- Each rule id in backticks is one rule in stage-a/NY.json, NYC.json or US.json. To see its quote, source,
  and any authorities and reasoning, run from research/legal-engine:
  `python3 review/show.py 'NY:GOL-7-108(1-a)(e)'` (a trailing * shows every rule with that prefix).
- "Judgment" marks a rule whose outcome depends on weighing facts (a STANDARD or MIXED rule). The rule states what
  is weighed; the case facts decide it.
- Dates are when a rule starts or stops applying. Today is 2026-09-30.
- `python3 review/check_review.py review/NYC_MARKET_RATE.md` confirms every cited id exists and that no rule in
  this review's scope is left out.

What you are accepting
- That these rules are the law for this chain, stated correctly, with nothing missing.
- Not: how Handoff operates. Where the law depends on an operating choice (for example, how Handoff is engaged to
  collect), the review states the rule for each choice; the choice comes later.

---

## Step 0. Is the unit market-rate, and which deposit regime applies?

The whole settlement turns on the unit's status and the lease date. These are facts about the unit, established
before the account is built.

0.1 Not stabilized. A unit is rent-stabilized when it is in a building of six or more units that meets one of the
coverage routes, or came in through the 1974 ETPA, or receives 421-a, J-51 or Article 18 benefits (any building
size). A co-op or condo building is excluded only if it was so owned by 1974-06-30 or as the GBL 352-eeee conversion
rules provide; a non-purchasing tenant who stayed through a conversion remains stabilized and goes to Review 2: `NYC:RSL-26-504(a)`, `NYC:RSL-26-504(a)(1)`, `NYC:RSL-26-504(a)(2)-(3)`, `NYC:RSL-26-504(b)`,
`NYC:RSL-26-504(c)`, `NYC:RS-status`. It is not stabilized when an exclusion holds:
- building of fewer than six units when it first became subject, with no other route: `NYC:RSC-2520.11(d)`;
- building completed or substantially rehabilitated on or after 1974-01-01, with no tax-benefit route:
  `NYC:RSC-2520.11(e)`;
- lawful high-rent vacancy deregulation before 2019-06-14: `NYC:RSC-2520.11(r)(1)`; high-income order with the lease
  expiring before 2019-06-14: `NYC:RSC-2520.11(s)(1)`. No new deregulation since 2019-06-14;
- 421-a-only units that have left under (p)(1)-(4): `NYC:RSC-2520.11(p)`;
- rents fixed or supervised by a public body (Mitchell-Lama, regulatory agreements): `NYC:RSC-2520.11(c)`;
  government-owned or public-housing units: `NYC:RSC-2520.11(b)`;
- a court has found the unit is not the tenant's primary residence (a manager cannot decide this itself):
  `NYC:RSC-2520.11(k)`.
A rent-controlled unit is excluded from stabilization and handled in Review 2: `NYC:RSC-2520.11(a)`.
The stabilization law runs through 2027-03-31 unless the City Council extends it: `NYC:RSL-26-520`.

0.2 Not rent-controlled. Rent control has no six-unit floor: `NYC:RC-status`. A one- or two-family house vacated
since 1953-04-01 is exempt: `NYC:RCL-26-403(e)(2)(i)(4)`. Any unit vacated since 1971-06-30 is exempt, so a
controlled tenancy today is one continuous since before July 1971 or a lawful successor:
`NYC:RCL-26-403(e)(2)(i)(9)`. Units deregulated from control by a high-income order before 2019-06-14 stay
deregulated: `NYC:RER-2211.8(a)`.

0.3 The state deposit statute. GOL 7-108 governs every dwelling unit in New York except the stabilized and ETPA
units named in 7-107: `NY:GOL-7-108(1)`. Its core rules, subdivision 1-a, do not reach rent-controlled units or
licensed senior and care facilities: `NY:GOL-7-108(1-a)-exclusions`.

0.4 Which version applies, by lease date. Subdivision 1-a (cap, inspections, 14-day statement, forfeiture) applies
to leases, rental agreements and renewals entered into on or after 2019-07-14: `NY:L2019-c36-PartM-s29`.
- A renewal, a month-to-month continuation, or rent accepted after the lease expired, on or after that date, brings
  1-a in: `NY:RPL-232-c`, `NY:CASE-Case-v-575Classon`, `NY:CASE-Bogom-Shanon-month-to-month`.
- A lease entered before 2019-07-14 and never renewed or continued since is under the old 7-108 scope (successor
  liability only) and the common-law return rule: `NY:GOL-7-108(1)-pre2019`, `NY:COMMONLAW-deposit-return`. On such
  a lease, the lease's own return period is an enforceable term: `NYC:CASE-Pezzo-lease-return-term`. Fees lawful
  under the lease may then be applied: `NY:ADJ-fee-retention-commonlaw`.
- A repealed or expired statute still governs what was done or incurred under it (a forfeiture, double damages, a Good
  Cause defense raised before 2034-06-15): `NY:GCN-93-repeal-saves-accrued`. A suit pending when the statute ends runs
  to judgment under it: `NY:GCN-94-pending-actions`.

0.5 Can rent be recovered at all? Three facts about the building decide it, before any rent goes on the account.
- The certificate of occupancy. A multiple dwelling is a building let or occupied by three or more families, counted
  as actually used, so a two-family house with a third unit is one: `NY:MDL-4(7)-multiple-dwelling`. A building
  built as, or converted into, a multiple dwelling after 1929-04-18 may not be occupied without a certificate of
  occupancy for that use; older class B buildings, old-law tenements and qualifying 1901-1909 class A buildings need
  none unless altered unlawfully (combining apartments so the legal number of families falls, without adding bulk,
  keeps the exception). A temporary certificate in force counts as a certificate. Check the Department of Buildings record for the construction or conversion date:
  `NY:MDL-301(1)`. For any period a building was occupied in violation, the owner
  recovers no rent and no use and occupancy, by suit, setoff or keeping the deposit; a later certificate does not
  revive it; damage claims are unaffected. The only exception is a tenant who actually blocked legalization.
  Judgment: `NY:MDL-302(1)(b)`. An owner of three or fewer rental units tells the tenant in bold before signing
  whether any required certificate is valid: `NY:RPL-235-bb-co-notice`.
- Registration. An unregistered multiple-dwelling owner recovers no rent while unregistered. This suspends, not
  forfeits: once it registers it recovers all accrued rent. Register before the 14-day statement so the deposit can
  be applied to rent: `NY:MDL-325(2)`. Rent the tenant paid voluntarily while the owner was unregistered stays
  paid. The city's discretionary stay applies too; for a one- or two-family house that must register it is the only
  consequence (Step 8.10).
- Rent-impairing violations. If HPD records a rent-impairing violation (a fire hazard or serious threat to life,
  health or safety) that stays uncorrected six months after notice, no rent is recovered for that unit, or for every unit when the condition is in a common part or a part the owner
  controls, while it remains uncorrected. The bar does not apply if the condition never existed, was in fact fixed, was caused by the
  tenant, its household or guests or another resident, or the tenant refused entry to fix it; rent the tenant paid
  voluntarily is not recovered back. Judgment: `NY:MDL-302-a(3)`. Read the building's HPD violation record before
  keeping any rent.
- Loft-law buildings. A unit in an interim multiple dwelling covered by the Loft Board is outside this walk; rent
  recovery there turns on the owner's compliance with article 7-C: `NY:MDL-285(1)-loft-law`.

- A one- or two-family house. The rent bars above apply only to multiple dwellings. A house of one or two families
  with an illegal unit (a basement apartment, a second unit in a one-family house) still recovers rent and may keep
  the deposit for it; a third family makes it a multiple dwelling: `NY:ADJ-MDL-rent-bar-not-1-2-family`. A cellar
  room may be rented only as a certified ancillary dwelling unit: `NYC:HMC-27-2087-cellar-basement`.
- Who is owed the rent. Check before collecting that the owner still holds the rent claim. A 7-A administrator
  collects rent after its judgment: `NY:RPAPL-776-778-administrator`. An HPD receiver collects accrued and accruing
  rents: `NYC:HMC-27-2135(c)-receiver-rents`. After an HPD rent notice, rent goes to HPD and counts as paid:
  `NYC:HMC-27-2147-rent-levy`. A foreclosure receiver collects what its order covers:
  `NY:CPLR-6401-foreclosure-receiver`. A buyer at a foreclosure sale takes subject to a market-rate tenant's right to
  stay for the rest of the lease or 90 days after its notice, whichever is longer, on the same terms, and must give
  the tenant its name and address: `NY:RPAPL-1305-successor`. A mortgagee with an assignment of rents collects only after it takes the rents:
  `NY:COMMONLAW-mortgagee-assignment-of-rents`. If an individual owner dies, the manager's authority ends; who then collects
  is set out under Owner death below: `NY:COMMONLAW-owner-death-agency`. If the owner is in chapter 7 the trustee collects:
  `US:11USC541-704-owner-chapter7`; in chapter 11 without a trustee, or chapter 13, the owner keeps collecting:
  `US:11USC1107-1306-owner-reorganization`. In every chapter the deposit stays the tenant's money if it can be traced
  (a separate account, or an account that never fell below the deposit). An untraceable commingled deposit leaves the
  tenant an unsecured creditor of the owner's estate, and the manager does not pay it from estate funds without the
  trustee's or the court's authority.
- Proof of the building's record. HPD's computerized violation and registration files are prima facie evidence in the
  Housing Part, so read them before keeping rent or suing: `NY:MDL-328-violation-files-evidence`. A city notice posted
  in the building and mailed to the registered address is served; an owner served that way cannot deny notice for the
  rent bars: `NY:MDL-326-service-on-owner`.
- More payees who displace the owner. A court nuisance receiver under MDL 309 collects accrued and accruing rent, and
  rent the tenant pays HPD on its written demand counts as rent paid: `NY:MDL-309-receiver-and-rent-demand`. An HPD
  lien receiver can be appointed on any premises, a one- or two-family house included, once repair liens reach $5,000:
  `NYC:HMC-27-2148-lien-receiver-rents`. A foreclosure receiver takes the deposits on its order and settles from them:
  `NY:RPAPL-1325(2-a)-receiver-deposits`. A stranger the tenant attorned to does not become the landlord:
  `NY:RPL-224-attornment-void`. When either side is insolvent, sued by creditors or in bankruptcy, the refund and the
  balance may be set off against each other (in the tenant's bankruptcy only after stay relief):
  `NY:DCL-151-insolvency-setoff`.
- Owner death. Rent that fell due before an individual owner died belongs to the estate's personal representative,
  even where the building is specifically devised; later rent follows the building:
  `NY:EPTL-13-1.1-accrued-rent-leasehold`. A voluntary administrator may collect that accrued rent but may not run the
  building: `NY:SCPA-1302-va-personal-property-only`. A dissolved owner partnership settles and sues through the
  persons winding it up, and the deposit is never distributed to partners:
  `NY:PTR-121-803-dissolved-owner-winding-up`.
- Owner in bankruptcy. The estate collects balances and pays refunds in the ordinary course, but rents subject to a
  lender's assignment of rents are cash collateral, used only with consent or a court order:
  `US:11USC363-owner-cash-collateral`, `US:11USC552(b)(2)-postpetition-rents`. A receiver or other custodian stops
  paying out and turns rents over to the trustee or debtor in possession: `US:11USC543-custodian-turnover`. An
  untraceable pre-filing deposit is a seventh-priority claim up to $3,800 per individual (cases filed from
  2025-04-01); damages for mishandling it are general claims: `US:11USC507(a)(7)-deposit-priority`. A deposit the
  estate itself took after filing is an administrative expense; a chapter 7 tenant's post-filing rent is not:
  `US:11USC503-admin-expense-refund`. In chapter 11 a scheduled, undisputed tenant claim is deemed filed; any other
  must be filed by the bar date: `US:11USC1111-deemed-filed`, `US:FRBP3003-ch11-bar-date`. The plan pays priority
  claims in cash: `US:11USC1129(a)(9)-priority-cash`. Confirmation binds tenants and returns the building to the
  owner; an entity owner is discharged at confirmation, an individual only on completing the plan:
  `US:11USC1141-owner-plan-confirmed`, `US:11USC1192-subv-discharge`.

0.6 Status variants that change the settlement. Record each at the start:
- Housing Choice Voucher (Section 8) tenant: Step 5.7. A victim of domestic violence keeps the tenancy, and the lease
  may be split to remove the abuser: `US:34USC12491-VAWA`.
- CityFHEPS or SOTA household, whose deposit is an HRA voucher, not cash: `NYC:RCNY68-10-14(c)`,
  `NYC:RCNY31-5-06(a)(1)`; see Step 5.8.
- Building with a city Article VIII rehabilitation loan: every unit is rent-controlled while the loan requires it, so
  the unit goes to Review 2: `NYC:RCL-26-403(e)(1)(c)`.
- Tenant is a company, not a person: federal debt-collection law does not apply to its balance:
  `US:15USC1692a(3)`.
- Tenant is a servicemember or dependent: `US:50USC3911(1)-(2)`, `US:50USC3911(4)`; Step 3.4.
- Military service for New York law includes state active duty ordered by a governor, so a guardsman on state duty has
  the Military Law protections even where the SCRA does not apply: `NY:MIL-301-military-service`.
- HRA HOME tenant-based rental assistance household: HRA pays only while the lease runs and the household lives there:
  `NYC:RCNY68-9-06-HOME-TBRA-payments`; see Step 5.7a.
- A voucher family whose assistance has been zero for 180 days is no longer a voucher tenancy; state law alone governs
  its settlement: `US:24CFR982.455-zero-hap`.

---

## Step 1. What was fixed at move-in

The settlement is only as good as the move-in record. Much of it cannot be repaired at move-out.

1.1 Deposit cap. The deposit plus any rent paid ahead for a later period (for example last month's rent) may not
exceed one month's rent. The first month's rent paid at signing is rent, not an advance: `NY:GOL-7-108(1-a)(a)`. Exceptions:
a registered seasonal unit, `NY:GOL-7-108(4)`, `NY:L2021-c428`, `NY:L2022-c111`; an owner-occupied co-op unit,
`NY:GOL-7-108(6)`, `NY:L2021-c789-s7`, `NY:L2022-c93`. An excess is refundable at settlement.

1.2 The deposit is the tenant's money in trust. Every rental deposit is covered: `NY:GOL-7-103(1)-scope`. It stays
the tenant's, may not be mixed with the landlord's money, and is not the landlord's asset:
`NY:GOL-7-103(1)-trust`. Waivers are void: `NY:GOL-7-103(3)`, `NY:GOL-7-108(3)`.
- If banked, the landlord must tell the tenant in writing the bank's name and address and the amount:
  `NY:GOL-7-103(2)-bank-notice`.
- In a building of six or more dwelling units, the deposit must be in an interest-bearing account at a New York bank:
  `NY:GOL-7-103(2-a)`. Units are counted per building; other buildings of the same owner are not added:
  `NY:ADJ-7103-2a-building-count`, `NY:CASE-Gihon-7-103(2-a)-building`.
- The landlord may keep 1% a year as its only administration fee: `NY:GOL-7-103(2)-admin-fee`. The rest of the
  interest is the tenant's, paid yearly, applied to rent, or held until settlement: `NY:GOL-7-103(2)-interest-owed`.
- A licensed broker holding the deposit puts it within three business days in a separate, special, federally
  insured account: `NY:19NYCRR-175.1-broker-escrow`.
- No bank notice lets a court infer commingling, which the landlord must rebut:
  `NY:CASE-Paterno-bank-notice-inference`. Commingling forfeits the deposit (Step 7.3).
- A broker-manager holding the deposit follows the trust and interest rules or risks its licence:
  `NY:19NYCRR-175.3-broker-manager-deposit`. An attorney holding it keeps it out of IOLA, in a separate account
  (interest-bearing in a building of six or more units): `NY:JUD-497-attorney-escrow-deposit`.

1.3 Move-in inspection. After the lease is signed and before occupancy, the landlord must offer a joint inspection;
if the tenant accepts, both sign a condition record: `NY:GOL-7-108(1-a)(c)-offer`. Nothing noted on it can be
deducted at move-out: `NY:GOL-7-108(1-a)(c)-bar`.

1.4 Fees disclosed before signing (leases signed on or after 2025-06-11). The landlord must give an itemized,
tenant-signed disclosure of every fee the tenant must pay in connection with the rental, and keep it three years:
`NYC:FARE-20-699.22(b)`, `NYC:DCWP-FARE-FAQ-disclosure`. A fee is a charge for services; rent and compensation for
loss are not fees: `NYC:FARE-20-699.20-fee`. Consequence at move-out: Step 5.4.
No other payment may be demanded for an application or before or at the start of the tenancy, except a background
or credit check at no more than the lesser of actual cost or $20. One still on the ledger is not carried into the
final account; one the tenant paid is credited against any balance: `NY:RPL-238-a(1)-no-move-in-fees`.

1.5 Painting records. In a multiple dwelling (three or more units), the owner must keep records of when each unit
was last painted and by whom: `NYC:HMC-27-2013(g)`. These decide painting charges (Step 5.3). A one- or two-family
house has no records duty: `NYC:HMC-27-2013(a)`.

1.6 HPD registration. The owner of a multiple dwelling, or of a one- or two-family house occupied by neither the
owner nor a family member, must register with HPD: `NYC:ADC-27-2097-registration`. What non-registration does to rent:
Step 0.5 and 8.10.

1.7 Electronic contact. Consent the tenant gives before move-out (lease or portal) to be contacted by email or text
can later carry into collection under the city rule from 2027: `NYC:SHIELD-5-77(b)(5)(i)(B)`. Electronic records
and signatures have the same force as paper: `NY:STT-305(3)`, `NY:STT-307`.

1.8 Payment methods and receipts. The landlord may not require electronic payment or charge for paper:
`NY:RPL-235-g`. Rent paid in cash or other non-personal-check form, including arrears paid at move-out, needs a
written receipt: `NY:RPL-235-e(a)`. A bill passed by both houses and not delivered to the Governor on 2026-09-29
would, from the day it becomes law, bar any fee for rent paid by ACH and require a fee-free payment method:
`NY:S947-ach-fee-ban`.

1.9 Possession never delivered. If the landlord does not deliver the unit at the start of the term and the lease does
not provide otherwise, the tenant may rescind and recover everything it paid, with damages; there is no tenancy to
settle: `NY:RPL-223-a-no-possession-rescission`.

---

## Step 2. Events during the tenancy that change the settlement

2.1 Building sold. The seller must turn the deposit over to the buyer within 5 days of the deed and notify the tenant
by registered or certified mail: `NY:GOL-7-105(1)`. That relieves the seller, and the buyer becomes responsible:
`NY:GOL-7-105(2)-transfer-effect`, unless the lease provides otherwise: `NY:GOL-7-105(2)-inconsistent-agreement`.
Failing to comply is a misdemeanor: `NY:GOL-7-105(3)`. A buyer with actual knowledge of a deposit it did not receive
is also liable: `NY:GOL-7-108(2)(a)`, `NY:GOL-7-108(2)(b)`, `NY:GOL-7-108(2)(c)`, `NY:GOL-7-108(2)(d)`. A receiver's
liability is limited: `NY:GOL-7-108(2)(e)`. The buyer collects rent and charges that fall due after title passes;
those that fell due before belong to the seller unless assigned to the buyer in writing, so the buyer's statement
keeps nothing for pre-sale arrears: `NY:RPL-223`.
Rent the tenant paid the seller before notice of the sale binds the buyer: `NY:RPL-248-payment-before-notice`. An
owner partnership that merges passes the building, the deposit and the balance to the survivor:
`NY:PTR-121-1104-merger-successor`.

2.2 Assignment and sublet. On a tenant's request, unreasonably refused consent to assign releases the tenant:
`NY:RPL-226-b(1)`. In buildings of four or more units, sublet consent may not be unreasonably withheld, and the
tenant stays liable: `NY:RPL-226-b(2)`. Scope limits: `NY:RPL-226-b(3)`.

2.3 Who is a tenant. Only parties to the lease are tenants. An occupant living there with consent is not and gains no
tenancy: `NY:RPL-235-f`.

2.4 One co-tenant leaves. The deposit clock does not start. It starts when the last tenant leaves. The departing
co-tenant looks to the others for a share unless the landlord agrees otherwise in writing:
`NY:ADJ-cotenants-vacated`.

2.5 Tenant dies. The estate may ask to assign or sublet. The landlord's silence for 30 days is consent; an
election to terminate or an unreasonable refusal ends the lease; a reasonable refusal keeps it: `NY:RPL-236`. The estate may terminate on notice and stays liable for rent and damage before termination:
`NY:RPL-236-a`. For collection, the deceased remains the consumer: `US:12CFR1006.2(e)`. The refund belongs to the
estate: it is paid to the executor or administrator, or to a voluntary administrator for an estate of $50,000 or
less; paying a relative without letters or a certificate does not discharge the landlord. The statement goes out
within the 14 days to the fiduciary or, if none is known, to the last address addressed to the estate, and the refund
is held in trust until a fiduciary appears. Claims against the estate go to the fiduciary within 7 months of letters,
and 18 months after death are not counted in the limitation period: `NY:ADJ-tenant-death-payee`,
`NY:CPLR-210-death`.
- A co-tenant's death leaves its estate and the survivors jointly liable for the whole balance:
  `NY:GOL-15-106-cotenant-death`.
- Who may receive the refund. A fiduciary on letters may collect, settle and compromise:
  `NY:EPTL-11-1.1-fiduciary-powers`. Letters are conclusive while in force; a clerk's certificate is good for six
  months: `NY:SCPA-703-letters-evidence`. Limited letters authorize only what they state:
  `NY:SCPA-702-limited-letters`. Where two courts issued letters, the first holder controls:
  `NY:SCPA-704-first-letters`. Surviving co-fiduciaries or a court-appointed successor act; the representative of a
  dead fiduciary does not: `NY:SCPA-706-surviving-successor-fiduciary`,
  `NY:EPTL-11-3.4-no-representative-of-representative`. A payment made in good faith before letters were revoked
  stands: `NY:SCPA-720-revoked-letters`.
- With no one eligible for letters, the county public administrator takes the refund and belongings, even before
  letters, and receives the landlord's claim; in a small estate its receipt discharges the landlord:
  `NY:SCPA-1112-public-administrator`, `NY:SCPA-1118-pa-before-letters`, `NY:SCPA-1115-pa-small-estate`. A
  rooming-house keeper reports a roomer's death to the public administrator within 12 hours:
  `NY:SCPA-1113-rooming-house-death-report`. A tenant who had an article 81 guardian: the refund goes to the personal
  representative or the public administrator, not the guardian: `NY:MHL-81.44-death-of-ward`.
- A tenant domiciled elsewhere: its foreign fiduciary may be paid without a court order unless the landlord has notice
  of a New York representative or New York creditors: `NY:EPTL-13-3.4-foreign-fiduciary`; another state's small-estate
  certificate is honored only on reciprocity: `NY:SCPA-1309-foreign-small-estate`.
- A servicemember's power of attorney survives the tenant's death for an agent acting in good faith without notice of
  it: `NY:GOL-3-501-servicemember-poa-death`.
- The claim against the estate is written, states its facts and amount, and describes the deposit applied:
  `NY:SCPA-1803-claim-form`. An estate fiduciary answers on its own contracts and on the estate's property in its
  representative capacity: `NY:EPTL-11-4.7-fiduciary-liability`. At trial the landlord's interested witnesses may not
  testify to personal dealings with the dead tenant: `NY:CPLR-4519-dead-mans-statute`. Costs against a fiduciary are
  charged to the estate: `NY:CPLR-8110-costs-against-fiduciary`.

2.6 Building destroyed without tenant fault. If a sudden casualty (fire, storm, collapse, flood) physically injures the
building and leaves it untenantable, the tenant may surrender, owes no rent after it, and rent paid ahead is adjusted
to the surrender date. Gradual wear and decay is not within this rule: `NY:RPL-227`.

---

## Step 3. How the tenancy ends, and when rent stops

3.1 End of a fixed term. The lease ends on its date. If the landlord will not renew, or will raise rent 5% or more,
it must give written notice of 30, 60 or 90 days by length of occupancy: `NY:RPL-226-c(2)`. Late notice extends the
tenancy on its existing terms until the notice period runs, which moves the end date and the rent owed:
`NY:RPL-226-c(1)(a)`.
- Good Cause Eviction applies in NYC: `NY:RPL-212`. For a covered unit, the landlord cannot end the tenancy by not
  renewing without a good-cause ground found by a court, so a non-renewal notice does not start the settlement; it
  starts when the tenant actually leaves or a court orders removal: `NY:RPL-215`. The rule lists all fifteen
  exemptions: `NY:RPL-214`. Those that decide most market-rate units: rent above 245% of HUD fair market rent,
  `NY:RPL-214(15)-high-rent`; a small landlord (ten units or fewer in the state, counted through every natural-person
  owner), `NY:RPL-211(3)-small-landlord`; an owner-occupied building of ten units or fewer; a condominium or co-op
  unit; a building with a certificate of occupancy from 2009 on, for thirty years. For an exempt unit a proper
  non-renewal ends the tenancy, and a tenant who stays owes use and occupancy. The law ends 2034-06-15.
- Automatic renewal. A lease clause renewing the term unless the tenant gives notice binds only if the landlord sent
  written notice of the clause, personally or by registered or certified mail, 15 to 30 days before the tenant's
  notice deadline. Without it the term ends on its date and no renewal rent is owed: `NY:GOL-5-905`.

3.2 Month-to-month tenancy in NYC.
- The landlord must give the 226-c notice periods to end it: `NY:RPL-232-a`. A tenancy at will or by sufferance ends
  on 30 days' written notice: `NY:RPL-228`.
- The tenant may leave at the end of any monthly term without notice, owing rent for each month begun. Both
  Appellate Terms hold this: `NY:COMMONLAW-NYC-monthly-tenant-surrender`. The one-month tenant notice applies only outside NYC: `NY:RPL-232-b`.
- If the lease or another agreement requires notice, the tenant owes rent through the agreed period, subject to
  mitigation: `NY:ADJ-NYC-monthly-agreed-notice`. Month counts: `NY:GCN-30`. A contract date on a weekend or holiday
  moves to the next business day: `NY:GCN-25(1)`, `NY:GCN-25-a(1)-contract-carveout`.

3.2a No stated term. An NYC agreement, oral or written, that fixes a monthly rent and says nothing about how long
the occupancy lasts is presumed month to month from the start: the tenant may leave at the end of any month without
notice and owes nothing after it: `NY:ADJ-RPL-232-monthly-letting`. Where the parties contemplated a longer stay but
did not fix its length ("a long time", "indefinitely"), RPL 232 runs the occupancy to the first October 1 after
possession began, and a tenant who leaves earlier owes rent to September 30, subject to re-letting (`NY:RPL-227-e`):
`NY:RPL-232`, `NY:ADJ-RPL-232-indefinite-term`. After that October 1 the tenancy is month to month:
`NY:ADJ-RPL-232-after-october`. An agreement
that says how it ends governs: `NY:ADJ-RPL-232-agreement-sets-end`. An oral lease for more than a year is void and the
tenancy is monthly from the start: `NY:ADJ-RPL-232-oral-term-over-one-year`. Judgment where the words are in dispute.

3.3 Leaving early. The landlord must take reasonable and customary steps to re-rent at fair market value or the lease
rate, whichever is lower. A new tenant's lease at fair market value or the agreed rate, once in effect, ends the old
one. The landlord carries the burden. Judgment:
`NY:RPL-227-e`. Actual re-renting is not required if the steps were reasonable: `NY:CASE-Toporek-227-e`. A lease
clause waiving mitigation is void: `NY:RPL-227-e-waiver`.
- Agreed early termination. A lease for more than a year ends early only by a writing the landlord or its authorized
  agent signs, or by surrender by operation of law; an oral release does not stop rent, and a no-oral-change clause
  is enforced: `NY:GOL-5-703-15-301-early-termination`.
- Surrender by operation of law. If the landlord and tenant both act in a way that shows they treat the lease as
  ended (for example the landlord takes the unit back for its own use, renovates or combines it for its own account,
  or releases the tenant), the lease and the rent end on that date. Accepting keys and re-letting for the tenant's
  account under 227-e is not surrender. Judgment: `NY:CASE-Riverside-surrender-by-operation`.
- Lease-break charges. A sum the lease fixes for leaving early is owed only if, when the lease was made, it was in
  reasonable proportion to the probable loss and the loss was hard to estimate; otherwise it is a penalty and only
  proven damages are owed. It cannot replace the duty to re-rent, it is never kept from the deposit, and it is not a
  FARE Act fee. On a lease entered into on or after 2022-06-22, the city cap below also applies. Judgment:
  `NY:ADJ-lease-break-charge`.
- A signed writing changes or discharges the lease or a charge without consideration:
  `NY:GOL-5-1103-written-modification`. A typed name, letterhead or e-mail signature adopted to authenticate the
  writing is a signature: `NY:GCN-46-signature`. When a manager or Handoff signs such a writing for the owner on a
  lease of more than a year, it is void unless the owner authorized the agent in writing first:
  `NY:GOL-5-1111-agent-written-authority`; a written management agreement with a licensed broker is that authority,
  without power-of-attorney formalities: `NY:GOL-5-1501C-broker-management-power`. A broker may not induce a tenant to
  break a lease to substitute another: `NY:19NYCRR-175.9-no-induced-breach`.
- Buyouts. An owner-initiated offer of money or other value to leave (a waived balance or a larger refund counts)
  carries eight written disclosures; a written refusal bars new offers for 180 days, and no offer may come with
  threats or abusive contact: `NYC:HMC-27-2004(48)-buyout-offers`. An agreed early termination in which the owner
  gives value and the tenant leaves is a buyout: `NYC:ADC-26-2402-buyout-definition`. It is filed with HPD within 90
  days: `NYC:ADC-26-2403-buyout-filing`, for agreements from 2020-07-01: `NYC:ADC-26-2401-buyout-scope`. A late filing
  is a violation but does not undo the surrender: `NYC:ADC-26-2405-buyout-penalty`.
- Vacating charges are capped (leases entered on or after 2022-06-22). When the tenant left in breach, so the 227-e
  duty to mitigate applies, the landlord recovers at most the fair market cost of preparing the unit's physical
  condition for rental, beyond the rent it proves under 227-e. Re-letting and broker fees, lease-break and
  early-termination sums fixed in the lease, and processing fees are within the cap, so none is recovered on top of
  it. Seeking the amount requires an itemized list of how it was calculated. The cap creates no charge: only damage
  the tenant caused beyond wear and tear is a preparation cost. Judgment on "fair market cost":
  `NYC:ADC-26-3402-vacating-fee-cap`. It applies exactly when 227-e does, never after a lawful termination:
  `NYC:ADC-26-3401-mitigation-definition`.

3.4 Statutory rights to end early (each fixes the end date and bars some charges):
- Senior or disabled tenant moving to care or family: `NY:RPL-227-a(1)`, `NY:RPL-227-a(2)`. Holding belongings for
  later rent is a misdemeanor: `NY:RPL-227-a(3)`.
- Domestic violence victim: `NY:RPL-227-c(1)`, `NY:RPL-227-c(2)`. Pro-rata rent, refund of prepaid amounts within 10
  days: `NY:RPL-227-c(3)(a)-(b)`. A defense to later rent: `NY:RPL-227-c(3)(c)`. No deposit withholding for using the
  right: `NY:RPL-227-c(3)(d)`. Co-tenants keep the tenancy: `NY:RPL-227-c(4)(b)`. The termination must not be
  described as early to a prospective landlord, a collector or any other third party; what goes to a credit bureau is
  governed by the federal accuracy duty, which also bars reporting it as early: `NY:RPL-227-c(5)(b)`. Penalties:
  `NY:RPL-227-c(6)(a)`.
- New York military termination: `NY:MIL-310(2)`.
- Federal servicemember termination (SCRA). A covered lease, `US:50USC3955(b)(1)`, may be ended by written notice
  with orders, `US:50USC3955(a)(1)`, `US:50USC3955(c)`, `US:50USC3955(i)`, including by a reservist on orders,
  `US:50USC3917(a)`, or by survivors, `US:50USC3955(a)(3)-(4)`. It ends for dependents and for every co-tenant:
  `US:50USC3955(a)(2)`, `US:50USC3955(a)(1)-all-parties`. Effective date: `US:50USC3955(d)(1)(A)`,
  `US:50USC3955(d)(1)(B)`. Rent is prorated to that date: `US:50USC3955(e)(1)-prorate`. No early-termination charge:
  `US:50USC3955(e)(1)-no-etf`. Other lease charges, including excess wear, remain: `US:50USC3955(e)(1)-other`.
  Prepaid rent is refunded within 30 days: `US:50USC3955(f)`. Only a court can modify relief: `US:50USC3955(g)`. A
  lease-clause waiver is ineffective: `US:50USC3918`. Holding the deposit or belongings for later rent is a crime:
  `US:50USC3955(h)`. Violations can be sued on: `US:50USC4042`.
- A senior who ended the lease under 227-a to enter a facility may reinstate it by written notice within five business
  days; the tenancy then continues and any new lease is cancelled: `NY:RPL-227-b(5)-(7)-senior-reinstatement`.
- New York military relief reaches a dependent unless the service did not materially impair its ability to comply; the
  landlord decides first: `NY:MIL-301-b-dependents`. No one may ask a servicemember to waive a Military Law right;
  such a waiver does not bind: `NY:MIL-318-no-waiver-request`.
- Federal SCRA. An attorney or attorney-in-fact acts as the servicemember: `US:50USC3920-representatives`, and a
  relative's power continues while the servicemember is missing: `US:50USC4022-poa-missing`. A citizen serving with an
  allied force has SCRA protection: `US:50USC3914-allied-forces`. A dependent may apply to a court for the housing
  protections: `US:50USC3959-dependents`. A lease signed before service is not ended for breach without a court order:
  `US:50USC3952-lease-no-termination-without-order`. A landlord's separate internet, security or gym contract ends on
  relocation orders, without charge, with prepayments refunded in 60 days: `US:50USC3956-landlord-service-contracts`.
- Voucher tenancy. The owner ends the tenancy only for a serious or repeated violation or other good cause, by court
  action with written grounds: `US:24CFR982.310-owner-termination`; every part 982 notice is written:
  `US:24CFR982.5-written-notices`. After 180 days with no family member living there, the assisted lease ends and
  assistance paid for later months goes back to the housing authority, never charged to the family:
  `US:24CFR982.312-absence`. Violence against a voucher tenant is not a ground to end its tenancy:
  `US:24CFR5.2005-hcv-owner-limits`; after the abuser is removed the others have 90 days to establish eligibility:
  `US:24CFR5.2009-bifurcation-remaining-tenant`.

3.5 Staying past the end. A tenant who gave notice and stays owes double rent while staying: `NY:RPL-229`. An
occupant without a lease owes reasonable use and occupancy: `NY:RPL-220`.
A tenant who stays is removed only by a special proceeding; a nonpayment case needs a written 14-day demand carrying
the Good Cause notice: `NY:RPAPL-711-summary-grounds`. The court may stay the warrant up to a year while the occupant
pays use and occupancy into court, which is credited as paid: `NY:RPAPL-753-warrant-stay`.

---

3.6 The building ends the tenancy. If a vacate order issues for conditions the owner was bound to prevent, no rent is
owed after the tenant had to leave, a tenant who left because of it gets back the share of an installment already
paid for the days after the order, and it may also claim damages from the owner: `NY:ADJ-vacate-order-rent`. If the landlord's acts substantially deprived the
tenant of the unit and the tenant left for that reason, no rent or re-letting claim runs after the departure; a lockout
suspends all rent: `NY:COMMONLAW-constructive-eviction`. Judgment. A voucher family may end the tenancy during an HQS
abatement, and the abated assistance is never its debt: `US:24CFR982.404(d)(3)-(4)`.
Ending the tenancy because of a protected class, or harassing the tenant into leaving, is discrimination, and charges
from that departure are offset by the tenant's damages: `US:24CFR100.60(b)(5)-(7)-ending-tenancy`. Wilfully cutting a
service the lease requires, or interfering with quiet enjoyment, is a violation and supports abatement and
constructive eviction: `NY:RPL-235-wilful-service-denial`.

3.7 Retaking the unit. Until the tenant has surrendered (returned the keys or otherwise clearly given up the unit) or
abandoned it, no one may change the lock, remove belongings or keep the tenant out without a warrant or court order.
Each violation is a misdemeanor and a civil penalty of $1,000 to $10,000, and the tenant may recover treble damages:
`NY:RPAPL-768-853-unlawful-eviction`.
While the tenant is still lawfully in occupancy, false statements about the tenancy, baseless cases, removing
belongings or locks, contact at night, on weekends or abusively without written consent, and status-based threats are
harassment; the owner answers for its manager and Handoff. The statutory notices (inspection, statement) may be sent
at any time: `NYC:HMC-27-2004(48)-ending-harassment`.

3.8 After an eviction case. If a summary proceeding came first, sums payable when it began that the judgment did not
award, and use and occupancy to the warrant, are pursued by separate action: `NY:RPAPL-749(3)-after-proceeding`.
A non-renewal within a year after the tenant's good-faith complaint is presumed retaliatory:
`NY:RPL-223-b-retaliation`. A lease term waiving Good Cause rights is void, covered leases carry the Good Cause
notice, and a tenant is never removed because of domestic-violence status: `NY:RPL-218-waiver-void`,
`NY:RPAPL-741(5-a)-231-c-notice`, `NY:RPAPL-744-dv-removal`. A tenant in military service is not evicted without
the court's leave, and on its application the court stays execution of a judgment and any attachment: `NY:MIL-306-309`.
- In a summary proceeding "rent" is only the monthly rent; fees and charges are never sought there:
  `NY:RPAPL-702-rent-only`. The Civil Court may award the rent due at any amount, and what it awards is carried as a
  judgment: `NY:CCA-204-summary-rent-judgment`. Only an attorney, judge or clerk issues the notice of petition, and
  full rent tendered before the hearing must be accepted: `NY:RPAPL-731-issuance-and-tender`. Rent deposited into
  court is credited when released: `NY:RPAPL-745-court-deposit-credit`. A stipulation with an unrepresented party
  binds only after the court's allocution: `NY:RPAPL-746-stipulation-allocution`. The judgment awards costs, which are
  enforced as a judgment and never kept from the deposit: `NY:RPAPL-747-judgment-costs`,
  `NY:CCA-1906-A-summary-costs`. In the housing part a corporate owner may appear by its officer; an LLC or
  partnership needs a lawyer: `NY:CCA-110-housing-part-appearance`.
- A retaliation claim must be brought within one year: `NY:CPLR-215(7)-retaliation-one-year`.

---

## Step 4. Before the tenant leaves: the pre-vacate inspection

4.1 Once either side has given notice of ending (unless the tenant gave under two weeks), the landlord must tell the
tenant in writing, within a reasonable time, of the right to request an inspection and attend. Judgment on
"reasonable time": `NY:GOL-7-108(1-a)(d)-notice`. Sent by email or text, this notice (and the 48-hour notice
below) counts only if a tenant who is a consumer first gave E-SIGN consent (a company tenant needs none); otherwise it goes on paper:
`US:15USC7001(c)-esign-consent`.

4.2 If asked, the inspection is held one to two weeks before the end, on 48 hours' written notice. The landlord then
gives an itemized list of proposed deductions, and the tenant may fix them before leaving:
`NY:GOL-7-108(1-a)(d)-inspection`.

4.3 Missing the inspection notice does not forfeit the deposit. It exposes the landlord to actual damages:
`NY:CASE-Toporek-forfeiture-scope`, `NY:GOL-7-108(1-a)(g)`.

---

## Step 5. Building the account: what may be kept and charged

5.1 What the deposit may be kept for. Only the reasonable, itemized cost of unpaid rent; damage the tenant caused
beyond normal wear and tear; utility charges payable to the landlord under the lease; and moving and storing the
tenant's belongings. Judgment on "reasonable" and "normal wear and tear": `NY:GOL-7-108(1-a)(b)-refundable`. Never
for ordinary wear and tear or a prior tenant's damage: `NY:GOL-7-108(1-a)(b)-excluded-costs`. Never for anything on
the move-in record: `NY:GOL-7-108(1-a)(c)-bar`.
- Repairs in a multiple dwelling are the owner's cost unless the tenant, its household or guest caused the condition,
  which the landlord proves: `NY:MDL-78-repair-allocation`. In a one- or two-family house a written lease may shift
  repair and painting to the tenant, but the deposit still covers only damage beyond wear and tear:
  `NYC:HMC-27-2005(c)-1-2-family-allocation`. A lease clause exempting the landlord from its own negligence is void,
  so damage the landlord caused is never charged: `NY:GOL-5-321-exculpation-void`.
- A no-pet clause is waived in a multiple dwelling after three months of open keeping the owner knew of; actual pet
  damage is still charged: `NYC:HMC-27-2009.1-pet-clause-waiver`. A renewal does not end the tenant's right to remove
  its fixtures: `NY:RPL-226-a-fixture-removal`.

5.2 Fees are not kept from the deposit. Late fees, returned-check fees and other fees are refunded within the 14 days
even if the lease calls them additional rent. A lawful fee may be pursued separately: `NY:ADJ-no-fee-retention`.
- Late fee limits: only after rent is more than 5 days late, at most the lesser of $50 or 5% of monthly rent:
  `NY:RPL-238-a(2)`. Returned check: only if the lease provides, at most the greater of actual cost or $20:
  `NY:RPL-238-a(2-a)`, `NY:GOL-5-328(3)(b)`. Waivers void: `NY:RPL-238-a(3)`.
- No legal fees of any kind (attorney, court, notary, legal administration) without a court order, whatever the
  lease says, since 2021-12-21: `NY:RPL-234-a`, `NY:L2021-c695-s6`, `NY:L2022-c162`. Where a lease lets the
  landlord recover legal fees, the tenant gets the same right, including under a clause for the fees of retaking
  possession after the tenant's default: `NY:RPL-234`.
- A lease clause printed under 8 points (5.5 points for upper case), or not clear and legible, cannot be put in
  evidence by the landlord that prepared it, so a charge resting only on it is not kept or pursued:
  `NY:CPLR-4544-small-print`.
- Key replacement at most 110% of actual cost: `NY:RPL-235-i`.
- A court may refuse to enforce an unconscionable clause (for example a move-out fee or cleaning schedule):
  `NY:RPL-235-c`.
- After a departure in breach on a lease from 2022-06-22, no re-letting, broker, processing or lease-break fee is
  recovered above the fair market cost of preparing the unit (3.3): `NYC:ADC-26-3402-vacating-fee-cap`.
- No extra charge for choosing paper statements or paying by mail: `NY:GBL-399-zzz-paper-fee`. Type size is measured
  by x-height (45% of the point size): `NY:GCN-62-type-size`. A bounced rent check carries only the 238-a
  returned-check fee; for other checks, statutory damages require the two-notice procedure:
  `NY:GOL-11-104-dishonored-check`.

5.3 Painting. Repainting needed after ordinary occupancy (fading, scuffs, small nail holes, paint at the end of its
cycle) is wear and tear and the owner's cost. In a multiple dwelling the owner must repaint every three years:
`NYC:HMC-27-2013(b)(2)`; in a one- or two-family house, whenever needed to keep surfaces sanitary:
`NYC:HMC-27-2013(a)`; `NYC:PAINT-wear-and-tear`. A painting charge is lawful only for proven damage beyond that (tenant-applied colors
needing extra coats, burns, tenant-caused staining, large holes), at the cost of the extra work. A painting and
spackling bill alone does not prove damage. Judgment. HPD's power to order a tenant to repaint during the tenancy
gives no move-out charge: `NYC:HMC-27-2013(c)`.
An electronic payment that fails because of a system malfunction is not late until the malfunction is fixed:
`US:15USC1693j-malfunction-suspends`. A returned-payment fee may be debited electronically only after notice given
before the payment: `US:12CFR1005.3(b)(3)-returned-fee-eft`.

5.4 Move-out service fees (leases signed on or after 2025-06-11). A fee for a move-out service (cleaning, repainting,
lock change, move-out processing) may be charged only if it was on the signed pre-lease fee disclosure. If it was not,
it may not appear on the statement, and DCWP can order restitution: `NYC:FARE-moveout-service-fee`,
`NYC:FARE-20-699.23(c)`. Unpaid rent, proven damage, lease utilities and moving and storage are not fees:
`NYC:FARE-damages-rent-not-fees`. A disclosed fee is still not kept from the deposit (5.2). If the landlord's listing
or leasing agent found or obtained the tenant (a managing agent that did so is one), that agent may not impose or
collect any fee from the tenant at all, disclosed or not, and the landlord is in violation too:
`NYC:FARE-20-699.21-agent-fee-ban`. After a departure in breach, city law also caps every vacating charge (3.3).
DCWP penalties for FARE Act violations run from $375 to $2,000 each, with restitution:
`NYC:RCNY6-6-89-FARE-penalties`.

5.5 Unpaid rent. The deposit may be applied to proven unpaid rent, but only through the timely itemized statement:
`NY:CASE-Mihalow-rent-arrears`, `NY:CASE-Gelbart-rent-offset`. Only rent already due and unpaid when the statement is
sent, and after an early move-out only up to the day before a new tenant's lease begins; later rent is claimed
separately: `NY:ADJ-early-departure-rent-retention`. No rent for a period barred in Step 0.5. Rent claimed for a period when the unit was unfit is
offset by habitability damages: `NY:RPL-235-b`.

5.5a Credits and owner costs.
- A utility bill the tenant paid for the landlord is credited against rent: `NY:RPL-235-a`. Fuel oil the tenant bought
  when the owner failed to supply it is credited too: `NY:MDL-302-c-fuel-credit`. Electricity billed through
  submeters is a lawful charge only under PSC-authorized submetering, and never above the utility's direct-metered rate:
  `NY:16NYCRR96-submetering`. A tenant's own
  added lock carries no charge: `NY:MDL-51-c-tenant-lock`. Rent paid to HPD under a
  levy is credited as paid: `NYC:HMC-27-2147-rent-levy`.
- Turnover work the law puts on the owner is never a charge: lead remediation in a pre-1960 building,
  `NYC:HMC-27-2056.8-lead-turnover`; mold and pest remediation before re-occupancy in a multiple dwelling, and pest and mold work in
  any dwelling, `NYC:HMC-27-2017.5-turnover` (Judgment where the tenant caused the condition); HPD repair charges and penalties,
  `NYC:HMC-27-2128-owner-debt`. A battery-operated detector lost or disabled during the tenancy is charged only
  within the $25/$50/$75 caps, and one replaced at turnover for age or defect is not charged; a hardwired one the tenant
  damaged is charged at the reasonable repair cost; in a class B building no reimbursement is charged at all:
  `NYC:HMC-27-2045-detector-charge`.
- Submetered electricity is charged at no more than the utility's direct-metered residential rate for the same period:
  `NY:16NYCRR-96.1(i)-rate-cap`.
- Submetering conditions: bills within 30 days of the master bill, records six years, time-of-use rates only by
  agreement, and HEFPA protections before any collection of overdue electric charges:
  `NY:16NYCRR-96.6-submeter-charge-limits`. A reading from a meter out of limits is recomputed:
  `NY:16NYCRR-96.7-submeter-accuracy`. While the PSC has suspended the owner's billing authority nothing is charged,
  and a PSC rebilling or reduced cap applies to the final account: `NY:16NYCRR-96.8-noncompliance`. A submetering
  refund that arrives after move-out is credited or paid to the former tenant:
  `NY:16NYCRR-96.5(f)-submeter-refund-credit`.
- Pests and mold are the owner's duty in every dwelling, one- and two-family houses included; only an infestation or
  mold the tenant caused is charged: `NYC:HMC-27-2017.1-pest-owner-duty`. A lease clause shifting that duty to the
  tenant is void, and seeking one is a misdemeanor: `NYC:HMC-27-2017.12-waiver-void`.
- In a class B building the owner maintains and replaces smoke and CO alarms, so no reimbursement is charged; only a
  device the occupant destroyed or took is damage: `NYC:RCNY28-12-03-classB-smoke`, `NYC:RCNY28-12-09-classB-CO`.

5.6 Interest. The remainder returned includes the tenant's interest, less the 1% fee. If the lease ends between bank
interest dates, the landlord pays what it can collect as of the end date: `NY:GOL-7-103(2-b)`,
`NY:GOL-7-103(2)-interest-owed`. Paying or crediting $10 or more of that interest to the tenant in a year needs a Form
1099-INT and a statement to the tenant: `US:26USC6049-deposit-interest`.

5.7 Housing Choice Voucher tenant.
- The deposit may be applied only to the tenant's own share of rent, damages and other lease amounts, subject to
  state law: `US:24CFR982.313(c)`. The tenant never owes the voucher's share, and any excess collected is returned:
  `US:24CFR982.451(b)(4)`.
- The owner keeps the move-out month's assistance payment and gets nothing after: `US:24CFR982.311(d)(1)`.
- Written list and prompt refund: meeting the 14-day state deadline satisfies "promptly": `US:24CFR982.313(d)`,
  `US:24CFR982.313(d)-promptly`.
- A shortfall is collected from the tenant; there is no housing-authority reimbursement: `US:24CFR982.313(e)`,
  `US:24CFR982.452(b)(5)`.
- The HUD tenancy addendum prevails over the lease and is applied first: `US:24CFR982.308-tenancy-addendum`. Rent to
  owner may not rise during the initial term: `US:24CFR982.309-term-rent-freeze`. No extra charge for items
  customarily included in rent or free to unsubsidized tenants: `US:24CFR982.510-other-charges`.
- When the housing authority ends the HAP contract (unit too small, no funding) no assistance is paid after, and the
  family never owes the lost share: `US:24CFR982.403-454-hap-ends`, `US:24CFR982.454-funding-termination`. Assistance
  paid for a period after the move-out month is repaid to the authority, not charged to the tenant:
  `US:24CFR982.453-overpayment-recovery`.

5.7a HRA HOME tenant-based rental assistance. HRA pays for the move-out month and nothing after; later payments go
back to HRA: `NYC:RCNY68-9-10(e)-HOME-TBRA-moveout-month`. The landlord may charge only the lease rent and lease fees
(customary fees need HRA approval) and returns overpayments: `NYC:RCNY68-9-14-HOME-TBRA-charges`. Months HRA abated
for failed inspections are not the household's debt: `NYC:RCNY68-9-09-HOME-TBRA-abatement`. The HOME lease must let
the owner dispose of property left after move-out only under state law and may not make a winning tenant pay fees:
`US:24CFR92.253(b)(2)`.

5.8 Deposits that are not cash held by the landlord.
- HRA security voucher (CityFHEPS, cash assistance): there is no cash deposit to refund. The landlord may claim only
  after move-out, within three months, up to one month's rent, with sworn proof: `NYC:HRA-voucher-claim-window`,
  `NYC:HRA-voucher-proof`. SOTA vouchers pay only for rent unpaid after the first year and damage:
  `NYC:DSS-SOTA-voucher-claim`. The landlord may not ask such households for more than the lease rent and fees:
  `NYC:RCNY68-10-14(a)`. It must notify HRA or DSS within 5 business days of learning the household left, and return
  subsidy for months not occupied: `NYC:RCNY68-10-14(e)`, `NYC:RCNY68-10-14(h)`, `NYC:RCNY31-5-06(a)(10)`.
- A cash deposit paid by the social services official is a GOL article 7 deposit; once the landlord knows the tenant
  assigned the refund to the official, the refund goes to the official and the statement to the tenant:
  `NY:SSL-143-c-agency-deposit-refund`. The district pays a damage claim only after it verifies the damage, by signed
  move-in and move-out condition records or other means: `NY:18NYCRR-352.6(c)(2)-damage-verification`. A knowingly
  false claim to a social services district costs three times the overstatement or $5,000, whichever is greater:
  `NY:SSL-145-b-false-claims`. A landlord paid an allowance to hold an apartment for a homeless family returns the
  unused pro rata part to the district when the family leaves early: `NY:18NYCRR-352.3(i)(7)-pro-rata-return`.
- SOTA payments HRA withheld for conditions are released only if the condition was fixed while the household lived
  there; withheld months are shown as HRA-withheld, not as the household's unpaid rent:
  `NYC:RCNY31-5-07-SOTA-withholding`.

5.9 Disability. An assistance animal is not a pet: pet fees, pet deposits and pet-based deductions must be waived
when the accommodation is necessary and reasonable. Judgment: `US:42USC3604(f)(3)(B)`,
`US:42USC3604(f)(3)(B)-animal-fees`. Actual, documented damage by the animal is chargeable like any damage:
`US:42USC3604(f)(3)(B)-animal-damage`. Restoration of the tenant's own disability modifications may be required
where reasonable: `US:42USC3604(f)(3)(A)`.
Handicap and familial status have the federal definitions: `US:42USC3602(h)-handicap`.

5.10 Equal treatment. Every settlement decision (what is deducted, how strictly damage is assessed, whether a balance
is pursued, reported or written off) applies the same standard to every tenant, whatever the tenant's race, creed,
color, national origin, gender, age, disability, sexual orientation, marital status, immigration status, military
service, children in the household, domestic-violence victim status or lawful source of income (a voucher included):
`US:24CFR100.65-terms`, `NY:EXEC-296(5)(a)(2)-terms`, `NYC:ADC-8-107(5)(a)-terms`, `NY:RPL-227-d-dv-status`. The
state and city exemptions reach only an owner-occupied two-family building (in the city, also not advertised) and
rooms in the owner's or occupant's own home. The owner and manager answer for their agents' discrimination,
including Handoff's and a collector's, and may not interfere with a tenant for using fair-housing rights:
`US:24CFR100.7-3617-liability`; a tenant may recover damages, including punitive damages:
`NY:EXC-297(9)-remedies`.
- Every charge and collection practice is also tested against the state ban on unfair, abusive and deceptive
  practices (from 2026-02-17): `NY:GBL-349-unfair-abusive`. A lease that is not in plain language stays enforceable;
  the tenant recovers actual damages plus $50: `NY:GOL-5-702-plain-language`.
- More equal-treatment rules. The tenant's association with a protected person is protected:
  `NY:9NYCRR-466.14-association`. A payment plan is credit, so its grant and terms may not vary by protected class;
  differences in objective creditworthiness are lawful: `NY:EXEC-296-a-payment-plan`. No worse treatment for
  tenant-group activity: `NY:RPL-230-tenant-group-no-penalty`, or for having children: `NY:RPL-237-a-children-remedy`.
  A licensed broker's discrimination is ground for discipline: `NY:19NYCRR-175.17(b)-broker-discrimination`.
  Deliberately refusing a tenant's self-identified name, pronoun or title in statements and letters violates city law:
  `NYC:RCNY47-2-06-self-identified-name`.
- Federal reach. A neutral policy (a flat charge schedule, automatic referral or reporting, refusing payment plans)
  that falls harder on a protected group is unlawful unless the landlord proves it necessary and no less
  discriminatory practice would serve. Judgment: `US:24CFR100.500-discriminatory-effect`. Quid pro quo or hostile
  harassment in settling or collecting is unlawful. Judgment: `US:24CFR100.600-harassment`. An agent that refuses to
  discriminate may not be penalized: `US:24CFR100.70(d)(1)-agent-refusal`. Occupancy-based charges beyond a reasonable
  occupancy limit are tested as familial-status discrimination: `US:24CFR100.10(a)(3)-occupancy-limits`. A voucher
  tenant who used VAWA rights may not be retaliated against: `US:34USC12494-no-retaliation`. A single-family house
  rented through a manager or Handoff, or any unit in a building of more than four families, is not exempt from the
  federal Act: `US:42USC3603(b)-exemptions`; religious, club and older-persons housing keep narrow exemptions:
  `US:42USC3607-religious-older-persons`. The federal ban on unfair, deceptive or abusive acts does not reach
  collection of a lease balance; it reaches a payment plan only where the landlord is a covered creditor:
  `US:12USC5536-cfpa-udaap-reach`.
- Enforcement. Federal: a HUD complaint within one year, `US:42USC3610-complaint-period`,
  `US:42USC3610-3612-hud-enforcement`; a suit within two years with actual and punitive damages and fees,
  `US:42USC3613-private-action`; Attorney General pattern suits with penalties up to $100,000,
  `US:42USC3614-ag-pattern`; force or threats are a crime, `US:42USC3631-criminal`. City: a court action within three
  years with punitive damages and fees, `NYC:ADC-8-502-private-action`; Commission damages and fees,
  `NYC:ADC-8-120-commission-remedies`, and penalties up to $250,000 for willful practices,
  `NYC:ADC-8-126-civil-penalty`. State: deceptive practices cost up to $5,000 each, `NY:GBL-350-d-civil-penalty`, and
  up to $10,000 more when aimed at tenants 65 or older, `NY:GBL-349-c-elderly-penalty`.

---

## Step 6. The 14-day statement and refund

6.1 The duty. Within 14 days after the tenant vacates, the landlord must give an itemized statement of the basis for
any amount kept and return the rest: `NY:GOL-7-108(1-a)(e)`.
- A creditor of the tenant may levy on or restrain the refund. The landlord then pays the officer or creditor as the
  process directs and is discharged to that extent; the statement still goes to the tenant showing the payment:
  `NY:CPLR-5209-landlord-as-garnishee`. Paying the tenant instead is contempt: `NY:CPLR-5251-disobedience-contempt`.
- An attachment works the same way: the landlord pays the sheriff, serves its garnishee statement within ten days, and
  may assert its lawful deductions against the attaching creditor: `NY:CPLR-6204-landlord-garnishee-attachment`,
  `NY:CPLR-6214-attachment-levy`, `NY:CPLR-6219-garnishee-statement`.

6.2 When the tenant vacated. Where disputed, it is a question of fact shaped by the lease, for example belongings
left behind: `NY:CASE-Urban-vacatur`. Keeping keys a few days past the end is not by itself a failure to surrender:
`NYC:CASE-Pezzo-surrender`. With co-tenants, the day the last one leaves: `NY:ADJ-cotenants-vacated`. A
servicemember's clock also runs from vacating, not from the SCRA termination date:
`US:50USC3955-deposit-clock-NY`. Judgment.
An occupant the tenant left behind is removed only by a proceeding after a ten-day notice; the tenant's vacating date
and the 14 days are not delayed by the occupant's stay, and the occupant's use and occupancy is its own debt:
`NY:RPAPL-713-occupant-after-tenant`.

6.3 Counting. Calendar days, excluding the vacating day; if day 14 is a Saturday, Sunday or public holiday, the next
business day: `NY:GCN-110`, `NY:GCN-19`, `NY:GCN-20`, `NY:GCN-20-event-day`, `NY:GCN-25-a(1)`, `NY:GCN-24`. The
Appellate Division applies this count (vacated July 24, due August 7): `NY:CASE-Cohen-deadline-count`.
The deadline runs on New York time: a statement e-mailed after midnight New York time on day 14 is late, wherever the
sender is: `NY:GCN-53-deadline-clock`. Daylight saving follows the federal dates, second Sunday in March to first
Sunday in November: `NY:GCN-52-standard-time`. A year is twelve months: `NY:GCN-58-year`.

6.4 What the statement must be. Written: letter, email, text or other writing. A phone call is not enough:
`NY:CASE-Bogom-Shanon-written`. It is provided on the day it is sent, with the refund, to the tenant:
`NY:ADJ-provide-written-dispatch`. A statement by email or text needs no E-SIGN consent, because the statute does
not require it 'in writing' and the courts accept email and text: `NY:ADJ-statement-electronic`. Estimated costs for work not yet done are allowed if each item is itemized with
its estimate; there is no follow-up statement, and any excess is a separate claim: `NY:CASE-Toporek-estimate`.
- A refund check suspends the refund until it is paid: a dishonored refund check not replaced within the 14 days means
  the deposit was not returned on time; a cashier's or teller's check discharges it on delivery:
  `NY:UCC-3-802-check-suspends-obligation`. A lost refund check is replaced; a court requires the tenant to post
  security before it recovers without the check: `NY:UCC-3-804-lost-refund-check`. An agent signing the check names
  the owner and shows its capacity, or is personally liable: `NY:UCC-3-403-agent-signature`.
- E-SIGN consent is owed only to a consumer; a company tenant may be sent records electronically without it:
  `US:15USC7006-esign-consumer`. No statement or letter may express a preference or limitation by protected class (a
  charge blamed on "the children"): `US:24CFR100.75-statements`. Business stationery may not carry the U.S. or New
  York flag: `NY:GBL-136(c)-no-flag-on-business-stationery`.

6.5 Where to send it.
- If the landlord has a forwarding address, an email address or a phone number, it must use them: a statement by
  email or text message is a written statement. Mailing to the vacated unit when
  another channel is known is not providing the statement: `NY:ADJ-provide-address-branches`,
  `NY:CASE-Pickens-provide`.
- With no channel at all, the landlord sends to the vacated unit within the 14 days. Waiting for an address forfeits:
  same rule. Whether the wait is willful is decided under 7.5.
- The multiple dwelling's emergency contact list is for evacuation only and is never a source for the statement,
  skip-tracing or collection: `NY:MDL-15-emergency-list-use`. No one may obtain a tenant's telephone records from a
  phone company without written authorization: `NY:GBL-399-dd-phone-records`.
- Payment channels. Regulation E binds a landlord, manager or Handoff that is not the tenant's bank only for check
  conversion, returned-item fees, recurring-debit authorization and notice, no compulsory autopay for credit, and
  records; a refund pushed by ACH to the tenant's account carries no Regulation E duty:
  `US:12CFR1005.3(a)-payee-duties`. A payment the tenant starts each time is not preauthorized, and a one-off refund
  prepaid card is not a gift card: `US:12CFR1005-cmt-2(k)-1-one-time-payments`.
- A tenant under guardianship. Deal with the guardian only within the powers its commission lists, which the landlord
  sees first: `NY:MHL-81.27-commission`, `NY:MHL-81.21-guardian-property-powers`. The tenant keeps every power not
  given to the guardian, and a court may undo an agreement the tenant made while incapacitated:
  `NY:MHL-81.29-retained-rights`. A temporary guardian acts only within its order, and a court may bar anyone from
  taking payment from the tenant: `NY:MHL-81.23-temporary-guardian`. A special guardian acts only for the transaction
  its order names: `NY:MHL-81.16-special-guardian`. When a guardian leaves office the standby, interim or successor
  guardian acts: `NY:MHL-81.38-interim-standby`.

6.6 Co-tenants. The statement goes to each co-tenant. The refund depends on what the landlord's records show:
`NY:ADJ-cotenants-payee`.
- One deposit with no record of who paid what: the refund is joint. Pay all co-tenants together or as all of them
  direct in writing; paying the whole to one of them also discharges the landlord.
- Records show each co-tenant paid an identified part: each owns that part. Deductions come out of the whole deposit,
  and the remainder is paid to each in proportion to what he paid, unless all direct otherwise in writing. Paying the
  whole to one co-tenant does not discharge the landlord as to the others.
- A single check to several co-tenants: payable "A or B" lets one take the whole, so where records show separate
  shares pay separate checks or one payable "A and B": `NY:UCC-3-116-cotenant-refund-check`.
- Competing claims to the refund. The landlord may interplead the claimants, pay into court and be discharged:
  `NY:CPLR-1006-interpleader`, in the Civil Court up to $50,000: `NY:CCA-205-interpleader`; money paid out of court
  carries a 2% fee: `NY:CPLR-8010-court-fund-fee`. When sued by one claimant while another cannot be served, it may
  give the absent claimant notice, which starts a one-year period for that claimant:
  `NY:CPLR-216-adverse-claimant-notice`. Money owed on a claim of an infant, incompetent or conservatee goes to its
  guardian, committee or conservator, not to the person: `NY:CPLR-1206-proceeds-payee`.

6.6a An agent for the tenant. A New York power of attorney is valid only with the statutory formalities, and one valid
where it was signed is valid here: `NY:GOL-5-1501B-poa-validity`, `NY:GOL-5-1512-foreign-poa`. It survives the
tenant's incapacity unless it says otherwise: `NY:GOL-5-1501A-durable-poa`. With the right grant the agent may end the
lease, receive the refund and settle claims: `NY:GOL-5-1502A-agent-lease-authority`,
`NY:GOL-5-1502H-agent-claims-authority`. The landlord honors or rejects a presented power within ten business days,
and a reasonable acceptance protects it; the statement still goes out on time and the refund is held in trust
meanwhile: `NY:GOL-5-1504-accept-poa`. The agent signs as agent: `NY:GOL-5-1507-agent-signature`; co-agents act
jointly: `NY:GOL-5-1508-co-agents`. A payment made without actual notice that the power ended binds the tenant and its
estate: `NY:GOL-5-1511-termination-notice`.

6.7 Tenant in bankruptcy. If the tenant filed before the deposit was applied, applying it to pre-filing charges is a
setoff stayed by the bankruptcy: `US:11USC362(a)(7)`, `US:11USC362(a)(7)-deposit-is-setoff`. The landlord may hold
the disputed part temporarily while it promptly asks the court for relief: `US:CASE-Strumpf-hold`. The statement is
still sent, without demanding a pre-filing balance. The refund is estate property: once the landlord knows of the
case, it is paid to the chapter 7 trustee (or as the trustee directs), or in chapter 13 to the tenant as debtor.
Paying a chapter 7 debtor after notice does not discharge the landlord, unless the refund is exempt or abandoned,
or the case is dismissed (below): `US:11USC542-refund-payee`.
- Which charges are stayed. Charges for time before the petition, including damage done before it but assessed later,
  are pre-petition claims; rent for time after it and damage done after it are post-petition debts. A residential
  balance owed by an individual is a consumer debt. Judgment: `US:11USC101(5)-charge-timing`.
- Notice. A debtor's notice is effective only at the address the landlord gave in two recent communications or filed
  with the court; no damages run for conduct before effective notice, but actual knowledge of the case is enough:
  `US:11USC342-effective-notice`.
- Who is paid the refund besides the trustee. A refund the tenant claims exempt goes to the tenant once no objection
  is filed within 30 days after the creditors' meeting; New York exempts a residential security deposit without dollar
  limit: `US:11USC522-refund-exemption`, `US:FRBP4003-exemption-objection`. A refund the trustee abandons, or that was
  scheduled and not administered when the case closed, goes to the tenant: `US:11USC554-abandoned-refund`. On
  conversion from chapter 13 to 7 an unpaid refund goes to the new trustee, and charges from the chapter 13 period
  become pre-petition: `US:11USC348-conversion`.
- Stay relief to apply the deposit is sought by motion; the stay ends 30 days after the motion unless continued, and
  an order granting relief waits 14 days, so the deposit is applied on day 15. A stipulation with the debtor needs
  court approval: `US:FRBP4001-stay-relief-procedure`.

6.8 Unclaimed refund. It stays the tenant's trust money. After three years unclaimed, it is reported and paid to the
State Comptroller: `NY:OSC-MS11-refunds-due`, `NY:ABP-1315(2)`. It is reported even if the tenant's claim is
time-barred, records are kept five years, and wilful failure costs $100 a day: `NY:ABP-1400-1412-reporting`. A licensed real-estate company holding it in escrow
reports it under code TR04, also after three years: `NY:OSC-TR04-broker-escrow`. At least 90 days before reporting, the landlord
mails the tenant a notice at the address it has (and a certified-mail notice 60 days before if over $1,000, whose
cost may be deducted from the refund), unless its only address is the vacated unit: `NY:ABP-1422`.
- Once paid to the Comptroller, the landlord is discharged: `NY:ABP-1404-holder-discharged`, and interest stops at
  that date: `NY:ABP-1405-no-interest-after-payment`. No dormancy or handling charge comes off the refund:
  `NY:ABP-1415-no-dormancy-charges`. An owner entity from another state not authorized here reports the same way:
  `NY:ABP-1312-foreign-holder`. Refunds of $20 or less may be reported in aggregate but are all delivered:
  `NY:ABP-1419-aggregate-small`. A wilful false report is perjury: `NY:ABP-1413-false-report`.

6.9 Belongings left behind. They stay the tenant's. The landlord may not hold them for rent and must allow retrieval.
It owes no duty of care unless it agreed to keep them: `NY:COMMONLAW-belongings-owner-keeps`, `NY:CASE-Facey-belongings`.
It may dispose of them only once they are abandoned, shown by the tenant's words or conduct or by written notice with
a stated period and no response for a substantial time. Judgment: `NY:COMMONLAW-belongings-abandonment`. Before
surrender or abandonment, removing them is unlawful eviction (3.7). No city rule
adds to this: `NYC:ABANDONED-city-layer`. Reasonable moving and storage cost may be kept from the deposit (5.1).
For a servicemember, selling or applying left belongings to a debt enforces a lien and needs a court order:
`US:50USC3958(a)`, `US:50USC3958-lien-enforcement`. Distress was abolished in New York, so the federal distress rule
does not arise: `US:50USC3951-distress-NY`.
A lease clause pledging exempt belongings for rent is void: `NY:RPL-231-illegal-use-and-exempt-pledge` (use of the
unit for an illegal business also voids the lease). A New York servicemember's stored goods may not be sold or held
for storage charges without a court order: `NY:MIL-316-a(2)-storage-lien`.

6.10 Data at move-out. In a smart access building, the owner and any third party running the system remove or
anonymize the departed tenant's reference data within 90 days: `NYC:ADC-26-3002(c)-moveout-data`. Whoever holds the
bank details used for an electronic refund keeps reasonable safeguards, including secure disposal:
`NY:GBL-899-bb-safeguards`. A breach is notified to affected tenants within 30 days: `NY:GBL-899-aa-breach-notice`.
The closed file is disposed of by shredding or making the personal information unreadable: `NY:GBL-399-h-disposal`;
consumer-report information in it follows the federal disposal rule instead (below).
Smart-access data is not sold or disclosed, for example to a collector, except as the law allows:
`NYC:ADC-26-3003-3006-data-sale`. No mailing shows the tenant's social security number: `NY:GBL-399-ddd-604-a`.
Court filings redact social security and account numbers to the last four digits, birth dates to the year and minors'
names to initials: `NY:22NYCRR-202.5(e)-redaction`, `NY:22NYCRR-208.4(b)-redaction`. A consumer report from the
application may be passed only to someone with a legitimate business need in a transaction with the tenant, such as
Handoff or a collector: `NY:GBL-380-i(c)-report-redisclosure`.
No one may require the tenant's social security number, or withhold the refund for refusing it, except where a listed
exception applies (the 1099-INT for deposit interest, a lawful report pull, fraud checks):
`NY:GBL-399-ddd2-ssn-demand`. Consumer-report information in the closed file is disposed of under the FTC disposal
rule: `US:15USC1681w-disposal`. A DCWP-licensed collector also sends DCWP a copy of any breach notice:
`NYC:ADC-20-117-breach-copy-to-DCWP`, `NYC:RCNY6-6-85-breach-copy-penalty`. A voucher tenant's VAWA documentation and
status are confidential and never passed to a collector or credit bureau without written consent; the owner may ask
for documentation in writing, with 14 business days to respond: `US:24CFR5.2007-documentation-confidentiality`.
Consumer-report information (the screening report and anything derived from it) is disposed of by reasonable measures:
shredding or burning paper, destroying or erasing electronic media, or a vetted destruction contractor:
`US:16CFR682.3-disposal`.

---

## Step 7. Consequences of getting it wrong

7.1 Forfeiture. Missing the 14-day statement and refund forfeits any right to keep any part of the deposit. No intent
is needed: `NY:GOL-7-108(1-a)(e)-forfeiture`.

7.2 The debt survives. Forfeiture takes the security, not the debt. The landlord still recovers proven rent and damage
by separate suit, counterclaim or setoff against the tenant's judgment: `NY:ADJ-forfeiture-claims-survive`,
`NY:CASE-Levine-counterclaim` (Appellate Term, First Department, 2026), `NY:CASE-Masseroli-separate-claim`,
`NY:CASE-Pickens-provide`.

7.3 Commingling. Mixing the deposit with the landlord's money (proved, or inferred from no bank notice) forfeits the
deposit at once, even if the tenant breached (both the First and Second Departments), but rent claims survive: `NY:CASE-Paterno-commingling-forfeiture`,
`NY:CASE-Paterno-rent-survives`.

7.4 Burden. In any dispute over the amount kept, the landlord proves it was reasonable: `NY:GOL-7-108(1-a)(f)`.

7.5 Damages. Actual damages (the deposit wrongly kept), and for a willful violation up to twice the deposit:
`NY:GOL-7-108(1-a)(g)`. "Willful" has two parts. The failure must be knowing, intentional or deliberate;
negligence and inadvertence are not willful. And knowledge of the law is charged to an experienced landlord or its
managing agent (every account a manager or Handoff handles), so a deliberate choice to keep the deposit without a
timely written statement is willful whatever its reading of the law. A miss from an honest process error (a misdated
send, a failed delivery, a channel the tenant supplied that never reached the manager's records) is not willful, even
for a manager. A manager that deliberately holds the statement waiting for an address is charged with knowing the
14-day rule has no such exception, which is evidence of willfulness; whether the violation is willful, and the amount
up to twice the deposit, is found on the whole record. Judgment: `NY:ADJ-willful-standard`, `NY:CASE-Prando-willful`, `NY:CASE-Karole-willful`,
`NY:CASE-Bogom-Shanon-willful`.
A deposit judgment resting on a willful breach of the trust (commingling, willful withholding) is enforced by contempt
as well as execution: `NY:CPLR-5105-fiduciary-contempt`.

7.6 The tenant's claims. The tenant has three years to sue for the punitive damages, or for a deposit recoverable only
because of the forfeiture, and six years for a deposit kept without a lawful basis, both from the end of the 14 days:
`NY:ADJ-tenant-deposit-claim-limitations`. Military service, the tenant's bankruptcy (two more years for its
trustee) and death extend these: `US:11USC108(a)-debtor-claims`. A tenant who had moved out of state by the end of the 14 days is
also held to its new state's period (8.13(c)). Keep the settlement file until the latest of those
dates. A tenant may sue in NYC small claims up
to $10,000 wherever the landlord lives: `NY:CCA-1801-tenant-claim`. A business that leaves a small-claims judgment
unpaid 30 days after notice, with two other unpaid ones from the same business, faces treble damages:
`NY:CCA-1812-treble`. A landlord settling the tenant's suit pays within 21 days of the release and stipulation:
`NY:CPLR-5003-a-settlement-payment`.
- A tenant's attorney has a lien on the deposit claim and any settlement; after notice of the lien, pay the tenant and
  attorney jointly or as the attorney directs: `NY:JUD-475-attorney-lien`, `NY:JUD-475-a-notice-of-lien`.
- A city discrimination complaint to the Commission is due within one year: `NYC:ADC-8-109-commission-complaint`. A
  winding-up owner partnership pays or reserves for the tenant's claim before partners:
  `NY:PTR-121-804-creditors-before-partners`.

7.7 Other liability. A payee that breaks a Regulation E duty owes actual and statutory damages ($100 to $1,000) and
fees, within one year: `US:15USC1693m-civil-liability`; a knowing and willful violation is a crime:
`US:15USC1693n(a)-criminal`. The Attorney General may seek SCRA penalties up to $55,000, and $110,000 for a later
violation: `US:50USC4041-ag-penalties`; SCRA remedies add to state-law damages: `US:50USC4043-other-remedies`. A
voucher tenant enforces the lease and the tenancy addendum, not the HAP contract:
`US:24CFR982.456-tenant-enforcement`.

---

## Step 8. A balance beyond the deposit: collecting it

8.1 What the balance is.
- Under state law it is a lease claim, not consumer credit, because both CPLR 105(f) and GBL 600(1) require credit
  offered or extended and a lease exchanges possession for rent (the statutes' text; Romea, Second Circuit;
  Lefferts). So the state collection-conduct law (GBL art. 29-H) does not apply, nor does the state collection
  regulation for third-party collectors, `NY:23NYCRR-1.1(d)-not-lease`, and today the landlord has six years to sue (an owner based outside New York is also held to its home state's
  period, 8.13(c)): `NY:ADJ-lease-balance-not-consumer-credit`, `NY:CASE-Lefferts-rent-not-consumer-credit`, `NY:CPLR-213(2)`,
  `NY:CPLR-214-i`. The Consumer Debt Uniformity Act passed both houses in June 2026 and has not been delivered to the Governor; from its
  90th day as law, a suit on a lease balance against a person must begin within three years:
  `NY:CPLR-214-i-consumer-debt-S9760`.
- Under federal law, rent and every other lease charge owed by a person is a "debt": `US:15USC1692a(5)`,
  `US:15USC1692a(5)-lease-charges`, `US:CASE-Romea-1998`. A non-party guest's damage is not that guest's debt:
  `US:15USC1692a(5)-non-party-tort`. The owner is the creditor: `US:15USC1692a(4)`.
- A guarantor is liable only on a guaranty in a writing it signed, and an individual guarantor has the same collection
  protections as the tenant: `NY:GOL-5-701(a)(2)-guaranty`.
- Under city law, a former tenant's balance is a consumer debt, so DCWP's collection rules apply to whoever collects
  it: `NYC:CPL-20-700`, `NYC:CPL-tenant-balance-consumer-debt`, `NYC:ADC-20-489(d)`.
- Who else owes the balance. A judgment against some co-tenants does not discharge the others:
  `NY:GOL-15-102-judgment-not-discharge`. A guarantor stays liable though the landlord does not sue the tenant:
  `NY:GOL-15-701-guarantor-not-discharged`. A spouse who did not sign owes nothing: `NY:GOL-3-305-spouse-not-bound`. A
  parent owes up to $5,000 for a minor child's wilful damage: `NY:GOL-3-112-parent-liability`. A tenant served with a
  third party's suit for the unit who does not tell the landlord forfeits three years' rent, claimed by action:
  `NY:RPL-225-notice-of-adverse-action`.
- A deceased tenant's heirs and beneficiaries owe the balance only up to what they received, only after the estate is
  shown unable to pay, in the statutory order and ratably: `NY:EPTL-12-1.1-distributee-liability`,
  `NY:EPTL-12-1.2-order`, `NY:EPTL-12-1.3-ratable`. A claim not yet fixed at death is protected by a contingent-claim
  affidavit: `NY:SCPA-1804-contingent-claim`.
- A written release of the balance, sent to the tenant, ends it; an internal write-off does not:
  `NY:GOL-15-303-written-release`.
- A person who says the tenancy was opened in its name by identity theft gets the application and payment records free
  within 30 days of a verified request: `US:15USC1681g(e)-victim-records`.

8.1a Coerced debt (from 2026-06-17). If a former tenant says all or part of the balance was incurred through an abuser's
coercion and gives a sworn statement with a police report, court order or other listed document, collection stops
within ten business days and a review
follows within thirty business days without contacting the accused person; a decision to resume goes to the tenant in
writing within five business days. If the tenant gives no documents, the landlord sends the statutory notice text.
The 14-day statement still goes out, itemizing without demanding the disputed part. Coercion is a defense to a suit:
`NY:GBL-604-bb-coerced-debt`, `NY:GBL-604-cc-coerced-defense`. The statute's credit-bureau notice does not bind a furnisher (8.7).
The coerced-debt rules apply in full to a lease balance; the deposit is not collateral:
`NY:GBL-604-dd-lease-balance-not-secured`. The landlord may sue the person who coerced the debt for the coerced amount
and fees within three years: `NY:GBL-604-ee-claim-against-coercer`.

8.1b Payments and settlements.
- A check marked "payment in full" for less than a disputed balance settles it if cashed without an explicit
  reservation of rights; with one ("under protest"), the rest stays owed: `NY:UCC-1-308-full-payment-check`.
- Settling with one co-tenant or a guarantor releases the others to the extent the statute provides unless the
  release expressly reserves rights against them: `NY:GOL-15-104-105-cotenant-release`.
- A signed promise after the balance accrued not to plead the limitation period is effective; one in the lease is
  not: `NY:GOL-17-103-limitations-promise`.
- Assigning the balance to Handoff, an affiliate or a collector so it can sue in its own name is champerty and void as
  a basis for suit; collection as the owner's agent is not: `NY:JUD-489-champerty`.
- A settlement of a pending case binds only in a signed writing, in open court, or as an order:
  `NY:CPLR-2104-stipulations`. A discontinuance is filed within 20 days: `NY:22NYCRR-208.16-file-discontinuance`,
  `NY:CPLR-3217-discontinuance`. Settlement talk is inadmissible to prove the amount, but the itemized statement is
  not settlement talk: `NY:CPLR-4547-compromise-inadmissible`. What the manager, Handoff or a collector says about the
  account can be used against the landlord, so it says only what the file supports: `NY:CPLR-4549-agent-statements`.
- Offers and tenders. A signed offer to settle for a stated sum becomes binding once the other side tenders it before
  revocation, so an offer states a deadline: `NY:GOL-15-503-offer-of-accord`; a signed offer stated to be irrevocable
  cannot be withdrawn meanwhile: `NY:GOL-5-1109-irrevocable-offer`. In a suit a party may tender payment into court,
  offer judgment for a sum, or offer damages if liable; a party that rejects and does no better pays the other's later
  costs: `NY:CPLR-3219-tender`, `NY:CPLR-3221-offer-to-compromise`, `NY:CPLR-3220-conditional-offer`; in the Civil
  Court the offer is filed with the clerk: `NY:CCA-802-tender-offer`.
- A confession of judgment states the facts and the 2% rate where it applies, is filed within three years in the
  county of the tenant's residence (the Civil Court for sums within its limit), and is never entered after the
  tenant's death: `NY:CPLR-3218-confession`, `NY:CCA-1403-confession-civil-court`.
- Settling with an infant, incompetent or conservatee tenant needs court approval on the representative's papers; the
  landlord's attorney never represents the tenant: `NY:CPLR-1207-incapacitated-settlement`,
  `NY:CPLR-1208-incapacitated-settlement-papers`, `NY:22NYCRR-208.36-incapacitated-settlement`, and a committee or
  conservator compromises only with court authority: `NY:DCL-251-committee-compromise`.
- Co-obligors. A payment by one co-tenant or guarantor is credited to all: `NY:GOL-15-103-payment-credited`. The title
  15 rules reach contract obligors only, not a guest liable in tort: `NY:GOL-15-101-contract-only`.
- A settlement of a dispute involving discrimination may not require the tenant to pay for breaching confidentiality
  or to disclaim discrimination: `NY:GOL-5-336(3)-discrimination-release`.
- Transferring the balance. It is assignable; the buyer takes it subject to the tenant's defenses, including the
  deposit claim: `NY:GOL-13-101-105-balance-transfer`. Payments to the landlord before notice of the transfer bind the
  buyer: `NY:GOL-13-105-notice-of-transfer`. A gratuitous assignment must be in a signed writing:
  `NY:GOL-5-1107-written-assignment`. A transfer in payment for services or an existing debt is not champerty:
  `NY:JUD-490-champerty-exception`. A collection attorney may not buy the claim to sue on it or pay for the referral:
  `NY:JUD-488-attorney-buying-claims`.
- Payment plans. A plan is a forbearance: interest (all charges for the forbearance) is capped at 16% a year,
  `NY:GOL-5-501-payment-plan-usury`; a usurious plan is void, though the lease claim itself survives,
  `NY:GOL-5-511-usurious-void`; the tenant recovers the excess without first repaying, `NY:GOL-5-513-recover-excess`,
  `NY:GOL-5-515-no-tender`; returning the excess ends further penalty, `NY:GOL-5-519-return-discharges`; a corporate
  tenant cannot plead civil usury, `NY:GOL-5-521-corporate-tenant-usury`.
- Payment plans under federal law. Any plan charge (interest, set-up fee) is a finance charge; a landlord that
  regularly offers such plans, or plans of more than four installments, is a TILA creditor and gives the closed-end
  disclosures: `US:15USC1605-plan-finance-charge`; plans with a company tenant or over $50,000 are exempt:
  `US:15USC1603-plan-exemptions`; unearned interest is refunded on prepayment: `US:15USC1615-unearned-interest`;
  wilful violations are crimes: `US:15USC1611-criminal`. The federal consumer-finance agency law does not reach the
  landlord's own plan unless it sells the plan before default, the credit exceeds the tenancy's value, or it regularly
  charges finance charges and is not a small business: `US:12USC5517(a)(2)-landlord-credit`. A plan refused or
  worsened because of a credit report requires an adverse-action notice: `US:15USC1681m(a)-adverse-action`.
- Electronic payments. A plan may not require autopay: `US:15USC1693k(1)-payment-plan-autopay`. Recurring debits need
  a signed or authenticated written authorization and a copy to the tenant: `US:15USC1693e(a)-autopay-authorization`;
  a debit of a different amount needs ten days' notice: `US:12CFR1005.10(d)-varying-debit-notice`; converting a paper
  check into a debit needs notice first: `US:12CFR1005.3(b)(2)-check-conversion`. These reach only natural persons'
  consumer accounts: `US:12CFR1005.2-reach`. Records are kept two years: `US:12CFR1005.13(b)-records`, and waivers are
  void: `US:15USC1693l-no-waiver`. Card acceptance limits are posted and follow GBL 518:
  `NYC:RCNY6-5-24-card-payments`.
- TILA part B. A landlord that is a TILA creditor gives the tenant the closed-end disclosures before the plan starts,
  to one primary obligor where several are liable: `US:15USC1631-plan-disclosure-duty`,
  `US:15USC1638-closed-end-disclosures`, clearly and conspicuously, with the APR and finance charge most prominent:
  `US:15USC1632-disclosure-form`. A failure costs actual damages plus twice the finance charge ($200 to $2,000) and
  fees, sued on within a year but usable later as a set-off when the landlord sues on the plan:
  `US:15USC1640-tila-civil-liability`. A buyer of the plan answers only for violations apparent on the face of the
  disclosures: `US:15USC1641-assignee-liability`.

8.2 Who is a federal "debt collector". This decides whether the FDCPA and Regulation F apply.
- An owner collecting its own balance in its own name is not one: `US:15USC1692a(6)-regularly-another`,
  `US:CASE-Henson-2017`, `US:12CFR1006-cmt-2(i)-1`, `US:12CFR1006.1(c)(1)`. Nor are its officers and employees:
  `US:15USC1692a(6)(A)`, or an affiliate collecting only for related owners: `US:15USC1692a(6)(B)`.
- An owner using another name that suggests a third party is collecting becomes one: `US:15USC1692a(6)-false-name`.
  Anyone supplying such forms without really collecting is liable: `US:15USC1692j(a)`.
- A business whose principal purpose is collecting is one: `US:15USC1692a(6)-principal-purpose`.
- A manager collecting as a minor part of broad management duties is excluded; a collections-only engagement is not.
  Judgment: `US:15USC1692a(6)(F)(i)`, `US:15USC1692a(6)(F)(i)-manager-incidental`,
  `US:15USC1692a(6)(F)(i)-collection-only`.
- Anyone who took on the account before it was in default is excluded for that account: `US:15USC1692a(6)(F)(iii)`,
  `US:15USC1692a(6)(F)(iii)-moveout-branches`. A move-out balance is not in default on its due date. It defaults when
  the lease's grace period runs or the owner treats it as in default (for example, referral to a collector):
  `US:15USC1692a(6)(F)(iii)-default-meaning`. Judgment.
- Handoff, by engagement: before default, not a debt collector for that account: `US:HANDOFF-config-pre-default`;
  after default, one if it regularly collects for others: `US:HANDOFF-config-post-default`; owner letters in
  Handoff's name without real collection work: `US:HANDOFF-config-owner-name-only`; by principal purpose:
  `US:HANDOFF-config-principal-purpose`; buying balances: `US:HANDOFF-config-owns-balance`. Which one applies is a
  later operating choice.
- New York has no state exemption; federal and stricter state or city rules both apply: `US:15USC1692o`,
  `US:15USC1692o-NY-VA-none`, `US:15USC1692n`.
- A letter sent under a name meant to mislead the tenant about who sends it is a state misdemeanor:
  `NY:GBL-133-deceptive-name`. Furnishing a form that suggests a third party collects when none does is a city
  deceptive practice, whether or not the sender is a federal debt collector: `NYC:RCNY6-5-78-deceptive-forms`.
- A balance reported as identity theft may not be sold or placed for collection, and a collector told it may be
  fraudulent tells the landlord: `US:15USC1681m(f)-(g)-identity-theft-debt`.

8.3 What a federal debt collector must do.
- Communications: `US:15USC1692a(2)`. Finding a tenant with no forwarding address: `US:15USC1692b`. Timing, place,
  represented tenants: `US:15USC1692c(a)`. No discussion with third parties such as a roommate or the new occupant:
  `US:15USC1692c(b)`. Stop on a written refusal: `US:15USC1692c(c)`; who counts as the consumer: `US:15USC1692c(d)`.
- Calls with a prerecorded or artificial voice, or from equipment that dials random or sequential numbers, to the
  tenant's cell phone need its prior consent; a revocation by any reasonable means is honored within ten business
  days; $500 to $1,500 per call: `US:47USC227-TCPA`. This binds every caller, not only debt collectors.
- No harassment: `US:15USC1692d`; call limit presumption, 7 calls in 7 days: `US:12CFR1006.14(b)(2)`. Email and text
  opt-out: `US:12CFR1006.6(e)`; no employer email or public social media: `US:12CFR1006.22(f)(3)-(4)`; passing on
  the tenant's email at hand-off: `US:12CFR1006.6(d)(3)-(4)`.
- Truth: the amount and status must be true, so a forfeited deposit, a wear-and-tear charge or a voucher share
  misstates it: `US:15USC1692e(2)(A)`. A notice stating a balance on which interest or fees accrue must say the
  balance may increase: `US:CASE-Avila-accruing-balance`. Threats only of lawful, intended action: `US:15USC1692e(5)`. Disputed debts
  reported as disputed: `US:15USC1692e(8)`. Required disclosures: `US:15USC1692e(11)`. True business name:
  `US:15USC1692e(14)`. Only amounts the lease or law allows: `US:15USC1692f(1)`. Envelope rules:
  `US:15USC1692f(7)-(8)`.
- Validation notice within 5 days of first contact: `US:15USC1692g(a)`, `US:12CFR1006.34(a)(1)`,
  `US:12CFR1006.34(c)`, `US:12CFR1006.34(d)(2)`. Itemization date (the move-out statement can be the "last
  statement"; judgment): `US:12CFR1006.34(b)(3)`. Validation period: `US:12CFR1006.34(b)(5)`. A lease balance is not a
  consumer financial product, so two notice items are optional: `US:12CFR1006.1(c)(2)`, `US:12USC5481(15)(A)(ii)`.
  The city's own itemization may substitute: `US:12CFR1006-cmt-34(c)(2)(viii)-2`.
- Delivery: mailing to the vacated unit when the collector knows the tenant moved is not safe-harbor delivery:
  `US:12CFR1006.42(a)(1)`. Electronic delivery needs E-SIGN consent: `US:12CFR1006.42(b)`.
- Disputes: stop until verification is sent: the lease terms and the itemized statement that establish each charge:
  `US:15USC1692g(b)`, `US:12CFR1006.38(d)(2)`. Nothing that overshadows dispute rights: `US:12CFR1006.38(b)`.
- Suits: only where the tenant signed or lives: `US:15USC1692i(a)`. No suit or threat on a time-barred debt:
  `US:12CFR1006.26(b)`. Keep records three years: `US:12CFR1006.100(a)`.
- Liability: actual and statutory damages, fees: `US:15USC1692k(a)`; bona fide error defense: `US:15USC1692k(c)`;
  one-year limit: `US:15USC1692k(d)`.
- Regulation F lists the false representations barred (government or credit-bureau affiliation, attorney involvement,
  arrest or seizure threats, simulated legal process): `US:12CFR1006.18-other-representations`. A single payment on
  several debts is not applied to a disputed one, and the tenant's direction is followed:
  `US:15USC1692h-multiple-debts`.

8.4 What the city requires of anyone collecting (until 2026-12-31).
- Staff who regularly collect, including the landlord's or manager's own staff, follow DCWP's practice rules, and
  the employer is liable: `NYC:RCNY6-5-76-debt-collector`, `NYC:RCNY6-5-77(g)`.
- A final statement demanding the full balance starts "debt collection procedures": `NYC:RCNY6-5-76-procedures`.
  After that, more than two contacts in seven days is presumed excessive: `NYC:RCNY6-5-77(b)(1)(iv)`.
- Only amounts the lease or law authorizes: `NYC:RCNY6-5-77(e)(1)`.
- The city rule imports the state conduct standards of GBL 601 for these collectors: no posing as government, no
  collecting fees not legally due, no false credit information, no contact with the employer before judgment, no
  disclosing a disputed debt without saying so, no threats of action not intended, no claiming rights that do not
  exist, no fake legal process: `NYC:RCNY6-5-77(d)(17)-GBL601`, `NYC:RCNY6-5-77(e)(8)-GBL601`.
- No one may tell a family member or heir they must pay the tenant's debt, or misstate their obligation:
  `NY:GBL-601-a-family`.
- The current validation procedure binds only lenders' collectors. A landlord is not one unless it regularly offers
  installment plans of more than four payments or with finance charges: `NYC:RCNY6-5-77(f)(1)`,
  `NYC:RCNY6-5-77(f)(1)-landlord-not-TILA-creditor`, `US:15USC1602(f)`, `US:15USC1602(g)`.
- Penalties. City Consumer Protection Law violations cost $350 to $2,500 each, with restitution, and give the tenant
  no private action: `NYC:ADC-20-703-CPL-remedies`, `NYC:RCNY6-6-47-CPL-penalties`; DCWP's schedule for the collection
  rules and licensed-agency duties: `NYC:RCNY6-6-62-collection-penalties`. Telling a relative it must pay costs $500
  to $1,000 per violation; the landlord avoids liability by curing within fifteen days: `NY:GBL-604-b-penalty-cure`.

8.5 What the city requires from 2027-01-01 (SHIELD Rule).
- In force 2027-01-01, with its penalties; its "September 1, 2026" text dates read as 2027-01-01:
  `NYC:SHIELD-effective-date`, `NYC:SHIELD-operative-date`, `NYC:SHIELD-penalty-effective-date`.
- A landlord or manager that regularly collects its own balances is a debt collector once procedures begin, and a
  final statement demanding the whole balance begins them: `NYC:SHIELD-5-76-debt-collector`,
  `NYC:SHIELD-5-76-procedures`, `NYC:DCWP-FAQ-procedures-trigger`.
- Mailed validation notice within five days of first contact, with the city items and an itemization, for accounts
  first requiring one from 2027-01-01: `NYC:SHIELD-5-77(f)(1)`, `NYC:SHIELD-5-77(f)(1)(viii)`,
  `NYC:DCWP-FAQ-validation-scope`.
- At most three contacts per seven days; ordinary non-collection landlord messages do not count:
  `NYC:SHIELD-5-77(b)(1)(iii)-frequency`, `NYC:SHIELD-5-77(b)(1)(iii)(D)(IX)`. Email or text only with consent, or where the tenant used
  that address or number with the collector about a debt in the past 60 days and has not opted out:
  `NYC:SHIELD-5-77(b)(5)(i)(B)`. Stop on request in any form: `NYC:SHIELD-5-77(b)(4)-cease`. Procedures to check the
  limitations period, and a notice before collecting a time-barred debt: `NYC:SHIELD-5-77(i)`.
- The rule's notice and 14-day wait before reporting to a credit bureau bind no one: federal law preempts state and
  city rules on furnishing (8.7). A federal debt collector still contacts the tenant before reporting:
  `NYC:SHIELD-5-77(e)(10)-credit-report-notice`.

8.6 City licensing.
- A debt collection agency needs a DCWP licence: `NYC:ADC-20-489(a)`, `NYC:ADC-20-490`.
- No licence: the owner's own staff, `NYC:ADC-20-489(a)(1)`, `NYC:DCA-owner-own-staff`; an affiliate collecting only
  for related owners, `NYC:DCA-affiliate-collector`; a manager whose business is operating buildings,
  `NYC:DCA-manager-for-owners`; Handoff when collecting is incidental to settling tenancies,
  `NYC:DCA-handoff-incidental`, `NYC:ADC-20-489(a)(7)`.
- Licence required: Handoff if collecting is its principal purpose, `NYC:DCA-handoff-principal-purpose`; a buyer of
  delinquent balances, `NYC:DCA-debt-buyer`. Only the lessor can claim the "originated the debt" exclusion:
  `NYC:DCA-originated-exclusion-scope`.
- A licensed broker-manager that mishandles tenant money or collections risks its licence: `NY:RPL-441-c-licence-discipline`.
- A licensed agency must verify on request with the landlord's final statement and an itemization:
  `NYC:ADC-20-493.2(a)`, `NYC:RCNY6-2-190(b)`. Time-barred debts need a disclosure first: `NYC:ADC-20-493.2(b)`,
  `NYC:RCNY6-2-191(a)` (until 2026-12-31). Payment plans are confirmed in writing within five business days:
  `NYC:ADC-20-493.1(b)`, with the items the rule lists: `NYC:RCNY6-2-192-payment-plan`. The agency keeps a separate
  file for each debt: `NYC:RCNY6-2-193-records`.
- Unlicensed collection costs $100 a day on top of the licence penalties, and DCWP may order the activity stopped:
  `NYC:ADC-20-105-unlicensed-daily-fine`; criminal fines and civil penalties escalate for repeat or revoked-licence
  operation: `NYC:ADC-20-106-unlicensed-sanctions`. A licensed agency answers for its staff acting within their
  authority: `NYC:ADC-20-493(d)-agency-vicarious`; shows its licence number on every letter and email:
  `NYC:RCNY6-1-05-licence-number`; answers its call-back number with a person within the 60-second standard:
  `NYC:RCNY6-2-194-callback-person`; and pays a tenant's judgment within 30 days: `NYC:RCNY6-1-15-licensee-judgment`.
- A missing licence number costs $175 to $500 per item: `NYC:RCNY6-6-11-licence-number-penalty`.

8.6a State licensing of whoever collects rent. Collecting rent for another for a fee, including a move-out rent
balance, requires a New York broker's licence; collecting only damage, fees, utilities or use and occupancy does not:
`NY:RPL-440(1)-rent-collection`. The owner and its salaried staff need none: `NY:ADJ-broker-owner-and-staff`. Only
court appointees, public officers and attorneys are exempt; a collection agency is not:
`NY:RPL-442-f-exemptions`. Collecting unlicensed is a misdemeanor and forfeits the fee, but the owner's claim is
unaffected: `NY:RPL-442-d-442-e-unlicensed`. A licensed manager may pay Handoff for settlement work, not for leasing
help: `NY:RPL-442-fee-split`. Handoff by configuration: it needs the licence if it demands, receives or applies rent:
`NY:HANDOFF-broker-config-collects-rent`; it does not if it only settles while the owner or licensed manager holds the
deposit, demands and receives: `NY:HANDOFF-broker-config-settlement-only`; its people may instead collect as licensed
salespersons of a broker, under the broker's regular personal supervision: `NY:HANDOFF-broker-config-under-broker`; a third-party collector of the rent part needs the
broker licence too: `NY:HANDOFF-broker-config-collection-agency`. Which one applies is a later operating choice.
- A broker-manager accounts to the owner and remits collections within a reasonable time:
  `NY:19NYCRR-175.2-broker-remit`. Where Handoff's people collect as salespersons of a broker, the broker supervises
  them regularly and personally and both keep transaction records: `NY:19NYCRR-175.21-broker-supervision`; the broker
  commits a misdemeanor if any of them is unlicensed: `NY:RPL-442-c-broker-responsibility`.
- Every rent receipt, including one for final rent or arrears, names the registered managing agent and any separate
  rent-collection agent; a new collection agent (Handoff or a collector) is announced by mail at least 15 days before
  it collects: `NYC:ADC-27-2105-rent-receipt-agent`.
- Handoff and managers may not solicit retainers for collection lawyers or take any share of their fees for placing
  claims: `NY:JUD-479-no-solicitation`, `NY:JUD-491-no-fee-sharing`.

8.7 Credit reporting. Whoever reports the balance must not report what it knows or has reason to believe is
inaccurate, must mark disputes, must report the delinquency date, and must investigate disputes:
`US:15USC1681s-2(a)(1)(A)`, `US:15USC1681s-2(a)(3)`, `US:15USC1681s-2(a)(5)(A)`, `US:15USC1681s-2(b)(1)`,
`US:15USC1681s-2(c)`, `US:12CFR1022.42(a)`, `US:12CFR1022.43(a)`. A federal debt collector must first contact the
tenant before reporting: `US:12CFR1006.30(a)`. A report on the tenant may be pulled only to review or collect its
account, and a collection account may be reported for seven years from 180 days after the delinquency began:
`US:15USC1681b-1681c-report-limits`.
- Federal preemption. No state or city requirement applies to the subject matter of the federal furnisher rules, and
  that includes common-law claims, even for malicious reporting (Second Circuit):
  `US:15USC1681t(b)(1)(F)-furnisher-preemption`. So the city's SHIELD pre-reporting notice, the state duty to tell a
  credit bureau a coerced debt is disputed, and the state criminal and military-law limits on what is reported do not
  bind a furnisher; the federal accuracy, dispute, identity-theft and debt-collector contact rules govern alone. State
  and city law on collection conduct still applies. Consumer-report information is disposed of under the FTC rule, not
  state disposal law.
- Who is a reporting agency. A landlord reporting only its own experience with the tenant is a furnisher, not a
  consumer reporting agency; Handoff becomes an agency if it sells several owners' tenant data to others:
  `US:15USC1681a(d)-(f)-own-experience-CRA`.
- Disputes and identity theft. The furnisher's investigation after a bureau's notice is done within the bureau's 30
  days (45 in some cases): `US:15USC1681i-furnisher-deadline`. After an identity-theft notice or report it stops
  refurnishing and may not sell or place the balance: `US:15USC1681c-2-furnisher-identity-theft`; what counts as an
  identity theft report: `US:12CFR1022.3(i)-identity-theft-report`.
- Pulling reports. A New York agency furnishes a report on a former tenant for locating it to deliver the statement or
  refund and for collecting the balance: `NY:GBL-380-b-permissible-purpose`. A security freeze does not block a pull
  to review or collect the account; a fraud alert limits opening a payment plan: `US:15USC1681c-1-freeze-alerts`,
  `NY:GBL-380-t-freeze-collection`. An address discrepancy notice requires reasonable steps to match the report to the
  tenant: `US:12CFR1022.82-address-discrepancy`. An investigative report (neighbor interviews) needs written
  disclosure within 3 days: `US:15USC1681d-investigative-report`.
- A servicemember's request for a stay or relief is never by itself reported as inability to pay:
  `US:50USC3919-no-adverse-report`; the state rule reaches decisions other than reporting to a bureau:
  `NY:MIL-313-a-no-adverse-report`. Court records of a tenant removed from a building in foreclosure are sealed and
  not used: `NY:RPAPL-757-foreclosure-eviction-sealed`.
- Liability. Federal: willful violations bring actual or statutory damages ($100 to $1,000), punitive damages and
  fees, `US:15USC1681n-willful`; negligent ones actual damages and fees, `US:15USC1681o-negligent`; suit within two
  years of discovery and five of the violation, `US:15USC1681p-limitations`; public enforcement,
  `US:15USC1681s-public-enforcement`; obtaining a report under false pretenses is a crime,
  `US:15USC1681q-false-pretenses`. A state defamation or negligence claim about reporting needs malice, and a claim
  about information furnished to a bureau is preempted altogether: `US:15USC1681h(e)-furnisher-immunity`. State
  (report users): willful violations bring actual and punitive damages and fees, `NY:GBL-380-l-willful`; negligent
  ones actual damages and fees, `NY:GBL-380-m-negligent`; suit within two years, `NY:GBL-380-n-limitations`; obtaining
  a report by false pretenses is a crime, `NY:GBL-380-o-false-pretenses`.

8.8 Bankruptcy. A filing stays all collection of pre-filing balances: `US:11USC362(a)(6)`. A discharge ends it for
good, and the balance may not be placed with a collector; collecting it anyway is contempt, and co-tenants and
guarantors stay liable: `US:11USC524(a)(2)`, `US:12CFR1006.30(b)`. In chapter 13
the landlord also may not collect from a co-tenant or individual guarantor while the case is open, unless the court
lifts that stay: `US:11USC1301-codebtor-stay`. In chapter 7 an unexpired lease the trustee does not assume within 60
days is rejected, a breach dated just before the filing: `US:11USC365(d)(1)-ch7-rejection`. The landlord's claim for
future rent is capped at the greater of one year or 15% of the remaining term (at most three years), plus unpaid rent:
`US:11USC502(b)(6)-lessor-cap`. The proof of claim is due within 70 days after the order for relief (90 in an
involuntary chapter 7); a late claim in chapter 7 is paid after the timely ones: `US:FRBP-3002(c)-claim-deadline`.
- Stay and discharge details. Dollar amounts are those in force when the case was filed (from 2025-04-01: $3,800
  deposit priority, $8,575 preference floor, $21,050 involuntary threshold): `US:11USC104-dollar-amounts`. Collecting
  a discharged balance is civil contempt when there is no fair ground of doubt the discharge covered it:
  `US:11USC105-discharge-contempt`. What survives: fraud, a materially false written financial statement relied on,
  and wilful and malicious damage the tenant intended (each only if the landlord sues by the deadline), and a balance
  the tenant never scheduled while the landlord had no notice; a landlord that loses a fraud claim on a consumer debt
  may pay the tenant's fees. Judgment: `US:11USC523-landlord-exceptions`. A completed chapter 13 plan discharges even
  wilful and malicious property damage; a hardship discharge does not; no discharge after a recent prior one:
  `US:11USC1328-ch13-discharge`.
- Chapter 13. The confirmed plan binds the landlord whether or not it filed a claim: `US:11USC1327-plan-binds`; the
  plan may assume or reject the lease and pay a balance shared with a co-debtor in full:
  `US:11USC1322-plan-lease-codebtor`; post-filing rent is claimed under 1305 or stays outside the discharge:
  `US:11USC1305-postpetition-claim`.
- Deposit held at filing. The landlord's claim is secured up to the deposit it may set off, and a deposit larger than
  the claim also covers lease interest and fees: `US:11USC506-deposit-secured-claim`.
- A case dismissed without discharge ends the stay; the landlord may collect and apply the deposit, and any refund
  goes to the tenant: `US:11USC349-dismissal`. A case is dismissed on day 46 if schedules are missing, and a landlord
  may ask for the tenant's tax return: `US:11USC521-schedules-dismissal`.
- Payments the landlord received. Payments on old arrears in the 90 days before filing may be recovered as
  preferences, subject to floors ($600 consumer, $8,575 other) and ordinary-course, new-value and full-deposit
  defenses: `US:11USC547-preference`. Rent paid by a parent or other non-liable payer may be recovered in that payer's
  bankruptcy (two years, four under state law): `US:11USC548-constructive-fraud-third-party`,
  `US:11USC544(b)-state-lookback`. These suits must be brought within two years of the order for relief:
  `US:11USC546(a)-avoidance-deadline`.
- A landlord alone may file an involuntary petition against a tenant with fewer than 12 creditors for an undisputed
  claim of $21,050 or more, at the risk of fees and damages if dismissed: `US:11USC303-involuntary`.
- A Supreme Court judge is told promptly of a settlement or a bankruptcy filing: `NY:22NYCRR-202.28-notify-court`. A
  tenant who wins on a discharge defense gets no costs: `NY:CCA-1905-no-costs-bankruptcy-defense`.
- More bankruptcy details. The trustee recovers payments made after filing from estate property (in chapter 13 all
  post-filing earnings are estate property): `US:11USC549-postpetition-payment`. An avoided payment is recovered from
  the landlord; a manager or collector that only passed the money on is not an initial transferee:
  `US:11USC550-transferee-liability`. The estate keeps every defense the debtor had, including the deposit forfeiture,
  and a post-filing acknowledgment does not bind it: `US:11USC558-estate-defenses`. A landlord may move to dismiss for
  abuse only if the tenant's income is above the state median, within 60 days after the creditors' meeting:
  `US:11USC707(b)-abuse-motion`. Chapter 7 pays priority claims first, then timely claims, then late ones, then
  penalties: `US:11USC726-ch7-distribution-order`. A company tenant gets no chapter 7 discharge; an individual's
  covers every pre-filing debt except the 523 exceptions: `US:11USC727-ch7-discharge`.
- Filing and deadlines. The proof of claim is on Form 410 with the lease and, in an individual's case, the itemized
  statement: `US:FRBP3001-claim-contents`; the manager or Handoff may sign it and vote, but motions and complaints for
  an entity owner need a lawyer: `US:FRBP9010-agent-authority`; identifiers are redacted to the last four digits:
  `US:FRBP9037-redaction`. Objections to a chapter 13 plan are due 7 days before confirmation:
  `US:FRBP3015-plan-objection`. Objections to discharge and 523(c) complaints are due 60 days after the first date set
  for the creditors' meeting: `US:FRBP4004-discharge-objection`, `US:FRBP4007-523c-deadline`. Bankruptcy deadlines
  count with New York holidays and add 3 days after mail service; the claim, exemption, discharge, dischargeability
  and reaffirmation deadlines are never shortened: `US:FRBP9006-time`. A reaffirmation binds only if made before
  discharge with the disclosures and filed on time; the landlord may accept but not ask for voluntary repayment, and
  co-tenants and guarantors stay liable: `US:FRBP4008-reaffirmation`. A case closed without discharge leaves the
  balance collectible: `US:FRBP4006-no-discharge-notice`.
- When the stay ends. It ends when the case closes or is dismissed or a discharge is granted or denied:
  `US:11USC362(c)-stay-ends`. A tenant with one case dismissed in the prior year gets 30 days of stay unless extended;
  with two or more, none arises: `US:11USC362(c)(3)-(4)-repeat-filer`. A relief motion ends the stay after 30 days
  unless the court continues it (60 days in an individual's case): `US:11USC362(e)-relief-deadline`. A willful
  violation costs the tenant's actual damages, fees and in some cases punitive damages:
  `US:11USC362(k)-willful-violation`.

8.9 Suing a tenant who does not appear. Before a default judgment, the landlord files an affidavit on military
service: `US:50USC3931(b)(1)`. At least 20 days before entry, it also mails the summons to the tenant's residence in a
"personal and confidential" envelope that does not show it concerns a debt, and files an affidavit of mailing.
This does not apply in the small claims part: `NY:CPLR-3215(g)(3)`. A clerk's default judgment also needs an affidavit
that the limitation period has not expired: `NY:CPLR-3215(j)-sol-affidavit`. State law adds no non-military affidavit
of its own: `NY:MIL-303(3)`. No default judgment against an infant or adjudicated incompetent without its
representative; a party's death requires substitution, and a judgment debtor's death requires the surrogate's leave:
`NY:CPLR-1203-1015-5208-parties`. A summary-proceeding petition states the building's registration status:
`NY:22NYCRR-208.42(g)-registration-plea`.

8.10 Before suing: registration, capacity, court and interest.
- Capacity. An owner LLC or corporation formed outside New York that does business here cannot sue a former tenant
  until it holds New York authority; the defect is curable and does not touch the lease or the statement:
  `NY:LLC-808(a)-foreign-authority`, `NY:BCL-1312(a)-foreign-authority`. A New York LLC that has not filed proof of
  publication cannot keep a suit going until it files; filing cures it at any time:
  `NY:LLC-206-publication-suspension`. A lease made under a business name needs the assumed-name certificate on
  file before suit: `NY:GBL-130-assumed-name`. An entity owner appears by a lawyer (in commercial claims, by its own
  officer or employee); Handoff and the manager may prepare evidence but may not appear for it; defending a small claim, a corporation may
  also appear by its own officer or employee: `NY:CPLR-321-JUD-495-appearance`.
- HPD registration. A multiple-dwelling owner that has not registered recovers no rent until it does, then recovers
  the accrued rent: `NY:MDL-325(2)`. For a one- or two-family house that must register, the court may stay the rent claim until it
  registers: `NYC:ADC-27-2107(b)-rent-stay`. A claim for damage to the unit is not a claim for rent. Before suing,
  also check the certificate of occupancy and rent-impairing violations (Step 0.5).
- Where to sue a small balance. An owner that is a corporation, partnership or LLC cannot use small claims:
  `NY:CCA-1809(1)`. It may use the commercial claims part only if its principal office is in New York State and the
  former tenant lives, works or has an office in the city when the claim is filed: `NY:CCA-1801-A(a)-eligibility`.
  There, because the lease with a natural person is a consumer transaction, it first mails the court's demand-letter
  form 10 to 180 days before filing and certifies no more than five such claims that month: `NY:CCA-1801-A(b)`,
  `NY:CCA-1803-A(b)`. Otherwise it sues in the regular part of the Civil Court, in a county 8.13(a) allows.
- Time limits. The period does not run during the tenant's military service, runs at least 30 days past the end of a
  bankruptcy stay, excludes 18 months after the tenant's death, and restarts on a signed written acknowledgment or a
  part payment: `US:50USC3936-tolling`, `US:11USC108(c)-extension`, `NY:CPLR-210-death`,
  `NY:GOL-17-101-acknowledgment`. Court and statutory stays, a six-month recommencement after certain dismissals,
  the tenant's absence where no jurisdiction was available, the claimant's infancy or insanity and state militia
  service also count: `NY:CPLR-204-208-tolling`.
- Rent for a period when a public-assistance tenant's building had a reported hazardous violation is not recoverable
  until corrected: `NY:SSL-143-b(5)-rent-bar`.
- Interest. Interest on the balance is recovered as of right from the date each amount was due:
  `NY:CPLR-5001(a)-(b)`. If the lease sets a rate for amounts after they fall due, that rate applies until judgment, and a rate stated
  without a period is yearly: `NY:CASE-NML-contract-rate`. But lease interest on late or unpaid rent is a late-payment charge, capped with any
  late fee at the lesser of $50 or 5% of the monthly rent: `NY:ADJ-lease-interest-on-rent`. Otherwise the statutory
  rate applies before and after judgment: 2% a year when the tenant is a natural person (a residential lease balance
  is a consumer debt for this purpose), 9% when the tenant is a company: `NY:CPLR-5004(a)-consumer-2pct`. A tenant who
  signed the lease before entering military service pays no more than 6% a year in interest, fees and charges during
  service once it gives notice with its orders; the excess is forgiven: `US:50USC3937-6pct`, `NY:MIL-323-a-6pct`.

- A DCWP-licensed collector that sues a former tenant pleads its licence name and number or faces dismissal:
  `NY:CPLR-3015(e)-licence-pleading`.
- More capacity rules. Settling claims, suing, defending and keeping bank accounts are not doing business, so a
  foreign corporation or LLC whose only New York acts are those may sue without authority; owning and leasing units
  here is weighed. A corporation authorized under a fictitious name uses it, and needs no assumed-name certificate for
  it. Judgment: `NY:BCL-1301-doing-business-and-fictitious-name`, `NY:LLC-803-doing-business-exclusions`. Authority is
  suspended, and suit barred until cured, when a foreign corporation's name or home-state change is not filed within
  20 days: `NY:BCL-1309(c)-authority-suspension`; when a foreign LLC, foreign or domestic limited partnership, or LLP
  does not file proof of publication: `NY:LLC-802-foreign-publication-suspension`,
  `NY:PTR-121-902-foreign-lp-publication`, `NY:PTR-121-201-lp-publication`, `NY:PTR-121-1500-llp-publication`; or when
  a partnership's process agent resigns and no new address is filed: `NY:PTR-121-104-a-process-address-suspension`,
  `NY:PTR-121-1506-llp-process-address-suspension`. Unauthorized foreign limited partnerships, LLPs and not-for-profit
  corporations cannot sue until authorized: `NY:PTR-121-907-foreign-lp-authority`, `NY:PTR-121-1502-foreign-llp`,
  `NY:PTR-121-1504-foreign-related-llp`, `NY:NPCL-1313-foreign-authority`, `NY:NPCL-1309(b)-name-change-suspension`.
  None of these touches the lease, the statement or the tenant's own suit.
- Who prepares and signs. A non-lawyer paid by the owner (Handoff, a manager) may assemble the evidence file but may
  not prepare pleadings: `NY:JUD-484-nonlawyer-preparation`; holding out as able to practice law and causing loss over
  $1,000 is a felony: `NY:JUD-485-a-felony`. A suit run by a non-lawyer in an attorney's name is a misdemeanor with a
  $50 forfeiture to the tenant: `NY:JUD-476-lending-name`, `NY:JUD-492-use-of-attorney-name`.
- A tenant who signed at 18 or over cannot disaffirm the lease for infancy: `NY:GOL-3-101-age-of-capacity`. Claims
  against a tenant with a committee or conservator are presented when it advertises for creditors, or its good-faith
  payments to others discharge it: `NY:DCL-250-committee-claim`, `NY:DCL-252-good-faith-payment`.
- A deceased tenant's estate. The landlord may petition for letters itself: `NY:SCPA-1002-creditor-petition`. A
  presented claim is deemed rejected after 90 days: `NY:SCPA-1806-allowance-rejection`; presenting it stops the
  limitation period: `NY:SCPA-1808-presentation-tolls`; a suit on a rejected claim is due within 60 days, or the claim
  is tried on the accounting: `NY:SCPA-1810-sue-within-60-days`. An unpresented claim may still be sued on against
  distributees within the limitation period: `NY:EPTL-12-2.1-unpresented-claim`.
- More stays. A rent claim may be stayed while a municipal violation order stands, with rent deposited in court:
  `NY:RPAPL-755-rent-action-stay`; any suit for rent is stayed while the landlord's unpaid utilities are shut off:
  `NY:RPAPL-756-utility-shutoff-stay`. A lease jury waiver is void for property-damage claims:
  `NY:RPL-259-c-jury-waiver-void`.
- HPD registration evidence. Without the HPD receipt, non-registration is presumed:
  `NYC:ADC-27-2106-registration-proof`. An HPD extension waives the city stay but not the state rent bar:
  `NYC:ADC-27-2103-registration-extension`.
- Military stays. New York: the court must stay a suit on the servicemember's application unless its ability to defend
  is unaffected, `NY:MIL-304-stay-on-application`, for service plus three months with installments,
  `NY:MIL-307-stay-terms`, extendable to a guarantor, whose waiver counts only in a separate instrument,
  `NY:MIL-302-guarantor-stay`; no penalty accrues during a stay, `NY:MIL-305-penalty-relief`; the court may spread a
  pre-service balance over the service period, `NY:MIL-323-further-relief`. Federal: no penalty during an SCRA stay,
  `US:50USC3933-penalties`; anticipatory relief spreads a pre-service obligation into installments,
  `US:50USC4021-anticipatory-relief`.
- Interest. A rate stated without a period is a yearly rate: `NY:GOL-5-1301-rate-per-annum`. A payment plan is a
  forbearance capped at 16% a year, counting every charge for the delay; late fees and statutory interest are not
  forbearance interest: `NY:GOL-5-501-payment-plan-usury`.

8.11 Tax at settlement. The part of the deposit the owner keeps is its income in the year kept; a deposit applied as
the last rent is advance rent, income when received: `US:IRS-Pub527-deposit-income`. Writing off a balance needs no
Form 1099-C: `US:26USC6050P-no-1099C`. A written-off rent balance is a bad-debt deduction only if the rent was already
reported as income: `US:26CFR1.166-1(e)-bad-debt`.
- Bad debt. Worthlessness needs no suit where a judgment would be uncollectible, and cannot be moved to the year a
  bankruptcy ends: `US:26CFR1.166-2-worthlessness-evidence`. A partial write-off is deductible only as charged off on
  the books: `US:26CFR1.166-3-charge-off`. An owner whose rental is an investment deducts only a wholly worthless
  balance, as a short-term capital loss: `US:26CFR1.166-5-nonbusiness`.
- A managing agent (or Handoff where it receives and remits the money) files the owner's 1099-MISC for gross rents,
  including the kept deposit, when they reach $2,000 (payments after 2025; $600 before); the one closest to the owner
  files: `US:26CFR1.6041-1-agent-reports-rent`.
- More information returns. A tenant paying a rental agent files nothing; no 1099-MISC goes to a corporate owner:
  `US:26CFR1.6041-3-exceptions`; a documented foreign owner gets a 1042-S under the withholding rules instead:
  `US:26CFR1.6041-4-foreign-owner`. Forms 1099 are filed by February 28 (March 31 electronically), with the owner's
  copy by January 31, and 10 or more returns must be filed electronically: `US:26CFR1.6041-6-filing-dates`.
- Deposit interest. The landlord passing bank interest to the tenant is a middleman: it files a 1099-INT for $10 or
  more in the year credited, backup-withholds without a TIN, and skips corporate tenants:
  `US:26CFR1.6049-4-middleman-return`; the tenant's copy goes out by January 31, to the forwarding address:
  `US:26CFR1.6049-6-tenant-statement`. Interest the landlord pays from its own funds is not 6049 interest:
  `US:26CFR1.6049-5-which-interest`. A nonresident-alien tenant in a listed country gets a 1042-S:
  `US:26CFR1.6049-8-nra-tenant`.
- Write-offs. A landlord never files a 1099-C; a buyer of the balance that lends regularly does, on the listed events,
  for discharges of $600 or more: `US:26CFR1.6050P-2-debt-buyer`, `US:26CFR1.6050P-1-identifiable-events`. The
  deduction is limited to basis (a rent balance only if the rent was reported as income), taken in the year the debt
  becomes worthless: `US:26USC166-writeoff-deduction`.
- Cash over $10,000 received in one payment or related payments (within 24 hours, or a known series) is reported on
  Form 8300 within 15 days, with a statement to the payer by January 31: `US:26USC6050I-cash-over-10000`. Card and
  payment-app receipts are reported on Form 1099-K by the settlement entity; where Handoff receives settlements for
  several owners and pays them out, Handoff files the 1099-Ks for the owners (network payments only over $20,000 and
  200 transactions): `US:26USC6050W-card-network-settlement`. A payment of $600 or more to a tenant's attorney (a
  deposit settlement or judgment) is reported for the attorney, and the part that is the tenant's income (damages
  above its own deposit) for the tenant: `US:26USC6045(f)-attorney-payments`.

8.12 After judgment. Recovery is limited by bank-account exemptions (amounts adjusted every three years), exemption notices, a
ten-percent cap on income executions and a presumption of payment after twenty years; the pursue-or-write-off estimate uses these limits:
`NY:CPLR-5205-5231-enforcement-limits`. When the judgment is paid, the satisfaction-piece is filed and a copy mailed:
`NY:CPLR-5020-satisfaction`.

8.13 Suing and enforcing: procedure. These rules apply whichever side sues, in the Supreme Court, the Civil Court or
its small claims and commercial claims parts.

(a) Court and venue.
- The Civil Court hears claims up to $50,000, counted without interest and costs; several joined claims each within
  the limit may exceed it, and a money counterclaim has no limit: `NY:CCA-202-money-limit`,
  `NY:CCA-201-limit-excludes-interest`, `NY:CCA-211-joinder`. Money claims of $10,000 or less in the regular part go
  to court-annexed arbitration where the program runs: `NY:CCA-206-compulsory-arbitration`.
- Venue today. A lease balance is not a consumer credit transaction, so the consumer-credit rule of suing in the
  tenant's county does not apply; the suit lies in any city county where a party resides, an entity owner residing
  wherever it does business or keeps an office, and an assignee counting as the original owner:
  `NY:CCA-2101(g)-balance-venue-current`. From the day the pending Consumer Debt Uniformity Act applies, suit lies
  only in the county where the tenant lives or where the transaction took place: `NY:S9760-venue`. A wrong county is
  waived unless the defendant moves by the time issue is joined: `NY:CCA-306-venue-objection`; in the Supreme Court by
  written demand: `NY:CPLR-511-venue-demand`. A lease venue clause is enforceable (it is not a consumer-goods
  contract), but a federal debt collector still sues only where the tenant signed or lives:
  `NY:CPLR-501-venue-clause`.
- Small claims. The tenant files without a summons for a $15 or $20 fee; the clerk mails notice, and the landlord may
  counterclaim for its balance within five days for $5: `NY:CCA-1803-small-claims-notice-counterclaim`,
  `NY:22NYCRR-208.41-small-claims-procedure`. A counterclaim in small claims is limited to $10,000, so a larger
  balance is sued elsewhere: `NY:CCA-1805-small-claims-remedies`. A defendant may demand a jury by affidavit, fee and
  $50 undertaking: `NY:CCA-1806-small-claims-jury`. A claim already lost, or brought to harass, may be barred:
  `NY:CCA-1810-harassing-refiling`. The tenant may sue the landlord under any business name it uses:
  `NY:CCA-1814-defendant-name`.
- An entity owner eligible for the commercial claims part files the signed application with both certifications; the
  tenant is presumed notified if the mailing is not returned in 30 days; the court rule's New York City office
  requirement yields to the statute's New York State office: `NY:22NYCRR-208.41-a-commercial-claims-procedure`.
- Commercial claims part: counterclaims only within its $10,000 limit, `NY:CCA-1805-A-commercial-claims-remedies`; a
  jury only on the tenant's demand, `NY:CCA-1806-A-commercial-claims-jury`; a claim already lost or brought to harass
  may be barred, `NY:CCA-1810-A-harassing-refiling`; a business may be named by any name it uses,
  `NY:CCA-1814-A-defendant-name`. A relative may appear for a disabled natural person without pay, never Handoff or a
  paid manager: `NY:CCA-1815-relative-representative`.

(b) Commencing and serving.
- Commencement. A Supreme Court action is commenced by filing with the index fee: `NY:CPLR-304-commencement`; a Civil
  Court action by filing the summons and complaint with the fee, with the index number on the summons served:
  `NY:CCA-400-commencement`. The Civil Court summons is issued by the attorney or, for an owner without one, the
  clerk: `NY:CCA-401-summons-form`; the claim may be endorsed on the summons: `NY:CCA-902-pleading-form`. A Supreme
  Court summons states the venue basis: `NY:CPLR-305-summons-contents`. Service must follow within 120 days or the
  action may be dismissed: `NY:CPLR-306-b-120-days`, `NY:CCA-411-120-days`.
- In the Supreme Court a represented party e-files where e-filing is mandatory; a self-represented individual owner or
  tenant is exempt: `NY:22NYCRR-202.5bb-mandatory-efiling`. In the Civil Court an e-filed summons is filed, and the
  claim interposed, when NYSCEF receives it with the fee; service stays in hard copy unless the tenant agrees:
  `NY:22NYCRR-208.4a-efiling`. The Civil Court summons follows the prescribed form, stating the sum and the interest
  date; the consumer-credit legends do not apply to a lease balance: `NY:22NYCRR-208.6-summons-form`. A summons naming
  the wrong county division is refused or re-filed with notice: `NY:22NYCRR-208.8-wrong-county`.
- Where service may be made. Civil Court service is made in the city unless a law reaches beyond it:
  `NY:CCA-403-service-within-city`, `NY:CCA-408-service-outside-city`, `NY:CCA-407-service-on-303-agent`. A tenant who
  moved away is subject to suit here on a claim from its NYC lease and is served outside the city or state:
  `NY:CPLR-302-long-arm`, `NY:CCA-404-long-arm`, `NY:CPLR-313-service-outside-state`. A tenant suing the landlord may
  be served in the landlord's own action through its attorney: `NY:CPLR-303-plaintiff-designates-agent`. Mail service
  is complete only when the signed acknowledgment comes back; otherwise serve another way and tax the cost:
  `NY:CPLR-312-a-mail-service`, `NY:CCA-1908-A-unacknowledged-mail-service`. Proof of service is filed with the clerk,
  and service by any means other than personal delivery is complete on filing: `NY:CCA-409-proof-of-service`,
  `NY:CCA-410-service-complete`. A court may keep a victim tenant's address confidential and name an agent for
  service: `NY:CPLR-2103-a-confidential-address`.
- Service on a person: personal delivery; delivery to a person of suitable age at the tenant's current home or
  business plus mailing; nail-and-mail only after due diligence; or a court-directed method. The vacated unit is no
  longer the former tenant's home, so substituted or nail-and-mail service there is void:
  `NY:CPLR-308-natural-person`. An infant, incompetent or conservatee is served through its guardian, committee or
  conservator: `NY:CPLR-309-infant-incompetent`. The proof of service states who, when, where and how, with a
  description of the person served: `NY:CPLR-306-proof-of-service`. A sworn statement may be an affirmation under
  penalty of perjury without a notary: `NY:CPLR-2106-affirmation`. A verified complaint may be verified by the
  managing agent in the listed cases: `NY:CPLR-3020-verification`.
- Serving an entity landlord or tenant: corporation, `NY:CPLR-311-corporation`; LLC, `NY:CPLR-311-a-llc`; partnership,
  `NY:CPLR-310-partnership`; limited partnership, `NY:CPLR-310-a-limited-partnership`. The owner keeps its Secretary
  of State address current so a deposit suit does not end in default.
- Time to answer: 20 days after personal delivery; otherwise 30 days after service is complete (in the Civil Court,
  after proof of service is filed): `NY:CPLR-320-appearance-time`, `NY:CCA-402-answer-time`.

(c) Answer, counterclaims and preclusion.
- Timeliness. A claim is interposed when filed: `NY:CPLR-203-accrual-interposition`. A charge payable on demand
  accrues when the demand could first be made, the deposit claim at the end of the 14 days, and each rent installment
  on its due date: `NY:CPLR-206-demand-accrual`. A plaintiff resident outside New York at accrual (an owner entity
  based elsewhere, a tenant who moved away) must also meet its home state's shorter period and tolling, and an
  assignee stands in the owner's place; a choice-of-law clause does not change this: `NY:CPLR-202-borrowing`. A crime
  victim landlord has seven years against a convicted tenant: `NY:CPLR-213-b-crime-victim`. War time is excluded for
  enemy nationals: `NY:CPLR-209-war-tolling`.
- Parties. Co-tenants sued jointly may be pursued through those served, and an unserved co-tenant's own property is
  reached only by a later action: `NY:CPLR-1501-joint-obligors`, `NY:CPLR-1502-later-action-co-obligor`. Suing one
  liable person is not an election against the others: `NY:CPLR-3002-no-election`. A guardian ad litem may be paid by
  the landlord: `NY:CPLR-1204-gal-compensation`; costs do not run against an incapacitated tenant without an order:
  `NY:CPLR-1205-no-costs-against-incapacitated`.
- Parties who cannot act for themselves. An infant appears by its guardian or parent, an incompetent by its committee,
  a conservatee by its conservator, otherwise by a guardian ad litem, which the landlord may move for after ten days:
  `NY:CPLR-1201-representation`, `NY:CPLR-1202-guardian-ad-litem-motion`. When a party dies, substitution is made
  within a reasonable time or the action may be dismissed as to that party: `NY:CPLR-1021-substitution-deadline`.
- Motions. Pre-answer dismissal grounds include release, payment, limitations, lack of capacity and lack of
  jurisdiction; most are waived unless raised in the motion or answer: `NY:CPLR-3211-dismissal-grounds`. A lease is
  not an instrument for the payment of money only, so a balance on it is sued by complaint; a signed payment agreement
  or guaranty of payment may use summary judgment in lieu of complaint: `NY:CPLR-3213-summary-judgment-in-lieu`. A
  case left idle may be dismissed after a 90-day demand: `NY:CPLR-3216-want-of-prosecution`. A dismissal after the
  plaintiff's evidence closes is on the merits: `NY:CPLR-5013-dismissal-effect`.
- Pleading and counterclaims. A lease clause shortening the tenant's time to sue over the deposit is void; other
  agreed shorter periods stand if reasonable: `NY:CPLR-201-agreed-shorter-period`. A counterclaim from the same
  tenancy offsets the other side's demand even if time-barred: `NY:CPLR-203(d)-counterclaim-offset`. Counterclaims are
  permissive; against a collector suing only for the owner, the tenant's claim is only an offset:
  `NY:CPLR-3019-counterclaims`. The Civil Court hears any money counterclaim regardless of amount:
  `NY:CCA-208-counterclaims`, and no reply is needed: `NY:CCA-907-counterclaim-reply`. Limitations, release, payment
  and preclusion are pleaded or waived: `NY:CPLR-3018-affirmative-defenses`.
- A small-claims judgment binds no finding of fact elsewhere, but it may bar a later claim between the same parties
  from the same transaction, and a landlord's balance from the same tenancy account is the same transaction; a later
  judgment on the same facts is reduced by the small-claims award. A landlord that did not counterclaim may sue later
  for its balance unless that suit would impair the rights the tenant's judgment established. Judgment:
  `NY:CCA-1808-preclusion`.
- A commercial-claims judgment has the same preclusive effect as a small-claims judgment: `NY:CCA-1808-A-preclusion`.

(d) Proof.
- Proof. Business records made in the regular course when the event happened are admissible; records received from
  another business (Handoff's, a vendor's) come in only if incorporated and relied on, and electronic records are
  admitted as accurate exhibits: `NY:CPLR-4518-business-records`. Scans and tamper-evident images are as good as
  originals: `NY:CPLR-4539-reproductions`. A paid, certified itemized repair bill up to $2,000, served ten days before
  trial, proves the work's reasonable value: `NY:CPLR-4533-a-repair-bill-proof`. In small claims and commercial claims
  a paid itemized bill or two itemized estimates are prima facie proof, but the landlord still carries the burden on
  amounts kept: `NY:CCA-1804-small-claims-proof`, `NY:CCA-1804-A-commercial-claims-proof`.
- An award for damage to the unit is reduced by what the owner's insurer paid, net of two years' premiums:
  `NY:CPLR-4545-collateral-source`.

(e) Defaults and relief from a judgment.
- A default on the Civil Court's endorsed summons is entered under CPLR 3215 with the extra mailing, limitations and
  military affidavits: `NY:CCA-1402-default-on-endorsed-summons`. A party that fails to appear on a calendar call may
  suffer default or dismissal, with the other side's counterclaims severed; a case struck from the Civil Court
  calendar is restored only within one year: `NY:22NYCRR-202.27-calendar-default`,
  `NY:22NYCRR-208.14-calendar-default`. At an inquest damages may be proved by sworn statements:
  `NY:22NYCRR-202.46-inquest-proof`, `NY:22NYCRR-208.32-inquest-proof`. The commercial claims clerk mails notice of a
  default judgment to both sides: `NY:CCA-1807-A-commercial-default`.
- A default taken on service other than personal delivery may be opened for up to five years if the tenant did not
  receive notice and has a meritorious defense; money collected may have to be restored:
  `NY:CPLR-317-defend-after-default`. A judgment may be vacated for excusable default within one year of service with
  notice of entry, and at any time for fraud or lack of jurisdiction (service at the vacated unit):
  `NY:CPLR-5015-relief-from-judgment`. An attorney's deceit toward the court or a party (a false affidavit of service)
  is a misdemeanor with treble damages: `NY:JUD-487-attorney-deceit`.
- Servicemembers. The court must stay the case at least 90 days on a servicemember's application with a commanding
  officer's letter: `US:50USC3932-stay-with-notice`; a stay may run for service plus 90 days with installment
  payments, and co-defendants are pursued only with the court's approval: `US:50USC3935-stay-term-codefendants`; the
  stay may extend to a guarantor or co-tenant, and a guarantor's waiver counts only in a separate instrument:
  `US:50USC3913-guarantor-cotenant`. A Defense Department certificate proves service status:
  `US:50USC4012-certificates`.

(f) Judgment, interest and costs.
- Interest runs from the decision to judgment at the judgment rate: `NY:CPLR-5002-decision-to-judgment`, and on the
  judgment from entry until paid, 2% against a person on a consumer debt and 9% otherwise, which a landlord owing a
  tenant's judgment pays too: `NY:CPLR-5003-judgment-interest`. Civil Court interest computed from commencement starts
  only when service with the index number is complete: `NY:CCA-412-interest-from-service`.
- Civil Court costs: $20/$35/$60 by stage on judgments of $6,000 or less, $50/$100/$150 otherwise, plus necessary
  disbursements (clerk, marshal and process-server fees, not attorney's fees), taxed by the clerk and reviewed on
  motion within ten days: `NY:CCA-1901-costs-amount`, `NY:CCA-1908-disbursements`, `NY:CCA-1907-taxation`,
  `NY:CCA-1909-review-of-taxation`, `NY:CCA-1903-cplr-costs-apply`; discretionary motion costs up to $50:
  `NY:CCA-1906-discretionary-costs`; security for costs at least $200: `NY:CCA-1900-security-for-costs`. Clerk fees
  ($45 index, $40 notice of trial, $70 jury); the consumer-credit surcharge does not apply to a lease balance:
  `NY:CCA-1911-clerk-fees`. None of these goes on the final account before judgment.
- Supreme Court: the index number costs $190 plus $20 in state fees: `NY:CPLR-8018-index-fee`; other court fees (RJI
  $95, motions $45, a $35 settlement filing fee paid by the defendant): `NY:CPLR-8020-court-fees`. The winner gets
  costs and disbursements unless a statute says otherwise; costs are not attorney's fees:
  `NY:CPLR-8101-costs-to-prevailing-party`; $200/$200/$300 by stage, `NY:CPLR-8201-costs-amount`, motion costs up to
  $100, `NY:CPLR-8202-motion-costs`, disbursements, `NY:CPLR-8301-disbursements`, taxed by the clerk,
  `NY:CPLR-8401-clerk-taxation`; a claim the Civil Court could have heard earns no costs in the Supreme Court below
  $6,000, `NY:CPLR-8102-costs-limit-higher-court`; each side may get costs on the claim it won,
  `NY:CPLR-8103-split-costs`. A frivolous claim or defense in a property-damage suit costs fees up to $10,000:
  `NY:CPLR-8303-a-frivolous-property-claim`. A non-resident plaintiff (a tenant who moved away, an unauthorized owner
  entity) must post $500 security for costs on the defendant's motion, or the case is stayed and may be dismissed:
  `NY:CPLR-8501-security-for-costs`, `NY:CPLR-8502-stay-dismissal`, `NY:CPLR-8503-undertaking-amount`.
- The prevailing party submits the proposed judgment within 60 days of the decision or the claim is deemed abandoned:
  `NY:22NYCRR-202.48-judgment-submission`, `NY:22NYCRR-208.33-judgment-submission`. An order to pay money may be
  docketed as a judgment and then bears judgment interest: `NY:CPLR-2222-docket-order`. Additional allowances: in a
  difficult case up to 5% capped at $3,000, and on an enforcement motion the greater of 5% or $50:
  `NY:CPLR-8303-additional-allowance`, `NY:CCA-1904-additional-allowances`. Witnesses get $15 a day and mileage:
  `NY:CPLR-8001-witness-fees`.
- A business pays a small-claims or commercial-claims judgment under any name it used, or faces a new suit for the
  judgment, fees and $100: `NY:CCA-1813-duty-to-pay`, `NY:CCA-1813-A-duty-to-pay`; once paid, the landlord files proof
  so the judgment leaves the unsatisfied index that counts toward treble damages: `NY:CCA-1811(d)-satisfaction-proof`,
  `NY:CCA-1811-A-satisfaction-proof`. If the tenant cannot be found to take payment of its judgment, the landlord
  deposits the amount with the clerk: `NY:CPLR-5020-a-deposit-with-clerk`.

(g) Enforcing a judgment.
- Before judgment the landlord may attach property of a tenant who lives outside New York, cannot be served, or is
  hiding assets: `NY:CPLR-6201-attachment-grounds`; the Civil Court's attachment runs only within the city:
  `NY:CCA-209-provisional-remedies`, `NY:CCA-801-provisional-city-only`.
- An attachment granted without notice is confirmed within five days after levy (ten against a non-resident), or it
  lapses: `NY:CPLR-6211-confirmation`. The landlord shows probable success and that its claim exceeds the tenant's
  known counterclaims, including the deposit claim, and posts an undertaking of at least $500; a wrongful attachment
  makes it liable for all damages and fees: `NY:CPLR-6212-attachment-motion`. The summons must be served within 60
  days: `NY:CPLR-6213-serve-within-60-days`. On a motion to vacate the landlord carries the burden:
  `NY:CPLR-6223-vacate-burden`.
- Issuing an execution. A Civil Court execution is issued by the attorney or, for an owner without one, the clerk:
  `NY:CCA-1501-who-issues-execution`; it reaches personal property anywhere in the city without docketing:
  `NY:CCA-1504-civil-court-execution`. If the tenant appeared, the judgment is first served on it or its attorney:
  `NY:22NYCRR-208.37-execution-precondition`. The execution states the judgment, the rate (2% where it applies), the
  amount due and the exemption notices, and is returned in 60 days: `NY:CPLR-5230-execution`. A bank levy binds for 90
  days; $2,500 of an account holding exempt deposits is untouchable and the bank holds funds 27 days:
  `NY:CPLR-5232-levy`. Anything the tenant owns or is owed is reachable unless exempt:
  `NY:CPLR-5201-reachable-property`. No levy within 24 hours after a nonpayment dispossess: `NY:CCA-1507-no-levy-24h`.
  Executions are paid in the order delivered: `NY:CPLR-5234-distribution-priority`. A third party claiming the
  property may sue to set the levy aside: `NY:CPLR-5239-adverse-claims`.
- Real property. A Civil Court judgment reaches real property only after a transcript is docketed with the county
  clerk ($25 in the city): `NY:CCA-1502-transcript`, `NY:CCA-1505-real-property`,
  `NY:CCA-1506-attached-real-property`, `NY:CPLR-5018-docketing`, `NY:CPLR-8021-transcript-fees`. The docketed
  judgment is a lien for ten years: `NY:CPLR-5203-real-property-lien`, renewable by a renewal judgment:
  `NY:CPLR-5014-renewal-judgment`. A home the tenant occupies is exempt up to $150,000 of equity in New York City, as
  adjusted: `NY:CPLR-5206-homestead`.
- Finding and reaching assets. Disclosure subpoenas to the tenant, its bank or employer, with information subpoenas
  answered in seven days; a subpoena to a third party needs the attorney's certification:
  `NY:CPLR-5223-disclosure-subpoena`, `NY:CPLR-5224-enforcement-subpoenas`, `NY:22NYCRR-208.39-enforcement-subpoenas`,
  `NY:CCA-1812-A-information-subpoenas`. Turnover of money held by the tenant or others: `NY:CPLR-5225-turnover`,
  `NY:CPLR-5227-debts-owed-to-tenant`; an installment order against other income: `NY:CPLR-5226-installment-order`; a
  receiver: `NY:CPLR-5228-receiver`; a restraint between decision and judgment: `NY:CPLR-5229-pre-judgment-restraint`;
  arrest only by court warrant for a tenant leaving the state or hiding: `NY:CPLR-5250-arrest-of-debtor`. The Civil
  Court hears these when the tenant lives or works in the city: `NY:CPLR-5221-enforcement-forum`,
  `NY:CCA-1508-enforcement-powers`.
- Exemptions and adjustments. Exemption amounts adjust every three years; the amount in force when the restraint or
  levy is served governs: `NY:CPLR-5253-exemption-adjustment`. Public assistance, and wages while it continues, are
  exempt: `NY:SSL-137-assistance-exempt`, `NY:SSL-137-a-wages-exempt`.
- Officers' fees. Sheriffs and marshals charge fixed fees and 5% poundage in the city, collected from the tenant under
  the execution; a settlement after a levy provides for poundage: `NY:CPLR-8011-sheriff-fees`,
  `NY:CPLR-8012-poundage`, `NY:CPLR-8014-fees-collected-on-execution`, `NY:CCA-1915-marshal-fees`.
- Transfers and satisfaction. A judgment is transferable: `NY:GOL-13-103-judgment-transfer`; the assignee files its
  authority with the clerk: `NY:CPLR-5019-assignee-of-judgment`. Satisfaction is entered on a satisfaction-piece, a
  court order or a deposit with the clerk: `NY:CPLR-5021-entry-of-satisfaction`.
- Special debtors. Execution against an estate's representative needs the surrogate's order:
  `NY:EPTL-11-4.6-execution-leave`; the estate pays funeral and administration costs, preferred debts, taxes and prior
  judgments before a lease balance: `NY:SCPA-1811-claim-priority`. A servicemember's execution or garnishment is
  stayed when service materially affects its ability to pay: `US:50USC3934-execution-stay`, except for transfers made
  to abuse the SCRA: `US:50USC4011-abuse`; its personal assets outside its business are protected from a business
  balance during service: `US:50USC4026-business-obligations`.

---

## Step 9. Test cases

Each case lists the rules that decide it. The files carry the full walk (`case_walks` in NY.json and NYC.json).

C3. Market-rate unit, building of six or more units, lease from 2023. Deposit in an interest-bearing account with
bank notice. Tenant vacates on the lease end date, leaves a forwarding email. Result: statement by email within 14
days; within the same 14 days, the refund (deposit plus interest less the 1% fee, less lawful deductions) by an
electronic payment to an account the landlord holds for her, or, if it holds none, a check mailed to the vacated
unit, with the email saying where the refund went; fees refunded;
painting after ordinary use not charged.
Rules: 0.3-0.4, 1.2, 5.1-5.3, 5.6, 6.1-6.5.

C4. Market-rate unit in a three-family house. Same as C3, except no interest-bearing account is required (count this
building only; the owner's other buildings are not added). The unit is not stabilized (fewer than six units, no
J-51 or 421-a) and not controlled (vacated since 1971-06-30). If the landlord banked the deposit anyway, bank notice
is owed, and interest less 1% if the account bears interest. A three-family house is a multiple dwelling, so the
three-year repaint cycle, painting records and HPD registration apply. If the house was converted to three
families after 1929-04-18 without a certificate of occupancy, no rent is recoverable for that period; if the owner is
unregistered, rent is suspended until it registers and then recovered. Rules: 0.1-0.2, 0.5, 1.2, 1.5,
1.6, 6.1.

C5a. Lease signed in 2018, rent accepted month to month since 2020. Rent acceptance after 2019-07-14 created a new
tenancy, so the 14-day regime applies. Rules: 0.4.

C6. Tenant leaves six months early. Rent after leaving is limited by the landlord's re-letting duty (its burden); a
domestic violence, senior or servicemember termination ends rent on the statutory date and bars an
early-termination charge. If the lease renews automatically, the renewal binds only with the GOL 5-905 notice. The
deposit clock still runs from vacating. At day 14 the deposit covers only rent already due and unpaid, up to a new
lease; a lease-break sum is owed only if it is valid liquidated damages and is never kept from the deposit, and on a lease
from 2022-06-22 left in breach no vacating charge exceeds the fair market cost of preparing the unit. Rules:
3.1, 3.3-3.4, 5.5, 6.2.

C7. Damage above the deposit, contractor not yet done by day 14. Statement with itemized estimates on time; the excess
is a separate claim, which survives even a forfeiture. No legal fees without a court order. If sued, the balance
carries 2% statutory interest (or the lease rate until judgment). Rent is not recoverable for a period without a
required certificate of occupancy or while a rent-impairing violation stands, and is suspended while a
multiple-dwelling owner is unregistered.
Six years to sue today. Collection rules by collector (Step 8). Rules: 0.5, 5.1-5.2, 6.4, 7.2, 8, 8.10.

C8. Two co-tenants, one leaves in month 8. No statement until the second leaves; then a statement to each. If the
landlord's records show each paid half, each gets half of the remainder; if the deposit was one sum with no record of
shares, one refund to both jointly. Rules: 2.3-2.4, 6.6.

C9. No forwarding address, no email or phone. Statement and refund to the vacated unit within 14 days; unclaimed
money stays the tenant's and goes to the Comptroller after three years; the pre-reporting notice is excused because
the only address is the vacated unit. Rules: 6.5, 6.8.

C10. Building sold mid-tenancy. Deposit turned over with certified-mail notice; the buyer settles. Rent that fell due
before the sale is the seller's unless assigned in writing, so the buyer keeps nothing from the deposit for it. A buyer of a
multiple dwelling recovers no rent until it files its registration; a buyer of a one- or two-family house that must
register faces only the court's discretionary stay. Rules: 2.1, 0.5, 8.10.

C11. Tenant leaves furniture. Not held for rent; retrievable on request; disposed of only once abandoned; moving and
storage cost may be kept. Rules: 6.9.

C12. Tenant vacates Friday 2026-12-11; day 14 is Friday 2026-12-25, a public holiday; the statement is due Monday
2026-12-28. Rules: 6.3.

C13. Housing Choice Voucher tenant owes her share of one month. Only her share is charged; the owner keeps the
move-out month's assistance; refund within 14 days. Rules: 5.7.

C14. Former tenant owes $2,400 after the deposit; the owner hands it to a collection agency. The agency is a federal
debt collector and a licensed city agency. Because part of the balance is rent, it also needs a New York real
estate broker's licence, or the rent part goes to an attorney (Step 8.6a). It sends a validation notice to an address where the tenant now receives mail (the vacated unit does not
qualify once it knows the tenant moved) and verifies with the lease and the statement. The balance has a six-year limit and 2% statutory
interest (three years, with new pleading, notice, venue and default rules, for suits begun from the 90th day after
the pending act becomes law: `NY:S9760-pleading-service`, `NY:S9760-notice-mailings`, `NY:S9760-venue`,
`NY:S9760-default-judgment`). The state collection regulation does not apply. Before a
suit for rent, the certificate of occupancy, registration and rent-impairing violations are checked. Rules: 0.5,
8.1-8.6, 8.10.

T-232. Oral agreement at $2,400 a month, possession 2026-02-01, nothing said about length. Tenant leaves 2026-06-30
without notice. The letting is month to month (`NY:ADJ-RPL-232-monthly-letting`,
`NY:COMMONLAW-NYC-monthly-tenant-surrender`): nothing is owed after June, and no July rent may be kept from the
deposit. The statement is due Tuesday 2026-07-14. Same facts, but the tenant said she would stay "a long time":
RPL 232 runs the term to 2026-10-01 (`NY:ADJ-RPL-232-indefinite-term`); July rent, due 2026-07-01 and unpaid, may be
kept from the deposit if no new tenant took the unit (`NY:ADJ-early-departure-rent-retention`); August and September
are a later claim subject to re-letting (`NY:RPL-227-e`).

T-vacate. HPD vacates a unit for a structural hazard the owner was bound to repair, 2026-03-10. No rent after that
date and none kept from the deposit for it (`NY:ADJ-vacate-order-rent`). March rent, due 2026-03-01 and paid, is
earned for March 1-10 (10/31); the other 21/31 is refunded or credited, and the tenant may claim damages from the
owner.

T-lead. Pre-1960 two-family house, owner lives in one unit, tenant leaves the other. The lead turnover work is the
owner's cost and never a deduction (`NYC:HMC-27-2056.8-lead-turnover`); a smoke/CO combination detector the tenant
removed, if battery-operated, is charged at no more than $50 (`NYC:HMC-27-2045-detector-charge`).

T-collect. Former tenant owes $1,800 of rent after the deposit. If Handoff sends a demand in its own name or takes
the payment into its account, it needs a broker licence (`NY:HANDOFF-broker-config-collects-rent`). If the licensed
manager sends the demand and the payment link settles into the manager's account, Handoff needs none
(`NY:HANDOFF-broker-config-settlement-only`). If the balance is only damage, no broker licence is needed by anyone
(`NY:RPL-440(1)-rent-collection`).

C15. Tenant files bankruptcy on day 5 after vacating. The deposit may not be applied to pre-filing charges without
relief from the stay; the disputed part may be held while the landlord promptly moves for relief. The statement goes
out by day 14 without a payment demand; the rest of the refund goes to the chapter 7 trustee (or to the tenant as
debtor in chapter 13). Rules: 6.7, 8.8.

---

## Covered in later reviews

These rules are in the files and in force. The first groups govern stabilized, ETPA or controlled units (Review 2) or
subsidized public and project-based housing (a later review).

Review 2 (stabilized, ETPA and rent-controlled units; ETPA and rent control outside NYC are outside the aperture):
- deferred: `NYC:RCNY28-1-01`
- deferred: `NYC:RCNY28-1-12(b)-cap`
- deferred: `NYC:RCNY28-1-12(b)-escrow`
- deferred: `NYC:HPD-ESCROW-no-owner-draw`
- deferred: `NYC:HPD-ESCROW-regulatory-agreement`
- deferred: `NY:9NYCRR-2105.5`
- deferred: `NY:9NYCRR-2505.4`
- deferred: `NY:ADJ-RS-pre2025-7108-inapplicable`
- deferred: `NY:CASE-Karole-RS-via-RSC`
- deferred: `NY:GOL-7-107(1)`
- deferred: `NY:GOL-7-107(10)`
- deferred: `NY:GOL-7-107(2)`
- deferred: `NY:GOL-7-107(3)-excluded-costs`
- deferred: `NY:GOL-7-107(3)-refundable`
- deferred: `NY:GOL-7-107(4)-bar`
- deferred: `NY:GOL-7-107(4)-offer`
- deferred: `NY:GOL-7-107(5)-inspection`
- deferred: `NY:GOL-7-107(5)-notice`
- deferred: `NY:GOL-7-107(6)`
- deferred: `NY:GOL-7-107(6)-forfeiture`
- deferred: `NY:GOL-7-107(7)`
- deferred: `NY:GOL-7-107(8)`
- deferred: `NY:GOL-7-107(9)(a)`
- deferred: `NY:GOL-7-107(9)(b)`
- deferred: `NY:GOL-7-107(9)(c)`
- deferred: `NY:GOL-7-107(9)(d)`
- deferred: `NY:GOL-7-107(9)(e)`
- deferred: `NY:GOL-7-107-pre2025(1)-scope`
- deferred: `NY:GOL-7-107-pre2025(2)(a)`
- deferred: `NY:GOL-7-107-pre2025(2)(b)`
- deferred: `NY:GOL-7-107-pre2025(3)`
- deferred: `NY:L2025-c436-memo-gap`
- deferred: `NY:L2025-c436-s2`

Virginia review:
- deferred: `US:50USC3951-distress-VA`
- deferred: `US:50USC3955-deposit-clock-VA`

Later review (public housing and project-based or other subsidized housing):
- deferred: `US:15USC1692a(6)(C)`
- deferred: `US:15USC1692a(6)(C)-PHA-staff`
- deferred: `US:15USC1692a(6)(C)-private-manager`
- deferred: `US:24CFR983.259(c)-(e)`
- deferred: `US:24CFR983.352(a)`
- deferred: `US:24CFR983.353(b)`
- deferred: `US:24CFR5.233-debts-owed-PHA`
- deferred: `US:24CFR5.233-multifamily-no-debts`
- deferred: `US:24CFR5.303-animal-program-rules`
- deferred: `US:24CFR5.318(d)(1)`
- deferred: `US:24CFR880.608(b)`
- deferred: `US:24CFR880.608(c)`
- deferred: `US:24CFR880.608(d)`
- deferred: `US:24CFR880.608(d)(2)-forfeit`
- deferred: `US:24CFR880.608(d)-anchor`
- deferred: `US:24CFR880.608(e)`
- deferred: `US:24CFR880.608(f)`
- deferred: `US:24CFR881.601`
- deferred: `US:24CFR882.414`
- deferred: `US:24CFR883.701`
- deferred: `US:24CFR884.115`
- deferred: `US:24CFR886.116`
- deferred: `US:24CFR886.315`
- deferred: `US:24CFR891.435(b)(3)`
- deferred: `US:24CFR891.435(c)`
- deferred: `US:24CFR960.707(d)`
- deferred: `US:24CFR966.4(b)(2)`
- deferred: `US:24CFR966.4(b)(4)`
- deferred: `US:24CFR966.4(b)(4)-after-vacating`
- deferred: `US:24CFR966.4(b)(5)`
- deferred: `US:24CFR966.4(f)(10)`
- deferred: `US:24CFR966.4(i)`
- deferred: `US:24CFR966.4(k)(1)(i)`
- deferred: `US:24CFR966.4(n)(1)`
- deferred: `US:24CFR966.5`
- deferred: `US:24CFR966.53`
- deferred: `US:24CFR966.53(f)-former-tenant`
- deferred: `US:24CFR966.6`
- deferred: `US:7CFR3560.204(d)-(f)`
- deferred: `US:7CFR3560.204(f)-state-unclaimed`
- deferred: `US:HUD-4350.3-6-18C`
- deferred: `US:HUD-4350.3-6-18D`
- deferred: `US:HUD-4350.3-6-23E`
- deferred: `US:HUD-4350.3-6-24E`
- deferred: `US:HUD-4350.3-6-25D`
- deferred: `US:HUD-4350.3-6-29-moveout`
- deferred: `US:HUD-90105a-8`
- deferred: `US:HUD-90105a-8a-state-law`
- deferred: `US:HUD-SpecialClaims-procedure`
- deferred: `US:HUD-SpecialClaims-renewal`

In the files, but deciding nothing for a market-rate NYC unit (GBL art. 29-H does not reach a lease balance by its own
terms, and the city rule that imports its conduct standards is cited in 8.4; distress
does not exist in New York; an unclaimed refund falls under ABP 1315, not 1310; Attorney General enforcement is not a
manager's decision):
- deferred: `NY:GBL-600(1)`
- deferred: `NY:GBL-600(3)`
- deferred: `NY:GBL-601(2)`
- deferred: `NY:GBL-601(3)`
- deferred: `NY:GBL-601(4)`
- deferred: `NY:GBL-601(5)`
- deferred: `NY:GBL-601(6)`
- deferred: `NY:GBL-601(7)`
- deferred: `NY:GBL-601(8)`
- deferred: `NY:GBL-601(9)`
- deferred: `NY:GBL-601(12)`
- deferred: `NY:GBL-601-b`
- deferred: `NY:GBL-602`
- deferred: `US:50USC3951(a)(1)(B)`
- deferred: `US:FR-2026-04689`
- deferred: `NY:ABP-1310`
- deferred: `NY:GOL-7-109`
