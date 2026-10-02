import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
RC = "excluded_regime"
rows = [
    D("NY:22 NYCRR 208.35", N, "Bifurcation of liability and damages in personal-injury trials in Civil Court; no deposit or balance suit is a personal-injury action."),
    D("NY:9 NYCRR 2200.1", RC, "Statutory authority of the City Rent and Eviction Regulations; regime: NYC rent control."),
    D("NY:9 NYCRR 2200.5", RC, "Administrator may amend the City Rent and Eviction Regulations; regime: NYC rent control."),
    D("NY:9 NYCRR 2200.6", RC, "Filing of amendments to the City Rent and Eviction Regulations; regime: NYC rent control."),
    D("NY:9 NYCRR 2200.7", RC, "Separability clause of the City Rent and Eviction Regulations; regime: NYC rent control."),
    D("NY:9 NYCRR 2200.8", RC, "District rent offices under the City Rent and Eviction Regulations, which govern only rent-controlled housing accommodations; regime: NYC rent control."),
    D("NY:9 NYCRR 2520.1", RC, "Statutory authority of the Rent Stabilization Code; regime: NYC rent stabilization."),
    D("NY:9 NYCRR 2520.10", RC, "Separability clause of the Rent Stabilization Code; regime: NYC rent stabilization."),
    D("NY:9 NYCRR 2520.5", RC, "Designations (RSL, ETPA, DHCR, Loft Board, TPU) used in the Rent Stabilization Code; regime: NYC rent stabilization."),
    D("NY:9 NYCRR 2520.7", RC, "Effective date of the Rent Stabilization Code; regime: NYC rent stabilization."),
    D("NY:9 NYCRR 2520.9", RC, "Filing of amendments to the Rent Stabilization Code; regime: NYC rent stabilization."),
    D("NY:9 NYCRR 466.1", N, "Human Rights Law notices posted by employers, employment agencies and labor organizations; employment, not housing or collection."),
    D("NY:9 NYCRR 466.4", N, "Human Rights Law notices posted by volunteer fire companies; outside the chain."),
    D("NY:9 NYCRR 466.5", N, "Employer plans to increase minority employment; employment only."),
    D("NY:9 NYCRR 466.9", N, "Mailing list for notice of Division of Human Rights rulemaking; no party duty."),
    D("NY:9 NYCRR 540.2", N, "Definitions for the ESRA regulations, which reach only electronic transactions by or with a governmental entity (540.2(g)); a landlord's electronic statement or refund to a tenant is governed by the stated STT 305/307 and E-SIGN rules."),
    D("NY:9 NYCRR 540.3", N, "Duties of the State's electronic facilitator (ITS) toward governmental entities; no private party duty."),
    D("NY:ABP 101", N, "Short title of the Abandoned Property Law; changes no rule's reach."),
    D("NY:ABP 1306", N, "Abandoned property held by the motor vehicle and tax commissioners; not held by a landlord or manager."),
    D("NY:ABP 1307", N, "Unclaimed proceeds from sales of wrecked property held by sheriffs and county treasurers; outside the chain."),
    D("NY:ABP 1308", N, "Unclaimed wages held by the Department of Labor; outside the chain."),
    D("NY:ABP 1420", N, "Exempts property held by agricultural cooperatives from the Abandoned Property Law; no landlord is such a cooperative."),
    D("NY:ABP 1421", N, "Exempts property held by rural electric cooperatives; outside the chain."),
]

