"""Handoff 0-to-1 outcome-path simulation.

Monthly Monte Carlo from October 2026 (month 0) to month 72 (October 2032).
Each path is a company shape plus an expansion direction. Every parameter carries a
provenance tag in PARAM_SOURCES (report.md renders it):
  [S n]   SIM.ledger.json source n (verbatim quote attached)
  [Lx §]  lane report section (research/expansion/lanes/), which cites its own sources
  [J]     Ferro judgment, stated with its reason; these are the ranges the
          sensitivity analysis varies.

Global constants that no source pins are calibrated so that a GENERIC B2B software
company reproduces the sourced base rates (calibrate.py). Path parameters then move
Handoff's paths relative to that calibrated generic company.
"""
from __future__ import annotations

import numpy as np

MONTHS = 72

# ---------------------------------------------------------------- global constants
GLOBAL = {
    # personal runway before any raise: 12 months at founder-only burn [J, founder facts unknown]
    "cash0": 180_000.0,
    "burn": [15_000.0, 60_000.0, 180_000.0, 450_000.0],  # by funding level 0..3 [J; seed median ~6 people, A ~16 (S9)]
    "round": [900_000.0, 3_300_000.0, 12_000_000.0],      # pre-seed [J], seed ~$3.5M (S2), A [J]
    "dil": [0.12, 0.19, 0.19],                            # [J; seed/A dilution ~19-20% per Carta via S5 page]
    "seed_bar": 400_000.0,                                # ARR needed for a priced seed [J]
    "a_bar": 2_500_000.0,                                 # Series A ARR bar, 2025 median ~$2.5M (S9)
    "sales_mult": [1.0, 1.6, 3.0, 6.0],                   # new-customer capacity by funding level [J]
    "giveup_month": 18,                                   # no paying customer by then: founders stop or pivot [J]
    # calibrated (calibrate.py writes calibration.json; these are the fallbacks)
    "lam0": 0.55, "p_pre": 0.10, "p_seed": 0.14, "p_A": 0.10,
    "r_ref": 0.03,      # referrals and reinvested revenue: new customers per existing customer per month [calibrated]
    "sigma_q": 0.8,     # spread of product-market fit across companies (lognormal) [calibrated]
    "n_max": 5_000,     # reachable customers per company in six years; ~238,000 residential PM firms (L5 §2.12) [J]
    # gross profit a company needs to keep going when cash runs out, by funding level: the smallest team it can cut to [J]
    "life_floor": [15_000.0, 25_000.0, 60_000.0, 150_000.0],
    # acquisition hazard per month by ARR band <0.5M, <1M, <3M, <10M, >=10M [J; tuned to PitchBook third/third/third, S5]
    "exit_h": [0.0015, 0.004, 0.007, 0.010, 0.012],
}

# ---------------------------------------------------------------- paths
# tri = (low, mode, high) triangular range; the sensitivity pass samples inside it.
DOORS, TURNOVER = 400, 0.28   # median client 100-2,000 doors (L3 C1); SFR turnover 22.8% (L2 §2.9) to 46.8% apts (L5 §2.12)
TURNS = DOORS * TURNOVER       # ~112 turns per client per year

