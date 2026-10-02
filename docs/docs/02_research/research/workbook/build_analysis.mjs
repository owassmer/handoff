import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';

// Run with the Codex primary Node runtime from a scratch folder whose node_modules
// symlink points to CODEX_PRIMARY_RUNTIME_NODE_MODULES. Workbook authoring uses
// only the public artifact-tool API. Inputs are preserved beside this builder.
const root=process.argv[2] || path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const out=process.argv[3] || path.join(root,'deliverables/02_research');
const qa=path.join(root,'research/workbook');
await fs.mkdir(out,{recursive:true}); await fs.mkdir(qa,{recursive:true});
const wb=Workbook.create();
const navy='#243B53', blue='#0000FF', green='#008000', ink='#202C39', muted='#526574', pale='#EDF2F6', yellow='#FFF2CC';
const num='#,##0;(#,##0);"–"';
const money='$#,##0;($#,##0);"–"';
const dec='$#,##0.00;($#,##0.00);"–"';
const pct='0.0%;(0.0%);"–"';
const sheets={};
for(const n of ['Economics','Assumptions','Sensitivity','Decisions','Competitors','Public data']) sheets[n]=wb.worksheets.add(n);
function val(s,a,v){s.getRange(a).values=[[v]];}
function formula(s,a,v){s.getRange(a).formulas=[[v]];}
function base(s,last='H80'){
  s.showGridLines=false;
  s.getRange(`A1:${last}`).format.font={name:'Arial',size:10,color:ink};
  s.getRange(`A1:${last}`).format.verticalAlignment='center';
}
function title(s,text,last='F'){
  val(s,'B2',text); s.getRange('B2').format.font={name:'Arial',size:16,bold:true,color:navy};
  s.getRange(`B3:${last}3`).format.borders={bottom:{style:'thin',color:navy}};
  s.getRange('A1:A90').format.columnWidth=3;
}
function section(s,r,text,last='D'){
  val(s,`B${r}`,text);s.getRange(`B${r}:${last}${r}`).format={fill:pale,font:{name:'Arial',bold:true,color:navy},rowHeight:24};
}
function total(s,r){s.getRange(`B${r}:D${r}`).format.font.bold=true;s.getRange(`B${r}:D${r}`).format.borders={top:{style:'thin',color:'#ABBAC8'}};}
function label(s,r,text,form,fmt=num,note=''){
  val(s,`B${r}`,text);formula(s,`D${r}`,form);s.getRange(`D${r}`).setNumberFormat(fmt);
  if(note)val(s,`F${r}`,note);
}

