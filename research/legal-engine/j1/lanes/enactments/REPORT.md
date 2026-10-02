# California enactments proposal — October 1, 2026

The proposed register combines selected current-code units with separate enactments where the enacted version, a transition, deferred operation, or uncodified authority matters. A chaptered act is not necessarily effective or operative. Whole-act acquisition entries are explicitly `source_unit_kind: document`; their internal sections remain for J2 subdivision and later temporal treatment.

## Integration files

- `instruments_2026.json`: 385 selected regular-session 2026 acts, with exact official bill-text targets, official status provenance, scope reasons and known specific timing evidence. Preserve these alongside current code because the current code may display a different operative version.
- `instruments_prior.json`: 17 selected earlier acts: four extraordinary budget acts; six regular 2025 budget acts; AB414, AB628, AB863 and SB655 from 2025; AB1572 (2023), AB2579 and AB2801 (2024). These preserve actual uncodified appropriations, future duties or relevant transition/history text. They do not replace consolidated current code.
- `bill_decisions.json`: individual dispositions for all 4,262 AB/SB entries in the official session inventory. The embedded `instrument_proposal` for an earlier ordinary amendment is a source description, **not an instruction to integrate every earlier act**. Only the two instrument files above are proposed additions.
- `prior_representation.json`: explicit current-code versus separate-act representation for selected 2025 enactments.
- `timing_and_prior_selections.json`: affected units and bill-specific timing/version evidence. This is also embedded in the proposed instruments.
- `reconciliation.json`, `session_inventory.json`, `chapters_2025.json`: source census and reconciliation. `selection_groups.json` and `scope_exclusions.json` record authored scope decisions; `build_proposal.py` only transcribes them.

## Session and status basis

The complete [official 2025–26 session search table](https://leginfo.legislature.ca.gov/faces/billSearchClient.xhtml?author=All&house=Both&lawCode=All&session_year=20252026) was captured through its final line (`sources/leginfo-session-*.txt`). It contains 5,065 measures: 5,064 parsed ordinary measures and GRP-1, referred to the agency lane. The enacted-bill census contains 1,830 regular-session bills and four 2025 first-extraordinary-session bills.

The complete [Secretary of State 2025 chapter index](https://admin.cdn.sos.ca.gov/bill-chapters/2025/Chapter-Number.pdf) identifies all regular chapters 1–790 (`sources/chapters-2025-*.txt`). Subtracting those exact identities from the regular chaptered inventory leaves 1,040 regular 2026 enacted bills. This establishes year without an introduced-year shortcut. The earlier 797 Governor announcement candidates and 177 early-year IDs form a nonoverlapping union of 974; 185 now-established 2026 chaptered bills were absent from that union. The earlier bullet parser also omitted prose-announced SB895. The Governor's 1,160 headline action total is corroboration, not the scope or completion criterion; the lane does not claim it has rebuilt an independently complete annual veto count.

No AB/SB row in the full table is enrolled, passed or pending Governor. Rows labeled passed are resolutions. The 31 Senate unfinished-business bills comprise 30 Governor-announced vetoes and SB1446. The latter is explicitly awaiting concurrence in Assembly amendments in the [Senate final daily summary](https://www.senate.ca.gov/system/files/2026-09/sds-8-31-2026.pdf), page 13 (`sources/sb1446-official-final-summary.txt`, lines 545–547). It is not a both-house-passed same-text bill. SB1238's individual official history corroborates the different veto-return meaning of unfinished business. No vetoed or one-house-passed bill becomes operative law in this proposal.

The extraordinary-session sources establish four 2025 budget enactments, individually retained for uncodified conditional recovery, legal-services or fee-payment authority. Their geographic and program conditions remain explicit. The 2024 second-extraordinary AB1 and 2023 first-extraordinary SB2 sources concern petroleum-market supply/pricing controls, and are excluded as additional residential-work/account enactments. Generally applicable current code remains separately represented. Earlier ordinary enactments are not re-added en masse: current code, including its future versions and annotations, supplies their continuing codified law. The three selected 2023–24 acts preserve concrete landscaping, inspection and deposit-evidence transitions.

## Consequential timing and source decisions

- SB1296 adds CIV 1942.7.5 with express April 1, 2027 operation. AB863 sets a January 1, 2027 Judicial Council summons-implementation deadline. These are different temporal events.
- SB417 is effective as an urgency enactment on June 25, 2026, but its sections 2 and 3 require voter adoption at the November 3 election. Approval is not assumed as of October 1.
- AB1795's LAB 6713 requires proposed worker-protection regulations by July 1, 2029. SB655 includes future agency consideration of indoor-temperature policy. Neither is represented as an already adopted regulation.
- AB1817, AB2689 and AB2559 were inspected through their complete captured text and have no special urgency/operative clause; the ordinary GOV 9600 default points to January 1, 2027, subject to later legislation. Other selected acts carry no invented uniform operative date.
- AB2596's official history establishes 2026 chapter 953, but the successful text response still displayed its August 17 enrolled version. It adds CIV 798.14.5. Status and captured-version evidence are deliberately separate; the exact official record is the acquisition target, and chaptered-version verification remains a J2 acquisition requirement.
- Successful `billNavClient` recoveries for AB863, SB1296 and extraordinary acts contain actual bill text. They are not navigation-shell substitutes. Acquisition has confirmed its adapter distinguishes the two.

## Scope judgment and limits

The selected acts cover housing/tenancy, physical-work permissions and standards, providers and utilities, accounts and civil remedies, and conditional housing/program effects. Mixed omnibus headings remain generously selected where embedded relevant provisions are plausible. Exclusions remove unrelated clinical practice, school instruction, separate industrial programs, criminal matters and named non-target geography; they do not exclude generally applicable codified law. Most individual decisions are heading-based instrument selections, not claims that every internal provision has been semantically adjudicated. Actual timing claims above are based on inspected source text.

The proposal is ready for coordinator review and canonical integration. The coordinator retains the substantive cross-lane completion judgment. J2 must acquire the selected documents and distinguish their internal legal sections and versions; J4 must evaluate operative branches against facts. Neither later task is claimed complete by this register. The report does not turn search nonresults into proof that no older law can ever have a material transition; current selected code preserves future versions and annotations, with the concrete older exceptions identified here.