PATHS = {
    "P1": dict(name="Software, tenancy depth (settlement-led)", shape="software",
               h1=(0.06, 0.10, 0.15), arpa=(TURNS*100, TURNS*175, TURNS*250), lam=(0.8, 1.0, 1.2),
               churn=(0.020, 0.030, 0.045), gm=(0.65, 0.75, 0.82),
               g=(0.25, 0.45, 0.70), pg=(0.50, 0.65, 0.80), comm=(0.15, 0.25, 0.35),
               fund=(1.0, 1.1, 1.3), exitm=(1.2, 1.5, 2.0), val=(1.0, 1.0, 1.0), ai=0.30),
    "P2": dict(name="Software, occupied maintenance", shape="software",
               h1=(0.06, 0.10, 0.15), arpa=(TURNS*100, TURNS*175, TURNS*250), lam=(0.8, 1.0, 1.2),
               churn=(0.020, 0.030, 0.045), gm=(0.65, 0.75, 0.82),
               g=(0.40, 0.80, 1.20), pg=(0.20, 0.30, 0.45), comm=(0.25, 0.35, 0.45),
               fund=(0.8, 0.9, 1.0), exitm=(1.0, 1.3, 1.6), val=(1.0, 1.0, 1.0), ai=0.25),
    "P3": dict(name="Software, owner-funded projects", shape="software",
               h1=(0.06, 0.10, 0.15), arpa=(TURNS*100, TURNS*175, TURNS*250), lam=(0.8, 1.0, 1.2),
               churn=(0.020, 0.030, 0.045), gm=(0.65, 0.75, 0.82),
               g=(0.10, 0.20, 0.35), pg=(0.40, 0.55, 0.70), comm=(0.15, 0.20, 0.30),
               fund=(0.9, 1.0, 1.1), exitm=(1.0, 1.2, 1.5), val=(1.0, 1.0, 1.0), ai=0.25),
    "P4": dict(name="Accountable service, tenancy close-out (outcome-priced)", shape="service",
               h1=(0.10, 0.15, 0.22), arpa=(TURNS*250, TURNS*350, TURNS*450), lam=(0.6, 0.8, 1.0),
               churn=(0.012, 0.020, 0.030), gm=(0.35, 0.50, 0.65),
               g=(0.20, 0.35, 0.55), pg=(0.55, 0.70, 0.85), comm=(0.08, 0.15, 0.22),
               fund=(0.7, 0.85, 1.0), exitm=(0.6, 0.8, 1.0), val=(0.50, 0.65, 0.80), ai=0.15,
               cap_fte=(6, 10, 15)),
    "P5": dict(name="Accountable service, turns plus owner projects", shape="service",
               h1=(0.10, 0.15, 0.22), arpa=(TURNS*250, TURNS*350, TURNS*450), lam=(0.6, 0.8, 1.0),
               churn=(0.012, 0.020, 0.030), gm=(0.30, 0.42, 0.55),
               g=(0.15, 0.30, 0.50), pg=(0.45, 0.60, 0.75), comm=(0.08, 0.12, 0.18),
               fund=(0.6, 0.75, 0.9), exitm=(0.6, 0.8, 1.0), val=(0.45, 0.55, 0.70), ai=0.10,
               cap_fte=(5, 8, 12)),
    # Service first, then software: P4 until automation is proven, then software economics.
    # Conversion odds: Pilot reached 60% gross margin; Bench and Atrium did not (L5 §2.4).
    "P9": dict(name="Service first, then software (tenancy close-out)", shape="service",
               h1=(0.10, 0.15, 0.22), arpa=(TURNS*250, TURNS*350, TURNS*450), lam=(0.6, 0.8, 1.0),
               churn=(0.012, 0.020, 0.030), gm=(0.35, 0.50, 0.65),
               g=(0.20, 0.35, 0.55), pg=(0.55, 0.70, 0.85), comm=(0.08, 0.15, 0.22),
               fund=(0.7, 0.85, 1.0), exitm=(0.6, 0.8, 1.0), val=(0.50, 0.65, 0.80), ai=0.15,
               cap_fte=(6, 10, 15),
               p_conv=(0.35, 0.50, 0.65), gm2=(0.60, 0.68, 0.75), val2=(0.8, 0.9, 1.0), fund2=(0.9, 1.0, 1.2),
               exitm2=(1.0, 1.3, 1.6)),
    "P6": dict(name="Engine for platforms and deposit insurers", shape="engine",
               h1=(0.025, 0.045, 0.07), arpa=(60_000, 150_000, 350_000), lam_abs=(0.05, 0.10, 0.18),
               churn=(0.005, 0.010, 0.020), gm=(0.75, 0.82, 0.88),
               g=(0.30, 0.60, 1.00), pg=(0.40, 0.55, 0.70), comm=(0.20, 0.30, 0.40),
               fund=(0.7, 0.85, 1.0), exitm=(1.5, 2.2, 3.0), val=(1.0, 1.0, 1.0), ai=0.30),
    "P7": dict(name="Engine for consolidators' portfolio transitions", shape="engine",
               h1=(0.03, 0.05, 0.08), arpa=(50_000, 120_000, 250_000), lam_abs=(0.06, 0.12, 0.20),
               churn=(0.015, 0.025, 0.040), gm=(0.60, 0.70, 0.80),
               g=(0.10, 0.20, 0.35), pg=(0.40, 0.55, 0.70), comm=(0.10, 0.15, 0.25),
               fund=(0.6, 0.75, 0.9), exitm=(1.0, 1.4, 2.0), val=(0.9, 1.0, 1.0), ai=0.20),
    "P8": dict(name="Own the operator (AI-native management roll-up)", shape="rollup",
               h1=(0.03, 0.05, 0.08),            # monthly hazard of closing the first acquisition once licensed/financed
               license=(3, 5, 9),                # months to a broker of record [J; VA/NY licensing unverified, L5 O6]
               doors_acq=(200, 350, 600),        # first firm size [J]
               fee=(1_500, 1_809, 2_100),        # revenue per door per year, NARPM 2017 (L1 §economics)
               m0=(0.04, 0.06, 0.08),            # starting margin 6% (L1, NARPM)
               m1=(0.12, 0.20, 0.28), pm1=(0.35, 0.50, 0.65),  # AI margin uplift: GC 'doubled EBITDA' claim (L5 §2.6) unproven
               owner_churn=(0.18, 0.25, 0.30),   # owners leaving per year, 25% (L1, NARPM)
               organic=(3, 6, 10),               # doors won per month organically [J]
               acq_h=(0.03, 0.05, 0.08),         # follow-on acquisition hazard when financed [J]
               per_door=(1_000, 1_500, 2_000),   # price per door (S7)
               hq=(8_000, 12_000, 20_000),     # founders take the seller's salary line; this is the extra overhead [J]
               fund=(0.6, 0.8, 1.0), exitm=(0.8, 1.0, 1.3), ai=0.0),
}

