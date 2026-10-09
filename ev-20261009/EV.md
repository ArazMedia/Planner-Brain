# EV evaluation: Dominic's debit-spread setups, Fri 2026-10-09
Planner (executor), 20261009-ev. **This is a proposal only.** No orders, no broker, no risk.md edits. Dominic sets the size and risk per trade.
Account context: $7,700 cash, Level 3, defined-risk debits only, no margin. Dominic prefers flat over weak evidence.
Generated 2026-10-09 13:05 ET by `outputs/ev_calc.py` and `outputs/make_report.py`. Table: `outputs/ev_table.csv`.
Inputs present: PA_baserates.md, UW_flowhist.md, RA_factors.md, RA_spy_baserates.md, RA_tsla.md, RA_mkt_probs.md. **Inputs missing: none.**

## 0. Bottom line
- **No TAKE.** Nothing has an edge that survives the honesty checks, so **flat is the default.** That matches Dominic's preference for flat over weak evidence.
- **2 WATCH, both conditional:**
  - **TSLA Oct16 385/390C.**
    - Grade B. EV +$40 (+17%); drift-neutral +$18; EV ≥ 0 across ±10pp.
    - Only on a 15m close >386.82 holding VWAP, with a re-quoted full-spread debit ≤ ~$243. RA's hard cap is $260.
    - It's the single tech+CPI-bucket pick.
  - **USO Nov20 150/160C.**
    - Grade C. EV +$68 (+20%); drift-neutral +$12.
    - Only if today's daily close is >148.07.
    - It's a cheap-lottery profile: about 73% stop-outs at a ~$96 loss each against the 147.12 stop.
