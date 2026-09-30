# MU Thursday Oct 1, 2026 playbook (first session after the Wed Sep 30 print)
Written Wed Sep 30 2026, ~00:45 ET. Research only. **Nothing has been traded, and nothing here places orders.**
Inputs: `bt_thursday.py` → `day1_dataset.csv` (74 prints, 2008-04 to 2026-06), `bt_thursday_results.csv` (1,830 rule × structure × exit × IV × slippage rows), `intraday_or60.csv`, `bt_thursday_out.txt` (full printout).
Account: $8,000 Robinhood. Risk per trade: $400–650. Defined risk preferred.

## 0. Verdict (read this first)
**PRIMARY: no robust edge, so skip Thursday by default.** No entry near the open (9:30–10:30) passes the robustness bar in any gap scenario. A bar pass means n ≥ 15, a 95% CI above 0, positive in both 2008–16 and 2017–26, not negative in the last 12 prints, and it holds at 45–75% IV.
- The only candidate that stays positive in both halves of history is the **OPTIONAL, speculative drift trade**: |gap| ≥ 7% and the gap still intact at 3:40 PM. Buy an **Oct 9 $10-wide debit vertical with the gap at ~3:45 PM Thu** and hold it to the **Mon Oct 5 close**.
  - EV **+$63/trade (+0.13R)**, win 63%, n = 19, **95% CI −$46 to +$172 (includes zero)**.
  - Last-12 cut: −0.06R (n = 6). Regime cut: 0.00R (n = 5).
- Take it only if Dominic accepts a coin-flip-plus edge. Use 1 lot, about $450–540 risk. It is not a same-day exit: it holds over Fri and the weekend.

## 1. Scenario tree
Let **C0 = Wed Sep 30 regular-session close** (unknown at writing). Example numbers use C0 = **1065.08** (Tue Sep 29 close). **Recompute the bands from the real C0.** Gap % = Thu 9:30 open / C0 − 1.

| Branch | Open vs C0 (at 1065) | PA map | History (day 1) | Action |
|---|---|---|---|---|
| **Flat** | within ±3% (1033–1097) | NML 1044–1073 / R1 1073–1089 / S1 1030–1044 | n = 21. Open→close is a coin flip (48% continue); gap fills same day 62% of the time. Small up-gaps faded 7/10 | **SKIP.** No structure passes: CIs span 0 and the sign flips between halves |
| **Up 3–7%** | 1097–1140 | Opens inside R2 1097–1125 (1105–1109 double top) | n = 16 up (33 both ways). 44% continue; fill by Fri 31–36% | **SKIP** (3–7% drift −0.11R; open trades −0.12 to +0.03R) |
| **Up 7–12%** | 1140–1193 | Above R2, into R3 1125–1168, then thin to 1233 | n = 7. 5/7 continued open→close; **0 filled** | Don't trade the open. **Optional drift at 3:45 PM** if armed (§2) |
| **Up >12%** | > 1193 | Thin pocket 1168–1233 → ATH supply 1233–1255 | n = 5. **All 5 faded open→close (−1.6% to −4.3%)**, first hour red in all 4 with hourly data, none filled. Speculative (n = 5) | **Do not chase the open.** Optional drift at 3:45 PM if armed. 2 of the 3 gaps >17% lost ~$360 each on the drift trade |
| **Down 3–7%** | 990–1033 | Into S1 1030–1044 / void 1016–1030 / S2 1000–1017 | n = 17. Coin flip; fill by Fri 41% | **SKIP** |
| **Down 7–12%** | 937–990 | Below S2/SMA20 (1000), into S3 941–970 (SMA50, TL ~956, Sep 17 gap) | n = 6. 5/6 continued lower open→close; 0 filled | Don't trade the open. **Optional short-side drift at 3:45 PM** if armed |
| **Down >12%** | < 937 | S4 902–940 (POC). **902.60** is the last D higher low, so below it is a structure break | n = 2 (speculative) | Same as Down 7–12% |

