import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s, r in [
  ("NY:GCN 91", "Repeal by the Consolidated Laws includes amending statutes; historical codification with no current settlement effect."),
  ("NY:GCN 92", "Repeal of an amending statute leaves the prior provision in force; no provision in this chain has been so affected."),
  ("NY:GCN 95", "A repeal that substantially re-enacts is a continuation; no stated rule turns on it beyond the point-in-time rules already recorded."),
  ("NY:GOL 1-201", "The 1963 General Obligations Law is a continuation of the provisions it replaced; historical codification."),
  ("NY:GOL 1-202", "Defines 'infant' and 'minor' as under 18 for the GOL; the age of capacity is proposed at GOL 3-101 (NY:GOL-3-101-age-of-capacity) and suits against infants are stated (NY:CPLR-1203-1015-5208-parties)."),
  ("NY:GOL 11-100", "Civil action against those who furnish alcohol to under-21s; not a tenancy settlement."),
  ("NY:GOL 11-101", "Dram-shop civil action; not a tenancy settlement."),
  ("NY:GOL 11-107", "Damages for injury to a guide or service dog by another dog; not a tenancy settlement."),
  ("NY:GOL 13-109", "'Transfer' in GOL 13-101 to 13-107 includes sale, assignment and gift; its reach is carried in the rule proposed at GOL 13-101 (NY:GOL-13-101-105-balance-transfer)."),
  ("NY:GOL 15-107", "Release of a partner from partnership liability; applies to a partnership tenant as the ordinary release rule already stated (NY:GOL-15-104-105-cotenant-release) and changes no settlement amount for a residential tenant."),
  ("NY:GOL 15-702", "Co-signer disclosure in consumer credit transactions; a lease guaranty is not consumer credit (NY:ADJ-lease-balance-not-consumer-credit), and the guaranty writing rule is stated (NY:GOL-5-701(a)(2)-guaranty)."),
  ("NY:GOL 3-102", "Married minors' medical obligations; not a tenancy settlement."),
  ("NY:GOL 3-107", "Parents' liability on infants' employment contracts; not a tenancy settlement."),
  ("NY:GOL 3-311", "Marriage does not change joint ownership of personal property; the co-tenant refund payee rule is stated (NY:ADJ-cotenants-payee)."),
  ("NY:GOL 3-315", "Married woman's right to her own wages; not a tenancy settlement."),
  ("NY:GOL 3-503", "Child-support certification in occupational licence applications; it concerns the licensing agency's process, not the settlement."),
]:
    rows.append(D(s, "no_decision", r))

rows.append(D("NY:GOL 5-101", "stated",
  "Defines 'interest in real property' for GOL 5-703 to include chattel interests (leases) and 'conveyance' to include "
  "a writing surrendering an interest; the stated early-termination rule depends on it.",
  ["NY:GOL-5-703-15-301-early-termination"]))

S = "NY:GCN 62"
rows.append(D(S, "partial",
  "The small-print rule is stated (NY:CPLR-4544-small-print); GCN 62 decides how the point size it requires is "
  "measured, which decides whether a lease clause may be put in evidence.",
  ["NY:CPLR-4544-small-print"], [R(
  "NY:GCN-62-type-size", S, "GCN 62", "landlord", "must",
  "A charge or term rests on a lease clause and a statute requires a minimum type size for it (CPLR 4544: eight "
  "points, 5.5 for upper case; other statutes stating a point size).",
  "The size requirement is met if the x-height of the type (height of lower-case letters without ascenders or "
  "descenders, as printed on the page) is at least 45% of the stated point size, each point being 0.351 mm; for "
  "eight-point type the x-height must be at least 1.264 mm. A clause below that measure is small print under "
  "NY:CPLR-4544-small-print.",
  Q(S, "the type size requirement shall be deemed met if the x-height of the type is a minimum of forty-five percent of the specified point size.",
    "Each point shall be measured as .351 millimeter."),
  "major", "Step 5.2 fees", dependencies=["NY:CPLR-4544-small-print"], amends="NY:CPLR-4544-small-print")]))
save(rows)
