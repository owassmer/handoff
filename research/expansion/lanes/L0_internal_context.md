# L0: Internal context. How Handoff should expand beyond move-out, according to its own record

Lane: internal materials only. No web research. Written 28 September 2026.
Scope question (Owen): once the manager-side move-out property work and the tenant-account settlement are built, how should the company expand?

How to read citations: `path:line` points into the local copies. Short forms used throughout:

| Short form | Path |
|---|---|
| `intent` | research/expansion/context/intent_notepad.md |
| `blueprint` | research/expansion/context/blueprint_notepad.md |
| `SR` | fe/context/playbook_strategy_review.txt |
| `0to1` | fe/context/pm_0_to_1_plan.txt |
| `PEB` | fe/context/public_evidence_brief.txt |
| `spec` | fe/context/deposit_closeout_spec.md |
| `McK` | fe/context/agentic_ai_real_estate.txt |
| `Nay` | fe/context/arxiv_2209.13020.txt |
| `README` | docs/docs/README.md |
| `PB` | docs/docs/01_playbook/Property_Management_Playbook.md |
| `FG` | docs/docs/01_playbook/Field_Guide.md |
| `RS` | docs/docs/02_research/Research_Synthesis.md |
| `ADJ` | docs/docs/Landlord_Tenant_Obligations_Adjudication.md |
| `OM` | docs/docs/02_research/research/operating_model.md |
| `ECO` | docs/docs/02_research/research/economics.md |
| `MP` | docs/docs/02_research/research/market_products.md |
| `AE` | docs/docs/02_research/research/automation_evidence.md |
| `AR` | docs/docs/02_research/research/attachment_review.md |
| `RF` | docs/docs/02_research/research/Review_Findings_and_Resolutions.md |
| `DI` | docs/docs/02_research/research/decision_inventory.csv (by decision ID) |
| `CMP` | docs/docs/02_research/research/competitors.csv (by provider) |
| `BRS` | B_REMAINING_SCOPE.md |
| `FIX` | FIXES.md |
| `BA` | BUILT_AROUND.md |
| `P2` / `P3` | fe/PROPOSAL_2.md / fe/PROPOSAL_3_MOTION.md |
| `code/x.ts` | core/typescript-functions/src/handoff/x.ts |

---

## Summary (read this first)

1. **No internal artifact answers "what after move-out" with a chosen lane.** Every strategic artifact makes expansion conditional on customer evidence the company does not yet have: a paying operator, a renewal, and a second operator reusing the same approach (0to1:8-9, 0to1:86-91; PB:204-220; RS:204; MP:113-122). The record contains no customer interview, no walkthrough result, no quote, no pilot and no payment (README:66; RS:24; PB:234). The build went ahead anyway, by Owen's explicit later choice (intent:101-108). So the gate the plans set before *building* was skipped, but the gate they set before *expanding* still stands and is unmet.
2. **The expansion paths the artifacts actually name**, in their own words: broader maintenance operations (PB:19, PB:218); property takeover and owner onboarding (PB:112, PB:218; MP:91; RS:130); a priced implementation/configuration service (PB:218; FG:136; SR:186-205); renewal/rent-change notice handling and household (roommate) changes (ADJ:65-72; 0to1:20-21; SR:141-152); utility responsibility and account changes (ADJ:71; SR:168); NYC violation/HPD chasing, insurance compliance and repair-to-billing (SR:153-178); commercial lease obligations and recoveries, month-end/trust accounting, associations (PB:113-119; MP:92-93); owning the P&L as an AI-native manager (SR:194-213, rejected later at AR:48); and a reusable rules API, agent tools or evaluation environments (ADJ:13, deferred at ADJ:115). The McKinsey paper adds maintenance, leasing/renewals, asset management and capex as "domains" (McK:230-353).
3. **The strongest internally supported answer:** expand first along the *customer* axis (the same move-out job at more operators, one dimension at a time). Then move into the *adjacent physical-work job for the same buyer*: occupied repairs and maintenance delivery. That path has the most explicit artifact support (PB:19, PB:111, PB:218; RS:125-129) and by far the most code reuse. Roughly two-thirds of the handoff backend is a generic quote → plan → decision → order → visit → report → invoice → payment loop with owner funds; only about a sixth is move-out-specific (§D). The obligation-side adjacencies (renewals, household changes, notice validity) and takeover projects are the credible second options. The first paying operator's funded pain should pick between them, as every artifact says.
4. **What is weak:** every market claim in the record is desk research from a single two-day burst (15-16 September), largely produced by the same pipeline and citing itself. The lane ranking flips three times in about 24 hours (deposits first → readiness first → obligations first → deposits first again) with no new field evidence between flips (§A.1, §E). Founder facts are thin. Connor's background is essentially undocumented, and nothing records capital, time commitment, licensure or ambition (§C).

---

## A. Artifact inventory

Dates come from the artifact text, or from PDF metadata (`pdfinfo CreationDate`) where the text is undated. "Superseded" is judged from the intent notepad's authority rule (intent:8, intent:123, intent:136) and the later artifacts' own statements.

