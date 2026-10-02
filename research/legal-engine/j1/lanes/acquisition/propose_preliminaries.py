"""Write lane proposals only; replace invented 'preliminary' units with named source units.

Scope/source basis: saved official root TOCs under j1/sources. Live display-text
route observations are separate in preliminary_route_observations.json. This
script does not fetch source text or modify canonical jurisdiction registers.
"""
import json
from pathlib import Path
from urllib.parse import urlencode

HERE = Path(__file__).resolve().parent
J1 = HERE.parents[1]
CAPTIONS = {code: ["GENERAL PROVISIONS"] for code in
            "BPC CORP FIN GOV HNC HSC INS LAB MVC PRC PUC RTC SHC UIC WAT WIC".split()}
CAPTIONS.update({
    "FAC": ["GENERAL PROVISIONS AND DEFINITIONS"],
    "FGC": ["General Provisions and Definitions"],
    "VEH": ["General Provisions"],
    "CIV": ["TITLE OF THE ACT", "PRELIMINARY PROVISIONS", "DEFINITIONS AND SOURCES OF LAW", "EFFECT OF THE 1872 CODES"],
    "CCP": ["TITLE OF ACT", "PRELIMINARY PROVISIONS"],
    "PEN": ["TITLE OF THE ACT", "PRELIMINARY PROVISIONS"],
})


def proposals():
    census = json.loads((J1 / "code_root_census.json").read_text())
    result = []
    for code in sorted(census):
        units = [{"unit": caption, "heading": caption,
                  "toc_url": "https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?" +
                             urlencode({"lawCode": code, "heading2": caption}),
                  "reason": "Shared code construction, definitions or commencement; actual unnumbered source unit."}
                 for caption in CAPTIONS.get(code, [])]
        note = "Replace the invented preliminary placeholder with the named unnumbered root units."
        if not units:
            note = ("Remove the invented preliminary placeholder: the saved root TOC has no separate unnumbered "
                    "general-provisions unit. Construction provisions in numbered divisions/titles remain the code lane's scope.")
        if code == "ELEC":
            note = "No preliminary unit added; code scope is excluded by the code lane."
        if code == "CONS":
            note = ("Remove the invented preliminary placeholder. The actual PREAMBLE remains a selected source; "
                    "it needs its own exact acquisition entry, separate from numbered article sections.")
        result.append({"instrument": f"CA:{code}", "replace_unit": "preliminary", "with_units": units,
                       "source_capture": census[code]["source_capture"], "integration_note": note})
    return result


if __name__ == "__main__":
    (HERE / "ca_preliminary_proposals.json").write_text(json.dumps(proposals(), indent=2) + "\n")