// One authoritative input set. All values below are illustrations, not operator observations.
const inputs=[
 ['Managed units',1000,'units','Illustration; replace with the actual portfolio.'],
 ['Annual turnover share',0.35,'share','Turn illustration, not repair-ticket volume. This is an assumption, not a market estimate.'],
 ['Share of turns eligible for the paid service',1,'share','Measure eligibility against an explicit scope, before choosing completed examples.'],
 ['Net manager minutes saved per serviced turn',60,'minutes/turn','Deduct new review, correction and escalation work before entering this value.'],
 ['Loaded manager labor cost per hour',45,'USD/hour','Illustrative loaded labor cost; not a measured employer burden.'],
 ['Share of saved time converted to cash value',0.50,'share','Count reduced paid time, avoided hires, or evidenced contribution; not all freed capacity.'],
 ['Owner actual expense reduction per turn',0,'USD/turn','No cost savings assumed. Replace only with demonstrated actual expense reductions.'],
 ['Owner added collected revenue per turn',null,'USD/turn','Calculated from monthly rent and collected rent days recovered below.'],
 ['Manager marginal fee on added revenue',0.08,'share','Applies only to additional collected revenue, not owner expense savings.'],
 ['Buyer share of remaining owner economics',1,'share','1 = integrated owner/operator; 0 = independent manager. Intermediate shares require a real contract.'],
 ['Monthly platform price',0,'USD/month','Test price only. Compare total price with the cost floor and buyer benefit ceiling.'],
 ['Price per eligible serviced turn',100,'USD/turn','Illustrative test quote, not a market rate. The workbook separately calculates economic bounds.'],
 ['Routine provider human minutes per turn',20,'minutes/turn','Unvalidated handling assumption. Include monitoring and routine corrections.'],
 ['Share of serviced turns with an exception',0.25,'share','Unvalidated assumption. Count exceptions over all eligible serviced turns.'],
 ['Additional provider minutes per exception',60,'minutes/exception','Unvalidated handling assumption. Additional to routine work; measure the tail.'],
 ['Loaded provider human cost per hour',35,'USD/hour','Illustrative blended handling cost.'],
 ['Model and communications cost per turn',2,'USD/turn','Include model calls, telephone, SMS and other volume-linked service costs.'],
 ['Recurring support and integration cost',400,'USD/month','Customer-specific maintenance/support, excluding per-turn human handling above.'],
 ['One-time onboarding and integration hours',20,'hours','Include implementation, configuration and initial data cleanup.'],
 ['Loaded onboarding cost per hour',50,'USD/hour','Illustrative implementation labor cost.'],
 ['Months to allocate onboarding cost',12,'months','Management contribution view; not a cash-flow forecast.'],
 ['Monthly rent for the average turning unit',2000,'USD/month','Illustration. Replace with the actual units entering the measured turn cohort.'],
 ['Collected rent days recovered per turn',3,'days/turn','Pure stress input, not expected savings. Readiness matters only when days become collected rent.'],
 ['Days in monthly-rent conversion',30,'days/month','Explicit pricing convention for the illustration. Use the contract or accounting convention.'],
 ['Provider contribution target for price test',0.60,'share','Optional pricing assumption. Illustrative 60%, before sales, central engineering, overhead and taxes.']
];
const a=sheets.Assumptions;base(a,'G34');title(a,'Editable assumptions','F');a.tabColor='#59758C';
val(a,'B4','Vacant-unit readiness. All commercial inputs are illustrative, not measured results.');
a.getRange('B4').format.font={italic:true,color:muted};
a.getRange('B6:D6').values=[['Input','Unit','Value']];a.getRange('F6').values=[['Definition and measurement']];
a.getRange('B6:D6').format={fill:navy,font:{color:'#FFFFFF',bold:true},rowHeight:25};
a.getRange('F6').format={fill:navy,font:{color:'#FFFFFF',bold:true},rowHeight:25};
for(let i=0;i<inputs.length;i++){
 const r=7+i; const [name,v,unit,note]=inputs[i];
 a.getRange(`B${r}:D${r}`).values=[[name,unit,v]];val(a,`F${r}`,note);
 a.getRange(`D${r}`).format={fill:yellow,font:{color:blue},horizontalAlignment:'right'};
 a.getRange(`D${r}`).setNumberFormat(unit==='share'?pct:unit.startsWith('USD')?dec:unit==='items/unit/month'?'0.00':num);
 a.getRange(`F${r}`).format.wrapText=true;
 a.getRange(`B${r}:F${r}`).format.rowHeight=42;
 if(unit==='share')a.getRange(`D${r}`).dataValidation={rule:{type:'decimal',operator:'between',formula1:0,formula2:1}};
}
a.getRange('D14').formulas=[['=IF(COUNT(D28:D30)<3,"n.a.",IF(D30>0,D28*D29/D30,"n.a."))']];a.getRange('D14').format={fill:'#FFFFFF',font:{color:'#000000'}};
a.getRange('B7:B31').format.wrapText=true;
a.getRange('B1:B34').format.columnWidth=48;a.getRange('C1:C34').format.columnWidth=19;a.getRange('D1:D34').format.columnWidth=16;a.getRange('E1:E34').format.columnWidth=3;a.getRange('F1:F34').format.columnWidth=78;
val(a,'B33','Yellow cells are editable inputs. Collected rent recovery and time conversion need field validation.');
val(a,'B34','The model keeps manager fees, owner economics and service-provider costs separate.');
a.freezePanes.freezeRows(6);