GENERIC = dict(name="Generic B2B software (calibration)", shape="software", h1=(1.0, 1.0, 1.0),
               arpa=(12_000, 12_000, 12_000), lam=(1.0, 1.0, 1.0), churn=(0.03, 0.03, 0.03),
               gm=(0.78, 0.78, 0.78), g=(0.0, 0.0, 0.0), pg=(0.0, 0.0, 0.0), comm=(0.0, 0.0, 0.0),
               fund=(1.0, 1.0, 1.0), exitm=(1.0, 1.0, 1.0), val=(1.0, 1.0, 1.0), ai=0.0)


def draw(tri, mode="mode", rng=None):
    lo, md, hi = tri
    if mode == "mode" or lo == hi:
        return md
    return float(rng.triangular(lo, md, hi))


def params_for(path, mode, rng):
    return {k: (draw(v, mode, rng) if isinstance(v, tuple) else v) for k, v in path.items()}


def multiple(arr, shape, val, ai_hit, rng):
    """Private sale multiple of ARR by band (S4); services discounted by val; AI premium 40-80% (S4)."""
    n = arr.shape[0]
    lo = np.where(arr < 2e6, 2.0, np.where(arr < 10e6, 3.0, 3.5))
    hi = np.where(arr < 2e6, 3.5, np.where(arr < 10e6, 5.0, 6.0))
    m = lo + (hi - lo) * rng.random(n)
    m = m * val * np.where(ai_hit, 1.4 + 0.4 * rng.random(n), 1.0)
    return m


