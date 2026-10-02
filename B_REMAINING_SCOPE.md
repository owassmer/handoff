Handoff — remaining B scope (Ferro, 2026-09-26)

Dated record, not authority. Authority: Notepad "Handoff — intent and operating model"
(ri.notepad.main.notepad.94df9b11-132f-412b-a917-8980d6d99e06) and "implementation blueprint
and current state" (ri.notepad.main.notepad.abdb3f8c-6d30-43bc-aeec-01eeb3215220, v16).
No protected case bodies or amounts belong here beyond what is needed to locate a defect.

1. Verified baseline (read-only, 2026-09-26)

- Backend Main stable 1.6.0 = 55be1fb (Core repo ri.stemma.main.repository.40ca55f8-0251-478b-95fc-0b2e5126641e).
- Frontend 0.1.0-handoff.7 = 31c693f on ai-fde/owassmer1/deposit-closeout-phase-e-ui
  (React repo ri.stemma.main.repository.83345d45-7af3-4fd4-9175-613c5971696a). React master is template only.
- Main Demo: 1 workspace, 1 case (Open, rev 105), 1 work plan (Ready, rev 29, basis 103,
  one assessment service, budget = quote total), Agent work "Waiting for decision",
  nextWakeAt null, businessTime 2018-03-08T05:12Z.
- Counts: Decision 0, Job 0, Inspection 0, Invoice 0, Funding 0, Payment 0, Quote 1 (Offered,
  validUntil 2018-03-09T23:59:59Z), Document 12, Party 7, Obligation 1, Message 112, Activity 106.
- Message growth stopped at 2026-09-25T16:44Z. The 1.5.1 coalescing fix holds in observation.
- Not verified by Ferro: Automate worker state (no public read), hosted app sign-in, React PR state.

2. Where each B exit clause stands

B exit (blueprint §11): (a) ending-tenancy information leads to investigation and a reasoned plan;
(b) the operator makes the judgment without coaching; (c) accepted work becomes provider
coordination and observable progress including a response/change; (d) work continues across
waits and browser closure.

  (a) Implemented and exercised on Main. Defects in 3.1–3.2 degrade its quality.
  (b) Not demonstrated. B.9 outstanding.
  (c) Not demonstrated as one integrated sequence. Engineering evidence exists per step on
      synthetic cases (blueprint §1 "B implementation and verification checkpoint").
  (d) Partly observed (workers ran scheduled turns 2026-09-25). Not observed across a delivery wait.

3. Findings that change the scope

3.1 Information counterpart cannot answer the question asked (B.4).
    inquiries.ts:86-91 replies to any non-quote inquiry with every document attributed to the
    recipient, regardless of the question. A correspondent with no attributed documents always
    returns "not yet available … remains open" with a 24 h due time (inquiries.ts:91,97).
    Observed on Main: the agent asked the owner and the provider for appointment windows; the
    owner reply is a dump of inspection findings, the provider reply restates the quote.
    Appointments exist only after commissioning (counterparts.ts:130), so pre-acceptance
    scheduling questions are unanswerable by construction. The agent's current next step still
    says availability "is still outstanding". The operator will see this in B.9.
    Result: 54 outgoing / 54 incoming "Information requested" rounds; 17 each to two parties.

3.2 Resident A has no attributed material (corrected by W1 F2).
    Resident B has one document. Arrival photos C1–C22 are unrecovered originals and the prepared
    access document says so. No world fact is missing; the repeated asking belongs to 3.1/W2.

3.3 Quote validity vs the business clock (B.7 dead-end risk).
    Commissioning requires quote Offered and validUntil >= business now (coordinator.ts:183).
    Business time advances to nextBusinessAt on each due wake (clock.ts:10). Remaining margin is
    ~1.8 business days. Further information follow-ups after acceptance can move business time
    past expiry; the counterpart then returns "no longer available" (counterparts.ts:115-116) and
    no alternative provider exists. Must be exercised in isolation before the real acceptance.

3.4 World has one provider and one service (assessment only).
    No repair or cleaning provider information exists. After the assessment report, a repair
    proposal cannot obtain quotes. B.8 "revised proposal when the mandate must change" and any
    repair delivery are unreachable in the current world.

3.5 Existing inspection is prepared text only.
    "Move-out inspection" is a Prepared document; Inspection objects = 0. The documented
    `report` envelope path (INTEGRATION.md "Already existing business records") can recognize it
    without fabricating history. Obligation count is 1; confirm against the agreement whether
    other genuine duties exist (intent §4: genuine duties only, not software tasks).

4. Work items, in order

W1  World coherence audit (B.1/B.3). Read-only. Walk the 12 documents, 7 parties, agreement and
    obligation against the supplied case package (NYC_001 media set) and Handoff Docs. Output:
    a short list of world facts to add or correct, each tagged source-backed or
    acquisition-gap fill. Covers 3.2, 3.4, 3.5. Lane: REST reads, media reads.
    Evidence: the list, with source references. No writes.

W2  DONE 2026-09-26. Merged by Owen: Core PR 07774dc4 (master b0014d6) and proposal dfefd000 (DEPLOYED).
    Actions bound to 1.6.1-branch-20260926-170725. Branch test evidence: w2/W2_EVIDENCE.md.
    Counterpart and agent fix for 3.1 (B.4/B.5). Owen chose (a) on 2026-09-26. Options were:
    (a) provider replies disclose service availability/response terms from Provider information;
        other parties answer only questions their attributed material covers, otherwise a
        definitive "cannot provide" once;
    (b) reasoner/tool guidance that availability is part of the offer (availableFrom,
        durationMinutes, responseMinutes) and is arranged after commissioning.
    Lane: fresh global branch in Core, tests, tag CI, proposal. Owen merges.
    Evidence: branch Action run on an isolated case showing one question → one relevant answer.

W3  World preparation on Main Demo for W1 findings (B.1). Configure-authorized
    receiveHandoffDocument / associate paths only; no raw patches, no reseed.
    Evidence: permissioned workspace read after each Action; exact replay = zero edits.

W4  Isolated delivery rehearsal (B.7). On a fresh global branch and an isolated synthetic
    workspace (not the primary case — intent §11, blueprint §15): accept → commission → advance
    payment if required → appointment → report with an honest Not checked item → completion
    check → invoice → final payment; plus Reject and Uncertain payment behaviors; plus 3.3 expiry.
    Evidence: object reads per step, Action responses, zero duplicate effects on replay.

W5  Mandate change (B.8). From the assessment report to a revised repair proposal, repair quote
    from a provider added in W3, second decision, and one within-mandate delivery adjustment that
    needs no new approval. Same isolated context first.

W6  B.9 operator check on Main (Owen). Review the plan and sources, make one meaningful change,
    accept, close the browser, observe the workers carry delivery forward. This acceptance is also
    the start of real B.7 on Main. Ferro prepares nothing on Owen's behalf and never submits the
    acceptance. Fix only named comprehension failures.

W7  Checkpoint. Update the blueprint current-state section after each merge, publication or
    observed result. Keep implemented, published, observed and accepted distinct.

5. Rules carried from the intent

- Owen decides; one multiple-choice question at a time, with a recommendation.
- Fresh global branch for any backend/schema change; never reopen a merged branch; Owen merges.
- No test mutations on the primary case; no reseed; no permission broadening; no worker changes
  unless a specific authorized correction needs one.
- Focused direct fixes, not long subagent cycles.
- Plain operator language; no stage labels in the product.
