# Handoff fix list

Source: the live case (142 West 88th Street) after the orders, reports and invoices, plus the hosted app read on 2026-09-27
(screenshots in fe/live/). C1-C2, B1-B3, B5-B11 and F1-F9 are fixed and merged (or in the open correspondence PR); B4 and the
items below from the 2026-09-27 tab review are open. Order of work is Owen's call.

## Status (verified 2026-09-28 against master and the finished w12 case, fe/fixture_w12_orders.json)
Open: B22; B26 (new); B27 (new, B18 residue); F19 (new, B2/F3 residue); B28 (new, B1 residue).
Fixed, not yet exercised on a live run: B4, B15, B17, B21, B25.
Fixed and verified: C1, C2, B1, B2 (report text), B3, B5, B6 (case clock), B7, B8, B9, B10, B11, B12, B13, B14, B16, B18
(booked visits), B19, B20, B23, B24, F1-F18. Owen has not yet reviewed F14-F18 (0.1.0-handoff.22).

B26. A model that reports propertyReady too early fails the whole turn: the check after reasoning is a requireHandoff, so
     the turn saves nothing and the error text reads "The property still needs supporting completion observations or
     remaining work." Return it to the model as a correction instead. Not seen on a run.
B27. A vendor on site is listed as "Waiting on": "Waiting on Westside Plaster & Paint. Next visit: Hudson ..." while
     Westside works Oct 5-16. A visit already under way isn't booked-in-future, so it falls into waitingOn. Say
     "Westside Plaster & Paint on site until Friday, October 16."
B28. Two activity lines still read as system text: "The property, tenancy and supporting documents are ready for a work
     recommendation." (notice received) and "The scope, budget and explicit requirements were accepted. Handoff will
     arrange delivery." (plan accepted).
F19. An assessment's Work row reads "Report: 3 findings" (one per deliverable line) although the report covers 11
     conditions, all 11 needing work on Sep 29 (before the railing was fixed). Count conditions, as the report does.

## Case content (fixed in the corrected-case rebuild, Question 11 (a))
C1. The urine odor was authored as "Not checked" in the starting condition record. The assessment can't record it, so Feld's job
    is stuck at Awaiting check, its $1,200.00 invoice is never paid, and the unit can't reach Ready. Author it as Deficient.
C2. Carroll's railing inherits the length of Carroll's whole service (with the $9,000 stair refinish). The visit is booked 9:00 a.m.
    to 1:00 a.m. and the report and payment are timed at 1:00 a.m. Make the railing its own short service.

## Backend (Core)
B1. Operator-visible status text is internal coordinator wording. It appears in the units list "Now" column, the unit's Handoff card
    and the job rows: "The payment service has returned an outcome. Continue with the confirmed result.", "The job's scope has
    supporting completion observations.", "Some of the job's scope still needs checking.", "The existing work is awaiting its
    provider response or scheduled report." Write plain operator sentences with the facts (vendor, amount, what's next).
B2. Report findings are one run-on string, "description.: State; ...". An assessment repeats the full 11-condition list under each
    of its three lines. Keep findings per condition, and per line only the conditions that line covers.
B3. Every plan requirement goes on every vendor's order. Feld's order carries the railing requirement. Send each vendor only the
    requirements that apply to its work, or phrase them for the whole plan.
B4. Owner/contact replies to yes/no questions paste whole documents (Eleanor on the railing, Morgan on scheduling).
B5. Plan titles use shorthand such as "+" and "(kitchen water excluded)".
B6. The case clock runs ahead of the real clock. On Sep 27 the app shows a completed job with a Sep 28 visit, a report dated Sep 30
    and a payment made on Sep 30. Vendors also reply within about a minute. Needs a decision on how demo time should read.
B8. The repair plan's budget is $65,000.00, the whole owner allocation, although $2,700.00 is already committed and
    $62,300.00 is available. The estimate ($59,689.33) fits, so ordering works, but a budget above the available funds reads
    wrong to a property manager. Cap a proposed budget at the available funds.
B9. (Fixed on branch, PR fa0e5f17) A draft request for an unread service failed the whole turn. Also: each release resets
    continueHandoff to the 60 s timeout; Owen sets 280 s after every merge.
B10. Vendor information replies read like data: "earliest visit 2026-10-05 13:00 UTC; a visit takes about 80 hours". Durations
    are continuous clock hours, so multi-day jobs book as one unbroken span through nights (same cause as C2). Write local dates
    and times, and model multi-day work in working days.
B11. Handoff's own questions to vendors and owners can still carry system detail: "(serviceId: entrance)", "deposit 2,500 cents".
    The copy check catches record IDs but not service IDs or amounts in cents. Seen in the plain-wording smoke test.
B7. The coordinator's instructions say "One small Demo indicator exists in the application". Remove with F1.

## Frontend (React)
F1. A "DEMO" badge shows in the top bar (App.tsx `demo-mark`, driven by workspace.mode). I carried it over from the old design.
    It breaks the no-demo-label standard. Remove it and its tests.
