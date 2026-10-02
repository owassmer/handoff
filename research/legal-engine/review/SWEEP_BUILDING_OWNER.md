# Sweep: building, owner and collecting-agent preconditions (discovery family 10), and RPL 232

2026-09-29. Scope: NY State, NYC and federal law for a market-rate NYC unit. Builder:
`build/sweep_building_owner.py` (idempotent; it always starts from `build/backups/{NY,NYC,US}_pre_sweep.json`).
Sections 1-7 are the first pass (29 atoms); section 8 is the resume pass after the pause: it corrects the RPL 232 and
broker-licensing atoms against decisions read after the first pass, compiles the sources that were fetched but
unused, and adds five atoms. Every quote and authority quote is verified against a saved file before anything is
written.

State after this pass:
- `stage_a_check.py` on NY, NYC, VA and US: 0 errors (NY 225 atoms, NYC 192, VA 277, US 179; cross-file 0).
- Mutation test: changing one word in the new quote of `NY:RPL-442-fee-split` ("regularly" to "usually") and one
  word in a new authority quote of `NY:ADJ-RPL-232-indefinite-term` makes the checker fail with 2 errors (exit 1).
- Rerunning the builder leaves the three files byte-identical.
- `review/NYC_MARKET_RATE.md` is unchanged. `check_review.py` lists the 34 sweep atoms as not cited (list at the end).
- 69 SWEEP_ source files (55 from the first pass, 14 added: Stauber is reused; new ones are Abbey, Hyacinth Green,
  1239 Madison v Neuburger, Norriv, Eaton, Kreuter, People v Darling, Sullivan v Rosson, GOL 5-703, CPLR 3015,
  22 NYCRR 208.42, 11 USC 1101, 1107, 1306).

---

## 1. Family 10 enumerated

| Item | Checked | In or out | Why |
|---|---|---|---|
| Certificate of occupancy, MDL 301-302 | earlier pass | in (`NY:MDL-301(1)`, `NY:MDL-302(1)(b)`) | bars rent in a multiple dwelling occupied without a CO |
| Illegal unit in a one- or two-family house | Pickering, Thomas v Brown | in: `NY:ADJ-MDL-rent-bar-not-1-2-family` | no statutory rent bar below three families |
| Cellar and basement rooms | Admin. Code 27-2087; MDL 34 | 27-2087 in; MDL 34 out | MDL 34 adds no rent rule beyond MDL 302 (see section 4) |
| HPD registration, MDL 325(2), Admin. Code 27-2107(b) | earlier pass | in | bars or stays rent claims |
| Registration pleading, 22 NYCRR 208.42(g) | text saved | out | reaches only a summary proceeding "to recover possession"; a move-out balance is a plenary action |
| Rent-impairing violations, MDL 302-a | earlier pass | in | |
| Vacate orders, Admin. Code 27-2139, 27-2140, 27-2142 | Younger v Campbell | in: `NY:ADJ-vacate-order-rent` | no rent after an owner-caused vacate order |
| Actual and constructive eviction | Barash (CoA) | in: `NY:COMMONLAW-constructive-eviction` | ends rent at abandonment |
| Tenant paid the landlord's utility bill, RPL 235-a | text | in: `NY:RPL-235-a` | credit against rent |
| Voucher HQS abatement | 24 CFR 982.404 | in: `US:24CFR982.404(d)(3)-(4)` | family's termination right; abated HAP never charged |
| Lead turnover, Local Law 1 | Admin. Code 27-2056.8 | in: `NYC:HMC-27-2056.8-lead-turnover` | owner's statutory cost |
| Mold and pest turnover, Local Law 55 | 27-2017.5 | in: `NYC:HMC-27-2017.5-turnover` | owner's statutory cost |
| Smoke, CO, gas detectors | 27-2045 | in: `NYC:HMC-27-2045-detector-charge` | capped charge |
| Window guards, bedbug notice, stove knobs, federal lead disclosure | read | out | no move-out charge or rent consequence |
| HPD emergency repair charges and liens | 27-2128, 27-2144 | in: `NYC:HMC-27-2128-owner-debt` | owner's debt, never a tenant charge |
| Relocation expenses, Alternative Enforcement Program charges | read | out | same character as 27-2128: owner's debt and lien |
| 7-A administrator, RPAPL 769-778 | 769, 770, 776, 778 | in: `NY:RPAPL-776-778-administrator` | administrator collects post-judgment rent |
| HPD receiver, Admin. Code 27-2130, 27-2135; MDL 309(5) | text | in: `NYC:HMC-27-2135(c)-receiver-rents` | receiver collects accrued and accruing rents |
| HPD rent levy, 27-2147; MDL 309(7) | text | in: `NYC:HMC-27-2147-rent-levy` | rent payable to HPD |
| Foreclosure receiver, CPLR 6401 | Holmes v Gravenhorst | in: `NY:CPLR-6401-foreclosure-receiver` | |
| Mortgagee with an assignment of rents | Sullivan v Rosson (CoA) | in (new): `NY:COMMONLAW-mortgagee-assignment-of-rents` | owner keeps collecting until the mortgagee takes the rents |
| Owner's death | Farmers' Loan v Wilson (CoA) | in: `NY:COMMONLAW-owner-death-agency` | manager's authority ends |
| Owner in chapter 7 | 11 USC 541, 704 | in: `US:11USC541-704-owner-chapter7` | trustee collects |
| Owner in chapter 11 or 13 | 11 USC 1101, 1107, 1306 | in (new): `US:11USC1107-1306-owner-reorganization` | owner keeps collecting |
| Collecting agent's broker licence, RPL 440-442-f | text, DOS guidance, cases | in (9 atoms, section 3) | decides who may collect rent |
| Fee-splitting, RPL 442 | text | in (new): `NY:RPL-442-fee-split` | decides whether a licensed manager may pay Handoff |
| DCWP licence pleading, CPLR 3015(e) | text | in (new): `NY:CPLR-3015(e)-licence-pleading` | condition on a licensed collector's suit |
| Loft Law IMDs, SROs, class B | read | out | not a market-rate apartment |
| RPL 232 (R2-08) | 13 decisions | in (6 atoms, section 2) | fixes the term of a no-term NYC agreement |

