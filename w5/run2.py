"""Branch test part 2: accept the Ready plan on the branch, then run order turns until the job is booked."""
import json
import time

from fapi import apply, objects

r = json.load(open("result.json"))
ws, h = r["workspaceId"], r["handoffId"]
state = {"steps": [], "workspaceId": ws, "handoffId": h}


def mine(api):
    return [x for x in objects(api) if x.get("workspaceId") == ws]


def save():
    json.dump(state, open("result2.json", "w"), indent=1)


def step(name, code, body):
    state["steps"].append({"at": time.strftime("%H:%M:%S", time.gmtime()), "name": name, "code": code,
                           "error": body.get("_body", "")[:600] if code != 200 else ""})
    print(state["steps"][-1], flush=True)
    save()


def counts_main():
    return {api: len(objects(api, branch=False)) for api in ["HandoffWorkspace", "HandoffCase", "HandoffJob", "HandoffMessage"]}


state["mainBefore"] = counts_main()
case = [x for x in mine("HandoffCase") if x["handoffId"] == h][0]
plan = [p for p in mine("HandoffWorkPlan") if p["workPlanId"] == case["workPlanId"]][0]
state["planAccepted"] = {k: plan.get(k) for k in ["workPlanId", "revision", "status", "fixedRequirements"]}
code, b = apply("accept-handoff-work-plan", {"workPlanId": plan["workPlanId"], "expectedRevision": int(plan["revision"]), "commandId": "ferro-w5-accept-2"})
step(f"accept plan rev {plan['revision']}", code, b)
if code == 200:
    for i in range(16):
        time.sleep(65)
        code, b = apply("resume-handoff", {"handoffId": h})
        w = mine("HandoffAgentWork")[0]
        step(f"order turn {i + 1}: {w.get('status')} | {str(w.get('nextStep'))[:160]}", code, b)
        jobs = mine("HandoffJob")
        if jobs and jobs[0].get("status") in ("Scheduled", "Underway", "Awaiting check", "Complete"):
            break
state["jobs"] = [{k: j.get(k) for k in ["title", "status", "requirements", "appointmentAt", "progressSummary"]} for j in mine("HandoffJob")]
msgs = sorted(mine("HandoffMessage"), key=lambda m: m.get("createdAt", ""))
state["messages"] = [{k: m.get(k) for k in ["createdAt", "direction", "purpose", "title", "body", "detailsJson"]} for m in msgs]
state["mainAfter"] = counts_main()
save()
print("done", flush=True)
