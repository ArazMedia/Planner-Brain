"""Daily breakout calibration (PA daily bars in inputs/pa_data, cut at Oct 7): apply the ev_calc rules mechanically to every
20-day-close-breakout event and score realized P&L. Structure = TSLA-row geometry from EV.md (long -0.17 ATR, short +0.29 ATR,
daily-close fail -0.53 ATR, H=5) and USO-row geometry (long +0.36, short +2.21, fail -0.18 ATR, H=30). Flat IV = RV20 (proxy),
debit = BS at that IV (so market EV ~ -costs), exit cost = 2% of width per leg-side (stated), nudge 0, LOO prior (own name, other
events) + pool (all names), cap mkt+10pp, EV_B with lift, rules as ev_calc."""
import json, math, glob, os, collections, statistics as stt, numpy as np, datetime as dt
from zoneinfo import ZoneInfo
Z = ZoneInfo('America/New_York'); R = 0.04
def ncdf(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))
def bs(S, K, T, iv):
    if T <= 0: return max(0.0, S - K)
    sd = iv * math.sqrt(T); d1 = (math.log(S / K) + R * T) / sd + sd / 2
    return S * ncdf(d1) - K * math.exp(-R * T) * ncdf(d1 - sd)
S = {}
for fn in glob.glob('/workspace/plans/20261009-ev/inputs/pa_data/*_1D.json'):
    nm = os.path.basename(fn).split('_')[0]
    if nm in ('GOOG', 'BTCUSD'): continue   # GOOG twin; BTCUSD dropped (IBIT covers it; $-scale would dominate)   # GOOGL kept; no twin double count
    B = json.load(open(fn)); rows = []
    for b in B:
        d = dt.datetime.fromtimestamp(b[0] / 1000 if b[0] > 1e12 else b[0], Z).date()
        if d <= dt.date(2026, 10, 7): rows.append(dict(d=d, o=b[1], h=b[2], l=b[3], c=b[4]))
    S[nm] = rows
def atr(s, i, n=14): return sum(max(s[k]['h'] - s[k]['l'], abs(s[k]['h'] - s[k-1]['c']), abs(s[k]['l'] - s[k-1]['c'])) for k in range(i-n+1, i+1)) / n
def rv(s, i): r = [math.log(s[k]['c'] / s[k-1]['c']) for k in range(i-19, i+1)]; m = sum(r)/20; return math.sqrt(sum((x-m)**2 for x in r)/19*(365 if False else 252))
GEOM = {'5d (TSLA-row geometry)': dict(dl=-0.17, ds=0.29, df=0.53, H=5), '30d (USO-row geometry)': dict(dl=0.36, ds=2.21, df=0.18, H=30)}
def outcome(s, i, g):
    a = atr(s, i); e = s[i]['c']; kl, ks, fl = e + g['dl'] * a, e + g['ds'] * a, e - g['df'] * a
    for j in range(1, g['H'] + 1):
        if s[i + j]['c'] < fl: return 's', j, (fl - s[i + j]['c']) / a
    c = s[i + g['H']]['c']; return ('t' if c >= ks else 'p' if c > kl else 'x'), g['H'], 0.0
def events(s, H):
    out = []; last = -10**9
    for i in range(21, len(s) - H - 1):
        if s[i]['c'] > max(b['h'] for b in s[i-20:i]) and i - last > H: out.append(i); last = i
    return out
def uncond(s, g, step=3):
    c = collections.Counter()
    for i in range(21, len(s) - g['H'] - 1, step): c[outcome(s, i, g)[0]] += 1
    return c
