# TSLA blind test (370.25 wick-reclaim, Thu Oct 8 2026): calibration of the Planner EV framework
Planner (executor), generated 2026-10-09 13:22 ET. Research only: no orders, no broker, no risk.md edits. Price history = PA TradingView exports; flow = UW; option prices = RA Black-Scholes model (as-of) and saved CBOE delayed chains (Oct 9, for exits). No yfinance or outside price data.
Code + intermediate data: `tsla_blind/work/` (events.py, fw.py, phase1.py, phase2.py, phase3a-e.py, calib.py; *.json). Phase 1 file SHA-256 (saved 13:17:55 ET, made read-only before the outcome was opened): `834ceee352ac1ec0038836547b1587037779dbe1838b404798adcd00e19d8a48`.

## 0. Bottom line
- **Blind verdict: WATCH, no TAKE.** Headline spread Oct 9 (1DTE) 375/385C, $127 mid, EV +$35 (+27%), p_t/p_p/p_s 0.04/0.28/0.34 (+OTM 0.34), grade C (+0.55). **The binding rule was the grade gate (C < B)**; the 375/385C passed every other TAKE condition (EV ≥ 0 at −10pp: +$1; EV_B +$46; brief's trigger fired).
- **What happened:** TSLA closed Oct 8 at 375.00 and ran to 388.55 on Oct 9 (MFE +7.1R, MAE −0.28R; the 368.04 stop was never touched). The 375/385C would have returned **+82% at the Oct 8 close, +$601 to +$632 (+470-500%) at real Oct 9 bids (10:13 / 12:38 ET), +536% if it settles at 383.08** (Oct 9 close pending). Under a strict *5m*-close-under-370.25 stop it would have been stopped at 13:45 for about −17%. Under the 15m-close rule it was not stopped.
- **Calibration (HISTORY, 24-29 events, Feb-Oct 2026, 6 structures each):** the framework said 0 TAKE / 17% WATCH / 83% SKIP. **SKIP was right 85 of 118 times (72%).** WATCH rows won 29% with mean −$18. The average trade across all decisions lost about the cost of trading (−$28, −1% of debit). Turning off the toward-flat safeguards created 6 TAKEs on 4 distinct days, and **all 6 lost (mean −$234).** On daily 20-day breakouts (366 events, 6 names) SKIP was right only 53%, SKIPs averaged +9% of debit, and the WATCH→SKIP demotion threw away rows that averaged about +17% of debit.
- **Bias found? Yes, in the verdict layer, but it was not costly on this setup.** On this setup the EV math is honest: there is no measurable edge in HISTORY, and flat was the right default on average. Oct 8 was a ~1.5-sd tail day. **One win proves nothing (n=1).** The verdict layer is still structurally flat-biased: TAKE is nearly unreachable, the grade gate scores missing data as 0, and the EV_B rule and the cap only ever act one way. The stop modelling is biased the other way: daily-close stops flatter the trade. For the 1DTE rows the two roughly cancel. Every EV here is within about 1-1.5 standard errors of zero, so no conclusion about edge is supportable at this n.

## 1. Blindness and leakage (read before trusting phase 1)
- **Mechanically blind: yes.** Phase 1 code loaded only PA HISTORY/as-of files ending at or before 13:40 Oct 8 (I verified they are byte-identical to my own 13:40 cut of the raw export), daily bars up to Oct 7, RA's as-of prices, and UW's as-of flow. TSLA_outcome.md, RA_audit_notes.md, RA_tsla_ivcal_LOOKAHEAD.csv, UW_tsla_LOOKAHEAD.md and raw_full_LOOKAHEAD/ were opened only after phase 1 was saved and chmod'd read-only.
- **Cognitively blind: no.** (1) The task brief itself states the outcome (Oct 8 close ~375, Oct 9 high 388.55). (2) The allowed method files `20261009-tsla-pa.md` and `20261009-1020-tsla-ra.md` narrate the whole post-cutoff path. (3) While checking formats I printed the last 8 daily rows of `pa_data/TSLA_1D.json`, which include Oct 8 and the partial Oct 9 bar (nothing beyond what the brief already said). (4) RA's IV level is inverted from Oct 8 EOD last trades: a mild IV lookahead. Spread debits move only ±$5-30 across RA's LOW/HIGH brackets, and the verdict is the same in both (phase 1 tables). (5) RA's executor saw the Oct 8 close in a web search (RA's disclosure).
- **Mitigation:** all rules are copied from `outputs/ev_calc.py` or declared before any result. The factor scores are RA's as-of scores, not mine. UW flow was scored 0 (two-sided), the same as RA. No parameter was changed after results came in. The one judgment call that cuts toward a positive EV in phase 1 is the long-call 'target' bucket definition (settle > break-even), which I disclose.
- **Residual risk:** the event definition, the strike set and the choice of the 15m sample as primary were made by someone who knew the outcome. The PA and RA files used for level definitions were also written after the cutoff. The critic should treat phase 1 as 'mechanically reproducible but designed by an informed analyst'.

