# RA: TSLA as of Thu Oct 8, 2026, 13:35 ET (BLIND)
Written Fri Oct 9 ~13:12 ET by RA.
- **Hard cutoff:** information available by the close of the 13:35 5m bar, i.e. **13:40 ET Oct 8**.
- **Underlying data:** PA TradingView bars only, truncated by RA.
  - 5m: `watchlist/checks/data_20261009_1210/TSLA_5.json` with t ≤ 13:35 Oct 8, saved as `inputs/RA_TSLA_5m_cut1335.json`.
  - 60m (for relative volume): `data_20261009_tsla/TSLA_60.json`, bars to 10-07.
  - Daily: `inputs/TSLA_1D_full.json`, bars ≤ 10-07.
- No yfinance.
- **Scripts:** `scripts/asof_struct.py`, `scripts/asof_options.py`, `scripts/asof_price2.py`. Full price grid in `inputs/RA_tsla_asof_prices.csv`.
- **Look-ahead flags:**
  - (1) The option IVs are inverted from Oct 8 **end-of-day** last-trade prints and the EOD underlying. That's mild look-ahead on the IV level only; the EOD numbers are deliberately not shown here. They're in `RA_tsla_ivcal_LOOKAHEAD.csv`; don't open it before the verdict.
  - (2) The liquidity score relies on the structural fact that TSLA weekly option markets are deep. The OI figures available to RA are Oct 8 EOD (posted Oct 9), so no OI numbers are used.
  - (3) **Contamination disclosure:** a web search for Oct 8 TSLA news returned a page showing the Oct 8 close. RA did not use it in any number or score here. Planner/critic should know RA has seen it.

## 1) Market state at 13:35 (PA bars)
- **Oct 8 RTH so far:**
  - Open 374.22; high 375.93 at 09:40.
  - **Low 368.04 on the 13:25 bar** (O 369.65, H 369.73, L 368.04, C 369.12).
  - **13:35 bar:** O 370.01, H 370.58, L 369.88, **C 370.57**. That's the first close back above 370.25.
  - Session VWAP **372.39**. Premarket range 373.23–376.66.
- **Path:** lower highs all session. The 370.3–371 area was tested from 12:55 to 13:20 and gave way at 13:20–13:25 (wick to 368.04), then reclaimed by 13:35.
- **Volume:** the PA 5m feed is BATS volume.
  - Session to 13:30: **1.10x** the 17-session average.
  - The 13:25 test bar was 57.6k, **1.6x** the session's average 5m bar.
  - The 13:35 reclaim bar was 17.4k, **0.5x**.
- **Daily context (to the 10-07 close):**
  - Oct 7 close 377.81. SMA20 367.22, SMA50 351.73, **SMA200 391.67**. TSLA is above the 20/50-day and below the 200-day: a mixed regime.
  - ATR14 11.09 (2.94%). RV10 34.5%, RV20 29.2%, RV60 50.3%.
  - Swing: 345.88 (9/30 low) → 383.33 (10/6 high). Oct 2 was a breakout day (close 370.59).
- **Level 370.25:**
  - **34 daily touch days within ±0.5% since 2024-12**; the most recent were 9/11, 9/17, 9/18, 9/21, 9/25, 9/28, 10/2, 10/5. A well-worked flip level.
  - PA's ledger zone R2 363–369 (drawn Sep 5) is just below. Its top plus 370.25 = the support shelf.
  - Overhead: VWAP 372.39, then the 10/7 low 374.43, the 375.93 HOD, and R3 376–388 (PA zone).
- **Expiries:** **Oct 10, 2026 is a Saturday, so there is no Oct 10 expiry.** TSLA lists a **Monday Oct 12** weekly, also Wed Oct 14 and Fri Oct 16 (CBOE chain expiry list). The Oct 12 weekly is included below in place of Oct 10.

