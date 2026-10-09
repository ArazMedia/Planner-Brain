"""Phase-1 framework for the TSLA 370.25 wick-reclaim (as of 2026-10-08 13:40 ET). Same rules as outputs/ev_calc.py:
prior (HISTORY event study) -> Dirichlet shrink to pool -> bounded log-odds nudge (RA as-of factors) -> market MC with the
SAME stop rule -> cap at mkt+10pp -> EV; drift-neutral EV_B; verdict TAKE/WATCH/SKIP (+ WATCH->SKIP if EV_B<0).
Switches (for the phase-3 audit) are keyword args of evaluate()."""
import math, json, datetime as dt, numpy as np
from events import *

R = 0.04
SPOT = 370.57; WICK = 368.04; LEVEL = 370.25
# RA variance clock: RTH day = 1, weeknight = 0.25, weekend day = 0.10, /252
def clock_steps(exp):
    """variance (trading-day units) from 13:40 Oct 8 to each daily close up to expiry: list of increments."""
    inc = [140 / 390]  # rest of Oct 8 RTH
    cal = {'261009': ['F'], '261012': ['F', 'M'], '261014': ['F', 'M', 'T', 'W'], '261016': ['F', 'M', 'T', 'W', 'Th', 'Fr']}[exp]
    for dname in cal:
        inc.append((0.25 + 0.10 + 0.10 + 1.0) if dname == 'M' else 1.25)
    return [x / 252 for x in inc]
EXPN = {'261009': 1, '261012': 2, '261016': 6}   # settle = day-N close after the event day

# ---- MID IVs from RA_tsla_asof_prices.csv (13:35 close); strikes not in RA's grid are linearly inter/extrapolated in strike
import csv
RAP = [r for r in csv.DictReader(open('../inputs/RA_tsla_asof_prices.csv')) if r['when'] == '13:35 close']
def iv_table(sc='MID'):
    T = {}
    for r in RAP:
        if r['sc'] == sc and r['iv']:
            T.setdefault(r['exp'], {})[float(r['leg'][:-1])] = float(r['iv'])
    return T
def iv_at(T, exp, K):
    ks = sorted(T[exp]); 
    if K in T[exp]: return T[exp][K]
    if K < ks[0]: a, b = ks[0], ks[1]
    elif K > ks[-1]: a, b = ks[-2], ks[-1]
    else: a = max(k for k in ks if k < K); b = min(k for k in ks if k > K)
    return T[exp][a] + (T[exp][b] - T[exp][a]) * (K - a) / (b - a)

def ncdf(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))
def bs(S, K, T, iv):
    if T <= 0 or iv <= 0: return max(0.0, S - K)
    sd = iv * math.sqrt(T); d1 = (math.log(S / K) + R * T) / sd + sd / 2
    return S * ncdf(d1) - K * math.exp(-R * T) * ncdf(d1 - sd)
def width_half(p): return 0.025 if p < 2 else (0.05 if p < 10 else 0.075)   # half of RA's assumed bid/ask

class Struct:
    def __init__(self, exp, kl, ks=None, sc='MID'):
        self.exp, self.kl, self.ks, self.sc = exp, kl, ks, sc
        self.T_inc = clock_steps(exp); self.T = sum(self.T_inc)
        IV = iv_table(sc); self.ivl = iv_at(IV, exp, kl); self.ivs = iv_at(IV, exp, ks) if ks else None
        self.name = f"Oct{int(exp[4:])} {kl:g}" + (f"/{ks:g}C" if ks else "C")
    def value(self, S, T, ivbump=0.0):
        v = bs(S, self.kl, T, self.ivl + ivbump)
        if self.ks: v -= bs(S, self.ks, T, self.ivs + ivbump)
        return v
    def legs_hs(self, S, T):  # half bid/ask per leg in $ (x100)
        h = width_half(bs(S, self.kl, T, self.ivl))
        if self.ks: h += width_half(bs(S, self.ks, T, self.ivs))
        return 100 * h
    def debit(self): return 100 * self.value(SPOT, self.T)
    def payoff(self, ST):
        v = max(ST - self.kl, 0.0)
        if self.ks: v = min(v, self.ks - self.kl)
        return v

STRUCTS = [Struct('261009', 370), Struct('261009', 372.5), Struct('261009', 375),
           Struct('261009', 370, 375), Struct('261009', 370, 380), Struct('261009', 372.5, 377.5), Struct('261009', 375, 380), Struct('261009', 375, 385),
           Struct('261012', 370, 375), Struct('261012', 370, 380),
           Struct('261016', 370, 380), Struct('261016', 375, 385), Struct('261016', 380, 390)]

