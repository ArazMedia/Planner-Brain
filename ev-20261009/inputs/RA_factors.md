# RA — factor checklist per setup (BRIEF format)
Written 2026-10-09 ~12:56 ET by RA; GOOGL re-scored ~13:02 ET on PA levels. Computed by `scripts/ra_factors.py` (asserts weights = 100 and scores in −2..+2). Machine-readable copy in `inputs/RA_factors.csv`.

**Scale:** each factor is scored −2..+2 (+ helps the spread, − hurts it). RA sets the weights per setup, and they sum to 100%.
**Weighted score** = Σ w·s / 100. **Grade:** A ≥ +1.2 | B +0.6..1.2 | C 0..0.6 | D −0.6..0 | F < −0.6.

**Paths:**
- `C/` = `/workspace/watchlist/checks/`
- `W` = `/workspace/watchlist/WATCHLIST.md`
- `rv` = `inputs/rv_pa.json`, RV computed from PA bars
- `mp` = `inputs/RA_mkt_probs.md`

**Option quotes:** CBOE delayed, quotes ≈12:32 ET (TSLA/IBIT ≈12:38).

**No double-count rule (flow vs gamma):**
- **Gamma** scores only the OI-derived walls, flip and pin vs the strikes (UW gamma/heatmap).
- **Flow** scores only *today's* premium direction: opening vs closing, at the ask vs the bid, $ size.
- Big standing OI is never scored as "flow" because it already shows up in the walls.
- **Liquidity** scores only OI, the bid/ask at the legs, and full-spread vs mid slippage. It does not re-score the walls.

## Summary
| Setup | Struct | Vol | Trend | Gamma | Flow | Catalyst | IV | Liq | Weighted | Grade |
|---|---|---|---|---|---|---|---|---|---|---|
| PLTR Oct16 205/210C | +1 (15) | +2 (15) | +1 (10) | +1 (15) | +1 (15) | 0 (10) | −1 (10) | +2 (10) | **+0.95** | **B** |
| PLTR Nov20 200/210C (alt) | +1 (15) | +2 (15) | +1 (10) | +1 (15) | +1 (15) | −1 (10) | −1 (10) | +2 (10) | +0.85 | B |
| TSLA Oct16 385/390C (conditional on trigger) | 0 (15) | 0 (10) | +1 (15) | +1 (15) | +2 (15) | 0 (10) | 0 (10) | +2 (10) | **+0.80** | **B** |
| SPY bull Oct16 778/781C | 0 (20) | 0 (10) | 0 (15) | +1 (15) | 0 (5) | −1 (15) | 0 (10) | +2 (10) | +0.20 | C |
| USO Nov20 150/160C | +1 (15) | 0 (10) | +1 (15) | 0 (5) | 0 (10) | −1 (25) | 0 (10) | 0 (10) | +0.05 | C |
| SPY bear Oct16 775/767P | 0 (20) | 0 (10) | −1 (15) | −1 (15) | 0 (5) | 0 (15) | +1 (10) | +2 (10) | 0.00 | C (on the C/D line) |
| USO Nov20 150/155C | +1 (15) | 0 (10) | +1 (15) | 0 (5) | 0 (10) | −1 (25) | 0 (10) | −1 (10) | −0.05 | D |
| GOOGL Nov20 355/365C (re-scored 13:02) | +1 (15) | 0 (10) | +1 (10) | −1 (15) | 0 (10) | −1 (20) | −1 (10) | +2 (10) | 0.00 | C (on the C/D line; was D −0.10) |
| BTC/IBIT Nov20 46/49C | +1 (15) | 0 (10) | 0 (15) | 0 (5) | −2 (20) | −1 (15) | 0 (10) | +2 (10) | −0.20 | D |
| GOOGL Nov20 360/370C (re-scored 13:02) | +1 (15) | 0 (10) | +1 (10) | −1 (15) | 0 (10) | −1 (20) | −1 (10) | +1 (10) | −0.10 | D (was −0.20) |

The summary reads score (weight %).

**Trigger status:**
- **Fired:** PLTR (204.42 broken on 3.70x).
- **Pending:** USO (daily close >148.07), GOOGL (daily close >353.22; above it intraday), SPY (daily close per RA_spy_baserates v2), TSLA (15m >386.82), IBIT (15m >47.16).
- For pending setups, the volume factor is scored 0, so re-score it when the trigger fires.
- No setup reaches A.

---

