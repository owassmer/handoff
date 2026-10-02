# Independent review 1: settling a market-rate tenancy in New York City

Reviewer: independent reviewer 1, 2026-09-28. Object: review/NYC_MARKET_RATE.md and the Stage A rules it cites (stage-a/NY.json, NYC.json, US.json). Evidence quotes are checked verbatim against the saved sources by review/ir1_verify.py. New sources carry the prefix REVIEW1_ in sources/.

## Summary

- Findings: 17. By severity: critical 4, major 2, minor 11.
- By kind: alignment 1, error 1, gap 7, misstatement-in-review 5, over-scope 1, stale-source 1, weak-support 1.
- Confirmed rulings and high-consequence rules: 30.
- Judgment: **accept after the listed corrections.**

The walk is faithful to its rules, and its core is right: the regime by lease date, the 14-day statement and its count, forfeiture of the security but not the debt, the willfulness standard, fees kept out of the deposit, painting as wear and tear, the FDCPA and DCWP coverage configurations and the SHIELD date all hold against the sources and the controlling courts. Every one of the 359 cited rules exists, and I read each rule's condition, effect and quote against the sentence citing it. Four corrections change money or liability and must be made before acceptance. The interest rate on a former tenant's balance is 2%, not 9% (CPLR 5004), and no rule says so. An automatic-renewal clause binds only with the GOL 5-905 notice, and no rule says so. The co-tenant payee rule misreads Holmes v Worthen and would let a landlord pay one co-tenant and still owe the other. After a tenant's bankruptcy the refund goes to the chapter 7 trustee, not the tenant. Two major gaps (HPD registration before suing for rent; Good Cause Eviction) and eleven minor items follow.

## Findings (most severe first)

### R1-01 (gap, critical)

- Rules: `NY:ADJ-lease-balance-not-consumer-credit`, `NY:CPLR-213(2)`, `NYC:CPL-tenant-balance-consumer-debt`, `NY:RPL-238-a(2)`
- Review step: 8.1; C7; C14
- What is wrong: No rule states the interest rate on a former tenant's balance. The review tells the operator the balance may be sued on for six years, but not that statutory interest on it is 2% a year, not 9%, when the tenant is a natural person. CPLR 5004(a), as amended by the Fair Consumer Judgment Interest Act (L.2021 c.831), sets 2% 'in an action arising out of a consumer debt where a natural person is a defendant', and 5004(b) defines consumer debt by purpose alone, 'including, but not limited to' a consumer credit transaction. So the files' ruling that a lease balance is not consumer credit (CPLR 214-i, GBL art. 29-H) does not decide the interest rate: 5004's definition is the broader one. The files already hold that a former tenant's balance is a household-purpose debt under identical wording (NYC:CPL-tenant-balance-consumer-debt), and the decision they cite for it, Allen v Whidbee, is a CPLR 5004 decision that applies 2% to rent. OCA's April 2024 memorandum tells judges to presume 2% on consumer-debt judgments. This changes the amount of every judgment and the pursue-or-write-off decision.
- Correct rule: Condition: a landlord, successor owner, assignee or collector sues a natural-person former tenant (or individual guarantor) for rent, use and occupancy, damage or any other amount owed under a residential lease. Effect: interest on the claim (CPLR 5001 pre-decision, 5002 verdict to judgment, 5003 post-judgment) runs at 2% a year for judgments entered on or after 2022-04-30, the 120th day after L.2021 c.831 became law; on a judgment entered earlier, post-judgment interest on the part unpaid at that date runs at 2% from then (CPLR 5004(a)). A tenant that is a company is not a natural person: 9% applies. A lease clause charging interest on late or unpaid rent is a 'payment, fee, or charge for the late payment of rent' and cannot exceed the RPL 238-a(2) cap (the lesser of $50 or 5% of the monthly rent); a lease term waiving that cap is void (238-a(3)). Authority: CPLR 5004 (statute; controls); Allen v Whidbee, 88 Misc 3d 319 (Yonkers City Ct 2025), applying it to rent arrears. No decision after the 2022 amendment holds otherwise; Saxon Assoc. v Barton (1989) predates it and construed the Bankruptcy Code definition.
- Evidence:
  - `sources/REVIEW1_NY_CPLR_5004_nysenate.txt`: "provided the annual rate of interest to be paid in an action arising out of a consumer debt where a natural person is a defendant shall be two per centum per annum"
  - `sources/REVIEW1_NY_CPLR_5004_nysenate.txt`: ""consumer debt" means any obligation or alleged obligation of any natural person to pay money arising out of a transaction in which the money, property, insurance or services which are the subject of the transaction are primarily for personal, family or household purposes"
  - `sources/NYC_CASE_Allen_v_Whidbee_2025.txt`: "this court determines residential rent arrears/unpaid rent is deemed a consumer debt pursuant to CPLR 5004"
  - `sources/REVIEW1_NY_L2021_c831_A6474A_bill.txt`: "This act shall take effect on the one hundred twentieth day after"
  - `sources/REVIEW1_SBJ_blog_OCA_2pct_memo_2026.txt`: "Before FCJIA’s effective date of April 30, 2022, rent arrears were"
  - `sources/NY_RPL_238-A.txt`: "No landlord, lessor, sub-lessor or grantor may demand any payment, fee, or charge for the late payment of rent unless the payment of rent has not been made within five days of the date it was due"

### R1-02 (gap, critical)

