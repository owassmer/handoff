"""Civil Code TOC decisions, made by the researcher and materialized without a relevance classifier."""
import re
from urllib.parse import urlencode
from build_register import HERE

# Only plainly separate transactions are excluded. Mixed units stay in.
PART_OUT={
 ('1','2.57'):'Retail department merchandising; not residential work, tenancy or account resolution.',
 ('1','2.7'):'Medical claims data correction; no residential operating decision.',
 ('1','2.9'):'Motor vehicle dealership relations; no residential operating decision.',
 ('4','5.3'):'Commercial/industrial common-interest developments; residential developments are in Part 5.',
 ('4','5.5'):'Retail automatic checkout systems; not residential payments.'}
TRANSACTION_OUT={
 '1':'Consignment of fine art', '1A':'Wholesale sales representatives',
 '1.1':'Political merchandise', '1.1A':'Autographed memorabilia', '1.2':'Fine prints',
 '1.2A':'Video game sales', '1.4':'Retail layaway', '1.4B':'Supermarket loyalty cards',
 '1.5A':'Vehicle history reports', '1.5B':'Automobile retail transactions',
 '1.6C.10':'Student lending', '1.6C.15':'Private student loans',
 '1.81.15':'Book reading service records', '1.81.27':'Sale of booking photographs',
 '1.81.45':'Child access to harmful online products', '1.81.46':'Online violence platforms',
 '1.81.47':'Child-facing digital products', '1.81.9':'Age assurance for operating systems',
 '2.4':'Dance instruction contracts', '2.6':'Discount buying services',
 '2.7':'Seller-assisted marketing businesses', '10':'Recording artist contracts',
 '11':'Pharmaceutical services', '15':'Internet service provider neutrality',
 '15.2':'Training general-purpose AI models', '17':'Year-2000 disclosure immunity',
 '20':'Firearm industry', '21':'Firearm manufacturing',
 '22':'Social-media child sexual abuse content', '25':'Social-media platform design'}
CHAPTER_OUT={
 ('3','2','5','2.1'):'Dating service contracts.',
 ('3','2','5','2.2'):'Weight-loss service contracts.',
 ('3','4','3','4'):'Commercial bulk grain storage.',
 ('3','4','4','1.5'):'Museum loans.',
 ('3','4','5','2.6'):'Commercial rent control; residential controls retained separately.',
 ('3','4','5','5.5'):'Abandoned property from commercial tenancy; residential property duties retained separately.'}

def refine(i):
    lines={}
    for f in (HERE/'sources').glob('civ-expanded-*.txt'):
        for n,t in re.findall(r'L(\d+): (.*)',f.read_text()): lines[int(n)]=t
    nodes=[]; stack={}; ranks={'DIVISION':0,'PART':1,'TITLE':2,'CHAPTER':3,'ARTICLE':4}
    fields=['division','part','title','chapter','article']
    for n,t in sorted(lines.items()):
        for h in re.findall(r'†([^]+)',t):
            m=re.match(r'(DIVISION|PART|TITLE|CHAPTER|ARTICLE) ([0-9A-Za-z.]+)\. (.+)',h)
            if not m:continue
            rank=ranks[m[1]]; num=m[2].rstrip('.')
            for k in list(stack):
                if k>=rank:del stack[k]
            stack[rank]=num
            path=tuple(stack.get(k,'') for k in range(5))
            if nodes and path==nodes[-1]['path'] and h==nodes[-1]['heading']:continue
            nodes.append({'heading':h,'path':path,'rank':rank,'line':n})
    ins=[];outs=[]
    for pos,n in enumerate(nodes):
        # Parents are represented by their descendants, so there is no duplicate acquisition.
        if pos+1<len(nodes) and nodes[pos+1]['rank']>n['rank']:continue
        d,p,t,c,a=n['path']; reason=PART_OUT.get((d,p))
        if (d,p)==('3','4') and t in TRANSACTION_OUT:
            reason=TRANSACTION_OUT[t]+': separate transaction outside residential operating flows.'
        reason=reason or CHAPTER_OUT.get((d,p,t,c))
        u={'unit':' / '.join(f'{fields[k]} {v}' for k,v in enumerate(n['path']) if v),
           'heading':n['heading'], 'toc_url':'https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?'+urlencode({'lawCode':'CIV',**{fields[k]:v+'.' for k,v in enumerate(n['path']) if v}}),
           'source_capture':'j1/sources/civ-expanded-{0,500,1000}.txt',
           'reason':reason or 'Property, tenancy, work, agreements, responsibility, information, payment or remedies; mixed units retained for complete section review.'}
        (outs if reason else ins).append(u)
    i['units_in_scope']=i['units_in_scope'][:1]+ins
    i['units_out']=outs
    i['scope_granularity']='Complete official expanded TOC, leaf articles/chapters/titles; explicit separate-industry exclusions.'