def simulate(path, n, rng, g=GLOBAL, mode="mode", fulltime=True, rollup_capital=False, start_with_revenue=False):
    p = params_for(path, mode, rng)
    if p["shape"] == "rollup":
        return simulate_rollup(p, n, rng, g, fulltime, rollup_capital)
    T = MONTHS
    tm = 1.0 if fulltime else 0.5
    alive = np.ones(n, bool); dead = np.zeros(n, bool); life = np.zeros(n, bool)
    has_rev = np.full(n, start_with_revenue); t_first = np.where(has_rev, 0, -1)
    cust = np.where(has_rev, 1.0, 0.0); arr = np.where(has_rev, p["arpa"], 0.0)
    arpa_new = np.full(n, p["arpa"]); cash = np.full(n, g["cash0"]); f = np.zeros(n, int)
    ft = np.full(n, fulltime); own = np.ones(n); raised = np.zeros(n)
    last_try = np.full(n, -99); comm = np.zeros(n, bool); exited = np.zeros(n, bool)
    exit_val = np.zeros(n); exit_m = np.full(n, -1); fprocs = np.zeros(n)
    exp_ok = rng.random(n) < p["pg"]
    q = np.exp(rng.normal(-g["sigma_q"] ** 2 / 2, g["sigma_q"], n))   # per-company fit, mean 1
    gm = np.full(n, p["gm"]); val = np.full(n, p["val"]); fund = np.full(n, p["fund"]); exm = np.full(n, p["exitm"])
    capx = np.ones(n); converted = np.zeros(n, bool)
    conv_ok = rng.random(n) < p.get("p_conv", 0.0)
    ever = {"pre": np.zeros(n, bool), "seed": np.zeros(n, bool), "A": np.zeros(n, bool)}
    t_seed = np.full(n, -1)
    hit1m = np.full(n, -1); hit3m = np.full(n, -1)
    comm_h = 1 - (1 - p["comm"]) ** (1 / 12)
    for t in range(T):
        live = alive & ~exited
        tmv = np.where(ft, 1.0, tm)
        # first paying customer
        new_first = live & ~has_rev & (rng.random(n) < p["h1"] * tmv * np.where(f > 0, 1.3, 1.0))
        has_rev |= new_first; t_first = np.where(new_first, t, t_first)
        cust = np.where(new_first, 1.0, cust); arr = np.where(new_first, arpa_new, arr)
        act = live & has_rev & ~new_first
        # commoditization of the wedge (incumbent bundles, point tools, partner builds in-house)
        comm_ev = act & ~comm & (rng.random(n) < comm_h)
        comm |= comm_ev; arpa_new = np.where(comm_ev, arpa_new * 0.75, arpa_new)
        cm = np.where(comm, 0.6, 1.0)
        # new customers
        sm = np.array(g["sales_mult"])[f]
        if "lam_abs" in p:   # few large buyers: no referral compounding
            lam = p["lam_abs"] * sm * tmv * cm * q
        else:
            lam = (g["lam0"] * sm + g["r_ref"] * cust) * p["lam"] * tmv * cm * q
            lam = lam * np.clip(1 - cust / g["n_max"], 0, 1)   # market saturation
        if "cap_fte" in p:  # accountable service: delivery capacity by funding level
            cap = p["cap_fte"] * np.array([0.6, 1.5, 4.0, 12.0])[f] * capx
            lam = np.where(cust >= cap, 0.0, lam)
        arrivals = np.where(act, rng.poisson(np.minimum(lam, 300.0)), 0)
        cust = cust + arrivals; arr = arr + arrivals * arpa_new
        # churn (commoditization raises it 30%)
        ch = np.minimum(p["churn"] * np.where(comm, 1.3, 1.0), 0.5)
        lost = np.where(act & (cust > 0), rng.binomial(cust.astype(int), ch), 0)
        avg = np.where(cust > 0, arr / np.maximum(cust, 1), 0)
        cust = cust - lost; arr = np.maximum(arr - lost * avg, 0)
        # expansion direction: unlocked 12 months after first revenue with 3+ customers, runs 36 months
        since = t - t_first
        grow = act & exp_ok & (since >= 12) & (since < 48) & (cust >= 3)
        arr = np.where(grow, arr * (1 + p["g"] / 12), arr)
        if "p_conv" in p:   # automation proven: software margins, valuation and capacity
            conv = act & conv_ok & ~converted & (since >= 24) & (cust >= 6)
            converted |= conv
            gm = np.where(conv, p["gm2"], gm); val = np.where(conv, p["val2"], val)
            fund = np.where(conv, p["fund2"], fund); exm = np.where(conv, p["exitm2"], exm); capx = np.where(conv, 3.0, capx)
        arpa_new = np.where(grow, arpa_new * (1 + p["g"] / 12), arpa_new)
        # cash
        burn = np.array(g["burn"])[f]
        burn = np.where(life, g["burn"][0], burn)
        cash = np.where(live, cash + arr / 12 * gm - burn, cash)
        # fundraising (attempt every 6 months, or when runway < 6 months)
        runway_low = cash < 6 * burn
        can_try = live & (f < 3) & ((t - last_try >= 6) | (runway_low & (t - last_try >= 3)))
        # pre-seed
        tryp = can_try & (f == 0) & (t >= 2)
        pp = g["p_pre"] * fund * np.where(has_rev, 1.6, 0.6) * np.where(ft, 1.0, 0.5)
        okp = tryp & (rng.random(n) < pp)
        # seed (from 0 or 1)
        trys = can_try & (f <= 1) & (arr >= g["seed_bar"])
        oks = trys & (rng.random(n) < g["p_seed"] * fund) & ~okp
        # Series A
        trya = can_try & (f == 2) & (arr >= g["a_bar"])
        oka = trya & (rng.random(n) < g["p_A"] * fund)
        last_try = np.where(tryp | trys | trya, t, last_try)
        for ok, lvl, key in ((okp, 1, "pre"), (oks, 2, "seed"), (oka, 3, "A")):
            cash = np.where(ok, cash + g["round"][lvl - 1], cash)
            raised = np.where(ok, raised + g["round"][lvl - 1], raised)
            own = np.where(ok, own * (1 - g["dil"][lvl - 1]), own)
            f = np.where(ok, np.maximum(f, lvl), f); ft |= ok; life &= ~ok
            ever[key] |= ok
        t_seed = np.where(oks & (t_seed < 0), t, t_seed)
        # survival: out of cash -> lifestyle if gross profit covers founders, else dead
        broke = live & (cash < 0)
        gp = arr / 12 * gm
        to_life = broke & (gp >= np.array(g["life_floor"])[f])
        life |= to_life; cash = np.where(to_life, 0.0, cash)
        die = broke & ~to_life
        die |= live & ~has_rev & (t >= g["giveup_month"])
        alive &= ~die; dead |= die
        # milestones
        hit1m = np.where((hit1m < 0) & (arr >= 1e6), t, hit1m)
        hit3m = np.where((hit3m < 0) & (arr >= 3e6), t, hit3m)
        # exit
        band = np.digitize(arr, [5e5, 1e6, 3e6, 10e6])
        eh = np.array(g["exit_h"])[band] * exm
        ex = alive & ~exited & has_rev & (rng.random(n) < eh)
        if ex.any():
            ai_hit = rng.random(n) < p["ai"]
            v = arr * multiple(arr, p["shape"], val, ai_hit, rng)
            v = np.where(arr < 5e5, np.maximum(v, 1e6 + 3e6 * rng.random(n)), v)  # acqui-hire floor $1-4M [J]
            inv = np.minimum(v, np.maximum(raised, (1 - own) * v))                  # 1x non-participating preference
            exit_val = np.where(ex, v, exit_val); fprocs = np.where(ex, v - inv, fprocs)
            exit_m = np.where(ex, t, exit_m); exited |= ex
    band = np.digitize(arr, [5e5, 1e6, 3e6, 10e6])
    paper = np.where(alive & ~exited, arr * np.array([2.0, 2.0, 2.75, 4.0, 4.75])[band] * val, 0.0)
    paper_f = np.where(alive & ~exited, paper - np.minimum(paper, np.maximum(raised, (1 - own) * paper)), 0.0)
    return dict(t_first=t_first, hit1m=hit1m, hit3m=hit3m, pre=ever["pre"], seed=ever["seed"], A=ever["A"],
                t_seed=t_seed, dead=dead, life=life & alive & ~exited, exited=exited, exit_val=exit_val,
                exit_m=exit_m, fprocs=fprocs, paper_f=paper_f, arr=arr, alive=alive)


