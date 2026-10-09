# Phase 1 (BLIND) — TSLA 370.25 wick-reclaim, as of Thu 2026-10-08 13:40 ET (close of the 13:35 5m bar)
Written 2026-10-09 13:17 ET by Planner (executor). **Written before outcome viewed:** TSLA_outcome.md and every TSLA bar after 13:35 Oct 8 were NOT opened by any code or read for this section; RA_audit_notes.md and RA_tsla_ivcal_LOOKAHEAD.csv NOT opened.

**Leakage disclosure (read first).** This phase is *mechanically* blind, not *cognitively* blind:
- The task brief itself states the outcome (Oct 8 close ~375, Oct 9 high 388.55). I could not avoid reading it.
- The permitted method files (`watchlist/checks/20261009-tsla-pa.md`, `20261009-1020-tsla-ra.md`) narrate the post-13:35 path (13:45 5m close 369.88, VWAP reclaim 15:10, close 375.00, Oct 9 gap to 382.19 and 388.55). I read them for level definitions, so I have seen that path.
- While inspecting daily-bar formats I printed the last 8 rows of `pa_data/TSLA_1D.json`, which include the Oct 8 and partial Oct 9 daily bars (no new information beyond the brief: close 375, Oct 9 high 388.56).
- RA's IV level is inverted from Oct 8 EOD last trades (mild IV lookahead; RA's LOW/MID/HIGH brackets used; spreads move ±$0.05-0.30 across them). RA's executor saw the Oct 8 close in a web search (RA disclosure).
- Mitigation: every number below comes from code that only loads bars ending ≤13:40 Oct 8 (PA HISTORY files, verified byte-identical to a 13:40 cut of the raw export) and daily bars ≤ Oct 7; all rules are copied from `outputs/ev_calc.py` or pre-declared here; factor scores are RA's as-of scores (not mine). No parameter was tuned after seeing results.

## Setup as of 13:40
- Spot 370.57 (13:35 5m close, first close back above 370.25). Wick low 368.04 (13:25). Session VWAP 372.39 (RA). Daily ATR14 (to Oct 7) **11.09**; stop distance to the wick = 0.23 ATR (2.53 pts).
- Expiries: **no Oct 10 expiry (Saturday)**; Oct 12 (Mon) weekly used instead; Oct 16 weekly. Prices: RA's Black-Scholes model (MID IV; no real Oct 8 intraday quotes exist), entry at mid, exit pays ½ the assumed bid/ask per leg.
- Trigger: the brief's trigger (5m reclaim close >370.25) **fired at 13:35**. RA's stricter trigger (15m close >370.25, the 13:30-13:45 bar) was **still pending** at 13:40.
- Grade (RA as-of, weights 25/15/20/5/5/10/10/10): structure +1, volume 0, trend 0, gamma 0 (n/a), flow 0 (n/a), catalyst 0, IV +1 (1DTE/Oct12) / 0 (Oct16), liquidity +2 → **+0.55 C (1DTE, Oct 12), +0.45 C (Oct 16)**. Direction nudge inputs (volume, merged gamma/flow; trend for EV_B) are all 0 → **nudge = 0 log-odds**.
- Mechanical check: my level detector (daily 5-bar pivots, clustered ±0.3%, ≥2 pivots, prior days only) independently flags Oct 8 as an event (cluster 368.78, 4 pivots/11 touches; wick 368.04; entry on the 13:25 close), so today's setup is in the same event class as the HISTORY sample.

## Base rates from HISTORY (event = intraday wick through a tested daily-pivot support, reclaim close within ≤2 (15m) / ≤4 (5m) bars, entry at the reclaim close 09:45-15:30, one per day; depth ≤0.4 ATR)
| Sample | n | Same-day close vs entry: mean / median (ATR), % up | Next-day close: mean / median (ATR), % up | P(next-day close ≥ 375-equiv, +0.4 ATR) | Day-6 close mean (ATR) | MFE / MAE to next-day close, median (ATR) | Target (+0.4 ATR) before wick stop | Target before a close back under the level | Daily close under wick on day 0 |
|---|---|---|---|---|---|---|---|---|---|
| TSLA 15m-bar events (Feb 2 - Oct 7 2026) | 29 | -0.01 / -0.06, 41% | -0.01 / -0.09, 45% | 38% | -0.72 (n=28) | +0.36 / -0.67 | 28% | 24% | 34% |
| TSLA 5m-bar events (Jul 27 - Oct 7 2026) | 5 | +0.06 / +0.17, 60% | +0.47 / +0.71, 80% | 60% | +0.48 (n=4) | +0.92 / -0.25 | 40% | 0% | 20% |
| SPY 5m-bar events (pool, Jul 27 - Oct 7) | 3 | +0.25 / +0.34, 67% | +0.73 / +1.13, 67% | 67% | +1.38 (n=2) | +1.56 / -0.39 | 33% | 33% | 33% |