# ---------------- HISTORY: events + forward paths (leak-free: all bars end <= 13:40 Oct 8; daily <= Oct 7) ----------------
D = load_daily('../inputs/TSLA_D_asof.json'); DI = {x['d']: n for n, x in enumerate(D)}
B5 = load5('../inputs/TSLA_5m_hist.json', sec=300); B15 = load5('../inputs/TSLA_15m_hist.json', sec=900)  # PA HISTORY (verified identical to raw cut at 13:40)
A_NOW = atr_at(D, len(D) - 1)

def build_events(bars, sec, rb, sym_daily=None):
    DD = sym_daily or D
    ev, days, dl = find_events(bars, DD, sec=sec, reclaim_bars=rb)
    di = {x['d']: n for n, x in enumerate(DD)}
    out = []
    for e in ev:
        i = di[e['day']]; dlist = list(days.keys()); k = dlist.index(e['day'])
        fwd = [DD[i + j]['c'] if i + j < len(DD) else None for j in range(0, 7)]   # day0..day6 closes (daily file)
        # intraday path from entry to next-day close (bars after entry)
        path = [b for b in days[e['day']] if b[0] > e['t_entry']]
        nxt = days[dlist[k + 1]] if k + 1 < len(dlist) else None
        p1 = path + (nxt or [])
        e2 = dict(e, fwd=fwd, path0=path, path1=p1 if nxt else None, sec=sec)
        out.append(e2)
    return out

def intraday_stats(e, d_short):
    """MFE/MAE (ATR) to day0 and day1 close; intraday stops; target-before-stop (target = entry + d_short*ATR)."""
    A, en, w, L = e['atr'], e['entry'], e['wick'], e['L']
    res = {}
    for tag, P in (('d0', e['path0']), ('d1', e['path1'])):
        if not P: res[tag] = None; continue
        mfe = (max(b[2] for b in P) - en) / A; mae = (min(b[3] for b in P) - en) / A
        tgt = en + d_short * A; first = None
        for b in P:
            hitS_wick = b[3] < w; hitS_close = b[4] < L; hitT = b[2] >= tgt
            if hitT and not (hitS_wick): first = first or 'T'; break
            if hitS_wick: first = 'S_wick'; break
        # reclaim-failure stop (close back under level) first?
        fc = None
        for b in P:
            if b[2] >= tgt: fc = 'T'; break
            if b[4] < L: fc = 'S_close'; break
        res[tag] = dict(mfe=mfe, mae=mae, first_wickstop=first or 'none', first_closestop=fc or 'none')
    return res

# ---------------- framework evaluation ----------------
SPYD = load_daily('../../inputs/pa_data/SPY_1D.json'); SPY5 = load5('../../inputs/pa_data/SPY_5m.json', sec=300)
E15 = build_events(B15, 900, 2); E5 = build_events(B5, 300, 4)
ESPY = build_events(SPY5, 300, 4, sym_daily=SPYD)
D_FAIL_NOW = (SPOT - WICK) / A_NOW

STOPREC = []
def elapsed_var(e, t):
    """variance-clock time (trading-day units /252) from the event entry to bar time t (end of bar)"""
    t0 = f(e['t_entry']); t1 = f(t + e['sec'])
    if t1.date() == t0.date(): return (t1 - t0).total_seconds() / 60 / 390 / 252
    close0 = t0.replace(hour=16, minute=0); open1 = t1.replace(hour=9, minute=30)
    return ((close0 - t0).total_seconds() / 60 / 390 + 0.25 + (t1 - open1).total_seconds() / 60 / 390) / 252