const e=sheets.Economics;base(e,'G77');title(e,'Vacant-unit readiness economics');e.tabColor=navy;
e.getRange('B1:B77').format.columnWidth=51;e.getRange('C1:C77').format.columnWidth=3;e.getRange('D1:D77').format.columnWidth=17;e.getRange('E1:E77').format.columnWidth=3;e.getRange('F1:F77').format.columnWidth=82;
e.getRange('B4:F77').format.rowHeight=23;
e.getRange('D6:D69').format.horizontalAlignment='right';
val(e,'B4','Monthly values in USD unless stated. Illustrative assumptions, not a forecast or market estimate.');e.getRange('B4').format.font={italic:true,color:muted};
section(e,6,'Monthly results');
label(e,7,'Buyer net cash-equivalent value','=D34-D35',money,'Manager cash benefit plus the buyer’s owner economics, less the product fee.');
label(e,8,'Owner value retained outside the buyer','=D32',money,'Avoid counting this as manager willingness to pay without an actual sharing agreement.');
label(e,9,'Provider contribution after customer delivery costs','=D51',money,'Before sales, central engineering, overhead and taxes.');
label(e,10,'Provider contribution margin','=D52',pct);
total(e,7);total(e,9);
section(e,13,'Work volume and manager labor');
label(e,14,'Managed units',"=IF(ISNUMBER('Assumptions'!D7),'Assumptions'!D7,\"n.a.\")",num);
label(e,15,'Turns per month',"=IF(ISNUMBER('Assumptions'!D8),D14*'Assumptions'!D8/12,\"n.a.\")",'#,##0.0');
label(e,16,'Eligible serviced turns per month',"=IF(ISNUMBER('Assumptions'!D9),D15*'Assumptions'!D9,\"n.a.\")",'#,##0.0');
label(e,17,'Manager hours released per month',"=D16*'Assumptions'!D10/60",'0.0');
label(e,18,'Labor capacity value',"=D17*'Assumptions'!D11",money,'A capacity equivalent. It is not automatically reduced payroll or added profit.');
label(e,19,'Realized manager labor value',"=D18*'Assumptions'!D12",money);
total(e,19);
section(e,22,'Owner, manager and buyer value');
label(e,23,'Owner actual expense reduction',"=D16*'Assumptions'!D13",money);
label(e,24,'Owner additional collected revenue',"=D16*'Assumptions'!D14",money);
label(e,25,'Total owner improvement before added fees','=D23+D24',money);
label(e,26,'Manager fees on additional revenue',"=D24*'Assumptions'!D15",money);
label(e,27,'Owner improvement after manager fees','=D25-D26',money);
label(e,29,'Standalone manager cash benefit','=SUM(D19,D26)',money,'Excludes owner expense savings and the value of unused capacity.');
label(e,30,'Buyer ownership or contractual economic share',"='Assumptions'!D16",pct);
label(e,31,'Owner economics captured by buyer','=D27*D30',money);
label(e,32,'Owner economics retained outside buyer','=D27-D31',money);
label(e,34,'Buyer value before product price','=SUM(D29,D31)',money);
label(e,35,'Product price to buyer',"='Assumptions'!D17+D16*'Assumptions'!D18",money);
label(e,36,'Buyer net value','=D34-D35',money);
label(e,37,'Buyer value / product price','=IF(D35=0,"n.a.",D34/D35)','0.00"x"');
total(e,25);total(e,34);total(e,36);
section(e,40,'Provider delivery costs and contribution');
label(e,41,'Routine handling minutes per serviced turn',"='Assumptions'!D19",'0.0');
label(e,42,'Expected additional exception minutes per turn',"='Assumptions'!D20*'Assumptions'!D21",'0.0');
label(e,43,'Human handling cost per serviced turn',"=SUM(D41:D42)/60*'Assumptions'!D22",dec);
label(e,44,'Model and communications cost per turn',"='Assumptions'!D23",dec);
label(e,45,'Variable delivery cost per turn','=SUM(D43:D44)',dec);
label(e,46,'Monthly variable delivery cost','=D16*D45',money);
label(e,47,'Recurring support and integration cost',"='Assumptions'!D24",money);
label(e,48,'One-time onboarding cost',"='Assumptions'!D25*'Assumptions'!D26",money);
label(e,49,'Allocated monthly onboarding cost',"=IF('Assumptions'!D27>0,D48/'Assumptions'!D27,\"n.a.\")",money,'The one-time cash outlay is shown above. Allocation spreads it over the assumed period.');
label(e,50,'Total monthly customer delivery cost','=SUM(D46:D47,D49)',money);
label(e,51,'Provider contribution','=D35-D50',money);
label(e,52,'Provider contribution margin','=IF(D35=0,"n.a.",D51/D35)',pct);
total(e,45);total(e,50);total(e,51);
section(e,55,'Price and volume constraints');
label(e,56,'Buyer zero-net-value total monthly price','=D34',money,'A mathematical ceiling before leaving the customer any return; not a recommended price.');
label(e,57,'Provider zero-contribution monthly price','=D50',money);
label(e,58,'Price room before buyer/provider surplus','=D56-D57',money,'Negative means no price satisfies both sides under these assumptions.');
label(e,59,'Provider contribution per additional turn',"='Assumptions'!D18-D45",dec);
label(e,60,'Recurring cost less platform fee',"=SUM(D47,D49)-'Assumptions'!D17",money);
label(e,61,'Minimum serviced turns for provider break-even','=IF(D59>0,MAX(0,ROUNDUP(D60/D59,0)),IF(D59=0,IF(D60<=0,0,"n.a."),"n.a."))',num,'When per-turn contribution is negative, more volume worsens contribution.');
label(e,62,'Maximum turns if unit contribution is negative','=IF(D59<0,IF(D60<=0,ROUNDDOWN(-D60/-D59,0),"n.a."),"n.a.")',num,'Only relevant when platform fees cover fixed cost but each extra turn loses money.');
label(e,64,'Provider minimum turn price at current volume',"=IF(D16=0,\"n.a.\",MAX(0,(D50-'Assumptions'!D17)/D16))",dec);
label(e,65,'Buyer maximum turn price at current volume',"=IF(D16=0,\"n.a.\",(D34-'Assumptions'!D17)/D16)",dec);
label(e,66,'Turn price at provider contribution target',"=IF(OR(D16=0,'Assumptions'!D31>=1),\"n.a.\",MAX(0,(D50/(1-'Assumptions'!D31)-'Assumptions'!D17)/D16))",dec,'Uses the editable contribution target. This still excludes central overhead and customer acquisition.');
label(e,67,'Collected rent days needed for buyer break-even',"=IF(D16*'Assumptions'!D28*('Assumptions'!D15+(1-'Assumptions'!D15)*D30)=0,\"n.a.\",MAX(0,(D35-D19-D23*D30)/(D16*'Assumptions'!D28/'Assumptions'!D30*('Assumptions'!D15+(1-'Assumptions'!D15)*D30))))",'0.00','Includes realized labor and expense savings; depends on which party captures recovered rent.');
total(e,58);
section(e,68,'Reconciliation and scope');
label(e,69,'Value allocation difference','=SUM(D29,D31,D32)-SUM(D19,D25)','0.00','Should equal zero. Manager fees transfer owner value; they do not create extra value.');
val(e,'B71','Resident safety, service quality, retention and trust are not monetized here.');
val(e,'B72','Do not add reduced payroll and an avoided hire for the same saved hours.');
val(e,'B73','All eligible items are assumed served and billable. Test failures, refunds and exclusions during pilots.');
for(const r of [7,9,36,51,58])e.getRange(`D${r}`).conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FCE4E4',font:{color:'#9C2525'}}});
e.getRange('D69').conditionalFormats.add('cellIs',{operator:'notEqual',formula:0,format:{fill:'#FCE4E4',font:{color:'#9C2525'}}});
for(let r=14;r<=65;r++)if(e.getRange(`D${r}`).formulas[0]?.[0]?.includes('Assumptions'))e.getRange(`D${r}`).format.font.color=green;

