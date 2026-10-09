# PA base rates: setups for 20261009-ev (TradingView history only)
_PA, Fri 2026-10-09, ~13:10 ET._

**Data.** Source is TradingView PA Analyst (ADJ off; splits adjusted, as TV always does), BATS feed for stocks. No yfinance; `sd-stats/session_stats.py` was not used because it fetches yfinance. Raw bars are in `pa_data/` as `[t,o,h,l,c,v]` epoch-second JSON. Scripts: `pa_data/es.py` (event engine), `run.py`, `deep.py`/`deep2.py` (history paging by zooming back, no `tv range`). Per-event detail: `pa_data/es_detail.json`. CSV: `PA_baserates.csv`.

| File | Bars | Span | Note |
|---|---|---|---|
| USO_1D.json | 1,506 | 2020-10-12 → 2026-10-09 | |
| GOOG_1D.json | 1,599 | 2020-06-01 → 2026-10-09 | |
| GOOGL_1D.json | 1,599 | 2020-06-01 → 2026-10-09 | |
| PLTR_1D.json | 1,514 | 2020-09-30 → 2026-10-09 | full history |
| SPY_1D.json | 1,599 | 2020-06-01 → 2026-10-09 | RA asked for ~500; this has more |
| IBIT_1D.json | 689 | 2024-01-11 → 2026-10-09 | full history |
| BTCUSD_1D.json | 1,999 | 2021-04-19 → 2026-10-08 (UTC days) | BITSTAMP |
| TSLA_1D.json | 1,599 | 2020-06-01 → 2026-10-09 | |
| **SPY_5m.json** | 10,155 | 2026-07-27 → 2026-10-09 = **54 sessions** RTH+ETH | Paging stopped growing at ~10.2k bars, so **60 sessions was not reachable** |

The last bar of each daily file is today's bar, still forming (~13:00 ET).

## Event definitions (mechanical)
- **Breakout (up)**
  - *Level:* a 5-bar pivot high (highest high within ±5 days), 10–250 trading days old.
  - *Tested:* at least one later daily high within 1.5% under the level, without a close above it.
  - *Event:* the **first daily close above the level** (prior close ≤ level, close ≤ 3% above).
  - *De-duplication:* one event per day (the level nearest the close), events at least 5 days apart.
- **Breakdown (down):** the mirror on 5-bar pivot lows.
- **Measurement**
  - *Distances:* targets and stops are % distances from the **level**, scaled to today's trigger → strike/stop distances.
  - *Target:* "hit" = an **intraday high (low)** reaches the target within the horizon.
  - *Stop:* "stop" = a **daily close** beyond the fail distance. If the target and the stop happen on the same day, it counts as the target.
  - *Columns:* `p_stop_first` = stopped before the first (smallest) target; `p_stop_any` = a stop close at any time in the window, including after targets.
  - *Completeness:* only events with a complete horizon are counted.
- **BTC/IBIT:** **daily-SMA50 test & hold** = day low ≤ SMA50, close > SMA50, prior 3 closes > SMA50. Measured from the event close. Stop = a close 2.75% under the event close (the 80,526 distance from ~82.8K).
- **TSLA**
  - *Flip-retest hold:* within 15 days after a breakout event, the first day with low ≤ level +1% and close ≥ level.
  - *388.55-type:* a close above the prior 20-day high.
  - Both are measured from the event close: targets +2.5/+5/+10%, fail = a close 3% under.

**Caution.** Small targets (<2%) are often hit intraday on the next day. Those rates mostly measure ordinary noise, not edge. Read `p_stop_first` and the far targets.

## Results

### USO: daily close >148.07 (fail <147.12 = −0.64%); 29 trading days to Nov 20
**n = 39** (2020-10 → 2026-09).

| Target | Distance | Hit rate | Median days |
|---|---|---|---|
| 150 | +1.30% | **74%** | 1 |
| user's +1.8% | +1.8% | 64% | 1 |
| 152.5 (mid of 150/155) | +2.99% | 54% | 2 |
| 155 | +4.68% | **46%** | 3 |
| 160 | +8.06% | **36%** | 8.5 |

