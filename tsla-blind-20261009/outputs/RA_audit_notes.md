# RA audit notes: does the desk default to "flat" because of its safeguards rather than the math?
Written Fri Oct 9 ~13:14 ET by RA. **SEPARATE from the blind file `RA_tsla_asof.md`.** These notes may use outcome information from past sessions, but RA did NOT open `TSLA_outcome.md`. The TSLA blind case is discussed here only in terms of what the framework *can* output, not how it turned out.

Sources:
- `../../BRIEF.md`
- `../../outputs/EV.md` and `../../outputs/ev_calc.py` (lines cited)
- `/workspace/session-desk/ledger/outcomes.csv` and `deviations.md`
- `/workspace/TRADE_HISTORY.md`, the consolidated table of executed and considered-not-taken ideas. Many of the original sd-review / plan-card files it cites were deleted on 2026-10-07; TRADE_HISTORY is the surviving record.

## (a) Mechanisms that push toward flat, ranked by how decisive they are

1. **The +10pp cap combined with the ±10pp robustness test makes TAKE close to impossible by construction.**
   - **The cap (`ev_calc.py` ~L459–463):** `p_t` is cut to `mkt_MC + 0.10` whenever it exceeds that.
   - **The TAKE test (L526):** TAKE needs `EV(p_t − 10pp) > 0`.
   - **Together:** for any row at or under the cap, `p_t − 10pp ≤ p_mkt`. EV at the market probability is about −exit costs, because the market prices each spread near fair (EV.md §5.1: risk-neutral EV −$4 to −$29 on every row).
   - **Result:** EV at −10pp is ≤ ~0 for every row unless our valuation buckets happen to differ from the MC's. EV.md bears this out: TSLA +$1, SPY bull −$0, USO 150/160 −$3, GOOGL −$51 / −$52 (15pp band).
   - **TAKE therefore requires the market to be mispriced by more than the cap allows.** The rule set can only ever print WATCH or SKIP. This is a structural property, not evidence about the setups.
2. **The cap is one-sided.**
   - When history says `p_t` is more than 10pp *above* the market, it is cut.
   - When history says `p_t` is more than 10pp *below* the market (e.g. the PLTR rows, SPY bear), nothing raises it.
   - 6 of 10 rows were capped (EV.md §5.3). The cap can only lower EVs.
3. **Drift-neutral EV_B is used one-way: it only demotes.**
   - L531: WATCH becomes SKIP if `EV_B < 0`. This "critic fix" demoted SPY bull and GOOGL 355/365, taking the BRIEF rule's 4 WATCHes down to 2.
   - The reverse never happens. PLTR Oct16 had **EV_B +$32**, grade B and a fired trigger, yet went SKIP because EV_A was +$3, under the 3% noise floor (L524).
   - Each safeguard is applied in whichever direction gives a less-taken book.
4. **EV_B starts from the market, which is ~−costs, and its nudge excludes structure.**
   - The B estimate begins at the risk-neutral buckets. It can only go positive through the measured trigger lift (±3pp, noisy) plus a nudge capped at 0.5 log-odds.
   - **The nudge explicitly excludes structure** (EV.md §2.3: "structure is the trigger type the prior already conditions on"). For level-test setups like TSLA at 370.25, level quality *is* the thesis, and it gets zero weight in EV_B.
5. **Grade compression.**
   - **n/a factors score 0 but keep their weight.** On Oct 9: USO/IBIT gamma, and in the blind case, gamma and flow.
   - **Pending triggers score volume as 0.**
   - **Reaching B (≥ +0.6) needs several +2s.** On Oct 9 no setup reached A, and all D/F rows are SKIP regardless of EV (L527: "flat beats weak evidence").
   - **In the blind TSLA case** the as-of grade is C (+0.55), and +0.70 / B only if the absorption on the test bar counts. Under these rules, a C caps the verdict at WATCH even before EV.
6. **Shrinkage plus hard shrink on small n.**
   - Dirichlet W = 5 for n ≥ 15, W = 10–20 otherwise (TSLA W = 20). That pulls toward pooled rates which embed sample drift.
   - Shrinkage is fine in itself. Combined with mechanisms 1–3, it removes most of any own-name signal before the cap even applies.
7. **Cost conservatism stacked three times:**
   - Exit costs on both legs, plus a full-spread-entry sensitivity, plus a 3% |EV| noise floor.
   - Each is defensible. Together, on $150–250 spreads, they eat 5–15% of the debit, about the size of the edge any nudge could create.
