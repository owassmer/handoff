"""adapter-test: fetch each adapter's SMOKE section live (routes in order, cache bypassed) and check the expected
phrase is in the text. --save writes the result to pipeline/tests/fixtures/<adapter>.json ({adapter, ref, label,
expect, source_url, route, retrieved, text}) and the saved text to fixtures/<adapter>.txt, which the test suite
re-parses offline. Exits non-zero when any adapter fails.
"""
from __future__ import annotations

import json

from . import adapters, core
from .adapters import base

FIX = core.PKG / "tests" / "fixtures"


def one(name, save=False):
    a = adapters.get(name)
    if not a.SMOKE:
        return None, f"{name}: no SMOKE section defined"
    base.REFRESH["on"] = True
    try:
        sec = a.section(a.SMOKE["ref"])
    except Exception as e:  # noqa: BLE001
        return False, f"{name}: FAILED {a.SMOKE['ref']}: {str(e)[:300]}"
    finally:
        base.REFRESH["on"] = False
    ok = a.SMOKE["expect"].lower() in core.norm(sec["text"]).lower()
    msg = (f"{name}: {'ok' if ok else 'EXPECTED PHRASE MISSING'} {a.SMOKE['label']} via {sec['route']}; "
           f"{len(sec['text'])} chars; {sec['source_url']}")
    if save and ok:
        FIX.mkdir(parents=True, exist_ok=True)
        text = a.save(FIX / f"{name}.txt", sec)
        (FIX / f"{name}.json").write_text(json.dumps({
            "adapter": name, "ref": a.SMOKE["ref"], "label": a.SMOKE["label"], "expect": a.SMOKE["expect"],
            "source_url": sec["source_url"], "route": sec["route"], "retrieved": core.now(),
            "extra": sec.get("extra") or {}, "chars": len(sec["text"]), "sha256": core.text_hash(text)}, indent=1) + "\n")
    return ok, msg


def main(names=None, save=False):
    names = names or sorted(adapters.NAMES)
    bad = 0
    for n in names:
        ok, msg = one(n, save)
        print(msg)
        bad += ok is False
    print(f"adapter-test: {len(names) - bad}/{len(names)} adapters passed")
    return 1 if bad else 0
