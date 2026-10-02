"""Mechanical dispatch preparation. Semantic context sufficiency remains agent work."""
from __future__ import annotations

from .run import validate_request


def prepare_dispatch(rows):
    ready, agent_work = [], []
    for row in rows:
        validate_request(row)
        task = next(iter(row['payload']['questions']))
        state = row['payload']['state']
        missing = []
        if task == 'scope_includes_use':
            for role in ('definition_location', 'use_location'):
                location = state.get(role)
                for field in ('instrument', 'unit', 'section_id'):
                    value = location.get(field) if isinstance(location, dict) else None
                    if not isinstance(value, str) or not value.strip():
                        missing.append(f'{role}.{field}')
        if missing:
            agent_work.append({'case_id': row['case_id'], 'request_hash': row['request_hash'],
                               'status': 'needs_context', 'missing_fields': missing,
                               'action': 'Recover and source the missing legal hierarchy, then assemble a new request.',
                               'model_answer': None})
        else:
            ready.append(row)
    return ready, agent_work
