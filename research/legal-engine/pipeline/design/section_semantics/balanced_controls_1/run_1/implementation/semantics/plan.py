"""Validate prepared semantic work; code does not invent legal meaning."""
from __future__ import annotations

import hashlib
from pathlib import Path
from pipeline import jev, jev_results
from . import templates

KINDS = {'entity', 'action', 'event', 'condition', 'duty', 'prohibition', 'permission',
         'definition', 'timing', 'consequence', 'relationship'}


def index(rows, name):
    if not isinstance(rows, list):
        raise ValueError(name + ' must be a list')
    out = {}
    for row in rows:
        key = row.get('id')
        if not isinstance(key, str) or not key or key in out:
            raise ValueError('Missing or duplicate ' + name + ' ID')
        out[key] = row
    return out


def source_text(selection, root):
    path = (Path(root) / selection['path']).resolve()
    if not path.is_relative_to(Path(root).resolve()):
        raise ValueError('Source outside research root')
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != selection['sha256']:
        raise ValueError('Source version changed')
    text = raw.decode('utf-8')
    start, end = selection['start'], selection['end']
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(text):
        raise ValueError('Invalid source selection')
    chosen = text[start:end]
    if chosen != selection['quote']:
        raise ValueError('Source selection differs from captured bytes')
    return chosen


def outcome_valid(job, value):
    kind = job['question']['primitive']
    return type(value) is bool if kind == 'noul' else isinstance(value, str) and value in job['question']['criteria']


def value_paths(value, prefix=''):
    if isinstance(value, dict) and value:
        return {p for key, child in value.items() for p in value_paths(child, prefix + '.' + key if prefix else key)}
    if isinstance(value, list) and value:
        return {p for i, child in enumerate(value) for p in value_paths(child, prefix + '.' + str(i))}
    return {prefix}


def validate(plan, root):
    if plan.get('format') != 'section-semantics-1' or not plan.get('id'):
        raise ValueError('Unknown semantic plan format or identity')
    jev_results.fingerprint(plan)  # No nonfinite/unserializable values.
    sources = index(plan['sources'], 'source')
    jobs = index(plan['jobs'], 'job')
    assertions = index(plan['assertions'], 'assertion')
    if not sources or not jobs:
        raise ValueError('Prepared evidence and jobs required')
    texts = {key: source_text(value, root) for key, value in sources.items()}
    for key, job in jobs.items():
        if not job.get('evidence') or len(set(job['evidence'])) != len(job['evidence']) or not set(job['evidence']) <= sources.keys():
            raise ValueError('Job evidence is missing, repeated or unknown')
        question = job['question']
        if question['primitive'] not in {'noul', 'choice'} or not question.get('instructions'):
            raise ValueError('A concrete supported question is required')
        if question['primitive'] == 'choice' and not question.get('criteria'):
            raise ValueError('Choice alternatives required')
        jev.sdk_questions({key: question})
        predecessors = job.get('after', [])
        if len(predecessors) != len(set(predecessors)) or not set(predecessors) <= jobs.keys() or key in predecessors:
            raise ValueError('Invalid job predecessors')
        for gate in job.get('when', []):
            if gate['job'] not in predecessors or not outcome_valid(jobs[gate['job']], gate['answer']):
                raise ValueError('Invalid dependency condition')
        context = job.get('context_from', [])
        if not isinstance(context, list) or any(not isinstance(item, dict) or
                item.get('job') not in predecessors or not isinstance(item.get('name'), str) or
                not item['name'].strip() for item in context):
            raise ValueError('Context must name a declared predecessor judgment')
        if len({item['name'] for item in context}) != len(context):
            raise ValueError('Repeated predecessor context name')
        for license in job.get('licenses', []):
            if (not isinstance(license, dict) or license.get('operation') not in templates.OPERATIONS
                    or not isinstance(license.get('target'), str) or not license['target']
                    or 'value' not in license or not outcome_valid(job, license.get('answer'))):
                raise ValueError('Invalid answer-to-field license')
        if 'state_template' in job:
            if context:
                raise ValueError('Use one predecessor context mechanism per job')
            ev, pred = templates.references(job['state_template'])
            if ev != set(job['evidence']):
                raise ValueError('Template evidence must match declared job evidence')
            for item in pred:
                if item['job'] not in predecessors or not any(templates.within(row['target'], item['field'])
                        for row in jobs[item['job']].get('licenses', [])):
                    raise ValueError('Template selects an undeclared predecessor field')
    remaining, ordered = set(jobs), []
    while remaining:
        ready = sorted(key for key in remaining if set(jobs[key].get('after', [])) <= set(ordered))
        if not ready:
            raise ValueError('Cyclic semantic dependencies')
        ordered.extend(ready)
        remaining.difference_update(ready)
    for assertion in assertions.values():
        if assertion.get('kind') not in KINDS or not isinstance(assertion.get('value'), dict) or not assertion['value']:
            raise ValueError('Invalid candidate assertion')
        conditions = assertion.get('established_by')
        if not conditions:
            raise ValueError('Every assertion requires a semantic judgment')
        for condition in conditions:
            if condition['job'] not in jobs or not outcome_valid(jobs[condition['job']], condition['answer']):
                raise ValueError('Invalid assertion judgment binding')
        evidence = assertion.get('evidence', [])
        if not evidence or not set(evidence) <= sources.keys():
            raise ValueError('Assertion evidence missing')
        judged = {e for c in conditions for e in jobs[c['job']]['evidence']}
        if not set(evidence) <= judged:
            raise ValueError('Assertion evidence was not supplied to establishing jobs')
        licenses = assertion.get('field_licenses', {})
        required_fields = value_paths(assertion['value']) | {'$kind'}
        if assertion.get('links'):
            required_fields.add('$links')
        establishing = {c['job'] for c in conditions}
        if set(licenses) != required_fields or any(not ids or not set(ids) <= establishing for ids in licenses.values()):
            raise ValueError('Every semantic field needs an exact establishing job license')
        links = assertion.get('links', [])
        if not set(links) <= assertions.keys():
            raise ValueError('Unknown assertion relationship target')
    # The review must assess semantic completeness; this only checks mechanical coverage.
    classified = {e for job in jobs.values() for e in job['evidence']}
    if set(sources) - classified:
        raise ValueError('Selected evidence has no prepared semantic job')
    return {'sources': sources, 'texts': texts, 'jobs': jobs, 'assertions': assertions, 'order': ordered}


