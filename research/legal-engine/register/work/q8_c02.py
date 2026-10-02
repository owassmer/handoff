import sys; sys.path.insert(0, "register/work")
from q8_lib import D, P, q, save
N = "no_decision"
F1309 = "register/texts/NY_NPCL/1309.txt"
F1313 = "register/texts/NY_NPCL/1313.txt"
r1309 = P("NY:NPCL-1309(b)-name-change-suspension", "N-PCL 1309(b); 1313(a)", "owner (foreign not-for-profit corporation); collector suing in its name", "may not / cure",
  "The owner is a foreign not-for-profit corporation authorized to conduct activities in New York that changed its name in its state of incorporation and did not deliver a certificate of amendment of its application for authority to the Department of State within twenty days after the change took effect; it (or a collector in its name) sues or would sue a former tenant for a balance.",
  "From the twenty-first day after the name change its New York authority is suspended, so it is a foreign corporation conducting activities without authority and cannot maintain the suit (NY:NPCL-1313-foreign-authority). Branch (a): the Department of State files a certificate of amendment changing the name within 120 days after the name change took effect: the suspension is annulled and authority continues as if no suspension had occurred, so capacity to sue is restored for the whole period. Branch (b): no such filing within 120 days: the suspension stands and the corporation cannot maintain the suit until it is authorized and has paid the fees, penalties and franchise taxes 1313(a) requires. In both branches the lease, the deposit statement, the tenant's right to sue it and its defense of the tenant's suit are unaffected (1313(b)), and the Secretary of State remains its agent for the tenant's process during the suspension. Check the Department of State entity record for a name change before a suit is filed.",
  F1309, q(F1309, "If an authorized foreign corporation has changed its name in the jurisdiction of its incorporation", "its authority to conduct activities in this state shall be restored and continue as if no suspension had occurred."),
  "major", "8.10", jurisdiction="NY", instrument="New York Not-for-Profit Corporation Law", dependencies=["NY:BCL-1312(a)-foreign-authority"],
  construction=[(F1313, q(F1313, "A foreign corporation conducting activities in this state without authority shall not maintain any action or special proceeding in this state unless and until such corporation has been authorized"))],
  reasoning="1309(b) suspends the authority of a foreign not-for-profit that fails to file its name change within twenty days; a corporation whose authority is suspended conducts activities without authority, which 1313(a) bars from maintaining any action until authorized. The 120-day filing annuls the suspension retroactively ('as if no suspension had occurred'); absent it, 1313(a)'s own cure (authorization plus back fees) governs. The rule depends on the queue's proposed NY:NPCL-1313-foreign-authority, which is not yet in the rule files, so the existing BCL analogue is listed as the dependency.")
save([
 D("NY:Military Law 328", N, "Short title of Military Law article 13; decides nothing."),
 D("NY:N-PCL 1301", N, "Requires a foreign not-for-profit to be authorized before conducting activities and lists acts that are not conducting activities (suing, settling, bank accounts); an owner leasing NYC units conducts activities under any reading, so the list does not change the reach of the proposed NY:NPCL-1313-foreign-authority bar."),
 D("NY:N-PCL 1302", N, "Transition rule continuing pre-1970 certificates of authority; no effect on a current owner's capacity beyond having authority, which the 1313 bar already tests."),
 D("NY:N-PCL 1303", N, "Attorney General actions to restrain or annul a foreign not-for-profit's authority; an owner whose authority is annulled is simply without authority, which the proposed NY:NPCL-1313-foreign-authority already covers."),
 D("NY:N-PCL 1304", N, "Contents of an application for authority; a filing form, the capacity consequence sits in 1313."),
 D("NY:N-PCL 1305", N, "Effect of filing the application: authority continues while the corporation keeps its home-state authority; capacity is tested under the proposed 1313 bar by whether authority exists, with nothing further for the account."),
 D("NY:N-PCL 1306", N, "Powers of an authorized foreign not-for-profit; no effect on the account."),
 D("NY:N-PCL 1307", N, "Foreign not-for-profit may hold and convey real property; ownership of the building is a Step 0 fact already assumed, no settlement rule turns on it."),
 D("NY:N-PCL 1308", N, "Permitted amendments to an application for authority; filing mechanics only (the name-change suspension is in 1309(b))."),
 D("NY:N-PCL 1309", "new_rule", "1309(b) suspends a foreign not-for-profit owner's authority twenty days after an unfiled name change, which bars it from suing a former tenant until cured; the 120-day retroactive cure is not in any rule.", proposed=[r1309]),
 D("NY:N-PCL 1310", N, "Certificate of change of office, process address or registered agent; filing mechanics, no suspension or capacity consequence."),
 D("NY:N-PCL 1311", N, "Surrender of authority and service on the Secretary of State for earlier liabilities; affects where a tenant serves process, not what the landlord does, owes or recovers."),
 D("NY:N-PCL 1316", N, "Members' right to inspect a foreign not-for-profit's member records; internal governance."),
 D("NY:N-PCL 1317", N, "Voting trust records of a foreign corporation; internal governance."),
 D("NY:N-PCL 1318", N, "Directors' and officers' liability under N-PCL 719-720 applied to foreign not-for-profits; runs to the corporation and its members, not to tenants or the account."),
 D("NY:N-PCL 1319", N, "Foreign not-for-profit's disclosure duty to its members; internal governance."),
 D("NY:N-PCL 1321", N, "Exemption of certain foreign not-for-profits from 1317(e), 1318(a)(1) and 1320(a)(2); internal governance."),
 D("NY:Partnership Law 121-1002", N, "Limited partners' derivative action; internal partnership governance."),
 D("NY:Partnership Law 121-1003", N, "Security for expenses in a derivative action; internal partnership governance."),
 D("NY:Partnership Law 121-1004", N, "Indemnification of general partners in derivative actions; internal partnership governance."),
])
