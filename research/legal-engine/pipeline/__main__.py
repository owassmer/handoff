"""python3 -m pipeline <command> [CODE] [options]   (run from research/legal-engine)

The skill's commands:
  init CODE --layer state|county|city|federal [--parent CODE] [--name NAME]
  instruments CODE                 J1 gate: instrument list against the chain map's legal functions
  harvest CODE [--instrument ID] [--unit UNIT] [--limit N] [--dry-run]
  match CODE                       J3: sections already stated by a rule in this or a parent layer
  calibrate CODE [--cached-only] [--version V ...] [--cap USD] [--limit N]
  triage CODE [--cap USD] [--limit N] [--cached-only] [--rerun]
  batch CODE [--dry-run]
  check-decisions CODE N|all | check-decisions [CODE] --self-test
  apply CODE
  authorities CODE
  check [CODE ...] [--upto J1..J8]  every gate; prints the stage each jurisdiction has reached
  show RULE_ID|PREFIX* [...]
  diff CODE [--limit N] [--instrument ID]
Support commands:
  coverage seed|save|status|check|export|digest CODE SCOPE
                        durable source/dependency investigation and independent review
  rules [CODE ...] [--legacy-hedge]   rule checks only (stage_a_check.py equivalent; --legacy-hedge uses its
                        shorter hedge list instead of the skill's)
  register CODE         register check only (check_register.py --strict equivalent)
  walk CODE             walk check only (check_review.py equivalent)
  export-data           rebuild pipeline/data/ (crosswalk, gold labels) from register/
  import-legacy DEST    import stage-a/, register/ and review/ into DEST/jurisdictions (never into this tree)
  adapter-test [NAME ...] [--save]   live-fetch each adapter's SMOKE section; --save writes tests/fixtures/
Every command prints what it did and exits non-zero on failure.
"""
from __future__ import annotations

import argparse
import os
import sys

from . import core

NEEDS_SDK = {"triage", "calibrate", "batch"}


def _reexec_in_venv(cmd):
    """Triage and calibrate need typesafe_sdk (installed in research/legal-engine/.venv, Python 3.12)."""
    from . import jev
    if cmd in NEEDS_SDK and not jev.sdk_available() and "--cached-only" not in sys.argv:
        py = core.VENV_PYTHON
        if py.exists() and os.path.realpath(sys.executable) != os.path.realpath(str(py)):
            os.execv(str(py), [str(py), "-m", "pipeline"] + sys.argv[1:])
        raise core.PipelineError(f"typesafe_sdk is not installed and {py} does not exist")


