# Broader prepared statutory-pointer evaluation

This is a fresh broader task test: 36 atomic selections, four source sections, three California code families (CCP, BPC, FIN). It is not representative jurisdiction-wide coverage, a human legal review, a candidate-discovery recall measurement, or a calibrated production policy. No Jev run was made and no prior model results or labels were consulted. The source-backed samples and author expectations were fixed before inference.

## Preparation and independence

Read HANDOFF_CONTEXT.md, the final statutory-pointer question, statutory.py and CONFIGURATION.md. Prior `prepared_tasks/*frozen/cases.json` files were inspected only to collect excluded source paths and inspect the schema/types/source_kind enum. All four source paths below were absent from those frozen inputs. This excludes previously evaluated prepared-task sections, not every source ever inspected: BPC 10176 and FIN 100001 had been read during the earlier, different legal-reference task assignment, and BPC 10176 was not selected into that earlier 48-case set. No earlier labels or results informed this selection. CCP 337 and 339 are newly read source sections for this author.

Full saved bodies of the four chosen source sections were read before preparing candidates, including exceptions, hierarchy locators, generic legal leads, and private-document references. Additional saved CCP 116.220, 116.221 and 116.231 bodies were read as possible sources but not selected; their pointers are outside this explicitly bounded inventory. No inventory completeness claim extends to those rejected source bodies or other files.

Source retrieval wrappers, hierarchy headings, section-number labels, and amendment-history trailers are outside the substantive body bounds below. They are not model passages and their historical citations are outside this inventory. All selected context and expression spans are exact Unicode slices of saved UTF-8 source bytes; all hashes and spans were verified. Every row uses source_kind `statute`. Paths, hashes, offsets and strata remain bookkeeping; selected context text contains no added source identifier.

## Meaning before dispatch

The operating use is to distinguish expressions naming statutory text from subjects discussed by that text, allowing the research agent to retain a dependency for retrieval and interpretation. The final question, native Noul, and its two criteria are unchanged. A positive answer does not resolve a target, validate a limitation period, decide licensing applicability, or authorize recovery.

Governing context was selected before inference by grammatical and legal relationship. CCP 337 uses full subdivisions for written-instrument, private-security, date, and limitation-period candidates, and the complete governing rescission sentence for the Insurance Code pointer. CCP 339 retains the opening limitations frame and full first numbered provision so its two adjacent statutory exceptions are independently visible. BPC 10176 retains the governing introductory scope sentence or full listed ground; notably `any provision` stays with its private agreement, and the licensed-person negative stays with its generic legal-language clause. FIN 100001 uses the licensing sentence, the opening exception/definition clause, the complete two-division licensing clause, the named-Act clause with hierarchy locator, or full subdivision (c) as appropriate. These are meaning-selected spans, not fixed token windows or contexts revised after model failure.

Adjacent distinct citations are separate atomic candidates, including CCP 339’s two exceptions, FIN’s Divisions 9/20 and their commencing Sections 22000/50000, and FIN’s Title 1.6C/Section 1788. A complete hierarchical locator can be one expression where it identifies one target (CCP subdivision 2 of Section 337 of this code); unrelated neighboring citations are never bundled into that expression. A selected subject next to a citation remains a negative rather than inheriting the passage’s positive status.

The 36 cases are grouped, not independent source draws: b001–b008 use CCP 337; b009–b013 use CCP 339; b014–b022 use BPC 10176; b023–b036 use FIN 100001. Author counts: {'YES': 21, 'NO': 15}. Reviewers should label the cases blind before reading author labels. No final freeze or adjudication is produced by this preparation step.

## Complete bounded pointer inventory

The tables enumerate every occurrence of an explicit statutory unit/name component in each chosen substantive body, preserving repeated occurrences. A composite target has multiple locator components, not multiple inferred legal rules. Listed components are traceable back to their complete saved body. Matching components were manually checked against the full bodies; enumeration uses a formatting regex only after the semantic reading, not as a discovery-recall claim. Case IDs indicate that a component occurs inside the exact selected expression. Retained entries were not dispatched because the bounded evaluation samples rather than exhaustively classifies all hierarchy locators and repeated references. None is silently treated as NO or dropped from the research inventory.

### CCP 337

Path: `jurisdictions/CA/texts/CA_CCP/337.txt`. Full substantive body: Unicode `520:2518`. Raw-file SHA-256: `5bb3e6711a498308b10a2086f3d692204288c3ac528501abf437341637264d53`.

| File span | Statutory pointer component | Dispatch or retention |
|---|---|---|
| `657:669` | `Section 336a` | b001 |
| `2109:2120` | `Section 359` | b005 |
| `2128:2142` | `Insurance Code` | b005 |
| `2279:2291` | `this section` | b006 |
| `2458:2470` | `this section` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `2506:2517` | `Section 360` | b007 |

### CCP 339

Path: `jurisdictions/CA/texts/CA_CCP/339.txt`. Full substantive body: Unicode `520:1833`. Raw-file SHA-256: `47cdfde7e502307c48fac9263fbff7d89827ba91d5ec8211c11f8959de6830a4`.

| File span | Statutory pointer component | Dispatch or retention |
|---|---|---|
| `657:669` | `Section 2725` | b009 |
| `677:692` | `Commercial Code` | b009 |
| `696:709` | `subdivision 2` | b010 |
| `713:724` | `Section 337` | b010 |
| `728:737` | `this code` | b010 |

### BPC 10176

Path: `jurisdictions/CA/texts/CA_BPC/10176.txt`. Full substantive body: Unicode `613:4542`. Raw-file SHA-256: `8f4c99930b5064ff5662b098e0803ac388514006b38a27cbf8e4c6e719c9e05a`.

