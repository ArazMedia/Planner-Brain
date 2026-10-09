# CRITIC: EV evaluation 2026-10-09 (independent; research only, no trading)
Critic pass on `EV.md` / `ev_table.csv` / `ev_calc.py` (13:05 ET). `CRITIC_self.md` was not supplied; `EV.md` §9 is taken as the self-critique. `ev_calc.py` cannot be re-run here (PA bars live on the desk box), so every number below is recomputed standalone from the table's parameters. My risk-neutral MC reproduces the model's TSLA market buckets (.333/.049/.030/.588 vs .335/.048/.029/.589), so comparisons are like-for-like.

## Verdicts
- **TSLA Oct16 385/390C: DOWNGRADE WATCH → SKIP.** History EV **−$6** (was +$40) once the stop is the 15m close Dominic actually uses; drift-neutral **−$3 to +$5** (was +$18) once RA's flow +2 is replaced by UW's tag 0 and the trend factor (= the trigger) is dropped. Inside the ±$7 noise band on every honest variant.
- **USO Nov20 150/160C: DOWNGRADE WATCH → SKIP.** Drift-neutral **+$5** with UW's −1 tag (was +$12; noise line $10), **−$30** at realistic round-trip costs. History +$68 is "market +0.83 log-odds" by construction; a BRIEF-consistent cap gives +$26 to +$35. The stop level is undefined between the desk's own files.
- **The 8 SKIPs: AGREE. Nothing upgrades.** PLTR Oct16's B +$32 is 100% factor nudge on A ≈ 0 (4/25 settle; −$5 with UW's tag), and its grade is inflated vs the pending rows because volume is scored only once a trigger fires.
- Flat is right. The ranking key min(A, B) already says edge ≤ 5% of debit everywhere; the two WATCHes survive only on the +10pp cap and on RA positioning scores that UW does not corroborate.

## 1. Overconfidence vs market; is +10pp defensible?
- Six of ten rows sit exactly at market +10pp, so their EV is a ceiling, not an estimate. Report them as ranges: TSLA [−$4 at market, +$40 at cap], USO [−$17, +$68].
- Absolute +10pp is not neutral. In log-odds it is +0.44 for TSLA (34→44%) and **+0.83 for USO (10→20%)**, more than the BRIEF's entire ±0.5 factor budget, granted on top of it. A +0.5 log-odds cap gives USO p_t 15.0%, EV +$35; +0.4 gives 13.8%, +$26. TSLA barely moves (cap 45%).
- No risk-premium defence exists: equity drift over 5 sessions shifts N(d2) by <1pp. Everything above market is "the 2020–26 tape beats the market", and the model's own drift-only column shows the trigger adds ~nothing (TSLA +0.1pp pooled; USO +3.1pp).
- Sampling error swamps it: TSLA own 24/58 = 41% ± 6.5pp is 1.2 SE above market and 0.2 SE above its own drift-only 40%; USO 9/39 = 23% ± 6.7pp is 1.3 SE above its drift-only 14%. Neither rejects "no edge".
- Correct in the model: MC-with-stop (TSLA 34%, USO 10%), not N(d2) (43%, 29%), is the comparator. But the cap must then follow the corrected stop rule (§3): TSLA's falls to 34%.

## 2. Double counting
Done well: trend out of A, gamma+flow merged once, UW as replacement not addition, structure never nudged. Three leaks remain:
1. **Trend in B is the trigger.** RA's TSLA trend +1 = "short-term turn up, 15m higher lows, on 381 support", i.e. the entry condition, already in the conditional prior and the (≈0) trigger lift. Dropping it: B +$18 → +$5 (RA pos) → **−$3** (UW pos).
2. **UW tags were applied to A only.** `EV_UWpos` leaves USO unchanged "because the cap binds", but B is uncapped and was never recomputed with UW. USO B at −1 (153C sold-call build 360→8,954; call walls 151/154 between the strikes): +$11 → **+$5**. TSLA B at 0: +$18 → **+$5**. USO 141.76-stop variant: +$18 → +$8. All under the 3%-of-debit noise line.
3. **The shrinkage pool is not neutral.** It is a 20-day-breakout study on QQQ/MU/AMD/NVDA/META/GOOG/TSLA/PLTR/SPY 2020–26: 6pp above market for TSLA's geometry (40% vs 34%), 8pp above for USO's (17.5% vs 9.7%), and a tech basket applied to oil. Shrinking toward drift does not remove drift.

Also: RA's TSLA flow +2 rests on 385C **Nov13** ($2.5M, earnings-week paper) and 400C **Jan27**. UW's Oct16 385C read is two-way (BID $1.58M vs ASK $1.44M). For an Oct16 spread, Oct16 flow is the evidence.