Primary own sample = the 15m-bar set (n=29, the only one with n ≥ 15; W=5). Pool = own + SPY 5m events (TSLA is in its own pool, as in ev_calc). Drift baseline = every 3rd 15m bar close on all HISTORY days with the same strikes/stop. **n is small and all events are from one 8-month regime; treat every rate as ±9-18pp (1 s.e.).**

## Framework run (ev_calc rules: daily-close stop at 368.04, shrink, nudge 0, cap at market+10pp, drift-neutral EV_B, TAKE/WATCH/SKIP + WATCH→SKIP if EV_B<0)
| Structure | Debit mid (full) | Grade | n own: t/p/x/s | Prior p_t | p_t / p_p / p_s (+OTM) | Mkt p_t (same stop) | Capped | V_t / V_p / V_s | EV $ (% debit) | EV @ p_t ±10pp | BE p_t | EV_B drift-neutral | Conservative min | Verdict (BRIEF rule → final) | Rule that drove it |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Oct9 370C | $345 ($350) | C (+0.55) | 29: 9/2/8/10 | 0.32 | 0.32 / 0.07 / 0.34 (+0.27) | 0.32 | no | 898 / 168 / 77 | -24 (-7%) | -108 / +60 | 0.34 | +9 | -24 | SKIP → **SKIP** | SKIP: EV <= 3% of debit (noise floor) |
| Oct9 372.5C | $243 ($248) | C (+0.55) | 29: 9/0/10/10 | 0.32 | 0.32 / 0.00 / 0.34 (+0.34) | 0.27 | no | 784 / 114 / 44 | +19 (+8%) | -57 / +95 | 0.29 | +54 | +19 | WATCH → **WATCH** | WATCH: EV>3% debit, grade C blocks TAKE (needs >=B) |
| Oct9 375C | $172 ($175) | C (+0.55) | 29: 9/0/10/10 | 0.32 | 0.32 / 0.00 / 0.34 (+0.34) | 0.22 | no | 707 / 82 / 26 | +60 (+35%) | -10 / +129 | 0.23 | +84 | +60 | WATCH → **WATCH** | WATCH: EV>3% debit, grade C blocks TAKE (needs >=B) |
| Oct9 370/375C | $172 ($180) | C (+0.55) | 29: 9/2/8/10 | 0.32 | 0.32 / 0.07 / 0.34 (+0.27) | 0.27 | no | 492 / 240 / 46 | +15 (+9%) | -30 / +60 | 0.28 | +52 | +15 | WATCH → **WATCH** | WATCH: EV>3% debit, grade C blocks TAKE (needs >=B) |
| Oct9 370/380C | $258 ($265) | C (+0.55) | 29: 4/7/8/10 | 0.15 | 0.15 / 0.24 / 0.34 (+0.27) | 0.13 | no | 992 / 460 / 63 | +18 (+7%) | -66 / +102 | 0.12 | +85 | +18 | WATCH → **WATCH** | WATCH: EV>3% debit, grade C blocks TAKE (needs >=B) |
| Oct9 372.5/377.5C | $121 ($128) | C (+0.55) | 29: 7/2/10/10 | 0.25 | 0.25 / 0.07 / 0.34 (+0.34) | 0.19 | no | 492 / 233 / 24 | +25 (+21%) | -21 / +71 | 0.19 | +58 | +25 | WATCH → **WATCH** | WATCH: EV>3% debit, grade C blocks TAKE (needs >=B) |
| Oct9 375/380C | $85 ($90) | C (+0.55) | 29: 4/5/10/10 | 0.15 | 0.15 / 0.17 / 0.34 (+0.34) | 0.14 | no | 495 / 232 / 12 | +30 (+35%) | -14 / +75 | 0.08 | +47 | +30 | WATCH → **WATCH** | WATCH: EV>3% debit, grade C blocks TAKE (needs >=B) |
| Oct9 375/385C | $127 ($132) | C (+0.55) | 29: 1/8/10/10 | 0.04 | 0.04 / 0.28 / 0.34 (+0.34) | 0.07 | no | 995 / 423 / 19 | +35 (+27%) | +1 / +122 | -0.00 | +46 | +35 | WATCH → **WATCH** | WATCH: EV>3% debit, grade C blocks TAKE (needs >=B) |
| Oct12 370/375C | $192 ($202) | C (+0.55) | 29: 8/2/2/17 | 0.28 | 0.28 / 0.07 / 0.58 (+0.07) | 0.28 | no | 490 / 248 / 89 | +15 (+8%) | -25 / +54 | 0.24 | +24 | +15 | WATCH → **WATCH** | WATCH: EV>3% debit, grade C blocks TAKE (needs >=B) |
| Oct12 370/380C | $316 ($324) | C (+0.55) | 29: 5/5/2/17 | 0.18 | 0.18 / 0.17 / 0.58 (+0.07) | 0.18 | no | 992 / 495 / 140 | +28 (+9%) | -51 / +107 | 0.14 | +74 | +28 | WATCH → **WATCH** | WATCH: EV>3% debit, grade C blocks TAKE (needs >=B) |
| Oct16 370/380C | $390 ($400) | C (+0.45) | 28: 2/1/2/23 | 0.08 | 0.08 / 0.04 / 0.82 (+0.07) | 0.19 | no | 990 / 537 / 248 | -93 (-24%) | -150 / -18 | 0.20 | -65 | -93 | SKIP → **SKIP** | SKIP: EV <= 3% of debit (noise floor) |
| Oct16 375/385C | $307 ($317) | C (+0.45) | 28: 0/2/3/23 | 0.01 | 0.01 / 0.07 / 0.82 (+0.11) | 0.16 | no | 990 / 508 / 178 | -120 (-39%) | -124 / -39 | 0.15 | -67 | -120 | SKIP → **SKIP** | SKIP: EV <= 3% of debit (noise floor) |
| Oct16 380/390C | $238 ($248) | C (+0.45) | 28: 0/2/3/23 | 0.01 | 0.01 / 0.07 / 0.82 (+0.11) | 0.13 | no | 990 / 492 / 124 | -97 (-41%) | -101 / -11 | 0.12 | -36 | -97 | SKIP → **SKIP** | SKIP: EV <= 3% of debit (noise floor) |

