import pathlib,subprocess,json,concurrent.futures,re
p=pathlib.Path(__file__).parent
jobs=[]
for key in ['84138911a4f7','6f73e9e86a50','a0e13d4ace57','121ff6ae16be','bef73b466cc9']:
 f=p/('carrier-'+key+'.txt')
 if f.exists():
  for i,t in enumerate(f.read_text().split('\f')[:-1],1):
   if len(t.strip())<80:jobs.append((key,i))
def run(job):
 key,page=job;pdf=p/('carrier-'+key+'.pdf');base=p/('ocr-'+key+'-page'+str(page));img=base.with_suffix('.png')
 subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1800','-singlefile','-png',str(pdf),str(base)],capture_output=True,check=True)
 subprocess.run(['tesseract',str(img),str(base)],capture_output=True,check=True);s=base.with_suffix('.txt').read_text();img.unlink();return {'carrier':key,'page':page,'text_file':base.with_suffix('.txt').name,'text_chars':len(s),'hits':[{'term':m.group(),'context':s[max(0,m.start()-150):m.end()+400]} for m in re.finditer(r'operating\s+guidelines|exhibit\s+a|25-16978|401289|401293|families\s+forward|mercy\s+house|\bTBRA\b',s,re.I)]}
if __name__=='__main__':
 print('OCR pages',len(jobs),flush=True);out=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:
  for r in e.map(run,jobs):out.append(r);print(r['carrier'],r['page'],r['text_chars'],len(r['hits']),flush=True);(p/'ocr-carrier-results.json').write_text(json.dumps(out,indent=2))
