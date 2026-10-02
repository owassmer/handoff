import sys
sys.path.insert(0, "register/work")
from q5_lib import add, nd, rule

J = "Judicial Conference notice of Jan. 30, 2025, 90 F.R. 8941 (corrected 90 F.R. 10643), effective 2025-04-01"

# 11 USC 104
add("US:11 USC 104", "new_rule",
    "Fixes which dollar amount applies to a case (priority for deposits, preference floor, involuntary-petition threshold, exemptions): the amount in effect when the case was commenced.",
    proposed=[rule("US:11 USC 104", "US:11USC104-dollar-amounts", "11 U.S.C. 104(a), (c)", "landlord; manager; Handoff",
                   "applies",
                   "A dollar amount from 11 U.S.C. 303(b), 507(a), 522(d), 522(f), 523(a)(2)(C), 547(c)(9) or 707(b) is used to decide a former tenant's or owner's bankruptcy case (deposit priority, preference floor, involuntary threshold, exemption).",
                   "Use the amount in effect on the date the case was commenced; an adjustment made later does not apply to a case commenced before it. The amounts adjust every three years on April 1 (1998, then each third year; next 2028-04-01). From 2025-04-01 (" + J + "): 303(b) $21,050; 507(a)(7) $3,800; 522(d)(5) $1,675 plus up to $15,800 of unused 522(d)(1); 547(c)(9) $8,575. Cases commenced 2022-04-01 to 2025-03-31 use the 2022 amounts (87 F.R. 6625): 303(b) $18,600; 507(a)(7) $3,350; 522(d)(5) $1,475 plus up to $13,950; 547(c)(9) $7,575. The amount in 547(c)(8) ($600) is not adjusted.",
                   "major", "8.8", "(a) On April 1, 1998, and at each 3-year interval", "shall not apply with respect to cases commenced before the date of such adjustments.")])

nd("US:11 USC 106", "Abrogates sovereign immunity of governmental units; a private landlord, manager, collector or tenant is not a governmental unit, and a public landlord is outside the aperture.")
nd("US:11 USC 109", "Eligibility to be a debtor; the stay, claim and discharge rules that change the landlord's conduct attach on the filing and are stated in the 362, 1301, 502, 524 rules. The ch.13 limit to individuals is carried in US:11USC1301-codebtor-stay and the proposed discharge rules.")

add("US:11 USC 1141", "partial",
    "The owner's chapter 11 plan binds the tenant, revests the estate in the owner and discharges an entity owner's pre-confirmation debts, including a tenant's untraceable deposit refund claim; the existing owner rule stops at the proof of claim.",
    atom_ids=["US:11USC1107-1306-owner-reorganization"],
    proposed=[rule("US:11 USC 1141", "US:11USC1141-owner-plan-confirmed", "11 U.S.C. 1141(a), (b), (d)(1)-(3), (d)(5)", "owner; manager; tenant",
                   "binds",
                   "The owner is a debtor in chapter 11 (including subchapter V) and the court has confirmed a plan while a former tenant's deposit refund or balance is outstanding.",
                   "The plan binds the owner and the former tenant whether or not the tenant filed a claim, accepted or objected. Unless the plan or confirmation order says otherwise, estate property vests in the owner, so the manager again collects balances and pays refunds for the owner, following the plan. A deposit the tenant can trace stays the tenant's trust money and is refunded in full with the 14-day statement (US:11USC1107-1306-owner-reorganization). A pre-petition claim for an untraceable deposit is paid only as the plan provides for its class (with the $3,800 seventh priority, US:11USC507(a)(7)-deposit-priority), and: (1) owner an entity: confirmation discharges the rest, whether or not the tenant filed a claim, unless the plan liquidates all or substantially all of the estate and the owner stops doing business (then no discharge); (2) owner an individual: the discharge comes only on completion of plan payments (or earlier on the court's order for cause), and never covers a debt excepted under 523, so the manager and owner owe the unpaid remainder of a debt the court has held nondischargeable. A subchapter V plan confirmed without creditor acceptance discharges on completion of the first 3 to 5 years of payments (US:11USC1192-subv-discharge).",
                   "critical", "0.5", "(a) Except as provided in subsections (d)(2) and (d)(3) of this section, the provisions of a confirmed plan bind the debtor",
                   "the holder of such claim has accepted the plan; and",
                   dependencies=["US:11USC1107-1306-owner-reorganization"])])

