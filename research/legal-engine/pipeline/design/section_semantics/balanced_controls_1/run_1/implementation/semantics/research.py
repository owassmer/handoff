"""Supply validated semantic fields to the existing section-review consumer."""
from pathlib import Path

from pipeline import core, jev_results
from .consumer import fields
from .run import read_run


def for_section(section, registration, root):
    root = Path(root).resolve()
    run_path = (root / registration['run']).resolve()
    text_path = (root / section['text_file']).resolve()
    if not run_path.is_relative_to(root) or not text_path.is_relative_to(root):
        raise ValueError('Semantic registration is outside the research root')
    source_hash = core.sha256_file(text_path)
    if source_hash != registration['section_source_sha256']:
        raise ValueError('Registered section source has changed')
    snapshot, state = read_run(run_path, root)
    plan = snapshot['plan']
    if jev_results.fingerprint(plan) != registration['plan_hash']:
        raise ValueError('Registered semantic plan has changed')
    selected = {row['id']: row for row in plan['sources']}
    evidence = registration['section_evidence']
    if not evidence or any(key not in selected or selected[key]['sha256'] != source_hash for key in evidence):
        raise ValueError('Semantic run does not bind the registered section source')
    indexed = fields(state['output'])
    return {'plan_id': plan['id'], 'plan_hash': state['output']['plan_hash'],
            'prepared_work_complete': state['output']['complete'],
            'established_fields': indexed['values'], 'field_evidence': indexed['bindings'],
            'open_items': indexed['open_items'], 'section_evidence': evidence,
            'review_instruction': 'Use established fields directly. Investigate open items and coverage; '
                                  'completed prepared jobs do not establish whole-section completeness.'}
