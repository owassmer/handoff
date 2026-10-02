import fs from 'node:fs/promises';
import {Workbook} from '@oai/artifact-tool';

const destination='/workspace/scratch/f54fe3f34593/deliverables/01_playbook';
const templates={
  Case_Log:[
    'Case ID','Case type','Home or asset','Original promised result','Original promised date',
    'Current promised date','Current blocker','Next action','Responsible person','Budget',
    'Actual cost','Currency','Key dates','Outcome and quality check','Open duties and owner',
    'Handling minutes','Value and attribution notes','Record reference'
  ],
  Event_Log:[
    'Event ID','Case ID','Event time','Actor','Event or decision','Facts available','Action',
    'Authority','Confirmed result','Next action and owner','Person-minutes','Handling party',
    'Amount','Currency','Amount type','Attribution and uncertainty','Source reference'
  ],
  Provider_Comparison:[
    'Provider','Case ID','Promised outcome','Accepted responsibility','Required inputs',
    'Permitted actions','Remaining operator work','Exception and recovery','Quality verification',
    'Implementation cost','Ongoing price and basis','Currency','Incremental cost',
    'Quote scope and volume','Evidence seen','Open questions','Source or quote reference'
  ],
  Pilot_Scorecard:[
    'Pilot or cohort','Metric','Unit','Scope and dates','Baseline value','Baseline case count',
    'Pilot value','Pilot case count','Change','Target','Comparison method','Value status',
    'Source reference','Attribution limits','Decision','Next action and owner'
  ]
};
await fs.mkdir(destination,{recursive:true});
const workbook=Workbook.create();
const quote=value=>/[",\r\n]/.test(String(value))?'"'+String(value).replaceAll('"','""')+'"':String(value);
for(const [name,headers] of Object.entries(templates)){
  if(new Set(headers).size!==headers.length)throw new Error(`Duplicate header: ${name}`);
  const sheet=workbook.worksheets.add(name);
  sheet.getRangeByIndexes(0,0,1,headers.length).values=[headers];
  const authored=sheet.getRangeByIndexes(0,0,1,headers.length).values[0];
  await fs.writeFile(`${destination}/${name}.csv`,authored.map(quote).join(',')+'\r\n','utf8');
}
workbook.recalculate();
console.log(JSON.stringify(Object.fromEntries(Object.entries(templates).map(([name,headers])=>[name,{columns:headers.length,dataRows:0}]))));
