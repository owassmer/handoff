import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *

A = "register/texts/NYC_ADC/"
dec("NYC:ADC 27-2005", "partial",
    "Owner repair duty is stated for painting; subdivision (c) lets a written lease allocate HMC repair and "
    "compliance to the tenant of a one- or two-family house, a branch no rule states. (d) harassment is decided at "
    "27-2004; (e)-(g) notices and (h) vacant-unit repair add no settlement decision.",
    ["NYC:HMC-27-2013(a)", "NYC:PAINT-wear-and-tear"],
    [rule("NYC:HMC-27-2005(c)-1-2-family-allocation", "Admin. Code 27-2005(a)-(c)", "owner; manager; tenant",
          "allocation", 
          "A departing tenant's unit and the account include repair, maintenance or painting work. Branch A: multiple "
          "dwelling (three or more units). Branch B: one- or two-family dwelling with no written lease term allocating "
          "that work. Branch C: one- or two-family dwelling where the written lease or another written contract puts "
          "that repair or HMC compliance on the tenant.",
          "A and B: the owner must keep the premises in good repair and comply with the Housing Maintenance Code, so "
          "repair and repainting needed from ordinary use is the owner's cost and is never charged; only damage the "
          "tenant caused beyond normal wear and tear is charged. C: the written allocation is valid under the Code, "
          "so the owner's statutory duty does not make that work the owner's cost as between the parties; the "
          "tenant's failure to do the allocated work is a lease claim at its reasonable cost. The deposit may still "
          "be kept only for the categories GOL 7-108(1-a)(b) allows (damage beyond normal wear and tear), so the cost "
          "of allocated work that only cures ordinary wear is pursued separately and never kept from the deposit. An "
          "oral allocation has no effect. Duties the Code imposes on the tenant alone (e.g. 27-2012(a) cleanliness, "
          "27-2045(c) detector upkeep) stay the tenant's in every branch.",
          A + "27-2005.txt", q(A + "27-2005.txt", "The owner of a one- or two-family dwelling shall keep the premises",
                               "imposed upon the tenant alone."),
          "major", "5.1; 5.3", determinacy="MIXED",
          judgment_terms=["lease term allocates the repair or compliance to the tenant", "ordinary wear and tear"],
          dependencies=["NY:GOL-7-108(1-a)(b)-refundable", "NYC:HMC-27-2013(a)", "NYC:PAINT-wear-and-tear"],
          amends="NYC:HMC-27-2013(a)")])
nd("NYC:ADC 27-2008", "Tenant must allow owner entry for code repairs and inspections during the tenancy; no "
   "settlement step turns on it (the refused-entry defence to the rent bar is stated at NY:MDL-302-a(3)).")
nd("NYC:ADC 27-2009", "Grounds for starting a summary proceeding after a tenant's code conviction; the chain begins "
   "once the ending is known and eviction grounds are the landlord's decision to begin an ending, not a step in "
   "settling it.")
dec("NYC:ADC 27-2009.1", "new_rule",
    "A no-pet lease clause is deemed waived after three months of open harboring known to the owner; this bars any "
    "move-out charge or deduction resting on breach of that clause. No rule states it.",
    proposed=[rule("NYC:HMC-27-2009.1-pet-clause-waiver", "Admin. Code 27-2009.1(b)-(e)", "owner; manager",
                   "bar",
                   "Tenant of a multiple dwelling (three or more units, not NYCHA) openly and notoriously harbored a "
                   "household pet the law does not prohibit for three months or more after taking possession; the owner "
                   "or its agent knew; the owner did not start a proceeding or action to enforce the lease's no-pet "
                   "clause within those three months.",
                   "The no-pet clause is waived: no pet-violation fee, penalty, or deduction based on breach of that "
                   "clause may appear on the move-out statement or be pursued, and a lease term or other restriction of "
                   "this right is void. Exception: the waiver does not apply where the pet caused damage to the "
                   "premises, created a nuisance, or substantially interfered with others' health, safety or welfare; "
                   "then the clause stays enforceable. In every branch, actual damage the pet caused beyond normal wear "
                   "and tear is chargeable like any tenant damage. A one- or two-family house is outside this section "
                   "(the lease clause governs).",
                   A + "27-2009.1.txt", q(A + "27-2009.1.txt", "Where a tenant in a multiple dwelling openly and notoriously",
                                          "such lease provision shall be deemed waived."),
                   "major", "5.1; 5.2", determinacy="MIXED",
                   judgment_terms=["openly and notoriously", "knowledge of the owner or agent",
                                   "damage, nuisance or substantial interference"],
                   dependencies=["NY:GOL-7-108(1-a)(b)-refundable"])])
nd("NYC:ADC 27-2010", "Allocates cleaning of roofs, yards and courts during occupancy (single-family occupant, "
   "otherwise the owner); a charge for debris left at move-out is decided by the deposit damage rule.")
