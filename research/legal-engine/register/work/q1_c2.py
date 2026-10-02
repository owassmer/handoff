import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
S = "NY:RPAPL 711"
rows.append(D(S, "partial",
  "Removal only by court process (NY:RPAPL-768-853-unlawful-eviction) and the 231-c notice (NY:RPAPL-741(5-a)-231-c-notice) "
  "are stated; 711 adds the holdover and nonpayment grounds, the 14-day written rent demand, the rule that rent "
  "accepted after a holdover is commenced does not end it, the successor's right to predecessor rent, and the "
  "estate-only possessory judgment after a tenant's death.",
  ["NY:RPAPL-768-853-unlawful-eviction", "NY:RPAPL-741(5-a)-231-c-notice", "NY:RPL-232-c"], [R(
  "NY:RPAPL-711-summary-grounds", S, "RPAPL 711 (opening), (1), (2)", "landlord", "must",
  "The landlord seeks to remove a tenant or lawful occupant who has not left: one holding over after the term, or one "
  "in default of rent.",
  "A tenant or lawful occupant of a dwelling (including a rooming-house or non-transient hotel occupant of 30 "
  "consecutive days or more; not a squatter) is removed only by a special proceeding. Holdover: the tenant stays after "
  "the term without the landlord's permission; rent the landlord accepts after the holdover proceeding is commenced "
  "does not end the proceeding or affect the award of possession. Nonpayment: the tenant defaulted in rent under the "
  "agreement and was first served (in the RPAPL 735 manner) a written demand giving at least 14 days' notice to pay "
  "the rent or give up possession; until 2034-06-15 that notice appends or contains the RPL 231-c Good Cause notice "
  "(covered or exempt and why; basis for non-renewal; justification for an increase above the local rent standard). "
  "A successor to the landlord's interest may proceed for rent due its predecessor only if it holds the right to that "
  "rent (NY:RPL-223). If a tenant dies during the term with rent unpaid and an occupant claims possession, the "
  "proceeding yields a possessory judgment only against the estate, without prejudice to the occupants, and the "
  "warrant does not run against them.",
  Q(S, "The tenant has defaulted in the payment of rent, pursuant to the agreement under which the premises are held",
    "section seven hundred thirty-five of this article."),
  "major", "Step 3.5 staying past the end; Step 3.8 after an eviction case",
  dependencies=["NY:RPAPL-741(5-a)-231-c-notice", "NY:RPL-223"],
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S, "Acceptance of rent after commencement of the special proceeding upon this ground",
                  "or to the new lessee, as the case may be.")}],
  reasoning="The holdover clause controls over RPL 232-c's month-to-month rule only for rent accepted after the "
            "proceeding is commenced; acceptance before commencement is governed by RPL 232-c.")]))

S = "NY:RPAPL 731"
rows.append(D(S, "new_rule",
  "Two parts change the chain: only an attorney, judge or clerk issues a notice of petition (so neither the owner in "
  "person nor Handoff), and full rent tendered before the hearing must be accepted and moots a nonpayment case.",
  proposed=[R("NY:RPAPL-731-issuance-and-tender", S, "RPAPL 731(1), (4)", "landlord", "must",
  "A summary proceeding is started, or a tenant in a nonpayment proceeding tenders the full rent due before the "
  "hearing.",
  "A notice of petition is issued only by an attorney, a judge or the court clerk, never by the party prosecuting in "
  "person, so a manager or Handoff cannot issue one. In a proceeding for nonpayment of rent, payment of the full amount "
  "of rent due, made at any time before the hearing, must be accepted by the landlord and makes the nonpayment ground "
  "moot, so the tenancy does not end on that ground and the account continues as a running tenancy.",
  Q(S, "4. In an action premised on a tenant defaulting in the payment of rent",
    "renders moot the grounds on which the special proceeding was commenced."),
  "major", "Step 3.8 after an eviction case",
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S, "A notice of petition may be issued only by an attorney, judge or the clerk of the court",
                  "it may not be issued by a party prosecuting the proceeding in person.")}],
  reasoning="Subdivision 1 decides who may start the proceeding (NY:CPLR-321-JUD-495-appearance for appearance); "
            "subdivision 4 decides whether a tender ends the nonpayment case.")]))

