"""Build the corrected 142 West 88th Street case on Main through existing Actions. Token from the environment only."""
import hashlib
import json
import os
import urllib.parse
import urllib.request

import case_content as c
from fapi import FH, O, T, apply, call

MS = "ri.mio.main.media-set.b820a6b1-478f-4cf8-bfd1-cc2fbad06427"
out = {"steps": []}


def save():
    json.dump(out, open("ids.json", "w"), indent=1)


def step(name, code, body):
    out["steps"].append({"name": name, "code": code, "operationId": body.get("operationId"), "error": body.get("_body", "")[:400]})
    print(out["steps"][-1], flush=True)
    save()
    if code != 200:
        raise SystemExit(1)


def sid(kind, ws, source):
    return f"{kind}:" + hashlib.sha256(json.dumps([ws, c.SOURCE_SYSTEM, source], separators=(",", ":")).encode()).hexdigest()


code, b = apply("create-handoff-workspace", {"name": c.WORKSPACE_NAME, "commandId": "ferro-w8-workspace-1"}, branch=False)
step("create workspace", code, b)
ws = [e["primaryKey"] for e in b["edits"]["edits"] if e["objectType"] == "HandoffWorkspace"][0]
out["workspaceId"] = ws
code, b = apply("receive-move-out-notice", {"workspaceId": ws, "noticeJson": json.dumps(c.notice(sid("party", ws, "company"))),
                                             "commandId": "ferro-w8-notice-1"}, branch=False)
step("receive notice", code, b)
h = [e["primaryKey"] for e in b["edits"]["edits"] if e["objectType"] == "HandoffCase"][0]
out["handoffId"] = h

files = [("lease.pdf", "Lease, 142 West 88th Street.pdf", "lease"), ("email.pdf", "Laura Brenner email, June 11, 2024.pdf", "laura-email-2024")]
out["items"] = {}
for revision, (local, path, source) in enumerate(files, start=1):
    data = open(local, "rb").read()
    req = urllib.request.Request(f"https://{FH}/api/v2/mediasets/{MS}/items?preview=true&mediaItemPath={urllib.parse.quote(path)}",
                                 data=data, method="POST", headers={"Authorization": "Bearer " + T, "Content-Type": "application/octet-stream"})
    item = json.loads(urllib.request.urlopen(req, timeout=120).read())["mediaItemRid"]
    back = urllib.request.urlopen(urllib.request.Request(f"https://{FH}/api/v2/mediasets/{MS}/items/{item}/content?preview=true",
                                                         headers={"Authorization": "Bearer " + T}), timeout=120).read()
    assert back == data, f"read-back differs for {path}"
    out["items"][path] = item
    code, b = apply("associate-handoff-original", {"handoffId": h, "preparedDocumentId": sid("document", ws, source), "expectedRevision": str(revision),
                                                   "commandId": f"ferro-w8-file-{revision}",
                                                   "sourceJson": json.dumps({"mediaSetRid": MS, "mediaItemRid": item, "kind": "Contextual material"})}, branch=False)
    step(f"associate {path}", code, b)

code, b = call("POST", f"/api/v2/ontologies/{O}/queries/getHandoffWorkspace/execute", {"parameters": {"handoffId": h}})
v = json.loads(b["value"])
out["readBack"] = {"documents": len(v["documents"]), "parties": len(v["parties"]), "agent": v["agent"]["status"],
                   "businessDate": v["handoff"].get("businessDate"), "files": [d["title"] for d in v["documents"] if d.get("sourceKind") == "Original"]}
save()
print(json.dumps(out["readBack"]), flush=True)
