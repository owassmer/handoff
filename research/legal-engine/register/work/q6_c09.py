"""q6 chunk 9: 24 CFR part 5, VAWA (34 USC), 24 CFR part 982, 47 CFR 64.1201."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q6_lib import D, P, q, save, tf

HCV = "24 CFR part 982 (Section 8 Tenant-Based Assistance: Housing Choice Voucher Program)"
VAWA5 = "24 CFR part 5, subpart L (VAWA protections)"
t = lambda n: tf("US:24 CFR " + n)
f2005, f2007, f2009 = t("5.2005"), t("5.2007"), t("5.2009")
f12494 = tf("US:34 USC 12494")

r_v05 = P("US:24CFR5.2005-hcv-owner-limits", "24 CFR 5.2005(b)-(d); 982.310(h)(4); 982.551(e)", "landlord; managing agent (voucher owner)", "must not",
          "The market-rate unit is rented with a tenant-based Housing Choice Voucher and the tenant, or an affiliated "
          "individual, is or has been a victim of domestic violence, dating violence, sexual assault or stalking.",
          "The owner may not evict or end the tenancy on the basis or as a direct result of that status. An incident of "
          "actual or threatened violence is not a serious or repeated lease violation or good cause to end the victim's "
          "tenancy. The owner keeps its authority to comply with a court order on access to or possession of property, to "
          "evict for a violation not premised on the violence (applying no more demanding standard than to other "
          "tenants), and to evict where it shows an actual and imminent threat to other tenants or staff, and then only if "
          "no lesser measure would remove the threat. Charges for the perpetrator's acts follow US:34USC12491-VAWA.",
          f2005, q(f2005, "may not be denied admission to, denied assistance under, terminated from participation in, or evicted from the housing on the basis or as a direct result of the fact that the applicant or tenant is or has been a victim"),
          "major", "3.4", determinacy="MIXED", judgment_terms=["actual and imminent threat", "more demanding standard"],
          instrument=VAWA5, dependencies=["US:34USC12491-VAWA"],
          construction=[(f2005, q(f2005, "An incident of actual or threatened domestic violence, dating violence, sexual assault, or stalking shall not be construed as:")),
                        (f2005, q(f2005, "the covered housing provider must not subject the tenant, who is or has been a victim of domestic violence, dating violence, sexual assault, or stalking, or is affiliated with an individual who is or has been a victim"))],
          reasoning="5.2005(b)-(d) state the protections and their limits; 982.310(h)(4) makes the voucher owner's terminations "
                    "subject to them.")

r_v07 = P("US:24CFR5.2007-documentation-confidentiality", "24 CFR 5.2007(a)-(c)", "landlord; managing agent; Handoff (voucher owner and its agents)",
          "may / must",
          "A voucher tenant tells the owner or its agent that the tenant is a victim entitled to VAWA protections or "
          "remedies (for example to explain damage, an early departure, or a perpetrator's removal).",
          "The owner may, but need not, ask in writing for documentation; the tenant chooses among the HUD certification "
          "form, a professional's signed statement, a law-enforcement, court or agency record, or (at the owner's "
          "discretion) other evidence. If none is provided within 14 business days of the written request (extendable), "
          "the VAWA protections do not limit the owner's lease remedies. Conflicting claims allow a demand for third-party "
          "documentation within 30 days. All of it, including the fact of victim status, is kept in strict confidence: "
          "no access for staff or contractors (Handoff, a collector) unless the owner specifically authorizes it for a "
          "legal need, no entry into a shared database, and no disclosure (for example to a collector, credit bureau or "
          "prospective landlord) except with the tenant's written time-limited consent, for an eviction or termination "
          "hearing, or as other law requires.",
          f2007, q(f2007, "shall be maintained in strict confidence by the covered housing provider."),
          "major", "6.10", instrument=VAWA5, dependencies=["US:34USC12491-VAWA", "NY:RPL-227-c(5)(b)"],
          construction=[(f2007, q(f2007, "within 14 business days after the date that the tenant receives a request in writing for such documentation from the covered housing provider")),
                        (f2007, q(f2007, "The covered housing provider shall not enter confidential information described in paragraph (c) of this section into any shared database or disclose such information to any other entity or individual, except to the extent that the disclosure is:"))],
          reasoning="5.2007(a)-(b) set the documentation request and 14-business-day window; (c) the confidentiality duty and "
                    "its three exceptions.")

r_v09 = P("US:24CFR5.2009-bifurcation-remaining-tenant", "24 CFR 5.2009(a)-(b)", "landlord; managing agent (voucher owner)", "must",
          "The owner bifurcates the voucher lease to remove a household member who committed the violence, and the removed "
          "person was the eligible (voucher-holding) tenant, so the remaining tenants are not yet eligible.",
          "The bifurcation follows state and local eviction procedure. The remaining tenants get 90 calendar days from "
          "the bifurcation (extendable by the owner up to 60 more) to establish eligibility for the program or another "
          "covered program, or to find other housing, but not beyond the lease's expiration; the owner does not end their "
          "occupancy for lack of eligibility during that period. Rent for that period follows the lease and the PHA's "
          "determination of assistance (US:24CFR982.451(b)(4)).",
          f2009, q(f2009, "the covered housing provider shall provide to any remaining tenant or tenants that were not already eligible a period of 90 calendar days from the date of bifurcation of the lease to:"),
          "major", "3.4", instrument=VAWA5, dependencies=["US:34USC12491-VAWA", "US:24CFR982.451(b)(4)"],
          construction=[(f2009, q(f2009, "The 90-day calendar period also will not apply beyond the expiration of a lease, unless this is permitted by program regulations.")),
                        (f2009, q(f2009, "may extend the 90-calendar-day period in paragraph (b)(2) of this section up to an additional 60 calendar days"))],
          reasoning="5.2009(a) authorizes bifurcation under state procedure; (b)(2) sets the 90-day period and its limits.")

r_ret = P("US:34USC12494-no-retaliation", "34 U.S.C. 12494", "landlord; managing agent; Handoff; collector (voucher owner and its agents)", "must not",
          "The unit is rented with a tenant-based voucher, and the tenant or another person has used, claimed or helped "
          "someone use VAWA housing protections, or opposed or reported a violation.",
          "The owner or manager may not discriminate against, coerce, intimidate, threaten, interfere with or retaliate "
          "against that person for it (for example by adding charges, pressing collection or reporting because the "
          "tenant invoked VAWA). HUD and the Attorney General enforce it with the rights and remedies of the Fair Housing "
          "Act (US:42USC3613-private-action, US:42USC3610-3612-hud-enforcement).",
          f12494, q(f12494, "No public housing agency or owner or manager of housing assisted under a covered housing program shall coerce, intimidate, threaten, or interfere with, or retaliate against, any person"),
          "major", "5.10", determinacy="MIXED", judgment_terms=["retaliate"],
          instrument="Violence Against Women Act housing provisions, 34 U.S.C. 12491-12496",
          dependencies=["US:34USC12491-VAWA", "US:42USC3613-private-action"],
          construction=[(f12494, q(f12494, "shall implement and enforce this subpart consistent with, and in a manner that provides, the rights and remedies provided for in title VIII of the Civil Rights Act of 1968"))],
          reasoning="12494(a)-(b) bar retaliation and coercion by owners and managers of covered housing; (c) imports the Fair "
                    "Housing Act remedies.")

f308, f309, f310, f312, f403, f453, f454, f455, f456, f510, f5 = map(t, ["982.308", "982.309", "982.310", "982.312", "982.403",
                                                                      "982.453", "982.454", "982.455", "982.456", "982.510", "982.5"])
r308 = P("US:24CFR982.308-tenancy-addendum", "24 CFR 982.308(f)(2), (g)(1)", "landlord; managing agent (voucher owner)", "must",
         "Settling a tenancy assisted by a tenant-based voucher, where the lease and the HUD tenancy addendum differ (for "
         "example on the deposit, charges or termination).",
         "The tenancy addendum prevails over any other lease provision, and the tenant may enforce it against the owner; "
         "changes the owner and tenant agreed must be in writing with a copy given to the PHA at once. The settlement "
         "applies the addendum's terms first.",
         f308, q(f308, "The tenant shall have the right to enforce the tenancy addendum against the owner, and the terms of the tenancy addendum shall prevail over any other provisions of the lease."),
         "major", "5.7", instrument=HCV, dependencies=["US:24CFR982.313(c)"])

r309 = P("US:24CFR982.309-term-rent-freeze", "24 CFR 982.309(a)(3), (b)(2), (c)", "landlord; managing agent (voucher owner)", "must not",
         "Settling a voucher tenancy whose rent to owner was raised during the initial lease term, or ending when the lease "
         "is terminated by either side.",
         "Rent to owner may not be raised during the initial term, so any increase billed in that term is not owed and is "
         "refunded or credited. The HAP contract ends when the lease is terminated by the owner or tenant, or when the PHA "
         "ends it or the family's assistance. The family's duties to copy the PHA on its termination notice and to "
         "notify the PHA and owner before moving out are program obligations enforced by the PHA; they do not add to "
         "what the owner may charge.",
         f309, q(f309, "During the initial term of the lease, the owner may not raise the rent to owner."),
         "major", "5.7", instrument=HCV, dependencies=["US:24CFR982.311(d)(1)"],
         construction=[(f309, q(f309, "The lease is terminated by the owner or the tenant;"))],
         reasoning="982.309(a)(3) freezes rent in the initial term; (b)(2) ties the HAP contract to the lease.")

r310 = P("US:24CFR982.310-owner-termination", "24 CFR 982.310(a)-(f); 982.5", "landlord; managing agent (voucher owner)", "may only",
         "The owner of a unit rented with a tenant-based voucher wants to end the tenancy during the lease term.",
         "Only for a serious or repeated lease violation (including failure to pay the tenant's rent or other amounts due "
         "under the lease), a violation of law tied to occupancy, or other good cause; during the initial term, 'other "
         "good cause' must rest on something the family did or failed to do (not a refused renewal offer, owner use, sale, "
         "renovation or a higher rent). The PHA's failure to pay its share is never a lease violation or ground to "
         "terminate. The owner must give the tenant written notice of the grounds at or before starting the eviction "
         "action (the tenancy does not end before it), give the PHA a copy of any eviction notice, and evict only by court "
         "action. Every notice under part 982 is written.",
         f310, q(f310, "During the term of the lease, the owner may not terminate the tenancy except on the following grounds:"),
         "major", "3.4", determinacy="MIXED", judgment_terms=["serious or repeated violation", "other good cause"],
         instrument=HCV, dependencies=["US:24CFR982.451(b)(4)", "US:24CFR5.2005-hcv-owner-limits"],
         construction=[(f310, q(f310, "The tenancy does not terminate before the owner has given this notice, and the notice must be given at or before commencement of the eviction action.")),
                       (f310, q(f310, "The owner may only evict the tenant from the unit by instituting a court action.")),
                       (f5, q(f5, "Where part 982 requires any notice to be given by the PHA, the family or the owner, the notice must be in writing."))],
         reasoning="982.310(a)-(f) limit grounds, require the notice of grounds and PHA copy, and require court action; 982.5 "
                   "requires writing.")

r312 = P("US:24CFR982.312-absence", "24 CFR 982.312(a)-(c)", "landlord; managing agent (voucher owner)", "must",
         "No member of a voucher family has resided in the unit for longer than the PHA's permitted absence, and in any "
         "case more than 180 consecutive days.",
         "The HAP payments, the HAP contract and the assisted lease terminate at that point, which fixes the end of the "
         "assisted tenancy for the settlement; the owner must repay the PHA any housing assistance payment received for "
         "the period after the termination, and that repayment is never charged to the family.",
         f312, q(f312, "Housing assistance payments terminate if the family is absent for longer than the maximum period permitted. The term of the HAP contract and assisted lease also terminate."),
         "critical", "3.4", instrument=HCV, dependencies=["US:24CFR982.451(b)(4)", "US:24CFR982.311(d)(1)"],
         construction=[(f312, q(f312, "(The owner must reimburse the PHA for any housing assistance payment for the period after the termination.)"))],
         reasoning="982.312(a)-(c) set the 180-day cap and the termination of the HAP contract and lease, with the owner's "
                   "reimbursement duty.")

r403 = P("US:24CFR982.403-454-hap-ends", "24 CFR 982.403(b), 982.454", "landlord; managing agent (voucher owner)", "scope",
         "The PHA terminates the HAP contract because the unit is too small for the family (after notice to the family and "
         "owner) or because program funding is insufficient.",
         "For a too-small unit, the HAP contract ends at the end of the calendar month after the month the PHA notifies the "
         "owner; for insufficient funding, when the PHA terminates it. The owner receives no housing assistance payment "
         "after that date, and the family is never liable for the assistance portion (US:24CFR982.451(b)(4)); the family "
         "may move with continued assistance.",
         f403, q(f403, "The HAP contract terminates at the end of the calendar month that follows the calendar month in which the PHA gives such notice to the owner."),
         "major", "5.7", instrument=HCV, dependencies=["US:24CFR982.451(b)(4)"],
         construction=[(f454, q(f454, "The PHA may terminate the HAP contract if the PHA determines, in accordance with HUD requirements, that funding under the consolidated ACC is insufficient to support continued assistance for families in the program."))],
         reasoning="982.403(b) fixes the termination date for a too-small unit; 982.454 allows funding terminations.")

r455 = P("US:24CFR982.455-zero-hap", "24 CFR 982.455", "landlord; managing agent", "scope",
         "A voucher family's assistance fell to zero (for example after an income increase) and 180 calendar days have "
         "passed since the last housing assistance payment to the owner.",
         "The HAP contract has ended automatically; from then on the tenancy is not a voucher tenancy, and its settlement "
         "follows state and local law alone, without the part 982 deposit and charge rules (US:24CFR982.313(c), "
         "US:24CFR982.451(b)(4)).",
         f455, q(f455, "The HAP contract terminates automatically 180 calendar days after the last housing assistance payment to the owner."),
         "major", "0", instrument=HCV, dependencies=["US:24CFR982.313(c)", "US:24CFR982.451(b)(4)"])

r453 = P("US:24CFR982.453-overpayment-recovery", "24 CFR 982.453(b)", "landlord; managing agent (voucher owner)", "must repay",
         "The PHA paid the owner housing assistance for a period after the move-out month or after the HAP contract ended, "
         "or the owner otherwise breached the HAP contract (for example HQS failures).",
         "The PHA may recover the overpayment from the owner, abate or reduce payments, or terminate the contract. An "
         "overpayment is repaid to the PHA; it is not credited to or charged against the tenant's account.",
         f453, q(f453, "The PHA rights and remedies against the owner under the HAP contract include recovery of overpayments, abatement or other reduction of housing assistance payments, termination of housing assistance payments, and termination of the HAP contract."),
         "major", "5.7", instrument=HCV, dependencies=["US:24CFR982.311(d)(1)", "US:24CFR982.451(b)(4)"])

r456 = P("US:24CFR982.456-tenant-enforcement", "24 CFR 982.456", "former tenant; landlord", "may",
         "A former voucher tenant disputes the settlement (for example deposit deductions or a charge for the assistance "
         "portion).",
         "The tenant may enforce the lease, including the owner's obligations under the tenancy addendum, against the "
         "owner; it is not a party to or beneficiary of the HAP contract and cannot enforce the HAP contract itself. The "
         "PHA may pursue its HAP-contract remedies against the owner even while the family occupies the unit.",
         f456, q(f456, "The tenant may exercise any right or remedy against the owner under the lease between the tenant and the owner, including enforcement of the owner's obligations under the tenancy addendum"),
         "minor", "7", instrument=HCV, dependencies=["US:24CFR982.308-tenancy-addendum"])

r510 = P("US:24CFR982.510-other-charges", "24 CFR 982.510", "landlord; managing agent (voucher owner)", "must not",
         "The owner bills a voucher tenant, during the tenancy or on the move-out account, for items other than rent (for "
         "example amenity, package, trash, or service fees, or meals and supportive services).",
         "It may not charge extra for items customarily included in rent in the locality or provided at no extra cost to "
         "unsubsidized tenants in the building, and the lease may not require payment for meals or supportive services; "
         "such charges are not owed, may not be deducted from the deposit, and non-payment of meal or service charges is "
         "not a ground to end the tenancy.",
         f510, q(f510, "The owner may not charge the tenant extra amounts for items customarily included in rent in the locality, or provided at no additional cost to unsubsidized tenants in the premises."),
         "major", "5.7", determinacy="MIXED", judgment_terms=["customarily included in rent in the locality"], instrument=HCV,
         dependencies=["US:24CFR982.313(c)", "EXT:state-charge-law"])

r5 = P("US:24CFR982.5-written-notices", "24 CFR 982.5", "landlord; managing agent; tenant", "must",
       "Part 982 requires a notice by the owner or the family (the owner's notice of grounds and copy of an eviction "
       "notice to the PHA; the family's notice of lease termination or move-out to the owner and PHA).",
       "The notice must be in writing.",
       f5, q(f5, "Where part 982 requires any notice to be given by the PHA, the family or the owner, the notice must be in writing."),
       "minor", "3.4", instrument=HCV, dependencies=["US:24CFR982.310-owner-termination"])

NOD_PHA = "PHA-internal administration of the voucher program; it sets no duty for the owner in the settlement and does not change what the tenant owes"
save([
    D("US:24 CFR 5.2005", "partial", "US:34USC12491-VAWA states that criminal activity relating to the violence is not "
      "cause to terminate and allows bifurcation; the ban on eviction because of victim status, the lease-violation "
      "construction rule and the limits on the protections are unstated. The notice-of-rights and emergency-transfer "
      "duties fall on the PHA in the voucher program.", ["US:34USC12491-VAWA"], [r_v05]),
    D("US:24 CFR 5.2007", "new_rule", "Documentation window and strict confidentiality of victim information bind the "
      "voucher owner and reach its agents and collectors.", proposed=[r_v07]),
    D("US:24 CFR 5.2009", "partial", "Bifurcation is stated by US:34USC12491-VAWA; the 90-day period for remaining "
      "tenants is unstated.", ["US:34USC12491-VAWA"], [r_v09]),
    D("US:24 CFR 5.2001", "stated", "Applies VAWA to tenant-based voucher tenancies, the reach US:34USC12491-VAWA already "
      "states; program-specific part 982 rules govern conflicts.", ["US:34USC12491-VAWA"]),
    D("US:24 CFR 5.2003", "no_decision", "Definitions (covered housing provider, affiliated individual, bifurcate, "
      "actual and imminent threat) used by the stated and proposed VAWA rules without changing their reach for a voucher "
      "owner."),
    D("US:24 CFR 5.2011", "no_decision", "Preserves more protective state law (NY:RPL-227-c, already stated) and fair "
      "housing law; changes nothing further."),
    D("US:34 USC 12494", "new_rule", "Owners and managers of voucher units may not retaliate against persons using VAWA "
      "rights; FHA remedies.", proposed=[r_ret]),
    D("US:34 USC 12495", "no_decision", "Bars penalties imposed by local governments' laws on residents who call police or "
      "are crime victims; it binds covered governments, not the landlord's settlement."),
    D("US:34 USC 12492", "no_decision", "Agency compliance reviews of VAWA housing requirements."),
    D("US:24 CFR 5.100", "no_decision", "General definitions for HUD programs; no stated rule's reach turns on them."),
    D("US:24 CFR 5.105", "no_decision", "Lists civil-rights requirements for HUD programs and the equal-access rule on "
      "eligibility; the settlement duties are stated under US:24CFR100.65-terms and the state and city rules, and a "
      "voucher owner is not a recipient of federal financial assistance for section 504 or title VI."),
    D("US:24 CFR 5.106", "excluded_regime", "Equal access in shelters and buildings funded by Community Planning and "
      "Development programs (HOME, CoC, ESG, HOPWA): subsidized housing outside the aperture."),
    D("US:24 CFR 5.107", "no_decision", "Audit requirements for nonprofit grantees."),
    D("US:24 CFR 5.109", "no_decision", "Participation of faith-based organizations in HUD grant programs."),
    D("US:24 CFR 5.110", "no_decision", "HUD waiver authority."),
    D("US:24 CFR 5.111", "no_decision", "Housing counseling requirements for HUD programs."),
    D("US:24 CFR 5.151", "no_decision", "Affirmatively-furthering-fair-housing certifications by program participants."),
    D("US:24 CFR 5.400", "no_decision", "Applicability of the family-income subpart to public housing and Section 8; income "
      "determination is PHA administration."),
    D("US:24 CFR 5.403", "no_decision", "Definitions for PHA income and eligibility determinations."),
    D("US:24 CFR Appendix_A_to_Subpart_A_of_Part_5", "no_decision", "Notice of funding opportunity terms for HUD grants."),
    D("US:24 CFR Appendix_B_to_Subpart_A_of_Part_5", "no_decision", "Notice of award terms for HUD grants."),
    D("US:24 CFR Appendix_C_to_Subpart_A_of_Part_5", "no_decision", "HUD grant administrative requirements."),
    D("US:47 CFR 64.1201", "no_decision", "Limits local exchange carriers' disclosure and use of billing name and address; "
      "binds telecommunications carriers and their billing agents, not a landlord, manager, Handoff or collector."),
    D("US:24 CFR 982.308", "new_rule", "The tenancy addendum prevails over the lease in a voucher settlement.", proposed=[r308]),
    D("US:24 CFR 982.309", "new_rule", "No rent increase during the initial term; the HAP contract ends with the lease.", proposed=[r309]),
    D("US:24 CFR 982.310", "new_rule", "Grounds, written notice, PHA copy and court action for an owner ending a voucher "
      "tenancy; decides how and when the tenancy ends.", proposed=[r310]),
    D("US:24 CFR 982.312", "new_rule", "Absence over 180 days ends the HAP contract and the assisted lease; the owner repays "
      "later HAP.", proposed=[r312]),
    D("US:24 CFR 982.403", "new_rule", "HAP contract termination date for an over-crowded unit; no HAP after it and none "
      "charged to the family.", proposed=[r403]),
    D("US:24 CFR 982.454", "new_rule", "Funding termination ends HAP; the owner cannot shift the lost HAP to the family.",
      proposed=[P("US:24CFR982.454-funding-termination", "24 CFR 982.454", "landlord; managing agent (voucher owner)", "scope",
                  "The PHA terminates the HAP contract for insufficient program funding while the family remains in the unit.",
                  "No housing assistance is paid after the termination, and the lost assistance is never charged to the "
                  "family (US:24CFR982.451(b)(4)); the remaining tenancy and its settlement follow the lease and state law.",
                  f454, q(f454, "The PHA may terminate the HAP contract if the PHA determines, in accordance with HUD requirements, that funding under the consolidated ACC is insufficient to support continued assistance for families in the program."),
                  "minor", "5.7", instrument=HCV, dependencies=["US:24CFR982.451(b)(4)", "US:24CFR982.403-454-hap-ends"])]),
    D("US:24 CFR 982.455", "new_rule", "180 days after the last HAP the contract ends and the tenancy is settled as an "
      "unassisted one.", proposed=[r455]),
    D("US:24 CFR 982.453", "new_rule", "HAP paid after move-out or contract end is recovered from the owner, not the tenant.", proposed=[r453]),
    D("US:24 CFR 982.456", "new_rule", "The tenant enforces the tenancy addendum, not the HAP contract.", proposed=[r456]),
    D("US:24 CFR 982.510", "new_rule", "Bars extra charges to voucher tenants for items included in rent or free to others; "
      "decides move-out charges.", proposed=[r510]),
    D("US:24 CFR 982.5", "new_rule", "All part 982 notices by owner and family are written.", proposed=[r5]),
    D("US:24 CFR 982.515", "stated", "The family owes the whole family share and the PHA never pays it, while the assistance "
      "portion is never the family's: US:24CFR982.451(b)(4) and US:24CFR982.452(b)(5).",
      ["US:24CFR982.451(b)(4)", "US:24CFR982.452(b)(5)"]),
    D("US:24 CFR 982.1", "no_decision", "Program overview; the end of the contract on move-out is stated in US:24CFR982.311(d)(1)."),
    D("US:24 CFR 982.4", "no_decision", "Definitions used by the stated voucher rules (rent to owner, family share, HAP "
      "contract, tenancy addendum); none narrows or widens them."),
    D("US:24 CFR 982.301", "no_decision", NOD_PHA + " (briefing a selected family)."),
    D("US:24 CFR 982.302", "no_decision", NOD_PHA + " (voucher issuance and tenancy request)."),
    D("US:24 CFR 982.303", "no_decision", NOD_PHA + " (voucher term)."),
    D("US:24 CFR 982.304", "no_decision", NOD_PHA + " (PHA help to a family facing discrimination)."),
    D("US:24 CFR 982.305", "no_decision", NOD_PHA + " (approval of the tenancy and HAP contract execution at move-in)."),
    D("US:24 CFR 982.306", "no_decision", NOD_PHA + " (PHA disapproval of owners)."),
    D("US:24 CFR 982.307", "no_decision", "Tenant screening at admission is the owner's; no settlement decision."),
    D("US:24 CFR 982.315", "no_decision", NOD_PHA + " (which members keep the voucher on family break-up)."),
    D("US:24 CFR 982.316", "no_decision", NOD_PHA + " (approving live-in aides)."),
    D("US:24 CFR 982.317", "no_decision", "Lease-purchase premiums excluded from rent reasonableness; no settlement decision."),
    D("US:24 CFR 982.351", "no_decision", "Overview of subpart H."),
    D("US:24 CFR 982.352", "no_decision", NOD_PHA + " (eligible housing types)."),
    D("US:24 CFR 982.353", "no_decision", NOD_PHA + " (where a family may lease; portability rights)."),
    D("US:24 CFR 982.354", "no_decision", "PHA permission to move with continued assistance, including VAWA moves; the "
      "owner's end date and charges follow the lease, state law (NY:RPL-227-c(1)) and US:24CFR982.311(d)(1)."),
    D("US:24 CFR 982.355", "no_decision", NOD_PHA + " (portability billing between PHAs)."),
    D("US:24 CFR 982.401", "no_decision", "Cross-reference to HQS; abatement consequences are stated in US:24CFR982.404(d)(3)-(4)."),
    D("US:24 CFR 982.402", "no_decision", NOD_PHA + " (subsidy standards)."),
    D("US:24 CFR 982.405", "no_decision", NOD_PHA + " (PHA inspections); repair failures lead to abatement, stated in US:24CFR982.404(d)(3)-(4)."),
    D("US:24 CFR 982.406", "no_decision", NOD_PHA + " (alternative inspections)."),
    D("US:24 CFR 982.407", "no_decision", "No private right to compel HQS enforcement against HUD or the PHA."),
    D("US:24 CFR 982.501", "no_decision", "Overview of subpart K."),
    D("US:24 CFR 982.503", "no_decision", NOD_PHA + " (payment standards)."),
    D("US:24 CFR 982.504", "excluded_regime", "Payment standard for families remaining in restructured project-based "
      "subsidized multifamily housing: project-based subsidized housing outside the aperture."),
    D("US:24 CFR 982.505", "no_decision", NOD_PHA + " (HAP calculation)."),
    D("US:24 CFR 982.506", "no_decision", "Rent negotiation at lease-up; no settlement decision."),
    D("US:24 CFR 982.507", "no_decision", NOD_PHA + " (rent reasonableness determinations)."),
    D("US:24 CFR 982.508", "no_decision", NOD_PHA + " (40% cap on initial family share)."),
    D("US:24 CFR 982.509", "no_decision", "Rent control limits on voucher rent apply only to regulated units, which the "
      "aperture excludes; for a market-rate unit it changes nothing."),
    D("US:24 CFR 982.514", "no_decision", NOD_PHA + " (distribution of HAP and utility reimbursements)."),
    D("US:24 CFR 982.516", "no_decision", NOD_PHA + " (reexaminations and effective dates of family-share changes); the owner "
      "bills the family share the PHA sets and never the assistance portion (US:24CFR982.451(b)(4))."),
    D("US:24 CFR 982.517", "no_decision", NOD_PHA + " (utility allowances)."),
    D("US:24 CFR 982.521", "excluded_regime", "Rent to owner for voucher units inside federally subsidized projects "
      "(Section 236, 221(d)(3), 202 and similar): subsidized project housing outside the aperture."),
    D("US:24 CFR 982.551", "no_decision", "Family obligations enforced by the PHA through termination of assistance; the "
      "owner's claims for damage or notice follow the lease and state law, and the VAWA construction rule is carried in "
      "US:24CFR5.2005-hcv-owner-limits."),
    D("US:24 CFR 982.552", "no_decision", NOD_PHA + " (denial or termination of assistance)."),
    D("US:24 CFR 982.553", "no_decision", NOD_PHA + " (criminal-activity grounds for PHA action)."),
    D("US:24 CFR 982.554", "no_decision", NOD_PHA + " (informal review for applicants)."),
    D("US:24 CFR 982.555", "no_decision", NOD_PHA + " (informal hearings for participants)."),
])
