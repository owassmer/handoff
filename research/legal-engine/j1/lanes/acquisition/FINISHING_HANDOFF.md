# Acquisition finishing handoff

`cornell_ccr` takes a unit's verified `toc_url` at a selected division or narrower hierarchy. Title roots are rejected. It recursively follows descendant hierarchy links and collects same-title `N-CCR-section` leaves, deduplicating the mirror's repeated Compare links. An empty branch fails enumeration. The verified source examples are title 25/division 1, its chapter 3.5, and section 4900. Focused fixtures exercise those relationships; no full live CCR hierarchy was harvested.

Generated leaves carry `source_authority: mirror`. Section acquisition saves the exact Cornell leaf URL and explicitly identifies convenience-mirror provenance. Harvest retains the marker and reports official-source reconciliation pending; `check.g_j2` cannot close on those mirror rows. Later work must reconcile selected sections against authoritative publication and applicable changes. Separate OAL/HCD amendment packages do not automatically certify every mirrored section.

Native DOC and DOCX use headless system `textutil`. Tests generate actual Word files and verify conversion. Native XLS uses `xlrd` for sheet names and stored cell values, without recalculating formulas or asserting layout fidelity. Install `pipeline/requirements-acquisition.txt` in the pipeline Python environment for that route; xlrd is absent in this environment, and the missing dependency raises an explicit acquisition error. Actual selected XLS files have not been fetched or converted here.

Generic and archive acquisition reject unsupported binary instead of decoding it as HTML. Native download URLs do not use a browser viewer as legal text. Conversion is mechanical acquisition, not internal provision enumeration; whole documents retain their document marker. PDF/image-only OCR remains a separate unresolved text-extraction need when pdftotext cannot recover text.

`ca_final_targets.json` contains the verified Water Service discriminated displayText URL (all 19 current headings) and complete unnumbered Constitution preamble. Constitution parsing supports actual SECTION and SEC. labels and preserves article identity. `usc_release_resolution.json` distinguishes the publisher's 119-111 search snapshots from unverified XML transport.

Focused check command:

```
python3 -m pytest research/legal-engine/pipeline/tests/test_acquisition.py research/legal-engine/pipeline/tests/test_adapters.py research/legal-engine/pipeline/tests/test_commands.py research/legal-engine/pipeline/tests/test_checkers.py research/legal-engine/pipeline/tests/test_jev_result_reuse.py -q
```