// Standalone algebraic sensitivities, not a second scenario forecast or stored captures.
const se=sheets.Sensitivity;base(se,'H42');title(se,'What changes the economics');
se.getRange('B1:B42').format.columnWidth=27;se.getRange('C1:F42').format.columnWidth=20;se.getRange('G1:G42').format.columnWidth=3;
val(se,'B4','Each table varies one assumption and keeps the current work volume and other inputs fixed.');se.getRange('B4').format.font={italic:true,color:muted};
val(se,'B6','Provider exception rate');
se.getRange('B7:F7').values=[['Exception share','Human min/turn','Variable cost/turn','Monthly contribution','Contribution margin']];
const ex=[0,0.10,0.15,0.25,0.50];
for(let i=0;i<ex.length;i++){let r=8+i;val(se,`B${r}`,ex[i]);formula(se,`C${r}`,`='Assumptions'!$D$19+B${r}*'Assumptions'!$D$21`);formula(se,`D${r}`,`=C${r}/60*'Assumptions'!$D$22+'Assumptions'!$D$23`);formula(se,`E${r}`,`='Economics'!$D$35-'Economics'!$D$16*D${r}-SUM('Economics'!$D$47,'Economics'!$D$49)`);formula(se,`F${r}`,`=IF('Economics'!$D$35=0,"n.a.",E${r}/'Economics'!$D$35)`);}
val(se,'B15','Cash realization of manager time');
se.getRange('B16:E16').values=[['Time converted to cash','Manager labor value','Buyer net value','Buyer price ceiling']];
for(let i=0;i<3;i++){const r=17+i;val(se,`B${r}`,[0,.5,1][i]);formula(se,`C${r}`,`='Economics'!$D$18*B${r}`);formula(se,`D${r}`,`=C${r}+SUM('Economics'!$D$26,'Economics'!$D$31)-'Economics'!$D$35`);formula(se,`E${r}`,`=D${r}+'Economics'!$D$35`);}
val(se,'B22','Who captures owner economics');
se.getRange('B23:E23').values=[['Buyer share','Owner value to buyer','Buyer net value','Owner value outside buyer']];
for(let i=0;i<3;i++){const r=24+i;val(se,`B${r}`,[0,.5,1][i]);formula(se,`C${r}`,`='Economics'!$D$27*B${r}`);formula(se,`D${r}`,`='Economics'!$D$29+C${r}-'Economics'!$D$35`);formula(se,`E${r}`,`='Economics'!$D$27-C${r}`);}
for(const r of [7,16,23])se.getRange(`B${r}:${r===7?'F':'E'}${r}`).format={fill:navy,font:{color:'#FFFFFF',bold:true},wrapText:true,rowHeight:34};
for(const range of ['B8:B12','B17:B19','B24:B26','F8:F12'])se.getRange(range).setNumberFormat(pct);
se.getRange('C8:C12').setNumberFormat('0.0');se.getRange('D8:D12').setNumberFormat(dec);
for(const range of ['E8:E12','C17:E19','C24:E26'])se.getRange(range).setNumberFormat(money);
for(const range of ['B8:B12','B17:B19','B24:B26'])se.getRange(range).format.font.color=blue;
for(const range of ['E8:E12','D17:D19','D24:D26'])se.getRange(range).conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FCE4E4',font:{color:'#9C2525'}}});
val(se,'B29','Owner benefits remain assumptions. Set both owner benefit inputs to zero to test a labor-only case.');
val(se,'B30','Exception rates change human handling costs; they do not change customer benefits in this isolated test.');
val(se,'B32','Collected rent days recovered');
se.getRange('B33:F33').values=[['Collected days/turn','Owner added revenue','Manager added fees','Owner gain after fee','Buyer net value']];
se.getRange('B33:F33').format={fill:navy,font:{color:'#FFFFFF',bold:true},wrapText:true,rowHeight:34};
for(let i=0;i<4;i++){const r=34+i;val(se,`B${r}`,[0,1,2,3][i]);formula(se,`C${r}`,`='Economics'!$D$16*'Assumptions'!$D$28/'Assumptions'!$D$30*B${r}`);formula(se,`D${r}`,`=C${r}*'Assumptions'!$D$15`);formula(se,`E${r}`,`=C${r}+'Economics'!$D$23-D${r}`);formula(se,`F${r}`,`='Economics'!$D$19+D${r}+E${r}*'Assumptions'!$D$16-'Economics'!$D$35`);}
se.getRange('C34:F37').setNumberFormat(money);se.getRange('B34:B37').format.font.color=blue;
se.getRange('F34:F37').conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FCE4E4',font:{color:'#9C2525'}}});

