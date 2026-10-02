"""Independent review 4A, Phase 1: build review/review4a_universe.json from saved sources (quotes cut by anchors).

Built BLIND: written before any rule file, the walk or any review file was opened. Every quote is cut mechanically
from a saved source by ir4a_lib.cut(); nothing is retyped. Run: python3 review/ir4a_build_universe.py
"""
import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ir4a_lib import cut  # noqa: E402

S = "sources/"
U = []
ERR = []


def add(citation, level, kind, step, effect, src, start, end=None):
    try:
        q = cut(S + src, start, end)
    except Exception as e:  # noqa: BLE001
        ERR.append(f"{citation}: {e}")
        return
    U.append({"id": f"U{len(U) + 1:03d}", "citation": citation, "level": level, "kind": kind, "decision_point": step,
              "one_line_effect": effect, "source_file": S + src, "verbatim_quote": q})


R0, R1, R2, R3, R4, R5 = ("S0 unit routing and regime", "S1 facts fixed at move-in", "S2 whether and how the tenancy ends; when rent stops",
                          "S3 who is owed what and who may collect", "S4 deposit trust, interest and custody", "S5 charges and credits; what may be kept")
R6, R7, R8, R9, R10 = ("S6 itemized statement: timing, form, delivery, payee", "S7 refund method and payee", "S8 consequences of a miss",
                       "S9 balance beyond deposit: pursue, hand off, report or write off", "S10 procedure and preconditions to suing")
R11, R12, R13, R14 = ("S11 limitations", "S12 interest", "S13 collection conduct and licensing", "S14 unclaimed funds")
R15, R16, R17, R18, R19 = ("S15 bankruptcy", "S16 death of tenant", "S17 military service", "S18 disability", "S19 domestic violence")
R20, R21, R22 = ("S20 tax and information reporting", "S21 data, privacy and credit reporting", "S22 anti-discrimination binding charges")

# ---------------- S0 routing ----------------
add("GOL 7-108(1), (1-a) opening", "state", "statute", R0,
    "7-108 governs every dwelling unit not referred to in 7-107 (rent-stabilized); subdivision 1-a excludes rent-controlled units and listed senior/care facilities.",
    "NY_GOL_7-108.txt", "1. This section shall apply to all dwelling units", "section 7-107 of this title.")
add("GOL 7-108(1-a) exclusions", "state", "statute", R0, "Subdivision 1-a does not reach city rent and rehabilitation law (rent control) units or listed facilities.",
    "NY_GOL_7-108.txt", "1-a. Except in dwelling units subject to the city rent and rehabilitation law", "emergency housing rent control law")
add("RPL 214 (Good Cause Eviction, covered housing)", "state", "statute", R2,
    "Good Cause Eviction reaches NYC market-rate housing unless an exemption applies (small landlord, owner-occupied, post-2009 construction, high-rent, etc.); decides whether a non-renewal ends the tenancy.",
    "REVIEW1_NY_RPL_214_nysenate.txt", "§ 214", "exempt")
add("RPL 215 (necessity for good cause)", "state", "statute", R2,
    "For covered housing, no landlord may remove, fail to renew, or otherwise end a tenancy without good cause.",
    "REVIEW1_NY_RPL_215_nysenate.txt", "No landlord shall, by action to evict", "as defined in section two hundred sixteen of this article.")

# ---------------- S1 move-in ----------------
add("GOL 7-108(1-a)(a)", "state", "statute", R1, "Deposit or advance may not exceed one month's rent (market-rate, not seasonal, not owner-occupied co-op).",
    "NY_GOL_7-108.txt", "(a) No deposit or advance shall exceed the amount of one month's rent", "one month's rent")
add("GOL 7-108(1-a)(c)", "state", "statute", R1,
    "Landlord must offer a pre-occupancy inspection; if requested, a signed condition agreement; conditions noted cannot be charged at move-out.",
    "NY_GOL_7-108.txt", "(c) After initial lease signing but before the tenant begins occupancy", "noted in such agreement.")
add("GOL 7-103(1)", "state", "statute", R4, "Deposit stays the tenant's money, held in trust, not commingled, not an asset of the recipient (incl. any agent who receives it).",
    "NY_GOL_7-103_nysenate.txt", "such money, with interest accruing thereon, if any, until repaid or so applied, shall continue to be the money", "become an asset of the person receiving the same")
add("GOL 7-103(2)", "state", "statute", R4, "If banked, written notice of bank name/address and amount to the tenant; NY bank; 1% per annum administration fee if interest-bearing; balance of interest belongs to tenant.",
    "NY_GOL_7-103_nysenate.txt", "2. Whenever the person receiving money so deposited or advanced shall deposit such money in a banking organization", "the amount of such deposit.")
add("GOL 7-103(2) administration fee", "state", "statute", R4, "If the deposit earns interest, the landlord may keep 1% per annum as administration expense in lieu of all other charges; the rest of the interest is the tenant's.", "NY_GOL_7-103_nysenate.txt", "If the person depositing such security money in a banking organization shall deposit same in an interest bearing account", "in lieu of all other administrative and custodial expenses.")
add("GOL 7-103(2-a)", "state", "statute", R4, "Buildings with six or more units: deposit must be in an interest-bearing NY account at the prevailing rate.",
    "NY_GOL_7-103_nysenate.txt", "2-a. Whenever the money so deposited or advanced is for the rental of property containing six or more family dwelling units", "in such area.")
add("GOL 7-103(3)", "state", "statute", R4, "Any lease waiver of 7-103 is void.", "NY_GOL_7-103_nysenate.txt", "3. Any provision of such a contract or agreement", "absolutely void.")
add("19 NYCRR 175.1", "state", "regulation", R4,
    "A licensed broker acting as managing agent must hold others' money (incl. tenant deposits) in a separate special account, never commingled.",
    "REVIEW4A_NY_19NYCRR_175.1_LII.txt", "A real estate broker shall not commingle the money or other", "special bank account")
add("RPL 238-a(1)", "state", "statute", R1, "No payment, fee or charge before or at the beginning of the tenancy except background/credit check capped at actual cost or $20.",
    "NY_RPL_238-A.txt", "or demand any other payment, fee or charge before or at the beginning of the tenancy", "credit checks as provided by paragraph (b) of this subdivision")
add("CPLR 4544", "state", "statute", R5, "Lease text printed below 8-point (5.5 upper case) cannot be received in evidence for the landlord who prepared it.",
    "REVIEW4A_NY_CPLR_4544_nysenate.txt", "The portion of any printed contract or agreement involving a consumer transaction or a lease for space to be occupied for residential purposes", "who caused said agreement or contract to be printed or prepared.")
add("RPL 235-bb", "state", "statute", R1, "Owners of 3 or fewer rental units must disclose in bold whether a required certificate of occupancy is valid before lease signing.",
    "REVIEW4A_NY_RPL_235-BB_nysenate.txt", "Prior to executing a residential lease or rental agreement with a", "currently valid for the dwelling unit subject to the lease or rental")
add("GOL 5-905", "state", "statute", R2, "An automatic-renewal clause in a lease is unenforceable unless the lessor gave the tenant written notice 15-30 days before the tenant's notice deadline.",
    "REVIEW1_NY_GOL_5-905_nysenate.txt", "No provision of a lease of any real property", "shall give to the tenant written notice")
add("NYC Admin Code 20-699.21 (FARE Act)", "city", "statute", R5,
    "Since 2025-06-11 a landlord (or its agent) may not impose on a tenant the fee of a broker who acts for the landlord; unlawful fees are recoverable by the tenant.",
    "NYC_ADC_20-699.21.txt", "20-699.21", "tenant")