About a ±10.9% (PA median) gap: ~1181 opens above R3 in the thin pocket, and ~949 lands in S3.

## 2. Triggers (all observable live)
**Skip triggers (any of these means no trade Thursday):**
1. |gap| < 7% at the 9:30 open.
2. The gap gets filled at any point on Thursday (price touches C0). This never happened in 20 prints with ≥ 7% gaps. If it does, the day is abnormal, so stand aside.
3. At 3:40 PM, price has given back more than 50% of the gap. That means it is on the C0 side of the **gap midpoint M = (Open + C0)/2**.
4. PA overlay (not backtested; it only removes trades): up branch with 3:40 PM price < **1125** (back inside R2), or down branch with 3:40 PM price > **1000** (back above SMA20/S2, where PA says repair).
5. The Oct 9 vertical costs more than $6.00 at mid, even after moving one strike further out.

**Arm and enter (optional drift trade):** |gap| ≥ 7%, AND none of the skip triggers fired by 3:40 PM. Then at **3:40–3:50 PM ET Thu**, enter with the gap direction (up gap → bull call vertical, down gap → bear put vertical).

**Why not 10:00 AM?**
- The 60-minute opening range on the 11 prints with hourly data showed no follow-through. The opening-range break went with the gap only 4 of 8 times, with a mean move after the break of **−0.82%**. The first hour went against the gap in 8 of 11 prints.
- After a first hour against the gap, 10:30→close drifted back toward the gap direction 5 of 8 times (+1.0% mean). With n = 8, that is speculative and not traded.
- The 30-minute opening range can't be measured: yfinance 30m/15m/5m bars only go back ~60 days, which covers 0 prints.

## 3. Structures
### Optional primary structure: Oct 9 debit vertical WITH the gap, entered Thu 3:40–3:50 PM
- **Long leg:** the first listed strike beyond the current price in the gap direction.
  - Up: the lowest call strike above spot.
  - Down: the highest put strike below spot.
- **Short leg:** $10 further out (calls +$10, puts −$10).
- **Examples (model, 55% IV):**
  - Thu close 1150 → buy Oct 9 1155C / sell 1165C, ~$4.47 mid.
  - Thu close 980 → buy Oct 9 975P / sell 965P, ~$4.61 mid.
- **Size:** 1 contract. Max loss = debit × 100 ≈ **$450–540**. Max gain ≈ $1,000 − debit (~$450–550).
- **Exit:** time stop at the **Mon Oct 5 close (3:45–3:55 PM)**, which is the tested rule. Optional profit-take at a spread value ≥ $8.50 is untested.
  - Do not hold to Oct 9. Exiting at the Fri close instead of Monday tested at about 0 (+0.01R).
- **Same-day exit needed?** No. It is an overnight/weekend hold.
  - PDT: FINRA's June 4, 2026 intraday-margin rule replaced the PDT/$25k rule, and Robinhood says it removed PDT flags on margin accounts. PDT is therefore probably not a constraint, but confirm in the app.
- **Oct 5 expiry note:** the chain lists a Mon Oct 5 weekly. A $10-wide Oct 5 vertical would be cheaper and expire exactly at the time stop. **It is untested here**, so stick with Oct 9.

### Single-leg fallback (if spreads aren't available)
- **6 MU shares with the gap at Thu 3:45 PM.** Hard stop 8.5% from entry (~$95 → **~$570 risk**). Exit at the Mon Oct 5 close.
  - Backtest: n = 19, EV **+$117 (+0.23R)**, win 68%, 95% CI **−$25 to +$258**.
  - Worst case was **−$631** (Jun 2026: stopped out Monday on the suspect Jun 29 wick).
  - Downsides: it ties up ~$6.9k of the $8k account, and weekend gap risk isn't capped.