Long calls: 'target' = settle above break-even, V_t = market-MC mean intrinsic above BE (the framework's bucket valuation; it truncates the tail).

**Market-measure check.** With the framework's flat MC vol (mean of the two leg IVs) the spreads show market EV of Oct9 370/375C +17, Oct9 370/380C +37, Oct9 372.5/377.5C +20, Oct9 375/380C +20, Oct9 375/385C +36. That is RA's upward call smile (OTM call IV > ATM) making spreads cheap vs flat vol — the same artifact EV.md flagged on SPY bear. Sensitivity with the MC vol calibrated so the market measure prices each debit exactly:
| Structure | EV (calibrated mkt) | EV ±10pp | EV_B | Verdict |
|---|---|---|---|---|
| Oct9 370C | -24 | -108 / +60 | +9 | SKIP |
| Oct9 372.5C | +19 | -57 / +95 | +54 | WATCH |
| Oct9 375C | +60 | -10 / +129 | +84 | WATCH |
| Oct9 370/375C | -10 | -55 / +34 | +29 | SKIP |
| Oct9 370/380C | +7 | -79 / +92 | +41 | SKIP |
| Oct9 372.5/377.5C | +14 | -32 / +60 | +33 | WATCH |
| Oct9 375/380C | +28 | -17 / +73 | +22 | WATCH |
| Oct9 375/385C | +22 | -12 / +110 | +3 | WATCH |
| Oct12 370/375C | +14 | -26 / +54 | +17 | WATCH |
| Oct12 370/380C | +24 | -55 / +104 | +51 | WATCH |
| Oct16 370/380C | -93 | -150 / -18 | -56 | SKIP |
| Oct16 375/385C | -121 | -125 / -40 | -71 | SKIP |
| Oct16 380/390C | -98 | -102 / -12 | -44 | SKIP |

**IV bracket (RA LOW/HIGH) on the 1DTE spreads:** debits Oct9 370/375C: LOW $163 / MID $172 / HIGH $178; Oct9 370/380C: LOW $230 / MID $258 / HIGH $281; Oct9 372.5/377.5C: LOW $105 / MID $121 / HIGH $136; Oct9 375/380C: LOW $67 / MID $85 / HIGH $102; Oct9 375/385C: LOW $93 / MID $127 / HIGH $159.
- Oct9 370/375C LOW: EV +17, EV_B +52, WATCH; Oct9 370/380C LOW: EV +29, EV_B +80, WATCH; Oct9 372.5/377.5C LOW: EV +36, EV_B +57, WATCH; Oct9 375/380C LOW: EV +44, EV_B +44, WATCH; Oct9 375/385C LOW: EV +53, EV_B +39, WATCH; Oct9 370/375C HIGH: EV +14, EV_B +52, WATCH; Oct9 370/380C HIGH: EV +9, EV_B +86, WATCH; Oct9 372.5/377.5C HIGH: EV +16, EV_B +56, WATCH; Oct9 375/380C HIGH: EV +18, EV_B +45, WATCH; Oct9 375/385C HIGH: EV +15, EV_B +47, WATCH

**Own-sample sensitivity (5m-bar events only, n=5, W=10):** Oct9 370/375C EV +67 / EV_B +119 → WATCH; Oct9 370/380C EV +148 / EV_B +238 → WATCH; Oct9 372.5/377.5C EV +80 / EV_B +154 → WATCH; Oct9 375/380C EV +77 / EV_B +133 → WATCH; Oct9 375/385C EV +124 / EV_B +103 → WATCH.

## As-of flow / gamma / PA cross-checks (scored before the verdict; no lookahead files opened)
- **UW flow to 13:35 (UW_tsla_asof.md): two-sided → flow 0.** Bearish-leaning: 1DTE 370P bought at the ask $484K (12:53), 1DTE calls sold at the bid above spot (372.5C $453K, 370C $280K, 375C $276K, 367.5C $308K), 370C net sold 13:20-13:35. Bullish-leaning: 1DTE 377.5P sold at the bid $509K, 365P net sold 13:20-13:35, 377.5C mostly bought at the ask into the test, a 372.5C $287K ask buy. Net: no directional edge, consistent with RA's 0.
- **Gamma: 0 (no as-of GEX; UW has only the 16:00 snapshot).** OI context known at the open: 1DTE put OI concentrated at 370 (8,562) / 365 (5,276), call OI stacked 375-390 (10.8k-15.7k) → plausibly a support/pin zone at 370 and overhead call OI at the 375-385 short strikes, but the sign of dealer exposure is unknown, so it is not scored.
- Nudge therefore stays **0**; grade stays **C**. (Under the RA weights the merged positioning term is 0 either way.)
- **PA's independent HISTORY definition** (HISTORY_events.csv, 15m pivot-low support tested 2+ times, 0.10-1.00% wick, reclaim within 2 bars, stop = wick, n=33): +1R before stop 47% within 16 bars (+2R 28%); within 64 bars +1R 50%, stop 72%; median 16-bar MFE +0.96% / MAE −0.74%. Coin-flip at 1R, same message as my sample.
- PA levels for context: VWAP 372.39 (price 1.82 below), 5m/15m below all SMAs; 1h SMA200 369.91 and D SMA20 367.57 under price; reclaim on shrinking volume (0.49-0.67x).

## VERDICT (phase 1, blind)
- **Desk verdict: WATCH — no TAKE on any of the 13 structures.** WATCH rows: Oct9 372.5C, Oct9 375C, Oct9 370/375C, Oct9 370/380C, Oct9 372.5/377.5C, Oct9 375/380C, Oct9 375/385C, Oct12 370/375C, Oct12 370/380C. SKIP: Oct9 370C, Oct16 370/380C, Oct16 375/385C, Oct16 380/390C.
- **Headline spread (best spread by conservative min(EV, EV_B)): Oct9 375/385C**, debit $127 mid ($132 full) | grade C (+0.55) | **EV +35 $ (+27% of debit)**, EV ±10pp +1 / +122, EV_B +46 | **p_t / p_p / p_s = 0.04 / 0.28 / 0.34** (+OTM 0.34) | **WATCH**.
- **Rule that drove it: the grade gate.** Oct9 375/385C is the only spread with EV ≥ 0 across the whole ±10pp band (Oct9 375/385C), EV_B > 0 and the brief's trigger fired, so the *only* failed TAKE condition is grade C < B. RA's own 15m trigger was also still pending at 13:40 (secondary).
- Best structure of any type: Oct9 375C (EV +60, EV_B +84, WATCH; −10pp band -10).
- Oct 16 spreads: SKIP on the math (the 0.23-ATR daily-close stop is hit by 23 of 28 HISTORY paths within 6 sessions; EV −$93 to −$120). Oct 12 spreads: WATCH, thin.
- Plain reading: HISTORY gives this trigger roughly a coin-flip with no reliable lift over random entries (n=29, lift −10 to +13pp depending on strikes), and the market prices the 1DTE spreads near fair. Every positive EV is small (+$15 to +$60) and within one standard error of zero. **The 'not TAKE' outcome is decided by the grade gate (missing gamma/flow scored 0, weights reallocated) rather than by the EV math.** What would have upgraded it at 13:40: RA's own sensitivities (volume +1 for test-bar absorption, or structure +2 on a 15m close/VWAP reclaim) lift the grade to B, which would make the 375/385C a TAKE under the rules.
