"""IR5A: render review/INDEPENDENT_REVIEW_5A.md from review/independent_review_5a.json (plus fixed narrative sections)."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
R = json.loads((ROOT / "review/independent_review_5a.json").read_text())
S = R["summary"]
C4 = R["comparison_4a"]
EARLIER = {
 "R5A-09": "Round 2 considered PSC submetering and left it out ('no utility charge fact pattern in scope'). 5A rejects that exclusion: GOL 7-108(1-a)(b) itself makes lease utility charges payable to the landlord a retainable head, so whether such a charge is lawful is in scope.",
 "R5A-39": "Round 1 noted RPL 231-c only as listed out of scope in the NY coverage table; no round stated its predicate-notice and petition consequence (RPAPL 741(5-a)).",
}
L = []
w = L.append
w("# Independent review 5A (completeness): NYC market-rate settlement chain\n")
w("2026-09-30. Reviewer 5A. Report only: no rule file, walk, source or skill was edited. Evidence prefix REVIEW5A_, helper prefix ir5a_.\n")
w("## Summary\n")
w(f"- Universe (enumerated blind from primary sources before any rule file was opened): **{R['universe_count']} items** "
  "(state, city and federal statutes, regulations, rules, controlling decisions, guidance and pending law), in `review/review5a_universe.json`, every item with a verbatim quote from a saved source.")
w(f"- Against the rule files: {S['covered_items']} items stated; {S['no_decision_items']} change no decision; **{S['gap_items']} items not stated or stated only in part**, grouped into **{S['findings']} findings**: "
  f"**{S['by_severity']['critical']} critical, {S['by_severity']['major']} major, {S['by_severity']['minor']} minor**.")
w(f"- Over-scope: {S['over_scope_groups']} group (5 NYC rules on HPD article VIII escrow), minor.")
w(f"- Convergence against round 4A's universe ({C4['universe_4a']} items): {C4['matched_5a_items']} of 5A's {R['universe_count']} items are in 4A's universe; "
  f"{len(C4['only_in_5a'])} are only in 5A; {len(C4['only_in_4a'])} of 4A's items are not in 5A (22 are decision-changing law 5A missed; 5 are guidance or law that does not reach a lease balance: U096, U105, U125, U126, U144). "
  f"**{C4['new_gaps_count']} gap items are in neither 4A's universe nor the rule files**; every one of the {S['findings']} findings carries law 4A did not enumerate.")
w("- Judgment on completeness: not converged. Two blind enumerations of the same chain overlap on 85% of 4A's items (149 of 176) and 56% of 5A's (148 of 264); each found real law the other missed, and 5A found "
  f"{S['by_severity']['critical']} critical gaps (a forfeiture-triggering delivery rule, a rewritten consumer statute in force since 2026-02-17, champerty on hand-off, a rent bar for public-assistance tenants, "
  "unlawful-eviction penalties on retaking a unit, TCPA damages, co-tenant releases, accord and satisfaction, submetering, the bankruptcy claim deadline, post-judgment recovery, a heating-oil credit, "
  "fair-housing liability for agents and the 30-day breach notice). The misses cluster where the chain leaves the deposit statute: general contract and payment law (GOL arts. 15 and 17, UCC 1-308), "
  "judgment enforcement and court practice (CPLR arts. 2, 3, 50, 52; Judiciary Law), communications law (TCPA, E-SIGN) and data law. The next round should sweep those families by table of contents.\n")
w("Severity: critical = amount, rate, deadline, forfeiture, damages, who is paid, liability, or whether a regime or licence applies; major = operator action; minor = wording or a narrow branch.\n")
w("## Findings (most severe first)\n")
for f in R["findings"]:
    w(f"### {f['id']} ({f['severity']}, {f['kind']}) — {f['step']}\n")
    if f["rule_ids"]:
        w("Related rules: " + ", ".join(f"`{r}`" for r in f["rule_ids"]) + "\n")
    w(f"**What is missing.** {f['finding']}\n")
    w(f"**Correct law, as a rule.** {f['correct_rule']}\n")
    w("**Evidence (verbatim, saved sources).**")
    for e in f["evidence"]:
        q = e["quote"] if len(e["quote"]) <= 700 else e["quote"][:700] + " [...]"
        w(f"- `{e['source_file']}`: \"{q}\"")
    if f["id"] in EARLIER:
        w(f"\n*Earlier rounds:* {EARLIER[f['id']]}")
    w("")
w("## Over-scope\n")
for o in R["over_scope"]:
    w("- " + ", ".join(f"`{r}`" for r in o["rule_ids"]) + f" ({o['severity']}): {o['reason']}")
w("\nNo other in-scope rule was found that corresponds to nothing in the universe and changes no decision; the public-housing and project-based HUD rules are already deferred in the walk.\n")
w("## Universe coverage table\n")
w("| 5A id | Citation | Status in rule files | Rules | In 4A |")
w("|---|---|---|---|---|")
for c in R["coverage"]:
    rules = " ".join(f"`{r}`" for r in c["rule_ids"]) if c["rule_ids"] else (c["note"] or "")
    w(f"| {c['universe_id']} | {c['citation']} | {c['status']} | {rules} | {' '.join(c['in_4a']) or '-'} |")
w("\n## Comparison with round 4A's universe\n")
w(f"(i) In 5A, not in 4A ({len(C4['only_in_5a'])}): " + "; ".join(C4["only_in_5a"]) + ".\n")
w(f"(ii) In 4A, not in 5A ({len(C4['only_in_4a'])}), with 5A's assessment:")
for x in C4["only_in_4a"]:
    w(f"- {x}")
w(f"\n(iii) Gap items in neither 4A's universe nor the rule files: **{C4['new_gaps_count']}** (" + ", ".join(C4["new_gap_items_not_in_4a_or_rules"]) + ").\n")
w("## New versus earlier rounds\n")
w("Read after the findings above were saved: INDEPENDENT_REVIEW_1-3, 4A, 4B and REVIEW_1-4_DISPOSITION. None of the 41 findings was raised as a finding in an earlier round. Two touch law an earlier round mentioned:")
for k, v in EARLIER.items():
    w(f"- {k}: {v}")
w("- RPL 235-e(d): round 2 excluded it as an eviction-only defense; 5A agrees and records it as no-decision-change (U5A-049).")
w("- GOL 5-703 appears in the rules only as authority for voiding an oral lease over one year (`NY:ADJ-RPL-232-oral-term-over-one-year`); its surrender-writing rule (R5A-16) is new.\n")
w("## Method\n")
w("- Phase 1 (blind): read only APERTURE.md and STAGE_A.md's 'Chain (aperture)' and 'Discovery method'. The statute-compilation skill (and its reference notes, which summarize earlier rounds) was loaded as the harness requires; the universe was built from tables of contents, not from those notes.")
w("- Tables of contents walked mechanically (`review/ir5a_toc.py`, newyork.public.law mirror of the official nysenate.gov text; nysenate.gov, Justia, FindLaw and LegiScan are Cloudflare-walled to curl and the browser): GOL arts. 3, 5, 7, 15, 17; RPL arts. 6-A, 7, 12-A; RPAPL arts. 7, 7-A, 7-C, 8; MDL arts. 1-3, 8; CPLR arts. 2, 10, 12, 50, 52 and the full article list; GBL article list and arts. 9-B, 22-A, 25, 29-H, 29-HH, 29-HHH, 39-F; Military Law art. 13; Executive Law art. 15; ABP arts. 13-14; Judiciary Law art. 15. NYC Admin. Code and RCNY sections were searched and extracted from American Legal's official bulk XML (`review/ir5a_aml.py`).")
w("- Pending law: the Assembly's full-text search returned all 21,519 bills of the 2025-26 session with summaries; 3,219 matching chain keywords had their action histories fetched and parsed for passage in both houses in the same year, signature, veto or delivery. Chain-relevant bills passed by both houses and not yet acted on: S9760/A10182-A, S947/A3121, S9650/A659. Enacted in the window and relevant: L.2025 c.708 (FAIR Act), c.710 and L.2026 c.90 (coerced debt), c.431 (dishonored-check fee), c.91 (breach notice to DFS). A8906/S6446 passed the Senate in 2025 and the Assembly in 2026 only, so it has not passed both houses.")
w("- Federal texts from uscode.house.gov and the eCFR renderer; cases from the Caselaw Access Project static JSON (Horn Waterproofing), the Wayback copy of the Court of Appeals slip opinion (Justinian) and supremecourt.gov (Duguid). web_extract and web search were unavailable (credits exhausted).")
w("- Quotes are cut from saved sources by anchors or regex (`review/ir5a_lib.py`, `review/ir5a_build_universe.py`), never retyped. Phase 2 mapped each universe item to rule ids (`review/ir5a_map.py` candidates, then hand adjudication recorded in `review/ir5a_coverage.py`), and findings were built by `review/ir5a_build_findings.py`.")
w("- One universe entry was corrected before the diff after reading the full section: SCPA 1310 does not reach a landlord's deposit refund (the rule files state this correctly).")
w("- `python3 review/ir5a_verify.py`: every universe and evidence quote is verbatim in its source (whitespace-normalized), every cited rule id exists, no banned hedge phrase; the self-test catches a planted altered quote, altered evidence and a bad rule id. `stage_a_check.py` and `check_review.py` pass unchanged (0 errors; 551 in scope, 0 uncited).")
(ROOT / "review/INDEPENDENT_REVIEW_5A.md").write_text("\n".join(L) + "\n")
print("written", len(L), "lines")