| # | Artifact | Date | Author/origin (as stated) | Purpose | Status / superseded by |
|---|---|---|---|---|---|
| 0 | "Handoff Partnership Playbook" (51 KB markdown, CBS examples) | Before 15 Sep | Supplied by the founders ("attached playbook", RS:24; AR:7, AR:13) | Original thesis: responsibility carried across boundaries; CBS household-change and utility cases | **Not in the source set.** Known only through reviews of it (SR; AR:13; RS:28). Superseded by #1 and #4. |
| 1 | playbook_strategy_review (.txt/.pdf), "First-Principles Strategy Review" | PDF created 15 Sep 2026 17:06 EDT; cites sources up to 8 Jul 2026 (SR:73) | Unnamed reviewer; writes to "the founders" | Venture-shape critique; ranks 6 lanes; D1-D5 partnership models; pricing; 30/60/90; kill criteria | Audited and partly rejected by AR:33-49 and RS:30. Its D5 path was explicitly rejected (AR:48). Still named as a core source by intent:119. |
| 2 | agentic_ai_real_estate (.txt/.pdf) | March 2026 (McK:17) | McKinsey (Wolkomir, Kapoor, Gujral, Stoica; McK:463-464) | Domain-level agentic redesign; four domains; five layers | External secondary source. Its "steps vs thoughts" split is rejected by intent:31, intent:51 and RS:32. Five layers rejected as a build plan (AR:15). |
| 3 | arxiv_2209.13020 (Nay, *Law Informs Code*) | 2023 (Nay:5-20) | John J. Nay, Stanford CodeX | Legal informatics as AI alignment; rules vs standards; fiduciary duty example | Conceptual source for intent §3 (intent:25-34, intent:119). Makes no market claim. |
| 4 | Research package: Playbook, Field Guide, Research Synthesis, research/* (operating model, economics, market products, automation evidence, attachment review, review findings, competitors, decision inventory, workbook, public data, RHFS microdata) | Research cutoff 15 Sep 2026 (README:3; PB:3) | "A practical playbook for Owen and Connor" (PB:3); generator not named. Workbook built with "@oai/artifact-tool" and a "Codex runtime" (README:60) | Broad operating model; readiness as the lead test; economics; competitor inventory; field method | Its readiness recommendation was replaced by #5 (ADJ:9, ADJ:104-115). Its method, operating model, corrections and economics stay in force (ADJ:19-25). Named by intent:120 as a valid source. |
| 5 | Landlord_Tenant_Obligations_Adjudication.md | 15 Sep 2026 (ADJ:3) | Unnamed; revises #4 | Promotes landlord-tenant obligations; deposits and renewals as equal candidates; readiness as the outside comparator | Not in Package_Manifest.json, so it was added after the package. Partly superseded by #9, which restored physical turnover as half the product. |
| 6 | pm_0_to_1_plan (.txt/.pdf), "LANDLORD–TENANT OBLIGATIONS / 0–1 PLAN" | PDF created 15 Sep 2026 23:26 EDT | Unnamed; assigns roles to Owen and Connor (0to1:94-95) | Two-page execution plan: 10 operators, 5 walkthroughs, one workflow, $1,000 pilot, 20 cases | "Open with deposit closeout" (0to1:20) superseded by intent:15 ("not Deposit Closeout"). "No substantial build without case access and a paid commitment" (0to1:44) overridden in practice by intent:101-108. Its expansion rule (0to1:86-91) is not superseded. |
| 7 | public_evidence_brief (.txt/.pdf) | 16 Sep 2026 (PEB:3; PDF 15:11 EDT) | Footer "OWEN + CONNOR" (PEB:44) | First research cohort: 4 prospects plus 2 calibration firms; worked deposit-closeout examples | Prospects are "public leads, not contacted or qualified buyers" (PEB:38). The underlying Public_Evidence_and_Prospects.zip (34 sources, 7 case reconstructions, 12 evaluation seeds; PEB:7) is **not in the source set**. |
| 8 | deposit_closeout_spec.md | 16 Sep 2026 (spec:3) | Unnamed; "Proposed design" (spec:5) | Build spec for NC deposit closeout: case = ending tenancy; six outputs; change loop; Python + React | Superseded as product and as stack by intent:15 and intent:101-102 (Foundry TSv2 backend). Its money, track and action-safety distinctions survive in blueprint §4 (blueprint:194-220). A legacy `deposit_closeout/` module (about 8.5k lines plus 32 test files) still sits in the Core repo beside `handoff/`. I observed it by directory listing only; it is outside this lane's read scope. |
| 9 | Intent notepad, "Handoff — intent and operating model" | Recorded 23 Sep 2026 (intent:5); presentation clarification 25 Sep (intent:76) | Owen's explicit agreements, as recorded | Authority on product scope, principles and implementation direction | **Highest authority on scope** (intent:8). Its "One small Demo indicator" (intent:72) was later overridden by Owen's no-badge rule (FIX:57-58). |
| 10 | Blueprint notepad, "implementation blueprint and current state" | Checkpoints to 26 Sep 2026 (blueprint:4-37); plan v14/16 | Engineering companion to #9 | World model, A-D build plan, acceptance matrix | Status sections stale by design. Design sections (§2-§12) current. C and D are "NOT STARTED" (blueprint:405, blueprint:441). |
| 11 | B_REMAINING_SCOPE.md | 26 Sep 2026 | Ferro (the build agent) | Remaining B scope against the B exit criteria | "Dated record, not authority" (BRS:3). Several items since fixed (FIX status block). |
| 12 | FIXES.md | Status verified 28 Sep 2026 (FIX:7) | Ferro, from the live case at 142 West 88th Street and Owen's reviews | Defect list | Current. |
| 13 | BUILT_AROUND.md | Audit of 28 Sep 2026 (BA:7) | Ferro, with Owen's corrections | Limits and workarounds, and why each exists | Current. |
| 14 | fe/PROPOSAL_2.md | 27 Sep 2026 | Ferro, from "Owen's walk-through with his co-founder" (P2:3) | Second frontend pass | Proposal; parts since built (FIX F11-F18). |
| 15 | fe/PROPOSAL_3_MOTION.md | 28 Sep 2026 | Ferro | Motion and live behavior | "Proposal only" (P3:3). |
| 16 | Backend code, core/.../handoff/*.ts (35 files, 4,433 lines) | Master head 6d96fc1 at read time | Built by Ferro under Owen's direction | The product | Implemented. §D separates implemented, demonstrated and accepted. |

**Artifact count:** 16 rows (17 including the missing original playbook). They are drawn from 56 files in docs/docs, 6 context items (12 files), 2 notepads, 5 workspace documents and 35 code files. **Referenced but missing:** #0 (the original playbook), the public-evidence ZIP, the demonstration case package ("NYC_001 media set", BRS:72) and the old "master/E plans" (blueprint:557).

**PDF twins.** The context PDFs are the sources of their .txt files. For the three docs PDFs (Playbook, Field Guide, Research_and_Operating_Model) I compared section headings and the "Should deposits lead?" table against the .md twins and found no divergence. Research_and_Operating_Model.pdf is the synthesis plus the operating-model appendix (README:15).

### A.1 How the reasoning evolved

1. **Before 15 Sep: from tenant pain to "responsibility across boundaries".** The founders' original playbook grew out of their own CBS (Charlottesville) and NYC resident experiences (SR:77-79, SR:252-253; AR:13). Two earlier theses had already been tried and dropped: the "unit-centric transition layer" and the "student-housing transition case" (SR:136). Earlier rounds defaulted to "August 2027" timelines and a "manual phase first" (SR:17-19).
2. **15 Sep afternoon: strategy review.** A services business with a software wedge. Deposits ranked #1 because they are penalty-backed. D2+D1 now, D5 (own the P&L) at 12 months. $40-75 per case (SR:4-19, SR:172-178, SR:289-302).
3. **15 Sep: research package.** It rejects the review's certainty (AR:33-49) and demotes deposits: "Not a new category … penalties do not prove budget" (PB:115). It makes **vacant-home readiness** the lead test, for an owner-funded buyer (PB:9-13, PB:111). Its economics show readiness only pays if it produces extra paid rent days (PB:170).
4. **15 Sep: adjudication addendum.** Removes readiness as the default. Promotes **landlord-tenant obligations**, with deposits and renewal/notice handling as equal candidates and readiness as the outside comparator (ADJ:9-17, ADJ:65-72).
5. **15 Sep 23:26: 0-to-1 plan.** "Open with deposit closeout. Choose renewal/notice handling instead when actual cases and buying commitment are stronger" (0to1:20-21). "No substantial build without case access and a paid commitment" (0to1:44).
6. **16 Sep: public evidence brief and deposit spec.** Deposit closeout for regional third-party managers of single-family and small multifamily rentals, starting in NC (PEB:5-6; spec:21).
7. **23 Sep: intent.** Owen's synthesis: "The product is Handoff—not Deposit Closeout." Handoff owns the whole move-out, with two outcomes: the property ready for the next occupant, and the departing tenancy's financial relationship resolved (intent:15-20). Marketing and leasing stay out (intent:21). Build now: "one complete working foundation with a real coordinating agent" (intent:103). This merges #3's readiness with #4-#6's obligations and deposit work, and overrides the "no build before a paid commitment" rule.
8. **23-28 Sep: build.** A is complete (blueprint:45). B (physical work) runs substantially on a live demo case: orders, reports, invoices and payments exercised, and the unit reached Ready (FIX:73, FIX:95). C (the tenant account) has not started (blueprint:405; P2:104).

Net effect for expansion: the product scope under construction is the *union* of the two rival first lanes from 15 September (readiness, and deposits/obligations). No artifact ever asked "what comes after move-out". The closest are PB:218-220, 0to1:86-91 and the D1-D5 table (SR:180-213).

---

## B. Direction reasoning, exhaustively

### B.1 Hypotheses about what the company is

| # | Hypothesis | Where | Later treatment |
|---|---|---|---|
| H1 | "Responsibility carried across organizational boundaries to a verified conclusion" is the core. It is "a services business with a software wedge, not a venture-scale SaaS company" | SR:4-6, SR:136-139 | The research kept "A bounded operating result, with software behind it" (RS:201) and dropped the venture conclusions (AR:14). |
| H2 | "The gap between AI use and AI completion is the wedge" (only 8% fully automated) | SR:9-12, SR:71-76 | Rejected as a structural inference: "Do not infer task capability, 92% addressability or a permanent services niche" (RS:40; AE:25; ECO:140). |
| H3 | Mission: "keep homes working and ready to live in, without constant chasing" | PB:7, README:11, PB:228 | Not revoked. The intent's two outcomes fit inside it (intent:16-17). |
| H4 | "The broad company thesis is to operate a recurring property responsibility with AI and a smaller amount of necessary human coordination" | RS:123 | Not revoked. The most general expansion statement in the record. |
| H5 | "Can we serve a specific customer's operating need better than its feasible alternatives?" replaces "nobody has built the connective software" | RS:115; MP:7-9 | Not revoked. |
| H6 | Legal informatics is central: consistent logic for determinate rules, adaptable reasoning for standards | intent:23-34; Nay:65-110; ADJ:59 | Owen's chosen thesis. It governs design, not market choice. |
| H7 | The right unit is "an obligation or outcome that joins several decisions" | RS:53; ADJ:21 | Adopted in the world model: Obligation is an "AGREED core object" (blueprint:120-122). |
| H8 | A reusable rules API, agent tools or evaluation environments may later be products | ADJ:13 | "not established buyers or revenue streams today". Deferred "until repeated demand supports them" (ADJ:115). |
| H9 | Durable advantage comes from reliable delivery through the operator's systems, reusable policies, integrations, vendor knowledge and trust. Data or learning moats are conditional | PB:224-226; MP:122; RF:15; McK:414-431 | McKinsey argues for owning the learning loop (McK:418-431). The research treats that as unproven (RF:15; PB:98). |

### B.2 Every candidate lane or expansion path named, and how each was ranked

**Strategy review ranking**, by "frequency × economic stake × delegability × low incumbent overlap × speed to first dollar" (SR:172-178):
1. Deposit disposition/compliance closeout (VA 45-day, NY 14-day). "Rank: #1" (SR:159-167).
2. Roommate-change closeout (student). "strong wedge, low ACV" (SR:141-152).
3. Utility transfer/verification (SR:168).
4. NYC HPD/violation and super coordination (SR:170).
5. Repair-to-billing closeout. "weaker; crowded and variance-heavy" (SR:153-157).
6. Insurance compliance chasing (SR:169).
Also named: vendor invoice reconciliation and owner-reporting escalation, which "overlaps APM Help" (SR:171).

**Playbook candidate table** (PB:108-119). The selection tests were "a comprehensible result, an observable deadline, enough connected decisions for AI to matter, and a plausible owner budget". The playbook states this was "not … a weighted scoring exercise with invented precision" (PB:121).
- Leasing and routine resident communication: strong competition (PB:110). Now also outside Handoff's scope (intent:21).
- **Maintenance and vacant-home readiness: "Preferred first test"** (PB:111).
- **Property takeover and owner onboarding: "Strong second offer when a partner has regular takeovers"** (PB:112).
- Month-end accounting and invoice control: mature competition (PB:113).
- Commercial lease obligations and expense recoveries: "Promising separate vertical" (PB:114).
- Deposit administration: "Not a new category … penalties do not prove budget" (PB:115).
- Household changes: "Volume, manager responsibility and willingness to pay are unproved" (PB:116).
- Utilities and insurance administration: "modest incremental value" (PB:117).
- Violations, claims and capital projects: "Attractive with a specialist partner" (PB:118).
- Association governance and reserves: a distinct buyer (PB:119).
- Student housing: "a different capacity problem and a poor year-round revenue assumption" (PB:125).

**Market-products ranking**, an "independent practical hypothesis" (MP:86-95):
- Turn readiness and maintenance delivery with spending authority: **First test** (MP:90).
- Portfolio takeover and owner onboarding: "Strong alternative when distribution is through acquisitive operators" (MP:91).
- Commercial lease obligations and recoveries: "Potentially valuable, specialist-led" (MP:92).
- Financial month-end and trust reconciliation: "Good business for a finance-operations team; weaker solo-builder first wedge" (MP:93).
- Staff coverage and resource allocation: "Part of the delivery model, not first standalone product" (MP:94).
- Household changes and deposit disposition: "Do not default here" (MP:95).

**Research synthesis "could beat turns" table** (RS:127-133): occupied maintenance ("more frequent", RS:125), takeover/onboarding, month-end/financial operations, commercial obligations and existing-stack implementation. Each has a stated condition and the measurement needed.

**Adjudication candidate roles** (ADJ:65-72): deposit disposition is the "Technical reference case and commercial candidate"; renewal/rent-change notice handling is an "Equal commercial candidate"; utility responsibility and account changes is an "Adjacent operational case"; vacant-home readiness is the "Outside comparator".

**0-to-1 plan** (0to1:19-24): deposit closeout first, or renewal/notice handling if its evidence is stronger. "Do not build both workflows."

**Explicit statements about expanding after the first workflow** (the core of this question):
- "The company can grow into broader maintenance operations if the same capability delivers recurring value. It does not need to become a property-management platform, acquire properties or buy management companies to test that proposition." (PB:19)
- "If turnover is too infrequent but a partner regularly takes on new portfolios, test **takeover and onboarding projects**. If clients pay for configuration but have no ongoing operating need, sell a clearly priced implementation service. If ordinary maintenance offers more repeatable value, extend there only after measuring its separate workload and economics. These are legitimate businesses; none requires pretending to be subscription software." (PB:218)
- "Do not expand merely because the operating map contains more boxes. Expand when a customer has an adjacent funded problem and the existing capability materially lowers the cost of solving it." (PB:220)
- "Then sell the same workflow to a second independent operator, preferably on the same software and in a similar legal regime. Measure reused logic, evaluations, integrations, and onboarding effort. Expand one dimension at a time. If existing software solves the problem, configure it; if the model-only version performs equally well, simplify." (0to1:87-91)
- "How should it scale? … Reproduce delivery with a second partner before expansion … Service cannot repeat profitably; remain a priced project business or stop" (RS:204).
- "Broaden testing only to resolve a concrete uncertainty." … "If only configuration is valuable, sell configuration. If no funded problem survives the comparison, stop investing in this hypothesis." (FG:134-136)
- "The map should remain broad even when the product is narrow. It reveals side effects and expansion possibilities; it does not require implementing every relationship in software." (RS:71)
- "Breadth is a discovery tool, not an implementation commitment." (OM:192)
- "Expand shared representations when several useful workflows require the same facts." (AE:48)
- "Introduce additional modeling only when a real exception or second workflow needs it." (AE:98)
- Day 90: "a decision on whether to expand lanes, add partners, or begin the D5 owned-P&L pilot" (SR:262-263). "$5M ≈ 40–80 partners or a few enterprise books + multi-lane expansion" (SR:237-238).
- "Product expansion: Defer nationwide compilation, a general-purpose DSL, and separately sold agent-training environments until repeated demand supports them." (ADJ:115)
- "Marketing and leasing remain separate. Handoff is not automatically a replacement for every function of a property-management business or every system that business uses." (intent:21)
- "Handoff owns the operational record for its job … Neither a particular PMS's schema nor a full PMS replacement is assumed." (intent:104)
- "Begin with one coordinating agent per Handoff … Do not start with a digital departmental hierarchy of independent agents." (intent:105)
- "Email and document exchange are the first channels; the model remains capable of supporting messaging and phone later." (intent:106)

**McKinsey domains** (McK:230-353): maintenance and facilities ("dispatch to done"); leasing and renewals; investing and asset management; construction and capital expenditures. Three futures: "New operating systems emerge", "Coordination layers quietly disappear", "Value creation gets harder" (McK:356-431). McKinsey expects some players "to bundle software and service delivery into a single operating system offer" (McK:429-431).

### B.3 Business-form options (partnership architecture)

The strategy review's D1-D5 table (SR:180-196):
- D1, delegated operator for PM companies: fast, medium ceiling. "Founder fit: High — quant/AI + ops".
- D2, AI implementation/configuration partner for incumbents: "Fastest (days–weeks)". Founder fit "Very high". High platform dependency.
- D3, broker trigger partner (NYC): low to medium.
- D4, white-label or co-sell with a point vendor: medium.
- D5, own the P&L (AI-native PM firm or roll-up): slow, "Highest" ceiling. Founder fit "High if paired with capital".

Its recommendation: "Run D2+D1 concurrently now … hold D5 as the 12-month option" (SR:211-213).

How later artifacts treated it:
- D5 rejected: "Owning a management firm is the natural next step → Outside the user's established partnership scope and unnecessary to test the company. Compare owner-operators as customers; do not prescribe buying their businesses" (AR:48). See also PB:19.
- AE:124-130 keeps three delivery shapes open: software, managed operation, and redesigning the partner's operation. "No source here establishes which is best for Owen" (AE:130).
- PB:218 accepts implementation services and project businesses as "legitimate businesses".
- Licensing: Handoff "must operate as the manager's delegate under the manager's license" (SR:49-53, SR:132-135). This was corrected: "Contractual delegation does not itself satisfy licensing or employee-specific exemptions" (AR:45; RS:44; FG:94).

### B.4 Economic models and assumptions

- **Strategy review scenarios** (SR:228-236). Service-heavy: $50/case, 30-40% gross margin. Hybrid: $45/case or $2/door/month, 55-65%. Software-led: $1.25/door/month, 70-80%. ACV about $22k-75k at 1,500 units and $75k-250k at 5,000 units. It assumed "~1 case/unit/yr" (SR:230), which AR:44 corrected. ARR paths: "$1M ≈ 15–25 mid-size partners … $20M requires either enterprise multifamily penetration … or the D5 owned-P&L flip" (SR:237-239). "PM-software TAM is modest — ~$6.5B in 2026 per Mordor Intelligence" (SR:280).
- **Turn scenario** (RS:147-168; ECO:118-134; RF:17-27). 1,000 units, 35% turnover, 29.17 turns/month, $100/turn, 35 provider minutes/turn. Integrated owner nets +$3,573/month. A fee manager at 8% nets −$1,794/month. Provider contribution $1,780 (61%). Break-even price $38.99/turn; 60% contribution needs $97.47/turn. With no extra paid-rent days the integrated owner loses $2,260/month. Break-even needs 1.1625 extra paid days per turn, and about 14.53 days for a fee manager (RS:168).
- **General work-item (maintenance) scenario** (ECO:91-106). 1,000 units × 0.30 items/unit/month × 70% eligible = 210 items/month, priced at $1,000/month + $5/item. The third-party manager nets −$307/month; the integrated owner-operator nets +$5,825/month. Without owner savings the integrated case falls to −$475/month.
- **Exception tail** (ECO:108-116). 3 routine minutes plus 15% of items needing 20 extra minutes gives 35.4% contribution. At 40% exceptions × 40 minutes, contribution is −$866/month. 60% contribution needs average handling under about 1.9 minutes per item.
- **Payer structure** (ECO:5-11; OM:11-19; PB:150-170). "A property manager is not always the economic beneficiary." Three recovered days across 400 turns is $80,000 of owner revenue against $6,400 of manager revenue at 8% (PB:164). The adjudication softens this: "a fee manager may be the buyer when it directly incurs the administrative cost and captures the improvement" (ADJ:78).
- **Denominators** (ECO:13-70; RS:81-107). 35.3% of units are managed by a management company and 22.0% by an owner-employed manager (RHFS 2024, reproduced). One-unit properties are 82.9% of properties but 31.5% of units. Median maintenance is $1,600 per unit property-weighted, or $1,175 unit-weighted, from a 46.9% valid-response share.
- **Turn frequency** (ECO:72-81). Invitation Homes at 22.8% implies 19 turns/month per 1,000 homes; AvalonBay at 37.2% implies 31. "A 30-day test at a 200-unit customer might observe only a handful of turns … Either combine several properties, extend the period, or use more frequent maintenance decisions for the first test" (ECO:81).
- **Proposed pilot prices.** $1,000 fixed for 20 cases (0to1:34-37); a $2,500-5,000 diagnostic sprint (SR:254); $40-75/case or $1.25-3/door/month (SR:219), corrected at AR:42. The original playbook proposed "$1,800 for 120 cases (=$15/case)" (SR:215).
- **Effort target:** "30% less recurring handling across the manager, you, and Connor combined" (0to1:73-75).
- **Public price anchors** (MP:72-80). Property Meld $1.60-2.00/unit/month plus $1.50 On-Call. RentCheck $1-1.75. LeadSimple $1.35 or $2.99 per door. Vendoroo $3 or $6 per unit with a $400 minimum. OJO $34-45/hour. Buildium $62, $192 or $400.
- **Pricing rule:** "our fully costed delivery floor must sit comfortably below the buyer's conservatively measured value … Do not solve it by assuming that models eliminate almost all human work" (PB:168).

### B.5 Competitor claims relevant to expansion

- Incumbents now sell agents: AppFolio, Yardi, RealPage (Lumina, 10 Aug 2026), MRI, Entrata (MP:7-11). Entrata announced "100+ embedded agentic AI agents" (SR:201).
- The maintenance adjacency is the most crowded: 23 of 37 providers show maintenance coverage (market_coverage_counts.json). The closest comparator is Vendoroo, which coordinates the customer's own vendors; its Command tier adds owner approvals and human failover (MP:38; CMP Vendoroo; PB:180). Also Lula and Lessen, which own physical delivery (MP:36), plus Latchel, Property Meld TrueCost and HappyCo ("Inspection-to-maintenance-to-spend is already a specialist expansion path", CMP HappyCo).
- The tenant-account adjacency: Obligo's Deposit Agent, announced 15 Jun 2026 with availability unverified (MP:46; ADJ:47); Rentable (ADJ:47); RentCheck AI Damage Assist and deduction reports (CMP RentCheck); Proper, a staffed AI accounting service that includes move-in/out accounting (CMP Proper); Zego deposit payouts (CMP Zego).
- Renewals and notices: Blue Moon, EliseAI, LeadSimple and native PMS tools (ADJ:49; CMP).
- Takeover and onboarding: LeadSimple owner onboarding (MP:48). Only 3 of 37 providers are coded for owner onboarding (market_coverage_counts.json). The record warns this is "not evidence that lower-count categories are underserved" (MP:30).
- Accounting: APM Help, OJO, Proper (MP:40). Utilities: Conservice, Zego, Second Nature (MP:42).
- Precedents on business form: Long Lake and the Creation Fund, Doorstead, Belong, PARES AI, Lette AI, Rely (SR:111-118), against the Fortune/Air Street critique (SR:39-44).
- "Deposits are not a protected gap" (MP:46). "A new company cannot justify a premium merely by consolidating tasks into a queue" (MP:48).

### B.6 Kill, pivot and continue criteria

- SR:281-287. Kill the delegated-service thesis if, after 5-8 reconstructions, managers "cannot name a case type they will pay >2× fully-costed delivery for, or refuse written delegation". Pivot to D2 if they pay for configuration but won't delegate. Pivot to D5 if execution quality is the moat and a Charlottesville student book is acquirable. "Leave if neither WTP nor reuse appears by ~90–120 days across ≥3 partners."
- PB:208-216, the continue/change table. Change course when: "Only residents benefit and no responsible buyer funds improvement"; "The constraint is mainly unavailable trades, capital or market demand that this service cannot change"; "We are responsible for outcomes without access, decision rights or practical control"; "Existing configuration or a specialist provider solves it more cheaply"; "Economics depend on free founder labor, optimistic exception rates or unearned rent gains"; "Each deployment requires rebuilding the service and integration from scratch".
- FG:132-136: continue if the customer wants the same responsibility again at a sustainable price and a second deployment can reuse the approach.
- RS:195-204: the recommendation-change table, including "Should deposits lead? … Reopen all lanes".
- 0to1:17, 0to1:24, 0to1:44: advance gates, and "No substantial build without case access and a paid commitment."
- 0to1:69-72: "Unresolved critical errors block the affected capability from live use."
- ECO:151: "Stop or redesign if the work merely moves to a different employee, reductions depend on deferred necessary maintenance, or the proposed buyer cannot capture enough value."
- intent:22: "A technically completed demonstration does not by itself establish customer demand, legal sufficiency, commercial viability or measured economic benefit."
- The strategy review's counter-thesis (SR:271-280). PMs may refuse to delegate funds-adjacent work. The residual work may be low-value by design. "Handoff's insight may be a feature they add, not a company." The founders' pain "is partly a consumer pain (resident experience) with no reliable B2B payer". Or "leave PropTech for a market where the founders' quant/AI edge compounds faster".
- RS:137-141, the counter-thesis on turns: low volume; rent gains may never arrive; an existing coordinator with standing approvals may do as well.

### B.7 Open questions the record names

- "target customer willingness to delegate and pay; actual preventable delay; local supplier availability; integration costs and commercial access; role-specific labor costs; callbacks and quality; founder/operator execution capability; and customer acquisition cost" (RS:210).
- The "question still requiring field evidence" column in RF:7-15, for example "Which work can the founder reach, understand and deliver reliably?" (RF:14).
- The Field Guide's blanks (FG:64-73): frequency, cost, controllable share, buyer capture, alternative, delegation boundary, success measure, price.
- "Who owns the learning loop—the owner, the property manager, the software vendor, or the services provider?" (McK:418-419)
- A repeatable acquisition channel: "A warm introduction is an initial advantage, not proof of a channel" (MP:120).
- Jurisdictions should come "from prospective customers' real footprints … not from founder residence or personal incidents" (ADJ:76).

### B.8 Where artifacts disagree

| Topic | Position A | Position B | Resolution in the record |
|---|---|---|---|
| First lane | Deposits #1 (SR:173; 0to1:20; PEB:5-6; spec) | Readiness (PB:111; MP:90); obligations with deposits and renewals as equals (ADJ:9) | The intent took both halves (intent:15-18). The same-day flip-flop is never explained. |
| Deposits as winner | "Do not substitute security deposits as an assumed winner" (ADJ:9) | "Open with deposit closeout" (0to1:20), written about 8 hours later the same day | Not reconciled. ADJ calls deposits a "technical reference case" (ADJ:69), which may explain it. |
| Build before selling | "No substantial build without case access and a paid commitment" (0to1:44); "Do not prepare a product demo first" (0to1:98-99) | "Build and sell concurrently" (PB:202; SR:300-302); the intent orders a complete foundation (intent:103) | Owen's intent wins by authority. The build happened with no documented case access. |
| Venture shape | Services with a software wedge; D5 as the ceiling (SR:4-8, SR:239-243) | Project and service businesses are legitimate, no need to pretend to be software (PB:218); D5 outside scope (AR:48) | Unresolved. The intent is silent on company form. |
| Who buys | Third-party managers (PEB:5; spec:9) | Owner-operator or an owner-funded budget (PB:11; RS:200) | ADJ:78 allows the fee manager when it bears the admin cost. Unresolved. |
| Human/AI boundary | McKinsey's "automate steps aggressively and protect thoughts deliberately" (McK:118) | No routine-vs-exception system; the agent must reason about the unfamiliar (intent:31, intent:51) | The intent wins. |
| Architecture | Five layers and atomic agents (McK:147-185) | One coordinating agent per Handoff (intent:105; blueprint:92) | The intent wins. |
| Integrate vs own the record | "Start in the manager's existing systems" (0to1:6); "Work through the manager's existing systems" (PB:9) | Handoff owns its operational record, reached through adapters (intent:104) | Compatible in principle. No real adapter has been built yet (§D). |
| Geography | Charlottesville and NYC for access (SR:250-253; PB:125) | NC (spec:21); TX, NC and CO (PEB) | The demo case is in NYC (FIX:3). ADJ:76 warns against choosing by founder residence. |
| Colon v. Martin | Cited for NY double damages (SR:164) | "concerns municipal pre-action examinations" (AR:47; RS:45) | Corrected. |
| Decision family index | 17 families (OM:117-135; README:24) | decision_family_index.csv lists 16; it omits D001-D007, Management mandate | Minor data inconsistency. |

---

## C. Founder facts: documented and not documented

### C.1 Owen

| Fact | Source | Grade |
|---|---|---|
| Co-founder. Leads "product, implementation, evaluation, and the commercial decision" | 0to1:94 | Proposed role assignment in a plan. Not a record of what he does. |
| Is in fact building the whole product himself, through an AI build agent (Ferro), on Palantir Foundry: TSv2 functions, Ontology, Automate, a React/OSDK app | intent:101-108; blueprint:83-94; BA; FIX | Observed in the build record. |
| Prior projects: **CPA** ("quantitative comparisons and repeatable calculations … evaluate them against historical cases"), **CORDON** ("distinguish a requirement, the facts that make it applicable, and whether those facts are actually established"), "**the Palantir work**" ("connect a choice to the action that changes operations"), integration experience ("identities, permissions, stale records and write failures"), and an **SBA lending project** with no material supplied | AR:60-66 | Named in a research note. No project details are in the source set. |
| "From your previous work, retain disciplined evaluation, explicit requirements, reliable calculations and practical integrations. Leave behind architecture that exists only to look comprehensive." | PB:186; RS:191 | Reasoned advice. Implies earlier projects had over-built architecture ("a generalized ontology, a legal compiler, a new operating system", AR:64). |
| "Reuse CORDON's method, not its entire architecture. No general-purpose language, nationwide corpus, or replacement platform." | 0to1:61-62 | Advice. Implies CORDON involved a legal-rules language or corpus. |
| An earlier broader thesis (probably Owen's) is adjudicated: "tokens plus human acceptance", a "100-fold reduction", "bright lines compile, standards do not", "shallow and complete", a "universal legal compiler", a rules API and evaluation environments | ADJ:13, ADJ:55-61 | Inferred from the adjudication. The original thesis text is not in the source set. |
| Intellectual center: legal informatics, rules plus standards, adaptable reasoning; Nay's paper is a core source | intent:23-34, intent:119 | Explicit choice. |
| "Quant/AI" profile; "fast shipping, quant rigor, evaluation discipline"; "founders' quant/AI edge" | SR:183, SR:212-213, SR:279 | Asserted by the strategy review. No evidence given. |
| Working preferences: plain language everywhere; minimality; no caveats or provenance clutter; one multiple-choice question at a time; do the reasoning, don't ask him to invent the model; demo realism | intent:66-75, intent:83-90, intent:124-132; FIX:57-58 | Explicit. |
| Delegates code review and merging; treats the build as reversible "because it is a demo"; rejects safety reasons the agent supplies for itself | BA:25-26, BA:32-34 | Explicit (recorded Owen statements). |
| Revealed preference: **build a complete working agent first**, before any documented customer contact, overriding the plan's "no substantial build without … a paid commitment" | intent:101-108 vs 0to1:44, 0to1:98-99 | Observed behavior. |
| A resident at CBS in Charlottesville and/or in NYC (the playbook's "lived CBS/NYC experience") | SR:252-253; SR:77-79; SR:278 | Asserted for "the founders" jointly. Which founder had which experience is not stated. |
| Personal landlord and family connections exist | 0to1:13-14 ("outside personal landlord and family connections") | Implied. Whose connections is not stated. |
| Handles platform configuration by hand: sets the 280 s function timeout after every release | BA:24; FIX:47-48 | Observed. |
| The frontend branch prefix is `ai-fde/owassmer1/…` | blueprint:516 | Observed string. **Do not infer** an employer or role from it; nothing in the record states one. |

### C.2 Connor

| Fact | Source | Grade |
|---|---|---|
| Co-founder. Leads "introductions, operational walkthroughs, and partner follow-through". "Both attend the first calls." | 0to1:94-95 | Proposed role. |
| Named co-recipient of the playbook and the evidence brief | PB:3; PEB:44 | Observed. |
| Counted in the effort target ("across the manager, you, and Connor combined") | 0to1:73-75 | Implies Connor does delivery work in a pilot. |
| Walked through the product with Owen on 27 Sep. His notes: "black box", "jumpy"; he could not open the app until access was granted | P2:3, P2:87-97; P3:8 | Observed. His first product contact came after the build. |
| Background, skills, industry experience, network and time commitment | — | **Not documented anywhere.** |

### C.3 Joint facts

- "Two-person AI-native team" (SR:212). The "founders' lived CBS/NYC experience" is proposed "as the wedge" (SR:252-253).
- The founders' pain "is partly a consumer pain (resident experience) with no reliable B2B payer" (SR:278). The original playbook's incidents are "selected historical examples" (AR:13).
- Warm leads: CBS, Woodard, Management Services Corporation, KRS, PMI Commonwealth, and "Thomas without establishing his buying authority" (PB:200). Also Wade Apartments (SR:251). "These are conversation leads, not verified qualified prospects or implied introductions" (PB:200).
- Prior theses already tried: a unit-centric transition layer and a student-housing transition case (SR:136).
- Operating constraint on the platform: the Foundry dev tier has a 5-user cap (P2:97).

### C.4 What is not documented, and matters for expansion

- Any operator or property-management work experience. The record only shows the founders as residents.
- Real-estate licensure. This matters because licensing limits what Handoff can do for a manager (SR:49-53, SR:125-135; AR:45) and rules out owning a management business (D5) without a broker.
- Capital, runway, fundraising intent, and full-time or part-time status. The strategy review had a "funding objective" that the research removed (AR:14). That is the only trace.
- Location. Charlottesville and NYC are implied, but ADJ:76 says not to pick jurisdictions by founder residence.
- Ambition and risk appetite: venture scale, a cash services business, or a research agenda. This is the unresolved company-form question in §B.8.
- Whether any walkthrough, prospect call or introduction has happened. None is recorded.
- Owen's relationship to Palantir and whether Foundry is the production platform (cost, customer acceptance). The record calls the build "a demo" (BA:25) and gives no production plan.
- Connor's domain access (the "operational walkthroughs" role implies it, but the record never shows it).

Consequence: any recommendation that rests on "founder fit" rests on Owen's documented building, legal-informatics and evaluation strengths, and on Connor's *assigned* distribution role. The record does not show Connor's reach into operators, and nobody's operating experience is recorded.

---

## D. Capability inventory: what the built system actually does

States used: **Implemented** = code on master. **Demonstrated** = observed on a real Foundry case run (the live NYC demo case or isolated test cases). **Accepted** = Owen approved the behavior as an operator (B.9/D.5). Nothing reaches a live external party: every write requires `workspace.mode === "demo"` (code/records.ts:50), and legacy correspondence also refuses any other mode (code/correspondence.ts:18).

### D.1 Records (world model)

- **Implemented types (19):** Workspace, Property, Party, Tenancy, Agreement, Obligation, Handoff (case), Document, Work plan, Decision, Message, Agent work, Activity, Job, Inspection, Quote, Invoice, Owner funding, Provider payment (code/records.ts:1-18; blueprint:523-538, blueprint:77).
- **Designed but not built:** Account, Account item, Account entry, Payment on the tenant account, Dispute, Conversation (blueprint:144-170; C.1 "NOT STARTED", blueprint:405-412).
- Generic or specific: all types except Tenancy and the notice fields are generic to any property job with parties, agreements, obligations, documents, quotes, work and money. Obligation is a first-class, generic object (blueprint:120-122), but today it is only captured from the notice and shown to the model (code/notice.ts:97-108; code/coordinateReasoning.ts:135). Nothing computes or tracks obligation performance yet (the demo case holds one obligation, BRS:17).
- Scale limits sized for one showcase case: `bounded()` reads at most 100 related records and fails loudly past that (code/records.ts:64-69). The Handoff list shows the first 25 cases (code/readWorkspace.ts:14-18). An access change rewrites every record in the workspace, up to 5,000 (code/team.ts:21-22). Owner funds are per property (code/coordinator.ts:60). A provider's jobs are read across the whole workspace, capped at 100 (code/counterparts.ts:214). A portfolio-scale product (many units, many open jobs) needs these reworked.

### D.2 Agent loop

- One coordinating turn per call. It is a deterministic priority ladder (recognize source records → owner funds → accepted earlier work → payment results → due vendor replies → reminders → completion checks → delivered visits → booking → funding bind → advances → invoice payment → ordering accepted work), and falls to model reasoning only when no deterministic step is due (code/coordinator.ts:105-259).
- Model reasoning: GPT-5.2 via the Foundry proxy (blueprint:236). Two tools, `readDocuments` and `quoteCosts`. A JSON-schema output of summary, proposal, requests and propertyReady. The server checks rules with named validation codes (copy, pricing, sources, requirements, existing work, request validity), allows up to 4 corrections, 40 tool calls, 16,000 tokens and 230 s (code/coordinateReasoning.ts:17, 49-66, 98-290; BA:17).
- Generic or specific: the machinery is generic. The *instructions* are move-out-specific ("You coordinate one Handoff: a move-out and property turnover", code/coordinateReasoning.ts:49), as is the readiness gate (the tenancy must be ending and every condition Satisfied, code/coordinator.ts:356-364). The model can only *request* (Quote, Information, Funding) and *propose*. Ordering, paying and completing are code (code/coordinator.ts:207-227).
- Durable waiting: Agent work stores status, nextWakeAt and business time. Automate workers resume it (code/clock.ts; blueprint:519-520). The case clock compresses waits (code/clock.ts:6-29).
- Status: **Implemented and Demonstrated**. On the live case (142 West 88th Street) it produced plans, orders, reports, invoices and payments, and brought the unit to Ready (FIX:73, FIX:95). Operator acceptance is **partial**: Owen accepted repair plans on the live case (FIX:59-61), but the formal B.9 check was "Not demonstrated" as of 26 Sep (BRS:29) and FIX records no later completion. Known open defects: B22 (two turns can run at once), B26, B27, B28, F19 (FIX:8-23).

### D.3 Checks (deterministic logic)

- Exact minor-unit money and BigInt arithmetic; quoted-line pricing identity; budget ≥ estimate; budget capped at available owner funds (code/proposal.ts; code/quoteCosts.ts; code/coordinator.ts:332-337).
- Funding position: a commitment is counted once, not again when paid; unknown payment outcomes keep funds held; existing commitments cannot exceed confirmed funds (code/funding.ts:15-39).
- Idempotency: stable identities from content digests; replays produce zero edits; "Same identity with changed content is not a retry" (code/deliveryRecords.ts:91-111; code/values.ts:77-81; blueprint:9).
- Decision binding: acceptance is bound to exact content and revision; the material basis is fingerprinted, and a stale basis blocks ordering (code/workPlans.ts:31, code/workPlans.ts:114; code/proposal.ts:67-68; code/coordinator.ts:212, code/coordinator.ts:223).
- Access: workspace readers, work/decide/admin grants, a server-bound actor; records must share the reader list (code/records.ts:25-61; code/team.ts).
- Source protection: original files need a live media-access check; Prepared vs Original distinctions are kept (code/originals.ts; code/sourceAccess.ts).
- Copy checks keep IDs, cents and shorthand out of operator text (code/coordinateReasoning.ts:143-155).
- Generic or specific: **all generic.** Nothing here is tied to move-out.

### D.4 Money

- **Implemented:** owner funding recognized from a confirmation document; provider advances and invoice payments requested against accepted jobs; payment observations (Settled, Failed, Returned, Confirming) with rules against duplicates and double counting (code/funding.ts:71-203).
- **Not implemented:** anything on the tenant account (charges, deposit application, refunds, statements, collections, disputes). That is all C (blueprint:405-440). P2:104 notes the UI shows move-out accounting "Not started". The old `deposit_closeout/` module (charges, money, statements, interim accounting) exists beside it but is not wired into Handoff.
- **Counterpart:** payments are answered by a test "payment service" whose behavior (Settle, Reject or Uncertain) is authored in the funding document (code/supportingSources.ts:23-26; code/providerDelivery.ts:131-147). There is no bank or PMS adapter.
- Generic or specific: provider-side money is generic to any owner-funded work. Tenant-account money is specific to the ending tenancy, although the blueprint's Account model is written generically (blueprint:144-158).

### D.5 Correspondence

- **Implemented:** outgoing requests (quote, information, funding, booking, invoice, progress) and incoming replies saved as email-like messages with greeting, body, sign-off and attachments (code/email.ts; code/inquiries.ts; code/counterparts.ts). The operator conversation gets saved replies (code/coordinator.ts:83-93).
- **Counterparts are test implementations:** vendor replies are computed from authored "Provider information" documents (services, lines, availability, durations, effects on named conditions). Owner and contact replies can only disclose documents attributed to that party (code/inquiries.ts:60-120; code/counterparts.ts:117-179). No real email is sent or received. That matches intent:103 ("test implementations of external interfaces") and blueprint:291 ("Live connector activation … remain[s] separate").
- Generic or specific: generic to any multi-party job.

### D.6 Scheduling and physical delivery

- **Implemented:** visit booking from vendor availability and existing appointments; multi-day work in working-day windows (code/counterparts.ts:94-113; code/wording.ts:3-55). An advance must be paid before booking. Reports become Inspections with per-line findings. A completion check turns a job into Complete, Needs attention or Awaiting check (code/delivery.ts:153-186).
- **Simulated:** physical work itself. `performService` flips condition states according to the vendor's authored effects (code/providerDelivery.ts:28-46, code/providerDelivery.ts:48-129).
- Generic or specific: generic to repair, cleaning, assessment and verification work anywhere. The four service kinds (code/supportingSources.ts:9) cover most maintenance jobs. Emergency triage, access coordination with an occupant, and recurrence are **not** implemented.

### D.7 Share of the backend that is move-out-specific (by bytes of handoff/*.ts)

| Group | Files | Share |
|---|---|---|
| Move-out entry and prompt (notice.ts, receiveNotice.ts, workDetails.ts, coordinateReasoning.ts) | 4 | 17% (and most of coordinateReasoning.ts is generic machinery) |
| Coordinator loop (generic sequencing; a move-out readiness gate of about 10 lines) | 1 | 10% |
| Generic work-delivery domain (delivery*, funding, quoteCosts, proposal, workPlans, acceptedWork) | 9 | 27% |
| Test counterparts: simulated vendors, owner and payment service (counterparts, providerDelivery, inquiries, supportingSources) | 4 | 16% |
| Generic platform (records, values, activity, clock, email, wording, team, originals, sourceAccess, sourceRecords, documentIntake, readWorkspace, contracts, conversation, recommendationValidation) | 15 | 21% |
| Legacy A-era code (reasoner.ts single-shot recommender plus the model client that is still used; correspondence.ts demo acknowledgment) | 2 | 9% |

So roughly **60% is generic and directly reusable** (delivery domain, platform, most of the coordinator), **16% is simulator** (reusable as a test harness, but a live product must replace it with real adapters for every path), and **about 15-20% is move-out-specific** (the notice schema, tenancy loading, prompt and readiness gate). This is a line-and-byte estimate, not measured porting effort.

### D.8 Reuse estimate for each expansion path the artifacts name

Reuse = the share of *today's* handoff backend that the path would use largely as-is. "New" = what the path needs that is not built. Every live path also needs the real adapters (email, vendor, bank/PMS) that nothing has yet.

| Path (source) | Reuse | What is new | Notes |
|---|---|---|---|
| Same move-out job at more operators (0to1:86-91) | ~100% of logic | Real adapters; per-operator policy and owner instructions as data; portfolio-scale limits (D.1); C (tenant account) | "Expand one dimension at a time." |
| Occupied repairs and maintenance delivery (PB:19, PB:218; DI D051-D061) | High (~65-75%): quotes → plan → decision → order → booking → report → completion check → invoice → payment → owner funds | Resident-originated intake instead of a move-out notice; emergency triage (D051); access with occupants (D057); tenant-caused cost allocation (needs C); recurrence and callbacks (D060); standing approvals and spending bands (PB:90; AE:75-76), because today every plan needs an acceptance | Most crowded category (§B.5). Economics are negative for a fee manager in the model (ECO:91-106). |
| Vacant-unit turns at portfolio volume, make-ready (MP:90) | ~90% | Cohort view, many concurrent cases, vendor capacity across units | Same product, different scale. |
| Tenant account settlement (the C premise) | Low in handoff/ (party, agreement, obligation, document, decision, activity); the old deposit_closeout module may cover charges and statements | Accounts, items, entries, disputes, collections, statements (blueprint C.1-C.10) | The question assumes this is built. It is not started. |
| Renewal / rent-change notice handling (ADJ:70; 0to1:20-21; DI D082-D084) | Moderate on records (~30-40%): tenancy, agreement, obligation, parties, documents, correspondence, decisions | A versioned rule library and deadline calculators (designed at blueprint:255-263, not built); notice generation and delivery proof; PMS writeback; the licensing limit on negotiating for another (SR:126-131) | Owen's legal-informatics interest fits. The physical-delivery half does not apply. |
| Household or roommate changes (SR:141-152; PB:116; DI D043) | Moderate. The notice already distinguishes "Occupant departure" from "Tenancy ending" (code/notice.ts:10, code/notice.ts:110-111), but readiness is gated to "Tenancy ending" (code/coordinator.ts:361) | Account carry-forward between residents (C); consent and signature collection; lease amendment | Student segment; seasonal (PB:125). |
| Takeover and owner onboarding (PB:112; MP:91; DI D008-D014) | Low to moderate (~25-35%): parties, agreements, obligations, documents and originals, access grants, decisions | Balance and deposit reconciliation (C-like), credential inventory, open-work dedupe (D012), vendor contract continuity (D013), notices (D014) | Project revenue; needs acquisitive customers. |
| Implementation and configuration partner for incumbents (SR:186-205; PB:218) | Near zero code reuse unless delivered on Foundry. Knowledge reuse only | Incumbent-specific configuration skills (AppFolio, LeadSimple and others) | Foundry-built code does not configure AppFolio. |
| NYC violation/HPD compliance chasing (SR:170; DI D063, D089) | Moderate (~40-50%): obligation with due date, jobs, inspections, correspondence | Agency data intake; certification of correction; deadline rules | Fits the NYC demo world. |
| Insurance, casualty and restoration (DI D089-D094; OM:104) | Moderate (~40-50%) | Claim lifecycle; insurer as a party; temporary housing | Physical-work loop reusable. |
| Capex and projects (McK:331-353; DI D064-D066) | Moderate to high (~50-60%): bids on the same inclusions, milestones, invoices against scope | Change orders, milestone acceptance, retainage | McKinsey domain. |
| Utility transfer and verification (SR:168; ADJ:71) | Low (~15-25%) | Utility account adapter; meter readings | External-party control (PB:117). |
| Month-end and trust accounting (PB:113; MP:93) | Low (~15-20%): exact money, idempotent observations | Ledgers, bank reconciliation, owner statements | "weaker solo-builder first wedge" (MP:93). |
| Commercial lease obligations and recoveries (PB:114; MP:92; DI D108-D109) | Low to moderate (~25%): agreement and obligation model | Clause abstraction, CAM reconciliation calculators | Specialist-led. |
| Rules API / evaluation environments / legal informatics layer (ADJ:13) | Pattern-level only: named validation codes and checked rules | A maintained rule and guidance library (not built), APIs, customers | Deferred by ADJ:115. |
| Own the P&L as an AI-native manager (SR:194-213) | All of it, internally | A brokerage license, capital, staff, leasing (which the intent excludes) | Rejected at AR:48. |

### D.9 Evidence of quality and cost the build has produced

- Tests: backend 1,422 passing with 5 existing skips, of which 315 are Handoff tests; frontend 945 (blueprint:8, blueprint:16). Those counts are from 25-26 Sep; later releases added tests (FIX), and the current count was not re-run for this report.
- A full case exercised end to end on the physical side: every job complete and paid, unit Ready (FIX:73, FIX:95).
- Real-model failure modes are documented and tied to their causes (FIX B21-B25; BA A1-A6), including an arbitrary 4-request cap that silently shrank plans (BA:13; FIX:135-146).
- **Not measured anywhere:** per-case model cost, human minutes per case, time to onboard a new case world, or accuracy against a reference set. These are the numbers the economics sections say decide viability (ECO:112-116; PB:168; 0to1:81-83).

---

## E. Evidence-quality audit

Grades: **M** = measured or primary-sourced (a reproduced calculation, a statute text, the operator's own filing, observed code or runs). **S** = secondary-sourced (vendor marketing, a survey reported by others, consultants). **R** = reasoned (arithmetic or argument from stated assumptions). **A** = asserted (no support given). **I** = inherited from an earlier artifact with no new evidence. **F** = founder decision (authoritative for scope, but not evidence about the market).

| # | Load-bearing claim | Where | Grade | Flags |
|---|---|---|---|---|
| 1 | Software is installed but execution is incomplete; only 8% fully automated a process | SR:21-25, SR:71-76 | S (Buildium vendor survey) | The strategy review over-read it. Corrected by AR:39, RS:40, ECO:140. Downstream claims built on "the 8% gap" are void. |
| 2 | CBS/NYC experience is representative of the market | SR:21-25, SR:252 | A | Corrected: "No representative sample is supplied" (AR:37). Origin is the founders' own resident experience. |
| 3 | Deposits rank #1 because penalties are quantifiable | SR:159-167, SR:289-291 | A, with statutes (M) as inputs | "Penalty exposure is not willingness to pay or expected loss" (AR:42). The Colon v. Martin citation was wrong (AR:47). Deposits nonetheless came back in 0to1:20, PEB and spec, then as half of the intent. **Anchoring**: this idea survived its own refutation. |
| 4 | Pricing: $40-75/case or $1.25-3/door/month; 2-5 minutes of verification; 55-65% margins; first $10k in about 30 days | SR:17, SR:219-236, SR:295 | A | Rejected at AR:42-43, AR:49. Nothing replaced it with measured prices. |
| 5 | A fee manager captures little of the readiness value; owner-funded buyers are needed | PB:11, PB:164; ECO:5-7, ECO:118-134 | R (arithmetic on assumed inputs) | Sound logic. Its inputs (3 recovered days, 60 minutes saved, 35 provider minutes) are assumptions (RS:147-158). ADJ:78 weakens it for obligation work. |
| 6 | Readiness break-even needs about 1.16 extra paid days per turn | RS:168; RF:27 | R | Independently recomputed (ADJ:33-41). Useful as a falsification test; no field value exists. |
| 7 | RHFS: 35.3% of units under management companies, 22.0% owner-employed | RS:91-97; ECO:44-56 | M | Reproduced against Census controls (ECO:34). Describes the stock, not buyers (RS:99). |
| 8 | 19-31 turns per month per 1,000 homes | ECO:72-81 | M (operator filings) | Two institutional portfolios; not a range for small managers. Turn volume, which limits a move-out-only business, is under-measured for the target segment. |
| 9 | Maintenance is a material expense ($1,600 median per unit, property-weighted) | RS:103; ECO:62 | M (RHFS, 46.9% valid responses) | Says nothing about avoidable cost (RS:107). |
| 10 | General maintenance model (210 items/month): fee manager −$307, owner-operator +$5,825 | ECO:91-106 | R | Every input is hypothetical ("neither effect is yet proven", ECO:93). It is the only model of the leading expansion lane. |
| 11 | Competitor coverage (38 entries; AppFolio read-only API; Rent Manager read/write; Vendoroo prices; Obligo deposit agent) | MP; CMP; market_source_audit.csv | M for what vendors publish; S for capability claims | "Documented coverage, not actual performance" (RS:113). Dated 15 Sep 2026 and likely to go stale fast (RealPage on 10 Aug, Entrata on 15 Sep; MP:11). |
| 12 | Readiness is the best first lane | PB:111; MP:90 | R | "It is not objectively established as the best lane" (RS:125). Replaced within hours by #13. |
| 13 | Landlord-tenant obligations should be primary; renewals equal to deposits | ADJ:9-17, ADJ:65-72 | R | No new field evidence beyond #12. Same day, same pipeline. **Circular**: it adjudicates its own package. |
| 14 | Move-out = readiness + financial resolution as one product | intent:15-20 | F | Owen's synthesis. The union of #12 and #13. Neither half has buyer evidence. |
| 15 | "Maintenance and readiness" as one candidate; the company "can grow into broader maintenance operations" | PB:19, PB:111 | R | The best-supported expansion statement, still desk-only. Maintenance is also the most contested category (23 of 37 providers; Vendoroo is the closest). |
| 16 | Takeover/onboarding is a strong second offer | PB:112; MP:91; RS:130 | R | Conditional on an acquisitive partner. No frequency data. |
| 17 | D5 (own the P&L) has the highest ceiling | SR:194-213 | S (Long Lake, Doorstead press) + A | Rejected as out of scope (AR:48). Needs capital, licensure and leasing, all undocumented or excluded (intent:21). |
| 18 | D2 (implementation partner) is fastest cash and a "Very high" founder fit | SR:186-205 | A | No customer evidence. Conflicts with the Foundry-native build: the code does not transfer (§D.8). |
| 19 | McKinsey: >30% maintenance time savings, 3-7% renewal uplift, >90% faster lead response | McK:249-251, McK:305-309 | S (consultant, no method) | "Keep these as hypotheses to test, not forecast inputs" (AR:31). |
| 20 | The founders' edge is quant/AI, evaluation discipline and fast shipping | SR:183, SR:212, SR:279 | A | Build speed is partly corroborated by the record: A was complete by the 25 Sep checkpoints and B largely running by 28 Sep (blueprint:45; FIX:95), on top of an earlier deposit-closeout build (blueprint:516, blueprint:557). Evaluation discipline is **not yet recorded** for the product. The sources record no held-out case set (0to1:65 asked for one), and model evaluations belong to D, which has not started (blueprint:450-452). |
| 21 | Licensing: Handoff must act as the manager's delegate; D5 needs a license | SR:49-53, SR:125-135 | M (statute text) + R | "Contractual delegation does not itself satisfy licensing" (AR:45). Jurisdiction- and action-specific. No counsel consulted (FG:97). |
| 22 | The build handles the physical move-out loop end to end | FIX:73, FIX:95; blueprint:78 | M (observed runs), on simulated counterparts | Demonstrated against authored vendors and a simulated payment service, not real parties. The formal operator check (B.9) is not recorded as passed (BRS:29). |
| 23 | About 60% of the backend is generic and reusable for adjacent physical work | This report, §D.7 | R (code classification) | My estimate by bytes. Not a measured port. |
| 24 | Proprietary learning is a moat | McK:414-431 | S | Conditional (RF:15; PB:98, PB:226: "Customer records cannot automatically be pooled into a proprietary training asset"). |

### E.1 Structural problems in the direction reasoning

1. **One burst, one pipeline.** Artifacts #1 and #4-#8 were produced between 15 Sep 17:06 and 16 Sep 15:11. They cite and correct each other. The lane ranking flips with no new observation between flips. The record says so itself: "The initial offer was not empirically selected" (ADJ:29-31).
2. **Zero customer contact.** Every commercial claim is desk research (README:66; RS:24; PB:234; AR:49). The 0-to-1 plan's first three moves (a prospect list, three walkthroughs, "Do not prepare a product demo first", 0to1:93-99) have no recorded outcome. The build that followed is a product demo.
3. **Anchoring on deposits and on NYC/Charlottesville.** Deposits were demoted with reasons (PB:115; MP:95; AR:42) and returned without new evidence (0to1:20; spec). They now form half the product (intent:15-20). The demo world is an NYC building (FIX:3), which matches founder residence, the thing ADJ:76 warns against.
4. **Expansion reasoning is inherited, not refreshed.** The only statements about growing past the first workflow (PB:218-220; 0to1:86-91; RS:204) come from 15 Sep and assume a *single* first workflow (readiness or deposits). The intent's merged scope was never re-examined for what it implies about adjacency.
5. **The payer question is unresolved and is load-bearing for the leading expansion lane.** Maintenance and readiness economics are negative for a fee manager in both models (ECO:104, ECO:127). Intent and build do not say who pays.
6. **Circular capability claims.** "Founder fit" (SR:183) and "reuse" (0to1:90) are asserted, then used to justify lanes. The Review Findings caught one case: "A founder-fit judgment could prematurely dismiss finance operations" (RF:14).
7. **Conclusions resting on unknown founder facts:** D5 (capital, license); D1 as a managed service (who does the human work; 0to1:73-75 counts Connor); D2 (incumbent configuration skills); the warm-lead channel (PB:200, "not verified qualified prospects"); and Connor's operating access.
8. **Internal contradictions:** ADJ:9 vs 0to1:20 on deposits; 0to1:44 and 0to1:98-99 vs the build; SR's D5 vs AR:48 and PB:19; the McKinsey human-judgment split vs intent:31 and intent:51; PEB:5 (third-party managers) vs PB:11 (owner-funded).
9. **Stale inputs.** Competitor facts are dated 15 Sep 2026. At least two fast-moving announcements (Obligo's deposit agent, Entrata Pro) were "not verified" even then (MP:11, MP:46).

---

## F. The answer the internal context alone supports

### F.1 A taxonomy of expansion moves

The artifacts mix moves along different axes. Kept apart, there are five:
1. **Customers** (same job, more operators, regions, legal regimes): 0to1:86-91.
2. **Adjacent jobs for the same buyer** (another property responsibility the same operator funds): PB:218-220; RS:127-133.
3. **New segments or buyers for the same engine** (student, commercial, associations, institutional SFR): PB:114, PB:119, PB:125; OM:139-160.
4. **Business form** (software, managed operation, implementation partner, owning the P&L): SR:180-213; AE:124-130; PB:218.
5. **Horizontal technology** (rules/obligation layer, evaluation environments): ADJ:13, ADJ:115; intent §3.

### F.2 Options

**O1. Replicate the move-out job across paying operators (customer axis).**
- What: take the finished move-out product (both outcomes) into one paying operator, then a second independent one "on the same software and in a similar legal regime" (0to1:88).
- Who pays: an owner-operator or a manager with an owner-funded turn budget (PB:11); or a fee manager where it bears the admin and account cost (ADJ:78).
- Why these founders: Owen can build and evaluate; Connor's assigned role is introductions and walkthroughs (0to1:94-95).
- Reuse: about 100% of logic. Needs real adapters (email, vendor, bank/PMS), portfolio-scale limits (§D.1) and C.
- Evidence: every plan's gate (0to1:8-9; PB:204-216; RS:204; MP:113-122) (R). No customer data (A).
- Risks: low turn volume per operator (ECO:81); fee-manager capture (ECO:127); Vendoroo, Lula and Obligo-type substitutes; licensing for funds-adjacent actions (AR:45).
- Falsified by: after 5-8 reconstructions, no operator names a case type it would pay >2× fully-costed delivery for, or it refuses written delegation (SR:282-283); or the second operator needs a rebuild (PB:216).
- Confidence: **high** that the record prescribes this as the next move; **low** on whether it succeeds (no evidence either way).

**O2. Occupied repairs and maintenance delivery for the same operator (adjacent job, physical).**
- What: the same agent loop triggered by a resident or staff repair need instead of a move-out notice: triage, quotes, plan, owner decision, order, booking, report, completion check, invoice, payment. Later, standing approvals for routine work.
- Who pays: the same operator. The economics favor an owner-operator or an owner-funded maintenance budget (ECO:91-106).
- Why these founders: it uses what Owen has already built. The record gives no evidence that either founder has maintenance operating experience.
- Reuse: highest of any path (~65-75%, §D.8).
- Evidence: PB:19 and PB:218 name it explicitly. PB:111 couples it with readiness. RS:125 ("more frequent"). ECO:81 recommends frequent maintenance decisions for early tests. Grade R.
- Risks: the most crowded category (23 of 37 providers; Vendoroo and Latchel directly comparable, MP:34-38); emergency obligations (PB:148; DI D051); the exception tail wrecks margins (ECO:113); fee-manager ROI is negative (ECO:102).
- Falsified by: the operator's existing coordinator or a specialist (Vendoroo, Property Meld) matches the outcome more cheaply in a same-case comparison (FG:46-60); or the workload is mostly exceptions beyond the ~1.9 routine minutes per item that 60% contribution requires (ECO:114).
- Confidence: **medium.** Best supported and most reusable; most contested market.

**O3. Tenancy-change obligations: renewals and rent-change notices, household and roommate changes, notice validity (adjacent job, obligation side).**
- What: apply the obligation and agreement model, plus the tenant-account engine from C, to the other points where a tenancy changes (DI D043, D082-D085).
- Who pays: the operator's leasing and accounting side. Student operators for roommate changes (SR:141-152).
- Why these founders: it fits Owen's legal-informatics center (intent:23-34; Nay; CORDON per AR:62) better than any physical lane.
- Reuse: moderate (~30-40% plus C). Needs the versioned guidance library the blueprint designed but did not build (blueprint:255-263).
- Evidence: ADJ:70 calls it an "Equal commercial candidate"; 0to1:20-21 names it as the alternative; SR ranks roommate changes #2. The playbook doubts household-change demand (PB:116) and MP:95 says "Do not default here". Grade R, and contested.
- Risks: per-jurisdiction rules; licensing limits on negotiating leases for another (SR:126-131); low ACV (SR:152); Blue Moon, EliseAI and PMS-native renewals.
- Falsified by: renewal/notice rework is not a named, funded pain in walkthroughs; or the PMS already completes it.
- Confidence: **low-medium.**

**O4. Takeover and owner-onboarding projects (adjacent job, event-driven).**
- What: when a manager takes on a new owner or building, reconcile leases, balances, deposits, open work, vendors, access and notices (DI D008-D014).
- Who pays: acquisitive fee managers, from a project budget (MP:91).
- Why these founders: records reconciliation and exact money suit Owen's build; Connor's introductions would need to reach growing managers.
- Reuse: low to moderate (~25-35%, higher once C exists).
- Evidence: PB:112 and PB:218; MP:91; RS:130. Grade R.
- Risks: episodic; bespoke migrations; seller cooperation (MP:91).
- Falsified by: the first partners do not take on portfolios regularly.
- Confidence: **low-medium**, contingent on the first partner's profile.

**O5. Change the business form: a managed service or implementation partner (form axis).**
- What: sell Handoff as a delegated operator (D1) with human review, or sell configuration of the operator's existing stack (D2).
- Who pays: the operator, as a setup fee plus a retainer or cohort price (PB:166; SR:254).
- Why these founders: D2 "Very high" founder fit is asserted (SR:183-187), not shown.
- Reuse: D1 reuses everything. D2 reuses knowledge only (§D.8).
- Evidence: SR:211-213; PB:218 ("If clients pay for configuration … sell a clearly priced implementation service"); AE:124-130. Grade R/A.
- Risks: service margins (ECO:116); platform dependency (SR:203-204); drifting away from the agent product the intent defines.
- Falsified by: the kill/pivot triggers in SR:282-287.
- Confidence: **medium as a way to earn early revenue; low as the expansion strategy.**

**O6. Other physical-work domains on the same engine: violation compliance, insurance and casualty restoration, capex and projects (adjacent jobs, specialist).**
- Reuse: moderate to high (~40-60%).
- Evidence: SR:170 (HPD, NYC); PB:118 ("Attractive with a specialist partner"); McK:331-353 (capex); OM:104 (casualty). Grade R/S.
- Risks: specialist expertise, uneven volume (PB:118).
- Confidence: **low.**

**O7. New segments for the same engine: student housing, commercial lease obligations, associations, institutional single-family.**
- Evidence: PB:114, PB:119, PB:125; MP:92; OM:139-160. Grade R.
- Reuse varies: student turns reuse the delivery loop at cohort scale (DI D112); commercial and associations need new obligation calculators and buyers.
- Confidence: **low.** Distinct buyers and decision rights (RS:61-71).

**O8. A horizontal obligation and rules layer (rules API, evaluation environments, agent substrate).**
- Evidence: ADJ:13 ("may subsequently be products, but … not established buyers"); deferred at ADJ:115; intent §3. Grade R.
- Reuse: pattern-level only. No rule library exists.
- Why these founders: the closest match to Owen's intellectual center.
- Confidence: **low** as a next step. The record explicitly defers it until repeated demand exists.

**O9. Own the P&L: an AI-native management firm or roll-up (form axis).**
- Evidence: SR:194-213, SR:285-286 (S/A). Rejected at AR:48; PB:19. Needs a license, capital and leasing, the last of which intent:21 excludes from Handoff.
- Confidence: **very low** on the internal record.

**O10. Leave property management.**
- Evidence: SR:279-280 (A).
- Confidence: **very low.** Named once, never developed.

### F.3 Ranking (internal context only)

1. **O1 (replicate across paying operators).** This is the precondition every artifact sets before expanding sideways. It is the next move, not an alternative to one.
2. **O2 (occupied repairs and maintenance for the same operator).** It has the most explicit support (PB:19, PB:218), the highest code reuse (§D.7-D.8), and the most frequent events (RS:125; ECO:81). The artifacts attach the condition "only after measuring its separate workload and economics" (PB:218).
3. **O4 and O3, tied, chosen by the first operator's profile.** O4 if the partner grows by takeovers (MP:91). O3 if walkthroughs show renewal, notice or roommate rework as a funded pain, which is also the better fit for Owen's legal-informatics work.
4. **O5 as a revenue form**, not a lane: price the work as a managed service or setup plus retainer while O1-O2 are proven (PB:166; PB:218).
5. **O6 and O7** as specialist extensions once a partner brings one.
6. **O8** only after repeated demand (ADJ:115).
7. **O9, then O10.**

The ranking is ordered by internal support × reuse × gate order. It is **not** a market ranking. The record contains no measured demand for any lane.

### F.4 The answer, in one paragraph

The internal record says expansion should follow a paying customer, not the operating map: "Expand when a customer has an adjacent funded problem and the existing capability materially lowers the cost of solving it" (PB:220), "one dimension at a time" (0to1:90). The company has built the move-out product without the customer evidence its plans required, so the first expansion is getting that product paid for and reused by a second operator. After that, the record and the code point most strongly to occupied repairs and maintenance for the same operator. That uses the same agent loop (roughly 60% of the backend is generic delivery and platform code), the playbook names it as the growth path, and it is the most frequent event type. It is also the most crowded and hardest-to-price category, and it only works where an owner-funded budget pays. Tenancy-change obligations (renewals, notices, roommate changes) and takeover projects are the credible alternatives. Pick between them by the first operator's funded pain and by whether Owen's legal-informatics strength or Connor's (undocumented) operator access is the binding constraint.

### F.5 What the internal context cannot answer

- Whether any operator will pay for move-out, maintenance or anything else, and at what price. There is no customer data.
- The actual frequency and cost of each adjacent job for a real target operator (FG:64-73 blanks).
- Current competitor performance and availability after 15 Sep 2026 (Vendoroo, Obligo, EliseAI, the incumbents' agents).
- Connor's background and operator access; either founder's operating experience; licensure; capital, runway and ambition (§C.4).
- Whether Foundry is viable as the production platform for customers (cost, tenancy, 5-user dev cap, P2:97). The record has no production plan.
- The real cost per case of the agent (model spend, human minutes), which decides every margin question (ECO:112-116).
- Whether the tenant-account settlement (C) can be built as specified. It is the stated premise of the question and has not started.
- Which jurisdictions to target. That depends on the first customers' footprints (ADJ:76).
