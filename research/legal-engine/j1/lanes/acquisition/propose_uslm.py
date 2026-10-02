"""Connect already selected legacy USC unit labels to the existing XML grouping.

Reads a register after scope reconciliation; writes only lane proposals. The
119-111 release is only the existing register's asserted pointer; this pass has
not independently retrieved that release and does not assert currentness.
Caller may pass a register path; no downloads or canonical writes occur.
"""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2]
sys.path.insert(0, str(BASE))
from register.tools.scope import USC


def propose(instruments):
    specs = {s["id"]: s for s in USC}
    proposals = []
    for instrument in instruments:
        spec = specs.get(instrument["id"])
        if not spec or instrument["id"] == "US:FRBP":
            continue
        if spec.get("note_of"):
            proposals.append({"instrument": instrument["id"], "integration_note":
                "Statutory note: select the full enclosing USLM section /us/usc/t12/s5220 including notes, "
                "or identify the exact note. Do not convert the note label into an invented section identifier."})
            continue
        url = instrument["toc_source_url"]
        proposals.append({"instrument": instrument["id"], "adapter": "usc", "units": [
            {"unit": u["unit"], "toc_url": url, "uslm_parent_heading": spec["filter"], "uslm_unit_depth": spec["depth"]}
            for u in instrument["units_in_scope"]],
            "source_status": "Existing register's asserted release pointer, not independently retrieved in this pass; federal lane must verify the selected release/currentness."})
    return proposals


if __name__ == "__main__":
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "jurisdictions/US/instruments.json"
    data = json.loads(source.read_text())
    instruments = data["instruments"] if isinstance(data, dict) else data
    (HERE / "uslm_route_proposals.json").write_text(json.dumps(propose(instruments), indent=2) + "\n")
