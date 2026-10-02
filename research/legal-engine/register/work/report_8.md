# Report 8: set-aside reviewer B (NY MDL through federal FRBP)

Reviewer q8, 2026-09-30. Batch `register/work/batch_8.json`: 420 sections Jev set aside as deciding nothing (NY 221, NYC 109, US 90; 905,152 characters). Every section was read in full from its register text; decisions are in `register/work/decisions_8.jsonl`, written by the idempotent scripts `register/work/q8_c*.py` (helpers `q8_lib.py`, this report `q8_report.py`). Report only: no rule file, walk, skill or source was edited.

## Counts

- Decided: 420/420. no_decision 413, new_rule 6, partial 1, stated 0, excluded_regime 0.
- Proposed rules: 7 (critical 1, major 5, minor 1).
- `python3 register/work/check_decisions.py 8`: 420/420 decided, 0 errors. `check_decisions.py all`: no id collisions (batch 7's 45 undecided sections belong to set-aside reviewer A, still running).

## Sections decided other than no_decision (Jev's misses)

| Section | Heading | Decision | Jev p_decides | Jev chain_duty | Proposed rule |
|---|---|---|---|---|---|
| NY:N-PCL 1309 | Certificate of amendment | new_rule | 0 | 0.04 | `NY:NPCL-1309(b)-name-change-suspension` |
| NY:Partnership Law 121-1504 | Foreign related limited liability partnership | new_rule | 0 | 0.05 | `NY:PTR-121-1504-foreign-related-llp` |
| NY:Partnership Law 121-1506 | Resignation for receipt of process | new_rule | 0.03 | 0.07 | `NY:PTR-121-1506-llp-process-address-suspension` |
| NY:Partnership Law 121-201 | Certificate of limited partnership | new_rule | 0.01 | 0.07 | `NY:PTR-121-201-lp-publication` |
| NY:Partnership Law 121-803 | Winding up | new_rule | 0.01 | 0.08 | `NY:PTR-121-803-dissolved-owner-winding-up` |
| NY:Partnership Law 121-804 | Distribution of assets | new_rule | 0 | 0.05 | `NY:PTR-121-804-creditors-before-partners` |
| NYC:ADC 20-105 | Additional powers of the commissioner with respect to unlice | partial | 0.04 | 0.08 | `NYC:ADC-20-105-unlicensed-daily-fine` |

All seven scored at or below 0.01 on p_decides and 0.04-0.08 on chain_duty: Jev read entity-filing and licensing boilerplate as internal governance and missed the suspension, winding-up and penalty clauses inside it. Six of the seven are owner-capacity or owner-status rules of the same family the queue reviewers already opened (LLC 206, BCL 1312, N-PCL 1313, Partnership Law 121-902/907/1500/1502/104-A); the set-aside list held the remaining branches of that family.

## Proposed rules, most severe first

### `NY:PTR-121-201-lp-publication` (critical, walk step 8.10, RULE)
- Section: NY:Partnership Law 121-201; provision Partnership Law 121-201(c)
- If: The owner is a New York limited partnership and it, or a collector in its name, sues or would sue a former tenant for a balance. Branch (a): the partnership was formed on or after the effective date of 121-201(c)(i) and did not file proof of publication (certificate of publication with the newspapers' affidavits) with the Department of State within 120 days after its formation. Branch (b): it was formed before that date, did not comply with the earlier publication requirement (a partnership formed before 1999-01-01, or formed from 1999-01-01 on that filed at least one publisher's affidavit, is deemed to have complied), and did not file proof of publication within twelve months after that date. Branch (c): it complied, or is deemed to have complied, with the requirement that applied to it.
- Then: (a) and (b): its authority to carry on, conduct or transact business in New York is suspended from the end of the 120-day (or twelve-month) period, and while suspended it cannot maintain the suit. Filing proof of publication in substantial compliance at any time annuls the suspension, so the suit may proceed once it is filed. The suspension does not impair the lease, the deposit statement, any right or remedy of the tenant, the tenant's right to sue the partnership, or the partnership's defense of the tenant's suit, and does not make any partner or agent liable for the partnership's obligations. (c): no bar. Operator step: confirm the Department of State record shows the publication filing before suing.
- Quote (register/texts/NY_PTR/121-201.txt): "If within one hundred twenty days after its formation, proof of such publication, consisting of the certificate of publication of the limited partnership with the affidavits of publication of the newspapers annexed thereto has not been filed with the department of state, the authority of such limited partnership to carry on, conduct or transact any business in this state shall be suspended, effect..."
- Reasoning: 121-201(c) uses the same suspension and annulment words as LLC Law 206, which the Appellate Division reads as barring the entity from maintaining an action while suspended (NY:LLC-206-publication-suspension, Small Step Day Care); the section's savings clause preserves contracts, the other party's rights and suits and the partnership's defense, and filing proof annuls the suspension. The queue's proposals cover foreign limited partnerships (121-902) and LLPs (121-1500, 121-1502); this is the domestic limited partnership branch.
- Depends on: NY:LLC-206-publication-suspension

### `NY:NPCL-1309(b)-name-change-suspension` (major, walk step 8.10, RULE)
- Section: NY:N-PCL 1309; provision N-PCL 1309(b); 1313(a)
- If: The owner is a foreign not-for-profit corporation authorized to conduct activities in New York that changed its name in its state of incorporation and did not deliver a certificate of amendment of its application for authority to the Department of State within twenty days after the change took effect; it (or a collector in its name) sues or would sue a former tenant for a balance.
- Then: From the twenty-first day after the name change its New York authority is suspended, so it is a foreign corporation conducting activities without authority and cannot maintain the suit (NY:NPCL-1313-foreign-authority). Branch (a): the Department of State files a certificate of amendment changing the name within 120 days after the name change took effect: the suspension is annulled and authority continues as if no suspension had occurred, so capacity to sue is restored for the whole period. Branch (b): no such filing within 120 days: the suspension stands and the corporation cannot maintain the suit until it is authorized and has paid the fees, penalties and franchise taxes 1313(a) requires. In both branches the lease, the deposit statement, the tenant's right to sue it and its defense of the tenant's suit are unaffected (1313(b)), and the Secretary of State remains its agent for the tenant's process during the suspension. Check the Department of State entity record for a name change before a suit is filed.
- Quote (register/texts/NY_NPCL/1309.txt): "If an authorized foreign corporation has changed its name in the jurisdiction of its incorporation, it shall deliver to the department of state within twenty days after the change became effective in that jurisdiction a certificate of amendment under paragraph (a). Upon its failure to deliver such certificate, its authority to conduct activities in this state shall upon the expiration of said twen..."
- Reasoning: 1309(b) suspends the authority of a foreign not-for-profit that fails to file its name change within twenty days; a corporation whose authority is suspended conducts activities without authority, which 1313(a) bars from maintaining any action until authorized. The 120-day filing annuls the suspension retroactively ('as if no suspension had occurred'); absent it, 1313(a)'s own cure (authorization plus back fees) governs. The rule depends on the queue's proposed NY:NPCL-1313-foreign-authority, which is not yet in the rule files, so the existing BCL analogue is listed as the dependency.
- Depends on: NY:BCL-1312(a)-foreign-authority

### `NY:PTR-121-1504-foreign-related-llp` (major, walk step 8.10, RULE)
- Section: NY:Partnership Law 121-1504; provision Partnership Law 121-1504
- If: The owner is a foreign related limited liability partnership (a foreign LLP that obtained a certificate of authority under LLC Law 802) that leases NYC units, and it or a collector in its name sues a former tenant.
- Then: Branch (a): within five years after it filed its application for the LLC Law 802 certificate of authority, having satisfied all of 802's requirements, it is deemed to have filed the 121-1502 notice, so the 121-1502 bar for a foreign LLP that has not filed its notice does not apply. Branch (b): from the fifth anniversary of that application it must file the 121-1502 notice; if it has not, it cannot maintain the suit until it files the notice and pays the fees (the queue's NY:PTR-121-1502-foreign-llp).
- Quote (register/texts/NY_PTR/121-1504.txt): "Any foreign related limited liability partnership that has filed a certificate of authority under and satisfied all the requirements of section eight hundred two of the limited liability company law shall be deemed to have filed a notice pursuant to section 121-1502 of this chapter until the fifth anniversary of filing its application for such certificate of authority, at which time the foreign re..."
- Depends on: NY:LLC-808(a)-foreign-authority

