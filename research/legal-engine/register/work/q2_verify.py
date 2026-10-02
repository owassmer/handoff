"""q2 verification: dependency resolution, numeric claims vs source, soft hedges, id collisions across batches."""
import json, re, pathlib
from q2_lib import LE, OUT, norm

rows = [json.loads(l) for l in OUT.read_text().splitlines() if l.strip()]
known = set()
for k in ("NY", "NYC", "US", "VA"):
    d = json.loads((LE / f"stage-a/{k}.json").read_text())
    known |= {a["id"] for a in d["atoms"]} | set(d.get("external_references", {}))
props = [p for r in rows for p in r.get("proposed", [])]
pids = {p["id"] for p in props}
print("proposed rules:", len(props), "unique ids:", len(pids))

# 1. dependencies / amends / ids cited in text resolve
bad = []
def fix(m):
    m = m.rstrip(".")
    while m.endswith(")") and m.count("(") < m.count(")"):
        m = m[:-1]
    return m.rstrip(".")
idpat = re.compile(r"\b(?:NY|NYC|US):[A-Za-z0-9().\-*]+[A-Za-z0-9)]")
for p in props:
    for dep in p["dependencies"] + ([p["amends"]] if p.get("amends") else []):
        if dep not in known and dep not in pids:
            bad.append((p["id"], "dep", dep))
    for m in idpat.findall(p["effect"] + " " + p["condition"]):
        m = fix(m)
        if m not in known and m not in pids:
            bad.append((p["id"], "text", m))
for r in rows:
    for m in idpat.findall(r["reason"]):
        m = fix(m)
        if m not in known and m not in pids:
            bad.append((r["section_id"], "reason", m))
print("unresolved ids:", len(bad))
for b in bad:
    print("  ", b)

# 2. numbers in effect not found in its own source text
words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "ten": 10}
num_issues = []
for p in props:
    src = norm((LE / p["source_file"]).read_text(errors="ignore")).lower()
    for n in re.findall(r"\$?\d[\d,]*(?:\.\d+)?%?", p["effect"]):
        raw = n.strip("$%").replace(",", "")
        if not raw:
            continue
        try:
            val = float(raw)
        except ValueError:
            continue
        cands = {raw, n.replace(",", ""), f"{int(val):,}" if val == int(val) else raw}
        if val == int(val):
            iv = int(val)
            # spelled-out numbers commonly used in NY statutes
            spelled = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
                       10: "ten", 14: "fourteen", 15: "fifteen", 20: "twenty", 21: "twenty-one", 25: "twenty-five", 27: "twenty-seven",
                       30: "thirty", 35: "thirty-five", 45: "forty-five", 50: "fifty", 60: "sixty", 90: "ninety", 100: "one hundred",
                       120: "one hundred twenty", 125: "one hundred twenty-five", 150: "one hundred fifty", 190: "one hundred ninety",
                       200: "two hundred", 250: "two hundred fifty", 300: "three hundred", 500: "five hundred", 1000: "one thousand",
                       2000: "two thousand", 2500: "two thousand five hundred", 3000: "three thousand", 5000: "five thousand",
                       6000: "six thousand", 10000: "ten thousand", 250000: "two hundred fifty thousand", 150000: "one hundred fifty thousand",
                       125000: "one hundred twenty-five thousand", 75000: "seventy-five thousand"}
            if iv in spelled:
                cands.add(spelled[iv])
        if not any(c.lower() in src for c in cands if c):
            num_issues.append((p["id"], n))
print("numbers not in own source:", len(num_issues))
for x in num_issues:
    print("  ", x)

# 3. soft hedges beyond the checker's list
soft = re.compile(r"\b(generally|usually|often|likely|probably|might|could be|perhaps|appears to|seems)\b", re.I)
for p in props:
    for f in ("condition", "effect", "reasoning"):
        m = soft.search(str(p.get(f, "")))
        if m:
            print("soft hedge", p["id"], f, m.group(0))
for r in rows:
    m = soft.search(r["reason"])
    if m:
        print("soft hedge reason", r["section_id"], m.group(0))

# 4. collisions with other batches' decision files present now
other = {}
for f in sorted((LE / "register/work").glob("decisions_*.jsonl")):
    if f.name == OUT.name:
        continue
    for l in f.read_text().splitlines():
        if l.strip():
            for p in json.loads(l).get("proposed", []):
                other[p["id"]] = f.name
coll = sorted(pids & set(other))
print("collisions with other batches:", coll)
