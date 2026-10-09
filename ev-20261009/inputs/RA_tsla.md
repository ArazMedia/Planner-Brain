# RA — TSLA: one forward debit spread (conditional) — verdict WATCH, not TAKE yet
Written 2026-10-09 ~12:56 ET by RA.
Sources:
- Option quotes: CBOE delayed chain, pulled 12:53 ET (quotes ≈12:38 ET), saved at `/workspace/plans/20261008-goog-uso-mu-watch/data/1247/TSLA.json`.
- Underlying "now": **382.795, the price embedded in the CBOE delayed chain**, not a live quote.
- Levels: PA (`checks/20261009-tsla-pa.md`, `checks/20261009-1210-pa.md`, `pa-agent/ledger/NASDAQ_TSLA.json`).
- Gamma and flow: UW (`checks/20261009-1210-uw.md`).
- No yfinance.

## Spread: TSLA Oct 16 385/390C (buy 385C / sell 390C), 7 days to expiry
| | 385C | 390C |
|---|---|---|
| Bid / ask | 7.15 / 7.25 | 5.20 / 5.30 |
| IV | 37.9% | 38.3% |
| OI | 10,137 | 10,316 |
- **Debit:**
  - Mid $195.
  - **Full spread $205** (pay 7.25 ask, receive 5.20 bid).
- **Max value** $500. Max loss = the debit.
- **Max gain** $295 at the full-spread debit, so R:R is **1.44**.
- **Breakeven at expiry** 387.05 on the full-spread debit (386.95 at mid).
- **Why these strikes:**
  - The short 390 = UW's Live call wall (390). The Gamma tab has the wall/magnet at 400.
  - The long 385 sits in UW's negative-gamma pocket (−85.8M at 385, −77.5M at 382.5), where moves can accelerate.
  - PA's resistance is 386.69–386.82, then today's high of 388.55. Above that, open air to 390.
- **Market-implied** (N(d2), from the price embedded in the CBOE chain; `RA_mkt_probs.md`):
  - P(>387.05) 0.41
  - P(>390, max) 0.36
  - P(<385, full loss) 0.55
- **Catalyst inside expiry:**
  - CPI Wed 10/14 (BLS) is inside.
  - **TSLA Q3 earnings (Oct 21 AMC, TeslaNorth 10/8) are AFTER the Oct 16 expiry.** That's why Oct 16 beats Oct 23: the Oct 23 IV is 48.9% vs 37.9% because it carries the earnings.
- **IV vs RV:** IV ≈38% vs PA daily RV10 38.8% and RV20 31.6% (`rv_pa.json`). That's fair.

## Trigger / invalidation (PA)
- **Trigger:**
  - **15m close >386.82** (PA "confirms the bounce") while holding VWAP (≈385.0 at 12:10).
  - The stronger version is a 15m close >388.55, today's high, but the spread costs more by then.
  - Both are NOT met now: the CBOE-embedded price is 382.795, below VWAP, and PA flagged "confirmation failed" at 12:10.
- **Invalidation:** 15m close <381. Hard fail on a 1h close <380, the UW put wall.
- If the trigger fires, re-quote. At ~387 the spread will cost more than $205 and R:R drops toward ~1.0. **Above ~$260 full spread (R:R <0.9), SKIP** and consider the Oct 16 390/400C instead (now $274 full, BE 392.74, R:R 2.65, short at the 400 Gamma-tab magnet, OI 10,316/31,253).

## Why not now / why not SKIP outright
- **For:**
  - Bullish flow, the strongest of the day: net +$31.4M; 385C 11/13 opening at the ask, $2.5M; 400C Jan27 at the ask, $2.64M.
  - Price is on the gamma flip (382.1), with negative gamma above.
  - The falling-line breakout retest held at 381.14.
  - Tight, deep chain (10¢ wide, 10k+ OI).
- **Against:**
  - Confirmation failed.
  - Price is back under VWAP with lower highs since 388.55.
  - The 08–12 4h bar printed 3.45x volume, but its long upper wick shows rejection: O 380.65, H 388.55, L 379.51, C 383.40 (PA `TSLA_240.json`). It closed only +2.75, giving back 5.15 from the high.
  - Earnings run-up flows may already be priced.
- **Net: WATCH.** Take it only on the 386.82 trigger, with the full spread ≤ ~$260. Otherwise SKIP.

## Earlier context (Oct 8 ~370 test)
- Oct 8 low 368.04 at 13:25 ET (PA TSLA_5). The 370 level = PA's flip / UW's accel level. Already played out; not a forward setup.
- Details in `watchlist/checks/20261009-1020-tsla-ra.md`.
