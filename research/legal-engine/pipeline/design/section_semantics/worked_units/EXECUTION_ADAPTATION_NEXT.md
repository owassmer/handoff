# Next-version execution proposal

The original OR490 and CA400 preparations are unchanged. No diagnostic response was read to prepare these changes, and no confidence policy or expected answer changed. New files are `or_entry.next.preparation.json` (491 jobs) and `ca_return.next.preparation.json` (403 jobs). They are proposals awaiting source/operation review, not accepted legal outputs.

Every relationship's `proposed_relationship_operation` is included in its native semantic question and YES license. Actual predecessor selectors now bind the relevant field producers, including condition nodes and timing fields. A descriptive relationship label has no execution authority.

## Already supported Boolean operations

The two cure relationships use `block_condition` with `conditions.landlord_cure_prevents.root` → `conditions.landlord_termination.refusal_lawful`, and `conditions.tenant_termination_cure.root` → `conditions.tenant_termination.root`. Exclusion relationships with established target conditions use the same operation. The 1965 exclusion uses newly proposed, separately judged initiated/completed predicates and their ANY group, targeting `conditions.alternate_surrender_route.root`. These mappings preserve the base requirements; a blocker cannot create missing prerequisites.

The two ordinary-return storage waivers retain `set_predicate` targeting `conditions.notice_period_return.storage_paid`. The source condition is respectively the1987(c) and1990(c) root. The yard-terms prerequisite uses `require_condition`.

## Proposed typed interfaces

`EXECUTION_TYPED_CONTRACTS.proposal.json` defines the following additional operations. They are not claims that runtime support exists.

- `independent_effects`: explicit record paths, optionally scoped by an additional condition or an `unless` condition. Return each applicable effect independently. No exclusive election or silent override. This covers coexisting permissions/prohibitions, distinct recipient routes and scope inheritance for standalone waiver records.
- `attach_requirements`: target record plus an ALL bundle of typed field/record selectors, each optionally conditioned. The output is a required notice, location or timing bundle; it is not a conclusion that the case complied. An ordinary landlord cause-notice bundle is excluded in the separately established repeat-notice branch, avoiding simultaneous30-day and10-day minima.
- `notice_methods`: explicit method-group selectors and their combination, preserving receiver/location/agreement qualifications and deemed-service timing. Emergency secure-attachment is now its own source-bound field job rather than an inferred meaning of the object field `tenant`.
- `calendar_binding`: exact target timing prefix, calendar-rule field and express anchor field. In particular, emergency postnotice retains entry as anchor rather than inheriting a calendar's service default.
- `conditional_expiration`: expiry timing and continuation-condition paths applied to a specific permission. Unknown continuation at expiry remains unresolved.
- `cost_component`: target payment record, storage component, conditional filter/rate/duplicate-exclusion/waiver mode, and typed parameters. Advertising and sale components remain separate. Duplicate detection requires stable incurred-cost IDs, not merely equal amounts. Unknown interest allocation or reasonableness prevents a final total.
- `waive_duty`: removes a mandatory duty under the named condition while preserving optional performance. The under700-dollar1988 branch removes the public-sale requirement; it does not forbid choosing sale.
- `alternative_route`: exposes the independently conditioned route without declaring an exclusive election or supplying its other missing prerequisites.

The JSON contains concrete selectors for every existing relationship in both units. Operations with natural-language accepted action/definition fields produce a case-classification requirement; code must not parse those strings into legal predicates or presume compliance. A separate semantic case job must establish whether supplied facts meet that accepted requirement.

## Review and implementation gates

1. Independently review each proposed operation's paths, polarity, scope and conditional structure. In particular, check cure/repeat branch applicability, optional-sale semantics, method alternatives and inherited scope.
2. Implement the small typed interfaces with unknown/conflict propagation and provenance. Do not dispatch these operations through the Boolean evaluator unless they are one of its explicit supported operations.
3. Assemble whole-record notice/timing/cost inputs using the indicated accepted field producers. Missing or rejected selectors prevent complete output; a legal field's existence is not proof of case compliance.
4. Freeze and evaluate only after these source and runtime gates close. The next files are not substitutes for the preserved first-wave diagnostic inputs.