- A single long option inside $650 is only possible far out of the money (an Oct 9 option at ≤ $6). Its "edge" depends on the IV assumption: +0.81R at 45% IV but −0.25R at 75%. **Not recommended.**

### Tested and rejected (all at open-proxy entry, IV 55%, headline slippage; details in §7)
- **Oct 2 debit vertical with the gap, 1 strike out, $10 wide, held to Fri:** +0.50R, n = 20, CI $14 to $388.
  - But it is **+0.98R in 2008–16 vs +0.10R in 2017–26**, and **−0.18R last 12**, **−0.14R regime**. The edge is old and has faded, so rejected.
  - Same structure with a Thu-close exit (same day): +0.09R, and −0.25R in 2017–26.
- **Credit spread on the fill side at the gap midpoint (the "gap holds" bet):** the midpoint held through Friday in 19/20 prints, but a 1-DTE $5-wide at the midpoint only collects ~$0.30–0.50. EV **−0.03R**, CI −$73 to +$15. The option market already prices in that gaps hold.
- **Fading big up-gaps** (Oct 2 put vertical, target 50% of the gap): +0.14R, n = 12, CI −$107 to +$232. Speculative, and most of the fade happens before 10:00.
- **Long single Oct 2 option:** "+1.25R" is an IV artifact. The historical open→Fri-close move is equivalent to ~107% annualized vol on all prints and ~67% on the last 12, versus the 55% it was priced at. 2017–26: +0.02R; last 12: −0.32R.
- **Shares from the open:** +0.09R for |gap| ≥ 7%.
- **3–7% and <3% gaps:** every structure has a CI spanning 0 and mixed sign across cuts.

## 4. Risk
- One trade maximum. Defined risk **≤ $540** (1 contract of the $10-wide Oct 9 vertical). Hard cap $650 including slippage; if the debit is > $6.00, skip.
- **IV anchors:**
  - Pre-print: Oct 2 ATM ~92–95%, Oct 5 76.6% (UW), Oct 9 68.9% (CBOE overnight) to ~70.5% (yfinance live). The brief's "Oct 9 ≈ 77%" is closer to the Oct 5 number.
  - Forward vol Oct 2→Oct 9 is ~49–59%, so post-print Oct 9 IV should be ~50–60% (55% base). MU has no historical IV series to verify the crush.
  - A $10-wide vertical near the money barely depends on IV: EV +0.10 to +0.16R across 45→75% entry IV and 55→45% crush on exit.
- **Slippage:** 4% of premium per side, floored at $0.10 per leg per side. At a $0.15 floor or 5%: +0.09R.
- **Do not add to it.** Don't roll it, don't average down, and don't hold past Monday.

## 5. Alerts (for the monitoring routine; recompute from the real C0)
| # | Level @ C0 = 1065.08 | Formula | What it means |
|---|---|---|---|
| A1 | **1139.6 / 990.5** | C0 × 1.07 / × 0.93 | Premarket or open beyond one of these → **drift-candidate day**; otherwise skip Thursday |
| A2 | **1096.9 / 1033.1** | C0 × 1.03 / × 0.97 | Open inside = flat band, **no-trade day** (can stop monitoring) |
| A3 | **1193 / 1233** | C0 × 1.12 / PA ATH zone low | Up-gap beyond 1193 = historically fades from the open (5/5); **don't chase**. 1233–1255 is ATH supply |
| A4 | **1125** (up) / **1000** (down) | PA R2 top / SMA20 + S2 bottom | 3:40 PM price must be **above 1125** (up) or **below 1000** (down) to arm the entry |
| A5 | **941 / 902.60** | PA S3 floor / last D higher low | Down branch: below 941 opens S4 902–940; below 902.60 = D structure break (thin air to 800–870) |
| A6 | **M = (Open + C0)/2** and **C0** | set at 9:30 | 3:40 PM price must be beyond M in the gap direction. **A touch of C0 = abort** (never happened for ≥ 7% gaps) |