## 2) Option prices at 13:25–13:35 (MODELLED: source (d))
**Source search:**
- (a) There are no UW prints or flow files for TSLA timestamped Oct 8. The UW TSLA coverage starts Oct 9; `uw-bridge/cache` has no TSLA.
- (b) No TSLA chain was saved on Oct 8.
- (c) Oct 8 EOD last-trade prints exist (the `prev_day_close` field of the CBOE chain pulled Oct 9 10:20). They're used **only to invert IV**.
- **So (d), Black-Scholes, was used:**
  - r = 4%. Trading-time variance clock: RTH day = 1, weeknight = 0.25, weekend day = 0.10, /252.
  - Sticky-moneyness IV.
  - The EOD prints are non-synchronous: OTM put prints imply ~32–35% IV and OTM call prints ~20–30%. The headline therefore uses **MID = the average of the call-side ATM and put-side levels**. LOW and HIGH bracket it.
- **ATM IV by expiry:**

| Expiry | LOW | MID | HIGH |
|---|---|---|---|
| Oct 9 | 20.3% | 26.2% | 32.0% |
| Oct 12 | 23.1% | 27.5% | 32.0% |
| Oct 16 | 29.6% | 32.5% | 35.4% |

- **Assumed bid/ask widths:** $0.05 when the price is under $2, $0.10 under $10, $0.15 under $20.
- **Full-spread debit** = long ask − short bid.
- **The spreads are robust to the IV choice** (they vary only ±$0.05–0.30 across LOW/HIGH). Single calls are not (about ±$0.60–0.70).

**At the 13:35 close (spot 370.57), MID IV.** Spot is PA's 13:35 close; at 13:25 it was 369.12.

| Expiry | Instrument | Bid | Ask | Mid | Full-spread debit | Max | BE (full) | R:R | Mid range LOW–HIGH | At 13:25 close: mid / full |
|---|---|---|---|---|---|---|---|---|---|---|
| Oct 9 (1DTE) | 370C | 3.39 | 3.49 | 3.44 | 3.49 | – | 373.49 | – | 2.75–4.14 | 2.81 / 2.86 |
| Oct 9 | 372.5C | 2.39 | 2.49 | 2.44 | 2.49 | – | 374.99 | – | 1.76–3.12 | 2.01 / 2.06 |
| Oct 9 | 375C | 1.69 | 1.74 | 1.72 | 1.74 | – | 376.74 | – | 1.12–2.35 | 1.40 / 1.43 |
| Oct 9 | **370/375C** | 1.65 | 1.80 | 1.72 | **1.80** ($180) | $500 | 371.80 | 1.78 | 1.63–1.79 | 1.41 / 1.48 |
| Oct 9 | **370/380C** | 2.55 | 2.70 | 2.63 | **2.70** ($270) | $1,000 | 372.70 | 2.70 | 2.33–2.85 | 2.13 / 2.21 |
| Oct 9 | **375/385C** | 1.24 | 1.34 | 1.29 | **1.34** ($134) | $1,000 | 376.34 | 6.45 | 0.93–1.60 | 1.03 / 1.08 |
| Oct 12 (Mon) | 370C | 4.83 | 4.93 | 4.88 | 4.93 | – | 374.93 | – | 4.16–5.60 | 4.20 / 4.25 |
| Oct 12 | 375C | 2.90 | 3.00 | 2.95 | 3.00 | – | 378.00 | – | 2.28–3.65 | 2.54 / 2.59 |
| Oct 12 | 370/375C | 1.82 | 2.02 | 1.92 | 2.02 | $500 | 372.02 | 1.47 | 1.88–1.96 | 1.67 / 1.77 |
| Oct 12 | 370/380C | 3.09 | 3.24 | 3.16 | 3.24 | $1,000 | 373.24 | 2.09 | 2.98–3.31 | 2.74 / 2.82 |
| Oct 12 | 375/385C | 1.89 | 2.04 | 1.97 | 2.04 | $1,000 | 377.04 | 3.90 | 1.67–2.21 | 1.70 / 1.77 |
| Oct 16 | 370C | 9.10 | 9.20 | 9.15 | 9.20 | – | 379.20 | – | 8.39–9.91 | 8.42 / 8.47 |
| Oct 16 | 375C | 6.91 | 7.01 | 6.96 | 7.01 | – | 382.01 | – | 6.21–7.72 | 6.39 / 6.44 |
| Oct 16 | 380C | 5.18 | 5.28 | 5.23 | 5.28 | – | 385.28 | – | 4.52–5.95 | 4.79 / 4.84 |
| Oct 16 | **370/380C** | 3.81 | 4.01 | 3.91 | **4.01** ($401) | $1,000 | 374.01 | 1.49 | 3.86–3.96 | 3.63 / 3.73 |
| Oct 16 | **375/385C** | 2.99 | 3.19 | 3.09 | **3.19** ($319) | $1,000 | 378.19 | 2.13 | 2.98–3.19 | 2.88 / 2.98 |
| Oct 16 | **380/390C** | 2.31 | 2.51 | 2.41 | **2.51** ($251) | $1,000 | 382.51 | 2.98 | 2.25–2.55 | 2.23 / 2.33 |

