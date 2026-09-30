"""Critic: defined-risk (debit-only, no margin) option structures for MU day 1 (Thu Oct 1 2026), $400-650 max risk.
Prices every structure on the 98 historical after-close prints (2001-12 .. 2026-06) with Black-Scholes, flat vol, r=4%,
historical % moves applied to today's price level (S_ref = 1065, the 9/29 close), $5 strike grid, 1 contract.
Fills: pay the full half-spread on EVERY leg on EVERY side ("natural"); base per-leg quoted width $1.00 (CBOE Oct-2 chain
on 9/29 shows $0.35-1.10 near ATM with heavy volume; day-1 opening quotes are wider), stress $2.00. Expiry = intrinsic, no cost.
Families:
  A. Open entry (09:30-09:35 Thu): Oct 2 (T=2/252) or Oct 9 (T=7/252) debit verticals; direction put / call / with-gap /
     against-gap; long strike ATM or 2% OTM; width 10/20/30/50; exit Thu close or Fri close; 10 gap conditions.
     Plus a single long Oct 2 put capped at a $6.50 debit ("lottery").
  B. Fallback (RA plan): 15:40 Thu entry, Oct 9 $10/15/20-wide debit vertical WITH the gap, |gap| >= thr, gap >= 50% intact
     at the close (proxy for 15:40), long = first strike beyond spot, hold to Fri / Mon close / Oct 9 expiry. Variants incl. against-gap.
Multiple testing: Bonferroni on the best t; White (2000) reality-check bootstrap over the whole family ($ P&L per print).
Outputs: critic_options_grid.csv, critic_options_out.txt (stdout).
"""
import pandas as pd, numpy as np, itertools, sys
from math import log, sqrt, exp, erf
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 400)
N = lambda x: 0.5 * (1 + erf(x / sqrt(2)))
def bs(S, K, T, v, cp, r=0.04):
    if T <= 0: return max(S - K, 0.0) if cp == "C" else max(K - S, 0.0)
    d1 = (log(S / K) + (r + v * v / 2) * T) / (v * sqrt(T)); d2 = d1 - v * sqrt(T)
    return S * N(d1) - K * exp(-r * T) * N(d2) if cp == "C" else K * exp(-r * T) * N(-d2) - S * N(-d1)

S_REF = 1065.0; FEE = 0.05          # $/contract/leg (regulatory+exchange; RH commission 0)
IV2, IV9 = 0.65, 0.55               # post-crush IV assumptions at Thu open: Oct-2 (1-2 DTE) and Oct-9 (7 DTE). Sensitivity below.
DIV2, DIV9 = 0.05, 0.03             # IV decay by Thu close
HALF = float(sys.argv[1]) if len(sys.argv) > 1 else 0.50   # half-spread paid per leg per side ($); $0.50 => $1.00 quoted width

# ---------- data: 98 prints + forward closes from the raw bars ----------
d = pd.read_csv("raw_daily_unadj.csv", index_col=0, parse_dates=True); idx = d.index
pl = pd.read_csv("day1_planner.csv", parse_dates=["report_date", "day1"])
rows = []
for _, r in pl.iterrows():
    i = idx.get_loc(r.day1)
    rows.append(dict(report=r.report_date.date(), year=r.year, gap=r.gap_pct, C0=r.prev_close, O=r.open, H=r.high, L=r.low, C=r.close,
                     C2=d.Close.iloc[i + 1], C3=d.Close.iloc[i + 2], C6=d.Close.iloc[i + 6] if i + 6 < len(d) else np.nan,
                     h1c=r.h1_close if "h1_close" in r and pd.notna(r.get("h1_close", np.nan)) else np.nan))
