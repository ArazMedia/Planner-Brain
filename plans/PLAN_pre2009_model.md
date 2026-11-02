# PLAN: extend the VIX-spike SPY call-spread backtest to 1990 with a fully model-priced book

Method plan only. No backtest was run. Numbers marked **[computed]** were produced by read-only Python on the attached `VIX_History.csv` and `VIX3M_History.csv`; everything else is an assumption, a design choice, or a source to verify. Existing scripts are not modified; all new work goes into new scripts that reuse `calib_ivsurf.py` (`sidx`, `design`, `wdesign`, `bs_call`, `bs_iv`) and `realq_full_bt.py` (`trade`, `fcn_exit`, `cap_idx`, `port_dd`, fees, `OFF=0.02`) via the same import / `exec`-up-to-marker pattern used by `realq_longhold_bt.py` and `vixlevel_bt.py`.

Strategy under test (unchanged): ~365-DTE SPY call spread, long ATM / short 10% OTM; entry = next open after VIX first closes >30 (or >35) in a spike episode (peak = close >=25 that is the highest close within +/-20 sessions; crossing rule as in `vixlevel_bt.py`); exits = fear curve normal (VIX < 0.85 x VIX3M, 60-session cap) and fixed holds 120/126/189/252 sessions, capped 10 sessions before expiry; fills $0.02 off mid per leg + Webull fees; overlap-aware slot-portfolio drawdown.

## 0. Facts that shape the plan [computed]

- Attached `VIX3M_History.csv` starts **2009-09-18**, not 2007-12. Cboe launched VXV in Nov 2007; whether `cdn.cboe.com` serves rows from 2007-12 is **verify** (step 1). If it does, 2008 becomes available for proxy validation, which is the regime that matters most.
- VIX `OPEN` equals `CLOSE` (OHLC all equal) on every session from 1990-01-02 through 1991-12-31 (505 rows) and on one 2004 session; real opens start 1992-01-02. Next-open repricing via the VIX gap is therefore impossible for 1990-91 entries.
- Calendar gaps >4 days in VIX: 2001-09-10 -> 2001-09-17 (9/11 closure), 2007-01-03, 2012-10-31 (Sandy).
- Pre-2009 peaks >=25: 32. Level-rule episodes with a valid trigger: **21 at >30, 8 at >35, 5 at >40** (list in section 6). At >30, 17 of 21 entries fall within 365 calendar days of the previous entry; max concurrent trades K = 3 (hold 120) / 4 (hold 252). 13 of 21 (>30) and 4 of 8 (>35) entries fall inside the 2000-03..2003-04 or 2007-07..2009-06 bear windows.
- Regression of ln(VIX3M) on VIX-only features, 2009-09..2026-10 (n=4306, in-sample): ln VIX alone R2 0.951, residual sd 0.058 (log); ln VIX + ln MA20 + ln MA120 R2 0.977, residual sd 0.039. Median VIX/VIX3M is 0.884 overall but rises with level: 0.95 at VIX 25-30, 0.99 at 30-40, 1.11 at 40+.
- Day-level agreement of the exit condition (VIX/VIX3M < 0.85) with its proxy (VIX/VIX3M_hat < 0.85): 0.82 for the 3-feature regression; the best single-MA rule (VIX < 0.85 x MA120) agrees 0.77. On the 21 post-2009 >30 entries, the proxy fear-curve exit date differs from the real one by median 6 sessions, but only 62% are within 10 sessions and the max difference is 56 sessions (in-sample fit; 2021-12-02, 2022-01-26, 2024-08-06 and 2020-09-04 are the 50+ session misses). The fear-curve exit is only partially reproducible from VIX alone; see section 2.
- Median 252-session VIX mean 1997-2002 was 23.8 vs 16.4 in 2010-2019: a fixed 30 threshold was a much smaller relative shock in the late 1990s.
- `ivsurf_params.json` holds leave-one-year-out folds for 2010-12, 2014-16, 2018-23; **2013 and 2017 are absent**. Check whether the parquet lacks those years before reusing the fold set.