**Market-implied odds at 13:35** (N(d2), MID IV, at expiry, unconditional):

| Spread | P(> BE) | P(max) | P(full loss) |
|---|---|---|---|
| Oct 9 370/375C | 0.44 | 0.31 | 0.47 |
| Oct 9 370/380C | 0.40 | 0.16 | 0.47 |
| Oct 9 375/385C | 0.26 | 0.09 | 0.70 |
| Oct 12 370/380C | 0.41 | 0.23 | 0.48 |
| Oct 16 370/380C | 0.44 | 0.34 | 0.49 |
| Oct 16 375/385C | 0.36 | 0.26 | 0.58 |
| Oct 16 380/390C | 0.30 | 0.20 | 0.67 |

## 3) Factor scores as of 13:35 (BRIEF / RA_factors format; −2..+2; weights sum to 100)
**Weights:** RA's standard TSLA weights, with the gamma and flow weight (n/a) moved to structure and volume.

| Weights | Struct | Vol | Trend | Gamma | Flow | Catalyst | IV | Liq |
|---|---|---|---|---|---|---|---|---|
| % | 25 | 15 | 20 | 5 | 5 | 10 | 10 | 10 |

- **Structure +1 (25):**
  - For: wick through a 34-touch flip level (370.25, top of the R2 363–369 shelf) and a reclaim close at 13:35 (370.57). A textbook spring.
  - Against: lower highs all session, below VWAP 372.39; the 10/7 low (374.43) was lost.
  - +1, not +2, because only one 5m close has reclaimed the level so far.
  - [PA 5m cut, PA daily, `pa-agent/ledger/NASDAQ_TSLA.json`] (+)
- **Volume 0 (15):** the test bar was 1.6x (absorption at the low), but the reclaim bar was only 0.5x and the session is 1.10x. Not confirmed. [PA 5m/60m] (0)
- **Trend / regime 0 (20):**
  - Daily: above the SMA20/50, below the SMA200, and the swing off the 9/30 low is still a higher low. Mixed.
  - Intraday trend is down, and the tech tape is weak after the FT OpenAI story at 12:42 ET.
  - [PA daily; FT; CNN 13:07] (0)
- **Gamma 0 (5):** n/a. There is no UW GEX snapshot timestamped ≤ 13:35 Oct 8. (0)
- **Flow 0 (5):** n/a. There are no UW TSLA flow files from Oct 8. (0)
- **Catalyst 0 (10):**
  - Nothing TSLA-specific inside the Oct 9 or Oct 12 expiry. Q3 earnings are Oct 21 AMC, after all three expiries.
  - CPI Wed Oct 14 is inside the Oct 16 expiry; it cuts both ways.
  - Macro (see §4): the hawkish Fed (Waller) and high yields hurt; the solid 30y auction at 13:00 and the 12:17 no-Iran-strike post (oil down) help.
  - Net 0.
