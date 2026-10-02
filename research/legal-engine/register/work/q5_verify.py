"""q5 self-checks: every rule id cited in a proposed rule exists (existing or proposed in batch 5); soft hedges; Jev>=0.9 no_decision."""
import json
import re
import sys
sys.path.insert(0, "register/work")
from q5_lib import rows, SEC, LE

known = set()
for k in ("NY", "NYC", "US", "VA"):
    d = json.loads((LE / f"stage-a/{k}.json").read_text())
    known |= {a["id"] for a in d["atoms"]} | set(d.get("external_references", {}))
r = rows()
proposed = {p["id"]: sid for sid, x in r.items() for p in x["proposed"]}
bad = []
for sid, x in r.items():
    texts = [x["reason"]] + [json.dumps(p) for p in x["proposed"]]
    for t in texts:
        for m in re.findall(r"\b((?:US|NY|NYC):[A-Za-z0-9().\-]+[A-Za-z0-9)])", t):
            while m.count(")") > m.count("("):
                m = m[:-1]
            if m not in known and m not in proposed:
                bad.append((sid, m))
    for p in x["proposed"]:
        for d in p["dependencies"]:
            if d not in known and d not in proposed:
                bad.append((sid, "dep " + d))
        for f in ("condition", "effect"):
            for w in re.findall(r"\b(generally|may be|possibly|likely|arguabl\w*|in practice|typically|usually)\b", p[f], re.I):
                print("soft?", sid, p["id"], f, w)
print("unresolved ids:", sorted(set(bad)))
print("proposed:", len(proposed))
for sid, x in r.items():
    j = SEC[sid].get("jev_p_decides")
    if x["decision"] == "no_decision" and j is not None and j >= 0.9:
        print("JEV>=0.9 no_decision:", sid, j)
