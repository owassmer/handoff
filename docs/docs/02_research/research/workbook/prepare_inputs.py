"""Normalize the research inventories for the artifact-tool workbook builder.

Read-only source processing. This file does not author or edit spreadsheets.
Run with CODEX_PRIMARY_RUNTIME_PYTHON and the analysis workspace as its argument.
"""
import csv
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[2]
research = root / 'research'
def rows(name):
    with (research / name).open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))

sources = {row['source_id']: row for row in rows('operating_sources.csv')}
decisions = rows('decision_inventory.csv')
for row in decisions:
    matches = [sources[source_id] for source_id in re.findall(r'O\d+', row['source_ids']) if source_id in sources]
    row['source_urls'] = '\n'.join(source['url'] for source in matches)
    row['source_scope'] = 'Domain anchors support parts of the decision family. The decision taxonomy and automation hypotheses are original synthesis, not claims validated in full by each source.'
    row['source_limitations'] = '\n'.join(source['source_id'] + ': ' + source['limitations'] for source in matches)

for name, data in [('decisions.json', decisions), ('public_data.json', rows('public_data.csv'))]:
    (research / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Prepared {len(decisions)} decision records and public-data JSON.')
