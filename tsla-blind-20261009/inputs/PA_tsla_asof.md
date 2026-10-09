# PA: TSLA as of 13:40 ET Thu 2026-10-08 (hindsight-free)
Source: TradingView PA Analyst, BATS:TSLA, ETH on, ADJ off.
- Bars come from the `TSLA_*_asof.json` files (identical copies named `*_cut.json`). The last 5m bar is the 13:35 bar, which closed 13:40.
- 15m, 60m and D each end with a **partial** bar rebuilt from those 5m bars:
  - 15m 13:30 (13:30–13:40)
  - 60m 13:00 (13:00–13:40)
  - D 10-08 (RTH 09:30–13:40)
- Volume caveat: intraday bars are BATS-only volume. Daily bars are consolidated, so the D partial's volume (1.77M, BATS) is **not** comparable to the daily average (35.5M consolidated).

## The level: 370.25
Daily bars before 10-08:
- **54 days** traded through 370.25 ±0.5% since 2020-06.
- His Macro green ray sits at **370.17** (anchored 2026-04-14 on 4h).
- 2025-09-12: L 370.24.
- 2026-06-26: daily pivot low 368.60.
- 2026-07-20 / 07-21: C 369.57, L 369.98.
- **Sept 2026 resistance:** 09-08 H 370.00, 09-10 H 369.21, 09-11 H 368.66, 09-18 H 370.90, 09-28 H 369.43. A run of lower highs capped at the level.
- **Flip:** on 10-02 it closed **370.59** (first close above, on 55.3M shares vs a 35.5M 20-day average, 1.56x). On 10-05 it dipped to 364.91, then closed 378.73.
- **Read then:** a multi-month resistance that flipped to support a week ago. This is the first full retest from above.

## Structure into the test (daily, complete bars to 10-07)
- **Closes:** 352.84 (09-29), 354.81, 354.11, 370.59 (breakout), 378.73, 380.68, **377.81** (10-07).
- Three sessions of drift down from the 10-06 high of 383.33.
- **Daily SMAs** (including the 10-08 partial close 370.57): SMA20 **367.57**, SMA50 353.18, SMA200 **391.11**.
  - Above SMA20/50, below SMA200: an intermediate uptrend inside a longer downtrend.
- **ATR14:** 11.09 (3.0%).
- **Today so far (RTH):** O 374.22, H 375.93, L 368.04, last 370.57, which is −7.24 (−1.9%) vs the 377.81 prior close.
- **Premarket:** 376.66 / 373.23.

## Intraday into the level (10-08)
- **15m sequence:**
  - Opening bars 09:30–09:45 (2.6–2.9x the day's 15m average): H 375.93, fading.
  - 10:00–12:30: a tight 371.5–373.9 range on falling volume.
  - **12:45 15m** broke the range low (L 370.94, C 371.20, 143k ≈ 1.5x).
  - 13:00 (L 369.75, 137k).
  - **13:15** (L 368.04, C 369.12, 131k, ≈1.4x).
  - The selling expanded into the level.
- **Test bar:** 5m **13:25**, O 369.65 / **L 368.04** / C 369.12, 57.6k shares (**1.84x** the day's 5m RTH average of 35.4k).
  - That was a 2.21 (0.60%) wick under 370.25 and 2.13 under his 370.17.
  - The low equals the 15m 13:15 low and the 1h 13:00 low.
- **Reclaim:**
  - 13:30 5m: C 369.99 (L 368.94, a higher low), 23.6k (0.67x).
  - **13:35 5m: C 370.57** (L 369.88), 17.4k (0.49x). This is the first 5m close back above 370.25.
  - The reclaim came on **shrinking** volume: sellers stopped, but buyers hadn't stepped in hard.
- **VWAP (RTH, 5m hlc3 × vol): 372.39.** Price is 1.82 under it, below VWAP since ~12:45.

## Moving averages at 13:40 (last bar close 370.57)
| TF | SMA20 | SMA50 | SMA200 | Read |
|---|---|---|---|---|
| 5m | 371.52 | 372.25 | 375.17 | below all three; 5m downtrend |
| 15m (13:30 partial) | 372.49 | 374.47 | 377.98 | below all three |
| 1h (13:00 partial) | 375.06 | 377.92 | **369.91** | sitting on the 1h SMA200 (support confluence) |
| D (partial) | **367.57** | 353.18 | 391.11 | above SMA20/50 |

**Confluence under price:** 370.25 / 370.17 (level), 369.91 (1h SMA200), 368.04 (test low), 367.57 (D SMA20).

## Triggers as they stood at 13:40
- **Hold / first confirmation:** a 5m close above 370.25. This happened at 13:35 (370.57).
- **Stronger:**
  - A **15m close above 370.25**: the 13:30 bar closes at 13:45; it was 370.57 partial at 13:40.
  - A 5m higher low above 368.94.
- **Momentum confirmation:**
  - **VWAP reclaim, a 5m/15m close above 372.39**, with the 5m SMA20/50 at 371.5–372.3 reclaimed.
  - Then the intraday range top at 373.6–373.9.
  - Then the prior close at 377.81.
- **Invalidation:**
  - A **15m close below 368.04** (the test low).
  - Structurally, a 1h close under 369.91 (1h SMA200) plus 367.57 (D SMA20).
  - A daily close under 370.25 would mark the 10-02 flip as failed.
- **Risk from a 370.57 entry:** to 368.03 = **2.54 (0.69%, ≈0.23 daily ATR)**. A tight stop relative to TSLA's 3% ATR.
- **Not yet in evidence at 13:40:**
  - No volume on the reclaim (0.49–0.67x).
  - Price still under VWAP and every intraday SMA.
  - The selloff into the level was a high-volume break of a 2.5-hour range.

## HISTORY (separate, leak-free)
- **Files**
  - `TSLA_5m_HISTORY.json` (= `TSLA_5m_hist.json`): 10,080 bars, 2026-07-27 04:00 → 2026-10-08 13:35. That's as far back as TV would load at 5m (~10.2k bars).
  - `TSLA_15m_HISTORY.json` (= `_hist`): 11,046 bars, 2026-02-02 → 2026-10-08 13:15. Only bars closed by 13:40; the 13:30 partial is excluded.
  - Daily: `TSLA_D_asof.json` covers 2020-06 → 10-07, plus the partial.
  - 60m: `TSLA_60m_asof.json` covers 2024-09-04 → 10-08 13:00 partial.
- **`HISTORY_events.csv`** (definitions in `hist_events.py`)
  - *Level:* a 15m pivot-low support (±8 bars), tested 2+ times within 0.25%, no close more than 0.3% under in between.
  - *Event:* a wick 0.10–1.00% through the level, then a close back above within 2 bars.
  - *Trade:* entry at the reclaim close; stop at the wick low (1R).
  - *Results:* **n = 33** (32 with complete windows).
    - Within 16 bars: +1R hit first **47%**, +2R 28%; a close under the wick low (at any point in the window) 53%.
    - Within 64 bars: +1R 50%, +2R 34%, stop 72%.
    - Median 16-bar MFE +0.96% / MAE −0.74%.
  - These are generic 15m analogs from Feb–Oct 2026, with no regime or volume filter. Small n; roughly a coin flip at 1R.

_Leak control: the full post-cut pulls were moved to `../raw_full_LOOKAHEAD/`, which is outside inputs/; do not read them for the verdict. Every `TSLA_*.json` in inputs/ was checked programmatically to have max bar start ≤ 13:35 ET 10-08 (see `CUT_VERIFY.json`)._
