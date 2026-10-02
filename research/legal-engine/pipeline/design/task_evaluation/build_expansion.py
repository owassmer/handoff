"""Historical v1 author generator. Current source-only repairs are applied by
correct_expansion_preparation.py after generation; do not treat generated labels as
reviewed expectations for the corrected cases. No inference."""
from pathlib import Path
import json,hashlib,collections
ROOT=Path(__file__).resolve().parents[3]; BASE=Path(__file__).parent; SRC=BASE/'expansion_sources'
T={p.stem:p.read_text() for p in SRC.glob('*.txt')}
P={}; cases=[];labels=[]
def excerpt(key,source,start,end=None):
 t=T[source];a=t.index(start);b=t.index(end,a) if end else t.index('\n',a) if '\n'in t[a:] else len(t)
 P[key]=(source,t[a:b].strip());return key
def exact(key,source,text):
 assert text in T[source],(key,text[:80]);P[key]=(source,text);return key
def add(task,fields,expected,reason,edge,cluster=None,criteria=None):
 state={};sources={};families=set()
 for field,value in fields.items():
  if isinstance(value,tuple):state[field]=value[0];continue
  source,text=P[value];state[field]=text;path=SRC/(source+'.txt');a=T[source].index(text);sources[field]={'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'start':a,'end':a+len(text)}
  families.add('administrative' if source.startswith(('EEOC','CFPB')) else 'judicial' if source in ['ARTIS','BOECHLER','FORT_BEND'] else 'statutory')
 row={'id':f'exp{len(cases)+1:03}','task':task,'family':next(iter(families)) if len(families)==1 else 'cross_family','source_cluster':cluster or '|'.join(sorted({P[v][0]+':'+v for v in fields.values() if isinstance(v,str)})),'state':state,'sources':sources}
 if criteria:row['criteria']=criteria
 cases.append(row);labels.append({'id':row['id'],'expected':expected,'reason':reason,'edge_case':edge,'downstream_failure':{'definition_present':'Incorrect extraction or missed assigned meaning.','candidate_term_use':'False meaning link or missed same-sense use.','candidate_meaning':'Wrong meaning selected for downstream interpretation.','exception_to_requirement':'Unlawfully retain or excuse a duty.','changes_deadline':'Apply the wrong deadline or miss a necessary modifier.','supports_claim':'Adopt an unwarranted proposition or reject supported evidence.'}[task]})
 save()
def save():
 (BASE/'expansion.cases.json').write_text(json.dumps({'cases':cases},indent=2,ensure_ascii=False)+'\n')
 (BASE/'expansion.author_labels.json').write_text(json.dumps({'cases':labels},indent=2,ensure_ascii=False)+'\n')
# Actual agency interpretations, not merely regulations on the same webpage.
excerpt('hardship','EEOC_ACCOMMODATION','"Undue hardship" means significant difficulty or expense')
excerpt('effective','EEOC_ACCOMMODATION','In the context of job performance, this means')
excerpt('choice','EEOC_ACCOMMODATION','The employer may choose among reasonable accommodations')
excerpt('essential','EEOC_ACCOMMODATION','An employer does not have to eliminate an essential function','An employer does not have to provide as reasonable accommodations')
excerpt('personal','EEOC_ACCOMMODATION','An employer does not have to provide as reasonable accommodations')
excerpt('accommodation_duty','EEOC_ACCOMMODATION','Reasonable accommodations must be provided to qualified employees')
excerpt('hardship_exception','EEOC_ACCOMMODATION','The only statutory limitation on an employer\'s obligation')
excerpt('documentation','EEOC_ACCOMMODATION','Yes. An employer cannot ask for documentation when:')
excerpt('prompt','EEOC_ACCOMMODATION','An employer should respond expeditiously')
excerpt('records','EEOC_ACCOMMODATION','Although individuals with disabilities are not required to keep records')
excerpt('charge','EEOC_CHARGE','The anti-discrimination laws give you','Note\n')
excerpt('charge180','EEOC_CHARGE','In general, you need to file a charge within','The 180 calendar day')
excerpt('charge300','EEOC_CHARGE','The 180 calendar day filing deadline','The rules are slightly')
excerpt('grievance','EEOC_CHARGE','Time limits for filing a charge with EEOC generally')
excerpt('holiday','EEOC_CHARGE','Holidays and weekends are included')
excerpt('harassment','EEOC_CHARGE','In harassment cases, you must file')
excerpt('events','EEOC_CHARGE','Also, if more than one discriminatory event took place')
excerpt('epa','EEOC_CHARGE','If you plan to file a charge alleging a violation')
excerpt('titlevii','EEOC_CHARGE','Keep in mind, Title VII also makes it illegal')
excerpt('receipt','CFPB_1026_10','The “date of receipt” is the date','For example:')
excerpt('check','CFPB_1026_10','i. Payment by check is received')
excerpt('webpay','CFPB_1026_10','iv. Payment made via the creditor\'s Web site')
excerpt('creditdate','CFPB_1026_10','Section 1026.10(a) does not require','2.\nDate of receipt.')
excerpt('fee','CFPB_1026_10','For purposes of §\u00a01026.10(e), the term “separate fee” means')
excerpt('expedited','CFPB_1026_10','For purposes of §\u00a01026.10(e), the term “expedited” means')
excerpt('representative','CFPB_1026_10','Service by a customer service representative of a creditor means')
excerpt('creditor','CFPB_1026_10','For purposes of §\u00a01026.10(e), the term “creditor” includes','For example:')
excerpt('provider_yes','CFPB_1026_10','i. Assume that a creditor uses a service provider')
excerpt('provider_no','CFPB_1026_10','ii. Assume that a consumer pays a fee')
excerpt('business','CFPB_1026_2','A more precise rule for what is a business day')
excerpt('functions','CFPB_1026_2','Activities that indicate that the creditor is open')
excerpt('cycle','CFPB_1026_2','Although cycles must be equal','4.\nPayment reminder.')
excerpt('reminder','CFPB_1026_2','The sending of a regular payment reminder')
# Court text retains PDF extraction and majority context.
excerpt('boechler_intro','BOECHLER','   Boechler, P.C., the petitioner','\f2')
excerpt('boechler_req','BOECHLER','Under §6330(d)(1), Boechler had 30 days','But Boechler')
excerpt('boechler_hold','BOECHLER','   None of this is to say','                                              It is so ordered.')
excerpt('boechler_def','BOECHLER','Jurisdictional requirements mark','Yet not all')
excerpt('fort_def','FORT_BEND','the word “juris-','   Congress may')
excerpt('fort_mandatory','FORT_BEND','A claim-\nprocessing rule may be','  The Court has characterized')
excerpt('artis_law','ARTIS','   Section 1367(d), addressing that issue','The question presented:')
excerpt('artis_proposal','ARTIS','The question presented:','   In the case before us')
excerpt('artis_def','ARTIS','We hold that § 1367(d)\'s instruction','Because the D. C.')
# State statutory source excerpts, never relabeled interpretations.
excerpt('wa_dwelling','WASHINGTON_59_18','(10) "Dwelling unit" is')
excerpt('wa_landlord','WASHINGTON_59_18','(16) "Landlord" means')
excerpt('wa_person','WASHINGTON_59_18','(21) "Person" means')
excerpt('wa_incorporation','WASHINGTON_59_18','(7) "Distressed home" has','(8)')
excerpt('wa_condemned','WASHINGTON_59_18','(1) If a governmental agency responsible for the enforcement of a building')
excerpt('wa_relocation','WASHINGTON_59_18','(3)(a) If a governmental agency responsible for the enforcement')
excerpt('wa_disaster','WASHINGTON_59_18','(ii) A landlord shall not be required to pay relocation assistance')
excerpt('wa_illegal','WASHINGTON_59_18','(i) A landlord shall not be required to pay relocation assistance')
excerpt('wa_damages','WASHINGTON_59_18','(2) If a landlord knowingly violates subsection (1) of this section')
excerpt('wa_payment','WASHINGTON_59_18','(c) The landlord shall pay relocation assistance and any prepaid deposit')
excerpt('or_dwelling','OREGON_90','(14) “Dwelling','(15)')
excerpt('or_landlord','OREGON_90','(25) “Landlord”','(26)')
excerpt('or_mail','OREGON_90','(2) If a notice\nis served by mail','(3) A landlord')
excerpt('or_alternative','OREGON_90','(3) A landlord or\ntenant may utilize alternative','(4)')
excerpt('or_entry','OREGON_90','(f) In all other\ncases, unless','(2) A landlord\nmay not abuse')
excerpt('or_emergency','OREGON_90','(b) In case of an\nemergency','(c) If the tenant')
# 16 definition judgments: affirmative assignment vs mere operation/reporting.
for key,answer,why in [
 ('hardship','YES','Agency expressly assigns significant difficulty or expense meaning.'),('receipt','YES','Interpretation expressly assigns receipt event.'),('expedited','YES','Interpretation defines expedited crediting.'),('representative','YES','Interpretation assigns scope including live agents and excluding automation.'),
 ('choice','NO','Alternative accommodation rule uses the term without assigning a meaning.'),('prompt','NO','Timing guidance is not a definition.'),('personal','NO','Personal-item duty limitations do not assign a term meaning.'),('grievance','NO','No-extension guidance does not assign meaning.'),
 ('boechler_def','YES','Court assigns jurisdictional requirements adjudicatory-boundary meaning.'),('artis_def','YES','Majority expressly assigns stop-clock meaning.'),('artis_proposal','NO','Question and competing proposed readings do not adopt either definition.'),('boechler_hold','NO','Holding concerns tollability and entitlement, not assignment of a term meaning.'),
 ('wa_incorporation','YES','Operative incorporation assigns a meaning despite absent incorporated content.'),('or_dwelling','YES','Statute supplies ordinary and space-only meanings.'),('wa_condemned','NO','Prohibition uses dwelling terminology without defining it.'),('or_alternative','NO','Additional service method rule assigns no term meaning.')]:
 add('definition_present',{'passage':key},answer,why,'assignment_vs_use_or_report',cluster=P[key][0]+':'+key)
print('definition increment',len(cases))
# Complete candidate definitions and selected occurrence expressions.
excerpt('general_business','CFPB_1026_2','(6) Business day','Official interpretation of 2(a)(6)')
exact('precise_business','CFPB_1026_2','all calendar days except Sundays and the Federal legal holidays specified in 5 U.S.C. 6103(a)')
exact('general_business_meaning','CFPB_1026_2',"a day on which the creditor's offices are open to the public for carrying on substantially all of its business functions")
excerpt('artis_grace','ARTIS','does “tolled” mean','Petitioner\nurges')
excerpt('or_space_meaning','OREGON_90','“Dwelling unit” regarding a','(15)')
# Term selection is semantic, not an applicability verdict; paired candidates retain clusters.
term_specs=[
 ('business day','precise_business','business','what is a business day','YES','calendar-day definition is the precise rule being explained','business-precise'),
 ('business day','general_business_meaning','business','what is a business day','NO','office-opening rule differs from the precise calendar-day meaning','business-precise'),
 ('creditor','creditor','provider_yes','considered a creditor','YES','Covered service provider is used in the included-agent sense','creditor-scope'),
 ('creditor','creditor','provider_no','considered a creditor','YES','Denial of category membership still invokes the supplied regulatory sense','creditor-scope'),
 ('separate fee','fee','fee','is not a separate fee','YES','The exclusion uses the same defined category under negation','fee-scope'),
 ('customer service representative','representative','representative','A customer service representative does not include automated means','YES','Negative category statement retains the live-representative sense','representative-scope'),
 ('Undue hardship','hardship','hardship','Undue hardship refers not only to financial difficulty','YES','The same agency hardship meaning includes nonfinancial burdens','hardship'),
 ('reasonable accommodation','effective','choice','among reasonable accommodations','YES','Choice among accommodations retains effective barrier-removal sense','accommodation'),
 ('toll','artis_def','artis_def','instruction to “toll”','YES','Majority adopts suspension meaning','artis-meaning'),
 ('tolled','artis_def','artis_grace','does “tolled” mean','NO','Selected proposed meaning lets clock run and adds grace period','artis-meaning'),
 ('tolled','artis_grace','artis_grace','does “tolled” mean','YES','Proposed grace meaning matches candidate regardless of ultimate rejection','artis-meaning'),
 ('jurisdictional','boechler_def','boechler_intro','the deadline is jurisdictional','YES','Rejected Commissioner characterization still uses adjudicatory-authority sense','boechler-jurisdiction'),
 ('dwelling unit','wa_dwelling','wa_condemned','for the dwelling unit','YES','Prohibited rental concerns residential structure','wa-dwelling'),
 ('landlord','or_landlord','or_entry','the landlord shall give the tenant','YES','Notice actor is owner/lessor or authorized manager','or-entry'),
 ('date of receipt','receipt','creditdate','the date of receipt','YES','Crediting-as-of invokes date payment reaches creditor','receipt-date'),
 ('dwelling unit','or_space_meaning','wa_condemned','for the dwelling unit','NO','Site-only meaning for separately owned manufactured home differs from residential structure being condemned','wa-dwelling')]
# The first accommodation expression uses plural text while term is singular substring; exact once is intentional.
for term,definition,use,expression,answer,why,cluster in term_specs:
 assert P[use][1].count(expression)==1,(use,expression)
 assert expression.count(term)==1,(term,expression)
 add('candidate_term_use',{'term':(term,),'definition_passage':definition,'use_passage':use,'use_expression':(expression,)},answer,why,'sense_not_legal_applicability',cluster=cluster)
# Choice candidates are agent-authored meanings, separate from quoted source fields.
# Each selected expression is new to Choice; source reuse across capabilities is disclosed.
meanings={
'business-precise':('Calendar days except Sundays and specified federal legal holidays.','Days the creditor opens for substantially all business functions.'),
'creditor-scope':('The creditor category including a third party acting on its behalf in receiving or processing payments.','A person owing money on a consumer account.'),
'fee-scope':('A charge for making a payment, distinguished from a charge for lateness.','An amount charged because payment is late.'),
'representative-scope':('A live representative or agent assisting a payment.','An automated payment system without a live representative.'),
'hardship':('Significant difficulty or expense for the particular employer.','Any preference for a cheaper accommodation.'),
'accommodation':('An effective workplace adjustment removing disability-related barriers.','A hotel room supplied to a traveler.'),
'artis-meaning':('Suspension of a limitations clock.','A grace period while the original limitations clock continues to run.'),
'boechler-jurisdiction':('A limitation on the court’s authority to adjudicate.','A requirement governing litigation procedure without conditioning adjudicatory authority.'),
'wa-dwelling':('A residential structure or part of one used as a home or sleeping place.','Only the rented site beneath a separately owned manufactured home.'),
'or-entry':('An owner, lessor, sublessor or authorized premises manager.','The resident renting the home from its owner.'),
'receipt-date':('The date the payment instrument or means reaches the creditor.','The date a deposited check finally clears.'),
'business-payment':('A payment-processing business day under the crediting context.','The special rescission calendar counting every day except Sundays and federal legal holidays.')}
for n,(term,definition,use,expression,answer,why,cluster) in enumerate(term_specs):
 good,bad=meanings[cluster]
 if cluster=='artis-meaning' and use=='artis_grace':good,bad=bad,good
 # Two actual NONE cases: supplied context is complete but neither offered meaning fits.
 if n in (4,12):
  options={'A':'A judicial grant of adjudicatory authority.','B':'The expiration date of a limitation period.','NONE':'Neither offered meaning fits.'};expected='NONE'
 else:
  expected='A' if n%2==0 else 'B';options={'A':good if expected=='A'else bad,'B':good if expected=='B'else bad,'NONE':'Neither offered meaning fits.'}
 add('candidate_meaning',{'term':(term,),'use_passage':use,'use_expression':(expression,)},expected,'Complete occurrence context selects '+('neither offered meaning.' if expected=='NONE'else good),'negation_or_contrary_proposal_or_no_fit',cluster=cluster,criteria=options)
print('term/choice increment',len(cases))
# Requirement relations. Select complete conditions rather than dropping qualifiers.
excerpt('records_base','EEOC_ACCOMMODATION','Employers, however, must keep all employment records','If a charge is filed, records')
excerpt('records_extension','EEOC_ACCOMMODATION','If a charge is filed, records must be preserved','29 C.F.R.')
excerpt('fort_objection','FORT_BEND','But an objection based on a mandatory claim-','  The Court has characterized')
# State actual notice duty (not an invented universal entry duty).
# Court strict filing requirement is paired with holding allowing equitable relief.
relations=[
 ('accommodation_duty','hardship_exception','YES','Hardship expressly excuses providing the accommodation.'),
 ('accommodation_duty','personal','YES','Personal-use-only items narrow what the accommodation duty requires.'),
 ('accommodation_duty','choice','NO','Choosing an effective alternative satisfies the unchanged accommodation duty.'),
 ('accommodation_duty','prompt','NO','Prompt response adds timing guidance, not an excuse.'),
 ('creditdate','webpay','NO','Receipt-trigger explanation preserves crediting as of receipt.'),
 ('records_base','records_extension','NO','Longer preservation adds protection rather than narrowing the duty.'),
 ('titlevii','epa','NO','Different statutory route does not excuse the specified TitleVII charge requirement.'),
 ('charge180','charge300','YES','Conditional300-day rule excuses compliance with ordinary180-day filing duration.'),
 ('boechler_req','boechler_hold','YES','Equitable tolling allows otherwise late petition in appropriate circumstances.'),
 ('boechler_req','boechler_def','NO','Definition alone does not excuse filing compliance.'),
 ('boechler_req','boechler_intro','YES','Court rejects lack of power to accept tardy filing through tolling.'),
 ('artis_law','artis_proposal','NO','Reported competing readings create no adopted exception.'),
 ('wa_relocation','wa_disaster','YES','Natural-disaster condition expressly excuses relocation assistance.'),
 ('wa_relocation','wa_illegal','YES','Specified illegal-conduct condition excuses relocation assistance.'),
 ('wa_condemned','wa_damages','NO','Damages for violation do not excuse the prohibition.'),
 ('or_entry','or_emergency','YES','Emergency entry dispenses with prior notice and consent under the chapter entry framework.')]
for req,cand,answer,why in relations:add('exception_to_requirement',{'requirement':req,'candidate':cand},answer,why,'exception_vs_alternative_or_remedy')
# Source text requirements and distinct modifiers, not calculations.
excerpt('epa_base','EEOC_CHARGE','The deadline for filing a charge or lawsuit under the EPA is two years','(this is extended')
exact('epa_extension','EEOC_CHARGE','this is extended to three years in the case of willful discrimination')
excerpt('artis_three_year','ARTIS','The D. C. False Claims Act and the tort of wrongful termination each',"Artis'\nwhistleblower")
# Notice by mail extension is tested against a written notice rule, not actual-notice entry.
excerpt('or_email_cancel','OREGON_90','(D) Allows the\nlandlord or tenant to terminate','(E) Includes')
# Washington post-deadline public advance does not extend landlord's seven days.
excerpt('wa_seven','WASHINGTON_59_18','(c) The landlord shall pay relocation assistance','The landlord shall pay relocation assistance and any prepaid deposit and prepaid rent either')
excerpt('wa_advance','WASHINGTON_59_18','If the landlord fails to complete payment of relocation assistance')
deadlines=[
 ('charge180','charge300','YES','Conditional duration extension changes selected filing period.'),
 ('charge180','holiday','YES','Terminal weekend/holiday adjustment modifies filing deadline.'),
 ('charge180','grievance','NO','Guidance expressly denies ordinary grievance tolling.'),
 ('events','harassment','YES','Ongoing harassment uses last incident trigger rather than independent event expiry.'),
 ('epa_base','epa_extension','YES','Willfulness changes two-year period to three.'),
 ('epa_base','titlevii','NO','Separate TitleVII filing expressly does not extend EPA suit deadline.'),
 ('records_base','records_extension','YES','Charge filing extends record preservation through resolution.'),
 ('creditdate','webpay','YES','After-cutoff web authorization changes deemed receipt day used for crediting.'),
 ('boechler_req','boechler_hold','YES','Tolling changes strict30-day temporal operation in appropriate cases.'),
 ('boechler_req','boechler_def','NO','Adjudicatory authority definition supplies no temporal modification.'),
 ('boechler_req','fort_objection','NO','Forfeiture of different claim-processing objection does not alter tax petition period.'),
 ('artis_three_year','artis_law','YES','Supplemental-claim tolling suspends the otherwise applicable state limitations period.'),
 ('or_email_cancel','or_mail','YES','First-class-mail service adds three days to written compliance period when this service route is used.'),
 ('or_entry','or_emergency','YES','Emergency entry replaces prior notice with specified post-entry notice when tenant absent.'),
 ('wa_seven','wa_advance','NO','Government may advance unpaid money after default; landlord deadline stays seven days.'),
 ('wa_seven','wa_damages','NO','Separate violation remedy does not modify seven-day payment deadline.')]
for req,cand,answer,why in deadlines:add('changes_deadline',{'requirement':req,'candidate':cand},answer,why,'trigger_extension_vs_independent_remedy')
claims=[
 ('hardship','Undue hardship is limited to financial difficulty.','NO','Text expressly includes nonfinancial difficulty.'),
 ('choice','An employer may choose among reasonable accommodations if the chosen accommodation is effective.','YES','Conditional discretion is expressly stated.'),
 ('personal','An employer is never required to provide an item that might otherwise be considered personal.','NO','Job-specific need qualification defeats never.'),
 ('documentation','An employer cannot ask for documentation when both the disability and need for accommodation are obvious.','YES','Enumerated condition expressly supports prohibition.'),
 ('provider_no','The consumer-side money transfer service in this example is a creditor for purposes of paragraph(e).','NO','Interpretation expressly denies category membership.'),
 ('business','Under the precise rule described, July3 is a business day when July4 falls on Saturday.','YES','Example expressly preserves precedingFriday as business day.'),
 ('charge','A local age-discrimination law alone extends the age charge deadline to300days.','NO','Age exception expressly requires state law and agency.'),
 ('epa','An Equal Pay Act claimant is allowed to go directly to court without filing an EEOC charge.','YES','Expressly stated statutory-route distinction.'),
 ('boechler_hold','The Court held that Boechler itself was entitled to equitable tolling on these facts.','NO','Actual entitlement reserved for remand.'),
 ('boechler_intro','The Commissioner argued that the Tax Court lacked power to accept a tardy filing through equitable tolling.','YES','Claim is explicitly about reported argument, not adopted rule.'),
 ('artis_proposal','The Supreme Court adopted the grace-period interpretation in this passage.','NO','Passage describes question and lowercourt adoption, not SupremeCourt holding.'),
 ('artis_def','The Court holds that the statutory instruction to toll means stopping the limitations clock.','YES','Express majority holding.'),
 ('wa_relocation','Every landlord must pay relocation assistance whenever a unit is condemned.','NO','Knowledge, code-condition and express exceptions qualify duty.'),
 ('wa_disaster','The specified natural-disaster condemnation condition excuses relocation assistance.','YES','Express conditional exception.'),
 ('or_emergency','Emergency entry always requires24hours of advance notice.','NO','Text dispenses with advance notice and specifies postentry notice if absent.'),
 ('or_mail','First-class-mail service under the specified subsection extends the compliance or termination period by three days.','YES','Extension expressly stated and properly qualified.')]
for text,claim,answer,why in claims:add('supports_claim',{'claim':(claim,),'text':text},answer,why,'modality_conditions_or_attribution')
assert len(cases)==96
assert set(collections.Counter(c['task']for c in cases).values())=={16}
for c in cases:
 for field,meta in c['sources'].items():
  assert (ROOT/meta['path']).read_text()[meta['start']:meta['end']]==c['state'][field]
print('complete',dict(collections.Counter(c['task']for c in cases)))
