import pathlib,json,urllib.request,urllib.parse,concurrent.futures,subprocess,hashlib,re
p=pathlib.Path(__file__).parent
rows=json.loads((p/'revize-document-candidates.json').read_text())
urls={urllib.parse.unquote(u.split('?')[0]):{'url':u,'timestamp':t} for t,u,m in rows}
for u in json.loads((p/'dec2025-cdbg-links.json').read_text()):
 if u.startswith('Documents/'):
  v='https://cms3.revize.com/revize/huntingtonbeachca/'+u
  key=urllib.parse.unquote(v.split('?')[0]);urls.setdefault(key,{'url':v})
selected=[]
for key,r in urls.items():
 name=key.rsplit('/',1)[-1];low=name.lower()
 if any(z in low for z in ['2024','2025','2026']) and any(z in low for z in ['handbook','caper','con plan','consolidated-plan','action plan','aap','cdbg application','cdbg-application']):
  if any(z in low for z in ['notice','public hearing','citizen']):continue
  r['label']=name;r['key']=hashlib.sha256(key.encode()).hexdigest()[:12];selected.append(r)
(p/'carrier-manifest.json').write_text(json.dumps(selected,indent=2))
def fetch(r):
 url=urllib.parse.quote(r['url'],safe=':/?=&%');dest=p/('carrier-'+r['key']+'.pdf');result=dict(r)
 try:
  b=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read()
  if not b.startswith(b'%PDF'):raise ValueError('Not PDF: '+str(b[:100]))
  dest.write_bytes(b);subprocess.run(['pdftotext','-layout',str(dest),str(dest.with_suffix('.txt'))],check=True,capture_output=True);s=dest.with_suffix('.txt').read_text();result.update({'bytes':len(b),'text_chars':len(s),'file':dest.name,'hits':[]})
  for m in re.finditer(r'operating\s+guidelines|exhibit\s+a|25-16978|401289|401293|families\s+forward|mercy\s+house|\bTBRA\b',s,re.I):result['hits'].append({'term':m.group(),'offset':m.start(),'page':s[:m.start()].count('\f')+1,'context':s[max(0,m.start()-180):m.end()+400]})
 except Exception as e:result['error']=str(e)
 (p/('carrier-'+r['key']+'-result.json')).write_text(json.dumps(result,indent=2));return r['label'],result.get('text_chars'),len(result.get('hits',[])),result.get('error')
if __name__=='__main__':
 print('selected',len(selected),flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:
  for z in e.map(fetch,selected):print(z,flush=True)
