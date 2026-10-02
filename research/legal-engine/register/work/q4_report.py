import sys, json, collections; sys.path.insert(0, 'register/work'); from q4_lib import *
rows = [json.loads(l) for l in DEC.read_text().splitlines() if l.strip()]
jev = {s['section_id']: s['jev_p_decides'] for s in BATCH}
cnt = collections.Counter(r['decision'] for r in rows)
props = [(p, r['section_id']) for r in rows for p in r.get('proposed', [])]
order = {'critical': 0, 'major': 1, 'minor': 2}
props.sort(key=lambda x: (order[x[1] and x[0]['severity']], x[0]['id']))
def one(p):
    e = p['effect'].split('. ')[0]
    return e if len(e) < 230 else e[:227] + '...'
L = []
L.append('# Queue review, batch 4 (reviewer q4): NY business, consumer, estates and status law\n')
L.append('Scope: 496 sections (GBL, SSL, 18 NYCRR 352, Partnership, LLC, BCL, N-PCL, UCC arts. 1 and 3, Military Law art. 13, '
         'Executive Law art. 15, MHL art. 81, SCPA, EPTL). Decisions: `register/work/decisions_4.jsonl`. '
         'Check: `python3 register/work/check_decisions.py 4` passes, 496/496, 0 errors. Every cross-reference in reasons, '
         'conditions, effects and dependencies resolves to an existing rule or a rule proposed here. Helper scripts: `register/work/q4_*.py`.\n')
L.append('## Counts\n')
L.append('| decision | sections |\n|---|---|')
for k in ('stated', 'partial', 'new_rule', 'no_decision', 'excluded_regime'):
    L.append(f'| {k} | {cnt.get(k, 0)} |')
L.append(f'| total | {len(rows)} |\n')
sev = collections.Counter(p['severity'] for p, _ in props)
L.append(f'Proposed rules: {len(props)} (critical {sev["critical"]}, major {sev["major"]}, minor {sev["minor"]}); '
         f'{sum(1 for p,_ in props if p.get("amends"))} carry `amends`.\n')
L.append('## Proposed rules, most severe first\n')
cur = None
for p, sid in props:
    if p['severity'] != cur:
        cur = p['severity']; L.append(f'\n### {cur}\n')
    am = f' (amends `{p["amends"]}`)' if p.get('amends') else ''
    L.append(f'- `{p["id"]}` [{p["determinacy"]}, step {p["walk_step"]}] from {sid}{am}: {one(p)}.')
L.append('\n## Existing rules that look wrong\n')
L.append('1. `NY:MIL-306-309` states: "an action against a person in service may be stayed during service and for sixty days after (306)". '
         'Military Law 306 does not stay the action; it stays execution of a judgment and vacates or stays attachments and garnishments, '
         'and it does so mandatorily on the servicemember\'s application unless ability to comply is not materially affected: '
         '"on application to it by such person or some person on his behalf shall, unless in the opinion of the court ... the ability of the party to comply with the judgment or order entered or sought is not materially affected by reason of his military service: 1. Stay the execution of any judgment or order entered against such person" '
         '(register/texts/NY_MIL/306.txt). The sixty days are when the action may be pending, not the stay\'s length; the stay of the action itself is 304 '
         '(proposed `NY:MIL-304-stay-on-application`) and its length is service plus three months (proposed `NY:MIL-307-stay-terms`).')
L.append('2. `NY:COMMONLAW-owner-death-agency` states: "the executor or administrator (or the devisee of a specifically devised building) collects". '
         'For rent that had accrued before the owner died this is wrong: EPTL 13-1.1(a)(6) makes it personal property passing to the personal representative, '
         '"Rent reserved to the decedent which had accrued at the time of his death." (register/texts/NY_EPTL/13-1.1.txt). Only rent falling due after death follows a specifically devised building. '
         'Proposed fix: `NY:EPTL-13-1.1-accrued-rent-leasehold`. A voluntary administrator also has no authority over the building (SCPA 1302; proposed `NY:SCPA-1302-va-personal-property-only`).')
L.append('3. `NY:ADJ-tenant-death-payee` is incomplete in a way that decides outcomes: it gives the 7-month presentation window but not the 90-day deemed rejection '
         '(SCPA 1806), the 60-day suit deadline after rejection (SCPA 1810), that presentation counts as commencement for limitations (SCPA 1808(6)), '
         'the public administrator as payee (SCPA 1112, 1115, 1118), foreign fiduciaries and small-estate certificates (EPTL 13-3.4, SCPA 1309), '
         'or heirs\' liability after distribution (EPTL 12-1.1 to 12-2.1). Each is proposed above.')
L.append('\n## no_decision sections where Jev had P(DECIDES) >= 0.9\n')
hi = [(r, jev[r['section_id']]) for r in rows if r['decision'] == 'no_decision' and (jev.get(r['section_id']) or 0) >= 0.9]
if not hi:
    L.append('None.')
for r, j in sorted(hi, key=lambda x: -x[1]):
    L.append(f'- {r["section_id"]} (P={j}): {r["reason"]}')
L.append('\n## Notes\n')
L.append('- No section was excluded_regime: the batch has no stabilized, controlled, public-housing or commercial provision; homeless-shelter rules (18 NYCRR 352.35-352.39, SSL 131-V) are recorded as no_decision because a shelter placement is not a tenancy.')
L.append('- Payment plans on a move-out balance are "credit" under Exec. Law 292 (a right to defer payment), which is why `NY:EXEC-296-a-payment-plan` applies; this does not contradict `NY:ADJ-lease-balance-not-consumer-credit`, which concerns the balance itself under GBL 600(1) and CPLR 105(f).')
L.append('- `NY:UCC-3-802-check-suspends-obligation` adds a consequence the walk does not state: a refund check that is dishonored and not replaced by payment within the 14 days has not returned the deposit on time.')
L.append('- `NY:SSL-143-c-agency-deposit-refund`: a cash deposit a social services official funded is refunded to that official once the tenant\'s required assignment is known; the statement still goes to the tenant.')
(WORK / 'report_4.md').write_text('\n'.join(L) + '\n')
print('\n'.join(L)[:3000]); print('...'); print(len(props), sev, cnt, len(hi))
