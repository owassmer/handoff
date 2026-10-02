import sys
sys.path.insert(0, "register/work")
from q5_lib import add, nd

add("US:11 USC 301", "stated",
    "Makes the filing of a voluntary petition the order for relief, the anchor of the 70-day claim deadline and the 60-day chapter 7 lease-rejection period already stated in the existing rules.",
    atom_ids=["US:FRBP-3002(c)-claim-deadline", "US:11USC365(d)(1)-ch7-rejection"])
nd("US:11 USC 302", "Joint cases of spouses; the landlord's rules apply to each debtor the same way.")
nd("US:11 USC 305", "Court abstention by dismissal or suspension; the effect of a dismissal is proposed at 349 (US:11USC349-dismissal).")
nd("US:11 USC 308", "Reporting duties of a small-business debtor to the court (case administration).")
TA = "Trustee administration"
nd("US:11 USC 323", TA + ": the trustee represents the estate and may sue and be sued; who is paid the refund is stated in US:11USC542-refund-payee.")
nd("US:11 USC 325", TA + ": a vacancy in the trustee's office does not abate a pending action.")
nd("US:11 USC 326", TA + ": limits on trustee compensation.")
nd("US:11 USC 328", TA + ": limits on compensation of professionals employed by the estate.")
nd("US:11 USC 329", "Review of the debtor's payments to its own attorney; no effect on the landlord's conduct.")
nd("US:11 USC 331", TA + ": interim compensation of trustees and professionals.")
nd("US:11 USC 332", TA + ": consumer privacy ombudsman on sales of personal information by the estate.")
nd("US:11 USC 341", "The U.S. trustee convenes the meeting of creditors; its first scheduled date anchors the deadlines proposed at FRBP 4003, 4004 and 4007, and the section itself imposes no duty on a creditor.")
nd("US:11 USC 343", "The debtor submits to examination at the 341 meeting and creditors may question it; an optional step that changes no deadline, amount or payee in the chain.")
nd("US:11 USC 344", "Immunity for compelled testimony; no effect on the chain.")
nd("US:11 USC 346", "State and local tax treatment of the estate and debtor (income of the estate, carryovers); none of the chain's tax events.")
nd("US:11 USC 347", TA + ": the trustee stops payment on dividend checks unclaimed 90 days after final distribution and pays the funds into court, where the creditor may claim them; the landlord's claim and distribution rights are unchanged.")
nd("US:11 USC 350", "Closing and reopening of a case; the stay ends on closing (362(c)), and reopening for a dischargeability complaint is stated in US:FRBP4007-523c-deadline.")
nd("US:11 USC 351", "Disposal of patient records in health-care business cases; out of scope for this batch.")
nd("US:11 USC 361", "Forms of adequate protection for an interest in estate property; a landlord's stay-relief position on the deposit is stated in US:CASE-Strumpf-hold and US:11USC362(a)(7)-deposit-is-setoff.")
nd("US:11 USC 364", "The estate's post-petition borrowing and priming liens; no effect on the landlord's or manager's chain decisions.")
nd("US:11 USC 366", "Protects the debtor's utility service and lets a utility set off its own deposit; a residential landlord is not a utility, and apartment utilities billed by the landlord are rent charges governed by the stay and claim rules.")