- **IV / vol:**
  - **+1 for Oct 9 / Oct 12:** ATM ~26–28% (range 20–32%) vs RV10 34.5% / RV20 29.2%, so the debit is cheap to fair.
  - **0 for Oct 16:** ~32.5% vs RV20 29.2%, fair.
  - [model, PA daily] (+ / 0)
- **Liquidity +2 (10):** TSLA near-ATM weeklies are among the deepest US single-stock options. The assumed widths are 5–10¢ per leg, and full spread − mid costs only $5–10 per spread. (+)

| Setup at 13:35 | Weighted score | Grade |
|---|---|---|
| **1DTE (Oct 9) 370/375C or 370/380C** | 25 + 0 + 0 + 0 + 0 + 0 + 10 + 20 = **+0.55** | **C** (top of C) |
| **Oct 12 370/380C** | +0.55 | **C** |
| **Oct 16 370/380C / 375/385C** | 25 + 0 + 0 + 0 + 0 + 0 + 0 + 20 = **+0.45** | **C** |

**Sensitivities:**
- **Volume to +1** (if absorption on the test bar counts): +0.70, so **B**.
- **Structure to +2** (after a second 15m close above 370.25 or a reclaim of VWAP 372.39): +0.80, so **B**.
- **Trend to −1** (if the OpenAI tape is weighted): +0.35, still C.

**Trigger / invalidation as RA would have stated it at 13:35:**
- **Trigger:** a 15m close > 370.25 holding (the 13:30–13:45 bar), better a reclaim of VWAP 372.39.
- **Invalidation:** a 15m close < 368 (below the wick low), or a 5m close back under 369.
- **Targets:** VWAP 372.4, then 374.4–375.9.

## 4) Catalysts known by 13:35 ET Oct 8 (all timestamps ET)
| Time | Item | Source |
|---|---|---|
| Thu Oct 2 | TSLA Q3 deliveries 486,532 vs ~462k est (beat); stock +4.7% that day | Motley Fool 10/8; PA daily (10/2 close 370.59) |
| Known before Oct 8 | **TSLA Q3 earnings Oct 21 after the close** (after all expiries in scope) | TeslaNorth 10/8; Motley Fool 10/8 |
| Oct 8, pre-market (WSJ card 04:52) | **Waller (Istanbul):** more hikes likely, "flexibility" on pace, "not at consecutive meetings". Used 75bp as an illustrative signaling example. Hawkish lean, but implies an October skip. | federalreserve.gov speech 20261008a; WSJ; Reuters/Kitco |
| Oct 8 morning | **10y yield high ~5.33%** (RA's 10/8 15:01 note; the request cites 5.36%, unverified). 30y ~5.70% morning high. Yields at multi-decade highs. | RA `checks/20261008-1501-ra.md` (morning-high figures only) |
| Oct 8 (time n/a) | Barron's: scrutiny of Optimus commercial progress; TSLA down ~1.4% intraday | SquawkNews (time not given) |
| 12:17 | **Trump (Truth Social):** no attack on Iran before the Nov 3 midterms; blockade stays. Oil eases. | trumpstruth.org; Yahoo Finance 13:00 |
| 12:42 | **FT: OpenAI annualised revenue ~$20bn below prior signals (~$50bn vs $70bn).** Nasdaq losses accelerate. | FT 16:42Z; CNN/KRDO 13:07 ("Nasdaq −1.4%, worst day since July") |
| 13:00 (results ~13:01; investingLive 13:06) | **30y auction ($22B reopen):** 5.618% high yield, +0.1bp tail, 2.54x bid-to-cover (vs 2.41 average), indirects 72.3%. Solid, so no supply shock. | investingLive 13:06; helious.io |
| Upcoming, inside Oct 16 | CPI Wed Oct 14 08:30 (BLS); PPI Oct 15 | BLS |

The overnight Cybercab registrations and China sales items were **excluded**: they weren't known by 13:35.