## 3. Touch→settle and stop modelling
- Touch→settle is handled (PA's 36–98% touch rates unused). The analog is still wrong for TSLA: the n = 58 sample conditions on a **daily close above the 20-day high** (388.55-type); the trade enters on a **15m close above 386.82**, below that high, after PA logged "confirmation failed" and a 4h bar that gave back 5.15 of its range. PA's closer analog (flip-retest hold, n = 10) runs 40% / stop-first 30% vs 60% / 36%.
- **Daily close for a 15m stop is the single largest flattering assumption.** MC at chain IV, 26 intraday bars + 30% overnight variance, same total variance as the model:

| TSLA 385/390C | daily-close stop (model) | 15m-close stop (Dominic's rule) |
|---|---|---|
| market p_t / p_s | 33.3% / 58.8% | **24.0% / 72.8%** |
| P(stopped \| daily-rule TARGET) | – | **28%** (PARTIAL: 52%) |
| history A: p_t / EV | 43.5% / +$40 | **31.4% / −$6** (extra stops exit ≈ $141 net; blended V_s $103) |
| drift-neutral B: RA pos / UW pos | +$18 / +$5 | +$12 / +$2 |

  At RV20 (30.6%) the stop-through is 21% and market p_t 27%: the sign does not depend on the vol choice. The stop is 1.5% from entry = 0.6 of TSLA's daily SD, and CPI prints pre-open on day 3; a 15m stop cannot act on a gap.
- USO's stop *is* a daily close, so the rule matches, but 147.12 is 0.23 daily SD under the trigger (~40% odds of closing through it on any single day), hence 73–88% stop-outs, and EV.md itself notes WATCHLIST lists 147.12 as the early 4h *trigger*, not a fail. Until that is settled the setup is undefined. With it, EV is a stop-residual model: each $10 of V_s moves EV $7.3. Residual at IV 40 / 37 / 35% instead of 45%: EV −$12 / −$20 / −$26. A 1.5-ATR gap through the stop (EIA 10/15, CPI, a Hormuz de-escalation, which drops oil price and oil IV together) makes the loss per stop $162, not $96.

## 4. Exit-cost assumptions
- Mid on entry, half the bid/ask per leg on exit is the best case for a $7.7k retail account. Realistic: entry half-way between mid and natural; full bid/ask per leg on exit (stops are urgent exits inside the −gamma pocket UW maps; deep-ITM legs on expiry day quote wider than 10¢; a cash account that cannot carry 100 TSLA at $385 is force-closed in the last hour).
- Under that case: TSLA A +$25 (daily stop) / **−$21** (15m stop). USO A +$26 but **B −$30** (UW −1: −$36). USO is uniquely cost-sensitive: 84% of B paths pay the round trip on a stop, so each $10 of exit cost removes ~$8 of EV. Closing a TSLA target at 3× the quoted half-spread costs a further $9.

## 5. Selection bias
- Agree with EV.md §5/§8; B is the right fix in principle, but §2 shows it still carries trigger-as-trend and RA-only positioning. Stripped, B = market EV ≈ −exit costs on both WATCHes.
- USO 2020-11→2026-05 is a $30→$148 instrument (drift-only p_t 14% vs market 10%); TSLA 2020-06→ is ~6×. Complete-horizon filtering drops the newest events (USO after 2026-05, TSLA after 2026-08): the current regime is partly excluded while the run that put these names on the watchlist is fully included.

## 6. Correlation and CPI 10/14
- The tech+CPI bucket rule (at most one of PLTR/TSLA/GOOGL/SPY bull) is right. But the two WATCHes are not independent either: CPI 08:30 sits inside both; a hot print (yields/USD up, risk-off) hits TSLA via duration and USO via USD/demand the same way, and both stops are under one daily SD. If both were on: $571 debit (7.4% of account), expected joint stop loss ≈ $240, ≈ $375 on gaps. Size is Dominic's call; the point is the two "independent" lotteries share their dominant stop-out day.
- Catalyst risk reaches only the grade (USO catalyst −1 × 25%), never the EV: event days are not isolated and the ±10pp band is the only accommodation. For a 5-session trade with the event on session 3, that is a quarter of the horizon.

## 7. Final
TSLA → SKIP (A −$6 to +$25 across stop/cost cases; B −$3 to +$5). USO → SKIP (A is cap-defined; B +$5 to −$30; stop undefined). Even if Dominic's TSLA stop were a daily close <381, B stays ≤ +$5 and fails the modeller's own tightened WATCH rule under UW's positioning. No upgrades: PLTR Oct16 A ≈ 0 (−$5 with UW); SPY bull B −$7 with the 780 pin capping the settle; GOOGL B < 0 with ER + FOMC inside. The report's own machinery says flat once the cap and the RA-only nudges are set aside.
