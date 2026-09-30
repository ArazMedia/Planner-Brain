# PLANNER cross-check: MU Thursday Oct 1, 2026 (first session after the Wed 9/30 after-close print)
Written Wed Sep 30 2026, ~00:40–01:00 ET by Planner's executor. **Proposal only. Nothing was traded, no broker was touched, and risk.md was not edited.**
Independent dataset and scripts: `planner_bt/` (listed in §8). RA's `PLAN.md` was read and was **not edited**. My proposed changes to it are in §7.

## VERDICT: EDGE CONFIRMED, narrow and stock-only. The options version is KILLED.
- **One rule survives everything I threw at it: short MU at Thursday's open, whatever the gap, with a 3% hard stop, and cover at 15:55 ET.**
  - Full sample: **n = 98** prints (2001–2026). **EV +0.33R (+0.99% per trade) after costs.** Win rate 59%.
  - Bootstrap CI on the EV: **90% +0.14 to +0.53R; 95% +0.10 to +0.56R.**
  - Stability:
    - Positive in both eras: 2001–15 +0.34R, 2016–26 +0.32R (each 95% CI above 0).
    - Walk-forward +0.32R.
    - Leave-one-out range +0.30 to +0.35R.
    - Positive in all six 5-year blocks.
  - **Placebo:** the same rule on non-earnings days loses (−0.06R over 6,146 days; −0.18R on non-earnings days with a gap of 3% or more). So the edge is specific to earnings day 1, not an artifact of how the stop is modeled.
  - It also passes RA's own robustness bar (n ≥ 15, 95% CI > 0, positive in 2008–16 and in 2017–26, positive in the last 12).
- **Why it's narrow:**
  - **The dollars are small.** The account can only carry about 7 shares short (≤1× equity), so risk is about $230 and EV is about **+$74 per trade**.
  - **It needs an entry at the open.** On the 11 prints that have hourly bars, the whole drift happens in the first hour: −2.0% from the open to 10:30, then +0.3% from 10:30 to the close. Any "wait for confirmation" entry gives the edge away.
  - **It dies if fills slip about 0.5% or more against the open print.**
- **Put debit spreads (Oct 2) don't survive natural fills.**
  - The same signal comes out at **−0.14R to +0.01R** for spreads 10–20 wide, and the 20-wide version is over budget at about $940.
  - At half-natural fills it is only +0.01 to +0.10R.
  - So there is **no options substitute: if you can't short the stock, stay flat.**
- **Every other rule tested was weak or killed:** gap-and-go, fading the gap back toward the prior close, the 60-minute opening range, and the run-up filter (§3).

