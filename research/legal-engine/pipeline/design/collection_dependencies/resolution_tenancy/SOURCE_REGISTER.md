# Source register

Captured/reviewed October 1, 2026. `sources/manifest.json` supplies SHA256 hashes for local files. HTML/PDF originals are source captures; TXT files with web line markers are retrieval extracts, not complete downloaded originals. Old authoritative sources remain under `../tenancy/sources/` and its register/manifest.

| Local file(s) | Source and authority | Exact relied-on location |
|---|---|---|
| civ1788_2.html | Official current [Civil Code1788.2](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1788.2.) | subdivisions(b),(c),(e),(f), amendment footer |
| civ1530.html, civ1531.html, civ1532.html | Official [1530](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1530.), [1531](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1531.), [1532](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1532.) | entire short sections, novation definition/modes/contract rules |
| alexander.txt | California Supreme Court primary opinion mirrored by [Stanford](https://scocal.stanford.edu/opinion/alexander-v-angel-29487/) | source lines43–46, novation intent and proof |
| hagey_hodge_web.txt | Published California appellate original opinion PDF reproduced [Justia](https://cases.justia.com/california/court-of-appeal/2023-g061836.pdf?ts=1693420286) | Hagey PDFpp6–7/source lines126–173, alleged debt and postpaid energy |
| hagey_modification.txt | California appellate modification/rehearing order mirrored [Justia](https://law.justia.com/cases/california/court-of-appeal/2023/g061836m.html) | source lines47–51, September26,2023 replacement footnote2; no change in judgment |
| hodge_end.txt; hagey_hodge_web.txt | Federal district primary opinion mirrored [CaseMine](https://www.casemine.com/judgement/us/679c520418d9be759544d32c) | source lines139–153, credit elements and nonpayment; pleading dismissal, not final factual determination |
| pollice_web.txt, pollice_plans.txt, pollice_paymentplan_footnote.txt | Third Circuit primary opinion mirrored [FindLaw](https://caselaw.findlaw.com/court/us-3rd-circuit/1401570.html) | original household utilities/tax distinction; n.40/source lines495–498 explains FDCPA original obligation versus TILA payment-plan credit |
| fleming.pdf/.txt | [Official Ninth Circuit](https://cdn.ca9.uscourts.gov/datastore/opinions/2009/09/09/07-35979.pdf), published | 581F3d922,925–926; text205–277, nonconsensual tort origin |
| hawthorne.pdf/.txt | [Official Eleventh Circuit](https://media.ca11.uscourts.gov/opinions/pub/files/19976731.OPN.pdf), published | 140F3d1367,1371–1372; text403–438 distinguishes Brown rental transaction from independent tort |
| denicolo_web.txt, denicolo_end.txt | Federal district primary opinion mirrored [CaseMine](https://www.casemine.com/judgement/us/5f7acc3c4653d05df39f2bbc?target=amp_references) | ending source lines262–300: summary judgment Rosenthal analysis, evidentiary/default issues, not blanket credit holding |

## Recovery failures and contrary material

- Hagey raw Justia PDF download returned HTTP403. Web tool successfully read the full original eight-page PDF with page/line locations, captured locally in hagey_hodge_web.txt. The local evidence is that extraction, not a downloaded binary; do not claim an original binary was saved.
- DeNicolo raw PDF download from `https://www.consumerfinancialserviceslawmonitor.com/wp-content/uploads/sites/501/2021/05/Denicolo-v.-Hertz-Corp._-2020-U.S.-Dist.-LEXIS-181248.pdf` returned403. Primary opinion mirror successfully read/captured instead.
- Considered [PG&E and utility companies' 2021 DFPI licensing comment](https://dfpi.ca.gov/wp-content/uploads/sites/337/2022/10/PRO-05-21-Pacific-Gas-and-Electric-Company.pdf), p4, claiming utility charges are not credit. Search retrieval exposed the relevant passage; full original was not saved. This is party advocacy; not relied on to establish law. Its cited dishonored-check/overdraft/tow examples do not decide agreed postpaid household energy. Later published Hagey directly does.
- Secondary article naming Hagey served as discovery only. Its characterizations were replaced with reading the actual opinion. CaseMine/FindLaw page navigation and marketing text are not legal authority; only reproduced opinions are used.
- Brown was analyzed through the subsequent official Hawthorne opinion's explicit treatment; no independent Brown binary was retrieved. Findings distinguish the actual no-credit-requirement holding from Hawthorne's transaction explanation.
- Hodge Jan.29,2025 order is used as persuasive reasoning only. Search surfaced later April2025 proceedings concerning amended pleading/TCPA; no assertion of final judgment or ultimate merits is made from the January dismissal with leave to amend.