def bucket_hist(E, st, debit, stop_mode='daily', d_fail_mode='own'):
    """count t/p/x/s for events E for structure st (strikes in ATR from entry). daily-close stop on days 0..N-1."""
    N = EXPN[st.exp]; dl = (st.kl - SPOT) / A_NOW
    ds = (st.ks - SPOT) / A_NOW if st.ks else (st.kl + debit / 100 - SPOT) / A_NOW   # long call: 'target' = settle > BE
    cnt = dict(t=0, p=0, x=0, s=0); sdays = []; over = []; realized = []
    for e in E:
        f_ = e['fwd']
        if any(c is None for c in f_[:N + 1]): continue
        A, en = e['atr'], e['entry']; fl = e['wick'] if d_fail_mode == 'own' else en - D_FAIL_NOW * A
        out = None
        if stop_mode == 'daily':
            for j in range(0, N):
                if f_[j] < fl: out = 's'; sdays.append(j); over.append((fl - f_[j]) / A); break
        else:  # intraday: first 5m/15m close < level (reclaim failure) or low < wick, scanned to day-1 close; daily closes after
            P = e['path1'] or []
            for b in P:
                if b[4] < e['L'] or b[3] < e['wick']:
                    px = (min(b[1], e['wick']) if b[3] < e['wick'] else b[4])          # stop order at the wick (gap -> open), else exit on the close
                    out = 's'; sdays.append(0); over.append((fl - min(b[4], fl)) / A)
                    STOPREC.append(((px - en) / A, elapsed_var(e, b[0]))); break
            if out is None:
                for j in range(2, N):
                    if f_[j] < fl: out = 's'; sdays.append(j); over.append((fl - f_[j]) / A); break
        if out is None:
            c = f_[N]
            out = 't' if c >= en + ds * A else ('p' if c > en + dl * A else 'x')
        cnt[out] += 1
    return cnt, sum(cnt.values()), sdays, over

def uncond(st, debit, stride=3):
    N = EXPN[st.exp]; dl = (st.kl - SPOT) / A_NOW
    ds = (st.ks - SPOT) / A_NOW if st.ks else (st.kl + debit / 100 - SPOT) / A_NOW
    days = rth_days(B15, 900); cnt = dict(t=0, p=0, x=0, s=0)
    for d, bars in days.items():
        if d not in DI: continue
        i = DI[d]
        if i < 20 or i + N >= len(D): continue
        A = atr_at(D, i - 1)
        for b in bars[2:-2:stride]:
            en = b[4]; fl = en - D_FAIL_NOW * A; out = None
            for j in range(0, N):
                if D[i + j]['c'] < fl: out = 's'; break
            if out is None:
                c = D[i + N]['c']; out = 't' if c >= en + ds * A else ('p' if c > en + dl * A else 'x')
            cnt[out] += 1
    return cnt, sum(cnt.values())

_IVC = {}
CALIB = False   # framework default (ev_calc): flat IV = mean of the two legs
def iv_calib(st, debit):
    """flat IV at which the lognormal (no-stop) expected payoff equals the quoted debit: the market measure consistent
    with RA's smile-priced debit (avoids the flat-IV-vs-skew artifact noted in EV.md)."""
    key = (st.name, st.sc)
    if key in _IVC: return _IVC[key]
    z = np.random.default_rng(3).standard_normal(200_000); T = st.T
    def val(iv):
        ST = SPOT * np.exp((R - iv * iv / 2) * T + iv * math.sqrt(T) * z)
        pay = np.clip(ST - st.kl, 0, None)
        if st.ks: pay = np.minimum(pay, st.ks - st.kl)
        return 100 * math.exp(-R * T) * pay.mean()
    lo, hi = 0.05, 1.5
    if st.ks:  # spread value is not monotone in iv in general; scan
        grid = np.linspace(0.08, 0.8, 145); vals = [val(g) for g in grid]
        k = int(np.argmin([abs(v - debit) for v in vals])); _IVC[key] = float(grid[k]); return _IVC[key]
    for _ in range(40):
        m = (lo + hi) / 2
        if val(m) > debit: hi = m
        else: lo = m
    _IVC[key] = (lo + hi) / 2; return _IVC[key]