rows.append(D("NY:RPAPL 735", "no_decision",
  "Service mechanics of a summary proceeding to recover possession; a balance after move-out is sued by action, and "
  "the section fixes no amount, date or payee in the settlement."))
rows.append(D("NY:RPAPL 743", "no_decision",
  "Form of answer in a summary proceeding for possession; it fixes nothing the settlement decides."))

S = "NY:RPAPL 745"
rows.append(D(S, "new_rule",
  "In NYC, rent or use and occupancy deposited under a court order in a summary proceeding is credited against the "
  "judgment and paid under it; the order's amount caps and exclusions decide what the landlord received.",
  proposed=[R("NY:RPAPL-745-court-deposit-credit", S, "RPAPL 745(2)(a)-(f)", "landlord", "must",
  "An NYC summary proceeding preceded the move-out and the court ordered the tenant to deposit accruing rent or use "
  "and occupancy (after two adjournments at the tenant's request, or 60 days after the first appearance).",
  "Sums so deposited are paid to the clerk or to whom the court directs; on final judgment they are credited against "
  "the judgment and paid under it without further order, so the settlement credits them as paid when released. The "
  "ordered amount never exceeds the regulated rent, the tenant's subsidy share or share under an expired subsidy "
  "(unless the tenant agreed anew to pay full rent); the subsidy-paid portion, SCRIE/DRIE exemptions and two-party "
  "or direct social-services payments are not deposited; a public-assistance household deposits only the shelter "
  "allowance and a fixed-income tenant at most 30% of monthly income; the amount is offset by payments under RPL "
  "235-a and MDL 302-c. No order issues where the tenant establishes a listed defense (improper petitioner, actual or "
  "constructive eviction after quitting, SSL 143-b, hazardous HMC violations, colorable overcharge, C of O or "
  "MDL/HMC illegality, no personal jurisdiction). Failure to pay ordered use and occupancy never dismisses the "
  "tenant's defenses or counterclaims.",
  Q(S, "(iii) Upon the entry of the final judgment in the proceeding such deposits shall be credited",
    "be paid in accordance with the judgment."),
  "major", "Step 3.8 after an eviction case; Step 5.5a credits",
  dependencies=["NY:RPL-235-a", "NY:MDL-302-c-fuel-credit", "NY:SSL-143-b(5)-rent-bar"])]))

S = "NY:RPAPL 747"
rows.append(D(S, "new_rule",
  "A summary-proceeding judgment awards costs to the winner; that sum is a judgment debt, not a category the deposit "
  "may be kept for.",
  proposed=[R("NY:RPAPL-747-judgment-costs", S, "RPAPL 747(1), (2), (4)", "landlord", "must_not",
  "A summary proceeding preceded the move-out and ended in a final judgment awarding costs (and any money for rent).",
  "The judgment determines the rights of the parties and awards the successful party the costs of the proceeding. "
  "Costs awarded to the landlord are recovered by enforcing the judgment; they are not rent, damage, lease utilities "
  "or moving and storage, so they are not kept from the deposit (NY:GOL-7-108(1-a)(b)-refundable). Rent the judgment "
  "awarded is applied to the deposit as rent. The judgment does not bar an action to recover possession, nor an "
  "action or counterclaim for affirmative equitable relief begun within 60 days of entry that the court's limited "
  "jurisdiction kept out of the proceeding.",
  Q(S, "The court shall direct that a final judgment be entered determining the rights of the parties",
    "the costs of the special proceeding."),
  "major", "Step 3.8 after an eviction case; Step 5.2 fees",
  dependencies=["NY:GOL-7-108(1-a)(b)-refundable", "NY:RPL-234-a"])]))

