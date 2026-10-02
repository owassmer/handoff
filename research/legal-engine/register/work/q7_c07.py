import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:BCL 1309-A", N, "Certificate of change of a foreign corporation's office, process address or registered agent; a filing with no effect on its authority or on the tenancy."),
    D("NY:BCL 1310", N, "Surrender of a foreign corporation's authority and service on the Secretary of State afterward; after surrender a suit on a pre-surrender lease is only the maintaining of an action, which BCL 1301(b)(1) excludes from doing business (proposed at NY:BCL-1301-doing-business-and-fictitious-name), so the section adds nothing further."),
    D("NY:BCL 1315", N, "Resident shareholders' inspection of a foreign corporation's shareholder records; internal corporate governance."),
    D("NY:BCL 1316", N, "Voting-trust records of foreign corporations; internal corporate governance."),
    D("NY:BCL 1317", N, "Liability of a foreign corporation's directors and officers under BCL 719-720 to the corporation; it gives a tenant no claim against the owner's officers and changes no settlement step."),
    D("NY:BCL 1318", N, "Disclosure to resident shareholders of dividends and share changes; internal corporate governance."),
    D("NY:BCL 1320", N, "Exempts listed or mostly out-of-state foreign corporations from BCL 1316(e), 1317(a)(1), 1318 and 1319(a)(4); governance provisions outside the chain."),
    D("NY:CCA 101", N, "Short title of the New York City Civil Court Act; changes no rule's reach."),
    D("NY:CCA 102", N, "Establishes the Civil Court as a city-wide court of record; its jurisdiction and procedure are stated in the CCA rules the chain uses."),
    D("NY:CCA 102-A", N, "Number, residence and election of Civil Court judges; court composition."),
    D("NY:CCA 103", N, "Appellate Division supervision of the Civil Court; court administration."),
    D("NY:CCA 104", N, "Civil Court expenses are a charge on the City; no party cost or step."),
    D("NY:CCA 109", N, "Chief clerk and staff may administer oaths, take acknowledgments and sign process; no party step or condition."),
]

S = "NY:CCA 2101"
rows.append(D(S, "partial",
  "The lease balance is stated not to be a consumer credit transaction under CPLR 105(f); CCA 2101(g) carries the same "
  "credit-extended definition into the Civil Court Act, which today keeps the consumer-credit venue branch of CCA 301(a) "
  "off a lease-balance suit (the pending S9760 changes that, as NY:S9760-venue states). No rule states current Civil "
  "Court venue for the balance.",
  ["NY:ADJ-lease-balance-not-consumer-credit", "NY:S9760-venue"], [R(
  "NY:CCA-2101(g)-balance-venue-current", S, "CCA 2101(g); CCA 301(a)", "landlord (plaintiff); collector suing in its name",
  "must",
  "The landlord or its collector sues a former tenant in the NYC Civil Court for a residential lease balance (rent, use "
  "and occupancy, damage or other lease charges), and the action is commenced before NY:S9760-venue takes effect.",
  "The action does not arise out of a 'consumer credit transaction' as CCA 2101(g) defines it (credit extended to an "
  "individual), so the tenant-county rule of CCA 301(a) for consumer credit actions does not apply. The action is "
  "brought in the county within the city where one of the parties resides when it is commenced: the tenant's county, "
  "or the owner's county, an entity owner residing in any county where it transacts business or keeps an office (CCA "
  "305). If no party resides in the city, CCA 301(b) governs. For actions commenced on or after NY:S9760-venue takes "
  "effect, that rule controls instead. The added consumer-credit filing fee does not apply (NY:CCA-1911-clerk-fees).",
  Q(S, "(g) \"Consumer credit transaction\" means a transaction wherein credit is extended to an individual"),
  "major", "Step 8.10 where to sue a small balance", dependencies=["NY:ADJ-lease-balance-not-consumer-credit", "NY:S9760-venue"],
  amends="NY:ADJ-lease-balance-not-consumer-credit",
  reasoning="CCA 301(a) confines the defendant's-county rule to 'an action arising out of a consumer credit transaction' "
            "and sends 'all other cases' to the county where one of the parties resides; the lease balance is not a "
            "credit extension (NY:ADJ-lease-balance-not-consumer-credit), so it is in 'all other cases'.",
  construction=[{"source_file": "register/texts/NY_CCA/301.txt", "quote": Q("register/texts/NY_CCA/301.txt",
    "(a) in an action arising out of a consumer credit transaction where a", "in the county in which one of the parties resides at the commencement thereof; or")}])]))

