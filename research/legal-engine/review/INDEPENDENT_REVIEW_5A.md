# Independent review 5A (completeness): NYC market-rate settlement chain

2026-09-30. Reviewer 5A. Report only: no rule file, walk, source or skill was edited. Evidence prefix REVIEW5A_, helper prefix ir5a_.

## Summary

- Universe (enumerated blind from primary sources before any rule file was opened): **264 items** (state, city and federal statutes, regulations, rules, controlling decisions, guidance and pending law), in `review/review5a_universe.json`, every item with a verbatim quote from a saved source.
- Against the rule files: 183 items stated; 8 change no decision; **73 items not stated or stated only in part**, grouped into **41 findings**: **14 critical, 10 major, 17 minor**.
- Over-scope: 1 group (5 NYC rules on HPD article VIII escrow), minor.
- Convergence against round 4A's universe (176 items): 148 of 5A's 264 items are in 4A's universe; 116 are only in 5A; 27 of 4A's items are not in 5A (22 are decision-changing law 5A missed; 5 are guidance or law that does not reach a lease balance: U096, U105, U125, U126, U144). **71 gap items are in neither 4A's universe nor the rule files**; every one of the 41 findings carries law 4A did not enumerate.
- Judgment on completeness: not converged. Two blind enumerations of the same chain overlap on 85% of 4A's items (149 of 176) and 56% of 5A's (148 of 264); each found real law the other missed, and 5A found 14 critical gaps (a forfeiture-triggering delivery rule, a rewritten consumer statute in force since 2026-02-17, champerty on hand-off, a rent bar for public-assistance tenants, unlawful-eviction penalties on retaking a unit, TCPA damages, co-tenant releases, accord and satisfaction, submetering, the bankruptcy claim deadline, post-judgment recovery, a heating-oil credit, fair-housing liability for agents and the 30-day breach notice). The misses cluster where the chain leaves the deposit statute: general contract and payment law (GOL arts. 15 and 17, UCC 1-308), judgment enforcement and court practice (CPLR arts. 2, 3, 50, 52; Judiciary Law), communications law (TCPA, E-SIGN) and data law. The next round should sweep those families by table of contents.

Severity: critical = amount, rate, deadline, forfeiture, damages, who is paid, liability, or whether a regime or licence applies; major = operator action; minor = wording or a narrow branch.

## Findings (most severe first)

### R5A-01 (critical, partial) — S6 statement delivery / S8 forfeiture

Related rules: `NY:ADJ-provide-written-dispatch`, `NY:STT-305(3)`, `NY:GOL-7-108(1-a)(e)-forfeiture`

**What is missing.** The rules let the landlord 'provide' the 14-day itemized statement by email or text with no consent condition, and read ESRA (STT 305) as making any electronic record equal to paper. Neither the rule files nor 4A contain the federal E-SIGN consumer-consent rule. GOL 7-108(1-a)(e) requires information (an itemized statement) to be provided to a consumer in writing; under 15 USC 7001(c) an electronic record satisfies that only after the tenant's affirmative E-SIGN consent. ESRA cannot displace 7001(c): it is not UETA, and its equivalence rule is inconsistent with 7001(c) (7002(a)). E-SIGN reaches residential rental agreements (7003(b)(2)(B) names them). A statement e-mailed without consent is not 'provided' in writing, so a landlord relying on it alone within 14 days forfeits.

**Correct law, as a rule.** If the itemized statement (GOL 7-108(1-a)(e)) or any other information the chain's statutes require be given to the tenant in writing is sent electronically, it counts as provided only if before sending the tenant (a) received the 7001(c)(1)(B) disclosures (right to paper, right to withdraw, scope, how to get paper), (b) affirmatively consented electronically in a way that reasonably shows it can access the format, and (c) has not withdrawn consent. Otherwise the statement must go on paper (mail or hand delivery) within the 14 days; email may be sent in addition. The refund payment itself is not 'information' and may be made by any means directed to the tenant. Notices of default, eviction or the right to cure under a residential rental agreement (e.g., the RPAPL 711(2) 14-day rent demand) are outside E-SIGN (7003(b)(2)(B)) and must be on paper. Federal law prevails over STT 305 to the extent inconsistent (Supremacy; 7002(a)).

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_US_15USC_7001_ESIGN.txt`: "(c) Consumer disclosures (1) Consent to electronic records Notwithstanding subsection (a), if a statute, regulation, or other rule of law requires that information relating to a transaction or transactions in or affecting interstate or foreign commerce be provided or made available to a consumer in writing, the use of an electronic record to provide or make available (whichever is required) such information satisfies the requirement that such information be in writing if- (A) the consumer has affirmatively consented to such use and has not withdrawn such consent;"
- `sources/NY_GOL_7-108_nysenate.txt`: "(e) Within fourteen days after the tenant has vacated the premises, the landlord shall provide the tenant with an itemized statement indicating the basis for the amount of the deposit retained, if any, and shall return any remaining portion of the deposit to the tenant. If a landlord fails to provide the tenant with the statement and deposit within fourteen days, the landlord shall forfeit any right to retain any portion of the deposit."
- `sources/REVIEW5A_US_15USC_7001_ESIGN.txt`: "(2) require any person to agree to use or accept electronic records or electronic signatures, other than a governmental agency with respect to a record other than a contract to which it is a party."
- `sources/REVIEW5A_US_15USC_7003_ESIGN.txt`: "(B) default, acceleration, repossession, foreclosure, or eviction, or the right to cure, under a credit agreement secured by, or a rental agreement for, a primary residence of an individual;"
- `sources/REVIEW5A_US_15USC_7002_ESIGN.txt`: "(B) if enacted or adopted after June 30, 2000, makes specific reference to this chapter."

### R5A-02 (critical, gap) — S5 charges / S13 collection conduct

Related rules: `NYC:CPL-20-700`

**What is missing.** No rule states GBL 349 at all, and in particular not as rewritten by the FAIR Business Practices Act (L.2025 c.708, signed 2025-12-19, effective the 60th day, 2026-02-17). It now bans unfair and abusive acts (not only deceptive ones) in any business, including residential leasing and collection, with no 'consumer-oriented' limit in Attorney General enforcement. A standard move-out charge practice (e.g., a fee the tenant cannot avoid or understand) is judged under the unfairness/abusiveness tests. The private action remains limited to deceptive acts (actual damages or $50, trebled up to $1,000 if willful, fees).

**Correct law, as a rule.** From 2026-02-17: (1) Any unfair act (causes or is likely to cause substantial injury not reasonably avoidable and not outweighed by benefits), abusive act (materially interferes with understanding a term, or takes unreasonable advantage of a tenant's lack of understanding, inability to protect interests, or reasonable reliance) or deceptive act in leasing or collecting from a residential tenant is unlawful; the Attorney General may enjoin, obtain restitution and penalties without showing consumer-oriented conduct, after 5 business days' certified-mail pre-suit notice. (2) A tenant injured by a consumer-oriented deceptive act or practice may sue for actual damages or $50, whichever is greater, trebled up to $1,000 for willful or knowing violations, plus attorney's fees. Charges and collection communications must be tested against both.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_GBL_349.txt`: "(a) Unfair, deceptive, or abusive acts or practices in the conduct of any business, trade or commerce or in the furnishing of any service in this state are hereby declared unlawful."
- `sources/REVIEW5A_NY_GBL_349.txt`: "(h) In addition to the right of action granted to the attorney general pursuant to this section, any person who has been injured by reason of any deceptive act or deceptive practice made unlawful by this section may bring an action in such person’s own name to enjoin such deceptive act or deceptive practice, an action to recover such person’s actual damages or fifty dollars, whichever is greater, or both such actions."
- `sources/REVIEW5A_NY_A08427A_S08416_FAIR_Act_L2025c708_Assembly.txt`: "§ 6. This act shall take effect on the sixtieth day after it shall 29 have become a law."

### R5A-03 (critical, gap) — S9 hand-off (assignment) / S10 who may sue

Related rules: `NY:HANDOFF-broker-config-collection-agency`, `NY:CCA-1809(1)`

**What is missing.** The hand-off configurations cover licensing and FDCPA status but not champerty. Judiciary Law 489 bars any collection business and any corporation from taking an assignment of a claim with the intent and primary purpose of suing on it; the $500,000 safe harbor needs a binding aggregate purchase price at or above that amount (Justinian, Court of Appeals 2016). An assignment of a former tenant's balance to Handoff or a collection agency so that the assignee can sue in its own name is champertous and void as a basis for suit; violators face a fine or misdemeanor.

