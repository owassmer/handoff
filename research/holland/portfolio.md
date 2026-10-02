# Holland Residential portfolio fact sheet

As of 2026-09-30. Covers the 61 publicly listed community entries on hollandresidential.com (`communities.json`). Every community's facts, with sources, are in `portfolio.json`. Saved copies of the pages relied on are under `sources/`:
- `sites/`: community websites.
- `sightmap/`: each site's fee feed.
- `web/`: developer, press and agency pages.
- `wayback/`: archived Apartments.com listings.
- `snippets/`: search-result text, used only where the page blocked automated access.

Holland Partner Group says Holland Residential "manages over 60 communities in Arizona, California, Colorado, Oregon, and Washington" and backs each with "dedicated property-specific accountants".[1]

## Reconciliation and scope

Reconciled 2026-09-30. The feed is a marketing inventory, not an audited operating portfolio: **61 entries, including Sloane’s 442 planned units with spring 2027 move-ins** (`sources/recheck_sloane.txt`). The 18,608-unit subtotal includes that future delivery; excluding it leaves **18,166 known units**, still missing Quin & Nita’s combined total and subject to phased-building/count conflicts. Do not use either subtotal as an occupied-unit count or a move-out-volume estimate.

Postal/marketing city names are not legal jurisdictions. Census geography at the saved feed coordinates (`build/geocode_census.json`) puts **Summerwalk at Klahanie in Sammamish**, **550 Harborfront in Los Angeles (San Pedro neighborhood)**, and **The Flats at Inverness in unincorporated Arapahoe County (Inverness CDP), outside Englewood and Centennial**. `portfolio.json` retains `listed_city` and adds the source-backed jurisdiction result; `communities.json` remains the unmodified source feed. Parcel-level or multi-building boundary verification is still required where facts straddle a boundary.

Opening-year flags are preliminary age screens, not accepted legal applicability. Marketing fees are what the sites disclose, not a legal-compliance finding or the terms of any resident’s lease. Management does not establish ownership, and an older building does not establish a Holland acquisition. The origin table below has been corrected accordingly.

## How this was built and how complete it is