## 2. Phase 1 (verbatim, as saved before the outcome was viewed)

### Phase 1 (BLIND) — TSLA 370.25 wick-reclaim, as of Thu 2026-10-08 13:40 ET (close of the 13:35 5m bar)
Written 2026-10-09 13:17 ET by Planner (executor). **Written before outcome viewed:** TSLA_outcome.md and every TSLA bar after 13:35 Oct 8 were NOT opened by any code or read for this section; RA_audit_notes.md and RA_tsla_ivcal_LOOKAHEAD.csv NOT opened.

**Leakage disclosure (read first).** This phase is *mechanically* blind, not *cognitively* blind:
- The task brief itself states the outcome (Oct 8 close ~375, Oct 9 high 388.55). I could not avoid reading it.
- The permitted method files (`watchlist/checks/20261009-tsla-pa.md`, `20261009-1020-tsla-ra.md`) narrate the post-13:35 path (13:45 5m close 369.88, VWAP reclaim 15:10, close 375.00, Oct 9 gap to 382.19 and 388.55). I read them for level definitions, so I have seen that path.
- While inspecting daily-bar formats I printed the last 8 rows of `pa_data/TSLA_1D.json`, which include the Oct 8 and partial Oct 9 daily bars (no new information beyond the brief: close 375, Oct 9 high 388.56).
- RA's IV level is inverted from Oct 8 EOD last trades (mild IV lookahead; RA's LOW/MID/HIGH brackets used; spreads move ±$0.05-0.30 across them). RA's executor saw the Oct 8 close in a web search (RA disclosure).
- Mitigation: every number below comes from code that only loads bars ending ≤13:40 Oct 8 (PA HISTORY files, verified byte-identical to a 13:40 cut of the raw export) and daily bars ≤ Oct 7; all rules are copied from `outputs/ev_calc.py` or pre-declared here; factor scores are RA's as-of scores (not mine). No parameter was tuned after seeing results.

### Setup as of 13:40
- Spot 370.57 (13:35 5m close, first close back above 370.25). Wick low 368.04 (13:25). Session VWAP 372.39 (RA). Daily ATR14 (to Oct 7) **11.09**; stop distance to the wick = 0.23 ATR (2.53 pts).
- Expiries: **no Oct 10 expiry (Saturday)**; Oct 12 (Mon) weekly used instead; Oct 16 weekly. Prices: RA's Black-Scholes model (MID IV; no real Oct 8 intraday quotes exist), entry at mid, exit pays ½ the assumed bid/ask per leg.
- Trigger: the brief's trigger (5m reclaim close >370.25) **fired at 13:35**. RA's stricter trigger (15m close >370.25, the 13:30-13:45 bar) was **still pending** at 13:40.
- Grade (RA as-of, weights 25/15/20/5/5/10/10/10): structure +1, volume 0, trend 0, gamma 0 (n/a), flow 0 (n/a), catalyst 0, IV +1 (1DTE/Oct12) / 0 (Oct16), liquidity +2 → **+0.55 C (1DTE, Oct 12), +0.45 C (Oct 16)**. Direction nudge inputs (volume, merged gamma/flow; trend for EV_B) are all 0 → **nudge = 0 log-odds**.
- Mechanical check: my level detector (daily 5-bar pivots, clustered ±0.3%, ≥2 pivots, prior days only) independently flags Oct 8 as an event (cluster 368.78, 4 pivots/11 touches; wick 368.04; entry on the 13:25 close), so today's setup is in the same event class as the HISTORY sample.

### Base rates from HISTORY (event = intraday wick through a tested daily-pivot support, reclaim close within ≤2 (15m) / ≤4 (5m) bars, entry at the reclaim close 09:45-15:30, one per day; depth ≤0.4 ATR)
| Sample | n | Same-day close vs entry: mean / median (ATR), % up | Next-day close: mean / median (ATR), % up | P(next-day close ≥ 375-equiv, +0.4 ATR) | Day-6 close mean (ATR) | MFE / MAE to next-day close, median (ATR) | Target (+0.4 ATR) before wick stop | Target before a close back under the level | Daily close under wick on day 0 |
|---|---|---|---|---|---|---|---|---|---|
| TSLA 15m-bar events (Feb 2 - Oct 7 2026) | 29 | -0.01 / -0.06, 41% | -0.01 / -0.09, 45% | 38% | -0.72 (n=28) | +0.36 / -0.67 | 28% | 24% | 34% |
| TSLA 5m-bar events (Jul 27 - Oct 7 2026) | 5 | +0.06 / +0.17, 60% | +0.47 / +0.71, 80% | 60% | +0.48 (n=4) | +0.92 / -0.25 | 40% | 0% | 20% |
| SPY 5m-bar events (pool, Jul 27 - Oct 7) | 3 | +0.25 / +0.34, 67% | +0.73 / +1.13, 67% | 67% | +1.38 (n=2) | +1.56 / -0.39 | 33% | 33% | 33% |

