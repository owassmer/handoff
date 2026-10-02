import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:22 NYCRR 202.17", N, "Medical examinations and report exchange in personal-injury and wrongful-death actions; a balance or deposit suit seeks no recovery for personal injury."),
    D("NY:22 NYCRR 202.18", N, "Court-appointed experts in matrimonial actions; outside any tenancy action."),
    D("NY:22 NYCRR 202.2", N, "Defines terms and parts of Supreme Court; court organization with no party step."),
    D("NY:22 NYCRR 202.20-g", N, "How disclosure-conference resolutions are recorded in Supreme Court; litigation mechanics after suit, fixing no settlement, collection or suit precondition."),
    D("NY:22 NYCRR 202.3", N, "Individual assignment of Supreme Court cases to judges; court administration."),
    D("NY:22 NYCRR 202.31", N, "Notice identifying trial counsel in Supreme Court; trial mechanics with no settlement step."),
    D("NY:22 NYCRR 202.34", N, "Pre-marking of trial exhibits; trial mechanics."),
    D("NY:22 NYCRR 202.36", N, "Trial counsel's attendance during trial; trial mechanics."),
    D("NY:22 NYCRR 202.50", N, "Forms of findings and judgments in matrimonial actions; outside any tenancy action."),
    D("NY:22 NYCRR 202.51", N, "Creditor notice when a corporate-dissolution receiver's accounts are settled; a landlord's claim against a dissolving corporate tenant is outside the aperture's consumer tenancy and the rule binds the receiver."),
    D("NY:22 NYCRR 202.54", N, "Notice to Mental Hygiene Legal Service in guardianship proceedings for facility patients; the landlord is not a party and the incapacity rules it needs (CPLR 1203) are stated."),
    D("NY:22 NYCRR 202.56", N, "Filing and conference rules for medical, dental and podiatric malpractice actions; outside any tenancy action."),
    D("NY:22 NYCRR 202.5a", N, "Fax and e-mail submissions to the Supreme Court; court filing mechanics with no settlement step."),
    D("NY:22 NYCRR 202.60", N, "Tax assessment review proceedings in NYC; outside the tenancy chain."),
]
save(rows)