# ---------------- S2 ending ----------------
add("RPL 232-c", "state", "statute", R2, "Holdover after a term longer than one month does not renew the term; landlord's acceptance of rent for a later period creates a month-to-month tenancy.",
    "NY_RPL_232-C.txt", "Where a tenant whose term is longer than one month holds over", "commencing on the first day after the expiration of such term.")
add("RPL 232-a", "state", "statute", R2, "NYC monthly tenant can be removed for holding over only after the 226-c notice period, served like a notice of petition.",
    "NY_RPL_232-A.txt", "No monthly tenant, or tenant from month to month", "the landlord will commence summary proceedings under the statute to remove such tenant therefrom.")
add("RPL 226-c", "state", "statute", R2, "Non-renewal or 5%+ increase requires 30/60/90-day written notice by occupancy length; late notice continues the tenancy on existing terms until the period runs.",
    "NY_RPL_226-C.txt", "If the landlord fails to provide timely notice, the occupant's lawful tenancy shall continue", "notwithstanding any provision of a lease or other tenancy agreement to the contrary.")
add("RPL 229", "state", "statute", R2, "Tenant who gives notice to quit and then holds over owes double rent while in possession.",
    "NY_RPL_229.txt", "If a tenant gives notice of his intention to quit the premises", "as the single rent.")
add("RPL 227-e", "state", "statute", R2, "Tenant vacating in breach: landlord must in good faith take reasonable, customary steps to re-rent; a new lease terminates the old lease and mitigates damages; landlord bears burden of proof.",
    "NY_RPL_227-E.txt", "if a tenant vacates a premises in violation of the terms of the lease, the landlord shall", "whichever is lower.")
add("Holy Props. v Kenneth Cole Prods., 87 NY2d 130 (1995)", "state", "case", R2,
    "Common-law rule where RPL 227-e does not reach the lease: landlord has no duty to mitigate after the tenant abandons.",
    "REVIEW4A_NY_CASE_HolyProperties_v_KennethCole_1995_CoA.txt", "If the lease provides that the tenant shall be liable for rent after eviction, the provision is enforceable", "arising under the lease")
add("14 E. 4th St. Unit 509 LLC v Toporek, 203 AD3d 17 (1st Dept 2022)", "state", "case", R8,
    "Failure to give the 7-108(1-a)(d) pre-vacate inspection notice does not forfeit the deposit; forfeiture attaches only to a missed (1-a)(e) statement.",
    "NY_CASE_Toporek_2022_203AD3d17.txt", "does not mandate forfeiture. The forfeiture penalty only applies to General Obligations Law § 7-108 (1-a) (e)", "which statement was indisputably provided here.")
add("Riverside Research Inst. v KMGA, 68 NY2d 689 (1986)", "state", "case", R2,
    "Surrender by operation of law requires conduct by both parties inconsistent with continuing the lease; the question decides when rent stops.",
    "REVIEW4A_NY_CASE_Riverside_v_KMGA_1986_CoA.txt", "A surrender by operation of law occurs when the parties to a lease both do some act so inconsistent", "intent to deem the lease terminated")
add("172 Van Duzer Realty v Globe Alumni, 24 NY3d 528 (2014)", "state", "case", R5,
    "Rent-acceleration clause is enforceable, but where the landlord keeps possession the tenant may show the accelerated sum is a disproportionate penalty.",
    "REVIEW4A_NY_CASE_172VanDuzer_v_GlobeAlumni_2014_CoA.txt", "Defendants are correct that an acceleration clause is subject to judicial scrutiny", "otherwise proscribed by the law.")
add("Truck Rent-A-Center v Puritan Farms 2nd, 41 NY2d 420 (1977)", "state", "case", R5,
    "Liquidated damages (e.g. lease-break fee) are enforceable only if actual damages were hard to estimate and the amount is not plainly disproportionate; otherwise a penalty.",
    "REVIEW4A_NY_CASE_TruckRent_v_PuritanFarms_1977_CoA.txt", "A contractual provision fixing damages in the event of breach will be sustained", "difficult of precise estimation.")
add("RPL 226-b(1)", "state", "statute", R2, "Tenant may not assign without consent; if landlord unreasonably withholds consent, landlord must release the tenant on 30 days' notice.",
    "REVIEW4A_NY_RPL_226-B_nysenate.txt", "a tenant renting a residence may not", "which release shall be the sole remedy of the tenant.")
add("RPL 226-b(2)", "state", "statute", R2, "Building of four or more units: tenant may sublet with consent not unreasonably withheld; landlord's silence 30 days = consent; tenant stays liable.",
    "REVIEW4A_NY_RPL_226-B_nysenate.txt", "Landlord's failure to send such a notice shall be deemed to be", "tenant's obligations under said lease.")
add("RPL 227", "state", "statute", R2, "If the premises are destroyed or made untenantable without the tenant's fault, the tenant may quit and surrender and owes no further rent.",
    "NY_RPL_227.txt", "§ 227", "rent")
add("RPL 227-a", "state", "statute", R2, "Tenant 62+ or disabled moving to care/family residence may terminate on notice; termination effective ~30 days after next rent due; liability ends then.",
    "NY_RPL_227-A.txt", "Such termination shall be effective no earlier than thirty days after the date on which the next rental payment", "is due and payable.")
add("RPL 227-c", "state", "statute", R19, "DV victim may terminate on written notice (termination date at least 30 days out; mailed notice deemed delivered 5 days after mailing) and is released from later rent.",
    "NY_RPL_227-C.txt", "The notice shall specify the termination date which shall be no earlier than thirty days after such notice is delivered.", "it shall be deemed delivered five days after mailing.")
add("RPL 236", "state", "statute", R16, "Estate of a deceased tenant may ask consent to assign/sublet; landlord silence 30 days = consent; unreasonable refusal releases the estate.",
    "NY_RPL_236.txt", "the executor, administrator or legal representative of a deceased tenant under such a lease, may request", "subletting of the premises demised thereby.")
add("RPL 236-a", "state", "statute", R16,
    "Estate may terminate the lease by notice (certified/registered mail) effective on notice plus surrender; estate owes rent and damages to termination but no penalty for short notice; co-tenant/guarantor consent required.",
    "REVIEW4A_NY_RPL_236-A_nysenate.txt", "the executor, administrator or legal representative of a deceased tenant under such a lease shall have the option to terminate", "surrenders possession of the premises.")
add("RPL 236-a (liability and notice)", "state", "statute", R16, "Estate stays liable for rent and damages to the termination date but not for short-notice penalties; notices by registered or certified mail, return receipt requested.", "REVIEW4A_NY_RPL_236-A_nysenate.txt", "Nothing in this section shall be construed to relieve the tenant's estate", "return receipt requested.")
add("50 USC 3955", "federal", "statute", R17, "Servicemember may terminate a residential lease on entering service/PCS orders; monthly lease ends 30 days after the next rent due date after notice; no early-termination charge; prepaid rent refunded within 30 days.",
    "US_50USC_3955.txt", "Rents or lease amounts paid in advance", "30 days")
add("NY Military Law 310", "state", "statute", R17, "State counterpart: person entering military service may terminate a lease; liability for rent after termination ends.",
    "NY_MIL_310.txt", "1. The provisions of this section shall apply to any lease covering premises occupied for dwelling", "entered military service")
add("RPAPL 1305", "state", "statute", R3, "After foreclosure, a successor must honor a market-rate tenant's lease (or 90 days) on the same terms and give notice of the new owner's name and address.",
    "REVIEW4A_NY_RPAPL_1305_nysenate.txt", "a successor in interest of residential real property shall provide written notice to all tenants", "(b) of the name and address of the new owner.")
