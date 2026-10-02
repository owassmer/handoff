"""Run the Handoff outcome-path simulation.

1. Base run: every path at its mode parameters, n=30,000, under three founder scenarios.
2. Uncertainty run: 300 draws; each draw samples every path parameter inside its range and the
   judgment globals inside theirs; n=2,000 per path per draw. Reports the median and 10-90% band of
   each metric and how often each path ranks first.
3. Drivers: for the paths that trade first place, which sampled parameters decide the order.
"""
import copy, json, sys, time
import numpy as np
from model import GLOBAL, PATHS, metrics, simulate

cal = json.load(open("calibration.json"))
G = copy.deepcopy(GLOBAL); G.update(cal["constants"])

SCEN = {"FT": dict(fulltime=True), "PT": dict(fulltime=False), "FT_CAP": dict(fulltime=True, rollup_capital=True)}
KEYS = ["first_rev_6m", "first_rev_12m", "arr1m_36m", "arr3m_60m", "raise_pre", "raise_seed", "raise_A",
        "exit_72m", "exit_ge_25m", "exit_ge_100m", "median_exit_value", "dead", "alive_small", "alive_72m",
        "founder_realized_mean", "founder_ge_5m", "founder_paper_mean"]
RANK_KEYS = ["first_rev_12m", "arr1m_36m", "raise_seed", "exit_72m", "exit_ge_25m", "founder_realized_mean",
             "founder_ge_5m"]
GLOBAL_J = {"seed_bar": (250_000, 400_000, 750_000), "a_bar": (2_000_000, 2_500_000, 5_000_000),
            "burn_scale": (0.8, 1.0, 1.25), "exit_scale": (0.6, 1.0, 1.6)}


def base():
    out = {}
    for sname, kw in SCEN.items():
        out[sname] = {}
        for j, (k, p) in enumerate(PATHS.items()):
            ms = [metrics(simulate(p, 10_000, np.random.default_rng(1000 * i + 17 * j), g=G, **kw)) for i in range(3)]
            out[sname][k] = {m: float(np.mean([x[m] for x in ms])) for m in KEYS}
    return out


def uncertainty(D=300, n=2_000):
    rng = np.random.default_rng(20260928)
    rows = []
    for d in range(D):
        g = copy.deepcopy(G)
        gj = {k: float(rng.triangular(*v)) for k, v in GLOBAL_J.items()}
        g["seed_bar"] = gj["seed_bar"]; g["a_bar"] = gj["a_bar"]
        g["burn"] = [b * gj["burn_scale"] for b in G["burn"]]
        g["exit_h"] = [h * gj["exit_scale"] for h in G["exit_h"]]
        row = {"globals": gj, "paths": {}}
        for k, p in PATHS.items():
            prng = np.random.default_rng(rng.integers(1 << 31))
            drawn = {kk: (float(prng.triangular(*v)) if isinstance(v, tuple) and v[0] != v[2] else
                          (v[1] if isinstance(v, tuple) else v)) for kk, v in p.items()}
            fixed = {kk: ((vv, vv, vv) if isinstance(vv, float) and isinstance(p[kk], tuple) else vv)
                     for kk, vv in drawn.items()}
            r = simulate(fixed, n, np.random.default_rng(rng.integers(1 << 31)), g=g, fulltime=True)
            row["paths"][k] = {"params": {kk: vv for kk, vv in drawn.items() if isinstance(p[kk], tuple)},
                               "m": metrics(r)}
        rows.append(row)
        if d % 50 == 0:
            print(f"draw {d}", file=sys.stderr, flush=True)
    return rows


def summarize(rows):
    ks = list(PATHS)
    summ = {k: {} for k in ks}
    for m in KEYS:
        for k in ks:
            v = np.array([r["paths"][k]["m"][m] for r in rows])
            summ[k][m] = {"p10": float(np.percentile(v, 10)), "p50": float(np.median(v)), "p90": float(np.percentile(v, 90))}
    wins = {m: {} for m in RANK_KEYS}
    for m in RANK_KEYS:
        best = [max(ks, key=lambda k: r["paths"][k]["m"][m]) for r in rows]
        wins[m] = {k: best.count(k) / len(rows) for k in ks}
    return summ, wins


def drivers(rows, a, b, metric="founder_realized_mean"):
    """Which sampled parameters decide whether path a beats path b (Spearman-style rank correlation)."""
    y = np.array([r["paths"][a]["m"][metric] > r["paths"][b]["m"][metric] for r in rows], float)
    res = []
    for side, k in (("a", a), ("b", b)):
        for pk in rows[0]["paths"][k]["params"]:
            x = np.array([r["paths"][k]["params"][pk] for r in rows])
            if np.std(x) == 0:
                continue
            rx = np.argsort(np.argsort(x)); c = np.corrcoef(rx, y)[0, 1]
            res.append((f"{k}.{pk}", float(c)))
    for gk in GLOBAL_J:
        x = np.array([r["globals"][gk] for r in rows]); rx = np.argsort(np.argsort(x))
        res.append((f"global.{gk}", float(np.corrcoef(rx, y)[0, 1])))
    res.sort(key=lambda t: -abs(t[1]))
    return {"share_a_wins": float(y.mean()), "top": res[:8]}


if __name__ == "__main__":
    t0 = time.time()
    b = base(); print(f"base {time.time() - t0:.0f}s", file=sys.stderr)
    rows = uncertainty(); print(f"uncertainty {time.time() - t0:.0f}s", file=sys.stderr)
    summ, wins = summarize(rows)
    # the pairs that decide the recommendation
    pairs = {f"{a}_vs_{c}": drivers(rows, a, c) for a, c in (("P9", "P1"), ("P4", "P1"), ("P9", "P4"), ("P6", "P1"), ("P1", "P2"))}
    json.dump({"globals": {k: G[k] for k in ("lam0", "p_pre", "p_seed", "p_A", "r_ref", "sigma_q")},
               "base": b, "uncertainty": summ, "wins": wins, "drivers": pairs,
               "names": {k: p["name"] for k, p in PATHS.items()}}, open("results.json", "w"), indent=1)
    print(f"done {time.time() - t0:.0f}s", file=sys.stderr)