## USO bull — Nov20 150/160C (alt 150/155C)
Trigger: daily close >148.07. Fail <147.12 (02_plan). Weights: catalyst is heaviest at 25 because oil is headline-driven.
- **Structure +1 (15):** 4h close 148.79 above 147.12/148.07; the next PA confirm is 150.67. The kill zone 134.34–136.57 is far below. [C/20261009-1210-pa.md, W] (+)
- **Volume 0 (10):** the 08–12 4h bar was only 1.05x. The daily close isn't in yet. [C/20261009-1210-pa.md] (0)
- **Trend +1 (15):** above the 4h SMA50 147.30. The oil regime is elevated (Iran/Hormuz, Isaias Gulf shut-ins). RV60 50.7% means it's choppy. [C/20261009-1210-pa.md, C/20261009-1209-ra.md, rv] (+)
- **Gamma 0 (5):** no USO GEX/walls in the UW files. Scored n/a = 0, with low weight. [C/20261009-1210-uw.md] (0)
- **Flow 0 (10):** quiet. Net +$0.96M, no opening bullish block, WATCHLIST says "no fresh bullish conviction". [C/20261009-1210-uw.md, W] (0)
- **Catalyst −1 (25):** EIA Wed 10/15 and CPI Wed 10/14 are inside expiry. The Iran headlines cut both ways: a Hormuz deal could gap oil down. [C/20261009-1209-ra.md, C/20261009-1005-ra.md] (−)
- **IV 0 (10):** IV ~45% vs RV20 43.1% / RV60 50.7%. That's fair. [rv, CBOE 1247] (0)
- **Liquidity:**
  - 150/160 scores 0: 150C OI 5,740, 160C OI 2,699; full-spread − mid = $27.50 (8% of the debit).
  - 150/155 scores −1: 155C OI 1,490; slippage $32.50 (17% of the debit).
  - [CBOE 1247] (0 / −)

## GOOGL bull — Nov20 355/365C (alt 360/370C) — RE-SCORED 13:02 ET on PA's GOOGL levels
- **PA's GOOGL levels (PA_baserates.md):**
  - Trigger: daily close **>353.22**, the GOOGL high on 10-01, the structural equivalent of GOOG 350.09.
  - Fail: close **<341.38** (GOOG 337.96 × 1.01012).
  - These replace the GOOG-level mismatch flagged at 12:56.
- **Trigger status: NOT fired.**
  - GOOGL is above 353.22 intraday: 354.11 in the CBOE chain (quotes ≈12:32 ET); PA's daily bar shows 354.24 at ~13:00.
  - The trigger needs a **daily close >353.22**. Re-check at the close.
  - When it fires, re-score volume: today's volume is 0.32x (partial). PA found no volume edge for GOOGL (n = 42).
- **Structure +1 (15):**
  - 353.22 is a well-defined ceiling (28 touch days since 04-27, per PA), and price is above it intraday.
  - The fail line at 341.38 is −3.35% below, about 1.4 ATR. That's sensible, not noise-tight.
  - Kept at +1 rather than +2 until the daily close. PA's strong breakout base rates (n = 42: 360 86%, 365 69%, 370 64%, stop-first 5%) belong in Planner's p, not in this score, to avoid double-counting.
  - [PA_baserates.md, C/20261009-1210-pa.md] (+)
- **Volume 0 (10):** pending (0.32x partial). PA found no volume edge. [PA_baserates.md] (0)
- **Trend +1 (10), was 0:**
  - GOOGL 354.24 > SMA50 346.30 > SMA200 340.04 (PA daily). That's a stacked uptrend.
  - PA's matching-regime subset (n = 29): 360 97%, 365 79%, 370 76%.
  - The QQQ softness note still applies, so +1, not +2.
  - [PA_baserates.md] (+)
- **Gamma −1 (15):** unchanged. Positive-gamma pin at 350–357.5, CW 355 (Gamma) / 357.5 (Live). The long 355 sits at the wall. [C/20261009-1210-uw.md] (−)
- **Flow 0 (10):** unchanged. Net +$11.8M on GOOG / +$3.57M on GOOGL, offset by the Feb27 345C sold at the bid ($7.23M). Call premium has been fading since late Sep. [C/20261009-1210-uw.md, W] (0)
- **Catalyst −1 (20):** unchanged. Earnings Oct 28 AMC (±7.8% implied) and FOMC Oct 28 fall inside the Nov 20 expiry; CPI 10/14. PA's base rates do not isolate earnings. [W, C/20261009-1005-ra.md] (−)
- **IV −1 (10):** unchanged. IV 34.6% vs RV10 15.6% / RV20 23.6%; IV rank 65. [rv, W] (−)
- **Liquidity +2 / +1 (10):** unchanged.
  - 355/365: OI 31,092/2,946, slippage $22.50.
  - 360/370: OI 11,499/34,302, slippage $27.50.
  - [CBOE 1247] (+)