Primary own sample = the 15m-bar set (n=29, the only one with n ≥ 15; W=5). Pool = own + SPY 5m events (TSLA is in its own pool, as in ev_calc). Drift baseline = every 3rd 15m bar close on all HISTORY days with the same strikes/stop. **n is small and all events are from one 8-month regime; treat every rate as ±9-18pp (1 s.e.).**

### Framework run (ev_calc rules: daily-close stop at 368.04, shrink, nudge 0, cap at market+10pp, drift-neutral EV_B, TAKE/WATCH/SKIP + WATCH→SKIP if EV_B<0)
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

### As-of flow / gamma / PA cross-checks (scored before the verdict; no lookahead files opened)
- **UW flow to 13:35 (UW_tsla_asof.md): two-sided → flow 0.** Bearish-leaning: 1DTE 370P bought at the ask $484K (12:53), 1DTE calls sold at the bid above spot (372.5C $453K, 370C $280K, 375C $276K, 367.5C $308K), 370C net sold 13:20-13:35. Bullish-leaning: 1DTE 377.5P sold at the bid $509K, 365P net sold 13:20-13:35, 377.5C mostly bought at the ask into the test, a 372.5C $287K ask buy. Net: no directional edge, consistent with RA's 0.
- **Gamma: 0 (no as-of GEX; UW has only the 16:00 snapshot).** OI context known at the open: 1DTE put OI concentrated at 370 (8,562) / 365 (5,276), call OI stacked 375-390 (10.8k-15.7k) → plausibly a support/pin zone at 370 and overhead call OI at the 375-385 short strikes, but the sign of dealer exposure is unknown, so it is not scored.
- Nudge therefore stays **0**; grade stays **C**. (Under the RA weights the merged positioning term is 0 either way.)
- **PA's independent HISTORY definition** (HISTORY_events.csv, 15m pivot-low support tested 2+ times, 0.10-1.00% wick, reclaim within 2 bars, stop = wick, n=33): +1R before stop 47% within 16 bars (+2R 28%); within 64 bars +1R 50%, stop 72%; median 16-bar MFE +0.96% / MAE −0.74%. Coin-flip at 1R, same message as my sample.
- PA levels for context: VWAP 372.39 (price 1.82 below), 5m/15m below all SMAs; 1h SMA200 369.91 and D SMA20 367.57 under price; reclaim on shrinking volume (0.49-0.67x).

### VERDICT (phase 1, blind)
- **Desk verdict: WATCH — no TAKE on any of the 13 structures.** WATCH rows: Oct9 372.5C, Oct9 375C, Oct9 370/375C, Oct9 370/380C, Oct9 372.5/377.5C, Oct9 375/380C, Oct9 375/385C, Oct12 370/375C, Oct12 370/380C. SKIP: Oct9 370C, Oct16 370/380C, Oct16 375/385C, Oct16 380/390C.
- **Headline spread (best spread by conservative min(EV, EV_B)): Oct9 375/385C**, debit $127 mid ($132 full) | grade C (+0.55) | **EV +35 $ (+27% of debit)**, EV ±10pp +1 / +122, EV_B +46 | **p_t / p_p / p_s = 0.04 / 0.28 / 0.34** (+OTM 0.34) | **WATCH**.
- **Rule that drove it: the grade gate.** Oct9 375/385C is the only spread with EV ≥ 0 across the whole ±10pp band (Oct9 375/385C), EV_B > 0 and the brief's trigger fired, so the *only* failed TAKE condition is grade C < B. RA's own 15m trigger was also still pending at 13:40 (secondary).
- Best structure of any type: Oct9 375C (EV +60, EV_B +84, WATCH; −10pp band -10).
- Oct 16 spreads: SKIP on the math (the 0.23-ATR daily-close stop is hit by 23 of 28 HISTORY paths within 6 sessions; EV −$93 to −$120). Oct 12 spreads: WATCH, thin.
- Plain reading: HISTORY gives this trigger roughly a coin-flip with no reliable lift over random entries (n=29, lift −10 to +13pp depending on strikes), and the market prices the 1DTE spreads near fair. Every positive EV is small (+$15 to +$60) and within one standard error of zero. **The 'not TAKE' outcome is decided by the grade gate (missing gamma/flow scored 0, weights reallocated) rather than by the EV math.** What would have upgraded it at 13:40: RA's own sensitivities (volume +1 for test-bar absorption, or structure +2 on a 15m close/VWAP reclaim) lift the grade to B, which would make the 375/385C a TAKE under the rules.