add("Protecting Tenants at Foreclosure Act (12 USC 5220 note)", "federal", "statute", R3, "Federal floor after foreclosure: 90-day notice and lease honored; state law giving longer protection controls.",
    "REVIEW4A_US_12USC_5220_uscode_PTFA.txt", "the provision, by such successor in interest of a notice to vacate", "at least 90 days before the effective date of such notice")

# ---------------- S3 who is owed / who collects ----------------
add("GOL 7-105(1)-(2)", "state", "statute", R3, "On conveyance/foreclosure the deposit must be turned over within 5 days with certified/registered notice to the tenant; transferee then owes the refund.",
    "NY_GOL_7-105_nysenate.txt", "Turn over to his or its grantee or assignee", "name and address of such grantee, assignee, purchaser or receiver.")
add("GOL 7-108(2)", "state", "statute", R3, "A grantee with actual knowledge of a deposit not turned over is also liable to the tenant for deposit plus interest; 30-day no-record notice procedure.",
    "NY_GOL_7-108.txt", "the grantee or assignee of the leased premises shall also be liable to such tenant", "as to which such grantee or assignee has actual knowledge.")
add("RPL 223", "state", "statute", R3, "Grantee of the reversion takes the landlord's rights to rent and remedies under the lease.",
    "NY_RPL_223.txt", "The grantee of leased real property, or of a reversion thereof", "as his grantor or lessor had")
add("RPL 440 / 440-a", "state", "statute", R3, "Collecting rent for another for a fee is real estate broker activity requiring a DOS licence.",
    "SWEEP_NY_RPL_440_nysenate.txt", "collects or offers or attempts to collect rent", "rent")
add("RPL 442-d", "state", "statute", R3, "An unlicensed person cannot sue for compensation for broker services (including rent collection).",
    "SWEEP_NY_RPL_442-D_nysenate.txt", "§ 442-d", "licensed")
add("BCL 1312", "state", "statute", R10, "Unauthorized foreign corporation doing business in NY cannot maintain an action until authorized and fees paid.",
    "REVIEW3_NY_BCL_1312_nysenate.txt", "shall not maintain any action or special proceeding in this state", "unless and until")
add("LLC Law 808", "state", "statute", R10, "Unauthorized foreign LLC cannot maintain an action until it registers.",
    "REVIEW3_NY_LLC_808_nysenate.txt", "may not maintain any action", "in this state")
add("MDL 325(2)", "state", "statute", R10, "Multiple-dwelling owner that has not registered cannot recover rent for any period of non-registration (bar lifted on registration for later periods).",
    "REVIEW2_NY_MDL_325_nysenate.txt", "no rent shall be recovered", "registration")
add("NYC Admin Code 27-2107(b)", "city", "statute", R10, "Owner who fails to file a valid HPD registration is denied the right to recover possession for non-payment of rent until registered.",
    "REVIEW1_NYC_ADC_27-2107.txt", "b. An owner who is required to file a statement of registration", "during such period.")
add("MDL 302(1)(b)", "state", "statute", R10, "No rent is recoverable by the owner of a multiple dwelling occupied in violation of the certificate-of-occupancy requirement for the period of the violation.",
    "REVIEW2_NY_MDL_302_nysenate.txt", "b. No rent shall be recovered by the owner of such premises for said period", "for nonpayment of such rent.")
add("MDL 301", "state", "statute", R10, "A multiple dwelling may not be occupied without a certificate of compliance or occupancy.",
    "REVIEW2_NY_MDL_301_nysenate.txt", "No multiple dwelling shall be occupied in whole or in part until the issuance of a certificate", "all other applicable law")
add("MDL 302-a", "state", "statute", R10, "Rent-impairing violations uncorrected for six months after notice: tenants may deposit/withhold rent; no rent recoverable for that period.",
    "NY_MDL_302-A_nysenate.txt", "then for the period that such violation remains uncorrected after the expiration of said six months, no rent shall be recovered", "rent impairing violation exists")
add("RPAPL 778", "state", "statute", R3, "Where an RPAPL 7-A administrator is appointed, rents are paid to the administrator, not the owner.",
    "SWEEP_NY_RPAPL_778_nysenate.txt", "to demand, collect and receive the rents from the tenants")
add("CPLR 6401", "state", "statute", R3, "A court-appointed receiver takes possession and collects rents in place of the owner.",
    "SWEEP_NY_CPLR_6401_nysenate.txt", "(b) Powers of temporary receiver. The court appointing a receiver may authorize him to take and hold real and personal property, and sue for, collect and sell debts or claims")
add("Heintz v Jenkins, 514 US 291 (1995)", "federal", "case", R13, "A lawyer who regularly collects consumer debts through litigation is an FDCPA 'debt collector'.",
    "REVIEW4A_US_CASE_Heintz_v_Jenkins_1995.txt", "The Act does apply to lawyers engaged in litigation.")
add("15 USC 1692a(6)", "federal", "statute", R13, "FDCPA 'debt collector' covers those collecting debts owed another; excludes the creditor itself and a person collecting a debt not in default when obtained (e.g. a managing agent engaged before default).",
    "US_15USC_1692a.txt", "The term \"debt collector\" means any person", "owed or due or asserted to be owed or due another")
add("Romea v Heiberger, 163 F3d 111 (2d Cir 1998)", "federal", "case", R13, "Back rent is a 'debt' under the FDCPA; a lawyer's rent demand is a collection communication.",
    "US_CASE_Romea_v_Heiberger_1998.txt", "We therefore hold that, under the FDCPA, back rent is debt.")

# ---------------- S4 interest / custody at end ----------------
add("GOL 7-103(2-b)", "state", "statute", R4, "If the lease ends between bank interest dates, the landlord pays the tenant the interest it can collect at termination.",
    "NY_GOL_7-103_nysenate.txt", "2-b. In the event that a lease terminates", "at the date of such lease termination.")
add("Paterno v Carroll, 75 AD3d 625 (2d Dept 2010); Gihon v 501 Second St., 103 AD3d 840 (2d Dept 2013)", "state", "case", R8,
    "Commingling (inferred from a missing bank notice) forfeits the landlord's right to use the deposit for any purpose; tenant has an immediate right to its return even if the tenant breached.",
    "NY_CASE_Gihon_v_501SecondSt_2013_103AD3d840.txt", "The LLC failed to provide the plaintiff with written notice of the banking institution", "even if the plaintiff had breached the lease")
add("LeRoy v Sayers, 217 AD2d 63 (1st Dept 1995)", "state", "case", R3, "Commingling is a conversion: the tenant recovers the deposit immediately, and the tenant's own lease breach is no defense (1st Dept, binds NY and Bronx County courts).",
    "REVIEW4A_NY_CASE_LeRoy_v_Sayers_1995_1stDept.txt", "it has been uniformly held that a commingling constitutes a conversion", "immediate recovery of his deposit or advances.")

# ---------------- S5 charges ----------------
add("GOL 7-108(1-a)(b)", "state", "statute", R5, "Only reasonable, itemized costs for unpaid rent, damage beyond normal wear and tear, unpaid landlord-billed utilities, and moving/storage of belongings may be kept; never ordinary wear and tear or a prior tenant's damage.",
    "NY_GOL_7-108.txt", "(b) The entire amount of the deposit or advance shall be refundable", "damage caused by a prior tenant.")
add("GOL 7-108(1-a)(d)", "state", "statute", R5, "Within a reasonable time after notice of termination (unless tenant gave <2 weeks), written notice of right to a pre-vacate inspection; 48-hour notice; itemized proposed deductions; right to cure.",
    "NY_GOL_7-108.txt", "(d) Within a reasonable time after notification of either party's intention to terminate the tenancy", "before the end of the tenancy.")
