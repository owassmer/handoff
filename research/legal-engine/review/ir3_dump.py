"""Dump the round-3 in-scope atoms (full JSON, including construction and reasoning) to a scratch text file."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ATOMS = {}
for k in ("NY", "NYC", "US"):
    for a in json.loads((ROOT / f"stage-a/{k}.json").read_text())["atoms"]:
        ATOMS[a["id"]] = a

ROUND2 = """NY:MDL-4(7)-multiple-dwelling NY:MDL-301(1) NY:MDL-302(1)(b) NY:MDL-325(2) NY:MDL-302-a(3)
NY:CPLR-214-i-consumer-debt-S9760 NY:RPL-214 NY:RPL-214(15)-high-rent NY:ADJ-willful-standard NY:ADJ-lease-break-charge
NY:ADJ-early-departure-rent-retention NY:ABP-1422 NY:23NYCRR-1.1(d)-not-lease NY:CPLR-3215(g)(3) NYC:ADC-27-2107(b)-rent-stay""".split()
SWEEP = """NY:ADJ-MDL-rent-bar-not-1-2-family NY:ADJ-RPL-232-after-october NY:ADJ-RPL-232-agreement-sets-end
NY:ADJ-RPL-232-indefinite-term NY:ADJ-RPL-232-monthly-letting NY:ADJ-RPL-232-oral-term-over-one-year
NY:ADJ-broker-owner-and-staff NY:ADJ-vacate-order-rent NY:COMMONLAW-constructive-eviction
NY:COMMONLAW-mortgagee-assignment-of-rents NY:COMMONLAW-owner-death-agency NY:CPLR-3015(e)-licence-pleading
NY:CPLR-6401-foreclosure-receiver NY:HANDOFF-broker-config-collection-agency
NY:HANDOFF-broker-config-collects-rent NY:HANDOFF-broker-config-settlement-only
NY:HANDOFF-broker-config-under-broker NY:RPAPL-776-778-administrator NY:RPL-232 NY:RPL-235-a
NY:RPL-440(1)-rent-collection NY:RPL-442-d-442-e-unlicensed NY:RPL-442-f-exemptions NY:RPL-442-fee-split
NYC:HMC-27-2017.5-turnover NYC:HMC-27-2045-detector-charge NYC:HMC-27-2056.8-lead-turnover
NYC:HMC-27-2087-cellar-basement NYC:HMC-27-2128-owner-debt NYC:HMC-27-2135(c)-receiver-rents
NYC:HMC-27-2147-rent-levy US:11USC1107-1306-owner-reorganization US:11USC541-704-owner-chapter7
US:24CFR982.404(d)(3)-(4)""".split()

if __name__ == "__main__":
    extra = sys.argv[1:]
    out = []
    for label, ids in (("ROUND2", ROUND2), ("SWEEP", SWEEP), ("EXTRA", extra)):
        for i in ids:
            a = ATOMS.get(i)
            out.append(f"===== {label} {i}")
            out.append(json.dumps(a, indent=1, ensure_ascii=False) if a else "MISSING")
    p = pathlib.Path(__import__("os").environ.get("TMPDIR", "/tmp")) / "ir3_atoms.txt"
    p.write_text("\n".join(out))
    print(p, len(ROUND2), len(SWEEP), sum(1 for i in ROUND2 + SWEEP if i not in ATOMS), "missing")
