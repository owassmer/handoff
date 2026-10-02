"""Compare composed fields against an independently mapped whole-unit denominator."""
from __future__ import annotations

from collections import Counter

from pipeline import jev_results
from .consumer import fields


def leaves(value, prefix=''):
    """JSON-pointer leaf paths, retaining empty structures as requirements."""
    if isinstance(value, dict) and value:
        return {p: v for key, child in value.items()
                for p, v in leaves(child, prefix + '/' + key.replace('~', '~0').replace('/', '~1')).items()}
    if isinstance(value, list) and value:
        return {p: v for i, child in enumerate(value) for p, v in leaves(child, prefix + '/' + str(i)).items()}
    return {prefix: value}


def requirements(expectations):
    result = {}
    components = expectations['components']
    if len({row['id'] for row in components}) != len(components):
        raise ValueError('Duplicate independent component ID')
    for component in components:
        for path, value in leaves(component['expected']).items():
            result['component:' + component['id'] + path] = value
    for i, relationship in enumerate(expectations.get('relationships', [])):
        result['relationship:' + str(i)] = relationship
    for case in expectations.get('operating_cases', []):
        for key in ('expected_outputs', 'must_not_output'):
            for i, value in enumerate(case.get(key, [])):
                name = 'case:' + case['id'] + '/' + key + '/' + str(i)
                if name in result:
                    raise ValueError('Duplicate independent operating case requirement')
                result[name] = value
    for i, value in enumerate(expectations.get('negative_controls', [])):
        result['negative:' + str(i)] = value
    return result


def evaluate(output, expectations, mapping, *, case_outputs=None):
    """Mappings are independently reviewed before inference, never inferred here.

    Each requirement maps to exact field comparisons or explicit missing work.
    Case comparisons use actual consumer outputs supplied separately; the engine
    never substitutes expected outputs when consumer execution is absent.
    """
    if mapping.get('format') != 'section-semantics-evaluation-mapping-1':
        raise ValueError('Unknown independent evaluation mapping format')
    if mapping.get('expectations_hash') != jev_results.fingerprint(expectations):
        raise ValueError('Evaluation expectations changed')
    if mapping.get('plan_hash') != output['plan_hash']:
        raise ValueError('Evaluation plan changed')
    required = requirements(expectations)
    entries = mapping['requirements']
    if not isinstance(entries, dict) or set(entries) - required.keys():
        raise ValueError('Evaluation mapping names unknown requirements')
    indexed = fields(output)
    actual_fields = indexed['values']
    cases = case_outputs or {}
    report = []
    for key, meaning in required.items():
        entry = entries.get(key)
        row = {'requirement': key, 'independent_meaning': meaning}
        if not entry or not entry.get('checks'):
            row.update(status='unmapped', reason=(entry or {}).get('missing_reason', 'No independently mapped check'))
            report.append(row)
            continue
        checks = []
        for check in entry['checks']:
            kind = check.get('kind')
            if key.startswith('case:') and (kind != 'case' or
                    check.get('case_id') != key.split('/', 1)[0][len('case:'):]):
                raise ValueError('Operating-case requirements need output from that actual case')
            if kind == 'field':
                present = check['target'] in actual_fields
                actual = actual_fields.get(check['target'])
            elif kind == 'case':
                case = cases.get(check['case_id'])
                case_fields = leaves(case) if case is not None else {}
                present = check['pointer'] in case_fields
                actual = case_fields.get(check['pointer'])
            else:
                raise ValueError('Unknown independent comparison kind')
            if 'expected' not in check:
                raise ValueError('An independently established comparison value is required')
            checks.append({'check': check, 'status': 'missing' if not present else
                           'correct' if jev_results.fingerprint(actual) == jev_results.fingerprint(check['expected']) else 'incorrect',
                           'actual': actual, 'present': present})
        row['checks'] = checks
        row['status'] = ('correct' if all(c['status'] == 'correct' for c in checks) else
                         'incorrect' if any(c['status'] == 'incorrect' for c in checks) else 'missing')
        report.append(row)
    counts = dict(Counter(row['status'] for row in report))
    return {'format': 'section-semantics-evaluation-1', 'plan_hash': output['plan_hash'],
            'requirements': report, 'counts': counts, 'denominator': len(required),
            'all_requirements_met': bool(required) and all(row['status'] == 'correct' for row in report),
            'open_semantic_items': indexed['open_items'],
            'sampling_note': 'Requirement checks within one source unit are dependent; '
                             'these counts are not independent trials or a generalization estimate.'}