add("GOL 7-108(1-a)(f)", "state", "statute", R5, "Landlord bears the burden of proving the reasonableness of any amount retained.",
    "NY_GOL_7-108.txt", "(f) In any action or proceeding disputing the amount", "reasonableness of the amount retained.")
add("RPL 238-a(2)", "state", "statute", R5, "Late fee only if rent is more than five days late and capped at $50 or 5% of monthly rent, whichever is less.",
    "NY_RPL_238-A.txt", "2. No landlord, lessor, sub-lessor or grantor may demand any payment, fee, or charge for the late payment of rent unless", "whichever is less")
add("RPL 238-a(2-a); GOL 5-328(3)(b) (L.2025 c.431)", "state", "statute", R5, "Dishonored rent check fee only if in the lease and capped at actual cost or $20, whichever greater, with substantiation on request.",
    "NY_RPL_238-A.txt", "2-a.", "dishonored")
add("RPL 235-g", "state", "statute", R7, "Landlord may not require electronic payment as the only method or charge a fee for choosing not to pay electronically.",
    "NY_RPL_235-G.txt", "A landlord shall not require a lessee or tenant to use an electronic billing and/or", "chooses not to use an electronic billing and/or payment system.")
add("RPL 234", "state", "statute", R9, "A lease fee clause for the landlord implies a reciprocal tenant right to fees; no attorney fees on a default judgment.",
    "NY_RPL_234.txt", "A landlord may not recover attorneys' fees upon a default judgment.", "void as against public policy.")
add("Graham Ct. Owner's Corp. v Taylor, 24 NY3d 742 (2015)", "state", "case", R9, "RPL 234 reciprocity applies to lease fee clauses broadly (including clauses keyed to the landlord's fees in any action), creating tenant fee exposure when a landlord's claim fails.",
    "REVIEW4A_NY_CASE_GrahamCourt_v_Taylor_2015_CoA.txt", "We hold that Real Property Law § 234, which imposes a covenant", "incurred in retaking possession.")
add("RPL 234-a", "state", "statute", R5, "Owner or agent may not assess a tenant any legal-services fee (attorney, court, notary, administrative) unless authorized by a court order; contrary agreement void.",
    "REVIEW4A_NY_RPL_234-A_nysenate.txt", "An owner, lessor or agent", "pursuant to a court order.")
add("RPL 235-i", "state", "statute", R5, "Fees for key reproductions are limited to reasonable cost.",
    "NY_RPL_235-I.txt", "A landlord shall not charge a tenant a fee for the reproduction of keys", "three times in a calendar year.")
add("RPL 235-b", "state", "statute", R5, "Warranty of habitability: a breach supports tenant abatement/counterclaim that reduces what the landlord may keep or recover.",
    "NY_RPL_235-B.txt", "§ 235-b", "habitation")
add("RPL 235-a", "state", "statute", R5, "Tenant who paid a utility's charge owed by the landlord may offset it against rent.",
    "SWEEP_NY_RPL_235-A_nysenate.txt", "§ 235-a", "rent")
add("NYC Admin Code 27-2013", "city", "statute", R5, "Owner must repaint dwelling units every three years (and on turnover); routine repainting is an owner cost, not tenant damage.",
    "NYC_ADC_27-2013.txt", "paint", "three years")
add("NYC Admin Code 27-2056.8", "city", "statute", R5, "On turnover the owner must remediate lead-based paint hazards and prepare surfaces; an owner statutory cost, not a tenant charge.",
    "NYC_ADC_27-2056.8.txt", "turnover", "owner")
add("NYC Admin Code 27-2017.5", "city", "statute", R5, "Upon turnover the owner must remove asthma triggers (clean, pest-free, mold) - owner statutory turnover work.",
    "NYC_ADC_27-2017.5.txt", "Prior to the reoccupancy of any vacant dwelling unit in a multiple dwelling, the owner shall", "provided by such owner to incoming occupants")
add("24 CFR 982.313", "federal", "regulation", R5, "HCV (Section 8) tenant in a private unit: owner may use deposit for unpaid rent/damages and must give the tenant a list of amounts; PHA not liable for amounts owed.",
    "US_24CFR_982.313.txt", "security deposit", "list")
add("24 CFR 982.311(b)", "federal", "regulation", R2, "HCV: HAP stops when the family moves out; owner may keep the HAP for the month the family moves out.",
    "US_24CFR_982.311.txt", "(d) Family move-out. (1) If the family moves out of the unit", "for the month when the family moves out of the unit.")
add("68 RCNY 10-14 (CityFHEPS)", "city", "rule", R3, "CityFHEPS: security-deposit voucher/payments and unit-damage claims run to DSS on its terms.",
    "NYC_RCNY68_10-14.txt", "(c) Landlords must accept the HRA security voucher in lieu of a cash security deposit", "additional security from the client.")
add("68 RCNY 10-14(e) (CityFHEPS move-out notice)", "city", "rule", R2, "CityFHEPS landlord must notify HRA within 5 business days of learning the household no longer lives in the unit.", "NYC_RCNY68_10-14.txt", "(e) Landlords must notify HRA within 5 business days of learning that the household no longer resides", "is being applied.")
add("HRA W-147N security voucher", "city", "guidance", R3, "Where HRA issued a security voucher instead of cash, claims for rent/damage go to HRA under the voucher's terms and deadline, not against a cash deposit.",
    "NYC_HRA_W-147N_SecurityVoucher_2025-05-07.txt", "This security voucher guarantees that the Human Resources Administration", "within three months after the tenant has vacated the apartment.")

# ---------------- S6 statement ----------------
add("GOL 7-108(1-a)(e)", "state", "statute", R6, "Within 14 days after the tenant vacates: itemized statement of the basis for any amount retained and return of the remainder; miss both -> forfeit any right to retain.",
    "NY_GOL_7-108.txt", "(e) Within fourteen days after the tenant has vacated the premises", "forfeit any right to retain any portion of the deposit.")
add("General Construction Law 25-a", "state", "statute", R6, "Where a period for doing an act ends on Saturday, Sunday or public holiday, the act may be done on the next business day.",
    "NY_GCN_25-A_nysenate.txt", "When any period of time, computed from a certain day", "next succeeding business day")
add("General Construction Law 20", "state", "statute", R6, "Day-count rule: exclude the day of the event, count the last day.",
    "NY_GCN_20.txt", "A number of days specified as a period from a certain day", "from which the reckoning is made.")
add("State Technology Law 305 (ESRA)", "state", "statute", R6, "Electronic records/signatures have the same force as paper unless a law requires otherwise.",
    "NY_STT_305.txt", "3. An electronic record shall have the same force and effect", "not produced by electronic means.")
add("Levine v Xu-Kehrli, 2026 NY Slip Op 50528(U) (App Term 1st Dept)", "state", "case", R8, "Binding in NY/Bronx County: no itemized statement within 14 days of vacatur -> deposit returned in full; separate property-damage counterclaim decided on its own proof.",
    "NY_CASE_Levine_v_XuKehrli_2026.txt", "return of the security deposit because defendant failed to provide plaintiff with an itemized statement", "(see Urban v Zipper")

# ---------------- S8 consequences ----------------
add("GOL 7-108(1-a)(g)", "state", "statute", R8, "Violation: actual damages; willful violation: punitive damages up to twice the deposit.",
    "NY_GOL_7-108.txt", "(g) Any person who violates the provisions of this subdivision", "twice the amount of the deposit or advance.")
