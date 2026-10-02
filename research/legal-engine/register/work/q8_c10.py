import sys; sys.path.insert(0, "register/work")
from q8_lib import D, save
N = "no_decision"
save([
 D("NY:SSL 131-SS", N, "OTDA data matching to enroll assistance recipients in utility affordability programs; binds OTDA and utility corporations, not a landlord billing lease utilities."),
 D("NY:SSL 131-Z", N, "Child assistance program; public assistance administration, no landlord duty."),
 D("NY:SSL 131-ZZ", N, "Child poverty reduction advisory council; policy body, decides nothing for the account."),
 D("NY:SSL 132", N, "Investigation of public assistance applications; binds social services officials, not landlords."),
 D("NY:SSL 132-A", N, "Paternity inquiry for assistance applicants; public assistance administration."),
])