nd("NYC:ADC 27-2011", "Owner cleans public parts; no tenant charge or settlement step depends on it.")
nd("NYC:ADC 27-2012", "Occupant keeps its unit clean during occupancy (owner cleans rooming units between "
   "occupancies); what a departing tenant may be charged for filth left behind is decided by the deposit damage "
   "rule and NYC:HMC-27-2017.5-turnover.")
nd("NYC:ADC 27-2014", "Owner paints exterior window frames and fire escapes; exterior painting is never a tenant "
   "charge and no settlement step turns on it.")
dec("NYC:ADC 27-2017.1", "partial",
    "The turnover rule covers multiple dwellings only; 27-2017.1 puts pest and allergen remediation on the owner of "
    "every dwelling, one- and two-family houses included, which changes what may be charged there.",
    ["NYC:HMC-27-2017.5-turnover"],
    [rule("NYC:HMC-27-2017.1-pest-owner-duty", "Admin. Code 27-2017.1 (with 27-2017 definitions)", "owner; manager",
          "allocation",
          "Any NYC dwelling (multiple dwelling or one- or two-family house) where, at or before move-out, pests "
          "(insects incl. bedbugs, rodents) or indoor mold hazards, or conditions conducive to them, are present and "
          "the account includes extermination, pest control or mold remediation.",
          "Keeping the premises free of pests and indoor allergen hazards, preventing their foreseeable occurrence and "
          "remediating them and their underlying defects (leaks, holes, entry paths) is the owner's statutory duty, "
          "so that cost is the owner's and is not charged to the departing tenant or kept from the deposit. It is "
          "chargeable only where the owner proves the departing tenant or its household caused the infestation or "
          "mold beyond normal wear and tear (e.g. food waste or filth left behind), and then only the reasonable cost "
          "of remedying what the tenant caused. Cost of curing an underlying building defect is never chargeable.",
          A + "27-2017.1.txt", q(A + "27-2017.1.txt", "An owner of a dwelling shall keep the premises free from pests",
                                 "when such underlying defect exists,"),
          "major", "5.5a", determinacy="MIXED",
          judgment_terms=["caused by the tenant beyond normal wear and tear", "reasonable cost"],
          dependencies=["NYC:HMC-27-2017.5-turnover", "NY:GOL-7-108(1-a)(b)-refundable"],
          amends="NYC:HMC-27-2017.5-turnover")])
dec("NYC:ADC 27-2017.12", "new_rule",
    "Voids any occupant waiver of article 4 (pest and mold) protections and makes seeking one a misdemeanor; a lease "
    "clause shifting remediation cost to the tenant is therefore void. Not stated.",
    proposed=[rule("NYC:HMC-27-2017.12-waiver-void", "Admin. Code 27-2017.12(a), (c), (d)", "owner; manager",
                   "prohibition",
                   "A lease or other agreement with the occupant of an NYC dwelling unit purports to make the occupant "
                   "bear duties or costs HMC article 4 puts on the owner (pest and mold remediation, turnover "
                   "remediation and certification); the unit is not an owner- or shareholder-occupied co-op or condo "
                   "unit and not NYCHA.",
                   "The waiver is void, so no charge or deduction may rest on it. An owner who seeks such a waiver "
                   "commits a misdemeanor (fine up to $500, up to six months, or both) and is liable for a civil "
                   "penalty up to $500 per violation. Charges for damage the tenant actually caused beyond wear and "
                   "tear rest on the damage rule, not on a waiver, and remain chargeable. Allocations between a co-op "
                   "and its shareholder or a condo board and unit owner are unaffected.",
                   A + "27-2017.12.txt", q(A + "27-2017.12.txt", "No owner may seek to have an occupant",
                                           "not more than five hundred dollars per violation."),
                   "major", "5.5a", dependencies=["NYC:HMC-27-2017.1-pest-owner-duty", "NYC:HMC-27-2017.5-turnover"])])
nd("NYC:ADC 27-2017.2", "Owner's yearly allergen investigation and lease notice; move-in paperwork and in-tenancy "
   "duties that fix no settlement amount.")
nd("NYC:ADC 27-2017.3", "Classes of HPD mold violations and correction dates during occupancy; no settlement step.")
nd("NYC:ADC 27-2017.6", "HPD inspection procedure; no settlement step.")
nd("NYC:ADC 27-2018.1", "Bedbug history notice with a vacancy lease and bedbug information at lease or renewal; "
   "move-in paperwork that fixes no settlement amount.")
nd("NYC:ADC 27-2019", "Storage of materials that harbor pests during occupancy; no settlement step.")
st("NYC:ADC 27-2017", ["NYC:HMC-27-2017.5-turnover"],
   "Article 4 definitions (pest incl. bedbugs; indoor allergen hazard; remediate; underlying defect) set the reach "
   "of the turnover remediation rule.")
commit()
