"""Retrieve the pilot's named missing dependencies from California's official site."""
import concurrent.futures
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
from datetime import datetime, timezone

HERE=Path(__file__).resolve().parent/'dependency-sources'
TARGETS=[('PUC',s) for s in ['777','777.1','10009','10009.1','12822','12822.1','16481','16481.1']]+[('GOV','60371'),('CCP','1280'),('CIV','1929')]

class Section(HTMLParser):
    def __init__(self):super().__init__();self.depth=0;self.parts=[]
    def handle_starttag(self, tag, attrs):
        if tag=='div':
            if self.depth:self.depth+=1
            elif dict(attrs).get('id')=='codeLawSectionNoHead':self.depth=1
        if self.depth and tag in ('p','h4','h5','h6','br'):self.parts.append('\n')
    def handle_endtag(self, tag):
        if self.depth and tag=='div':self.depth-=1
        if self.depth and tag in ('p','h4','h5','h6'):self.parts.append('\n')
    def handle_data(self, data):
        if self.depth:self.parts.append(data)

def fetch(pair):
    code,section=pair;stem=f'{code}-{section}'
    url=f'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode={code}&sectionNum={section}.'
    dest=HERE/f'{stem}.html'
    row={'code':code,'section':section,'url':url,'retrieved_at':datetime.now(timezone.utc).isoformat()}
    try:
        subprocess.run(['curl','-fLsS','--max-time','25',url,'-o',str(dest)],check=True,capture_output=True)
        parser=Section();parser.feed(dest.read_text())
        text='\n'.join(line.strip() for line in ''.join(parser.parts).splitlines() if line.strip())
        if section+'.' not in text or len(text)<100:raise ValueError('No expected statutory body')
        (HERE/f'{stem}.txt').write_text(text+'\n')
        row.update(status='retrieved',html_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
                   text_sha256=hashlib.sha256((HERE/f'{stem}.txt').read_bytes()).hexdigest())
    except Exception as exc:row.update(status='retrieval_failed',error=str(exc))
    return row

if __name__=='__main__':
    HERE.mkdir(exist_ok=False)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(fetch,TARGETS))
    (HERE/'manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps([{k:r[k] for k in ('code','section','status')} for r in rows]))