### `NY:PTR-121-1506-llp-process-address-suspension` (major, walk step 8.10, RULE)
- Section: NY:Partnership Law 121-1506; provision Partnership Law 121-1506(b)-(d)
- If: The owner is a New York registered limited liability partnership; the party whose address it designated for the Secretary of State to mail process filed a certificate of resignation for receipt of process, and the partnership has not filed a certificate of amendment or statement designating a new address, when it or a collector in its name sues a former tenant.
- Then: Its authority to do business in New York is suspended, so it cannot maintain the suit until the Department of State files its certificate of amendment or statement of a new address; that filing annuls the suspension and restores authority as if no suspension had occurred. While suspended, the tenant may serve process on the partnership through the Secretary of State. The lease and the deposit statement are unaffected.
- Quote (register/texts/NY_PTR/121-1506.txt): "Upon the failure of the designating limited liability partnership to file a certificate of amendment providing for the designation by the limited liability partnership of the new address after the filing of a certificate of resignation for receipt of process with the secretary of state, its authority to do business in this state shall be suspended."
- Reasoning: Suspension of authority to do business bars maintaining an action, as with the publication suspensions (NY:LLC-206-publication-suspension); 121-1506(d) annuls it retroactively on filing a new address. The queue's NY:PTR-121-104-a-process-address-suspension states the same rule for limited partnerships; this is the LLP branch.
- Depends on: NY:LLC-206-publication-suspension

