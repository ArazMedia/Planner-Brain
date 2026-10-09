# BRIEF: 20261009-ev (Planner -> RA lead, PA, UW). Fri 10/9 ~13:00 ET
Scope and tasks: see 02_plan.md. Proposal only. Account: $7,700 cash, L3, debits only, no margin, Dominic sets risk. Flat beats weak evidence. No yfinance or outside price data (PA = price history, UW = flow history).

## Factor gate (grade A-F)
Factors, each scored -2..+2: structure/level quality; volume on trigger; trend/regime; gamma/GEX vs the strikes (wall above = headwind, pin); flow (opening vs closing, $ premium, sweep vs block); catalyst risk inside expiry (CPI 10/14, EIA 10/15, GOOGL ER 10/28); IV/vol (debit paid vs RV); liquidity/OI and bid/ask at the strikes.
RA sets the weights in RA_factors.md. Weighted score -> A (>=+1.2), B (+0.6..1.2), C (0..0.6), D (-0.6..0), F (< -0.6). Don't let flow and gamma double-count the same positioning.

## Probabilities
- Prior = PA base rate for the same trigger type on that name (target before stop, within the expiry window), with n and lookback. If n < 15, shrink toward a pooled/cross-name rate (e.g., beta prior with weight ~10).
- Adjust with bounded log-odds nudges from the factor score (max +/-0.5 log-odds in total), pre-declared, not fitted.
- Cross-check against the market-implied p (deltas / lognormal with UW IV; RA_mkt_probs.md). If our p(target) exceeds the market's by >10pp, justify it or cut it.
- Outcomes: target (full width at expiry or a TP exit), partial (between the strikes / midpoint exit), stop (fail level hit -> exit at the modelled residual).

## EV
EV = p_t*(width*100 - debit) + p_p*(partial - debit) + p_s*(residual - debit), net of exit costs (half the bid/ask per leg from UW; state the assumption otherwise). Report EV $, EV % of debit, break-even p, and EV at p(target) +/-10pp.
Verdict: TAKE only if EV > 0 across the +/-10pp range and the evidence is at least a B grade; WATCH if EV > 0 only at the base case or the trigger hasn't fired; SKIP otherwise.

## Owners and deadlines
- PA: inputs/PA_baserates.md (+csv), ~15:30.
- UW: inputs/UW_flowhist.md, ~15:30.
- RA: RA_factors.md, RA_spy_baserates.md, RA_tsla.md, RA_mkt_probs.md, ~14:30-15:30; final grade sign-off.
- Planner: outputs/EV.md, ev_calc.py, ev_table.csv; Fable critic; SUMMARY_FOR_ARAZ.md. RA signs off before it goes to Araz.
- Extra bars/flow: write REQUESTS.md (symbol, timeframe, lookback) and SendToAgent Planner. I route it to PA/UW.

## Deliverable to Araz
One line per setup, ranked: '<rank>. SETUP spread | grade | EV $ (% debit) | p(target) | trigger'.
