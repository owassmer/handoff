"""Render result tables from results.json (no hand-copied numbers)."""
import json

R = json.load(open("results.json")); N = R["names"]; cal = json.load(open("calibration.json"))
pct = lambda x: f"{x * 100:.0f}%"
usd = lambda x: f"${x / 1e6:.1f}M"
out = []

out.append("## Calibration (generic B2B software company)\n")
out.append("| Base rate | Source | Target | Model |\n|---|---|---|---|")
lab = {"m1_36": ("Reach $1M ARR within 3 years of first revenue", "S1"),
       "m1_60": ("Reach $1M ARR within 5 years", "S1"),
       "seed_given_pre": ("Pre-seed companies that raise a seed", "S3"),
       "a24_given_seed": ("Seeded companies that raise a Series A within 24 months", "S2"),
       "dead_given_seed": ("Seeded companies that fail (PitchBook: lifetime; model: within 6 years)", "S5")}
for k, (t, s) in lab.items():
    out.append(f"| {t} | {s} | {pct(cal['targets'][k])} | {pct(cal['check_n20000'][k])} |")

def table(sc, title):
    out.append(f"\n## {title}\n")
    out.append("| Path | Paying customer in 12 mo | $1M ARR by mo 36 | $3M ARR by mo 60 | Pre-seed | Seed | Series A | Any exit by mo 72 | Exit >= $25M | Median exit | Dead | Founders >= $5M |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for k, m in R["base"][sc].items():
        out.append(f"| {k} {N[k]} | {pct(m['first_rev_12m'])} | {pct(m['arr1m_36m'])} | {pct(m['arr3m_60m'])} | "
                   f"{pct(m['raise_pre'])} | {pct(m['raise_seed'])} | {pct(m['raise_A'])} | {pct(m['exit_72m'])} | "
                   f"{m['exit_ge_25m'] * 100:.1f}% | {usd(m['median_exit_value'])} | {pct(m['dead'])} | {m['founder_ge_5m'] * 100:.1f}% |")

table("FT", "Base run: both founders full-time from October 2026 (n = 30,000 per path)")
table("PT", "Base run: founders part-time until the first round")
out.append("\nWith founder or angel capital for the first acquisition, only P8 changes: "
           + ", ".join(f"{k} {pct(v)}" for k, v in (("paying customer in 12 mo", R['base']['FT_CAP']['P8']['first_rev_12m']),
                                                    ("$1M revenue by mo 36", R['base']['FT_CAP']['P8']['arr1m_36m']),
                                                    ("dead", R['base']['FT_CAP']['P8']['dead']),
                                                    ("any exit", R['base']['FT_CAP']['P8']['exit_72m'])))
           + f"; median exit {usd(R['base']['FT_CAP']['P8']['median_exit_value'])}.")

out.append("\n## Uncertainty: median and 10-90% band across 300 parameter draws (full-time)\n")
out.append("| Path | Paying customer in 12 mo | $1M ARR by mo 36 | Seed | Any exit | Exit >= $25M | Dead | Founders >= $5M |")
out.append("|---|---|---|---|---|---|---|---|")
U = R["uncertainty"]
band = lambda d: f"{d['p50'] * 100:.0f}% ({d['p10'] * 100:.0f}-{d['p90'] * 100:.0f})"
for k in U:
    u = U[k]
    out.append(f"| {k} | {band(u['first_rev_12m'])} | {band(u['arr1m_36m'])} | {band(u['raise_seed'])} | {band(u['exit_72m'])} | "
               f"{band(u['exit_ge_25m'])} | {band(u['dead'])} | {band(u['founder_ge_5m'])} |")

out.append("\n## How often each path ranks first (share of 300 draws)\n")
lab2 = {"first_rev_12m": "Paying customer in 12 months", "arr1m_36m": "$1M ARR by month 36", "raise_seed": "Seed round",
        "exit_72m": "Any exit by month 72", "exit_ge_25m": "Exit of $25M or more", "founder_ge_5m": "Founders take home $5M or more",
        "founder_realized_mean": "Expected founder proceeds"}
out.append("| Goal | " + " | ".join(R["wins"]["arr1m_36m"].keys()) + " |")
out.append("|---|" + "---|" * len(R["wins"]["arr1m_36m"]))
for m, w in R["wins"].items():
    out.append(f"| {lab2[m]} | " + " | ".join(pct(v) if v >= 0.005 else "-" for v in w.values()) + " |")

out.append("\n## What decides the close contests (rank correlation with 'first path wins' on expected founder proceeds)\n")
for pr, d in R["drivers"].items():
    a, b = pr.split("_vs_")
    out.append(f"- {a} beats {b} in {pct(d['share_a_wins'])} of draws. Largest drivers: "
               + "; ".join(f"{x} ({c:+.2f})" for x, c in d["top"][:5]) + ".")

open("tables.md", "w").write("\n".join(out) + "\n")
print("\n".join(out))
