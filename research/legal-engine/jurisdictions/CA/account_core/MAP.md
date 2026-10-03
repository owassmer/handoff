# California account-core legal map

Draft for the coordinator, October 3, 2026. Proposal only: no rule here is accepted or compiled.

**Setting.** A departing tenancy at a market-rate apartment community in Huntington Beach (Orange County). The owner is a private institution with a third-party manager. The move-out is in 2026. Decision points come from `pipeline/chain_map.json` (DP0–DP9, PW0, PW3).

**Layers.** [US] federal, [CA] state, [OC] Orange County, [HB] Huntington Beach. Neither OC nor HB has an account rule identified for this setting. County ordinances on these subjects reach only unincorporated areas. HB has no rent-stabilization, just-cause, deposit-interest or collection ordinance identified, but the search was not exhaustive (GAPS.md). So the account is governed by state and federal law.

**How each entry is marked**
- **Code** — computable from records (dates, amounts, caps).
- **Judgment** — a standard that needs judgment.
- **(T)** — read in official text: a saved capture under `jurisdictions/CA/texts/`, or a federal source under `research/legal-engine/sources/`.
- **(G)** — official guidance, not law. Mainly the DRE *California Tenants* guide, 2026 edition, at `account_core/sources/DRE_2026_Landlord_Tenant_Guide.txt`.
- **(M)** — case text read from a mirror, not an official reporter.
- **(I)** — my inference or a reasoned application.
- **(N)** — cited from secondary material and not read here.

Section numbers are the Civil Code unless marked.

---

## DP0 Unit status and the regimes that apply

**DP0.1 Rent regulation and just cause**
- [CA] 1946.2 (T), as amended by AB 1529 (Stats. 2025 ch. 203), effective Jan 1, 2026.
  - After 12 months of occupancy, termination requires just cause.
  - A no-fault termination requires relocation equal to one month's rent, or a written waiver of the final month's rent before it falls due (d)(1)–(3).
  - Strict compliance is required, or the notice is void (d)(4).
  - If the tenant fails to vacate, the relocation payment or waiver is recoverable only as damages in the action for possession (d)(3)(B).
  - Account effect: an owner-initiated no-fault ending puts a credit (the waived final month) or a payable into the account.
- [CA] 1947.12 rent cap (T).
  - Rent collected above the cap is recoverable by the tenant, as damages for the excess. In a dispute this is an offset the tenant can raise.
- Exemptions that decide coverage (Code), from 1946.2(e) and 1947.12(d):
  - certificate of occupancy within the previous 15 years;
  - deed- or agreement-restricted affordable housing (a later variation);
  - single-family homes owned by natural persons, with notice.
  - An institutional owner of a 1970s building is covered (I).
- Both sections are repealed Jan 1, 2030.
- [HB] No local regime identified.

**DP0.2 Which deposit regime applies**
1950.5(a) covers security for a dwelling (T). Which branch of 1950.5 applies is decided by dates (Code):

| Branch | Date that triggers it | Rule |
|---|---|---|
| (c)(1) | Security demanded or received on or after Jul 1, 2024 ((c)(6)) | Cap of one month's rent |
| (b)(3) | Tenancy began after Jan 1, 2003 | Cleaning only back to the cleanliness at the inception of the tenancy |
| (g)(1) | Tenancy began on or after Jul 1, 2025 | Move-in photographs required |
| (g)(2) | Possession returned on or after Apr 1, 2025 | Photographs required after possession returns, and again after repairs |
| (h)(1)(A)(ii) and (C) | AB 414 (Stats. 2025 ch. 340), effective Jan 1, 2026 | Electronic refund duty; agreements among multiple tenants |

The version that governs a statement is the one in force on the vacate date (I; no transition clause was found in AB 414).

Chapter 2.5 (water submeters) applies only where submeters are used, or were required, to bill water separately (1954.216) (T).

**DP0.3 Can rent be recovered**
- 1942.4 (T). The landlord may not demand or collect rent while all of these hold:
  - a housing official has cited substandard conditions in writing;
  - the conditions remain unabated 35 days after the notice, without good cause;
  - the tenant did not cause them.
  - Code: the citation date plus 35 days. Judgment: good cause, and whether the tenant caused the condition.
- 1962(c) (T). A successor owner or manager who has not made the disclosures within 15 days may not evict for rent that accrued during the noncompliance. The tenant still owes that rent. This matters for the building-sold template.
- The warranty of habitability is a rent-reduction defense in disputes. The leading case is *Green v. Superior Court* (1974) 10 Cal.3d 616 (N).
- Capacity of the owner entity to sue: CORP 17708.07, CORP 2203 and RTC 23301 (T). See DP8.9.

**DP0.4 Status facts to record at intake**
These are the facts that switch branches below:
- owner entity type and registration, and the manager's DRE broker licence;
- certificate-of-occupancy date;
- lease start date (move-in photo duty), and the dates the deposit was demanded and paid (cap);
- whether any rent or the deposit was paid electronically (refund method);
- adult tenants on the lease, and adult tenants residing;
- water billing method (submeter or ratio/RUBS) and gas/electric metering;
- internet bulk billing (1942.8);
- voucher or HAP contract;
- servicemember status;
- whether the unit is restricted or publicly owned (out of this milestone; GAPS).

---

## DP1 Facts fixed at move-in

**DP1.1 Lawful deposit and advance payments**
- 1950.5(b) (T). "Security" includes any payment, fee, deposit or charge imposed at the beginning of the tenancy, other than the 1950.6 screening fee. So a move-in, administrative or pet "fee" is security: it counts toward the cap and is refundable subject to (e) (I from the text).
- Cap (c)(1) (T): one month's rent. The two-month exception for small landlords in (c)(5) is not available to an institutional owner.
- (c)(2): six months' advance rent is allowed on a lease of six months or more.
- (c)(4): a servicemember's higher-than-standard security must be returned after six months without arrears.
- (n): a lease may not call security "nonrefundable".
- Code: compare the total of start-of-tenancy charges with the cap. An excess is a tenant claim, and bad-faith exposure under (m).
- SB 1296 (Stats. 2026 ch. 1025) adds 1942.7.5, operative Apr 1, 2027: pet-policy disclosure, and refund of the application fee when the policy was not disclosed. It is pre-tenancy only, with no effect on the move-out account (read).

**DP1.2 How the deposit is held**
- 1950.5(d) (T): security is held for the tenant who is a party to the lease. The tenant's claim ranks ahead of the landlord's creditors.
- No statewide rule on interest, a separate account or a bank notice was found in the deposit statutes read. No HB interest ordinance was identified (I; absence). Code: interest owed = 0.
- If a DRE-licensed manager receives the deposit, BPC 10145 trust-fund rules apply (T); the regulation 10 CCR 2832 was not retrieved. A breach is a licensing matter. It does not change the tenant's account (I).

**DP1.3 Move-in condition record**
- No statutory move-in inspection or checklist exists (I; absence in 1950.5).
- (g)(1) (T): for tenancies beginning on or after Jul 1, 2025, photographs are required "immediately before, or at the inception of" the tenancy. (h)(2)(D) requires the (g) photographs to accompany every repair or cleaning deduction.
- For earlier tenancies, any credible record of move-in condition serves as evidence. The landlord carries the burden on reasonableness ((m) and *Granberry*).

**DP1.4 Fees disclosed or barred at signing (they carry into the move-out account)**
- Barred outright (T):
  - a fee for paying rent or deposit by check (1947.3(b));
  - a fee for serving, posting or delivering any notice under CCP 1161 (1161(6); SB 611, operative Feb 1, 2025);
  - any "nonrefundable" security (1950.5(n));
  - any lease clause requiring professional cleaning, unless reasonably necessary (1950.5(e)(2)(C));
  - lease waivers of 1950.5 or 1954 rights, which are void (1953(a)(1)).
