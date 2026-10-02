W1 — World coherence audit (Ferro, 2026-09-26). Read-only. No writes to Foundry.

Inputs
- Main Demo objects via REST v2 (snapshots in this folder: Handoff*.json).
- Supplied package NYC001 via dataset "Extracted source pages"
  ri.foundry.main.dataset.d2e5e807-c61b-4072-84e3-be53d54349c3,
  media set ri.mio.main.media-set.b820a6b1-478f-4cf8-bfd1-cc2fbad06427 (21 PDFs).

Coherent (no action)
- Tenancy, lease, modification, 48 h walk-through, wear-and-tear and pets terms match PDF 01/package guide.
- Move-out inspection document matches PDF 06 (court-derived; 55 of 60 photo labels described).
- Kitchen-water separation matches PDF 05 and PDF 10 (invoice 829 dispute).
- Quote and funding agree: USD 1,200, valid through 2018-03-09; business time 2018-03-08T05:12Z.
- Outcome material (PDF 14–16, 19–20) is not connected to the case. Correct: it postdates the business date.

F1  Repair providers exist in the source but not in the world (scope 3.4). Source-backed identity.
    Flooring Contractor A (PDF 07, paid 2018-07-20), Finish Contractor A (PDF 08, paid through
    2018-04-23), Stair Contractor A (PDF 09), Carpet Contractor A (PDF 11, paid 2018-04-23 and
    2018-05-17). Restoration Firm A (PDF 12) is July 2019, outside the window.
    Their March 2018 offers are not in the source; only later payments are. Adding provider
    information is an acquisition-gap fill, labeled prepared, with prices anchored to recorded
    paid amounts. Needed for B.8 (revised proposal, repair quote, second decision).

F2  Correction to scope 3.2. Resident B has one attributed document (condition and maintenance
    history). Resident A has none and received 17 information requests. Arrival photos C1–C22 are
    unrecovered originals (PDF 04), and the prepared access document already says so. No world fact
    is missing; the repeated asking is a counterpart/agent defect (scope 3.1, W2).

F3  Two connected originals are indistinguishable to the operator. Both documents are titled
    "Reconstructed material", have no party, and say "Open the attached file."
      original:74ff0f19…c673 -> media item …de81 = PDF 04, Resident B's June 2016 condition email.
      original:3d2bc925…3c31 -> media item …de82 = PDF 05, condition and maintenance history.
    Needs a proper title and, for PDF 04, party Resident B. Affects B.6/B.9. Fix path to confirm
    in W3 (configure-authorized receive/associate only).
    Caveat (React PR 11009685): both files are associated with the prepared "Condition and
    maintenance history" summary and open from it. Whether the operator ever sees the generic
    title is unverified. Check the hosted app before any fix.
    W3a result (2026-09-26, read-only): CLOSED, no change. getHandoffWorkspace returns the media
    file names as titles (readWorkspace.ts:76 originalTitles): "05_Condition_and_Maintenance_History.pdf"
    and "04_Condition_Report_Email.pdf", kind "Reconstructed material". The app lists them under
    "Supporting files" in the summary dialog (DocumentDialog.tsx:246-257). The view carries no sender
    for any document, so a missing party is not operator-visible. Snapshot: w1/demo_workspace_view.json.

F4  Inspection record (scope 3.5). The prepared document is faithful to its court-derived source.
    Recognizing it as an Inspection object is optional and not needed for B exit. Defer.
