"""Calibrate the unsourced global constants on a generic B2B software company.

Targets (SIM.ledger.json):
  S1 ChartMogul: 13.4% reach $1M ARR within 3 years of monetizing; 25.1% within 5 years.
  S3 Incisive: 45-55% of pre-seed companies raise a seed.
  S2 Carta: 20% of seed companies raise a Series A within 24 months.
  S5 PitchBook: roughly one third of seed deals fail.
"""
import copy, json, time
import numpy as np
from model import GENERIC, GLOBAL, simulate

TARGETS = {"m1_36": 0.134, "m1_60": 0.251, "seed_given_pre": 0.50, "a24_given_seed": 0.20, "dead_given_seed": 0.33}
WEIGHTS = {"m1_36": 3.0, "m1_60": 3.0, "seed_given_pre": 1.0, "a24_given_seed": 1.0, "dead_given_seed": 1.0}


def stats(g, n, seed):
    rng = np.random.default_rng(seed)
    r = simulate(GENERIC, n, rng, g=g, start_with_revenue=True)
    h = r["hit1m"]; pre = r["pre"]; sd = r["seed"]
    # seed within 24 months of the seed round -> Series A: approximate with A among seeded companies whose seed came
    # early enough to observe 24 months
    obs = sd & (r["t_seed"] >= 0) & (r["t_seed"] <= 48)
    return {
        "m1_36": float(np.mean((h >= 0) & (h <= 36))),
        "m1_60": float(np.mean((h >= 0) & (h <= 60))),
        "seed_given_pre": float(np.mean(sd[pre])) if pre.any() else 0.0,
        "a24_given_seed": float(np.mean(r["A"][obs])) if obs.any() else 0.0,
        "dead_given_seed": float(np.mean(r["dead"][sd])) if sd.any() else 0.0,
    }


def loss(s):
    return sum(WEIGHTS[k] * (s[k] - TARGETS[k]) ** 2 / TARGETS[k] for k in TARGETS)


def main():
    rng = np.random.default_rng(7)
    best = None; t0 = time.time()
    for i in range(400):
        g = copy.deepcopy(GLOBAL)
        g["lam0"] = float(rng.uniform(0.15, 1.2)); g["p_pre"] = float(rng.uniform(0.05, 0.4))
        g["p_seed"] = float(rng.uniform(0.05, 0.6)); g["p_A"] = float(rng.uniform(0.05, 0.6))
        g["r_ref"] = float(rng.uniform(0.0, 0.08)); g["sigma_q"] = float(rng.uniform(0.3, 1.5))
        s = stats(g, 3000, 100 + i); L = loss(s)
        if best is None or L < best[0]:
            best = (L, g, s)
    # refine around the best point
    L0, g0, _ = best
    for i in range(200):
        g = copy.deepcopy(g0)
        for k, sc in (("lam0", 0.08), ("p_pre", 0.03), ("p_seed", 0.04), ("p_A", 0.04), ("r_ref", 0.006), ("sigma_q", 0.08)):
            g[k] = float(max(0.01, g0[k] + rng.normal(0, sc)))
        s = stats(g, 4000, 1000 + i); L = loss(s)
        if L < best[0]:
            best = (L, g, s)
    L, g, s = best
    check = stats(g, 20000, 99)   # out-of-sample check with a fresh seed and a larger sample
    out = {k: g[k] for k in ("lam0", "p_pre", "p_seed", "p_A", "r_ref", "sigma_q")}
    json.dump({"constants": out, "fit": s, "check_n20000": check, "targets": TARGETS, "loss": L},
              open("calibration.json", "w"), indent=2)
    print(json.dumps({"constants": out, "check": check, "targets": TARGETS}, indent=1))
    print(f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
