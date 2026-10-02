import pytest
from pipeline import core, jev


def test_existing_registry_serializes_identically():
    reg = core.questions()
    prof = {'jev': {'scope': 'a California residential unit'}}
    rules = '\n'.join(f'- {jev.fill(r, prof)}' for r in reg['global_rules'])
    expected = {q['id']: {'primitive': q['primitive'],
        'instructions': f"Global rules:\n{rules}\n\nQuestion:\n{jev.fill(q['prompt']['instructions'], prof)}",
        'criteria': {k: jev.fill(v, prof) for k, v in q['prompt']['criteria'].items()}}
        for q in reg['questions']}
    assert jev.built_questions(reg, prof) == expected


def test_native_types_and_structures_survive_together():
    pytest.importorskip('typesafe_sdk')
    specs = {
        'binary': {'primitive': 'noul', 'instructions': {'question': 'Does this define a term?', 'term': 'tenant'}},
        'selection': {'primitive': 'choice', 'instructions': 'Which meaning fits?',
                      'criteria': {'a': {'definition': 'occupant'}, 'b': ['owner']}},
        'ordered': {'primitive': 'score', 'instructions': ['Rate document legibility.'],
                    'criteria': [{'level': 'Unreadable'}, {'level': 'Partly readable'}, {'level': 'Readable'}]},
        'bounded': {'primitive': 'noul', 'instructions': 'Is the text legible?',
                    'criteria': {'true': {'description': 'Can read text'}, 'false': 'Cannot read text'}}}
    built = jev.sdk_questions(specs)
    for key, spec in specs.items():
        wire = built[key].model_dump(mode='json')
        assert wire['type'] == spec['primitive']
        assert wire['instructions'] == spec['instructions']
        if 'criteria' in spec:
            assert wire['criteria'] == spec['criteria']
    assert built['binary'].criteria is None


def test_structured_registry_scope_and_optional_criteria():
    reg = {'questions': [{'id': 'q', 'primitive': 'noul',
                         'prompt': {'instructions': {'question': 'Applies to {scope}?', 'examples': ['{scope}', None]}}}]}
    spec = jev.built_questions(reg, {'jev': {'scope': 'this tenancy'}})
    assert spec['q']['instructions'] == {'question': 'Applies to this tenancy?', 'examples': ['this tenancy', None]}
    assert 'criteria' not in spec['q']


def test_unknown_primitive_rejected_instead_of_becoming_choice():
    pytest.importorskip('typesafe_sdk')
    with pytest.raises(ValueError, match='Unknown Jev primitive'):
        jev.sdk_questions({'q': {'primitive': 'typo', 'instructions': 'Question', 'criteria': {'a': 'A', 'b': 'B'}}})
