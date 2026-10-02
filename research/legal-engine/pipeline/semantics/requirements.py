"""Resolve judged requirement attachments without inferring case compliance."""
from __future__ import annotations


def select(indexed, path, required_fields=None):
    if not isinstance(path, str) or not path:
        raise ValueError('Requirement selector must be a nonempty field path')
    matches = {key: value for key, value in indexed['values'].items()
               if key == path or key.startswith(path + '.')}
    if required_fields is None:
        required_fields = [path] if path in indexed['values'] else []
    if (not isinstance(required_fields, list) or any(not isinstance(key, str) or not key for key in required_fields)
            or len(set(required_fields)) != len(required_fields)):
        raise ValueError('Required selection fields must be explicit unique paths')
    missing = [key for key in required_fields if key not in indexed['values']]
    matches.update({key: indexed['values'][key] for key in required_fields if key in indexed['values']})
    pending = [row for row in indexed['open_items'] if any(
        key == path or key.startswith(path + '.') or path.startswith(key + '.')
        for key in ([row['target']] if 'target' in row else row.get('candidate_targets', [])))]
    return {'path': path, 'fields': matches,
            'bindings': {key: indexed['bindings'][key] for key in matches},
            'status': 'unresolved' if pending or missing or not required_fields else 'resolved_fields',
            'required_fields': required_fields, 'missing_fields': missing,
            'selection_contract_missing': not required_fields,
            'open_items': pending}


def attachments(indexed, evaluate_condition):
    bundles = []
    for key, relation in indexed['values'].items():
        if not key.startswith('relations.') or not isinstance(relation, dict):
            continue
        execution = relation.get('execution', {})
        if execution.get('operation') != 'attach_requirements':
            continue
        if execution.get('combine') != 'all' or not isinstance(execution.get('requirements'), list) or not execution['requirements']:
            raise ValueError('Requirement attachment needs a nonempty all-of bundle')
        target = select(indexed, execution.get('target'), execution.get('target_required_fields'))
        items = []
        for item in execution['requirements']:
            if not isinstance(item.get('kind'), str) or not item['kind']:
                raise ValueError('Requirement kind must be explicit')
            selected = select(indexed, item.get('path'), item.get('required_fields'))
            conditions = []
            for field in ('when', 'unless'):
                if field in item:
                    path = item[field]
                    if not isinstance(path, str) or not path.startswith('conditions.'):
                        raise ValueError('Conditional requirement needs an explicit condition path')
                    result = evaluate_condition(path)
                    value = result['value']
                    if field == 'unless' and value is not None:
                        value = not value
                    conditions.append({'role': field, 'path': path, 'value': value, 'evaluation': result})
            answers = [condition['value'] for condition in conditions]
            applies = False if False in answers else None if None in answers else True
            items.append({'kind': item['kind'], 'selection': selected, 'applies': applies,
                          'conditions': conditions,
                          'status': 'not_applicable' if applies is False else 'unresolved' if
                          applies is None or selected['status'] != 'resolved_fields' else 'required',
                          'case_compliance': 'not_evaluated'})
        bundles.append({'relationship': key, 'target': target, 'combine': 'all', 'requirements': items,
                        'evidence': indexed['bindings'][key],
                        'status': 'unresolved' if target['status'] != 'resolved_fields' or any(
                            item['status'] == 'unresolved' for item in items) else 'resolved_requirements'})
    return bundles