## 1. 1-year ATM and 10%-OTM IV from VIX alone (replaces VIX3M/6M/1Y)

Keep the two-layer structure of `calib_ivsurf.py` so the surface regression and its validation harness are reused unchanged; only the term-structure input `s_idx(T)` changes.

**Primary (A): regression node model + refit of the surface in "VIX-only" mode.**
1. Stage 1 (new `vix_nodes_model.py`): for each tenor node T in {91, 182, 365} fit on Cboe indices (all available days 2009-09+ for VIX3M, whatever VIX6M/VIX1Y cover; check their first dates on the box):
   `ln s_T = a_T + b_T ln VIX + c_T ln MA20 + d_T ln MA120 + e_T ln MA252 + f_T ln(RV21 / VIX)` where MAk = k-session mean of VIX close, RV21 = 21-session close-to-close realized vol of the underlying (SPX/10 pre-1993, SPY after; section 3). All features exist from 1991 (MA252 warm-up) and are computable at the open (use VIX open, MAs as of trigger close). Fit in logs, weighted x3 on the post-spike regime (VIX 18-45) to match the existing weighting. Drop `f_T` if it does not cut OOS error by >=0.2 vol pt at the 1y node.
2. Stage 2: run `calib_ivsurf.fit` with `s = sidx(dte, VIX, v3_hat, v6_hat, v1y_hat)` in place of the real indices (a `--vixonly` flag on a new `calib_ivsurf_vixonly.py` that imports from `calib_ivsurf.py`). `design()` is unchanged: its skew terms (`x`, `x*L`, `x*v`, `x^2`...) depend only on DTE, moneyness and VIX, so the ATM-vs-10%-OTM skew is already VIX-only. Optional extra column `s*m`, `m = ln(VIX/MA120)`, lets the surface level respond to the mean-reversion state; keep only if LOYO error at 1y ATM improves >=0.2 vol pt.
3. Next-open entry: compute nodes from the VIX open directly (stage 1 with VIX open, MAs from the trigger close). This replaces the `dv*sqrt(30/tenor)` shift. Check on 2010-2023 that entry mids agree with the current shift method within the model's own error.
4. Write `data/ivsurf_params_vixonly.json` with the same layout (`iv`, `width`, `loyo`) plus a `nodes` block so `realq_full_bt.model_quote` can be swapped by changing `PAR` and the `sidx` inputs only.

**Fallback (B): mean-reverting variance form, 2-3 parameters.** `s_T^2 = theta + (VIX^2 - theta) (1 - e^{-kappa T}) / (kappa T)`, `theta = (lambda x MA252)^2`, kappa and lambda fitted by least squares to the Cboe nodes. Fewer parameters, bounded extrapolation at VIX 60-80 (2008 marks), VIX + MA252 only. Use B when A's node residuals at VIX>45 exceed 2x their regime-average, and always report A vs B for pre-2009 as a sensitivity.

**Baseline to beat:** flat term structure `s_T = VIX` (what a naive 1990 model would do). Report its error alongside A and B so the gain from stage 1 is explicit.

**Skew in the 1990s-2000s:** cannot be validated from free data. Treat the `x`-coefficients as a sensitivity axis (x0.5, x1.0, x1.5 on the three `x` terms). Optional free feature: VXO (OEX, ATM-only, 1986-2021; Cboe `https://cdn.cboe.com/api/global/us_indices/daily_prices/VXO_History.csv` **verify**, FRED `VXOCLS` **verify** - discontinued Sep 2021 but FRED keeps discontinued series). VIX/VXO is a crude skew-premium proxy available for the whole pre-2009 window; include `ln(VIX/VXO)` in the `x` terms only if it lowers OOS 10%-OTM 1y error by >=0.3 vol pt on 2010-2021; otherwise use it as a plausibility check on pre-2009 skew.

## 2. Fear-curve exit without VIX3M