### `NY:PTR-121-803-dissolved-owner-winding-up` (major, walk step 0.5, RULE)
- Section: NY:Partnership Law 121-803; provision Partnership Law 121-803
- If: The owner is a New York limited partnership that is dissolved (121-801 or 121-802) before a departing tenant's account is closed.
- Then: Dissolution does not end the settlement or the claim. The persons winding up act in the partnership's name: the general partners who did not wrongfully dissolve it, or if none the limited partners, or, where the Supreme Court winds up the affairs on a partner's application or after a judicial dissolution under 121-802 (to which the partners' own winding-up right does not extend), the receiver or liquidating trustee it appoints. They may send the statement and refund, settle, and prosecute or defend suits in the partnership's name, including a suit for the former tenant's balance; the manager and any collector take instructions and pay remittances only to them. The deposit stays the tenant's trust money (NY:GOL-7-103(1)-trust) and is returned or applied under the deposit rules, not distributed to partners.
- Quote (register/texts/NY_PTR/121-803.txt): "Upon dissolution of a limited partnership, the persons winding up the limited partnership’s affairs may, in the name of, and for and on behalf of, the limited partnership prosecute and defend suits, whether civil, criminal or administrative, settle and close the limited partnership’s business, dispose of and convey the limited partnership’s property, discharge the limited partnership’s liabilities"
- Depends on: NY:GOL-7-103(1)-trust

### `NYC:ADC-20-105-unlicensed-daily-fine` (major, walk step 8.6, RULE)
- Section: NYC:ADC 20-105; provision Admin. Code 20-105(a), (b), (d), (g); amends `NYC:ADC-20-490`
- If: A person that must hold a DCWP licence under Admin. Code title 20 chapter 2 (for this chain, a debt collection agency under 20-489 and 20-490) collects former NYC tenants' balances without the licence.
- Then: Besides the chapter 2 penalties (20-490, 20-494) and the 20-106 sanctions, DCWP may, after notice and hearing: (1) fine it $100 per violation for each day of unlicensed activity, each day a separate violation, not offset by the chapter 2 penalties; (2) order it to stop the activity at the premises at once; (3) seal premises used primarily for the activity; and (4) remove or seal the devices and goods used in it. Orders under (2)-(4) are stayed for a person that filed a full and complete licence or renewal application with the fee before DCWP served its notice, while the application is pending. Sealed premises and devices are released only on payment of all fines and costs and proof of a licence. Operator step: hold the licence (or a pending complete application) before any collection that makes Handoff or a buyer a debt collection agency.
- Quote (register/texts/NYC_ADC/20-105.txt): "to impose fines upon any person in violation of subdivision a of this section of one hundred dollars per violation per day"
- Reasoning: 20-105(a) makes unlicensed activity unlawful for anyone chapter 2 requires to be licensed, which includes a debt collection agency under subchapter 30 (20-489, 20-490); (b)(1) adds a per-day fine expressly cumulative with chapter 2 penalties, which NYC:ADC-20-490 does not list.
- Depends on: NYC:ADC-20-490, NYC:ADC-20-489(a), NYC:DCA-handoff-principal-purpose, NYC:DCA-debt-buyer

### `NY:PTR-121-804-creditors-before-partners` (minor, walk step 7.6, RULE)
- Section: NY:Partnership Law 121-804; provision Partnership Law 121-804(a)
- If: A dissolved owner limited partnership winds up while a former tenant's refund, interest or damages claim (for example 7-108(1-a)(g) damages) is unpaid or in dispute.
- Then: The partnership's assets go first to creditors, the former tenant included, by payment or by an adequate reserve for the claim, before any distribution to partners on their interests or contributions.
- Quote (register/texts/NY_PTR/121-804.txt): "to creditors, including partners who are creditors, to the extent permitted by law, in satisfaction of liabilities of the limited partnership, whether by payment or by establishment of adequate reserves"
- Depends on: NY:GOL-7-108(1-a)(g)

## Notes for adjudication

- Dependencies on queue proposals. The capacity rules above rest on the queue's proposed `NY:NPCL-1313-foreign-authority`, `NY:PTR-121-1502-foreign-llp` and `NY:PTR-121-104-a-process-address-suspension`, which are not yet in the rule files; the checker accepts only existing ids in `dependencies`, so those names appear in the effect or reasoning text and the existing analogues (`NY:LLC-206-publication-suspension`, `NY:BCL-1312(a)-foreign-authority`, `NY:LLC-808(a)-foreign-authority`) are listed as dependencies. If Owen rejects a queue proposal, the dependent rule here falls with it.
- Suspension bars suit. `NY:PTR-121-201-lp-publication` and `NY:PTR-121-1506-llp-process-address-suspension` read 'authority ... suspended' as barring the entity from maintaining an action, on the Appellate Division's reading of the identical LLC Law 206 words (Small Step Day Care, the construction behind `NY:LLC-206-publication-suspension`). `NY:NPCL-1309(b)-name-change-suspension` applies N-PCL 1313(a), whose text bars a corporation 'conducting activities ... without authority'.
- Boundary calls decided no_decision, stated here so Owen can overrule them in one line each:
  - Partnership Law 121-303 and 121-403 (limited and general partners' personal liability for the owner partnership's debts): reaching an owner's principals to enforce a tenant's judgment is not a step any chain actor takes; consistent with the queue's 121-1001 decision. If Owen wants the tenant's enforcement against principals in scope, both become rules (general partners liable as partners in a general partnership; limited partners not liable unless they take part in control and the tenant reasonably relied on it).
  - RPL 442-A (salespersons paid only through their broker for 'leasing, renting'): decided on the construction already in `NY:RPL-442-fee-split` (Kreuter, strict construction; 'renting' excludes rent collection). If that construction falls, 442-A would bar Handoff from paying its own salesperson-employees for rent collection under Configuration 3.
  - SCPA 2108 (court-authorized continuation of a decedent's business): the existing owner-death and fiduciary rules decide who collects and who is paid; a continuation decree adds no settlement step.
  - 6 RCNY 5-42 (price gouging, 'merchant' includes a lessor): a move-out charge passes on the landlord's repair or cleaning cost under the deposit rules and is not a sale of covered goods or services by the landlord.
  - MHL 81.03, N-PCL 1301, Partnership Law 121-101 and 121-1507, 24 CFR 982.2, 28 RCNY 12-05 (definitions and applicability): each read against the rules that use its terms; none widens or narrows a stated or proposed rule.

## Existing rules that look wrong

None found in the rules this batch touched (`NYC:ADC-20-490`, `NY:RPL-223`, `NY:GBL-130-assumed-name`, `NY:HMC-27-2045-detector-charge`, `NY:HANDOFF-broker-config-under-broker`, `NY:RPL-442-fee-split`, `NY:LLC-206-publication-suspension`, `NY:GOL-7-103(1)-trust`). One incompleteness, proposed above: `NYC:ADC-20-490` lists the 20-494 penalties but not the separate 20-105 per-day fine, stop order and sealing for unlicensed activity.