- Penalty test for fixed sums such as late fees, lease-break fees or a holdover premium:
  - 1671(d) (T): in a residential lease, a liquidated-damages clause is void unless fixing actual damages would be impracticable or extremely difficult.
  - Late-fee case law (*Orozco v. Casimiro* (2004) 121 Cal.App.4th Supp. 7) is (N).
  - Judgment: impracticability, and whether the sum reasonably estimates actual loss.
- Water (submetered) (T):
  - pre-lease written disclosure in 10-point type (1954.204);
  - a billing or administrative fee no higher than the lesser of $4.75 (adjusted by CPI) or 25% of the usage charge (1954.205(a)(3));
  - late fees under 1954.213;
  - no pass-through of the landlord's own deposits, penalties, disconnection or late fees to the purveyor (1954.208).
- Gas and electric: 1940.9 shared meters (T). PUC 739.5(a) (T): a master-meter customer serving apartment tenants must charge each user the rate the utility would charge directly. Code: the tenant's gas or electric charge cannot exceed the utility tariff for that usage.
- Internet: 1942.8 (T), from Jan 1, 2026. The tenant may opt out of bulk-billed internet. If the landlord refuses, the tenant may deduct the cost from rent. Code: credit the bulk-billing charges made after the opt-out.
- The CLRA drip-pricing rule (1770(a)(29), SB 478) may not reach residential leases. One line in GAPS.

**DP1.5 Owner records the settlement relies on**
- 1962 (T): disclosure of the owner's and manager's names and addresses for service and notices. A signer who does not disclose becomes the owner's agent for service and notices (1962(d)).
- (g) photographs.
- Lead-paint disclosures do not change the account (out of scope).

**DP1.6 Electronic contact and delivery**
- Statement by email: (h)(1)(B)(ii) (T), "upon mutual agreement … at the commencement of the tenancy or at any time during or after the tenancy." A written agreement collected on the tenant page satisfies it (I).
- Refund: electronic return is mandatory where the tenant paid the security or rent electronically, to an account the tenant designates in writing ((h)(1)(A)(ii)).
- Water bills: electronic delivery needs written agreement and can be rescinded (1954.206(b)) (T).
- UETA (1633.7) (T): an electronic record satisfies a writing requirement once the parties have agreed to transact electronically (1633.5, not saved).

**DP1.7 Payment methods and receipts**
1947.3(a)(1) (T): the landlord must accept at least one method that is neither cash nor electronic funds transfer. Cash-only is allowed for three months after a dishonored check (a)(2). Third-party payment rules are in (a)(3). No receipt rule specific to the account was identified (thin).

---

## DP2 Events during the tenancy

**DP2.1 The building is sold**
- On sale, 1950.5(i) requires within a reasonable time one of:
  - (i)(1): transfer the remaining security to the successor and notify the tenant by personal delivery or first-class mail, listing the claims made, the amount transferred and the successors' names, addresses and telephones; or
  - (i)(2): return the security with an (h) accounting.
- (j): a written statement must go to the successor before transfer.
- (k)(1): noncompliance makes the successor jointly liable. (k)(2): the successor may still recover damages beyond the security. (k)(3): a successor who has a good-faith belief after inquiry and reasonable investigation escapes (m) damages.
- (l): a successor holding security has the landlord's obligations.
- (h)(1)(A)(ii)(I): the successor must refund electronically only if it received rent electronically.
- 1962(c) (rent accrued during noncompliance; see DP0.3).
- Code: transfer and notice dates. Judgment: "reasonable investigation" under (k)(3). All (T).

**DP2.2 Assignment or sublet**
- Security is held for "the tenant who is party to the lease" ((d)) (T).
- The refund goes to the adult tenants "on the rental or lease agreement at the time the tenancy terminates" ((h)(1)(C)(i)) (T). An approved assignee who is on the lease at termination is the payee (I).
- The transfer-of-lessee's-interest statutes (1995.010 et seq.) were not retrieved; their account effect is thin (GAPS).

**DP2.3 Tenant, occupant or guarantor**
- (h)(1)(C) uses two different sets: "adult tenants residing in the unit" (whether the multi-tenant rule applies) and "adult tenants on the rental or lease agreement at the time the tenancy terminates" (the payees). An occupant not on the lease is not a payee (I).
- Guarantor liability is suretyship law (2787 et seq., not retrieved). The guarantor is not a payee (I).

**DP2.4 One co-tenant leaves first**
The 21-day clock runs from when "the tenant has vacated the premises" ((h)(1)) (T). Reading the clock from surrender of the whole premises, not one co-tenant's departure, is (I). No statute addresses partial vacatur. A tenant who ends a lease under 1946.7 may ask that the refund be split otherwise ((h)(1)(C)(iii)).

**DP2.5 Death or incapacity of the tenant**
- 1934 (T): a hiring terminable at will (periodic) ends on notice of the death. A fixed term is not ended by death.
- (G) DRE guide p. 88:
  - The estate is liable for the rest of a fixed term, subject to the landlord's good-faith re-letting.
  - A periodic tenancy ends on the 30th day after the last rent payment.
- The refund is the decedent's property. It goes to the personal representative or to a small-estate successor under PROB 13100 and 13101 (T). The affidavit procedure applies 40 days after death when the estate is under the 13100 threshold. The text says $166,250, as adjusted under Prob 890; the current adjusted figure must be read from the Judicial Council table (GAPS). Code: date of death + 40 days, and an affidavit on file.
- A balance claim against the estate has to fit the probate claim period (PROB 9100 (T): the later of four months after letters issue or 60 days after notice of administration, without extending CCP 366.2) and the one-year limit after death (CCP 366.2 (T)). Code: date of death + 1 year.
- Belongings: 1980–1991 and 1965 (DP6.9).

**DP2.6 Casualty**
- 1932(2): the tenant may end the tenancy when the greater part of the premises perishes other than from the tenant's want of ordinary care. 1933(4): the hiring ends on destruction.
- 1941.9 (T), from Jan 1, 2026 (SB 610):
  - advance rent covering any period after termination must be returned within 21 days, to the address the tenant provides or else the unit;
  - termination date = the tenant's notice of intent, or other dates in (a)(3).
- 1935 (T): rent is due only in proportion to use actually made.
- Code: per-diem refund. Judgment: "greater part" or "material inducement", and the tenant's want of care.
- Relocation is owed when a local enforcement agency orders vacation because violations endanger health and safety (HSC 17975(a) (T); amounts in 17975.2 et seq., not retrieved). Untenantability alone does not trigger it.

---

## DP3 How the tenancy ends and when rent stops

**DP3.1 End of a fixed term**
- 1945 (T): if rent is accepted after the term expires, a renewal is presumed — month to month where rent is monthly.
- 1945.5 (T): an automatic-renewal clause is voidable unless printed in at least 8-point bold in the body, with a bold recital just above the signature.
- 1946.2 limits owner-initiated endings only.
- Code: the lease end, the vacate date, and the dates rent was accepted.

**DP3.2 Periodic tenancy notice**
1946 and 1946.1 (T): the tenant gives notice at least as long as the rental period; the owner gives 30 or 60 days. Code: the notice-effective date bounds the rent owed.

**DP3.3 The tenant leaves early**
- 1951.2 (T): the landlord recovers unpaid rent less the rental loss the tenant proves could reasonably have been avoided.
  - Code: rent to the re-let date, less the new tenant's rent.
  - Judgment: reasonable mitigation (the burden is on the tenant).