---

## 2. RPL 232 resolution

Question: does an NYC agreement for monthly rent with no stated term "particularly specify" a monthly duration (so
the month-to-month rules govern), or does RPL 232 run it to the next October 1?

Ruling: RPL 232 runs it to the next October 1. A statement of the rent per month is a rent term, not a period of
occupancy. Only an agreement that the letting itself is by the month ("month to month", "by the month", one month at
a time) specifies the duration.

Authority and why it prevails:
- Stauber v Antelo, 163 AD2d 246 (1st Dept 1990, unanimous): an oral sublet at a monthly rent, paid and accepted
  monthly, with "no agreement ... as to the period" ran by RPL 232 to October 1, and was month to month after. This
  is the highest and latest decision on the point.
- Spies v Voss (Common Pleas General Term 1890) and Souhami (2d Dept 1919) read the same words the same way: a monthly
  rent "does not affect the question"; the statute governs occupation "without a fixed period of letting having been
  agreed upon".
- Legislative purpose: the 1918 amendment made unwritten occupancies monthly; the 1920 committee restored the
  October 1 rule because tenants without written leases were being treated as monthly tenants and pressed with
  repeated increases (committee explanation quoted in 1239 Madison Ave. Corp. v Neuburger, 1922).
- Applied today in both Departments covering the city: Abbey v Henriquez (Sup Ct Kings 2006, written lease
  "indefinitely" at $1,000 a month) and Hyacinth Green v Green (Civ Ct Kings 2025, oral occupancy at a fixed monthly
  sum).
- Rejected: Spies's side remark that a monthly hiring with nothing said of the term is a tenancy for a month. Stauber
  is higher and later, and the 1920 re-enactment was made to stop exactly that treatment. Gilfoyle (App Term 1896)
  survives only for an agreement that the letting is by the month.
