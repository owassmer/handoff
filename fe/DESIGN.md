Handoff frontend: design brief (Ferro, 2026-09-26). Internal. Nothing here appears in the product.

0. Vocabulary

- Use the property manager's own terms: unit, building/property, tenant, move-out, turn, make-ready, owner,
  vendor, work order, deposit, move-out accounting. Not pitch or founder language ("home", "responsibility").
- Test every label: would a property manager say it about their own portfolio?

1. What the product must do for the person using it

Sources: intent notepad §5 and §7; Playbook §1 and §7; Strategy Review; 0-to-1 Plan §04; McKinsey "Automate steps and
protect thoughts".

- The operator is a property manager. Handoff takes a move-out from notice to "unit ready, move-out accounting settled" and brings
  them only the choices that need them (Playbook §1).
- The operator's working view is one list: unit, promised ready date, current blocker, next action, responsible person, cost
  exposure. Open a unit to see the supporting record and the proposed choice (Playbook §7, line 142).
- Each case shows the facts, the proposed disposition, missing information, next action, owner, deadline and actual
  completion status (0-to-1 Plan §04).
- Steps are automated and visible; thoughts are protected. Judgment sits in exactly two places: accepting or changing the
  work plan and budget, and later the account recommendation (intent §5).
- Two outcomes progress independently: the unit's readiness and the move-out accounting (the case goal).
- A prospect judges the product by whether the workflow feels like their own work, done for them. The screen must look
  like a mature operations product, not a demo or an AI transcript.

2. Design principles for this build

P1 Decision first. Opening a unit answers three questions in order: does anything need me, what is being done, what is
   the state of the unit and the accounting. History and the case file are one click away, never in front.
P2 Values, not prose. Money, dates, people, statuses and line items are labelled values, rows and comparisons. Agent prose
   is limited to a one-line "what Handoff is doing" and the reasons attached to a decision.
P3 One accent, one weight of emphasis. Colour marks only what needs the operator (the decision) and state (a small dot and
   word). No rainbow pills, no card-on-card nesting.
P4 Exact money. Tabular figures, right-aligned, cents shown. Budget, set-aside funds, committed, invoiced and paid are
   distinct numbers and never merged.
P5 Evidence on demand. Every figure and reason can open its source: quote, document, file or correspondence. The source
   keeps its original wording.
P6 Quiet trust. The agent's work shows as a factual trail (sent, replied, booked, invoiced, paid) with times. No
   narration and no disclaimers. One small Demo mark in the top bar.
P7 Nothing invented by the frontend. It renders only what the workspace view returns and acts only through the four
   gateway operations: message, accept, change budget, change plan. Files open through the existing protected read.

3. Information architecture (two screens)

A. Units (landing)
   One row per unit in turnover, sorted by "needs you" first, then by last movement.
   Columns: Unit (address, departing tenant) | Readiness (physicalProgress) | Move-out accounting (financialProgress) |
   Now (the agent's current step, one line, or "Your decision" in accent) | Committed of budget.
   A header count: "1 needs your decision".

B. Unit (move-out)
   Header: address; tenancy ("Laura and Michael Brenner, ended February 28, 2018"); two compact outcome tracks:
     Readiness: Assessing, Plan ready, Arranging work, Waiting for provider, Ready
     Move-out accounting: Not started (until the account recommendation exists)
   Main column
     1. Needs you: the decision sheet (only when a plan is Ready and the user can decide).
        Title; one-line purpose; line items table grouped by provider (work, provider, amount, source link);
        total, budget, funds available after this plan; fixed requirements as a short checklist;
        "Why this plan" collapsed to three short reasons; actions: Accept plan (primary), Change.
        Change opens in place: adjust budget; remove or add quoted lines (from received quotes); add a requirement;
        or ask Handoff in words. Budget changes are computed locally for display; the server revision is authoritative.
        After accepting: the sheet collapses into a one-line accepted record with who and when.
     2. When nothing needs the operator: a single line "Handoff is <status>" and the next expected event.
     3. Work: one row per job or pending request: provider, work, status dot, appointment or reply due, amount,
        invoice and payment state. Expands to its trail (sent, replied, booked, report, invoice, payment).
     4. Money: set aside, committed, invoiced, paid, available. Owner funds and deposit shown separately.
   Side panel (tabs, fixed width, collapsible)
     Conversation: the operator and Handoff thread with the composer. This is where "ask in words" lands.
     Correspondence: provider, owner and resident messages grouped by person, original wording.
     Case file: property, tenancy, lease terms, obligations, people, documents with their files.
     Activity: the full factual log.

4. States each component must handle (from the backend)
   Agent: Preparing plan, Waiting for information, Waiting for decision, Waiting for provider, Ready to continue,
   Recommendation unavailable, Paused. Plan: Ready, Accepted, Superseded. Job: Commissioned, Scheduled, Underway,
   Complete. Payment: Requested, Confirming, Settled, Failed, Returned. Permissions: canDecide false hides actions.
   Empty, loading, rejected change, stale revision, lost access, file unavailable.

5. Visual system (to confirm with Owen, see question)
   Light, calm workspace. Neutral warm greys, near-black text, one deep accent for "needs you". Inter or system UI,
   tabular numerals, 14 px base, 8 px grid, generous row height, hairline dividers instead of boxes. Desktop-first
   (1280 to 1600), usable at 1024, readable on phone.

6. Engineering approach
   - Keep: gateway.ts, contracts.ts validators, session/auth, branchConfig, sources.ts. They are the tested seam to
     the backend.
   - Replace: every Handoff component and stylesheet. Drop Blueprint from the Handoff surface; plain CSS with tokens.
   - Remove: the retired Deposit Closeout frontend (features/, commands/, contracts/, data/, phaseE0 and related) after
     confirming the router no longer reaches it (intent §8: retire obsolete screens after replacement).
   - Review loop: fixture gateway built from read-only snapshots of the live case (plan ready; later states from the
     W4 branch rehearsal), Vite preview, headless Chromium screenshots at 1440, 1280, 1024 and 390 px, and scripted
     walkthroughs of accept, change budget, remove a line, ask Handoff, open a file. Vision review of every screen.
   - Delivery: fresh branch ferro/frontend-overhaul from React master; tests, typecheck, lint, build; PR; Owen merges;
     tag 0.1.0-handoff.9.