## 3. Phase 2: what each structure actually returned
Entry = RA MID model price at 13:35 (370.57). Exits: (a) a strict 5m-close stop (13:45 close 369.88 < 370.25, out ~13:50 at the model value); (b) the Oct 8 close, 375.00 (model value, ½ spread); (c) real CBOE delayed quotes on Oct 9 at ~10:13 ET (S 384.49) and ~12:38 ET (S 382.80), selling the long at the bid and buying the short at the ask; (d) a model mark at the 388.55 high (not realistic: peak timing); (e) 1DTE intrinsic if Oct 9 settles at 383.08 (13:10 price; **the Oct 9 close is pending**). 15m-close stop and RA's invalidation (15m <368 / 5m <369): **not hit**. The 368.04 wick stop: not hit.
| Structure | Debit (mid) | (a) 5m-close stop | (b) Oct 8 close | (c) Oct 9 10:13 at bid | (c) Oct 9 12:38 at bid | (d) at 388.55 (model) | (e) settle @383.08 |
|---|---|---|---|---|---|---|---|
| Oct9 370C | $345 | -45 (-13%) | +250 (+73%) | +1090 (+316%) | +925 (+268%) | +1509 (+438%) | +963 (+279%) |
| Oct9 372.5C | $243 | -36 (-15%) | +188 (+77%) | +947 (+389%) | +782 (+321%) | +1361 (+560%) | +815 (+335%) |
| Oct9 375C | $172 | -27 (-16%) | +134 (+78%) | +773 (+448%) | +603 (+349%) | +1187 (+688%) | +636 (+369%) |
| Oct9 370/375C | $172 | -23 (-13%) | +106 (+62%) | +288 (+167%) | +303 (+176%) | +307 (+178%) | +328 (+190%) |
| Oct9 370/380C | $258 | -33 (-13%) | +183 (+71%) | +662 (+257%) | +692 (+269%) | +680 (+264%) | +742 (+288%) |
| Oct9 372.5/377.5C | $121 | -20 (-17%) | +87 (+72%) | +334 (+276%) | +354 (+293%) | +346 (+286%) | +379 (+313%) |
| Oct9 375/380C | $85 | -15 (-18%) | +67 (+78%) | +345 (+404%) | +370 (+433%) | +358 (+420%) | +415 (+486%) |
| Oct9 375/385C | $127 | -21 (-17%) | +104 (+82%) | +632 (+498%) | +601 (+473%) | +679 (+535%) | +681 (+536%) |
| Oct12 370/375C | $192 | -21 (-11%) | +69 (+36%) | +213 (+111%) | +203 (+106%) | +252 (+132%) | n/a (later expiry) |
| Oct12 370/380C | $316 | -28 (-9%) | +132 (+42%) | +474 (+150%) | +439 (+139%) | +534 (+169%) | n/a (later expiry) |
| Oct16 370/380C | $390 | -22 (-6%) | +66 (+17%) | +245 (+63%) | +245 (+63%) | +301 (+77%) | n/a (later expiry) |
| Oct16 375/385C | $307 | -21 (-7%) | +61 (+20%) | +248 (+81%) | +228 (+74%) | +295 (+96%) | n/a (later expiry) |
| Oct16 380/390C | $238 | -20 (-8%) | +51 (+21%) | +222 (+93%) | +192 (+80%) | +276 (+116%) | n/a (later expiry) |

- Every call structure was a large winner at any realistic Oct 9 exit. The 1DTE long calls (+270-450%) and the 375/385C (+470-500%) did best. The Oct 16 spreads, which the framework SKIPped on the math, made +63-93% at 10:13.
- How rare was the path? Oct 8 13:40 → Oct 9 10:13 was +13.9 pts, about +1.25 daily ATR and roughly 1.6-1.8 one-day sd at RA's 26-32% IV. In HISTORY, 3 of 29 events closed the next day ≥ +1.25 ATR. Phase 1 put p(375/385 settles at or above 385) at 4% (market 7%). The outcome sits in the right tail of both distributions. It does not contradict them.
- Realized vs phase-1 EV: headline spread EV +$35 against a realized ≈ +$600. One draw; uninformative about calibration on its own.