def requests(plan, root, registry, outcomes):
    """Prepare the next independent wave; unresolved prerequisites never become NO."""
    checked = validate(plan, root)
    for key, result in outcomes.items():
        if key not in checked['jobs'] or result.get('plan_hash') != jev_results.fingerprint(plan):
            raise ValueError('Unknown or stale predecessor outcome')
        if result.get('status') == 'answered' and not outcome_valid(checked['jobs'][key], result.get('answer')):
            raise ValueError('Invalid predecessor answer')
    ready, waiting, inapplicable = [], [], []
    for key in checked['order']:
        if key in outcomes:
            continue
        job = checked['jobs'][key]
        after = job.get('after', [])
        if any(outcomes.get(dep, {}).get('status') == 'not_applicable' for dep in after):
            inapplicable.append(key)
            continue
        if any(outcomes.get(dep, {}).get('status') != 'answered' for dep in after):
            waiting.append(key)
            continue
        if any(outcomes[g['job']]['answer'] != g['answer'] for g in job.get('when', [])):
            inapplicable.append(key)
            continue
        ready.append(key)
    groups = {}
    for key in ready:
        job = checked['jobs'][key]
        # Evidence text only, in stable source order. IDs/paths are not semantic context.
        state = [checked['texts'][sid] for sid in job['evidence']]
        if 'state_template' in job:
            state = templates.render(job['state_template'], checked['texts'], checked['jobs'], outcomes)
        if job.get('context_from'):
            judgments = {}
            for item in job['context_from']:
                predecessor = checked['jobs'][item['job']]['question']
                answer = outcomes[item['job']]['answer']
                judgments[item['name']] = {
                    'question': predecessor['instructions'], 'answer': answer,
                    'selected_meaning': (predecessor['criteria'][answer]
                                         if predecessor['primitive'] == 'choice' else answer)}
            state = {'evidence': state, 'prior_judgments': judgments}
        groups.setdefault(jev_results.fingerprint(state), {'state': state, 'ids': []})['ids'].append(key)
    result = []
    for group in groups.values():
        questions = {key: checked['jobs'][key]['question'] for key in group['ids']}
        identity = {'format': 'semantic-wave-1', 'plan_hash': jev_results.fingerprint(plan),
                    'base_url': registry['base_url'], 'model': registry['model'],
                    'pinned_build': registry['pinned_build'], 'questions': questions, 'state': group['state'],
                    'predecessors': {dep: outcomes[dep] for key in group['ids'] for dep in checked['jobs'][key].get('after', [])}}
        result.append({'case_id': '+'.join(group['ids']), 'request_hash': jev_results.fingerprint(identity),
                       'identity': identity, 'expected_wire': {'model': registry['model'], 'state': group['state'],
                       'questions': {key: q.model_dump(exclude_none=True) for key,q in jev.sdk_questions(questions).items()}}})
    return {'requests': result, 'waiting': waiting, 'inapplicable': inapplicable}
