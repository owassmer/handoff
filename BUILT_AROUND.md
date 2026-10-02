# Limits and workarounds: why is each one there?

Pattern (B24): a limit caused a failure, and the fix built around the limit instead of asking why it existed.
Rule: before stating a limit to the model, adding a rule, a fallback or a manual step to cope with it, find its origin
(`git log -S`, specs, platform docs). No recorded reason means it is a candidate to remove, not a fact to design around.

Audit of 2026-09-28. Origin is the first commit that contains it.

## A. Code limits that change what Handoff sees or does

| # | Limit | Where / origin | Reason found | Effect | Action |
|---|-------|----------------|--------------|--------|--------|
| A1 | At most 4 requests per turn | coordinateReasoning.ts, 1a9105f (09-25) | None; generic list bound sized to the early test case | First turn asks 4 of 6 vendors; every plan built from 4 quotes (B24). Built around 3 times: stated in instructions (1.7.2), "decide once" (1.7.5), coverage machinery (proposed, withdrawn) | Removed in 1.7.6: bounded by the case |
| A2 | Handoff sees only the latest 24 messages | coordinateReasoning.ts `.slice(-24)`, 1a9105f | None | A full run has 42 messages (w9 end). Past 24, the first quote requests, vendor replies and the operator's early messages leave its view | Fixed in 1.7.6 (184534): whole conversation |
| A3 | A plan holds at most 24 scope lines, but up to 48 priced selections | workPlans.ts `"Proposed work", 24`, d81129d (09-23) vs proposal.ts 48 | None; two bounds that disagree | A plan with 25+ lines fails as `format`; latent (w9 full plan had 13) | Fixed in 1.7.6: scope bound 48, as selections |
| A4 | Email attachments cut at 20; reply bodies cut at 12,000 characters | email.ts, inquiries.ts, 24d11ed (Ferro, 09-28) | None | Silent loss: a cut attachment list or body looks complete | Fixed in 1.7.6: no cut; over 50,000 characters fails at write |
| A5 | 4 corrections, 40 tool calls, 16,000 tokens, 230 s per turn | coordinateReasoning.ts, 3be0583 / 1.7.5 | Yes: the turn must finish inside the 280 s function limit, and cost | Bounds a failing turn | Keep |
| A6 | readDocuments 16 per call; notice: 80 documents, 32 parties, 16 services per vendor | 1a9105f, d81129d | Input sanity bounds; they reject loudly, and the model can call again | None seen (largest case: 51 documents after a full run, 37 in the notice) | Keep |

## B. Process workarounds

| # | Workaround | Reason found | Cost | Action |
|---|------------|--------------|------|--------|
| B1 | Owen sets the 280 s timeout by hand after every release | Yes, observed 2026-09-28: 1.7.7 arrived by Auto upgrade at 60 s and Owen had to set it | One manual step per release, his only one | Keep; look for an API or config to set it from code |
| B2 | Owen rebinds Continue and Resume handoff by hand every release, Auto upgrade off | None that holds. Ferro's "unreviewed code reaches main" was its own assertion: Owen doesn't review code before merging, changes are reversible, and this has never caused a problem. It is a demo | A global branch, a rebind and a proposal per release | Remove: Auto upgrade on, once, for every function-backed action |
| B3 | The app reads through a pinned function version, bumped by hand | None that holds. "Prospects see a release before merge" was Ferro's assertion, not Owen's priority. An unpinned read runs the newest published version (probe 2026-09-28), which is what we want | Stale pins caused F10 | Remove the pin |
| B4 | Frontend files a reply with no sender under the vendor of its job | Built around B3's stale pin (F10) | Turns a missing sender into a guess | Remove with the pin |
| B5 | Skill guidance: "tell Owen not to accept a partial plan and message Handoff to add the rest"; B19 rule; "decide once" | Built around A1 | Owen decides twice | Revisit after the fresh-case run on 1.7.6 |
| B6 | Case controls page (loop outside the function) | Yes: one call can't read its own edits, so it takes one step | Extra page | Keep |
| B7 | Every release tagged as a prerelease `<next>-branch-YYYYMMDD-HHMMSS` | Made for branch testing on a global branch; kept for every release | Blocked Auto upgrade ("choose a non-prerelease version"), so every release needed a manual rebind | Removed 2026-09-28: plain semver tag on master (1.7.6 first) |

## Second instance of the pattern (2026-09-28)
After the audit, Ferro kept B2 and B3 on reasons it supplied itself (protect prospects, protect main from unreviewed code).
Owen: those are not his priorities. A reason counts only if it comes from Owen, the specs, or an observed problem.
