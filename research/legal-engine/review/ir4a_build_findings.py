"""Independent review 4A, Phase 2: build review/independent_review_4a.json from the diff of the universe against the rules.

Evidence quotes are cut mechanically from saved sources (ir4a_lib.cut). Newness versus earlier rounds is added by
ir4a_newness.json (written only after the findings were saved). Run: python3 review/ir4a_build_findings.py
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ir4a_lib import cut  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
S = "sources/"
F = []
ERR = []


def ev(src, start, end=None):
    try:
        return {"source_file": S + src, "quote": cut(S + src, start, end, maxlen=1400)}
    except Exception as e:  # noqa: BLE001
        ERR.append(f"{src}: {e}")
        return {"source_file": S + src, "quote": "ERROR"}


def add(kind, severity, step, rule_ids, finding, correct_rule, evidence):
    F.append({"id": f"R4A-{len(F) + 1:02d}", "kind": kind, "severity": severity, "rule_ids": rule_ids, "step": step,
              "finding": finding, "correct_rule": correct_rule, "evidence": evidence})


# ============================ CRITICAL ============================
add("partial", "critical", "S5 charges and credits (move-out fees)",
    ["NYC:FARE-moveout-service-fee", "NYC:FARE-20-699.20-fee", "NYC:FARE-20-699.22(b)"],
    "The FARE atoms treat a move-out service fee as lawful if it was on the pre-lease disclosure. They miss Admin Code "
    "20-699.21: a 'landlord's agent' (a licensed agent who found or obtained the tenant for the landlord) may not impose "
    "or collect ANY fee from the tenant related to the rental, disclosed or not, and the landlord is itself in violation "
    "when its agent does. Small managers who lease their own units are exactly this agent.",
    "Condition: a fee (a charge for services: move-out cleaning, repainting service, lock change service, processing or "
    "administration) related to the rental is imposed or collected on or after 2025-06-11. Branch (a): the person imposing or "
    "collecting it is a landlord's agent for this landlord (listing agent, cooperating agent, landlord's subagent or broker's "
    "agent who found or obtained this tenant; not a dual agent), or an agent who published the listing with the landlord's "
    "authorization (presumed). Effect: the fee is barred whether or not disclosed; the landlord is in violation "
    "(20-699.21(b)); the tenant may sue for compensatory relief (20-699.24); the final statement and any balance may not "
    "carry it. Branch (b): the landlord itself, or a manager who is not such an agent, imposes it: NYC:FARE-moveout-service-fee "
    "applies (disclosure governs). Rent and compensation for damage the tenant caused are not fees in either branch "
    "(NYC:FARE-20-699.20-fee).",
    [ev("NYC_ADC_20-699.21.txt", "1. a landlord’s agent shall not impose any fee on, or collect any fee from, a tenant related to the rental of residential real property"),
     ev("NYC_ADC_20-699.21.txt", "b. A landlord is in violation of subdivision a of this section if:", "1. a landlord’s agent of such landlord violates such subdivision"),
     ev("NYC_ADC_20-699.20.txt", "Landlord’s agent. The term “landlord's agent” means a listing agent who acts alone", "to find or obtain a tenant for residential real property."),
     ev("NYC_ADC_20-699.24.txt", "Such court may order compensatory, injunctive and declaratory relief.")])

add("gap", "critical", "S19 domestic violence; S9 pursuing a balance; S21 credit reporting",
    ["NY:RPL-227-c(1)", "US:15USC1681s-2(a)(3)", "NY:ADJ-lease-balance-not-consumer-credit"],
    "No atom states New York's coerced-debt law (GBL art. 29-HHH, 604-aa to 604-dd, in force 2026-06-17). Unlike GBL "
    "art. 29-H, its 'coerced debt' needs no extension of credit, only a household-purpose transaction, so it reaches a "
    "residential lease balance; the landlord, its manager and any collector are 'creditors'.",
    "Condition: a former tenant who is a natural person tells the landlord, manager or collector that all or part of a lease "
    "balance is coerced debt (incurred through duress, coercion or undue influence by an intimate partner, family or household "
    "member, trafficker, parent/caretaker, or caregiver of an elderly or protected person). Branch (a): the tenant supplies a "
    "sworn statement and adequate documentation (police report, law-enforcement report, court order, or sworn statement of a "
    "qualified third party). Effect: within 10 business days stop collection activity on that debt; within 10 business days "
    "tell any consumer reporting agency the landlord reports to that the account is disputed; within 30 business days "
    "complete a review without contacting the alleged abuser, using only the contact details the tenant gave, and without "
    "disclosing the documents; if collection resumes, within 5 business days send the written determination and its "
    "good-faith basis. Branch (b): the tenant notifies without documents: send the statutory 604-bb(2)(a) notice text. In any "
    "suit, coerced debt is an affirmative defense; a tenant who proves it gets a declaration of non-liability, an injunction, "
    "dismissal of the landlord's claim, deletion of reported data and fees. The 14-day deposit statement is still sent: it is "
    "a statutory duty, not collection. Exclusion: a creditor who itself did the coercing is not a 'creditor'.",
    [ev("REVIEW4A_NY_GBL_604-AA_nysenate.txt", "3. \"Coerced debt\" means a debt arising out of a transaction primarily for personal, family or household purposes", "within the context of intimate relationships or relationships between family or household members"),
     ev("REVIEW4A_NY_GBL_604-BB_nysenate.txt", "1. Within ten business days of receipt of the following, a creditor shall cease collection activities", "is coerced debt."),
     ev("REVIEW4A_NY_GBL_604-BB_nysenate.txt", "3. (a) Within ten business days of receiving all the information required under subdivision one of this section", "notify such consumer reporting agency that the account is disputed."),
     ev("REVIEW4A_NY_GBL_604-CC_nysenate.txt", "4. In any action by a creditor against a debtor to collect a debt, it shall be an affirmative defense", "is coerced debt.")])

add("gap", "critical", "S16 death of tenant (who is paid; claims against the estate)",
    ["NY:RPL-236-a", "NY:RPL-236", "NY:GOL-7-103(1)-trust", "NY:ADJ-provide-address-branches", "NY:COMMONLAW-owner-death-agency"],
    "The rules cover the estate's options to end the lease (RPL 236, 236-a) and the owner's death, but no atom says who "
    "receives the statement and refund when the tenant dies, or how the landlord preserves its claim against the estate.",
    "Condition: the tenant (or the last surviving co-tenant) dies before the refund is paid or the balance collected. "
    "Payee: the refund belongs to the estate. Pay it to the executor or administrator on letters, or, for an estate of "
    "personal property of $50,000 or less, to a voluntary administrator on the court's short-form certificate, which "
    "discharges the landlord (SCPA 1301, 1305). SCPA 1310's pay-without-administration list (bank deposits, wages, public "
    "payments and similar) does not include a landlord's refund, so payment to a relative without letters or a certificate "
    "does not discharge the landlord. Statement: still due within 14 days of vacatur; send it to the fiduciary if one is known, "
    "otherwise to the last known address addressed to the tenant's estate (NY:ADJ-provide-address-branches), and hold the "
    "refund in trust (NY:GOL-7-103(1)-trust) until a fiduciary presents authority. Claims against the estate: present the "
    "claim to the fiduciary within 7 months of letters (after that the fiduciary is not chargeable for good-faith "
    "distributions, SCPA 1802); the limitation period against the estate is extended by 18 months after death (CPLR 210(b)); "
    "the estate's own deposit claim may be brought within one year after death if not yet expired (CPLR 210(a)).",
    [ev("REVIEW4A_NY_SCPA_1301_nysenate.txt", "A small estate is the estate of a domiciliary or a non-domiciliary", "$50,000 or less"),
     ev("REVIEW4A_NY_SCPA_1305_nysenate.txt", "The delivery by a voluntary administrator to a debtor", "shall constitute a complete release and discharge"),
     ev("REVIEW4A_NY_SCPA_1310_nysenate.txt", "(a) \"Debt\" means (i) money or securities payable on account of a deposit in a bank", "branch of a foreign banking corporation"),
     ev("REVIEW4A_NY_SCPA_1802_nysenate.txt", "If any claim is not presented within 7 months from the date of issue of letters, the fiduciary shall not be chargeable", "before such claim was presented."),
     ev("REVIEW4A_NY_CPLR_210_nysenate.txt", "(b) Death of person liable.", "against his executor or administrator.")])

add("gap", "critical", "S11 limitations (tolling and extension)",
    ["NY:CPLR-213(2)", "NY:CPLR-214-i", "US:11USC362(a)(6)", "US:50USC3911(1)-(2)"],
    "The limitation atoms state the six-year and three-year periods but no tolling or extension: military service, the "
    "debtor's bankruptcy, the debtor's death, or a written acknowledgment. Each moves the last day to sue.",
    "Add to every limitation computation for a claim by or against a former tenant: (1) the tenant's period of military "
    "service is excluded, for claims by or against the servicemember, heirs or representatives (50 USC 3936(a); Military Law "
    "308 to the same effect); (2) if the tenant filed bankruptcy before the period ran, the period ends no earlier than 30 days "
    "after notice that the stay (or the chapter 13 co-debtor stay) ended (11 USC 108(c)); (3) 18 months after the tenant's "
    "death are excluded (CPLR 210(b)); (4) for the six-year contract period, a written acknowledgment or promise signed by the "
    "tenant restarts it and a part payment keeps its common-law effect (GOL 17-101); for a claim that is a consumer credit "
    "transaction CPLR 214-i bars revival, and a lease balance is not one (NY:ADJ-lease-balance-not-consumer-credit).",
    [ev("REVIEW4A_US_50USC_3936_uscode.txt", "The period of a servicemember's military service may not be included", "heirs, executors, administrators, or assigns."),
     ev("REVIEW4A_US_11USC_108_uscode.txt", "(c) Except as provided in section 524 of this title", "as the case may be, with respect to such claim."),
     ev("REVIEW4A_NY_CPLR_210_nysenate.txt", "(b) Death of person liable.", "against his executor or administrator."),
     ev("REVIEW4A_NY_GOL_17-101_nysenate.txt", "An acknowledgment or promise contained in a writing signed", "does not alter the effect of a payment of principal or interest.")])

add("gap", "critical", "S8 consequences of a miss; S11 limitations (landlord's exposure window)",
    ["NY:GOL-7-108(1-a)(g)", "NY:GOL-7-108(1-a)(e)-forfeiture", "NY:CPLR-213(2)"],
    "No atom states how long a former tenant may sue the landlord over the deposit. The punitive damages in 7-108(1-a)(g) "
    "and a recovery that exists only because of the (1-a)(e) forfeiture are liabilities created by statute (CPLR 214(2), "
    "three years); a claim for a deposit wrongly kept at common law is contract/trust (six years).",
    "Condition: a former tenant's claim concerning the deposit. Branch (a): punitive damages for a willful violation, or "
    "recovery of amounts the landlord could have kept at common law but lost only by the 14-day forfeiture: three years from "
    "accrual (CPLR 214(2); Gaidon: 214(2) governs where liability would not exist but for the statute). Branch (b): return of a "
    "deposit kept without a lawful basis (no rent owed, no tenant damage, wear and tear), or actual damages for it: six years "
    "(CPLR 213(1), (2)), the claim existing at common law under the 7-103 trust. Accrual: the day after the 14-day deadline "
    "passes. Tolling per R4A-04. The operator keeps the settlement file at least six years after vacatur.",
    [ev("REVIEW4A_NY_CPLR_214_nysenate.txt", "2\\. an action to recover upon a liability, penalty or forfeiture", "215;"),
     ev("REVIEW4A_NY_CASE_Gaidon_v_GuardianLife_2001_CoA.txt", "CPLR 214 (2) does not automatically apply", "recognized or implemented by statute")])

add("gap", "critical", "S15 bankruptcy (who may be pursued)",
    ["US:11USC362(a)(6)", "US:11USC524(a)(2)", "US:11USC542-refund-payee"],
    "No atom states the chapter 13 co-debtor stay. When one tenant files chapter 13, the landlord may not collect the lease "
    "balance (a consumer debt) from a co-tenant or guarantor who is liable with the debtor.",
    "Condition: a tenant has a chapter 13 case pending (order for relief entered) and another individual is liable on the same "
    "lease balance or secured it (co-tenant, individual guarantor). Effect: the landlord, its manager and collectors may not "
    "act or sue to collect any part of the balance from that individual until the case is closed, dismissed or converted to "
    "chapter 7 or 11, unless the court grants relief (e.g., the co-debtor received the consideration, the plan does not pay the "
    "claim, or the landlord would be irreparably harmed). Exception: an individual who became liable in the ordinary course of "
    "its business (a commercial guarantor) is not protected. Chapter 7 has no co-debtor stay. Limitation against the co-debtor "
    "runs until 30 days after notice the stay ended (11 USC 108(c)).",
    [ev("REVIEW4A_US_11USC_1301_uscode.txt", "(a) Except as provided in subsections (b) and (c) of this section, after the order for relief under this chapter", "converted to a case under chapter 7 or 11 of this title.")])

add("gap", "critical", "S15 bankruptcy (amount of the landlord's claim)",
    ["US:11USC542-refund-payee", "NY:RPL-227-e"],
    "No atom states the cap on a lessor's claim for lease-termination damages in the tenant's bankruptcy.",
    "Condition: the landlord files a proof of claim in a former tenant's bankruptcy for damages from termination of the lease "
    "(future rent). Effect: the allowed claim is capped at the rent reserved, without acceleration, for the greater of one year "
    "or 15% (not over three years) of the remaining term, counted from the earlier of the petition date and the date the tenant "
    "surrendered or the landlord repossessed, plus unpaid rent due on that earlier date. The claim is further reduced by "
    "mitigation under RPL 227-e and by any deposit applied after stay relief.",
    [ev("REVIEW4A_US_11USC_502_uscode.txt", "(6) if such claim is the claim of a lessor for damages resulting from the termination of a lease of real property", "any unpaid rent due under such lease, without acceleration, on the earlier of such dates;")])

add("gap", "critical", "S17 military service (rate on the balance)",
    ["NY:ADJ-lease-interest-on-rent", "NY:RPL-238-a(2)", "US:50USC3911(1)-(2)"],
    "No atom states the 6% cap on interest and fees for obligations a servicemember incurred before entering service.",
    "Condition: the tenant (alone or jointly with a spouse) signed the lease before entering military service, the lease makes "
    "the balance bear interest or late fees or other charges above 6% a year, and the tenant gives written notice with the "
    "orders (or the landlord confirms service through the DMDC) no later than 180 days after release. Effect: during the "
    "period of service the balance may not bear interest above 6% a year, 'interest' including service charges, fees and other "
    "charges; the excess is forgiven, not deferred; the landlord may obtain relief only by court order showing the tenant's "
    "ability to pay was not materially affected. Military Law 323-a imposes the same cap for state and federal active duty.",
    [ev("REVIEW4A_US_50USC_3937_uscode.txt", "An obligation or liability bearing interest at a rate in excess of 6 percent per year", "in the case of any other obligation or liability."),
     ev("REVIEW4A_US_50USC_3937_uscode.txt", "The term \"interest\" includes service charges, renewal charges, fees, or any other charges", "with respect to an obligation or liability."),
     ev("REVIEW4A_NY_MIL_323-A_nysenate.txt", "As used in this section the term \"interest\" includes", "with respect to such obligation or liability.")])

add("partial", "critical", "S2 when rent stops (fixed-term lease ended by the parties' conduct)",
    ["NY:COMMONLAW-NYC-monthly-tenant-surrender", "NYC:CASE-Pezzo-surrender", "NY:RPL-227-e"],
    "Surrender is covered for monthly tenancies and for keys kept past expiry, and RPL 227-e covers re-letting. No atom "
    "states the Court of Appeals rule on surrender by operation of law, which ends a fixed-term lease (and the rent) mid-term "
    "when both parties act inconsistently with its continuance, e.g. the landlord takes back possession for its own use or "
    "accepts the keys and treats the unit as its own.",
    "Condition: a tenant with a fixed term leaves early and the landlord's conduct, together with the tenant's, is so "
    "inconsistent with the landlord-tenant relationship that it shows intent to treat the lease as ended (for example: the "
    "landlord accepts the keys and occupies, renovates or combines the unit for its own account, or releases the tenant). "
    "Effect: the lease ends on that date and rent stops; the landlord recovers only rent accrued before it and proven damages. "
    "Standard, decided on all the facts. Mere acceptance of keys for re-letting on the tenant's account, or re-letting under "
    "227-e, is not surrender by operation of law (227-e governs that branch).",
    [ev("REVIEW4A_NY_CASE_Riverside_v_KMGA_1986_CoA.txt", "A surrender by operation of law occurs when the parties to a lease both do some act so inconsistent", "intent to deem the lease terminated"),
     ev("REVIEW4A_NY_CASE_Riverside_v_KMGA_1986_CoA.txt", "As distinguished from an express surrender, a surrender by operation of law is inferred from the conduct of the parties", "is a determination to be made on the facts.")])

# ============================ MAJOR ============================
add("partial", "major", "S13 collection conduct (NYC)",
    ["NY:GBL-601(2)", "NY:GBL-601(9)", "NY:ADJ-lease-balance-not-consumer-credit", "NYC:RCNY6-5-77(e)(1)", "NYC:RCNY6-5-76-debt-collector"],
    "The walk defers GBL 601 as deciding nothing because art. 29-H does not reach a lease balance. That is right for the "
    "state statute, but the current 6 RCNY 5-77 incorporates GBL 601's conduct into the city rule: (d)(17) makes conduct "
    "proscribed by GBL 601(1), (3), (5), (7), (8) or (9) deceptive, and (e)(8) makes conduct prohibited by 601(2) or (4) "
    "unconscionable. 5-77 reaches a landlord's own staff collecting NYC former-tenant balances. No atom states this.",
    "Condition: a debt collector under 6 RCNY 5-76 (including the landlord's or manager's staff who regularly collect) collects "
    "a NYC former tenant's balance after debt collection procedures begin (a final statement demanding the balance starts "
    "them). Effect: it may not (601(1)) pose as law enforcement or a government agency; (601(2)) knowingly collect or assert "
    "a collection fee, attorney's fee, court cost or expense not justly due and legally chargeable; (601(3)) disclose credit "
    "information it knows or should know is false; (601(4)) tell the tenant's employer about the claim before final judgment; "
    "(601(5)) disclose a debt it knows is disputed without saying so; (601(7)) threaten action it does not in fact take in the "
    "usual course; (601(8)) claim or threaten to enforce a right it knows or should know does not exist; (601(9)) use a "
    "communication that looks like legal process or like it comes from a government body or an attorney when it does not. "
    "Each is a DCWP violation charged to the employer (NYC:RCNY6-5-77(g)).",
    [ev("NYC_RCNY6_5-77.txt", "(17) any conduct proscribed by New York General Business Law §§ 601(1), (3), (5), (7), (8), or (9);"),
     ev("NYC_RCNY6_5-77.txt", "(8) engaging in any conduct prohibited by New York General Business Law §§ 601(2) or (4); or")])

add("gap", "major", "S21 credit reporting (NYC, from 2027-01-01)",
    ["NYC:SHIELD-5-76-debt-collector", "NYC:SHIELD-operative-date", "US:12CFR1006.30(a)"],
    "The SHIELD atoms omit new 6 RCNY 5-77(e)(10): before furnishing a debt to a consumer reporting agency, a debt collector "
    "(which from 2027 includes a landlord that regularly collects its own balances) must send notice and wait 14 days.",
    "Condition: from 2027-01-01, a landlord, manager or collector that is a 'debt collector' under the SHIELD definition "
    "intends to report a NYC former tenant's balance to a consumer reporting agency. Effect: first send, in at least one "
    "medium used to collect and also by U.S. mail, a clear notice that the debt will be reported; wait 14 consecutive days; "
    "monitor for undeliverability notices and, if one arrives, do not report until the notice is re-sent properly. Exemption: "
    "furnishers subject to FCRA 623(a)(7) (financial institutions), which does not include a landlord.",
    [ev("NYC_DCWP_SHIELD_NOA_2026.txt", "(10) furnishing to a consumer reporting agency, as defined in section 603(f)", "has waited 14 consecutive days after sending such notice.")])

add("gap", "major", "S13 collection letters (balance that grows)",
    ["US:15USC1692e(2)(A)", "US:12CFR1006.34(c)", "NY:ADJ-lease-interest-on-rent"],
    "No atom states the controlling Second Circuit rule that a collection notice stating a current balance must disclose "
    "that the balance may increase when interest or fees are accruing.",
    "Condition: an FDCPA debt collector (a collector, a law firm, or a manager collecting a balance obtained after default) "
    "states a former tenant's balance while interest or fees accrue on it (lease interest, statutory prejudgment interest "
    "being claimed, late fees). Effect: the notice must say the balance may increase due to interest and fees; otherwise it is "
    "misleading under 1692e. If nothing accrues, no disclosure is needed.",
    [ev("REVIEW4A_US_CASE_Avila_v_Riexinger_2016_2dCir.txt", "We hold that Section 1692e of the FDCPA requires debt", "interest and fees.")])

add("gap", "major", "S10 procedure before judgment",
    ["NY:CPLR-3215(g)(3)", "US:50USC3931(b)(1)"],
    "The default-judgment atoms cover the additional mailing and the SCRA affidavit, not CPLR 3215(j): a clerk's default "
    "judgment needs an affidavit that the limitation period has not expired.",
    "Condition: the landlord or its collector asks the clerk for a default judgment on a former tenant's balance. Effect: "
    "attach an affidavit by the plaintiff or its attorney that, after reasonable inquiry, the plaintiff believes the "
    "limitation period has not expired (using the OCA form); without it the clerk cannot enter judgment.",
    [ev("REVIEW4A_NY_CPLR_3215_nysenate.txt", "(j) Affidavit. A request for a default judgment entered by the clerk", "the statute of limitations has not expired.")])

add("gap", "major", "S5 charges (what the lease can prove)",
    ["NY:ADJ-lease-break-charge", "NY:RPL-238-a(2)", "NY:ADJ-lease-interest-on-rent"],
    "No atom states CPLR 4544: lease text in print under 8 points (5.5 for upper case) cannot be received in evidence for the "
    "landlord who prepared it, so a charge resting only on that clause (late fee, lease-break fee, interest, fee clause) cannot "
    "be proved.",
    "Condition: a charge on the final account rests on a lease clause printed in type smaller than 8 points (5.5 for upper "
    "case) or not clear and legible, in a lease the landlord or its agent printed or prepared. Effect: the clause cannot be "
    "put in evidence by the landlord, so the charge is not kept from the deposit and is not pursued; the tenant may still rely "
    "on it. Waiver void.",
    [ev("REVIEW4A_NY_CPLR_4544_nysenate.txt", "The portion of any printed contract or agreement involving a consumer transaction or a lease for space to be occupied for residential purposes", "who caused said agreement or contract to be printed or prepared.")])

add("gap", "major", "S4 custody of the deposit by a licensed managing agent",
    ["NY:GOL-7-103(1)-trust", "NY:HANDOFF-broker-config-collects-rent", "NY:RPL-440(1)-rent-collection"],
    "The broker-licence configuration atoms do not state the DOS escrow rule for a licensed broker who holds tenants' "
    "deposits for the owner.",
    "Condition: a licensed real estate broker (the managing agent, or Handoff in its broker configuration) receives or holds a "
    "tenant's deposit or other money of its principal. Effect: it may not commingle that money with its own and must keep it in "
    "a separate special bank account used only for such funds; a breach is a licensing violation in addition to the 7-103 trust "
    "breach (which forfeits use of the deposit, NY:CASE-Paterno-commingling-forfeiture).",
    [ev("REVIEW4A_NY_19NYCRR_175.1_LII.txt", "A real estate broker shall not commingle the money or other", "special bank account")])

add("gap", "major", "S1 facts fixed at move-in; S5 credits",
    ["NY:RPL-238-a(2)", "NY:RPL-238-a(3)", "NYC:FARE-20-699.22(b)"],
    "RPL 238-a(1) has no atom: except background and credit checks (actual cost or $20, whichever is less), no payment, fee or "
    "charge may be demanded before or at the beginning of the tenancy. A move-in, amenity or application fee still on the "
    "ledger cannot be carried into the final account, and one paid is recoverable by the tenant.",
    "Condition: the ledger shows a fee or charge demanded before or at the start of the tenancy other than the deposit, the "
    "first rent and a background/credit check within the cap. Effect: do not charge it on the final account or keep it from the "
    "deposit; if the tenant paid it, it is a tenant claim that can be offset against any balance. Background/credit fees over "
    "the lesser of actual cost or $20, or charged without giving the tenant a copy of the check and receipt, are the same.",
    [ev("NY_RPL_238-A.txt", "or demand any other payment, fee or charge before or at the beginning of the tenancy", "credit checks as provided by paragraph (b) of this subdivision")])

add("gap", "major", "S9 pursuing a guarantor",
    ["US:15USC1692a(3)", "NY:RPL-236-a"],
    "No atom states when a guarantor of a residential lease may be pursued for the former tenant's balance.",
    "Condition: the landlord seeks the balance from a person other than the tenant who promised to answer for it. Effect: only "
    "if the guaranty is in a writing signed by the guarantor (GOL 5-701(a)(2)); an oral guaranty is void. The guarantor is a "
    "consumer for FDCPA and city collection rules when the guaranty was personal. The chapter 13 co-debtor stay protects an "
    "individual guarantor (R4A-06).",
    [ev("REVIEW4A_NY_GOL_5-701_nysenate.txt", "2\\. Is a special promise to answer for the debt, default or miscarriage", "of another person;")])

add("gap", "major", "S22 anti-discrimination binding charges and settlement",
    ["US:42USC3604(f)(3)(A)", "US:42USC3604(f)(3)(B)-animal-fees", "NY:RPL-227-c(1)"],
    "No atom states the general anti-discrimination rules that bind terms of the tenancy, which include deposit handling, "
    "deductions and collection: the FHA terms-and-conditions rule, NY Executive Law 296(5)(a)(2), NYC Admin Code "
    "8-107(5)(a)(1)(b) (including lawful source of income, which covers vouchers), and RPL 227-d (domestic-violence status).",
    "Condition: any settlement decision (what is deducted, how strictly damage is assessed, whether a balance is pursued or "
    "reported). Effect: apply the same standard to every tenant; do not vary it because of race, creed, color, national origin, "
    "citizenship or immigration status, gender, age, disability, sexual orientation, marital or partnership status, military or "
    "uniformed service, height, weight, familial status or children, domestic-violence victim status, or lawful source of "
    "income (a voucher or other assistance, whether paid to the landlord or the tenant). Exemption for the NYC and state housing "
    "provisions: owner-occupied two-family buildings not publicly advertised, and owner-occupied rooms. Violations carry "
    "damages and penalties before the city and state commissions and courts.",
    [ev("REVIEW4A_US_24CFR_100.65_ecfr.txt", "(1) Using different provisions in leases or contracts of sale, such as those relating to rental charges, security deposits", "because of race, color, religion, sex, handicap, familial status, or national origin."),
     ev("REVIEW4A_NY_EXEC_296_nysenate.txt", "(2) To discriminate against any person because of race, creed, color, national origin, citizenship or immigration status", "in the furnishing of facilities or services in connection therewith."),
     ev("REVIEW4A_NYC_ADC_8-107.txt", "(b) To discriminate against any such person or persons in the terms, conditions or privileges of the sale, rental or lease", "in connection therewith; or"),
     ev("REVIEW4A_NYC_ADC_8-102.txt", "Lawful source of income. The term \"lawful source of income\" includes", "paid or attributed directly to a landlord."),
     ev("REVIEW4A_NY_RPL_227-D_nysenate.txt", "(a) No person, firm or corporation owning or managing any building used for dwelling purposes", "(2) discriminate in the terms, conditions, or privileges of any such rental")])

add("gap", "major", "S20 tax and information reporting (deposit interest)",
    ["NY:GOL-7-103(2)-interest-owed", "NY:GOL-7-103(2-a)", "NY:GOL-7-103(2-b)"],
    "No atom states the information-return duty when the landlord passes deposit interest to the tenant.",
    "Condition: the deposit is in an interest-bearing account (required in buildings of six or more units), the bank pays the "
    "interest to the landlord, and the landlord pays or credits $10 or more of it to the tenant in a calendar year (annually, "
    "or at termination under 7-103(2-b)). Effect: the landlord received it as nominee and must file an information return "
    "(Form 1099-INT) and furnish the tenant a statement, which requires the tenant's name, address and TIN. Below $10 a year, "
    "no return.",
    [ev("REVIEW4A_US_26USC_6049_uscode.txt", "(2) who receives payments of interest (as so defined) as a nominee", "the name and address of the person to whom paid.")])

add("gap", "major", "S21 data at move-out (NYC smart-access buildings)",
    [],
    "No atom states the NYC Tenant Data Privacy Act duty triggered by the tenant's move-out.",
    "Condition: the unit is in a class A multiple dwelling that uses a smart access system (key fob, app, biometric or other "
    "electronic entry). Effect: within 90 days after the tenant permanently vacates, remove the tenant's reference data from "
    "the system (or anonymize it where removal would disable the system); authentication data must in any case be destroyed "
    "within 90 days of collection. Private right of action and civil penalties apply.",
    [ev("REVIEW4A_NYC_ADC_26-3002.txt", "c. Reference data for any tenant who has permanently vacated a smart access building", "no later than 90 days after such tenant has permanently vacated such building.")])

add("gap", "major", "S13 licensed collection-agency configuration",
    ["NY:HANDOFF-broker-config-collection-agency", "NYC:ADC-20-493.1(b)", "NYC:ADC-20-490"],
    "For the configuration in which the collector is a DCWP-licensed agency, the atoms cover 20-493.1(b) but not the rules "
    "that say what the written payment-plan confirmation must contain and what records must be kept.",
    "Condition: a DCWP-licensed debt collection agency agrees a payment schedule or settlement with a former tenant, or collects "
    "at all. Effect: the written confirmation must name the originating creditor, the agency, the employee (or supervisor), "
    "the consumer, the agreement date, each payment's amount and due date, where to pay, all other terms and the conditions for "
    "satisfying the balance (6 RCNY 2-192); the agency keeps a separate file for each debt with the records in 6 RCNY 2-193.",
    [ev("REVIEW4A_NYC_RCNY6_2-192.txt", "(a) The written confirmation of the debt payment schedule or settlement agreement", "the conditions for satisfying the outstanding balance."),
     ev("REVIEW4A_NYC_RCNY6_2-193.txt", "2-193 Records to be Maintained by Debt Collection Agency.", "a separate file for each debt")])

add("gap", "major", "S3 who may collect after foreclosure",
    ["NY:GOL-7-105(1)", "NY:RPL-223", "NY:CPLR-6401-foreclosure-receiver"],
    "The rules cover the deposit's transfer on foreclosure and receivers, but not the successor's duties toward a market-rate "
    "tenant under RPAPL 1305, which decide who may collect rent and from when.",
    "Condition: the building is sold in foreclosure (or transferred during it) while a market-rate tenant is in occupancy. "
    "Effect: the successor takes subject to the tenant's right to stay for the rest of the lease (or 90 days after notice, "
    "whichever is greater) on the same terms, and must give written notice of that right and of its name and address; until "
    "the tenant has that notice, rent paid to the former landlord's representative is not a default. The federal Protecting "
    "Tenants at Foreclosure Act gives a 90-day floor where the mortgage was federally related; the longer state protection "
    "controls.",
    [ev("REVIEW4A_NY_RPAPL_1305_nysenate.txt", "a successor in interest of residential real property shall provide written notice to all tenants", "(b) of the name and address of the new owner."),
     ev("REVIEW4A_US_12USC_5220_uscode_PTFA.txt", "the provision, by such successor in interest of a notice to vacate", "at least 90 days before the effective date of such notice")])

add("gap", "major", "S7 payment fees (pending bill)",
    ["NY:RPL-235-g"],
    "S947/A3121 (amending RPL 235-g) passed the Senate on 2026-03-18 and the Assembly on 2026-05-13 and has not been "
    "delivered to the Governor. No dated future atom records it.",
    "Pending, effective immediately upon becoming law: a landlord may not charge any fee for rent paid by ACH, and must offer "
    "at least one rent-payment method with no landlord fee (e.g., cash or personal check); any waiver is void. Until then "
    "NY:RPL-235-g governs. Any convenience fee on a former tenant's balance paid by ACH after enactment is barred.",
    [ev("REVIEW4A_NY_S00947_Assembly_2025-26.txt", "2. A landlord shall not assess any fee or other charge for the use of", "an automated clearing house payment for the payment of rent."),
     ev("REVIEW4A_NY_S00947_Assembly_2025-26.txt", "03/18/2026PASSED SENATE", "05/13/2026passed assembly")])

add("gap", "major", "S15 bankruptcy (lease still running when a chapter 7 is filed)",
    ["US:11USC362(a)(6)", "US:11USC542-refund-payee"],
    "No atom states the deemed rejection of a residential lease in chapter 7, which fixes when post-petition rent becomes a "
    "pre-petition claim.",
    "Condition: a tenant files chapter 7 while the lease is unexpired. Effect: unless the trustee assumes it within 60 days of "
    "the order for relief (or a court-extended period), the lease is deemed rejected; rejection is a breach as of immediately "
    "before the petition, so the landlord's damages are a pre-petition unsecured claim (capped under R4A-07) and are "
    "dischargeable; the tenant's continued occupancy after the petition is claimed as use and occupancy.",
    [ev("REVIEW4A_US_11USC_365_uscode.txt", "(d)(1) In a case under chapter 7 of this title, if the trustee does not assume or reject an executory contract or unexpired lease of residential real property", "then such contract or lease is deemed rejected."),
     ev("REVIEW4A_US_11USC_365_uscode.txt", "the rejection of an executory contract or unexpired lease of the debtor constitutes a breach of such contract or lease-", "immediately before the date of the filing of the petition;")])

# ============================ MINOR ============================
add("gap", "minor", "S20 tax (owner income; write-off)", [],
    "No atom states the federal tax treatment the owner meets at settlement: kept deposit is income in the year kept; no "
    "cancellation-of-debt return is due on a write-off by a non-financial landlord.",
    "A refundable deposit is not income when received; the part kept is income in the year kept; a deposit to be applied as "
    "last month's rent is advance rent, income when received (IRS Pub. 527). Writing off a former tenant's balance creates no "
    "Form 1099-C duty, because 6050P applies only to financial entities and government agencies.",
    [ev("REVIEW4A_US_IRS_Pub527_2025.txt", "Don’t include a security deposit in your income when you receive it", "include the amount you keep in your income in that year."),
     ev("REVIEW4A_US_26USC_6050P_uscode.txt", "The term \"applicable entity\" means-", "an applicable financial entity.")])

add("gap", "minor", "S8 consequences (unpaid small-claims judgment)", [],
    "No atom states CCA 1812: a business that leaves small-claims judgments unpaid faces a treble-damages action.",
    "Condition: a tenant holds an unpaid NYC small-claims judgment against the landlord arising from its business, there are at "
    "least two other unpaid small-claims judgments from the same business, and the landlord does not pay within 30 days of "
    "notice. Effect: the tenant may sue for three times the judgment plus fees; inability to pay is the only defense.",
    [ev("REVIEW4A_NY_CCA_1812_nysenate.txt", "(b) Where each of the elements of subdivision (a) of this section are present", "together with reasonable counsel fees")])

add("gap", "minor", "S8 forum for the tenant's deposit claim", ["NY:CCA-1809(1)"],
    "No atom states that a tenant may sue a landlord in NYC small claims over a NYC tenancy regardless of where the landlord "
    "lives, up to $10,000.",
    "A former tenant's deposit claim up to $10,000 (exclusive of interest and costs) may be brought in NYC small claims when "
    "the property is in NYC, even if the landlord neither lives nor does business in NYC.",
    [ev("REVIEW4A_NY_CCA_1801_nysenate.txt", "or where", "situated within the city of New York.")])

add("partial", "minor", "S4 commingling (First Department authority)",
    ["NY:CASE-Paterno-commingling-forfeiture", "NY:CASE-Paterno-bank-notice-inference"],
    "The commingling forfeiture is grounded only on Second Department cases. The First Department holds the same (LeRoy v "
    "Sayers), and adds that the tenant's own lease breach is no defense; worth citing for New York and Bronx County.",
    "Commingling is a conversion: the tenant recovers the deposit at once, and the tenant's breach of the lease is no defense "
    "(1st Dept).",
    [ev("REVIEW4A_NY_CASE_LeRoy_v_Sayers_1995_1stDept.txt", "it has been uniformly held that a commingling constitutes a conversion", "immediate recovery of his deposit or advances.")])

add("partial", "minor", "S9 fee exposure when pursuing", ["NY:RPL-234"],
    "NY:RPL-234 states reciprocity but not its breadth under Graham Court: a clause giving the landlord fees for retaking "
    "possession after the tenant's default triggers the tenant's reciprocal right.",
    "A lease clause letting the landlord recover attorneys' fees incurred in retaking possession after the tenant's default "
    "is within RPL 234, so a tenant who defeats the landlord's claim (or wins its own claim for the landlord's breach) recovers "
    "reasonable fees.",
    [ev("REVIEW4A_NY_CASE_GrahamCourt_v_Taylor_2015_CoA.txt", "We hold that Real Property Law § 234, which imposes a covenant", "incurred in retaking possession.")])

add("gap", "minor", "S13 statements about family members", ["NY:GBL-601(2)"],
    "GBL 601-a is not in the files. It is not limited to 'consumer claims', so it reaches a lease balance.",
    "No landlord, manager or collection agency may represent that a family member must pay the tenant's debt contrary to the "
    "FDCPA, or misrepresent a family member's obligation (e.g., telling a parent or the estate's heirs they owe the balance).",
    [ev("REVIEW4A_NY_GBL_601-A_nysenate.txt", "No principal creditors and/or debt collection agencies shall make any representation", "obligation to pay such debts.")])

add("partial", "minor", "S14 unclaimed funds (reporting code)", ["NY:OSC-MS11-refunds-due"],
    "NY:OSC-MS11-refunds-due is right for an owner. A real-estate company holding deposits in escrow reports under TR04.",
    "Branch (a): the owner (or a non-broker manager) holds the unclaimed refund: MS11 Refunds Due, three years. Branch (b): a "
    "real-estate company (licensed managing agent) holds it in its escrow account: TR04 Escrow Accounts (held by real estate "
    "companies), three years. Same dormancy, different code.",
    [ev("NY_OSC_unclaimed_property_type_table.txt", "TR04 1315 Escrow Accounts (held by real estate companies) 3 years")])

add("gap", "minor", "S21 data security for refund data", [],
    "No atom states the SHIELD Act safeguard duty for the bank-account data collected to pay refunds electronically.",
    "Anyone holding a New York resident's private information (e.g., account number with access code for an ACH refund) must "
    "keep reasonable administrative, technical and physical safeguards, including secure disposal.",
    [ev("REVIEW4A_NY_GBL_899-BB_nysenate.txt", "reasonable safeguards to protect the security, confidentiality and integrity of the private information")])

add("gap", "minor", "S1 move-in disclosure (1-3 unit buildings)", ["NY:MDL-301(1)", "NY:ADJ-MDL-rent-bar-not-1-2-family"],
    "RPL 235-bb has no atom: owners of three or fewer rental units must disclose in bold whether any required certificate of "
    "occupancy is valid before the lease is signed. The statute states no remedy; it is evidence in a later dispute over "
    "rent for an unlawful unit.",
    "Condition: owner of 3 or fewer rental units. Effect: before signing, a bold notice whether a required CO is valid (or a copy "
    "of the CO); waiver void.",
    [ev("REVIEW4A_NY_RPL_235-BB_nysenate.txt", "Prior to executing a residential lease or rental agreement with a", "currently valid for the dwelling unit subject to the lease or rental")])

add("gap", "minor", "S10 non-military affidavit (state law)", ["US:50USC3931(b)(1)"],
    "Military Law 303(3) is not in the files. It removes any state-law non-military affidavit requirement except where federal "
    "law requires one; federal law (50 USC 3931) does, so the practical rule is unchanged.",
    "State law adds no non-military affidavit; the SCRA affidavit remains required for every default judgment.",
    [ev("REVIEW4A_NY_MIL_303_nysenate.txt", "3\\. Where a default judgment may properly be rendered", "where authorized by federal law.")])

# ============================ OVER-SCOPE ============================
OVER = [
    {"rule_ids": ["US:24CFR983.259(c)-(e)", "US:24CFR983.352(a)", "US:24CFR983.353(b)"], "severity": "minor",
     "why": "Project-based voucher rules. A PBV contract unit is project-based assistance, which the aperture for this review "
            "excludes and which the walk itself sends to the later subsidized-housing review; yet Step 5 cites these three as "
            "applying ('Project-based vouchers follow the same rules'). They decide nothing for a market-rate unit and "
            "should be listed as deferred with the other public/project-based rules."},
]

if __name__ == "__main__":
    universe = json.loads((HERE / "review4a_universe.json").read_text())
    newness = {}
    p = HERE / "ir4a_newness.json"
    if p.exists():
        newness = json.loads(p.read_text())
    for f in F:
        if f["id"] in newness:
            f["earlier_rounds"] = newness[f["id"]]
    out = {"review": "Independent Review 4A (completeness)", "date": "2026-09-29", "universe_count": len(universe),
           "findings": F, "over_scope": OVER}
    (HERE / "independent_review_4a.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    if ERR:
        print("EVIDENCE ERRORS:")
        print("\n".join(ERR))
    from collections import Counter
    print(len(F), "findings", Counter(f["severity"] for f in F), "over-scope", len(OVER), "errors", len(ERR))