**Correct law, as a rule.** Configuration A (owner keeps the claim; Handoff/agency collects as agent and any suit is the owner's): 489 does not apply. Configuration B (the balance is assigned or sold to Handoff, an affiliate or a collection business, and the assignee intends to sue on it): the assignment is champertous unless the assignee paid or is bound to pay an aggregate purchase price of at least $500,000 for claims against the same obligor (never met for a tenant balance); the assignee cannot maintain the action (defense of champerty) and faces a fine up to $5,000 (corporation) or misdemeanor (person). An assignment taken for collection without intent to sue, with suit left to the owner, is outside 489. CCA 1809 separately bars assignees from small claims.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_JUD_489.txt`: "1. No person or co-partnership, engaged directly or indirectly in the business of collection and adjustment of claims, and no corporation or association, directly or indirectly, itself or by or through its officers, agents or employees, shall solicit, buy or take an assignment of, or be in any manner interested in buying or taking an assignment of a bond, promissory note, bill of exchange, book debt, or other thing in action, or any claim or demand, with the intent and for the purpose of bringing an action or proceeding thereon"
- `sources/REVIEW5A_NY_CASE_Justinian_Capital_v_WestLB_2016_CoA.txt`: "As pertinent here, the statute prohibits the purchase of notes, securities, or other instruments or claims with the intent and for the primary purpose of bringing a lawsuit (see id."

### R5A-04 (critical, gap) — S10 preconditions to recovering rent (public-assistance tenant)

Related rules: `NY:MDL-302-a(3)`, `NY:MDL-302(1)(b)`

**What is missing.** The rent-bar family (MDL 302, 302-a, 325) omits SSL 143-b(5): when the tenant was a public-assistance recipient, no money judgment for rent is available for any period during which a reported dangerous or hazardous violation was outstanding. This decides whether that part of a market-rate tenant's arrears can be kept from the deposit or sued for.

**Correct law, as a rule.** If the former tenant received public assistance with a shelter component during the period claimed, and the building had a violation of law relating to dangerous, hazardous or health-detrimental conditions reported to the social services department by the enforcing agency, then no money judgment for rent for any period while that violation was outstanding (until the date the condition was actually corrected, proved by the landlord) is available; that rent is not 'lawfully retained' from the deposit (GOL 7-108(1-a)(b)) and is not pursued. Rent for periods after correction, and damage claims, are unaffected; DSS may itself pay withheld rent after correction.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_SSL_143-B.txt`: "(b) In any such action or proceeding the plaintiff or landlord shall not be entitled to an order or judgment awarding him possession of the premises or providing for removal of the tenant, or to a money judgment against the tenant, on the basis of non-payment of rent for any period during which there was outstanding any violation of law relating to dangerous or hazardous conditions or conditions detrimental to life or health."

### R5A-05 (critical, partial) — S2 whether and how the tenancy ends (retaking possession) / S5 belongings

Related rules: `NY:COMMONLAW-belongings-abandonment`, `NYC:ABANDONED-city-layer`

**What is missing.** The belongings rules state the abandonment standard for disposal but not the unlawful-eviction statutes that govern retaking the unit when the tenant has not clearly surrendered. RPAPL 768 and Admin. Code 26-521 make it unlawful to evict an occupant of 30+ days (or with a lease) other than by warrant, including by removing possessions, removing the door or changing the lock; each violation is a class A misdemeanor and a $1,000-$10,000 civil penalty (city and state), and RPAPL 853 gives treble damages. The NYC 'ABANDONED-city-layer' rule states there is no city law on a departing tenant's belongings, which is correct only after surrender or abandonment; before it, 26-521 applies.

**Correct law, as a rule.** Branch (a) tenant surrendered possession (returned keys or otherwise unequivocally gave up occupancy) or abandoned the unit: the landlord may re-enter and change locks; belongings follow the abandonment standard. Branch (b) no surrender or abandonment is established (occupant of 30+ days or with a lease, belongings present, keys not returned, no unequivocal relinquishment): the landlord may not change the lock, remove possessions or otherwise exclude the occupant without a warrant or court order; doing so is unlawful eviction (RPAPL 768; Admin. Code 26-521) punishable as a class A misdemeanor and by a civil penalty of $1,000-$10,000 per violation, with a duty to restore, and exposes the landlord to treble damages (RPAPL 853). Rent and the 14-day clock in branch (b) run from the actual vacatur established by surrender or by the warrant.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_RPAPL_768.txt`: "(b) Such person shall also be subject to a civil penalty of not less than one thousand nor more than ten thousand dollars for each violation."
- `sources/REVIEW5A_NY_RPAPL_853.txt`: "If a person is disseized, ejected, or put out of real property in a forcible or unlawful manner, or, after he has been put out, is held and kept out by force or by putting him in fear of personal violence or by unlawful means, he is entitled to recover treble damages in an action therefor against the wrong-doer."
- `sources/REVIEW5A_NYC_ADC_26-523.txt`: "Such person shall also be subject to a civil penalty of not less than one thousand nor more than ten thousand dollars for each violation."

### R5A-06 (critical, gap) — S13 collection conduct (calls and texts)

Related rules: `US:12CFR1006.14(b)(2)`, `NYC:RCNY6-5-77(e)(1)`

**What is missing.** No rule states the TCPA, which binds any caller (owner, manager, Handoff, agency), not only debt collectors. Calls or texts to a former tenant's cell phone using an artificial or prerecorded voice, or an autodialer, need the called party's prior express consent; consent may be revoked by any reasonable means; each violation carries $500 statutory damages, trebled to $1,500 if willful. After Duguid an 'autodialer' must use a random or sequential number generator, so ordinary texting platforms are outside the ATDS clause, but prerecorded/artificial voice calls are covered regardless.

**Correct law, as a rule.** Before placing a collection or settlement call to a cellular number with an artificial or prerecorded voice (including ringless or prerecorded voicemail) or with equipment that generates numbers randomly or sequentially: have the tenant's prior express consent; honor a revocation made by any reasonable means within a reasonable time not exceeding ten business days, without designating an exclusive revocation channel (47 CFR 64.1200(a)(10)); otherwise liability is actual damages or $500 per call, up to $1,500 per call if willful or knowing. Live, manually placed calls and texts not sent by an ATDS are outside 227(b)(1)(A) (Duguid) but remain subject to FDCPA/Reg F and DCWP frequency limits where those apply.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_US_47USC_227_TCPA.txt`: "or (iii) to any telephone number assigned to a paging service, cellular telephone service, specialized mobile radio service, or other radio common carrier service, or any service for which the called party is charged for the call, unless such call is made solely to collect a debt owed to or guaranteed by the United States;"
- `sources/REVIEW5A_US_47CFR_64.1200.txt`: "(10) A called party may revoke prior express consent, including prior express written consent, to receive calls or text messages made pursuant to paragraphs (a)(1) through (3) and (c)(2) of this section by using any reasonable method to clearly express a desire not to receive further calls or text messages from the caller or sender."
- `sources/REVIEW5A_US_CASE_Facebook_v_Duguid_2021_SCOTUS.txt`: "” The TCPA defines such “autodialers” as equipment with the capacity both “to store or produce telephone numbers to be called, us- ing a random or sequential number generator,” and to dial those num- bers."
- `sources/REVIEW5A_US_47CFR_64.1200.txt`: "All requests to revoke prior express consent or prior express written consent made in any reasonable manner must be honored within a reasonable time not to exceed ten business days from receipt of such request."
- `sources/REVIEW5A_US_47USC_227_TCPA.txt`: "(B) an action to recover for actual monetary loss from such a violation, or to receive $500 in damages for each such violation, whichever is greater"

### R5A-07 (critical, gap) — S9 settling with one co-tenant

Related rules: `NY:ADJ-cotenants-payee`, `NY:ADJ-cotenants-vacated`

**What is missing.** The co-tenant rules decide who receives the refund but not what happens to the claim against the others when the landlord settles with or releases one co-tenant. GOL 15-104/15-105 fix the amount: a release with express reservation of rights preserves the claim against co-tenants (reduced by what was paid); a release without reservation satisfies the claim against the others to the released tenant's share.

**Correct law, as a rule.** When the landlord (or its collector) releases or settles with one of several jointly liable tenants or a guarantor: (a) if the release expressly reserves rights against the others, they stay liable for the balance less the amount paid and less the released obligor's share only to the extent 15-104 provides; (b) if it contains no express reservation, the claim against each other co-obligor is satisfied to the amount the landlord knew or had reason to know the released one was bound (as between them) to pay, or, without such knowledge, to the lesser of the released obligor's fractional share or the amount it was bound to pay. Every settlement with one co-tenant must say whether rights against the others are reserved.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_GOL_15-104.txt`: "Section 15-104 Discharge of one obligor, with reservations Subject to the provisions of section 15-103, the obligee’s release or discharge of one or more of several obligors, or of one or more of joint, or of joint and several obligors shall not discharge co-obligors, against whom the obligee in writing and as part of the same transaction as the release or discharge, expressly reserves his rights; and in the absence of such a reservation of rights shall discharge co-obligors only to the extent provided in section 15-105."
- `sources/REVIEW5A_NY_GOL_15-105.txt`: "1. If an obligee releasing or discharging an obligor without express reservation of rights against a co-obligor, then knows or has reason to know that the obligor released or discharged did not pay so much of the claim as he was bound by his contract or relation with that co-obligor to pay, the obligee’s claim against that co-obligor shall be satisfied to the amount which the obligee knew or had reason to know that the released or discharged obligor was bound to such co-obligor to pay. 2. If an obligee so releasing or discharging an obligor has not then such knowledge or reason to know, the obligee’s claim against the co-obligor shall be satisfied to the extent of the lesser of two amounts,  [...]"

### R5A-08 (critical, gap) — S9 partial payment tendered as full satisfaction

**What is missing.** No rule addresses a former tenant's check or payment marked 'payment in full' for less than the balance. In New York, UCC 1-308 (formerly 1-207) lets the creditor accept it under an explicit reservation of rights without an accord and satisfaction (Horn Waterproofing, Court of Appeals 1985). Without the reservation, depositing a check tendered in full settlement of a disputed balance completes an accord and satisfaction and extinguishes the rest.

**Correct law, as a rule.** If a former tenant tenders less than the claimed balance on the condition that it be accepted in full satisfaction: (a) accepting it with an explicit reservation of rights ('without prejudice', 'under protest' or like words, e.g., endorsed on the check or stated in writing at acceptance) preserves the claim to the remainder (UCC 1-308; Horn Waterproofing); (b) accepting it without reservation, where the balance was disputed, discharges the remainder by accord and satisfaction. A written promise to accept a stated performance in future satisfaction is an enforceable executory accord (GOL 15-501).

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_UCC_1-308.txt`: "A party that with explicit reservation of rights performs or promises performance or assents to performance in a manner demanded or offered by the other party does not thereby prejudice the rights reserved. Such words as “without prejudice,” “under protest,” or the like are sufficient."
- `sources/REVIEW5A_NY_CASE_Horn_Waterproofing_v_Bushwick_1985_CoA.txt`: "Uniform Commercial Code § 1-207 changed the law of accord and satisfaction in the case of a party who indorses a full payment check under protest."
- `sources/REVIEW5A_NY_GOL_15-501.txt`: "2. An executory accord shall not be denied effect as a defense or as the basis of an action or counterclaim by reason of the fact that the satisfaction or discharge of the claim, cause of action, contract, obligation, lease, mortgage or other security interest which is the subject of the accord was to occur at a time after the makin"

### R5A-09 (critical, gap) — S5 charges (electricity billed by the landlord)

Related rules: `NY:GOL-7-108(1-a)(b)-refundable`, `NY:RPL-235-a`

**What is missing.** GOL 7-108(1-a)(b) lets the landlord keep unpaid 'utility charges payable directly to the landlord under the lease'. Whether an electricity charge is lawful at all turns on the PSC's residential submetering rule, which no rule states: submetered electric service to residential units is lawful only if authorized by PSC order and consistent with 16 NYCRR Part 96.

**Correct law, as a rule.** Electricity billed by the landlord to a market-rate NYC tenant through submeters may be charged, retained from the deposit or pursued only if the building's submetering is and continues to be authorized by PSC order (where one was required) and consistent with the order and Part 96; otherwise the electricity charge is not a lawful charge and is not retained. Utility charges for services the landlord does not provide through authorized submetering (e.g., a flat 'utility fee') are fees, not lawful utility charges (see NY:ADJ-no-fee-retention).

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_16NYCRR_96.2.txt`: "(1) Electric service shall only be provided to a multi-unit residential premises in which individual dwelling units in the premises receive submetered electric service if the submetering (i) is and continues to be authorized by commission order where a commission order was necessary"

*Earlier rounds:* Round 2 considered PSC submetering and left it out ('no utility charge fact pattern in scope'). 5A rejects that exclusion: GOL 7-108(1-a)(b) itself makes lease utility charges payable to the landlord a retainable head, so whether such a charge is lawful is in scope.

### R5A-10 (critical, gap) — S15 bankruptcy (claim deadline)

Related rules: `US:11USC362(a)(6)`, `US:11USC502(b)(6)-lessor-cap`, `US:11USC542-refund-payee`

**What is missing.** The bankruptcy rules state the stay, setoff, the payee and the 502(b)(6) cap, but not the deadline to file a proof of claim. In chapter 7 and chapter 13 cases a claim is timely only within 70 days after the order for relief (with listed exceptions); a late claim is disallowed on objection in chapter 13 and subordinated in chapter 7.

**Correct law, as a rule.** If a former tenant files a voluntary chapter 7, 12 or 13 petition while a balance is owed (or its deposit is being held), the landlord's proof of claim (net of the deposit, subject to 502(b)(6) and 553) must be filed within 70 days after the order for relief or conversion (90 days in an involuntary chapter 7), subject to Rule 3002(c)'s listed exceptions. A claim not timely filed is disallowed (11 USC 502(b)(9)) except to the extent tardy filing is permitted by 726(a)(1)-(3) or the Rules; the debt is still subject to discharge.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_US_FRBP_3002.txt`: "In a voluntary Chapter 7 case or in a Chapter 12 or 13 case, the proof of claim is timely if filed within 70 days after the order for relief or entry of an order converting the case to Chapter 12 or 13."
- `sources/REVIEW4A_US_11USC_502_uscode.txt`: "(9) proof of such claim is not timely filed, except to the extent tardily filed as permitted under paragraph (1), (2), or (3) of section 726(a) or under the Federal Rules of Bankruptcy Procedure"

### R5A-11 (critical, gap) — S2 when rent stops after a summary proceeding / S9 balance

Related rules: `NY:RPL-220`, `NY:RPL-232-c`

**What is missing.** No rule states what the landlord may still recover after a holdover or nonpayment judgment. RPAPL 749(3) (as amended 2019) lets the petitioner recover by separate action any sum payable when the proceeding began and the reasonable value of use and occupancy up to the warrant for periods the agreement does not cover; RPAPL 741(5) lets the petition itself seek use and occupancy only if the notice of petition demanded it.

**Correct law, as a rule.** Where a summary proceeding preceded the move-out: amounts not awarded in the judgment that were payable when the proceeding was commenced, and the reasonable value of use and occupancy to the date the warrant issued (for periods without a rent term), may be pursued by separate action; use and occupancy is recoverable in the proceeding only if the notice of petition contained the demand. After the warrant, charges accrue only as use and occupancy for any continued occupation.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_RPAPL_749.txt`: "Petitioner may recover by action any sum of money which was payable at the time when the special proceeding was commenced and the reasonable value of the use and occupation to the time when the warrant was issued, for any period of time with respect to which the agreement does not make any provision for payment of rent."
- `sources/REVIEW5A_NY_RPAPL_741.txt`: "5. State the relief sought. The relief may include a judgment for rent due, and for a period of occupancy during which no rent is due, for the fair value of use and occupancy of the premises if the notice of petition contains a notice that a demand for such a judgment has been made."

### R5A-12 (critical, gap) — S5 credits

Related rules: `NY:RPL-235-a`

**What is missing.** RPL 235-a (utility offset) is stated but MDL 302-c is not: in a multiple dwelling with an oil-fired heating plant the owner fails to supply, tenants who buy oil following the statute's steps may deduct the payment from rent. The account must credit it.

**Correct law, as a rule.** If during the tenancy the owner failed to have heating oil supplied and the tenant (alone or with others) paid for delivery after substantially complying with 302-c's steps (reasonable efforts to reach the owner, etc.), the payment (allocated per the statute) is deductible from rent: credit it on the move-out account; rent claimed for those months is reduced by it.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_MDL_302-c.txt`: "Any payment so made shall be deductible from rent providing the following provisions have been substantially complied with by the tenant or someone acting on his behalf"

### R5A-13 (critical, gap) — S21 anti-discrimination (who is liable)

Related rules: `US:24CFR100.65-terms`, `NY:EXEC-296(5)(a)(2)-terms`, `NYC:ADC-8-107(5)(a)-terms`

**What is missing.** The anti-discrimination rules bind owners and agents but do not state HUD's liability rule: a person is directly liable for its own discriminatory practices and for failing to correct an agent's or employee's discrimination it knew of, and vicariously liable for its agents' and employees' discriminatory practices regardless of knowledge. 42 USC 3617 separately bars coercion, intimidation, threats or interference (e.g., collection threats because the tenant asserted fair-housing rights).

**Correct law, as a rule.** Owner and manager are each liable under the Fair Housing Act for discriminatory charges, deductions or collection conduct by their agents or employees (including Handoff or a collection agency acting for them) on a vicarious basis, and directly for their own conduct and for failing to take prompt corrective action they had the power to take; collection conduct that coerces, intimidates, threatens or interferes with a tenant because of the exercise of fair-housing rights violates 3617.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_US_24CFR_100.7.txt`: "A person is vicariously liable for a discriminatory housing practice by the person's agent or employee, regardless of whether the person knew or should have known of the conduct that resulted in a discriminatory housing practice, consistent with agency law."
- `sources/REVIEW5A_US_42USC_3617.txt`: "Interference, coercion, or intimidation It shall be unlawful to coerce, intimidate, threaten, or interfere with any person in the exercise or enjoyment of, or on account of his having exercised or enjoyed, or on account of his having aided or encouraged any other person in the exercise or enjoyment of, any right granted or protected by section 3603, 3604, 3605, or 3606 of this title."

### R5A-14 (critical, gap) — S20 data (breach)

Related rules: `NY:GBL-899-bb-safeguards`, `NYC:ADC-26-3002(c)-moveout-data`

**What is missing.** GBL 899-bb (safeguards) is stated but not GBL 899-aa (breach notification). Any business owning or licensing computerized private information of NY residents (tenant SSN, account or driver's licence numbers held in the tenant file, including by a manager or Handoff) must notify affected residents of a breach in the most expedient time possible and within 30 days after discovery, and notify the AG, Department of State and State Police (and DFS for covered entities).

**Correct law, as a rule.** If a tenant's private information held by the owner, manager or Handoff is, or is reasonably believed to have been, accessed or acquired without authorization: notify each affected resident within 30 days after discovery (law-enforcement delay excepted), with the content 899-aa requires, and notify the state agencies it lists (a service provider holding data for the owner notifies the owner immediately). Failure exposes the business to AG civil penalties.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_GBL_899-AA.txt`: "The disclosure shall be made in the most expedient time possible and without unreasonable delay, provided that such notification shall be made within thirty days after the breach has been discovered, except for the legitimate needs of law enforcement, as provided in subdivision four of this section."

### R5A-15 (major, gap) — S2 non-renewal / tenancy end

Related rules: `NY:RPL-226-c(2)`, `NY:RPL-215`

**What is missing.** No rule states RPL 223-b. A notice to quit, non-renewal or action for possession within a year after a tenant's good-faith complaint to a governmental authority or to the landlord, or tenant-organization activity, raises a rebuttable presumption of retaliation; the landlord is liable for damages and fees. This conditions the 'notice that the tenancy is ending' for every market-rate unit (owner-occupied buildings of fewer than four units excepted).

**Correct law, as a rule.** Before serving a non-renewal notice or notice to quit on a tenant who, within the preceding year, made a good-faith complaint (to an agency or in writing to the landlord) about a violation or habitability, or joined a tenant group, record a non-retaliatory reason: in any proceeding the tenant's showing of such activity and the landlord's notice raises a rebuttable presumption of retaliation; a retaliating landlord is liable for damages, attorney's fees and costs, and may be enjoined. Exception: owner-occupied premises with fewer than four units.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_RPL_223-b.txt`: "5. In an action or proceeding instituted against a tenant of premises or a unit to which this section is applicable, a rebuttable presumption that the landlord is acting in retaliation shall be created if the tenant establishes that the landlord served a notice to quit, or instituted an action or proceeding to recover possession, or attempted to substantially alter the terms of the tenancy, within one year after: a."

### R5A-16 (major, gap) — S2 surrender / when rent stops

Related rules: `NY:CASE-Riverside-surrender-by-operation`, `NY:COMMONLAW-NYC-monthly-tenant-surrender`

**What is missing.** Surrender by operation of law is stated (Riverside) but not the writing requirement for a consensual early termination of a lease for more than one year (GOL 5-703(1)) or the no-oral-modification rule (GOL 15-301(1)). An oral 'you can leave early' agreement does not end a two-year lease or stop rent unless the parties' conduct amounts to surrender by operation of law.

**Correct law, as a rule.** An agreement ending a lease for a term over one year before its end is effective only if in a writing signed by the landlord (or its agent authorized in writing) or if a surrender by operation of law occurs (conduct of both parties inconsistent with the continuing tenancy, e.g., landlord's acceptance of keys as surrender and reletting for its own account). Where the lease bars oral modification, an unexecuted oral agreement to change its terms is unenforceable. Rent stops on the effective surrender date.

**Evidence (verbatim, saved sources).**
- `sources/SWEEP_NY_GOL_5-703_nysenate.txt`: "An estate or interest in real property, other than a lease for a term not exceeding one year, or any trust or power, over or concerning real property, or in any manner relating thereto, cannot be created, granted, assigned, surrendered or declared, unless by act or operation of law, or by a deed or conveyance in writing, subscribed by the person creating, granting, assigning, surrendering or declaring the same, or by his lawful agent, thereunto authorized by writing."
- `sources/REVIEW5A_NY_GOL_15-301.txt`: "1. A written agreement or other written instrument which contains a provision to the effect that it cannot be changed orally, cannot be changed by an executory agreement unless such executory agreement is in writing and signed by the party against whom enforcement of the change is sought or by his agent."

### R5A-17 (major, gap) — S11 limitations (extension agreements)

Related rules: `NY:GOL-17-101-acknowledgment`, `NY:CPLR-213(2)`

**What is missing.** GOL 17-101 (acknowledgment) is stated but not GOL 17-103: a post-accrual written promise to waive, extend or not plead the statute of limitations is effective for a new period measured from the promise; a lease clause waiving limitations made before accrual has no effect.

**Correct law, as a rule.** A payment plan or settlement letter signed by the former tenant after the balance accrued that promises not to plead limitations (or extends it) lets the landlord sue within the six-year period running from the date of the promise (or any shorter period stated). A lease term made before accrual that waives or extends limitations is ineffective.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_GOL_17-103.txt`: "1. A promise to waive, to extend, or not to plead the statute of limitation applicable to an action arising out of a contract express or implied in fact or in law, if made after the accrual of the cause of action and made, either with or without consideration, in a writing signed by the promisor or his agent is effective, according to its terms, to prevent interposition of the defense of the statute of limitation in an action or proceeding commenced within the time that would be applicable if the cause of action had arisen at the date of the promise, or within such shorter time as may be provided in the promise."

### R5A-18 (major, gap) — S10 capacity and who may appear

Related rules: `NY:CCA-1809(1)`, `NY:CCA-1801-A(a)-eligibility`, `NY:HANDOFF-broker-config-collects-rent`

**What is missing.** The rules decide which court part an entity may use but not who may appear. CPLR 321(a) requires a corporation or LLC owner to appear by attorney (outside the small/commercial claims provisions); Judiciary Law 495 bars a corporation (e.g., Handoff) from appearing as attorney for another or practising law, and Judiciary Law 478 bars non-lawyer individuals from appearing for another in a court of record. A manager or Handoff cannot file or appear in the owner's Civil Court action.

**Correct law, as a rule.** Suit on the balance: (a) owner is a natural person: may sue pro se or by attorney; (b) owner is a corporation, LLC or partnership: must appear by a licensed attorney, except that in the commercial claims part a corporation may appear by an authorized officer, director or employee of the corporation itself (CCA 1809-A(d)) — not by an outside manager or Handoff; (c) Handoff or a manager (entity) may prepare evidence for counsel but may not appear, sign pleadings as attorney, or hold out legal services for the owner (JUD 495; for its individual staff, JUD 478); violation is a misdemeanor and the papers are a nullity.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_CPLR_321.txt`: "A party, other than one specified in § 1201 (Representation of infant, incompetent person, or conservatee)section 1201 of this chapter, may prosecute or defend a civil action in person or by attorney, except that a corporation or voluntary association shall appear by attorney, except as otherwise provided in sections 1809 and 1809-A of the New York city civil court act, sections 1809 and 1809-A of the uniform district court act and sections 1809 and 1809-A of the uniform city court act, and except as otherwise provided in section 501 and section 1809 of the uniform justice court act."
- `sources/REVIEW5A_NY_JUD_495.txt`: "1. No corporation or voluntary association shall (a) practice or appear as an attorney-at-law for any person in any court in this state or before any judicial body, nor (b) make it a business to practice as an attorney-at-law, for any person, in any of said courts"
- `sources/REVIEW5A_NY_JUD_478.txt`: "It shall be unlawful for any natural person to practice or appear as an attorney-at-law or as an attorney and counselor-at-law for a person other than himself or herself in a court of record in this state"
- `sources/REVIEW4A_NY_CCA_1809-A_nysenate.txt`: "(d) A corporation may appear as a party in any action brought pursuant to this article by an attorney as well as by any authorized officer, director or employee of the corporation provided that the appearance by a non-lawyer on behalf of a corporation shall be deemed to constitute the requisite authority to bind the corporatio"

### R5A-19 (major, gap) — S10 capacity (assumed name)

Related rules: `NY:LLC-808(a)-foreign-authority`, `NY:BCL-1312(a)-foreign-authority`

**What is missing.** Capacity rules cover foreign LLCs/corporations and LLC publication but not GBL 130: an owner or manager doing business under an assumed name (the name on the lease, e.g., 'Maple Properties' when the entity is 'Maple 12 LLC') without a filed certificate cannot maintain an action on contracts made in that name until it files.

**Correct law, as a rule.** If the lease or collection correspondence was made in a name other than the owner's legal name, confirm a GBL 130 assumed-name certificate is on file before suing; if not, the action cannot be maintained until filed (filing cures; knowing failure is a misdemeanor).

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_GBL_130.txt`: "Any person or persons carrying on, conducting or transacting business as aforesaid who fails to comply with the provisions of this section shall be prohibited from maintaining any action or proceeding in any court in this state on any contract, account or transaction made in a name other than its real name until the certificate required by this section has been executed and filed in accordance with the provisions set forth herein."

### R5A-20 (major, gap) — S9 closing the account after judgment

**What is missing.** No rule states CPLR 5020. When a money judgment is fully satisfied, the judgment creditor must execute and file a satisfaction-piece and mail a copy to the debtor within ten days after filing; for a judgment under $5,000, failure or refusal within 20 days after full satisfaction subjects it to a $100 penalty recoverable by the debtor.

**Correct law, as a rule.** On full payment of a judgment against a former tenant: execute and file the satisfaction-piece with the clerk within 20 days after receiving full satisfaction and mail a copy to the debtor within ten days after filing; for judgments below $5,000 the penalty for failure is $100 recoverable by the debtor (larger judgments carry the further consequences 5020(c) states).

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_CPLR_5020.txt`: "(c) When a judgment for less than five thousand dollars is fully satisfied, if the person required to execute and file with the proper clerk pursuant to subdivisions (a) and (d) of this section fails or refuses to do so within twenty days after receiving full satisfaction, then the judgment creditor shall be subject to a penalty of one hundred dollars recoverable by the judgment debtor pursuant to § 7202 (Action by person aggrieved)section seventy-two hundred two of this chapter or article eighteen of either the New York City civil court act, uniform district court act or uniform city court act."

### R5A-21 (major, gap) — S9 pursue or write off (recovery value)

Related rules: `NY:CPLR-5004(a)-consumer-2pct`

**What is missing.** The decision to pursue a balance to judgment turns on what can be collected, but no rule states the enforcement limits: exempt bank-account amounts (CPLR 5205(l): $2,500 where exempt payments were direct-deposited in the prior 45 days; 5222(i) exempt amount), mandatory exemption notices with restraints (5222(e), 5222-a), income executions capped at 10% of gross income (5231(b)), and the 20-year presumption of payment (CPLR 211(b)).

**Correct law, as a rule.** Expected recovery on a judgment against a natural person is limited by: exempt funds in bank accounts (5205(l) and 5222(i)), income execution of no more than 10% of gross income subject to the minimum-wage floor (5231(b)), exemption notice and claim-form service with every restraining notice (5222(e); 5222-a), and the judgment's presumption of payment after 20 years (211(b)); the renewal action is available in the tenth year (5014).

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_CPLR_5205.txt`: "then two thousand five hundred dollars in the judgment debtor’s account is exempt from application to the satisfaction of a money judgment."
- `sources/REVIEW5A_NY_CPLR_5222.txt`: "Except where the provisions of § 5222-A (Service of notices and forms and procedure for claim of exemption)section fifty-two hundred twenty-two-a of this article are applicable, pursuant to subdivision (a) of such section, if a notice in the form prescribed in subdivision (e) of this section has not been given to the judgment debtor or obligor within a year before service of a restraining notice, a copy of the restraining notice together with the notice to judgment debtor or obligor shall be mailed by first class mail or personally delivered to each judgment debtor or obligor who is a natural person within four days of the service of the restraining notice."
- `sources/REVIEW5A_NY_CPLR_5231.txt`: "Where a judgment debtor is receiving or will receive money from any source, an income execution for installments therefrom of not more than ten percent thereof may be issued and delivered to the sheriff of the county in which the judgment debtor resides or, where the judgment debtor is a non-resident, the county in which he is employed;"
- `sources/REVIEW5A_NY_CPLR_211.txt`: "A money judgment is presumed to be paid and satisfied after the expiration of twenty years from the time when the party recovering it was first entitled to enforce it."

### R5A-22 (major, gap) — S20 data (closing the file)

Related rules: `NY:GBL-899-bb-safeguards`

**What is missing.** GBL 399-h governs how the tenant file is disposed of when the account closes: records containing personal identifying information may be disposed of only by shredding, destroying the information or making it unreadable. Not stated in the rules.

**Correct law, as a rule.** When the settlement file (applications, IDs, bank or card details, SSNs) is disposed of by the owner, manager or Handoff, shred it or destroy or render unreadable the personal identifying information (or use a method consistent with accepted industry practice reasonably believed to ensure no unauthorized access).

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_GBL_399-H.txt`: "shall dispose of a record containing personal identifying information unless the person, business, firm, partnership, association, or corporation, or other person under contract with the business, firm, partnership, association, or corporation does any of the following: a. shreds the record before the disposal of the record; or b. destroys the personal identifying information contained in the record; or c. modifies the record to make the personal identifying information unreadable"

### R5A-23 (major, gap) — S18 domestic violence (voucher tenant) / S2 tenancy end

Related rules: `US:24CFR982.313(d)`, `US:24CFR982.311(d)(1)`

**What is missing.** The HCV rules are stated but not VAWA (34 USC 12491), which covers tenant-based HCV tenancies in market-rate units: an owner may not terminate or deny tenancy because the tenant is a victim of domestic violence, dating violence, sexual assault or stalking, and may bifurcate the lease to remove the perpetrator while the victim stays.

**Correct law, as a rule.** HCV-assisted unit: criminal activity directly relating to domestic violence against the tenant is not cause to terminate the victim's tenancy; the owner may bifurcate the lease to evict the perpetrator; the victim's tenancy continues. Charges arising from the perpetrator's acts follow the lease and state law against the liable party.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_US_34USC_12491_VAWA.txt`: "(B) Bifurcation (i) In general Notwithstanding subparagraph (A), a public housing agency or owner or manager of housing assisted under a covered housing program may bifurcate a lease for the housing in order to evict, remove, or terminate assistance to any individual who is a tenant or lawful occupant of the housing and who engages in criminal activity directly relating to domestic violence, dating violence, sexual assault, or stalking against an affiliated individual or other individual, without evicting, removing, terminating assistance to, or otherwise penalizing a victim of such criminal activity who is also a tenant or lawful occupant of the housing."

### R5A-24 (major, gap) — S20 credit reporting (pulling a report for collection)

Related rules: `US:15USC1681s-2(a)(1)(A)`, `US:12CFR1006.30(a)`

**What is missing.** Furnishing duties are stated, but not the permissible purpose to obtain a former tenant's consumer report (FCRA 1681b(a)(3)(A): review or collection of the consumer's account) nor the seven-year reporting limit on collection accounts (1681c(a)(4), running from 180 days after delinquency, 1681c(c)).

**Correct law, as a rule.** The owner or its collector may obtain a former tenant's consumer report to locate or evaluate collection of that tenant's account (1681b(a)(3)(A)); obtaining it for another purpose is unlawful. A collection account may be reported by a CRA for seven years from 180 days after the delinquency began; the furnisher reports the date of first delinquency (1681s-2(a)(5)).

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_US_15USC_1681b.txt`: "(3) To a person which it has reason to believe- (A) intends to use the information in connection with a credit transaction involving the consumer on whom the information is to be furnished and involving the extension of credit to, or review or collection of an account of, the consumer;"
- `sources/REVIEW5A_US_15USC_1681c.txt`: "(4) Accounts placed for collection or charged to profit and loss which antedate the report by more than seven years."

### R5A-25 (minor, gap) — S2 non-renewal

Related rules: `NY:RPL-215`

**What is missing.** RPL 218 (waiver of Good Cause rights void) is not stated.

**Correct law, as a rule.** Any lease term waiving or modifying Good Cause rights is void.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_RPL_218.txt`: "Section 218 Waiver of rights void Any agreement by a tenant heretofore or hereinafter entered into in a written lease or other rental agreement waiving or modifying their rights as set forth in this article shall be void as contrary to public policy."

### R5A-26 (minor, gap) — S13 licensing (exposure)

Related rules: `NY:RPL-440(1)-rent-collection`

**What is missing.** RPL 441-c (DOS may revoke, suspend or fine a licensee for untrustworthiness or incompetency, e.g., mishandling deposits or collections) is not stated.

**Correct law, as a rule.** A licensed broker-manager's mishandling of tenant funds or collections exposes its licence to revocation, suspension or fine by DOS.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_RPL_441-c.txt`: "(a) The department of state may revoke the license of a real estate broker or salesperson or suspend the same, for such period as the department may deem proper, or in lieu thereof may impose a fine not exceeding two thousand dollars payable to the department of state, provided that fifty percent of all moneys received by the department of state for such fines shall be payable to the anti-discrimination in housing fund established pursuant to State Finance Law § 80-A (Anti-discrimination in housing fund)section eighty-a of the state finance law, or a reprimand upon conviction of the licensee of a violation of any provision of this article, or for a violation of subdivision four of § 442-H (R [...]"

### R5A-27 (minor, gap) — S18 domestic violence

Related rules: `NY:RPL-227-d-dv-status`

**What is missing.** RPAPL 744 (no removal because of domestic violence victim status) is not stated.

**Correct law, as a rule.** A tenant may not be removed from possession in a summary proceeding because of domestic violence victim status.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_RPAPL_744.txt`: "1. A tenant shall not be removed from possession of a residential unit pursuant to this article because of such person’s domestic violence victim status"

### R5A-28 (minor, gap) — S10 preconditions (pleading)

Related rules: `NY:MDL-325(2)`, `NYC:ADC-27-2107(b)-rent-stay`

**What is missing.** 22 NYCRR 208.42(g) (petition must allege multiple-dwelling registration status) is not stated.

**Correct law, as a rule.** Every RPAPL 711 petition alleges either that the premises are not a multiple dwelling or that a current HPD registration naming the managing agent is on file.

**Evidence (verbatim, saved sources).**
- `sources/SWEEP_NY_22NYCRR_208.42_LII.txt`: "In every summary proceeding brought to recover possession of real property pursuant to section 711 of the Real Property Actions and Proceedings Law, the petitioner shall allege either: (1) that the premises are not a multiple dwelling; or (2) that the premises are a multiple dwelling and, pursuant to the Administrative Code, sections 27-2097 _et seq.,_ there is a currently effective registration statement on file"

### R5A-29 (minor, gap) — S5 charges

Related rules: `NY:RPL-238-a(1)-no-move-in-fees`

**What is missing.** MDL 51-c (tenant's own lock; lease charge for it void) is not stated.

**Correct law, as a rule.** No charge may be made or kept for the tenant's installing its own additional lock; the tenant must give a duplicate key on request.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_MDL_51-c.txt`: "every provision of any lease hereafter made or entered into which reserves or provides for the payment by such tenant of any additional rent, bonus, fee or other charge or any other thing of value for the right or privilege of installing and/or maintaining any such lock, shall be deemed to be void as against public policy and wholly unenforceable"

### R5A-30 (minor, gap) — S11 tolling

Related rules: `US:11USC108(c)-extension`, `US:50USC3936-tolling`, `NY:CPLR-210-death`

**What is missing.** State tolling rules other than CPLR 210 are not stated: 204(a) (stays), 205(a) (six-month savings), 207 (absence), 208 (infancy/insanity of the claimant) and Military Law 308 (NY militia service).

**Correct law, as a rule.** Add to the limitations computation: time a court or statutory stay prevented suit is excluded (204(a)); a timely action dismissed other than on the merits/neglect/voluntary discontinuance/lack of jurisdiction may be recommenced within six months (205(a)); defendant's 4-month absence tolls only where personal jurisdiction could not otherwise be obtained (207); NY military service is excluded (MIL 308).

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_CPLR_204.txt`: "Where the commencement of an action has been stayed by a court or by statutory prohibition, the duration of the stay is not a part of the time within which the action must be commenced."
- `sources/REVIEW5A_NY_CPLR_205.txt`: "If an action is timely commenced and is terminated in any other manner than by a voluntary discontinuance, a failure to obtain personal jurisdiction over the defendant, a dismissal of the complaint for neglect to prosecute the action, or a final judgment upon the merits, the plaintiff, or, if the plaintiff dies, and the cause of action survives, his or her executor or administrator, may commence a new action upon the same transaction or occurrence or series of transactions or occurrences within six months after the termination provided that the new action would have been timely commenced at the time of commencement of the prior action and that service upon defendant is effected within such s [...]"
- `sources/REVIEW5A_NY_CPLR_207.txt`: "If, after a cause of action has accrued against a person, that person departs from the state and remains continuously absent therefrom for four months or more, or that person resides within the state under a false name which is unknown to the person entitled to commence the action, the time of his absence or residence within the state under such a false name is not a part of the time within which the action must be commenced."
- `sources/REVIEW5A_NY_CPLR_208.txt`: "Civil Practice Law & Rules Section 208 Infancy, insanity (a) If a person entitled to commence an action is under a disability because of infancy or insanity at the time the cause of action accrues, and the time otherwise limited for commencing the action is three years or more and expires no later than three years after the disability ceases, or the person under the disability dies, the time within which the action must be commenced shall be extended to three years after the disability ceases or the person under the disability dies, whichever event first occurs;"
- `sources/REVIEW4A_NY_MIL_308_nysenate.txt`: "The period of military service shall not be included in computing any period now or hereafter to be limited by any law, regulation or order for the bringing of any action or proceeding in any court, board, bureau, commission, department or other agency of government of this state or any of its governmental subdivisions by or against any person in military service, or by or against his heirs, executors, administrators, or assigns, whether such cause of action or the right or privilege to institute such an action or proceeding shall have accrued prior to or during the period of such service, nor shall any part of such period which occurs after the date of enactment of this act be included in c [...]"

### R5A-31 (minor, gap) — S10 procedure (incapacity, death)

Related rules: `NY:CPLR-3215(g)(3)`

**What is missing.** CPLR 1203 (no default against an infant or adjudicated incompetent without guardian), 1015 (substitution on death) and 5208 (execution after the debtor's death needs surrogate's leave) are not stated.

**Correct law, as a rule.** No default judgment against an infant or adjudicated incompetent unless its representative appeared or 20 days after a guardian ad litem's appointment; on a party's death, substitute the representative; after the judgment debtor's death, enforce only with surrogate's court leave.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_CPLR_1203.txt`: "Civil Practice Law & Rules Section 1203 Default judgment No judgment by default may be entered against an infant or a person judicially declared to be incompetent unless his representative appeared in the action or twenty days have expired since appointment of a guardian ad litem for him."
- `sources/REVIEW5A_NY_CPLR_1015.txt`: "If a party dies and the claim for or against him is not thereby extinguished the court shall order substitution of the proper parties."
- `sources/REVIEW5A_NY_CPLR_5208.txt`: "Civil Practice Law & Rules Section 5208 Enforcement after death of judgment debtor leave of court extension of lien Except where otherwise prescribed by law, after the death of a judgment debtor, an execution upon a money judgment shall not be levied upon any debt owed to him or any property in which he has an interest, nor shall any other enforcement procedure be undertaken with respect to such debt or property, except upon leave of the surrogate’s court which granted letters testamentary or letters of administration upon the estate."

### R5A-32 (minor, gap) — S8 settlement of a tenant's deposit suit

**What is missing.** CPLR 5003-a (settling defendant must pay within 21 days of tender of release and stipulation, else costs, interest and fees) is not stated.

**Correct law, as a rule.** When the landlord settles a tenant's deposit action, pay within 21 days after the tenant tenders the release and stipulation of discontinuance, or judgment may be entered for the settlement plus interest, costs and fees.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_CPLR_5003-A.txt`: "Civil Practice Law & Rules Section 5003-A Prompt payment following settlement (a) When an action to recover damages has been settled, any settling defendant, except those defendants to whom subdivisions (b) and (c) of this section apply, shall pay all sums due to any settling plaintiff within twenty-one days of tender, by the settling plaintiff to the settling defendant, of a duly executed release and a stipulation discontinuing action executed on behalf of the settling plaintiff."

### R5A-33 (minor, gap) — S13 collection scope

Related rules: `NY:GBL-600(1)`, `NY:23NYCRR-1.1(d)-not-lease`

**What is missing.** GBL art. 29-HH (identity-theft cease-collection, 604-a) is not addressed; like art. 29-H it reaches only consumer claims arising from credit, so it does not govern a lease balance. GBL 399-ddd (no SSN on mailed materials) is not stated.

**Correct law, as a rule.** GBL 604-a does not apply to a residential lease balance (no credit extended). Do not print the tenant's SSN on any mailed statement or collection letter (399-ddd).

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_GBL_604-A.txt`: "1. Upon receipt from a debtor of the following, a principal creditor shall cease collection activities until completion of the review provided in subdivision five of this section"
- `sources/REVIEW5A_NY_GBL_399-DDD.txt`: "(e) Print an individual’s social security account number on any materials that are mailed to the individual, unless state or federal law requires the social security account number to be on the document to be mailed."

### R5A-34 (minor, gap) — S14 unclaimed funds

Related rules: `NY:ABP-1315(2)`, `NY:ABP-1422`

**What is missing.** ABP 1400 (limitations no bar to reporting), 1412 ($100/day forfeiture for wilful failure to report; interest) and 1412-a (keep records five years after the report year) are not stated.

**Correct law, as a rule.** Report and pay unclaimed refunds even if the tenant's claim is time-barred; keep supporting records five years after the report year; wilful failure to report forfeits $100 per day, and late-paid property bears interest at 10% per annum.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_ABP_1400.txt`: "Abandoned Property Law Section 1400 Statutes of limitations not a bar The expiration of any period of time specified by law, during which an action or proceeding may be commenced or enforced to secure payment of a claim for money or recovery of property, shall not prevent any such money or property from being deemed abandoned property, nor affect any duty to file a report required by this chapter or to pay or deliver to the state comptroller any such abandoned property;"
- `sources/REVIEW5A_NY_ABP_1412.txt`: "Abandoned Property Law Section 1412 Penalty, interest and special proceedings 1 Any person wilfully failing to make any full and complete report or to file any affidavit required by this chapter shall forfeit to the people of the state the sum of one hundred dollars for each day such report or affidavit shall be wilfully delayed or withheld, except that the state comptroller may extend the time for making any such report or filing any such affidavit and may waive the payment of any penalty or part thereof provided for by this subdivision."
- `sources/REVIEW5A_NY_ABP_1412-A.txt`: "Except as provided in § 513-A (Retention of books and records)section five hundred thirteen-a of this chapter, every person, co-partnership, unincorporated association or corporation required to file a report of abandoned property pursuant to this chapter, shall retain for a period of five years following the thirty-first day of December of the year for which such report has been filed, all books, records and documents necessary to establish the accuracy and completeness of such report."

### R5A-35 (minor, gap) — S17 military

Related rules: `US:50USC3951(a)(1)(B)`, `NY:MIL-310(2)`

**What is missing.** NY Military Law 309 (no eviction or distress against a person in military service without court leave) and 306 (discretionary stay of actions up to 60 days after service) are not stated.

**Correct law, as a rule.** Eviction or distress against a NY military-service tenant or dependents needs court leave (MIL 309); actions against them may be stayed during service and for 60 days after (MIL 306).

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_MIL_309.txt`: "No eviction or distress shall be made during the period of military service in respect of any premises occupied chiefly for dwelling purposes by a person in military service or the spouse, children, or other dependents of a person in military service, except upon leave of court granted upon application therefor or granted in any action or proceeding affecting the right of possession."
- `sources/REVIEW5A_NY_MIL_306.txt`: "In any action or proceeding commenced in any court or in any adjudicatory or licensing proceeding before any state agency, including any public benefit corporation or public authority, or any political subdivision of the state, against a person in military service: before or during the period of such service, or within sixty days thereafter"

### R5A-36 (minor, gap) — S21 exposure

Related rules: `NY:EXEC-296(5)(a)(2)-terms`

**What is missing.** Executive Law 297(9) remedies (court action for damages, including punitive damages in housing cases) are not stated.

**Correct law, as a rule.** A tenant subjected to discriminatory charges or collection may sue for compensatory and punitive damages and fees.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_EXC_297.txt`: "(iv) awarding of punitive damages, in cases of employment discrimination related to private employers, and, in cases of housing discrimination, with damages in housing discrimination cases in an amount not to exceed ten thousand dollars, to the person aggrieved by such practice;"

### R5A-37 (minor, gap) — S20 tenant data

Related rules: `NYC:ADC-26-3002(c)-moveout-data`

**What is missing.** Admin. Code 26-3003(a)(1) (no sale or disclosure of smart-access data except as listed) and 26-3006 (private action for unlawful sale) are not stated.

**Correct law, as a rule.** Smart-access data of a departed tenant may not be sold or disclosed (e.g., to a collector) except as 26-3003 allows; unlawful sale is actionable by occupants.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NYC_ADC_26-3003.txt`: "1. sell, lease or otherwise disclose such data to another person except:"
- `sources/REVIEW5A_NYC_ADC_26-3006.txt`: "a. A lawful occupant of a dwelling unit, or a group of such occupants, in a smart access building may bring an action alleging an unlawful sale of data"

### R5A-38 (minor, gap) — S19 tax

Related rules: `US:26USC6050P-no-1099C`, `US:IRS-Pub527-deposit-income`

**What is missing.** IRC 6041's threshold (now $2,000 under Pub. L. 119-21) and Treas. Reg. 1.166-1(e) (unpaid rent deductible as bad debt only if previously included in income) are not stated.

**Correct law, as a rule.** Writing off a lease balance yields a bad-debt deduction only for rent the owner previously reported as income (accrual basis); a cash-basis owner has none. No 1099 is due for returning a tenant's own deposit.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_US_26USC_6041.txt`: "of $2,000 or more in any calendar year"
- `sources/REVIEW5A_US_26CFR_1.166-1.txt`: "(e) Prior inclusion in income required. Worthless debts arising from unpaid wages, salaries, fees, rents, and similar items of taxable income shall not be allowed as a deduction under section 166 unless the income such items represent has been included in the return of income"

### R5A-39 (minor, gap) — S1 lease form / S10 predicate notices

Related rules: `NY:RPL-214`, `NY:RPL-215`

**What is missing.** RPL 231-c (Good Cause notice in leases) and its RPAPL 741(5-a) consequence (petition must append it) are not stated.

**Correct law, as a rule.** Covered leases and renewals carry the 231-c notice; a summary-proceeding petition must append or incorporate it.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_RPAPL_741.txt`: "5-a. Append or incorporate the notice required pursuant to Real Property Law § 231-C"

*Earlier rounds:* Round 1 noted RPL 231-c only as listed out of scope in the NY coverage table; no round stated its predicate-notice and petition consequence (RPAPL 741(5-a)).

### R5A-40 (minor, gap) — S1 lease form

Related rules: `NY:GOL-5-905`

**What is missing.** GOL 5-702 (plain language) is not stated: violation gives actual damages plus $50 but does not void the lease or supply a defense.

**Correct law, as a rule.** A non-plain-language residential lease remains enforceable; the tenant may recover actual damages plus $50.

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_GOL_5-702.txt`: "b. A violation of the provisions of subdivision a of this section shall not render any such agreement void or voidable nor shall it constitute: 1. A defense to any action or proceeding to enforce such agreement; or 2. A defense to any action or proceeding for breach of such agreement."

### R5A-41 (minor, gap) — S0 routing (pending)

Related rules: `NYC:RS-status`, `NYC:RSC-2520.11(p)`

**What is missing.** S9650/A659 (passed both houses 2026, not delivered) would penalize incorrect decontrol statements in 421-a (Affordable New York) leases; not recorded as a dated future rule.

**Correct law, as a rule.** Pending: if signed, from its 60th day, leases/renewals of 421-a units with incorrect decontrol information carry a $1,000 violation; routing is unchanged (421-a units remain stabilized and outside this engine).

**Evidence (verbatim, saved sources).**
- `sources/REVIEW5A_NY_A00659_Assembly_2025-26.txt`: ": Summary Actions Committee Votes Floor Votes Memo Text LFIN Chamber Video/Transcript A00659 Summary: BILL NOA00659 SAME ASSAME AS S09650 SPONSORRosenthal COSPNSRTaylor, Simone, Levenberg, Burdick, Wright, Simon MLTSPNSR Amd §421-a, RPT L Prohibits landlords from including incorrect information relating to rent decontrol in certain leases and renewals thereof;"

## Over-scope

- `NYC:RCNY28-1-01`, `NYC:RCNY28-1-12(b)-cap`, `NYC:RCNY28-1-12(b)-escrow`, `NYC:HPD-ESCROW-no-owner-draw`, `NYC:HPD-ESCROW-regulatory-agreement` (minor): 28 RCNY ch. 1 applies to multiple dwellings with a PHFL article VIII city loan; the rule files' own NYC:RCL-26-403(e)(1)(c) states every unit in such a building is rent-controlled while article VIII requires it, and HPD regulatory agreements attach regulated rents. A unit reached by these rules is routed out of the market-rate engine at Step 0, so for a market-rate unit they change no decision; they belong with the controlled/regulated review (defer, do not cite as market-rate law).

No other in-scope rule was found that corresponds to nothing in the universe and changes no decision; the public-housing and project-based HUD rules are already deferred in the walk.

## Universe coverage table

| 5A id | Citation | Status in rule files | Rules | In 4A |
|---|---|---|---|---|
| U5A-001 | GOL 7-108(1) | covered | `NY:GOL-7-108(1)` | U001 |
| U5A-002 | GOL 7-108(1-a) preamble | covered | `NY:GOL-7-108(1-a)-exclusions` | U002 |
| U5A-003 | GOL 7-108(1-a)(a) | covered | `NY:GOL-7-108(1-a)(a)` `NY:GOL-7-108(4)` `NY:GOL-7-108(6)` | U005 |
| U5A-004 | GOL 7-108(1-a)(b) | covered | `NY:GOL-7-108(1-a)(b)-refundable` `NY:GOL-7-108(1-a)(b)-excluded-costs` | U060 |
| U5A-005 | GOL 7-108(1-a)(c) | covered | `NY:GOL-7-108(1-a)(c)-offer` `NY:GOL-7-108(1-a)(c)-bar` | U006 |
| U5A-006 | GOL 7-108(1-a)(d) | covered | `NY:GOL-7-108(1-a)(d)-notice` `NY:GOL-7-108(1-a)(d)-inspection` | U061 |
| U5A-007 | GOL 7-108(1-a)(e) | partial:R5A-01 | `NY:GOL-7-108(1-a)(e)` `NY:GOL-7-108(1-a)(e)-forfeiture` | U080 |
| U5A-008 | GOL 7-108(1-a)(f) | covered | `NY:GOL-7-108(1-a)(f)` | U062 |
| U5A-009 | GOL 7-108(1-a)(g) | covered | `NY:GOL-7-108(1-a)(g)` | U085 |
| U5A-010 | GOL 7-108(2) | covered | `NY:GOL-7-108(2)(a)` `NY:GOL-7-108(2)(b)` `NY:GOL-7-108(2)(c)` | U041 |
| U5A-011 | GOL 7-103(1) | covered | `NY:GOL-7-103(1)-trust` | U007 |
| U5A-012 | GOL 7-103(2) | covered | `NY:GOL-7-103(2)-bank-notice` `NY:GOL-7-103(2)-admin-fee` `NY:GOL-7-103(2)-interest-owed` | U008 U009 |
| U5A-013 | GOL 7-103(2-a) | covered | `NY:GOL-7-103(2-a)` | U010 |
| U5A-014 | GOL 7-103(2-b) | covered | `NY:GOL-7-103(2-b)` | U057 |
| U5A-015 | GOL 7-103(3) | covered | `NY:GOL-7-103(3)` | U011 |
| U5A-016 | GOL 7-105 | covered | `NY:GOL-7-105(1)` `NY:GOL-7-105(2)-transfer-effect` | U040 |
| U5A-017 | GOL 5-328 as amended by L.2025 c.431 | covered | `NY:GOL-5-328(3)(b)` `NY:RPL-238-a(2-a)` | U064 |
| U5A-018 | GOL 5-905 | covered | `NY:GOL-5-905` | U016 |
| U5A-019 | GOL 5-703(1) | gap:R5A-16 |  | - |
| U5A-020 | GOL 5-701(a)(1)-(2) | covered | `NY:GOL-5-701(a)(2)-guaranty` | U100 |
| U5A-021 | GOL 15-104 | gap:R5A-07 |  | - |
| U5A-022 | GOL 15-105 | gap:R5A-07 |  | - |
| U5A-023 | GOL 15-301(1) | gap:R5A-16 |  | - |
| U5A-024 | GOL 15-501 | gap:R5A-08 |  | - |
| U5A-025 | UCC 1-308 | gap:R5A-08 |  | - |
| U5A-026 | Horn Waterproofing Corp. v Bushwick Iron & Steel Co., 66 NY2d 321 (1985) | gap:R5A-08 |  | - |
| U5A-027 | GOL 17-101 | covered | `NY:GOL-17-101-acknowledgment` | U107 |
| U5A-028 | GOL 17-103 | gap:R5A-17 |  | - |
| U5A-029 | GOL 5-702 | gap:R5A-40 |  | - |
| U5A-030 | RPL 220 | covered | `NY:RPL-220` | - |
| U5A-031 | RPL 223 | covered | `NY:RPL-223` | U042 |
| U5A-032 | RPL 223-b(5) | gap:R5A-15 |  | - |
| U5A-033 | RPL 226-b | covered | `NY:RPL-226-b(1)` `NY:RPL-226-b(2)` `NY:RPL-226-b(3)` | U028 U029 |
| U5A-034 | RPL 226-c | covered | `NY:RPL-226-c(1)(a)` `NY:RPL-226-c(2)` | U020 |
| U5A-035 | RPL 227 | covered | `NY:RPL-227` | U030 |
| U5A-036 | RPL 227-a | covered | `NY:RPL-227-a(1)` `NY:RPL-227-a(2)` | U031 |
| U5A-037 | RPL 227-c | covered | `NY:RPL-227-c(1)` `NY:RPL-227-c(2)` | U032 |
| U5A-038 | RPL 227-d | covered | `NY:RPL-227-d-dv-status` | U166 |
| U5A-039 | RPL 227-e | covered | `NY:RPL-227-e` `NY:RPL-227-e-waiver` | U022 |
| U5A-040 | RPL 228 | covered | `NY:RPL-228` | - |
| U5A-041 | RPL 229 | covered | `NY:RPL-229` | U021 |
| U5A-042 | RPL 232 | covered | `NY:RPL-232` `NY:ADJ-RPL-232-monthly-letting` | - |
| U5A-043 | RPL 232-a | covered | `NY:RPL-232-a` | U019 |
| U5A-044 | RPL 232-c | covered | `NY:RPL-232-c` | U018 |
| U5A-045 | RPL 234 | covered | `NY:RPL-234` | U066 |
| U5A-046 | RPL 234-a | covered | `NY:RPL-234-a` | U068 |
| U5A-047 | RPL 235-b | covered | `NY:RPL-235-b` | U070 |
| U5A-048 | RPL 235-c | covered | `NY:RPL-235-c` | - |
| U5A-049 | RPL 235-e(d) | no-decision-change | RPL 235-e(d) supplies only a defense in a nonpayment proceeding against a tenant in possession (agreeing with round 2's exclusion); it decides nothing after the tenancy ends. | - |
| U5A-050 | RPL 235-f | covered | `NY:RPL-235-f` | - |
| U5A-051 | RPL 235-g | covered | `NY:RPL-235-g` | U065 |
| U5A-052 | RPL 235-i | covered | `NY:RPL-235-i` | U069 |
| U5A-053 | RPL 236 | covered | `NY:RPL-236` | U033 |
| U5A-054 | RPL 236-a | covered | `NY:RPL-236-a` | U034 U035 |
| U5A-055 | RPL 238-a(1)(a) | covered | `NY:RPL-238-a(1)-no-move-in-fees` | U013 |
| U5A-056 | RPL 238-a(2) | covered | `NY:RPL-238-a(2)` | U063 |
| U5A-057 | RPL 211 (Good Cause definitions) | covered | `NY:RPL-211(3)-small-landlord` | - |
| U5A-058 | RPL 214 | covered | `NY:RPL-214` `NY:RPL-214(15)-high-rent` | U003 |
| U5A-059 | RPL 215-216 | covered | `NY:RPL-215` | U004 |
| U5A-060 | RPL 218 | gap:R5A-25 |  | - |
| U5A-061 | RPL 440-a / 440(1) | covered | `NY:RPL-440(1)-rent-collection` | U043 |
| U5A-062 | RPL 442-d | covered | `NY:RPL-442-d-442-e-unlicensed` | U044 |
| U5A-063 | RPL 441-c | gap:R5A-26 |  | - |
| U5A-064 | RPAPL 702 | covered | `NY:ADJ-no-fee-retention` | - |
| U5A-065 | RPAPL 711(2) | no-decision-change | RPAPL 711(2) governs a nonpayment proceeding against a tenant in possession; it changes no settlement decision after the tenancy ends. | - |
| U5A-066 | RPAPL 744 | gap:R5A-27 |  | - |
| U5A-067 | RPAPL 749(3) | gap:R5A-11 |  | - |
| U5A-068 | RPAPL 768 | partial:R5A-05 |  | - |
| U5A-069 | RPAPL 853 | partial:R5A-05 |  | - |
| U5A-070 | RPAPL 769-778 (art. 7-A) | covered | `NY:RPAPL-776-778-administrator` | U052 |
| U5A-071 | RPAPL 1305 | covered | `NY:RPAPL-1305-successor` | U038 |
| U5A-072 | 22 NYCRR 208.42(g) | gap:R5A-28 |  | - |
| U5A-073 | MDL 4(7) | covered | `NY:MDL-4(7)-multiple-dwelling` | - |
| U5A-074 | MDL 301-302(1)(b) | covered | `NY:MDL-301(1)` `NY:MDL-302(1)(b)` | U049 U050 |
| U5A-075 | MDL 302-a | covered | `NY:MDL-302-a(3)` | U051 |
| U5A-076 | MDL 302-c | gap:R5A-12 |  | - |
| U5A-077 | MDL 325(2) | covered | `NY:MDL-325(2)` | U047 |
| U5A-078 | MDL 51-c | gap:R5A-29 |  | - |
| U5A-079 | CPLR 105(f),(u) | covered | `NY:ADJ-lease-balance-not-consumer-credit` | U104 |
| U5A-080 | CPLR 203 | covered | `NY:ADJ-tenant-deposit-claim-limitations` | U106 |
| U5A-081 | CPLR 204(a) | gap:R5A-30 |  | - |
| U5A-082 | CPLR 205(a) | gap:R5A-30 |  | - |
| U5A-083 | CPLR 207 | gap:R5A-30 |  | - |
| U5A-084 | CPLR 208 | gap:R5A-30 |  | - |
| U5A-085 | CPLR 210(b) | covered | `NY:CPLR-210-death` | U108 |
| U5A-086 | CPLR 211(b) | gap:R5A-21 |  | - |
| U5A-087 | CPLR 213(2) | covered | `NY:CPLR-213(2)` | U102 |
| U5A-088 | CPLR 214(4) | no-decision-change | A landlord's claim for damage to the unit is on the lease (six years, CPLR 213(2)); the three-year tort period never shortens it. | - |
| U5A-089 | CPLR 214-i | covered | `NY:CPLR-214-i` | U103 |
| U5A-090 | CPLR 321(a) | gap:R5A-18 |  | - |
| U5A-091 | CPLR 1201, 1203 | gap:R5A-31 |  | - |
| U5A-092 | CPLR 1015 | gap:R5A-31 |  | - |
| U5A-093 | CPLR 3015(e) | covered | `NY:CPLR-3015(e)-licence-pleading` | U097 |
| U5A-094 | CPLR 3012 | no-decision-change | CPLR 3012 answer timing does not change the landlord's decision. | - |
| U5A-095 | CPLR 3215(g)(3) | covered | `NY:CPLR-3215(g)(3)` | U094 |
| U5A-096 | CPLR 4544 | covered | `NY:CPLR-4544-small-print` | U014 |
| U5A-097 | CPLR 5001 | covered | `NY:CPLR-5001(a)-(b)` | U113 |
| U5A-098 | CPLR 5003-a | gap:R5A-32 |  | - |
| U5A-099 | CPLR 5004 | covered | `NY:CPLR-5004(a)-consumer-2pct` | U114 |
| U5A-100 | CPLR 5014 | no-decision-change | CPLR 5014 renewal is a post-judgment step 10 years out; it does not change the settlement decision (see R5A-21 for 211(b)). | - |
| U5A-101 | CPLR 5020 | gap:R5A-20 |  | - |
| U5A-102 | CPLR 5205(l) | gap:R5A-21 |  | - |
| U5A-103 | CPLR 5222(e) | gap:R5A-21 |  | - |
| U5A-104 | CPLR 5231(b) | gap:R5A-21 |  | - |
| U5A-105 | CPLR 5208 | gap:R5A-31 |  | - |
| U5A-106 | CCA 1801 | covered | `NY:CCA-1801-tenant-claim` | U089 |
| U5A-107 | CCA 1809 | covered | `NY:CCA-1809(1)` | U091 |
| U5A-108 | CCA 1801-A, 1803-A | covered | `NY:CCA-1801-A(a)-eligibility` `NY:CCA-1801-A(b)` `NY:CCA-1803-A(b)` | U092 |
| U5A-109 | CCA 1812 | covered | `NY:CCA-1812-treble` | U090 |
| U5A-110 | GCN 20 | covered | `NY:GCN-20` `NY:GCN-20-event-day` | U082 |
| U5A-111 | GCN 25-a | covered | `NY:GCN-25-a(1)` | U081 |
| U5A-112 | State Technology Law 304-305 | covered | `NY:STT-305(3)` | U083 |
| U5A-113 | 22 NYCRR 208.6 | no-decision-change | 22 NYCRR 208.6(d) consumer-credit summons form does not apply to a lease balance (not credit). | - |
| U5A-114 | GBL 349 as amended by L.2025 c.708 (FAIR Business Practices Act, eff. 2026-02-17) | gap:R5A-02 |  | - |
| U5A-115 | GBL 349(h) | gap:R5A-02 |  | - |
| U5A-116 | L.2025 c.708 s.6 | gap:R5A-02 |  | - |
| U5A-117 | GBL 600(1) | covered | `NY:GBL-600(1)` | U124 |
| U5A-118 | GBL 601 | covered | `NY:GBL-601(2)` `NY:GBL-601(6)` | U124 |
| U5A-119 | GBL 604-aa(3) (coerced debt), L.2025 c.710 as amended by L.2026 c.90 | covered | `NY:GBL-604-bb-coerced-debt` `NY:GBL-604-cc-coerced-defense` | U140 U141 |
| U5A-120 | L.2026 c.90 (A9460/S8830) effective-date amendment | covered | `NY:GBL-604-bb-coerced-debt` | U140 |
| U5A-121 | GBL 604-a (identity theft) | gap:R5A-33 |  | - |
| U5A-122 | GBL 130(9) | gap:R5A-19 |  | - |
| U5A-123 | GBL 399-h | gap:R5A-22 |  | - |
| U5A-124 | GBL 399-ddd | gap:R5A-33 |  | - |
| U5A-125 | GBL 899-aa | gap:R5A-14 |  | - |
| U5A-126 | GBL 899-bb | covered | `NY:GBL-899-bb-safeguards` | U172 |
| U5A-127 | Judiciary Law 489 | gap:R5A-03 |  | - |
| U5A-128 | Justinian Capital SPC v WestLB AG, 28 NY3d 160 (2016) | gap:R5A-03 |  | - |
| U5A-129 | Judiciary Law 495 | gap:R5A-18 |  | - |
| U5A-130 | Judiciary Law 478 | gap:R5A-18 |  | - |
| U5A-131 | SSL 143-b(5) | gap:R5A-04 |  | - |
| U5A-132 | ABP 1315 | covered | `NY:ABP-1315(2)` | U143 |
| U5A-133 | ABP 1422 | covered | `NY:ABP-1422` | U145 |
| U5A-134 | ABP 1400 | gap:R5A-34 |  | - |
| U5A-135 | ABP 1412 | gap:R5A-34 |  | - |
| U5A-136 | ABP 1412-a | gap:R5A-34 |  | - |
| U5A-137 | SCPA 1310 | covered | `NY:ADJ-tenant-death-payee` | U154 U153 |
| U5A-138 | SCPA 1802 | covered | `NY:ADJ-tenant-death-payee` | U156 |
| U5A-139 | EPTL 11-1.1 | no-decision-change | EPTL 11-1.1 fiduciary powers do not change the landlord's decision; SCPA rules govern payee and claims. | U157 |
| U5A-140 | Military Law 309 | gap:R5A-35 |  | - |
| U5A-141 | Military Law 310 | covered | `NY:MIL-310(2)` | U037 |
| U5A-142 | Military Law 308 | gap:R5A-30 |  | U111 |
| U5A-143 | Military Law 323-a | covered | `NY:MIL-323-a-6pct` | U116 |
| U5A-144 | Military Law 306 | gap:R5A-35 |  | - |
| U5A-145 | Executive Law 292(36) | covered | `NY:EXEC-296(5)(a)(2)-terms` | - |
| U5A-146 | Executive Law 296(5)(a) | covered | `NY:EXEC-296(5)(a)(2)-terms` | U165 |
| U5A-147 | LLC Law 206 | covered | `NY:LLC-206-publication-suspension` | - |
| U5A-148 | LLC Law 808 | covered | `NY:LLC-808(a)-foreign-authority` | U046 |
| U5A-149 | BCL 1312 | covered | `NY:BCL-1312(a)-foreign-authority` | U045 |
| U5A-150 | 23 NYCRR 1.1(d) | covered | `NY:23NYCRR-1.1(d)-not-lease` | U127 |
| U5A-151 | 23 NYCRR 1.2-1.6 | covered | `NY:23NYCRR-1.1(d)-not-lease` | - |
| U5A-152 | 19 NYCRR 175.1 | covered | `NY:19NYCRR-175.1-broker-escrow` | U012 |
| U5A-153 | 16 NYCRR 96.2 | gap:R5A-09 |  | - |
| U5A-154 | Admin. Code 26-504 | covered | `NYC:RSL-26-504(a)` `NYC:RS-status` | - |
| U5A-155 | Admin. Code 8-107(5)(a) | covered | `NYC:ADC-8-107(5)(a)-terms` | U163 |
| U5A-156 | Admin. Code 20-489 | covered | `NYC:ADC-20-489(a)` `NYC:ADC-20-489(d)` | U128 |
| U5A-157 | Admin. Code 20-490 | covered | `NYC:ADC-20-490` | U128 |
| U5A-158 | Admin. Code 20-493.1 | covered | `NYC:ADC-20-493.1(b)` | U129 |
| U5A-159 | Admin. Code 20-493.2 | covered | `NYC:ADC-20-493.2(a)` `NYC:ADC-20-493.2(b)` | U129 |
| U5A-160 | 6 RCNY 5-76 | covered | `NYC:RCNY6-5-76-debt-collector` | U134 |
| U5A-161 | 6 RCNY 5-77 | covered | `NYC:RCNY6-5-77(e)(1)` | U135 |
| U5A-162 | 6 RCNY 2-191 | covered | `NYC:RCNY6-2-191(a)` | U131 |
| U5A-163 | 6 RCNY 2-192 | covered | `NYC:RCNY6-2-192-payment-plan` | U132 |
| U5A-164 | 6 RCNY 2-193 | covered | `NYC:RCNY6-2-193-records` | U133 |
| U5A-165 | DCWP SHIELD rule (adopted 2026-02-26; effective 2027-01-01) | covered | `NYC:SHIELD-effective-date` `NYC:SHIELD-operative-date` | U136 U138 |
| U5A-166 | DCWP SHIELD NOA (original creditors) | covered | `NYC:SHIELD-5-76-debt-collector` | U137 |
| U5A-167 | Admin. Code 20-699.21 (FARE Act) | covered | `NYC:FARE-20-699.21-agent-fee-ban` | U017 |
| U5A-168 | Admin. Code 20-699.22 | covered | `NYC:FARE-20-699.22(b)` | - |
| U5A-169 | 6 RCNY 6-89 | covered | `NYC:FARE-20-699.23(c)` | - |
| U5A-170 | Admin. Code 20-700, 20-701 | covered | `NYC:CPL-20-700` | U139 |
| U5A-171 | Admin. Code 26-3002(c) | covered | `NYC:ADC-26-3002(c)-moveout-data` | U173 |
| U5A-172 | Admin. Code 26-3003(a)(1) | gap:R5A-37 |  | - |
| U5A-173 | Admin. Code 26-3006 | gap:R5A-37 |  | - |
| U5A-174 | Admin. Code 26-521, 26-523 | partial:R5A-05 |  | - |
| U5A-175 | Admin. Code 27-2013(b) | covered | `NYC:HMC-27-2013(b)(2)` | U072 |
| U5A-176 | Admin. Code 27-2017.5 | covered | `NYC:HMC-27-2017.5-turnover` | U074 |
| U5A-177 | Admin. Code 27-2056.8 | covered | `NYC:HMC-27-2056.8-lead-turnover` | U073 |
| U5A-178 | Admin. Code 27-2045 | covered | `NYC:HMC-27-2045-detector-charge` | - |
| U5A-179 | Admin. Code 27-2107(b) | covered | `NYC:ADC-27-2107(b)-rent-stay` | U048 |
| U5A-180 | 68 RCNY 10-14(c) (CityFHEPS) | covered | `NYC:RCNY68-10-14(c)` | U077 |
| U5A-181 | HRA Security Voucher W-147N | covered | `NYC:HRA-voucher-claim-window` | U079 |
| U5A-182 | 15 USC 1692a(5) | covered | `US:15USC1692a(5)` `US:15USC1692a(5)-lease-charges` | U056 |
| U5A-183 | 15 USC 1692a(6) | covered | `US:15USC1692a(6)-principal-purpose` `US:15USC1692a(6)-regularly-another` | U055 |
| U5A-184 | 15 USC 1692c | covered | `US:15USC1692c(a)` | U120 |
| U5A-185 | 15 USC 1692e | covered | `US:15USC1692e(2)(A)` | U120 |
| U5A-186 | 15 USC 1692f(1) | covered | `US:15USC1692f(1)` | U120 |
| U5A-187 | 15 USC 1692g | covered | `US:15USC1692g(a)` | U117 |
| U5A-188 | 15 USC 1692i | covered | `US:15USC1692i(a)` | U121 |
| U5A-189 | 15 USC 1692k | covered | `US:15USC1692k(a)` | U122 |
| U5A-190 | 12 CFR 1006.14(b)(2) | covered | `US:12CFR1006.14(b)(2)` | - |
| U5A-191 | 12 CFR 1006.26(b) | covered | `US:12CFR1006.26(b)` | - |
| U5A-192 | 12 CFR 1006.30(a) | covered | `US:12CFR1006.30(a)` | U119 |
| U5A-193 | 12 CFR 1006.34 | covered | `US:12CFR1006.34(c)` | U118 |
| U5A-194 | 12 CFR 1006.100 | covered | `US:12CFR1006.100(a)` | - |
| U5A-195 | 12 USC 5481(15)(A)(ii) | covered | `US:12USC5481(15)(A)(ii)` | - |
| U5A-196 | 15 USC 1681b(a)(3)(A) | gap:R5A-24 |  | - |
| U5A-197 | 15 USC 1681c(a)(4),(c) | gap:R5A-24 |  | - |
| U5A-198 | 15 USC 1681s-2(a) | covered | `US:15USC1681s-2(a)(1)(A)` | U170 |
| U5A-199 | 12 CFR 1022.42 | covered | `US:12CFR1022.42(a)` | U171 |
| U5A-200 | 47 USC 227(b)(1)(A)(iii) | gap:R5A-06 |  | - |
| U5A-201 | 47 CFR 64.1200(a)(10) | gap:R5A-06 |  | - |
| U5A-202 | Facebook, Inc. v Duguid, 592 US 395 (2021) | gap:R5A-06 |  | - |
| U5A-203 | 15 USC 7001(a),(c) | partial:R5A-01 |  | - |
| U5A-204 | 50 USC 3955 | covered | `US:50USC3955(f)` `US:50USC3955(e)(1)-no-etf` | U036 |
| U5A-205 | 50 USC 3931 | covered | `US:50USC3931(b)(1)` | U098 |
| U5A-206 | 50 USC 3936 | covered | `US:50USC3936-tolling` | U110 |
| U5A-207 | 50 USC 3937 | covered | `US:50USC3937-6pct` | U115 |
| U5A-208 | 50 USC 3958 | covered | `US:50USC3958(a)` `US:50USC3958-lien-enforcement` | - |
| U5A-209 | 50 USC 3951 | covered | `US:50USC3951(a)(1)(B)` | U158 |
| U5A-210 | 42 USC 3604(b),(f)(3)(B) | covered | `US:42USC3604(f)(3)(B)` | U160 |
| U5A-211 | 42 USC 3617 | gap:R5A-13 |  | - |
| U5A-212 | 24 CFR 100.7 | gap:R5A-13 |  | - |
| U5A-213 | 24 CFR 100.65 | covered | `US:24CFR100.65-terms` | U162 |
| U5A-214 | 34 USC 12491 | gap:R5A-23 |  | - |
| U5A-215 | 24 CFR 982.313(c)-(e) | covered | `US:24CFR982.313(c)` `US:24CFR982.313(d)` `US:24CFR982.313(e)` | U075 |
| U5A-216 | 24 CFR 982.311(d)(1) | covered | `US:24CFR982.311(d)(1)` | U076 |
| U5A-217 | 11 USC 362(a) | covered | `US:11USC362(a)(6)` `US:11USC362(a)(7)` | U146 |
| U5A-218 | 11 USC 541, 542 | covered | `US:11USC542-refund-payee` | U147 |
| U5A-219 | 11 USC 553 | covered | `US:11USC362(a)(7)-deposit-is-setoff` | U148 |
| U5A-220 | 11 USC 502(b)(6) | covered | `US:11USC502(b)(6)-lessor-cap` | U150 |
| U5A-221 | 11 USC 524(a) | covered | `US:11USC524(a)(2)` | U149 |
| U5A-222 | 11 USC 1301 | covered | `US:11USC1301-codebtor-stay` | U151 |
| U5A-223 | Fed. R. Bankr. P. 3002(c) | gap:R5A-10 |  | - |
| U5A-224 | 11 USC 108(c) | covered | `US:11USC108(c)-extension` | U112 |
| U5A-225 | 26 USC 6050P | covered | `US:26USC6050P-no-1099C` | U169 |
| U5A-226 | 26 USC 6041 / 26 CFR 1.6041-1 | gap:R5A-38 |  | - |
| U5A-227 | 26 USC 166 / 26 CFR 1.166-1(e) | gap:R5A-38 |  | - |
| U5A-228 | IRS Publication 527 | covered | `US:IRS-Pub527-deposit-income` | U167 |
| U5A-229 | LeRoy v Sayers, 217 AD2d 63 (1st Dept 1995) | covered | `NY:GOL-7-103(1)-trust` | U059 |
| U5A-230 | Paterno v Carroll, 75 AD3d 625 (2d Dept 2010) | covered | `NY:CASE-Paterno-commingling-forfeiture` | U058 |
| U5A-231 | Gihon, LLC v 501 Second St., LLC, 103 AD3d 840 (2d Dept 2013) | covered | `NY:CASE-Gihon-7-103(2-a)-building` | U058 |
| U5A-232 | Cohen v Abruzzo, 228 AD3d 724 (2d Dept 2024) | covered | `NY:CASE-Cohen-deadline-count` | - |
| U5A-233 | Urban v Zipper, 241 AD3d 1186 (1st Dept 2025) | covered | `NY:CASE-Urban-vacatur` | - |
| U5A-234 | Karole v 340 W. End (Civ Ct 2022) / Prando v Kelly | covered | `NY:CASE-Karole-willful` `NY:ADJ-willful-standard` | - |
| U5A-235 | Lasky v Lissik (1931) | covered | `NY:ADJ-cotenants-payee` | - |
| U5A-236 | Kunik v Club at Pearl River (App Term 2d 2023) | covered | `NY:ADJ-early-departure-rent-retention` | - |
| U5A-237 | JMD Holding Corp. v Congress Fin. Corp., 4 NY3d 373 (2005) | covered | `NY:ADJ-lease-break-charge` | - |
| U5A-238 | Truck Rent-A-Center v Puritan Farms 2nd, 41 NY2d 420 (1977) | covered | `NY:ADJ-lease-break-charge` | U027 |
| U5A-239 | 172 Van Duzer Realty Corp. v Globe Alumni Student Assistance Assn., 24 NY3d 528 (2014) | covered | `NY:ADJ-lease-break-charge` | U026 |
| U5A-240 | Riverside Research Inst. v KMGA, 68 NY2d 689 (1986) | covered | `NY:CASE-Riverside-surrender-by-operation` | U025 |
| U5A-241 | 8902 Corp. v Helmsley-Spear, 12 AD3d 193 (1st Dept 2005) | covered | `NY:COMMONLAW-belongings-owner-keeps` | - |
| U5A-242 | Stauber v Antelo, 163 AD2d 246 (1st Dept 1990) | covered | `NY:RPL-232` | - |
| U5A-243 | Chazon, LLC v Maugenest, 19 NY3d 410 (2012) | covered | `NY:MDL-302(1)(b)` | - |
| U5A-244 | Fields v Pinkney (2d Dept 2025) | covered | `NY:RPL-440(1)-rent-collection` | - |
| U5A-245 | Romea v Heiberger & Assocs., 163 F3d 111 (2d Cir 1998) | covered | `US:CASE-Romea-1998` | U056 |
| U5A-246 | Henson v Santander, 582 US 79 (2017) | covered | `US:CASE-Henson-2017` | - |
| U5A-247 | Heintz v Jenkins, 514 US 291 (1995) | no-decision-change | Heintz binds the lawyer, not the landlord's decision; attorney-collectors are within 15 USC 1692a(6) as stated. | U054 |
| U5A-248 | Avila v Riexinger & Assocs., 817 F3d 72 (2d Cir 2016) | covered | `US:CASE-Avila-accruing-balance` | U123 |
| U5A-249 | Alibrandi v Financial Outsourcing Servs., 333 F3d 82 (2d Cir 2003) | covered | `US:15USC1692a(6)(F)(iii)-default-meaning` | - |
| U5A-250 | Lefferts (2026) | covered | `NY:CASE-Lefferts-rent-not-consumer-credit` | - |
| U5A-251 | In re Sweet N Sour 7th Ave. Corp. (Bankr SDNY 2010) | covered | `US:11USC362(a)(7)-deposit-is-setoff` | - |
| U5A-252 | Citizens Bank of Md. v Strumpf, 516 US 16 (1995) | covered | `US:CASE-Strumpf-hold` | - |
| U5A-253 | S9760/A10182-A Consumer Debt Uniformity Act (passed both houses 2026-06-02/03; not delivered) | covered | `NY:CPLR-214-i-consumer-debt-S9760` | U176 |
| U5A-254 | S00947/A03121 (ACH / online rent payment fee ban; passed Senate 2026-03-18, Assembly 2026-05-13; not delivered) | covered | `NY:S947-ach-fee-ban` | U174 U175 |
| U5A-255 | S09650/A00659 (421-a lease decontrol information; passed both houses 2026; not delivered) | gap:R5A-41 |  | - |
| U5A-256 | 11 USC 1306(b) | covered | `US:11USC1107-1306-owner-reorganization` | - |
| U5A-257 | 50 USC 3918 | covered | `US:50USC3918` | - |
| U5A-258 | RPL 231-c | gap:R5A-39 |  | - |
| U5A-259 | RPAPL 741(5) | gap:R5A-11 | `NY:RPL-220` | - |
| U5A-260 | Admin. Code 27-2097 | covered | `NYC:ADC-27-2097-registration` | - |
| U5A-261 | Admin. Code 8-102 (lawful source of income) | covered | `NYC:ADC-8-107(5)(a)-terms` | U164 |
| U5A-262 | GOL 7-109 | covered | `NY:GOL-7-109` | U088 |
| U5A-263 | Executive Law 297(9) | gap:R5A-36 |  | - |
| U5A-264 | HUD-52641-A HCV Tenancy Addendum | covered | `US:24CFR982.451(b)(4)` | - |

## Comparison with round 4A's universe

(i) In 5A, not in 4A (116): U5A-019 GOL 5-703(1); U5A-021 GOL 15-104; U5A-022 GOL 15-105; U5A-023 GOL 15-301(1); U5A-024 GOL 15-501; U5A-025 UCC 1-308; U5A-026 Horn Waterproofing Corp. v Bushwick Iron & Steel Co., 66 NY2d 321 (1985); U5A-028 GOL 17-103; U5A-029 GOL 5-702; U5A-030 RPL 220; U5A-032 RPL 223-b(5); U5A-040 RPL 228; U5A-042 RPL 232; U5A-048 RPL 235-c; U5A-049 RPL 235-e(d); U5A-050 RPL 235-f; U5A-057 RPL 211 (Good Cause definitions); U5A-060 RPL 218; U5A-063 RPL 441-c; U5A-064 RPAPL 702; U5A-065 RPAPL 711(2); U5A-066 RPAPL 744; U5A-067 RPAPL 749(3); U5A-068 RPAPL 768; U5A-069 RPAPL 853; U5A-072 22 NYCRR 208.42(g); U5A-073 MDL 4(7); U5A-076 MDL 302-c; U5A-078 MDL 51-c; U5A-081 CPLR 204(a); U5A-082 CPLR 205(a); U5A-083 CPLR 207; U5A-084 CPLR 208; U5A-086 CPLR 211(b); U5A-088 CPLR 214(4); U5A-090 CPLR 321(a); U5A-091 CPLR 1201, 1203; U5A-092 CPLR 1015; U5A-094 CPLR 3012; U5A-098 CPLR 5003-a; U5A-100 CPLR 5014; U5A-101 CPLR 5020; U5A-102 CPLR 5205(l); U5A-103 CPLR 5222(e); U5A-104 CPLR 5231(b); U5A-105 CPLR 5208; U5A-113 22 NYCRR 208.6; U5A-114 GBL 349 as amended by L.2025 c.708 (FAIR Business Practices Act, eff. 2026-02-17); U5A-115 GBL 349(h); U5A-116 L.2025 c.708 s.6; U5A-121 GBL 604-a (identity theft); U5A-122 GBL 130(9); U5A-123 GBL 399-h; U5A-124 GBL 399-ddd; U5A-125 GBL 899-aa; U5A-127 Judiciary Law 489; U5A-128 Justinian Capital SPC v WestLB AG, 28 NY3d 160 (2016); U5A-129 Judiciary Law 495; U5A-130 Judiciary Law 478; U5A-131 SSL 143-b(5); U5A-134 ABP 1400; U5A-135 ABP 1412; U5A-136 ABP 1412-a; U5A-140 Military Law 309; U5A-144 Military Law 306; U5A-145 Executive Law 292(36); U5A-147 LLC Law 206; U5A-151 23 NYCRR 1.2-1.6; U5A-153 16 NYCRR 96.2; U5A-154 Admin. Code 26-504; U5A-168 Admin. Code 20-699.22; U5A-169 6 RCNY 6-89; U5A-172 Admin. Code 26-3003(a)(1); U5A-173 Admin. Code 26-3006; U5A-174 Admin. Code 26-521, 26-523; U5A-178 Admin. Code 27-2045; U5A-190 12 CFR 1006.14(b)(2); U5A-191 12 CFR 1006.26(b); U5A-194 12 CFR 1006.100; U5A-195 12 USC 5481(15)(A)(ii); U5A-196 15 USC 1681b(a)(3)(A); U5A-197 15 USC 1681c(a)(4),(c); U5A-200 47 USC 227(b)(1)(A)(iii); U5A-201 47 CFR 64.1200(a)(10); U5A-202 Facebook, Inc. v Duguid, 592 US 395 (2021); U5A-203 15 USC 7001(a),(c); U5A-208 50 USC 3958; U5A-211 42 USC 3617; U5A-212 24 CFR 100.7; U5A-214 34 USC 12491; U5A-223 Fed. R. Bankr. P. 3002(c); U5A-226 26 USC 6041 / 26 CFR 1.6041-1; U5A-227 26 USC 166 / 26 CFR 1.166-1(e); U5A-232 Cohen v Abruzzo, 228 AD3d 724 (2d Dept 2024); U5A-233 Urban v Zipper, 241 AD3d 1186 (1st Dept 2025); U5A-234 Karole v 340 W. End (Civ Ct 2022) / Prando v Kelly; U5A-235 Lasky v Lissik (1931); U5A-236 Kunik v Club at Pearl River (App Term 2d 2023); U5A-237 JMD Holding Corp. v Congress Fin. Corp., 4 NY3d 373 (2005); U5A-241 8902 Corp. v Helmsley-Spear, 12 AD3d 193 (1st Dept 2005); U5A-242 Stauber v Antelo, 163 AD2d 246 (1st Dept 1990); U5A-243 Chazon, LLC v Maugenest, 19 NY3d 410 (2012); U5A-244 Fields v Pinkney (2d Dept 2025); U5A-246 Henson v Santander, 582 US 79 (2017); U5A-249 Alibrandi v Financial Outsourcing Servs., 333 F3d 82 (2d Cir 2003); U5A-250 Lefferts (2026); U5A-251 In re Sweet N Sour 7th Ave. Corp. (Bankr SDNY 2010); U5A-252 Citizens Bank of Md. v Strumpf, 516 US 16 (1995); U5A-255 S09650/A00659 (421-a lease decontrol information; passed both houses 2026; not delivered); U5A-256 11 USC 1306(b); U5A-257 50 USC 3918; U5A-258 RPL 231-c; U5A-259 RPAPL 741(5); U5A-260 Admin. Code 27-2097; U5A-263 Executive Law 297(9); U5A-264 HUD-52641-A HCV Tenancy Addendum.

(ii) In 4A, not in 5A (27), with 5A's assessment:
- U023 Holy Props. v Kenneth Cole (CoA 1995): real law for leases predating RPL 227-e (no mitigation duty); missed by 5A.
- U024 Toporek (1st Dept 2022): real controlling authority on 227-e/forfeiture scope; missed by 5A.
- U039 PTFA (12 USC 5220 note): real federal successor-in-foreclosure protection; missed by 5A.
- U067 Graham Court v Taylor (CoA 2015): real controlling RPL 234 decision; 5A dropped it for want of a clean majority quote.
- U071 RPL 235-a (utility offset): real; 5A enumerated MDL 302-c but not 235-a.
- U078 68 RCNY 10-14(e) (CityFHEPS landlord's 5-business-day move-out notice to HRA): real operator duty; missed by 5A.
- U084 Levine v Xu-Kehrli (App Term 1st 2026): real (forfeiture leaves claims); 5A dropped it for want of a clean quote.
- U086 CPLR 214(2) (three years for statutory liability, e.g., tenant's 7-108 penalty claim): real; missed by 5A.
- U087 Gaidon (CoA 2001) GBL 349 accrual: real; missed by 5A.
- U093 CCA 1809-A (commercial claims certification and appearance): real; 5A used it only as evidence in R5A-18.
- U095 CPLR 3215(j) limitations affidavit on default: real; missed by 5A.
- U096 CPLR 3016(j): applies to consumer credit only; not applicable to a lease balance (no decision change).
- U099 Military Law 303(3): real (representation/affidavit for NY military defendants); missed by 5A.
- U101 CCA 1810 / 1810-A (claim-count limits): real; missed by 5A.
- U105 DCWP SHIELD NOA statement on 214-i: agency statement, adjudicated against by the rule files; guidance.
- U109 CPLR 210(a) (death of claimant): real; 5A enumerated only 210(b).
- U125 GBL 601-a: real within art. 29-H scope; art. 29-H does not reach a lease balance.
- U126 GBL 602: penalties under art. 29-H; same scope limit.
- U130 6 RCNY 2-190 (documentation to be provided by agency): real; missed by 5A.
- U142 L.2019 c.36 Part M s29 (7-108 applies to leases entered/renewed on or after 2019-06-14): real point-in-time rule; missed by 5A.
- U144 OSC property-type table (reporting codes): guidance; real for reporting.
- U152 11 USC 365(d)(1) (chapter 7 deemed rejection): real; missed by 5A.
- U153 SCPA 1301 (voluntary administration): real; 5A cites it only via SCPA 1310.
- U155 SCPA 1305: real; missed by 5A.
- U159 SCRA 2026 rent threshold (FR 2026-04689): real; missed by 5A.
- U161 24 CFR 100.203 (reasonable modifications): real; missed by 5A.
- U168 26 USC 6049 (deposit interest reporting): real; missed by 5A.

(iii) Gap items in neither 4A's universe nor the rule files: **71** (U5A-019, U5A-021, U5A-022, U5A-023, U5A-024, U5A-025, U5A-026, U5A-028, U5A-029, U5A-032, U5A-060, U5A-063, U5A-066, U5A-067, U5A-068, U5A-069, U5A-072, U5A-076, U5A-078, U5A-081, U5A-082, U5A-083, U5A-084, U5A-086, U5A-090, U5A-091, U5A-092, U5A-098, U5A-101, U5A-102, U5A-103, U5A-104, U5A-105, U5A-114, U5A-115, U5A-116, U5A-121, U5A-122, U5A-123, U5A-124, U5A-125, U5A-127, U5A-128, U5A-129, U5A-130, U5A-131, U5A-134, U5A-135, U5A-136, U5A-140, U5A-144, U5A-153, U5A-172, U5A-173, U5A-174, U5A-196, U5A-197, U5A-200, U5A-201, U5A-202, U5A-203, U5A-211, U5A-212, U5A-214, U5A-223, U5A-226, U5A-227, U5A-255, U5A-258, U5A-259, U5A-263).

## New versus earlier rounds

Read after the findings above were saved: INDEPENDENT_REVIEW_1-3, 4A, 4B and REVIEW_1-4_DISPOSITION. None of the 41 findings was raised as a finding in an earlier round. Two touch law an earlier round mentioned:
- R5A-09: Round 2 considered PSC submetering and left it out ('no utility charge fact pattern in scope'). 5A rejects that exclusion: GOL 7-108(1-a)(b) itself makes lease utility charges payable to the landlord a retainable head, so whether such a charge is lawful is in scope.
- R5A-39: Round 1 noted RPL 231-c only as listed out of scope in the NY coverage table; no round stated its predicate-notice and petition consequence (RPAPL 741(5-a)).
- RPL 235-e(d): round 2 excluded it as an eviction-only defense; 5A agrees and records it as no-decision-change (U5A-049).
- GOL 5-703 appears in the rules only as authority for voiding an oral lease over one year (`NY:ADJ-RPL-232-oral-term-over-one-year`); its surrender-writing rule (R5A-16) is new.

## Method

- Phase 1 (blind): read only APERTURE.md and STAGE_A.md's 'Chain (aperture)' and 'Discovery method'. The statute-compilation skill (and its reference notes, which summarize earlier rounds) was loaded as the harness requires; the universe was built from tables of contents, not from those notes.
- Tables of contents walked mechanically (`review/ir5a_toc.py`, newyork.public.law mirror of the official nysenate.gov text; nysenate.gov, Justia, FindLaw and LegiScan are Cloudflare-walled to curl and the browser): GOL arts. 3, 5, 7, 15, 17; RPL arts. 6-A, 7, 12-A; RPAPL arts. 7, 7-A, 7-C, 8; MDL arts. 1-3, 8; CPLR arts. 2, 10, 12, 50, 52 and the full article list; GBL article list and arts. 9-B, 22-A, 25, 29-H, 29-HH, 29-HHH, 39-F; Military Law art. 13; Executive Law art. 15; ABP arts. 13-14; Judiciary Law art. 15. NYC Admin. Code and RCNY sections were searched and extracted from American Legal's official bulk XML (`review/ir5a_aml.py`).
- Pending law: the Assembly's full-text search returned all 21,519 bills of the 2025-26 session with summaries; 3,219 matching chain keywords had their action histories fetched and parsed for passage in both houses in the same year, signature, veto or delivery. Chain-relevant bills passed by both houses and not yet acted on: S9760/A10182-A, S947/A3121, S9650/A659. Enacted in the window and relevant: L.2025 c.708 (FAIR Act), c.710 and L.2026 c.90 (coerced debt), c.431 (dishonored-check fee), c.91 (breach notice to DFS). A8906/S6446 passed the Senate in 2025 and the Assembly in 2026 only, so it has not passed both houses.
- Federal texts from uscode.house.gov and the eCFR renderer; cases from the Caselaw Access Project static JSON (Horn Waterproofing), the Wayback copy of the Court of Appeals slip opinion (Justinian) and supremecourt.gov (Duguid). web_extract and web search were unavailable (credits exhausted).
- Quotes are cut from saved sources by anchors or regex (`review/ir5a_lib.py`, `review/ir5a_build_universe.py`), never retyped. Phase 2 mapped each universe item to rule ids (`review/ir5a_map.py` candidates, then hand adjudication recorded in `review/ir5a_coverage.py`), and findings were built by `review/ir5a_build_findings.py`.
- One universe entry was corrected before the diff after reading the full section: SCPA 1310 does not reach a landlord's deposit refund (the rule files state this correctly).
- `python3 review/ir5a_verify.py`: every universe and evidence quote is verbatim in its source (whitespace-normalized), every cited rule id exists, no banned hedge phrase; the self-test catches a planted altered quote, altered evidence and a bad rule id. `stage_a_check.py` and `check_review.py` pass unchanged (0 errors; 551 in scope, 0 uncited).
