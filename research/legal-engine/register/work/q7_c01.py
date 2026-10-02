import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:16 NYCRR 96.9", N, "Severability clause for Part 96; it keeps the other submetering conditions in force if one is struck and changes no charge, credit or collection step."),
    D("NY:18 NYCRR 352.1", N, "Statewide standard of need for public-assistance eligibility; it fixes the household's grant, not any landlord's deposit, charge, statement or collection step."),
    D("NY:18 NYCRR 352.12", N, "Social services district's verification of the applicant's employment and work benefits; no duty or right of a landlord or collector."),
    D("NY:18 NYCRR 352.14", N, "Support from spouses, parents and relatives in the assistance budget; binds the district and applicant only."),
    D("NY:18 NYCRR 352.17", N, "Defines and computes earned income for the assistance grant; the rental-income passage concerns a recipient who owns the home, not a landlord settling a tenancy."),
    D("NY:18 NYCRR 352.18", N, "Repealed section; no text in force."),
    D("NY:18 NYCRR 352.19", N, "Work-expense disregard in the assistance budget; binds the district only."),
    D("NY:18 NYCRR 352.2", N, "Schedules of monthly assistance grants exclusive of shelter; no landlord duty, charge or payee rule."),
    D("NY:18 NYCRR 352.20", N, "Earned-income exemptions in the assistance budget; binds the district only."),
    D("NY:18 NYCRR 352.21", N, "Individual development accounts for Family Assistance recipients; no step in settling or collecting a tenancy."),
    D("NY:18 NYCRR 352.24", N, "Repealed section; no text in force."),
    D("NY:18 NYCRR 352.28", N, "Repealed section; no text in force."),
]
save(rows)