## 1. The playbook: "DAY1-SHORT" (MU, Thu Oct 1)
| Item | Rule |
|---|---|
| Precondition | MU reported Wed after the close (confirmed). Robinhood margin account with short selling enabled, and MU shows as **shortable** Thursday pre-market. **No gap or regime filter:** trade any gap direction and size. (The gap-up ≥ +3% bucket is the weakest, +0.15R with a CI spanning 0, but it isn't carved out, to avoid fitting subgroups.) |
| Trigger / entry | **09:30:00–09:32 ET.** Sell short using a marketable limit (bid − ~$1). **Entry gate:** filled by **09:35** at a price **no more than 0.3% below the official 09:30 opening print** (≈ $3 at ~$1,065). Miss that gate and there is **no trade** (don't chase; the edge sits in the first hour). |
| Instrument / size | MU shares, short. **Shares = min(floor($450 / (0.03 × fill)), 7, what Robinhood's short buying power allows).** At about $1,065 that is **7 shares**: roughly $7.5k notional, **≈ $225–240 risk at the stop** (under the $400–650 cap by design, to keep leverage ≤ 1× on a binary day). If a big gap puts the open near $1,150–1,200, use 6 shares. |
| Stop / invalidation | **As soon as the short fills, enter a buy-stop (stop-market) at fill × 1.03**, good for the day. Never move it further away. If you can't place the stop immediately, cover right away. |
| Target | None. The tested exit is time-based: holding to the close beat every stop and target variant I checked. |
| Time stop | **Buy to cover at 15:55 ET** (market or marketable limit). One variant is allowed if you can't monitor: cover at **11:30 ET**. On the 11 hourly prints it was +0.71R vs +0.58R for holding to the close, but n = 11, so it is **low confidence**. |
| No-trade conditions | (1) Short not available or needs a locate, or the margin requirement leaves fewer than 3 shares. (2) MU halted at the open, or no opening print by 09:35. (3) Entry gate missed. (4) You can't enter the stop right away. (5) Any urge to swap in options: the options version is negative EV at natural fills. (6) You have already taken a Thursday MU trade: **one trade max**, and this trade replaces RA's optional drift trade (§7). |
| Account notes | A same-day round trip is a day trade. RA reports that FINRA's June 2026 intraday-margin rule removed the PDT flag, but I have not verified that; confirm in the app. Borrow fees for one day are negligible. Short proceeds don't add buying power. |

**Worked example** (C0 is unknown; assume the Thursday open is 1,100). Short 7 at about 1,099 → buy-stop at 1,132 → worst case about −$235 plus slippage → cover at 15:55. The historical average outcome is +0.99% of 1,099 × 7 ≈ **+$76**. It's roughly a coin flip on any single day (59% win rate); the edge is in the average.

## 2. Stats behind it (R0; costs: 0.10% entry and exit slippage, 0.20% extra on stop fills; a stop touch counts as a stop-out)
| Cut | n | Win | EV (R) | EV %/trade | $ @ 7 sh | 90% CI (R) | 95% CI (R) |
|---|---|---|---|---|---|---|---|
| **All 2001–2026** | **98** | 59% | **+0.33** | +0.99% | +$74 | +0.14 / +0.53 | +0.10 / +0.56 |
| 2001–2015 | 56 | 57% | +0.34 | +1.01% | +$76 | +0.07 / +0.62 | +0.01 / +0.67 |
| 2016–2026 | 42 | 62% | +0.32 | +0.96% | +$72 | +0.06 / +0.58 | +0.02 / +0.63 |
| RA window 2008–2016 / 2017–2026 | 36 / 38 | – | +0.17 / +0.41 | – | +$39 / +$91 | – | −0.26/+0.64 ; +0.08/+0.74 |
| Last 12 (**n < 15, low confidence**) | 12 | 83% | +0.56 | +1.68% | +$125 | +0.25 / +0.82 | – |
| Gap ≥ +3% | 34 | 56% | +0.15 | +0.44% | +$33 | −0.15 / +0.46 | – |
| \|gap\| < 3% | 33 | 61% | +0.36 | +1.08% | +$81 | +0.02 / +0.72 | – |
| Gap ≤ −3% | 31 | 61% | +0.50 | +1.49% | +$111 | +0.16 / +0.85 | – |
| 20-day run-up > 10% (context, not a filter) | 23 | 74% | +0.56 | +1.67% | +$125 | +0.21 / +0.91 | – |
| Walk-forward (trade only if the prior mean > 0) | 86 | – | +0.32 | – | – | – | – |
| **Placebo:** non-earnings days / non-earnings \|gap\| ≥ 3% | 6,146 / 470 | – | −0.06 / −0.18 | −0.18% / −0.55% | – | – | – |

**Robustness checks:**
- Leave-one-out: +0.30 to +0.35R.
- 5-year blocks: +0.42 / +0.19 / +0.59 / +0.09 / +0.38 / +0.49 (the last block has n = 6).
- Excluding the suspect Jun 2026 print: +0.33R.
- Raw open-to-close drift with no stop: −0.99% (t = −2.31). By era: t = −1.13 for 2001–15 and −2.81 for 2016+.
- Bonferroni across the 6 pre-declared rules: bootstrap p ≈ 0.002, which is below 0.05/6.

**Stop sensitivity** (reported as-is; 3% was declared up front):

| Stop | 2% | **3%** | 4% | 5% | 6% | none |
|---|---|---|---|---|---|---|
| EV (R) | +0.30 | **+0.33** | +0.23 | +0.17 | +0.14 | n/a |
| EV (%/trade) | +0.59 | **+0.99** | +0.93 | +0.86 | +0.82 | +0.79 |

**Slippage sensitivity** (entry/exit %, stop-fill %):

| Slippage | 0.1 / 0.2 | 0.2 / 0.4 | 0.3 / 0.6 | 0.5 / 1.0 |
|---|---|---|---|---|
| EV (R) | +0.33 | +0.25 | +0.16 | **−0.04** |

This is why the entry gate exists. On earnings days, yfinance's hourly-bar opens differ from the official daily open by about 0.2% on average (up to 1.26% on 9/24/2025), versus 0.08% on normal days.

## 3. Every pre-declared rule (stock at a 3% stop; options = Oct 2 ATM 15-wide debit vertical, IV 55%, natural fills)
| Rule | n | Stock EV (R) [90% CI] | 2001–15 / 2016–26 | Options EV (R) | Verdict |
|---|---|---|---|---|---|
| **R0 Day-1 short at the open** | 98 | **+0.33 [+0.14, +0.53]** | +0.34 / +0.32 | −0.05 | **Stock: CONFIRMED. Options: killed** |
| R1 Gap-and-go (with the gap, \|gap\| ≥ 3%) | 65 | +0.20 [−0.04, +0.44] | +0.42 / **−0.04** | −0.11 | KILLED (the edge has faded; last 12 is −0.19) |
| R1f Gap fade toward the prior close | 65 | **−0.22 [−0.42, −0.00]** | −0.32 / −0.10 | −0.33 | **KILLED, reliably negative.** Fill rates: 16–17% for 3–8% gaps, **0/16 for gaps ≥ 8%** |
| R2 Fade gap-up ≥ +3% | 34 | +0.15 [−0.15, +0.46] | +0.04 / +0.24 | −0.15 | WEAK |
| R3 Continue gap-down ≤ −3% | 31 | +0.50 [+0.16, +0.84] | +0.60 / +0.36 | +0.06 | A subset of R0; nothing extra |
| R4 R0 with a 20-day run-up > 10% | 23 | +0.56 [+0.20, +0.91] | **+0.23** / +1.07 (9/9) | +0.12 (−0.07 pre-2016) | Filter rejected: the post-2016 9/9 looks overfit |
| R5 60-minute opening range, first-hour direction | **11** | +0.02 [−0.23, +0.28] | – / +0.02 | −0.34 | KILLED (low n) |

**Options grid for R0** (put debit spread, Oct 2 expiry, entry T = 2/252, exit T = 1/252, exit IV = entry IV − 3 pts, flat vol; costs per spread per side = sum of the legs' half-spreads):

| Cost per side | ATM 10w (≈ $550 risk) | ATM 15w (≈ $755) | ATM 20w (≈ $940) |
|---|---|---|---|
| $0.40 (half-natural) | +0.01 | +0.07 | +0.10 |
| **$0.80 (natural, base)** | **−0.14** | −0.05 | +0.01 |
| $1.20 (stress) | −0.27 | −0.14 | −0.07 |

Centering the strikes around spot or changing IV (45/55/70%) moves the numbers by ≤ 0.07R. Leg widths come from the 9/29 RTH Oct 2 chain (near-the-money $0.50–1.10). The reason it fails: 1-DTE theta plus paying two legs' spread on the way in and out eats a roughly 1% edge. The only way to lower costs is a stock stop, which the account can't hold at full risk size anyway.

## 4. Data: what exists and what doesn't
- **Daily:** yfinance unadjusted OHLC, 98 after-close prints (2001-12 to 2026-06).
  - Timing is from yfinance's earnings timestamps. Two ambiguous "12:00" stamps (2011-03-23, 2011-09-29) were confirmed by a volume spike on the next day. They match RA's SEC-verified date fixes.
  - **Reconciled with RA's `day1_dataset.csv`:** all 74 overlapping prints match exactly (gap, open-to-close, close-to-close, fill flags). I add 24 prints from 2001–2007.
  - **Caveat:** both datasets come from the same vendor, so agreement is not independent verification. Stooq was unreachable and Alpha Vantage needs a key (I did not sign up).
- **Intraday:** yfinance 1h goes back only to 2023-10-31, which covers **11 prints**. 5m/15m/30m bars start Jul 7 2026, which covers **0 prints**.
  - So **15- and 30-minute opening-range claims can't be tested.** The 60-minute opening range was tested on n = 11 only.
  - RA's first-hour numbers differ from mine on 9/24/2025 because RA measures from the hourly bar's open (163.00) while I use the official daily open (165.08).
- **Jun 2026 bars** (1211 → 1052 → 1048 → 1213): the hourly bars are internally consistent, with heavy volume (the Jun 23 first hour traded 20.9M shares). So I kept the print, but it is unverified against a second vendor. R0 doesn't depend on it (+0.33R either way).
- **Not reconcilable:** UW's historical "actual 1d move" column (for example 2024-06-26 shows +0.88% vs −7.12% close-to-close) doesn't match any price series I could build. Don't use it.

## 5. Critique pass. The Fable 5.1 agent did NOT run
- **CloudAgent status:** no CloudAgent (or equivalent) tool was available in this executor session; a tool search for cloud/agent/fable came back empty. **No Fable agent was launched, so there is no bcId or URL.**
- I **did not push a branch** to `ArazMedia/Planner-Brain`. Its only purpose was to feed the agent.
- A ready-to-use brief is at `planner_bt/CRITIC_BRIEF.md` if Planner wants to launch one itself.
- In-house critique at high effort, including what it changed:
  1. **Look-ahead.** The rule set was declared after I'd seen 2015+ per-print moves from yesterday's work. So 2001–2014 (56 prints) serves as the out-of-sample check, and R0 holds there (+0.34R).
  2. **Stop modeling.** Daily bars can't tell whether the high or low came first, so any touch of the stop is counted as a stop-out. That is conservative. The placebo (−0.06R on normal days) shows this method doesn't manufacture edge.
  3. **Multiple testing.** 6 stock rules plus 162 option configurations. I **did not select** from the options grid; it is reported only to show that nothing clears natural fills. R0 survives a Bonferroni correction across the 6 rules.
  4. **Subgroup filters** (run-up, gap bucket) raise post-2016 numbers but are unstable before 2016. Rejected; R0 stays unfiltered.
  5. **Mechanism.** This is consistent with the published "overnight returns / buying at the open" effect: attention-driven buying at the open on news days, followed by an intraday reversal (e.g., Berkman, Koch, Tuttle & Zhang, JFQA 2012). I cite this from memory; I did not re-check it this session. The first-hour concentration (n = 11) and RA's finding that "the first hour went against the gap in 8 of 11 prints" both fit this story.
  6. **Refinements considered (max 3):**
     - (a) An **entry gate at 0.3% from the open**: **adopted**. It comes from the slippage stress test, not from outcomes.
     - (b) An **11:30 time stop**: allowed only as a fallback (n = 11).
     - (c) **Half size on gaps ≥ +3%**: **not adopted** (subgroup fitting). Noted as the weakest bucket.

## 6. Inputs needed at the open
- **Hard inputs** (the only things the rule uses):
  - C0 = Wed 9/30 close. Gap % is logged only; it doesn't gate the trade.
  - Robinhood pre-market: MU shortable, short buying power ≥ 7 shares, margin requirement.
  - The official 09:30 opening print (for the entry gate and the stop).
- **Context only** (`PA_*.md` / `UW_*.md` landing in this folder):
  - These are **not backtested** and must not override the rule, the stop, or the size.
  - Allowed use: note whether a PA level (e.g., R1 1073–1089, R2 1097–1125, S1 1030–1044, S2 1000–1017, depending on the gap) sits just inside the 3% stop, so a stop-out isn't a surprise. Log UW flow, GEX, and the expected move for the post-mortem.

## 7. Proposed edits to PLAN.md (for RA/Planner to apply; I did not edit PLAN.md)
1. **§0 Verdict:** change "no robust edge, skip Thursday by default" to "**One robust stock-only edge: DAY1-SHORT** (short at the open, any gap, 3% stop, cover 15:55; n = 98, +0.33R, 95% CI +0.10/+0.56; passes RA's own bar)." Keep the "no options edge at the open" finding; it matches mine.
   - Why RA missed it: RA framed open trades as *with* or *against* the gap, which splits one signal into two halves that are each underpowered (continue on gap-downs + fade gap-ups).
   - RA's own numbers corroborate it: first hour against the gap in 8/11; big up-gaps all faded open-to-close (5/5); "most of the fade happens before 10:00".
2. **§1 Scenario tree:** in every branch, replace "SKIP" at the open with "**DAY1-SHORT if the entry gate is met**". Also note that **"do not chase the open" in the >12% up-gap branch should read "short it, don't buy it."**
3. **§0/§3 Optional drift trade** (|gap| ≥ 7%, Oct 9 vertical at 15:45, hold to Monday):
   - Its 95% CI includes 0, the last 12 are −0.06R, and the regime cut is 0.00R. Given Dominic's "flat over weak" rule, **downgrade it to "not recommended."**
   - Enforce **one MU trade max for Thursday**: if DAY1-SHORT is taken, no drift trade.
4. **§3 "Shares from the open +0.09R (|gap| ≥ 7%)"**: add the unconditional short-at-open result and the placebo, and note that **fading the gap toward C0 is reliably negative** (my R1f: −0.22R, CI entirely below 0).
5. **§4 Risk:** add a stock-short sizing line: min(floor($450 / (0.03 × fill)), 7 shares, short buying power). Buy-stop at +3% placed immediately. Keep "no options substitute" because the put-spread version is negative at natural fills.
6. **§8 Checklist:**
   - Add a Thursday 08:00–09:25 step: confirm MU is shortable and check short buying power.
   - Add a Thursday 09:30–09:35 step: run the entry gate, place the stop, and set the 15:55 cover.
7. **§7 Data caveats:** add that RA's and Planner's datasets agree exactly on 74/74 prints, but come from one vendor. Add that the hourly vs daily open mismatch on 9/24/2025 (1.26%) explains the first-hour differences.
8. **§9 Planner reconciliation:** replace "PENDING" with a pointer to this file.

## 8. Files (all under `/workspace/plans/20261001-mu-thursday/planner_bt/`)
- **Data:**
  - `fetch.py` pulls `raw_daily_unadj.csv`, `raw_earnings_dates.csv`, and `raw_1h.csv` (yfinance, pulled 9/30 ~00:27 ET).
  - `build_dataset.py` builds **`day1_planner.csv`** (98 prints: gap, open-to-close, close-to-close, high/low, fill, continuation, MFE/MAE, run-up, hourly first-hour fields).
- **Backtests:**
  - `bt_planner_thu.py` (pre-declared rules R0–R5; stock + options) → `trades_base.csv`, `summary_base.csv`, `bt_out.txt`.
  - `robust.py` → `robust_out.txt` (stops, slippage, blocks, walk-forward, buckets, hourly timing).
  - `placebo.py` → `placebo_out.txt`.
  - `grid.py` → `grid_options.csv` / `grid_out.txt`.
  - `refine_timestop.py` → `refine_out.txt`.
- **Critic brief (not launched):** `CRITIC_BRIEF.md`.

**Proposal only. Dominic decides.**
