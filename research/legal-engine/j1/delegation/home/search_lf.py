import json,subprocess,pathlib,concurrent.futures
P=pathlib.Path(__file__).parent
BASE='https://records.huntingtonbeachca.gov/WebLink/'
def post(endpoint,data):
 r=subprocess.run(['curl','--max-time','60','-c',str(P/'cookies.txt'),'-b',str(P/'cookies.txt'),'-fsSL',BASE+endpoint,'-H','Content-Type: application/json','--data',json.dumps(data)],capture_output=True,text=True,check=True)
 return json.loads(r.stdout)['data']
def search(pair):
 name,q=pair
 a=post('SearchService.aspx/GetSearchListing',{'repoName':'COHB','searchSyn':q,'searchUuid':'','sortColumn':'','startIdx':0,'endIdx':1000,'getNewListing':True,'sortOrder':0,'displayInGridView':False})
 (P/(name+'.json')).write_text(json.dumps(a,indent=2));print(name,a.get('hitCount'),a.get('errMsg'));return name,a
if __name__=='__main__':
 qs=[('tbra-all','"TBRA"'),('rental-guidelines','"Rental Assistance" & "Guidelines"'),('home-amendment','"HOME" & "Subrecipient" & "amendment"'),('tbra-2025','"TBRA" & "2025"')]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
  for name,a in ex.map(search,qs):
   print(name,[(r['entryId'],r['name']) for r in a.get('results',[])])
