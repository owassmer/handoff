"""Consume established semantic fields without reopening source prose."""
from __future__ import annotations

from pipeline import jev_results
from .requirements import attachments


def fields(output):
    """Index supported fields while retaining conflicts and incomplete targets."""
    if output.get('format') != 'section-semantics-output-1':
        raise ValueError('Unknown semantic output format')
    grouped = {}
    open_items = []
    for row in output['field_assignments']:
        if row['status'] == 'supported':
            grouped.setdefault(row['target'], []).append(row)
        elif row['status'] not in {'not_supported', 'not_applicable'}:
            open_items.append(row)
    blocked = {row['target'] for row in open_items if 'target' in row}
    blocked.update(target for row in open_items for target in row.get('candidate_targets', []))
    values, bindings = {}, {}
    for target, rows in grouped.items():
        if target in blocked:
            open_items.append({'target': target, 'status': 'unresolved', 'judgments': rows})
            continue
        if len({jev_results.fingerprint(row['value']) for row in rows}) != 1:
            open_items.append({'target': target, 'status': 'conflicting', 'judgments': rows})
            continue
        values[target] = rows[0]['value']
        bindings[target] = [{'job': row['job'], 'evidence': row['evidence']} for row in rows]
    return {'values': values, 'bindings': bindings, 'open_items': open_items}


def evaluate_conditions(output, facts):
    """Evaluate licensed Boolean groups against established case predicates.

    Facts use exact predicate targets, with True/False/None values. Fact
    interpretation is upstream semantic work. This computes branch conditions;
    it does not authorize actions or silently resolve rule-to-rule exceptions.
    """
    indexed = fields(output)
    values = indexed['values']
    predicates = {key for key in values if key.startswith('conditions.') and key.endswith('.predicate')}
    if not set(facts) <= predicates or any(value is not None and type(value) is not bool for value in facts.values()):
        raise ValueError('Case facts must bind established predicates as Boolean or unknown')
    states, visiting = {}, set()
    effects = {}
    for key, relation in values.items():
        if not key.startswith('relations.') or not isinstance(relation, dict) or 'execution' not in relation:
            continue
        execution = relation['execution']
        operation = execution.get('operation')
        if operation == 'attach_requirements':
            continue
        if operation not in {'set_predicate', 'block_condition', 'require_condition'}:
            indexed['open_items'].append({'target': key, 'status': 'unsupported_relationship_operation',
                                          'execution': execution})
            continue
        target = execution.get('target')
        source = execution.get('condition') if operation == 'require_condition' else execution.get('when')
        if (not isinstance(target, str) or not target.startswith('conditions.') or
                not isinstance(source, str) or not source.startswith('conditions.')):
            raise ValueError('Condition effects require explicit condition paths')
        if operation == 'set_predicate' and (target + '.predicate' not in predicates or type(execution.get('value')) is not bool):
            raise ValueError('A predicate override needs an established predicate and Boolean value')
        if operation == 'block_condition' and target + '.predicate' not in predicates and (
                not isinstance(values.get(target), dict) or values[target].get('operator') not in {'all', 'any', 'not'}):
            raise ValueError('A conditional blocker needs an established condition target')
        if 'unless' in execution and (operation != 'block_condition' or
                not isinstance(execution['unless'], str) or not execution['unless'].startswith('conditions.')):
            raise ValueError('A blocker exception requires an explicit condition path')
        effects.setdefault(target, []).append((key, execution, source))

    def evaluate(target):
        if target in states:
            return states[target]
        if target in visiting:
            return {'value': None, 'reason': 'cyclic_condition', 'target': target}
        visiting.add(target)
        if target + '.predicate' in predicates:
            value = facts.get(target + '.predicate')
            result = {'value': value, 'reason': 'case_fact' if value is not None else 'missing_case_fact',
                      'target': target + '.predicate'}
        else:
            group = values.get(target)
            if not isinstance(group, dict) or group.get('operator') not in {'all', 'any', 'not'}:
                result = {'value': None, 'reason': 'missing_established_group', 'target': target}
            else:
                children = group.get('children')
                if (not isinstance(children, list) or not children or
                        any(not isinstance(key, str) or not key or '.' in key for key in children) or
                        (group['operator'] == 'not' and len(children) != 1)):
                    raise ValueError('Malformed established condition group')
                prefix = target.rsplit('.', 1)[0]
                components = [evaluate(prefix + '.' + child) for child in children]
                answers = [row['value'] for row in components]
                if group['operator'] == 'not':
                    value = None if answers[0] is None else not answers[0]
                elif group['operator'] == 'all':
                    value = False if False in answers else None if None in answers else True
                else:
                    value = True if True in answers else None if None in answers else False
                result = {'value': value, 'operator': group['operator'], 'components': components}
        overrides, conditional, constraints, trace = [], [], [], []
        for key, effect, source in effects.get(target, []):
            trigger = evaluate(source)
            if 'unless' in effect:
                exception = evaluate(effect['unless'])
                answers = [trigger['value'], None if exception['value'] is None else not exception['value']]
                trigger = {'value': False if False in answers else None if None in answers else True,
                           'when': trigger, 'unless': exception,
                           'reason': 'conditional_blocker_exception'}
            trace.append({'relationship': key, 'operation': effect, 'condition': trigger,
                          'evidence': indexed['bindings'][key]})
            if effect['operation'] == 'require_condition':
                constraints.append(trigger['value'])
            elif effect['operation'] == 'block_condition':
                constraints.append(None if trigger['value'] is None else not trigger['value'])
            elif trigger['value'] is True:
                overrides.append(effect['value'])
            elif trigger['value'] is None:
                conditional.append(effect['value'])
        if trace:
            base = result
            possible = set(overrides) if overrides else ({False, True} if base['value'] is None else {base['value']})
            possible.update(conditional)
            value = next(iter(possible)) if len(possible) == 1 else None
            answers = [value] + constraints
            value = False if False in answers else None if None in answers else True
            result = {'value': value, 'base': base, 'effects': trace,
                      'reason': 'conflicting_overrides' if len(set(overrides)) > 1 else 'established_condition_effects'}
        visiting.remove(target)
        states[target] = result
        return result

    branches = []
    for target, role in values.items():
        if not target.startswith('relations.') or '.applies_under.' not in target:
            continue
        record, node = target[len('relations.'):].split('.applies_under.', 1)
        condition = 'conditions.' + record + '.' + node
        branches.append({'record': record, 'condition_role': role, 'condition': evaluate(condition),
                         'relationship_evidence': indexed['bindings'][target]})
    return {'plan_hash': output['plan_hash'], 'branches': branches,
            'requirement_bundles': attachments(indexed, evaluate),
            'open_items': indexed['open_items'],
            'scope': 'Condition evaluation; interacting rule effects require their established relationships.'}