F2. Ask Handoff has no lasting replies. The only Handoff bubble is its current status note, shown while a decision is pending,
    so it reads as the answer to the operator's last message. Owen saw it: after he accepted the repair plan, the reply under
    "Please go ahead with the accepted work." disappeared. Show Handoff's replies as saved messages that stay in the thread;
    keep the current status out of the chat.
F3. Findings are squeezed into a narrow sub-column, run to 4-5 lines, and repeat the state (dot plus ": Satisfied"). Show them as a
    full-width list, one condition per line, collapsed for long assessments.
F4. An invoice that isn't paid shows no payment state (Feld's $1,200.00). "Paid $1,500.00" is plain text, not a status.
F5. Invoice lines wrap mid-metadata and repeat "payer Whitcomb Holdings LLC" on every invoice.
F6. The sticky top bar is translucent; scrolled content shows through it.
F7. "Needs attention" shows in neutral grey, not the attention colour.
F8. The Visit column shows the booked time even after the job is complete; it doesn't say the visit happened.
F9. The Handoff card shows raw agent states ("Ready to continue") as its status label. Fold into B1's plain wording.

## From the tab review of the live case (2026-09-27, fe/shots2/)
B12. All six jobs are complete and paid, yet readiness stays at "Arranging work". Handoff is holding the unit on the status of
     the separate kitchen water repair (Feld's earlier job, excluded from this plan) and keeps asking Feld and Eleanor. Their
     replies restate vendor terms and point at documents (same cause as B4). Decide whether an excluded prior job can hold
     readiness, and give the case a clear answer to that question in the rebuild.
B13. Records saved before the correspondence release keep event labels as subjects ("Reply received", "Appointment",
     "Provider offer received") and data-style bodies ("earliest visit ...; replies within 4 hours"). New records get real emails;
     the rebuilt case (step 4) is the clean path.
B14. Timeline text from the coordinator stays in the present tense after the fact ("sent the report and invoice. Handoff is
     checking them." on a paid job). Write completed steps in the past tense.
B15. The failed-plan chat reply reads as system text ("couldn't prepare a plan it could check this time ... work already
     ordered continues"). Say what happened and what Handoff will do next in one plain sentence.
B16. Handoff's quote requests use shorthand a PM wouldn't write ("sand/refinish", "plaster repair + soot cleanup",
     "treat/seal"). Its reply to the operator says "there are no formal Quotes loaded in the file yet". Plain sentences only.
B17. The failed-turn reply is saved in the chat as a Handoff message (03:46 on the rebuilt case), so the operator sees the
     system failure text as an answer. Same wording issue as B15.
B18. With every open job booked, the coordinator's status still reads "Waiting on <vendors>." (status Waiting for provider). Name
     the next visit instead. The app now derives this itself (React PR c318b036); fix the saved wording in a later backend pass.
F10. (Fixed in React PR c318b036) App reads were pinned to 1.6.0, so senders and attachments were missing; booking replies showed
     as "Unknown party". Bump the read pin with every backend release that changes the workspace view.
B19. Handoff proposed a partial repair plan in the same turn it asked Carroll (stairs) and Broadway (runner, carpet) for quotes,
     so the operator is asked to decide before all quoted work is in, then again for the rest. When quotes for the remaining
     deficiencies are outstanding and due within the day, wait for them and propose one plan.
B20. When the unit reaches Ready, Handoff's saved status stays "Waiting for information" (app: "Waiting for replies") with no
     wake, and its summary uses slash shorthand ("floors/inlay", "billing/deposit"). A finished physical turn should read as
     done in plain words, e.g. "All work is complete and paid. The unit is ready for the next tenant."

## From Owen's review of the motion release (2026-09-28)
F11. Money has no home of its own. Quotes and invoices sit in Documents beside the lease and letters, owner funds sit at
     the bottom of Overview, payments show only as rail dots and timeline lines. Cause: the page is grouped by kind of
     artifact (everything is a "document") instead of by the job the operator is doing. Records answer "what do we
     know about this unit"; money answers "what have we committed, been billed, paid and what's left". Give money one
     place (funds, quotes and commitments, invoices, payments) and keep Documents for records and correspondence files.
     Applies wherever money is scattered: Overview funds section, Work row Quote/Invoice links, calendar invoice dates,
     later the tenant account (move-out accounting).
F12. Multi-pane tabs scroll the wrong thing. In Documents the wheel moves the long list (the whole page) while the open
     document stays put; a tall invoice or PDF can't be scrolled on its own. Messages has the same pattern: the list
     grows the page, the thread has its own scroll inside it, so the page and the thread compete. Cause: the whole
     document scrolls, and panes either have no height limit (list) or sit sticky with their own limit (preview,
     thread), so two scroll areas nest. Fix pattern (Gmail, Front, Drive, Linear): on desktop the tab body is a fixed
     viewport-height frame and each pane scrolls independently (`min-height: 0; overflow: auto;
     overscroll-behavior: contain`); the page itself doesn't scroll under a split view. Single column under 720 px
     keeps normal page scroll. Applies to Documents, Messages, the calendar event panel, the Ask Handoff dock, and
     Case controls' step log.
B21. A failed model call (timeout, rate limit, provider error) fails the whole turn: nothing is saved, the app shows no
     change, and the log line's cause (status) sits only in attributes the Automate viewer hides. Per-call timeout is
     45 s with no retry, which a large repair-plan turn can exceed. Retry once, keep calls inside the 280 s turn limit,
     and on a final failure save "Recommendation unavailable" with the cause in the log message.
B22. Two reasoning turns can run at once on one case (automation and Case controls, or both automations). Both spend
     model calls; the later one is discarded at best. Seen on the fresh case at 16:40 and 16:41.
B23. Handoff fails checks because it isn't told the rules up front, not because it can't follow them. From the W10
     repair-plan transcript (2026-09-28 16:41Z):
     - It read 14 documents but not Broadway's or Carroll's service information, then drafted quote requests to them.
       "Read the service information first" appears only in the correction, never in the instructions or the context.
     - The instructions say "include their source documents" in each selection reason, so it wrote document IDs into
       reasons ("Source: ... (document:8a68...)"). The ID ban is stated only for request questions and summaries.
       quoteCosts accepted those reasons; the copy check rejected them only at the final draft.
     - A rejected final draft is dropped from the conversation, so each correction names a fault in text Handoff can
       no longer see. Every correction is a full rewrite at 16,000 tokens, which is also why calls hit the 45 s limit.
     - It drafted a partial plan (Westside and Hudson) while asking Broadway and Carroll for quotes (B19 again).
     Cause: checks guard rules the model meets only as rejections. Fix: state each checked rule in the instructions
     with its reason, remove the contradiction, mark in the context what still needs reading, keep the rejected draft
     in the turn so a correction is an edit, and check copy where it is first written (quoteCosts).
B24. Plans leave out work because the first turn may ask only 4 vendors for quotes. The cap has no reason.
     - Origin: `entries(output.requests, "Requests", 4)` arrived in the original coordination release (1a9105f, 2026-09-25)
       as a generic list bound, the same pattern as every other `entries(..., max)` (16, 24, 48), sized to the small test
       world of the time. No product rule, platform limit or document asks for it. A property manager sends a request for
       quotes to every trade at move-out.
     - 1.7.2 (Ferro) wrote the cap into the instructions ("send at most 4 ... later requests can follow") instead of asking
       why it existed; that taught Handoff to plan around it. 1.7.5's "decide once" rule and the proposed coverage machinery
       were more of the same: building around a limit that should not be there.
     - Effect, both 142 West 88th Street cases: 6 services, 4 asked (Feld, Carroll railing, Westside, Hudson). Carroll's
       stair repair and Broadway were never asked in the first turn, so every later plan was built from 4 quotes.
     Fix: remove the fixed cap; bound requests by the case (at most one Quote request per service, one question per party
     per turn) and drop the "at most 4" wording from the instructions and correction text.
B25. Repair quotes go out before the assessment that defines their scope (w12, 1.7.6). The owner wrote "Have Feld walk the
     apartment first and give me a condition schedule and a scope with a budget before we commit to repairs. Then line up
     the trades." Turn 1 sent all six quote requests, repairs included. Cause: Ferro's 1.7.6 instruction "ask every vendor
     whose service is needed in the same turn", written unconditionally; nothing says an assessment sets the repair scope,
     and quote requests carry no report. The plan itself sequenced correctly (assessment and railing first).
F13. Money shows quotes and invoices as one total per document; line items only in the drawer. A PM compares and
     tracks commitments by line (Procore commitment schedule of values, Bill.com bill lines); the Overview plan already
     shows lines, so Money, the tab meant for money, shows less than Overview.
F14. Every action button greyed out and blinked on each background refresh (Send, Accept, Change...). Cause:
     `stale = read.failed || read.loading`, and loading turns on for every poll. A duplicate guard: the server's
     expectedRevision check already refuses a change made against an outdated plan. Rule: a background refresh never
     changes control state; only the operator's own in-flight submit or a failed read holds a control back.
F15. Update toasts closed after 6 s; "Your change was saved" stayed on the page with no close. Rule: confirmations and
     update toasts close themselves after 10 s (TRANSIENT_MS), paused while hovered or focused; problems stay until
     closed; every banner has a close except the unrecoverable-journal warning.
F16. Money document tables wrapped the description column (fixed 170 px on every column but the first). Rule: in
     document tables the description column takes the free width; name, date, status and amount columns are sized to
     content and never wrap.
F17. Money line status read "Offered, not selected" for accepted lines not yet ordered (a bug) and as a hedge label.
     States are now Ordered, Approved (accepted, order pending), In proposed plan, Not ordered.
F18. Quote and invoice lines start folded, with per-row and section toggles (Owen: design for any case size).
F20. Case controls' planning turns are refused: "Ask the workspace owner to enable access to the work recommendation
     service." Resume handoff runs as the signed-in user, and the model call uses the app's OAuth token, which lacked
     `api:use-language-models-execute`. Automations use Owen's full token, so they plan fine; bookkeeping steps make no
     model call. Fix: enable the permission in Developer Console (Platform SDK page), then request it in client.ts.