S = "NY:RPAPL 753"
rows.append(D(S, "new_rule",
  "The warrant stay of up to a year moves the date the tenancy ends and fixes, through court deposits, what the landlord "
  "receives for the stay period; the 30-day cure stay decides whether a breach ends the tenancy.",
  proposed=[R("NY:RPAPL-753-warrant-stay", S, "RPAPL 753(1)-(5)", "court; landlord", "may",
  "A holdover or breach-of-lease proceeding for a dwelling (not an hotel, lodging-house or rooming-house room) ends in "
  "a judgment of possession against the occupant.",
  "On the occupant's good-faith application the court may stay the warrant (and execution for costs) up to one year "
  "where similar premises in the neighborhood cannot be found despite due efforts, or refusal would cause extreme "
  "hardship (serious ill health, worsening condition, a child's local school, other circumstances), weighing any "
  "substantial hardship to the landlord. The stay holds only while the occupant deposits in court, in full or in "
  "instalments the court sets, use and occupancy for the stay period at the last month's rent rate plus any difference "
  "the court finds to the reasonable value, and may include rent unpaid before the stay; the court's amount is final. "
  "The clerk pays the deposits to the landlord or its authorized agent under the stay, so the account credits them as "
  "paid and the tenancy ends when the warrant executes or the occupant leaves. No stay where the landlord proves the "
  "occupant objectionable. Where the proceeding rests on breach of a lease provision, the court must grant a 30-day "
  "stay in which the tenant may cure. A lease waiver of this section is void.",
  Q(S, "Such stay shall be granted and continue effective only upon the condition", "the further order of the court."),
  "major", "Step 3.5 staying past the end; Step 3.8 after an eviction case", determinacy="MIXED",
  judgment_terms=["good faith", "suitable premises similar", "due and reasonable efforts", "extreme hardship",
                  "substantial hardship", "objectionable"],
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S, "4. In the event that such proceeding is based upon a claim that the tenant or lessee has breached",
                  "during which time the respondent may correct such breach.")}],
  reasoning="Subdivision 4's cure stay is mandatory ('shall grant'); the subdivision 1 stay is discretionary.")]))

S = "NY:RPAPL 755"
rows.append(D(S, "new_rule",
  "A court may stay any action for rent or rental value while a dangerous or constructively evicting condition "
  "remains; this reaches the landlord's suit for a move-out rent balance.",
  proposed=[R("NY:RPAPL-755-rent-action-stay", S, "RPAPL 755(1)-(4)", "court; landlord", "may",
  "The landlord sues (by summary proceeding or action) for rent or rental value, and the tenant proves a municipal "
  "notice or order to remove a nuisance or violation or make repairs, or proves the condition directly, and the "
  "condition constructively evicts the tenant from part of the premises or is or is likely to become dangerous to "
  "life, health or safety.",
  "The court may stay the proceeding or action for rent or rental value. Where a municipal notice or order is proved, "
  "the landlord bears the burden of disproving the condition it describes. No stay where the tenant or its agent "
  "created the condition wilfully or negligently. The tenant must deposit with the clerk the rent then due (the prior "
  "month's rent or the agreement's monthly rent), and the stay may be vacated on three days' notice if it fails to "
  "deposit within five days after rent falls due. The stay lasts until vacated on three days' notice and proof the "
  "order was complied with; meanwhile deposits may be released to contractors or the city for repairs and "
  "maintenance, and on vacatur the remainder goes to the landlord or its authorized agent. No costs to either side "
  "while a stay is granted, save costs up to $25 against a tenant whose wilful act caused the condition.",
  Q(S, "(b) Upon proper proof of the existence of a condition", "any action for rent or rental value."),
  "major", "Step 8.10 before suing", determinacy="MIXED",
  judgment_terms=["such as to constructively evict", "dangerous to life, health, or safety", "wilful or negligent act"],
  dependencies=["NY:MDL-302-a(3)", "NY:RPL-235-b"])]))

rows.append(D("NY:RPAPL 761", "no_decision",
  "Redemption of possession by a lessee whose unexpired term exceeds five years after a nonpayment warrant; it restores "
  "possession and fixes nothing in a market-rate move-out settlement."))
rows.append(D("NY:RPAPL 771", "no_decision",
  "Commencement and service of the tenants' article 7-A petition; the article's effect on the settlement, rent payable "
  "to the administrator, is stated by NY:RPAPL-776-778-administrator."))
rows.append(D("NY:RPAPL 780", "no_decision",
  "Voids lease waivers of article 7-A tenant protections; the article's settlement effect is stated by "
  "NY:RPAPL-776-778-administrator and nothing in it turns on a lease term."))
rows.append(D("NY:RPAPL 783", "no_decision",
  "Bars the habitability defense in the 7-A administrator's own rent proceeding; that rent is the administrator's to "
  "collect (NY:RPAPL-776-778-administrator), not the landlord's or Handoff's."))
