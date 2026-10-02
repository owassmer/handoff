"""Copy bill identifiers/headings and announced actions from saved official Governor indexes.
This performs transcription only. Scope decisions are in bill_scope.json.
"""
from pathlib import Path
import re,json
HERE=Path(__file__).resolve().parent
rows={}
for f in sorted((HERE/'sources').glob('*.txt')):
    for block in f.read_text().split('--------------------------------------------------------------------------------'):
        m=re.search(r'^.*\((https://www.gov.ca.gov/2026/[^)]+)\)',block.strip())
        if not m:continue
        url=m[1]
        for l in block.splitlines():
            m=re.search(r'\* (AB|SB) (\d+) (?:by\s+|Senator )(.+)',l)
            if not m:continue
            bid=m[1]+m[2]
            # Delimit the title after the author, not at a dash inside a district name.
            tail=m[3]
            author_end=re.search(r'\([DRI][^)]*\)\s*[—–-]*\s*',tail)
            if author_end: tail=tail[author_end.end():]
            else: tail=re.split(r'\s+[—–]\s*|\s+-–-\s*',tail,maxsplit=1)[-1]
            title=tail.strip(' -–—\u00a0')
            title=re.split(r'A (?:veto|signing) message|View signing',title)[0].strip(' -–—.')
            if not title:continue
            row={'id':bid,'title':title,'status':'vetoed' if 'veto message' in l else 'signed',
                 'source_url':url,'source_capture':str(f.relative_to(HERE.parent)),
                 'text_url':'https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260'+bid}
            rows[bid]=row
(HERE/'bill_candidates.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
print(len(rows),'officially announced bill actions transcribed')
