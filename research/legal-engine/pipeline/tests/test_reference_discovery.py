import hashlib
import json

import pytest

from pipeline.reference_discovery import prepare, report


def input_source(tmp_path):
    text = 'SOURCE: bookkeeping\n(a) Follow Rule 3.\n(b) Pay the charge.'
    (tmp_path / 'source.txt').write_text(text)
    start, split = text.index('(a)'), text.index('(b)')
    source = {'id': 'X', 'file': 'source.txt', 'sha256': hashlib.sha256(text.encode()).hexdigest(),
              'body': {'start': start, 'end': len(text)}, 'passages': [
                  {'id': 'p1', 'start': start, 'end': split},
                  {'id': 'p2', 'start': split, 'end': len(text)}]}
    return {'sources': [source]}, {'base_url': 'example', 'model': 'test', 'pinned_build': 'test'}


def test_each_passage_has_answer_and_source_metadata_stays_out(tmp_path):
    prep, registry = input_source(tmp_path)
    requests = prepare(prep, tmp_path, registry)
    wire = requests[0]['expected_wire']
    assert set(wire['questions']) == {'p1', 'p2'}
    assert 'bookkeeping' not in json.dumps(wire)
    assert 'expression' not in json.dumps(wire)
    rows = report(requests, [])['passages']
    assert len(rows) == 2 and all(r['reference_probability'] is None for r in rows)


def test_partition_cannot_skip_text(tmp_path):
    prep, registry = input_source(tmp_path)
    prep['sources'][0]['passages'][1]['start'] += 1
    with pytest.raises(ValueError, match='gap/overlap'):
        prepare(prep, tmp_path, registry)


def test_changed_source_requires_repartitioning(tmp_path):
    prep, registry = input_source(tmp_path)
    (tmp_path / 'source.txt').write_text('Changed law')
    with pytest.raises(ValueError, match='Source changed'):
        prepare(prep, tmp_path, registry)