add("CPLR 214(2)", "state", "statute", R11, "Three years for a liability, penalty or forfeiture created by statute (7-108(1-a)(g) punitive damages); contract refund claim stays six years (CPLR 213).",
    "REVIEW4A_NY_CPLR_214_nysenate.txt", "2\\. an action to recover upon a liability, penalty or forfeiture", "215;")
add("Gaidon v Guardian Life, 96 NY2d 201 (2001)", "state", "case", R11, "CPLR 214(2) governs where liability would not exist but for the statute; claims existing at common law keep their own period.",
    "REVIEW4A_NY_CASE_Gaidon_v_GuardianLife_2001_CoA.txt", "CPLR 214 (2) does not automatically apply", "recognized or implemented by statute")
add("GOL 7-109", "state", "statute", R8, "Attorney General may sue to enforce the deposit statutes (restitution, penalties).",
    "NY_GOL_7-109_nysenate.txt", "If it appears to the attorney general", "enjoin any violation or threatened violation thereof.")
add("CCA 1801", "state", "statute", R8, "NYC small claims up to $10,000; a tenant may sue the landlord there over a NYC tenancy regardless of the landlord's residence.",
    "REVIEW4A_NY_CCA_1801_nysenate.txt", "The term \"small claim\"", "situated within the city of New York.")
add("CCA 1812", "state", "statute", R8, "Business judgment debtor with three unpaid small-claims judgments who does not pay within 30 days of notice faces an action for treble damages plus fees.",
    "REVIEW4A_NY_CCA_1812_nysenate.txt", "(b) Where each of the elements of subdivision (a) of this section are present", "together with reasonable counsel fees")

# ---------------- S9/S10 pursuing ----------------
add("CCA 1809", "state", "statute", R10, "Corporations, partnerships, associations and assignees may not sue in small claims (they use commercial claims).",
    "REVIEW1_NY_CCA_1809_nysenate.txt", "no assignee of any small claim shall institute an action", "article")
add("CCA 1803-A", "state", "statute", R10, "Commercial claim on a consumer transaction needs a certified demand letter mailed at least 10 and not more than 180 days before filing.",
    "REVIEW1_NY_CCA_1803-A_nysenate.txt", "(i) that the claimant has mailed by ordinary first class mail to the party complained against a demand letter", "prior to the commencement of the claim")
add("CCA 1809-A", "state", "statute", R10, "Entity claimants limited to five commercial claims per calendar month with a verified certification; no assignee/collector suits.",
    "REVIEW4A_NY_CCA_1809-A_nysenate.txt", "(c) A corporation, partnership or association, which institutes an action", "in this part of the court.")
add("CPLR 3215(g)(3)", "state", "statute", R10, "Default judgment against a natural person on a contractual obligation needs an additional first-class 'personal and confidential' summons mailing at least 20 days before entry (not in small claims).",
    "REVIEW4A_NY_CPLR_3215_nysenate.txt", "When a default judgment based upon nonappearance is sought against a natural person in an action based upon nonpayment of a contractual obligation", "concerns an alleged debt.")
add("CPLR 3215(j)", "state", "statute", R10, "A clerk's default judgment requires an affidavit that, after reasonable inquiry, the statute of limitations has not expired.",
    "REVIEW4A_NY_CPLR_3215_nysenate.txt", "(j) Affidavit. A request for a default judgment entered by the clerk", "the statute of limitations has not expired.")
add("CPLR 3016(j)", "state", "statute", R10, "In a consumer-credit-transaction action the contract must be attached and eight items pleaded (original creditor, itemization, etc.) - applies only if the claim is a consumer credit transaction.",
    "REVIEW4A_NY_CPLR_3016_nysenate.txt", "(j) Consumer credit transactions. In an action arising out of a consumer credit transaction", "the following information shall be set forth in the complaint:")
add("CPLR 3015(e)", "state", "statute", R10, "Complaint on a claim arising from a business requiring a DCWP licence must plead the licence and number.",
    "SWEEP_NY_CPLR_3015_nysenate.txt", "(e) License to do business", "license")
add("50 USC 3931", "federal", "statute", R17, "Before any default judgment the plaintiff must file an affidavit stating whether the defendant is in military service.",
    "US_50USC_3931.txt", "affidavit", "military service")
add("NY Military Law 303(3)", "state", "statute", R17, "NY requires no non-military affidavit unless federal law does (it does: 50 USC 3931).",
    "REVIEW4A_NY_MIL_303_nysenate.txt", "3\\. Where a default judgment may properly be rendered", "where authorized by federal law.")
add("GOL 5-701(a)(2)", "state", "statute", R9, "A guarantor's promise to answer for the tenant's debt must be in a signed writing.",
    "REVIEW4A_NY_GOL_5-701_nysenate.txt", "2\\. Is a special promise to answer for the debt, default or miscarriage", "of another person;")
add("CCA 1810 / 1810-A", "state", "statute", R10, "Clerk may bar repeat or harassing small/commercial claims.",
    "REVIEW4A_NY_CCA_1810_nysenate.txt", "If the clerk shall find that the procedures of the small claims part are sought to be utilized by a claimant for purposes of oppression or harassment", "to prosecute the claim.")

# ---------------- S11 limitations / S12 interest ----------------
add("CPLR 213(2)", "state", "statute", R11, "Six years for contract claims (rent arrears, damages, deposit refund).",
    "NY_CPLR_213.txt", "2. an action upon a contractual obligation or liability", "express or implied")
add("CPLR 214-i", "state", "statute", R11, "Three years, and no revival by payment, for actions arising out of consumer credit transactions (credit extended to an individual).",
    "NY_CPLR_214-I.txt", "An action arising out of a consumer credit transaction where a purchaser, borrower or debtor is a defendant must be commenced within three years")
add("CPLR 105(f)", "state", "statute", R11, "'Consumer credit transaction' means a transaction in which credit is extended to an individual primarily for personal, family or household purposes.",
    "NY_CPLR_105.txt", "Consumer credit transaction", "household purposes")
add("DCWP SHIELD NOA (2026) statement on CPLR 214-i", "city", "guidance", R11, "DCWP reads rental arrears as outside 'consumer credit transactions', so payment may revive them.",
    "NYC_DCWP_SHIELD_NOA_2026.txt", "because certain types of debt are excluded from the definition of", "rental arrears")
add("CPLR 203(a)", "state", "statute", R11, "Limitations run from accrual to interposition of the claim.",
    "REVIEW4A_NY_CPLR_203_nysenate.txt", "The time within which an action must be commenced, except as otherwise expressly prescribed", "to the time the claim is interposed.")
add("GOL 17-101", "state", "statute", R11, "Only a signed written acknowledgment or promise restarts limitations (payment effect preserved).",
    "REVIEW4A_NY_GOL_17-101_nysenate.txt", "An acknowledgment or promise contained in a writing signed", "does not alter the effect of a payment of principal or interest.")
add("CPLR 210(b)", "state", "statute", R16, "Eighteen months after a debtor's death are excluded from the limitations period against the estate.",
    "REVIEW4A_NY_CPLR_210_nysenate.txt", "(b) Death of person liable.", "against his executor or administrator.")
add("CPLR 210(a)", "state", "statute", R16, "A deceased tenant's representative may sue within one year after death if the claim had not expired.",
    "REVIEW4A_NY_CPLR_210_nysenate.txt", "(a) Death of claimant.", "within one year after his death.")
add("50 USC 3936", "federal", "statute", R17, "Military service time is excluded from any limitations period for actions by or against the servicemember.",
    "REVIEW4A_US_50USC_3936_uscode.txt", "The period of a servicemember's military service may not be included", "heirs, executors, administrators, or assigns.")
