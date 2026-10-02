"""Expand declared condition groups into actual predecessor field selections."""
from copy import deepcopy

from .templates import within


def expand_condition_context(proposal):
    """Return a new preparation and a change log; never infer predicate meaning.

    A group's declared child paths determine which existing field-producing jobs
    to select. All candidate group structures are covered before answers arrive.
    The ordinary compiler must still validate the resulting dependency graph.
    """
    result = deepcopy(proposal)
    jobs = {job['id']: job for job in result['jobs']}
    producers = []
    for job in jobs.values():
        for license in job.get('licenses', []):
            if license['operation'].startswith('establish_'):
                producers.append((job['id'], license))
    changes = []

    def expand(value, owner):
        if isinstance(value, list):
            for child in value:
                expand(child, owner)
        elif isinstance(value, dict):
            if 'from_actual_results' not in value:
                for child in value.values():
                    expand(child, owner)
                return
            refs = value['from_actual_results']
            seen = {(ref['job'], ref['field']) for ref in refs}
            # Appending while walking closes nested groups, including cycles of
            # legal relationships; seen prevents unbounded traversal.
            for ref in refs:
                for license in jobs[ref['job']].get('licenses', []):
                    group = license['value']
                    target = license['target']
                    if (not license['operation'].startswith('establish_') or
                            not within(target, ref['field']) or not target.startswith('conditions.') or
                            not isinstance(group, dict) or group.get('operator') not in {'all', 'any', 'not'}):
                        continue
                    children = group.get('children')
                    if not isinstance(children, list) or not children or any(
                            not isinstance(child, str) or not child or '.' in child for child in children):
                        raise ValueError('Condition context has malformed child paths')
                    for child in children:
                        path = target.rsplit('.', 1)[0] + '.' + child
                        candidates = {(jid, row['target']) for jid, row in producers
                                      if row['target'] in {path, path + '.predicate'}}
                        if not candidates:
                            raise ValueError('Condition context has no field producer: ' + path)
                        for jid, field in sorted(candidates):
                            if jid == owner['id']:
                                raise ValueError('Condition context would require its own answer')
                            if (jid, field) not in seen:
                                refs.append({'job': jid, 'field': field})
                                seen.add((jid, field))
                                changes.append({'consumer': owner['id'], 'group': target,
                                                'producer': jid, 'field': field})
                            if jid not in owner['requires']:
                                owner['requires'].append(jid)

    for job in jobs.values():
        expand(job.get('state_template', {}), job)
    return result, changes