D = pd.DataFrame(rows)
for c in ["O", "H", "L", "C", "C2", "C3", "C6", "h1c"]: D[c + "r"] = D[c] / D["C0"]          # relative to report-day close
D["era"] = np.where(D.year <= 2015, "2001-15", "2016-26")
print("prints:", len(D), "| realized vol (annualized) of the horizons the structures bet on:")
for nm, x in [("day-1 open->close", np.log(D.C / D.O)), ("day-1 open->Fri close", np.log(D.C2 / D.O)), ("Thu close->Mon close", np.log(D.C3 / D.C)), ("Thu close->Fri close", np.log(D.C2 / D.C))]:
    days = {"day-1 open->close": 1, "day-1 open->Fri close": 2, "Thu close->Mon close": 2, "Thu close->Fri close": 1}[nm]
    print("  %-24s std %.2f%% -> %.0f%% annualized (n=%d)" % (nm, x.std() * 100, x.std() * sqrt(252 / days) * 100, len(x)))

# ---------- pricing helpers ----------
def vertical(cp, K1, K2, Se, Te, ive, Sx, Tx, ivx, half=HALF):
    """1-lot debit vertical: long K1, short K2. returns (pnl$, maxloss$, debit$/sh). Natural fills both ways; expiry = intrinsic."""
    deb = bs(Se, K1, Te, ive, cp) - bs(Se, K2, Te, ive, cp) + 2 * half + 2 * FEE / 100
    val = bs(Sx, K1, Tx, ivx, cp) - bs(Sx, K2, Tx, ivx, cp) - ((2 * half + 2 * FEE / 100) if Tx > 0 else 0.0)
    return (val - deb) * 100, deb * 100, deb
def grid5(x, how="round"):
    return {"round": round(x / 5) * 5, "up": np.ceil(x / 5) * 5, "down": np.floor(x / 5) * 5}[how]

# ---------- family A: open entry ----------
COND = {"all": lambda g: True, "|gap|<3": lambda g: abs(g) < 3, "|gap|<7": lambda g: abs(g) < 7, "|gap|>=7": lambda g: abs(g) >= 7,
        "gap>=3": lambda g: g >= 3, "gap<=-3": lambda g: g <= -3, "gap>=7": lambda g: g >= 7, "gap<=-7": lambda g: g <= -7,
        "gap>0": lambda g: g > 0, "gap<=0": lambda g: g <= 0}
def side_for(direction, g):
    if direction == "put": return -1
    if direction == "call": return 1
    s = 1 if g > 0 else -1
    return s if direction == "with_gap" else -s
recs = []; PNL = {}   # PNL[name] = per-print $ P&L (0 when flat) for the reality check
def add(name, fam, pnl_by_print, ml_by_print, cond_mask):
    p = np.array(pnl_by_print, float); ml = np.array(ml_by_print, float); m = np.array(cond_mask, bool)
    if m.sum() == 0: return
    pp, mm = p[m], ml[m]
    with np.errstate(invalid="ignore"): R = pp / mm
    t = pp.mean() / (pp.std(ddof=1) / sqrt(len(pp))) if len(pp) > 2 and pp.std() > 0 else np.nan
    e1, e2 = (D.era.values[m] == "2001-15"), (D.era.values[m] == "2016-26")
    recs.append(dict(name=name, family=fam, n=int(m.sum()), maxloss=mm.mean(), maxloss_max=mm.max(), in_budget=(mm <= 650).mean(),
                     EV_usd=pp.mean(), EV_R=R.mean(), t=t, win=(pp > 0).mean(), EV_R_pre16=R[e1].mean() if e1.any() else np.nan,
                     EV_R_post16=R[e2].mean() if e2.any() else np.nan, n_pre16=int(e1.sum()), n_post16=int(e2.sum()), last12_R=R[-12:].mean()))
    full = np.where(m, p, 0.0); PNL[name] = full