rows += [
    D("NY:CCA 2103", N, "Appellate Divisions adopt Civil Court rules; the rules themselves (22 NYCRR Part 208) are decided where they bind a party."),
    D("NY:CPLR 102", N, "Only the Legislature amends CPLR rules and no amendment changes substantive rights; no party step."),
    D("NY:CPLR 1026", N, "Names the Chief Administrator as the party when court administrative determinations are reviewed; outside the chain."),
    D("NY:CPLR 107", N, "Chief Administrator's appendix of official CPLR forms; the forms a landlord must use (the commercial-claims demand letter) are fixed by the stated CCA rules."),
]

S = "NY:CPLR 1208"
rows.append(D(S, "new_rule",
  "The proposed CPLR 1207 rule makes a settlement with an infant or incapacitated former tenant bind only on court "
  "approval; 1208 fixes what the application must contain, who must attend, who may represent the tenant, and that the "
  "landlord's attorney may prepare the papers when the tenant has none. No rule states it.",
  proposed=[R("NY:CPLR-1208-incapacitated-settlement-papers", S, "CPLR 1208(a)-(f)", "landlord and its attorney; tenant's representative",
  "must",
  "The landlord settles a claim with a former tenant who is an infant, adjudicated incompetent or conservatee (the "
  "tenant's deposit claim or the landlord's balance claim), so the settlement needs court approval under CPLR 1207.",
  "The application includes an affidavit of the tenant's representative stating his name, residence and relationship; "
  "the tenant's name, age and residence; the circumstances of the claim; the nature and extent of the damages; the "
  "settlement terms and proposed distribution and his approval of both; any other settlement application on the same "
  "claim; any reimbursement received; and any related family claim. If the tenant or representative has an attorney, "
  "that attorney's affidavit states the reasons for recommending the settlement, that he is not concerned in it at the "
  "landlord's instance and takes no compensation from the landlord, and his services. At the hearing the moving party, "
  "the tenant and his attorney attend unless excused for good cause. No attorney with an interest conflicting with the "
  "tenant's may represent him, so the landlord's attorney never represents the tenant; if the tenant has no attorney, "
  "the landlord's attorney may prepare the papers and they must say so. A settlement without this approval does not "
  "bind (dependency).",
  Q(S, "(e) Representation. No attorney having or representing any interest conflicting with that of an infant or incompetent may represent the infant or incompetent.",
    "the papers may be prepared by the attorney for an adverse party or person and shall state that fact."),
  "minor", "Step 8.1b payments and settlements; Step 7.6 the tenant's claims",
  dependencies=["NY:CPLR-1207-incapacitated-settlement", "NY:CPLR-1203-1015-5208-parties"])]))

rows += [
    D("NY:CPLR 1211", N, "Petition to apply an infant's property to its support; no landlord or tenant settlement step."),
    D("NY:CPLR 208-A", N, "Extra two-year window for injury claims of persons in correctional custody; no deposit or balance claim is such an injury claim."),
    D("NY:CPLR 214-A", N, "Limitation period for medical, dental and podiatric malpractice; the lease and deposit limitation periods are stated."),
    D("NY:CPLR 214-B", N, "Limitation period for Agent Orange injury claims; outside the chain."),
]
save(rows)