- **SKIP the other 8**, including PLTR Oct16, which fired but is negative on a settle basis (only 4 of 25 analog breakouts settled at the target). SPY bull and GOOGL 355/365 have +EV only from sample drift.
- **Where the edge is:** essentially nowhere demonstrable.
  - The breakout trigger adds −3 to +4pp over plain drift.
  - The market prices every spread so its EV ≈ −exit costs.
  - Every positive EV comes from history beating the market by ~10pp (it's capped there). Read the EVs as "if the 2020–26 tape repeats", not as edge.

## 1. Source check (each number checked against the files; mismatches flagged)
| Item | Given in the task / 02_plan | What the sources say | Flag |
|---|---|---|---|
| USO trigger | daily close >148.07 | Same (WATCHLIST, 1210-pa). 4h 08–12 C148.79; daily close still pending | ok |
| **USO fail** | <147.12 | **In PA/WATCHLIST, 147.12 is the *early 4h trigger*, not a fail level.** PA's floor warning is <141.76 and the kill is a daily close <134.34–136.57 | **MISMATCH.** I used 147.12 as the plan says, as a daily close. It sits only 0.18 ATR under the entry, so ~78% of historical paths stop out. A sensitivity with a 141.76 stop is shown |
| USO debits | $192.50 / $337.50 | $192.50 / $337.50 at the 12:47 snapshot (the 150/160 was $330 at 10:05 and $367.50 at 12:09). Full-spread fills are $225 / $365 | ok; volatile quote |
| **GOOGL levels** | >350.09, <337.96 | **These are GOOG chart levels.** The spreads are GOOGL, which is +3.675 vs GOOG in the same CBOE snapshot | **MISMATCH (RA correction 1). Resolved:** PA's native GOOGL levels are used: trigger daily close >353.22, fail close <341.38. (The provisional GOOG+3.675 conversion to 353.77/341.64 is withdrawn.) GOOG and GOOGL bars are never mixed. The daily close is pending (GOOGL ~354.2 intraday) |
| GOOGL debits | $437.50 / $392.50 | Same, at the snapshot | ok |
| Catalysts | CPI 10/14, EIA 10/15, GOOGL ER 10/28 | Confirmed: CPI **Wed** 10/14 08:30 (BLS), EIA Thu 10/15 12:00 (Columbus Day shift). **Missing from the task list:** FOMC 10/27–28 (inside every Nov 20 expiry), PPI 10/15, PLTR ER Nov 2 or Nov 9 (unconfirmed; inside Nov 20), TSLA ER 10/21 AMC (after Oct 16) | add FOMC/PPI/PLTR ER |
| PLTR | >204.4, tgt 207.5–210, 205/210C $220 | PA level 204.42 (fired intraday, 4h C205.45 at 3.70x). **The 207.5–210 target comes from UW gamma (CW 210), not a PA target.** PA fail: 4h close <204.42 | ok; target source noted |
| SPY | bull >779.27 → 778/781C $152; bear <774.90 → 775/767P $170.50 | Same at spot 778.11. **Entry only happens at the trigger, so the debit there is different:** bull ≈$165, bear ≈$243 (BS repriced at the trigger, calibrated to the snapshot mid). Bear fail = close back above 779.27 (PA definition; the earlier assumed 777 is withdrawn). Both triggers need a **DAILY** close (RA v2) | debit at trigger used |
| BTC/IBIT | Nov20 46/49C ~$138 | $138 at 12:09; **$137 at the 12:53 snapshot used here**. RA: **trade cancelled by Dominic (10:04)**. Entry trigger (15m close >47.16) not fired | cancelled; scored for completeness |
| TSLA | levels only | RA proposes Oct16 385/390C, $195 mid / $205 full at 382.80. **At the 386.82 trigger the estimated cost is ≈$233 mid / ≈$243 full**, under RA's $260 cap. ER 10/21 falls after expiry | RA spread used, debit at trigger |
| SPY daily bars | RA: "no SPY 1D in any PA export" | `/workspace/pa-agent/macro_review/20261008/raw/ohlcv_1D_SPY.json` (260 bars) existed, and PA's `inputs/pa_data/SPY_1D.json` (2020→) has since landed | told RA via this report |
| session_stats.py | base-rate tool | **Imports yfinance** (`yf.Ticker(...).history`), so it was **not run**, per the no-outside-data rule. The SPY base rates come from RA's PA-bar script plus my daily study | tool unusable under the rule |

**Single quote snapshot (RA correction 2):** every debit, mid, IV and delta comes from the CBOE delayed chains saved in `/workspace/plans/20261008-goog-uso-mu-watch/data/1247/`. USO/GOOGL/PLTR/SPY were pulled 12:47 ET (quotes ≈12:32 ET). IBIT/TSLA were pulled 12:53 ET (quotes ≈12:38 ET). Debit = the snapshot mid. The full-spread fill is shown as the worst case.

## 2. Method (pre-declared in `ev_calc.py`; nothing fitted)
1. **Prior (PA price history only, TradingView exports, no yfinance).**
   - Event: a daily close above the prior 20-day high (bull) or below the 20-day low (bear), de-clustered.
   - Strikes and the fail level are placed at today's ATR(14) multiples from the entry.
   - Path rule: the first daily close through the fail level = **STOP**. Otherwise, at expiry (H = 5 sessions for Oct 16, 30 for Nov 20), the close decides: ≥ short strike = **TARGET**, between the strikes = **PARTIAL**, otherwise **OTM** (no stop hit, expires ~0).
   - 4h fail levels (PLTR, SPY, TSLA) are approximated by daily closes. That makes the stop slower than Dominic's real rule, which flatters p_t a little.
2. **Shrinkage.** A Dirichlet prior centred on the pooled rate (the same study on all 11–12 PA names; GOOG and GOOGL are never pooled together). Weight W = 10 if own n < 15, else 5. p_k = (count_k + W·pool_k)/(n + W).
3. **Factor gate.** RA's scores and weights (`RA_factors.csv`), grade A ≥1.2 / B 0.6–1.2 / C 0–0.6 / D −0.6–0 / F <−0.6.
   - The log-odds nudge on p_t uses only factors that aren't already in the prior: volume, trend, and **one merged positioning term**. That term is RA's gamma and flow, weighted by their weights, and counted once at the larger of the two weights, so dealer positioning isn't counted twice.
   - Nudge = 0.5·clip(dir/2, −1, 1), so |nudge| ≤ 0.5. Structure is the trigger type the prior already conditions on, so it isn't nudged. Catalyst, IV and liquidity work through the variance and the costs, not direction.
4. **Market cross-check.** N(d2) with each strike's IV (RA_mkt_probs agrees), **plus** a risk-neutral Monte Carlo at the chain IV with the **same stop rule**. That is the like-for-like comparison, because a tight stop removes most terminal-ITM paths. If our p_t is more than 10pp above the MC market p_t, it is **cut** to market +10pp.
5. **EV** = Σ p_k (V_k − debit).
   - V_target = width·100 − exit cost.
   - V_partial = the MC mean intrinsic of in-between paths − exit cost.
   - V_stop = the Black–Scholes spread value at (fail − the mean historical close-through overshoot), at the pooled median stop day, − exit cost.
   - V_OTM = 0.
   - Exit cost = ½ the bid/ask of each leg ×100. UW doesn't give leg widths, so these are CBOE snapshot widths. **Exit-cost assumption:** entry at the snapshot mid, exit pays ½ the quoted bid/ask per leg. Sensitivities: 2x exit cost (the full bid/ask per leg), plus a full-spread entry. UW positioning tags replace RA's gamma/flow only as a sensitivity and are never added on top. UW's USO dark-pool study is excluded (it used yfinance).
   - Also reported: break-even p_t, EV at p_t ±10pp (the other buckets rescale), and EV at a full-spread fill.
6. **Drift-neutral EV (B), added after the first pass showed the problem (see §5).** It starts from the risk-neutral MC buckets, adds the measured **trigger lift** (event p_t − drift-only p_t from the same names), then applies the same factor nudge.
7. **Verdict rules (BRIEF, plus two stated tightenings).**
   - **TAKE:** EV > 0 across ±10pp, grade ≥ B, trigger fired, **and** drift-neutral EV > 0.
   - **WATCH:** EV > 3% of the debit at the base case and grade ≥ C (trigger pending or not robust).
   - **SKIP:** otherwise. D/F grades are SKIP regardless of EV, because flat beats weak evidence. |EV| < 3% of the debit counts as zero.
   - **Ranking** is by the conservative min(EV, drift-neutral EV).
   - **Correlation (RA correction 4):** PLTR, TSLA, GOOGL and SPY bull form one tech+CPI bucket, so pick at most one.

## 3. Ranked table
| # | Setup | Bucket | Grade (score) | p_t / p_p / p_s(+OTM) | mkt p_t (same stop rule) | Debit (snapshot mid) | EV $ (% debit) | BE p_t | EV @ p_t −band / +band (10pp; GOOGL 15pp) | EV_B drift-neutral | Verdict (BRIEF rule → final) | Trigger / status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | TSLA Oct16 385/390C | tech+CPI | B (+0.80) | 44% / 6% / 50%(+1%) | 34% CAPPED | $233 (full $243) | +$40 (+17%) | 33% | +$1 / +$78 | +$18 | WATCH → **WATCH** | 15m close >386.82 holding VWAP (fail: 15m close <381, hard 1h <380); RA spread, skip if full > ~$260; CPI inside, ER 10/21 after expiry — not fired (15m close >386.82 holding VWAP; PA 12:10: confirmation failed, 383.94 under VWAP) |
| 2 | USO Nov20 150/160C | USO | C (+0.05) | 20% / 7% / 73%(+0%) | 10% CAPPED | $338 (full $365) | +$68 (+20%) | 10% | -$3 / +$139 | +$12 | WATCH → **WATCH** | daily close >148.07 (fail: daily close <147.12) — pending (daily close >148.07 today) |
| 3 | PLTR Oct16 205/210C | tech+CPI | B (+0.95) | 25% / 14% / 58%(+3%) | 25% | $220 (full $230) | +$3 (+1%) | 24% | -$33 / +$38 | +$32 | SKIP → **SKIP** | hold >204.4 (fail: 4h close <204.42; modelled as daily close); target 207.5-210 — fired intraday (broke 204.42, 4h C205.45 at 3.70x); retest-hold pending |
| 4 | SPY Oct16 778/781C (bull) | tech+CPI | C (+0.20) | 49% / 16% / 28%(+7%) | 39% CAPPED | $165 (full $167) | +$22 (+13%) | 39% | -$0 / +$43 | -$7 | WATCH → **SKIP** | DAILY close >779.27 (RA v2: a 4h/intraday poke is not enough; PA: >1x vol) (fail: close <774.90); CPI 10/14 inside — not fired (needs a DAILY close >779.27; 777.87 at 12:21, 778.29 PA ~13:00) |
| 5 | GOOGL Nov20 360/370C | tech+CPI | D (-0.10) | 34% / 7% / 52%(+7%) | 24% CAPPED | $392 (full $420) | +$65 (+17%) | 25% | -$51 / +$182 | -$8 | SKIP → **SKIP** | GOOGL daily close >353.22 (PA native; = GOOG 350.09); fail GOOGL close <341.38; ER + FOMC 10/28 inside — pending (GOOGL daily close >353.22; above it intraday ~354.2) |
| 6 | IBIT Nov20 46/49C | IBIT | D (-0.20) | 22% / 3% / 75%(+0%) | 20% | $137 (full $139) | +$1 (+1%) | 21% | -$19 / +$22 | -$9 | SKIP → **SKIP** | 15m close >47.16 w/ BTC >82,714 (stop: close -2.75% = IBIT ~45.53 / BTC 80,526, PA def; setup-invalid 46.25) — entry trigger not fired (15m close >47.16 on vol); RA 12:09 lists the trade as CANCELLED |
| 7 | GOOGL Nov20 355/365C | tech+CPI | C (+0.00) | 36% / 5% / 54%(+5%) | 26% CAPPED | $438 (full $460) | +$60 (+14%) | 27% | -$52 / +$172 | -$10 | WATCH → **SKIP** | GOOGL daily close >353.22 (PA native; = GOOG 350.09); fail GOOGL close <341.38; ER + FOMC 10/28 inside — pending (GOOGL daily close >353.22; above it intraday ~354.2; GOOG 4h 08-12 C349.55 missed) |
| 8 | PLTR Nov20 200/210C | tech+CPI | B (+0.85) | 10% / 0% / 90%(+0%) | 11% | $490 (full $505) | -$17 (-4%) | 13% | -$73 / +$40 | +$30 | SKIP → **SKIP** | hold >204.4 (fail: 4h close <204.42, modelled as daily close); PLTR ER (Nov 2 or 9) INSIDE expiry — fired intraday (broke 204.42, 4h C205.45 at 3.70x); retest-hold pending |
| 9 | USO Nov20 150/155C | USO | D (-0.05) | 21% / 3% / 76%(+0%) | 11% CAPPED | $192 (full $225) | +$6 (+3%) | 19% | -$28 / +$40 | -$19 | SKIP → **SKIP** | daily close >148.07 (fail: daily close <147.12) — pending (daily close >148.07 today; 4h 08-12 C148.79) |
| 10 | SPY Oct16 775/767P (bear) | SPY | C (+0.00) | 13% / 13% / 66%(+8%) | 21% | $243 (full $244) | -$45 (-19%) | 19% | -$114 / +$24 | -$3 | SKIP → **SKIP** | DAILY close <774.90 (RA v2) (fail: close >779.27, PA def); CPI 10/14 inside — not fired (needs a DAILY close <774.90) |

Sensitivity (not ranked): USO with PA's floor-warning 141.76 as the stop instead of 147.12

| Setup | p_t / p_p / p_s | EV $ (% debit) | EV ±10pp | EV_B |
|---|---|---|---|---|
| USO Nov20 150/155C [sens: fail 141.76] | 33% / 5% / 59% | +$18 (+9%) | -$21 / +$56 | -$18 |
| USO Nov20 150/160C [sens: fail 141.76] | 30% / 10% / 57% | +$89 (+26%) | +$12 / +$167 | +$18 |

Other sensitivities: UW positioning tag used *instead of* RA gamma/flow (never added on top), 2x exit costs (full bid/ask per leg), full-spread entry, and RA SPY settle priors

| Setup | UW tag | p_t with UW pos | EV with UW pos | EV 2x exit cost | EV full-spread entry | EV with RA SPY prior (raw / capped at mkt+10) |
|---|---|---|---|---|---|---|
| TSLA Oct16 385/390C | +0 | 41% | +$30 | +$30 | +$30 | – |
| USO Nov20 150/160C | -1 | 20% | +$68 | +$40 | +$40 | – |
| PLTR Oct16 205/210C | +0 | 22% | -$5 | -$7 | -$7 | – |
| SPY Oct16 778/781C (bull) | +1 | 49% | +$22 | +$20 | +$20 | +$39 / +$28 |
| GOOGL Nov20 360/370C | +0 | 34% | +$65 | +$40 | +$38 | – |
| IBIT Nov20 46/49C | +0 | 27% | +$11 | -$1 | -$1 | – |
| GOOGL Nov20 355/365C | +0 | 36% | +$60 | +$39 | +$38 | – |
| PLTR Nov20 200/210C | +0 | 9% | -$23 | -$32 | -$32 | – |
| USO Nov20 150/155C | -1 | 21% | +$6 | -$27 | -$27 | – |
| SPY Oct16 775/767P (bear) | +0 | 14% | -$36 | -$46 | -$47 | -$7 / -$7 |

p_s(+OTM) = the stop-out probability, with the no-stop-but-OTM probability in brackets. Together they are the loss buckets.

## 4. Probability build (prior → shrink → nudge → market check)
| Setup | Own-name sample | n own: t/p/OTM/stop | n pool | Pool p_t | Drift-only p_t (no trigger) | Trigger lift | W | Prior p_t | Dir score -> nudge (log-odds) | Nudged p_t | Mkt p_t: N(d2) / MC w/ stop | Edge vs mkt (pp) | Final p_t |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TSLA Oct16 385/390C | PA event def (b20), settle-based, 2020-06-30..2026-08-31 | 58: 24/3/0/31 | 497 | 40% | 40% (n=3786) | +0pp | 20 | 41% | +0.94 -> +0.23 | 47% | 43% / 34% | +13 | 44% (cut to mkt+10) |
| USO Nov20 150/160C | PA event def (level), settle-based, 2020-11-23..2026-05-19 | 39: 9/3/0/27 | 223 | 18% | 14% (n=3682) | +3pp | 5 | 22% | +0.43 -> +0.00 | 22% | 29% / 10% | +13 | 20% (cut to mkt+10) |
| PLTR Oct16 205/210C | PA event def (level), settle-based, 2021-06-02..2026-09-23 | 25: 4/4/1/16 | 497 | 31% | 28% (n=3786) | +3pp | 5 | 18% | +1.38 -> +0.38 | 25% | 36% / 25% | -0 | 25% |
| SPY Oct16 778/781C (bull) | PA event def (level), settle-based, 2020-07-20..2026-08-03 | 42: 21/7/3/11 | 497 | 43% | 44% (n=3786) | -0pp | 5 | 49% | +0.28 -> +0.11 | 52% | 45% / 39% | +13 | 49% (cut to mkt+10) |
| GOOGL Nov20 360/370C | PA event def (level), settle-based, 2020-07-06..2026-08-03 | 42: 16/3/3/20 | 192 | 34% | 33% (n=3164) | +1pp | 5 | 38% | +0.03 -> -0.09 | 36% | 35% / 24% | +12 | 34% (cut to mkt+10) |
| IBIT Nov20 46/49C | PA event def (sma_hold), settle-based, 2021-11-15..2026-08-10 | 24: 6/0/0/18 | 223 | 29% | 29% (n=3682) | -1pp | 20 | 27% | -0.71 -> -0.27 | 22% | 35% / 20% | +2 | 22% |
| GOOGL Nov20 355/365C | PA event def (level), settle-based, 2020-07-06..2026-08-03 | 42: 18/2/2/20 | 192 | 36% | 36% (n=3164) | +0pp | 5 | 42% | +0.03 -> -0.09 | 40% | 39% / 26% | +14 | 36% (cut to mkt+10) |
| PLTR Nov20 200/210C | PA event def (level), settle-based, 2021-06-02..2026-08-04 | 24: 1/0/0/23 | 223 | 21% | 18% (n=3682) | +2pp | 5 | 7% | +1.38 -> +0.38 | 10% | 43% / 11% | -2 | 10% |
| USO Nov20 150/155C | PA event def (level), settle-based, 2020-11-23..2026-05-19 | 39: 11/1/0/27 | 223 | 18% | 16% (n=3682) | +2pp | 5 | 27% | +0.43 -> +0.00 | 27% | 37% / 11% | +16 | 21% (cut to mkt+10) |
| SPY Oct16 775/767P (bear) | PA event def (level), settle-based, 2020-09-08..2026-07-23 | 27: 4/2/2/19 | 275 | 13% | 16% (n=3786) | -3pp | 20 | 14% | -0.66 -> -0.11 | 13% | 25% / 21% | -8 | 13% |
| USO Nov20 150/155C [sens: fail 141.76] | PA event def (level), settle-based, 2020-11-23..2026-05-19 | 39: 16/2/1/20 | 223 | 32% | 32% (n=3682) | -0pp | 5 | 40% | +0.43 -> +0.00 | 40% | 37% / 23% | +17 | 33% (cut to mkt+10) |
| USO Nov20 150/160C [sens: fail 141.76] | PA event def (level), settle-based, 2020-11-23..2026-05-19 | 39: 14/4/1/20 | 223 | 30% | 28% (n=3682) | +1pp | 5 | 35% | +0.43 -> +0.00 | 35% | 29% / 20% | +16 | 30% (cut to mkt+10) |

## 5. Where the edge is (plainly)
**Plainly: no setup shows a demonstrated edge.** The evidence:

1. **The market prices these spreads close to fair.**
   - In a risk-neutral Monte Carlo at the chain IV, with the same stop rule, EV is between −$4 and −$29 for every spread. That's just the exit costs. (SPY bear shows +$29, but that's an artifact of the flat-IV MC vs the skew; see caveats.)
   - The break-even p_t is within about 1pp of the market's p_t on every row. So any +EV needs the market to be wrong about direction.