for exp_, Te, Tx_thu, Tx_fri, ive, dive in [("Oct2", 2 / 252, 1 / 252, 0.0, IV2, DIV2), ("Oct9", 7 / 252, 6 / 252, 5 / 252, IV9, DIV9)]:
    for direction in ["put", "call", "with_gap", "against_gap"]:
        for place in ["atm", "otm2"]:
            for W in [10, 20, 30, 50]:
                for exit_ in ["thu_close", "fri_close"]:
                    pn, ml, sides = [], [], []
                    for _, r in D.iterrows():
                        s = side_for(direction, r.gap); cp = "C" if s > 0 else "P"
                        Se = S_REF * r.Or; m = 0.0 if place == "atm" else 0.02
                        K1 = grid5(Se * (1 + s * m)); K2 = K1 + s * W
                        Sx = S_REF * (r.Cr if exit_ == "thu_close" else r.C2r); Tx = Tx_thu if exit_ == "thu_close" else Tx_fri
                        p_, ml_, _ = vertical(cp, K1, K2, Se, Te, ive, Sx, Tx, ive - dive)
                        pn.append(p_); ml.append(ml_)
                    for cn, cf in COND.items():
                        add(f"A|{exp_}|{direction}|{place}|W{W}|{exit_}|{cn}", "A-open", pn, ml, [cf(g) for g in D.gap])
# single long Oct-2 put, debit <= $6.50 (strike solved per print), exit Thu close or expiry
for exit_ in ["thu_close", "fri_close"]:
    pn, ml = [], []
    for _, r in D.iterrows():
        Se = S_REF * r.Or; K = grid5(Se, "down")
        while bs(Se, K, 2 / 252, IV2, "P") + HALF + FEE / 100 > 6.50 and K > 5: K -= 5
        deb = bs(Se, K, 2 / 252, IV2, "P") + HALF + FEE / 100
        Sx = S_REF * (r.Cr if exit_ == "thu_close" else r.C2r); Tx = 1 / 252 if exit_ == "thu_close" else 0.0
        val = bs(Sx, K, Tx, IV2 - DIV2, "P") - ((HALF + FEE / 100) if Tx > 0 else 0.0)
        pn.append((val - deb) * 100); ml.append(deb * 100)
    for cn, cf in COND.items(): add(f"A|Oct2|long_put<=650|{exit_}|{cn}", "A-open", pn, ml, [cf(g) for g in D.gap])

# ---------- family B: 15:40 entry, Oct 9, with (or against) the gap ----------
for thr in [3, 5, 7, 10]:
    for intact in ["any", ">=50%"]:
        for direction in ["with_gap", "against_gap", "put"]:
            for W in [10, 15, 20]:
                for exit_, Tx, col in [("fri_close", 5 / 252, "C2r"), ("mon_close", 4 / 252, "C3r"), ("oct9_expiry", 0.0, "C6r")]:
                    pn, ml, mask = [], [], []
                    for _, r in D.iterrows():
                        g = r.gap; s = side_for(direction, g); cp = "C" if s > 0 else "P"
                        Se = S_REF * r.Cr; mid = (r.Or + 1.0) / 2      # gap midpoint, relative to C0
                        ok = abs(g) >= thr and (intact == "any" or (r.Cr >= mid if g > 0 else r.Cr <= mid))
                        K1 = grid5(Se, "up" if s > 0 else "down"); K1 = K1 + s * 5 if K1 == round(Se, 2) else K1; K2 = K1 + s * W
                        p_, ml_, _ = vertical(cp, K1, K2, Se, 6 / 252, IV9, S_REF * r[col] if pd.notna(r[col]) else Se, Tx, IV9 - 0.03)
                        pn.append(p_); ml.append(ml_); mask.append(bool(ok) and pd.notna(r[col]))
                    add(f"B|thr{thr}|intact{intact}|{direction}|W{W}|{exit_}", "B-close", pn, ml, mask)

G = pd.DataFrame(recs); G.to_csv("critic_options_grid.csv", index=False, float_format="%.4f")
M = len(G); print(f"\nstructures priced: {M} (family A {int((G.family=='A-open').sum())}, family B {int((G.family=='B-close').sum())}) | half-spread/leg ${HALF:.2f} | IV Oct2 {IV2:.0%}, Oct9 {IV9:.0%}")