## 4. Phase 3 audit
### (a) Remove each safeguard, one at a time (as-of data; cells = EV $ / EV_B $ and the verdict initial T/W/S)
| Structure | base | no cap | no drift-min | intraday stops | no demotion | convexity | grade B | all toward-flat off | …+intraday stops | …+intraday+convexity |
|---|---|---|---|---|---|---|---|---|---|---|
| Oct9 370C | -24 / +9 S | -24 / +9 S | -24 / +9 S | -1 / -113 S | -24 / +9 S | +114 / +9 W | -24 / +9 S | -24 / +9 S | -1 / -113 S | +48 / -113 W |
| Oct9 372.5C | +19 / +54 W | +19 / +54 W | +19 / +54 W | +9 / -91 S | +19 / +54 W | +111 / +54 W | +19 / +54 W | +19 / +54 W | +9 / -91 W | +44 / -91 W |
| Oct9 375C | +60 / +84 W | +60 / +84 W | +60 / +84 W | +25 / -54 S | +60 / +84 W | +91 / +84 W | +60 / +84 W | +60 / +84 W | +25 / -54 W | +35 / -54 W |
| Oct9 370/375C | +15 / +52 W | +15 / +52 W | +15 / +52 W | +9 / -44 S | +15 / +52 W | +19 / +52 W | +15 / +52 W | +15 / +52 W | +9 / -44 W | +8 / -44 W |
| Oct9 370/380C | +18 / +85 W | +18 / +85 W | +18 / +85 W | +23 / -35 S | +18 / +85 W | +86 / +85 W | +18 / +85 W | +18 / +85 W | +23 / -35 W | +36 / -35 W |
| Oct9 372.5/377.5C | +25 / +58 W | +25 / +58 W | +25 / +58 W | +6 / -34 S | +25 / +58 W | +55 / +58 W | +25 / +58 W | +25 / +58 W | +6 / -34 W | +19 / -34 W |
| Oct9 375/380C | +30 / +47 W | +30 / +47 W | +30 / +47 W | +10 / -17 S | +30 / +47 W | +63 / +47 W | +30 / +47 W | +30 / +47 W | +10 / -17 W | +23 / -17 W |
| Oct9 375/385C | +35 / +46 W | +35 / +46 W | +35 / +46 W | +7 / -15 S | +35 / +46 W | +87 / +46 W | +35 / +46 T | +35 / +46 T | +7 / -15 T | +30 / -15 T |
| Oct12 370/375C | +15 / +24 W | +15 / +24 W | +15 / +24 W | +5 / -35 S | +15 / +24 W | +19 / +24 W | +15 / +24 W | +15 / +24 W | +5 / -35 S | +11 / -35 W |
| Oct12 370/380C | +28 / +74 W | +28 / +74 W | +28 / +74 W | +24 / -33 S | +28 / +74 W | +38 / +74 W | +28 / +74 W | +28 / +74 W | +24 / -33 W | +33 / -33 W |
| Oct16 370/380C | -93 / -65 S | -93 / -65 S | -93 / -65 S | -25 / -36 S | -93 / -65 S | -78 / -65 S | -93 / -65 S | -93 / -65 S | -25 / -36 S | -16 / -36 S |
| Oct16 375/385C | -120 / -67 S | -120 / -67 S | -120 / -67 S | -42 / -33 S | -120 / -67 S | -83 / -67 S | -120 / -67 S | -120 / -67 S | -42 / -33 S | -27 / -33 S |
| Oct16 380/390C | -97 / -36 S | -97 / -36 S | -97 / -36 S | -37 / -30 S | -97 / -36 S | -91 / -36 S | -97 / -36 S | -97 / -36 S | -37 / -30 S | -30 / -30 S |

Classification (the parent's / Fable critic's framing):
| Safeguard | Direction of bias | Effect today | Effect in HISTORY calibration |
|---|---|---|---|
| market+10pp cap | toward flat (one-sided) | **never bound** (history p_t was at or below market+10 on every row) | rarely binds on intraday rows; it bound on 6/10 rows in the daily EV run |
| drift-neutral min / EV_B>0 for TAKE | toward flat | not binding at base. With intraday stops EV_B goes negative on every 1DTE row and would block TAKE | removing it (with the others) created TAKEs that all lost on the intraday sample |
| WATCH→SKIP demotion (EV_B<0) | toward flat (one-way) | not binding at base; binds under intraday stops (all 1DTE rows → SKIP) | **daily breakouts: the 180 demoted rows averaged about +17% of debit (+$9), while the surviving WATCHes averaged −34%.** Anti-predictive there, likely noise |
| grade gate (TAKE needs ≥B; n/a factors = 0 with weight kept) | toward flat | **binding: the only failed TAKE condition for 375/385C.** RA's volume +1 sensitivity → B → TAKE | historically not separable (no historical factor scores); grade B vs C gave identical calibration because the ±10pp band and EV_B bound first |
| ±10pp robustness band + 3% noise floor | toward flat | blocks TAKE on every 1DTE row except 375/385C | with the band, 0 TAKEs across 142 intraday decisions |
| **daily-close stop modelling** | **toward trading** (it flatters) | intraday 15m stops cut EV on the 1DTE rows (375C +60→+25, 375/385C +35→+7, 370/375C +15→+9) and flip EV_B negative on all of them; p_s rises 0.34→0.83 | realized win rate 28%→14%. Matches the Fable critic (28% of target paths stop first on Oct 16) |
| flat-vol market MC vs RA's smile | toward trading on spreads | market-measure EV is +$17-37 on the 1DTE spreads, which is an artifact. Calibrating the MC vol to the debit flips 370/375C and 370/380C to SKIP | n/a |
| entry at mid, ½-spread exit | toward trading | full-spread entry costs $5-10 per spread | n/a |
| bucket valuation (no convexity, no TP) | toward flat | empirical-payoff EV is higher on every 1DTE row (375/385C +35→+87, 370C −24→+114), but each is within 1-1.75 s.e. (s.e. $36-113, n=32) | TP rules (+0.8 ATR or 50% of max) are all within 1 s.e. of zero (table in (b)) |