- 1951.3 (T): written notice of belief of abandonment is allowed after 14 consecutive days of unpaid rent and a reasonable belief of abandonment. The lease ends 15 days after personal service, or 18 days after mailing, unless the tenant objects in writing.
- 1951.4 (T): continuing the lease is available only if the lease provides for it and allows subletting or assignment.
- 1951.5 and 1671(d): lease-break fees are judged as liquidated damages.
- Breakwater re-let after 47 days: the rent-loss calculation is Code.

**DP3.4 Statutory early termination**
- 1946.7 (T):
  - written notice with an order, police report or qualified third-party statement;
  - rent for no more than 14 days after the notice ((e));
  - no forfeiture of the deposit or advance rent, and not a breach ((f));
  - notice within 180 days of the order, report or act, or as 1946 allows ((d)).
  - Code: notice date + 14. Judgment: whether the documentation conforms.
- SCRA 50 U.S.C. 3955 [US] (see federal.md): the lease ends 30 days after the next rent due date following the notice; rent paid in advance is refunded within 30 days; there is no early-termination charge.
- MVC 409.3 (T) gives court relief on pre-service obligations only.
- No California age or disability early-termination right was identified (I).

**DP3.5 Holdover**
- 1945 (renewal if rent is accepted).
- 3334 (T): the value of use during wrongful occupation, measured as the greater of reasonable rental value or the benefit to the occupier ((b)(1)), plus restoration and recovery costs. 3334 does not apply where CCP 1174 governs.
- CCP 1174(b) (T): unlawful-detainer damages, plus up to $600 statutory damages for malice.
- 1671(d): any holdover premium (for example, 150% rent) faces the penalty test.
- 1935: pro rata.
- Code: days × daily rent. Judgment: reasonable rental value, and whether the premium is a penalty.
- The schedule's "holdover" rate should be the contract rent or proven rental value, not a premium (I).

**DP3.6 Government order or untenantability**
1942.4, 1941.9 and HSC 17975 et seq. (owner-caused displacement relocation). Thin.

**DP3.7 Surrender without eviction**
- 1933(2) mutual consent (T); 1951.3; 1954(a)(3) entry after abandonment or surrender (T).
- Self-help is barred while the tenant is in possession: no utility interruption or lockout intended to end the occupancy (789.3 (T)).
- "Vacated" (the DP6.2 trigger) is a Judgment over keys, belongings, a written surrender and access.

**DP3.8 After an eviction case**
- CCP 1174 (T): the judgment covers possession, rent due and damages to the date of judgment.
- 1950.5 still applies after the tenant vacates (I). (f)(7) and (h)(1)(A)(ii)(II) drop the inspection and electronic-refund notice duties where termination was under CCP 1161(2)–(4) (T).

---

## DP4 The pre-vacate inspection

- **Notice.** 1950.5(f)(1) (T): "within a reasonable time after notification of either party's intention to terminate the tenancy, or before the end of the lease term", the landlord gives written notice of the right to request an initial inspection and to be present.
- **The inspection.** On request, the landlord inspects no earlier than two weeks before termination. It needs 48 hours' written notice, unless a written waiver is signed by both. It proceeds even if the tenant is absent. The notice must include the abandoned-property statement quoted in (f)(1).
- **Statement and cure.** (f)(2): an itemized statement of proposed deductions, with the text of (b)(1)–(4), handed over or left inside. (f)(3): the tenant may cure until termination.
- **Entry.** 1954(a)(2) (T) authorizes entry for an (f) inspection.
- **Consequences.**
  - (f)(4): if the inspection is held and the unit is not obstructed by possessions, there is no deduction for repairs or cleaning not listed. Exceptions: uncured listed items (f)(5); damage arising after the inspection, or hidden by possessions (f)(6).
  - Tenant declines: the landlord's (f) duties are discharged.
  - Landlord never sent the (f)(1) notice: no express consequence. It is a violation of the section that could feed (m) bad faith. Whether it bars deductions an inspection would have caught is contested (C9).
- **Code:** notice dates, the two-week window and the 48-hour notice. **Judgment:** reasonable time; obstruction; whether damage arose after the inspection.
- **Owen's design fits.** The pre-move-out list handed over at the inspection is the (f)(2) statement. Each later deduction must trace to a listed item or an (f)(6) exception (I).

---

## DP5 Building the account: what may be kept and charged

**DP5.1 What the deposit may be kept for**
- (b) purposes (T):
  - (1) rent default;
  - (2) repair of damage, exclusive of ordinary wear and tear, caused by the tenant or a guest or licensee;
  - (3) cleaning back to the cleanliness at the inception of the tenancy;
  - (4) restoring, replacing or returning personal property or appurtenances, if the rental agreement authorizes it.
- The list follows "used or to be used for any purpose, including, but not limited to". (e)(1) limits claims to "amounts as are reasonably necessary for the purposes specified in subdivision (b)".
- Whether other lease debts, such as utilities, can come out of the deposit is contested (C6). Brooks v. Greystar, ECF 56 (S.D. Cal. Aug. 7, 2025), pp. 13–14 (read from `research/california-case/sources/brooks-greystar-2025-08-07.pdf`): "the plain text of subsections (b) and (e) of Section 1950.5 expressly allow security deposits to be used 'for any purpose' … Therefore, utility charges may be claimed from security deposits." A nonbinding district-court order at the pleading stage.

**DP5.2 Fees and charges**
See DP1.4.
- Collection costs and attorney fees: only on an original lease clause, and only actual. 1717 makes fee clauses reciprocal (T). See OPERATING_BRANCHES C12.
- The flat "cleaning fee" theory survived a motion to dismiss in Brooks ECF 48 (nonbinding). Owen has excluded flat fees.
- A returned-payment fee rests on 1719(a)(1) (T): up to $25 for the first check returned for insufficient funds and $35 for each later one. A treble-damages demand procedure is in (a)(2).

**DP5.3 Wear and tear, painting, cleaning and turnover**
- (e)(2)(A)–(C), (b)(3) (T).
- AB 2801 §1 (uncodified; text saved at `j1/lanes/enactments/sources/202320240AB2801.txt`): the intent is "to ensure that landlords do not subsidize improvements to their rental properties with a former tenant's security deposit." Owner upgrades are excluded.
- (G) DRE guide pp. 83–85:
  - a useful-life proration method (the tenant pays only the remaining life of a damaged item);
  - a two-year paint-life table: under 6 months, full cost; 6–12 months, two-thirds; 1–2 years, one-third; 2+ years, none.
  - The guide says these "are not necessarily the law". The paint table is sourced to a Nolo treatise.
- Code: proration from the company schedule's useful lives. Judgment: classification (see Standards below).

**DP5.4 Move-out service fees agreed in the lease**
(n), (e)(2)(C) and 1953(a)(1) (T). Fixed move-out or cleaning fees are not recoverable as such; only cleaning reasonably necessary under (b)(3) (I). Excluded by Owen's posture.

**DP5.5 Unpaid rent, accelerated rent and lease-break sums**
- (b)(1); 1951.2; 1951.4; 1671(d); 1946.7(e); SCRA 3955; 1941.9; 1942.4; 1946.2(d) waiver; 1947.12 overcharge offset.
- Proration: 1935 states the principle. No statute fixes the daily rate (actual days in the month versus 30). That is a company-schedule choice (I).

**DP5.6 Interest and administrative fee on the deposit**
None in state or HB law identified (I). Code: 0.

