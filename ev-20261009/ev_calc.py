#!/usr/bin/env python3
"""EV evaluation of Dominic's debit-spread setups, Fri 2026-10-09 (Planner / 20261009-ev).
Reproducible: python3 ev_calc.py  -> prints tables, writes ev_table.csv next to this file.

RULES: no yfinance / outside price data. Price history = PA TradingView bar exports on the box.
Option quotes/IV = CBOE delayed chains saved by RA (12:47 ET; IBIT 12:09 ET). Flow/gamma = UW check files
(encoded as factor scores below, with the source line in the comment).

Pipeline per setup (all constants pre-declared here, nothing fitted):
 1. Prior: event study on daily bars. Event = daily close above the prior 20-day high (bull) / below the prior
    20-day low (bear), de-clustered (no new event while one is open, H days). For each event, strikes and the fail
    level are placed at the SAME ATR(14) multiples from the entry close as today's setup. Path: first daily close
    beyond the fail level -> STOP; else at day H (expiry) the close vs the strikes -> TARGET (>= short strike),
    PARTIAL (between strikes), OTM (beyond long strike, no stop hit -> expires ~0).
 2. Shrinkage: Dirichlet/beta prior on the 4 buckets centred on the POOLED rate (same study across all names),
    weight W = 10 if own n < 15 else 5.  p_k = (count_k + W*pool_k)/(n + W).
 3. Factor nudge: logit(p_t) += 0.5*clip(dir_score/2, -1, 1), dir_score = weighted mean of the factors NOT already
    in the prior (volume, trend/regime, positioning). Max |nudge| = 0.5 log-odds. Other buckets rescale.
 4. Market cross-check: lognormal N(d2) with each strike's CBOE IV (r=4%, q=0) at the entry price. If our p_t
    exceeds the market's by > 10pp, it is CUT to market + 10pp (excess moved to the other buckets pro rata).
 5. EV = sum p_k*(V_k - debit). V_target = width*100 - exit cost; V_partial = width*50 - exit cost;
    V_stop = Black-Scholes spread value at the fail level, at the pooled median stop day, minus exit cost;
    V_otm = 0 (let expire). Exit cost = half the bid/ask of each leg (CBOE quotes) x 100.
    Debit = quoted mid (and a worst-case 'full spread' fill shown separately). SPY setups are entered only at the
    trigger, so their debit is re-priced by BS at the trigger, calibrated to the quoted mid.
"""
import json, math, os, csv, datetime as dt, zoneinfo, glob
import numpy as np

Z = zoneinfo.ZoneInfo('America/New_York')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INPUTS = os.path.join(ROOT, 'inputs')
R = 0.04

# ---------------- price history (PA TradingView exports only) ----------------
CK = '/workspace/watchlist/checks'
MR = '/workspace/pa-agent/macro_review/20261008'
SOURCES = {  # name: list of candidate files (daily 'D' or 4h '240'); the longest history wins
    'USO':  [f'{CK}/data_20261008_1119/USO_D.json'],
    'GOOGL': [],
    'GOOG': [f'{MR}/exec/bars240_GOOG.json', f'{MR}/raw/ohlcv_1D_GOOG.json', f'{CK}/data_20261008_1119/GOOG_D.json'],
    'IBIT': [f'{MR}/exec/bars240_IBIT.json', f'{MR}/raw/ohlcv_1D_IBIT.json'],
    'PLTR': [f'{CK}/data_20261009_1210/PLTR_240.json'],
    'SPY':  [f'{MR}/raw/ohlcv_1D_SPY.json', f'{CK}/data_20261009_1210/SPY_240.json'],
    'TSLA': [f'{CK}/data_20261009_tsla/TSLA_D.json'],
    'BTCUSD': [],
    'QQQ':  [f'{CK}/data_20261008_1119/QQQ_D.json', f'{MR}/raw/ohlcv_1D_QQQ.json'],
    'MU':   [f'{CK}/data_20261008_1119/MU_D.json'],
    'AMD':  [f'{MR}/exec/bars240_AMD.json', f'{MR}/raw/ohlcv_1D_AMD.json'],
    'NVDA': [f'{MR}/raw/ohlcv_1D_NVDA.json'],
    'META': [f'{MR}/raw/ohlcv_1D_META.json'],
}
# deeper pulls PA may drop into inputs/pa_data/ (e.g. USO_D.json, PLTR_D.json, PLTR_240.json) are picked up automatically
for f in glob.glob(os.path.join(INPUTS, 'pa_data', '*.json')):
    b = os.path.basename(f).split('_')[0].upper()
    if b in SOURCES: SOURCES[b].insert(0, f)


def load_daily(path):
    d = json.load(open(path))
    if isinstance(d, dict):
        for k in ('bars', 'data', 'candles'):
            if k in d: d = d[k]; break
    rows = [r if isinstance(r, list) else [r.get('time', r.get('t')), r['open'], r['high'], r['low'], r['close'], r.get('volume', 0)] for r in d]
    rows = [[r[0] / 1000 if r[0] > 1e12 else r[0]] + list(r[1:6]) for r in rows]
    hrs = {dt.datetime.fromtimestamp(r[0], Z).hour for r in rows}
    if len(hrs) == 1:  # already daily
        return [dict(d=dt.datetime.fromtimestamp(r[0], Z).date(), o=r[1], h=r[2], l=r[3], c=r[4]) for r in rows]
    # 4h ETH bars (04/08/12/16): daily H/L over 04-16 bars, close = close of the 12:00 bar (= 16:00 RTH close)
    days = {}
    for r in rows:
        t = dt.datetime.fromtimestamp(r[0], Z)
        if t.hour >= 16: continue
        x = days.setdefault(t.date(), dict(d=t.date(), o=r[1], h=r[2], l=r[3], c=None))
        x['h'] = max(x['h'], r[2]); x['l'] = min(x['l'], r[3])
        if t.hour == 12: x['c'] = r[4]
    return [x for x in sorted(days.values(), key=lambda x: x['d']) if x['c'] is not None]


def best_series(name):
    best = None
    for p in SOURCES[name]:
        if not os.path.exists(p): continue
        try: s = load_daily(p)
        except Exception: continue
        if best is None or len(s) > len(best[1]): best = (p, s)
    return best