add("NY Military Law 308", "state", "statute", R17, "State counterpart tolling limitations during military service.",
    "REVIEW4A_NY_MIL_308_nysenate.txt", "The period of military service shall not be included", "or against his heirs, executors, administrators, or assigns")
add("11 USC 108(c)", "federal", "statute", R15, "A limitations period that had not expired at the bankruptcy filing runs until at least 30 days after notice that the stay ended.",
    "REVIEW4A_US_11USC_108_uscode.txt", "(c) Except as provided in section 524 of this title", "as the case may be, with respect to such claim.")
add("CPLR 5001", "state", "statute", R12, "Prejudgment interest is recoverable as of right on contract damages (each item from its own date).",
    "NY_CPLR_5001_nysenate.txt", "Interest shall be recovered upon a sum awarded because of a breach of performance of a contract", "contract")
add("CPLR 5004", "state", "statute", R12, "Statutory interest 9%; 2% on judgments for consumer debt (unless the plaintiff is not a creditor of a consumer debt).",
    "REVIEW1_NY_CPLR_5004_nysenate.txt", "Interest shall be at the rate of nine per centum per annum", "shall be two per centum per annum")
add("50 USC 3937", "federal", "statute", R17, "Pre-service obligations bearing over 6% (interest incl. fees/charges) are capped at 6% during service on written notice; excess forgiven.",
    "REVIEW4A_US_50USC_3937_uscode.txt", "An obligation or liability bearing interest at a rate in excess of 6 percent per year", "in the case of any other obligation or liability.")
add("NY Military Law 323-a", "state", "statute", R17, "State 6% cap on pre-service obligations during service; 'interest' includes fees and other charges.",
    "REVIEW4A_NY_MIL_323-A_nysenate.txt", "As used in this section the term \"interest\" includes", "with respect to such obligation or liability.")

# ---------------- S13 collection conduct ----------------
add("15 USC 1692g", "federal", "statute", R13, "Debt collector must send a validation notice within five days of initial communication; must pause on timely dispute.",
    "US_15USC_1692g.txt", "Within five days after the initial communication", "written notice")
add("12 CFR 1006.34", "federal", "regulation", R13, "Reg F validation information (itemization date, itemization, dispute rights); model form safe harbor.",
    "US_12CFR_1006.txt", "(a) Validation information required — (1) In general.", "(A) In the initial communication")
add("12 CFR 1006.30(a)", "federal", "regulation", R21, "Debt collector may not furnish a debt to a consumer reporting agency before communicating with the consumer about it (passive reporting ban).",
    "US_12CFR_1006.txt", "1006.30", "consumer reporting agency")
add("15 USC 1692c / 1692d / 1692e / 1692f", "federal", "statute", R13, "Communication limits, no harassment, no false/misleading statements (incl. character or amount of debt), no collection of amounts not authorized by agreement or law.",
    "US_15USC_1692f.txt", "The collection of any amount", "permitted by law")
add("15 USC 1692i", "federal", "statute", R10, "A debt collector suing a consumer must sue where the consumer signed the contract or resides.",
    "US_15USC_1692i.txt", "judicial district", "resides")
add("15 USC 1692k", "federal", "statute", R13, "Civil liability: actual damages, statutory up to $1,000, fees; one-year limitations; bona fide error defense.",
    "US_15USC_1692k.txt", "(2)(A) in the case of any action by an individual", "not exceeding $1,000")
add("Avila v Riexinger & Assocs., 817 F3d 72 (2d Cir 2016)", "federal", "case", R13, "A collection notice stating a 'current balance' that is accruing interest or fees must disclose that the balance may increase.",
    "REVIEW4A_US_CASE_Avila_v_Riexinger_2016_2dCir.txt", "We hold that Section 1692e of the FDCPA requires debt", "interest and fees.")
add("GBL 601", "state", "statute", R13, "Principal creditors and their agents (not only collectors) may not use the listed abusive practices, including claiming rights they know do not exist.",
    "NY_GBL_601.txt", "No principal creditor, as defined by this article, or his agent shall:", "legally chargeable against the debtor")
add("GBL 601-a", "state", "statute", R13, "No representation that a family member must pay the debt contrary to the FDCPA.",
    "REVIEW4A_NY_GBL_601-A_nysenate.txt", "No principal creditors and/or debt collection agencies shall make any representation", "obligation to pay such debts.")
add("GBL 602", "state", "statute", R13, "GBL 601 violations: AG enforcement, civil penalties, misdemeanor.",
    "NY_GBL_602.txt", "any person who violates the terms of section six hundred one of this article is guilty of a misdemeanor", "separate offense.")
add("23 NYCRR 1.1 (DFS debt collection regulation)", "state", "regulation", R13, "DFS disclosure, substantiation and time-barred rules bind third-party debt collectors and debt buyers (not original creditors).",
    "REVIEW2_NY_23NYCRR_1.1_justia.txt", "Debt collector means any person engaged in a business the principal purpose", "in the name of the creditor")
add("NYC Admin Code 20-489, 20-490", "city", "statute", R13, "Debt collection agencies (principal purpose collection or regularly collecting for others; debt buyers) need a DCWP licence to collect NYC consumer debts.",
    "NYC_ADC_20-489.txt", "shall mean a person engaged in business the principal purpose of which is to regularly collect", "collecting debts for such creditor")
add("NYC Admin Code 20-493.1, 20-493.2", "city", "statute", R13, "Licensed collectors must give itemization, confirm payment schedules in writing, and not collect time-barred debt deceptively.",
    "NYC_ADC_20-493.1.txt", "a. In any permitted communication with the consumer, provide:", "v. the amount of the debt at the time of the communication.")
add("6 RCNY 2-190", "city", "rule", R13, "Licensed debt collection agency must provide documentation/itemization of the debt on request.",
    "NYC_RCNY6_2-190.txt", "2-190", "debt")
add("6 RCNY 2-191", "city", "rule", R13, "Current rule (repealed by SHIELD eff. 2027-01-01): SOL disclosure before collecting a time-barred debt.",
    "NYC_RCNY6_2-191.txt", "2-191", "statute of limitations")
add("6 RCNY 2-192", "city", "rule", R13, "Licensed agency must confirm any payment schedule or settlement in writing with specified content.",
    "REVIEW4A_NYC_RCNY6_2-192.txt", "(a) The written confirmation of the debt payment schedule or settlement agreement", "the conditions for satisfying the outstanding balance.")
add("6 RCNY 2-193", "city", "rule", R13, "Licensed agency record-keeping duties.", "REVIEW4A_NYC_RCNY6_2-193.txt", "2-193", "record")
add("6 RCNY 5-76 (definition in force until 2026-12-31)", "city", "rule", R13, "'Debt collector' = an individual who as part of the job regularly collects debts - reaches a landlord's or manager's own staff who regularly collect tenants' consumer debts.",
    "NYC_RCNY6_5-76.txt", "Debt collector. The term \"debt collector\" means an individual who, as part of his or her job, regularly collects", "alleged to be owed or due.")
add("6 RCNY 5-77 (in force until 2026-12-31)", "city", "rule", R13, "Conduct rules (contact times, frequency twice per 7 days, cease on request, language access) once debt collection procedures start.",
    "NYC_RCNY6_5-77.txt", "It is an unconscionable and deceptive trade practice for a debt collector to attempt to collect a debt", "except in accordance with the following rules:")
