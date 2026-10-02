"""Step 3, mechanical match (code only, no model).

For every section in register/sections.jsonl, list the rule-file atom ids whose `provision` or `source_file` refers
to it, the review 4A and 5A universe items whose `citation` refers to it, and the 5A gap findings whose evidence
source files or universe items refer to it. Writes register/match.json:
  {"sections": {section_id: {atom_ids, universe_4a, universe_5a, gap_5a}},
   "atom_citations": {atom_id: [{key, number, instrument, section_id|null, via}]},
   "unmatched": [...citations to registered instruments whose section is outside the in-scope units...],
   "unregistered": [...citations whose instrument is not in the register...]}
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import cites  # noqa: E402

REG = pathlib.Path(__file__).resolve().parent.parent
ROOT = REG.parent


def load_sections():
    return [json.loads(l) for l in (REG / "sections.jsonl").read_text().splitlines() if l.strip()]


def index(secs):
    idx = {}
    for s in secs:
        idx.setdefault(cites.section_key(s["section_id"]), []).append(s["section_id"])
    return idx


def resolve(key, num, idx, secs_by_key):
    if num.startswith("RANGE:"):
        _, a, b = num.split(":")
        a, b = int(a), int(b)
        out = []
        for (k, n), ids in idx.items():
            m = re.match(r"(\d+)", n)
            if k == key and m and a <= int(m.group(1)) <= b:
                out.extend(ids)
        return out
    return idx.get((key, num), [])


def atoms():
    for f in ("NY", "NYC", "US"):
        for a in json.loads((ROOT / "stage-a" / f"{f}.json").read_text())["atoms"]:
            yield f, a


def main():
    secs = load_sections()
    idx = index(secs)
    res = {s["section_id"]: {"atom_ids": [], "universe_4a": [], "universe_5a": [], "gap_5a": []} for s in secs}
    atom_cites, unmatched, unregistered = {}, [], []

    def cite_list(text, via):
        return [(k, n, via) for k, n in cites.parse(text)]

    for f, a in atoms():
        cl = cite_list(a.get("provision", ""), "provision")
        if re.search(r"\bcomments?\s+\d", a.get("provision", ""), re.I) and "1006" in (a.get("provision", "") + a.get("instrument", "")):
            cl.append(("12 CFR", "SUPPLEMENT_I_TO_PART_1006", "provision"))
        sf = cites.source_file_cite(a.get("source_file"))
        if sf:
            cl.append((sf[0], sf[1], "source_file"))
        rows = []
        for k, n, via in cl:
            inst = cites.cite_instrument(k, n.split(":")[1] if n.startswith("RANGE:") else n)
            hits = resolve(k, n, idx, None)
            for h in hits:
                if a["id"] not in res[h]["atom_ids"]:
                    res[h]["atom_ids"].append(a["id"])
            rows.append({"key": k, "number": n, "via": via, "instrument": inst, "section_ids": hits})
            if not hits:
                (unmatched if inst else unregistered).append({"atom_id": a["id"], "file": f, "key": k, "number": n,
                                                             "via": via, "instrument": inst, "provision": a.get("provision"),
                                                             "atom_instrument": a.get("instrument")})
        atom_cites[a["id"]] = rows

    for tag, fn in (("universe_4a", "review4a_universe.json"), ("universe_5a", "review5a_universe.json")):
        for u in json.loads((ROOT / "review" / fn).read_text()):
            cl = cites.parse(u.get("citation", ""))
            sf = cites.source_file_cite(u.get("source_file"))
            if sf:
                cl.append(sf)
            for k, n in cl:
                for h in resolve(k, n, idx, None):
                    if u["id"] not in res[h][tag]:
                        res[h][tag].append(u["id"])

    rv = json.loads((ROOT / "review" / "independent_review_5a.json").read_text())
    u5 = {u["id"]: u for u in json.loads((ROOT / "review" / "review5a_universe.json").read_text())}
    for fnd in rv["findings"]:
        cl = []
        for e in fnd.get("evidence") or []:
            sf = cites.source_file_cite(e.get("source_file") if isinstance(e, dict) else None)
            if sf:
                cl.append(sf)
        for uid in fnd.get("universe_ids") or []:
            if uid in u5:
                cl.extend(cites.parse(u5[uid].get("citation", "")))
        for k, n in cl:
            for h in resolve(k, n, idx, None):
                if fnd["id"] not in res[h]["gap_5a"]:
                    res[h]["gap_5a"].append(fnd["id"])

    out = {"sections": res, "atom_citations": atom_cites, "unmatched": unmatched, "unregistered": unregistered}
    (REG / "match.json").write_text(json.dumps(out, indent=1))
    stated = sum(1 for v in res.values() if v["atom_ids"])
    print(f"sections: {len(res)}; stated: {stated}; cited by 4A: {sum(1 for v in res.values() if v['universe_4a'])}; "
          f"cited by 5A: {sum(1 for v in res.values() if v['universe_5a'])}; 5A gap sections: {sum(1 for v in res.values() if v['gap_5a'])}")
    print(f"atom citations to registered instruments outside in-scope units: {len(unmatched)}; to unregistered instruments: {len(unregistered)}")
    noc = [a['id'] for f, a in atoms() if not atom_cites[a['id']]]
    print(f"atoms with no statutory/regulatory citation (case law, guidance, forms, session laws): {len(noc)}")


if __name__ == "__main__":
    main()