def atr(s, i, n=14):
    trs = []
    for k in range(i - n + 1, i + 1):
        trs.append(max(s[k]['h'] - s[k]['l'], abs(s[k]['h'] - s[k - 1]['c']), abs(s[k]['l'] - s[k - 1]['c'])))
    return sum(trs) / n


def rv20(s):
    r = [math.log(s[k]['c'] / s[k - 1]['c']) for k in range(len(s) - 20, len(s))]
    m = sum(r) / len(r)
    return math.sqrt(sum((x - m) ** 2 for x in r) / (len(r) - 1) * 252)


def study(s, side, H, d_long, d_short, d_fail, L=20):
    """counts of target/partial/otm/stop for breakout events; distances in ATR multiples from the entry close
    (positive = in the trade direction for strikes, against it for the fail level)."""
    sg = 1 if side == 'bull' else -1
    cnt = dict(t=0, p=0, x=0, s=0); stop_days = []; over = []; last = -10 ** 9; i = max(L, 15)
    while i < len(s) - 1:
        prior = s[i - L:i]
        brk = s[i]['c'] > max(b['h'] for b in prior) if sg > 0 else s[i]['c'] < min(b['l'] for b in prior)
        if brk and i - last > H:
            if i + H >= len(s): break  # unresolved at the end of the data: excluded (stated)
            a = atr(s, i); e = s[i]['c']
            kl, ks, fl = e + sg * d_long * a, e + sg * d_short * a, e - sg * d_fail * a
            out = None
            for j in range(1, H + 1):
                c = s[i + j]['c']
                if sg * (c - fl) < 0: out = 's'; stop_days.append(j); over.append(sg * (fl - c) / a); break
            if out is None:
                c = s[i + H]['c']
                out = 't' if sg * (c - ks) >= 0 else ('p' if sg * (c - kl) > 0 else 'x')
            cnt[out] += 1; last = i
        i += 1
    n = sum(cnt.values())
    return cnt, n, (stop_days, over)


def study_uncond(s, side, H, d_long, d_short, d_fail, step=3):
    """Same path rule, but entering on EVERY `step`-th day (no breakout condition): the drift-only baseline.
    p_t(events) - p_t(uncond) = what the trigger itself adds over the sample's drift."""
    sg = 1 if side == 'bull' else -1
    cnt = dict(t=0, p=0, x=0, s=0)
    for i in range(15, len(s) - H, step):
        a = atr(s, i); e = s[i]['c']
        kl, ks, fl = e + sg * d_long * a, e + sg * d_short * a, e - sg * d_fail * a
        out = None
        for j in range(1, H + 1):
            if sg * (s[i + j]['c'] - fl) < 0: out = 's'; break
        if out is None:
            c = s[i + H]['c']
            out = 't' if sg * (c - ks) >= 0 else ('p' if sg * (c - kl) > 0 else 'x')
        cnt[out] += 1
    return cnt, sum(cnt.values())


# ---------------- PA event definitions (inputs/pa_data/es.py + run.py), re-scored SETTLE-based ----------------
import sys
sys.path.insert(0, os.path.join(INPUTS, 'pa_data'))
try:
    import es as PAES   # PA's engine: load(), levels_events() (tested 5-bar pivot breakouts, first close through)
except Exception:
    PAES = None


def pa_sma_hold(df):   # copied from pa_data/run.py (BTC/IBIT daily-SMA50 test & hold)
    ev = []; last = -99
    for i in range(205, len(df)):
        r = df.iloc[i]
        if r.l <= r.s50 and r.c > r.s50 and (df.c.iloc[i - 3:i] > df.s50.iloc[i - 3:i]).all() and i - last >= 5:
            ev.append(dict(i=i, lev=r.c)); last = i
    return ev


def pa_b20(df):        # copied from pa_data/run.py (TSLA close above the prior 20-day high)
    out = []; last = -99
    for i in range(21, len(df)):
        if df.c.iloc[i] > df.h.iloc[i - 20:i].max() and df.c.iloc[i - 1] <= df.h.iloc[i - 21:i - 1].max() and i - last >= 5:
            out.append(dict(i=i, lev=df.c.iloc[i])); last = i
    return out


def pa_settle(st):
    """Own-name sample = PA's event set for this setup. Distances are PA-style % from the level (or from the event
    close for IBIT/TSLA, as PA measured them). Path: any daily CLOSE through the fail -> STOP (this is PA's 'stop any',
    i.e. whipsaw-inclusive, not 'stop first'). Else the CLOSE at the horizon vs the strikes -> TARGET/PARTIAL/OTM.
    Touch rates are NOT used."""
    if PAES is None: return None
    pm = st['pa']; sg = 1 if st['side'] == 'bull' else -1
    df = PAES.load(pm['sym'])
    if pm['kind'] == 'level': E = PAES.levels_events(df, 'up' if sg > 0 else 'down')
    elif pm['kind'] == 'sma_hold': E = pa_sma_hold(df)
    else: E = pa_b20(df)
    ref = pm['ref']
    # strikes are placed relative to the EVENT CLOSE (= where we would actually buy; entry ref = st['entry']);
    # the fail level is relative to the LEVEL (it is a level-defined stop). Prevents events that closed far above the
    # level (PA allows up to +3%) from starting already in the money.
    rl, rs, rf = st['long'][0] / st['entry'] - 1, st['short'][0] / st['entry'] - 1, st['fail'] / ref - 1
    C = df.c.values; H = pm.get('H', st['H'])
    cnt = dict(t=0, p=0, x=0, s=0); dates = []
    for e in E:
        i = e['i']
        if i + H > len(df) - 1: continue
        L = e['lev']
        kl, ks, fl = C[i] * (1 + rl), C[i] * (1 + rs), L * (1 + rf)
        out = None
        for j in range(i + 1, i + H + 1):
            if sg * (C[j] - fl) < 0: out = 's'; break
        if out is None:
            c = C[i + H]
            out = 't' if sg * (c - ks) >= 0 else ('p' if sg * (c - kl) > 0 else 'x')
        cnt[out] += 1; dates.append(str(df.d[i]))
    return cnt, sum(cnt.values()), (dates[0] if dates else '', dates[-1] if dates else '')