8. **Settle-only payoff with no take-profit exit.**
   - BRIEF allows a "TP exit". `ev_calc` values outcomes at expiry or at the stop.
   - Short-dated debit spreads are normally managed at 50–70% of max. EV.md's own ledger evidence shows big MFE before stops (09-14 SPY-01: MFE 3.70R before −1R).
   - Ignoring path value systematically understates EV for momentum and mean-reversion entries.
9. **Policy-level priors.**
   - BRIEF: "Flat beats weak evidence".
   - EV.md §0: "flat is the default"; at most one name per correlation bucket.
   - These are explicit preferences, not math, and they should be reported as such.

**Bottom line for (a):**
- **What's sound:** the math (market ≈ fair, history ≈ drift) is a legitimate finding.
- **What's not:** the verdict *rules* turn "no demonstrated edge" into "never TAKE". Mechanisms 1 and 3 should be fixed so they apply symmetrically, or TAKE should be redefined; see the proposals at the end.

## (b) Factors missing from the framework (they matter for setups like the 370.25 test)
- **Intraday mean reversion at a tested level.**
  - A wick through a multi-touch level followed by a reclaim close. The event studies are daily-close only (20-day high / pivot breaks), so a 5m spring can't be represented.
  - PA's `TSLA_5m_hist` request is the right fix.
- **VWAP position and reclaims.** Price vs session VWAP, and the distance to it as the first target. It isn't in the rubric.
- **Relative volume at the test vs on the reclaim.** For example, absorption: a 1.6x test bar followed by a 0.5x reclaim. "Volume on trigger" covers breakouts only.
- **Intraday dealer gamma flip and live GEX.** Today's UW snapshot is session-delayed or EOD, so the flip at test time isn't captured.
- **Time of day.** The 13:30–14:00 post-lunch window, power-hour drift, and the time left for a 1DTE to work.
- **0DTE/1DTE convexity.** 1DTE 370/380C ≈ $270 for $1,000 max (R:R 2.7), and 375/385C ≈ $134 (R:R 6.5). The EV engine only handles H = 5 or 30 sessions.
- **Event-premium term structure.**
  - IV of 1DTE vs 1-week vs post-earnings expiries, against RV. In the blind case, 1DTE ATM ~26% vs RV10 34.5% is cheap.
  - The rubric's IV factor only compares the debit paid to RV20.
- **Sector and tape context.** QQQ/semis intraday (e.g. the 12:42 FT OpenAI story) as a separate regime term, not folded into trend.
- **Skew carry.** Selling the richer-skew leg. RA scores this ad hoc (SPY bear +1), but it isn't modelled.
- **Path value and management.** MFE distribution, TP at x% of max, time stops.

## (c) How often "flat" is the call vs how often flat was right

**Proposed method (prospective, pre-registered):**
1. **A `flat_ledger.csv` row for every setup the desk evaluates (TAKE / WATCH / SKIP).** Record the decision time, the spread, the full-spread debit, the trigger and fail rules, `p_t`, `p_mkt`, and the reason code. Reason codes: cap-binding, D/F grade, trigger pending, demoted by EV_B, noise floor, correlation bucket, policy.
2. **A counterfactual for every SKIP and untriggered WATCH, as if taken at the full-spread debit.** For WATCH, entry happens when the trigger fires. Mark at three fixed points:
   - (i) expiry settle
   - (ii) a TP rule (50% of max) / stop rule
   - (iii) +1 session
   - Use PA bars plus CBOE closing quotes only.
3. **Metrics:**
   - **Flat rate** = (SKIP + untaken WATCH) / evaluated.
   - **Flat-right rate** = the share of flat calls whose counterfactual P&L ≤ −exit costs.
   - **Opportunity cost** = the sum of positive counterfactual P&L, compared with losses avoided.
   - **Calibration:** a Brier score / reliability curve of `p_t` vs outcome, and the same for `p_mkt`.
   - **Breakdown:** split by reason code to see *which* safeguard costs money.
4. **Decision rule:** with n ≥ 30 flat calls, test the mean counterfactual EV of SKIPs against 0 (sign test / bootstrap).
   - If SKIPs are positive on average and significantly so, the gate is too tight.
   - If they're ≤ 0, flat was right.