Proxies, in order of preference:
1. `v3_hat` from stage 1 (T=91). Exit when `VIX < 0.85 x v3_hat`. Same object as the pricing model, so one validation covers both.
2. Pure moving-average rule `VIX < 0.85 x MA120` [computed best single-MA match]. Simpler, but it is a different rule, not a proxy; label it "VIX-only exit" and keep it as a defined-in-advance alternative rule for 1990-2026, not as a stand-in for the curve.
3. VXV/VIX3M backfill: only 2007-12+ at best (**verify** on cdn.cboe.com); nothing free before Nov 2007. If 2007-12..2009-09 exists, add it to the validation set (covers 2008).

Validation vs real VIX3M (2009-09+, out-of-sample by year, run on the >30 and >35 entries):
- Signal agreement: day-level agreement of `ratio<0.85` vs proxy on the first 60 sessions after each entry; **pass >= 0.85** (in-sample whole-period value is 0.82, so expect this to be borderline).
- Exit-date difference: `proxy_exit - real_exit` in sessions; **pass if >= 70% within +/-10 sessions and |median signed difference| <= 3**. In-sample value is 62% within 10 [computed], i.e. currently failing.
- P&L impact: re-run the 2009+ fear-curve trades with proxy exits, same entries; **pass if |mean(ret_proxy - ret_real)| <= 3 return pts and the IQR of the difference <= 10 pts**.
- Decision rule: if any criterion fails, pre-2009 fear-curve rows are published flagged "proxy exit, not validated" and the headline pre-2009 results are the fixed holds (120/126/189/252), which need no VIX3M. Do not tune the 0.85 threshold on the proxy to force agreement.

## 3. Underlying, dividends, rates

- 1993-01-29 onward: SPY unadjusted OHLC and cash dividends, yfinance `SPY` with `auto_adjust=False` (free, no sign-up; same source as `spy_ohlc_raw.csv`). Trailing-12m `Dividends.rolling('365D').sum()/Close` as today. First 12 months (1993) fall back to the index yield below.
- 1990-01 to 1993-01: `^GSPC`/10 via yfinance (daily OHLC from 1927). Caveat: SPX "open" in that era is the first index print, which uses previous closes for stocks not yet open, so it sits near the prior close and understates gaps; SPY open is a traded print. Since VIX open is also unavailable until 1992 [computed], treat 1990-91 entries as **close-anchored**: price the entry at the next session's close with that close's VIX (consistent inputs), flag `anchor='next_close'`, and report pre-2009 results with and without the 1990-91 entries (3 of 21 at >30, 2 of 8 at >35). For 1992 use the real VIX open with SPX open, flagged.
- Dividend yield pre-1993 (and 1993 warm-up): Shiller monthly `ie_data.xls` (`http://www.econ.yale.edu/~shiller/data.htm`): trailing-12m D / P, forward-filled daily. Cross-check: multpl.com S&P 500 dividend yield by month (**verify**, scrape, no sign-up). Alternative SPX daily source if Yahoo opens look bad: Stooq `^spx` (previously blocked by a JS challenge per `vix_dip_summary.md`; **verify**); Kenneth French daily `Mkt-RF`+`RF` (free, no sign-up) only for a realized-vol cross-check, not for prices.
- Rates: `r` = FRED `DTB3` (continuous, as today; already on the box, 1954+). Sensitivity: FRED `DGS1` (1-year CMT, 1962+) since the option is 1y and 1990 rates were ~8%: report the mean per-trade return difference DTB3 vs DGS1.
- Tick size: SPX options traded in 1/16 (<$3) and 1/8 (>=$3) until options decimalization completed in 2001; on SPX/10 that is $0.00625-$0.0125, below the $0.01 of the model grid, so the fill convention (`OFF=0.02`) dominates and no explicit tick model is needed. Strike grid for synthetic chains: SPX LEAPS strikes were 25 pts apart ($2.50 on SPX/10); with SPY at $40-150 the existing `$5 if DTE>200` grid is too coarse (12% of a $40 spot), so use `g = 1 if S < 150 else 5` for LEAPS pre-2009 and keep `listed_expiries()` (standard third-Friday monthlies plus Mar/Jun/Sep/Dec/Jan beyond 240 days; SPX LEAPS in the 1990s were listed on a December cycle (**verify**), so also run a Dec-only variant and report the DTE actually obtained).

