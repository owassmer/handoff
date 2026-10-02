"""Branch test: an accepted case requirement that the vendor's offer does not state is ordered and confirmed.

Runs only against global branch ri.branch..branch.dc8da35a-b273-4a16-9867-5df0a514608c. Main is read, never written.
"""
import hashlib
import json
import sys
import time

from fapi import B, apply, call, objects, O

REQ = "Keep the existing entrance door."
OUT = "result.json"
state = {"steps": []}


def save():
    json.dump(state, open(OUT, "w"), indent=1)


def step(name, code, body):
    err = body.get("_body", "")[:600] if code != 200 else ""
    state["steps"].append({"at": time.strftime("%H:%M:%S", time.gmtime()), "name": name, "code": code, "error": err})
    print(state["steps"][-1], flush=True)
    save()


def mine(api, ws):
    return [x for x in objects(api) if x.get("workspaceId") == ws]


def counts_main():
    return {api: len(objects(api, branch=False)) for api in ["HandoffWorkspace", "HandoffCase", "HandoffJob", "HandoffMessage"]}


state["mainBefore"] = counts_main()
ws = "workspace:a9578a5862eee0ba9020f3001e2e8d3ed8a19b6c7bf0ba1517c3dc4fc4d08cc0"  # created 05:08 UTC on the branch; reused
state["workspaceId"] = ws

n = json.load(open("../w2/w2_notice.json"))
n["sourceRecordId"] = "w5-notice-1"
n["title"] = "Garden house entrance"
n["fixedRequirements"] = [REQ]
owner = "party:" + hashlib.sha256(json.dumps([ws, n["sourceSystem"], "owner"], separators=(",", ":")).encode()).hexdigest()
for d in n["documents"]:
    if d["kind"] == "Owner funding":
        det = json.loads(d["detailsJson"]); det["ownerPartyId"] = owner; d["detailsJson"] = json.dumps(det)
for attempt in range(16):
    code, b = apply("receive-move-out-notice", {"workspaceId": ws, "noticeJson": json.dumps(n), "commandId": "ferro-w5-notice-1"})
    step(f"receive notice (attempt {attempt + 1})", code, b)
    if code == 200 or "NotIndexed" not in b.get("_body", ""):
        break
    time.sleep(60)
if code != 200:
    sys.exit(1)
h = [e["primaryKey"] for e in b["edits"]["edits"] if e["objectType"] == "HandoffCase"][0]
state["handoffId"] = h


def work():
    return mine("HandoffAgentWork", ws)[0]


def plan():
    c = [x for x in mine("HandoffCase", ws) if x["handoffId"] == h][0]
    return next((p for p in mine("HandoffWorkPlan", ws) if p["workPlanId"] == c.get("workPlanId")), None)


def resume(label):
    code, b = apply("resume-handoff", {"handoffId": h})
    w = work()
    step(f"{label}: resume -> {w.get('status')} | {str(w.get('nextStep'))[:140]}", code, b)


# Plan phase
for i in range(10):
    resume(f"plan turn {i + 1}")
    p = plan()
    if p and p.get("status") == "Ready":
        break
    time.sleep(65)
p = plan()
state["plan"] = p and {k: p.get(k) for k in ["workPlanId", "revision", "status", "title", "fixedRequirements", "estimatedCostCents", "budgetCents"]}
save()
if not p or p.get("status") != "Ready":
    print("no plan", flush=True); sys.exit(2)

code, b = apply("accept-handoff-work-plan", {"workPlanId": p["workPlanId"], "expectedRevision": int(p["revision"]), "commandId": "ferro-w5-accept-1"})
step("accept plan", code, b)

# Delivery phase
for i in range(16):
    time.sleep(65)
    resume(f"delivery turn {i + 1}")
    jobs = mine("HandoffJob", ws)
    if jobs and jobs[0].get("status") in ("Scheduled", "Underway", "Awaiting check", "Complete"):
        break

state["jobs"] = [{k: j.get(k) for k in ["title", "status", "requirements", "appointmentAt", "progressSummary"]} for j in mine("HandoffJob", ws)]
msgs = sorted(mine("HandoffMessage", ws), key=lambda m: m.get("createdAt", ""))
state["messages"] = [{k: m.get(k) for k in ["createdAt", "direction", "purpose", "title", "body", "detailsJson"]} for m in msgs]
state["work"] = {k: work().get(k) for k in ["status", "nextStep"]}
state["mainAfter"] = counts_main()
save()
print("done", flush=True)
