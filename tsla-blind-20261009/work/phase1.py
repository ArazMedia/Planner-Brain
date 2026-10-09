import statistics as stt, datetime as dt, json, sys
from fw import *
import fw

def base_rate_table(E, label):
    rows = []
    d375 = (375 - SPOT) / A_NOW; d380 = (380 - SPOT) / A_NOW
    st = dict(n=len(E))
    r0 = [(e['fwd'][0] - e['entry']) / e['atr'] for e in E if e['fwd'][0] is not None]
    r1 = [(e['fwd'][1] - e['entry']) / e['atr'] for e in E if e['fwd'][1] is not None]
    r6 = [(e['fwd'][6] - e['entry']) / e['atr'] for e in E if e['fwd'][6] is not None]
    I = [intraday_stats(e, d375) for e in E]
    I1 = [x['d1'] for x in I if x['d1']]
    I0 = [x['d0'] for x in I if x['d0']]
    dc_stop0 = sum(1 for e in E if e['fwd'][0] is not None and e['fwd'][0] < e['wick'])
    out = dict(label=label, n=len(E), n_d1=len(r1),
               d0_mean=stt.mean(r0), d0_med=stt.median(r0), d0_up=sum(x > 0 for x in r0) / len(r0),
               d1_mean=stt.mean(r1), d1_med=stt.median(r1), d1_up=sum(x > 0 for x in r1) / len(r1),
               d1_ge375=sum(1 for e in E if e['fwd'][1] is not None and e['fwd'][1] >= e['entry'] + d375 * e['atr']) / len(r1),
               d6_mean=stt.mean(r6) if r6 else float('nan'), n_d6=len(r6),
               mfe1_med=stt.median(x['mfe'] for x in I1), mae1_med=stt.median(x['mae'] for x in I1),
               mfe0_med=stt.median(x['mfe'] for x in I0), mae0_med=stt.median(x['mae'] for x in I0),
               t_before_wick=sum(1 for x in I1 if x['first_wickstop'] == 'T') / len(I1),
               t_before_close=sum(1 for x in I1 if x['first_closestop'] == 'T') / len(I1),
               dclose_stop0=dc_stop0 / len(r0))
    return out

def fmt_pct(x): return f"{100*x:.0f}%"

