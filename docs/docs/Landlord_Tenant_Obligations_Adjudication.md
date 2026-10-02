# Landlord–tenant obligations: adjudication and revision addendum

**Research date:** 15 September 2026  
**Applies to:** Property_Management_Research_and_Playbook(1).zip  
**Status:** Revised product hypothesis and research design; not a finding of customer demand. Original package unchanged.

## 1. Decision

Promote landlord–tenant obligation decisions and execution to a primary product hypothesis. Remove vacant-home readiness as the default first business, while retaining it as an alternative against which the new hypothesis must compete. Do not substitute security deposits as an assumed winner.

The proposed capability is to take the governing rules, agreements, and current case facts; determine what is owed, by whom, to whom, and when; and help the operator complete the resulting work through its existing systems. Evaluate the quality of decisions, completion of actions, remaining human work, and economics.

The initial business should be attached to a recurring operational decision family, not to the promise of a universal legal compiler. A reusable rules API, agent tools, or evaluation environments may subsequently be products, but they are not established buyers or revenue streams today.

**Replacement executive recommendation for the playbook:**

> Investigate software that helps residential operators determine and complete landlord–tenant obligations as tenancies change. Compare security-deposit disposition and renewal/rent-change notice handling using actual cases, installed products, and buyer economics. Retain vacant-home readiness as an outside alternative. Select the first paid workflow only when the product improves a recurring decision or its execution, the buyer captures sufficient value, and a second customer can reuse the approach. Work inside existing operating systems where possible; do not assume that delivering useful software requires taking over every connected physical task.

## 2. What survives from the original package

The operating model's concurrent lifecycles, separation of people and agreements, explicit authority, attention to physical work versus accounting completion, and requirement to identify the beneficiary and payer remain useful. The original research already identifies an obligation or outcome joining multiple decisions as a unit of analysis. This is a sharpening of that insight, not its invention.

The corrections to inflated automation statistics, inappropriate causal extrapolations, unsupported legal citations, integration assumptions, and hypothetical margins remain in force. Maximum legal remedies are not expected customer savings. A competitor's marketing silence does not establish inability, and an announcement does not establish general availability.

The original Field Guide is stronger than a simple turns-only plan: it already asks for cross-domain examples, consecutive cases, a competent comparison operator, real-system demonstrations, and total effort. Keep those methods. Change the favored candidates and evaluation design rather than replacing the research with a deposit-only discovery script.

## 3. What the evidence changes

### The initial offer was not empirically selected

The original research explicitly reports no operator interviews, vendor quotes, authenticated property-management-software trials, or live experiments. Make-ready was a plausible lead experiment, not an observed comparative winner. Its illustrative economics also depend materially on whether earlier readiness produces earlier collected rent.

Independent arithmetic from the original baseline reproduces:

| Original illustrative quantity | Result |
|---|---:|
| Monthly turns: 1,000 units × 35% turnover ÷ 12 | 29.1667 |
| Cash-realized labor benefit | $656.25/month |
| Service price at $100/turn | $2,916.67/month |
| Buyer net value with no additional collected rent days | −$2,260.42/month |
| Additional collected-rent days needed to break even | 1.1625/turn |

These calculations do not estimate obligation-product economics. That requires a different event denominator and measured handling, error, support, and maintenance costs.

### The market is not empty

Rentable markets automated deposit collection and refunds, compliance tools, and integrations with Yardi, Rent Manager, and MRI. Obligo announced a Deposit Agent on 15 June 2026 covering requirements, charges, refunds, compliance, and disputes; the announcement describes future availability and early access. The original package already records this announcement and its rollout qualification. It is not a newly discovered omission. [S1, S2]

Blue Moon supplies apartment-association lease forms, electronic execution, portfolio tools, and integrations. Conservice offers resident utility billing, lease review/localized support, and move-in/out data integration. These are competitors or adjacent substitutes, not evidence that every operational obligation is already solved. [S3, S4]

Catala and OpenFisca refute a literal claim that executable legal rules did not previously exist. Avalara's lodging-tax offering also refutes the claim that short-term-rental managers receive no third-party compliance assistance; that does not mean all local zoning or permitting requirements are covered. [S5–S7]

