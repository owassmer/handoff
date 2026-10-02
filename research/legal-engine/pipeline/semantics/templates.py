"""Resolve prepared evidence and actual predecessor selections into semantic state."""
from __future__ import annotations


OPERATIONS = {'establish_field_only', 'establish_relation_only', 'establish_group_only',
              'establish_definition_only', 'retain_open', 'reject_only'}


def within(target, field):
    return target == field or target.startswith(field + '.')


def references(value):
    """Return evidence IDs and predecessor field references in a state template."""
    evidence, predecessors = set(), []
    if isinstance(value, dict):
        if 'evidence_ref' in value:
            if set(value) != {'evidence_ref'} or not isinstance(value['evidence_ref'], str):
                raise ValueError('Invalid evidence template reference')
            evidence.add(value['evidence_ref'])
        elif 'from_actual_results' in value:
            if set(value) - {'from_actual_results', 'bind_result_and_request_hashes'}:
                raise ValueError('Invalid predecessor template reference')
            if not isinstance(value['from_actual_results'], list):
                raise ValueError('Predecessor references must be a list')
            for item in value['from_actual_results']:
                if not isinstance(item, dict) or set(item) != {'job', 'field'} or any(
                        not isinstance(v, str) or not v for v in item.values()):
                    raise ValueError('Invalid predecessor field selector')
                predecessors.append(item)
        else:
            for child in value.values():
                ev, pred = references(child)
                evidence.update(ev)
                predecessors.extend(pred)
    elif isinstance(value, list):
        for child in value:
            ev, pred = references(child)
            evidence.update(ev)
            predecessors.extend(pred)
    return evidence, predecessors


def render(value, texts, jobs, outcomes):
    if isinstance(value, dict):
        if 'evidence_ref' in value:
            return texts[value['evidence_ref']]
        if 'from_actual_results' in value:
            selected = []
            for item in value['from_actual_results']:
                result = outcomes[item['job']]
                if result['status'] != 'answered':
                    raise ValueError('Cannot supply an unanswered predecessor as context')
                job = jobs[item['job']]
                matches = [license for license in job.get('licenses', [])
                           if within(license['target'], item['field']) and license['answer'] == result['answer']]
                # No matching assignment is explicit, never a fabricated negative.
                selected.append({'field': item['field'], 'answer': result['answer'],
                                 'assignments': [{'target': row['target'], 'operation': row['operation'], 'value': row['value']}
                                                 for row in matches]})
            return selected
        return {key: render(child, texts, jobs, outcomes) for key, child in value.items()}
    if isinstance(value, list):
        return [render(child, texts, jobs, outcomes) for child in value]
    return value