add("SHIELD Rule (6 RCNY 5-76/5-77 as amended, adopted 2026-02-26, effective 2027-01-01)", "city", "pending", R13,
    "From 2027-01-01 'debt collector' includes anyone regularly collecting its own debts, and 'debt collection procedures' include an original creditor's collection after demanding the full balance: mailed 5-day validation notice, e-contact consent, credit-reporting notice 14 days before furnishing, time-barred-debt notice.",
    "NYC_DCWP_SHIELD_NOA_2026.txt", "any person, including any natural person or organization, including a debt collection agency, who:", "to the person collecting or attempting to collect the debts.")
add("SHIELD Rule: debt collection procedures definition", "city", "pending", R13, "Original creditors are within 'debt collection procedures' from 2027-01-01.",
    "NYC_DCWP_SHIELD_NOA_2026.txt", "The term “debt collection procedures” means any attempt by [a debt collector] any person, including an original creditor", "demanded the full balance due.")
add("SHIELD effective-date notice (City Record 2026-07-22)", "city", "pending", R13, "SHIELD takes effect 2027-01-01, not 2026-09-01.",
    "NYC_CROL_DCWP_SHIELD_ChangeEffDate_2026-07-22.txt", "will go into effect on January 1, 2027", "not September 1, 2026")
add("NYC Admin Code 20-700", "city", "statute", R13, "Deceptive or unconscionable trade practices in collecting consumer debts are unlawful under the NYC Consumer Protection Law.",
    "NYC_ADC_20-700.txt", "No person shall engage in any deceptive or unconscionable trade practice", "or in the collection of consumer debts.")
add("GBL 604-aa, 604-bb (coerced debt, eff. 2026-06-17)", "state", "statute", R19,
    "On receiving a coerced-debt statement plus adequate documentation, a creditor must stop collecting within 10 business days, notify any CRA it reports to, and complete a review within 30 business days.",
    "REVIEW4A_NY_GBL_604-BB_nysenate.txt", "1. Within ten business days of receipt of the following, a creditor shall cease collection activities", "is coerced debt.")
add("GBL 604-aa(3)-(4) definitions", "state", "statute", R19, "'Coerced debt' covers household-purpose debts incurred under coercion in intimate/family relationships; 'creditor' includes the person owed and collectors.",
    "REVIEW4A_NY_GBL_604-AA_nysenate.txt", "4. \"Creditor\" means any person, firm, corporation or organization to whom a debt is owed", "debt collector as defined by section six hundred of this chapter")

add("L.2019 c.36 Part M, section 29 (effective dates)", "state", "statute", R0, "HSTPA Part M (7-108(1-a), 238-a, 227-e) took effect 2019-06-14 and applies to actions commenced on or after that date; one section applies only to leases entered or renewed 30 days after enactment - point-in-time branch per lease date.",
    "NY_L2019_c36_PartM.txt", "§ 29. This act shall take effect immediately and shall apply to actions and proceedings commenced on or after such effective date", "entered into on or after such date")

# ---------------- S14 unclaimed ----------------
add("Abandoned Property Law 1315(2)", "state", "statute", R14, "An amount deposited to secure performance that stays unclaimed three years after it became payable is abandoned property reportable to the Comptroller.",
    "NY_ABP_1315.txt", "shall be deemed abandoned property when: a. such amount is held or owing in this state", "for three years")
add("OSC property-type table (TR04 / MS11; AC06 is the banks' code)", "state", "guidance", R14, "A real-estate company holding deposits in escrow reports unclaimed amounts as TR04 (ABP 1315, three years); other holders report an unpaid refund as MS11 Refunds Due (three years); AC06 applies to banking institutions. [Corrected in Phase 2: first draft named AC06, which the table places under banks.]",
    "NY_OSC_unclaimed_property_type_table.txt", "TR04 1315 Escrow Accounts (held by real estate companies) 3 years")
add("Abandoned Property Law 1422", "state", "statute", R14, "Holder must mail notice to the owner of record before reporting abandoned property.",
    "REVIEW2_NY_ABP_1422_justia.txt", "1. Any holder of unclaimed funds which is not otherwise required", "written notice by first-class mail to each person appearing to be the owner")

# ---------------- S15 bankruptcy ----------------
add("11 USC 362(a)", "federal", "statute", R15, "Filing stays any act to collect a prepetition claim, including setoff of the deposit, without relief.",
    "US_11USC_362.txt", "any act to collect, assess, or recover a claim against the debtor", "commencement of the case under this title")
add("11 USC 541 / 542", "federal", "statute", R15, "The tenant's refund right is estate property; a holder must turn it over to the trustee (chapter 7) rather than pay the debtor.",
    "REVIEW1_US_11USC_542.txt", "(a) Except as provided in subsection (c) or (d) of this section, an entity", "value of such property")
add("11 USC 553", "federal", "statute", R15, "Mutual prepetition debts may be set off (subject to the stay).", "US_11USC_553.txt", "(a) Except as otherwise provided in this section and in sections 362 and 363 of this title, this title does not affect any right of a creditor to offset a mutual debt", "that arose before the commencement of the case")
add("11 USC 524(a)", "federal", "statute", R15, "Discharge enjoins collection of discharged prepetition debts.", "US_11USC_524.txt", "operates as an injunction", "debt")
add("11 USC 502(b)(6)", "federal", "statute", R15, "Lessor's claim for lease-termination damages is capped at the greater of one year's rent or 15% of the remaining term (max three years), plus unpaid rent at the earlier of petition or surrender.",
    "REVIEW4A_US_11USC_502_uscode.txt", "(6) if such claim is the claim of a lessor for damages resulting from the termination of a lease of real property", "any unpaid rent due under such lease, without acceleration, on the earlier of such dates;")
add("11 USC 1301(a)", "federal", "statute", R15, "Chapter 13: creditor may not collect a consumer debt from a co-debtor (co-tenant, guarantor) without stay relief unless the co-debtor became liable in the ordinary course of business.",
    "REVIEW4A_US_11USC_1301_uscode.txt", "(a) Except as provided in subsections (b) and (c) of this section, after the order for relief under this chapter", "converted to a case under chapter 7 or 11 of this title.")
add("11 USC 365(d)(1)", "federal", "statute", R15, "Chapter 7: an unexpired residential lease not assumed within 60 days is deemed rejected.",
    "REVIEW4A_US_11USC_365_uscode.txt", "(d)(1) In a case under chapter 7 of this title", "deemed rejected")

# ---------------- S16 death ----------------
add("SCPA 1301 (small estate)", "state", "statute", R16, "Estate of personal property of $50,000 or less may be settled by a voluntary administrator.",
    "REVIEW4A_NY_SCPA_1301_nysenate.txt", "A small estate is the estate of a domiciliary or a non-domiciliary", "$50,000 or less")
add("SCPA 1310(1)(a) (debts payable without administration)", "state", "statute", R16, "Payment without letters is limited to listed debts (bank deposits, wages, public payments, etc.); a landlord's deposit refund is not one, so it is paid to a fiduciary or voluntary administrator.",
    "REVIEW4A_NY_SCPA_1310_nysenate.txt", "(a) \"Debt\" means (i) money or securities payable on account of a deposit in a bank", "branch of a foreign banking corporation")
add("SCPA 1305", "state", "statute", R16, "A debtor who pays a voluntary administrator is discharged.", "REVIEW4A_NY_SCPA_1305_nysenate.txt", "The delivery by a voluntary administrator to a debtor", "shall constitute a complete release and discharge")
add("SCPA 1802", "state", "statute", R16, "Claims presented after 7 months from letters: fiduciary not liable for good-faith distributions made before presentation.",
    "REVIEW4A_NY_SCPA_1802_nysenate.txt", "If any claim is not presented within 7 months from the date of issue of letters, the fiduciary shall not be chargeable", "before such claim was presented.")
