import json, statistics as stt, random
from fw import *
B60 = load5('../inputs/TSLA_60m_asof.json', sec=3600)
E60 = build_events(B60, 3600, 1)
E60 = [e for e in E60 if e['day'] < dt.date(2026, 2, 2)]
SPYdays = rth_days(SPY5, 300)
def feats(e, days_bars):
    bars = days_bars[e['day']]; A = e['atr']
    upto = [b for b in bars if b[0] <= e['t_entry']]
    vw = sum((b[2] + b[3] + b[4]) / 3 * b[5] for b in upto) / max(sum(b[5] for b in upto), 1)
    brk = [b for b in upto if b[3] < e['L']]
    avgv = stt.mean(b[5] for b in upto) if upto else 1
    i = DI[e['day']]; sma20 = stt.mean(D[k]['c'] for k in range(i - 20, i))
    t = f(e['t_entry']); tod = t.hour + t.minute / 60
    rs = None
    if e['day'] in SPYdays:
        sb = SPYdays[e['day']]; s_up = [b for b in sb if b[0] <= e['t_entry']]
        if s_up: rs = (e['entry'] / bars[0][1] - 1) - (s_up[-1][4] / sb[0][1] - 1)
    return dict(touches=e['ntouch'], pivots=e['npiv'], depth=(e['L'] - e['wick']) / A, closes_below=e['closes_below'],
                vwap_gap=(e['entry'] - vw) / A, mom=(e['entry'] - bars[0][1]) / A, testvol=(max(b[5] for b in brk) / avgv) if brk else float('nan'),
                trend=(D[i - 1]['c'] - sma20) / A, tod=tod, rs_spy=rs)
def outcomes(e):
    f_ = e['fwd']; A = e['atr']
    if f_[1] is None: return None
    stop_intra = any(b[4] < e['L'] or b[3] < e['wick'] for b in (e['path1'] or []))
    return dict(d1=(f_[1] - e['entry']) / A, win375=f_[1] >= e['entry'] + 0.4 * A, survive=not stop_intra,
                dstop0=f_[0] < e['wick'])
rows = []
for E, bars in ((E15, rth_days(B15, 900)), (E60, rth_days(B60, 3600))):
    for e in E:
        o = outcomes(e)
        if o: rows.append(dict(day=str(e['day']), src='15m' if e['sec'] == 900 else '60m', **feats(e, bars), **o))
def split(key, rows, thr=None, hi_good=True):
    R = [r for r in rows if r[key] is not None and r[key] == r[key]]
    if len(R) < 6: return None
    thr = thr if thr is not None else stt.median(r[key] for r in R)
    hi = [r for r in R if r[key] > thr]; lo = [r for r in R if r[key] <= thr]
    if not hi or not lo: return None
    m = lambda S, k: stt.mean(float(r[k]) for r in S)
    diff = m(hi, 'd1') - m(lo, 'd1')
    random.seed(1); bs_ = []
    for _ in range(2000):
        h = [random.choice(hi) for _ in hi]; l = [random.choice(lo) for _ in lo]; bs_.append(m(h, 'd1') - m(l, 'd1'))
    bs_.sort()
    return dict(key=key, thr=thr, n_hi=len(hi), n_lo=len(lo), d1_hi=m(hi, 'd1'), d1_lo=m(lo, 'd1'), diff=diff, ci=(bs_[50], bs_[1949]),
                win_hi=m(hi, 'win375'), win_lo=m(lo, 'win375'), surv_hi=m(hi, 'survive'), surv_lo=m(lo, 'survive'))
res = {}
for key, thr in (('touches', None), ('pivots', 2), ('depth', None), ('closes_below', 0), ('vwap_gap', 0.0), ('mom', None), ('testvol', None),
                 ('trend', 0.0), ('tod', 12.0), ('rs_spy', 0.0)):
    for lab, R in (('15m', [r for r in rows if r['src'] == '15m']), ('all', rows)):
        s = split(key, R, thr)
        res[f'{key}|{lab}'] = s
        if s: print(f"{key:12s} {lab:4s} thr={s['thr']:.2f} n={s['n_hi']}/{s['n_lo']} d1 hi {s['d1_hi']:+.2f} lo {s['d1_lo']:+.2f} diff {s['diff']:+.2f} CI[{s['ci'][0]:+.2f},{s['ci'][1]:+.2f}] win {s['win_hi']:.0%}/{s['win_lo']:.0%} surv {s['surv_hi']:.0%}/{s['surv_lo']:.0%}")
        else: print(key, lab, 'n too small')
today = dict(touches=11, pivots=4, depth=(368.78 - 368.04) / A_NOW, closes_below=2, vwap_gap=(370.57 - 372.39) / A_NOW, mom=(370.57 - 374.22) / A_NOW,
             testvol=1.84, trend=(377.81 - 367.22) / A_NOW, tod=13 + 35 / 60, rs_spy=None)
print('today', today); print('n rows', len(rows), 'n60', len(E60))
json.dump(dict(rows=rows, res=res, today=today, n60=len(E60)), open('phase3b.json', 'w'), indent=1, default=str)