rng = np.random.default_rng(5)
RES = {}
for gname, g in GEOM.items():
    EV_ = {nm: [(i,) + outcome(s, i, g) for i in events(s, g['H'])] for nm, s in S.items()}
    pool = collections.Counter(o for L in EV_.values() for (_, o, _, _) in L); npool = sum(pool.values())
    unc = collections.Counter()
    for nm, s in S.items(): unc += uncond(s, g)
    unc_t = unc['t'] / sum(unc.values())
    T = g['H'] / 252
    rows = []
    for nm, L in EV_.items():
        s = S[nm]
        own_all = collections.Counter(o for (_, o, _, _) in L)
        for (i, o, j_stop, ov) in L:
            own = own_all.copy(); own[o] -= 1; n_own = sum(own.values())
            pl = pool.copy(); pl[o] -= 1; n_pl = npool - 1
            pool_p = {k: pl[k] / n_pl for k in 'tpxs'}; W = 10 if n_own < 15 else 5
            p = {k: (own[k] + W * pool_p[k]) / (n_own + W) for k in 'tpxs'}
            a = atr(s, i); e = s[i]['c']; iv = max(rv(s, i), 0.08)
            kl, ks, fl = e + g['dl'] * a, e + g['ds'] * a, e - g['df'] * a
            width = ks - kl; hs = 100 * 0.02 * width  # stated exit-cost proxy
            debit = 100 * (bs(e, kl, T, iv) - bs(e, ks, T, iv))
            z = rng.standard_normal((20000, g['H'])); dtau = T / g['H']
            P = e * np.exp(np.cumsum((R - iv*iv/2) * dtau + iv * math.sqrt(dtau) * z, axis=1))
            hit = (P < fl).any(axis=1); ST = P[:, -1]
            mk = dict(t=((~hit) & (ST >= ks)).mean(), p=((~hit) & (ST > kl) & (ST < ks)).mean(), s=hit.mean()); mk['x'] = 1 - mk['t'] - mk['p'] - mk['s']
            pm = (~hit) & (ST > kl) & (ST < ks); Vp = 100 * np.clip(ST[pm] - kl, 0, width).mean() - hs if pm.any() else 0
            Sst = fl - 0.55 * a; Tst = max(T - 2 * dtau, 0); Vs = max(100 * (bs(Sst, kl, Tst, iv) - bs(Sst, ks, Tst, iv)) - hs, 0)
            V = dict(t=100 * width - hs, p=Vp, s=Vs, x=0.0)
            if p['t'] > mk['t'] + .1:
                new = mk['t'] + .1
                for b in 'pxs': p[b] = p[b] / (1 - p['t']) * (1 - new)
                p['t'] = new
            def ev_at(pt):
                o_ = {b: p[b] for b in 'pxs'}; tot = sum(o_.values()) or 1
                return pt * (V['t'] - debit) + sum((1 - pt) * o_[b] / tot * (V[b] - debit) for b in o_)
            ev = ev_at(p['t']); lo = ev_at(max(p['t'] - .1, 0))
            lift = pool_p['t'] - unc_t; tb = min(max(mk['t'] + lift, .001), .999)
            q = {b: mk[b] / (1 - mk['t']) * (1 - tb) for b in 'pxs'}; q['t'] = tb
            evb = sum(q[k] * (V[k] - debit) for k in q)
            # realized
            if o == 's':
                Sx = s[i + j_stop]['c']; Tr = max(T - j_stop * dtau, 0); real = max(100 * (bs(Sx, kl, Tr, iv) - bs(Sx, ks, Tr, iv)) - hs, 0) - debit
            else:
                c = s[i + g['H']]['c']; v = 100 * min(max(c - kl, 0), width); real = v - (hs if v > 0 else 0) - debit
            for grade in ('B', 'C'):
                if lo > 0 and grade == 'B' and evb > 0: vb = 'TAKE'
                elif ev > 0.03 * debit: vb = 'WATCH'
                else: vb = 'SKIP'
                vf = 'SKIP' if vb == 'WATCH' and evb < 0 else vb
                rows.append(dict(name=nm, d=str(s[i]['d']), grade=grade, verdict=vf, verdict_brief=vb, ev=ev, evb=evb, lo=lo, real=real, debit=debit))
    def summ(grade, key='verdict'):
        R_ = [r for r in rows if r['grade'] == grade]
        out = dict(n=len(R_), counts=dict(collections.Counter(r[key] for r in R_)))
        for v in ('TAKE', 'WATCH', 'SKIP'):
            X = [r for r in R_ if r[key] == v]
            if X: out[v] = dict(n=len(X), win=sum(r['real'] > 0 for r in X) / len(X), mean_real=stt.mean(r['real'] for r in X), mean_pct=stt.mean(r['real'] / r['debit'] for r in X))
        out['skip_right'] = sum(1 for r in R_ if r[key] == 'SKIP' and r['real'] <= 0); out['skip_wrong'] = sum(1 for r in R_ if r[key] == 'SKIP' and r['real'] > 0)
        out['all'] = dict(win=sum(r['real'] > 0 for r in R_) / len(R_), mean_real=stt.mean(r['real'] for r in R_), mean_pct=stt.mean(r['real'] / r['debit'] for r in R_))
        return out
    RES[gname] = dict(B=summ('B'), C=summ('C'), B_brief=summ('B', 'verdict_brief'), names=sorted(S), unc_t=unc_t, pool_t=pool['t'] / npool)
    print(gname, json.dumps(RES[gname], default=lambda x: round(x, 3)))
json.dump(RES, open('phase3d.json', 'w'), indent=1, default=float)
