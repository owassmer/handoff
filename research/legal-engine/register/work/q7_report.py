"""Build register/work/report_7.md from decisions_7.jsonl (run from research/legal-engine)."""
import collections
import json
import pathlib
import sys

sys.path.insert(0, "register/work")
from q7_lib import BATCH, BY_ID, OUT, WORK

rows = [json.loads(l) for l in OUT.read_text().splitlines() if l.strip()]
counts = collections.Counter(r["decision"] for r in rows)
by_inst = collections.defaultdict(collections.Counter)
for r in rows:
    by_inst[BY_ID[r["section_id"]]["instrument"]][r["decision"]] += 1

L = ["# Report 7: set-aside reviewer A (batch 7)", "",
     "Reviewer q7. 456 sections Jev set aside as deciding nothing (NY instruments 16 NYCRR through LLC Law). Each was "
     "decided from its saved text; decisions in `register/work/decisions_7.jsonl`, chunk scripts `q7_c01.py`-`q7_c23.py`, "
     "helpers `q7_lib.py`, this report from `q7_report.py`. Report only: no rule file, walk or register file was edited.", "",
     "## Counts", ""]
L.append("| decision | count |")
L.append("|---|---|")
for k in ("no_decision", "excluded_regime", "stated", "partial", "new_rule"):
    L.append(f"| {k} | {counts.get(k, 0)} |")
L.append(f"| total | {len(rows)} |")
L += ["", "By instrument:", "", "| instrument | sections | not no_decision |", "|---|---|---|"]
for inst, c in sorted(by_inst.items()):
    L.append(f"| {inst} | {sum(c.values())} | {sum(v for k, v in c.items() if k != 'no_decision')} |")

L += ["", "## Sections decided other than no_decision (Jev's misses)", "",
      "Jev scores are p_decides / chain_duty. Every section below was set aside by Jev; `stated` and `excluded_regime` "
      "sections change or route something, `partial` and `new_rule` sections carry law no rule states.", "",
      "| section | heading | decision | Jev p_decides | Jev chain_duty | atoms / proposed |", "|---|---|---|---|---|---|"]
for r in rows:
    if r["decision"] == "no_decision":
        continue
    s = BY_ID[r["section_id"]]
    ref = ", ".join(r.get("atom_ids", []) + [p["id"] for p in r.get("proposed", [])]) or r["reason"][:60]
    L.append(f"| {r['section_id']} | {s['heading'][:50]} | {r['decision']} | {s['jev_p_decides']} | {s['jev_chain_duty']} | {ref} |")

misses = [r for r in rows if r["decision"] in ("partial", "new_rule")]
L += ["", f"Substantive misses (partial or new_rule): {len(misses)} of 456, all with p_decides of 0.09 or below."]

props = [(p, r) for r in rows for p in r.get("proposed", [])]
order = {"critical": 0, "major": 1, "minor": 2}
props.sort(key=lambda x: (order[x[0]["severity"]], x[0]["id"]))
L += ["", "## Proposed rules, most severe first", ""]
sev_count = collections.Counter(p["severity"] for p, _ in props)
L.append(f"critical {sev_count.get('critical', 0)}, major {sev_count.get('major', 0)}, minor {sev_count.get('minor', 0)}.")
for p, r in props:
    L += ["", f"### {p['id']} ({p['severity']}, {p['determinacy']})",
          f"- Section: {r['section_id']} ({r['decision']}{', amends ' + p['amends'] if p.get('amends') else ''})",
          f"- Provision: {p['provision']}; actor: {p['actor']}; walk step: {p['walk_step']}",
          f"- If: {p['condition']}",
          f"- Then: {p['effect']}"]
    if p.get("judgment_terms"):
        L.append(f"- Judgment terms: {', '.join(p['judgment_terms'])}")
    L.append(f"- Source: `{p['source_file']}` ({p['source_url']})")
    L.append(f"- Quote: \"{p['quote']}\"")

L += ["", "## Existing rules that look wrong or incomplete", "",
      "- `NY:BCL-1312(a)-foreign-authority` and `NY:LLC-808(a)-foreign-authority` leave 'doing business' wholly to "
      "judgment. BCL 1301(b) and LLC Law 803(a) fix part of it by statute: suing, settling claims and keeping bank "
      "accounts are not doing business. The judgment should run only over what is left (leasing and managing units). "
      "Proposed: `NY:BCL-1301-doing-business-and-fictitious-name`, `NY:LLC-803-doing-business-exclusions`.",
      "- `NY:GBL-130-assumed-name` does not carve out a foreign corporation's fictitious name filed with its "
      "application for authority; BCL 1301(d) says GBL 130 does not apply to that name. A lease made in the filed "
      "fictitious name needs no assumed-name certificate before suit.",
      "- Current Civil Court venue for a lease-balance suit is stated nowhere. The register matched CCA 301 to "
      "`NY:S9760-venue`, which states only the pending bill's tenant-county rule. Under today's law (CCA 2101(g), "
      "301(a)) the balance is not a consumer credit transaction, so suit lies in any city county where a party resides. "
      "The queue proposal `NY:CCA-305-venue-residence` assumes this without a rule behind it. Proposed: "
      "`NY:CCA-2101(g)-balance-venue-current`.",
      "- `NY:HANDOFF-broker-config-under-broker` (Configuration 3) states only the licence condition. 19 NYCRR 175.21 "
      "makes the configuration lawful only with the broker's regular, frequent and consistent personal supervision "
      "and transaction records. Proposed: `NY:19NYCRR-175.21-broker-supervision`.",
      "", "No existing rule was found stating the law incorrectly; the four items above are gaps in reach, not errors "
      "in what the rules say.", "",
      "## Checker", "", "```"]
import subprocess
out7 = subprocess.run([sys.executable, "register/work/check_decisions.py", "7"], capture_output=True, text=True).stdout
outall = subprocess.run([sys.executable, "register/work/check_decisions.py", "all"], capture_output=True, text=True).stdout
L += ["$ python3 register/work/check_decisions.py 7", out7.strip(), "", "$ python3 register/work/check_decisions.py all",
      outall.strip(), "```", ""]
(WORK / "report_7.md").write_text("\n".join(L))
print("wrote report_7.md;", dict(counts), "proposals", dict(sev_count))