## 4. Bid-ask and fills, 1990s-2000s

No free source of historical SPX/SPY LEAPS quotes is known to me; this stays an assumption with sensitivity runs. Use the existing width model (depends on DTE, moneyness, VIX, mid) scaled by an era multiplier `m`:

| Era | Instrument actually available | m (base) | Sensitivity |
|---|---|---|---|
| 1990-1992 | SPX options only, fractional ticks, pre-LEAPS liquidity thin | 3.0 | 2, 4 |
| 1993-2000 | SPX LEAPS; SPY exists but has no options | 2.5 | 1.5, 3.5 |
| 2001-2004 | SPX decimalized, no SPY options | 2.0 | 1.5, 3 |
| 2005-2008 | SPY options listed Jan 2005; SPY LEAPS listing date **verify**; penny pilot for SPY from 2007 | 1.5 | 1, 2 |

Report for every era and multiplier: `ret` ($0.02 off mid, as today), `cross_ret` (hit bid / lift offer, already computed by `trade()`), and `mid_ret`. Additionally scale the per-leg offset with width: `OFF_era = max(0.02, 0.25 x half_width)` as a third fill mode. Pre-2005 the instrument is a synthetic "SPX/10 call" (European, cash-settled, 10x SPY notional). Implications to state in the output: (a) minimum ticket is 10 SPY-equivalent contracts, so the "slot" sizing is coarser than the model assumes; (b) European exercise means BS, which is what the model legs use anyway; (c) the Webull per-contract fee is ~1/10 per SPY-equivalent and immaterial; (d) the result is "what the quoted index option would have returned", not a record a retail account could have produced in 1995.

## 5. Validation on 2010-2023 real quotes with pre-2009-available inputs only

Inputs allowed: VIX (close and open), VXO, realized vol, SPX/SPY prices and dividends, DTB3/DGS1. Forbidden: VIX3M/6M/1Y, real chain for contract selection (use `listed_expiries` + grid), VIX3M-based shifts.

1. Leg level (`realq_full_bt.py model` / `loyo` machinery with `PAR` = VIX-only params): IV error (model - real) by DTE bucket and moneyness as in `calib_ivsurf.py`'s report, plus a VIX>45 stress bucket (2020-03 and a few 2011-08 sessions are the only real-quote samples of that regime). **Pass**: in the post-spike regime, 1y ATM median |error| <= 1.0 vol pt in-sample and <= 1.5 OOS; 1y 10% OTM <= 1.5 / 2.0; VIX>45 bucket <= 3.0 OOS; width median |log error| <= 0.35.
2. Trade level: for every real-quote episode and every exit rule, model return vs real return on identical dates (contracts chosen by the model grid; also run with the real contracts to separate selection error from pricing error). Report mean/median bias, IQR, p10-p90, sign agreement, Spearman rank correlation. **Pass**: |median bias| <= 5 return pts on Hold 120 (the current full model is ~5 pts optimistic, so the VIX-only model should not be worse than 7); sign agreement >= 85%; rank correlation >= 0.90; fold-to-fold bias sd <= 3 pts.
3. Walk-forward: train on years < Y, test Y, for Y = 2014..2023 (expanding), in addition to LOYO. Pre-2009 is a pure extrapolation backwards, so the expanding-window degradation (bias drift per year added) is the most relevant number; **pass** if OOS bias in walk-forward is within 2 pts of LOYO bias.
4. Bias correction: estimate on LOYO OOS trade residuals per exit rule. Apply only if the sign is the same in >= 10 of 12 folds and |bias| > 2 pts; apply as a reported shift (publish raw and corrected columns), never inside the pricing function. Carry the OOS p10-p90 band to the pre-2009 tables as the error band of every mean/median.
5. Stage-1 node model: validate separately on Cboe indices (more years than the parquet): OOS-by-year RMSE of ln(v3), ln(v6), ln(v1y); **pass** if 1y node residual sd <= 0.06 log and no year's mean residual exceeds 0.05.