- **Stop:** stop before 150 = **26%**. A stop close at any point in the window = 69% (the fail line is very tight; most events close under it at some point).
- **Regime:** close > SMA50: n = 36, 72 / 42 / 31% (150 / 155 / 160), stop-first 28%.
- **Volume:** trigger-day volume ≥ 20d average: n = 22 → 82 / 45 / 32%, stop-first 18%. Below average: n = 17 → 65 / 47 / 41%, stop-first 35%.
- **Level quality**
  - 148.07 ±0.5% was touched on **19 days** since 2026-04-29, with 6 of the last 8 sessions in the band. 147.12 was touched 21 times.
  - It's a heavily worked shelf, not a clean single pivot. The trigger is only 0.64% above the fail line, inside one ATR.
- **Regime now:** close 147.59 > SMA50 139.15 > SMA200 117.12 (strong uptrend). ATR **3.66%** (the fail band is 0.17 ATR, so expect noise stops).
- **Trigger status / volume:** no daily close >148.07 yet. Today's volume is 0.26x the 20d average at ~13:00 ET (partial).

### GOOGL (spreads are on GOOGL): GOOG 350.09 / 337.96 converted
- **Method**
  - *Structural (used for the trigger):* GOOG 350.09 is the 2026-10-01 daily high (350.0935). GOOGL's high that day was **353.22**, the GOOGL trigger.
  - *Ratio (used for the fail level):* 337.96 has no exact GOOG bar match (nearest close 337.75 on 04-23). So the fail level uses the current ratio GOOGL/GOOG = 1.01012 → **341.38**.
  - *Ratio, for reference:* the ratio gives trigger 353.63.
- **Setup:** GOOGL trigger daily close >353.22; fail close <341.38 (−3.35%); 29 trading days. **The window includes the Oct 28 earnings (not isolated; n too small).**
- **Results (n = 42, 2020-06 → 2026-09)**

| Target | Distance | Hit rate | Median days |
|---|---|---|---|
| 355 | +0.50% | 95% | 1 |
| 360 | +1.92% | **86%** | 1 |
| 365 | +3.34% | **69%** | 3 |
| 370 | +4.75% | **64%** | 5 |

- **Stop:** stop-first **5%**; stop close at any time 48%.
- **Regime:** close > SMA50 > SMA200: n = 29, 97 / 79 / 76% (360 / 365 / 370), stop-first 0%.
- **Volume:** trigger volume ≥ 1x: n = 26, 81 / 62 / 58%, stop-first 19%. Below 1x: n = 16, 94 / 81 / 75%, stop-first 6%. No volume edge; low-volume breakouts did better, inside small n.
- **Level quality:** 353.22 ±0.5% has 28 touch days since 2026-04-27, with 4 of the last 6 sessions. A well-defined, repeatedly tested ceiling.
- **Regime now:** GOOGL 354.24 (above the trigger intraday; not a close yet) > SMA50 346.30 > SMA200 340.04. ATR 2.45%.
- **Status:** today's volume 0.32x (partial).

### PLTR: >204.4 → 207.5–210 by Oct 16 (5 trading days); fail = close back under the level
**n = 25** (2020-09 → 2026-09).

| Target | Distance | Hit rate |
|---|---|---|
| 205 | +0.29% | 92% |
| 207.5 | +1.52% | **92%** |
| 210 | +2.74% | **84%** |

- Median 1 day.
- **Stop:** stop-first **8%**; a close back under the level within 5 days **64%**. Breakouts usually extend first, then often come back to the level.
- **Regime:** uptrend subset n = 15: 93 / 87%, stop-first 7%.
- **Volume:** ≥ 1x: n = 21, 90 / 81%. Below: n = 4 (too few).
- **Level quality:** 204.4 = the 2025-10-31 / 11-03 highs (one-year-old ATH area). Only 4 touch days, so a clean, rarely tested level. The breakout is above an old high.
- **Regime now:** 205.47 > SMA50 176.91 > SMA200 152.31 (very extended: +16% over SMA50). ATR 2.89%.
- **Volume:** today 0.88x (partial, strong pace).

### SPY bull: >779.27 → 781 by Oct 16 (5 days); fail = close <0.56% under (774.90)
**n = 42.**

| Target | Hit rate |
|---|---|
| 781 (+0.22%) | **98%** |
| 781.62 (+0.30%) | **93%** |

