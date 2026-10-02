import json
from pathlib import Path
b=Path(__file__).resolve().parent
ledger=json.loads((b/'q4-final-disposition-ledger.json').read_text())
actions=json.loads((b/'q4-2025-action-census.json').read_text())['actions']
rows=json.loads((b/'q4-row-decisions.json').read_text())
for n,(action,row) in enumerate(zip(actions,rows),1):
    assert (n,action['title'],action['filed_on'],action['action']) == (row['row'],row['title'],row['filed_on'],row['action']), 'Action identity changed; human review required'
assert len(actions)==len(rows)
ledger['rows']=rows
(b/'q4-final-disposition-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
