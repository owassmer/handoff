"""Official-primary acquisition only; no labels or inference."""
from pathlib import Path
import urllib.request,hashlib,json,datetime,re,subprocess,concurrent.futures
from html.parser import HTMLParser
B=Path(__file__).parent;S=B/'heldout_ds_sources';S.mkdir(exist_ok=True)
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip-=1
 def handle_data(self,d):
  if not self.skip and d.strip():self.parts.append(d.strip())
def capture(row):
 id,url,family,lineage=row
 try:
  request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  r=urllib.request.urlopen(request,timeout=65);data=r.read();pdf=data.startswith(b'%PDF');ext='.pdf'if pdf else'.xml'if url.endswith('.xml')else'.html'
  if not pdf and any(x in data for x in [b'Page Not Found | GovInfo',b'Site is currently under maintenance']):raise RuntimeError('official soft404/maintenance response, not operative text')
  raw=S/(id+ext);raw.write_bytes(data);txt=S/(id+'.txt')
  if pdf:subprocess.run(['pdftotext','-layout',str(raw),str(txt)],check=True);text=txt.read_text()
  else:
   encoding='windows-1252'if b'charset=windows-1252'in data[:10000]else'utf-8';parser=Text();parser.feed(data.decode(encoding,errors='replace'));text='\n'.join(parser.parts)
  text=text.replace('\r\n','\n').replace('\r','\n');txt.write_text(text)
  return {'id':id,'url':url,'resolved_url':r.url,'family':family,'authority_lineage':lineage,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raw_path':str(raw.relative_to(B.parents[2])),'raw_sha256':hashlib.sha256(data).hexdigest(),'text_path':str(txt.relative_to(B.parents[2])),'text_sha256':hashlib.sha256(txt.read_bytes()).hexdigest(),'text_characters':len(text),'status':'captured','extraction':'HTMLParser data nodes or pdftotext-layout; UTF8 LF text'}
 except Exception as e:return {'id':id,'url':url,'status':'failed','reason':str(e)}
def run(rows):
 old=json.loads((S/'manifest.json').read_text())if(S/'manifest.json').exists()else[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=8)as ex:
  for row in ex.map(capture,rows):old.append(row);print(row['id'],row['status'],row.get('text_characters',row.get('reason')))
 (S/'manifest.json').write_text(json.dumps(old,indent=2)+'\n')
if __name__=='__main__':
 regs=[(24,4,'982.4'),(24,1,'100.20'),(12,8,'1024.2'),(12,8,'1022.3'),(16,1,'433.1'),(16,1,'444.1'),(16,1,'310.2'),(29,3,'825.102'),(40,34,'745.103'),(31,3,'1010.100'),(24,4,'982.351'),(24,1,'100.60'),(12,8,'1024.17'),(12,8,'1022.43'),(16,1,'433.2'),(16,1,'444.2'),(16,1,'310.4'),(29,3,'825.300'),(40,34,'745.107'),(31,3,'1010.311')]
 rows=[]
 for title,vol,section in regs:
  key=f'CFR2024_{title}_{section.replace(".","_")}';name=f'CFR-2024-title{title}-vol{vol}';url=f'https://www.govinfo.gov/content/pkg/{name}/xml/{name}-sec{section.replace(".","-")}.xml';rows.append((key,url,'regulatory',f'2024annual:{title}CFRpart{section.split(".")[0]}'))
 for s in ['83.43','83.51','83.49','83.56']:rows.append(('FL_'+s.replace('.','_'),'https://www.flsenate.gov/Laws/Statutes/2025/'+s,'statutory','Florida2025Chapter83'))
 for s in ['55.1-1200','55.1-1220','55.1-1226','55.1-1245']:rows.append(('VA_'+s.replace('.','_'),'https://law.lis.virginia.gov/vacode/title55.1/chapter12/section'+s+'/','statutory','VirginiaCodeTitle55.1Chapter12'))
 for s in ['504B.001','504B.161','504B.178','504B.211']:rows.append(('MN_'+s.replace('.','_'),'https://www.revisor.mn.gov/statutes/cite/'+s,'statutory','MinnesotaChapter504B'))
 for chapter in ['PR.92','BC.17','LA.61','CP.92']:code,num=chapter.split('.');rows.append(('TX_'+code+'_'+num,f'https://statutes.capitol.texas.gov/Docs/{code}/htm/{code}.{num}.htm','statutory','Texas'+chapter))
 for s in ['33-1310','33-1324','33-1321','33-1341']:rows.append(('AZ_'+s,'https://www.azleg.gov/ars/33/'+s.split('-')[1].zfill(5)+'.htm','statutory','ArizonaTitle33Chapter10'))
 run(rows)
