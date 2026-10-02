"""Jev client (J4 triage and calibration), generalized from register/jev_triage.py.

Jev is typesafe/jev-1.13 through OpenRouter, called with typesafe_sdk (installed in research/legal-engine/.venv;
`python3 -m pipeline triage|calibrate` re-runs itself there when the SDK is missing). It answers two typed
questions per section (pipeline/jev_questions.json) and never states law.

Credential: OPENROUTER_API_KEY from the environment, else read at run time from the Slope repository's .env. The key
is never printed, logged or written: every string that reaches a log passes through redact().
Pinned build: every response's model must equal jev_questions.json pinned_build; any other build stops the run
before anything is cached.
Budget: a spend cap per run (provider-reported cost, with a conservative reservation before dispatch) and a
physical-attempt ceiling per run (SDK retries included).
Files, per jurisdiction: jev/cache/<full versioned request identity hash>.json; jev/exchanges.jsonl (request without
credentials plus raw response or error); jev/results.jsonl (answers per section); jev/runs.jsonl (usage per run).
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import pathlib
import re
from decimal import Decimal

from . import core, jev_results as reuse

SLOPE_ENV = pathlib.Path("/Users/owenwassmer/dev/Slope_Sparse_Events/.env")
LONG = 12000
MAX_RETRIES = 2
RESERVE_PRICE_PER_TOKEN = Decimal("0.20") / 10 ** 6
_KEY = {"v": None}


def api_key():
    if _KEY["v"]:
        return _KEY["v"]
    k = os.environ.get("OPENROUTER_API_KEY")
    if not k and SLOPE_ENV.is_file():
        for line in SLOPE_ENV.read_text().splitlines():
            m = re.match(r"\s*(?:export\s+)?OPENROUTER_API_KEY\s*=\s*(.*)\s*$", line)
            if m:
                k = m.group(1).strip().strip('"').strip("'")
    if not k:
        raise core.PipelineError("OPENROUTER_API_KEY not found in the environment or the Slope .env file")
    _KEY["v"] = k
    return k


def redact(s):
    s = str(s)
    k = _KEY["v"]
    if k and k in s:
        s = s.replace(k, "[redacted]")
    return re.sub(r"sk-or-[A-Za-z0-9_\-]{8,}", "[redacted]", s)


def canonical_sha256(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()


def fill(value, prof):
    """Substitute profile scope without flattening structured question content."""
    if isinstance(value, str):
        return value.replace("{scope}", (prof.get("jev") or {}).get("scope") or "a residential unit in this jurisdiction")
    if isinstance(value, dict):
        return {k: fill(v, prof) for k, v in value.items()}
    if isinstance(value, list):
        return [fill(v, prof) for v in value]
    return value


def built_questions(reg, prof):
    """Preserve legacy strings and native structured instructions/criteria."""
    rules = "\n".join(f"- {fill(r, prof)}" for r in reg.get("global_rules", []))
    out = {}
    for q in reg["questions"]:
        instructions = fill(q["prompt"].get("instructions"), prof)
        if rules:
            instructions = (f"Global rules:\n{rules}\n\nQuestion:\n{instructions}"
                            if isinstance(instructions, str) else
                            {"global_rules": fill(reg["global_rules"], prof), "question": instructions})
        spec = {"primitive": q["primitive"], "instructions": instructions}
        if "criteria" in q["prompt"]:
            spec["criteria"] = fill(q["prompt"]["criteria"], prof)
        out[q["id"]] = spec
    return out


def sdk_questions(spec):
    from typesafe_sdk import Choice, Noul, Score
    constructors = {"noul": Noul, "choice": Choice, "score": Score}
    out = {}
    for key, value in spec.items():
        primitive = value["primitive"]
        if primitive not in constructors:
            raise ValueError(f"Unknown Jev primitive: {primitive!r}")
        kwargs = {"instructions": value.get("instructions")}
        if "criteria" in value:
            kwargs["criteria"] = value["criteria"]
        out[key] = constructors[primitive](**kwargs)
    return out


def state_for(sec, prof, inst_names):
    text = (core.ROOT / sec["text_file"]).read_text()
    return {"instrument": f"{inst_names.get(sec['instrument'], sec['instrument'])}, {sec['section_id'].split(':', 1)[1]}",
            "heading": sec.get("heading") or "", "section_text": core.body_of(text),
            "chain_description": (prof.get("jev") or {}).get("chain_description", ""),
            "aperture_exclusions": (prof.get("aperture") or {}).get("exclusions", "")}


def record_from_entry(sid, entry, hit):
    request, raw = entry['request'], entry['raw']
    reuse.validate_entry(entry, request)
    role, duty = raw['answers']['role'], raw['answers']['chain_duty']
    return {'section_id': sid, 'cache_key': entry['request_hash'], 'model': raw['model'],
            'registry_version': request['registry_version'], 'role': role['choice'],
            'role_probabilities': role['probabilities'], 'role_confidence': role['confidence'],
            'chain_duty': duty['noul'], 'usage': raw.get('usage'),
            'created_at': entry['created_at'], 'response_hash': entry['response_hash'], 'cache_hit': hit,
            'origin': {k: request[k] for k in ('format', 'assembly_version', 'base_url', 'model',
                       'pinned_build', 'registry_version', 'question_versions')}}


class Answers(dict):
    """Validated answers plus explicit outcomes for every requested input."""
    def __init__(self):
        super().__init__()
        self.outcomes = []


def prepare(sid, sec, prof, names, reg):
    if sid != sec['section_id']:
        raise ValueError('Section identity mismatch')
    if not sec.get('text_file'):
        raise ValueError('Source text unavailable')
    state = state_for(sec, prof, names)
    if sec.get('chars', 0) > LONG or len(state['section_text']) > LONG:
        raise ValueError('Source exceeds section input limit')
    spec = built_questions(reg, prof)
    if spec.get('role', {}).get('primitive') != 'choice' or spec.get('chain_duty', {}).get('primitive') != 'noul':
        raise ValueError('Triage requires role Choice and chain_duty Noul')
    if 'DECIDES' not in spec['role'].get('criteria', {}):
        raise ValueError('Triage requires DECIDES criterion')
    request = reuse.identity(reg, spec, state)
    reuse.fingerprint(request)  # Reject unserializable/nonfinite prepared input before dispatch.
    return request


def lookup(P, request):
    key = reuse.fingerprint(request)
    path = P['cache'] / f'{key}.json'
    if path.exists():
        entry, error = reuse.read(path, request)
        return entry, {'status': 'cache_hit' if entry else 'cache_rejected',
                       'cache_key': key, 'reason': error}
    # V1 omitted endpoint/pin/version and stored no origin request. It is evidence,
    # not a demonstrably compatible v2 entry. Never rewrite it as current history.
    legacy = canonical_sha256({'model': request['model'], 'questions': request['questions'], 'state': request['state']})
    if (P['cache'] / f'{legacy}.json').exists():
        return None, {'status': 'cache_rejected', 'cache_key': key, 'legacy_cache_key': legacy,
                      'reason': 'Legacy cache lacks complete origin identity; preserved, fresh inference required'}
    return None, {'status': 'cache_miss', 'cache_key': key}


class Budget:
    def __init__(self, cap, ceiling):
        self.cap, self.ceiling = Decimal(str(cap)), int(ceiling)
        self.attempts = self.inflight_attempts = self.requests = self.cache_hits = self.errors = 0
        self.inflight_usd = self.spent = Decimal(0)

    def reserve(self, chars):
        att = 1 + MAX_RETRIES
        est = Decimal(chars // 3 + 1500) * RESERVE_PRICE_PER_TOKEN * att
        if self.attempts + self.inflight_attempts + att > self.ceiling:
            raise RuntimeError(f"attempt ceiling {self.ceiling} reached")
        if self.spent + self.inflight_usd + est > self.cap:
            raise RuntimeError(f"spend cap ${self.cap} would be exceeded")
        self.inflight_attempts += att
        self.inflight_usd += est
        return att, est

    def release(self, att, est):
        self.inflight_attempts -= att
        self.inflight_usd -= est


def paths(code):
    d = core.jdir(code) / "jev"
    return {"dir": d, "cache": d / "cache", "exchanges": d / "exchanges.jsonl", "results": d / "results.jsonl",
            "runs": d / "runs.jsonl"}


def _append(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        f.write(redact(json.dumps(obj, ensure_ascii=False)) + "\n")


def cached_answers(code, items, reg=None):
    """Read only: return validated current answers and per-input lookup outcomes."""
    reg = reg or core.questions()
    P = paths(code)
    out = Answers()
    seen = set()
    for sid, sec, prof, names in items:
        if sid in seen:
            raise core.PipelineError('Duplicate requested section: ' + sid)
        seen.add(sid)
        try:
            request = prepare(sid, sec, prof, names, reg)
            entry, outcome = lookup(P, request)
            if entry:
                out[sid] = record_from_entry(sid, entry, True)
        except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
            outcome = {'status': 'preparation_error', 'reason': str(exc)}
        out.outcomes.append({'section_id': sid, **outcome})
    return out


def preserve_file(path, directory):
    """Keep exact previous bytes before replacing a current snapshot or bad entry."""
    if path.exists():
        raw = path.read_bytes()
        directory.mkdir(parents=True, exist_ok=True)
        target = directory / (hashlib.sha256(raw).hexdigest() + path.suffix)
        if not target.exists():
            reuse.atomic_write(target, raw)


async def _run(code, items, cap, ceiling, concurrency):
    if concurrency < 1:
        raise ValueError('Concurrency must be positive')
    reg = core.questions()
    P = paths(code)
    budget = Budget(cap, ceiling)
    stop = {'reason': None}
    out = Answers()
    jobs = []
    seen = set()
    for sid, sec, prof, names in items:
        if sid in seen:
            raise core.PipelineError('Duplicate requested section: ' + sid)
        seen.add(sid)
        try:
            request = prepare(sid, sec, prof, names, reg)
            entry, outcome = lookup(P, request)
            if entry:
                budget.cache_hits += 1
                out[sid] = record_from_entry(sid, entry, True)
            else:
                jobs.append((sid, request, outcome))
        except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
            outcome = {'status': 'preparation_error', 'reason': str(exc)}
        out.outcomes.append({'section_id': sid, **outcome})

    # SDK and credentials are unnecessary when every request is reusable.
    if jobs:
        import httpx2
        from pydantic import BaseModel, ConfigDict
        from typesafe_sdk import AsyncTypeSafeClient, RetryPolicy

        class Raw(BaseModel):
            model_config = ConfigDict(extra='allow')

        async def count(_req):
            budget.attempts += 1

        qcache = {}
        sem = asyncio.Semaphore(concurrency)
        client = AsyncTypeSafeClient(api_key=api_key(), base_url=reg['base_url'],
                    retry=RetryPolicy(max_retries=MAX_RETRIES),
                    http_client=httpx2.AsyncClient(timeout=120.0, event_hooks={'request': [count]}))

        async def one(sid, request, lookup_outcome):
            key = reuse.fingerprint(request)
            result = {'section_id': sid, 'cache_key': key, 'status': 'not_sent',
                      'lookup': lookup_outcome}
            async with sem:
                if stop['reason']:
                    result['reason'] = stop['reason']
                    return result
                try:
                    att, estimate = budget.reserve(len(reuse.serialized(request)))
                except RuntimeError as exc:
                    stop['reason'] = str(exc)
                    result['reason'] = str(exc)
                    return result
                raw = None
                accounted = False
                created = core.now()
                try:
                    qkey = reuse.fingerprint(request['questions'])
                    if qkey not in qcache:
                        qcache[qkey] = sdk_questions(request['questions'])
                    budget.requests += 1
                    response = await client.system_one(state=request['state'], questions=qcache[qkey],
                                                        model=request['model'], response_model=Raw)
                    raw = response.model_dump(mode='json')
                    cost = reuse.usage_cost(raw)
                    paid = cost if cost is not None else estimate
                    budget.spent += paid
                    accounted = True
                    entry = reuse.envelope(request, raw, created)
                    safe_entry = redact(reuse.serialized(entry))
                    reuse.validate_entry(json.loads(safe_entry), request)
                    path = P['cache'] / f'{key}.json'
                    # Do not destroy an invalid prior entry while recovering with a fresh answer.
                    preserve_file(path, P['dir'] / 'replaced-cache')
                    reuse.atomic_write(path, safe_entry + '\n')
                    out[sid] = record_from_entry(sid, entry, False)
                    result['status'] = 'answered'
                except Exception as exc:
                    budget.errors += 1
                    result.update(status='invalid_response' if raw is not None else 'execution_error',
                                  reason=redact(f'{type(exc).__name__}: {exc}')[:600])
                    if not accounted:
                        budget.spent += estimate  # Unknown billed cost; reserve remains accounted.
                    if isinstance(raw, dict) and raw.get('model') != request['pinned_build']:
                        stop['reason'] = result['reason']
                finally:
                    budget.release(att, estimate)
                    _append(P['exchanges'], {'created_at': created, 'section_id': sid, 'cache_key': key,
                                            'request': request, 'response': raw, 'outcome': result})
            return result

        async with client:
            completed = await asyncio.gather(*(one(*job) for job in jobs))
        by = {r['section_id']: r for r in completed}
        out.outcomes = [by.get(r['section_id'], r) for r in out.outcomes]

    # Snapshot contains only this run's validated results. Preserve old snapshot bytes;
    # append origin-bearing records instead of relabeling old rows under current registry.
    preserve_file(P['results'], P['dir'] / 'result-snapshots')
    reuse.atomic_write(P['results'], ''.join(redact(reuse.serialized(r))+'\n' for r in out.values()))
    for record in out.values():
        _append(P['dir'] / 'result-history.jsonl', {'observed_at': core.now(), 'result': record})
    usage = {'requests': budget.requests, 'cache_hits': budget.cache_hits, 'physical_attempts': budget.attempts,
             'attempt_ceiling': budget.ceiling, 'errors': budget.errors, 'spent_usd': str(budget.spent),
             'spend_cap_usd': str(budget.cap), 'stopped': stop['reason'], 'answered': len(out),
             'requested': len(seen), 'unanswered': len(seen)-len(out), 'outcomes': out.outcomes}
    _append(P['runs'], {'at': core.now(), **usage})
    return out, usage


def run(code, items, cap=2.00, ceiling=12000, concurrency=8):
    """Ask Jev about items [(sid, section, profile, instrument names)]; returns ({sid: record}, usage)."""
    return asyncio.run(_run(code, items, cap, ceiling, concurrency))


def sdk_available():
    try:
        import typesafe_sdk  # noqa: F401
        return True
    except ImportError:
        return False
