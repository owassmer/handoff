W2 evidence: information replies answer from the recipient's own material (Ferro, 2026-09-26)

Change
- Core PR ri.pull-request.main.pull-request.07774dc4-e962-4b5c-a5af-5fdc937b9bcb, branch
  ferro/handoff-information-replies at cfb9d240a00af4b23a29042b864e89527df013fc. CI PASSED (62 tests in
  coordinator.test.ts, full suite). Tag 1.6.1-branch-20260926-170725 on the same commit.
- Global branch ri.branch..branch.df9ea893-e8f8-4906-9ccb-8c8bc7474406:
  - Continue handoff and Resume handoff rebound to 1.6.1-branch-20260926-170725 (Owen, Ontology Manager, Rules).
  - 19 Handoff object types indexed on the branch (Owen). Only visible metadata difference: SELECTABLE render
    hint on 10 array properties.
  - Functions with external calls enabled on branches for create-handoff-workspace, receive-move-out-notice,
    send-handoff-message, resume-handoff (Owen, Security and submission criteria).
  - Caller-visible parameters unchanged on both rebound Actions (REST v2 read, main vs branch).

Branch test (REST v2 applyAction ?branch=, synthetic case, never on Main)
- Workspace workspace:2b877f71c1dce7e8b2ef0a98e5fc02fecf1145bf4edbc2a8895b278172985c2f ("W2 branch test").
- Handoff handoff:f0161ef82130151cef93041478cbbcb0758711444e4f85016c0b36849debe666. Parties: Morgan (owner),
  Casey (departing tenant, nothing on file), House Care (provider with Provider information).
- Operator message asked for House Care timing and Casey's move-in photos. Real GPT-5.2 turns via resume-handoff.

Results (messages: branch_messages.json; action responses: actions_log.jsonl)
1. House Care, one reply, from service terms:
   "Make the entrance secure: earliest visit 2026-09-28 09:00 UTC; a visit takes about 2 hours; replies within
   1 minute; offer valid until 2026-10-09 17:00 UTC. Advance of 2500; balance after completion. A visit time is
   agreed once the work is commissioned."  This text exists only in the new version.
2. Casey, one reply: "I can't provide this. I have no further information on it." unanswered=false, no due time.
3. No repeat: across turns 2-6 each recipient received exactly one Information request
   (House Care 1, Casey 1, Morgan 1). The agent moved on to a formal quote (received, 12500) and an owner question.
- Main unchanged during the test: 1 workspace, 1 case, 112 messages.

Observed, outside W2 scope
- The agent asked Morgan (owner party) for approval; the reply disclosed the funding document, the pre-existing
  behavior for correspondents with attributed documents. Approval of work belongs to the operator decision.
  Candidate follow-up, not part of this change.
