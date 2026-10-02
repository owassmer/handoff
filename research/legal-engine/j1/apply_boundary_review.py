"""Apply the root's reviewed J1 selections; this does not determine completion."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
from collections import Counter
from urllib.parse import unquote, urlsplit

from build_register import save

BASE = Path(__file__).resolve().parents[1]
HERE = BASE / "j1"


def read(relative):
    return json.loads((BASE / relative).read_text())


def append_unique(target, values):
    for value in values:
        if value not in target:
            target.append(deepcopy(value))


def set_fields(target, fields):
    for dotted, value in fields.items():
        parts = dotted.split(".")
        parent = target
        for part in parts[:-1]:
            parent = parent.setdefault(part, {})
        parent[parts[-1]] = deepcopy(value)


def document(unit, heading, ref, reason):
    return {"unit": unit, "heading": heading, "adapter": "generic",
            "toc_url": ref, "source_unit_kind": "document", "reason": reason,
            "section_list": [{"number": unit, "heading": heading, "ref": ref}]}


def main():
    path = HERE / "register_updates.json"
    backup = HERE / "history" / "before-boundary-integration"
    backup.mkdir(parents=True, exist_ok=True)
    if not (backup / path.name).exists():
        shutil.copy2(path, backup / path.name)
    data = read("j1/register_updates.json")
    entries = {i["id"]: i for i in data["instruments"]}
    for code in ("US", "CA", "CA-OC", "CA-HB"):
        for item in read(f"jurisdictions/{code}/instruments.json")["instruments"]:
            entries.setdefault(item["id"], item)

    local = read("j1/lanes/acquisition/restored-local/integration-review-patch.json")
    for patch in local["updates"]:
        item = entries[patch["id"]]
        set_fields(item, patch.get("set_fields", {}))
        for field, values in patch.get("append_fields", {}).items():
            append_unique(item.setdefault(field, []), values)
        for unit_patch in patch.get("unit_updates_by_unit", []):
            matches = [u for u in item["units_in_scope"] if u["unit"] == unit_patch["unit"]]
            if len(matches) != 1:
                raise ValueError(f"Expected one unit for {patch['id']}: {unit_patch['unit']}")
            set_fields(matches[0], unit_patch["set_fields"])
    for item in local["add"]:
        entries[item["id"]] = deepcopy(item)
    clarifications = read("j1/lanes/acquisition/restored-local/final-selection-clarifications.json")
    for patch in clarifications["updates"]:
        item = entries[patch["id"]]
        set_fields(item, patch.get("set_fields", {}))
        for field, values in patch.get("append_fields", {}).items():
            append_unique(item.setdefault(field, []), values)
        item["final_selection_evidence"] = deepcopy(patch["evidence"])
    ordinance = entries["CA-HB:ORD4348"]
    ordinance["current_publication_evidence"] = "City publication identifies the first amendment as effective July2,2026; certified June2 minutes now establish ordinance adoption. See final_selection_evidence."
    for route in ordinance.get("alternate_source_routes", []):
        if "7348631" in route["ref"]:
            route["role"] = "Certified June2,2026 minutes, item24 pages14–16; adoption and corrected vote read."
    layer_path = HERE / "function_layer_decisions.json"
    if not (backup / layer_path.name).exists():
        shutil.copy2(layer_path, backup / layer_path.name)
    layers = read("j1/function_layer_decisions.json")
    layers["CA-HB"] = [x for x in layers["CA-HB"] if x["function"] != "data_security"]
    save(layer_path, layers)
    tbra = entries["CA-HB:TBRA-GUIDELINES-2020"]
    tbra["functions"] = list(dict.fromkeys("early_termination" if f == "termination" else f for f in tbra["functions"]))

    boundary = read("j1/lanes/acquisition/boundary-scope-review-delta.json")
    rain = deepcopy(boundary["rainwater_instrument"])
    rain["level"] = "agency rule"
    for unit in rain["units_in_scope"]:
        unit.setdefault("heading", unit["unit"])
    entries[rain["id"]] = rain
    sce = entries["CA:SCE-TARIFF"]
    sce_delta = read("j1/lanes/acquisition/sce-acquisition-units-delta.json")
    census_path = "j1/lanes/acquisition/" + sce_delta["census_file"]
    exclusions = {x["source_document_url"]: x for x in boundary["tariff_exclusions"]}
    sce["units_in_scope"] = []
    out = []
    for unit in sce_delta["replace_pending_with_selected_units"]:
        decision = exclusions.get(unit["source_document_url"])
        if decision:
            out.append({**deepcopy(unit), "reason": decision["reason"],
                        "scope_source_basis": decision["source_basis"]})
        else:
            sce["units_in_scope"].append(deepcopy(unit))
    for row in read(census_path):
        if row["scope"] == "out":
            out.append({"unit": row["name"], "heading": row["heading"],
                        "source_url": row["document_url"], "reason": row["scope_reason"]})
    sce["units_out"] = out
    names = Counter(u["unit"] for u in sce["units_in_scope"])
    for unit in sce["units_in_scope"]:
        if names[unit["unit"]] > 1:
            folder = Path(unquote(urlsplit(unit["source_document_url"]).path)).parent.name
            unit["shared_form_identity"] = unit["unit"]
            unit["unit"] += " — " + folder
            for section in unit["section_list"]:
                section["number"] += " — " + folder
            unit["version_note"] = "Same form number occurs in distinct publisher folders with different file metadata. Preserve both source candidates for J2 edition reconciliation; do not assert identical bodies or separate legal obligations."
    version_review = HERE / "reassessment" / "sce" / "version-decisions.json"
    if version_review.exists():
        settled = json.loads(version_review.read_text())
        sce["units_in_scope"] = [u for u in sce["units_in_scope"] if "shared_form_identity" not in u] + deepcopy(settled["selected_units"])
        sce["source_version_reassessment"] = {"evidence": "j1/reassessment/sce/version-decisions.json", "decision": "Actual sheets distinguish five edition pairs and two same-edition publication aliases; J1 identity/status reconciliation completed."}
    if "pending_acquisition_units" in sce:
        sce["historical_pending_identities"] = sce.pop("pending_acquisition_units")
    sce["adapter"] = "sharepoint"
    sce["acquisition"] = {
        "text_adapter": "sharepoint",
        "status": "Selected current publisher file identities and observed public folder routes; complete body capture and legal edition reconciliation are J2.",
        "source_census": census_path,
        "edition_limit": "Publisher modification timestamps are not tariff operative dates. Read actual sheet status, effective dates and CPUC approval conditions downstream.",
        "route": "Each explicit reference binds the observed public share folder to the exact server-relative document path. The registered adapter uses the public browser session.",
    }
    sce["census_limit"] = "Current observed publisher census, with reasoned selected and excluded document units. Repeated form numbers in different folders remain separately identified source candidates for edition reconciliation, not independently asserted legal obligations."
    sce["scope_boundary_review"] = boundary["retained_families"]
    if "named_pending_action" in sce:
        sce["historical_action_lead"] = sce.pop("named_pending_action")
        sce["historical_action_lead"]["current_selection"] = "Current Rule31 is identified in the selected live publisher census. The old calendar lead no longer establishes a missing instrument; the actual sheet resolves approval/operation during J2."
    entries["CA:SOCALGAS-TARIFF"]["scope_boundary_review"] = boundary["socalgas"]

    reviewed = read("j1/lanes/j1-selection-final-exclusions.json")
    for decision in reviewed["exclusions"]:
        item = entries[decision["instrument_id"]]
        if item["units_in_scope"]:
            item.setdefault("historical_selected_units", deepcopy(item["units_in_scope"]))
        if item["functions"]:
            item.setdefault("historical_function_assignments", deepcopy(item["functions"]))
        item["units_in_scope"] = []
        item["functions"] = []
        item["units_out"] = [{"unit": "Complete act", "heading": decision["actual_subject"],
                              "source_url": decision["primary_url"], "reason": decision["reason"]}]
        item["selection_status"] = "excluded_from_operating_aperture"
        item["selection_review"] = deepcopy(decision)
        item.setdefault("acquisition", {})["status"] = "Discovery retained; no J2 harvest required for this excluded act."

    outcomes = read("j1/lanes/local_agency/regulatory/restored-access/narrow-outcome-findings.json")
    gg, oehha = outcomes["actions"]
    ccr4 = entries["CA:CCR4"]
    for record in ccr4["version_records"]:
        if "2026-0826" in record["action"]:
            record["agency_adoption"] = deepcopy(gg)
            record["legal_status"] = "Permanent package adopted by CAEATFA August18,2026, Resolution26-08-4.C. The OAL outcome and resulting operative text are not established by the acquired records. Preserve both emergency chains independently."
            record["remaining"] = "Downstream version acquisition must establish OAL action and operative text before applying the permanent amendments. J1 selects the existing and agency-adopted package; it does not assert approval or lapse."
    adoption = document("GoGreen-business-permanent-adoption-2026", "CAEATFA August18,2026 adopted permanent GoGreen Business amendments", gg["source_url"],
                        "Agency adoption identifies permanent multifamily retrofit/financing amendments; read minutes pages6–7 with the selected existing regulatory package.")
    if not any(u["unit"] == adoption["unit"] for u in ccr4["units_in_scope"]):
        ccr4["units_in_scope"].append(adoption)
    ccr27 = entries["CA:CCR27"]
    record = {"action": oehha["action"], "section": oehha["unit"],
              "subject": oehha["identified_subject"], "agency_adoption": oehha["agency_adoption"],
              "oal_outcome": oehha["oal_outcome"], "source_urls": oehha["source_urls"],
              "text_route": oehha["text_route"], "text_route_limit": oehha["text_route_limit"],
              "j1_decision": oehha["selection_decision"]}
    ccr27["version_records"] = [v for v in ccr27.get("version_records", []) if v.get("action") != record["action"]] + [record]
    package = document("OEHHA-25705-2026-submitted-package", "OEHHA25705(b)(1) submitted amendment package and published rulemaking materials", oehha["text_route"],
                       "Proposition65 exposure thresholds bear on residential remediation, materials and warnings. Select the identified submitted amendment alongside existing Title27; published proposal bodies are not certified final text.")
    package["status_evidence"] = deepcopy(record)
    ccr27["units_in_scope"] = [u for u in ccr27["units_in_scope"] if u["unit"] != package["unit"]] + [package]

    oc = entries["CA-OC:CODE"]
    oc.pop("unresolved_unit_routes", None)
    oc["acquisition_route_limits"] = "All selected code/history node IDs are now observed in publisher job488007. J2 expands or reads the exact selected nodes; historical search captures are not substitutes for current text."
    airport = read("j1/lanes/local_agency/regulatory/restored-access/oc-airport/selection-delta.json")
    emergency = entries[airport["parent_source_id"]]
    for name, selected in zip(("AIRPORT-LOCAL-PROCLAMATION-2024", "AIRPORT-ORD24-006"), airport["instruments"]):
        unit = document(name, selected["identity"], selected["source_route"], selected["operating_connection"])
        unit["source_selection"] = deepcopy(selected)
        unit["acquisition_note"] = "Acquire the carrier packet and extract only the identified attachment/pages as this instrument. The PDF fragment is a reader locator, not an assertion of adapter page filtering."
        emergency["units_in_scope"] = [u for u in emergency["units_in_scope"] if u["unit"] != name] + [unit]
    emergency.pop("unresolved_dependencies", None)
    emergency["airport_selection_review"] = "Original adopted action and signed debris ordinance now identified with exact attachment/page routes. Historical survival, duration and charge effects are downstream interpretation."

    ccr14 = entries["CA:CCR14"]
    bof = next(v for v in ccr14["version_records"] if v.get("oal_file") == "2025-1119-03")
    for unit in ccr14["units_in_scope"]:
        if any(s.get("number") == "CCR14-BOF-2025-1119-03" for s in unit.get("section_list", [])):
            unit["legal_status"] = bof["legal_status"]
            unit["withdrawn_proposals"] = deepcopy(bof["withdrawn_subsections"])
            unit["operative_dates"] = deepcopy(bof["operative_dates"])
            unit["acquisition_note"] = "Signed partial approval and withdrawal read; preserve the version record's reconciliation with marked text and conflicting published histories. Complete section capture is J2."
    ccr24 = entries["CA:CCR24"]
    part7 = read("j1/lanes/federal_programs/restored-access/part7-filing-continuity-delta.json")
    ccr24["part7_stage_boundary"] = part7["j1_boundary"]
    ccr24["version_records"][0]["remaining_dependency"] = "May6 readoption and August25 certifying-package approvals established. Exact filing and operative continuity interval belong to downstream version acquisition and interpretation."
    ccr24["intervening_cycle_identity_review"]["boundary"] = "Historical package-identity review supplemented by the August adoption sources and final action map. Adopted packages and selected units/routes are established; complete final-text capture, filing and operative-date compilation follow J1."
    for decision in ccr24["intervening_cycle_identity_review"].get("effective_date_decisions", []):
        if "Final express terms/action matrices still needed" in decision.get("decision", ""):
            decision["decision"] = "Package-specific final materials and action matrices now selected; preserve the separate evidence for commission approval, publication and operative dates. Exact temporal compilation follows J1."
    fees = entries["CA-HB:FEES2026:COMPLETE"]
    for related in fees.get("remaining_related_source_selections", []):
        ident = {"CA-HB:RES2026-07": "CA-HB:WEED-RES2026-07", "CA-HB:RES2026-32": "CA-HB:WEED-RES2026-32"}.get(related["id"], related["id"])
        selected = entries[ident]
        related.update(id=ident, url=selected["toc_source_url"], status="Related instrument selected with exact source route; detailed provision/page processing is J2.")
    fees["related_source_selections"] = fees.pop("remaining_related_source_selections", fees.get("related_source_selections", []))
    save(path, {**data, "instruments": list(entries.values())})


if __name__ == "__main__":
    if (Path(__file__).resolve().parent / "reassessment/moved-items.json").exists():
        raise SystemExit("Historical boundary integration superseded by j1/reassessment/apply_reassessment.py; refusing to restore withdrawn decisions.")
    main()