add("US:11 USC 1192", "new_rule",
    "In an owner's subchapter V case with a plan confirmed without creditor acceptance, fixes when the owner's debts to former tenants are discharged and excepts 523(a) debts.",
    proposed=[rule("US:11 USC 1192", "US:11USC1192-subv-discharge", "11 U.S.C. 1192", "owner; tenant", "discharges",
                   "The owner is a subchapter V chapter 11 debtor and its plan was confirmed under 1191(b) (without acceptance by every impaired class) while a former tenant's untraceable deposit refund claim is outstanding.",
                   "The owner is discharged only after completing the payments due in the first 3 years of the plan (or a longer period up to 5 years the court fixes); the discharge excludes any debt whose last payment is due after that period and any debt of a kind in 523(a). Until then the tenant's claim is paid as the plan provides. A consensual plan (1191(a)) discharges under 1141(d) at confirmation (US:11USC1141-owner-plan-confirmed).",
                   "minor", "0.5", "If the plan of the debtor is confirmed under section 1191(b) of this title", "of the kind specified in section 523(a) of this title.")])

add("US:11 USC 1305", "new_rule",
    "A former tenant in chapter 13 who incurs rent or charges after the filing: the landlord may file a postpetition claim and be paid through the plan, and loses it if trustee approval was practicable and not obtained.",
    proposed=[rule("US:11 USC 1305", "US:11USC1305-postpetition-claim", "11 U.S.C. 1305(a)(2), (b), (c); 1328(d)", "landlord", "may",
                   "The tenant is a debtor in chapter 13 and, after the order for relief, incurred rent, use and occupancy or other lease charges (a consumer debt) that remain unpaid at move-out.",
                   "The landlord may file a proof of claim for the postpetition charges if the housing was property or services necessary for the debtor's performance under the plan. The claim is allowed or disallowed as if it arose before the filing, and is paid as the plan (as modified) provides. It is disallowed if the landlord knew or should have known that getting the trustee's prior approval of the debtor incurring the obligation was practicable and it was not obtained; a claim allowed without that approval where approval was practicable is not discharged (1328(d)). If the landlord files no 1305 claim, the postpetition balance is not provided for by the plan and is not discharged under 1328(a); it is collected outside the plan only from property that is not property of the estate or after the case closes, is dismissed or the stay is lifted.",
                   "major", "8.8", "(a) A proof of claim may be filed by any entity that holds a claim against the debtor", "was practicable and was not obtained.",
                   determinacy="MIXED", judgment_terms=["necessary for the debtor's performance under the plan", "knew or should have known", "practicable"])])

add("US:11 USC 1322", "new_rule",
    "In a tenant's chapter 13, the plan decides whether the unexpired lease is assumed or rejected and may pay a balance shared with a co-tenant or guarantor in full; priority claims are paid in full.",
    proposed=[rule("US:11 USC 1322", "US:11USC1322-plan-lease-codebtor", "11 U.S.C. 1322(a)(2), (b)(1), (b)(3), (b)(7)", "landlord; tenant", "may",
                   "A tenant files chapter 13 while the lease is unexpired, or owes a balance for which a co-tenant or individual guarantor is also liable.",
                   "The plan may assume, reject or assign the unexpired lease if it was not already rejected (and subject to 365: a lease that ended before the filing cannot be assumed; an assumption requires the debtor to cure defaults and give adequate assurance). A rejection damages claim is a pre-petition unsecured claim (US:11USC365(d)(1)-ch7-rejection breach date; US:11USC502(b)(6)-lessor-cap). The plan may pay the landlord's claim on a consumer debt shared with a co-debtor differently from other unsecured claims, including in full; the co-debtor stay stays in force while the case is pending (US:11USC1301-codebtor-stay). The landlord receives on its pre-petition balance what the confirmed plan pays on its allowed claim (US:11USC1327-plan-binds).",
                   "major", "8.8", "(7) subject to section 365 of this title, provide for the assumption, rejection, or assignment", "not previously rejected under such section;",
                   dependencies=["US:11USC1301-codebtor-stay", "US:11USC502(b)(6)-lessor-cap"])])