| File span | Statutory pointer component | Dispatch or retention |
|---|---|---|
| `1080:1092` | `this chapter` | b014 |
| `1773:1786` | `Section 10131` | b015 |
| `2293:2305` | `this chapter` | b017 |
| `3201:3213` | `this section` | b019 |

### FIN 100001

Path: `jurisdictions/CA/texts/CA_FIN/100001.txt`. Full substantive body: Unicode `559:2492`. Raw-file SHA-256: `8d077a1bd90e6341f59c7acbf6c6213f8f8771b2880c97b576d39d0106f436e2`.

| File span | Statutory pointer component | Dispatch or retention |
|---|---|---|
| `681:694` | `this division` | b023 |
| `1210:1223` | `paragraph (2)` | b024 |
| `1225:1238` | `this division` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1298:1310` | `Section 1420` | b026 |
| `1342:1352` | `Division 9` | b027 |
| `1370:1383` | `Section 22000` | b028 |
| `1388:1399` | `Division 20` | b029 |
| `1417:1430` | `Section 50000` | b030 |
| `1463:1469` | `Part 1` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1487:1500` | `Section 10000` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1505:1515` | `Division 4` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1523:1552` | `Business and Professions Code` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1585:1613` | `Karnette Rental-Purchase Act` | b031 |
| `1615:1625` | `Title 2.96` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1643:1659` | `Section 1812.620` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1664:1670` | `Part 4` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1674:1684` | `Division 3` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1692:1702` | `Civil Code` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1791:1800` | `Article 1` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1818:1830` | `Section 2920` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1835:1844` | `Chapter 2` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1848:1856` | `Title 14` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1860:1866` | `Part 4` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1870:1880` | `Division 3` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1888:1898` | `Civil Code` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `1956:1970` | `Section 100005` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `2005:2015` | `Title 1.6C` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `2033:2045` | `Section 1788` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `2050:2062` | `Title 1.6C.5` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `2080:2095` | `Section 1788.50` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `2100:2106` | `Part 4` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `2110:2120` | `Division 3` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `2128:2138` | `Civil Code` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `2164:2177` | `paragraph (1)` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `2183:2196` | `This division` | b036 |
| `2254:2267` | `Division 12.5` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `2285:2298` | `Section 28100` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `2408:2418` | `Title 1.6C` | b034 |
| `2436:2448` | `Section 1788` | b035 |
| `2453:2459` | `Part 4` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `2463:2473` | `Division 3` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |
| `2481:2491` | `Civil Code` | Retained, undispatched: repeated pointer or hierarchy locator; bounded sample budget, not a negative finding. |

## Broad leads and nonstatutory references retained for the agent

- CCP 337(a): contract/obligation/liability, written instrument, deed of trust or mortgage, power of sale and security arrangement. Private-instrument negatives b002–b003 do not close investigation of those documents or governing law. Subdivision (b)’s book/account-stated/mutual-account categories and account-entry dates remain factual characterization/accrual leads; b004 judges a date expression only. Subdivision (c)’s rescission, fraud and mistake remain substantive research leads. Subdivision (d)’s suit/arbitration/proceeding and debt remain recovery facts and procedural leads; b008 only classifies the debt expression.
- CCP 339: private contracts, written instruments, title certificates/abstracts/guaranties and title insurance policies; loss/discovery dates; judgment enforcement, official acts/duties, and rescission/fraud/mistake. b011–b013 sample title/policy/duty subjects. Other terms are retained without dispatch because they are additional private/factual or broad doctrine leads, not necessary additional atomic selections within this sample.
- BPC 10176: private agreements, contractual provisions, escrow documents, written owner authorization, loan commitments, and consent; alleged misconduct and licensed actors. Selected private-document and actor expressions are b016, b018, b020–b022. In (m), `any section, division, or article of law`, `that section, division, or article of law`, and `that person’s licensing law` are all retained broad statutory leads. The first ranges over unspecified laws, the second refers conditionally back to them, and the last names no particular enactment. They are deliberately undispatched pending agent framing/resolution, rather than forced into an untested generic-expression policy by this two-criterion task. This omission is an explicit limit on breadth, not an absence of potentially consequential legal dependencies.
- FIN 100001(a): `federal law` is a broad governing-law lead, retained for the agent and not dispatched because it names no specific statute/unit. License, licensee, principal place of business, branch office, geographic operation and debtor location are factual/licensing subjects. Subdivision (b) retains institution types, licensed persons, trustee and nonjudicial-foreclosure subjects alongside the enumerated pointers. Subdivision (c)’s `covered commercial debt` and `covered commercial credit` are separately sampled defined-subject negatives b032–b033; their definition sources remain independent positives b034–b035. A negative subject classification cannot exclude the adjacent defining statute.

All other ordinary body wording is context or substantive conduct, not an omitted identified statutory target. Dates here are semantic temporal expressions in the operative text, including `the date of the last item`; no amendment-history date is inserted merely to obtain an easy negative. The dataset has no authored passages and no automatic candidate discovery evaluation. Source freshness/legal effect and jurisdiction-wide representativeness remain outside the test.

## Identities

Question SHA-256: `ee80128558fa375cdf724278f9fd15a2fc666b86384eb68583de92fab7097e86`.

Cases SHA-256: `53f5b60f211c6c3dbc4ef4db48150dc6ec610705393a377dbe631f801fe03acc`.

Only broader.cases.json, broader.author_labels.json and broader.design.md were written. Author labels remain separate from model inputs. A Noul majority comparison is an evaluation convention, not a calibrated confidence threshold or permission for unattended exclusion.