- **Result:**
  - 355/365: **0.00 → C** (on the C/D line; was D −0.10).
  - 360/370: **−0.10 → D** (was −0.20).

## PLTR bull — Oct16 205/210C (alt Nov20 200/210C)
Trigger >204.4 has fired. Target 207.5–210. Fail is a 4h close <204.42 (PA).
- **Structure +1 (15):** a breakout of yesterday's high (204.42) to a 300-bar 4h high. There's no overhead supply, but the retest hasn't happened yet, so chasing is a risk. [C/20261009-1210-pa.md] (+)
- **Volume +2 (15):** the 3.70x 4h bar closed near its high. [C/20261009-1210-pa.md] (+)
- **Trend +1 (10):** new highs, a momentum name. The tech backdrop (QQQ) is soft. [C/20261009-1210-pa.md, W] (+)
- **Gamma +1 (15):** magnet 205 right below; CW 210 (Gamma) = the short strike, which caps the move where the spread maxes. The flip at 196/193 is far below. −13.8M gamma at 202.5 means a fast drop if 204 fails. [C/20261009-1216-gamma.md] (+)
- **Flow +1 (15):** net +$21.25M, heavy 205C/207.5C volume. Opening status isn't fully confirmed, so +1, not +2. [C/20261009-1216-gamma.md] (+)
- **Catalyst:**
  - Oct16 scores 0: no earnings inside (Nov 2–9 est.), only CPI 10/14.
  - Nov20 scores −1: earnings inside.
  - [C/20261009-options-prep.md] (0 / −)
- **IV −1 (10):** weekly IV 41% vs RV20 24.8% (PA 4h); Nov IV 54.8%. That's rich vs recent RV (RV60 70.6% includes the Aug earnings). [rv, CBOE 1247] (−)
- **Liquidity +2 (10):**
  - Oct16: OI 8,003/11,407, slippage $10 (4.5%).
  - Nov20: OI 12,744/7,776, slippage $15.
  - [CBOE 1247] (+)

## SPY bull — Oct16 778/781C
Trigger: 4h close >779.27 on >1x volume, toward the 780 pin / 781.62.
- **Structure 0 (20):** the trigger sits just under 779.27–781.62 resistance (the 10/06 high). Exact-level history n=2: one tagged 780 then failed, one hit nothing. [C/20261009-1210-pa.md, RA_spy_baserates.md] (0)
- **Volume 0 (10):** the trigger hasn't fired. The last 4h bar was a 0.92x inside bar. [C/20261009-1210-pa.md] (0)
- **Trend 0 (15):** range regime. On 4h breaks, 77–91% close back inside within 20 bars, but small targets get touched about 70% of the time. [RA_spy_baserates.md] (0)
- **Gamma +1 (15):** the 778–780 negative-gamma pocket feeds a run to the CW/magnet at 780. A pin at 780 pays ≈$200 of $300. The flip is 777. [C/20261009-1216-gamma.md] (+)
- **Flow 0 (5):** net +$7.42M, which is noise for SPY. [C/20261009-1216-gamma.md] (0)
- **Catalyst −1 (15):** CPI Wed 10/14 and PPI are inside the expiry, so the binary risk hits the narrow 3-wide spread. [C/20261009-1005-ra.md] (−)
- **IV 0 (10):** IV ≈9.4–9.7% vs RV20 9.9%. That's fair. [rv, CBOE 1247] (0)
- **Liquidity +2 (10):** OI 6,334/9,780, 1–2¢ wide legs, slippage $2. [CBOE 1247] (+)

## SPY bear — Oct16 775/767P
Trigger: 4h close <774.90, toward 770 and then 767 (the accel level).
- **Structure 0 (20):** 774.90 is a real shelf (18 touches). The 770/767 zone is heavily traded (32/34 touches), so price can stall there. The trigger is ~3.2 below spot. [RA_spy_baserates.md] (0)
- **Volume 0 (10):** the trigger hasn't fired. (0)
- **Trend −1 (15):** SPY is near its highs (781.62), above the put wall. Base rate p(770) ≈ 0.25, fail-back 75–100%. [RA_spy_baserates.md] (−)
- **Gamma −1 (15):** the put wall / flip at 777 (+1.52B) and positive gamma at 775–777 dampen downside until they give way. Only below that does the 767 accel help. [C/20261009-1216-gamma.md] (−)
- **Flow 0 (5):** net +$7.42M, noise. (0)
- **Catalyst 0 (15):** CPI 10/14 is two-way. It could hurt or deliver the move; a long-premium debit is fine with event vol. (0)
- **IV +1 (10):** the short 767P carries 11.3% IV vs 10.1% on the long 775P, so we sell richer skew. RV20 is 9.9%. [CBOE 1247, rv] (+)
- **Liquidity +2 (10):** OI 8,689/9,826, slippage $1.50. [CBOE 1247] (+)

