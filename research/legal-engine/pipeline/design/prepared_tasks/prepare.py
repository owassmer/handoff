"""Serialize agent-selected passages. Selection and semantic sufficiency are agent work."""
import hashlib
import json
from pathlib import Path
from pipeline.design.legal_references.experiment import make_requests


def prepare(cases, selections, question, root):
    by_id = {c['case_id']: c for c in cases}
    if len(by_id) != len(cases) or len({s['case_id'] for s in selections}) != len(selections):
        raise ValueError('Duplicate case identity')
    if {s['case_id'] for s in selections} != set(by_id):
        raise ValueError('Every input needs a preparation outcome')
    ready, outcomes = [], []
    for selection in selections:
        case = by_id[selection['case_id']]
        original = case['text']
        if selection['input_sha256'] != hashlib.sha256(original.encode()).hexdigest():
            raise ValueError('Selection refers to changed input')
        if not selection.get('reason'):
            raise ValueError('Preparation outcome needs a reason')
        status = selection['status']
        if status not in {'ready', 'source_metadata', 'needs_context', 'different_task'}:
            raise ValueError('Unknown preparation outcome')
        if status != 'ready':
            if 'start' in selection or 'end' in selection:
                raise ValueError('Unready input cannot have a dispatch span')
            if not selection.get('next_action'):
                raise ValueError('Unfinished input needs a next action')
            outcomes.append(dict(selection))
            continue
        a,b = selection['start'],selection['end']
        if not 0 <= a < b <= len(original) or not original[a:b].strip():
            raise ValueError('Invalid selected passage')
        row = {'case_id':case['case_id'], 'text':original[a:b], 'strata':case['strata']}
        if case.get('source'):
            row['source'] = dict(case['source'],start=case['source']['start']+a,end=case['source']['start']+b)
        elif case.get('authored'):
            row['authored'] = True
        else:
            raise ValueError('Unattributed input')
        ready.append(row)
        outcomes.append(dict(selection))
    # Existing exact-source verification and label-free request construction.
    requests = make_requests(ready,question,root) if ready else []
    return ready, outcomes, requests