def parser():
    p = argparse.ArgumentParser(prog="python3 -m pipeline", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd")
    a = s.add_parser("init")
    a.add_argument("code")
    a.add_argument("--layer", required=True)
    a.add_argument("--parent")
    a.add_argument("--name")
    for c in ("instruments", "match", "apply", "authorities", "register", "walk"):
        s.add_parser(c).add_argument("code")
    a = s.add_parser("harvest")
    a.add_argument("code")
    a.add_argument("--instrument")
    a.add_argument("--unit")
    a.add_argument("--limit", type=int)
    a.add_argument("--dry-run", action="store_true")
    a = s.add_parser("calibrate")
    a.add_argument("code")
    a.add_argument("--cached-only", action="store_true")
    a.add_argument("--version", action="append")
    a.add_argument("--cap", type=float, default=2.00)
    a.add_argument("--limit", type=int)
    a = s.add_parser("triage")
    a.add_argument("code")
    a.add_argument("--cap", type=float, default=2.00)
    a.add_argument("--limit", type=int)
    a.add_argument("--cached-only", action="store_true")
    a.add_argument("--rerun", action="store_true")
    a = s.add_parser("batch")
    a.add_argument("code")
    a.add_argument("--dry-run", action="store_true")
    a = s.add_parser("check-decisions")
    a.add_argument("args", nargs="*")
    a.add_argument("--self-test", action="store_true")
    a = s.add_parser("check")
    a.add_argument("codes", nargs="*")
    a.add_argument("--upto", default="J8")
    s.add_parser("show").add_argument("ids", nargs="*")
    a = s.add_parser("diff")
    a.add_argument("code")
    a.add_argument("--limit", type=int)
    a.add_argument("--instrument")
    a = s.add_parser("rules")
    a.add_argument("codes", nargs="*")
    a.add_argument("--legacy-hedge", action="store_true")
    a = s.add_parser("export-data")
    a.add_argument("--src")
    a.add_argument("--out")
    a = s.add_parser("import-legacy")
    a.add_argument("dest")
    a.add_argument("--src")
    a = s.add_parser("adapter-test")
    a.add_argument("names", nargs="*")
    a.add_argument("--save", action="store_true")
    a = s.add_parser("coverage")
    cs = a.add_subparsers(dest="action", required=True)
    for action in ("seed", "save", "followup", "link-research", "status", "check", "export", "digest"):
        ca = cs.add_parser(action)
        ca.add_argument("code")
        ca.add_argument("scope")
        if action == "seed":
            ca.add_argument("--purpose", required=True)
            ca.add_argument("--author", required=True)
        elif action in ("save", "followup", "link-research"):
            ca.add_argument("--file", required=True)
            ca.add_argument("--expected-revision", type=int, required=True)
            if action == "followup":
                ca.add_argument("--author", required=True)
        else:
            ca.add_argument("--revision", type=int)
            if action == "digest":
                ca.add_argument("--kind", choices=["item", "boundary", "scope"], required=True)
                ca.add_argument("--target", required=True)
            elif action in ("status", "check"):
                ca.add_argument("--as-of")
    return p


def run(argv):
    p = parser()
    a = p.parse_args(argv)
    if not a.cmd:
        p.print_help()
        return 1
    _reexec_in_venv(a.cmd)
    if a.cmd == "coverage":
        from . import coverage
        return coverage.main(a)
    if a.cmd == "init":
        from . import init
        return init.main(a.code, a.layer, a.parent, a.name)
    if a.cmd == "instruments":
        from . import instruments
        return instruments.main(a.code)
    if a.cmd == "harvest":
        from . import harvest
        return harvest.main(a.code, instrument=a.instrument, unit=a.unit, limit=a.limit, dry_run=a.dry_run)
    if a.cmd == "match":
        from . import match
        return match.main(a.code)
    if a.cmd == "calibrate":
        from . import triage
        return triage.calibrate_main(a.code, cached_only=a.cached_only, versions=a.version, cap=a.cap, limit=a.limit)
    if a.cmd == "triage":
        from . import triage
        return triage.triage_main(a.code, cap=a.cap, limit=a.limit, cached_only=a.cached_only, rerun=a.rerun)
    if a.cmd == "batch":
        from . import batch
        return batch.main(a.code, dry_run=a.dry_run)
    if a.cmd == "check-decisions":
        from . import decisions
        args = list(a.args)
        if a.self_test:
            return decisions.main(args[0] if args else None, "--self-test")
        if not args:
            print("usage: check-decisions CODE N|all | check-decisions [CODE] --self-test")
            return 1
        return decisions.main(args[0], args[1] if len(args) > 1 else "all")
    if a.cmd == "apply":
        from . import apply
        return apply.main(a.code)
    if a.cmd == "authorities":
        from . import authorities
        return authorities.main(a.code)
    if a.cmd == "check":
        from . import check
        return check.main(a.codes, a.upto)
    if a.cmd == "show":
        from . import show
        return show.main(a.ids)
    if a.cmd == "diff":
        from . import diff
        return diff.main(a.code, limit=a.limit, instrument=a.instrument)
    if a.cmd == "rules":
        from . import rulecheck
        return rulecheck.main(a.codes or core.codes(), a.legacy_hedge)
    if a.cmd == "register":
        from . import registercheck
        errs, ok = registercheck.main(a.code)
        print(f"{a.code} register: {'PASS' if not errs and ok else 'FAIL'} ({len(errs)} problems; strict)")
        return 0 if not errs and ok else 1
    if a.cmd == "walk":
        from . import walkcheck
        return walkcheck.main(a.code)
    if a.cmd == "export-data":
        from . import export
        return export.main(a.src, a.out)
    if a.cmd == "import-legacy":
        from . import legacy_import
        return legacy_import.main(a.dest, a.src)
    if a.cmd == "adapter-test":
        from . import adapter_test
        return adapter_test.main(a.names, save=a.save)
    p.print_help()
    return 1


def main():
    try:
        rc = run(sys.argv[1:])
    except core.PipelineError as e:
        print(f"FAIL: {e}")
        rc = 1
    sys.exit(rc or 0)


if __name__ == "__main__":
    main()
