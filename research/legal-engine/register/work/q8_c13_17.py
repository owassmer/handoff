import sys, re; sys.path.insert(0, "register/work")
from q8_lib import D, save, chunks
N = "no_decision"
special = {
 "NYC:RCNY 6 1-02": "Expiration dates of DCWP licences (a debt collection agency licence expires January 31 of odd years); whether a collector's licence is current is a fact the stated licensing rules (NYC:ADC-20-490) test, and the calendar adds no settlement step.",
 "NYC:RCNY 6 1-18": "Former licensees destroy DCWP identification documents after non-renewal; licensing administration.",
 "NYC:RCNY 6 1-23": "References to the Department of Consumer Affairs mean DCWP; a naming rule that changes no rule's reach.",
 "NYC:RCNY 6 5-22": "Reserved section; no text.",
 "NYC:RCNY 6 5-23": "Merchants' layaway plans must follow GBL 396-t; sale of goods, not tenancy.",
 "NYC:RCNY 6 5-31": "Cancellation charges and refunds for contracts for future consumer services (lessons, memberships); a residential lease is a letting of real property, not a consumer-services contract, and boarding accommodations are excluded.",
 "NYC:RCNY 6 5-35": "Disclosure when selling above the manufacturer's suggested price; sale of goods.",
 "NYC:RCNY 6 5-36": "Disclosure that an item sold is used; sale of goods.",
 "NYC:RCNY 6 5-38": "Sales of goods declared in temporary short supply; sale of goods.",
 "NYC:RCNY 6 5-39": "Sellers' cancellation of home pick-up, delivery or repair appointments; a seller-of-goods duty, not a landlord's move-out duty.",
 "NYC:RCNY 6 5-42": "Price gouging on covered emergency goods and services during a declared emergency; a move-out charge passes on the landlord's cost of repair or cleaning to the tenant under the deposit rules and is not a sale of covered goods or services by the landlord.",
 "NYC:RCNY 6 5-79": "Severability clause of the consumer protection rules; decides nothing.",
 "NYC:RCNY 6 5-80": "Citation form for the consumer protection rules; decides nothing.",
}
rows = []
for k in range(13, 18):
    for s in chunks()[k]:
        sid = s["section_id"]
        if sid in special:
            rows.append(D(sid, N, special[sid])); continue
        h = re.sub(r"\s*Penalty Schedule\.?", "", s["heading"]).strip().rstrip(".")
        if "[Repealed]" in s["heading"]:
            rows.append(D(sid, N, f"Repealed DCWP penalty schedule ({h.replace('[Repealed]','').strip()}); no text in force."))
        else:
            rows.append(D(sid, N, f"DCWP penalty schedule for {h}; fines a regulated industry unrelated to the tenancy, its collection or the account."))
save(rows)
