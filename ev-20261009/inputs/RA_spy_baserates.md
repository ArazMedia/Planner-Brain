# RA — SPY Oct 16 trigger base rates (v2, sd-stats style, PA bars only)
Updated 2026-10-09 ~13:02 ET by RA.
- **Script:** `scripts/spy_sdstats.py`.
- **Outputs:** `inputs/RA_spy_baserates_v2.csv` (all variants) and `inputs/RA_spy_5m_events.csv` (each 5m touch).
- **Data:** PA TradingView exports in `inputs/pa_data/`:
  - `SPY_5m.json`: 10,155 bars, 2026-07-27 04:00 → 2026-10-09 12:55 ET, 54 sessions, RTH+ETH.
  - `SPY_1D.json`: 2020-06-01 → 2026-10-09. Today's forming bar is excluded.
- **No yfinance; `session_stats.py` was not run.** Its level method was rebuilt from the PA bars instead.
- **Rule: n<30 = WEAK.** Touch ≠ settle: the Oct 16 spreads pay on the expiry close, so the settle columns are what Planner should use for p(max)/p(loss).

## Today's yardsticks
- SPY daily ATR14 (to the 10-08 close) = **6.81 pts = 0.874%**.
- **Bull, from 779.27:**
  - 780 = +0.73 = **0.11 ATR** (+0.09%).
  - 781.62 = +2.35 = **0.34 ATR** (+0.30%).
  - Spread breakeven 779.54 = +0.04 ATR; the 781 short strike = +0.25 ATR.
- **Bear, from 774.90:**
  - 770 = −4.90 = **0.72 ATR** (−0.63%).
  - 767 = −7.90 = **1.16 ATR** (−1.02%).
  - Spread breakeven 773.28 = −0.24 ATR.

## A) 5m level method (touch within ±0.25 of the level, last 54 sessions)
**Definitions:**
- *Touch:* a 5m bar whose range comes within ±0.25 of the level.
- *De-clustering:* there is no new touch until a 5m close has been >1.0 pt away, and at least 12 bars have passed.
- *Approach side:* the close 6 bars before the touch.
- *Outcome (first passage, next 48 bars ≈ 4h; session-end results match):*
  - "thru X" = reached X points through the level before a 1.0-pt move back to the approach side.
  - "reject" = moved 1.0 pt back to the approach side.

| Level | Approach | n | Thru +0.73 (780) | Thru +2.35 (781.62) | Thru 1.0 | Thru 4.90 (770) | Thru 7.90 (767) | Reject 1.0 first | Status |
|---|---|---|---|---|---|---|---|---|---|
| 779.27 | from below | **2** (08-13, 10-06) | 0.50 | 0.50 | | | | 0.50 | WEAK, unusable |
| 779.27 | from above | **1** (10-06 13:02) | 0.00 | 0.00 | | | | 1.00 | WEAK, unusable |
| 774.90 | from above (bear side) | **8** | | | 0.50 | 0.12 | 0.00 | 0.62 | WEAK |
| 774.90 | from below | **15** | | | 0.40 | 0.00 | 0.00 | 0.73 | WEAK |

**Read:**
- 779.27 is near the highs and has almost no 5m history (3 touches in 54 sessions), so there is no usable level-method rate.
- 774.90 is a heavily worked intraday pivot (23 touches). On the first test, it rejects 62–73% of the time. From above, 1 in 8 touches reached 770 within 4h, and none reached 767.
- Intraday, the bear target almost never comes in one push. Whatever edge exists only appears after **closes** (section B).

## B) Generalized daily version (since 2020; first eligible event 2021-06 because of the 252-day lookback)
**Definitions:**
- **Bull event:** a daily close above the prior L-day high (L = 10 or 20), where the prior close was at or below it, and the level is within 1% (or 2%) of the 252-day high. Today's analog is a range edge / ATH zone.
- **Bear event:** a daily close below the prior L-day low (L = 5 or 10), where the prior close was within 1.5% (or 3%) of the 252-day high. This is a rejection from near the ATH, which matches today's regime.
- **Hit:** an intraday high (or low) reaches X·ATR beyond the level on days 1–5, **before** a daily close back through the level.
  - *tie=hit:* a hit and a close back through on the same day counts as a hit.
  - *tie=fail:* the same case counts as a fail.
