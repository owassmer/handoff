# Analysis workbook reproduction

The delivered workbook is `02_research/Property_Management_Analysis.xlsx` in the complete package.

`prepare_inputs.py` reads the decision and public-data CSV files and joins the decision sources. `build_analysis.mjs` creates the workbook with the public `@oai/artifact-tool` API. The commercial model is a single, editable vacant-unit readiness illustration; it is not a forecast or an empirical savings estimate.

Run the preparation script with Python 3, passing the extracted package's `02_research/` directory as its argument. Run the builder with the bundled Node runtime from a temporary folder whose `node_modules` symlink points to `CODEX_PRIMARY_RUNTIME_NODE_MODULES`. Pass the absolute path to `02_research/` as the builder's first argument and the desired output directory as its second argument. The builder reads `decisions.json`, `competitors.json` and `public_data.json` from the `research/` subdirectory. Choosing a separate output directory preserves the delivered workbook. Its default output path, retained for the original analysis workspace, is `deliverables/02_research/` beneath the first argument.

The builder includes independent arithmetic checks and changes/restores the owner share, time conversion, rent recovery and work volume. It also distinguishes a blank rent-recovery input from an explicit zero. The exported workbook was checked for native tables and cached formula-error cells. All six worksheets were visually reviewed. Recalculation was verified with artifact-tool; Excel desktop was unavailable for a native-application check.

`validation.json` and the inspection files record the checks. PNG files are visual QA previews, not separate deliverables. The independent public-data calculations are owned by `economic_calculations.py` and documented in `economics.md`, rather than duplicated inside this workbook builder.

The decision inventory sources are domain anchors. The taxonomy and automation hypotheses are original synthesis and should be validated with actual operators. Competitor capabilities and prices are vendor statements unless their evidence column says otherwise.
