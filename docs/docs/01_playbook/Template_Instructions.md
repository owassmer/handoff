# Using the blank templates

The CSVs contain headers only. Use the Field Guide for detailed questions and measurement definitions; these logs hold the working facts.

| File | One row represents |
|---|---|
| Case_Log.csv | One case and its current position |
| Event_Log.csv | One event, decision, action or time entry |
| Provider_Comparison.csv | One provider evaluated against one case |
| Pilot_Scorecard.csv | One metric for a pilot and its comparison |

## Basic conventions

- Keep the same Case ID across files. Reference supporting records instead of copying whole documents.
- Use YYYY-MM-DD dates. Add the time and UTC offset when event ordering matters.
- Leave unknown numbers blank. Zero means an actual or explicitly estimated zero. Mark values as observed, estimated, missing or not applicable in the available status or notes field.
- Enter amounts without currency symbols; use Currency for USD or another code. Identify costs, commitments, collections and refunds with Amount type. Do not count a commitment and its payment twice.
- Person-minutes add each participant's active time. Include review, corrections, meetings, training, support and founder work.

## Cases and events

Keep the original promised result and date unchanged. Record revised commitments, failed attempts, reopenings and corrections as new events. Confirmed result records what actually happened, not merely that an action was attempted.

In Key dates, label physical readiness, legal release, possession and collected-rent commencement where relevant. These are different events. Earlier readiness creates additional rent only when an earlier paying tenancy follows; the date cash arrived is also distinct from the occupancy period it covers.

Use Open duties and owner for remaining work, including financial disputes that continue after readiness. Keep excluded, aborted and unsuccessful cases visible, with reasons in Outcome and quality check. Handling minutes is a case summary; do not add it to its underlying event entries again.

Put decision alternatives, missing facts and a brief operational rationale in Facts available or the referenced record. Authority identifies the actual delegation or approval.

## Comparisons and scorecard

Give providers the same case facts and authority limits. Test a real exception. Distinguish demonstrated behavior, written commitments and unverified claims in Evidence seen. Compare costs over the same volume and period; separate already-paid licenses from incremental spending.

Use the Field Guide's measurement definitions. State populations, periods, exclusions and rate denominators in Scope and dates or the supporting reference. Change means pilot minus baseline; changes in percentage rates use percentage points. Include all eligible cases.

Separate time released from cash actually saved. Count only benefits the buyer captures. Provider contribution includes human work, tools, support, integration and remediation. Preserve uncertainty about whether the intervention caused an improvement.

The CSVs contain no formulas. Retain transparent calculations in the referenced record. Record the resulting decision and next action with its owner.
