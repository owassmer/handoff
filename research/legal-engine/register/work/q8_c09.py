import sys; sys.path.insert(0, "register/work")
from q8_lib import D, save
N = "no_decision"
PA = "public assistance program administration; no duty on a landlord and no effect on the account"
save([
 D("NY:SCPA 1109", N, "Public administrators' reports and audits; administrative."),
 D("NY:SCPA 1117", N, "No separate bond or oath for NYC public administrators; the landlord pays a public administrator on its letters or certificate under the queue's SCPA 1112, 1115 and 1118 proposals, and this changes nothing it checks."),
 D("NY:SCPA 1616", N, "Scope of the ancillary-administration article (non-domiciliary estates); the payee rule for a foreign small estate is the queue's SCPA 1309 proposal."),
 D("NY:SCPA 2108", N, "Court authority for a fiduciary to continue a decedent's sole-proprietor business; who collects rent and receives the statement after an individual owner's or tenant's death is decided by the existing and queued fiduciary rules (NY:COMMONLAW-owner-death-agency, SCPA 1302, 703), and a continuation decree adds no settlement step."),
 D("NY:SCPA 2111", N, "Advance fees of attorney-fiduciaries; estate administration."),
 D("NY:SCPA 2114", N, "Review of a corporate trustee's compensation; estate administration."),
 D("NY:SCPA 2115", N, "Review of a trustee's delegation costs; estate administration."),
 D("NY:SCPA 714", N, "Filing of Supreme Court orders removing guardians or trustees in surrogate's court; court records."),
 D("NY:SCPA 715", N, "Fiduciary's petition to resign; the effect on whom the landlord pays after a fiduciary leaves office is in the queue's SCPA 706 and 720 proposals."),
 D("NY:SCPA 722", N, "Deposit of securities on a removed fiduciary's surcharge; estate administration."),
 D("NY:SCPA 723", N, "Transmission of letters issued to a county fiscal officer to the comptroller; administrative."),
 D("NY:SSL 131-AA", N, "OTDA monthly statistical reports; " + PA + "."),
 D("NY:SSL 131-AAA", N, "Adverse childhood experiences materials; " + PA + "."),
 D("NY:SSL 131-B", N, "Fees for social services to non-recipients; " + PA + "."),
 D("NY:SSL 131-C", N, "Household composition for a minor's public assistance; " + PA + "."),
 D("NY:SSL 131-D", N, "Substance abuse services; " + PA + "."),
 D("NY:SSL 131-E", N, "Family planning services; " + PA + "."),
 D("NY:SSL 131-F", N, "Disregard of retroactive social security increases; " + PA + "."),
 D("NY:SSL 131-G", N, "Acceptance of gifts by social services districts; " + PA + "."),
 D("NY:SSL 131-H", N, "Family homes for adults; " + PA + "."),
 D("NY:SSL 131-I", N, "Inter-district agreements; " + PA + "."),
 D("NY:SSL 131-I*2", N, "Family loan program; " + PA + "."),
 D("NY:SSL 131-K", N, "Referral of undocumented applicants; " + PA + "."),
 D("NY:SSL 131-M", N, "Information and referral services; " + PA + "."),
 D("NY:SSL 131-P", N, "Group health insurance as an eligibility condition; " + PA + "."),
])
