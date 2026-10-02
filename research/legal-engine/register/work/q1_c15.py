import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s, r in [
  ("NY:GCN 13-A", "Defines 'armed forces of the United States' for statutes using that term; the chain's military rules carry their own definitions (US:50USC3911(1)-(2), NY:MIL-310(2))."),
  ("NY:GCN 14", "An undertaking satisfies a required bond; no settlement step requires a bond."),
  ("NY:GCN 24-A", "Saturday and emergency closings are holidays only for the closed banking organization's own acts; the chain's deadlines fall on the landlord and are counted under NY:GCN-20, NY:GCN-24 and NY:GCN-25-a(1)."),
  ("NY:GCN 41-A", "Recitals in minutes of meetings as evidence; not a settlement matter."),
  ("NY:GCN 45", "Private seals of officers as a corporate seal; seals have no effect on any instrument in this chain."),
  ("NY:GCN 57", "Which years are leap years; chain deadlines are counted in calendar days under NY:GCN-20, which this does not change."),
  ("NY:GCN 59", "Terminology for children born out of wedlock; not a settlement matter."),
  ("NY:GCN 80", "A reference to a repealed and re-enacted provision reads as a reference to the new one; no stated rule turns on a renumbered cross-reference."),
  ("NY:GCN 90", "Repealing a repealing statute does not revive the earlier provision; no provision in this chain has been so revived or depends on it."),
  ("NY:GOL 1-203", "Start dates (1928 to 1974) of GOL sections; every tenancy in this chain arose after them, so they change nothing."),
  ("NY:GOL 11-103", "Civil action against unlawful sellers of controlled substances; not a tenancy settlement."),
  ("NY:GOL 15-110", "Repeal clause of GOL title 15; it states no operative rule."),
  ("NY:GOL 17-105", "Waivers and promises extending the time to foreclose a mortgage; mortgage enforcement."),
  ("NY:GOL 17-107", "Part payment extending the time to foreclose a mortgage; mortgage enforcement."),
  ("NY:GOL 3-103", "Capacity of minor veterans for GI Bill loans; not a lease."),
]:
    rows.append(D(s, "no_decision", r))

S = "NY:GCN 58"
rows.append(D(S, "partial",
  "Month counting is stated (NY:GCN-30); GCN 58 fixes what 'year' means in statutes and leases (twelve months; 365 "
  "days with the leap day and the day before counted as one), which governs the chain's yearly periods.",
  ["NY:GCN-30", "NY:GCN-20"], [R(
  "NY:GCN-58-year", S, "GCN 58", "landlord, manager, Handoff", "must",
  "A statute, lease or other instrument in the chain sets a period in years (the three-year unclaimed-refund period, "
  "limitation periods, a one-year lease, 'per annum' interest and the 1% yearly fee, 'within one year' notices).",
  "A year is twelve months (a half year six months, a quarter three months); counted in days it is 365 days, with the "
  "leap day and the day before it counted as one day. The period ends on the corresponding date the stated number of "
  "years later, subject to NY:GCN-25-a(1) where the last day is a weekend or holiday.",
  Q(S, "The term year in a statute, contract, or any public or private instrument, means three hundred and sixty-five days",
    "the term a quarter of a year, three months."),
  "minor", "Step 6.3 counting", dependencies=["NY:GCN-30", "NY:GCN-20"])]))

save(rows)
