"""Capture the primary statutory sources used in the assigned-debt investigation."""
import concurrent.futures
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import urllib.request
from html.parser import HTMLParser

class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.hidden=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.hidden+=1
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.hidden=max(0,self.hidden-1)
        if tag in ('p','div','br','h1','h2','h3','h4','h5','h6','li'): self.parts.append('\n')
    def handle_data(self, value):
        if not self.hidden: self.parts.append(value)


ROOT = Path(__file__).resolve().parent
URLS = {f'CIV_{s}': f'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum={s}.&lawCode=CIV'
        for s in ['1788.1','1788.2','1788.14.5','1788.50','1788.52','1788.54','1788.56','1788.58','1788.60','1788.62','1788.64','1788.66']}
URLS.update({'SB531_chaptered':'https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202120220SB531',
             'SB1286_chaptered':'https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240SB1286'})

def fetch(pair):
    name,url=pair
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=60) as response:
            data=response.read();status=response.status;final=response.url
        (ROOT/'sources'/f'{name}.html').write_bytes(data)
        parser=Text(); parser.feed(data.decode('utf-8'))
        body='\n'.join(line.strip() for line in ''.join(parser.parts).splitlines() if line.strip())
        (ROOT/'sources'/f'{name}.txt').write_text(body+'\n')
        return {'id':name,'url':url,'final_url':final,'retrieved_at':datetime.now(timezone.utc).isoformat(),
                'http_status':status,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'text_chars':len(body)}
    except Exception as error:
        return {'id':name,'url':url,'error':str(error)}

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        result=list(pool.map(fetch, URLS.items()))
    (ROOT/'sources.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