**Netting it out honestly (today's case).** Remove every toward-flat rule and keep daily stops: 375/385C goes to TAKE at +$35. Also correct the main toward-trade bias (intraday 15m stops): EV +$7, EV_B −$15. It stays a TAKE only because the drift-min was removed; restore the min and it is SKIP. Add convexity: +$30. **So the TAKE/no-TAKE call flips on one judgment (the grade, 0.55 vs 0.60), and the EV it would rest on is $7-35 on a $127 debit with a ±$40-60 standard error.** The safeguards did not suppress a demonstrable edge here. They converted 'no measurable edge, small positive point estimate' into 'WATCH'. The honest-stop correction pushes in the same direction.

### (b) Missing factors: measurable from HISTORY? Do they add lift?
Sample: 29 TSLA 15m-bar events (Feb-Oct 2026) plus 20 older 60m-bar events (Sep 2024-Jan 2026), n=49. Outcome = next-day close vs entry (ATR). Median split (or a natural threshold); bootstrap 95% CI. **About 20 comparisons, so expect about one false 'hit' at 95% by chance.**
| Factor | Measurable? | Split | n hi/lo | Next-day close (ATR) hi vs lo | diff [95% CI] | P(close ≥ +0.4 ATR) hi/lo | Survives 15m-close stop hi/lo | Today |
|---|---|---|---|---|---|---|---|---|
| Level quality: prior touches (±0.3%) | yes | >6.00 | 24/25 | -0.23 vs +0.28 | -0.51 [-0.98, -0.03] | 29%/48% | 17%/32% | 11 |
| Level quality: pivots in cluster | yes | >2.00 | 6/43 | -0.33 vs +0.08 | -0.41 [-1.09, +0.36] | 33%/40% | 17%/26% | 4 |
| Wick depth (ATR) | yes | >0.08 | 24/25 | +0.05 vs +0.01 | +0.04 [-0.44, +0.55] | 42%/36% | 21%/28% | 0.07 |
| Closes below before reclaim | yes | >0.00 | 8/41 | +0.09 vs +0.02 | +0.08 [-0.59, +0.87] | 50%/37% | 25%/24% | 2 |
| Entry vs session VWAP (ATR) | yes | >0.00 | 24/25 | -0.25 vs +0.29 | -0.54 [-1.00, -0.09] | 25%/52% | 29%/20% | -0.16 |
| Intraday momentum: entry − open (ATR) | yes | >-0.23 | 24/25 | -0.15 vs +0.20 | -0.36 [-0.83, +0.11] | 29%/48% | 29%/20% | -0.33 |
| Test-bar relative volume | yes | >1.12 | 24/25 | -0.13 vs +0.18 | -0.31 [-0.79, +0.22] | 25%/52% | 25%/24% | 1.84 |
| Daily trend: prior close − SMA20 (ATR) | yes | >0.00 | 24/25 | +0.16 vs -0.10 | +0.26 [-0.20, +0.77] | 46%/32% | 29%/20% | 0.95 |
| Time of day (entry hour) | yes | >12.00 | 7/42 | +0.38 vs -0.03 | +0.41 [-0.08, +0.97] | 43%/38% | 71%/17% | 13.58 |
| Relative strength vs SPY (open→entry) | yes | >0.00 | 1/5 | +0.04 vs +0.75 | -0.71 [-1.44, +0.27] | 0%/80% | 100%/20% | n/a |
| QQQ relative strength | **no** (no QQQ intraday in PA exports; SPY 5m only from Jul 27, n=6) | | | | | | | n/a |
| Gamma flip / dealer positioning / GEX | **no** (UW has no historical intraday GEX; as-of Oct 8 = NO DATA) | | | | | | | n/a |
| 0-1DTE gamma convexity | yes, as payoff valuation (not a factor) | see (a): +$4 to +$138 vs bucket EV, all ≤1.75 s.e. | | | | | | |

Reading:
- **Candidate signals (CI excludes 0 in at least one sample):** entry *below* VWAP did better (+0.54 ATR, both samples); a deeper intraday selloff into the level did better (15m sample); more prior touches did *worse* (pooled); trend above the daily SMA20 did better (borderline). After-noon entries survived the 15m stop far more often (71% vs 17%, n=7). These point to mean reversion: tested-level springs that come after an intraday flush work better than shallow dips from strength.
- **Today's profile was favorable on 4 of these** (below VWAP −0.16 ATR, momentum −0.33 ATR, trend +0.95 ATR above SMA20, 13:35 entry) and **unfavorable on 2** (11 touches, test-bar volume 1.84x). The framework scored none of them. Its 'structure +1' and 'volume 0' don't capture them.
- **Do they add lift? Not demonstrably.** They were found in-sample on n=49 with about 20 tests, and they have not been validated. They are hypotheses to pre-register and test forward or out of sample. They are not nudges to add today.

Exit-management test (HISTORY 15m events, 1DTE structures at today's ATR geometry, flat IV 0.9×RV20). Mean realized $ (win rate, s.e.):
| Structure | Hold, daily stop (framework) | 15m-close stop | TP at +0.8 ATR / 50% max, else hold | Exit at same-day close | 15m stop + TP |
|---|---|---|---|---|---|
| Oct9 370/380C | +12 (31%, ±100) | -3 (14%, ±63) | -9 (45%, ±76) | -13 (38%, ±48) | -6 (21%, ±46) |
| Oct9 375/385C | +17 (31%, ±69) | -17 (14%, ±42) | +46 (41%, ±57) | +1 (31%, ±40) | -1 (17%, ±37) |
| Oct9 375C | +6 (31%, ±84) | -38 (14%, ±42) | +36 (41%, ±63) | +20 (31%, ±63) | -6 (17%, ±43) |
| Oct9 370/375C | -22 (31%, ±53) | -11 (14%, ±32) | -30 (59%, ±31) | -15 (38%, ±25) | -17 (31%, ±14) |
All within about 1 s.e. of zero: no exit rule creates a demonstrable edge for this setup.

### (c) Calibration: apply the framework mechanically to every historical instance
Method: each HISTORY 15m event is re-run with today's structures mapped to the same ATR offsets. The debit is BS at a flat IV of 0.90×RV20 (today's MID-ATM/RV20 ratio), so the market EV is about −costs. The prior uses **only events resolved before the event date (expanding window; events need ≥5 priors)**, with a leave-one-out variant too. Nudge = 0 (there are no historical factor scores). Market MC uses the same stop rule. Cap, EV_B, the rules and the realized P&L come from the actual forward closes or path. 'SKIP right' means the trade would have lost money net of costs.
| Variant (expanding window) | Decisions (events) | TAKE / WATCH / SKIP | SKIP right / wrong | TAKE: n, win, mean $ | WATCH: n, win, mean $ | All decisions: win, mean $ |
|---|---|---|---|---|---|---|
| framework as run (grade C, daily stops) | 142 (24) | 0 / 24 / 118 | 85 / 33 | — | 24, 29%, -18 | 28%, -29 |
| math-only (grade B assumed), daily stops | 142 (24) | 0 / 24 / 118 | 85 / 33 | — | 24, 29%, -18 | 28%, -29 |
| grade B, intraday stops | 142 (24) | 0 / 0 / 142 | 122 / 20 | — | — | 14%, -10 |
| grade B, no cap/min/demotion, daily stops | 142 (24) | 6 / 21 / 115 | 82 / 33 | 6, 0%, -234 | 21, 33%, +19 | 28%, -29 |
| grade B, no cap/min/demotion, intraday stops | 142 (24) | 2 / 23 / 117 | 99 / 18 | 2, 0%, -138 | 23, 9%, -53 | 14%, -10 |
Leave-one-out (uses later events too, so it has mild lookahead), framework as run: {'WATCH': 61, 'SKIP': 112}; SKIP right/wrong 78/34; WATCH win 20%, mean -83 $. With all toward-flat rules off: 14 TAKEs, 0% win, mean −$202.

Per structure (expanding, framework as run):
| Structure | n | Verdicts | Win rate if always taken | Mean realized $ if always taken (% debit) | SKIP right / wrong |
|---|---|---|---|---|---|
| Oct9 375C | 24 | {'SKIP': 5, 'WATCH': 19} | 33% | +9 (+13%) | 3 / 2 |
| Oct9 370/375C | 24 | {'SKIP': 24} | 33% | +1 (+1%) | 16 / 8 |
| Oct9 370/380C | 24 | {'SKIP': 23, 'WATCH': 1} | 33% | +43 (+11%) | 15 / 8 |
| Oct9 375/385C | 24 | {'SKIP': 23, 'WATCH': 1} | 33% | +18 (+14%) | 16 / 7 |
| Oct12 370/380C | 24 | {'SKIP': 21, 'WATCH': 3} | 29% | -51 (-5%) | 14 / 7 |
| Oct16 375/385C | 22 | {'SKIP': 22} | 5% | -205 (-44%) | 21 / 1 |

Daily breakout calibration (PA daily bars in `inputs/pa_data`, cut at Oct 7; GOOGL, IBIT, PLTR, SPY, TSLA, USO; 20-day-close breakouts, de-clustered; ev_calc rules; IV = RV20 proxy; LOO prior + pool; exit cost 2% of width per leg-side):
| Geometry | Events | Grade C: TAKE/WATCH/SKIP | SKIP right / wrong | SKIP mean (% debit) | WATCH win, mean % | Grade B (math-only): TAKE n, win, mean % | All events: win, mean % |
|---|---|---|---|---|---|---|---|
| 5d (TSLA-row geometry) | 366 | 0/46/320 | 170 / 150 | +9.2% | 26%, -17.1% | 21, 43%, +3.5% | 44%, +5.9% |
| 30d (USO-row geometry) | 163 | 0/67/96 | 77 / 19 | +2.2% | 15%, +1.8% | 2, 0%, -21.0% | 18%, +2.0% |
Brief rule without the demotion (5d geometry, grade B): 205 WATCH averaging +10.4% of debit, against 25 WATCH at −34% once demoted. The demotion removed the better rows. This is a 2020-26 bull sample of watchlist names (selection bias), so treat the +6% 'all events' mean as drift, not edge.

**Sizing the conclusion to n:**
- Intraday setup: 24-29 independent events (the 142-173 'decisions' are 6 correlated structures per event). Distinguishing a 30% from a 40% hit rate needs about 90+ events, so this sample can only rule out large edges. **It shows no large edge, and it shows the framework's SKIP calls were mostly right (72%) on this setup.**
- Oct 8 is n=1. That the framework said WATCH on a day that paid +500% is **no evidence** of bias by itself. At phase 1's own odds, a tail day like this happens about 1 time in 15-25.
- Daily breakouts (366 events): the framework is roughly a coin flip on SKIP (53% right), and its EV_B demotion was anti-predictive. That is the stronger evidence that the verdict layer is mis-specified, though it is not proof of a missed edge.

## 5. Recommended fixes (each testable) and what to keep
Fixes:
1. **Grade on available evidence: renormalise weights over the scored factors, and flag 'insufficient data' instead of scoring n/a as 0 with weight kept.** Test: re-grade the flat_ledger rows both ways and compare the hit rate and realized EV by grade after 30+ rows.
2. **Model stops on the rule Dominic actually trades (5m/15m close, or the wick) in the event study and the market MC.** This removes the main toward-trade bias. Test: realized vs predicted p_s on the ledger.
3. **Make EV_B symmetric, or make it a diagnostic, not a gate.** Either promote and demote, or drop the WATCH→SKIP demotion. Test: the daily-breakout calibration showed the demoted rows at +17% of debit; re-run on the forward ledger.
4. **Replace the fixed ±10pp band + one-sided cap with an n-scaled band (±1 s.e. of p_t) and a two-sided Bayesian blend toward the market** (weight = n/(n+k), k pre-declared, e.g. 30). Test: Brier score / reliability of p_t vs p_mkt on the ledger.
5. **Value the full payoff distribution for 0-1DTE and long calls** (empirical/MC payoff, not 4 buckets), and **price the market benchmark from the debit** (smile-consistent), not a flat leg-mean vol. Test: market-measure EV should equal −costs on every row; check it.
6. **Pre-register an intraday level-test module** (VWAP gap, intraday momentum into the level, touch count, test-bar RVOL, time of day, daily trend) as hypotheses, with a fixed scoring rule. Validate it on the older 60m sample and the forward ledger before it moves any probability.
7. **Start `flat_ledger.csv` now** (RA's proposal): every TAKE/WATCH/SKIP with p_t, p_mkt, reason code, and counterfactual P&L at fixed exits. Review at n ≥ 30 flat calls with a sign test or bootstrap.

Keep:
- Market cross-check with the same stop rule.
- Drift baseline and trigger-lift reporting, as a diagnostic.
- Gamma+flow merged once (no double count).
- Shrinkage on small n.
- Exit costs, the full-spread sensitivity and the correlation bucket.
- Settle-based (not touch-based) probabilities.
- The habit of stating that history ≈ drift.
- The cap never bound today, and it is not the problem on 0-1DTE intraday setups. Its one-sidedness still needs fixing for daily setups.

## 6. Critic
**The CloudAgent critic was NOT launched.** No CloudAgent / launch tool is available in this executor session: a tool-catalog search for cloud|agent|launch returned no matches. Nothing was faked: there is no agent id, no `tsla-blind-20261009` branch, and no CRITIC.md in Planner-Brain. To run it, the parent should launch it with: repo https://github.com/ArazMedia/Planner-Brain, model claude-fable-5-1, model_params {"thinking":"true","effort":"high"}, title 'TSLA blind-test critic', branch tsla-blind-20261009, output CRITIC.md. Attach this report, `tsla_blind/outputs/phase1_verdict.md` (+ .sha256), `tsla_blind/work/*.py` + `*.json`, `inputs/RA_tsla_asof.md`, `RA_tsla_asof_prices.csv`, `PA_tsla_asof.md`, `UW_tsla_asof.md`, `HISTORY_events.csv`, `TSLA_outcome.md`, `RA_audit_notes.md`, and `outputs/CRITIC_fable.md`. **Tell the critic about the leakage items in §1, including RA's web-search exposure to the Oct 8 close.**
