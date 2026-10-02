import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s in ["NY:RPAPL 796-J", "NY:RPAPL 796-M"]:
    rows.append(D(s, "excluded_regime", "Article 7-C administrator; RPAPL 796-A(4) makes article 7-C inapplicable in New York City (outside NYC)."))
for s in ["NY:RPAPL 797", "NY:RPAPL 797-A", "NY:RPAPL 797-C", "NY:RPAPL 797-D", "NY:RPAPL 797-E", "NY:RPAPL 797-H",
          "NY:RPAPL 797-I", "NY:RPAPL 797-J"]:
    rows.append(D(s, "excluded_regime",
      "Article 7-D tenant repair proceeding; RPAPL 797(3) bars it in New York, Bronx, Kings, Queens and Richmond "
      "counties (outside NYC)."))
for s, r in [
  ("NY:RPAPL 801", "Common-law waste action against a tenant for years; for a departed tenant it gives no remedy beyond the lease damage claim already stated (NY:GOL-7-108(1-a)(b)-refundable, NY:ADJ-forfeiture-claims-survive)."),
  ("NY:RPAPL 815", "Judgment in a waste action (compensatory damages; forfeiture of an unexpired term); the damage recovery duplicates the stated lease claim and forfeiture of the term is moot once the tenant has left."),
  ("NY:RPAPL 851", "Holdover by a guardian, trustee or life tenant after the estate ends; not a market-rate lease."),
  ("NY:RPL 221", "Rent on leases for life; not a market-rate term or monthly tenancy."),
  ("NY:RPL 222", "Apportionment of rent when a life tenant who let the property dies; not a market-rate tenancy."),
  ("NY:RPL 226", "Surrender and renewal of an original lease as against an under-lease; no settlement amount or payee turns on it."),
  ("NY:RPL 227-F", "Bars refusing to rent to an applicant because of past landlord-tenant cases; it governs new rentals, not the departing tenancy's settlement."),
  ("NY:RPL 231-A", "Sprinkler disclosure in the lease at signing; it carries no settlement consequence."),
  ("NY:RPL 231-B", "Flood history and risk disclosure in the lease at signing; it carries no settlement charge, credit or deadline."),
  ("NY:RPL 235-D", "Injunction against harassment of tenants in former manufacturing buildings without a residential certificate; it creates no settlement charge, credit or deadline, and rent in such buildings is governed by the certificate-of-occupancy rules already stated."),
  ("NY:RPL 235-J", "Notice to neighbouring tenants of a bed-bug infestation; the turnover remediation cost is stated by NYC:HMC-27-2017.5-turnover and no settlement step turns on the notice."),
  ("NY:RPL 237", "Makes a childless-tenancy lease clause a violation; equal treatment in settlement is stated (NY:EXEC-296(5)(a)(2)-terms)."),
]:
    rows.append(D(s, "no_decision", r))

S = "NY:RPL 223-A"
rows.append(D(S, "new_rule",
  "If the landlord never delivers possession at the start of the term, the tenant may rescind and recover everything it "
  "paid; this ends the tenancy before it begins and fixes the refund.",
  proposed=[R("NY:RPL-223-a-no-possession-rescission", S, "RPL 223-a", "landlord", "must",
  "The landlord does not deliver possession at the beginning of the term (for example the prior occupant holds over "
  "or the unit is not ready), and the lease does not expressly provide otherwise.",
  "The tenant may rescind the lease and recover the consideration it paid (deposit, advance rent, any other sums), in "
  "addition to any damages. On rescission there is no tenancy to settle: no rent accrued, no deduction is taken, and "
  "the whole of what was paid is refunded.",
  Q(S, "there shall be implied in every lease of real property a condition that the lessor will deliver possession",
    "any right of action he may have to recover damages."),
  "critical", "Step 1 what was fixed at move-in; Step 3 how the tenancy ends")]))

S = "NY:RPL 224"
rows.append(D(S, "new_rule",
  "A tenant's attornment to a stranger is void against the landlord, so a stranger (for example a deed thief or a party "
  "claiming title) does not become the payee of rent or the settlement unless the landlord consents, a court orders it, "
  "or it is the foreclosure-sale purchaser.",
  proposed=[R("NY:RPL-224-attornment-void", S, "RPL 224", "landlord; tenant", "must",
  "A person other than the landlord (not its agent or successor in title) claims to be the landlord and the tenant "
  "acknowledges it and pays it rent or looks to it for the refund.",
  "The attornment is void and does not affect the landlord's possession or position unless the landlord consented, a "
  "court judgment or order directs it, or the stranger is the purchaser at a foreclosure sale (then "
  "NY:RPAPL-1305-successor governs). The landlord remains the party that settles the account and to whom rent is due, "
  "and it credits only payments made to it or its authorized agent, a court-appointed receiver or administrator, or "
  "an entity entitled by law (Step 0.5).",
  Q(S, "The attornment of a tenant to a stranger is absolutely void", "3. To a purchaser at foreclosure sale."),
  "major", "Step 0.5 who is owed the rent", dependencies=["NY:RPAPL-1305-successor", "NY:CPLR-6401-foreclosure-receiver"])]))

S = "NY:RPL 225"
rows.append(D(S, "new_rule",
  "A tenant served with process in an action to recover the property must notify the landlord at once or forfeits three "
  "years' rent value to the landlord; a claim no rule states.",
  proposed=[R("NY:RPL-225-notice-of-adverse-action", S, "RPL 225", "landlord; tenant", "may",
  "While in possession the tenant is served with a summons or process in an action by a third party to recover the "
  "unit or its possession (ejectment, a title or foreclosure action naming the tenant) and does not forthwith notify "
  "the landlord.",
  "The tenant forfeits to the landlord (or other person of whom it holds) the value of three years' rent of the "
  "premises; the landlord may claim that sum from the tenant, including in the move-out account's separate claim. It "
  "is a statutory forfeiture, not rent or damage, so it is not kept from the deposit "
  "(NY:GOL-7-108(1-a)(b)-refundable) and is pursued by action.",
  Q(S, "Where a process or summons in an action to recover the real property occupied by him", "to the landlord or other person of whom he holds."),
  "critical", "Step 8 collecting a balance", dependencies=["NY:GOL-7-108(1-a)(b)-refundable"])]))

