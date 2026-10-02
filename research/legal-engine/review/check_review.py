"""Check a review walk against the Stage A files.

Usage: python3 review/check_review.py review/NYC_MARKET_RATE.md

Fails (exit 1) when the review cites a rule id that does not exist, or when a rule in the review's scope is
neither cited nor listed as deferred to a later review. Scope for the market-rate review: every NY and US rule,
and the NYC rules that reach a unit that is not rent-stabilized or rent-controlled.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ATOMS = {}
for k in ("NY", "NYC", "US"):
    for a in json.loads((ROOT / f"stage-a/{k}.json").read_text())["atoms"]:
        ATOMS[a["id"]] = a

# NYC rules that govern only stabilized or controlled tenancies belong to the second review.
REGULATED_ONLY = re.compile(r"^NYC:(RSC-2525|RSC-2526|RSC-2527|RSC-2522|RSC-2523|RSC-2528|RSC-2520\.(6|12|13)|"
                            r"RSL-26-5(09|11|12|16|17)|RER-22|RCL-26-4(03\(f\)|03\(i\)|03\(e\)\(1\)|03\(e\)\(2\)\(h\)|05|12|13|14|16|17|01)|"
                            r"RS-|DHCR|RGB|CASE-(Middleton|Samson))")
text = pathlib.Path(sys.argv[1]).read_text()
cited = set(re.findall(r"`((?:NY|NYC|US):[^`\s]+)`", text))
deferred = set(re.findall(r"deferred: `((?:NY|NYC|US):[^`\s]+)`", text))
errs = [f"cited but not a rule: {i}" for i in sorted(cited) if i not in ATOMS]
scope = {i for i in ATOMS if not REGULATED_ONLY.match(i)}
missing = sorted(scope - cited - deferred)
print(f"in scope {len(scope)}: cited {len((cited - deferred) & scope)}, deferred {len(deferred & scope)}, "
      f"not cited {len(missing)}; also cited from outside scope {len((cited - deferred) & set(ATOMS) - scope)}")
for i in missing:
    print("   not cited:", i)
for e in errs:
    print("  ", e)
sys.exit(1 if errs or missing else 0)
