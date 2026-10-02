"""Smoke test on ri.branch..branch.0e1ca62b-0361-4582-94e8-13e2af9596b4: a small case plans under release 1.6.6. Main is read only."""
import hashlib, json, sys, time
from fapi import apply, objects

state = {"steps": []}
def save(): json.dump(state, open("result.json", "w"), indent=1)
def step(name, code, body):
    state["steps"].append({"at": time.strftime("%H:%M:%S", time.gmtime()), "name": name, "code": code,
                           "error": body.get("_body", "")[:500] if code != 200 else ""}); print(state["steps"][-1], flush=True); save()
def counts_main(): return {a: len(objects(a, branch=False)) for a in ["HandoffWorkspace", "HandoffCase", "HandoffWorkPlan", "HandoffMessage"]}

state["mainBefore"] = counts_main()
code, b = apply("create-handoff-workspace", {"name": "Correction test", "commandId": "ferro-w6-workspace-1"}); step("create workspace", code, b)
if code != 200: sys.exit(1)
ws = [e["primaryKey"] for e in b["edits"]["edits"] if e["objectType"] == "HandoffWorkspace"][0]; state["workspaceId"] = ws
n = json.load(open("../w2/w2_notice.json")); n["sourceRecordId"] = "w6-notice-1"; n["title"] = "Garden house entrance"
owner = "party:" + hashlib.sha256(json.dumps([ws, n["sourceSystem"], "owner"], separators=(",", ":")).encode()).hexdigest()
for d in n["documents"]:
    if d["kind"] == "Owner funding":
        det = json.loads(d["detailsJson"]); det["ownerPartyId"] = owner; d["detailsJson"] = json.dumps(det)
for attempt in range(10):
    code, b = apply("receive-move-out-notice", {"workspaceId": ws, "noticeJson": json.dumps(n), "commandId": "ferro-w6-notice-1"})
    step(f"receive notice {attempt + 1}", code, b)
    if code == 200 or "NotIndexed" not in b.get("_body", ""): break
    time.sleep(60)
if code != 200: sys.exit(1)
h = [e["primaryKey"] for e in b["edits"]["edits"] if e["objectType"] == "HandoffCase"][0]; state["handoffId"] = h
def mine(api): return [x for x in objects(api) if x.get("workspaceId") == ws]
for i in range(10):
    code, b = apply("resume-handoff", {"handoffId": h})
    w = mine("HandoffAgentWork")[0]
    step(f"turn {i + 1}: {w.get('status')} | {str(w.get('nextStep'))[:140]}", code, b)
    plans = [p for p in mine("HandoffWorkPlan") if p.get("status") == "Ready"]
    if plans: state["plan"] = {k: plans[0].get(k) for k in ["title", "revision", "fixedRequirements", "estimatedCostCents", "budgetCents"]}; break
    time.sleep(65)
state["messages"] = [{k: m.get(k) for k in ["createdAt", "direction", "purpose", "title"]} for m in sorted(mine("HandoffMessage"), key=lambda m: m.get("createdAt", ""))]
state["mainAfter"] = counts_main(); save(); print("done", flush=True)