def mc_market(st, debit, n=100_000, seed=7, stop_mode='daily', ivb=0.0):
    rng = np.random.default_rng(seed); iv = (iv_calib(st, debit) if CALIB else (st.ivl + (st.ivs or st.ivl)) / 2) + ivb
    N = EXPN[st.exp]; inc = st.T_inc
    if stop_mode == 'daily':
        steps = inc; is_close = [True] * len(inc)
    else:  # 15m RTH substeps; overnight as one jump
        steps = []; is_close = []
        nrest = 9
        steps += [inc[0] / nrest] * nrest; is_close += [False] * (nrest - 1) + [True]
        for x in inc[1:]:
            day = 1 / 252; night = x - day
            steps.append(night); is_close.append(False)
            steps += [day / 26] * 26; is_close += [False] * 25 + [True]
    steps = np.array(steps); z = rng.standard_normal((n, len(steps)))
    paths = SPOT * np.exp(np.cumsum((R - iv * iv / 2) * steps + iv * np.sqrt(steps) * z, axis=1))
    close_idx = [k for k, c in enumerate(is_close) if c]
    if stop_mode == 'daily':
        chk = paths[:, close_idx[:-1]]; beyond = chk < WICK; idxmap = close_idx[:-1]
    else:
        chk = paths[:, :close_idx[-1]]; beyond = (chk < LEVEL); idxmap = list(range(close_idx[-1]))
    hit = beyond.any(axis=1); first = np.where(hit, beyond.argmax(axis=1), -1)
    ST = paths[:, -1]
    dl = st.kl; dsK = st.ks if st.ks else st.kl + debit / 100
    t_m = (~hit) & (ST >= dsK); p_m = (~hit) & (ST > dl) & ~t_m; x_m = (~hit) & ~t_m & ~p_m
    intr = np.array([st.payoff(s) for s in ST[: min(n, 40000)]]); 
    cum = np.cumsum(steps); Ttot = cum[-1]
    resid = []
    for k in np.where(hit)[0][:15000]:
        j = idxmap[first[k]]; resid.append(st.value(paths[k, j], max(Ttot - cum[j], 0)))
    m = min(n, 40000)
    V_part = intr[p_m[:m]].mean() if p_m[:m].any() else 0
    V_targ = intr[t_m[:m]].mean() if t_m[:m].any() else 0
    return dict(t=t_m.mean(), p=p_m.mean(), x=x_m.mean(), s=hit.mean(), part=V_part, targ=V_targ,
                resid=float(np.mean(resid)) if resid else 0.0, gross=100 * (np.mean(intr) if True else 0))

GRADE = {'261009': ('C', 0.55), '261012': ('C', 0.55), '261016': ('C', 0.45)}
NUDGE_A = 0.0; NUDGE_B = 0.0   # RA as-of: volume 0, gamma 0 (n/a), flow 0 (n/a), trend 0  -> dir scores 0 -> nudge 0