S = "NY:BCL 1301"
rows.append(D(S, "partial",
  "The capacity bar on a foreign corporate owner is stated with 'doing business' left as a judgment; 1301(b) removes "
  "from that judgment the acts of suing, settling claims and keeping bank accounts, and 1301(d) takes a fictitious name "
  "filed with the corporation's authority out of the GBL 130 assumed-name precondition.",
  ["NY:BCL-1312(a)-foreign-authority", "NY:GBL-130-assumed-name"], [R(
  "NY:BCL-1301-doing-business-and-fictitious-name", S, "BCL 1301(a), (b), (d)", "owner (foreign corporation); collector in its name",
  "must",
  "The owner is a corporation formed outside New York, and it or a collector in its name is about to sue a former "
  "tenant or settle the tenancy account.",
  "Only activity other than the acts listed in 1301(b) counts toward 'doing business' for the BCL 1312 bar: "
  "maintaining or defending an action or proceeding, settling it or settling claims or disputes (including the tenant's "
  "deposit claim or the balance), holding directors' or shareholders' meetings, keeping bank accounts (including the "
  "deposit account), and securities-transfer offices are not doing business. Owning and leasing New York units is "
  "weighed under NY:BCL-1312(a)-foreign-authority; a corporation whose only New York acts are those listed may sue "
  "without authority. A foreign corporation authorized under a fictitious name because its own name was unavailable "
  "must use that fictitious name in its New York business, including leases, statements and suits, and GBL 130 does "
  "not apply to that name: no assumed-name certificate is needed before suing on a lease made in it, and a GBL 130 "
  "filing does not adopt a fictitious name. A lease made in any other name than the corporate or filed fictitious name "
  "stays subject to NY:GBL-130-assumed-name.",
  Q(S, "(b) Without excluding other activities which may not constitute doing business in this state,",
    "or effecting settlement thereof or the settlement of claims or disputes."),
  "major", "Step 8.10 before suing: capacity", determinacy="MIXED", judgment_terms=["doing business in this state"],
  dependencies=["NY:BCL-1312(a)-foreign-authority", "NY:GBL-130-assumed-name"],
  amends="NY:BCL-1312(a)-foreign-authority",
  reasoning="1301(d) excludes GBL 130 for a filed fictitious name, so the assumed-name precondition does not reach it.",
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S,
    "The provisions of section one hundred thirty of the general business law shall not apply to any fictitious name filed by a foreign corporation pursuant to this section")}])]))

rows += [
    D("NY:BCL 1302", N, "Keeps in force authority issued under statutes before the BCL; a corporation's current authority is what the stated BCL 1312 rule checks."),
    D("NY:BCL 1303", N, "Attorney General's action to restrain or annul a foreign corporation's authority; enforcement by the State, not a step for the owner, manager or tenant in the settlement."),
    D("NY:BCL 1304", N, "Contents of a foreign corporation's application for authority; the filing the stated capacity rule requires, with no condition on the tenancy or the suit."),
    D("NY:BCL 1305", "stated", "Authority begins on the Department of State's filing of the application and lasts while not surrendered, suspended or annulled; the stated rule's pre-suit check is exactly whether that authority is in force.", ["NY:BCL-1312(a)-foreign-authority"]),
    D("NY:BCL 1306", N, "Powers of an authorized foreign corporation match a domestic one's; leasing and suing are within them, so nothing in the chain turns on it."),
    D("NY:BCL 1307", N, "A foreign corporation may hold and convey New York real property; ownership of the building is a fact the chain starts from, and the transfer rules on sale are stated (GOL 7-105)."),
    D("NY:BCL 1308", N, "Matters a foreign corporation may amend in its application; the consequence of a missed amendment is decided under BCL 1309."),
]

S = "NY:BCL 1309"
rows.append(D(S, "partial",
  "The capacity bar is stated; 1309(c) adds that a foreign corporation that changed its name or state of incorporation "
  "and did not file an amendment within 20 days has its authority suspended, which again bars its suit until an "
  "amendment is filed.",
  ["NY:BCL-1312(a)-foreign-authority"], [R(
  "NY:BCL-1309(c)-authority-suspension", S, "BCL 1309(c)", "owner (foreign corporation); collector in its name", "must",
  "An authorized foreign corporation owning the unit changed its corporate name or its jurisdiction of incorporation "
  "in its home jurisdiction and did not deliver a certificate of amendment to the Department of State within 20 days "
  "after the change took effect there.",
  "From the 21st day its New York authority is suspended, so while suspended it is not authorized and cannot "
  "maintain a suit against a former tenant (NY:BCL-1312(a)-foreign-authority). If the Department of State files the "
  "amendment within 120 days after the change, the suspension is annulled and authority continues as if never "
  "suspended. The Secretary of State remains its agent for process on "
  "liabilities incurred before the filing, so the tenant's suit on the deposit is served there. Operator step: before "
  "suing, confirm the owner's New York authority is not suspended and the name on the suit matches the name on file.",
  Q(S, "If an authorized foreign corporation has changed its name in the jurisdiction of its incorporation,",
    "its authority to do business in this state shall upon the expiration of said twenty days be suspended."),
  "minor", "Step 8.10 before suing: capacity", dependencies=["NY:BCL-1312(a)-foreign-authority"],
  amends="NY:BCL-1312(a)-foreign-authority")]))
save(rows)