def simulate_rollup(p, n, rng, g, fulltime, capital):
    """Own the operator: buy a small management firm, run it on Handoff, add doors and firms."""
    T = MONTHS
    tm = 1.0 if fulltime else 0.5
    cap_m = 2.0 if capital else 1.0
    alive = np.ones(n, bool); dead = np.zeros(n, bool); exited = np.zeros(n, bool)
    doors = np.zeros(n); t_first = np.full(n, -1); has = np.zeros(n, bool)
    cash = np.full(n, g["cash0"]); own = np.ones(n); raised = np.zeros(n); pre = np.zeros(n, bool)
    seed = np.zeros(n, bool); A = np.zeros(n, bool)
    ai_ok = rng.random(n) < p["pm1"]
    hit1m = np.full(n, -1); hit3m = np.full(n, -1); exit_val = np.zeros(n); fprocs = np.zeros(n)
    exit_m = np.full(n, -1); last_try = np.full(n, -99); life = np.zeros(n, bool)
    oc = 1 - (1 - p["owner_churn"]) ** (1 / 12)
    for t in range(T):
        live = alive & ~exited
        licensed = t >= p["license"]
        # equity for acquisitions: roll-up investors exist (Dwelly, Rising Tide, Oakline, L2 §2.6)
        tryp = live & ~pre & (t - last_try >= 6) & (t >= 2)
        okp = tryp & (rng.random(n) < g["p_pre"] * 1.6 * p["fund"] * cap_m * tm)
        last_try = np.where(tryp, t, last_try)
        cash = np.where(okp, cash + 1_500_000, cash); raised = np.where(okp, raised + 1_500_000, raised)
        own = np.where(okp, own * 0.80, own); pre |= okp
        financed = pre | capital
        first = live & ~has & licensed & financed & (rng.random(n) < p["h1"] * tm)
        size = p["doors_acq"] * (0.7 + 0.6 * rng.random(n))
        price = size * p["per_door"]
        doors = np.where(first, size, doors); cash = np.where(first, cash - 0.4 * price, cash)  # 60% seller note/SBA [J]
        has |= first; t_first = np.where(first, t, t_first)
        act = live & has & ~first
        # follow-on acquisitions once the first firm runs on Handoff (12+ months) and a platform round is raised
        tryseed = act & ~seed & (doors >= 800) & (t - last_try >= 6)
        oks = tryseed & (rng.random(n) < g["p_seed"] * 1.5 * p["fund"])
        cash = np.where(oks, cash + 8_000_000, cash); raised = np.where(oks, raised + 8_000_000, raised)
        own = np.where(oks, own * 0.75, own); seed |= oks; last_try = np.where(tryseed, t, last_try)
        more = act & (seed | capital) & (t - t_first >= 12) & (rng.random(n) < p["acq_h"])
        add = p["doors_acq"] * (0.7 + 0.8 * rng.random(n))
        doors = np.where(more, doors + add, doors); cash = np.where(more, cash - 0.4 * add * p["per_door"], cash)
        doors = np.where(act, doors + rng.poisson(p["organic"] * tm, n) - rng.binomial(doors.astype(int), oc), doors)
        doors = np.maximum(doors, 0)
        since = t - t_first
        margin = np.where(ai_ok & (since >= 18), p["m1"], np.where(ai_ok & (since >= 6), (p["m0"] + p["m1"]) / 2, p["m0"]))
        rev = doors * p["fee"]
        founder_pay = np.where(has, 0.0, g["burn"][0])   # founders are paid inside the operating costs once operating
        cash = np.where(live, cash + rev / 12 * margin - founder_pay - np.where(has, p["hq"], 0), cash)  # HQ/software beyond the firm's own costs [J]
        broke = live & (cash < 0)
        die = broke | (live & ~has & (t >= 24))
        alive &= ~die; dead |= die
        hit1m = np.where((hit1m < 0) & (rev >= 1e6), t, hit1m)
        hit3m = np.where((hit3m < 0) & (rev >= 3e6), t, hit3m)
        # exit: sell to a consolidator (Oakline, Evernest, PURE: L2 §2.6, L3) at 1-2.5x revenue (S7);
        # platforms with 20%+ margins priced on EBITDA 4-8x (S7)
        eh = np.where(doors >= 1500, 0.010, np.where(doors >= 500, 0.005, 0.002)) * p["exitm"]
        ex = alive & ~exited & has & (rng.random(n) < eh)
        if ex.any():
            v_rev = rev * (1.0 + 1.5 * rng.random(n))
            v_ebitda = rev * margin * (4 + 4 * rng.random(n))
            v = np.where((margin >= 0.15) & (doors >= 1000), np.maximum(v_rev, v_ebitda), v_rev)
            inv = np.minimum(v, np.maximum(raised, (1 - own) * v))
            debt = 0.6 * doors * p["per_door"] * 0.5   # half the seller notes still outstanding [J]
            exit_val = np.where(ex, v, exit_val); fprocs = np.where(ex, np.maximum(v - inv - debt, 0), fprocs)
            exit_m = np.where(ex, t, exit_m); exited |= ex
    rev = doors * p["fee"]
    paper = np.where(alive & ~exited, rev * 1.5, 0.0)
    paper_f = np.where(alive & ~exited, np.maximum(paper - np.minimum(paper, np.maximum(raised, (1 - own) * paper)), 0), 0.0)
    return dict(t_first=t_first, hit1m=hit1m, hit3m=hit3m, pre=pre, seed=seed, A=A, t_seed=np.full(n, -1),
                dead=dead, life=life, exited=exited, exit_val=exit_val, exit_m=exit_m, fprocs=fprocs,
                paper_f=paper_f, arr=rev, alive=alive)