- **Settle:** the day-5 close vs the level, in ATR units. This is the Oct 16 expiry proxy.
- **De-clustering:** there is no new event until the prior one has resolved.

| Set | n | Window | Touch 780 (0.11 ATR) | Touch 781.62 (0.34 ATR) | Close back <level within 5d | Settle ≥779.54 BE | Settle ≥781 (max) |
|---|---|---|---|---|---|---|---|
| bull L10, within 1% | **59** | 2021-06-14 → 2026-09-21 | 0.88 / 0.75 | 0.81 / 0.75 | 0.49 | 0.76 | **0.71** |
| bull L10, within 2% | **67** | 2021-06-14 → 2026-09-21 | 0.90 / 0.73 | 0.79 / 0.73 | 0.49 | 0.78 | 0.73 |
| bull L20, within 1% | **57** | 2021-06-14 → 2026-08-13 | 0.90 / 0.74 | 0.81 / 0.74 | 0.47 | 0.77 | 0.72 |
| bull L20, within 2% | **62** | 2021-06-14 → 2026-08-13 | 0.90 / 0.76 | 0.82 / 0.76 | 0.48 | 0.77 | 0.73 |

| Set | n | Window | Touch 770 (0.72 ATR) | Touch 767 (1.16 ATR) | Close back >level within 5d | Settle ≤773.28 BE | Settle ≤770 | Settle ≤767 (max) |
|---|---|---|---|---|---|---|---|---|
| bear L5, within 1.5% | **32** | 2021-06-18 → 2026-08-18 | 0.78 / 0.66 | 0.59 / 0.53 | 0.66 | 0.41 | 0.28 | **0.22** |
| bear L5, within 3% | **46** | 2021-06-18 → 2026-09-16 | 0.67 / 0.57 | 0.54 / 0.48 | 0.72 | 0.33 | 0.24 | 0.17 |
| bear L10, within 1.5% | 15 (WEAK) | 2021-06-18 → 2026-08-20 | 0.73 / 0.53 | 0.53 / 0.47 | 0.73 | 0.33 | 0.33 | 0.27 |
| bear L10, within 3% | 29 (WEAK) | 2021-06-18 → 2026-09-16 | 0.59 / 0.45 | 0.45 / 0.41 | 0.79 | 0.28 | 0.28 | 0.17 |

Touch cells read as tie=hit / tie=fail. The rows overlap (shared events), so they aren't independent.

## C) Comparison with PA_baserates.md
1. **Bull touch rate: PA's is higher than RA's.**
   - PA: 781.62 touched 93% of the time (n = 42).
   - RA: 0.79–0.82 (tie=hit), or 0.73–0.76 (tie=fail), with n = 57–67.
   - The gap comes from definitions: PA uses a tested 5-bar pivot and counts ties as hits.
   - Both agree on the main point: the touch is near-certain once a daily close >779.27 prints. It's inside one day's range (0.34 ATR).
2. **Bull stop: the fail definitions differ, so the numbers aren't comparable.**
   - PA: stop-first 2%, where the stop is a close <774.90 (−0.56%).
   - RA: the fail is a close back below the **trigger level** itself, which happens 47–49% of the time within 5 days.
   - The 4h appendix shows 77–91% closing back below on 4h closes (n ≤ 17).
   - So the breakout often slips back under 779.27 without ever reaching 774.90. For a 778/781C, that drift is what turns a touch into a partial or loss at settle.
3. **Bear regime: RA's regime-matched sample gives a usable n where PA's didn't.**
   - PA said the uptrend subset is n = 2, unusable, and gave 771 74% / 767 56% unconditionally (n = 27).
   - RA's near-ATH filter (prior close within 1.5–3% of the 252-day high) gives **n = 32–46** with 770 at 0.67–0.78 and 767 at 0.54–0.59 (tie=hit). That's consistent with PA's numbers, but now regime-matched.
4. **Touch vs settle: PA's touch rates overstate what the spread pays (PA said so too).**
   - Bear max requires settling ≤767, which happens only 0.17–0.22 of the time. Settling ≤ breakeven happens 0.33–0.41.
   - Bull max requires settling ≥781, which happens 0.71–0.73.
