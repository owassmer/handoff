"""Jev triage of register sections (Step 4). Jev (typesafe/jev-1.13 via OpenRouter) answers two typed questions per
section (jev_questions.json); it never states law. Routing is owned by code (routing.json, build_outputs.py).

Usage (interpreter: the profile venv with typesafe-sdk, e.g. .../scratch/jevenv/bin/python):
  python jev_triage.py ask SECTION_ID [...]        ask Jev about specific sections, print answers (no text)
  python jev_triage.py run --set calibration        positives + hand-checked negatives (calibration.json inputs)
  python jev_triage.py run --set triage             every in-scope section that is not 'stated' (and not LONG)
Options: --concurrency N (default 8), --limit N

Credential: OPENROUTER_API_KEY from the environment, else read at runtime from the Slope repository's .env file.
The key is never printed, logged, copied or written. Spend cap per run $2.00 (provider-reported cost, with a
conservative reservation before dispatch); physical attempt ceiling per run 12,000 (SDK retries included).
Cache: jev_cache/<sha256(model, built questions, state)>.json. Every network exchange (request without credentials,
raw response) is appended to jev_exchanges.jsonl; answers per section to jev_results.jsonl.
"""
import asyncio
import datetime
import hashlib
import json
import os
import pathlib
import re
import sys
from decimal import Decimal

REG = pathlib.Path(__file__).resolve().parent
CACHE = REG / "jev_cache"
EXCH = REG / "jev_exchanges.jsonl"
RESULTS = REG / "jev_results.jsonl"
SLOPE_ENV = pathlib.Path("/Users/owenwassmer/dev/Slope_Sparse_Events/.env")
MODEL = "typesafe/jev-1.13"
BASE_URL = "https://openrouter.ai/api"
MARKER = "jev-1.13"
SPEND_CAP = Decimal("2.00")
ATTEMPT_CEILING = 12000
MAX_RETRIES = 2
RESERVE_PRICE_PER_TOKEN = Decimal("0.20") / 10**6  # conservative reservation; actual spend = provider-reported cost
LONG = 12000


def api_key():
    k = os.environ.get("OPENROUTER_API_KEY")
    if k:
        return k
    if SLOPE_ENV.is_file():
        for line in SLOPE_ENV.read_text().splitlines():
            m = re.match(r"\s*(?:export\s+)?OPENROUTER_API_KEY\s*=\s*(.*)\s*$", line)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    raise SystemExit("OPENROUTER_API_KEY not found in the environment or the Slope .env file")


