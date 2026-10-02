"""Record agent-resolved targets and open investigation after the bounded probe."""
import hashlib
import json
from pathlib import Path
from pipeline import core
P=Path(__file__).resolve().parent

def main():
    cases=json.loads((P/'statutory-fresh-corrected-frozen/cases.json').read_text())
    observed={r['case_id']:r for r in json.loads((P/'statutory-fresh-batched-run/evaluation.json').read_text())['rows']}
    utilities=[f'PUC:{s}' for s in ['777','777.1','10009','10009.1','12822','12822.1','16481','16481.1']]
    assigned={
      'fresh-1942.1-01':(['CIV:1941','CIV:1942'],'Read together with waiver restriction and tenant-contribution provisions.'),
      'fresh-1942.1-04':(['CIV:1941']+[f'CIV:1941.{i}' for i in range(1,10)]+['CIV:1942','CIV:1942.1'],'Range expanded against saved inventory; current official range enumeration and substantive review remain open.'),
      'fresh-1942.1-05':(['CCP:Title9','CCP:1280'],'Retrieved starting definitions, not the complete arbitration title. Enumerate title and investigate applicable arbitration requirements before use.'),
      'fresh-1942.2-01':(utilities,'Retrieved all eight statutory alternatives. Select applicable provider and metering branch from case facts.'),
      'fresh-1942.2-02':(['GOV:60371'],'Retrieved district utility rule; establish whether this district/provider branch applies.'),
      'fresh-1942.2-03':(utilities+['GOV:60371'],'Anaphoric reference depends on which antecedent payment route applies. Do not arbitrarily choose the nearest named section.'),
      'fresh-1942.6-03':(['CIV:1942.6'],'Self-reference; source already present.'),
      'fresh-1942.6-04':(['CIV:1942.6'],'Self-reference; source already present.'),
      'fresh-1942-01':(['CIV:1962(a)'],'Existing source defines relevant owner/agent disclosures. Inspect before serving or assessing notice.'),
      'fresh-1942-04':(['CIV:1942'],'Self-reference; source already present.'),
      'fresh-1942-05':(['CIV:1942(b)'],'Local timing presumption; source already present.'),
      'fresh-1942-07':(['CIV:1942(a)'],'Corrected occurrence in subdivision c points to local repair-and-deduct remedy.'),
      'fresh-1942-08':(['CIV:1929','CIV:1941.2'],'Retrieved ordinary-care provision; read tenant contribution restriction in existing source. Establish causation and responsibilities before account treatment.'),
      'fresh-1942-09':(['CIV:1942'],'Self-reference; source already present.'),
      'fresh-1942-10':(['CIV:Division3/Part4/Title5/Chapter2'],'Enclosing chapter; enumerate and investigate applicable additional remedies rather than treating the whole chapter as applied.')}
    rows=[]
    for c in cases:
        cid=c['case_id'];a,b=c['expression_span'];answer=observed[cid]
        targets,note=assigned.get(cid,([],answer['reason']))
        action='target_identified_for_agent_followup' if targets else 'not_statutory_reference'
        if cid=='fresh-1942.1-02':note='False-positive lead: private waiver agreement, not a statutory target. Preserve agreement as relevant case evidence.'
        if cid=='fresh-1942-06':note='False-positive lead: timing condition. Agent establishes notice event; code handles date arithmetic.'
        rows.append({'case_id':cid,'expression':c['text'][a:b],'source':c['source'],
                     'expression_span':[a,b],'jev_noul':answer['noul'],'diagnostic_majority':answer['actual'],
                     'agent_action':action,'targets':targets,'followup':note})
    sources=json.loads((P/'dependency-sources/manifest.json').read_text())
    report={'scope':'First-hop follow-up for four bounded statutory bodies, not California mapping completion.',
      'preparation_correction':'fresh-preparation-correction.json','rows':rows,'retrieved_sources':sources,
      'next_dependencies':[
       {'targets':['CIV:1632','HSC:17008','BPC:6213','CCP:697.310'],'cause':'Named in retrieved utility statutes; language, housing type, legal-services and judgment-recording dependencies. Not retrieved in this bounded first-hop run.'},
       {'targets':['utility rules and tariffs','implementing rules/orders','local utility protections'],'cause':'Retrieved statutes expressly require these or preserve local authority. Need case provider and jurisdiction.'},
       {'targets':['CCP:Title9','CIV:1941 through 1942.1','CIV:Title5/Chapter2'],'cause':'Unit/range pointers require broader enumeration and interpretation, not just first-section retrieval.'},
       {'targets':['existing law in CIV1942.6','other applicable statutory or common law in CIV1942(d)'],'cause':'Three broad lead occurrences were retained outside the particular-statutory-reference probe; agent research remains open.'}],
      'findings':[
       'CIV1942.2 requires following the referenced utility payment route; the short section alone does not establish any claimed rent deduction.',
       'The retrieved payment routes require case facts about provider type, metering, customer status, bundled rental charges and payments. A rent ledger alone is insufficient.',
       'CIV1942 and its tenant-contribution dependencies affect repair responsibility and claimed rent credits; detecting references does not decide causation or entitlement.'],
      'limits':['No independent recall review in this run.','Preparation/retrieval wall time and full agent cost were not instrumented; no end-to-end speed claim.','No runtime legal rule or production routing changed.']}
    (P/'fresh.followup.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