## 4. Adjudication of the broader thesis

**Retain:** reusable domain knowledge; decision-family focus; jurisdictional reuse; a maintained update process; delivery inside the system where a decision occurs.

**Replace “tokens plus human acceptance” with an economic hypothesis.** Drafting is only one cost. Measure interpretation, review, evaluation, customer configuration, integration, maintenance, and case handling. Neither the quoted 100-fold reduction nor a viable end-to-end cost reduction has been demonstrated. Human approval is an input to production, not proof of quality or commercial viability.

**Replace “bright lines compile, standards do not” with differentiated evaluation.** Deterministic calculations, factual judgments, and discretionary decisions need different implementations and tests. A standard can be decomposed and evaluated without pretending it has a unique arithmetic answer. Nay's 2022 research explicitly treats standards as useful for circumstances that cannot be fully specified in advance; Norm describes both decision representations and trained legal engineers using its proprietary LEAP platform. [S8–S10]

**Replace “shallow and complete” with “narrow in purpose, complete for that purpose.”** A deadline answer may depend on occupancy, dates, exceptions, recipients, notice methods, and earlier actions. California's deposit statute illustrates the dependency: it combines a return/accounting period with inspection and dated photography requirements. A move-out system cannot recover a missing move-in photograph simply by learning the rule at move-out. [S11]

**Add the second maintenance loop.** Rule updates are one loop. Changes to tenancy, occupancy, account ownership, authority, amounts, delivery, or performance are another. A correct rule evaluated against stale facts can still produce the wrong result. Preserve the relevant rule version and the facts relevant to the decision's time.

## 5. Candidate roles—not fabricated market scores

| Candidate | Role in the next comparison | Key question |
|---|---|---|
| Deposit disposition | Technical reference case and commercial candidate | Can the product improve decision quality or remaining work beyond native tools and deposit specialists? |
| Renewal/rent-change notice handling | Equal commercial candidate | Can it apply the relevant timing/content requirements and complete the notice process with less rework than existing workflows? |
| Utility responsibility and account changes | Adjacent operational case | Is the failure caused by rules, missing facts, authority, or an uncompleted provider-account transition? |
| Vacant-home readiness | Outside comparator | Is physical coordination a more valuable, controllable business than obligation-based software? |

New York's residential notice provision is an example of the second family's structure: proposed rent change/nonrenewal, tenancy duration, notice content, and timing interact. It is not a complete model of all renewal rights or jurisdictions. [S12]

Select jurisdictions from prospective customers' real footprints and meaningful rule differences, not from founder residence or personal incidents. Nationwide coverage is not a prerequisite to determining whether the product helps a buyer.

The current recommendation favors an operator-facing workflow as the first test. A regional multi-jurisdiction operator is a useful discovery profile, not an established ideal customer. Do not carry over the original owner-operator requirement mechanically: a fee manager may be the buyer when it directly incurs the administrative cost and captures the improvement.

## 6. Agent evaluation design

### Compare three ways of doing the same work

1. A competent existing process, including the installed product or relevant specialist.
2. A capable model given the same documents, facts, permissions, and action tools.
3. The model with the proposed domain representation and decision tools.

Hold the underlying information and available actions constant where practical. Record both quality and total cost. This distinguishes the benefit of domain formalization from simply adding a better model, more context, or more human support.

### Evaluate four dimensions

**Decision quality:** correct applicability, relevant facts, dates, amounts, parties, required actions, and treatment of judgment. Create reference cases independently rather than deriving every expected answer from the same rules being tested.

**Useful completion:** successful required actions; timely notices or payments; unresolved/reopened work; justified versus unnecessary escalation; remaining work for operators and residents. An agent that avoids errors by referring every case to a person has not demonstrated useful automation.

**Change and reuse:** performance after a legal amendment or case change; update effort; regressions; onboarding effort for a second customer; proportion of the representation and evaluation suite actually reused.

**Economics:** customer benefit at the proposed price, all human review/support, model/tool expense, integration upkeep, and shared content maintenance. Count legitimate corrections and reduced burden, not simply higher resident charges or movement of work to another party.