rows.append(D("NY:RPAPL 796-H", "excluded_regime",
  "Article 7-C rent-deposit judgment; RPAPL 796-A(4) makes the article inapplicable in New York City (outside NYC)."))
rows.append(D("NY:RPAPL 796-L", "excluded_regime",
  "Waiver bar for article 7-C, which RPAPL 796-A(4) excludes from New York City (outside NYC)."))
rows.append(D("NY:RPL 217", "no_decision",
  "Conditions a Good Cause possession judgment on notice compliance; the walk already starts the settlement only at "
  "actual departure or court-ordered removal (NY:RPL-215), which this does not change."))

S = "NY:RPL 227-B"
rows.append(D(S, "partial",
  "RPL 227-a termination by a senior moving to care is stated; 227-b adds the senior's right to reinstate the "
  "terminated residential lease within five business days, and what happens to a reletting and broker fees.",
  ["NY:RPL-227-a(1)", "NY:RPL-227-a(2)"], [R(
  "NY:RPL-227-b(5)-(7)-senior-reinstatement", S, "RPL 227-b(5), (6), (7), (10)", "landlord", "must",
  "A tenant who terminated under RPL 227-a to enter an adult care or senior housing facility cancels that facility "
  "contract within its 227-b cancellation window and gives the landlord or its agent written notice of reinstatement "
  "by midnight of the fifth business day after the 227-a termination notice was delivered (a mailed notice counts on "
  "its postmark date).",
  "The original lease is reinstated and continues for its stated period as if never interrupted, so the tenancy does "
  "not end, no move-out settlement is made, and rent continues. Any lease the landlord signed to relet the unit is "
  "cancelled; the landlord owes the prospective tenant only a refund of rent or security it paid, and owes nothing to "
  "a broker or agent for the reletting, and any broker's fee paid for that reletting is refunded to whoever paid it. "
  "An agreement waiving these rights is void.",
  Q(S, "5. Where a person exercises their right to cancel a lease or contract pursuant to this section",
    "as if there had been no interruption in the lease period."),
  "critical", "Step 3.4 statutory rights to end early", dependencies=["NY:RPL-227-a(1)", "NY:RPL-227-a(2)"],
  amends="NY:RPL-227-a(2)",
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S, "6. Any lease or rental agreement entered into by a lessor or owner to relet the premises",
                  "in connection with such reletting.")}],
  reasoning="Subdivision 6 fixes the reletting consequence; subdivision 7 the broker-fee refund.")]))

S = "NY:RPL 231"
rows.append(D(S, "partial",
  "The common-law rule that belongings may not be held for rent is stated (NY:COMMONLAW-belongings-owner-keeps); 231(4) "
  "voids a residential lease clause pledging exempt personal property as rent security, and 231(1) ends the lease on "
  "illegal business use.",
  ["NY:COMMONLAW-belongings-owner-keeps"], [R(
  "NY:RPL-231-illegal-use-and-exempt-pledge", S, "RPL 231(1), (4)", "landlord", "must_not",
  "(a) A residential lease contains a clause pledging the tenant's personal property that is exempt from execution as "
  "security for rent; or (b) the tenant used or occupied the unit for an illegal trade, manufacture or business.",
  "(a) The clause is void; the landlord takes no security interest in exempt property through it and may not hold or "
  "apply such belongings for rent under it. (b) The lease becomes void on that use and the landlord may re-enter "
  "(removal of an occupant still in possession goes through a summary proceeding, NY:RPAPL-711-summary-grounds); "
  "lease rent stops with the lease, and occupation after it is charged as use and occupancy (NY:RPL-220).",
  Q(S, "4. Any lease or agreement hereafter executed for the letting or occupancy of real property",
    "is void as to such provision."),
  "major", "Step 6.9 belongings left behind; Step 3 how the tenancy ends",
  dependencies=["NY:COMMONLAW-belongings-owner-keeps", "NY:RPL-220"],
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S, "1. Whenever the lessee or occupant other than the owner",
                  "the landlord of such lessee or occupant may enter upon the premises so let or occupied.")}],
  reasoning="Subdivision 1 is the ending rule; subdivision 4 the void pledge.")]))

save(rows)