**What can be computed now (retrospective, from recorded outcomes only; WEAK, n small, selection-biased):**
- **Desk ledger** (`outcomes.csv`, 9/11–9/21, 11 rows, 7 sessions):
  - **Taken: 0 of 11.**
  - Cards: 5 (four on 9/11, one on 9/14), with grades A+ to A++. No-card days: 6 rows (9/11 pre-open, then 9/15, 9/16, 9/17, 9/18, 9/21).
  - Card outcomes:
    - SPY-01 9/11: cancelled when price cleared its stop. **Flat right.**
    - SPY-02 9/11, A++: unfilled, entry never printed; sim +0.80R open. **Flat wrong / no fill.**
    - SPY-03: never triggered. n/a.
    - SPY-04: failed hold, rule not met. **Flat right.**
    - SPY-01 9/14: sim −1R. **Flat right.**
  - The no-card days are all self-graded "No A++ correct", **with no counterfactual measured.**
    - 9/16 ran 12.07 pts (2.2x the expected move) with an FOMC dump.
    - 9/21 was an R1-break grind.
    - These are unfalsifiable as recorded.
- **TRADE_HISTORY "considered, not taken"** (20 rows, 9/7–10/5), with outcomes as recorded:

| Flat call | Recorded outcome | Label |
|---|---|---|
| ORCL puts (9/8) | Stand-down right, view wrong | Flat right |
| ADBE puts (9/10) | Direction right but small vs rich IV | Flat right / neutral |
| SPY 9/11 SPY-01 | Price cleared the stop | Flat right |
| SPY 9/11 SPY-04 | Failed hold | Flat right |
| SPY 9/14 SPY-01 | Sim −1R | Flat right |
| SPY 9/9 regime-short / 0DTE short ideas | "Worked … not executed" | Flat wrong |
| SPY 9/10 CF-2/CF-3 pin longs | "Knowable in real time", est. +$120–700 | Flat wrong |
| SPY 9/11 SPY-02 (A++) | Unfilled; sim +0.80R | Flat wrong (by fill mechanics) |
| SPY 9/8 770/760P | Never Ready, "direction mildly right" | Flat mildly wrong |

  - **Unknown / constraint-driven (no grade): 11.** USO adds ×2, KR, USO call credit, NEOV (undefined risk), SFIX, MU ×2 (one was margin), BTC/IBIT (no trigger), SPY-03 (no trigger), plus the 5 no-card days counted once.
- **Tally:**
  - The desk's own cards and ideas since 9/7 were flat in ~100% of cases. The only executed trades came from Dominic directly (USO call +$762; 9/10 SPY 0DTE puts: one stopped, one unrecorded; 10/5 SPY 770P −$171).
  - **Of the 9 flat calls with a recorded outcome, flat was right in 5 and wrong in 4 (≈55% right).** n = 9 is weak.
  - **The wrong ones cluster on intraday SPY mean-reversion / pin plays** (9/9, 9/10, 9/11 SPY-02). That's exactly the factor class missing in (b).
- **Today's EV run (10/9):**
  - **0 TAKE, 2 WATCH, 8 SKIP.**
  - The cap bound on 6 of 10 rows.
  - The EV_B demotion removed 2 WATCHes.
  - The noise floor turned PLTR Oct16 (B, fired, EV_B +$32) into a SKIP.
  - Outcomes aren't known yet. Log these 10 as the first `flat_ledger` rows.

**RA's initial view:**
- Dominic's suspicion is **partly right**.
- **Where the math is honest:** the market prices these spreads near fair, and the daily-bar history shows little trigger lift.
- **Where the verdict layer goes wrong:**
  - It's asymmetric: the one-sided cap, demotion-only EV_B, and stacked costs.
  - It's structurally unable to print TAKE (mechanism 1).
  - It's blind to the intraday factors where the recorded flat-wrong cases actually occurred.
- **Proposed fixes, for Planner/critic:**
  1. Make the cap symmetric (±10pp), or replace it with a Bayesian blend toward the market.
  2. Run the robustness test around the *uncapped* estimate, or require EV > 0 at −5pp.
  3. Use EV_B both ways: promote when EV_B > 0, grade ≥ B and the trigger has fired.
  4. Value a TP exit.
  5. Score n/a factors with their weight removed (renormalise), rather than as 0 with weight kept.
  6. Add an intraday level-test module (5m base rates, VWAP, RVOL, time of day) for 0–1DTE.
  7. Start the `flat_ledger` today.