def canonical_sha256(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()


def registry():
    return json.loads((REG / "jev_questions.json").read_text())


def build_questions(reg):
    from typesafe_sdk import Choice, Noul
    rules = "\n".join(f"- {r}" for r in reg["global_rules"])
    qs = {}
    for q in reg["questions"]:
        instr = f"Global rules:\n{rules}\n\nQuestion:\n{q['prompt']['instructions']}"
        cls = Noul if q["primitive"] == "noul" else Choice
        qs[q["id"]] = cls(instructions=instr, criteria=q["prompt"]["criteria"])
    return qs


def sections():
    return {json.loads(l)["section_id"]: json.loads(l) for l in (REG / "sections.jsonl").read_text().splitlines() if l.strip()}


def body_of(sec):
    t = (REG / sec["text_file"]).read_text()
    return t.split("\n\n", 1)[1] if "\n\n" in t else t


def instrument_names():
    f = REG / "instruments.json"
    if not f.exists():
        f = REG / ".work" / "instruments_core.json"
    d = json.loads(f.read_text())
    lst = d["instruments"] if isinstance(d, dict) else d
    return {i["id"]: i["name"] for i in lst}


def state_for(sec, reg, names):
    return {"instrument": f"{names.get(sec['instrument'], sec['instrument'])}, {sec['section_id'].split(':', 1)[1]}",
            "heading": sec["heading"], "section_text": body_of(sec),
            "chain_description": reg["chain_description"], "aperture_exclusions": reg["aperture_exclusions"]}


class Budget:
    def __init__(self):
        self.attempts = 0
        self.inflight_attempts = 0
        self.inflight_usd = Decimal(0)
        self.spent = Decimal(0)
        self.requests = 0
        self.cache_hits = 0
        self.errors = 0

    def reserve(self, chars):
        att = 1 + MAX_RETRIES
        est = Decimal(chars // 3 + 1500) * RESERVE_PRICE_PER_TOKEN * att
        if self.attempts + self.inflight_attempts + att > ATTEMPT_CEILING:
            raise RuntimeError(f"attempt ceiling {ATTEMPT_CEILING} reached")
        if self.spent + self.inflight_usd + est > SPEND_CAP:
            raise RuntimeError(f"spend cap ${SPEND_CAP} would be exceeded")
        self.inflight_attempts += att
        self.inflight_usd += est
        return att, est


async def run(ids, concurrency=8):
    raise RuntimeError("Legacy Jev execution is historical-only. Use python -m pipeline triage or calibrate "
                       "for request-bound, validated result reuse. Existing experiment records remain available.")
    import httpx2
    from pydantic import BaseModel, ConfigDict
    from typesafe_sdk import AsyncTypeSafeClient, RetryPolicy

    class Raw(BaseModel):
        model_config = ConfigDict(extra="allow")

    reg = registry()
    qs = build_questions(reg)
    qdump = {k: v.model_dump(mode="json") for k, v in qs.items()}
    secs = sections()
    names = instrument_names()
    budget = Budget()

    async def count(_req):
        budget.attempts += 1

    client = AsyncTypeSafeClient(api_key=api_key(), base_url=BASE_URL, retry=RetryPolicy(max_retries=MAX_RETRIES),
                                 http_client=httpx2.AsyncClient(timeout=120.0, event_hooks={"request": [count]}))
    CACHE.mkdir(exist_ok=True)
    sem = asyncio.Semaphore(concurrency)
    out = []
    stop = {"reason": None}

    async def one(sid):
        sec = secs[sid]
        if not sec.get("text_file") or sec["chars"] > LONG:
            return None
        state = state_for(sec, reg, names)
        key = canonical_sha256({"model": MODEL, "questions": qdump, "state": state})
        cf = CACHE / f"{key}.json"
        hit = cf.exists()
        if hit:
            d = json.loads(cf.read_text())
            raw, created = d["raw"], d["created_at"]
            budget.cache_hits += 1
        else:
            if stop["reason"]:
                return None
            async with sem:
                try:
                    att, est = budget.reserve(len(json.dumps(state)))
                except RuntimeError as e:
                    stop["reason"] = str(e)
                    return None
                try:
                    budget.requests += 1
                    resp = await client.system_one(state=state, questions=qs, model=MODEL, response_model=Raw)
                    raw = resp.model_dump(mode="json")
                except Exception as e:  # noqa: BLE001
                    budget.errors += 1
                    budget.inflight_attempts -= att
                    budget.inflight_usd -= est
                    with EXCH.open("a") as f:
                        f.write(json.dumps({"created_at": datetime.datetime.now(datetime.UTC).isoformat(), "section_id": sid,
                                            "cache_key": key, "request": {"model": MODEL, "base_url": BASE_URL,
                                                                          "questions": qdump, "state": state},
                                            "error": f"{type(e).__name__}: {str(e)[:300]}"}) + "\n")
                    return None
                budget.inflight_attempts -= att
                budget.inflight_usd -= est
            cost = (raw.get("usage") or {}).get("cost")
            budget.spent += Decimal(str(cost)) if cost is not None else est
            created = datetime.datetime.now(datetime.UTC).isoformat()
            if MARKER not in str(raw.get("model")):
                stop["reason"] = f"unexpected model {raw.get('model')!r}"
                raise SystemExit(stop["reason"])
            cf.write_text(json.dumps({"raw": raw, "created_at": created}))
            with EXCH.open("a") as f:
                f.write(json.dumps({"created_at": created, "section_id": sid, "cache_key": key,
                                    "request": {"model": MODEL, "base_url": BASE_URL, "questions": qdump, "state": state},
                                    "response": raw}) + "\n")
        a = raw.get("answers") or {}
        role, duty = a.get("role") or {}, a.get("chain_duty") or {}
        rec = {"section_id": sid, "cache_key": key, "returned_model": raw.get("model"), "registry_version": reg["registry_version"],
               "role": role.get("choice"), "role_probabilities": role.get("probabilities"), "role_confidence": role.get("confidence"),
               "chain_duty": duty.get("noul"), "usage": raw.get("usage"), "created_at": created, "cache_hit": hit}
        out.append(rec)
        return rec

    await asyncio.gather(*(one(s) for s in ids))
    prev = {}
    if RESULTS.exists():
        for l in RESULTS.read_text().splitlines():
            if l.strip():
                r = json.loads(l)
                prev[r["section_id"]] = r
    for r in out:
        prev[r["section_id"]] = r
    RESULTS.write_text("".join(json.dumps(r) + "\n" for r in prev.values()))
    usage = {"requests": budget.requests, "cache_hits": budget.cache_hits, "physical_attempts": budget.attempts,
             "attempt_ceiling": ATTEMPT_CEILING, "errors": budget.errors, "spent_usd": str(budget.spent),
             "spend_cap_usd": str(SPEND_CAP), "stopped": stop["reason"], "answered": len(out)}
    runs = REG / "jev_runs.jsonl"
    with runs.open("a") as f:
        f.write(json.dumps({"at": datetime.datetime.now(datetime.UTC).isoformat(), "sections_requested": len(ids), **usage}) + "\n")
    return out, usage


def target_set(name):
    secs = sections()
    m = json.loads((REG / "match.json").read_text())["sections"]
    if name == "calibration":
        pos = [s for s in secs if m[s]["atom_ids"] or m[s]["gap_5a"]]
        neg = [x["section_id"] for x in json.loads((REG / "calibration_negatives.json").read_text())["negatives"]]
        return pos + neg
    if name == "triage":
        return [s for s in secs if not m[s]["atom_ids"]]
    raise SystemExit(f"unknown set {name}")


def main():
    args = sys.argv[1:]
    conc = int(args[args.index("--concurrency") + 1]) if "--concurrency" in args else 8
    limit = int(args[args.index("--limit") + 1]) if "--limit" in args else None
    if args[0] == "ask":
        ids = [a for a in args[1:] if not a.startswith("--") and not a.isdigit()]
    elif args[0] == "run":
        ids = target_set(args[args.index("--set") + 1])
    else:
        raise SystemExit(__doc__)
    if limit:
        ids = ids[:limit]
    out, usage = asyncio.run(run(ids, conc))
    if args[0] == "ask":
        for r in out:
            print(r["section_id"], r["role"], r["role_probabilities"], r["role_confidence"], r["chain_duty"], r["returned_model"])
    print(json.dumps(usage))


if __name__ == "__main__":
    main()
