import json,re
from pathlib import Path
P=Path(__file__).parent
rows=json.loads((P/'jc_rows.json').read_text())
families={'WG','VL','MC','SUM','SER','RA','INT','JUD','CP','CD','EFS','DAL','MIL','CLETS','EPO'}
out={'WG-004',*[f'WG-0{x}' for x in range(20,27)],'MC-1000','MC-200','MC-201','MC-202','MC-500','MC-510','MC-600','MC-600A','MC-800','MIL-100','MIL-183','MIL-184','MIL-412','CLETS-002','EPO-002'}
selected=[x for x in rows if re.match('[A-Z]+',x['number'])[0] in families and x['number'] not in out]
(P/'jc_priority_selected.json').write_text(json.dumps(selected,indent=2)+'\n')
print(json.dumps(selected))