## 6. Episodes 1990-2008 [computed], overlap, regimes

Level rule applied to all pre-2009 peaks (the existing `vixlevel_bt.py` iterates over curve-signal episodes only, so 2009+ counts can differ by one). Entry = session after the trigger.

| Peak date (VIX) | >30 trigger -> entry | >35 trigger -> entry | Regime note |
|---|---|---|---|
| 1990-08-23 (36.5) | 08-06 (35.9) -> 08-07 | 08-06 (35.9) -> 08-07 | Gulf War; no VIX open; SPX bottomed 10-11 |
| 1990-10-11 (34.0) | 09-06 (30.2) -> 09-07 | - | same war drawdown, overlaps |
| 1991-01-14 (36.2) | 01-08 (30.4) -> 01-09 | 01-14 (36.2) -> 01-15 | Desert Storm; no VIX open |
| 1997-10-30 (38.2) | 10-27 (31.1) -> 10-28 | 10-30 (38.2) -> 10-31 | Asian crisis one-day crash |
| 1997-12-24 (30.3) | 12-24 -> 12-26 | - | marginal crossing |
| 1998-10-08 (45.7) | 08-21 (33.1) -> 08-24 | 08-27 (38.6) -> 08-28 | LTCM; SPX fell another ~10% to 10-08 |
| 1998-12-14 (31.3) | 12-14 -> 12-15 | - | |
| 1999-01-14 (33.0) | 01-13 (30.1) -> 01-14 | - | Brazil |
| 2000-04-14 (33.5) | 04-14 -> 04-17 | - | bear starts |
| 2000-10-12 (30.5) | 10-12 -> 10-13 | - | bear |
| 2000-12-20 (31.7) | 12-20 -> 12-21 | - | bear |
| 2001-04-03 (34.7) | 03-12 (30.3) -> 03-13 | - | bear |
| 2001-09-20 (43.7) | 09-07 (31.0) -> **09-10** | 09-17 (41.8) -> 09-18 | >30 entry is the session before the 9/11 closure; next mark is 09-17 |
| 2002-08-05 (45.1) | 07-09 (30.2) -> 07-10 | 07-15 (35.0) -> 07-16 | bear bounce |
| 2002-10-07 (42.6) | 08-27 (30.1) -> 08-28 | 09-03 (40.0) -> 09-04 | bear, final low 10-09 |
| 2003-01-27 (34.7) | 2002-12-19 (30.2) -> 12-20 | - | pre-Iraq, bear ends 03-2003 |
| 2007-08-16 (30.8) | 08-15 (30.7) -> 08-16 | - | quant quake |
| 2007-11-12 (31.1) | 11-12 -> 11-13 | - | bear starts |
| 2008-01-22 (31.0) | 01-22 -> 01-23 | - | bear |
| 2008-03-17 (32.2) | 03-14 (31.2) -> 03-17 | - | Bear Stearns |
| 2008-11-20 (80.9) | 09-15 (31.7) -> 09-16 | 09-29 (46.7) -> 09-30 | Lehman; marks during hold at VIX 60-80 are extrapolation |

Also >40 (5): 1998-09-01, 2001-09-18, 2002-07-23, 2002-09-20, 2008-10-03. 1987 excluded (no VIX).

Overlap: with 1y holds, 1990-91, 1997-99, 2000-03 and 2007-08 are clusters (K up to 4). Use the existing slot portfolio; also report the "first entry per cluster" subset (entries >= 252 sessions after the previous entry) so the n is honest. Regime pitfalls: (i) 13/21 of >30 entries are inside bear markets, so expect clustered losses; the 2009-2026 sample has no multi-year bear, so a drop in win rate is the expected finding, not a model bug; (ii) 9/11: the 09-10 entry cannot be exited before 09-17; set the first exit-eligible session to 09-17 and flag; VIX and SPX gaps over the closure violate the next-open repricing assumptions; (iii) 1998 and 2002 bear bounces: the >30 trigger fires 25-33 sessions before the peak, so entries are early in the run-up; (iv) 2008-09-16: hold-252 exits in 2009-09, through the March 2009 low; model width at VIX 80 is unvalidated; (v) 1990s baseline VIX ~23: consider reporting a relative trigger (VIX > 1.5 x MA252) as a sensitivity, not as a replacement.