- Rules: `NY:RPL-226-c(1)(a)`, `NY:ADJ-NYC-monthly-agreed-notice`, `NY:RPL-227-e`
- Review step: 3.1-3.3; C6
- What is wrong: GOL 5-905 is not in the files. Residential leases often provide that the term renews automatically unless the tenant gives notice. Under 5-905 that clause does not operate unless the landlord, 15 to 30 days before the tenant's notice deadline, served written notice personally or by registered or certified mail calling attention to it. Without that notice, a tenant who leaves at the end of the term without notice owes nothing for the renewal period. Step 3 would let an operator bill a renewal term, or treat the tenant as leaving early, when the law ends the tenancy on the stated date.
- Correct rule: Condition: the lease says its term is deemed renewed for a specified additional period unless the tenant gives notice of intent to quit. Effect: the renewal clause binds the tenant only if the landlord gave written notice, served personally or by registered or certified mail, at least 15 and not more than 30 days before the last day for the tenant's notice, calling attention to the clause (GOL 5-905). Without that notice the term ends on its stated date, the tenant owes no rent for the renewal period, and the settlement runs from the actual vacate date. With that notice and no tenant notice, the renewal term binds, and rent after an early departure is limited by the mitigation duty (RPL 227-e). A lease clause cannot displace 5-905.
- Evidence:
  - `sources/REVIEW1_NY_GOL_5-905_nysenate.txt`: "No provision of a lease of any real property or premises which states that the term thereof shall be deemed renewed for a specified additional period of time unless the tenant gives notice to the lessor of his intention to quit the premises at the expiration of such term shall be operative unless the lessor, at least fifteen days and not more than thirty days previous to the time specified for the furnishing of such notice to him, shall give to the tenant written notice, served personally or by registered or certified mail, calling the attention of the tenant to the existence of such provision in the lease."
  - `sources/REVIEW1_NY_AG_Residential_Tenants_Rights_Guide.txt`: "A lease may contain an automatic renewal clause. In such cases, the landlord must give the tenant advanced notice of the existence of this clause between 15 and 30 days before the tenant is required to notify the landlord of an intention not to renew the lease."

### R1-03 (error, critical)

- Rules: `NY:ADJ-cotenants-payee`
- Review step: 6.6; C8
- What is wrong: NY:ADJ-cotenants-payee says paying the whole refund to one co-tenant who made the deposit discharges the landlord, and rests that on Holmes v Worthen. Holmes does not decide it. The majority gave the remaining co-tenant the whole deposit only because the landlord never argued for a split, and it said it would not reach an issue the parties had not raised. The only judge who reached it (the dissent) held that the departed co-tenant kept his interest in his own $1,100. GOL 7-103(1) makes a deposit 'the money of the person making such deposit'. Where identified co-tenants paid identified parts, that text is a word of severance, so the joint-obligee discharge rule of Lasky v Lissik, which applies only where there are 'no words indicating a several liability', does not reach it. As written, the rule lets a landlord pay one co-tenant and remain liable to the other.
- Correct rule: Statement: send the itemized statement within 14 days to every co-tenant at the channel held for each (GCN 35). Refund, branch (a): one deposit paid by or for the tenants together, with no record of who paid what. The refund is a joint obligation. Pay it by one payment to all co-tenants jointly or as all of them direct in writing; payment to one of them also discharges the landlord (Lasky v Lissik; Freedman v Montague), and the co-tenants settle between themselves. Branch (b): the landlord's records show that identified co-tenants paid identified parts. Each co-tenant owns his part (GOL 7-103(1)). Lawful deductions for the joint lease obligations come out of the whole deposit, and the remainder is paid to each co-tenant in proportion to what he paid, unless all of them direct otherwise in writing. Paying the whole remainder to one co-tenant does not discharge the landlord as to another co-tenant's part.
- Evidence:
  - `sources/NY_CASE_Holmes_v_Worthen_2008_AppTerm2d.txt`: "We note that neither party is here arguing the position espoused in the dissenting opinion that plaintiff is entitled to a return of only half of the security deposit."
  - `sources/NY_CASE_Holmes_v_Worthen_2008_AppTerm2d.txt`: "We should not speculate as to matters regarding which the parties themselves have raised no issue"
  - `sources/NY_CASE_Holmes_v_Worthen_2008_AppTerm2d.txt`: "The letter submitted into evidence makes it abundantly clear that the cotenant did not assign his rights to plaintiff and consequently still retains possessory interest over those funds."
  - `sources/NY_GOL_7-103_nysenate.txt`: "shall continue to be the money of the person making such deposit or advance"
  - `sources/NY_CASE_Lasky_v_Lissik_1931.txt`: "where they are payable to individuals jointly and there are no words indicating a several liability, a payment to one of the joint obligees, payees, promisees or mortgagees is a discharge"
  - `sources/NY_CASE_Lasky_v_Lissik_1931.txt`: "words of severance being necessary to overcome this primary presumption"

### R1-04 (gap, critical)