## BTC/IBIT — Nov20 46/49C (trade was cancelled by Dominic at 10:04; scored for completeness)
- **Structure +1 (15):**
  - BTC 4h close 82,816 held the 82,714 retest and is above the 4h SMA200 (81,674). T1 83,160 has been tagged.
  - The IBIT trigger (15m >47.16) is not fired; IBIT is 46.82 (CBOE-embedded).
  - [C/20261009-1210-pa.md, W] (+)
- **Volume 0 (10):** the 08–12 4h bar was 1.30x, but the prior bar was 0.81x and 15m IBIT volume is fading. (0)
- **Trend 0 (15):** a bounce inside a correction. Price is above the daily 50-day, below the 20-day, and −8% from 87k. [W, plans/20261009-btc/ra.md] (0)
- **Gamma 0 (5):** no IBIT walls in the UW files. n/a. (0)
- **Flow −2 (20):** no opening call buying. Nov27 49.5C/52.5C were sold at the bid, opening; net −$0.5M. Spot ETF net outflows the last two sessions. [C/20261009-1210-uw.md, plans/20261009-btc/uw.md, plans/20261009-btc/ra.md] (−)
- **Catalyst −1 (15):** CPI 10/14 and FOMC 10/28 (hawkish Fed talk) are inside expiry, with yields high. [C/20261009-1005-ra.md, C/20261009-1209-ra.md] (−)
- **IV 0 (10):** IV 37% vs RV20 39.7%. That's fair. [rv, CBOE IBIT 12:53] (0)
- **Liquidity +2 (10):** OI 22,023/26,057, slippage $2. [CBOE] (+)

## TSLA — Oct16 385/390C (conditional; details in `RA_tsla.md`)
- **Structure 0 (15):** the falling-line breakout retest held at 381.14, but confirmation failed: no 15m close >388.55, and price is below VWAP. [C/20261009-tsla-pa.md, C/20261009-1210-pa.md] (0)
- **Volume 0 (10):** the 08–12 bar was 3.45x, but it had a long upper wick (H 388.55 → C 383.40). Mixed. [PA TSLA_240.json] (0)
- **Trend +1 (15):** short-term turn up (gap over the falling line, 15m higher lows), on 381 support. [C/20261009-tsla-pa.md] (+)
- **Gamma +1 (15):** on the flip (382.1). Negative gamma at 382.5–387.5 accelerates moves through the spread's range. The short 390 = the Live CW, and the put wall at 380 = invalidation. [C/20261009-1210-uw.md] (+)
- **Flow +2 (15):** net +$31.4M, the strongest read of the day. 385C 11/13 opening at the ask ($2.5M, vol 2,749 vs OI 189); 400C Jan27 at the ask ($2.64M). [C/20261009-1210-uw.md] (+)
- **Catalyst 0 (10):** earnings Oct 21 AMC fall after expiry. CPI 10/14 is inside. [C/20261009-1020-tsla-ra.md] (0)
- **IV 0 (10):** IV ~38% vs RV10 38.8% / RV20 31.6%. That's fair. [rv] (0)
- **Liquidity +2 (10):** OI 10,137/10,316, 10¢ wide, slippage $10. [CBOE 12:53] (+)
- The grade is valid **only if** a 15m close >386.82 prints and the full-spread debit is ≤ ~$260.

## RA notes for Planner / critic
- **Market cross-check (`RA_mkt_probs.md`):** risk-neutral P(max) ranges from 0.17 (SPY bear) to 0.43 (PLTR Nov). Any p_adj that sits >10pp above these needs a justification, per BRIEF.
- **Slippage:** the CBOE fair value ≈ mid, so EV_mkt at the full-spread debit is about −$1.50 to −$32.50 before exit costs. USO 150/155 is the worst.
- **Data limits:** USO and IBIT gamma are n/a. PLTR's flow is not confirmed as opening. All the base rates are thin (see `RA_spy_baserates.md`; PA owns the rest).
- **Correlated setups:** PLTR, TSLA, GOOGL and SPY bull share risk (tech beta + CPI). If Planner ranks several, treat them as correlated.