def evaluate(st, cap=True, driftmin=True, stop_mode='daily', demote=True, convex=False, grade_override=None, own=None,
             nudgeA=None, nudgeB=None, ivsc=None):
    debit = st.debit(); hs_entry = st.legs_hs(SPOT, st.T)
    own = own if own is not None else E15
    c_own, n_own, sd, ov = bucket_hist(own, st, debit, stop_mode)
    c_pool, n_pool, sdp, ovp = bucket_hist(own + ESPY, st, debit, stop_mode)
    pool_p = {k: c_pool[k] / n_pool for k in c_pool}
    W = 10 if n_own < 15 else 5
    p = {k: (c_own[k] + W * pool_p[k]) / (n_own + W) for k in c_own}; prior = dict(p)
    nA = NUDGE_A if nudgeA is None else nudgeA; nB = NUDGE_B if nudgeB is None else nudgeB
    pt = 1 / (1 + math.exp(-(math.log(max(p['t'], 1e-4) / (1 - p['t'])) + nA)))
    for b in 'pxs': p[b] = p[b] / (1 - p['t']) * (1 - pt)
    p['t'] = pt
    mc = mc_market(st, debit, stop_mode=stop_mode)
    capped = False
    if cap and p['t'] > mc['t'] + 0.10:
        new = mc['t'] + 0.10
        for b in 'pxs': p[b] = p[b] / (1 - p['t']) * (1 - new)
        p['t'] = new; capped = True
    N = EXPN[st.exp]
    med = sorted(sdp)[len(sdp) // 2] if sdp else 0; over = float(np.mean(ovp)) if ovp else 0.0
    if stop_mode == 'daily':
        Tst = max(st.T - sum(st.T_inc[:med + 1]), 0); Sst = WICK - over * A_NOW
    else:
        Sst = LEVEL; Tst = st.T
    resid = 100 * st.value(Sst, Tst); hs_stop = st.legs_hs(Sst, Tst)
    if stop_mode != 'daily':   # empirical: each pool stop mapped to today (price offset in ATR, elapsed variance-time)
        STOPREC.clear(); bucket_hist(own + ESPY, st, debit, stop_mode)
        vs = [100 * st.value(SPOT + d * A_NOW, max(st.T - el, 1e-6)) - st.legs_hs(SPOT + d * A_NOW, max(st.T - el, 1e-6)) for d, el in STOPREC]
        resid = float(np.mean(vs)) if vs else 0.0; hs_stop = 0.0
    if st.ks: Vt = (st.ks - st.kl) * 100 - hs_entry
    else: Vt = 100 * mc['targ'] - hs_entry
    V = dict(t=Vt, p=100 * mc['part'] - hs_entry, s=max(resid - hs_stop, 0), x=0.0)
    def ev_at(ptv, D_=debit, P=p):
        o = {b: P[b] for b in 'pxs'}; tot = sum(o.values())
        return ptv * (V['t'] - D_) + sum((1 - ptv) * o[b] / tot * (V[b] - D_) for b in o)
    ev = ev_at(p['t']); ev_lo = ev_at(max(p['t'] - .1, 0)); ev_hi = ev_at(min(p['t'] + .1, 1))
    be = -ev_at(0) / ((V['t'] - debit) - ev_at(0))
    ev_full = ev_at(p['t'], debit + hs_entry)
    # convexity variant: empirical payoff distribution (exact payoff at each event's settle, stop residual), shrunk 1:1 to pool events
    ev_cvx = None
    if convex:
        vals = []
        for E_, wgt in ((own, 1.0), (ESPY, 1.0)):
            for e in E_:
                f_ = e['fwd']
                if any(c is None for c in f_[:N + 1]): continue
                A, en = e['atr'], e['entry']; stopped = None
                if stop_mode == 'daily':
                    for j in range(N):
                        if f_[j] < e['wick']: stopped = (j, e['wick'] - over * A); break
                else:
                    for b in (e['path1'] or []):
                        if b[4] < e['L'] or b[3] < e['wick']: stopped = (0, None); break
                if stopped:
                    vals.append((wgt, V['s'] - debit))
                else:
                    S_map = SPOT + (f_[N] - en) / A * A_NOW
                    vals.append((wgt, 100 * st.payoff(S_map) - (hs_entry if st.payoff(S_map) > 0 else 0) - debit))
        ev_cvx = sum(w * v for w, v in vals) / sum(w for w, v in vals)
    # drift-neutral EV_B
    cu, nu = uncond(st, debit); unc_t = cu['t'] / nu
    lift = pool_p['t'] - unc_t
    q = dict(t=mc['t'], p=mc['p'], x=mc['x'], s=mc['s'])
    tb = min(max(q['t'] + lift, 0.001), 0.999); tb = 1 / (1 + math.exp(-(math.log(tb / (1 - tb)) + nB)))
    for b in 'pxs': q[b] = q[b] / (1 - mc['t']) * (1 - tb)
    q['t'] = tb
    ev_b = sum(q[k] * (V[k] - debit) for k in q)
    ev_mkt = sum({'t': mc['t'], 'p': mc['p'], 'x': mc['x'], 's': mc['s']}[k] * (V[k] - debit) for k in q)
    g, score = grade_override or GRADE[st.exp]
    fired = True
    ev_use = ev_cvx if convex else ev
    lo_use = ev_lo if not convex else ev_cvx - (ev - ev_lo)
    noise = 0.03 * debit
    take_ok = lo_use > 0 and g in 'AB' and fired and (ev_b > 0 if driftmin else True)
    if take_ok: v = 'TAKE'
    elif ev_use > noise and g in 'ABC': v = 'WATCH'
    else: v = 'SKIP'
    vb = v
    if demote and v == 'WATCH' and ev_b < 0: v = 'SKIP'
    rule = ('TAKE: all gates pass' if v == 'TAKE' else
            'WATCH: EV>3% debit, grade C blocks TAKE (needs >=B)' if v == 'WATCH' and g == 'C' else
            'WATCH: EV>0 but -10pp band or EV_B fails TAKE' if v == 'WATCH' else
            'SKIP: WATCH demoted because drift-neutral EV_B<0' if vb == 'WATCH' and v == 'SKIP' else
            'SKIP: EV <= 3% of debit (noise floor)' if ev_use <= noise else 'SKIP: grade')
    return dict(name=st.name, debit=debit, debit_full=debit + hs_entry, grade=g, score=score, n_own=n_own, own=c_own, n_pool=n_pool,
                pool_t=pool_p['t'], unc_t=unc_t, n_unc=nu, lift=lift, W=W, prior=prior, p=p, mkt=mc, capped=capped, V=V, ev=ev, ev_lo=ev_lo,
                ev_hi=ev_hi, be=be, ev_full=ev_full, ev_b=ev_b, q=q, ev_mkt=ev_mkt, ev_cvx=ev_cvx, cons=min(ev_use, ev_b) if driftmin else ev_use,
                verdict=v, verdict_brief=vb, rule=rule, med_stop=med, over=over)