- Rules: `US:CASE-Strumpf-hold`, `US:11USC362(a)(7)`, `US:11USC362(a)(7)-deposit-is-setoff`
- Review step: 6.7; C15
- What is wrong: The review says that after the tenant's bankruptcy filing the landlord 'refunds the rest under state law', which an operator will read as 'pay the tenant'. After a petition, the tenant's interest in the deposit (the tenant's own money under GOL 7-103(1)) is property of the estate (11 U.S.C. 541(a)(1)). In chapter 7, an entity holding estate property, or owing a matured debt that is estate property, must deliver or pay it to the trustee, except to the extent of setoff (542(a), (b)). Paying the debtor is protected only where the payer had neither notice nor knowledge of the case (542(c)). In chapter 13 the debtor remains in possession of estate property (1306(b)). No rule in US.json states the payee after a filing.
- Correct rule: Condition: the tenant filed a bankruptcy petition before the refund was paid, and the landlord has notice or knowledge of the case. Effect: (1) the 14-day statement is still sent, listing the charges and any amount held pending stay relief, without demanding payment of a pre-petition balance (362(a)(6)); (2) the landlord may hold only the amount subject to setoff, and only while it promptly moves for stay relief (Strumpf); (3) the rest is paid, in chapter 7 to the trustee or on the trustee's written order (542(a), (b)), in chapter 13 to the debtor (1306(b)). A refund paid to a chapter 7 debtor after notice does not discharge the landlord as against the trustee. Without notice or knowledge of the case, a good-faith refund to the tenant discharges it (542(c)).
- Evidence:
  - `sources/REVIEW1_US_11USC_541.txt`: "all legal or equitable interests of the debtor in property as of the commencement of the case"
  - `sources/REVIEW1_US_11USC_542.txt`: "an entity that owes a debt that is property of the estate and that is matured, payable on demand, or payable on order, shall pay such debt to, or on the order of, the trustee, except to the extent that such debt may be offset under section 553 of this title against a claim against the debtor"
  - `sources/REVIEW1_US_11USC_542.txt`: "an entity that has neither actual notice nor actual knowledge of the commencement of the case concerning the debtor may transfer property of the estate, or pay a debt owing to the debtor, in good faith"
  - `sources/REVIEW1_US_11USC_1306.txt`: "the debtor shall remain in possession of all property of the estate"
  - `sources/NY_GOL_7-103_nysenate.txt`: "shall continue to be the money of the person making such deposit or advance"

### R1-05 (gap, major)

- Rules: `NY:CPLR-213(2)`, `US:15USC1692e(5)`
- Review step: 8 (decision to pursue); C7; C14
- What is wrong: HPD registration is missing. The owner of every NYC multiple dwelling, and of every one- or two-family house where neither the owner nor a family member lives, must register with HPD each year (Admin. Code 27-2097). An owner that has not registered may, in the court's discretion, 'suffer a stay of proceedings to recover rents' for the period of non-compliance (27-2107(b)). That decides whether a suit for a former tenant's rent can go forward, and a collector threatening suit for an unregistered owner risks threatening action that cannot then be taken (1692e(5)). Most units in the segment (non-owner-occupied houses and small multifamily buildings) are within it.
- Correct rule: Condition: the unit is in a multiple dwelling, or in a one- or two-family dwelling occupied by neither the owner nor a family member (27-2097(b)(1), (3)), and the owner has no current registration. Effect: before suing a former tenant for rent or use and occupancy, or handing the balance to a collector that will sue, the owner files the registration; while it is unregistered, the court may stay the claim for rent until it registers (27-2107(b)). A claim for damage to the unit is not a claim for rent and is not within the stay.
- Evidence:
  - `sources/REVIEW1_NYC_ADC_27-2107.txt`: "An owner who is required to file a statement of registration under this article and who fails to file as required shall be denied the right to recover possession of the premises for nonpayment of rent during the period of noncompliance, and shall, in the discretion of the court, suffer a stay of proceedings to recover rents, during such period."
  - `sources/REVIEW1_NYC_ADC_27-2097.txt`: "For every existing multiple dwelling."
  - `sources/REVIEW1_NYC_ADC_27-2097.txt`: "For all one- and two-family dwellings where neither the owner nor any family member occupies the dwelling"

### R1-06 (gap, major)

- Rules: `NY:RPL-226-c(2)`, `NY:RPL-226-c(1)(a)`, `NY:RPL-220`
- Review step: 3.1, 3.5
- What is wrong: The Good Cause Eviction Law (RPL art. 6-A, applied to New York City by RPL 212) is absent; the NY coverage table lists only its lease-notice section (231-c) as out of scope. Step 3.1 treats a landlord's non-renewal notice as ending the tenancy. For a covered unit, RPL 215 forbids removing a tenant 'by failure to renew any lease, or otherwise' without good cause. A non-renewal of a covered tenancy therefore does not create a departure, and a tenant who stays is not a holdover to be charged as one.
- Correct rule: Condition: a market-rate NYC unit not exempt under RPL 214 (exemptions include premises of a small landlord, an owner-occupied building of no more than ten units, a building whose certificate of occupancy issued on or after 2009-01-01, for 30 years, condominium and cooperative units, and units regulated or income-restricted under other law). Effect: the landlord cannot end the tenancy by non-renewal without a good-cause ground under RPL 216; a 226-c non-renewal notice alone does not start the settlement chain, which starts on the tenant's actual departure or a court order of removal. For an exempt unit Step 3.1 applies as written. Article 6-A is repealed 2034-06-15.
- Evidence:
  - `sources/REVIEW1_NY_RPL_215_nysenate.txt`: "No landlord shall, by action to evict or to recover possession, by exclusion from possession, by failure to renew any lease, or otherwise, remove any tenant from housing accommodations covered by section two hundred fourteen of this article except for good cause as defined in section two hundred sixteen of this article."
  - `sources/REVIEW1_NY_RPL_212_nysenate.txt`: "Upon the effective date of this section, this article shall apply to the city of New York."
  - `sources/REVIEW1_NY_RPL_214_nysenate.txt`: "owner-occupied housing accommodation with no more then ten units"
  - `sources/REVIEW1_NY_RPL_214_nysenate.txt`: "certificate of occupancy was issued on or after the first of January, two thousand nine"
  - `sources/REVIEW1_NY_RPL_215_nysenate.txt`: "NB Repealed June 15, 2034"

### R1-07 (misstatement-in-review, minor)

- Rules: `NYC:HMC-27-2013(b)(2)`, `NYC:HMC-27-2013(g)`, `NYC:PAINT-wear-and-tear`
- Review step: 1.5, 5.3
- What is wrong: The review says the owner 'must repaint every three years' and 'must keep records of when each unit was last painted' without the condition that both duties apply only in a multiple dwelling. In a tenant-occupied one- or two-family house, 27-2013(a) requires repainting only when HPD judges it necessary to keep surfaces sanitary, and no painting records are required. The wear-and-tear outcome does not change, but an operator of single-family houses would look for a cycle and records the law does not require.
- Correct rule: Multiple dwelling: repaint every three years (27-2013(b)(2)) and keep painting records (27-2013(g)). One- or two-family dwelling: paint, and repaint when necessary to keep surfaces sanitary (27-2013(a)); no records duty. In both, repainting made necessary by ordinary occupancy is wear and tear and not chargeable to the tenant (GOL 7-108(1-a)(b); Bohl v Poffenbarger).
- Evidence:
  - `sources/NYC_ADC_27-2013.txt`: "In the public parts of a multiple dwelling, and in a tenant-occupied dwelling unit in a one- or two-family dwelling, the owner shall:"
  - `sources/NYC_ADC_27-2013.txt`: "Repaint or re-cover the walls and ceilings with wallpaper or other acceptable wall covering whenever necessary in the judgement of the department to keep such surfaces sanitary."

### R1-08 (misstatement-in-review, minor)

- Rules: `NY:RPL-236`
- Review step: 2.5
- What is wrong: The review says 'the landlord's refusal or silence can end the lease'. Under RPL 236 silence is deemed consent to the estate's proposed assignment or sublet; it does not end the lease. The lease ends only if the landlord elects to terminate or unreasonably refuses.
- Correct rule: When a deceased tenant's estate asks in the statutory form to assign or sublet: silence for 30 days is consent; a landlord election to terminate or an unreasonable refusal terminates the lease and discharges the estate and co-tenants from the last day of the month in which the landlord had to act; a reasonable refusal keeps the lease in force (RPL 236).
- Evidence:
  - `sources/NY_RPL_236.txt`: "Landlord's failure to send such a notice shall be deemed to be a consent to the proposed assignment or subletting."

### R1-09 (misstatement-in-review, minor)

- Rules: `NY:GOL-7-108(1-a)(a)`
- Review step: 1.1
- What is wrong: 'Deposit plus any advance rent may not exceed one month's rent' (and the rule's 'Advance includes prepaid rent') will be read to forbid collecting the first month's rent together with a one-month deposit at signing. The cap reaches money paid ahead as security or as prepayment of a later period, such as last month's rent; the Attorney General's guide reads it that way.
- Correct rule: Deposit plus any rent paid ahead for a later period (for example last month's rent) may not exceed one month's rent (GOL 7-108(1-a)(a)). The first month's rent paid at signing for the first rental period is rent, not an advance. Any excess is refundable at settlement.
- Evidence:
  - `sources/NY_GOL_7-108_nysenate.txt`: "No deposit or advance shall exceed the amount of one month's rent"
  - `sources/REVIEW1_NY_AG_Residential_Tenants_Rights_Guide.txt`: "The one-month limit means that a landlord cannot ask for last month’s rent and a security deposit."

### R1-10 (misstatement-in-review, minor)

- Rules: `NY:ADJ-willful-standard`, `NY:CASE-Bogom-Shanon-willful`
- Review step: 7.5
- What is wrong: The review states flatly that 'a mistake of law is no defense'. The rule limits that to a landlord experienced with the law or acting through a managing agent, and keeps Masseroli's result (no willfulness) for an individual owner without that experience who sent a late statement in good faith. Bogom-Shanon's defendant was an attorney.
- Correct rule: For a landlord experienced with the deposit law, or acting through a managing agent (every account a manager or Handoff handles), ignorance or a mistaken reading of the law is no defense to willfulness. For an individual owner without that experience who sent a late written statement in good faith, the violation alone does not show willfulness.
- Evidence:
  - `sources/NY_CASE_Bogom-Shanon_v_Altman_2025.txt`: "a unilateral mistake of law, particularly where defendant is an attorney admitted in this state, is not a defense to liability"
  - `sources/NY_CASE_Masseroli_v_Gatfield_2024.txt`: "Under the circumstances, the court finds that defendant did not willfully violate the statute."

### R1-11 (misstatement-in-review, minor)

- Rules: `NY:GOL-7-108(1-a)(e)`, `NY:ADJ-provide-address-branches`
- Review step: C3
- What is wrong: C3 says 'statement and refund, with interest less 1%, by email within 14 days'. An email carries the statement; it does not return money. The statute requires the landlord to 'return' the remainder within the 14 days.
- Correct rule: Send the statement by email within 14 days, and within the same 14 days pay the refund by a method that reaches the tenant: an electronic transfer to an account the tenant can receive, or a check mailed to a postal forwarding address or, with none, to the vacated unit.
- Evidence:
  - `sources/NY_GOL_7-108_nysenate.txt`: "shall return any remaining portion of the deposit to the tenant"

### R1-12 (weak-support, minor)

- Rules: `NY:ADJ-provide-address-branches`, `NY:CASE-Pickens-provide`
- Review step: 6.5
- What is wrong: The rule that mailing to the vacated unit is not 'providing' the statement when another channel is known rests on one New York County Civil Court decision, where the landlord held an email the tenant used. The rule extends it to any known 'phone number' without citing anything for that limb. The outcome is right, but the phone limb needs its own ground.
- Correct rule: Where the landlord holds an email address or phone number the tenant used with it, the landlord sends the itemized statement through that channel within 14 days (an email or text message is a written statement: Bogom-Shanon); mailing only to the vacated unit is then not providing it (Pickens), and forfeiture follows. With no forwarding address and no electronic channel, mail to the vacated unit within 14 days.
- Evidence:
  - `sources/NY_CASE_Pickens_v_Lane_2023.txt`: "claimant testified that defendant had claimant's email"
  - `sources/NY_CASE_Bogom-Shanon_v_Altman_2025.txt`: "whether by letter, email, text, or any other written means"

### R1-13 (gap, minor)

- Rules: `US:50USC3931(b)(1)`
- Review step: 8.9
- What is wrong: Step 8.9 gives only the SCRA affidavit before a default judgment. CPLR 3215(g)(3) adds a state step for any action on a contractual obligation against a natural person: an additional mailed notice at least 20 days before the default judgment, proved by affidavit.
- Correct rule: Condition: the landlord or collector seeks a default judgment against a natural-person former tenant on the lease. Effect: at least 20 days before entry, mail a copy of the summons first class to the tenant's residence in an envelope marked 'personal and confidential' that does not show it concerns a debt, and file an affidavit of that mailing (CPLR 3215(g)(3)), in addition to the SCRA affidavit.
- Evidence:
  - `sources/REVIEW1_NY_CPLR_3215_justia.txt`: "When a default judgment based upon nonappearance is sought against a natural person in an action based upon nonpayment of a contractual obligation an affidavit shall be submitted that additional notice has been given by or on behalf of the plaintiff at least twenty days before the entry of such judgment"

### R1-14 (gap, minor)

- Rules: `NY:CPLR-213(2)`
- Review step: 8 (decision to pursue)
- What is wrong: The review does not say where a small balance can be sued. A corporate or LLC owner cannot use the NYC Civil Court small claims part, and its commercial claims part requires a pre-suit demand letter for a claim arising from a consumer transaction, which a residential lease with a natural person is.
- Correct rule: An owner that is a corporation, partnership or association (including an LLC) cannot bring a small claim (CCA 1809(1)). It may bring a commercial claim within the small-claims dollar limit; where the defendant is a natural person and the claim arises from a residential lease (a 'consumer transaction', CCA 1801-A(b)), it must first mail the OCA-form demand letter 10 to 180 days before filing and certify that it has filed no more than five such claims that month (CCA 1803-A).
- Evidence:
  - `sources/REVIEW1_NY_CCA_1809_nysenate.txt`: "No corporation, except a municipal corporation, public benefit corporation, school district or school district public library wholly or partially within the municipal corporate limit, no partnership, or association and no assignee of any small claim shall institute an action or proceeding under this article"
  - `sources/REVIEW1_NY_CCA_1801-A_nysenate.txt`: "The term "consumer transaction" means a transaction between a claimant and a natural person, wherein the money, property or service which is the subject of the transaction is primarily for personal, family or household purposes."
  - `sources/REVIEW1_NY_CCA_1803-A_nysenate.txt`: "the claimant has mailed by ordinary first class mail to the party complained against a demand letter, no less than ten days and no more than one hundred eighty days prior to the commencement of the claim"

### R1-15 (over-scope, minor)

- Rules: `NY:GBL-600(1)`, `NY:GBL-600(3)`, `NY:GBL-601(2)`, `NY:GBL-601(3)`, `NY:GBL-601(4)`, `NY:GBL-601(5)`, `NY:GBL-601(6)`, `NY:GBL-601(7)`, `NY:GBL-601(8)`, `NY:GBL-601(9)`, `NY:GBL-601(12)`, `NY:GBL-601-b`, `NY:GBL-602`, `US:50USC3951(a)(1)(B)`, `US:50USC3951-distress-NY`, `US:FR-2026-04689`, `NY:ABP-1310`, `NY:GOL-7-109`
- Review step: 6.8, 6.9, 7.6, 8.1
- What is wrong: These rules change no decision for a market-rate NYC unit. The review itself holds that GBL art. 29-H does not reach a lease balance, so its thirteen conduct rules are recorded 'for completeness' only. Distress was abolished in New York in 1846, so the SCRA distress rule and its rent threshold decide nothing here. ABP 1310 covers property 'not otherwise subject to' the Abandoned Property Law, and an unclaimed deposit refund is subject to ABP 1315. GOL 7-109 is Attorney General enforcement, not a manager's choice.
- Correct rule: Keep them in the files. In the walk, keep one sentence for each point (art. 29-H does not apply: NY:ADJ-lease-balance-not-consumer-credit; no distress in New York: US:50USC3951-distress-NY) and move the rest to the deferred list.
- Evidence:
  - `sources/NY_GBL_600.txt`: "arises out of a transaction wherein credit has been offered or extended to a natural person"
  - `sources/US_CASE_Van_Rensselaer_v_Snyder_1855.txt`: "The act of 1846 (ch. 274) abolished the remedy of distress for rent"
  - `sources/NY_ABP_1310.txt`: "which is not otherwise subject to the provisions of this chapter"

### R1-16 (alignment, minor)

- Rules: none (review text)
- Review step: 8.1; 'Where the rulings rest on lighter authority'
- What is wrong: The review states the law, then adds provenance that invites doubt: 'No appellate court has ruled on this' (8.1) and a closing list of 'lighter authority' rulings 'so you know what a higher court could change'. The owner's ruling asks for the answer and its controlling authority, not a weight warning. The list is also wrong on its own terms: it includes the Second Circuit's default test, which binds.
- Correct rule: State each ruling once with its controlling authority and why it prevails (for example: 'CPLR 214-i does not apply: the lease is not a credit transaction (CPLR 105(f) text; Romea, 2d Cir.; Lefferts; Rhumb W 21; Allen)'). Drop the 'lighter authority' section.
- Evidence:
  - `review/NYC_MARKET_RATE.md`: "No appellate court has ruled on"
  - `review/NYC_MARKET_RATE.md`: "The debt "default" test (8.2): the Second Circuit, binding on New York federal courts."

### R1-17 (stale-source, minor)

- Rules: `NY:CASE-Gelbart-rent-offset`, `US:50USC3951-distress-NY`, `NY:RPL-235-b`, `NY:ADJ-cotenants-vacated`, `US:15USC1692a(5)-lease-charges`
- Review step: 5.5, 6.2, 6.9, 8.1
- What is wrong: Five rules quote unofficial mirrors: Gelbart and Van Rensselaer from hallapproved.com, RPL 235-b and GCN 35 from Justia, Mabe from openjurist.org. The quoted words are the law, but the files' own standard is the official text.
- Correct rule: Re-save from official text: Gelbart from the nycourts.gov reporter (2023 NY Slip Op 51404(U)); RPL 235-b and GCN 35 from nysenate.gov (or the Legislative Bill Drafting Commission text); Van Rensselaer and Mabe from CourtListener or the official reporter. Re-run stage_a_check.py.
- Evidence:
  - `sources/NY_CASE_Gelbart_v_Spota_2023.txt`: "reprint of 2023 NY Slip Op 51404(U) from CourtListener bulk data"

## Confirmed

- Forfeiture removes the security, not the debt (NY:ADJ-forfeiture-claims-survive; 7.2). Stands. 7-108(1-a)(e) forfeits only the 'right to retain any portion of the deposit'; Levine (App Term 1st Dept 2026) decided the damage counterclaim on its merits after full return; Paterno (2d Dept) keeps rent claims after a 7-103 forfeiture; Pickens netted rent. No contrary decision found.
- 'Willfully' in 7-108(1-a)(g) (NY:ADJ-willful-standard; 7.5). Stands, subject to R1-10's wording. Knew-or-should-have-known is the Appellate Division meaning in punitive civil statutes; Wagenheim v Bencheikh (App Term 2d Dept 2023) confirms punitive damages need record evidence of willfulness.
- 'Provide': written, timed by the send date (NY:ADJ-provide-written-dispatch; 6.4). Stands. Cohen (2d Dept) counted the send date; Urban (1st Dept) asked whether vacatur was more than 14 days before the email 'providing' the statement; Freeland (1st Dept 2026) accepts email where the parties used it.
- No forwarding address: send to the vacated unit within 14 days (NY:ADJ-provide-address-branches (b); C9). Stands. Prando (App Term) upheld forfeiture where the landlord waited for an address.
- Estimated costs on the statement (NY:CASE-Toporek-estimate; 6.4). Stands. Toporek (1st Dept) held a timely statement itemizing estimates compliant; cost disputes go to trial on the landlord's burden.
- Co-tenant clock starts when the last tenant leaves (NY:ADJ-cotenants-vacated; 2.4). Stands. The tenancy and 'the tenant' (GCN 35) have not vacated while a co-tenant holds under the lease; Holmes' facts fit. The payee half does not stand (R1-03).
- A former tenant's lease balance is not consumer credit: GBL art. 29-H does not apply; CPLR 213(2) six years, not 214-i (8.1). Stands, on more authority than the file cites: CPLR 105(f) and GBL 600(1) both require credit offered or extended; Romea (2d Cir.); Lefferts (Civ Ct Kings 2026); Rhumb W 21 LLC v Wolfe (Sup Ct NY County 2023) and Allen v Whidbee (Yonkers 2025), as recounted in Allen. The separate CPLR 5004 interest rate is R1-01.
- Abandoned belongings (NY:COMMONLAW-belongings-*; 6.9; C11). Stands. No statute governs a voluntary move-out; 8902 Corp (1st Dept) no bailment without agreement; Cretaro (4th Dept) and Henryka (App Term 2d Dept) abandonment test; Facey: no holding for rent.
- NYC month-to-month tenant may surrender at month end without notice (NY:COMMONLAW-NYC-monthly-tenant-surrender; 3.2). Stands, and binds in both departments: besides T.I.B. Corp (App Term 1st Dept, affd 261 AD 813), Srinivasan v Silvi (App Term 2d Dept 2008) holds the NYC month-to-month tenant has no statutory duty to give notice. The file should add Srinivasan.
- Fees are not retainable from the deposit (NY:ADJ-no-fee-retention; 5.2). Stands. The four retention categories are closed (Colon, Statutes 240); RPAPL 702 in the same act separates rent from fees; 7-108(3) voids relabelling. A CourtListener search found no decision allowing a late fee to be kept from a 7-108(1-a) deposit.
- FARE Act move-out service fees (NYC:FARE-moveout-service-fee; 5.4). Stands. 20-699.22(b) covers 'any fees' the tenant must pay 'in connection with' the rental; 20-699.20 defines a fee as a charge for services, so rent and damages are outside it.
- Painting and wear and tear (NYC:PAINT-wear-and-tear; 5.3). Stands for multiple dwellings (Bohl, App Term 2d Dept; HMC 27-2013(b)(2)); see R1-07 for one- and two-family houses.
- FDCPA 'default' test (US:15USC1692a(6)(F)(iii)-default-meaning; 8.2). Stands. Alibrandi (2d Cir. 2003) rejects default-on-due-date, lets the contract set the delinquency period and treats referral to a self-identified collector as a declaration of default; it binds federal courts in New York.
- Property-manager fiduciary exclusion (US:15USC1692a(6)(F)(i)-manager-incidental; 8.2). Stands. Wilson (4th Cir.) incidental-versus-central test, Harris (11th Cir.) applied to a manager; no circuit applies another test; collection-only engagements fall outside it (FTC 1988 commentary).
- Handoff configurations A-E (US:HANDOFF-config-*; 8.2). Stand. The (F) exclusions qualify both prongs (Franceschi); 'obtained' includes authority to collect; Henson governs own-account collection; Barbato reaches a principal-purpose buyer; Vincent and Maguire fix the false-name limb.
- NYC DCWP licensing configurations (NYC:DCA-*; 8.6). Stand. 20-489(a) joins 'principal purpose' and 'regularly'; (a)(7)(i) fiduciary exclusion; (a)(7)(iii) is limited to a secured party in a commercial credit transaction, so it gives no pre-default exclusion, and the review correctly does not claim one.
- Current 6 RCNY 5-76/5-77 bind the landlord's and manager's own staff (8.4). Stands. The current 'debt collector' definition covers any individual who regularly collects 'a debt owed or due' and has no creditor-employee exclusion.
- SHIELD Rule operative 2027-01-01 (NYC:SHIELD-operative-date; 8.5). Stands. DCWP, which adopted and enforces the rule, published the change of effective date in the City Record before 2026-09-01, and its conforming rule is still 'Proposed' on rules.cityofnewyork.us on 2026-09-28 (comment period closed 2026-09-17).
- Bankruptcy: applying the deposit is a stayed setoff; a Strumpf hold is allowed (6.7; C15). Stands as to the stay and the hold. The payee after a filing is R1-04.
- 14-day count and holidays (6.3; C12). Stands. GCN 20 excludes the vacate day; GCN 25-a moves a Saturday, Sunday or holiday deadline to the next business day. Checked by computation: vacate Friday 2026-12-11, day 14 Friday 2026-12-25 (GCN 24 holiday), due Monday 2026-12-28; Cohen: vacated 2020-07-24, due 2020-08-07.
- Interest-bearing account per building, six units (NY:ADJ-7103-2a-building-count; 1.2). Stands. Gihon (2d Dept) tests the building; the Attorney General's guide says 'buildings with six or more apartments'.
- Commingling forfeiture and the bank-notice inference (7.3). Stands. Paterno and Gihon (2d Dept); Wagenheim (App Term 2d Dept 2023, citing Milkie, 2d Dept 2016) applied it and held that naming the bank after vacatur does not cure it.
- Which regime applies by lease date; renewal by rent acceptance (0.4; C5a). Stands. Part M s.29 applies 1-a to leases and renewals entered from 2019-07-14; Case v 575 Classon (App Term 2d Dept) treats rent acceptance after expiry as a renewal tenancy (RPL 232-c).
- Mitigation (RPL 227-e; Toporek; 3.3). Stands. Text plus Toporek (1st Dept): the landlord's burden; actual re-letting not required.
- Late fee and returned-check caps; legal fees only by court order (5.2). Stands on the text of RPL 238-a(2), (2-a), GOL 5-328(3)(b), RPL 234-a and L.2021 c.695 as amended by L.2022 c.162.
- Housing Choice Voucher settlement (5.7; C13). Stands on 24 CFR 982.311(d)(1), 982.313(c)-(e) and 982.451(b)(4).
- SCRA termination and deposit clock (3.4, 6.2). Stands on 50 U.S.C. 3955(a)-(h) text; the deposit clock follows State law, and 3955(h) bars holding it for post-termination rent.
- Owner collecting in its own name is not an FDCPA debt collector (8.2). Stands. Henson (U.S. 2017); Reg F comment 2(i)-1; 1692a(6)(A) for the creditor's own staff.
- 7-108(1-a)(d) inspection-notice failure does not forfeit (4.3). Stands. Toporek (1st Dept): only paragraph (e) carries forfeiture.
- Interest on the deposit (5.6). Stands on GOL 7-103(2), (2-a), (2-b); the Attorney General's guide gives the same 1% administration rule.

## Test cases (decided independently from the law)

| Case | My answer | Against the review |
|---|---|---|
| C3 | Statement by email within 14 days itemizing each deduction; refund of the deposit plus the interest the bank paid, less 1% a year of the deposit as the landlord's fee, less lawful deductions; no fees retained; no charge for repainting from ordinary use. The refund itself must be a payment that reaches the tenant within the 14 days. | Differs in wording only (R1-11). |
| C4 | Agree. No interest-bearing account required (building of fewer than six units, counted alone); bank notice and interest less 1% only if the landlord banked the deposit in such an account. Not stabilized (fewer than six units, no J-51, Article 18 or 421-a); not controlled (vacated since 1971-06-30; the one- and two-family exemption does not apply to a three-family house, but the 1971 vacancy exemption does). A three-family house is a multiple dwelling, so the three-year repaint rule and HPD registration (R1-05) apply. | Agrees; adds registration. |
| C5a | Agree. Rent accepted after the 2018 lease expired created a month-to-month tenancy after 2019-07-14 (RPL 232-c; Case v 575 Classon), so 7-108(1-a) applies. | Agrees. |
| C6 | Agree on mitigation (landlord's burden; re-letting efforts, not success) and on statutory terminations (DV: 30 days after notice; senior/disabled: 30 days after the next rent date; SCRA: 30 days after the next rent date for a monthly lease). Add: if the lease has an automatic renewal clause, it binds only with the GOL 5-905 notice (R1-02). Deposit clock runs from vacating. | Agrees; adds 5-905. |
| C7 | Agree: timely statement itemizing estimates (Toporek); the excess is a separate claim that survives forfeiture; no legal fees without a court order. Add: any judgment against a natural-person tenant carries 2% interest (R1-01); an unregistered owner may have the rent claim stayed (R1-05). | Agrees; adds interest rate and registration. |
| C8 | No statement or refund when the first co-tenant leaves. After the second leaves: statement to each within 14 days. Refund: if the deposit was paid as one sum with no record of who paid what, one payment to both jointly (payment to either also discharges); if the landlord's records show each paid a part, each gets the remainder in proportion to what he paid unless both direct otherwise in writing. | Differs (R1-03): the review lets the landlord pay the whole refund to one co-tenant in every case. |
| C9 | Agree. Statement and refund mailed to the vacated unit within 14 days; an unclaimed refund stays the tenant's trust money and is reported and paid to the Comptroller after three years (ABP 1315). | Agrees. |
| C10 | Agree. Seller turns the deposit (with interest) over within five days of the deed and notifies the tenant by registered or certified mail; the buyer settles. If it was not turned over, a buyer with actual knowledge (deemed from a lease acknowledging it or a 7-103(2-a) bank deposit) is also liable. | Agrees. |
| C11 | Agree. Belongings stay the tenant's; no holding for rent; release on request; disposal only once abandoned; reasonable moving and storage cost may be kept from the deposit. | Agrees. |
| C12 | Agree. Vacated Friday 2026-12-11; day 14 is Friday 2026-12-25 (Christmas, a GCN 24 public holiday); Saturday and Sunday follow; statement and refund due Monday 2026-12-28. | Agrees (computed). |
| C13 | Agree. Only the tenant's share of rent is charged; the owner keeps the move-out month's HAP and gets none after; written list and refund within 14 days. | Agrees. |
| C14 | Agree: the agency is a federal debt collector and needs a DCWP licence; validation notice within five days of first contact by a method that reaches the tenant (not the vacated unit once it knows she moved); verification with the lease and the landlord's final statement; six-year limit. Add: statutory interest on any judgment is 2% (R1-01); check the owner's HPD registration before suing for rent (R1-05); from 2027-01-01 the SHIELD notice applies to accounts first requiring validation then. | Agrees; adds interest and registration. |
| C15 | Tenant filed on day 5. Statement still due by day 14, listing charges and any amount held, with no demand for payment. The landlord may hold only the amount subject to setoff while it promptly moves for stay relief. The rest is paid to the chapter 7 trustee (or to the debtor in chapter 13), not to the tenant, once the landlord knows of the case. | Differs on the payee (R1-04). |

## Method

- Read APERTURE.md, STAGE_A.md, CORDON DESIGN_PRINCIPLES (method), the review in full, and the statute-compilation reference notes. Ran check_review.py (437 in scope: 359 cited, 78 deferred, 0 uncited) and stage_a_check.py (0 errors in all four files).
- Fidelity: review/ir1_dump.py printed, for every cited rule, the citing paragraph next to the rule's condition, effect, quote, source and construction quotes (3,782 lines); I read all of it. Opened sources in context for the rulings that carry forfeiture, payee or liability: Holmes, Lasky, Freedman, Allen, Freeland, Levine, Pickens, Bogom-Shanon, Masseroli, HMC 27-2013, RPL 236, 6 RCNY 5-76, Admin. Code 20-489.
- Adjudications: re-decided each listed ruling; searched for later or contrary authority on CourtListener (v4 search API: 7-108 late fees, 214-i and rent, 5004 and rent, 7-108 willfulness) and the web (nycourts.gov reporter, Justia, FindLaw case pages). Found and saved Srinivasan v Silvi (App Term 2d Dept 2008) and Wagenheim v Bencheikh (App Term 2d Dept 2023), both confirming; found the CPLR 5004 line (Allen; OCA 2024 memorandum) that the files cite for a different point but never apply to the balance.
- Completeness: compared the RPL art. 7 index and the files' coverage table section by section; searched the files for CPLR 5004/5001, Good Cause, GOL 5-905, 11 U.S.C. 541/542, HPD registration, CPLR 3215 and the Civil Court Act. Each absent item that changes a decision is a finding; each carries a saved source.
- Sources saved (REVIEW1_): CPLR 5004 and 3215; L.2021 c.831 bill text; GOL 5-905; RPL 212, 214, 215, 216; CCA 1801-A, 1803-A, 1809; Admin. Code 27-2097 and 27-2107 (extracted mechanically from American Legal's official bulk XML by review/ir1_aml.py); 11 U.S.C. 541, 542, 1306 (uscode.house.gov); the Attorney General's Residential Tenants' Rights Guide; Srinivasan; Wagenheim; a law-firm note reporting OCA's April 2024 2% memorandum.
- Access: nysenate.gov returned an empty page for CPLR 3215, so the Justia 2025 compilation is saved instead; American Legal's web pages are Cloudflare-walled, so Admin. Code text came from the bulk XML; the OCA memorandum itself was not found online and is evidenced through a secondary report; Google Scholar was not used.
- No rule file, review, scope file or existing source was edited. Helpers: review/ir1_dump.py, ir1_aml.py, ir1_build.py, ir1_verify.py.