add("US:11 USC 1327", "new_rule",
    "A confirmed chapter 13 plan binds the landlord whether or not it filed, objected or was provided for; this governs what it may collect during the case.",
    proposed=[rule("US:11 USC 1327", "US:11USC1327-plan-binds", "11 U.S.C. 1327(a)-(c)", "landlord; collector", "binds",
                   "A former tenant's chapter 13 plan has been confirmed while the landlord holds a pre-petition balance (or, if the owner is the chapter 13 debtor, while the tenant holds a refund claim).",
                   "The plan's provisions bind the landlord whether or not its claim is provided for and whether or not it objected to, accepted or rejected the plan. The landlord takes on the pre-petition balance only what the plan pays; it may not collect the balance outside the plan while the case is pending. Unless the plan or confirmation order says otherwise, estate property vests in the debtor on confirmation free and clear of the claims the plan provides for. An objection to confirmation must be raised before confirmation (FRBP 3015(f), US:FRBP3015-plan-objection).",
                   "major", "8.8", "(a) The provisions of a confirmed plan bind the debtor and each creditor", "has accepted, or has rejected the plan.")])

add("US:11 USC 1328", "new_rule",
    "Decides which part of a former tenant's balance a chapter 13 discharge ends: willful property damage is discharged in a completed-plan discharge but not in a hardship discharge; fraud debts survive.",
    atom_ids=[],
    proposed=[rule("US:11 USC 1328", "US:11USC1328-ch13-discharge", "11 U.S.C. 1328(a)-(f)", "landlord; collector", "discharges",
                   "A former tenant is (or was) a chapter 13 debtor and owes the landlord a balance that arose before the filing, or a claim the plan provides for.",
                   "(1) Completed plan (1328(a)): the court discharges every debt provided for by the plan (a plan provides for the balance when it makes provision for it, including through a class of general unsecured claims, whether or not the landlord filed a claim) or disallowed under 502, except debts of the kinds in 523(a)(2) (false pretenses, fraud, a materially false written statement of financial condition), (a)(3) (unscheduled without notice), (a)(4) (fiduciary fraud, embezzlement, larceny), (a)(1)(B)-(C) and 507(a)(8)(C) taxes, (a)(5) domestic support, (a)(8) student loans and (a)(9) intoxicated-driving injuries, long-term debts cured under 1322(b)(5), criminal restitution and fines, and damages awarded in a civil action for willful or malicious injury that caused personal injury or death. A debt for willful and malicious damage to the unit or the landlord's property (523(a)(6)) IS discharged by a completed-plan discharge. (2) Hardship discharge before completion (1328(b), (c)): only unsecured debts provided for by the plan are discharged, and every 523(a) kind is excepted, including willful and malicious injury to property. (3) No discharge if the debtor received a chapter 7, 11 or 12 discharge in a case filed in the 4 years before this case's order for relief, or a chapter 13 discharge in a case filed in the 2 years before; the balance then survives the case. (4) A creditor may ask to revoke the discharge within one year after it is granted only for fraud it learned of after the discharge. A discharged balance is enjoined (US:11USC524(a)(2)). A 523(a)(2) or (a)(4) debt survives only if the landlord obtains a determination by the FRBP 4007(c) deadline (US:FRBP4007-523c-deadline).",
                   "critical", "8.8", "the court shall grant the debtor a discharge of all debts provided for by the plan or disallowed under section 502 of this title, except any debt",
                   "or in paragraph (1)(B), (1)(C), (2), (3), (4), (5), (8), or (9) of section 523(a);",
                   determinacy="MIXED", judgment_terms=["provided for by the plan", "willful or malicious injury"],
                   dependencies=["US:11USC524(a)(2)"])])