add("EPTL 11-1.1", "state", "statute", R16, "Fiduciaries may collect and receive the decedent's property and pay claims.",
    "SWEEP_NY_EPTL_11-1.1_nysenate.txt", "(A) To take possession of, collect the rents from and manage the same.")

# ---------------- S17 military (other) ----------------
add("50 USC 3951", "federal", "statute", R17, "No eviction of a servicemember's dependents from a residence at or below the adjusted rent ceiling during service without court order.",
    "US_50USC_3951.txt", "Except by court order, a landlord (or another person with paramount title) may not-", "occupied primarily as a residence")
add("SCRA rent threshold 2026 (91 FR / FR 2026-04689)", "federal", "guidance", R17, "The 2026 adjusted 3951 monthly-rent ceiling.",
    "US_FR_2026-04689_SCRA_rent_threshold.txt", "the maximum monthly rental amount calculated as of January 1, 2026, is $10,542.60.")

# ---------------- S18 disability / S22 discrimination ----------------
add("42 USC 3604(f)(3)(A)", "federal", "statute", R18, "Landlord must permit reasonable modifications at the tenant's expense and may condition them on the tenant restoring the interior at the end of the tenancy (reasonable wear excepted).",
    "US_42USC_3604.txt", "the landlord may where it is reasonable to do so condition permission for a modification on the renter agreeing to restore the interior of the premises", "reasonable wear and tear excepted")
add("24 CFR 100.203", "federal", "regulation", R18, "Restoration condition and interest-bearing escrow for restoration costs; no increased deposit for disability.",
    "US_24CFR_100.203.txt", "increase", "security deposit")
add("24 CFR 100.65(b)(1)", "federal", "regulation", R22, "Using different lease provisions, rental charges or security deposits because of a protected class is unlawful.",
    "REVIEW4A_US_24CFR_100.65_ecfr.txt", "(1) Using different provisions in leases or contracts of sale, such as those relating to rental charges, security deposits", "because of race, color, religion, sex, handicap, familial status, or national origin.")
add("NYC Admin Code 8-107(5)(a)(1)(b)", "city", "statute", R22, "NYC HRL bars discrimination in terms, conditions or privileges of rental (incl. deposits, charges, settlement) because of protected status or lawful source of income.",
    "REVIEW4A_NYC_ADC_8-107.txt", "(b) To discriminate against any such person or persons in the terms, conditions or privileges of the sale, rental or lease", "in connection therewith; or")
add("NYC Admin Code 8-102 'lawful source of income'", "city", "statute", R22, "Lawful source of income includes public/housing assistance (e.g., vouchers) whether paid to the landlord or the tenant.",
    "REVIEW4A_NYC_ADC_8-102.txt", "Lawful source of income. The term \"lawful source of income\" includes", "paid or attributed directly to a landlord.")
add("Executive Law 296(5)(a)(2)", "state", "statute", R22, "State HRL: owner or managing agent may not discriminate in the terms, conditions or privileges of a rental because of protected status, including lawful source of income and domestic-violence victim status.",
    "REVIEW4A_NY_EXEC_296_nysenate.txt", "(2) To discriminate against any person because of race, creed, color, national origin, citizenship or immigration status", "in the furnishing of facilities or services in connection therewith.")
add("RPL 227-d", "state", "statute", R19, "Landlord may not discriminate in terms or conditions of a tenancy because of domestic-violence victim status.",
    "REVIEW4A_NY_RPL_227-D_nysenate.txt", "(a) No person, firm or corporation owning or managing any building used for dwelling purposes", "(2) discriminate in the terms, conditions, or privileges of any such rental")

# ---------------- S20 tax ----------------
add("IRS Pub. 527 (security deposits)", "federal", "guidance", R20, "A refundable deposit is not the owner's income on receipt; any part kept is income in the year kept; a deposit to be used as final rent is advance rent.",
    "REVIEW4A_US_IRS_Pub527_2025.txt", "Don’t include a security deposit in your income when you receive it", "include the amount you keep in your income in that year.")
add("26 USC 6049(a)(2)", "federal", "statute", R20, "A person receiving interest as nominee and paying $10+ in a year to another files an information return (1099-INT) - reaches deposit interest passed to the tenant.",
    "REVIEW4A_US_26USC_6049_uscode.txt", "(2) who receives payments of interest (as so defined) as a nominee", "the name and address of the person to whom paid.")
add("26 USC 6050P(c)", "federal", "statute", R20, "Cancellation-of-debt reporting (1099-C) applies only to financial entities and agencies, so a landlord writing off a tenant balance files none.",
    "REVIEW4A_US_26USC_6050P_uscode.txt", "The term \"applicable entity\" means-", "an applicable financial entity.")

# ---------------- S21 data / credit reporting ----------------
add("15 USC 1681s-2(a)", "federal", "statute", R21, "Furnishers (a landlord reporting a balance) must report accurately, flag disputes, report the delinquency date, and investigate direct disputes.",
    "US_15USC_1681s-2.txt", "shall not furnish any information", "inaccurate")
add("12 CFR 1022.42 / 1022.43", "federal", "regulation", R21, "Furnisher accuracy/integrity policies and direct-dispute investigation duties.",
    "US_12CFR_1022.43.txt", "(a) General rule. Except as otherwise provided in this section, a furnisher must conduct a reasonable investigation of a direct dispute", "debt with the furnisher")
add("GBL 899-bb", "state", "statute", R21, "Anyone holding NY residents' private information (e.g., bank account numbers for refunds) must keep reasonable safeguards.",
    "REVIEW4A_NY_GBL_899-BB_nysenate.txt", "reasonable safeguards", "private information")
add("NYC Admin Code 26-3002(c) (Tenant Data Privacy Act)", "city", "statute", R21, "Smart-access buildings: a vacated tenant's reference data must be removed or anonymized within 90 days after permanent vacatur.",
    "REVIEW4A_NYC_ADC_26-3002.txt", "c. Reference data for any tenant who has permanently vacated a smart access building", "no later than 90 days after such tenant has permanently vacated such building.")

# ---------------- pending state bills ----------------
add("S947 / A3121 (2025-26): RPL 235-g amendment, passed Senate 2026-03-18 and Assembly 2026-05-13, not yet delivered", "state", "pending", R5,
    "If signed (effective immediately): no landlord fee for ACH rent payment; landlord must offer a fee-free payment method.",
    "REVIEW4A_NY_S00947_Assembly_2025-26.txt", "2. A landlord shall not assess any fee or other charge for the use of", "an automated clearing house payment for the payment of rent.")
add("S947 actions", "state", "pending", R5, "Passed both houses 2026; returned to Senate, not delivered to the Governor as of 2026-09-29.",
    "REVIEW4A_NY_S00947_Assembly_2025-26.txt", "03/18/2026PASSED SENATE", "05/13/2026passed assembly")
add("S9760 / A10182-A Consumer Debt Uniformity Act (passed both houses June 2026)", "state", "pending", R11,
    "If signed: replaces 'consumer credit transaction' with 'consumer debt' across CPLR provisions, bringing rent arrears within the 3-year limit, pleading and default-judgment rules.",
    "REVIEW3_NY_A10182_S9760_Assembly_actions_2026-09-29.txt", "06/02/2026 PASSED SENATE", "06/03/2026 passed assembly")

if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parent / "review4a_universe.json"
    if ERR:
        print("ERRORS:")
        print("\n".join(ERR))
    out.write_text(json.dumps(U, indent=1, ensure_ascii=False))
    print(len(U), "items written;", len(ERR), "errors")