Provenance supports explanations, evaluation, diagnosis, and updates. More citations or retained records are not success metrics by themselves. Request evidence because a decision needs it, not because collecting evidence is the product.

## 7. Revision register

| Original artifact / section | Change |
|---|---|
| Property_Management_Playbook.md — recommendation | Replace turns as the default with the comparative obligation-product hypothesis above. |
| Research_Synthesis.md — strategic conclusion | Separate operating-model findings from selection of the initial buyer, workflow, and business form. |
| operating_model.md | Preserve the map; connect applicable rules, agreements, current parties/facts, decisions, and resulting actions for one chosen family. |
| decision_inventory.csv | Preserve all 115 decisions; add an obligation-focused view rather than deleting unrelated decisions to fit the new thesis. |
| competitors.csv / market_products.md | Add Rentable and Blue Moon as explicit comparisons; retain Obligo's existing announcement and rollout qualification; test actual performance instead of inferring gaps from pages. |
| Field_Guide.md — discovery candidates | Put deposits and renewal/notices alongside make-ready; preserve operator-nominated alternatives and consecutive sampling. |
| Field_Guide.md — technical evaluation | Add the three-way comparison, change/reuse tests, and metrics for unnecessary escalation and resident work. |
| Economics workbook | Keep the original turn scenario labeled as such; create obligation economics only from the selected workflow's event and cost data. No fictional baseline imported from turns. |
| Claims about defensibility | Treat reusable accepted representations, evaluation cases, integrations, and update efficiency as hypotheses to measure—not a moat already possessed. |
| Product expansion | Defer nationwide compilation, a general-purpose DSL, and separately sold agent-training environments until repeated demand supports them. |

## 8. Scope of this review

This addendum reviews the main playbook and research conclusions, field guide, decision and provider inventories, and the illustrative workbook economics. It independently checks selected market and legal assertions relevant to the new thesis. It does not repeat the original Census microdata weighting or claim new customer observations, vendor trials, quotes, or a live deployment. Workbook baseline arithmetic was recomputed independently; a fresh native spreadsheet recalculation was not completed.

All 55 original archive files were retained unchanged. This is a separate strategic and research-design addendum, not a silent rewrite of the underlying evidence.

## Sources

Public pages checked for this review on 15 September 2026. Vendor pages establish what is offered or announced, not independently measured performance. Paper abstracts and project descriptions establish the stated research approach; this review is not a full technical evaluation of those implementations.

- **S1:** Rentable, product description and integrations. https://www.rentable.com/
- **S2:** Obligo, *Obligo Introduces the First AI Agent for Security Deposits*, 15 June 2026. https://www.obligo.com/blog/obligo-introduces-the-first-ai-agent-for-security-deposits
- **S3:** Blue Moon Software, products, portfolio functionality, and integrations. https://cms.bluemoonforms.com/
- **S4:** Conservice, *Expense Recovery*. https://www.conservice.com/solutions/expense-recovery/
- **S5:** Merigoux, Chataing, and Protzenko, *Catala: A Programming Language for the Law*, 2021. https://arxiv.org/abs/2103.03198
- **S6:** OpenFisca, project and uses. https://openfisca.org/en/
- **S7:** Avalara, MyLodgeTax. https://www.avalara.com/mylodgetax/en/index.html
- **S8:** John J. Nay, *Law Informs Code*, 2022. https://arxiv.org/abs/2209.13020
- **S9:** Norm Ai, *What is a Regulatory AI Agent?*, 15 September 2025. https://www.norm.ai/resources/what-is-a-regulatory-ai-agent
- **S10:** Norm Ai, *Legal Engineering: A Paradigm Shift in Law*, 24 October 2025. https://www.norm.ai/resources/legal-engineering-a-paradigm-shift-in-law
- **S11:** California Civil Code §1950.5, current text, including subdivisions (f), (g), and (h). https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1950.5.
- **S12:** New York Real Property Law §226-c, current operative notice provision. https://www.nysenate.gov/legislation/laws/RPP/226-C

Original package evidence: *Property Management Playbook*, recommendation and selection sections; *Research and Operating Model*, pp. 2–4 and 8; *Field Guide*, sections 1–9; *Review Findings and Resolutions*; decision and competitor CSVs; workbook scenario inputs.
