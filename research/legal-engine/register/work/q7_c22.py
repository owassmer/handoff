import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:Judiciary Law 460", N, "Bar examination and admission of attorneys; which counsel an entity owner must use is stated (NY:CPLR-321-JUD-495-appearance), and admission procedure adds no step."),
    D("NY:Judiciary Law 460-B", N, "Special arrangements for bar examinees; outside the chain."),
    D("NY:Judiciary Law 461", N, "Compensation of the Board of Law Examiners; outside the chain."),
    D("NY:Judiciary Law 462", N, "Board of Law Examiners' annual account; outside the chain."),
    D("NY:Judiciary Law 463", N, "Times and places of bar examinations; outside the chain."),
    D("NY:Judiciary Law 464", N, "Certification of successful bar candidates; outside the chain."),
    D("NY:Judiciary Law 465", N, "Bar examination fees and refunds; outside the chain."),
    D("NY:Judiciary Law 466", N, "Attorney's oath of office on admission; outside the chain."),
    D("NY:Judiciary Law 467", N, "Lists of newly admitted attorneys sent to the Court of Appeals; outside the chain."),
    D("NY:Judiciary Law 468", N, "Official register of attorneys kept by the Chief Administrator; a public record, not a step for the landlord or collector."),
    D("NY:Judiciary Law 468-A", N, "Biennial attorney registration and fee; binds attorneys, not the owner hiring one."),
    D("NY:Judiciary Law 468-B", N, "Lawyers' Fund for Client Protection reimburses losses from attorney dishonesty; a remedy against the attorney, not a step in the settlement."),
    D("NY:Judiciary Law 470", N, "Attorneys with a New York office may live in an adjoining state; outside the chain."),
    D("NY:Judiciary Law 471", N, "A judge's partner or clerk may not practice before the judge; outside the chain."),
    D("NY:Judiciary Law 472", N, "A surrogate's parent or child barred where the surrogate's partner is; outside the chain."),
    D("NY:Judiciary Law 473", N, "Court officers and sheriffs may not practice law while in office; outside the chain."),
    D("NY:Judiciary Law 474", N, "Attorney compensation is by agreement, with court control of contingency fees on infants' claims; whether the landlord may recover legal fees from the tenant is decided by the stated RPL 234 and 234-a rules."),
    D("NY:Judiciary Law 480", N, "Bars entering a hospital to obtain releases from injured patients within 15 days; personal-injury releases only."),
    D("NY:Judiciary Law 482", N, "Binds attorneys: an attorney may not employ a person to solicit legal business; the matching bars on Handoff or a manager soliciting for, or being paid for placing claims with, a collection attorney are proposed at NY:JUD-479-no-solicitation and NY:JUD-491-no-fee-sharing, so no further step changes."),
    D("NY:Judiciary Law 486-A", N, "Court clerks report attorneys' felony convictions; outside the chain."),
    D("NY:Judiciary Law 493", N, "Attorneys may not defend prosecutions their partners bring; criminal practice, outside the chain."),
    D("NY:Judiciary Law 494", N, "Attorneys may defend themselves notwithstanding 493; outside the chain."),
    D("NY:Judiciary Law 496", N, "Filing duties of legal-services organizations under Judiciary Law 495(7); outside the chain."),
    D("NY:Judiciary Law 498", N, "Bar association referral immunity and privilege; outside the chain."),
    D("NY:Judiciary Law 499", N, "Privilege and immunity for lawyer assistance committees; outside the chain."),
    D("NY:LLC Law 201", N, "An LLC may be formed for any lawful purpose; owning and leasing units is lawful, so no rule's reach changes."),
    D("NY:LLC Law 203", N, "Formation of an LLC by filing articles and its separate existence until cancellation; the owner entity's capacity rules (publication, foreign authority) are stated, and formation mechanics add no settlement step."),
    D("NY:LLC Law 204", "stated", "204(c) requires an LLC to do business in its filed name unless it has complied with GBL 130; the consequence of using another name on a lease or letter (no action until the assumed-name certificate is filed) is stated.", ["NY:GBL-130-assumed-name"]),
    D("NY:LLC Law 205", N, "Reservation of LLC names at the Department of State; a filing formality with no settlement step."),
    D("NY:LLC Law 207", N, "Who signs LLC articles and certificates; a filing formality with no settlement step."),
    D("NY:LLC Law 208", N, "Court-ordered execution of LLC certificates when a signer refuses; internal to the LLC."),
]
save(rows)