5. **Intraday vs close-based: the 5m level method agrees with neither touch rate.**
   - Intraday, 774.90 from above reached 770 only 1 time in 8 within 4h, and 779.27 has n = 3.
   - The edge in A–C only exists **after a daily close** through the level. Planner should condition on the daily-close trigger. A 15m/4h poke isn't enough.

## Recommended priors for Planner (all conditional on a DAILY close through the trigger, payoff at the Oct 16 settle)
| Setup | p(max) | p(partial) | p(loss) | Touch priors | n / basis | Note |
|---|---|---|---|---|---|---|
| **SPY bull 778/781C** | **0.60** (settle ≥781) | **0.10** (settle 779.54–781) | **0.30** (settle <779.54) | 780 0.85, 781.62 0.75 | Daily n = 59 (strong): raw 0.71 / 0.05 / 0.24 | Shrunk toward the 4h fail-back evidence (n ≤ 17, weak) and the 780 gamma pin, which caps the settle near 780 (≈ $200 of $300). |
| **SPY bear 775/767P** | **0.20** (settle ≤767) | **0.15** (settle 767–773.28) | **0.65** (settle >773.28) | 770 0.60, 767 0.45 | Daily n = 32 (L5, within 1.5%), cross-checked with n = 46; raw 0.22 / 0.19 / 0.59 | Shrunk for the 777 put wall / positive gamma and the 4h fail-back of 75–100%. |

- **Market cross-check (unconditional, from now; `RA_mkt_probs.md`):** bull P(max) 0.41, P(profit) 0.47; bear P(max) 0.17, P(profit) 0.32.
- These priors are *conditional on the trigger*, so they should sit above the market numbers for the bull and close to them for the bear. Planner should apply the factor nudges (±0.5 log-odds max) on top.
- **Without a daily-close trigger,** fall back to the market numbers.

---
## Appendix: v1 4h-bar analysis (written 12:56 ET, superseded by the above but kept)
Written 2026-10-09 ~12:56 ET by RA. Script: `scripts/spy_baserates.py`. Raw output: `inputs/RA_spy_baserates.csv`, `inputs/spy_events_bull_l20.csv`, `inputs/spy_events_bear_l20.csv`.
Data: PA TradingView export `/workspace/watchlist/checks/data_20261009_1210/SPY_240.json` (4h ETH bars at 04/08/12/16 ET), **300 bars, 2026-06-24 04:00 → 2026-10-09 12:00 ET** (the last bar was still forming at export). No yfinance or other outside price data. No SPY 5m or SPY 1D exists in any PA export, so the sd-stats / `session_stats.py` level method could NOT be run (it also fetches yfinance, which is banned). See `../REQUESTS.md`.

**Every n below is < 30, so every rate is WEAK.** Per BRIEF, n<15 should be shrunk toward the pooled rate (beta prior, weight ~10).

### Levels (from `checks/20261009-1210-pa.md` and `checks/20261009-1216-gamma.md`)
- SPY at 778.11, CBOE-embedded price (chain quote ≈12:32 ET). ATR14 on the 4h bars = **2.891**.
- **Bull:** trigger is a 4h close >779.27 on >1x volume. Targets are the 780 CW/magnet (+0.73 from the trigger, 0.25 ATR) and 781.62, the 10/06 high (+2.35, 0.81 ATR).
- **Bear:** trigger is a 4h close <774.90. Targets are 770 (−4.90, 1.69 ATR) and 767, the gamma acceleration level (−7.90, 2.73 ATR).

### Definitions
- **Event:** a 4h bar closes beyond the high (bull) or low (bear) of the prior L bars, with L = 4, 10 or 20. Events are de-clustered: there is no new event until the prior one resolves.
- **Hit:** the target distance, scaled to ATR at the event, is touched by a bar's high or low within H bars (H = 10 or 20; 20 4h ETH bars ≈ 5 sessions ≈ time to the Oct 16 expiry). The target must be touched **before** a 4h close back through the broken level.
- **Fail-back:** a 4h close back through the broken level within H bars, whether or not the target was hit first.
- **These are touch rates, not expiry-settlement rates.** The Oct 16 spreads pay on the expiry close. A touch of 781.62 is not the same as SPY settling above 781.
- The vol filter means the trigger bar's volume is ≥ its 20-bar average.