- Geiger v Braun (1876) and People v Darling (CoA 1872): an oral lease for more than a year is void (GOL 5-703(2));
  the tenant paying monthly is monthly from the start and RPL 232 does not apply, because a duration was stated.
  Geiger's further holding that such a tenant must give a month's notice does not govern: Darling decided a landlord's
  removal (now RPL 232-a), and T.I.B. v Repetto (App Term 1st Dept, affirmed by the Appellate Division) is later and
  higher on the tenant's side; RPL 232-b's tenant notice applies only outside the city.
- Souhami's year-to-year holdover rule and Norriv's (1930) are displaced by RPL 232-c: after the statutory term,
  accepted monthly rent makes the tenancy month to month.

Corrections made (the first-pass atoms had the opposite rule for a bare monthly rent):
- `NY:ADJ-RPL-232-monthly-letting` now covers only an agreement that the letting is by the month. Spies's remark is
  removed from its authorities; Stauber and the 1920 committee explanation are added.
- `NY:ADJ-RPL-232-indefinite-term` now covers any agreement that states a rent but no period, or an open stay. Its
  main quote is Stauber's; authorities add Souhami, 1239 Madison and Abbey.
- `NY:RPL-232` condition routes to the branches. `NY:ADJ-RPL-232-after-october` adds Norriv and Hyacinth Green.
- New: `NY:ADJ-RPL-232-oral-term-over-one-year`.
- Case-walk notes C4 and C6 (NY) rewritten to match.

What it changes for settlement: a tenant under a no-term agreement who leaves before the first October 1 of the
occupancy owes rent to September 30, as damages subject to the landlord's duty to re-rent (`NY:RPL-227-e`); the
14-day statement keeps only rent already due and unpaid. After that October 1 the monthly rules govern
(`NY:COMMONLAW-NYC-monthly-tenant-surrender`).

Dodge v Richmond and Futersak v Perl, listed in the checkpoint as RPL 232 decisions, are broker-licensing decisions
and are compiled in section 3.

---

## 3. Broker licensing resolution (highest consequence for Handoff)

Statute: RPL 440(1) makes a broker of anyone who "for another and for a fee ... collects or offers or attempts to
collect rent for the use of real estate"; 440-a requires the licence; 442-e makes each act a misdemeanor with a
penalty of one to four times the fee; 442-d and the illegality rule (Bendell, CoA) bar suing for the fee; 442-f
exempts court appointees, public officers and attorneys only.

Rulings:
1. A former tenant's balance is rent. The words carry no time limit, so rent that fell due during the tenancy (and
   rent reserved by the lease for months after an early departure) is still "rent for the use of real estate" when
   collected after move-out. Reading it so applies the words; it does not extend a penal statute.
2. Strict construction (Weingast, CoA; Kreuter and Eaton, 2d Dept) keeps out what the words do not name: charges
   other than the periodic rent (damage, late fees, utilities, a fixed lease-break sum), and use and occupancy owed
   after the tenancy ended, which the Real Property Law names separately as "reasonable compensation for the use and
   occupation" (RPL 220). Collecting only these needs no broker licence.
3. Settling a deposit statement is not collecting rent by itself. Computing the account, preparing the itemized
   statement, inspecting and refunding the tenant's own deposit are not listed acts. Three things are: (a) holding the
   deposit or a payment in an account one controls and applying or remitting it as rent; (b) demanding a rent balance,
   in anyone's name, by a letter one sends or by calls or messages; (c) receiving rent as the owner's agent. The
   Department of State draws the line at handling another person's money. A payment link that settles directly into
   the owner's or licensed manager's account, without Handoff taking custody, is the owner's collection.
4. The incidental-feature rule (Weingast, Dodge, Eaton) spares services about something else (a business sale, a
   financing plan). It does not spare rent collection within services for a rental property: the Second Department
   refused it for property-management services including rent collection (Fields v Pinkney, 2025), the Department of
   State requires the licence of a management company that collects rent, and a new label does not help (Futersak,
   2d Dept 2011, reversing the 2010 Supreme Court decision). The first-pass reasoning that Fields "rejected the
   doctrine for rent collection" overstated it; Fields held the plaintiffs raised no triable issue that their rent
   collection was incidental. The ruling for Handoff is unchanged because Handoff's whole engagement concerns the
   rental unit and its tenancy.
