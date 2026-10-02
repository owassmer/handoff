"""Importer equivalence on a temporary copy: the package's checks reproduce the legacy checkers' results exactly.

Runs `import-legacy` into a fresh temporary folder (never the live tree), then compares, on that copy:
  stage_a_check.py      NY 694, NYC 244, VA 277, US 359 atoms, 0 errors, cross-file 0
                        == `rules --legacy-hedge` (the skill's longer hedge list is tested separately)
  check_review.py       in scope 1200, cited 1098, deferred 102, not cited 0 == `walk NYC`
  check_register.py     strict PASS with its route and decision counts == `register` of US, NY and NYC, summed
Also: the citation engine built from the imported profiles parses every rule exactly as register/tools/cites.py.
"""
import collections
import hashlib
import json
import pathlib
import re
import subprocess
import sys

import pytest

from pipeline import core, legacy_import, registercheck, rulecheck, walkcheck

LIVE = core.PKG.parent


@pytest.fixture(scope="module")
def imported(tmp_path_factory):
    dest = tmp_path_factory.mktemp("pipeline_import_test")
    old = core.ROOT
    assert legacy_import.main(dest) == 0
    yield dest
    core.set_root(old)


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True).stdout


def test_refuses_live_tree():
    live = LIVE / "jurisdictions"
    def snapshot():
        return {str(p.relative_to(live)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in live.rglob("*") if p.is_file()}
    existed, before = live.exists(), snapshot()
    with pytest.raises(core.PipelineError):
        legacy_import.main(live)
    assert live.exists() == existed and snapshot() == before


def test_rule_checks_match_stage_a_check(imported):
    core.set_root(imported)
    out = run([sys.executable, "stage_a_check.py", "stage-a/NY.json", "stage-a/NYC.json", "stage-a/VA.json", "stage-a/US.json"], imported)
    legacy = {m.group(1): (int(m.group(2)), int(m.group(3))) for m in re.finditer(r"stage-a/(\w+)\.json: (\d+) atoms, (\d+) errors", out)}
    assert legacy == {"NY": (694, 0), "NYC": (244, 0), "VA": (277, 0), "US": (359, 0)}
    assert "cross-file: 0 errors" in out
    for code, (n, e) in legacy.items():
        errs, count = rulecheck.check(code, legacy_hedge=True)
        assert (count, len(errs)) == (n, e), code


def test_skill_hedge_list_is_stricter(imported):
    core.set_root(imported)
    errs, _ = rulecheck.check("VA")
    assert errs == ["VA:business-day-meaning: hedging in reasoning: 'persuasive only'"]


def test_walk_matches_check_review(imported):
    core.set_root(imported)
    out = run([sys.executable, "review/check_review.py", "review/NYC_MARKET_RATE.md"], imported)
    legacy = out.splitlines()[0]
    assert legacy == "in scope 1200: cited 1098, deferred 102, not cited 0; also cited from outside scope 3"
    errs, missing, summary = walkcheck.check("NYC")
    assert summary == legacy and not errs and not missing


def test_register_matches_check_register(imported):
    core.set_root(imported)
    out = run([sys.executable, "register/check_register.py"], imported)
    assert "PASS:" in out and "(strict)" in out
    routes = {k: int(v) for k, v in re.findall(r"^  (stated|review_queue|triaged_no_decision|triaged_excluded|unfetched)\s+(\d+)$", out, re.M)}
    dec = dict((k, int(v)) for k, v in re.findall(r"(\w+) (\d+)", out.split("Reviewer decisions (strict): ")[1].split(";")[0]))
    got_r, got_d = collections.Counter(), collections.Counter()
    for code in ("US", "NY", "NYC"):
        d = registercheck.load(code)
        assert registercheck.check(d) == [], code
        assert all(registercheck.self_test(d).values())
        got_r.update(r["legacy"]["route"] for r in d["triage"])
        assert all(r.get("jev") is None for r in d["triage"])
        assert all(r["legacy"]["current_jev_verified"] is False for r in d["triage"])
        got_d.update(r["review_decision"] for r in d["triage"])
    assert {k: got_r.get(k, 0) for k in routes} == routes
    assert dict(got_d) == dec


def test_decisions_match_legacy_check_decisions(imported):
    """register/work/check_decisions.py all == check-decisions all of US, NY and NYC, per batch (layers summed)."""
    core.set_root(imported)
    from pipeline import decisions
    out = run([sys.executable, "register/work/check_decisions.py", "all"], imported)
    pat = r"batch (\d+): (\d+)/(\d+) decided (\{.*?\}); (\d+) errors"
    legacy = {int(m[0]): (int(m[2]), json.loads(m[3].replace("'", '"')), int(m[4])) for m in re.findall(pat, out)}
    assert len(legacy) == 9 and all(e == 0 for _, _, e in legacy.values())
    known, rules = decisions.all_known(), core.rule_index(core.codes())
    got = collections.defaultdict(lambda: [0, collections.Counter(), 0])
    for code in ("US", "NY", "NYC"):
        new_ids = {}
        for n in decisions.batch_numbers(code):
            errs, undecided, cnt, total = decisions.check_batch(code, n, known, rules, new_ids)
            assert not undecided, (code, n)
            got[n][0] += total
            got[n][1].update(cnt)
            got[n][2] += len(errs)
    assert {n: (t, {k: c[k] for k in d}, e) for n, (t, c, e) in got.items() for d in [legacy[n][1]]} == legacy


def test_citation_engine_matches_legacy(imported):
    core.set_root(imported)
    sys.path.insert(0, str(imported / "register" / "tools"))
    import cites as legacy
    from pipeline import cites
    eng = cites.engine(["NY", "NYC", "US"])
    n = 0
    for code in ("NY", "NYC", "US"):
        for a in json.loads((imported / "stage-a" / f"{code}.json").read_text())["atoms"]:
            for t in (a.get("provision", ""), a.get("instrument", "")):
                assert sorted(eng.parse(t)) == sorted(legacy.parse(t)), (a["id"], t)
                for k, num in legacy.parse(t):
                    num = num.split(":")[1] if num.startswith("RANGE:") else num
                    assert eng.cite_instrument(k, num) == legacy.cite_instrument(k, num)
                n += 1
    assert n > 2000
