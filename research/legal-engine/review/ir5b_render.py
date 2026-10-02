"""IR5B: render review/INDEPENDENT_REVIEW_5B.md from review/independent_review_5b.json and ir5b_text.py.

Optional review/ir5b_round4.json ({"round4_ids": [...], "newness": {"R5B-01": "..."}}) adds round-4 marks and the
newness section; it is written only after the findings were saved.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ir5b_text  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
doc = json.loads((ROOT / "review/independent_review_5b.json").read_text())
extra_p = ROOT / "review/ir5b_round4.json"
extra = json.loads(extra_p.read_text()) if extra_p.exists() else {}
r4 = set(extra.get("round4_ids", []))

sev_order = {"critical": 0, "major": 1, "minor": 2}
F = sorted(doc["findings"], key=lambda f: (sev_order[f["severity"]], f["id"]))
counts = {}
for f in F:
    counts.setdefault(f["severity"], 0)
    counts[f["severity"]] += 1
kinds = {}
for f in F:
    kinds[f["kind"]] = kinds.get(f["kind"], 0) + 1

L = []
L.append("# Independent review 5B: correctness of the market-rate NYC walk")
L.append("")
L.append("Reviewer 5B, 2026-09-29/30. Report only; no rule file, walk, source or skill was edited. Evidence script: "
         "`python3 review/ir5b_verify.py` (all quotes verbatim, all ids exist, self-test passes).")
L.append("")
L.append("## Summary")
L.append("")
L.append(f"- Rules checked: {doc['rules_checked_count']} (every id the walk cites: 453 in scope plus 2 cited from outside "
         "scope), each read beside its walk sentence; sources opened in context where the effect goes beyond the quote.")
L.append(f"- Findings: {len(F)}. By severity: " + ", ".join(f"{k} {counts.get(k,0)}" for k in ("critical", "major", "minor"))
         + ". By kind: " + ", ".join(f"{k} {v}" for k, v in sorted(kinds.items())) + ".")
L.append("- Judgment: **accept after the listed corrections.** The four critical findings change who is paid or how much: "
         "the prepaid rent after an owner-caused vacate order (R5B-01), the scope of RPL 227 (R5B-02), pre-sale rent "
         "arrears after a building sale (R5B-03), and the tenant's extended time to sue and the file-retention period "
         "(R5B-04). Everything else checked is confirmed below; the interpretive rulings re-decided (willfulness, address "
         "and dispatch, RPL 232, co-tenants, forfeiture survival, fee retention, lease balance not consumer credit, 2% "
         "interest, broker and DCWP licensing, FDCPA configurations, SHIELD dates, bankruptcy payee and setoff) hold.")
L.append("- T-vacate open branch: decided. The tenant recovers the per-day share of the prepaid installment for the days "
         "after the ouster (apportioned on failure of consideration); see the ruling below.")
L.append("")
L.append("## Findings (most severe first)")
for f in F:
    L.append("")
    L.append(f"### {f['id']} ({f['severity']}, {f['kind']})")
    L.append("")
    L.append(f"- Rules: " + ", ".join(f"`{i}`" + (" (round 4)" if i in r4 else "") for i in f["rule_ids"]))
    L.append(f"- Walk step: {f['step']}")
    L.append(f"- What is wrong: {f['finding']}")
    L.append(f"- Correct rule: {f['correct_rule']}")
    L.append("- Evidence:")
    for e in f["evidence"]:
        L.append(f"  - `{e['source_file']}`: \"{e['quote']}\"")
L.append("")
L.append("## T-vacate ruling")
L.append("")
L.append(doc["t_vacate_ruling"]["rule"])
L.append("")
L.append("Evidence:")
for e in doc["t_vacate_ruling"]["evidence"]:
    L.append(f"- `{e['source_file']}`: \"{e['quote']}\"")
L.append("")
L.append("Branches the operator applies: (a) installment paid before the ouster, tenant leaves: refund or credit the "
         "days after the ouster; (b) installment unpaid: charge or keep only the earned days; (c) tenant keeps possession "
         "of part: no proportionate recovery, rent suspended for later periods only (Barash, actual eviction); (d) order "
         "caused only by conditions the tenant or its household created: no defence, the lease governs; (e) order after "
         "a sudden casualty without tenant fault: RPL 227, same adjustment to the surrender date.")
L.append("")
L.append("## Confirmed")
L.append("")
L.append("Each line was checked quote-to-effect in the dump and, where marked, against the statute text (T) or the "
         "decision (C) in context." + (" Rules added or changed in round 4 are marked (round 4)." if r4 else ""))
L.append("")
for c in doc["confirmed"]:
    ids = re.findall(r"(?:NY|NYC|US):[^\s,;:]+(?:\([^)]*\))*[^\s,;:]*", c)
    mark = " (round 4: " + ", ".join(sorted(i for i in ids if i in r4)) + ")" if any(i in r4 for i in ids) else ""
    L.append(f"- {c}{mark}")
L.append("")
L.append("## Test cases (decided before reading the walk's answers)")
L.append("")
L.append("| Case | 5B answer | Difference from the walk |")
L.append("|---|---|---|")
for t in doc["test_cases"]:
    L.append(f"| {t['case']} | {t['answer']} | {t['difference']} |")
L.append("")
if extra.get("newness"):
    L.append("## New versus earlier rounds (written after the findings were saved)")
    L.append("")
    for k, v in extra["newness"].items():
        L.append(f"- {k}: {v}")
    L.append("")
    if extra.get("earlier_corrections"):
        L.append("Earlier corrections rated:")
        L.append("")
        for x in extra["earlier_corrections"]:
            L.append(f"- {x}")
        L.append("")
L.append("## Method")
L.append("")
for m in ir5b_text.METHOD:
    L.append(f"- {m}")
L.append("")
L.append("New sources saved (sources/REVIEW5B_*): Kennedy v Peterart Realty (App Term 1st 1939); Matter of Strasburger "
         "(CoA 1892); Peerless Candy v Halbreich (App Term 2d 1925); Suydam v Jackson (Commission of Appeals 1873); Warrin v "
         "Haverty (1st Dept 1913); Niles v Iroquois Realty (1st Dept 1909); Getty Realty v 2 East 61st Street (App Term 1st "
         "1939); 1239 Madison Ave v Neuburger (1st Dept 1924); Mayer Meat v Heilman (App Term 1st 1923); 11 USC 108; "
         "Assembly actions for S947 and S9760 as of 2026-09-29.")
(ROOT / "review/INDEPENDENT_REVIEW_5B.md").write_text("\n".join(L) + "\n")
print("written", len(L), "lines; round-4 ids", len(r4))
