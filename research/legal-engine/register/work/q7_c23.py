import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:LLC Law 209", N, "Department of State files LLC instruments on form review only; a filing formality with no settlement step."),
    D("NY:LLC Law 211", N, "Amendment of an LLC's articles, required within 90 days of a name change; the LLC Law attaches no suspension or suit bar to a late amendment, and the name the owner must use is governed by the stated GBL 130 rule."),
    D("NY:LLC Law 211-A", N, "Certificate of change of an LLC's office, process address or registered agent; a filing formality with no settlement step."),
    D("NY:LLC Law 212", N, "Correction of LLC filings; a filing formality that expressly leaves accrued rights and liabilities unaffected."),
    D("NY:LLC Law 213", N, "Member and manager authorization of amendments to LLC articles; internal to the LLC."),
    D("NY:LLC Law 214", N, "Restated LLC articles; a filing formality with no settlement step."),
    D("NY:LLC Law 801", N, "Home-state law governs a foreign LLC's internal affairs and members' liability; the chain claims against the owner LLC itself, and the capacity bar is stated (NY:LLC-808(a)-foreign-authority)."),
]

S = "NY:LLC Law 803"
rows.append(D(S, "partial",
  "The capacity bar on a foreign LLC owner is stated with 'doing business' left as a judgment; 803(a) removes from that "
  "judgment suing, settling claims, members' meetings and keeping bank accounts. The same exclusions as BCL 1301(b) for "
  "corporations.",
  ["NY:LLC-808(a)-foreign-authority"], [R(
  "NY:LLC-803-doing-business-exclusions", S, "LLC Law 803(a)", "owner (foreign LLC); collector in its name", "must",
  "The owner is a limited liability company formed outside New York, and it or a collector in its name is about to sue a "
  "former tenant or settle the tenancy account.",
  "Only activity other than the acts listed in 803(a) counts toward 'doing business' for the LLC Law 808 bar: "
  "maintaining or defending an action or proceeding, settling it or settling claims or disputes (including the tenant's "
  "deposit claim or the balance), holding members' or managers' meetings, keeping bank accounts (including the deposit "
  "account), and offices only for membership-interest transfers are not doing business. Owning and regularly leasing "
  "New York units is weighed under NY:LLC-808(a)-foreign-authority; a foreign LLC whose only New York acts are those "
  "listed may sue without a certificate of authority. The list does not decide whether the LLC may be served with "
  "process in New York.",
  Q(S, "(a) Without excluding other activities that may not constitute doing business in this state,",
    "or effecting settlement thereof or the settlement of claims or disputes;"),
  "major", "Step 8.10 before suing: capacity", determinacy="MIXED", judgment_terms=["doing business in this state"],
  dependencies=["NY:LLC-808(a)-foreign-authority"], amends="NY:LLC-808(a)-foreign-authority")]))

rows += [
    D("NY:LLC Law 804", N, "A foreign LLC amends its application for authority within 90 days of a home-state name change; the section attaches no suspension or suit bar to a late filing, unlike BCL 1309(c) for corporations."),
    D("NY:LLC Law 804-A", N, "Certificate of change of a foreign LLC's office, process address or registered agent; a filing formality with no settlement step."),
    D("NY:LLC Law 805", "stated", "A foreign LLC is authorized on the Department of State's filing of its application, and authority lasts while it keeps home-state authority and has not surrendered or lost it; the stated rule's pre-suit check is whether that certificate of authority is in force.", ["NY:LLC-808(a)-foreign-authority"]),
    D("NY:LLC Law 806", N, "Surrender of a foreign LLC's authority, with the Secretary of State kept as agent for process on New York causes of action; after surrender a suit on a pre-surrender lease is only the maintaining of an action, which LLC Law 803(a)(1) excludes from doing business (proposed at NY:LLC-803-doing-business-exclusions)."),
    D("NY:LLC Law 809", N, "Attorney General actions to restrain or annul a foreign LLC's authority; State enforcement, not a step for owner, manager or tenant."),
    D("NY:LLC Law 810", N, "Beneficial ownership disclosure by foreign LLCs (marked effective and repealed 2026-01-01); a past-due or delinquent record notation that bars no suit or collection, as the queue decision on LLC Law 215 also records."),
]
save(rows)
