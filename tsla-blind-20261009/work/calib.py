"""Phase-3c calibration: apply the framework mechanically to every historical TSLA wick-reclaim event in HISTORY.
Per event: strikes at the same ATR offsets as today's structures, debit = BS at a flat IV proxy (0.90 x RV20 of that date,
the Oct-8 ratio MID-ATM-IV/RV20 = 0.263/0.292), prior = OTHER events only (expanding window = strictly earlier events; LOO
also reported), shrink to pool (same + SPY), nudge 0 (no historical factor data), market MC same stop rule, cap mkt+10pp,
EV_B drift-neutral, verdict under grade C (as RA graded today) and under grade B (math-only). Realized P&L uses the actual
forward closes (daily-close stop) and an intraday-stop variant."""
import math, numpy as np
from fw import *

def rv20_at(DD, i):
    r = [math.log(DD[k]['c'] / DD[k - 1]['c']) for k in range(i - 20, i)]
    m = sum(r) / 20; return math.sqrt(sum((x - m) ** 2 for x in r) / 19 * 252)

class RelStruct:
    """structure defined by ATR offsets from entry, priced at a flat IV."""
    def __init__(self, base, spot, A, iv):
        self.exp = base.exp; self.T_inc = base.T_inc; self.T = base.T; self.name = base.name
        self.kl = spot + (base.kl - SPOT) / A_NOW * A; self.ks = spot + (base.ks - SPOT) / A_NOW * A if base.ks else None
        self.ivl = iv; self.ivs = iv if base.ks else None; self.spot = spot
    def value(self, S, T, ivbump=0.0):
        v = bs(S, self.kl, T, self.ivl)
        if self.ks: v -= bs(S, self.ks, T, self.ivs)
        return v
    def legs_hs(self, S, T):
        h = width_half(bs(S, self.kl, T, self.ivl))
        if self.ks: h += width_half(bs(S, self.ks, T, self.ivs))
        return 100 * h
    def debit(self): return 100 * self.value(self.spot, self.T)
    def payoff(self, ST):
        v = max(ST - self.kl, 0.0)
        if self.ks: v = min(v, self.ks - self.kl)
        return v

SREC = []
def bucket_rel(E, base, debit_frac, stop_mode):
    """buckets for events E for a structure given in ATR offsets (base = today's Struct). debit_frac = debit/(100*A) for BE of calls."""
    N = EXPN[base.exp]; dl = (base.kl - SPOT) / A_NOW
    cnt = dict(t=0, p=0, x=0, s=0); sd = []; ov = []
    for e in E:
        f_ = e['fwd']
        if any(c is None for c in f_[:N + 1]): continue
        A, en = e['atr'], e['entry']
        ds = (base.ks - SPOT) / A_NOW if base.ks else dl + debit_frac
        out = None
        if stop_mode == 'daily':
            for j in range(N):
                if f_[j] < e['wick']: out = 's'; sd.append(j); ov.append((e['wick'] - f_[j]) / A); break
        else:
            for b in (e['path1'] or []):
                if b[4] < e['L'] or b[3] < e['wick']:
                    px = (min(b[1], e['wick']) if b[3] < e['wick'] else b[4])
                    out = 's'; sd.append(0); ov.append(0.0); SREC.append(((px - en) / A, elapsed_var(e, b[0]))); break
            if out is None:
                for j in range(2, N):
                    if f_[j] < e['wick']: out = 's'; sd.append(j); ov.append((e['wick'] - f_[j]) / A); break
        if out is None:
            c = f_[N]; out = 't' if c >= en + ds * A else ('p' if c > en + dl * A else 'x')
        cnt[out] += 1
    return cnt, sum(cnt.values()), sd, ov

def mc_rel(st, wick, level, N, stop_mode, n=40000, seed=7):
    rng = np.random.default_rng(seed); iv = st.ivl; spot = st.spot
    if stop_mode == 'daily':
        steps = list(st.T_inc); is_close = [True] * len(steps)
    else:
        steps = [st.T_inc[0] / 9] * 9; is_close = [False] * 8 + [True]
        for x in st.T_inc[1:]:
            steps.append(x - 1 / 252); is_close.append(False); steps += [1 / 252 / 26] * 26; is_close += [False] * 25 + [True]
    steps = np.array(steps); z = rng.standard_normal((n, len(steps)))
    paths = spot * np.exp(np.cumsum((R - iv * iv / 2) * steps + iv * np.sqrt(steps) * z, axis=1))
    ci = [k for k, c in enumerate(is_close) if c]
    if stop_mode == 'daily': beyond = paths[:, ci[:-1]] < wick
    else: beyond = paths[:, :ci[-1]] < level
    hit = beyond.any(axis=1); ST = paths[:, -1]
    return hit, ST

