"""Minimal Foundry REST v2 helper for the W5 branch test. Token comes from the environment only."""
import json
import os
import urllib.error
import urllib.request

T = os.environ["FOUNDRY_TOKEN"]
FH = os.environ["FH"]
O = "ri.ontology.main.ontology.cfb1478a-5b0e-466a-aaff-b212870e8861"
B = "ri.branch..branch.dc8da35a-b273-4a16-9867-5df0a514608c"
LOG = os.path.join(os.path.dirname(__file__), "actions_log.jsonl")


def call(method, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(f"https://{FH}{path}", data=data, method=method,
                                 headers={"Authorization": "Bearer " + T, "Content-Type": "application/json"})
    try:
        return 200, json.loads(urllib.request.urlopen(req, timeout=180).read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, {"_body": e.read()[:2000].decode(errors="replace")}


def objects(api, branch=True):
    out, tok = [], None
    while True:
        q = f"?pageSize=500" + (f"&branch={B}" if branch else "") + (f"&pageToken={tok}" if tok else "")
        code, b = call("GET", f"/api/v2/ontologies/{O}/objects/{api}{q}")
        if code != 200:
            raise RuntimeError(f"{api} {code} {b}")
        out += b["data"]
        tok = b.get("nextPageToken")
        if not tok:
            return out


def apply(action, params, branch=True):
    q = "?branch=" + B if branch else ""
    code, b = call("POST", f"/api/v2/ontologies/{O}/actions/{action}/apply{q}",
                   {"parameters": params, "options": {"returnEdits": "ALL"}})
    with open(LOG, "a") as f:
        f.write(json.dumps({"action": action, "params": {k: (v if len(str(v)) < 300 else str(v)[:300] + "...") for k, v in params.items()},
                            "code": code, "response": b}) + "\n")
    return code, b