2. **History says "yes, by ~10pp", but that's drift, not the trigger.**
   - Same names, same path rule, entering on any day with no trigger: p_t comes out nearly the same.
   - Pooled trigger lift is −3 to +3pp. Own-name lift with PA's event definitions is −9 to +12pp, at n = 24–58, which is noise.
   - The history is 2020–26 on names chosen *because* they're on today's watchlist (GOOGL/PLTR/TSLA/SPY all ran hard). That's survivorship plus hindsight selection.
3. **Six of the ten rows hit the cap.** Our p_t was more than market +10pp and was cut to exactly market +10. For those rows the EV isn't really an estimate: it's "the EV if you believe the market is 10pp too bearish".
4. **Drift-neutral EV (B)** strips the drift by starting from market odds + the measured trigger lift + RA's factor nudge. It's positive only for:
   - TSLA (+$18): flow/gamma nudge
   - USO 150/160 (+$12): structure of the payoff and trend nudge
   - PLTR Oct16 (+$32) and PLTR Nov (+$30): volume/flow nudge

   Those nudges are pre-declared judgments, never calibrated on outcomes.
5. **So, if there's an edge anywhere:**
   - It's in **TSLA**, on its trigger. It's the only row positive in A, in B, and across ±10pp. UW calls TSLA flow two-way (tag 0, vs RA's +2), and with UW's tag the EV falls to +$30.
   - **USO 150/160** is the other WATCH: positive in A and B, but −$3 at −10pp, and UW's tag is −1 (sold-call build at 153 and call walls at 151/154 between the strikes). The cap already binds, so the tag doesn't change the EV.
6. **Correlation:** PLTR, TSLA, GOOGL and SPY bull are one tech+CPI bucket, so take at most one: TSLA, conditionally.

## 6. Payoff inputs per setup
| Setup | Width | Exit cost (½ bid/ask per leg) | V_target | V_partial (MC mean intrinsic) | V_stop (BS at fail − overshoot, med stop day) | Stop dist (ATR) | Strikes long/short (ATR from entry) | IV long / RV20 | Factors (RA scores; pos = merged gamma+flow) |
|---|---|---|---|---|---|---|---|---|---|
| TSLA Oct16 385/390C | 5 | $10 | $490 | $253 | $92 (day 2, overshoot 0.54 ATR) | 0.53 | -0.17 / 0.29 | 37.9% / 30.6% | struct=+0;vol=+0;trend=+1;gamma=+1;flow=+2;pos=+1.5;cat=+0;iv=+0;liq=+2;iv_rv_rule=-1 (RA_factors.csv) |
| USO Nov20 150/160C | 10 | $28 | $972 | $517 | $241 (day 2, overshoot 0.65 ATR) | 0.18 | 0.36 / 2.21 | 45.1% / 40.6% | struct=+1;vol=+0;trend=+1;gamma=+0;flow=+0;pos=+0;cat=-1;iv=+0;liq=+0;iv_rv_rule=+0 (RA_factors.csv) |
| PLTR Oct16 205/210C | 5 | $10 | $490 | $260 | $112 (day 2, overshoot 0.54 ATR) | 0.26 | -0.16 / 0.68 | 41.3% / 24.3% | struct=+1;vol=+2;trend=+1;gamma=+1;flow=+1;pos=+1;cat=+0;iv=-1;liq=+2;iv_rv_rule=-2 (RA_factors.csv) |
| SPY Oct16 778/781C (bull) | 3 | $2 | $298 | $155 | $56 (day 2, overshoot 0.55 ATR) | 0.7 | -0.2 / 0.28 | 9.7% / 9.9% | struct=+0;vol=+0;trend=+0;gamma=+1;flow=+0;pos=+0.75;cat=-1;iv=+0;liq=+2;iv_rv_rule=+0 (RA_factors.csv) |
| GOOGL Nov20 360/370C | 10 | $28 | $972 | $484 | $187 (day 6, overshoot 0.58 ATR) | 1.47 | 0.68 / 1.83 | 34.6% / 24.4% | struct=+1;vol=+0;trend=+1;gamma=-1;flow=+0;pos=-0.6;cat=-1;iv=-1;liq=+1;iv_rv_rule=-1 (RA_factors.csv) |
| IBIT Nov20 46/49C | 3 | $2 | $298 | $169 | $90 (day 5, overshoot 0.61 ATR) | 1.08 | -0.69 / 1.83 | 37.3% / 39.2% | struct=+1;vol=+0;trend=+0;gamma=+0;flow=-2;pos=-1.6;cat=-1;iv=+0;liq=+2;iv_rv_rule=+0 (RA_factors.csv) |
| GOOGL Nov20 355/365C | 10 | $22 | $978 | $496 | $230 (day 6, overshoot 0.58 ATR) | 1.47 | 0.1 / 1.26 | 34.6% / 24.4% | struct=+1;vol=+0;trend=+1;gamma=-1;flow=+0;pos=-0.6;cat=-1;iv=-1;liq=+2;iv_rv_rule=-1 (RA_factors.csv) |
| PLTR Nov20 200/210C | 10 | $15 | $985 | $731 | $417 (day 3, overshoot 0.66 ATR) | 0.26 | -1.0 / 0.68 | 54.8% / 24.3% | struct=+1;vol=+2;trend=+1;gamma=+1;flow=+1;pos=+1;cat=-1;iv=-1;liq=+2;iv_rv_rule=-2 (RA_factors.csv) |
| USO Nov20 150/155C | 5 | $32 | $468 | $241 | $123 (day 2, overshoot 0.65 ATR) | 0.18 | 0.36 / 1.28 | 45.1% / 40.6% | struct=+1;vol=+0;trend=+1;gamma=+0;flow=+0;pos=+0;cat=-1;iv=+0;liq=-1;iv_rv_rule=+0 (RA_factors.csv) |
| SPY Oct16 775/767P (bear) | 8 | $2 | $798 | $405 | $64 (day 2, overshoot 0.49 ATR) | 0.7 | -0.02 / 1.27 | 10.1% / 9.9% | struct=+0;vol=+0;trend=-1;gamma=-1;flow=+0;pos=-0.75;cat=+0;iv=+1;liq=+2;iv_rv_rule=+0 (RA_factors.csv) |
| USO Nov20 150/155C [sens: fail 141.76] | 5 | $32 | $468 | $226 | $75 (day 6, overshoot 0.64 ATR) | 1.17 | 0.36 / 1.28 | 45.1% / 40.6% | struct=+1;vol=+0;trend=+1;gamma=+0;flow=+0;pos=+0;cat=-1;iv=+0;liq=-1;iv_rv_rule=+0 (RA_factors.csv) |
| USO Nov20 150/160C [sens: fail 141.76] | 10 | $28 | $972 | $490 | $152 (day 6, overshoot 0.64 ATR) | 1.17 | 0.36 / 2.21 | 45.1% / 40.6% | struct=+1;vol=+0;trend=+1;gamma=+0;flow=+0;pos=+0;cat=-1;iv=+0;liq=+0;iv_rv_rule=+0 (RA_factors.csv) |

## 7. Per-setup notes
**UW_flowhist.md integration.**
- RA's factor scores **already contain flow and gamma**, so UW's tags were **not added on top**. They were used only as a *replacement* sensitivity for the merged positioning term (see the "Other sensitivities" table).
  - Where p_t is capped (TSLA, USO, SPY bull, GOOGL), the tag changes nothing.
  - Uncapped rows: PLTR Oct16 drops to −$5 with tag 0, and IBIT rises to +$11 with tag 0 vs RA's −2. Both are SKIP anyway.
- **UW has no bid/ask** (Mr. Whale "NO DATA"). Exit costs use the **CBOE snapshot bid/ask**: ½ the spread per leg on exit, entry at mid. Shown alongside are 2x exit cost (full bid/ask per leg) and a full-spread entry.
- UW's flow-setup history is n = 0 (Whale NO DATA), so it isn't used.
- **UW's USO dark-pool study is excluded** because it used yfinance prices.
- New facts UW added that RA didn't score:
  - USO Nov 153C short-call build (OI 360 → 8,954) and call walls 151/154 between the strikes.
  - SPY IVR 9.3 (cheap).
  - IBIT CW 47.5 below the 49 short strike.
  - PLTR leg flow is opening but with mixed sides.

**Per setup:**
- **TSLA Oct16 385/390C. B. WATCH, conditional on the 386.82 trigger.**
  - PA "close above 20-day high", settle-based with a close <381 as the stop: n = 58, 24 target / 3 partial / 31 stopped. Hard-shrunk (W = 20) per PA's flag.
  - Nudge +0.23 (RA: flow +2, gamma +1, merged into one term). Capped at market 34% + 10 = 44%.
  - The debit is BS-estimated **at the trigger**: ~$233 mid / ~$243 full, not today's $195. Re-quote.
  - UW: 385C flow two-way (BID $1.58M vs ASK $1.44M, both vol > OI). On the flip 381.2, CW 390 (= short strike).
  - ER 10/21 falls after expiry. CPI 10/14 is inside.
- **USO Nov20 150/160C. C. WATCH (pending the daily close >148.07).**
  - PA tested-pivot events, settle-based: n = 39, 9 target / 3 partial / 27 stopped.
  - On PA's whipsaw note: I stop on **any** close <147.12 before expiry, not "stop first". The stop is 0.17 ATR away, so about 73% of paths stop out. Each stop costs only ~$96, because the spread keeps time value: the residual is ~$241 after an overshoot of 0.64 ATR.
  - The 150/160 beats the 150/155: paths that survive the tight stop for 30 sessions are strong trends that usually clear 160 too. The 155C is also thin (OI 1,490) with $32.50 full-spread slippage.
  - With PA's 141.76 floor as the stop, EV is +$89 and holds across ±10pp.
  - EIA 10/15, CPI and FOMC are inside, and the Iran reply is a two-way gap risk.
- **PLTR Oct16 205/210C. B. SKIP as a chase.**
  - Fired intraday.
  - PA's settle sample (n = 25): 4 target / 4 partial / 16 closed back under 204.42. PA's 84% *touch* of 210 does not translate to the settle.
  - History EV +$3 (noise); drift-neutral +$32 is all nudge; −10pp gives −$33.
  - Re-check only on a held retest of 204.4.
- **PLTR Nov20 200/210C. B. SKIP.** Over 30 sessions, the close-under-204.42 stop hits 23 of 24 events, and ER (Nov 2/9) is inside.
- **SPY Oct16 778/781C. C. BRIEF rule = WATCH → final SKIP (critic rule: drift-neutral EV −$7).**
  - **Reconciliation with RA v2:**
    - RA (daily-close trigger, n = 59, settle measured vs the **level**, no stop): raw 0.71/0.05/0.24 → RA prior **0.60/0.10/0.30**.
    - Mine (PA pivot events, n = 42, strikes measured from the event **close**, stop on a close <774.90): 21/7/3/11, so p_t 0.50 → shrunk 0.49 → cap 0.49.
  - **Why the ~11pp gap:**
    - (a) Measuring settle from the level gives a head start to events that closed well above it. PA allows up to +3%, and SPY's ATR is 0.87%. I measure from the close, where the spread is actually bought.
    - (b) My stop exits 28% of paths early at a residual.
    - (c) Different event definitions: tested pivot vs L-day high near the ATH.
  - Using RA's prior: EV +$39, or +$28 with p_t capped at market settle +10 (0.55). Same sign, same weakness.
  - RA: 47–49% of breaks close back under 779.27 within 5 days. The 780 pin caps the settle near $200 of $300. CPI is inside.
  - If the trigger is only intraday, use market odds (0.41): EV ≈ −costs.
- **SPY Oct16 775/767P. C. SKIP.**
  - At the 774.90 trigger the spread costs ~$243, not $170.50 (that price was from 778).
  - Mine: −$45. With RA's 0.20/0.15/0.65 prior: −$7. Both negative.
  - Fail = close >779.27 (PA's definition; my earlier assumed 777 is withdrawn).
- **GOOGL Nov20 355/365C (C, re-scored) / 360/370C (D). SKIP.**
  - PA native levels 353.22 / 341.38 (my provisional GOOG+3.675 conversion is withdrawn).
  - Settle n = 42: 18 target / 20 stopped. Capped at market +10.
  - The ±15pp band (ER not isolated) gives −$52 to +$172. Drift-neutral −$10 / −$8.
  - UW: the 355 magnet sits at the long strike, the 370C is closing, and IVR is 54 with ER + FOMC 10/28 inside.
- **IBIT Nov20 46/49C. D. SKIP.** Dominic cancelled it at 10:04. BTC-proxy SMA50-hold events, n = 24, hard-shrunk. EV +$1 (noise); drift-neutral −$9.
- **USO Nov20 150/155C. D. SKIP.** EV +$6 (3%, noise). With a full-spread entry it's −$27.

## 8. Caveats
- **Sample bias.** PA history runs 2020–26 on names picked *because* they're on today's watchlist. That's a strong bull sample, so any history-based p carries drift and hindsight selection. See §5 and the drift-neutral column.
- **Small n.** Every n here is ≤ 58. The pool only adds generic breakouts (n ≈ 190–500). The rows are overlapping and correlated, not independent.
- **Stops are approximated.** 4h and 15m fail rules (PLTR, SPY, TSLA) are modelled as daily closes. That's slower than Dominic's real stop: it understates stop-outs and overstates partial/target.
- **Stop-residual assumptions.** The stop residual is Black–Scholes at (fail − the historical mean overshoot ≈0.55–0.67 ATR), at the pooled median stop day, with today's leg IVs.
  - It ignores IV changes. IV crush after GOOGL ER or after CPI would lower it.
  - Gaps through the stop would also lower it.
- **Exit costs** = ½ the snapshot bid/ask per leg. Deep-ITM spreads near expiry often quote wider. Entry is assumed at mid; the full-spread fill EV is in the CSV (`EV_fullfill`).
- **Debits at the trigger** (SPY, TSLA) are BS estimates calibrated to the snapshot. Re-quote when the trigger fires.
- **Single snapshot.** All debits come from CBOE delayed chains (12:47 ET, quotes ≈12:32; IBIT/TSLA 12:53, ≈12:38). Quotes have moved since (the USO 150/160 ran $330 → $367.50 → $337.50 today).
- **Catalysts not isolated.** CPI 10/14, PPI 10/15, EIA 10/15, FOMC 10/27–28, GOOGL ER 10/28 and PLTR ER Nov 2/9 are all left un-isolated in the base rates. The Iran/Hormuz reply is "within days".
- **Correlation.** The tech+CPI bucket (PLTR/TSLA/GOOGL/SPY bull) is one bet on CPI and tech beta.
- **Base-rate tool.** `session_stats.py` was not used (it imports yfinance). No outside price data was used anywhere.
- **Factor nudges** (±0.5 log-odds max) are RA's scores turned into odds by a pre-declared mapping. They are not calibrated against outcomes. RA kept PA's breakout rates out of the factor scores, so the prior and the nudge don't overlap. The structure factor isn't nudged either.
- **UW_flowhist.md** landed ~13:04 ET and is integrated as a sensitivity (see §7). UW flow-setup history is n = 0.
- **SPY bear market-measure EV is +$29.** That's a model artifact: the MC uses one flat IV (the mean of the legs), while the debit at the trigger is repriced per-leg with skew (767P 11.3% vs 775P 10.1%). It doesn't change the verdict.
- **The ranking key is min(A, B)** and is only meaningful among WATCH rows. The SKIP rows are ordered for reference.

## 9. Critic
**The CloudAgent critic was NOT launched.** No CloudAgent/launch tool is available in this executor session (a tool-catalog search for cloud/agent returned nothing). Per the task, **I ran the critique pass myself**. There is no agent id and no `ev-20261009` branch or CRITIC.md in Planner-Brain. If Planner wants the independent Fable critic, launch it from the parent with EV.md, ev_calc.py, ev_table.csv and inputs/*.

**Self-critique: attacks and what changed**
1. **Double-counted trend → FIXED.**
   - The history prior already embeds 2020–26 drift, and RA's trend factor nudged it again.
   - Now the history EV (A) nudges only on volume and the merged positioning term. Trend stays only in the drift-neutral EV (B).
   - Effect: USO nudge +0.11 → 0. Small elsewhere.
2. **Flow vs gamma vs UW → CHECKED.**
   - Gamma and flow are merged into one positioning term, counted once at the larger weight.
   - UW's tags are a replacement sensitivity, never added on top of RA, because RA's scores already contain flow and gamma.
3. **Touch rates used as p(full width) → AVOIDED.**
   - Every own-name p is settle-based: the close at the 5- or 30-session horizon vs the strikes, with stops on any close through the fail level.
   - PA's touch rates (84–98%) are reported only as context.
4. **Shrinkage.** W = 5 (n ≥ 15), W = 10 (n < 15), and W = 20 for PA-flagged rows (IBIT, SPY bear, TSLA).
   - Weak point: the pool uses a different (generic 20-day-high, ATR-scaled) event type than the own-name PA events.
   - This can pull PLTR's own 4/25 toward a 31% pool. Judged acceptable; stated.
5. **The market cap does most of the work → DISCLOSED.**
   - Six of ten rows sit at market +10pp, so their EV equals "+10pp over the market" by construction. That's why the drift-neutral EV and the trigger-lift columns were added.
6. **Verdict rule tightened → CHANGED.**
   - A WATCH whose drift-neutral EV is negative rests only on sample drift, so it's now SKIP.
   - Effect: **SPY bull and GOOGL 355/365 go from WATCH to SKIP**. The BRIEF-rule verdict is kept alongside in the table.
7. **Debit at the trigger vs today → FIXED earlier.** SPY and TSLA are entered only at their triggers, so their debits are repriced there. The SPY bear moved from $170.50 to ~$243, which alone flips it negative.
8. **Not fixed (open):**
   - 4h/15m stops modelled as daily closes. This is optimistic.
   - IV crush is not in the stop residuals (GOOGL ER, post-CPI).
   - The pool and own-name event types differ.
   - Small n everywhere (≤ 58).
