# Property management: research and action resources

Research cutoff: **15 September 2026**. Two groups separate the practical recommendation from the material needed to inspect and challenge it.

## 1. Playbook and field resources

Start with `01_playbook/Property_Management_Playbook.pdf` (13 pages). It connects the full operating picture to a provisional business: taking responsibility for getting vacant homes ready, initially through an existing operator and its approved trades. The first week compares actual work across several opportunities before committing to that starting point.

`01_playbook/Field_Guide.pdf` (6 pages) supplies the interview, case review, provider comparison, pilot terms, measurements and decision gates. The blank CSVs and `Template_Instructions.md` turn those exercises into usable working records. Editable Markdown versions accompany both PDFs.

The mission is simple: **keep homes working and ready to live in, without constant chasing.** The service, buyer and initial scope remain hypotheses to test against real work and payment.

## 2. Research, operating model and calculations

Read `02_research/Research_and_Operating_Model.pdf` (24 pages) for the evidence synthesis, recommendation changes, economic tests, and complete operating-model narrative. Its appendix covers parties, flows, concurrent lifecycles, transitions, exceptions, segment differences and decision families.

Open `02_research/Property_Management_Analysis.xlsx` to change commercial assumptions and examine the decision and market inventories. Its six worksheets contain:

| Worksheet | Use |
|---|---|
| Economics | Monthly buyer value and provider contribution; traceable formulas |
| Assumptions | Editable illustration with units and definitions |
| Sensitivity | Effects of captured value, delivery effort and additional collected rent |
| Decisions | 115 decision records across 17 families, with triggers, choices, authority, dependencies and questions to validate |
| Competitors | 38 entries: 37 current providers plus Mezo's acquired lineage |
| Public data | 106 descriptive estimates and source records |

Change the blue input cells on Assumptions. Green figures link to other worksheets. Preserve the distinction between zero and unknown. The baseline assumes an integrated owner/operator; changing owner value captured to zero shows the much weaker economics of a fee manager paying from its own margin. Released staff time only becomes cash value at the entered realization share.

The workbook is an illustration, not a forecast, quote or measured pilot result. Formulas were recalculated and changed-input cases tested with the spreadsheet engine; cached formula errors were checked and all six sheets visually reviewed. Excel desktop was unavailable for an application-specific check. Details are in `research/workbook/validation.json`.

### Supporting corpus

All paths below are relative to `02_research/research/`.

| File or group | What it supports |
|---|---|
| `attachment_review.md` | Full review of the three supplied attachments; retained ideas, rejected assumptions and consequential source corrections |
| `automation_evidence.md` | Forbes and Palantir audits, cross-industry studies, automation implications and limits |
| `market_products.md`, `competitors.csv`, `market_source_audit.csv` | Market synthesis, detailed provider comparisons and 75 opened primary market-source pages |
| `operating_model.md`, `operating_*.csv` | Parties, flows, lifecycles, branches, segment distinctions and source anchors |
| `decision_inventory.csv`, `decision_family_index.csv` | The complete decision register and its family index |
| `economics.md`, `public_data.csv`, `economic_outputs.json` | Independent public-data analysis, definitions, limitations and commercial calculations |
| `rhfspuf2024.csv`, `Codebook-Version-1.pdf`, `rhfs_verification.xls` | Retained Census microdata, documentation and published verification controls |
| `Review_Findings_and_Resolutions.md` | Substantive challenges to the draft and changes made before delivery |
| `workbook/` | Workbook source, normalized inputs documentation and validation records |

The broad model includes residential, commercial, association and specialist property operations. The quantitative research is deepest in US residential. The 115 records are a structured inventory of decision families and recurring decisions, not a claim that every local fact pattern or jurisdiction has been enumerated. Source anchors support particular domain facts; the taxonomy itself is synthesis.

### Reproducing the calculations

With Python 3 installed, run:

```bash
python3 02_research/research/economic_calculations.py
```

The script uses the standard library and the bundled raw CSV. It verifies all five Census size-stratum controls and regenerates descriptive outputs and the illustrative scenarios beside itself. Network access is needed only if the raw file is absent or `--download` is requested. The Census frame, disclosure modifications, missing values, property-versus-unit weighting and lack of new confidence intervals are documented in `economics.md`.

To rebuild PDFs, install ReportLab and the DejaVu Sans fonts in the path named by `build_reports.py`, then run that script. It reads the editable Markdown in this package and overwrites the three PDFs. To rebuild the workbook, follow `research/workbook/README.md`; its authoring dependency is `@oai/artifact-tool` and the documented Codex runtime. The delivered XLSX does not require that dependency to open or edit.

The competitor and decision builder scripts preserve the curated research records. They reconstruct the inventories; they do not refresh the web research. Run `build_competitors.py` followed by `extend_competitors.py` to reconstruct the final provider inventory.

### How to interpret the evidence

Public observations, vendor claims, reported studies, independent calculations and proposed business assumptions are identified separately. The work does not include customer interviews, private-system access, binding provider quotes, paid demand or live operating outcomes. The next evidence to obtain is specified in the playbook and Field Guide. The recommendation should change if that evidence favors another opportunity.