def main(out_path):
    now = dt.datetime.now(Z).strftime('%Y-%m-%d %H:%M ET')
    BR = [base_rate_table(E15, 'TSLA 15m-bar events (Feb 2 - Oct 7 2026)'), base_rate_table(E5, 'TSLA 5m-bar events (Jul 27 - Oct 7 2026)'),
          base_rate_table(ESPY, 'SPY 5m-bar events (pool, Jul 27 - Oct 7)')]
    R = [evaluate(st) for st in STRUCTS]
    fw.CALIB = True; Rc = {r['name']: r for r in (evaluate(st) for st in STRUCTS)}; fw.CALIB = False
    L = []
    P = L.append
    P(f"# Phase 1 (BLIND) — TSLA 370.25 wick-reclaim, as of Thu 2026-10-08 13:40 ET (close of the 13:35 5m bar)")
    P(f"Written {now} by Planner (executor). **Written before outcome viewed:** TSLA_outcome.md and every TSLA bar after 13:35 Oct 8 were NOT opened by any code or read for this section; RA_audit_notes.md and RA_tsla_ivcal_LOOKAHEAD.csv NOT opened.")
    P("")
    P("**Leakage disclosure (read first).** This phase is *mechanically* blind, not *cognitively* blind:")
    P("- The task brief itself states the outcome (Oct 8 close ~375, Oct 9 high 388.55). I could not avoid reading it.")
    P("- The permitted method files (`watchlist/checks/20261009-tsla-pa.md`, `20261009-1020-tsla-ra.md`) narrate the post-13:35 path (13:45 5m close 369.88, VWAP reclaim 15:10, close 375.00, Oct 9 gap to 382.19 and 388.55). I read them for level definitions, so I have seen that path.")
    P("- While inspecting daily-bar formats I printed the last 8 rows of `pa_data/TSLA_1D.json`, which include the Oct 8 and partial Oct 9 daily bars (no new information beyond the brief: close 375, Oct 9 high 388.56).")
    P("- RA's IV level is inverted from Oct 8 EOD last trades (mild IV lookahead; RA's LOW/MID/HIGH brackets used; spreads move ±$0.05-0.30 across them). RA's executor saw the Oct 8 close in a web search (RA disclosure).")
    P("- Mitigation: every number below comes from code that only loads bars ending ≤13:40 Oct 8 (PA HISTORY files, verified byte-identical to a 13:40 cut of the raw export) and daily bars ≤ Oct 7; all rules are copied from `outputs/ev_calc.py` or pre-declared here; factor scores are RA's as-of scores (not mine). No parameter was tuned after seeing results.")
    P("")
    P("## Setup as of 13:40")
    P(f"- Spot 370.57 (13:35 5m close, first close back above 370.25). Wick low 368.04 (13:25). Session VWAP 372.39 (RA). Daily ATR14 (to Oct 7) **{A_NOW:.2f}**; stop distance to the wick = {D_FAIL_NOW:.2f} ATR (2.53 pts).")
    P("- Expiries: **no Oct 10 expiry (Saturday)**; Oct 12 (Mon) weekly used instead; Oct 16 weekly. Prices: RA's Black-Scholes model (MID IV; no real Oct 8 intraday quotes exist), entry at mid, exit pays ½ the assumed bid/ask per leg.")
    P("- Trigger: the brief's trigger (5m reclaim close >370.25) **fired at 13:35**. RA's stricter trigger (15m close >370.25, the 13:30-13:45 bar) was **still pending** at 13:40.")
    P("- Grade (RA as-of, weights 25/15/20/5/5/10/10/10): structure +1, volume 0, trend 0, gamma 0 (n/a), flow 0 (n/a), catalyst 0, IV +1 (1DTE/Oct12) / 0 (Oct16), liquidity +2 → **+0.55 C (1DTE, Oct 12), +0.45 C (Oct 16)**. Direction nudge inputs (volume, merged gamma/flow; trend for EV_B) are all 0 → **nudge = 0 log-odds**.")
    P("- Mechanical check: my level detector (daily 5-bar pivots, clustered ±0.3%, ≥2 pivots, prior days only) independently flags Oct 8 as an event (cluster 368.78, 4 pivots/11 touches; wick 368.04; entry on the 13:25 close), so today's setup is in the same event class as the HISTORY sample.")
    P("")
    P("## Base rates from HISTORY (event = intraday wick through a tested daily-pivot support, reclaim close within ≤2 (15m) / ≤4 (5m) bars, entry at the reclaim close 09:45-15:30, one per day; depth ≤0.4 ATR)")
    P("| Sample | n | Same-day close vs entry: mean / median (ATR), % up | Next-day close: mean / median (ATR), % up | P(next-day close ≥ 375-equiv, +0.4 ATR) | Day-6 close mean (ATR) | MFE / MAE to next-day close, median (ATR) | Target (+0.4 ATR) before wick stop | Target before a close back under the level | Daily close under wick on day 0 |")
    P("|---|---|---|---|---|---|---|---|---|---|")
    for b in BR:
        P(f"| {b['label']} | {b['n']} | {b['d0_mean']:+.2f} / {b['d0_med']:+.2f}, {fmt_pct(b['d0_up'])} | {b['d1_mean']:+.2f} / {b['d1_med']:+.2f}, {fmt_pct(b['d1_up'])} | {fmt_pct(b['d1_ge375'])} | {b['d6_mean']:+.2f} (n={b['n_d6']}) | {b['mfe1_med']:+.2f} / {b['mae1_med']:+.2f} | {fmt_pct(b['t_before_wick'])} | {fmt_pct(b['t_before_close'])} | {fmt_pct(b['dclose_stop0'])} |")
    P("")
    P("Primary own sample = the 15m-bar set (n=29, the only one with n ≥ 15; W=5). Pool = own + SPY 5m events (TSLA is in its own pool, as in ev_calc). Drift baseline = every 3rd 15m bar close on all HISTORY days with the same strikes/stop. **n is small and all events are from one 8-month regime; treat every rate as ±9-18pp (1 s.e.).**")
    P("")
    P("## Framework run (ev_calc rules: daily-close stop at 368.04, shrink, nudge 0, cap at market+10pp, drift-neutral EV_B, TAKE/WATCH/SKIP + WATCH→SKIP if EV_B<0)")
    P("| Structure | Debit mid (full) | Grade | n own: t/p/x/s | Prior p_t | p_t / p_p / p_s (+OTM) | Mkt p_t (same stop) | Capped | V_t / V_p / V_s | EV $ (% debit) | EV @ p_t ±10pp | BE p_t | EV_B drift-neutral | Conservative min | Verdict (BRIEF rule → final) | Rule that drove it |")
    P("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in R:
        o = r['own']; p = r['p']; m = r['mkt']
        P(f"| {r['name']} | ${r['debit']:.0f} (${r['debit_full']:.0f}) | {r['grade']} ({r['score']:+.2f}) | {r['n_own']}: {o['t']}/{o['p']}/{o['x']}/{o['s']} | {r['prior']['t']:.2f} | {p['t']:.2f} / {p['p']:.2f} / {p['s']:.2f} (+{p['x']:.2f}) | {m['t']:.2f} | {'yes' if r['capped'] else 'no'} | {r['V']['t']:.0f} / {r['V']['p']:.0f} / {r['V']['s']:.0f} | {r['ev']:+.0f} ({100*r['ev']/r['debit']:+.0f}%) | {r['ev_lo']:+.0f} / {r['ev_hi']:+.0f} | {r['be']:.2f} | {r['ev_b']:+.0f} | {min(r['ev'], r['ev_b']):+.0f} | {r['verdict_brief']} → **{r['verdict']}** | {r['rule']} |")
    P("")
    P("Long calls: 'target' = settle above break-even, V_t = market-MC mean intrinsic above BE (the framework's bucket valuation; it truncates the tail).")
    P("")
    P("**Market-measure check.** With the framework's flat MC vol (mean of the two leg IVs) the spreads show market EV of " +
      ", ".join(f"{r['name']} {r['ev_mkt']:+.0f}" for r in R if 'Oct9' in r['name'] and '/' in r['name']) +
      ". That is RA's upward call smile (OTM call IV > ATM) making spreads cheap vs flat vol — the same artifact EV.md flagged on SPY bear. Sensitivity with the MC vol calibrated so the market measure prices each debit exactly:")
    P("| Structure | EV (calibrated mkt) | EV ±10pp | EV_B | Verdict |")
    P("|---|---|---|---|---|")
    for r in R:
        c = Rc[r['name']]
        P(f"| {r['name']} | {c['ev']:+.0f} | {c['ev_lo']:+.0f} / {c['ev_hi']:+.0f} | {c['ev_b']:+.0f} | {c['verdict']} |")
    P("")
    # IV bracket sensitivity on the best rows
    P("**IV bracket (RA LOW/HIGH) on the 1DTE spreads:** debits " + "; ".join(
        f"{s.name}: LOW ${Struct(s.exp, s.kl, s.ks, 'LOW').debit():.0f} / MID ${s.debit():.0f} / HIGH ${Struct(s.exp, s.kl, s.ks, 'HIGH').debit():.0f}" for s in STRUCTS if s.exp == '261009' and s.ks) + ".")
    LOWHIGH = []
    for scn in ('LOW', 'HIGH'):
        for s in STRUCTS:
            if s.exp == '261009' and s.ks:
                r = evaluate(Struct(s.exp, s.kl, s.ks, scn)); LOWHIGH.append(f"{s.name} {scn}: EV {r['ev']:+.0f}, EV_B {r['ev_b']:+.0f}, {r['verdict']}")
    P("- " + "; ".join(LOWHIGH))
    P("")
    # sensitivities on own sample
    s5 = [evaluate(st, own=E5) for st in STRUCTS if st.exp == '261009' and st.ks]
    P("**Own-sample sensitivity (5m-bar events only, n=5, W=10):** " + "; ".join(f"{r['name']} EV {r['ev']:+.0f} / EV_B {r['ev_b']:+.0f} → {r['verdict']}" for r in s5) + ".")
    P("")
    spreads = [r for r in R if '/' in r['name']]
    best = max(spreads, key=lambda r: min(r['ev'], r['ev_b']))
    bestall = max(R, key=lambda r: min(r['ev'], r['ev_b']))
    watch = [r for r in R if r['verdict'] == 'WATCH']
    band_ok = [r['name'] for r in R if r['ev_lo'] > 0]
    P("## As-of flow / gamma / PA cross-checks (scored before the verdict; no lookahead files opened)")
    P("- **UW flow to 13:35 (UW_tsla_asof.md): two-sided → flow 0.** Bearish-leaning: 1DTE 370P bought at the ask $484K (12:53), 1DTE calls sold at the bid above spot (372.5C $453K, 370C $280K, 375C $276K, 367.5C $308K), 370C net sold 13:20-13:35. Bullish-leaning: 1DTE 377.5P sold at the bid $509K, 365P net sold 13:20-13:35, 377.5C mostly bought at the ask into the test, a 372.5C $287K ask buy. Net: no directional edge, consistent with RA's 0.")
    P("- **Gamma: 0 (no as-of GEX; UW has only the 16:00 snapshot).** OI context known at the open: 1DTE put OI concentrated at 370 (8,562) / 365 (5,276), call OI stacked 375-390 (10.8k-15.7k) → plausibly a support/pin zone at 370 and overhead call OI at the 375-385 short strikes, but the sign of dealer exposure is unknown, so it is not scored.")
    P("- Nudge therefore stays **0**; grade stays **C**. (Under the RA weights the merged positioning term is 0 either way.)")
    P("- **PA's independent HISTORY definition** (HISTORY_events.csv, 15m pivot-low support tested 2+ times, 0.10-1.00% wick, reclaim within 2 bars, stop = wick, n=33): +1R before stop 47% within 16 bars (+2R 28%); within 64 bars +1R 50%, stop 72%; median 16-bar MFE +0.96% / MAE −0.74%. Coin-flip at 1R, same message as my sample.")
    P("- PA levels for context: VWAP 372.39 (price 1.82 below), 5m/15m below all SMAs; 1h SMA200 369.91 and D SMA20 367.57 under price; reclaim on shrinking volume (0.49-0.67x).")
    P("")
    P("## VERDICT (phase 1, blind)")
    P(f"- **Desk verdict: WATCH — no TAKE on any of the 13 structures.** WATCH rows: {', '.join(r['name'] for r in watch)}. SKIP: {', '.join(r['name'] for r in R if r['verdict'] == 'SKIP')}.")
    P(f"- **Headline spread (best spread by conservative min(EV, EV_B)): {best['name']}**, debit ${best['debit']:.0f} mid (${best['debit_full']:.0f} full) | grade {best['grade']} ({best['score']:+.2f}) | **EV {best['ev']:+.0f} $ ({100*best['ev']/best['debit']:+.0f}% of debit)**, EV ±10pp {best['ev_lo']:+.0f} / {best['ev_hi']:+.0f}, EV_B {best['ev_b']:+.0f} | **p_t / p_p / p_s = {best['p']['t']:.2f} / {best['p']['p']:.2f} / {best['p']['s']:.2f}** (+OTM {best['p']['x']:.2f}) | **WATCH**.")
    P(f"- **Rule that drove it: the grade gate.** {best['name']} is the only spread with EV ≥ 0 across the whole ±10pp band ({', '.join(band_ok)}), EV_B > 0 and the brief's trigger fired, so the *only* failed TAKE condition is grade C < B. RA's own 15m trigger was also still pending at 13:40 (secondary).")
    P(f"- Best structure of any type: {bestall['name']} (EV {bestall['ev']:+.0f}, EV_B {bestall['ev_b']:+.0f}, WATCH; −10pp band {bestall['ev_lo']:+.0f}).")
    P("- Oct 16 spreads: SKIP on the math (the 0.23-ATR daily-close stop is hit by 23 of 28 HISTORY paths within 6 sessions; EV −$93 to −$120). Oct 12 spreads: WATCH, thin.")
    P("- Plain reading: HISTORY gives this trigger roughly a coin-flip with no reliable lift over random entries (n=29, lift −10 to +13pp depending on strikes), and the market prices the 1DTE spreads near fair. Every positive EV is small (+$15 to +$60) and within one standard error of zero. **The 'not TAKE' outcome is decided by the grade gate (missing gamma/flow scored 0, weights reallocated) rather than by the EV math.** What would have upgraded it at 13:40: RA's own sensitivities (volume +1 for test-bar absorption, or structure +2 on a 15m close/VWAP reclaim) lift the grade to B, which would make the 375/385C a TAKE under the rules.")
    open(out_path, 'w').write('\n'.join(L) + '\n')
    json.dump(dict(rows=[{k: (v if not isinstance(v, dict) else {kk: float(vv) if not isinstance(vv, (int, str)) else vv for kk, vv in v.items()}) for k, v in r.items()} for r in R], base_rates=BR),
              open(out_path.replace('.md', '.json'), 'w'), indent=1, default=float)
    print('\n'.join(L))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '/tmp/p1.md')