5. The owner and its salaried employees need no licence. Text confirms this: RPL 440(1) brings an owner's salaried
   employees in ("shall also include") only for article 9-A lot sales, so they are otherwise outside (Colon, CoA). A
   separate company collecting for a fee, even an affiliate, acts "for another".
6. A collection agency collecting the rent part for a fee needs the broker licence as well as its DCWP licence; an
   attorney needs neither broker licence (442-f); damage-only balances need none. A DCWP-licensed collector that sues
   pleads its licence (CPLR 3015(e)).
7. A licensed manager may pay Handoff for turnover, inspection and statement work without fee-splitting: RPL 442 lists
   leasing and renting, not rent collection, and 440(1) names those acts separately. It may not pay an unlicensed
   business for leasing help.

Handoff configurations (the choice is Owen's):
- Configuration 1, Handoff demands, receives or applies rent: broker licence required (company licence through a
  representative broker; rent-collecting staff licensed): `NY:HANDOFF-broker-config-collects-rent`.
- Configuration 2, Handoff settles, the owner or licensed manager holds the deposit, demands and receives: no licence:
  `NY:HANDOFF-broker-config-settlement-only`.
- Configuration 3, Handoff's people work as licensed salespersons under a manager's brokerage:
  `NY:HANDOFF-broker-config-under-broker`.
- Configuration 4, balance handed to a third-party collector: `NY:HANDOFF-broker-config-collection-agency`.

Atoms corrected: `NY:RPL-440(1)-rent-collection` (condition names the three acts, the move-out balance, the
exclusions and the incidental test; new authorities Eaton, Kreuter, Dodge, Futersak, DOS fiduciary line, RPL 220),
`NY:RPL-442-d-442-e-unlicensed` (Futersak), `NY:ADJ-broker-owner-and-staff` (article 9-A text, Colon),
`NY:HANDOFF-broker-config-collects-rent` (incidental reasoning corrected), `NY:HANDOFF-broker-config-settlement-only`
(the three acts, the letterhead point, payment links). Unchanged after recheck: `NY:RPL-442-f-exemptions`,
`NY:HANDOFF-broker-config-under-broker`, `NY:HANDOFF-broker-config-collection-agency`.

---

## 4. Sources fetched in the first pass and not used then

| Source | Disposition |
|---|---|
| Dodge v Richmond (1st Dept 1958) | compiled: authority in `NY:RPL-440(1)-rent-collection`, `NY:HANDOFF-broker-config-collects-rent` |
| Futersak v Perl (2d Dept 2011) | compiled: `NY:RPL-440(1)-rent-collection`, `NY:RPL-442-d-442-e-unlicensed` |
| Futersak v Perl (Sup Ct 2010) | changes nothing: reversed in 2011 |
| Geiger v Braun (1876) | compiled: `NY:ADJ-RPL-232-oral-term-over-one-year` (its notice holding rejected, section 2) |
| Souhami v Brownstone (2d Dept 1919) | compiled as history in `NY:ADJ-RPL-232-indefinite-term`; its 1918-text holding changes nothing (text replaced in 1920; holdover rule displaced by RPL 232-c) |
| RPAPL 769, 770 | compiled as authority in `NY:RPAPL-776-778-administrator` (who may sue, grounds); the rent consequence comes only from 776 and 778 |
| MDL 34 | changes nothing: a cellar or basement room in breach is occupancy the CO does not permit, already decided by `NY:MDL-302(1)(b)` |
| MDL 309 | compiled: 309(5) receiver in `NYC:HMC-27-2135(c)-receiver-rents`; 309(7) rent demand in `NYC:HMC-27-2147-rent-levy` |
| RPL 442 | compiled: `NY:RPL-442-fee-split` |
| Admin. Code 27-2130 | compiled in `NYC:HMC-27-2135(c)-receiver-rents`: HPD receiverships reach multiple dwellings only |
| Admin. Code 27-2139, 27-2140 | compiled in `NY:ADJ-vacate-order-rent`: the vacate power and the order requiring every occupant to leave |

---

## 5. Every sweep atom: controlling authority and adjudication

RPL 232 and the ending of no-term tenancies
- `NY:RPL-232` (RPL 232 text): an NYC agreement that does not particularly specify its duration runs to the first
  October 1 after possession began.
- `NY:ADJ-RPL-232-indefinite-term` (Stauber, 1st Dept): a monthly rent with no agreed period, or an open stay, is
  such an agreement; a tenant leaving before October 1 owes rent to September 30, subject to re-letting.
- `NY:ADJ-RPL-232-monthly-letting` (Gilfoyle; consistent with Stauber): an agreement that the letting is by the
  month specifies the duration, so the monthly rules apply from the start.
- `NY:ADJ-RPL-232-after-october` (RPL 232-c; Stauber; Adina): after the statutory term, accepted rent makes the
  tenancy month to month; no second statutory year.
- `NY:ADJ-RPL-232-agreement-sets-end` (City of New York v State, CoA): an agreement that says how it ends governs;
  RPL 232 does not override it, and Adina's contrary reading yields to the Court of Appeals.
- `NY:ADJ-RPL-232-oral-term-over-one-year` (GOL 5-703(2); Darling, CoA; T.I.B.): an oral term over a year is void; the
  tenant is monthly from the start and may leave at the end of any month without notice.

Building status and building-caused endings
- `NY:ADJ-MDL-rent-bar-not-1-2-family` (Pickering, App Term 2d Dept): no statutory rent bar for an illegal unit in a
  house of two families or fewer; a third family makes it a multiple dwelling.
- `NYC:HMC-27-2087-cellar-basement` (Admin. Code 27-2087, as amended 2026): a cellar room may be rented only as a
  certified ancillary dwelling unit; breach makes the unit illegal but does not bar rent in a one- or two-family house.
- `NY:ADJ-vacate-order-rent` (Younger v Campbell, 1st Dept; Admin. Code 27-2139, 27-2140, 27-2142): no rent after a
  vacate order the owner was bound to prevent; tenant-caused conditions are no defense.
- `NY:COMMONLAW-constructive-eviction` (Barash, CoA): substantial deprivation plus abandonment ends rent; a physical
  exclusion suspends all rent.
- `NY:RPL-235-a` (RPL 235-a): a utility bill the tenant paid for the landlord is credited against rent.
- `US:24CFR982.404(d)(3)-(4)` (24 CFR 982.404, 982.451): during HQS abatement the voucher family may end the tenancy;
  abated assistance is never the family's debt.

Turnover work whose cost is the owner's
- `NYC:HMC-27-2056.8-lead-turnover` (Admin. Code 27-2056.8, 27-2056.15): lead remediation at turnover is the owner's
  duty and cost; never a deposit deduction.
- `NYC:HMC-27-2017.5-turnover` (Admin. Code 27-2017.5): mold and pest remediation before re-occupancy in a multiple
  dwelling is the owner's cost unless it repairs tenant-caused damage.
- `NYC:HMC-27-2045-detector-charge` (Admin. Code 27-2045(e)): a detector lost or disabled during the tenancy is
  charged only up to $25, $50 or $75 by type.
- `NYC:HMC-27-2128-owner-debt` (Admin. Code 27-2128, 27-2144): HPD repair charges and penalties are the owner's debt;
  the owner may claim tenant-caused damage only as damage, at reasonable cost.

Who is owed and may collect
- `NY:RPAPL-776-778-administrator` (RPAPL 776, 778): rent after a 7-A judgment is the administrator's to collect.
- `NYC:HMC-27-2135(c)-receiver-rents` (Admin. Code 27-2135; 27-2130; MDL 309(5)): an HPD receiver of a multiple
  dwelling collects accrued and accruing rents.
- `NYC:HMC-27-2147-rent-levy` (Admin. Code 27-2147; MDL 309(7)): after HPD's notice, rent is paid to HPD and counts as
  paid to the owner.
- `NY:CPLR-6401-foreclosure-receiver` (CPLR 6401; Holmes v Gravenhorst): a foreclosure receiver collects the rents
  its order covers, including rents due and unpaid.
- `NY:COMMONLAW-mortgagee-assignment-of-rents` (Sullivan v Rosson, CoA): a mortgage assignment of rents is a pledge;
  the owner collects until the mortgagee takes the rents by possession, arrangement or receiver.
- `NY:COMMONLAW-owner-death-agency` (Farmers' Loan v Wilson, CoA): the owner's death ends the manager's authority; the
  estate fiduciary collects.
- `US:11USC541-704-owner-chapter7` (11 USC 541, 704): in chapter 7 the trustee collects; the deposit stays the
  tenant's.
- `US:11USC1107-1306-owner-reorganization` (11 USC 1101, 1107, 1306): in chapter 11 without a trustee, or chapter 13,
  the owner keeps collecting.

Licensing and pleading of the collecting agent
- `NY:RPL-440(1)-rent-collection` (RPL 440(1), 440-a; Fields; Weingast): collecting rent, including a move-out rent
  balance, for another for a fee requires a broker licence; non-rent charges and use and occupancy do not.
- `NY:RPL-442-d-442-e-unlicensed` (RPL 442-d, 442-e; Bendell, CoA; Fields; Futersak): each unlicensed act is a
  misdemeanor; the fee is unrecoverable and up to four times it is payable; the owner's claim is unaffected.
- `NY:RPL-442-f-exemptions` (RPL 442-f; Colon, CoA): only court appointees, public officers and attorneys are exempt.
- `NY:ADJ-broker-owner-and-staff` (RPL 440(1), (3); DOS guidance; Colon): the owner and its salaried staff need no
  licence; a broker's rent-collecting staff do.
- `NY:RPL-442-fee-split` (RPL 442(1)): a licensed broker may pay Handoff for non-brokerage work, not for leasing help.
- `NY:CPLR-3015(e)-licence-pleading` (CPLR 3015(e)): a DCWP-licensed collector suing a former tenant pleads its
  licence or faces dismissal.
- `NY:HANDOFF-broker-config-collects-rent`, `NY:HANDOFF-broker-config-settlement-only`,
  `NY:HANDOFF-broker-config-under-broker`, `NY:HANDOFF-broker-config-collection-agency`: section 3.

---

## 6. Over-scope items (recorded, not compiled)

- A licensed broker's own operating duties (escrow of client money, supervision, advertising): they arise only if Owen
  chooses Configuration 1 and belong to that build.
- Rent-stabilized and rent-controlled consequences of the same building facts (DHCR rent reductions for service
  failures, fair-market-rent appeals): the second review.
- Loft Law interim multiple dwellings, SROs and class B dwellings: not market-rate apartments.
- Money-transmission licensing if Handoff ever holds tenant funds: a payments-regulation question outside the
  tenancy-settlement aperture; it arises only in Configuration 1 and belongs to that build.

---

## 7. Proposed walk text for review/NYC_MARKET_RATE.md

Ferro folds these in; the review walk was not edited.

### Step 0.5 (building facts): add after the three existing bullets

- A one- or two-family house. The rent bars above apply only to multiple dwellings. A house of one or two families
  with an illegal unit (a basement apartment, a second unit in a one-family house) still recovers rent and may keep
  the deposit for it; a third family makes it a multiple dwelling: `NY:ADJ-MDL-rent-bar-not-1-2-family`. A cellar
  room may be rented only as a certified ancillary dwelling unit: `NYC:HMC-27-2087-cellar-basement`.
- Who is owed the rent. Check before collecting that the owner still holds the rent claim. A 7-A administrator
  collects rent after its judgment: `NY:RPAPL-776-778-administrator`. An HPD receiver collects accrued and accruing
  rents: `NYC:HMC-27-2135(c)-receiver-rents`. After an HPD rent notice, rent goes to HPD and counts as paid:
  `NYC:HMC-27-2147-rent-levy`. A foreclosure receiver collects what its order covers:
  `NY:CPLR-6401-foreclosure-receiver`. A mortgagee with an assignment of rents collects only after it takes the rents:
  `NY:COMMONLAW-mortgagee-assignment-of-rents`. If an individual owner dies, the manager's authority ends and the
  estate collects: `NY:COMMONLAW-owner-death-agency`. If the owner is in chapter 7 the trustee collects:
  `US:11USC541-704-owner-chapter7`; in chapter 11 without a trustee, or chapter 13, the owner keeps collecting:
  `US:11USC1107-1306-owner-reorganization`. In every case the deposit stays the tenant's money.

### Step 3 (ending): add as 3.2a, after the month-to-month bullets

3.2a No stated term. An NYC agreement, oral or written, that states a rent but no period of occupancy runs to the
first October 1 after possession began: `NY:RPL-232`, `NY:ADJ-RPL-232-indefinite-term`. A rent "of $X a month" is
not a period; a tenant who leaves before that October 1 owes rent to September 30, subject to re-letting
(`NY:RPL-227-e`). After that October 1 the tenancy is month to month: `NY:ADJ-RPL-232-after-october`. An agreement
that the letting itself is month to month is monthly from the start: `NY:ADJ-RPL-232-monthly-letting`. An agreement
that says how it ends governs: `NY:ADJ-RPL-232-agreement-sets-end`. An oral lease for more than a year is void and the
tenancy is monthly from the start: `NY:ADJ-RPL-232-oral-term-over-one-year`. Judgment where the words are in dispute.

### Step 3 (ending): add as 3.6

3.6 The building ends the tenancy. If a vacate order issues for conditions the owner was bound to prevent, no rent is
owed after the tenant had to leave: `NY:ADJ-vacate-order-rent`. If the landlord's acts substantially deprived the
tenant of the unit and the tenant left for that reason, no rent or re-letting claim runs after the departure; a lockout
suspends all rent: `NY:COMMONLAW-constructive-eviction`. Judgment. A voucher family may end the tenancy during an HQS
abatement, and the abated assistance is never its debt: `US:24CFR982.404(d)(3)-(4)`.

### Step 5 (account): add as 5.x, "Credits and owner costs"

- A utility bill the tenant paid for the landlord is credited against rent: `NY:RPL-235-a`. Rent paid to HPD under a
  levy is credited as paid: `NYC:HMC-27-2147-rent-levy`.
- Turnover work the law puts on the owner is never a charge: lead remediation in a pre-1960 building,
  `NYC:HMC-27-2056.8-lead-turnover`; mold and pest remediation before re-occupancy in a multiple dwelling,
  `NYC:HMC-27-2017.5-turnover` (Judgment where the tenant caused the condition); HPD repair charges and penalties,
  `NYC:HMC-27-2128-owner-debt`. A detector lost or disabled during the tenancy is charged only within the $25/$50/$75
  caps: `NYC:HMC-27-2045-detector-charge`.

### Step 8 (collecting): add as 8.6a, after city licensing

8.6a State licensing of whoever collects rent. Collecting rent for another for a fee, including a move-out rent
balance, requires a New York broker's licence; collecting only damage, fees, utilities or use and occupancy does not:
`NY:RPL-440(1)-rent-collection`. The owner and its salaried staff need none: `NY:ADJ-broker-owner-and-staff`. Only
court appointees, public officers and attorneys are exempt; a collection agency is not:
`NY:RPL-442-f-exemptions`. Collecting unlicensed is a misdemeanor and forfeits the fee, but the owner's claim is
unaffected: `NY:RPL-442-d-442-e-unlicensed`. A licensed manager may pay Handoff for settlement work, not for leasing
help: `NY:RPL-442-fee-split`. Handoff by configuration: it needs the licence if it demands, receives or applies rent:
`NY:HANDOFF-broker-config-collects-rent`; it does not if it only settles while the owner or licensed manager holds the
deposit, demands and receives: `NY:HANDOFF-broker-config-settlement-only`; its people may instead collect as licensed
salespersons of a broker: `NY:HANDOFF-broker-config-under-broker`; a third-party collector of the rent part needs the
broker licence too: `NY:HANDOFF-broker-config-collection-agency`. Which one applies is a later operating choice.

### Step 8 (collecting): add to 8.10

- A DCWP-licensed collector that sues a former tenant pleads its licence name and number or faces dismissal:
  `NY:CPLR-3015(e)-licence-pleading`.

### Step 9 (test cases): add

- T-232. Oral agreement at $2,400 a month, possession 2026-02-01, nothing said about length. Tenant leaves 2026-06-30
  without notice. RPL 232 fixes the term to 2026-10-01 (`NY:ADJ-RPL-232-indefinite-term`). The statement is due by
  2026-07-14; July rent fell due 2026-07-01 and may be kept from the deposit if unpaid and no new tenant took the unit
  (`NY:ADJ-early-departure-rent-retention`); August and September are a later claim subject to re-letting
  (`NY:RPL-227-e`). Same facts but the agreement said "month to month": nothing is owed after June
  (`NY:ADJ-RPL-232-monthly-letting`, `NY:COMMONLAW-NYC-monthly-tenant-surrender`).
- T-vacate. HPD vacates a unit for a structural hazard the owner was bound to repair, 2026-03-10. No rent after that
  date and none kept from the deposit for it (`NY:ADJ-vacate-order-rent`); February rent stays owed.
- T-lead. Pre-1960 two-family house, owner lives in one unit, tenant leaves the other. The lead turnover work is the
  owner's cost and never a deduction (`NYC:HMC-27-2056.8-lead-turnover`); a smoke/CO combination detector the tenant
  removed is charged at no more than $50 (`NYC:HMC-27-2045-detector-charge`).
- T-collect. Former tenant owes $1,800 of rent after the deposit. If Handoff sends a demand in its own name or takes
  the payment into its account, it needs a broker licence (`NY:HANDOFF-broker-config-collects-rent`). If the licensed
  manager sends the demand and the payment link settles into the manager's account, Handoff needs none
  (`NY:HANDOFF-broker-config-settlement-only`). If the balance is only damage, no broker licence is needed by anyone
  (`NY:RPL-440(1)-rent-collection`).

---

## 8. Case walks updated

NY: C3, C4, C6, C7, C10 and C14 (first pass) and in this pass C4, C6, C7, C9, C10, C14; C4 and C6 notes rewritten
for the RPL 232 ruling. NYC: C3, C4, C7, C10, C14 (first pass) and C14 (CPLR 3015(e)) in this pass.

## 9. New ids that check_review.py reports as not cited (34)

`NY:ADJ-MDL-rent-bar-not-1-2-family`, `NY:ADJ-RPL-232-after-october`, `NY:ADJ-RPL-232-agreement-sets-end`,
`NY:ADJ-RPL-232-indefinite-term`, `NY:ADJ-RPL-232-monthly-letting`, `NY:ADJ-RPL-232-oral-term-over-one-year`,
`NY:ADJ-broker-owner-and-staff`, `NY:ADJ-vacate-order-rent`, `NY:COMMONLAW-constructive-eviction`,
`NY:COMMONLAW-mortgagee-assignment-of-rents`, `NY:COMMONLAW-owner-death-agency`, `NY:CPLR-3015(e)-licence-pleading`,
`NY:CPLR-6401-foreclosure-receiver`, `NY:HANDOFF-broker-config-collection-agency`,
`NY:HANDOFF-broker-config-collects-rent`, `NY:HANDOFF-broker-config-settlement-only`,
`NY:HANDOFF-broker-config-under-broker`, `NY:RPAPL-776-778-administrator`, `NY:RPL-232`, `NY:RPL-235-a`,
`NY:RPL-440(1)-rent-collection`, `NY:RPL-442-d-442-e-unlicensed`, `NY:RPL-442-f-exemptions`, `NY:RPL-442-fee-split`,
`NYC:HMC-27-2017.5-turnover`, `NYC:HMC-27-2045-detector-charge`, `NYC:HMC-27-2056.8-lead-turnover`,
`NYC:HMC-27-2087-cellar-basement`, `NYC:HMC-27-2128-owner-debt`, `NYC:HMC-27-2135(c)-receiver-rents`,
`NYC:HMC-27-2147-rent-levy`, `US:11USC1107-1306-owner-reorganization`, `US:11USC541-704-owner-chapter7`,
`US:24CFR982.404(d)(3)-(4)`.

The proposed walk text in section 7 cites all 34: `check_review.py` run on a scratch copy of the walk plus section 7
reports 0 not cited (the walk itself was not edited).
