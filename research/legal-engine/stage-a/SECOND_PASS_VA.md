# Virginia Stage A: second pass (2026-09-28)

`stage-a/VA.json` now has 251 atoms and 13 bounded unknowns, down from 22. `python3 stage_a_check.py stage-a/VA.json` exits 0.
Mutating one word in a new quote, a clean-act quote or the 1-238 quote makes the check fail. No VA quote is found in a non-VA source file.
Status: a candidate for Owen's review, not accepted.

## Unknowns closed (9)

| Unknown | Closed by (atoms / refs) | Reason |
|---|---|---|
| UNK:VA-unclaimed-interplay | VA:55.1-2500-intangible-security-deposits, -holder, -payable; VA:55.1-2501 | Ch. 25 lists "security deposits" and "refunds" as intangible property. A landlord or agent owing the refund is a "holder". The refund is "payable" by the end of the 45-day period at the latest. A landlord that does not use the optional one-year remittance in 1226(B) must still report once the 5-year presumption in 55.1-2501 runs. |
| UNK:VA-unclaimed-form | VA:TreasuryUP-guidance-report-channel, -early-report, -due-diligence (GUIDANCE) | Treasury's only reporting channel is the vamoneysearch.gov holder report: a NAUPA file, or "Enter a Manual Report". Treasury accepts voluntary early reports when the owner cannot be found. It lists property code AC06 "SECURITY DEPOSIT". Items of $100 or more need a due-diligence letter 60 days before reporting. The guidance never names 1226(B), so treating this report as the prescribed form is an inference. |
| UNK:VA-HUD-programs | refs US:24CFR982.313(c)-(e), US:24CFR966.4(b)(2),(4),(5), US:24CFR880.608 | This is federal meaning, so US.json owns it. VA.json keeps only the Virginia routing rule VA:55.1-1201(A)-HUD. |
| UNK:VA-FDCPA | refs US:15USC1692a(6), US:12CFR1006 (dependencies of VA:55.1-1209(A)(11)) | This is federal meaning, so US.json owns it. |
| UNK:VA-collection-agency-licensing | VA:54.1-3904-collection-agency-referral | I searched the full text of Code Titles 6.2, 18.2, 54.1 and 59.1 and found no licensing, registration or bonding statute for private collection agencies. The one general rule found: an agency may refer a debt to an attorney only with the creditor's approval of the referral and the fee. Other titles were not searched. |
| UNK:VA-18VAC-prior-version | VA:18VAC135-20-180(A)(1), (B)(1)(b), (B)(1)(b)-tenant-consent, (B)(2)(b), (B)(4), (C)(2) | The repealed text was recovered from Va. Reg. Vol. 42 Iss. 14, which prints the repealed section struck through. It matches the LII copy line for line. |
| UNK:VA-1209F-threshold | VA:55.1-1209(F)-2027 (effect rewritten; `exemption_quote` added) | The text is determinate. Four units is not "fewer than four", and the second clause reaches only interests in "more than four". So a landlord that owns exactly four units is not exempt. The unusual drafting is a policy gap, not an ambiguity. |
| UNK:VA-accrual | VA:8.01-230 | A contract claim accrues when the breach occurs, not when the damage is discovered. Each unpaid rent installment is breached on its due date. |
| UNK:VA-manufactured-home-lot | coverage 7 `decided_out`; section_table row | OUT. Ch. 13 governs renting a lot in a park of 5 or more homes, where the tenant owns the home. That is not a move-out from a dwelling unit. If lot rentals are ever added, 55.1-1302(E) and 55.1-1311 import 1226 and other ch. 12 sections. |

Three more were narrowed but stay open: deceased payee, refund method, and 2027 versions (see below).

## Remaining unknowns (13), by closable_by

**counsel** (no controlling authority found; searched the Supreme Court of Virginia and Court of Appeals on CourtListener and vacourts.gov):
- UNK:VA-willful: what "willfully" means in 1226(E). One circuit court opinion, persuasive only, says negligent failure to itemize is not willful (Reed v. Smith, 90 Va. Cir. 220; saved).
- UNK:VA-1-210E-private-acts: read literally, the weekend/holiday rollover covers any act a statute requires. No court has applied it to a private act.
- UNK:VA-early-vacate-termination-date: whether handing back the keys early is "abandonment", which would start the 45-day clock at move-out.
- UNK:VA-business-day: undefined for ch. 12. The only Code definitions found count Saturdays (Title 59.1, chapter-specific).
- UNK:VA-oral-lease-late-charge: 1204(C)(5) and 1204(E) conflict.
- UNK:VA-former-tenant-requests: whether a former tenant can request the 1204(D) statement (and, from 2027-07-01, the 1209(F) statement).
- UNK:VA-mitigation: the residential duty to mitigate exists only by statute, and its content is undefined.
- UNK:VA-deceased-payee (narrowed): the personal representative, or a small-asset successor under 64.2-601/602, is a safe payee (discharge under 64.2-603). Payment to the 1256(B) authorized contact alone is unresolved.
- UNK:VA-wear-and-tear: remains a STANDARD for the operator to judge.
- UNK:VA-2027-versions-existing-leases (narrowed): 1-238 and Berner v. Mills make the amendments prospective. Still open: whether a 2027 rule can override a term of a lease signed earlier (e.g. 1245(G) late fees).
- UNK:VA-damage-insurance-settlement (narrowed): damage insurance is not a "security deposit". Still open: whether the landlord can recover from the tenant a loss the insurer paid, and whether the insurer can (subrogation).