def metrics(r):
    tf = r["t_first"]; ex = r["exited"]; ev = r["exit_val"]
    return {
        "first_rev_6m": float(np.mean((tf >= 0) & (tf <= 6))),
        "first_rev_12m": float(np.mean((tf >= 0) & (tf <= 12))),
        "arr1m_36m": float(np.mean((r["hit1m"] >= 0) & (r["hit1m"] <= 36))),
        "arr3m_60m": float(np.mean((r["hit3m"] >= 0) & (r["hit3m"] <= 60))),
        "raise_pre": float(np.mean(r["pre"])), "raise_seed": float(np.mean(r["seed"])), "raise_A": float(np.mean(r["A"])),
        "exit_72m": float(np.mean(ex)),
        "exit_ge_25m": float(np.mean(ex & (ev >= 25e6))), "exit_ge_100m": float(np.mean(ex & (ev >= 100e6))),
        "median_exit_value": float(np.median(ev[ex])) if ex.any() else 0.0,
        "dead": float(np.mean(r["dead"])), "alive_small": float(np.mean(r["life"])),
        "alive_72m": float(np.mean(r["alive"] & ~ex)),
        "founder_realized_mean": float(np.mean(r["fprocs"])),
        "founder_ge_5m": float(np.mean(r["fprocs"] >= 5e6)),
        "founder_paper_mean": float(np.mean(r["paper_f"])),
    }
