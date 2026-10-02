# Handoff: second frontend pass (proposal)

Source: Owen's walk-through with his co-founder on 2026-09-27 (notes 1-6), plus Ferro's own findings.
Status: proposal only. Nothing below is built.

## Principles
1. One status per thing, and it says who or what the work is waiting on. Never show two statuses that disagree.
2. A document is a document. If there's no document, show a note inline; don't open a viewer.
3. Correspondence is correspondence. Emails read like emails. What Handoff took from an email (price, date,
   confirmation) is shown separately, as a record.
4. Show the agent's work as a timeline of what it did and why, grouped by vendor. Don't show a log of turns.
5. The layout stays stable while data changes. New things are marked "new"; nothing jumps or reorders.
6. Every addition removes or replaces something.

## 1. One lifecycle status per job (note 1)
Problem: the Status column shows the backend's work state ("Awaiting advance", "Complete") while the payment
lines say otherwise. "Complete" shows while the invoice is still being paid. The backend also leaves
"Awaiting advance" in place after the advance is paid, until the visit is booked.
- Frontend: derive one stage from the job, its payments and its invoice. The stages are: Ordered, Advance
  requested, Booking visit, Visit booked <date>, On site, Checking report, Invoice to pay, Paid (closed), and
  Needs attention. "Complete" appears only once the work is checked and the invoice is paid.
- Replace the separate Status pill, the payment lines and the findings sub-rows with the stage pill plus a
  small five-step rail under the vendor (Ordered · Advance · Visit · Report · Paid). Each step shows its date.
- Backend: when the advance settles, move the job to "Booking visit". This removes the stale state at its
  source.

## 2. Make the agent legible (note 2)
Problem: the "Handoff" status card shows the last step. The Activity tab is a flat log of one-minute turns.
Bursts of changes (four orders in four minutes) feel jumpy.
- Replace the Handoff card with a "Now / Next" strip. Now: "Waiting on Westside to book the visit (asked
  Sep 30)." Next: "When Westside confirms, Handoff books Hudson after the plaster work." It also says who
  acts: Handoff, a vendor, the owner, or you.
- Replace the Activity tab with a Timeline, grouped by vendor lane plus an Owner & you lane. Each entry is one
  business event with a link to its evidence (the email, the report, the invoice). Consecutive events from
  the same run collapse into one entry ("Ordered 4 jobs from the repair plan") that can be expanded.
- Mark entries that arrived since you last looked as "new". Updates land in place, and rows keep their order.
- Show the case's today date in the unit header ("Today: Wednesday, September 30"). Dates run on the case
  clock, so this anchors them.
