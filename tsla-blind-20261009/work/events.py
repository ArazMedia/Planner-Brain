"""Intraday tested-support wick-and-reclaim event study on PA 5m bars (HISTORY only).
All level definitions use ONLY daily data strictly before the event day. Leak guard: CUT = 2026-10-08 13:40 ET."""
import json, math, datetime as dt
from zoneinfo import ZoneInfo
Z = ZoneInfo('America/New_York')
CUT = dt.datetime(2026, 10, 8, 13, 40, tzinfo=Z).timestamp()
f = lambda t: dt.datetime.fromtimestamp(t, Z)

def load5(path, cut=True, sec=300):
    B = json.load(open(path))
    B = [[b[0] / 1000 if b[0] > 1e12 else b[0]] + list(b[1:6]) for b in B]
    if cut: B = [b for b in B if b[0] + sec <= CUT]
    return B

def rth_days(B5, sec=300):
    days = {}
    for b in B5:
        t = f(b[0]); tt = t.time()
        if dt.time(9, 30) <= tt and (t + dt.timedelta(seconds=sec)).time() <= dt.time(16, 0) and tt < dt.time(16,0):
            days.setdefault(t.date(), []).append(b)
    return dict(sorted(days.items()))

def load_daily(path, before=dt.date(2026, 10, 8)):
    B = json.load(open(path))
    out = []
    for b in B:
        d = f(b[0] / 1000 if b[0] > 1e12 else b[0]).date()
        if d < before: out.append(dict(d=d, o=b[1], h=b[2], l=b[3], c=b[4], v=b[5]))
    return out

def atr_at(D, i, n=14):
    tr = [max(D[k]['h'] - D[k]['l'], abs(D[k]['h'] - D[k-1]['c']), abs(D[k]['l'] - D[k-1]['c'])) for k in range(i - n + 1, i + 1)]
    return sum(tr) / n

def levels_before(D, i, look=250, tol=0.003, k=2, min_touch=2):
    """tested levels from daily pivots (k bars each side) in D[i-look:i] (all strictly before day i).
    Returns list of (level, n_pivots, n_touches, last_touch_idx). Level = mean of clustered pivot prices."""
    lo = max(k, i - look); piv = []
    for j in range(lo, i - k):
        w = D[j - k:j + k + 1]
        if D[j]['l'] == min(x['l'] for x in w): piv.append(D[j]['l'])
        if D[j]['h'] == max(x['h'] for x in w): piv.append(D[j]['h'])
    piv.sort(); cl = []
    for p in piv:
        if cl and abs(p / (sum(cl[-1]) / len(cl[-1])) - 1) <= tol: cl[-1].append(p)
        else: cl.append([p])
    out = []
    for c in cl:
        if len(c) < min_touch: continue
        L = sum(c) / len(c)
        touches = sum(1 for j in range(lo, i) if abs(D[j]['l'] / L - 1) <= tol or abs(D[j]['h'] / L - 1) <= tol)
        out.append((L, len(c), touches))
    return out

def find_events(B5, D, sec=300, max_depth_atr=0.4, reclaim_bars=4, last_entry=dt.time(15, 30), first_entry=dt.time(9, 45)):
    days = rth_days(B5, sec); didx = {x['d']: n for n, x in enumerate(D)}
    dlist = list(days.keys()); ev = []
    for di, d in enumerate(dlist):
        if d not in didx: continue
        i = didx[d]
        if i < 30: continue
        A = atr_at(D, i - 1); pc = D[i - 1]['c']
        bars = days[d]
        lv = [x for x in levels_before(D, i) if x[0] < pc and (pc - x[0]) < 3 * A]  # support below prior close
        best = None
        for (L, npiv, ntouch) in lv:
            above = False; k = 0
            while k < len(bars):
                b = bars[k]
                if b[4] > L and not above: above = True
                if above and b[3] < L:
                    # broke: find reclaim close > L within reclaim_bars of the first close below L (or same bar)
                    wick = b[3]; j = k; closes_below = 0; ok = False
                    while j < len(bars):
                        wick = min(wick, bars[j][3])
                        if bars[j][4] > L and (j > k or bars[j][4] > L):
                            ok = True; break
                        closes_below += 1
                        if closes_below > reclaim_bars: break
                        j += 1
                    if ok and (L - wick) <= max_depth_atr * A and (L - wick) > 0.0005 * L:
                        tt = f(bars[j][0]).time()
                        if first_entry <= tt <= last_entry:
                            cand = dict(day=d, di=di, i=i, k_break=k, k_entry=j, L=L, npiv=npiv, ntouch=ntouch, wick=wick,
                                        entry=bars[j][4], t_entry=bars[j][0], atr=A, closes_below=closes_below)
                            if best is None or cand['t_entry'] < best['t_entry']: best = cand
                    break  # one test per level per day
                k += 1
        if best: ev.append(best)
    return ev, days, dlist