## 7. Outputs the future run should produce

- `data/`: `spx_ohlc_1990_1993.csv`, `shiller_divyield_monthly.csv`, `vxo_history.csv` (if found), `dgs1.csv`, `vix3m_backfill_2007.csv` (if found).
- `data/vix_nodes_vixonly_params.json`, `data/ivsurf_params_vixonly.json` (same layout as `ivsurf_params.json`, plus `nodes`, `loyo`, `walkforward`).
- Validation: `valid_vixonly_legs.csv`, `valid_vixonly_trades.csv`, `valid_vixonly_summary.md` (pass/fail per criterion in section 5), `fcn_proxy_validation.csv` (+ summary rows for section 2 criteria).
- Backtest: `leaps_pre2009_episodes.csv` (columns as `leaps_vixlevel_episodes.csv` plus `era`, `anchor`, `instrument` (SPX10/SPY), `width_mult`, `fill_mode`, `node_model` (A/B/flat), `exit_flag`), `leaps_pre2009_summary.csv`, `leaps_1990_2026_summary.csv` (combined, by era and level, raw and bias-corrected columns with p10-p90 band), `leaps_pre2009_sensitivity.csv` (width x fill x skew x rate x node model), PNG tables via `render_pro_table` with the assumptions in the notes.

## 8. Ordered checklist

1. Download and check first/last dates: Cboe VIX3M/VIX6M/VIX1Y (`https://cdn.cboe.com/api/global/us_indices/daily_prices/<IDX>_History.csv`), VXO (verify), FRED DTB3/DGS1/VXOCLS, yfinance `^GSPC` and `SPY` (auto_adjust=False), Shiller `ie_data.xls`. Record every source and date range in the summary.
2. Check why 2013 and 2017 have no LOYO folds; fix the fold set before any refit.
3. Fit stage 1 (A, B, flat) on Cboe indices; node validation (section 5.5).
4. Refit the surface in VIX-only mode; leg-level and trade-level validation incl. LOYO and walk-forward (sections 5.1-5.4); decide bias correction.
5. Fear-curve proxy validation on 2009+ entries (section 2); decide flag.
6. Build the 1990-2008 input frame (SPX/10 then SPY, q, r, MAs, RV21, VXO), episodes per section 6, 9/11 and 1990-91 anchoring rules.
7. Run pre-2009 with the sensitivity grid of section 4 and the skew/rate/node-model axes; produce section 7 outputs.
8. Combine with 2009-2026, publish raw and corrected results with bands; write the caveats section below into the summary.

## 9. What could make this misleading

- Every pre-2009 price is a model output; no leg was ever quoted. Mean returns are only as good as the 2010-2023 fit, extrapolated backwards 20 years into a different market-structure and skew regime.
- The 1-year node has the shortest real history, and the 2008 and 1990s term structures were never observed; the mean-reversion state (MA features) is doing the work.
- The fear-curve exit is a proxy with a 62% in-sample hit rate within 10 sessions [computed]; its pre-2009 P&L could differ materially from what the real curve would have produced.
- Bid-ask widths are assumptions; a 2.5x width at 1y moneyness 1.10 can erase a meaningful part of the spread's premium. Always read the cross-fill column.
- Pre-2005 the instrument did not exist for SPY; the synthetic SPX/10 result is a price-history statement, not an executable track record.
- Sample is small (21 / 8 entries), clustered, and bear-heavy; win rates on 8 entries have a +/-30 pt binomial band.
- 1990-91 entries lack opens (VIX and effectively SPX); the 9/11 entry is priced across a closure.
- Selection effect: a fixed 30 threshold fires more often when baseline VIX is high (late 1990s), tilting the pre-2009 sample toward bear-market entries.
- Any bias correction is itself estimated on 2010-2023 and may not transfer.
