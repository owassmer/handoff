"""Run frozen atomic development requests through the installed Jev SDK.

Use the legal-engine .venv Python. No author expectations are read. A first request
checks connectivity/build/shape before bounded concurrent batches. Results never
change pipeline routing or legal rules. Every invocation needs a fresh output path.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import math
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from pipeline import core, jev
from pipeline.design.agent_jev_code import prepare


def validate_request(row):
    identity = {key: row[key] for key in ("assembler_version", "task_version", "pinned_build", "payload")}
    if prepare.digest(identity) != row["request_hash"]:
        raise ValueError(f"Request hash mismatch: {row['case_id']}")
    payload = row["payload"]
    if set(payload) != {"model", "questions", "state"} or len(payload["questions"]) != 1:
        raise ValueError("Expected one atomic question and exact payload fields")
    question = next(iter(payload["questions"].values()))
    if question["primitive"] != "choice" or set(question["criteria"]) != {"YES", "NO", "INSUFFICIENT"}:
        raise ValueError("Unexpected question primitive or choices")


def validate_response(row, raw):
    if raw.get("model") != row["pinned_build"]:
        raise ValueError(f"Unexpected build {raw.get('model')!r}; expected {row['pinned_build']!r}")
    questions = row["payload"]["questions"]
    answers = raw.get("answers")
    if not isinstance(answers, dict) or set(answers) != set(questions):
        raise ValueError("Missing or unexpected answer IDs")
    qid = next(iter(questions))
    answer = answers[qid]
    allowed = questions[qid]["criteria"]
    if not isinstance(answer, dict) or answer.get("choice") not in allowed:
        raise ValueError("Missing or unknown answer choice")
    probabilities = answer.get("probabilities")
    if probabilities is not None:
        if not isinstance(probabilities, dict) or set(probabilities) != set(allowed):
            raise ValueError("Unexpected probability keys")
        values = list(probabilities.values())
        if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x)
               or not 0 <= x <= 1 for x in values) or abs(sum(values) - 1) > 0.02:
            raise ValueError("Invalid probabilities")
    return answer


def write(path, obj):
    path.write_text(jev.redact(json.dumps(obj, ensure_ascii=False, indent=2)) + "\n")


async def execute(rows, output, cap, concurrency, response_validator=validate_response):
    from pydantic import BaseModel, ConfigDict
    from typesafe_sdk import AsyncTypeSafeClient, RetryPolicy
    import httpx2

    class Raw(BaseModel):
        model_config = ConfigDict(extra="allow")

    budget = jev.Budget(cap, len(rows) * 3)
    records = []
    # No retries: make attempted request count and failures explicit for this experiment.
    physical_attempts = 0

    async def count(_request):
        nonlocal physical_attempts
        physical_attempts += 1

    # Retain the project's conservative reservation; actual attempts have retries disabled.
    config = core.questions()
    client = AsyncTypeSafeClient(api_key=jev.api_key(), base_url=config["base_url"],
                                retry=RetryPolicy(max_retries=0),
                                http_client=httpx2.AsyncClient(timeout=30.0, event_hooks={"request": [count]}))

    async def one(row):
        started = time.monotonic()
        result = {"case_id": row["case_id"], "request_hash": row["request_hash"], "status": "not_sent"}
        try:
            att, reserve = budget.reserve(len(json.dumps(row["payload"])))
        except RuntimeError as exc:
            result["error"] = str(exc)
            return result
        try:
            payload = row["payload"]
            response = await client.system_one(state=payload["state"],
                        questions=jev.sdk_questions(payload["questions"]), model=payload["model"], response_model=Raw)
            raw = response.model_dump(mode="json")
            result["raw"] = raw
            cost = (raw.get("usage") or {}).get("cost")
            from decimal import Decimal
            reported = Decimal(str(cost)) if cost is not None else None
            if reported is not None and (not reported.is_finite() or reported < 0):
                raise ValueError("Invalid reported cost")
            budget.spent += reported if reported is not None else reserve
            result["answer"] = response_validator(row, raw)
            result["status"] = "answered"
        except Exception as exc:
            result["status"] = "invalid_response" if "raw" in result else "execution_error"
            result["error"] = jev.redact(f"{type(exc).__name__}: {exc}")[:600]
        finally:
            budget.release(att, reserve)
            budget.attempts += 1
        result["elapsed_seconds"] = round(time.monotonic() - started, 4)
        return result

    started = time.monotonic()
    async with client:
        for start in range(0, len(rows), concurrency):
            # The first request is intentionally isolated; remaining requests run in batches.
            if start == 0:
                first = await one(rows[0])
                records.append(first)
                if first["status"] != "answered":
                    break
                batch = rows[1:concurrency]
            else:
                batch = rows[start:start + concurrency]
            records.extend(await asyncio.gather(*(one(row) for row in batch)))
            write(output / "results.json", records)
            if any(r["status"] != "answered" for r in records):
                break
    done = {r["case_id"] for r in records}
    records.extend({"case_id": r["case_id"], "request_hash": r["request_hash"], "status": "not_sent",
                    "error": "Stopped after an earlier failed request"} for r in rows if r["case_id"] not in done)
    write(output / "results.json", records)
    summary = {"requested": len(rows), "answered": sum(r["status"] == "answered" for r in records),
               "physical_attempts": physical_attempts, "accounted_spend_usd": str(budget.spent),
               "spend_cap_usd": str(cap), "budget_note": "Uses existing project reservation estimate; not a provider-enforced billing cap.",
               "elapsed_seconds": round(time.monotonic() - started, 4), "retries": 0,
               "concurrency_after_first": concurrency, "accuracy": None,
               "status": "complete" if all(r["status"] == "answered" for r in records) else "incomplete"}
    write(output / "summary.json", summary)
    print(json.dumps(summary))
    return 0 if summary["status"] == "complete" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requests", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cap", type=float, default=0.25)
    parser.add_argument("--concurrency", type=int, default=4)
    args = parser.parse_args()
    if not math.isfinite(args.cap) or args.cap <= 0 or args.concurrency < 1:
        parser.error("Positive finite cap and positive concurrency required")
    rows = [json.loads(line) for line in args.requests.read_text().splitlines() if line.strip()]
    if not rows or len({r["case_id"] for r in rows}) != len(rows):
        parser.error("Requests must be nonempty with unique case IDs")
    for row in rows:
        validate_request(row)
    args.output.mkdir(parents=True, exist_ok=False)
    write(args.output / "requests.json", rows)
    return asyncio.run(execute(rows, args.output, args.cap, args.concurrency))


if __name__ == "__main__":
    raise SystemExit(main())