def eval_event(e, base, own, pool, unc_t_cache, stop_mode='daily', cap=True, demote=True, driftmin=True, grade='C'):
    A, spot = e['atr'], e['entry']; i = DI[e['day']]
    iv = 0.90 * rv20_at(D, i); st = RelStruct(base, spot, A, iv)
    debit = st.debit(); hs = st.legs_hs(spot, st.T); N = EXPN[base.exp]
    dfrac = debit / 100 / A
    co, no, _, _ = bucket_rel(own, base, dfrac, stop_mode); cp, np_, sdp, ovp = bucket_rel(pool, base, dfrac, stop_mode)
    if np_ == 0: return None
    pool_p = {k: cp[k] / np_ for k in cp}; W = 10 if no < 15 else 5
    p = {k: (co[k] + W * pool_p[k]) / (no + W) for k in co}
    hit, ST = mc_rel(st, e['wick'], e['L'], N, stop_mode)
    tK = st.ks if st.ks else st.kl + debit / 100
    pay = np.array([st.payoff(x) for x in ST])
    t_m = (~hit) & (ST >= tK); p_m = (~hit) & (ST > st.kl) & ~t_m; x_m = (~hit) & ~t_m & ~p_m
    mk = dict(t=t_m.mean(), p=p_m.mean(), x=x_m.mean(), s=hit.mean())
    if cap and p['t'] > mk['t'] + .1:
        new = mk['t'] + .1
        for b in 'pxs': p[b] = p[b] / (1 - p['t']) * (1 - new)
        p['t'] = new
    over = float(np.mean(ovp)) if ovp else 0.0; med = sorted(sdp)[len(sdp) // 2] if sdp else 0
    if stop_mode == 'daily': Sst, Tst = e['wick'] - over * A, max(st.T - sum(st.T_inc[:med + 1]), 0)
    else: Sst, Tst = e['L'], st.T
    Vs = max(100 * st.value(Sst, Tst) - st.legs_hs(Sst, Tst), 0)
    if stop_mode != 'daily':
        SREC.clear(); bucket_rel(pool, base, dfrac, stop_mode)
        if SREC: Vs = float(np.mean([max(100 * st.value(spot + d * A, max(st.T - el, 1e-6)) - st.legs_hs(spot + d * A, max(st.T - el, 1e-6)), 0) for d, el in SREC]))
    V = dict(t=((st.ks - st.kl) * 100 - hs) if st.ks else 100 * pay[t_m].mean() - hs if t_m.any() else 0,
             p=100 * pay[p_m].mean() - hs if p_m.any() else 0, s=Vs, x=0.0)
    def ev_at(pt, P):
        o = {b: P[b] for b in 'pxs'}; tot = sum(o.values()) or 1
        return pt * (V['t'] - debit) + sum((1 - pt) * o[b] / tot * (V[b] - debit) for b in o)
    ev = ev_at(p['t'], p); lo = ev_at(max(p['t'] - .1, 0), p)
    lift = pool_p['t'] - unc_t_cache[(base.name, stop_mode)]
    q = dict(mk); tb = min(max(q['t'] + lift, .001), .999)
    for b in 'pxs': q[b] = q[b] / (1 - mk['t']) * (1 - tb) if mk['t'] < 1 else 0
    q['t'] = tb; evb = sum(q[k] * (V[k] - debit) for k in q)
    noise = 0.03 * debit
    if lo > 0 and grade in 'AB' and (evb > 0 or not driftmin): v = 'TAKE'
    elif ev > noise and grade in 'ABC': v = 'WATCH'
    else: v = 'SKIP'
    if demote and v == 'WATCH' and evb < 0: v = 'SKIP'
    # realized P&L (actual forward path), same stop rule as the evaluation
    f_ = e['fwd']; stopped = False
    if stop_mode == 'daily':
        for j in range(N):
            if f_[j] < e['wick']:
                stopped = True; Tr = max(st.T - sum(st.T_inc[:j + 1]), 0); real = max(100 * st.value(f_[j], Tr) - st.legs_hs(f_[j], Tr), 0) - debit; break
    else:
        for b in (e['path1'] or []):
            if b[4] < e['L'] or b[3] < e['wick']:
                stopped = True; px = (min(b[1], e['wick']) if b[3] < e['wick'] else b[4]); Tr = max(st.T - elapsed_var(e, b[0]), 1e-6)
                real = max(100 * st.value(px, Tr) - st.legs_hs(px, Tr), 0) - debit; break
        if not stopped:
            for j in range(2, N):
                if f_[j] < e['wick']:
                    stopped = True; Tr = max(st.T - sum(st.T_inc[:j + 1]), 0); real = max(100 * st.value(f_[j], Tr) - st.legs_hs(f_[j], Tr), 0) - debit; break
    if not stopped:
        pv = 100 * st.payoff(f_[N]); real = pv - (hs if pv > 0 else 0) - debit
    return dict(day=e['day'], verdict=v, ev=ev, evb=evb, lo=lo, debit=debit, real=real, stopped=stopped, p_t=p['t'], mk_t=mk['t'])

def run_calib(bases, mode='expanding', stop_mode='daily', grade='C', **kw):
    unc = {}
    for b in bases:
        cu, nu = uncond(b, b.debit()); unc[(b.name, stop_mode)] = cu['t'] / nu   # whole-sample drift baseline (stated)
    rows = []
    for b in bases:
        N = EXPN[b.exp]
        for k, e in enumerate(E15):
            if any(c is None for c in e['fwd'][:N + 1]): continue
            if mode == 'expanding':
                own = [x for x in E15 if x['day'] < e['day'] and DI[x['day']] + N < DI[e['day']]]   # resolved before the event
                pool = own + [x for x in ESPY if x['day'] < e['day']]
                if len(own) < 5: continue
            else:
                own = [x for x in E15 if x is not e]; pool = own + ESPY
            r = eval_event(e, b, own, pool, unc, stop_mode=stop_mode, grade=grade, **kw)
            if r: rows.append(dict(r, struct=b.name))
    return rows
