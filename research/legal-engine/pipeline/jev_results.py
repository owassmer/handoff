"""Identity and validation for reusable Jev judgments; no semantic routing decisions."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile

FORMAT = 'jev-result-2'
ASSEMBLY = 'pipeline-section-state-1'


def serialized(value):
    # Object order is immaterial; list order remains material. No coercion or NaN.
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False, sort_keys=True)


def fingerprint(value):
    return hashlib.sha256(serialized(value).encode()).hexdigest()


def identity(registry, questions, state):
    return {'format': FORMAT, 'assembly_version': ASSEMBLY,
            'base_url': registry['base_url'], 'model': registry['model'],
            'pinned_build': registry['pinned_build'], 'registry_version': registry['registry_version'],
            'question_versions': {q['id']: q['version'] for q in registry['questions']},
            'questions': questions, 'state': state}


def number(value, low, high, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError('Invalid ' + name)


def distribution(value, keys):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError('Probability keys do not match criteria')
    for p in value.values():
        number(p, 0, 1, 'probability')
    # Provider answers round probabilities; do not renormalize missing mass.
    if abs(sum(value.values()) - 1) > .02 + 1e-9:
        raise ValueError('Probabilities do not sum to one within 0.02')


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError('Missing origin timestamp')
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise ValueError('Invalid origin timestamp') from exc
    if parsed.tzinfo is None:
        raise ValueError('Origin timestamp must include timezone')


def usage_cost(raw):
    usage = raw.get('usage')
    if usage is None:
        return None
    if not isinstance(usage, dict):
        raise ValueError('Invalid usage object')
    cost = usage.get('cost')
    if cost is None:
        return None
    try:
        parsed = Decimal(str(cost))
    except InvalidOperation as exc:
        raise ValueError('Invalid reported cost') from exc
    if isinstance(cost, bool) or not parsed.is_finite() or parsed < 0:
        raise ValueError('Invalid reported cost')
    return parsed


def validate(raw, request):
    if not isinstance(raw, dict) or raw.get('model') != request['pinned_build']:
        raise ValueError('Unexpected model build')
    usage_cost(raw)
    questions = request['questions']
    answers = raw.get('answers')
    if not isinstance(answers, dict) or set(answers) != set(questions):
        raise ValueError('Missing or unexpected answer IDs')
    for key, spec in questions.items():
        answer = answers[key]
        kind = spec['primitive']
        if not isinstance(answer, dict) or answer.get('type') != kind:
            raise ValueError('Wrong answer type for ' + key)
        if kind == 'noul':
            number(answer.get('noul'), 0, 1, 'Noul')
        elif kind == 'choice':
            criteria = spec['criteria']
            if not isinstance(criteria, dict) or not criteria:
                raise ValueError('Invalid Choice criteria')
            choice = answer.get('choice')
            if not isinstance(choice, str) or choice not in criteria:
                raise ValueError('Unknown Choice value')
            distribution(answer.get('probabilities'), criteria)
            number(answer.get('confidence'), 0, 1, 'Choice confidence')
            if answer['probabilities'][choice] < max(answer['probabilities'].values()):
                raise ValueError('Choice contradicts highest probability')
        elif kind == 'score':
            criteria = spec['criteria']
            if not isinstance(criteria, list) or not criteria:
                raise ValueError('Invalid Score criteria')
            if answer.get('legend') != {str(i): value for i, value in enumerate(criteria)}:
                raise ValueError('Score legend does not match requested criteria')
            distribution(answer.get('probabilities'), [str(i) for i in range(len(criteria))])
            number(answer.get('score'), 0, len(criteria)-1, 'Score')
            number(answer.get('confidence'), 0, 1, 'Score confidence')
            mean = sum(int(k)*p for k, p in answer['probabilities'].items())
            if abs(answer['score']-mean) > .05 + 1e-9:
                raise ValueError('Score contradicts its distribution')
        else:
            raise ValueError('Unsupported answer primitive ' + str(kind))
    return answers


def envelope(request, raw, created):
    validate(raw, request)
    timestamp(created)
    return {'format': FORMAT, 'request_hash': fingerprint(request), 'request': request,
            'created_at': created, 'response_hash': fingerprint(raw), 'raw': raw}


def validate_entry(entry, request):
    if not isinstance(entry, dict) or entry.get('format') != FORMAT:
        raise ValueError('Legacy or unknown cache format: complete origin identity is unavailable')
    expected = fingerprint(request)
    if entry.get('request_hash') != expected or fingerprint(entry.get('request')) != expected:
        raise ValueError('Cached request identity mismatch')
    timestamp(entry.get('created_at'))
    validate(entry.get('raw'), request)
    if entry.get('response_hash') != fingerprint(entry['raw']):
        raise ValueError('Cached response identity mismatch')
    return entry


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError('Nonfinite JSON number: ' + value)


def read(path, request):
    try:
        return validate_entry(json.loads(Path(path).read_text(), object_pairs_hook=unique_object,
                                               parse_constant=invalid_constant), request), None
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
        return None, f'{type(exc).__name__}: {exc}'


def atomic_write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    name = None
    try:
        with tempfile.NamedTemporaryFile(mode='wb', dir=path.parent, delete=False) as f:
            name = f.name
            f.write(text.encode("utf-8") if isinstance(text, str) else text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if name is not None and os.path.exists(name):
            os.unlink(name)