- Backend: when Handoff processes your message, it writes a real reply to you ("Done. I've asked all four
  trades for quotes; Hudson and Westside have replied."). Today the chat stitches a reply together from
  activity.

## 3. Messages as real correspondence (note 3)
Problem: a vendor thread mixes Handoff's email, pasted quote data, an order written as a bullet list, an
"Appointment: A; B" line and a report dump with repeated lines.
- Backend: generate outgoing and incoming correspondence as real emails. That means a subject, a greeting,
  prose, requirements written as sentences, and a signature. Vendor replies are written in the vendor's voice.
  Reports, quotes and invoices travel as attachments ("Our invoice INV-2041 is attached"), not as pasted text.
  Remove the repeated finding lines: today a condition covered by two report lines prints twice.
- Frontend: the Messages tab becomes an inbox. The list shows one thread per vendor or person: subject, last
  message and date. The thread reads like an email client: From, To, date, body, and attachments as chips
  that open the document. Under each incoming email, a small "Recorded by Handoff" line shows what was
  extracted (Quote $37,912.49 · Visit booked Monday, October 5 · Requirements confirmed).
- Delete: the "Waiting on" section (it's covered by the Now strip and the inbox's "awaiting reply" marker)
  and the Handoff chat bubbles in threads.

## 4. Documents that are documents (note 4)
Problem: nearly every item opens a "document" viewer that shows one paragraph. "Invoice $9,000.00" shows one
sentence.
- Records Handoff creates are rendered in the viewer as the document they stand for, from the saved record,
  with exact amounts taken from that record:
  - Invoice: vendor letterhead, invoice number, date, bill-to, line items, total, terms, due date and paid
    stamp.
  - Quote: letterhead, line items, total, validity, terms and requirements.
  - Report: date, inspector, a table of conditions with results, and the method.
  - Payment: a receipt.
  - Print and PDF download come from the same template.
- Source records become real files in the rebuild: owner instructions as an email printout, the access note
  as a letter, the walk-through as a report PDF, and vendor service sheets as PDFs. The lease PDF and email
  PDF already exist.
- A plain note (for example an operator note) opens inline and never in a document viewer. The viewer's
  close button reads "Close".
- Unit file groups: Lease & records · Reports · Quotes · Invoices & payments · Vendors · People.

## 5. Calendar (note 5)
- Add "Calendar" to the top nav next to "Units" (all units), and as a tab on the unit page.
- Week and month views on the case clock. The view shows:
  - Vendor visits, with multi-day work drawn across its working days.
  - Report due dates, invoice due dates and offer expiries.
  - Lease end, the showing target (late October) and move-in (December 1).
  - A "today" marker.
- Clicking an item opens a side sheet: vendor, scope, access instructions, status, and the scheduling emails
  for that visit.
- Everything comes from existing records: appointments, invoice due dates and offer validity. Visit rows in
  Work link to the calendar item.

## 6. Your co-founder can't open the app (note 6), root cause confirmed
- The workspace grants read, work and decide to one person only: Owen
  (c47a52a0-0048-4607-931f-f4df283ae7c4). Every record carries the same reader list, and every read checks
  it. So any other user in the organization gets refused, and the app shows its generic "Try again" notice.
- Backend fix: a new admin action, "Add a teammate". It grants read, work or decide to a Foundry user and
  updates the reader list on the workspace and every record in one change, with an activity entry. There's
  also a matching "Remove".
- (Dropped by Owen: no Team page.) Replace the generic error with "You don't
  have access to Whitcomb Holdings yet. Ask an admin to add you."
- Owen checks in Foundry: the co-founder can view the Handoff project, and the Developer Console
  application allows his account. The dev tier also has a 5-user cap.

## Also (not named in the notes)
- Readiness bar: today it's 4 unlabeled segments. Replace it with a labeled stepper (Assess · Plan · Work ·
  Ready) with dates and "on track / at risk for late-October showings".
- Owner funds: add "Requested, not yet paid". Show a per-vendor ledger (committed, invoiced, paid) in a Money
  section. Remove the ambiguous standalone "Invoiced".
- Move-out accounting says "Not started" forever. Until that track exists, show the deposit held and the
  statement deadline. Otherwise remove the track from the header.
- Units list: replace the "Now" column (the last step) with "Waiting on" and "Needs you". Add a decision badge
  on the nav.
- Remove "Other quoted work" once every quoted line has been ordered or declined.
- Handoff's own questions still carry system detail ("serviceId", "cents"). Extend the copy check (fix list
  B11).
- Mobile: the Timeline, Inbox and Calendar each get a single-column layout.

## Delete or replace summary
- Delete: Activity tab (becomes Timeline) · "Waiting on" section · findings sub-rows in Work · payment text
  lines · Handoff status card (becomes Now/Next strip) · stitched chat replies (become real replies) ·
  document viewer for plain notes · "Invoiced" tile.
- Replace: status pill → lifecycle stage · Messages list → inbox · text "documents" → rendered documents
  and real files · readiness segments → labeled stepper.
- Add: Calendar (nav and tab) · Team page · Now/Next strip · "new since you looked".

## Sequence
1. Access: the "Add a teammate" action, the Team page and the access message. It's small, and the co-founder
   is blocked until it's done.
2. Backend correspondence and lifecycle: real email bodies with attachments, Handoff's replies to the
   operator, job stage after the advance, deduplicated findings, and B11.
3. Frontend pass: lifecycle stage and rail, Now/Next and Timeline, Inbox, rendered documents, Calendar,
   stepper, money ledger, and the deletions.
4. Rebuild the case with real source files, then repoint the workers and tag the release.