### Results
| Side | L | H | Vol filter | n | p(0.25 ATR → 780) | p(0.81 ATR → 781.62) | p(1.69 ATR → 770) | p(2.73 ATR → 767) | Fail-back |
|---|---|---|---|---|---|---|---|---|---|
| bull | 20 | 20 | – | 6 | 0.667 | 0.500 | | | 0.833 |
| bull | 20 | 20 | ≥1x | 5 | 0.800 | 0.600 | | | 0.800 |
| bull | 10 | 20 | – | 8 | 0.750 | 0.375 | | | 0.875 |
| bull | 10 | 20 | ≥1x | 7 | 0.571 | 0.286 | | | 0.857 |
| bull | 4 | 10 | – | 17 | 0.647 | 0.412 | | | 0.765 |
| bull | 4 | 20 | – | 11 | 0.727 | 0.364 | | | 0.909 |
| bear | 20 | 20 | – | 6 | | | 0.167 | 0.000 | 1.000 |
| bear | 20 | 20 | ≥1x | 4 | | | 0.000 | 0.000 | 1.000 |
| bear | 10 | 20 | – | 8 | | | 0.250 | 0.125 | 0.875 |
| bear | 10 | 20 | ≥1x | 6 | | | 0.167 | 0.167 | 0.833 |
| bear | 4 | 10 | – | 16 | | | 0.375 | 0.188 | 0.750 |
| bear | 4 | 20 | – | 10 | | | 0.300 | 0.300 | 0.800 |

The rows share events, so they are not independent. Don't add them up.

### Exact-level history (4h closes through the actual levels in the window)
- **Close >779.27 (n=2):**
  - 10/06 08:00: hit 780, never 781.62, closed back below the next bar.
  - 10/06 16:00: hit neither.
- **Close <774.90 (n=2):**
  - 08/17 12:00: hit 770 and 767.
  - 10/08 04:00: hit neither, closed back above at bar 3.
- **Level touches (4h bars that traded through the price):** 779.27: 5; 780: 3; 777: 12; 774.90: 18; 770: 32; 767: 34. 770/767 is a heavily traded zone from Aug–Sep. 779–781 has barely traded, since it's the area near the highs.

### RA read (for Planner's prior, before factor nudges)
- **Bull:**
  - p(touch 780 | trigger) ≈ **0.70** (range 0.57–0.80). That's close to trivial at 0.25 ATR, and the gamma file has 780 as the pin/magnet.
  - p(touch 781.62 | trigger) ≈ **0.40** (range 0.29–0.60).
  - Breaks usually fail. 77–91% close back through the level within H, so expect the 780 pin rather than a trend leg.
  - For the 778/781C (BE 779.54 full spread), a pin at 780 pays ≈ $200 of $300.
- **Bear:**
  - p(touch 770 | trigger) ≈ **0.25** (range 0–0.375).
  - p(touch 767 | trigger) ≈ **0.15** (range 0–0.30).
  - Fail-back 75–100%.
  - The 775/767P needs ≈ 773.28 at expiry just to break even.
- **Beta-shrink suggestion:** pooled across L, the 0.81 ATR bull ≈ 0.40 and the 1.69 ATR bear ≈ 0.28. Use these as the prior means with weight 10.
- **Market cross-check:** see `RA_mkt_probs.md`. Risk-neutral P(SPY >781.62 at Oct 16) = 0.386; P(<770) = 0.231; P(<767) = 0.172. These are unconditional, from the current price, and at expiry. The base rates above are conditional on the trigger and are touch rates, so they aren't directly comparable.

### Desk ledger (`/workspace/session-desk/ledger/outcomes.csv`)
- 11 rows, all SPY intraday plays, Sep 11–21, 2026.
- Setup types: pdh_reject, call_wall_r3_reject, pdh_s2_magnet_dp_bounce, flip_reclaim, pdl_reject.
- Only **1 closed trade** (09-14 SPY-01, −1.0R). The rest were not taken.
- **No ledger rows match a multi-day 4h level break toward an Oct 16 expiry, so the relevant n = 0.** The ledger adds no information here.
