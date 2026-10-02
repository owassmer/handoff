import sys; sys.path.insert(0, "register/work")
from q8_lib import D, save
N = "no_decision"
save([
 D("NY:MDL 1", N, "Short title of the Multiple Dwelling Law; states no duty, amount or deadline."),
 D("NY:MDL 11", N, "Rebuilding standards for a multiple dwelling damaged two-thirds or moved; a construction rule, no effect on rent, deposit or the account (casualty surrender runs under RPL 227)."),
 D("NY:MDL 2", N, "Legislative finding for the Multiple Dwelling Law; declares policy, decides nothing."),
 D("NY:MDL 28", N, "Open-space and access rules for two buildings on one lot; construction standard only."),
 D("NY:MDL 288", N, "Definitions for MDL art. 7-D (inhabited basement and cellar units in listed community districts); the article's operative sections (289, 290) were decided no_decision in the queue and no stated or proposed rule depends on these terms."),
 D("NY:MDL 300", N, "Building permits for construction, alteration and conversion, and the cellar/basement occupancy permit; rent recovery for unlawful occupancy runs through MDL 301-302 and the cellar rule NYC:HMC-27-2087, already stated; the permit procedure itself changes no settlement step."),
 D("NY:MDL 310", N, "Board of Standards and Appeals variance powers; administrative, no effect on the account."),
 D("NY:MDL 36", N, "Window and skylight dimensions for public halls; construction standard only."),
 D("NY:MDL 50", N, "Entrance hall widths; construction standard only."),
 D("NY:MDL 51", N, "Shaft, elevator and dumbwaiter construction; no charge, deadline or recovery consequence."),
 D("NY:MDL 54", N, "Cellar entrance construction; construction standard only."),
 D("NY:MDL 56", N, "Frame building and extension limits, store-to-dwelling conversion approvals; construction standard only."),
 D("NY:MDL 58", N, "Fire-test standard for incombustible materials; construction standard only."),
 D("NY:MDL 61", N, "Business uses in multiple dwellings (egress, fire-retarding); governs non-residential space, not the tenancy account."),
 D("NY:MDL 63", N, "Fireproofing and egress for sub-curb living rooms; construction standard only."),
 D("NY:MDL 65", N, "Boiler room enclosure; construction standard only."),
 D("NY:MDL 8", N, "Specific-over-general rule for applying MDL requirements by dwelling class; no stated or proposed rule in the chain turns on it (MDL 4(7), 301-302, 325 and 302-a apply by their own terms)."),
 D("NY:MHL 81.01", N, "Legislative findings for the article 81 guardianship system; the operative guardian powers are in 81.21, 81.29 and related sections decided in the queue."),
])
