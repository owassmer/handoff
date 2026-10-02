import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:22 NYCRR 202.61", N, "Appraisal-report exchange in eminent domain proceedings; outside the tenancy chain."),
    D("NY:22 NYCRR 202.62", N, "Notice on applications to be paid an eminent domain award; outside the tenancy chain."),
    D("NY:22 NYCRR 202.64", N, "Election Law proceedings in Supreme Court; outside the tenancy chain."),
    D("NY:22 NYCRR 202.66", N, "Court approval of third-party settlements under the Workers' Compensation Law; outside the tenancy chain."),
    D("NY:22 NYCRR 202.67", N, "This text is marked effective only until 2025-07-07, so it is not in force; it governed court approval of settlements of claims brought by infants and incapacitated persons, and the incapacity rules the chain needs (CPLR 1203, 1015, 5208) are stated."),
    D("NY:22 NYCRR 202.68", N, "Indian Child Welfare Act verification in custody proceedings; outside the tenancy chain."),
    D("NY:22 NYCRR 202.69", N, "Repealed section; no text in force."),
    D("NY:22 NYCRR 202.72", N, "Dedicated parts and schedules for child-sexual-abuse actions revived under CPLR 214-g; outside the tenancy chain."),
    D("NY:22 NYCRR 202.9-a", N, "Special proceeding by public employees or defense attorneys to expunge a retaliatory UCC financing statement; no landlord, tenant or collector step."),
    D("NY:22 NYCRR 208.13", N, "Medical report exchange in personal-injury actions in Civil Court; a deposit or balance suit seeks no personal-injury recovery."),
    D("NY:22 NYCRR 208.19", N, "Law-journal publication of Civil Court reserve calendar calls; court administration with no party step before or at suit."),
    D("NY:22 NYCRR 208.2", N, "Names the five county divisions of the Civil Court and its terms; where a balance is sued is decided by the stated CCA and CPLR venue rules."),
    D("NY:22 NYCRR 208.28", N, "Trial counsel's attendance during a Civil Court jury trial; trial mechanics."),
    D("NY:22 NYCRR 208.3", N, "Structure of Civil Court parts (calendar, trial, motion, small claims); which part a landlord or tenant may use is decided by the stated CCA 1801, 1801-A and 1809 rules."),
    D("NY:22 NYCRR 208.34", N, "Reassignment when a Civil Court judge is absent or disqualified; court administration."),
]
save(rows)