# ---------- the desk's two headline expressions ----------
print("\n=== Desk headline expressions (natural fills) ===")
for key in ["A|Oct2|put|atm|W10|thu_close|all", "A|Oct2|put|atm|W20|thu_close|all", "A|Oct9|put|atm|W10|thu_close|all", "A|Oct2|put|atm|W10|fri_close|all",
            "A|Oct2|long_put<=650|thu_close|all", "A|Oct2|long_put<=650|fri_close|all",
            "B|thr7|intact>=50%|with_gap|W10|mon_close", "B|thr7|intactany|with_gap|W10|mon_close", "B|thr7|intact>=50%|with_gap|W10|fri_close", "B|thr5|intact>=50%|with_gap|W10|mon_close"]:
    g = G[G.name == key]
    if len(g): print(g[["name", "n", "maxloss", "EV_usd", "EV_R", "t", "win", "EV_R_pre16", "EV_R_post16", "last12_R"]].round(3).to_string(index=False, header=False))

# ---------- leaderboard among tradeable structures (budget: max loss <= $650 on >= 90% of prints, n >= 15) ----------
T = G[(G.in_budget >= 0.9) & (G.n >= 15)].copy()
print(f"\n=== Leaderboard by t-stat among tradeable structures (n>=15, in budget): {len(T)} of {M} ===")
print(T.sort_values("t", ascending=False).head(15)[["name", "n", "maxloss", "EV_usd", "EV_R", "t", "win", "EV_R_pre16", "EV_R_post16", "last12_R"]].round(3).to_string(index=False))
print("\nworst 5:"); print(T.sort_values("t").head(5)[["name", "n", "maxloss", "EV_usd", "EV_R", "t"]].round(3).to_string(index=False))
print("\nfamily B (fallback variants) sorted by t:")
print(T[T.family == "B-close"].sort_values("t", ascending=False).head(12)[["name", "n", "maxloss", "EV_usd", "EV_R", "t", "win", "EV_R_pre16", "EV_R_post16", "last12_R"]].round(3).to_string(index=False))

# ---------- multiple testing ----------
best = T.sort_values("t", ascending=False).iloc[0]
from scipy import stats as st
p_one = 1 - st.t.cdf(best.t, best.n - 1)
print(f"\n=== Multiple-testing haircut ===\nbest tradeable: {best['name']} t={best.t:.2f} n={best.n} one-sided p={p_one:.4f}")
for m_ in [M, M + 1830 + 168]:
    print(f"  Bonferroni with M={m_}: adjusted p = {min(1, p_one * m_):.3f}; t needed for family-wise 5%: {st.norm.ppf(1 - 0.05 / m_):.2f}; expected max |t| of M null tests ~ sqrt(2 ln M) = {sqrt(2 * log(m_)):.2f}")
# White reality check: statistic = mean $ P&L per print (0 when flat); bootstrap prints iid
rng = np.random.default_rng(3)
names = [k for k in PNL if k in set(T.name)]; X = np.column_stack([PNL[k] for k in names]); n = X.shape[0]
fbar = X.mean(0); V = sqrt(n) * fbar.max()
B = 4000; Vb = np.empty(B)
for b in range(B):
    ii = rng.integers(0, n, n); Vb[b] = (sqrt(n) * (X[ii].mean(0) - fbar)).max()
print(f"White reality check over {len(names)} tradeable structures ($/print, B={B}): best mean ${fbar.max():.1f}/print ({names[int(fbar.argmax())]}), p = {(Vb >= V).mean():.3f}")
# same for the fallback family only and the open family only
for fam in ["A-open", "B-close"]:
    nm_ = [k for k in names if k.startswith("A|" if fam == "A-open" else "B|")]; Xf = np.column_stack([PNL[k] for k in nm_]); fb = Xf.mean(0); Vf = sqrt(n) * fb.max()
    Vbf = np.array([(sqrt(n) * (Xf[rng.integers(0, n, n)].mean(0) - fb)).max() for _ in range(B)])
    print(f"  {fam}: {len(nm_)} structures, best ${fb.max():.1f}/print ({nm_[int(fb.argmax())]}), reality-check p = {(Vbf >= Vf).mean():.3f}")