**owner** (a product choice, not a legal gap):
- UNK:VA-cotenant-partial-refund: the law has no partial disposition, so any partial refund needs a written agreement of all tenants.
- UNK:VA-refund-method (narrowed): with multiple tenants, one check to all unless each tenant agrees in writing. With one tenant, no method is set by law.

Each counsel item records a conservative operating position that Owen can adopt while it stays open.

No unknown is closable_by `reading`, `case_law` or `event` any more. Possible later events: DHCD templates under Acts 2026 c. 640 and c. 1105, and any technical amendment.

## Source replacements

- **2026 acts.** The first-pass files mixed struck and inserted words. Fifteen chapters now hold clean enacted text: cc. 353, 354, 624, 640, 722, 723, 783, 784, 844, 1050, 1066, 1105, 1111, 1117, 1118. The mixed files for cc. 353, 624, 640, 722, 783, 784, 844, 1066, 1105 and 1117 were overwritten; cc. 354, 723, 1050, 1111 and 1118 are new.
  - Method: take the LIS `#bill-text` element and remove every `<s>` (stricken) span before reading the text. The only clean-up is collapsing spaces.
  - Each file records its official chapter PDF URL and a cross-check. Paragraphs found verbatim in the saved Code sections: 7 of 8 for c. 1117 (the mixed text matched 3 of 8), 19 of 30 for c. 1105 (mixed 12), 22 of 36 for c. 783 (mixed 20). The misses are titles and enacting lines, sections that were not saved, or paragraphs that another 2026 chapter also amended.
  - The pairs 722/723, 353/354 and 783/784 are identical apart from the chapter and bill labels.
  - Only four atoms quote the acts (the enactment clauses of c. 783, 1105, 1117 and 640). All four quotes verify against the clean text, so no first-pass quote depended on a struck word.
- **18VAC135-20-180** (repealed 2026-04-01): `VA_18VAC135-20-180_pre-2026-04-01.txt`, from the Virginia Register.
- **New statutes:** 1-238, 8.01-230, 64.2-600/601/602/603, 55.1-1300/1302/1311, 54.1-3904.
- **Guidance** (labelled as guidance in each file): Treasury unclaimed-property holder instructions, the how-to-report guide, and the property-code and dormancy chart.
- **Cases:** Berner v. Mills (Supreme Court of Virginia, 2003; controlling on prospectivity) and Reed v. Smith (circuit court, 2015; persuasive only).

## Atoms changed because the first pass was wrong or incomplete

- **VA:55.1-1209(F)-2027**: the first pass flagged the four-unit threshold as unclear. The literal text settles it, and the effect now says so.
- **UNK:VA-2027-versions-existing-leases**: the first pass searched Title 1 ch. 2.1 only for "business day" and missed 1-238, which makes "reenacted" amendments prospective. Added VA:1-238 and VA:case-Berner-v-Mills-2003, and narrowed the unknown.
- **Federal atoms**: six US: atoms (24 CFR 982.313(c)-(e), 966.4(b)(2),(4),(5)) were removed and became US: external references.
  - EXT:HUD-regs, EXT:SCRA and EXT:FDCPA became US: ids.
  - VA:55.1-1201(A)-HUD, VA:55.1-1235(B) and VA:55.1-1209(A)(11) now depend on those ids.
  - The source files US_24CFR_*.txt stay in place for US.json.
- **Escrow before 2026-04-01**: the first pass had no rule for escrow events before that date. The recovered 18VAC135-20-180 carries a rule that 18VAC135-20-181 dropped: a deposit may not leave a lease-required escrow account without the tenant's written consent unless the landlord has become entitled to it. That is now atom VA:18VAC135-20-180(B)(1)(b)-tenant-consent.
- **Version notes**:
  - VA:55.1-1208(C) and the 1204 atoms pointed readers at the mixed c. 722 text; they now point at the clean text.
  - The notes on the act-clause atoms record the re-check.
  - Coverage no longer says that the identity of cc. 723 and 354 is "inferred, not verified".
- **New case walks**: `deceased_sole_tenant` and `lease_signed_before_2027_amendments`.

## Cross-file note

US.json did not exist when this pass finished, so `python3 stage_a_check.py stage-a/VA.json stage-a/US.json` has not been run. VA.json expects US.json to declare:
- US:24CFR982.313(c), (d), (e)
- US:24CFR966.4(b)(2), (4), (5)
- US:24CFR880.608
- US:15USC1692a(6)
- US:12CFR1006
- US:50USC3955

If the federal sibling chooses other ids, rename these in `external_references` and in the dependencies of VA:55.1-1201(A)-HUD, VA:55.1-1235(B) and VA:55.1-1209(A)(11).