**DP5.7 Assisted (voucher) tenants**
- [US] The tenant owes only the tenant share (24 CFR 982.451(b)(4)).
- Housing assistance payments for the move-out month: the owner may keep the HAP for the month the family moves out (982.311(d)).
- The deposit may be applied to amounts owed under the lease, with a list given to the tenant; 982.313 "promptly" is satisfied by the 21-day deadline (US atoms).
- There is no PHA or HUD reimbursement route for unpaid amounts in the HCV program; the owner collects from the tenant (US atom 24CFR982.313(e)). The OCHA administrative plan was not read (GAPS).
- [CA] Gov 12955 (T) covers source of income, including vouchers, for equal treatment.

**DP5.8 Deposits that are not cash**
No California statute on deposit-alternative or surety products was located. Guarantor law is suretyship (GAPS). Thin.

**DP5.9 Disability**
- [CA] 54.1(b)(6) (T): the landlord may not refuse a guide, signal or service dog. (B) keeps the tenant liable for property damage the dog causes "when proof of the damage exists". The no-pet-fee or deposit rule comes from the FEHA regulations (GAPS) and federal law.
- FEHA regulations 2 CCR 12185 et seq. (GAPS).
- [US] 42 U.S.C. 3604(f)(3)(B) and 24 CFR 100.204 (atoms).
- Code: no pet fees or deposits for an assistance animal. Actual damage is chargeable like any other.

**DP5.10 Equal treatment**
- Gov 12955 (T); FHA [US]; Unruh 51 (not retrieved).
- The company-wide schedule applied uniformly is the control (I).

---

## DP6 The statement and the refund

**DP6.1 The deadline**
- 1950.5(h)(1) (T): no later than 21 calendar days after the tenant vacates. Not earlier than a notice to terminate under 1946 or 1946.1 or CCP 1161, nor earlier than 60 days before a fixed term expires.
- Final documents: (h)(3), within 14 days of completing the repair or receiving the documentation.
- Documents on request: (h)(5), within 14 days of receiving a request made within 14 days of the statement.
- Code: all of these dates.

**DP6.2 When the tenant vacated**
A Judgment over the evidence: keys, belongings, written surrender, notice end date and the end of access. It is the start of every clock. Abandonment under 1951.3 has its own Code date.

**DP6.3 Counting days**
- Civ 10 (T): exclude the first day and include the last, unless the last day is a holiday.
- Civ 7 (T): holidays are Sundays plus the days the Government Code makes holidays. GOV 6700 (T; amended by AB 2156, Stats. 2026 ch. 7, effective Mar 26, 2026) lists them. They include Lunar New Year, Mar 31 (Farmworkers Day), Apr 24, Diwali, Juneteenth, Admission Day (Sep 9), Native American Day and Columbus Day. Good Friday counts only from noon to 3 p.m., and days appointed by the President or Governor are included. GOV 6701 (T): a holiday on Sunday moves to Monday; Nov 11 on a Saturday moves to Friday. No other Saturday observance.
- Civ 11 (T): an act due on a holiday may be done on the next business day.
- CCP 12a (T): extends any period set by law when its last day is a Saturday or a CCP 135 judicial holiday. 12a(b) applies it to all codes.
- Whether "21 calendar days" displaces the extension is contested (C5).
- Code computes:
  - the nominal day 21;
  - the extended date under Civ 10/11 (Gov Code holidays);
  - the extended date under CCP 12a (Saturdays and judicial holidays).
- The two holiday calendars differ. CCP 135 (T; AB 268, effective Jan 1, 2026) makes every Gov 6700 holiday a judicial holiday except Lunar New Year, Diwali, Apr 24 (Genocide Remembrance Day), Admission Day, Columbus Day and days appointed by the Governor. It adds every Saturday and the day after Thanksgiving. So Gov Code holidays that fall outside CCP 135 extend under Civ 10/11 only, and Saturdays extend under CCP 12a only.
- AB 2156 is already in force. AB 2017, AB 2294 and SB 1394 change GOV 6700 from (presumably) Jan 1, 2027: two Eid days, Apr 14 Sylvia Mendez Day, and Mar 31 naming. None of the new days is a CCP 135 judicial holiday (see the effective-date table).
- Recommended operating date: the nominal day 21.

**DP6.4 Contents and form**
- The statement gives the basis and amount of the security received, its disposition, and the remainder returned ((h)(1)).
- Documents (h)(2):
  - (A) in-house work: a description, time spent and a reasonable hourly rate;
  - (B) vendor work: the bill, invoice or receipt, plus the vendor's name, address and telephone if not on it;
  - (C) materials: the bill, invoice or receipt; for items bought regularly, a price list or vendor document will do;
  - (D) for repair or cleaning deductions, the (g) photographs and a written cost explanation, delivered by mail, email, flash drive or link.