# ---------- IV sensitivity for the key structures ----------
print("\n=== IV sensitivity (natural fills): EV_R for key structures ===")
def ev_struct(kind, iv, half=HALF):
    out = []
    for _, r in D.iterrows():
        if kind == "open_put_W10":
            Se = S_REF * r.Or; K1 = grid5(Se); p_, ml_, _ = vertical("P", K1, K1 - 10, Se, 2 / 252, iv, S_REF * r.Cr, 1 / 252, iv - DIV2, half); out.append((p_, ml_, True))
        elif kind == "open_put_W20_fri":
            Se = S_REF * r.Or; K1 = grid5(Se); p_, ml_, _ = vertical("P", K1, K1 - 20, Se, 2 / 252, iv, S_REF * r.C2r, 0.0, iv, half); out.append((p_, ml_, True))
        elif kind == "open_put_W10_fri":
            Se = S_REF * r.Or; K1 = grid5(Se); p_, ml_, _ = vertical("P", K1, K1 - 10, Se, 2 / 252, iv, S_REF * r.C2r, 0.0, iv, half); out.append((p_, ml_, True))
        elif kind == "fallback":
            g = r.gap; s = 1 if g > 0 else -1; cp = "C" if s > 0 else "P"; Se = S_REF * r.Cr; mid = (r.Or + 1) / 2
            ok = abs(g) >= 7 and (r.Cr >= mid if g > 0 else r.Cr <= mid); K1 = grid5(Se, "up" if s > 0 else "down"); K1 = K1 + s * 5 if K1 == round(Se, 2) else K1
            p_, ml_, _ = vertical(cp, K1, K1 + s * 10, Se, 6 / 252, iv, S_REF * r.C3r, 4 / 252, iv - 0.03, half); out.append((p_, ml_, ok))
    o = pd.DataFrame(out, columns=["p", "ml", "ok"]); o = o[o.ok]
    return (o.p / o.ml).mean(), o.p.mean(), len(o), o.ml.mean()
for kind, ivs in [("open_put_W10", [0.45, 0.55, 0.65, 0.80, 1.00]), ("open_put_W10_fri", [0.45, 0.55, 0.65, 0.80, 1.00]), ("open_put_W20_fri", [0.45, 0.55, 0.65, 0.80, 1.00]), ("fallback", [0.40, 0.45, 0.55, 0.65, 0.75])]:
    print(" ", kind, " | ".join(f"iv{iv:.0%}: {ev_struct(kind, iv)[0]:+.3f}R (${ev_struct(kind, iv)[1]:+.0f}, n={ev_struct(kind, iv)[2]}, risk ${ev_struct(kind, iv)[3]:.0f})" for iv in ivs))
print("  fill stress (half-spread/leg $0.10 RA-style / $0.25 / $0.50 base / $1.00 wide), fallback @55%:", " | ".join(f"${h:.2f}: {ev_struct('fallback', 0.55, h)[0]:+.3f}R" for h in [0.10, 0.25, 0.50, 1.00]))
print("  fill stress, open put W10 exit Thu close @65%:", " | ".join(f"${h:.2f}: {ev_struct('open_put_W10', 0.65, h)[0]:+.3f}R" for h in [0.10, 0.25, 0.50, 1.00]))
print("  fill stress, open put W10 hold to Fri expiry @65%:", " | ".join(f"${h:.2f}: {ev_struct('open_put_W10_fri', 0.65, h)[0]:+.3f}R" for h in [0.10, 0.25, 0.50, 1.00]))
print("\n=== Put debit spreads at the open (day-1 drift bet), by gap condition, natural fills ===")
s_ = G.name.str.split("|")
m_ = (s_.str[0] == "A") & (s_.str[2] == "put") & (s_.str[3].isin(["atm", "otm2"])) & (s_.str[4].isin(["W10", "W20"])) & (G.name.str.contains(r"\|(all|\|gap\|<3|\|gap\|<7|\|gap\|>=7|gap<=-3|gap>=3)$"))
print(G[m_].sort_values("name")[["name", "n", "maxloss", "EV_usd", "EV_R", "t", "win", "EV_R_pre16", "EV_R_post16", "last12_R"]].round(3).to_string(index=False))
print("\n=== With-gap / against-gap Oct 2 ATM $10-wide verticals at the open, hold to expiry ===")
print(G[G.name.str.match(r"A\|Oct2\|(with_gap|against_gap)\|atm\|W10\|fri_close\|")][["name", "n", "maxloss", "EV_usd", "EV_R", "t", "win", "EV_R_pre16", "EV_R_post16", "last12_R"]].round(3).to_string(index=False))

