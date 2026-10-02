import sys; sys.path.insert(0, "register/work")
from q8_lib import D, save
N = "no_decision"
PA = "public assistance program administration; no landlord duty and no effect on the account"
save([
 D("NY:SSL 133", N, "Emergency needs assistance pending investigation; " + PA + " (HRA security vouchers and rent payments are in the NYC rules already stated)."),
 D("NY:SSL 133-A", N, "Contracts to distribute assistance grants; " + PA + "."),
 D("NY:SSL 134-A", N, "Conduct of eligibility investigations; " + PA + "."),
 D("NY:SSL 134-B", N, "Front-end fraud detection; " + PA + "."),
 D("NY:SSL 134-C", N, "Posting of applicants' rights; " + PA + "."),
 D("NY:SSL 135", N, "Cooperation among welfare officials; " + PA + "."),
 D("NY:SSL 136-A", N, "Tax information for welfare fraud investigations; " + PA + "."),
 D("NY:SSL 138-A", N, "Assistance for residents of family care homes; " + PA + "."),
 D("NY:SSL 144", N, "Welfare officials' oath and subpoena powers; " + PA + "."),
 D("NY:SSL 147", N, "Crimes of misusing food stamps and EBT devices; not a tenancy matter."),
 D("NY:SSL 149", N, "Penalty for bringing a needy person into the state; not a tenancy matter."),
 D("NY:SSL 150", N, "Penalties on welfare officers for failing to report or pay over; " + PA + "."),
 D("NY:SSL 152", N, "Public welfare association funding; " + PA + "."),
 D("NY:SSL 152-C", N, "Menstrual products in state-funded temporary shelters; binds shelter providers, not a market-rate landlord."),
 D("NY:SSL 152-D", N, "Replacement of stolen public assistance; binds social services districts, not the landlord's account."),
 D("NY:STT 301", N, "Short title of the Electronic Signatures and Records Act; the operative rules are stated in NY:STT-305(3) and NY:STT-307."),
 D("NY:STT 303", N, "Office of Information Technology Services as electronic facilitator; administrative."),
 D("NY:UCC 1-101", N, "Short title of the UCC."),
 D("NY:UCC 1-105", N, "UCC severability clause; decides nothing."),
 D("NY:UCC 1-106", N, "Singular/plural and gender construction in the UCC; changes the reach of no rule."),
 D("NY:UCC 1-107", N, "Section captions are part of the UCC; changes the reach of no rule (the full-payment-check rule UCC 1-308 is stated in its text)."),
 D("NY:UCC 1-203", N, "Distinguishes a lease of goods from a security interest; applies to goods, not a residential real-property lease."),
 D("NY:UCC 3-101", N, "Short title of UCC article 3."),
 D("NY:UCC 3-102", N, "Article 3 definitions (issue, order, instrument); no stated or proposed rule depends on them (a refund check's delivery and discharge are governed by the deposit rules)."),
 D("NY:UCC 3-701", N, "Letters of advice for international sight drafts; banking matter."),
 D("NYC:ADC 20-101", N, "Legislative intent of the DCWP licensing title; declares policy, decides nothing."),
 D("NYC:ADC 20-102", N, "Definitions for the DCWP licensing title (license, organization, person, trade name); the debt-collection licence rules (NYC:ADC-20-489(a), 20-490) apply by their own definitions and these terms do not change their reach."),
])