- Estimates (h)(3): a good-faith estimate may be deducted if a repair cannot reasonably be completed within 21 days, or the vendor documents are not in hand. If documents are missing, name the vendor with its address and telephone. Complete the statement within 14 days.
- Exemption (h)(4): (h)(2) and (h)(3) do not apply when repair and cleaning deductions total no more than $125, or when the tenant has validly waived them (signed at or after the termination notice, or within 60 days of the term's end, and substantially including the text of (h)(2)).
- (h)(5) overrides (h)(4) when the tenant asks within 14 days.

**DP6.5 Delivery**
- Refund (h)(1)(A):
  - (ii) If the security or rent was received electronically, refund electronically to a bank account the tenant designates in writing, or by an agreed electronic method, or by another method agreed in writing.
  - (ii)(II) Give written notice of that right within a reasonable time after notice of termination. This is not required after CCP 1161(2)–(4) terminations, or where a written agreement already designates a method.
  - (i) Otherwise, by personal delivery or a check mailed first-class.
- Statement (h)(1)(B): personal delivery or first-class mail; or, by mutual agreement, email, or mail to an address the tenant provides.
- Address (h)(6): the address the tenant provides, otherwise the vacated unit.
- Code: route selection. Judgment: none, except whether a written designation or agreement exists.
- With no forwarding address, mail to the vacated unit. That satisfies (h)(6) (T).
- Whether timely mailing on day 21 is enough, or receipt is needed, is (I): "furnish … by … first-class mail" reads as complete on mailing. Not tested here.

**DP6.6 Co-tenants**
- (h)(1)(C)(i): absent a written agreement with all adult tenants, the refund is one check payable to all adult tenants on the lease at termination. The statement goes to any one of them, chosen by the landlord.
- (ii): an agreement with all adult tenants can set allocation percentages, electronic deposits and statement channels per tenant.
- (iii): a tenant who ended the lease under 1946.7 may ask for another method.
- How (C)(i)'s check rule interacts with the electronic duty in (A)(ii) is contested (C8).

**DP6.7 Tenant in bankruptcy**
[US] (federal.md): applying the deposit after the petition is a setoff and needs stay relief (11 U.S.C. 362(a)(7), 553; *Strumpf*). The refund is estate property (541, 542). A temporary hold pending a prompt motion is allowed.

**DP6.8 Unclaimed refund**
- CCP 1520 (T): intangible property escheats after three years unclaimed.
- Reporting: CCP 1530(d) (T): a report before Nov 1 each year as of Jun 30. Remitting: CCP 1532(a) (T), seven months to seven months and 15 days after the report deadline. CCP 1513.5 (T) covers banking organizations only; a holder-notice rule for other business holders was not identified (GAPS).
- Code: check date + 3 years, and the report and remit windows. See DP9.2.

**DP6.9 Belongings left behind**
- Two routes:
  - Chapter 5 (1980–1991): notice under 1983 (15 days personal, 18 days mailed); storage costs; release.
  - 1965: the tenant's written request within 18 days, and the landlord's itemized cost demand within 5 days.
- No storage charge if reclaimed within two days of vacating, from the dwelling (1987(c)) or from the premises (1990(c)).
- Post-writ property: CCP 1174(h).
- Full analysis: `pipeline/design/coverage_tracking/fresh_research/FINDINGS.md`. The 1950.5(f)(1) notice carries the reclaim statement.

**DP6.10 Tenant data at move-out**
1798.81 (disposal) and 1798.82 (breach) (T). They do not change the account. Retention is driven by limitation periods (DP7.6 and DP9.3).

---

## DP7 Consequences of getting it wrong

**DP7.1 Forfeiture**
1950.5(h)(7) (T), added by AB 2801: "The landlord shall not be entitled to claim any amount of the security if the landlord, in bad faith, fails to comply with this subdivision." The bad faith of the failure to comply is a Judgment. Scope is contested (C1).

**DP7.2 Does the underlying debt survive?**
- *Granberry v. Islay Investments* (1995) 9 Cal.4th 738, 749–750 (M), decided before AB 2801. A landlord who fails in good faith to follow the deduct-and-retain procedure may still recover rent, repair and cleaning damages, by setoff or claim, if it proves the damages and that the amount is reasonable. Equitable defenses (laches, unclean hands, estoppel) remain. The court expressly declined to decide the rights of landlords who acted in bad faith (fn. 6).
- 1950.5(k)(2) preserves a successor's claim for damages beyond the security (T).
- (G) DRE guide p. 86 reads Granberry this way: the landlord "loses the right to keep any of the security deposit and must return the entire deposit", but may still claim damages by setoff or counterclaim.

**DP7.3 Commingling and holding**
No owner-level rule (I). Brokers: BPC 10145 and 10176 (T). No effect on the tenant's account.

**DP7.4 Burden of proof**
- (m) (T): the landlord has the burden of proof on the reasonableness of amounts claimed.
- (p): the deposit may be proved by any credible evidence.
- *Granberry*: preponderance of the evidence.

**DP7.5 Damages and penalties**
- (m) (T): for bad-faith claim or retention, statutory damages up to twice the security, plus actual damages. The court may award them on its own motion.
- Prejudgment interest: 3287(a) (T; from the day a right to damages certain vests) and 3289 (T; 10% after breach where the contract sets no rate).
- Attorney fees only under a lease clause, made reciprocal by 1717 (T).
- UCL and class exposure for systemic practices (Brooks; RECORD.md).
- Code, for each line: the exposure to show the operator = the disputed amount + up to 2× security + interest + (if a fee clause exists) fees.

**DP7.6 The tenant's claim: who, where, by when**
- Small claims (1950.5(o); CCP 116.220 and 116.221) (T): limits are $6,250 generally and $12,500 for a natural-person plaintiff. A tenant suing for a deposit is within the $12,500 limit.
- CCP 116.231(a) (T): no person may file more than two small-claims actions demanding more than $2,500 anywhere in the state in a calendar year. A declaration is required ((b)). The public-entity exception in (d) does not apply to a private owner. This binds the operator as plaintiff (DP8.9).
- CCP 116.540(h) (T): the owner may appear through a property agent under contract to manage the property, if the agent was retained principally to manage and the claim relates to the property. A declaration is required ((j)).
- CCP 116.710 (T): the plaintiff cannot appeal its own claim; the defendant can appeal to the superior court. In practice, the operator as defendant can appeal a tenant's deposit judgment, but not its own claim as plaintiff.
- Venue: CCP 116.370 (T).
- Limitations:
  - CCP 337 (T): 4 years on a written lease;
  - CCP 339: 2 years on an oral one (DRE guide p. 86);
  - the period for the (m) statutory damages is contested: 338(a) 3 years (T: a liability created by statute other than a penalty), or 340(a) 1 year (T: an action on a statute for a penalty given to an individual) (C10).

---

## DP8 Collecting a balance beyond the deposit

The collection research is substantial and already integrated in `pipeline/design/collection_dependencies/OPERATING_BRANCHES.md` (C01–C20, A01–A35). This map points to it rather than restating it.

**DP8.1 What the balance is**
- Components: rent; utilities; damage and cleaning; lawful lease fees; interest; less credits.
- Interest: 3289(b) 10% after breach where the contract is silent (T); 3287(a) prejudgment interest on certain sums (T).
- Collection fees only under the C12 limits.
- Code: the amount by component.

**DP8.2 Who is a debt collector**
- Rosenthal 1788.2 (T; AB 1521, effective Jan 1, 2026) requires a consumer-credit transaction. Coverage of tenancy balances is contested by component (C3).
- FDCPA [US] reaches a third-party collector of lease debts. The (F)(i) and (F)(iii) exclusions apply to the manager (federal.md).

**DP8.3 What a collector must and must not do**
OPERATING_BRANCHES C06–C11, C13–C15 and C19–C20, including 1788.17, 1788.14.5, 1788.52 and 1812.700 (T).

**DP8.4 Local collection rules**
None identified in OC or HB (I; search not exhaustive).

**DP8.5 Licences**
- FIN 100001 (T) DCLA licence, which excludes Real Estate Law licensees.
- BPC 10131(b) (T): managing rentals and collecting rent for others for compensation needs a broker licence. 10133 sets out the exemptions.
- A collector needs its own DCLA licence (C18).

**DP8.6 Credit reporting**
- 1785.25(a) accuracy (T).
- 1785.26(b)–(c) (T): a "creditor" must notify the consumer in writing before, or within 30 days after, reporting negative information. (a)(1) includes the creditor's agent or collector. But (a)(2) excludes information "arising from a nonconsumer transaction or any other credit transaction outside the scope of this title". So whether a rent balance is "credit" here is open (C12; compare C3). Safe practice: send the notice (I).
- FCRA 1681s-2 [US].

**DP8.7 Bankruptcy**
[US] stay, discharge and proofs of claim (federal.md).

**DP8.8 Servicemembers**
[US] SCRA 3931 default-judgment affidavit; 3955 termination; 3937 the 6% cap on pre-service debt. [CA] MVC 409.3 (T).

**DP8.9 Before suing**
- Limitations: CCP 337(a) 4 years (written), 339 2 years (oral) (T). CCP 360 (T): only a written acknowledgment or promise signed by the debtor takes a debt outside the limitation period. Its part-payment clause speaks of promissory notes. So a payment plan should carry the former tenant's signed acknowledgment.
- After a death: CCP 366.2 (T), one year from death, which displaces the ordinary period.
- Capacity:
  - a foreign LLC transacting intrastate business without registration may not maintain an action, but may defend (CORP 17708.07(a)–(b) (T));
  - CORP 2203 is the parallel rule for foreign corporations (T);
  - RTC 23301 (T): a taxpayer suspended by the Franchise Tax Board loses its powers, rights and privileges.
  - Code: check entity status before any filing.
- Small claims for the owner: an entity plaintiff is limited to $6,250 (116.220(a)(1)) and to two filings above $2,500 per calendar year statewide (116.231(a)). Each owner entity counts separately, so a single-asset owner entity gets two (I). The property agent may appear under 116.540(h). Code: the remaining filing count per owner entity per year. Balances above $6,250, or beyond the two filings, go to limited civil court with counsel, which changes net recovery.
- Payment plans: no statute prescribes their terms. A plan that adds interest or finance charges may itself be a credit transaction that brings in Rosenthal (C3; OPERATING_BRANCHES A23).

**DP8.10 Tax**
[US] only (federal.md).

**DP8.11 After judgment**
- CCP 685.010 (T): 10% interest. For judgments entered from Jan 1, 2023, the rate is 5% on judgments under $50,000 against a natural person for "personal debt". Personal debt is debt from a transaction in money, property or services primarily for personal or household purposes; debts from tortious conduct are excluded.
- Whether a lease balance is "personal debt" is (I): likely yes for contract components, unclear for tort-style damage claims (C11).
- Code: the rate by judgment date, amount and debtor type.
- Enforcement, exemptions and satisfaction: not retrieved (GAPS).

---

## DP9 Closing the account

**DP9.1 Writing off a balance**
No California rule. [US] tax atoms (federal.md). Owen's net-recovery rule governs the decision.

**DP9.2 Unclaimed funds**
CCP 1520 (T): three years. CCP 1530(d) (T): report before Nov 1 as of Jun 30. CCP 1532(a) (T): remit 7 months to 7 months and 15 days after the report deadline. Code: the dates.

**DP9.3 Records**
- 1798.81 (T): disposal of records containing personal information.
- BPC 10148(a) (T): a broker keeps trust records and transaction documents for 3 years.
- Practical retention runs at least to the limitation periods: 4 years from vacating (CCP 337), plus the small-claims appeal period (I).

---

## PW0 Lawful entry and control of the premises

**PW0.1 Entry**
- 1954 (T): entry for necessary or agreed repairs, an (f) inspection, showing the unit, on abandonment or surrender, by court order, or for water-submeter work under Chapter 2.5.
- Reasonable written notice is required; 24 hours is presumed reasonable. Entry is in business hours, except emergency or surrender.
- An (f) inspection needs 48 hours' written notice (T).
- 1954.211 (T): entry to read a submeter needs written notice only.
- Code: notice timing.

**PW0.2 Possession recovered**
- Surrender or abandonment (1951.3) or a writ (CCP 1174).
- Self-help lockout or utility shutoff is barred (789.3 (T)). Water shutoff is barred (1954.213(e)) (T).
- Keys and access credentials: no specific statute; evidence of surrender (I).

**PW0.3 Conditions requiring immediate action**
Physical-work track. Account effect only through 1942.4 and 1941.9.

**PW0.4 Authority to act**
- The manager as the owner's agent: 1962(d) (T); BPC 10131(b) (T); 2343(3) (T) on an agent's own liability to third persons where its acts are "wrongful in their nature".
- Death: PROB (DP2.5).
- Public ownership and program limits: a later variation.

## PW3 Completion and the connection to the account

- **PW3.1 Completion evidence.** For the account, completion evidence is the (g)(2) post-repair photographs and the date the (h)(3) 14-day clock starts. Permits are physical-work matters.
- **PW3.2 Defective or incomplete vendor work.** Only the "reasonable amount necessary to restore" is chargeable ((e)(2)(B)). Rework or a vendor's own defect is not the tenant's cost (I).
- **PW3.3 Records.**
  - (g)(1) and (g)(2) photographs: before possession (for tenancies from Jul 1, 2025), after possession returns but before work, and after work.
  - (h)(2) documents; in-house work orders must show hours and rate.
  - (h)(3) vendor name, address and phone when the invoice is missing.
  - 1954.207(c): the final water bill attached.
- **PW3.4 Work cost versus tenant liability.**
  - Charge = the reasonable cost to restore to inception condition, less ordinary wear ((e)(2)(B)).
  - No upgrades (AB 2801 §1).
  - (c)(3) separately allows agreed paid alterations, not chargeable to the previous tenant.
  - The tenant pays the tenant's share; provider cost does not establish tenant liability (I).

---

## Standards: the factors California authority uses

| Standard (text) | Factors with authority | Where authority is silent |
|---|---|---|
| Ordinary wear and tear ((b)(2), (e)(2)(A)) | **Statute (T):** excluded whether preexisting or arising during the tenancy, including "the effects thereof" and cumulative wear over tenancies. Damage must be "caused by the tenant or by a guest or licensee." **DRE guide (G), pp. 81–85:** wear is deterioration from normal use or aging. Examples of wear: simple wearing of carpet or drapes, moderate dirt or spotting, minor nicks, a sofa mark. Examples of damage: large rips, indelible stains, many holes needing plaster, large gouges, pet chewing. Age matters: a 10-year-old worn carpet is wear. | No statutory definition. No California appellate decision defining it was located (search limited). Factors used: cause, severity, the item's age and useful life, length of tenancy, move-in record. |
| Reasonably necessary; reasonable amount to restore ((e)(1), (e)(2)(B), (e)(2)(C)) | **Statute (T):** the amount needed to restore inception condition, exclusive of wear. In-house work is priced at a reasonable hourly rate ((h)(2)(A)). Professional cleaning is allowed only if reasonably necessary ((e)(2)(C)). AB 2801 §1: no subsidizing improvements. **Granberry (M):** the landlord proves damages and reasonableness by a preponderance. **DRE (G):** useful-life proration; the paint table. | No case states pricing factors (market rate, repair versus replace, like-kind replacement). These are (I). |
| Cleanliness "at the inception of the tenancy" ((b)(3)) | **Statute (T):** the same level as at inception (tenancies after 2003). **DRE (G) p. 83:** compare with move-in; no routine charges. Chargeable examples: fleas, oven, decals, mildew, refrigerator, floors. Built-up wax from years of use is cumulative wear. **Evidence:** (g)(1) photographs (tenancies from Jul 1, 2025). | No case factors. |
| Bad faith ((h)(7), (m)) | **Granberry (M)** declined to define it, and reserved the position of bad-faith landlords (fn. 6). Its fn. 4 notes that the Court of Appeal upheld a jury instruction defining "bad faith". That opinion was superseded on review (I) and is not citable. **DRE (G):** no factors. | **No controlling definition was located** (J5 search needed). Candidate factors (I, not authority): knowledge of the duty; a pattern or practice; no reasonable basis for the charge; ignoring requests; charges that are fabricated or unsupported by evidence. |
| Reasonable time ((f)(1), (g)(2), (i), (h)(1)(A)(ii)(II)) | **Statute only (T).** (g)(2) photographs must be taken before the work is done. | **No authority supplies factors.** Code can set conservative internal targets: the (f)(1) notice on receiving notice of termination; (g)(2) photographs before any work order starts. |
| Good-faith estimate ((h)(3)); reasonable hourly rate ((h)(2)(A)) | Statute only (T). | No factors. Use a written quote or the schedule rate as the basis (I). |

---

## Condition structures: the core deduction provisions

Notation: ALL / ANY / NOT, UNLESS, ONLY IF. Each item ends with the evidence or record that settles it. **[D]** = determinate (code). **[S]** = semantic (a Jev question over evidence).

### 1950.5(b) and (e): may line L, of amount A, be charged against the security?

ALL of the following:

1. **The money is security.** It was charged at the beginning of the tenancy or is advance rent, and it is not a 1950.6 screening fee [D]. *Evidence:* the lease and the move-in ledger.
2. **Purpose.** ANY of:
   - (b)(1) rent default [D]. *Evidence:* the ledger, and the rent-period computation.
   - (b)(2) repair of damage, caused by the tenant, a guest or a licensee [S], AND NOT ordinary wear [S]. *Evidence:* move-in and move-out photographs, inspection notes, a cause narrative.
   - (b)(3) cleaning, ONLY IF the tenancy began after Jan 1, 2003 [D], AND the unit is less clean than at inception [S]. *Evidence:* (g) photographs.
   - (b)(4) restoring or replacing personal property or appurtenances, ONLY IF the lease authorizes applying the deposit [D], AND NOT ordinary wear [S]. *Evidence:* the lease clause and the inventory.
   - Another lease obligation, such as utilities, under "any purpose" — contested (C6).
3. **Not excluded by (e)(2)(A).** NOT preexisting [S]; NOT ordinary wear or its effects [S]; NOT cumulative wear across tenancies [S]. *Evidence:* move-in record, unit history, the item's age.
4. **Amount (e)(1), (e)(2)(B).** A ≤ the reasonable cost to restore inception condition, exclusive of wear [S + D]. *Evidence:* invoice or hours × rate; the useful-life proration [D] from the schedule; no upgrade component [S].
5. **Professional cleaning (e)(2)(C).** ONLY IF reasonably necessary [S]. A lease clause requiring it is not a basis.
6. **The (f)(4) gate.** IF an initial inspection was held [D] AND the unit was not obstructed by possessions [S], THEN L must satisfy ANY of:
   - listed in the (f)(2) statement and not cured [D/S];
   - arose between the inspection and the return of possession [S];
   - not identifiable because of the tenant's possessions [S].

   *Evidence:* the inspection statement, its photographs, and the obstruction notes.
7. **Photographs (g) and (h)(2)(D)** — required for repair or cleaning lines:
   - the (g)(2) before-work set exists, ONLY IF possession returned on or after Apr 1, 2025 [D];
   - a post-work set exists [D];
   - a move-in set exists, ONLY IF the tenancy began on or after Jul 1, 2025 [D].
8. **Documents (h)(2)(A)–(C)** — UNLESS (h)(4) applies [D]: repair and cleaning total ≤ $125, OR a valid waiver (the timing [D] and whether it substantially includes the text of (h)(2) [S]). A tenant request under (h)(5) revives the duty [D].

### 1950.5(g) photograph duties
- **G1:** IF the tenancy begins on or after Jul 1, 2025 → photographs "immediately before, or at the inception of" the tenancy [D: timestamp ≤ the move-in date].
- **G2:** IF possession is returned on or after Apr 1, 2025 AND the landlord will deduct for repairs or cleaning → photographs within a reasonable time after possession returns AND before those repairs or cleanings [D: timestamp before the work order starts; S: reasonable time], AND within a reasonable time after completion [D/S].
- The consequence runs through (h)(2)(D), and through (h)(7) if the failure is in bad faith.

### 1950.5(h): statement and refund
- **H1 trigger.** The tenant has vacated [S over keys, possessions, surrender]. The statement is not earlier than a 1946, 1946.1 or CCP 1161 notice, or 60 days before a fixed term ends [D].
- **H2 deadline.** The vacate date + 21 calendar days [D]. The holiday-extension variant is contested (C5).
- **H3 contents.** Security received; the basis and amount of each deduction; the disposition; the remainder [D].
- **H4 refund route.**
  - IF the security or any rent was received electronically [D] → electronic transfer to an account designated in writing, OR another method agreed in writing [D].
  - ELSE personal delivery or a first-class check [D].
  - IF multiple adult tenants reside [D], AND there is NO written agreement with all of them [D], AND NOT a (C)(iii) request → one check payable to all adult tenants on the lease at termination. The interaction with the electronic duty is contested (C8).
- **H5 statement route.** Personal delivery or first-class mail; OR email or a provided address, ONLY IF mutually agreed [D].
- **H6 address.** The tenant-provided address, ELSE the vacated unit [D].
- **H7 documents.** As in item 8 above.
- **H8 estimate.** ANY of: an in-house repair cannot reasonably be completed by day 21 [S]; vendor documents are not in hand by day 21 [D]. → Deduct a good-faith estimate [S] and include the vendor's name, address and phone if documents are missing [D]. Within 14 days of completion or receipt, complete the statement and documents [D].
- **Effects.**
  - Compliance → the landlord keeps the itemized amounts.
  - Noncompliance AND bad faith [S] → no amount of the security may be claimed ((h)(7)), and exposure under (m).
  - Noncompliance in good faith → *Granberry* setoff or claim, which survives AB 2801 only if (h)(7) leaves it alone (C1).

---

## The late final utility bill (coordinator question)

**Question.** The final utility bill arrives after day 21. What may the landlord do?

**What the text says**
- **Submetered water** (Chapter 2.5 applies, 1954.216) (T):
  - 1954.207(b): at the end of a tenancy the submeter is read within five days if possible. If it cannot be read, the final month's bill is based on the previous month's bill.
  - 1954.207(c): the landlord "may, at his or her discretion, deduct an unpaid water service bill from the security deposit during or upon termination of a tenancy, if the last water service bill showing the amount due is attached to the documentation required by Section 1950.5."
  - The "water service bill" is the landlord's or billing agent's bill to the tenant under 1954.205 and 1954.206. It is not the purveyor's master bill (I from 1954.202 and 1954.206).
  - 1954.205(a)(1)(A) prices the tenant's usage as a share of the purveyor's bill for the period. The (B) and (C) methods use the purveyor's rate schedule instead.
  - 1954.212: if a reading is unavailable and the tenant gave access, the charge is 75% of the average of the last three months. Water charges are not rent (1954.213(d)).
- **1950.5(h)(3)** (T): a good-faith estimate is allowed "if the documents from a person or entity providing services, materials, or supplies are not in the landlord's possession within 21 calendar days". The sentence sits inside a subdivision whose paragraph (2) concerns documents "to repair or clean".
- **Ratio billing (RUBS), gas and electric:** no billing statute was read for RUBS. Chapter 2.5 expressly takes no position on it (1954.216(c)). The charge is contractual under the lease. 1940.9 (T) governs shared gas and electric meters. PUC 739.5(a) (T) limits submetered gas or electric charges to the utility's direct rate. The timing of the final gas or electric bill follows the master-meter billing cycle, which no statute addresses (I).

**What the landlord may do**

1. **Submetered water, final reading taken.** If the billing agent can price the final period by day 21 using a 1954.205 method, deduct it and attach the final water bill (1954.207(c)). If the reading cannot be taken, 1954.207(b) supplies a statutory final-month amount: the previous month's bill. That is the cleanest lawful way to finish on time (T plus I).
2. **Estimate under (h)(3).**
   - The text supports an estimate where the utility biller's document is late. The provider of "services" is the biller.
   - Counter-reading: (h)(3) belongs to the repair and cleaning documentation scheme. For submetered water, 1954.207(c) conditions any deposit deduction on attaching the actual final bill.
   - Treat this as **contested (C7)**. If used, label the line an estimate, name the biller with its address and phone, and send the final bill and any refund difference within 14 days of receiving it.
3. **Withhold an unitemized amount "pending" the bill.** Not supported. (h)(1) requires returning "any remaining portion" within 21 days. (h)(3) is the only mechanism for deducting a cost not yet documented, and it requires an itemized estimate (T plus I).
4. **Bill it separately later.** Nothing in 1950.5 bars a separate later claim for a lawful lease charge. The deposit-statement rules govern only the security. Granberry preserves claims after good-faith noncompliance (I).
   - Consequences: the refund goes out without the deduction, and the utility becomes a balance owed (DP8).
   - That utility component is the one most likely to be Rosenthal "consumer credit" (postpaid service; OPERATING_BRANCHES C01/A16), so collection-law duties attach.
   - Net recovery is usually small. Owen's net-recovery rule decides.
5. **If the final bill exceeds the estimate.** (h)(3) speaks only of completing the statement. Whether the difference can be added to the deposit retention or must be billed as a balance is unresolved (C7).

**Recommended engine posture (for the coordinator to decide).**
- Submetered water: if the read is done but the bill is not priced by about day 18, use 1954.207(b) or the estimate route and record the risk.
- RUBS and other utilities: (h)(3) estimate, or bill separately.
- Show the operator the exposure of the estimate route (C7).
- Never hold an unitemized reserve.

---

## Effective-date variants that matter for a 2026 move-out

| Variant | Date | Source |
|---|---|---|
| Deposit cap of one month | Security demanded or received on or after Jul 1, 2024 | 1950.5(c)(1), (c)(6) (T) |
| Move-out photographs (before and after work) | Possession returned on or after Apr 1, 2025 | (g)(2) (T) |
| Move-in photographs | Tenancy began on or after Jul 1, 2025 | (g)(1) (T) |
| Bad-faith forfeiture; photographs with the statement | AB 2801, Stats. 2024 ch. 280 (approved Sep 19, 2024; effective Jan 1, 2025, with the (g) dates above); carried forward by AB 414 | (h)(2)(D), (h)(7) (T) |
| Electronic refund duty; agreements among multiple tenants | Jan 1, 2026 (AB 414, ch. 340) | (h)(1)(A)(ii), (C) (T) |
| Internet bulk-billing opt-out | Tenancies commenced, renewed or month-to-month on or after Jan 1, 2026 | 1942.8 (T) |
| Advance-rent refund after casualty | Jan 1, 2026 (SB 610) | 1941.9 (T) |
| Just-cause amendments | Jan 1, 2026 (AB 1529) | 1946.2 (T) |
| Rosenthal definitions | Jan 1, 2026 (AB 1521) | 1788.2 (T) |
| No fee for serving notices; no fee for check payments | Jan 1 / Feb 1, 2025 (SB 611) | CCP 1161(6), 1947.3(b) (T) |
| Small-claims limits $6,250 / $12,500 | in force | CCP 116.220, 116.221 (T) |
| 5% judgment interest on personal debt | Judgments from Jan 1, 2023 | CCP 685.010(a)(2) (T) |
| Holiday calendar | GOV 6700 amended by AB 2156 (Stats. 2026 ch. 7), effective Mar 26, 2026 (T). AB 2017 (Stats. 2026 ch. 571) adds Eid al-Fitr and Eid al-Adha to GOV 6700. AB 2294 (ch. 596) adds Apr 14 (Sylvia Mendez Day). Both are excepted from the CCP 135 judicial holidays. SB 1394 (ch. 708) amends GOV 6700, 6701 and 6717 on Cesar Chavez Day / Farmworkers Day (Mar 31). All read. No urgency clause, so presumably effective Jan 1, 2027; the three are double-jointed. AB 1841 (state-employee holidays, Gov 19853) and AB 395 (schools, meetings) do not change counting. | The new 2027 dates (two Eid days, Apr 14) cannot fall on a 2026 move-out's day 21, which lands by Jan 21, 2027 at the latest. Code: version the holiday table by effective date. |
| 2026 acts touching tenancy | SB 1072 (housing omnibus), AB 2025 (Civ 1940.11: altered images in rental ads), SB 1296 (Civ 1942.7.5 pet policy, operative Apr 1, 2027) | Read (`sources/bills/`). None changes the departing account. AB 2025 concerns advertising, not the (g) photographs. |
| Rent cap and just cause sunset | Jan 1, 2030 | 1946.2, 1947.12 (T) |

For a move-out in late December 2026 whose day 21 falls in January 2027: the duties attach at vacating under the 2026 text (I). Only the holiday calendar for counting may change.

---

## Contested questions (not resolved)

- **C1. Scope of the (h)(7) forfeiture after AB 2801, against Granberry.**
  - Reading A: bad-faith noncompliance bars only keeping the security. Damages can still be pursued by separate claim.
  - Reading B: it bars any claim against the tenant for those items.
  - For good-faith noncompliance, the question is whether *Granberry*'s setoff survives. (h)(7)'s express bad-faith condition implies that good-faith noncompliance does not forfeit (I).
  - Consequence: a late or defective statement sent in good faith may still support the charges, with exposure. A bad-faith failure means refunding everything, and perhaps pursuing damages separately.
- **C2. Damages under (m) after AB 2801.**
  - Is a bad-faith (h) documentation failure (for example, missing photographs) a "retention … in violation of this section" that triggers up to 2×, even when the charge itself is valid?
  - Exposure: up to 2× the security per tenant, and class or UCL aggregation (Brooks).
- **C3. Rosenthal coverage of tenancy balances.**
  - Ordinary rent paid in advance is not "credit" — persuasive district courts (*Yatooma*, *Phillips*, *Leasure*).
  - Postpaid utilities and services likely are credit (*Davidson*, *Paredes*).
  - Damage claims depend on the underlying promise.
  - Payment plans may create new credit.
  - No controlling tenancy holding exists (collection_dependencies/tenancy/FINDINGS.md).
  - Consequence: which notices and holds apply when Handoff or the manager pursues each component.
- **C4. The manager as agent.**
  - Is the third-party manager a "landlord" liable under 1950.5(h) and (m)? 1950.5 does not define "landlord"; it refers to "the landlord's agent" in (i).
  - Agent liability under 2343(3) for wrongful acts.
  - Restitution liability under the UCL (*Leaser v. Prime Ascot*, cited in ECF 56; N).
  - FDCPA: the (F)(i) incidental and (F)(iii) pre-default exclusions.
  - DCLA: excluded as a Real Estate Law licensee (FIN 100001).
  - Small claims: the manager may appear for the owner (116.540(h)).
  - Consequence: who signs, who is exposed, and how disputes are staffed.
- **C5. Day 21 on a weekend or holiday.**
  - CCP 12a(b) and Civ 10/11 extend; "21 calendar days" may be read to exclude the extension.
  - The two holiday calendars differ (Gov 6700 versus CCP 135).
  - Consequence: one to three days of margin. Recommend acting by the nominal day 21.
- **C6. Applying the deposit to utilities and other non-(b) lease debts.**
  - "Any purpose, including, but not limited to" against (e)(1) "reasonably necessary for the purposes specified in subdivision (b)".
  - Brooks ECF 56 at 13–14 (S.D. Cal., nonbinding; read) struck the utility-deduction class: (b)'s "any purpose, including, but not limited to" allows utility charges. The contrary reading, that (e)(1) limits claims to (b)'s four enumerated purposes, was the plaintiffs' argument and has no appellate test. For submetered water, 1954.207(c) expressly permits it on conditions.
- **C7. Late final utility bills.**
  - Does (h)(3)'s estimate reach non-repair documents (utility bills)?
  - Can an estimate satisfy 1954.207(c)'s attached-bill condition?
  - Can a final bill above the estimate be retained from the deposit, or must the excess be billed?
- **C8. Several adult tenants who paid electronically.** (h)(1)(A)(i) is "subject to subparagraph (C)", but the electronic clause (ii) is not expressly subject to (C)(i)'s check payable to all. Consequence: the payment route and the risk of a double-payment claim. Avoid by getting the (C)(ii) agreement in writing on the tenant page.
- **C9. Skipping the (f)(1) notice.** It has no stated consequence. Is it a (m) "violation of this section", or an equitable bar to deductions an inspection would have caught?
- **C10. Limitation period for the tenant's statutory damages.** CCP 340(a), one year for a statutory penalty; 338(a), three years for a liability created by statute; or 337, four years, as a contract claim. Consequence: the dispute-exposure window and record retention.
- **C11. CCP 685.010(a)(2) 5% judgment interest on lease balances.** Is it "personal debt" from a household transaction? Are tort-style damage components excluded?
- **C12. Credit reporting by landlords.** Is a landlord a "creditor" for the 1785.26 negative-information notice?
- **C13. Partial vacatur.** When co-tenants leave on different dates, when does "the tenant has vacated" occur?

Authority on C1, C2, C4 and C10 needs a J5 search: subsequent treatment of *Granberry*, any post-AB 2801 appellate decision, and bad-faith definitions. This session located none, but the search was not a citator certification.
