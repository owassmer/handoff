import sys
sys.path.insert(0, "register/work")
from q5_lib import add, nd, rule

CH11 = "Chapter 11 plan process (who proposes, classifies, solicits, votes, modifies or implements a plan); the tenant's and manager's positions are fixed by the confirmed plan's effect (US:11USC1141-owner-plan-confirmed), the deposit priority (US:11USC507(a)(7)-deposit-priority) and the bar date (US:FRBP3003-ch11-bar-date)"
for s in ["US:11 USC 1121", "US:11 USC 1122", "US:11 USC 1123", "US:11 USC 1124", "US:11 USC 1125", "US:11 USC 1126", "US:11 USC 1127", "US:11 USC 1128", "US:11 USC 1142", "US:11 USC 1143"]:
    nd(s, CH11 + ".")
nd("US:11 USC 1144", "Revocation of a chapter 11 confirmation order procured by fraud, on request within 180 days; a remedy of plan administration that changes no step of the settlement chain.")
nd("US:11 USC 1146", "Stamp-tax exemption for plan transfers and state tax determinations for the plan proponent; none of the chain's tax events.")
SUBV = "Subchapter V (small business chapter 11) administration"
nd("US:11 USC 1181", SUBV + ": lists chapter 11 sections that do not apply; the discharge consequence is proposed at 1192 (US:11USC1192-subv-discharge).")
nd("US:11 USC 1182", SUBV + ": definitions of small business debtor and debtor for subchapter V; the rules proposed for the owner's chapter 11 apply the same way.")
nd("US:11 USC 1183", SUBV + ": the standing trustee's role (trustee administration).")
nd("US:11 USC 1184", SUBV + ": the debtor in possession's rights; the owner keeps collecting as stated in US:11USC1107-1306-owner-reorganization.")
nd("US:11 USC 1185", SUBV + ": removal of the debtor in possession (trustee administration).")
nd("US:11 USC 1186", SUBV + ": after a nonconsensual plan, post-petition property and earnings are estate property and the debtor stays in possession; the owner's collection role is unchanged.")
nd("US:11 USC 1187", SUBV + ": debtor reporting duties to the court and U.S. trustee.")
nd("US:11 USC 1188", SUBV + ": status conference and debtor's report.")
nd("US:11 USC 1189", SUBV + ": only the debtor may file a plan, within 90 days.")
nd("US:11 USC 1190", SUBV + ": plan contents.")
nd("US:11 USC 1191", SUBV + ": confirmation standards; the discharge effect is proposed at 1192.")
nd("US:11 USC 1193", SUBV + ": plan modification.")
nd("US:11 USC 1194", SUBV + ": trustee's retention and distribution of plan payments.")
nd("US:11 USC 1195", SUBV + ": transactions with professionals.")

add("US:11 USC 1129", "new_rule",
    "A chapter 11 plan must pay a former tenant's priority deposit claim in full in cash (on the effective date unless the class accepts deferred payment), which fixes what the tenant receives and what the manager pays under the owner's plan.",
    proposed=[rule("US:11 USC 1129", "US:11USC1129(a)(9)-priority-cash", "11 U.S.C. 1129(a)(9)(B)", "owner; manager; tenant", "shall",
                   "The owner is a chapter 11 debtor and former tenants hold deposit-refund claims entitled to seventh priority (US:11USC507(a)(7)-deposit-priority).",
                   "Unless a tenant agrees to different treatment, the plan can be confirmed only if each tenant in the priority class receives cash equal to the allowed priority amount on the effective date of the plan, or, if the class has accepted the plan, deferred cash payments whose value on the effective date equals that amount. In a subchapter V case confirmed without consent the same requirement applies (1191(b) keeps 1129(a)(9)). The amount above the priority cap is a general unsecured claim paid as its class is treated.",
                   "minor", "0.5", "(B) with respect to a class of claims of a kind specified in section 507(a)(1), 507(a)(4), 507(a)(5), 507(a)(6), or 507(a)(7) of this title",
                   "cash on the effective date of the plan equal to the allowed amount of such claim;")])

add("US:FRBP 3003", "new_rule",
    "In an owner's chapter 11, a former tenant whose refund claim is unscheduled or scheduled as disputed, contingent or unliquidated must file by the court's bar date or receive nothing on it.",
    proposed=[rule("US:FRBP 3003", "US:FRBP3003-ch11-bar-date", "FRBP 3003(b)(1), (c)(2), (c)(3), (c)(5)", "tenant; owner; manager", "shall",
                   "The owner is a chapter 11 debtor and a former tenant has a pre-petition claim (an untraceable deposit refund or statutory damages).",
                   "A scheduled claim not marked disputed, contingent or unliquidated is prima facie valid in the scheduled amount and needs no proof of claim (US:11USC1111-deemed-filed). A tenant whose claim is not scheduled, or is scheduled as disputed, contingent or unliquidated, must file a proof of claim within the time the court sets (the bar date); a tenant that does not is not treated as a creditor for that claim for voting and distribution, and the claim is discharged on confirmation for an entity owner (US:11USC1141-owner-plan-confirmed). A late claim is allowed only on the conditions of Rule 3002(c)(2)-(4) and (7). A filed claim supersedes the schedule.",
                   "major", "0.5", "(b) Scheduled Liabilities and Listed Equity Security Holders as Prima Facie Evidence of Validity and Amount.", "supersedes any scheduling of the claim or interest under § 521(a)(1).",
                   dependencies=["US:11USC1107-1306-owner-reorganization"])])