# ---------- fallback: per-trade detail ----------
print("\n=== Fallback (thr7, intact>=50%, with gap, W10, Oct 9, exit Mon close) per-trade, natural fills, IV 55% ===")
det = []
for _, r in D.iterrows():
    g = r.gap; s = 1 if g > 0 else -1; cp = "C" if s > 0 else "P"; Se = S_REF * r.Cr; mid = (r.Or + 1) / 2
    if not (abs(g) >= 7 and (r.Cr >= mid if g > 0 else r.Cr <= mid)): continue
    K1 = grid5(Se, "up" if s > 0 else "down"); K1 = K1 + s * 5 if K1 == round(Se, 2) else K1
    p_, ml_, deb = vertical(cp, K1, K1 + s * 10, Se, 6 / 252, IV9, S_REF * r.C3r, 4 / 252, IV9 - 0.03)
    det.append(dict(report=r.report, gap=round(g, 1), thu_cc=round((r.Cr - 1) * 100, 1), thu_to_mon=round((r.C3r / r.Cr - 1) * 100, 2), dir="call" if s > 0 else "put", debit=round(deb, 2), pnl=round(p_, 0), R=round(p_ / ml_, 2)))
det = pd.DataFrame(det); print(det.to_string(index=False))
x = det.pnl.values; print("n=%d mean $%.0f  meanR %+.3f  t=%.2f  win %.0f%%  | bootstrap 95%% CI $: (%.0f, %.0f) | with-gap drift Thu->Mon: mean %+.2f%%, t=%.2f" % (
    len(x), x.mean(), det.R.mean(), x.mean() / (x.std(ddof=1) / sqrt(len(x))), (x > 0).mean() * 100,
    *np.percentile(rng.choice(x, (10000, len(x))).mean(1), [2.5, 97.5]), (det.thu_to_mon * np.where(det.dir == "call", 1, -1)).mean(),
    (det.thu_to_mon * np.where(det.dir == "call", 1, -1)).mean() / ((det.thu_to_mon * np.where(det.dir == "call", 1, -1)).std(ddof=1) / sqrt(len(det)))))
# underlying drift Thu close -> Mon close with the gap, by threshold, all prints (no option layer)
print("\nUnderlying Thu close -> Mon close drift WITH the gap (no options), by |gap| threshold:")
for thr in [0, 3, 5, 7, 10]:
    m = D.gap.abs() >= thr; x = (np.sign(D.gap[m]) * (D.C3r[m] / D.Cr[m] - 1) * 100)
    print("  |gap|>=%2d: n=%2d mean %+.2f%% t=%.2f | 2001-15 %+.2f%% (n=%d) | 2016-26 %+.2f%% (n=%d)" % (thr, m.sum(), x.mean(), x.mean() / (x.std(ddof=1) / sqrt(len(x))),
          x[D.era[m] == "2001-15"].mean(), (D.era[m] == "2001-15").sum(), x[D.era[m] == "2016-26"].mean(), (D.era[m] == "2016-26").sum()))