## 6. Robinhood setup (optional trade only; describe what you see, since labels may differ)
1. Open MU and go into the options chain (Trade → options).
2. **Expiration:** pick **Oct 9, 2026** (not Oct 2, and not Oct 5).
3. **Side:** up gap = calls (buy side), down gap = puts (buy side).
4. **Pick two strikes.** Use the app's multi-leg or spread mode (it may say something like selecting more than one option, or offer a strategy builder).
   - Up gap: **buy** the first call strike above the current price and **sell** the call $10 higher.
   - Down gap: **buy** the first put strike below the current price and **sell** the put $10 lower.
   - Check that the order summary reads as a **debit** vertical, with max loss = debit × 100 and max profit = ($10 − debit) × 100.
5. **Quantity:** 1 contract. That gives max loss of about $450–540. If the debit shown is > $6.00, move both strikes one step further out. If it's still > $6.00, skip.
6. **Limit price:** start at the **mid** (halfway between the spread's bid and ask). If it isn't filled within 1–2 minutes, raise by $0.05 at a time, to no more than mid + $0.20 and never above $6.00. Use a Day order. Don't use market orders on a post-earnings chain.
7. **Exit:**
   - Optional: after the fill, place a GTC limit to **sell to close** the same spread at ~$8.50, if the app allows closing orders on spreads.
   - Otherwise, and in any case: on **Mon Oct 5 at ~3:45 PM ET**, close the spread with a limit at or near the mid.
   - Robinhood may not support stop orders on multi-leg spreads, so the risk is the debit already paid.
   - If the short leg is in the money near expiry, you face assignment risk. The plan exits on Oct 5, well before the Oct 9 expiry.
8. Confirm the account has options approval for spreads (usually the level that allows verticals) **before** Thursday.

## 7. Evidence
**Dataset:**
- 74 after-close prints, 2008-04-02 to 2026-06-24, yfinance daily (auto-adjusted; all fields are ratios, so adjustment is consistent).
- Upstream fix: `pe_moves_all.csv` has **2011-03-22 → really 03-23** and **2011-09-28 → really 09-29** (SEC 8-K press releases). Both are corrected in this dataset; the upstream file is unchanged.

**Day-1 facts (`day1_dataset.csv`):**

| Cut | n | Cont. % (open→close with gap) | Median MFE / MAE from open | Fill day 1 | Fill by Fri (day 2) | Day-2 dir mean |
|---|---|---|---|---|---|---|
| All | 74 | 51% | 2.5% / 1.7% | 27% | 34% | +0.07% |
| <3% | 21 | 48% | 2.9 / 1.4 | 62% | 62% | +0.19 |
| 3–7% | 33 | 48% | 2.5 / 1.7 | 21% | 36% | −0.77 |
| 7–12% | 13 | 77% | 2.4 / 1.7 | 0% | 0% | +2.00 |
| >12% | 7 | 29% (up 0/5) | 1.8 / 4.5 | 0% | 0% | +0.12 |
| Run-up > 10% regime | 21 | 62% | 3.6 / 1.1 | 24% | 29% | +0.22 |
| Last 12 | 12 | 50% | 2.3 / 3.1 | 8% | 17% | −0.26 |

- **≥ 7% gaps (n = 20):**
  - 0/20 filled by Fri.
  - Max giveback through Fri: median 29%, max 88%.
  - Fri close kept ≥ 50% of the gap 19/20 (the miss was Jun 2026).
  - **Threshold-sensitive:** ≥ 6% → 21/26 kept and 2 filled; ≥ 5% → 23/30 kept and 3 filled.
- **Drift from Thu close to Mon close, in the gap direction, ≥ 7%:**
  - Mean +2.46%, median +2.6%, 70% positive.
  - 2008–16: +2.44%; 2017–26: +2.47%.
  - For 3–7% gaps: +0.03%. This is the basis for the optional trade.
- **Now:** 20-day run-up is +11.1% (as of the Sep 29 close), so MU is in the regime. The regime cut adds nothing for the drift (0.00R, n = 5). rv20 is 50.9%, so 1 daily σ ≈ 3.2% and a 7% gap ≈ 2.2σ.

**Optional drift trade robustness** (`bt_thursday_out.txt` §PRIMARY). Cells are EV R, with the 95% CI of $/trade in brackets:

| Variant | n | EV |
|---|---|---|
| Base (55% IV, headline slippage) | 19 | **+0.13R [−46, +172]**, win 63%, leave-one-out min +$42 |
| IV 45 / 65→55 / 75→65 | 19 | +0.16 / +0.12 / +0.10 |
| Slippage $0.15 floor / 5% + $0.15 | 19 | +0.09 / +0.09 |
| 2008–16 / 2017–26 | 9 / 10 | +0.17 / +0.09 |
| Last 12 prints / regime run20 > 10% | 6 / 5 | **−0.06 / 0.00** (speculative) |
| Up-gaps / down-gaps only | 12 / 7 | +0.06 / +0.25 (speculative) |
| Excluding the flagged Jun 2026 print | 18 | +0.18 [−18, +191] |
| ≥ 5% threshold instead of 7% | 26 | +0.07 [−50, +128] |
| 3–7% (control, should fail) | 33 | −0.11 (fails, as expected) |
| Shares fallback | 19 | +0.23R [−25, +258] |

Everything with n < 15 above is **speculative**.

**Data caveats:**
- **Jun 2026 yfinance bars look odd:**
  - Jun 22 close 1211 → Jun 23 open 1080 (−10.8%, no news found).
  - Jun 26 daily close 1132.16 vs the last 60m bar at 1125.39.
  - Jun 29 first-hour low 1023.65 vs close 1145.
  - These affect that print's run-up and Fri/Mon stats.
- 60m bars are unadjusted vs adjusted daily bars (~0.1–0.9% level offsets), so only intraday ratios are used.
- The entry at 10:00 for open trades is proxied by the 9:30 open.
- There is no option-price history: everything is Black-Scholes with flat IV and no skew. Real post-print 1-DTE marks may differ a lot.
- 2008–2012 moves are much larger (MU was an $5–15 stock then); the half-splits show how much this matters.

## 8. Re-eval checklist (after the print)
1. **Wed 4:00 PM:** record C0 and recompute A1–A6 (formulas above).
2. **Wed 4:05–8:00 PM:** after-hours price vs the ±3% / ±7% bands, and the headline (FQ4 vs ~$51.4B / $31.7 EPS bar; FQ1 guide). Only the band matters for this plan.
3. **Thu 8:00–9:25:** classify the premarket branch. If it is inside ±3%, the plan is **done: skip**.
4. **Thu 9:30:** record the open, gap %, and M = (Open + C0)/2. **No trade at the open.**
5. **Thu 10:00:** log Oct 2 and Oct 9 ATM straddle / IV for the record. It doesn't change the vertical decision; it does matter if anyone proposes long single options or credit spreads.
6. **Thu 15:40:** check skip triggers 2–5 and A4/A6. If armed, pull the Oct 9 chain, price the vertical at mid, and confirm debit ≤ $6.00 and risk ≤ $650. Then 1 contract.
7. **Fri:** no action needed (the tested rule holds). Note if Friday closes beyond C0. That never happened in the sample and would be a thesis break; closing early is untested but reasonable.
8. **Mon Oct 5 15:45:** close.
9. **Planner cross-check:** `PLANNER.md` was not present when this plan was written; Planner's `planner_bt/` work was in progress in this folder. Reconcile when it lands (§9).

## 9. Planner reconciliation
- PENDING. When this plan was finalized, `/workspace/plans/20261001-mu-thursday/PLANNER.md` did not exist; only `planner_bt/` scripts/CSVs in progress.
