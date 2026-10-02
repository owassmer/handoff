import sys, re; sys.path.insert(0, "register/work")
from q8_lib import D, save, chunks
N = "no_decision"
rows = []
for s in chunks()[18][:11]:
    h = re.sub(r"\s*Penalty Schedule\.?", "", s["heading"]).strip().rstrip(".")
    rows.append(D(s["section_id"], N, f"DCWP penalty schedule for {h}; fines a regulated industry unrelated to the tenancy, its collection or the account."))
rows += [
 D("NYC:RCNY 68 7-01", N, "Definitions for the LINC VI rental assistance chapter, which expired and was repealed on 2024-12-31 (68 RCNY 7-08, decided in the queue); no current rule depends on them."),
 D("US:11 USC 1110", N, "Chapter 11 protection of aircraft and vessel lessors and financiers; not a residential lease."),
 D("US:11 USC 1114", N, "Retiree insurance benefits in chapter 11; not a tenancy matter."),
 D("US:11 USC 304", N, "Repealed section; no text in force."),
 D("US:11 USC 307", N, "United States trustee may be heard in any case; no duty on the landlord (who is paid a refund in a tenant's case is in US:11USC542-refund-payee)."),
 D("US:11 USC 321", N, "Eligibility to serve as bankruptcy trustee; the landlord pays whoever is appointed trustee under the stated payee rules."),
 D("US:11 USC 324", N, "Removal of a trustee or examiner; the landlord pays the trustee in office under the stated payee rules, with no further step."),
 D("US:11 USC 333", N, "Patient care ombudsman for health care debtors; not a tenancy matter."),
 D("US:11 USC 555", N, "Securities contract safe harbor from the stay; not a residential lease."),
 D("US:11 USC 556", N, "Commodity and forward contract safe harbor; not a residential lease."),
 D("US:11 USC 557", N, "Grain storage facility procedures; not a tenancy matter."),
 D("US:11 USC 559", N, "Repurchase agreement safe harbor; not a residential lease."),
 D("US:11 USC 728", N, "Repealed section; no text in force."),
 D("US:12 CFR 1005.14", N, "Regulation E duties of an EFT service provider that issues its own access device for a consumer's account held elsewhere; a landlord, manager or Handoff taking or paying by ACH issues no access device, and the payee duties are in the queue's US:12CFR1005.3(a)-payee-duties."),
]
save(rows)