# ---------------- options math ----------------
def ncdf(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def bs(S, K, T, iv, cp):
    if T <= 0: return max(0.0, (S - K) if cp == 'C' else (K - S))
    d1 = (math.log(S / K) + (R + iv * iv / 2) * T) / (iv * math.sqrt(T)); d2 = d1 - iv * math.sqrt(T)
    if cp == 'C': return S * ncdf(d1) - K * math.exp(-R * T) * ncdf(d2)
    return K * math.exp(-R * T) * ncdf(-d2) - S * ncdf(-d1)


def p_beyond(S, K, T, iv, cp):  # risk-neutral P(S_T > K) for calls, P(S_T < K) for puts
    d2 = (math.log(S / K) + (R - iv * iv / 2) * T) / (iv * math.sqrt(T))
    return ncdf(d2) if cp == 'C' else ncdf(-d2)


# ---------------- setups (numbers verified against the check files; see EV.md section 1) ----------------
# legs: (strike, bid, ask, iv, delta, OI) from CBOE chain 12:47 ET (IBIT 12:09 ET). Expiry close 16:00 ET.
TODAY = dt.datetime(2026, 10, 9, 13, 0, tzinfo=Z)
GOOGL_MINUS_GOOG = 354.11 - 350.435  # +3.675 in the CBOE snapshot; reference only. GOOGL levels now come from PA_baserates.md
# (native GOOGL: trigger 353.22 = GOOGL high on 10-01 when GOOG made 350.09; fail 341.38 by ratio). All GOOGL math uses GOOGL prices.
SETUPS = [
    dict(id='USO 150/155C', name='USO', hist='USO', side='bull', cp='C', exp='2026-11-20', H=30, spot=148.0499,
         entry=148.07, fail=147.12, quoted_debit=192.50, pa=dict(sym='USO', kind='level', ref=148.07), trig_fired='pending (daily close >148.07 today; 4h 08-12 C148.79)',
         long=(150, 8.10, 8.50, .4507, .5022, 5740), short=(155, 6.25, 6.50, .4545, .4192, 1490),
         trigger='daily close >148.07 (fail: daily close <147.12)'),
    dict(id='USO 150/160C', name='USO', hist='USO', side='bull', cp='C', exp='2026-11-20', H=30, spot=148.0499,
         entry=148.07, fail=147.12, quoted_debit=337.50, pa=dict(sym='USO', kind='level', ref=148.07), trig_fired='pending (daily close >148.07 today)',
         long=(150, 8.10, 8.50, .4507, .5022, 5740), short=(160, 4.85, 5.00, .4628, .3449, 2699),
         trigger='daily close >148.07 (fail: daily close <147.12)'),
    dict(id='GOOGL 355/365C', name='GOOGL', hist='GOOGL', side='bull', cp='C', exp='2026-11-20', H=30, spot=354.11,
         entry=354.11, fail=341.38, quoted_debit=437.50, pa=dict(sym='GOOGL', kind='level', ref=353.22),
         trig_fired='pending (GOOGL daily close >353.22; above it intraday ~354.2; GOOG 4h 08-12 C349.55 missed)',
         long=(355, 17.00, 17.15, .3461, .5328, 31092), short=(365, 12.55, 12.85, .3463, .4392, 2946),
         trigger='GOOGL daily close >353.22 (PA native; = GOOG 350.09); fail GOOGL close <341.38; ER + FOMC 10/28 inside'),
    dict(id='GOOGL 360/370C', name='GOOGL', hist='GOOGL', side='bull', cp='C', exp='2026-11-20', H=30, spot=354.11,
         entry=354.11, fail=341.38, quoted_debit=392.50, pa=dict(sym='GOOGL', kind='level', ref=353.22),
         trig_fired='pending (GOOGL daily close >353.22; above it intraday ~354.2)',
         long=(360, 14.60, 14.90, .3460, .4854, 11499), short=(370, 10.70, 10.95, .3456, .3944, 34302),
         trigger='GOOGL daily close >353.22 (PA native; = GOOG 350.09); fail GOOGL close <341.38; ER + FOMC 10/28 inside'),
    dict(id='PLTR 205/210C', name='PLTR', hist='PLTR', side='bull', cp='C', exp='2026-10-16', H=5, spot=205.94,
         entry=205.94, fail=204.42, quoted_debit=220.00, pa=dict(sym='PLTR', kind='level', ref=204.42), trig_fired='fired intraday (broke 204.42, 4h C205.45 at 3.70x); retest-hold pending',
         long=(205, 5.20, 5.35, .4134, .5456, 8003), short=(210, 3.05, 3.10, .4129, .3826, 11407),
         trigger='hold >204.4 (fail: 4h close <204.42; modelled as daily close); target 207.5-210'),
    dict(id='SPY 778/781C', name='SPY', hist='SPY', side='bull', cp='C', exp='2026-10-16', H=5, spot=778.11,
         entry=779.27, fail=774.90, quoted_debit=152.00, pa=dict(sym='SPY', kind='level', ref=779.27),
         ra_prior=dict(t=.60, p=.10, l=.30, be=779.54), trig_fired='not fired (needs a DAILY close >779.27; 777.87 at 12:21, 778.29 PA ~13:00)',
         long=(778, 4.52, 4.54, .0972, .5232, 6334), short=(781, 3.00, 3.02, .0941, .4089, 9780),
         trigger='DAILY close >779.27 (RA v2: a 4h/intraday poke is not enough; PA: >1x vol) (fail: close <774.90); CPI 10/14 inside'),
    dict(id='SPY 775/767P', name='SPY', hist='SPY', side='bear', cp='P', exp='2026-10-16', H=5, spot=778.11,
         entry=774.90, fail=779.27, quoted_debit=170.50, pa=dict(sym='SPY', kind='level', ref=774.90), hard=True,
         ra_prior=dict(t=.20, p=.15, l=.65, be=773.28), trig_fired='not fired (needs a DAILY close <774.90)',
         long=(775, 2.85, 2.87, .1010, -.3786, 8689), short=(767, 1.15, 1.16, .1134, -.1755, 9826),
         trigger='DAILY close <774.90 (RA v2) (fail: close >779.27, PA def); CPI 10/14 inside'),
    dict(id='IBIT 46/49C', name='IBIT', hist='IBIT', side='bull', cp='C', exp='2026-11-20', H=30, spot=46.82,
         entry=46.82, fail=round(46.82 * (1 - 0.0275), 2), quoted_debit=138.00, pa=dict(sym='BTCUSD', kind='sma_hold', ref=46.82, H=42), hard=True, trig_fired='entry trigger not fired (15m close >47.16 on vol); RA 12:09 lists the trade as CANCELLED',
         long=(46, 2.91, 2.93, .3731, .5974, 22023), short=(49, 1.54, 1.56, .3678, .4003, 26057),
         trigger='15m close >47.16 w/ BTC >82,714 (stop: close -2.75% = IBIT ~45.53 / BTC 80,526, PA def; setup-invalid 46.25)'),
    dict(id='PLTR Nov20 200/210C', name='PLTR', hist='PLTR', side='bull', cp='C', exp='2026-11-20', H=30, spot=205.94,
         entry=205.94, fail=204.42, quoted_debit=490.00, pa=dict(sym='PLTR', kind='level', ref=204.42), trig_fired='fired intraday (broke 204.42, 4h C205.45 at 3.70x); retest-hold pending',
         long=(200, 18.65, 18.80, .5480, .6085, 12744), short=(210, 13.75, 13.90, .5446, .5060, 7776),
         trigger='hold >204.4 (fail: 4h close <204.42, modelled as daily close); PLTR ER (Nov 2 or 9) INSIDE expiry'),
    dict(id='TSLA 385/390C', name='TSLA', hist='TSLA', side='bull', cp='C', exp='2026-10-16', H=5, spot=382.795,
         entry=386.82, fail=381.0, quoted_debit=195.00, reprice=True, pa=dict(sym='TSLA', kind='b20', ref=386.82), hard=True,
         trig_fired='not fired (15m close >386.82 holding VWAP; PA 12:10: confirmation failed, 383.94 under VWAP)',
         long=(385, 7.15, 7.25, .3794, .4730, 10137), short=(390, 5.20, 5.30, .3828, .3797, 10316),
         trigger='15m close >386.82 holding VWAP (fail: 15m close <381, hard 1h <380); RA spread, skip if full > ~$260; CPI inside, ER 10/21 after expiry'),
]
# sensitivity variants (not ranked): USO with PA's floor-warning 141.76 as the stop instead of 147.12
SENS = [dict(SETUPS[0], id='USO 150/155C [sens: fail 141.76]', fail=141.76),
        dict(SETUPS[1], id='USO 150/160C [sens: fail 141.76]', fail=141.76)]

# ---------------- factor scores (-2..+2), provisional Planner scores pending RA_factors.md ----------------
# keys: struct, vol, trend, gamma, flow, cat, liq.   (iv is computed: IV/RV20 rule below)
F = {
 'USO':   dict(struct=1, vol=0, trend=1, gamma=0, flow=0, cat=-1, liq=-1),
 # struct: narrowing range on support, 4h close 148.79 above 147.12/148.07 (1210-pa); vol 1.05x 4h, 0.65x open;
 # trend: 4h > SMA50 147.30, oil supportive (Hormuz escalation, Isaias shut-ins; 1209-ra); gamma: no UW GEX for USO (n/a=0);
 # flow: net +$0.96M quiet, 150C 10/16 traded both ways, 'no fresh bullish conviction' (1210-uw, WATCHLIST);
 # cat: EIA 10/15 + Iran reply 'within days' both inside -> two-way headline risk; liq: 150C $0.40 wide, 155C OI 1,490.
 'GOOGL': dict(struct=1, vol=0, trend=0, gamma=-1, flow=0, cat=-1, liq=1),
 # struct: 200DMA/trendline bounce, but 4h close 349.55 missed 350.09 and falling line ~353.33 overhead (GOOG);
 # vol: 1.59x 4h bar but bounce volume average / push on falling volume; trend: above 4h SMA200, QQQ weak (<751.75);
 # gamma: CW 355/357.5 at the long strike, +gamma 350-357.5 = pin (1210-uw); flow: GOOG +$11.8M vs GOOGL 345C Feb sold
 # $7.23M at bid, call premium fading since late Sep (WATCHLIST) -> net 0; cat: ER 10/28 inside (last -7%/+10%);
 # liq: 355C 31k OI 15c wide; 360/370 11.5k/34k.
 'PLTR':  dict(struct=1.5, vol=2, trend=1.5, gamma=0.5, flow=1, cat=-0.5, liq=2),
 # struct: broke 204.42 to a 300-bar high; vol 3.70x 4h bar closing near high (1210-pa); gamma: 205 magnet, CW 210 =
 # short strike (good for 205/210), but Live 'Amplifying' with -13.8M at 202.5 = fast drop if 204.4 fails (1216-gamma);
 # flow: net +$21.25M, 205C 19k/207.5C 15k vol (largest prints are deep-ITM/0DTE, discounted); cat: CPI 10/14 only.
 'SPY_bull': dict(struct=0, vol=0, trend=0.5, gamma=0, flow=0, cat=-1, liq=2),
 # struct: zone top 779.27 with 781.62 (10-06 high) 2.3 pts above -> stall zone; vol: 08-12 0.92x inside bar;
 # gamma: -gamma pocket 778-780 helps reach 780, but 780 magnet/call wall pins below the 781 short strike;
 # flow: net +$7.42M but puts -$8.6M, 765P 10/30 $3.43M sweep -> 0; cat: CPI 10/14 08:30 inside the Oct 16 expiry.
 'SPY_bear': dict(struct=-1, vol=0, trend=-1, gamma=-0.5, flow=0, cat=-1, liq=2),
 # struct: 774.90 under a +1.52B put wall at 777 and +gamma 775-777 ('774.90 should hold'); counter-trend;
 # gamma: support to break first, accel only at 767 (= short strike).
 'TSLA':  dict(struct=0.5, vol=0.5, trend=0.5, gamma=0.5, flow=1.5, cat=-0.5, liq=2),
 # struct: falling-line breakout, retest held 381.14, 370.25 spring 10/8; but 386.82/388.55 confirmation failed, lower highs
 # (1210-pa); vol: 3.45x 4h bar but long upper wick (C383.40 vs H388.55; RA_tsla); trend: above 370.25 role-reversal;
 # gamma: on the flip 382.1, -gamma 382.5-387.5 can accelerate, CW 390 (Live) = short strike (1210-uw);
 # flow: net +$31.4M, 385C 11/13 opening at ask $2.5M, 400C Jan27 ask $2.64M (deep-ITM rolls discounted);
 # cat: CPI 10/14 inside, ER 10/21 AFTER the Oct 16 expiry; liq: 10c wide, 10k OI.
 'IBIT':  dict(struct=0.5, vol=0, trend=0.5, gamma=0, flow=-1.5, cat=-0.5, liq=2),
 # struct: BTC reclaimed 4h SMA200 (trap confirmed) but IBIT fading at VWAP; vol: 0.81x breakout bar, 1.30x 08-12;
 # flow: no opening call buying, Nov27 49.5C/52.5C sold opening at bid ($1.15M) above spot (1210-uw); gamma n/a.
}
FKEY = {'USO 150/155C': 'USO', 'USO 150/160C': 'USO', 'GOOGL 355/365C': 'GOOGL', 'GOOGL 360/370C': 'GOOGL',
        'PLTR 205/210C': 'PLTR', 'PLTR Nov20 200/210C': 'PLTR', 'TSLA 385/390C': 'TSLA', 'SPY 778/781C': 'SPY_bull', 'SPY 775/767P': 'SPY_bear', 'IBIT 46/49C': 'IBIT'}
# weights (provisional; RA_factors.md overrides when present). gamma+flow are merged into ONE 'positioning'
# factor = mean(gamma, flow) with weight 1.0, so the same dealer/customer positioning is not counted twice.
W = dict(struct=1.0, vol=0.75, trend=1.0, pos=1.0, cat=0.75, iv=0.5, liq=0.5)
DIR_KEYS = ('vol', 'trend', 'pos')   # only these move p (struct is the prior's trigger type; cat/iv/liq act via variance/cost)


# RA_factors.csv (RA = lead; per-setup weights summing to 100) overrides the provisional Planner scores above.
RA_MAP = {'USO 150/155C': 'USO Nov20 150/155C', 'USO 150/160C': 'USO Nov20 150/160C', 'GOOGL 355/365C': 'GOOGL Nov20 355/365C',
          'GOOGL 360/370C': 'GOOGL Nov20 360/370C', 'PLTR 205/210C': 'PLTR Oct16 205/210C', 'PLTR Nov20 200/210C': 'PLTR Nov20 200/210C', 'SPY 778/781C': 'SPY bull Oct16 778/781C',
          'SPY 775/767P': 'SPY bear Oct16 775/767P', 'IBIT 46/49C': 'BTC/IBIT Nov20 46/49C', 'TSLA 385/390C': 'TSLA Oct16 385/390C (cond.)'}


def load_ra():
    f = os.path.join(INPUTS, 'RA_factors.csv')
    if not os.path.exists(f): return {}
    out = {}
    for r in csv.DictReader(open(f)):
        out[r['setup']] = {k[2:]: float(v) for k, v in r.items() if k.startswith(('w_', 's_'))} | \
            {'w': {k[2:]: float(v) for k, v in r.items() if k.startswith('w_')}, 's': {k[2:]: float(v) for k, v in r.items() if k.startswith('s_')}}
    return out


RA = load_ra()


# UW_flowhist.md tags (positioning judgement by the flow owner). RA's scores ALREADY contain flow + gamma, so these are
# NOT added on top; they are used only as a REPLACEMENT sensitivity for the merged positioning term (EV_UWpos).
UW_TAG = {'USO': -1, 'GOOGL': 0, 'PLTR': 0, 'SPY_bull': 1, 'SPY_bear': 0, 'IBIT': 0, 'TSLA': 0}


def iv_score(ratio):
    return 1 if ratio < 0.9 else 0 if ratio <= 1.2 else -1 if ratio <= 1.5 else -2


def grade(x):
    return 'A' if x >= 1.2 else 'B' if x >= 0.6 else 'C' if x >= 0 else 'D' if x >= -0.6 else 'F'


def clip(x, a, b): return max(a, min(b, x))


def mc_market(st, T, H, e, n=100_000, seed=7):
    """Risk-neutral benchmark: GBM at the CBOE IV (mean of the two legs), daily closes, SAME stop rule as ours.
    Returns bucket probabilities, mean partial intrinsic, mean stop residual (BS at the stop close), and the
    market EV of the strategy before costs (should be ~0 if the debit is fair)."""
    rng = np.random.default_rng(seed)
    sg = 1 if st['side'] == 'bull' else -1
    kl, ks = st['long'][0], st['short'][0]; ivl, ivs = st['long'][3], st['short'][3]
    iv = (ivl + ivs) / 2; dtau = T / H
    z = rng.standard_normal((n, H))
    paths = e * np.exp(np.cumsum((R - iv * iv / 2) * dtau + iv * math.sqrt(dtau) * z, axis=1))
    beyond = sg * (paths - st['fail']) < 0
    hit = beyond.any(axis=1); first = np.where(hit, beyond.argmax(axis=1), -1)
    ST = paths[:, -1]
    intr = np.clip(sg * (ST - kl), 0, abs(ks - kl))
    t_mask = (~hit) & (sg * (ST - ks) >= 0)
    p_mask = (~hit) & (sg * (ST - kl) > 0) & ~t_mask
    x_mask = (~hit) & ~t_mask & ~p_mask
    # stop residual: BS spread value at the stop close with the remaining time
    resid = np.zeros(n)
    idx = np.where(hit)[0]
    for k in idx[:20000]:  # cap for speed; mean is stable
        j = first[k]; S = paths[k, j]; Tr = max(T - (j + 1) * dtau, 0)
        resid[k] = bs(S, kl, Tr, ivl, st['cp']) - bs(S, ks, Tr, ivs, st['cp'])
    res_mean = resid[idx[:20000]].mean() if len(idx) else 0.0
    pt, pp, px, ps = t_mask.mean(), p_mask.mean(), x_mask.mean(), hit.mean()
    part_mean = intr[p_mask].mean() if p_mask.any() else abs(ks - kl) / 2
    disc = math.exp(-R * T)
    ev_gross = 100 * (disc * (pt * abs(ks - kl) + pp * part_mean) + ps * res_mean)
    return dict(t=pt, p=pp, x=px, s=ps, part=part_mean, resid=res_mean, gross=ev_gross)


def evaluate(st, series):
    name = st['hist']; src, s = series[name]
    a_now = atr(s, len(s) - 1)
    kl, ks = st['long'][0], st['short'][0]
    sg = 1 if st['side'] == 'bull' else -1
    e = st['entry']; H = st['H']
    d_long, d_short, d_fail = sg * (kl - e) / a_now, sg * (ks - e) / a_now, sg * (e - st['fail']) / a_now
    own, n_own, (sd_own, ov_own) = study(s, st['side'], H, d_long, d_short, d_fail)
    own_src = 'Planner 20d-breakout study'
    if st.get('pa'):
        r_pa = pa_settle(st)
        if r_pa and r_pa[1] > 0:
            own, n_own, _span = r_pa; own_src = f"PA event def ({st['pa']['kind']}), settle-based, {_span[0]}..{_span[1]}"

    pool = dict(t=0, p=0, x=0, s=0); n_pool = 0; sd_pool = []; ov_pool = []
    for k, v in series.items():
        if v is None or k == 'BTCUSD' or k == 'GOOG' and name == 'GOOGL' or k == 'GOOGL' and name == 'GOOG': continue  # no twin double count
        c, n, (sd, ov) = study(v[1], st['side'], H, d_long, d_short, d_fail)
        for b in pool: pool[b] += c[b]
        n_pool += n; sd_pool += sd; ov_pool += ov
    pool_p = {b: pool[b] / n_pool for b in pool}
    ut = un = 0
    for k, v in series.items():
        if v is None or k == 'BTCUSD' or k == 'GOOG' and name == 'GOOGL' or k == 'GOOGL' and name == 'GOOG': continue
        c, n = study_uncond(v[1], st['side'], H, d_long, d_short, d_fail)
        ut += c['t']; un += n
    uncond_t = ut / un if un else float('nan')
    c_o, n_o = study_uncond(s, st['side'], H, d_long, d_short, d_fail)
    own_uncond_t = c_o['t'] / n_o if n_o else float('nan')
    Wt = 20 if st.get('hard') else (10 if n_own < 15 else 5)   # PA-flagged rows (IBIT, SPY bear, TSLA) shrink hard
    p = {b: (own[b] + Wt * pool_p[b]) / (n_own + Wt) for b in pool}
    prior = dict(p)
    fk = FKEY[st['id'].split(' [')[0]]
    fs = dict(F[fk])
    T = ((dt.datetime.fromisoformat(st['exp']).replace(hour=16, tzinfo=Z) - TODAY).total_seconds()) / (365 * 86400)
    rv = rv20(s); ivl = st['long'][3]
    fs['iv'] = iv_score(ivl / rv)
    fs['pos'] = (fs['gamma'] + fs['flow']) / 2
    score = sum(W[k] * fs[k] for k in W) / sum(W.values())
    dir_score = sum(W[k] * fs[k] for k in DIR_KEYS) / sum(W[k] for k in DIR_KEYS)
    dir_A = dir_score
    factor_src = 'Planner provisional'
    ra = RA.get(RA_MAP.get(st['id'].split(' [')[0], ''), None)
    if ra:
        w, sc = ra['w'], ra['s']
        fs = dict(struct=sc['structure'], vol=sc['volume'], trend=sc['trend'], gamma=sc['gamma'], flow=sc['flow'],
                  cat=sc['catalyst'], iv=sc['iv'], liq=sc['liquidity'])
        fs['pos'] = (w['gamma'] * sc['gamma'] + w['flow'] * sc['flow']) / max(w['gamma'] + w['flow'], 1e-9)
        score = sum(w[k] * sc[k] for k in w) / 100.0
        # direction nudge: volume, trend, and ONE positioning term (gamma+flow merged, weight = the larger of the two)
        wp = max(w['gamma'], w['flow'])
        dir_score = (w['volume'] * sc['volume'] + w['trend'] * sc['trend'] + wp * fs['pos']) / (w['volume'] + w['trend'] + wp)
        # CRITIC FIX (self-critique pass): the history prior already carries the sample's trend/drift, so for the
        # history-based EV (A) the trend factor is NOT nudged again; it stays in the drift-neutral EV (B).
        dir_A = (w['volume'] * sc['volume'] + wp * fs['pos']) / (w['volume'] + wp)
        factor_src = 'RA_factors.csv'
    fs['iv_rv_rule'] = iv_score(ivl / rv)
    if ra:
        dir_uw = (w['volume'] * sc['volume'] + wp * UW_TAG[fk]) / (w['volume'] + wp)
    else:
        dir_uw = dir_score
    nudge_uw = 0.5 * clip(dir_uw / 2, -1, 1)
    nudge_B = 0.5 * clip(dir_score / 2, -1, 1)
    nudge = 0.5 * clip((dir_A if ra else dir_score) / 2, -1, 1)
    pt_new = 1 / (1 + math.exp(-(math.log(p['t'] / (1 - p['t'])) + nudge)))
    rest = 1 - p['t']
    for b in ('p', 'x', 's'): p[b] = p[b] / rest * (1 - pt_new)
    p['t'] = pt_new
    nudged = dict(p)
    # market benchmarks
    nd2_t = p_beyond(e, ks, T, st['short'][3], st['cp'])
    mc = mc_market(st, T, H, e)
    capped = False
    if p['t'] > mc['t'] + 0.10:
        new = mc['t'] + 0.10; rest = 1 - p['t']
        for b in ('p', 'x', 's'): p[b] = p[b] / rest * (1 - new)
        p['t'] = new; capped = True
    width = abs(ks - kl)
    hs = 100 * ((st['long'][2] - st['long'][1]) / 2 + (st['short'][2] - st['short'][1]) / 2)
    mid_now = (st['long'][1] + st['long'][2]) / 2 - (st['short'][1] + st['short'][2]) / 2
    full_now = st['long'][2] - st['short'][1]
    if st.get('reprice') or (name == 'SPY' and abs(e - st['spot']) > 1e-6):
        calib = mid_now / (bs(st['spot'], kl, T, st['long'][3], st['cp']) - bs(st['spot'], ks, T, st['short'][3], st['cp']))
        debit = 100 * calib * (bs(e, kl, T, st['long'][3], st['cp']) - bs(e, ks, T, st['short'][3], st['cp']))
    else:
        debit = 100 * mid_now   # ONE snapshot for every debit: CBOE data/1247 (quotes ~12:32 ET; IBIT/TSLA ~12:38 ET)
    debit_full = debit + 100 * (full_now - mid_now)
    med_stop = sorted(sd_pool)[len(sd_pool) // 2] if sd_pool else max(1, H // 3)
    over = float(np.mean(ov_pool)) if ov_pool else 0.0
    T_stop = max(T - med_stop * T / H, 0)
    S_stop = st['fail'] - sg * over * a_now
    resid = 100 * (bs(S_stop, kl, T_stop, st['long'][3], st['cp']) - bs(S_stop, ks, T_stop, st['short'][3], st['cp']))
    V = dict(t=width * 100 - hs, p=100 * mc['part'] - hs, s=max(resid - hs, 0), x=0.0)

    def ev_at(pt, D=debit):
        others = {b: p[b] for b in ('p', 'x', 's')}; tot = sum(others.values())
        return pt * (V['t'] - D) + sum((1 - pt) * others[b] / tot * (V[b] - D) for b in others)
    ev = ev_at(p['t']); o_bar = ev_at(0.0)
    # UW-positioning replacement sensitivity: same prior, nudge with UW's tag instead of RA's gamma/flow, same cap
    pu = 1 / (1 + math.exp(-(math.log(prior['t'] / (1 - prior['t'])) + nudge_uw)))
    pu = min(pu, mc['t'] + 0.10)
    ev_uw = ev_at(pu)
    # exit-cost sensitivity: full bid/ask per leg on exit (2x the base assumption)
    V2 = dict(V); V2['t'] -= hs; V2['p'] -= hs; V2['s'] = max(V2['s'] - hs, 0)
    others_ = {b: p[b] for b in ('p', 'x', 's')}
    ev_exit2x = sum(p[k] * (V2[k] - debit) for k in p)
    be = -o_bar / ((V['t'] - debit) - o_bar)
    band = 0.15 if st['name'] == 'GOOGL' else 0.10   # GOOGL: ER 10/28 not isolated in the base rate -> wider band
    ev_lo, ev_hi = ev_at(max(p['t'] - band, 0)), ev_at(min(p['t'] + band, 1))
    ev_full = ev_at(p['t'], debit_full)
    ev_mkt = mc['gross'] - debit - 100 * 0 - (mc['t'] + mc['p'] + mc['s']) * hs  # market-measure EV, same exit costs
    # (B) drift-neutral estimate: start from the market (risk-neutral, same stop rule), add the measured trigger lift
    # and the same factor nudge. This strips the 2020-26 sample drift / hindsight name selection out of the prior.
    lift = pool_p['t'] - uncond_t
    qb = dict(t=mc['t'], p=mc['p'], x=mc['x'], s=mc['s'])
    tb = clip(qb['t'] + lift, 0.001, 0.999)
    tb = 1 / (1 + math.exp(-(math.log(tb / (1 - tb)) + nudge_B)))
    rb = 1 - qb['t']
    for b in ('p', 'x', 's'): qb[b] = qb[b] / rb * (1 - tb)
    qb['t'] = tb
    ev_b = sum(qb[k] * (V[k] - debit) for k in qb)
    # (C) RA's settle-based prior (SPY only, RA_spy_baserates v2): buckets are settle regions, valued by the
    # lognormal mean intrinsic inside each region (MC at entry, no stop), exit costs on non-zero buckets.
    ev_ra = ev_ra_cap = None; ra_t_cap = None
    if st.get('ra_prior'):
        rp = st['ra_prior']; rng = np.random.default_rng(11)
        iv = (st['long'][3] + st['short'][3]) / 2
        ST = e * np.exp((R - iv * iv / 2) * T + iv * math.sqrt(T) * rng.standard_normal(200_000))
        intr = np.clip(sg * (ST - kl), 0, width) * 100
        tm = sg * (ST - ks) >= 0; pmk = (~tm) & (sg * (ST - rp['be']) >= 0); lm = ~(tm | pmk)
        vt, vp, vl = width * 100 - hs, intr[pmk].mean() - hs, max(intr[lm].mean() - hs * (intr[lm] > 0).mean(), 0)
        mk_settle_t = tm.mean()
        ev_ra = rp['t'] * (vt - debit) + rp['p'] * (vp - debit) + rp['l'] * (vl - debit)
        ra_t_cap = min(rp['t'], mk_settle_t + 0.10)
        sc_ = (1 - ra_t_cap) / (rp['p'] + rp['l'])
        ev_ra_cap = ra_t_cap * (vt - debit) + rp['p'] * sc_ * (vp - debit) + rp['l'] * sc_ * (vl - debit)
    fired = st['trig_fired'].startswith('fired')
    # pre-declared: |EV| < 3% of the debit is noise (= 0). TAKE also needs the drift-neutral EV (B) > 0.
    noise = 0.03 * debit
    if ev_lo > 0 and ev_b > 0 and grade(score) in ('A', 'B') and fired: verdict = 'TAKE'
    elif ev > noise and grade(score) in ('A', 'B', 'C'): verdict = 'WATCH'   # D/F = SKIP: flat beats weak evidence
    else: verdict = 'SKIP'
    verdict_brief = verdict
    # CRITIC FIX: a WATCH whose drift-neutral EV is negative rests only on sample drift -> SKIP
    if verdict == 'WATCH' and ev_b < 0: verdict = 'SKIP'
    if 'CANCELLED' in st['trig_fired'] and verdict != 'SKIP': verdict += ' (RA cancelled)'
    if '[sens' in st['id']: verdict = 'sensitivity: ' + verdict; verdict_brief = 'sensitivity: ' + verdict_brief
    return dict(setup=st['id'], grade=grade(score), factor_score=round(score, 2), dir_score=round(dir_score, 2),
        nudge_logodds=round(nudge, 3), nudge_B=round(nudge_B, 3), dir_A=round(dir_A, 2), own_src=own_src, sens_band_pp=int(round(band * 100)), n_own=n_own, n_pool=n_pool, shrink_W=Wt,
        own_t=own['t'], own_p=own['p'], own_x=own['x'], own_s=own['s'],
        own_uncond_t=round(own_uncond_t, 3), own_lift_pp=round(100 * (own['t'] / max(n_own, 1) - own_uncond_t), 1),
        uncond_pool_t=round(uncond_t, 3), n_uncond=un, trigger_lift_pp=round(100 * (pool_p['t'] - uncond_t), 1),
        pool_t=round(pool_p['t'], 3), pool_p=round(pool_p['p'], 3), pool_x=round(pool_p['x'], 3), pool_s=round(pool_p['s'], 3),
        prior_t=round(prior['t'], 3), prior_p=round(prior['p'], 3), prior_x=round(prior['x'], 3), prior_s=round(prior['s'], 3),
        nudged_t=round(nudged['t'], 3),
        p_t=round(p['t'], 3), p_p=round(p['p'], 3), p_x=round(p['x'], 3), p_s=round(p['s'], 3), p_loss=round(p['x'] + p['s'], 3),
        mkt_nd2_t=round(nd2_t, 3), mkt_t=round(mc['t'], 3), mkt_p=round(mc['p'], 3), mkt_x=round(mc['x'], 3), mkt_s=round(mc['s'], 3),
        delta_short=abs(st['short'][4]), delta_long=abs(st['long'][4]), capped_to_mkt=capped,
        edge_vs_mkt_pp=round(100 * (nudged['t'] - mc['t']), 1),
        debit=round(debit, 2), debit_fullfill=round(debit_full, 2), width=width, exit_cost=round(hs, 2),
        V_t=round(V['t'], 2), V_p=round(V['p'], 2), V_s=round(V['s'], 2), med_stop_day=med_stop, stop_overshoot_atr=round(over, 2),
        EV=round(ev, 2), EV_pct=round(100 * ev / debit, 1), BE_p_t=round(be, 3), EV_pt_minus10=round(ev_lo, 2),
        EV_pt_plus10=round(ev_hi, 2), EV_fullfill=round(ev_full, 2), EV_market_measure=round(ev_mkt, 2),
        EV_RAprior=None if ev_ra is None else round(ev_ra, 2), EV_RAprior_capped=None if ev_ra_cap is None else round(ev_ra_cap, 2),
        RA_pt_capped=ra_t_cap,
        p_t_UWpos=round(pu, 3), EV_UWpos=round(ev_uw, 2), EV_exit2x=round(ev_exit2x, 2), uw_tag=UW_TAG[fk],
        rank_key_minEV=round(min(ev, ev_b), 2), pB_t=round(qb['t'], 3), pB_p=round(qb['p'], 3), pB_s=round(qb['s'], 3), EV_B_driftneutral=round(ev_b, 2),
        atr=round(a_now, 3), d_long_atr=round(d_long, 2), d_short_atr=round(d_short, 2), d_fail_atr=round(d_fail, 2),
        rv20=round(rv, 3), iv_long=ivl, iv_rv=round(ivl / rv, 2), H_days=H, T_years=round(T, 4),
        fs=';'.join(f'{k}={fs[k]:+.2g}' for k in ('struct', 'vol', 'trend', 'gamma', 'flow', 'pos', 'cat', 'iv', 'liq', 'iv_rv_rule')),
        factor_src=factor_src,
        quoted_debit_plan=st['quoted_debit'], snapshot_mid=round(100 * mid_now, 2),
        bucket=('tech+CPI' if st['name'] in ('PLTR', 'TSLA', 'GOOGL') or (st['name'] == 'SPY' and st['side'] == 'bull') else st['name']),
        trigger=st['trigger'], trig_status=st['trig_fired'], verdict=verdict, verdict_brief_rule=verdict_brief, hist_src=os.path.basename(src), hist_days=len(s),
        hist_from=str(s[0]['d']), hist_to=str(s[-1]['d']))


def main(write=True, quiet=False):
    series = {k: best_series(k) for k in SOURCES}
    rows = [evaluate(st, series) for st in SETUPS]
    rows.sort(key=lambda r: -r['rank_key_minEV'])   # conservative ranking: min(EV_A, EV_B)
    sens = [evaluate(st, series) for st in SENS]
    if write:
        with open(os.path.join(HERE, 'ev_table.csv'), 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows + sens)
    if not quiet:
        for r in rows + sens:
            print(f"{r['setup']:34s} {r['grade']} fs={r['factor_score']:+.2f} n={r['n_own']}/{r['n_pool']} own t/p/x/s={r['own_t']}/{r['own_p']}/{r['own_x']}/{r['own_s']} "
                  f"uncond={r['uncond_pool_t']:.2f} lift={r['trigger_lift_pp']:+.0f}pp pool_t={r['pool_t']:.2f} prior_t={r['prior_t']:.2f} nudged={r['nudged_t']:.2f} p_t={r['p_t']:.2f} p_p={r['p_p']:.2f} p_x={r['p_x']:.2f} p_s={r['p_s']:.2f} | mkt t/p/x/s={r['mkt_t']:.2f}/{r['mkt_p']:.2f}/{r['mkt_x']:.2f}/{r['mkt_s']:.2f} nd2={r['mkt_nd2_t']:.2f} cap={r['capped_to_mkt']}")
            print(f"     D={r['debit']:.0f} V=({r['V_t']:.0f},{r['V_p']:.0f},{r['V_s']:.0f}) EV={r['EV']:+.0f} ({r['EV_pct']:+.0f}%) BE={r['BE_p_t']:.2f} "
                  f"[{r['EV_pt_minus10']:+.0f},{r['EV_pt_plus10']:+.0f}] full={r['EV_fullfill']:+.0f} pB_t={r['pB_t']:.2f} EV_B={r['EV_B_driftneutral']:+.0f} mktEV={r['EV_market_measure']:+.0f} {r['verdict']}")
            print('    ', r['fs'], f"ivrv={r['iv_rv']} atr={r['atr']} d(l,s,f)=({r['d_long_atr']},{r['d_short_atr']},{r['d_fail_atr']}) stopday={r['med_stop_day']} over={r['stop_overshoot_atr']} src={r['hist_src']} {r['hist_from']}..{r['hist_to']}")
    return rows, sens


if __name__ == '__main__':
    main()