async function readRecords(name){try{return JSON.parse(await fs.readFile(path.join(root,'research',name),'utf8'));}catch(err){if(err.code==='ENOENT')return [];throw err;}}
function col(n){let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}
function stringify(v){return v===null||v===undefined?'':v instanceof Date?v:Array.isArray(v)?v.map(stringify).join('; '):typeof v==='object'?JSON.stringify(v):v;}
function table(s,titleText,rows,columns,tableName){
 const nr=rows.length+6,nc=columns.length;base(s,`${col(nc)}${nr}`);title(s,titleText,col(nc-1));
 val(s,'B4',`${rows.length} records. Filter the headers and scroll right for full detail.`);
 const headers=columns.map(c=>c[1]);s.getRangeByIndexes(5,0,1,nc).values=[headers];
 if(rows.length)s.getRangeByIndexes(6,0,rows.length,nc).values=rows.map(row=>columns.map(c=>stringify(row[c[0]])));
 const range=s.getRangeByIndexes(5,0,rows.length+1,nc);range.format.wrapText=true;range.format.verticalAlignment='top';
 const t=s.tables.add(`A6:${col(nc-1)}${nr}`,true,tableName);t.style='TableStyleMedium2';t.showFilterButton=true;
 s.getRangeByIndexes(5,0,1,nc).format={fill:navy,font:{color:'#FFFFFF',bold:true},wrapText:true,rowHeight:32,verticalAlignment:'center'};
 for(let c=0;c<nc;c++)s.getRangeByIndexes(0,c,nr,1).format.columnWidth=columns[c][2]||36;
 for(let r=0;r<rows.length;r++){
  const maxLines=Math.max(...columns.map((c)=>{const value=rows[r][c[0]];const text=value instanceof Date?'2026-09-15':String(stringify(value));return Math.ceil(text.length/((c[2]||36)*0.9));}));
  s.getRangeByIndexes(6+r,0,1,nc).format.rowHeight=Math.min(260,Math.max(46,maxLines*13+8));
 }
 s.freezePanes.freezeRows(6);s.freezePanes.freezeColumns(2);
 return {rows:rows.length,cols:nc};
}
// Inventory paths may be adapted once source research has finished.
const decisions=await readRecords('decisions.json');
const competitors=(await readRecords('competitors.json')).map(row=>({...row,checked_date:/^\d{4}-\d{2}-\d{2}$/.test(row.checked_date)?new Date(`${row.checked_date}T00:00:00Z`):row.checked_date}));
const publicData=(await readRecords('public_data.json')).map(x=>({...x,value:x.value!==''&&Number.isFinite(Number(x.value))?Number(x.value):x.value}));
const dcols=decisions.length?Object.keys(decisions[0]).map(k=>[k,k.replaceAll('_',' '),k==='decision_id'?10:k==='family'?26:k==='scope'?28:k==='decision'?55:k==='source_urls'?75:42]):[['id','ID',10],['stage','Stage',25],['decision','Decision',60]];
const ccols=competitors.length?Object.keys(competitors[0]).map(k=>[k,k.replaceAll('_',' '),k==='provider'?24:k==='category'?25:k.includes('date')?15:k==='source_urls'?75:45]):[['provider','Provider',24],['category','Category',25],['capabilities_observed','Capabilities observed',60]];
const pcols=publicData.length?Object.keys(publicData[0]).map(k=>[k,k.replaceAll('_',' '),k==='value'?18:k==='metric'?52:k.includes('url')?65:40]):[['metric','Metric',50],['value','Value',18],['source','Source',65]];
const inventories={
 Decisions:table(sheets.Decisions,'Property-manager decision inventory',decisions,dcols,'DecisionInventory'),
 Competitors:table(sheets.Competitors,'Products and market evidence',competitors,ccols,'CompetitorInventory'),
 'Public data':table(sheets['Public data'],'Independent public-data analysis',publicData,pcols,'PublicDataInventory')
};
for(const n of ['Decisions','Competitors','Public data']){const s=sheets[n];s.getRange('A2').values=s.getRange('B2').values;s.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:navy};s.getRange('B2').clear({applyTo:'contents'});s.getRange('A4').values=s.getRange('B4').values;s.getRange('B4').clear({applyTo:'contents'});}
const checkedDateColumn=ccols.findIndex(c=>c[0]==='checked_date');if(checkedDateColumn>=0)sheets.Competitors.getRangeByIndexes(6,checkedDateColumn,competitors.length,1).setNumberFormat('mm/dd/yy');
for(let i=0;i<publicData.length;i++){
 const row=publicData[i],idx=pcols.findIndex(c=>c[0]==='value');
 if(typeof row.value==='number')sheets['Public data'].getRangeByIndexes(i+6,idx,1,1).setNumberFormat(row.measure?.startsWith('share')||row.measure?.includes('fraction')?'0.0%':row.measure?.startsWith('percent')?'0.0"%"':row.measure?.startsWith('USD')?money:Math.abs(row.value)>=100?'#,##0':'0.00');
}