- **Community websites.** All 61 were crawled. Sixty are Holland-branded sites built on Razz; Meridian at Midtown still runs its previous operator's site. The page data names the resident portal and application link. It also embeds an Engrain SightMap map whose "Calculate My Cost" feed publishes the full fee schedule: application fee, deposits, pets, parking, each utility and how it is billed, insurance, and other charges.[11][12][13] That feed is the fee source for 57 communities.
- **Build year, units and ownership.** These come from developer, contractor and architect pages, business press, public agencies (Portland's MULTE list, the California AG) and Yardi Matrix. Archived Apartments.com listings add 25 snapshots.
- **Blocked listing sites.** Apartments.com, ForRent, Zillow, RentCafe and Apartment Finder block automated access. For those, only the search-result description was read, and those facts are marked `search_snippet` in the JSON.
- **County assessor records.** None were reached: the Maricopa and King County endpoints did not answer usable queries. Purchase years for older acquired buildings are therefore mostly missing (see Gaps).

| Field | Communities with a value (of 61) |
|---|---|
| units | 60 |
| year_built_or_opened | 61 |
| origin (developed/acquired/third-party) | 51 |
| acquired/sold year | 10 |
| affordable status (yes/no/no_evidence) | 56 |
| building type | 59 |
| stories | 56 |
| resident portal | 59 |
| fee schedule (any) | 58 |
| lease terms | 20 |
| renters insurance required | 57 |
| origin known (not "unknown") | 51 |
| affordable confirmed yes | 15 |
| security deposit amount | 56 |
| application fee amount | 58 |
| pet deposit/rent | 58 |
| parking prices | 56 |
| utility billing method | 57 |
| deposit alternative found | 0 |
| move-out/cleaning/damage schedule found | 0 |
| resident handbook/lease addendum found | 0 |

## Portfolio at a glance

| State | Communities | Units (known) | Communities with unit count missing |
|---|---|---|---|
| CA | 21 | 6,946 | 0 |
| WA | 19 | 5,794 | 0 |
| CO | 12 | 3,138 | 1 |
| OR | 8 | 2,530 | 0 |
| AZ | 1 | 200 | 0 |
| **Total** | **61** | **18,608** | 1 |

Unit counts include Sloane: 442 units in Seattle, still under construction, with 2027 move-ins. Coen & Columbia is counted at its 2022 figure of 202 units; the newer Coen North building adds an unpublished number. Quin & Nita has no reconciled combined total. Quin’s architect identifies 208 units and Holland Partners as client (`sources/quin_architect.txt`); earlier sources differ (Quin 207, planned Nita 225, listing Nita 215). A component or planned count is not a verified combined current total.

Units by city:

| City | Communities | Units (known) |
|---|---|---|
| Seattle, WA | 12 | 3,811 |
| Denver, CO | 8 | 1,890 + unknown |
| Hillsboro, OR | 4 | 1,803 |
| San Diego, CA | 5 | 1,481 |
| Oakland, CA | 5 | 1,480 |
| Los Angeles, CA (including San Pedro) | 4 | 1,271 |
| Santa Clara, CA | 1 | 724 |
| Portland, OR | 3 | 511 |
| Bothell, WA | 1 | 451 |
| Vista, CA | 1 | 410 |
| Bellevue, WA | 1 | 402 |
| Glendale, CA | 1 | 401 |
| Vancouver, WA | 2 | 388 |
| Sammamish, WA | 1 | 354 |
| Huntington Beach, CA | 1 | 346 |
| Duarte, CA | 1 | 344 |
| Westminster, CO | 1 | 332 |
| Lone Tree, CO | 1 | 316 |
| Unincorporated Arapahoe County, CO | 1 | 309 |
| Centennial, CO | 1 | 291 |
| Long Beach, CA | 1 | 271 |
| Mukilteo, WA | 1 | 235 |
| San Jose, CA | 1 | 218 |
| Beaverton, OR | 1 | 216 |
| Scottsdale, AZ | 1 | 200 |
| Renton, WA | 1 | 153 |

Building types:
- 31 mid-rise.
- 14 high-rise.
- 12 garden.
- 2 townhome (Inspiration; Savanna at Reed's Crossing).
- 2 not established.

34 communities are mixed-use (ground-floor retail or office). The portfolio is overwhelmingly new urban construction. 50 of 61 communities (15,306 units) opened in 2012 or later.

## Age, and which rent-cap and rent-control rules can apply

The new-construction exemptions key on the date of the first certificate of occupancy:
- California's AB 1482 exempts housing "issued a certificate of occupancy within the previous 15 years".[4]
- Oregon's cap exempts units whose first certificate of occupancy was "issued less than 15 years" before the rent-increase notice.[9]
- Washington's cap exempts units whose first certificate of occupancy "was issued 12 or less years" before the notice.[7] It limits increases to "seven percent plus consumer price index, or 10 percent, whichever is less".[8]

The table below uses opening year as a preliminary research screen. It does not establish first CO dates, exact anniversary days, unit-level affordability exclusions, phased development or accepted legal applicability. Read its “exempt” labels only as age-screen results.

| State | Test | Communities newer than the line | Units | At the line (borderline) | Older | Units older |
|---|---|---|---|---|---|---|
| CA | AB 1482: CO within 15 yrs | 21 | 6,946 | 0 (0 units) | 0 | 0 |
| OR | ORS 90.323: first CO <15 yrs | 7 | 2,033 | 0 (0 units) | 1 | 497 |
| WA | RCW 59.18.710: first CO 12 yrs or less | 14 | 4,468 | 2 (584 units) | 3 | 742 |
| CO | no statewide cap (15-yr view for reference) | 6 | 1,275 | 0 (0 units) | 6 | 1,863 |
| AZ | no statewide cap (15-yr view for reference) | 0 | 0 | 0 (0 units) | 1 | 200 |
| All | built within 15 years (opened 2012 or later) | 50 | 15,306 | - | 11 | 3,302 |

Buildings at or past the line:

| Community | City | State | Year | Units |
|---|---|---|---|---|
| Ezlyn Westminster | Westminster | CO | 1986 | 332 |
| Summerwalk at Klahanie | Sammamish | WA | 1991 | 354 |
| The Soleil | Centennial | CO | 1994 | 291 |
| Contour 39 | Lone Tree | CO | 1996 | 316 |
| Palladia | Hillsboro | OR | 1999 | 497 |
| Commons Park West | Denver | CO | 2000 | 339 |
| The Preserve at Cedar River | Renton | WA | 2001 | 153 |
| Inspiration | Scottsdale | AZ | 2002 | 200 |
| Bella Terra | Mukilteo | WA | 2002 | 235 |
| The District at Hampden South | Denver | CO | 2007 | 276 |
| The Flats at Inverness | Unincorporated Arapahoe County | CO | 2009 | 309 |
| Dimension | Seattle | WA | 2014 | 298 |
| True North | Seattle | WA | 2014 | 286 |

What the table shows:
- **California.** All 21 communities opened in 2013 or later, so their reported opening years fall inside the 15-year age window; exact exemptions require first CO and applicable unit/tenancy facts. The first to lose the exemption are 1111 Wilshire (opened 2013; about 2028), Meridian at Midtown (2014; about 2029), and The Brand and Preserve at Melrose (2015; about 2030).
- **Local rent control.** The reported construction dates fall after the cited older-building local rent-control cutoffs; this is an age screen, not a finding that all local tenant protections are inapplicable. The LA RSO covers pre-Oct 1978 buildings, Oakland's ordinance pre-1983, and San Jose's ARO pre-1979; Holland's buildings there date from 2013 to 2026. These thresholds are as given in the brief and were not re-checked here.
- **Washington.** Five communities’ opening years are beyond or at the age threshold; actual cap applicability also requires the law’s other conditions:
  - Summerwalk at Klahanie (1991), The Preserve at Cedar River (2001) and Bella Terra (2002) are beyond the new-construction age window.
  - Dimension and True North (both 2014) sit on the 12-year line in 2026.
  - Coen & Columbia includes the 82-unit Columbia building from 2002, so that phase is beyond the age window too.
  - The Villas at Beardslee was built in phases from 2014 to 2017, so its phases cross the line between 2026 and 2029.
- **Oregon.** Palladia (1999, 497 units) is beyond the new-construction age window. Orenco Station (about 2015) and Villas at Amberglen (2016-17) lose their exemption around 2030-2032.
- **Colorado and Arizona.** No statewide cap was found for these states' 13 communities (not re-verified here). Seven of them date from 1986-2009, where wear-and-tear arguments on move-out are more common.

## Who developed and who owns them

| Development/acquisition evidence | Entries | Known units |
|---|---|---|
| Holland development involvement | 40 | 12,428 |
| Reported Holland/JV acquisition | 6 | 1,714 |
| Other developer/owner; Holland management | 5 | 1,577 |
| Holland acquisition/ownership unestablished | 10 | 2,889 |

These categories describe the retrieved development/acquisition evidence, not current title. Quin is attributed to Holland by its architect; the combined Nita total remains unknown. Eight former “acquired” entries were downgraded because age, management or renovation did not prove acquisition. Esperanza’s seller leaves the buyer undisclosed; business press names Holland, so its “third_party” label must not be read as proof Holland has no ownership.

**Holland development involvement (40 entries; 12,428 known units plus unresolved Quin & Nita).** NASH is a documented repeat capital partner; no source-backed majority proportion has been established. Holland frequently sells after lease-up and keeps managing:
- Westlake Steps and One Lakefront were sold in 2017 to entities named "BPP Holland ..." (Blackstone Property Partners).[20]
- Kiara was sold to Oxford in 2020 and is now owned by Pontegadea.[31]
- The Ivey on Boren was sold to Sekisui House REIT; its filing names Holland Residential, LLC.[22]
- Savanna at Reed's Crossing sold to BGO for $160 million in August 2026.[23]
- The Ballard Independent sold for $152 million in August 2026.[24]
- The Society's Bradbury and Felix buildings went to Pacific Life, with Holland keeping a minority stake (search snippet only).

**Acquisitions and third-party management.** Mesirow is a repeat owner in the managed book:
- GID sold The District at Hampden South in January 2025;[28] the buyers were Mesirow and Holland together.[21] Mesirow's fund entity bought Commons Park West in January 2024.[30]
- Mesirow bought Preserve at Melrose from MG Properties in December 2024.[29]
- Holland sold The Villas at Beardslee to Mesirow in 2025.[21]
- Other Holland purchases: Bella Terra (with Principal, 2022),[27] Coen & Columbia (with EJF, 2020),[35] Ezlyn (formerly SoFi Westminster, 2019, search snippet), and Meridian at Midtown from Essex (mid-2026).[25]
- Contour 39 is an older asset Holland repositioned; it won a 2018 renovation award.[36]
- Five entries have evidence of another developer or owner; current equity interests are not uniformly established: Adera (Hurley),[34] Dimension (Heitman),[32] Esperanza at Duarte Station (built by MBK, sold 2026 to an undisclosed buyer),[33] Preserve at Melrose and Commons Park West (Mesirow).

**What this means for a sale:** for many communities the decision-maker on move-out economics is a separate owner (Blackstone, Mesirow, Pacific Life, Pontegadea, Heitman, BGO, Sekisui House REIT), with Holland Residential as operator.

## Affordable and income-restricted units

15 communities have confirmed income-restricted units:

| Community | City | Program(s) | What the source says |
|---|---|---|---|
| Adera | Vancouver, WA | Vancouver MFTE | Site: "Adera participates in Vancouver's Multifamily Tax Exemption (MFTE) program"; floor plans tagged "MFTE - Income Restricted"; MFTE prices include utilities. |
| The Ayer | Seattle, WA | Seattle MFTE | DJC: "Income-restricted rents are lower for the units covered by the city's multifamily tax exemption program"; site lists "Affordable" floor plans tagged "MFTE: Income Restricted". |
| The Lark Uptown | Oakland, CA | Oakland Below Market Rate (BMR) | Site: "proud to partner with the city of Oakland and take part in their Below Market Rate (BMR) program"; BMR waitlist page. Unit count not published. |
| Westlake Steps | Seattle, WA | Seattle MFTE | Floor plans labelled "MFTE" and tagged "MFTE: Income Restricted" on the site. |
| West SD | San Diego, CA | San Diego Housing Commission rent-set units | "Included will be 41 designated low-income units with rents set by the San Diego Housing Commission." |
| Orlo & Alba | Santa Clara, CA | Santa Clara Below Market Rate (BMR) | Site: takes part in Santa Clara's BMR program (waitlist closed). A housing listing says 90% of units are market-rate, implying about 10% BMR at 80%/100% AMI. |
| The Huxley | Seattle, WA | Seattle MFTE | Site: "In collaboration with Seattle's MFTE Program, The Huxley offers an extensive selection of income restricted MFTE apartment homes." |
| Coen & Columbia | Vancouver, WA | Workforce set-aside (20% of Coen), Income Restricted plans | "118-unit multifamily community with 20% of the units set aside for workforce housing"; site tags plans "Income Restricted". |
| The Torrey | San Diego, CA | On-site affordable units | BuildSD: "The tower also features 19 affordable units." |
| Vicino | Bellevue, WA | Bellevue MFTE, Land Use Code (LUC) affordable | Site: "offers a selection of income-restricted apartment homes through the MFTE and LUC programs". |
| The Ballard Independent | Seattle, WA | Seattle MFTE | Site MFTE page: "proudly participates in the Seattle Multifamily Property Tax Exemption (MFTE) program to supply rent-restricted homes". |
| The Rodney | Portland, OR | Portland MULTE | 48 MULTE units restricted at 80% of median income (10 studios, 32 one-bed, 6 two-bed); exemption expires June 30, 2030. |
| Sloane | Seattle, WA | Income-restricted (program not named; 60-85% AMI) | "442 new residential units, 90 of which are designated to serve residents between 60% and 85% AMI". |
| Paxton | Huntington Beach, CA | On-site low-income units (city approval condition) | "the approval of the project requires ... 20 percent of the apartments as low-income affordable units" (about 69 of 346). |
| Maestro | Portland, OR | Portland MULTE | 25 MULTE units at 80% of median income (9 studios, 12 one-bed, 4 two-bed); exemption expires June 30, 2030. |

- **Confirmed none.** The Society (Ruby, Bradbury, Felix) has no subsidized units; Holland paid San Diego $9.8 million in fees instead.[14] Dimension was built as all market-rate.
- **None found.** 37 communities show no income-restricted floor plans or program on their site or in the sources checked.
- **Unknown.** Five new CA/CO buildings (Hallasan, The Daphne, 550 Harborfront, Resa, The Deveraux) show no restricted plans online, and no covenant search was done.
- **No LIHTC or project-based Section 8 was found anywhere.** The restricted units are tax-exemption set-asides: MFTE in Seattle, Bellevue and Vancouver; MULTE in Portland.[15] The rest are city inclusionary/BMR or approval conditions: Oakland, Santa Clara, San Diego,[16][17] and Huntington Beach.[18] Sloane adds 90 units at 60-85% AMI when it opens.[19]
- **Fee rules differ for these units.** Holland's fee feed notes that "Certain fees may not apply to apartments under housing vouchers/affordable programs".[13] Hallasan waives the application fee for subsidized applicants.[11]

## Software and vendors seen across the portfolio

- **Yardi RentCafe** is the property-management and resident platform everywhere a portal link exists (59 communities). Resident logins sit at `*.securecafe.com/residentservices/...`, applications at `.../onlineleasing/...`, and the SightMap leasing provider is `yardi_rentcafe` on every feed. Meridian at Midtown's apply link is also RentCafe. The underlying accounting system is presumably Yardi Voyager; not confirmed.
- **Engrain SightMap** (unit map plus fee calculator): 57 communities.
- **Assurant renters insurance** (footer link `assurantrenters.com/Holland`): 57.
- **AnyoneHome** (lead handling; contact addresses `@leads.anyonehome.com`): 53.
- **MyShowing** (tour scheduling): 58.
- **EliseAI** (leasing AI): 16.
- **Snappt** (application-document fraud screening): 3.
- **NOVA Credit** (optional international-credit screening): offered in 43 fee feeds.
- **Parcel Pending** lockers: a $20 registration fee at 20 or more communities. Also Luxer One (2), ButterflyMX (1) and Tour24 (1).
- **Bilt Payments** link (`paywithbilt.com/Holland`): Preserve at Melrose only.
- **Meridian at Midtown** still uses the prior operator's Alfred app and Funnel chat.
- **Tenant screening:** the California AG's 2024 action says RealPage provided screening reports to Holland. RealPage paid $625,000; Holland accepted injunctive terms.[2]
- **Not found anywhere:** Entrata, RealPage/ActiveBuilding portals, ResMan, AppFolio, Conservice, or any deposit-alternative product (Rhino, LeaseLock, Obligo, TheGuarantors, Jetty). The Razz page code lists those vendors only as generic form options.

## Fee patterns (from the communities' own fee feeds)

| State | Communities with fee feed | Application fee | Base security deposit | Holding / approved-application deposit | Admin or move-in fee (where charged) | Pet deposit | Pet rent (monthly) | Utility-billing admin fee (monthly) | Porter / common-area fee (monthly) |
|---|---|---|---|---|---|---|---|---|---|
| CA | 21 | $50-$64.50 | $250-$1,500 | $200-$1,500 | - (0 of 21) | $99-$500 | $50-$75 | $2.60-$6 | $13.55-$49.38 |
| WA | 17 | $40-$50 | $300-$1,500 | $300-$500 | $200-$300 (7 of 17) | $100-$300 | $25-$50 | $4.15-$5 | $10-$18.18 |
| CO | 11 | $26.75 | $150-$500 | $150-$500 | $200 (3 of 11) | $300 | $35 | $4-$10 | - |
| OR | 8 | $26.75 | $300-$700 | $300-$700 | - (0 of 8) | $200-$400 | $30-$50 | - | - |
| AZ | 1 | $50 | $250 | $100 | $200 (1 of 1) | $200 | $50 | $4.15 | - |

- **Observed application fees vary by state; this is not a compliance conclusion.** California charges $64.50 at every Holland community with a feed; Meridian charges $50. Colorado and Oregon charge $26.75 everywhere. Washington charges $40-$50 and Arizona $50.
- **Deposits.** The base deposit is low, $150-$1,500, and nearly every feed says it "may increase up to 1 month's rent based on screening results" or similar. Three Portland communities (Strauss, Rodney, Maestro) list "1 Month's Rent" outright.[11]
- **Holding deposit.** Almost every community collects a "Holding Deposit" or "Approved Application Deposit" at approval, $100-$1,500, and credits it toward the move-in deposit.
- **Non-refundable move-in fees** appear in 11 communities, all outside California and Oregon: Adera (WA) $200.00 "Move In Fee (non-refundable)"; The Villas at Beardslee (WA) $300.00 "Move In Fee (non-refundable)"; Inspiration (AZ) $200.00 "Move In Fee"; The Preserve at Cedar River (WA) $300.00 "Move In Fee (non-refundable)"; The District at Hampden South (CO) $200.00 "Nonrefundable Administration Fee"; Bella Terra (WA) $300.00 "Move In Fee (non-refundable)"; Commons Park West (CO) $200.00 "Nonrefundable Administration Fee"; Coen & Columbia (WA) $200.00 "Move In Fee (non-refundable)"; Vicino (WA) $300.00 "Move In Fee (non-refundable)"; The Flats at Inverness (CO) $200.00 "Nonrefundable Administration Fee"; Summerwalk at Klahanie (WA) $300.00 "Move In Fee (non-refundable)".
- **Utilities are billed back, not included in rent.** Exceptions seen: Adera's MFTE prices include utilities, and a 2021 listing shows gas included at 1717 Webster.
  - RUBS appears in 56 fee feeds and usage-based submetering in 38 (usually water and sewer), for example "Apartment is sub-metered for water usage" and "Total cost divided between all occupied apts".[11]
  - Most communities have electricity billed directly by the provider.
  - A third-party billing fee applies almost everywhere: $2.60 in LA-area buildings, $4.15 in most, $4-$10 in Colorado, $4.70 at Meridian. The biller is not named.[12]
- **Porter / common-area charges.** Most California buildings add a flat monthly "Porter Service" charge ($13.55-$49.38). Washington buildings bill it by ratio.
- **Government pass-throughs.** LA buildings pass through the city's SCEP and Just Cause Ordinance fees ($5.41/month).[11] Oakland buildings pass through the gross-receipts rental tax ($13.95 per $1,000 of rent). Ezlyn passes through Westminster's $1.67 rental-registry fee.
- **Amenity/technology fees are rare:**
  - $10/month "Building Technology Fee" for Bluetooth locks and cameras at The Daphne, Paxton and Resa.
  - $35 per-lease "Amenity Fee" at Bella Terra.
  - $25/month package fee at Commons Park West.
- **Parking** runs $0-$660/month in California, $40-$500 in Washington, $0-$299 in Colorado and $35-$400 in Oregon.
- **Renters liability insurance** is required at 57 communities.[12] Meridian's fee guide adds an optional $15/month third-party "Damage Waiver Liability".[26]
- **Pets** carry a refundable deposit ($99-$500), $25-$75/month pet rent, and in some cases a one-time fee.
- **Lease terms** (20 archived listings): mostly 12-24 months. Older listings show 6-12 months.
- **No full move-out schedule, handbook or lease addenda was found in the checked public materials.** The crawl did not recover a move-out, cleaning or damage-charge schedule, a resident handbook, or lease addenda. The only published move-out-related terms are in Meridian's guide: tenant responsible "for any damages beyond normal wear and tear", early termination at "2X RENT + Concession Repayment", and $75 per access device.[26]

## Per-community summary

| Community | City, St | Units | Year | Origin | Type (stories) | Affordable | App fee | Deposit (base) | Admin/move-in fee | Utility billing |
|---|---|---|---|---|---|---|---|---|---|---|
| Inspiration | Scottsdale, AZ | 200 | 2002 | Unknown | townhome (2) | None found | $50.00 | $250.00 | $200.00 | RUBS, direct |
| Esperanza at Duarte Station | Duarte, CA | 344 | 2022 | Third-party (2026) | mid-rise (wrap) (5) | None found | $64.50 | $600.00 - $1000.00 | - | submeter, RUBS, direct |
| The Brand | Glendale, CA | 401 | 2015 | Developed | mid-rise (7), mixed-use | None found | $64.50 | $500.00 - $700.00 | - | RUBS, direct |
| Paxton | Huntington Beach, CA | 346 | 2025 | Developed | mid-rise (5) | Yes: On-site low-income units (city approval condition) | $64.50 | $300.00 - $700.00 | - | submeter, RUBS, direct |
| Resa | Long Beach, CA | 271 | 2025 | Developed | mid-rise (8), mixed-use | Unknown | $64.50 | $500.00 - $700.00 | - | submeter, RUBS, direct |
| 1111 Wilshire | Los Angeles, CA | 210 | 2013 | Developed | mid-rise (7), mixed-use | None found | $64.50 | $500.00 - $1000.00 | - | RUBS, direct |
| Hallasan | Los Angeles, CA | 375 | 2023 | Developed | high-rise (37), mixed-use | Unknown | $64.50 | $500.00 - $1000.00 | - | submeter, RUBS |
| The Daphne | Los Angeles, CA | 311 | 2026 | Developed | mid-rise (8), mixed-use | Unknown | $64.50 | - | - | submeter, RUBS, direct |
| 1717 Webster | Oakland, CA | 247 | 2021 | Developed | high-rise (25), mixed-use | None found | $64.50 | $500.00 - $800.00 | - | RUBS, direct |
| Forma | Oakland, CA | 223 | 2022 | Developed | high-rise (24) | None found | $64.50 | $600.00 - $800.00 | - | submeter, RUBS, direct |
| Lydian | Oakland, CA | 261 | 2021 | Developed | mid-rise (podium) (7), mixed-use | None found | $64.50 | $600.00 - $1500.00 | - | submeter, RUBS, direct |
| The Lark Uptown | Oakland, CA | 330 | 2024 | Developed | high-rise (16), mixed-use | Yes: Oakland Below Market Rate (BMR) | $64.50 | $250.00 - $400.00 | - | submeter, RUBS, direct |
| Vespr | Oakland, CA | 419 | 2022 | Developed | high-rise (18), mixed-use | None found | $64.50 | $300.00 - $500.00 | - | RUBS, direct |
| Bradbury at The Society | San Diego, CA | 173 | 2021 | Developed | mid-rise (7) | No | $64.50 | $550.00 - $950.00 | - | submeter, RUBS, direct |
| Felix at The Society | San Diego, CA | 282 | 2021 | Developed | mid-rise (7) | No | $64.50 | $550.00 - $950.00 | - | submeter, RUBS, direct |
| Ruby at The Society | San Diego, CA | 145 | 2023 | Developed | mid-rise (8) | No | $64.50 | $550.00 - $950.00 | - | submeter, RUBS, direct |
| The Torrey | San Diego, CA | 450 | 2026 | Developed | high-rise (34), mixed-use | Yes: On-site affordable units | $64.50 | $500.00 - $1200.00 | - | submeter, RUBS, direct |
| West SD | San Diego, CA | 431 | 2024 | Developed | high-rise (37), mixed-use | Yes: San Diego Housing Commission rent-set units | $64.50 | $500.00 - $1200.00 | - | submeter, RUBS, direct |
| Meridian at Midtown | San Jose, CA | 218 | 2014 | Acquired (2026) | mid-rise (4), mixed-use | None found | $50.00 | $500.00 | - | - |
| 550 Harborfront | Los Angeles (San Pedro), CA | 375 | 2020 | Developed | mid-rise (podium) (7), mixed-use | Unknown | $64.50 | $500.00 - $1000.00 | - | RUBS, direct |
| Orlo & Alba | Santa Clara, CA | 724 | 2025 | Developed | mid-rise (podium) (11), mixed-use | Yes: Santa Clara Below Market Rate (BMR) | $64.50 | $250.00 - $500.00; $500.00 - $1000.00 | - | submeter, RUBS, direct |
| Preserve at Melrose | Vista, CA | 410 | 2015 | Third-party (2024) | ? | None found | $64.50 | $500.00 | - | submeter, RUBS, direct |
| The Soleil | Centennial, CO | 291 | 1994 | Unknown | garden (3) | None found | $26.75 | $500.00 | - | submeter, RUBS, direct |
| 1880 Little Raven | Denver, CO | 161 | 2018 | Developed | mid-rise (7) | None found | $26.75 | $400.00 - $500.00 | - | submeter, RUBS, direct |
| Bromwell | Denver, CO | 170 | 2020 | Developed | mid-rise (8) | None found | - | - | - | - |
| Commons Park West | Denver, CO | 339 | 2000 | Third-party (2024) | mid-rise (4), mixed-use | None found | $26.75 | $500.00 | $200.00 | RUBS, direct |
| Quin & Nita | Denver, CO | ? | 2024 (phase dates unresolved) | Developed (Quin) | ? | None found | $26.75 | $500.00 | - | submeter, RUBS |
| Rosewind | Denver, CO | 209 | 2025 | Developed | garden (3) | None found | $26.75 | $500.00 | - | submeter, RUBS, direct |
| Sabine | Denver, CO | 361 | 2024 | Developed | garden (3) | None found | $26.75 | $500.00 | - | submeter, RUBS, direct |
| The Deveraux | Denver, CO | 374 | 2024 | Developed | mid-rise (8), mixed-use | Unknown | $26.75 | $300.00 - $500.00 | - | RUBS |
| The District at Hampden South | Denver, CO | 276 | 2007 | Acquired (2025) | mid-rise, mixed-use | None found | $26.75 | $300.00 | $200.00 | submeter, direct |
| The Flats at Inverness | Unincorporated Arapahoe County, CO | 309 | 2009 | Unknown | garden (3) | None found | $26.75 | $500.00 | $200.00 | RUBS, direct |
| Contour 39 | Lone Tree, CO | 316 | 1996 | Unknown | garden (2) | None found | $26.75 | $150.00 - $250.00 | - | submeter, RUBS, direct |
| Ezlyn Westminster | Westminster, CO | 332 | 1986 | Acquired (2019) | garden (3) | None found | $26.75 | $350.00 - $500.00 | - | submeter, RUBS, direct |
| The Miles at South Cooper Mountain | Beaverton, OR | 216 | 2024 | ? | garden (3) | None found | $26.75 | $300.00 - $700.00 | - | RUBS, direct |
| Orenco Station | Hillsboro, OR | 609 | 2015 | Developed | mid-rise (6), mixed-use | None found | $26.75 | $400.00 | - | RUBS, direct |
| Palladia | Hillsboro, OR | 497 | 1999 | Unknown | garden (3) | None found | $26.75 | - | - | submeter, RUBS, direct |
| Savanna at Reed's Crossing | Hillsboro, OR | 301 | 2025 | Developed | townhome (4) | None found | $26.75 | $300-1 month's Rent | - | RUBS, direct |
| Villas at Amberglen | Hillsboro, OR | 396 | 2017 | ? | garden (3) | None found | $26.75 | $500.00 | - | submeter, RUBS, direct |
| Maestro | Portland, OR | 124 | 2019 | Developed | mid-rise (6) | Yes: Portland MULTE | $26.75 | 1 Month's Rent | - | RUBS, direct |
| The Rodney | Portland, OR | 230 | 2019 | Developed | high-rise (16), mixed-use | Yes: Portland MULTE | $26.75 | 1 Month's Rent | - | RUBS, direct |
| The Strauss on Burnside | Portland, OR | 157 | 2017 | Unknown | mid-rise (6), mixed-use | None found | $26.75 | 1 Month's Rent | - | RUBS, direct |
| Vicino | Bellevue, WA | 402 | 2024 | Developed | mid-rise (9), mixed-use | Yes: Bellevue MFTE, Land Use Code (LUC) affordable | $46.00 | $300.00 | $300.00 | submeter, RUBS, direct |
| The Villas at Beardslee | Bothell, WA | 451 | 2015 | Acquired (2017) | mid-rise, mixed-use | None found | $46.00 | $300.00 | $300.00 | submeter, RUBS |
| Summerwalk at Klahanie | Sammamish, WA | 354 | 1991 | Unknown | garden (3) | None found | $46.00 | $300.00 | $300.00 | RUBS, direct |
| Bella Terra | Mukilteo, WA | 235 | 2002 | Acquired (2022) | garden (3) | None found | $46.00 | $300.00 | $300.00 | submeter, RUBS, direct |
| The Preserve at Cedar River | Renton, WA | 153 | 2001 | Unknown | garden (3) | None found | $46.00 | $300.00 | $300.00 | submeter, RUBS, direct |
| 1075 Lenora | Seattle, WA | 44 | 2026 | Developed | high-rise (44), mixed-use | None found | - | - | - | - |
| Dimension | Seattle, WA | 298 | 2014 | Third-party (2015) | high-rise (27), mixed-use | No | $50.00 | $400.00 | - | RUBS, direct |
| JUXT | Seattle, WA | 361 | 2016 | Developed | mid-rise (8), mixed-use | None found | $40.00 | $300.00 | - | submeter, RUBS, direct |
| Kiara | Seattle, WA | 461 | 2018 | Developed | high-rise (41) | None found | $40.00 | $500.00 | - | submeter, RUBS, direct |
| One Lakefront | Seattle, WA | 317 | 2017 | Developed | mid-rise (6), mixed-use | None found | $40.00 | $300.00 | - | submeter, RUBS, direct, flat fees |
| Sloane | Seattle, WA | 442 | 2027 | Developed | high-rise (45), mixed-use | Yes: Income-restricted (program not named; 60-85% AMI) | - | - | - | - |
| The Ayer | Seattle, WA | 454 | 2024 | Developed | high-rise (45) | Yes: Seattle MFTE | $40.00 | $500.00 - $1000.00 | - | submeter, RUBS, direct, flat fees |
| The Ballard Independent | Seattle, WA | 238 | 2024 | Developed | mid-rise (podium), mixed-use | Yes: Seattle MFTE | $50.00 | $300.00 | - | submeter, RUBS, direct |
| The Huxley | Seattle, WA | 119 | 2019 | Developed | mid-rise (7), mixed-use | Yes: Seattle MFTE | $45.00 | $300.00 | - | submeter, RUBS, direct |
| The Ivey on Boren | Seattle, WA | 406 | 2022 | Developed | high-rise (44), mixed-use | None found | $40.00 | $500.00 - $1500.00 | - | submeter, RUBS, direct |
| True North | Seattle, WA | 286 | 2014 | Developed | mid-rise (8), mixed-use | None found | $40.00 | $500.00 | - | submeter, RUBS, direct |
| Westlake Steps | Seattle, WA | 385 | 2017 | Developed | mid-rise (6), mixed-use | Yes: Seattle MFTE | $40.00 | $300.00 | - | submeter, RUBS, direct |
| Adera | Vancouver, WA | 186 | 2024 | Third-party | mid-rise (6), mixed-use | Yes: Vancouver MFTE | $50.00 | $300.00 - $500.00 | $200.00 | RUBS |
| Coen & Columbia | Vancouver, WA | 202 | 2020 | Acquired (2020) | mid-rise (6), mixed-use | Yes: Workforce set-aside (20% of Coen), Income Restricted plans | $50.00 | $300.00 | $200.00 | RUBS, direct |

## What this means for settlement law and for Handoff

- **Four state regimes, plus city overlays, and Holland is operating in all of them.**
  - California (21 communities, about 6,900 units): itemized statement within 21 days.[3] For tenancies starting on or after July 1, 2025, photos at move-in and again after the tenant leaves, before repairs or cleaning.[3] The deposit cap is one month's rent,[3] which matches Holland's "up to 1 month's rent" deposit language.
  - Washington (19 communities, about 5,800 units): full and specific statement within 30 days,[5] and deductions only for items documented in the written move-in checklist.[6]
  - Oregon (8 communities, about 2,500 units): written accounting within 31 days.[9]
  - Arizona (1): itemized list within 14 business days after the tenant's demand, and security capped at one and a half months' rent.[10]
  - Colorado (12 communities, about 3,100 units) is the fifth regime; its deadline (one month, extendable to 60 days by lease) was not re-fetched and is [unverified].
  - A single playbook will not fit. The job is choosing the right rule set per building, and sometimes per unit (MFTE, MULTE and BMR units have fee exceptions).
- **The typical settlement is a small deposit plus unbilled charges.** Base deposits are $300-$1,000 against rents of $2,000-$6,000. Utility true-ups (RUBS and submeter) and third-party billing, pet charges and parking are the variable items. Those need reconciling against the deposit in a legally compliant statement, which is the part Handoff owns.
- **The paper trail runs through Yardi RentCafe.** Resident ledgers, move-in/move-out records and the fee schedule live in Yardi and SightMap. There is no deposit-alternative or surety vendor to work around.
- **Newer buildings mean fewer depreciation disputes, not no disputes.** 50 of 61 communities opened in 2012 or later, so most units are near original finish. The 11 pre-2012 communities (six in Colorado, three in Washington, Palladia in Oregon, Inspiration in Arizona) are where wear-and-tear arguments will concentrate.
- **Who signs.** Holland often manages for other owners (Blackstone, Mesirow, Pacific Life, Pontegadea, Heitman, BGO, Sekisui House REIT). A pilot must satisfy both Holland operations and, for some buildings, the owner's asset manager.
- **Compliance history is a hook.** California's AG obtained injunctive terms against Holland over tenant screening in 2024.[2] Holland's own fee disclosures read as built to comply with price-transparency rules. Both suggest a buyer that responds to regulatory risk.

## Gaps and what was tried

- **Acquisition year unknown** for Contour 39, Inspiration, The Preserve at Cedar River, The Strauss on Burnside (probably formerly "Aura Burnside"), The Flats at Inverness, The Soleil, Summerwalk at Klahanie and Palladia.
  - Tried: search for sale press, archived listings, and the Maricopa and King County assessor endpoints (no usable response).
  - Next step: county recorder deed searches in Douglas, Maricopa, King, Multnomah, Arapahoe and Washington (OR) counties.
- **Developer or owner unknown** for Villas at Amberglen (2017 sale seen only as a CompStak snippet) and The Miles at South Cooper Mountain. Quin development involvement is now supported by its architect, but the combined Quin & Nita unit count remains unresolved.
- **Current owner unconfirmed** for 1111 Wilshire, The Brand, True North, JUXT, The Rodney (listed for sale in Nov 2024) and The Huxley (listed with JLL).
- **Affordable-unit counts** are not published for the Seattle, Bellevue and Vancouver MFTE buildings, Oakland's Lark, or Orlo & Alba (about 10% by one listing). No covenant searches were run for Hallasan, The Daphne, 550 Harborfront, Resa or The Deveraux.
- **No fee feed** for 1075 Lenora, Bromwell or Sloane (no SightMap embed; Sloane not leasing).
- **Lease terms** exist only in 20 archived listings; RentCafe's term pricing is behind Cloudflare.
- **Not recovered from checked public sources:** move-out or damage schedules, resident handbooks, lease addenda, and the utility biller's name.
- **Conflicting unit counts** are recorded in the JSON notes. Examples: One Lakefront (317 vs 236/320/326), The Ayer (454 vs 430), Vespr (419 vs 405/437), Meridian (218 vs 224), Maestro (124 vs 128).
- **Litigation not pursued:** a 2025 federal case, Nicherie v. Holland Partner Group and 2016 Telegraph Owner, LLC (Forma), appears on a docket listing; its subject was not established.

## Sources

[1] https://www.hollandpartnergroup.com/services — Holland Partner Group - Services
    > "Holland Residential, which manages over 60 communities in Arizona, California, Colorado, Oregon, and Washington"
    > "dedicated property-specific accountants"
[2] https://oag.ca.gov/news/press-releases/attorney-general-bonta-secures-625000-settlements-realpage-and-holland-violating — CA AG: settlements with RealPage and Holland
    > "RealPage must pay $625,000 in penalties and restitution, and both RealPage and Holland must comply with strong injunctive terms"
[3] https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1950.5 — Cal. Civ. Code 1950.5
    > "No later than 21 calendar days after the tenant has vacated the premises"
    > "For tenancies that begin on or after July 1, 2025, the landlord shall take photographs of the unit immediately before, or at the inception of, the tenancy"
[4] https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12 — Cal. Civ. Code 1947.12 (AB 1482)
    > "Housing that has been issued a certificate of occupancy within the previous 15 years"
[5] https://app.leg.wa.gov/RCW/default.aspx?cite=59.18.280 — RCW 59.18.280
    > "Within 30 days after the termination of the rental agreement and vacation of the premises"
[6] https://app.leg.wa.gov/RCW/default.aspx?cite=59.18.260 — RCW 59.18.260
    > "Written checklist required"
[7] https://app.leg.wa.gov/RCW/default.aspx?cite=59.18.710 — RCW 59.18.710
    > "the first certificate of occupancy was issued 12 or less years before the date of the notice of the rent increase"
[8] https://app.leg.wa.gov/RCW/default.aspx?cite=59.18.720 — RCW 59.18.720
    > "up to seven percent plus consumer price index, or 10 percent, whichever is less"
[9] https://www.oregonlegislature.gov/bills_laws/ors/ors090.html — ORS chapter 90
    > "within 31 days after the tenancy terminates and the tenant delivers possession the landlord shall give to the tenant a written accounting"
    > "The first certificate of occupancy for the dwelling unit was issued less than 15 years from the date of the notice of the rent increase"
[10] https://www.azleg.gov/ars/33/01321.htm — A.R.S. 33-1321
    > "more than one and one-half month's rent"
    > "Within fourteen days, excluding Saturdays, Sundays or other legal holidays"
[11] https://sightmap.com/embed/r5v51yd3wny — Hallasan - SightMap fee feed
    > "Apartment is sub-metered for water usage"
    > "Total cost divided between all occupied apts"
    > "City of LA: SCEP Fee, $2.83; JCO Fee, $2.58"
    > "May increase up to 1 month's rent based on screening results"
[12] https://sightmap.com/embed/d7p1mkm8pkx — The Ayer - SightMap fee feed
    > "Resident must maintain liability renter's insurance"
    > "Third party monthly trash billing fee"
[13] https://sightmap.com/embed/40vl5rorwle — Adera - SightMap fee feed
    > "Move In Fee (non-refundable)"
    > "Certain fees may not apply to apartments under housing vouchers/affordable programs"
[14] https://www.sandiegouniontribune.com/2022/06/16/the-society-a-mission-valley-apartment-complex-with-37k-rent-finishes-3rd-tower-with-plans-for-a-4th — SD Union-Tribune on The Society
    > "Holland Partner Group did not include any subsidized housing in The Society project"
    > "The company had to pay the city $9.8 million in fees for not including rent-restricted units"
[15] https://www.portland.gov/phb/documents/multiple-unit-limited-tax-exemption-multe-unit-list/download — Portland MULTE unit list (April 2026)
    > "The Rodney fka 14th & Glisan"
    > "Maestro (PKA: NW 17th & Kearney)"
[16] https://www.hollandpartnergroup.com/blog/holland-partner-group-west-grand-opening — HPG: West opens
    > "Included will be 41 designated low-income units with rents set by the San Diego Housing Commission"
[17] https://buildsd.org/projects/front-and-a — BuildSD: The Torrey
    > "The tower also features 19 affordable units"
[18] https://la.urbanize.city/post/346-apartments-debut-18750-delaware-street-huntington-beach — Urbanize LA: Paxton
    > "20 percent of the apartments as low-income affordable units"
[19] https://www.weberthompson.com/thought/sloane-high-rise-milestone — Weber Thompson: Sloane
    > "90 of which are designated to serve residents between 60% and 85% AMI"
[20] https://www.djc.com/news/re/12106961.html — DJC: Holland, NASH sell Westlake Steps
    > "The buyers were BPP Holland One Lakefront LLC and BPP Holland Marina SLU LLC"
[21] https://curiousdeal.substack.com/p/curious-deal-s2e23?triedRedirect=true — Curious Deal S2E23
    > "Buyer: Mesirow Financial, Holland Partner Group"
    > "Seller: Holland Partner Group | Buyer: Mesirow Financial"
[22] https://sekisuihouse-reit.co.jp/file/en-term-c5a40e9d9f187913e0186b4b06984de536366bda.pdf — Sekisui House REIT: Ivey on Boren acquisition
    > "Holland Residential, LLC"
[23] https://crenews.com/2026/08/20/bgo-pays-160mln-for-portland-area-apartment-property — CRE News: BGO buys Savanna
    > "has paid $160 million"
[24] https://www.myballard.com/2026/08/05/ballard-independent-apartment-building-sells-for-152-million — My Ballard: Ballard Independent sells
    > "sold for $152 million"
[25] https://www.rentv.com/content/multifamily/mainnews/news/34177 — RentV: Holland buys Meridian at Midtown
    > "Holland Partner Group has purchased Meridian at Midtown, a 218-unit luxury apartment complex in San Jose"
[26] https://canva.com/design/DAHPp34-vVY/V4e05ZnZVELgCr6kDPhYnw/view — Meridian at Midtown Resident Fee Guide
    > "Required to select one of the following deposit options"
    > "You are required to maintain insurance as specified in the lease and are responsible for any damages beyond normal wear and tear"
[27] https://www.multifamilybiz.com/pressreleases/15156/cbre_arranges_67_million_in_financing_for_recapita... — CBRE: Bella Terra recap
    > "Holland Partners Group and Principal Real Estate Investors, which recently purchased the property"
[28] https://www.denverpost.com/2025/01/15/hampden-south-apartments-sold-housing-real-estate — Denver Post: Hampden South sale
    > "sold by GID, a real estate company based in Boston, to Mesirow Financial"
[29] https://sdbj.com/real-estate/vista-apartment-sale-among-highest-in-ca — SDBJ: Preserve at Melrose sale
    > "was sold by MG Properties Group based in Sorrento Valley to Mesirow Institutional Real Estate Direct Investments"
[30] https://businessden.com/2024/01/19/the-pipeline-commercial-real-estate-deals-for-1-19-24 — BusinessDen: Commons Park West sale
    > "MFREVF IV Commons LLC purchased the Commons Park West apartme"
[31] https://en.wikipedia.org/wiki/Kiara_%28building%29 — Wikipedia: Kiara
    > "Kiara was sold by Holland in 2020 to Oxford Properties"
    > "who acquired the building in 2022"
[32] https://www.woodpartners.com/wood-partners-sells-dimension-seattle — Wood Partners sells Dimension
    > "sold to Heitman Real Estate Investment Management"
[33] https://www.mbk.com/2026/02/26/mbk-rental-living-sells-la-county-luxury-apartment-community — MBK sells Esperanza
    > "Opened in November 2022, Esperanza at Duarte Station is a five-story community with a total of 344"
[34] https://hurleydev.com/projects/adera-apartments-400-washington-st — Hurley: Adera
    > "Adera Apartments is a 6-story, 258,281sf mixed-use apartment complex"
[35] https://www.connectcre.com/stories/holland-ejc-jv-acquires-pair-of-vancouver-mfs-for-63m — Connect CRE: EJF/Holland buy Coen & Columbia
    > "118-unit multifamily community"
[36] https://milehighcre.com/apartment-association-of-metro-denver-announces-2018-tributes-awards — AAMD 2018 Tributes
    > "Most Impactful Renovation to a Community: Contour 39, Holland Partner Group"
