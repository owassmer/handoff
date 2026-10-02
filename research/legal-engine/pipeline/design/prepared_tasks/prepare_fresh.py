"""Agent's explicit selections from four complete statutory bodies."""
import hashlib
import json
from pathlib import Path
from pipeline import core
from pipeline.design.prepared_tasks.statutory import freeze
HERE = Path(__file__).resolve().parent
# Enumerated by reading each complete section before model execution.
SELECTIONS = {
 '1942.1': [
  ('Section 1941 or 1942', 'YES', 'Two Civil Code repair provisions.'),
  ('Any agreement', 'NO', 'Private agreement whose waiver is regulated.'),
  ('the premises', 'NO', 'Physical dwelling.'),
  ('Sections 1941 to 1942.1, inclusive', 'YES', 'Civil Code range.'),
  ('Title 9 (commencing with Section 1280), Part 3 of the Code of Civil Procedure', 'YES', 'Statutory arbitration title with starting section and parent part.'),
  ('an agreement', 'NO', 'Written private agreement.'),
  ('the arbitrator', 'NO', 'Person allocating costs.')],
 '1942.2': [
  ('Section 777, 777.1, 10009, 10009.1, 12822, 12822.1, 16481, or 16481.1 of the Public Utilities Code', 'YES', 'Eight Public Utilities Code alternatives.'),
  ('Section 60371 of the Government Code', 'YES', 'Government Code dependency.'),
  ('that section', 'YES', 'Anaphoric reference to the applicable payment statute.'),
  ('the payment', 'NO', 'Money paid to the utility.'),
  ('the rent', 'NO', 'Rent amount rather than statutory text.')],
 '1942.6': [
  ('an occupant', 'NO', 'Person inviting entry.'),
  ('tenants’ rights', 'NO', 'Rights as a subject of information, no statutory text identified.'),
  ('this section', 'YES', 'Enclosing statutory section; first occurrence.'),
  ('this section', 'YES', 'Enclosing statutory section; second occurrence.')],
 '1942': [
  ('subdivision (a) of Section 1962', 'YES', 'Agent/owner identification dependency.'),
  ('one month’s rent', 'NO', 'Amount limit computed from rent.'),
  ('12-month period', 'NO', 'Time interval.'),
  ('this section', 'YES', 'Enclosing statutory section in subdivision b.'),
  ('this subdivision', 'YES', 'Enclosing subdivision b.'),
  ('the 30th day following notice', 'NO', 'Temporal event rather than statutory unit.'),
  ('subdivision (a)', 'YES', 'Repair remedy in same section.'),
  ('Section 1929 or 1941.2', 'YES', 'Tenant-caused condition dependencies.'),
  ('this section', 'YES', 'Enclosing section in subdivision d.'),
  ('this chapter', 'YES', 'Enclosing Civil Code chapter.'),
  ('the rental\nagreement', 'NO', 'Private agreement is a separate source of remedies.')]
}

def prepare():
    cases=[]; labels=[]; coverage=[]
    for section, selections in SELECTIONS.items():
        path=core.ROOT/f'jurisdictions/CA/texts/CA_CIV/{section}.txt'
        raw=path.read_bytes(); text=raw.decode()
        body_start=text.index(section+'.\n\n')+len(section+'.\n\n')
        body_end=text.rfind('\n('); body=text[body_start:body_end]
        seen={}; expressions=[]
        for expression, expected, reason in selections:
            search_start=seen.get(expression,0)
            if section=='1942' and expression=='subdivision (a)':
                search_start=body.index('The tenant’s remedy under')
            start=body.index(expression, search_start);end=start+len(expression)
            seen[expression]=end
            cid=f'fresh-{section}-{len(expressions)+1:02d}'
            cases.append({'case_id':cid,'text':body,'source_kind':'statute',
                'expression_span':[start,end], 'strata':['fresh_section',section],
                'source':{'path':str(path.relative_to(core.ROOT)),'sha256':hashlib.sha256(raw).hexdigest(),
                          'start':body_start,'end':body_end}})
            labels.append({'case_id':cid,'expected':expected,'reason':reason})
            expressions.append({'case_id':cid,'text':expression,'body_span':[start,end]})
        broad=[]
        if section=='1942.6':
            broad=[{'text':'existing law','occurrences':2,'action':'Agent investigates background law; no particular statute identified.'}]
        if section=='1942':
            broad=[{'text':'other applicable statutory or common law','occurrences':1,'action':'Agent investigates additional remedies; no determinate target identified.'}]
        coverage.append({'section':section,'body_start':body_start,'body_end':body_end,
            'body_sha256':hashlib.sha256(body.encode()).hexdigest(),'expressions':expressions,
            'broader_research_leads':broad,
            'excluded_metadata':'SOURCE/RETRIEVED headers, section locator and amendment history.',
            'coverage_review':'Preparing agent enumerated references across this complete body. No independent recall measurement.'})
    (HERE/'fresh.coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
    freeze(cases,json.loads((HERE/'statutory.question.json').read_text()),labels,HERE/'statutory-fresh-corrected-frozen')
if __name__=='__main__': prepare()