wb.recalculate();
// Calculation checks use independent arithmetic rather than formula counts.
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:50},summary:'Formula error scan'});
await fs.writeFile(path.join(qa,'formula_error_scan.ndjson'),errors.ndjson);
const read=addr=>e.getRange(addr).values[0][0];
const close=(actual,expected,label)=>{if(typeof actual!=='number'||Math.abs(actual-expected)>1e-7)throw new Error(`${label}: ${actual} != ${expected}`);};
close(read('D16'),1000*.35/12,'Eligible volume');close(read('D7'),3572.916666666667,'Integrated buyer net value');close(read('D9'),1779.513888888889,'Provider contribution');close(read('D69'),0,'Allocation reconciliation');close(read('D66'),97.47023809523809,'Target contribution price');close(read('D67'),1.1625,'Required rent recovery');
// Prove owner capture, zero cash realization and the zero-volume boundary react.
a.getRange('D16').values=[[0]];wb.recalculate();close(read('D7'),-1793.75,'Standalone manager buyer value');close(read('D67'),14.53125,'Standalone PM required recovery');
a.getRange('D16').values=[[1]];a.getRange('D12').values=[[0]];wb.recalculate();close(read('D7'),2916.666666666667,'No cash realization buyer value');
a.getRange('D12').values=[[.5]];a.getRange('D29').values=[[0]];wb.recalculate();close(read('D7'),-2260.416666666667,'No collected rent recovery');
a.getRange('D29').values=[[null]];wb.recalculate();if(a.getRange('D14').values[0][0]!=='n.a.')throw new Error('Missing rent-days input was hidden');
a.getRange('D29').values=[[3]];a.getRange('D8').values=[[0]];wb.recalculate();close(read('D16'),0,'Zero volume');close(read('D9'),-483.3333333333333,'Zero volume contribution');
a.getRange('D8').values=[[.35]];wb.recalculate();close(read('D7'),3572.916666666667,'Restored base');
const inspection=await wb.inspect({kind:'table',range:'Economics!B6:D10',include:'values,formulas',tableMaxRows:8,tableMaxCols:4});
await fs.writeFile(path.join(qa,'headline_inspection.ndjson'),inspection.ndjson);
const checks={base:{eligibleTurns:read('D16'),buyerNet:read('D7'),providerContribution:read('D9'),ownerValueOutsideBuyer:read('D8'),providerCostFloorPerTurn:read('D64'),buyerCeilingPerTurn:read('D65')},checks:['Independent arithmetic','Owner share changed to 0%','Time cash realization changed to 0%','Collected rent recovery changed to zero','Work volume changed to zero','Original assumptions restored'],inventories,limitations:['Recalculation verified with artifact-tool; Excel desktop was not available for a native application check.','Illustrative commercial assumptions have not been validated by customer observations.']};
await fs.writeFile(path.join(qa,'validation.json'),JSON.stringify(checks,null,2));
for(const [name,range,suffix] of [['Economics','B2:F19',''],['Economics','B40:F67','_costs'],['Assumptions','B2:F15',''],['Assumptions','B16:F31','_remaining'],['Sensitivity','B2:F26',''],['Sensitivity','B29:F37','_rent'],['Decisions','A2:F11',''],['Decisions','M6:R9','_detail'],['Competitors','A2:F10',''],['Competitors','G6:M9','_detail'],['Competitors','A37:F44','_extension'],['Public data','A2:F11',''],['Public data','F6:H9','_sources']]){
 if(process.env.PM_RENDER_ONLY&&!process.env.PM_RENDER_ONLY.split(',').includes(name))continue;
 const png=await wb.render({sheetName:name,range,scale:1.3,format:'png'});
 await fs.writeFile(path.join(qa,`${name.replaceAll(' ','_')}${suffix}.png`),new Uint8Array(await png.arrayBuffer()));
}
const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(path.join(out,'Property_Management_Analysis.xlsx'));
try{await fs.rename(path.join(out,'Property_Management_Analysis.xlsx.inspect.ndjson'),path.join(qa,'export_inspection.ndjson'));}catch(error){if(error.code!=='ENOENT')throw error;}
console.log(JSON.stringify(checks,null,2));
