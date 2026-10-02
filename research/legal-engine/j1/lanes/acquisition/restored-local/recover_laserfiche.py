import json,subprocess,pathlib
P=pathlib.Path(__file__).parent
BASE='https://records.huntingtonbeachca.gov/WebLink/'
def post(endpoint,data):
 r=subprocess.run(['curl','-c','/tmp/hb-cookie','-b','/tmp/hb-cookie','-fsSL',BASE+endpoint,'-H','Content-Type: application/json','--data',json.dumps(data)],capture_output=True,text=True,check=True)
 return json.loads(r.stdout)['data']
def search(form,values,name):
 q=post('CustomSearchService.aspx/GetSearchQuery',{'repoName':'COHB','searchFormID':form,'queryValues':values})
 a=post('SearchService.aspx/GetSearchListing',{'repoName':'COHB','searchSyn':q,'searchUuid':'','sortColumn':'','startIdx':0,'endIdx':100,'getNewListing':True,'sortOrder':0,'displayInGridView':False})
 (P/(name+'.json')).write_text(json.dumps(a,indent=2));return a
if __name__=='__main__':
 for name,vals in [('mercy-contracts',{'Contracts_Input3':['Mercy House']}),('tbra-contracts',{'Contracts_Input0':['TBRA']}),('mobilehome-contracts',{'Contracts_Input0':['Mobile Home']})]:
  a=search('Contracts',vals,name)
  print(name,a['hitCount'])
  for r in a['results']:print(r['entryId'],r['name'],[(m['name'],m['values']) for m in r['metadata'] if m['name'] in ['Description','End Date']])