- Median 1 day. Stop-first **2%**; stop any 26%.
- **Regime:** uptrend subset n = 26: 96 / 89%.
- **Volume:** ≥ 1x n = 14: 100%. Below n = 28: 96%.
- The +0.22% target is inside one day's range (ATR 0.80%), so this is close to a given once the trigger closes. The spread payoff depends on the **close** at expiry, not the touch; RA/Planner should model the settle.
- **Level quality:** 779.27 had 9 touch days since 2026-08-05 (zone top; ATH 781.62 on 10-06).

### SPY bear: <774.90 → 767 by Oct 16 (5 days); fail = close >0.56% above (779.27)
**n = 27.**

| Target | Hit rate |
|---|---|
| 771 (−0.50%) | **74%** |
| 767 (−1.02%) | **56%** |

- Median 1 day. Stop-first **26%**; stop any 70%.
- **In an uptrend at the event (today's regime): n = 2. Unusable.** Breakdowns of tested lows in the data mostly happened in down/sideways regimes.
- **Level quality:** 774.90 had 25 touch days since 2026-08-04 (his red pivot inside the zone).
- **Regime now:** SPY 778.29 > SMA50 767.57 > SMA200 722.93. ATR **0.80%**.
- **Volume:** today 0.21x (partial).

### IBIT 46 → 49 by Nov 20: daily-SMA50 test & hold (today's BTC pattern)
- **BTC proxy** (Bitstamp, 2021-04 → 2026-10, 42 calendar-day bars ≈ 29 trading days), **n = 24**:
  - Reaches +1.28% (IBIT 47.5) **79%**; +4.48% (IBIT 49) **46%**, median 2 days.
  - Stop (−2.75% close) before 47.5: **21%**; stop at any time 75%.
  - With close > SMA200 (today's regime): n = 16, 75 / **31%**, stop-first 25%.
- **IBIT itself** (2024-01 → 2026-10), **n = 7**: 57 / 43%, stop-first 43%. Close > SMA200: n = 5. **Too small; use the BTC row.**
- **Regime now:** BTC 82,714 > SMA50 80,720 > SMA200 71,857. ATR 2.43%. IBIT 46.84 > SMA50 43.07 > SMA200 41.87; ATR 2.55%.
- The 49 short strike needs about +4.5% from 46.9. The proxy says roughly a third to a half, with a high chance of a −2.75% close at some point.

### TSLA (no spread yet)
| Event | Horizon | n | +2.5% | +5% | +10% | Stop-first (−3% close) | Median fwd return | % up |
|---|---|---|---|---|---|---|---|---|
| Flip-retest hold (370-type) | 5d | **10** | 40% | 30% | 20% | 30% | +0.16% | 60% |
| Flip-retest hold (370-type) | 20d | **10** | 60% | 50% | 40% | 40% | +4.78% | 80% |
| Close above 20-day high (388.55-type) | 5d | 58 | 60% | 50% | 36% | 36% | +0.74% | 57% |
| Close above 20-day high (388.55-type) | 20d | 58 | 62% | 55% | 41% | 38% | +3.44% | 60% |

- **381 retest:** the 381 line is a falling trendline, so there's no horizontal analog. Its retest behaves like the flip-retest row (small n). TSLA is a wide-swing name: stop-first runs 30–40% in every variant.
- **Level quality**
  - 370.25 ±0.5%: 35 touch days since 2024-12 (a strong multi-year flip level).
  - 381: 47 touch days.
  - 388.55: 50 touch days since 2024-12 (a congested band, many touches; not a clean single level).
- **Regime now:** 383.35 > SMA50 354.76 but **< SMA200 390.61**, a mixed regime. ATR 2.88%.

## Honest limits
- **Generic analogs:** the events are generic analogs on the same name, not his exact levels. Overlapping/nearby levels are de-duplicated but not independent.
- **Small n:** n ≥ 25 for USO, GOOGL, PLTR, SPY bull/bear and the BTC proxy. **n < 15 for the IBIT direct test, SPY-bear-in-uptrend (2) and the TSLA retests (10).** Shrink those hard toward a prior.
- **Settle-based payoff:** "hit" is an intraday touch. Spread value at expiry depends on the settle, so p(touch) overstates p(settle ≥ strike), especially for tight SPY / PLTR targets.
- **Same-day ties:** count as a target hit. That is optimistic when a day both spikes up and closes under the fail line.
- **Earnings:** GOOGL earnings (10-28), and any USO / EIA / CPI event days, are not isolated.
