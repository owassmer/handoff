"""Check Stage A jurisdiction files. Usage: python3 stage_a_check.py stage-a/NY.json [more files]

Stage A retrieves and adjudicates the law. Nothing is left open. The check fails (exit 1) when:
  - an atom lacks a required field or uses an unknown determinacy;
  - a STANDARD or MIXED atom has no judgment_terms;
  - an atom's quote is not found verbatim (whitespace-normalized) in its saved source file;
  - an atom resolved by interpretation has a 'construction' entry whose quote is not verbatim in its source,
    or has construction entries but no 'reasoning';
  - an atom's condition, effect or reasoning uses hedging language (the law is stated, not caveated);
  - an atom id is duplicated, or a dependency names an id that is neither an atom nor a declared external reference;
  - the file lists any bounded unknown: every question is resolved into atoms (a fact-dependent outcome is a
    condition, a standard is a STANDARD atom with its authoritative content, a sunset is an effective_to);
  - with several files, a cross-file reference names nothing in the target file.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
REQ = ["id", "jurisdiction", "instrument", "provision", "effective_from", "effective_to", "actor", "modality",
       "condition", "effect", "determinacy", "dependencies", "source_file", "source_url", "quote"]
DET = {"RULE", "STANDARD", "MIXED"}
HEDGE = re.compile(r"\b(unclear|unsettled|open question|working position|conservative position|arguabl\w*|"
                   r"consult counsel|needs counsel|not yet known|bounded unknown|undetermined|uncertain whether|"
                   r"may or may not|it is possible that)\b", re.I)
norm = lambda s: re.sub(r"\s+", " ", s).strip()


def check(path):
    d = json.loads(pathlib.Path(path).read_text())
    errs = []
    atoms = d.get("atoms", [])
    ids = [a.get("id") for a in atoms]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        errs.append(f"duplicate ids: {sorted(dup)}")
    known = set(ids) | set(d.get("external_references", {}))
    cache = {}

    def verbatim(src, quote):
        f = ROOT / src
        if not src or not f.is_file():
            return f"source file missing {src}"
        cache.setdefault(f, norm(f.read_text(errors="ignore")))
        return None if quote and norm(quote) in cache[f] else f"quote not verbatim in {src}"

    for a in atoms:
        miss = [k for k in REQ if k not in a]
        if miss:
            errs.append(f"{a.get('id')}: missing {miss}")
            continue
        if a["determinacy"] not in DET:
            errs.append(f"{a['id']}: determinacy {a['determinacy']}")
        if a["determinacy"] != "RULE" and not a.get("judgment_terms"):
            errs.append(f"{a['id']}: STANDARD/MIXED needs judgment_terms")
        e = verbatim(a["source_file"], a["quote"])
        if e:
            errs.append(f"{a['id']}: {e}")
        for c in a.get("construction", []):
            e = verbatim(c.get("source_file", ""), c.get("quote", ""))
            if e:
                errs.append(f"{a['id']}: construction {e}")
        if a.get("construction") and not a.get("reasoning"):
            errs.append(f"{a['id']}: construction without reasoning")
        for field in ("condition", "effect", "reasoning"):
            m = HEDGE.search(str(a.get(field, "")))
            if m:
                errs.append(f"{a['id']}: hedging in {field}: '{m.group(0)}'")
        for dep in a["dependencies"]:
            if dep not in known:
                errs.append(f"{a['id']}: dependency {dep} is not an atom or declared external reference")
    for u in d.get("bounded_unknowns", []):
        errs.append(f"open question {u.get('id')}: resolve it into atoms")
    return errs, len(atoms)


def cross(paths):
    """A reference into another checked jurisdiction must name an atom there or an entry it declares."""
    files = {pathlib.Path(p).stem: json.loads(pathlib.Path(p).read_text()) for p in paths}
    known = {k: {a["id"] for a in d.get("atoms", [])} | set(d.get("external_references", {})) for k, d in files.items()}
    errs = []
    for k, d in files.items():
        for ref in d.get("external_references", {}):
            target = ref.split(":")[0]
            if target in files and target != k and ref not in known[target]:
                errs.append(f"{k}: {ref} is not an atom or declared reference in {target}.json")
    return errs


if __name__ == "__main__":
    bad = False
    for p in sys.argv[1:]:
        errs, n = check(p)
        print(f"{p}: {n} atoms, {len(errs)} errors")
        for e in errs:
            print("  ", e)
        bad |= bool(errs)
    if len(sys.argv) > 2:
        errs = cross(sys.argv[1:])
        print(f"cross-file: {len(errs)} errors")
        for e in errs:
            print("  ", e)
        bad |= bool(errs)
    sys.exit(1 if bad else 0)