S = "NY:RPL 226-A"
rows.append(D(S, "new_rule",
  "A tenant's right to remove its fixtures or improvements survives a renewal, which decides at move-out whether the "
  "tenant may take them or the landlord keeps them.",
  proposed=[R("NY:RPL-226-a-fixture-removal", S, "RPL 226-a", "landlord", "must",
  "The tenant had a right (under the lease or law) to remove fixtures or improvements it installed and renewed or took "
  "a new lease of the same unit without surrendering possession between terms.",
  "Unless expressly agreed otherwise, the renewal does not lose or impair the removal right; at move-out under the "
  "later lease the tenant may still remove them, and the landlord may not treat them as its own by reason of the "
  "renewal. Damage the removal causes beyond wear and tear is chargeable as tenant damage "
  "(NY:GOL-7-108(1-a)(b)-refundable).",
  Q(S, "Unless otherwise expressly agreed, where a tenant has a right to remove fixtures or improvements",
    "without any surrender of possession between terms."),
  "minor", "Step 5.1 what the deposit may be kept for; Step 6.9 belongings left behind",
  dependencies=["NY:GOL-7-108(1-a)(b)-refundable"])]))

S = "NY:RPL 230"
rows.append(D(S, "partial",
  "Retaliation for complaints is stated (NY:RPL-223-b-retaliation); RPL 230 adds that no landlord may penalize or "
  "withhold any right or benefit of the tenancy because the tenant took part in a tenants' group.",
  ["NY:RPL-223-b-retaliation"], [R(
  "NY:RPL-230-tenant-group-no-penalty", S, "RPL 230(1)", "landlord, manager, Handoff", "must_not",
  "The departing tenant formed, joined or took part in the lawful activities of a tenants' group, committee or "
  "organization.",
  "No settlement decision may harass, punish, penalize, diminish or withhold any right, benefit or privilege of the "
  "tenancy for that reason (a stricter damage assessment, a charge not made to others, withholding the refund, "
  "pursuing or reporting a balance others would not face).",
  Q(S, "nor shall any landlord harass, punish, penalize, diminish, or withhold any right, benefit or privilege of a tenant under his tenancy for exercising such right."),
  "minor", "Step 5.10 equal treatment", determinacy="MIXED", judgment_terms=["for exercising such right"],
  dependencies=["NY:RPL-223-b-retaliation"])]))

S = "NY:RPL 235"
rows.append(D(S, "new_rule",
  "Wilfully withholding services or interfering with quiet enjoyment (for example to hasten a departure) is a "
  "violation by the lessor or its manager or agent; it limits what a manager may do in the notice period.",
  proposed=[R("NY:RPL-235-wilful-service-denial", S, "RPL 235(1), (2)", "landlord, managing agent", "must_not",
  "The tenancy is ending (notice given, or the tenant is in the pre-vacate period) and the lease, expressly or "
  "impliedly, requires the landlord to furnish water, heat, light, power, elevator, telephone or another service.",
  "No lessor, agent, manager, superintendent or janitor may wilfully or intentionally fail to furnish the service when "
  "needed for proper or customary use, or wilfully and intentionally interfere with the tenant's quiet enjoyment, or "
  "obstruct a fuel-oil delivery or burner refiring under MDL 302-c; each is a violation. Such conduct also supports "
  "the tenant's abatement and constructive-eviction claims (NY:RPL-235-b, NY:COMMONLAW-constructive-eviction).",
  Q(S, "who wilfully or intentionally fails to furnish such water, heat, light, power, elevator service",
    "interferes with the quiet enjoyment of the leased premises by such occupant, is guilty of a violation."),
  "minor", "Step 3 how the tenancy ends", determinacy="MIXED", judgment_terms=["wilfully or intentionally", "quiet enjoyment"],
  dependencies=["NY:RPL-235-b", "NY:COMMONLAW-constructive-eviction"])]))

S = "NY:RPL 237-A"
rows.append(D(S, "partial",
  "Familial-status equal treatment is stated (NY:EXEC-296(5)(a)(2)-terms); 237-A adds a misdemeanor and a private "
  "action with attorney's fees for discriminating in rental terms because of children.",
  ["NY:EXEC-296(5)(a)(2)-terms", "NY:EXC-297(9)-remedies"], [R(
  "NY:RPL-237-a-children-remedy", S, "RPL 237-a(a), (b)", "landlord, manager", "must_not",
  "A settlement decision treats a tenant worse solely because it has a child or children, in a building that is not "
  "federally subsidized senior housing, an owner-occupied one- or two-family house, or a 55-plus manufactured home "
  "park.",
  "It is a misdemeanor (fine $50 to $100 per offense), and the tenant has a cause of action for damages, declaratory "
  "and injunctive relief, with reasonable attorney's fees to a prevailing tenant, in addition to Human Rights Law "
  "remedies.",
  Q(S, "who discriminates in the terms, conditions, or privileges of any such rental, solely on the ground that such person or family has or have a child or children",
    "reasonable attorney’s fees as determined by the court may be awarded to a prevailing plaintiff."),
  "minor", "Step 5.10 equal treatment", dependencies=["NY:EXEC-296(5)(a)(2)-terms"])]))

save(rows)
