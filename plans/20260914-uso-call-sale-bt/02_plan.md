# Plan: USO call-sale strategies + backtests — catalog of four strategies (defined CCS, covered, timed reject-at-supply, wall-fade) with entry/exit tied to PA S1–S4 / wall 160, versioned historical level spec, walk-forward backtests (hit rate, avg R, max DD, n) split by regime (`AI-up` vs `OE reject`) and by FOMC/BOJ filter, decision-complete REPORT; proposals only, no live trade cards

```
plan_id: 20260914-uso-call-sale-bt
title: USO call-sale strategies + backtests — catalog of four strategies (defined CCS, covered, timed reject-at-supply, wall-fade) with entry/exit tied to PA S1–S4 / wall 160, versioned historical level spec, walk-forward backtests (hit rate, avg R, max DD, n) split by regime (AI-up vs OE reject) and by FOMC/BOJ filter, decision-complete REPORT; proposals only, no live trade cards
requester: Dominic (via Research Analyst; host Sequence T1–T6 already issued)
created: 2026-09-14
status: ready
brain: fable-5.1
depth: in-depth
version: 1
```

> **Execution state at plan time:** the host Sequence for this work has **already been issued** to the desk as six steps T1–T6. This plan **formalizes** that Sequence — same `plan_id`, same task numbers, same order (PA versioned level spec → UW optional cache → RA catalog → RA methods → RA backtests → RA `REPORT.md`), same owners — so the desk has a checkable card and a definition of done. It does not add steps, renumber tasks, rename the plan, or change owners relative to the host Sequence. **This plan is not for today's execution:** no step is due on 2026-09-14, nothing in it produces a live trade card, and every output is a proposal. The prior plan `20260914-uso-call-sale` (closed) supplies **context only** — its Oct 16 165/175 call credit spread is an illustration instance in the catalog, not a candidate re-decided here.

## Goal

Dominic wants the USO call-sale idea taken from a single-instance read (the closed plan) to **strategies with evidence**: a catalog of four call-sale strategies with entry and exit rules precise enough to backtest and to journal, tied to the Price Action Analyst's supply levels S1–S4 and the UW GEX call wall at 160; historical backtests of those rules with the four numbers Dominic asked for (hit rate, average R, max drawdown, n) split by regime and by event filter; and a REPORT that says, per strategy, whether the history supports it, with the caveats stated once. FOMC and BOJ enter as **filters** — a column in the results table — not as sermons.

Four things must be in the RA `REPORT.md`, each traceable to a task:

1. **Catalog** — four strategies, fixed ids `C1` defined call credit spread at supply, `C2` covered call at supply, `C3` timed reject-at-supply, `C4` wall-fade; for each: structure, trigger, entry timing, short / long strike rule, expiry (DTE) band, exit rules (profit target, time stop, level stop), regime applicability, event handling, account requirement, and a `backtestable` flag stating what is proxied. Every trigger and every exit is written against `S1`–`S4` or `wall 160`, and a **current-instance table** maps each strategy onto today's levels as an illustration, labelled `illustration — not a card`.
2. **Historical backtests** — for each strategy × regime bucket × event bucket: `n`, `hit_rate`, `avg_R`, `max_DD_R`, plus the flags that make a small or proxied sample honest (`LOW-N`, `NO-READ`, `PREMIUM:MODELED`, `ZONE:PROXY`, `WALL:NA`). Walk-forward: no level, regime label, or wall enters a trade before the date it was knowable.
3. **Regime and event filters** — regime buckets `AI-up` / `OE reject` / `NEUTRAL` (the two named buckets are PA's labels; `NEUTRAL` is the residual), event buckets `EVT:OUT` / `EVT:IN` / `EVT:SPAN` for FOMC and BOJ decision days; each is a split of the same trade list, reported as a table with at most one line of reading.
4. **Proposals only** — numbered proposals in the REPORT (which strategies to journal forward, which to drop, what the next `plan_id` would test), each marked `proposal only`; no sizing, no order, no live trade card, no thesis / `risk.md` / routine / skill edit.

Owners: Research Analyst (catalog, methods, backtests, REPORT), Price Action Analyst (versioned historical level spec for S1–S4 / wall), UW (optional cache of wall history). No MHM.

## Success criteria

Must (each has exactly one task):

| id | criterion | checked by | task |
|---|---|---|---|
| M1 | `pa_level_spec_v1.md` exists with header `version: 1`, `as_of:` date, `spot:` + read timestamp, `ATR14:`; a `## Rule` section stating PA's **mechanical** zone-identification rule (timeframe, swing-high definition, zone low/high construction, validity / breach rule, test counting) or the literal `rule: discretionary` with the closest mechanical proxy PA accepts; a `## Current levels` table with exactly four rows `S1`–`S4` (columns `level_id`, `timeframe`, `low`, `high`, `formation_date`, `tests`, `status`, `dist_$`, `dist_ATR`), all `low` < `high`, all above `spot`, `formation_date` ≤ `as_of`; a `## Wall` section naming `wall 160` as an external (UW) level with PA's confluence read (`confluence: Sn` or `confluence: none`); a `## Regime labels` section defining `AI-up` and `OE reject` in price / structure terms; a `## Changelog` line; the file contains **no fundamentals tokens** (`Hormuz`, `pipeline`, `FOMC`, `BOJ`, `OPEC`, `inventor`, `WTI`, `geo`) | file + grep rows; row count = 4; negative grep | T1 |
| M2 | **Optional.** If UW holds historical call-wall data for USO: cache files (call wall by date, put wall by date, zero-gamma by date, as far back as available; plus the current GEX profile) are fresh at the UW cache location and `uw_cache_index.md` lists **paths + timestamps + field names + date range only** — no values, no exports, no images; UW writes nothing else under `outputs/`. If UW holds no history: `uw_cache_index.md` exists with the single line `WALL:NA — no historical call-wall data` plus the current-profile row if refreshed | index file; each listed path exists; index has no numeric strike / gamma values; or `WALL:NA` literal | T2 |
| M3 | `ra_catalog.md` has one section per strategy (`## C1 Defined CCS at supply`, `## C2 Covered call at supply`, `## C3 Timed reject-at-supply`, `## C4 Wall-fade`), each with the fields `structure`, `trigger`, `entry_timing`, `short_strike`, `long_strike`, `expiry_DTE`, `exit_profit`, `exit_time`, `exit_level`, `regime_intent`, `event_rule`, `requires`, `backtestable`; every `trigger` and `exit_level` cell references at least one of `S1`, `S2`, `S3`, `S4`, `wall 160`; a `## Current instance` table (one row per strategy) mapping the rule onto `pa_level_spec_v1.md` levels with the literal `illustration — not a card`; a `## Definitions` section defining `timed`, rejection bar, buffer, and the R unit per strategy; `proposals only`; `## Sources` citing `pa_level_spec_v1.md` | file + headings + grep per section | T3 |
| M4 | `ra_methods.md` has `## Data` (instrument, series, source, adjustment for the 2020-04-29 1:8 reverse split, date range, pull timestamp, OVX series), `## Walk-forward` (the look-ahead rule for levels, regimes, walls), `## Zone generation` (PA rule from T1 or `ZONE:PROXY` with the proxy stated), `## Premium model` (`PREMIUM:MODELED` with model, IV source, strike convention, cost), `## Metrics` (definitions of `n`, `hit_rate`, `avg_R`, `max_DD_R`, R per strategy, overlap rule), `## Regime rule` (mechanical definitions for `AI-up`, `OE reject`, `NEUTRAL` with thresholds), `## Event rule` (FOMC / BOJ calendar source, `EVT:OUT` / `EVT:IN` / `EVT:SPAN` windows), `## Sample-size rule` (`LOW-N` and `NO-READ` thresholds), `## No-search rule` (parameters fixed from `ra_catalog.md`; sensitivity limited and labelled `SENS`), `## Windows` (full, 5y), `## Sources` | file + headings + grep tokens | T4 |
| M5 | `ra_backtests.md` + `backtests/` exist: `backtests/run_bt.py` (or equivalent script) and `backtests/events.csv` (FOMC + BOJ dates with source), `backtests/trades_C1.csv` … `trades_C4.csv` (or `trades_C4.csv` absent with `WALL:NA` stated), `backtests/summary.csv`; `ra_backtests.md` has `## Summary` table with one row per (strategy × regime × event × window) carrying `n`, `hit_rate`, `avg_R`, `max_DD_R`, `flags`; every row with `n` < 20 carries `LOW-N`, every row with `n` < 10 carries `NO-READ`; a `## Per-strategy` section per `C1`–`C4` with the full-sample and 5y headline rows, the equity curve in R (path to a PNG under `backtests/`), worst trade, and the regime × event cross-table; `## Sensitivity` labelled `SENS` (≤ 2 parameters per strategy, ±1 step) or `SENS: none`; `## Regime proxy validation` against PA's labelled sample if T1 supplied one (S1) or `na`; `## Reproduction` (command line + data pull timestamp); `## Sources` | files exist; CSV row counts match `n`; grep tokens; flags applied per rule | T5 |
| M6 | `REPORT.md` is decision-complete: `## Verdict` with exactly one token per strategy — `C1:`, `C2:`, `C3:`, `C4:` each followed by exactly one of `EDGE` / `NO-EDGE` / `LOW-N` / `NA` — and one line naming the regime bucket and event bucket in which each `EDGE` holds; `## Catalog summary`; `## Backtest results` (headline table, full + 5y); `## Regime filter`; `## Event filter` (table + ≤ 1 line of reading; section ≤ 8 lines); `## Level spec` (version cited); `## UW read` (RA prose ≤ 6 lines + cache path + timestamp, or `WALL:NA`); `## Caveats` (modeled premium, zone proxy, look-ahead, sample, split adjustment); `## Proposals` (numbered, each ending `proposal only`; no sizing; no order); `## Compliance`; `## Verification`; `## Sources`; contains `no live trade cards` and `no trade today`; last line is the post reference to Dominic | file + headings + token counts + negative grep + post reference | T6 |

Should:

| id | criterion | task |
|---|---|---|
| S1 | `pa_level_spec_v1.md` includes a `## Historical labels` table of ≥ 10 past USO instances PA would label `OE reject` and ≥ 10 PA would label `AI-up` (date, adjusted price, level or structure), as a validation sample for RA's mechanical regime proxy | T1 |
| S2 | `ra_catalog.md` `## Current instance` row for `C1` reproduces the closed plan's Oct 16 165/175 spread as the illustration and cites `plans/20260914-uso-call-sale/outputs/REPORT.md` as its source, so the two plans read consistently | T3 |
| S3 | `ra_backtests.md` reports, per strategy, `median_R`, `profit_factor`, `avg_hold_sessions`, and the fraction of trades whose short strike was touched intraday but not breached at the close (`touch_no_breach`) | T5 |
| S4 | `REPORT.md` `## Proposals` includes a forward paper-journal spec (file path pattern `outputs/journal/YYYY-MM-DD.md`, fields, owner RA) for any strategy whose verdict is `LOW-N` or `NA`, with `Dominic: approve / decline` as the last line of that section | T6 |

## Out of scope

| item | why |
|---|---|
| **Any live trade card, order, sizing, or entry timing for today or any specific session** | Brief: no live trade cards; proposals only; not for today's execution. Negative grep enforced in M6 and DoD. |
| **Re-deciding the Oct 16 165/175 spread** from the closed plan `20260914-uso-call-sale` | Context only. It appears once, as an illustration row (S2). Any decision on it is Dominic's, outside this plan. |
| **Editing the USO thesis file, `risk.md`, any routine or skill** | Proposals only. The optional paper journal (S4) is a proposal with an approval line, not a routine change. |
| **MHM** — any task, engine run, or artifact | Roster for this plan is Research Analyst, Price Action Analyst, UW. RA runs its own script. |
| **Session-desk SPY factor gate** (`05_factor_gate.md`, F1–F10) | Single-name options research, not a session card. |
| **Pasting UW output to Dominic** — screenshots, exports, verbatim blocks | UW writes to cache + index only; RA writes its own read. |
| **Parameter optimization** — grid search, walk-forward re-fitting, or picking headline numbers from a sweep | Rules are fixed in `ra_catalog.md` before `ra_backtests.md` runs; `SENS` is a ±1-step check reported separately, never a selection. |
| **Backtesting the absolute levels 140–175 as such** | In the split-adjusted series those prices have little or no history (A5). The backtest is of the **rule class** (zones generated walk-forward by PA's rule), stated in `ra_methods.md`. |
| **A bearish USO thesis** or any trade premised on invalidation | The catalog is thesis-aware (field `regime_intent`); the backtest is thesis-agnostic. A bearish structure is a new `plan_id`. |
| **Other instruments** (CL futures, XLE, XOP, BNO, USL) as backtest series or candidates | USO only; OVX only as the IV proxy. |
| **Intraday data purchase or new data feeds** | Daily bars (4H only if PA's rule requires it and the data is on disk; A13, Q3). |
| **EIA / API / OPEC as event filters** | Brief names FOMC and BOJ. Others are a later `plan_id` if the FOMC/BOJ split shows anything. |
| **Renumbering or renaming T1–T6, the plan, or any output file relative to the host Sequence** | Plan formalizes; numbers and owners are fixed by the host Sequence. |

## Constraints

Hard (from brief and host Sequence):

- `plan_id` is `20260914-uso-call-sale-bt`; tasks are `T1`–`T6` in the host Sequence's order and owners. No rename, no renumber, no added step.
- Every step ends in a **named file path** under `/workspace/plans/20260914-uso-call-sale-bt/outputs/` (UW cache files sit at the UW cache location and are named by path in `outputs/uw_cache_index.md`). "RA says done" / "PA sent the spec" is not a stop condition.
- **No live trade cards.** No output contains an order, a size, a contract count, an arm token, or a grade: negative grep over `outputs/*.md` for `GATE:ARM`, `A++`, `qty`, `contracts:`, `ORDER`, `BUY TO`, `SELL TO`. The catalog's current-instance table is labelled `illustration — not a card`. `REPORT.md` contains `no live trade cards` and `no trade today`.
- **Proposals only.** Every RA file carries `proposals only`. No task edits the thesis file, `risk.md`, any routine, or any skill. `REPORT.md` `## Proposals` rows end in `proposal only`.
- **Walk-forward, no look-ahead.** A zone enters the backtest from `formation_date` + 1 session; regime labels use data through the prior close; walls come from the UW cache as of the prior session; the current S1–S4 are used only in the illustration table, never as historical test levels.
- **No parameter search.** Every parameter used in `ra_backtests.md` is written in `ra_catalog.md` or `ra_methods.md` **before** the run (T3, T4 precede T5). `SENS` is limited to ≤ 2 parameters per strategy at ±1 step and reported in its own section; the headline row is the pre-registered parameter set.
- **Regime tokens are exactly `AI-up` and `OE reject`** (PA's labels, not expanded by the Planner) plus the residual `NEUTRAL`. RA's mechanical rule is a proxy for PA's labels and is validated against PA's sample where one exists (S1).
- **FOMC / BOJ as filters.** `## Event filter` in `REPORT.md` is a table plus at most one line of reading and is ≤ 8 lines. No paragraph on event risk anywhere in `REPORT.md`.
- **PA never writes fundamentals.** `pa_level_spec_v1.md` is levels, structure, dates, regime labels in price terms. Negative grep in M1.
- **UW cache; never paste.** UW writes only to its cache location and to `outputs/uw_cache_index.md`. Missing history → `WALL:NA`; the C4 backtest reads `NA` and the plan does not stall.
- **Versioning.** Level specs are never edited in place: a change is `pa_level_spec_v2.md` with a changelog line; `ra_backtests.md` and `REPORT.md` cite the version used.
- Owners only from {Research Analyst, Price Action Analyst, UW}. Planner owns the critique line in the DoD. Dominic decides.
- 5–8 tasks (this plan: 6; T2 optional). Deadlines assume start 2026-09-15; nothing is due 2026-09-14; `REPORT.md` target 2026-09-24 11:30 UTC (07:30 ET Thu).
- Non-trivial test for every `.md` artifact: ≥ 25 non-blank lines; no `TODO` / `TBD` / `FIXME`; every quoted number has a source in the same section (data pull timestamp, CSV path, spec version, or cache path); a `## Sources` section.
- Critique `02_plan.critique.md` must show 8/8 PASS before the card is considered formalized.

Soft:

- Effort units: S < 1h, M 1–3h, L 3–8h (T5 only).
- Default backtest rules (Q5–Q8; RA may replace any with a stated rule in `ra_methods.md`): one open position per strategy at a time; entry at next session's close after the trigger; CCS width $5 in adjusted-price terms with the short strike at zone high + buffer (buffer default 0.5 × expected move to expiry, EM from OVX); DTE band 30–45, exit at 50 % of credit, time stop 21 DTE, level stop on a daily close above the short strike; R for C1 / C3 / C4 = P&L ÷ (width − credit); R for C2 = overlay P&L ÷ credit; cost $0.05 per share per spread round trip; `LOW-N` if `n` < 20, `NO-READ` if `n` < 10; windows full (from data start) and 5y.
- Default regime proxy (Q6): `OE reject` = trigger bar closes ≥ 2.0 × ATR14 above the 20EMA **and** is a rejection bar at the zone (high ≥ zone low, close < zone low, upper wick ≥ 50 % of range); `AI-up` = ≥ 3 consecutive higher closes **and** 10-session return ≥ +8 % **or** a daily close above the zone high within the prior 5 sessions; else `NEUTRAL`.
- Default event windows (Q7): `EVT:IN` if the entry session is within [T−2, T+1] sessions of an FOMC statement day or a BOJ decision day; `EVT:SPAN` if any such day falls inside the hold; else `EVT:OUT`.
- Default zone proxy if PA's rule is discretionary (Q2): 10-bar pivot high; zone = [max(pivot close, pivot high − 0.5 × ATR14), pivot high]; valid until a daily close > zone high; tests counted on highs ≥ zone low.
- If T1 misses its deadline, T3 writes the catalog against the closed plan's `pa_zones.md` zone ids relabelled `S1`–`S4` in price order and marks `spec: pending v1`; T4 / T5 use the zone proxy with `ZONE:PROXY`; T6 lists the miss under `## Verification`.
- Cutoffs in UTC with ET in parentheses (EDT = UTC−4).

## Assumptions

| id | assumption | status | where handled |
|---|---|---|---|
| A1 | The host Sequence's T1–T6 order is: T1 PA versioned level spec → T2 UW optional cache → T3 RA catalog → T4 RA methods → T5 RA backtests → T6 RA REPORT, matching the brief's owner listing. Planner cannot read the host Sequence text from this scratchpad. If the desk's numbering differs, the host Sequence governs and this file is revised as version 2 with the same `plan_id`. | assumed from brief | Header note; Q1 resolved by RA in T3 header (`host_sequence: T1–T6 order confirmed` or a mapping line). |
| A2 | `/workspace/plans/20260914-uso-call-sale-bt/outputs/` exists or is created by the first writer (PA or RA); `outputs/backtests/` by RA. | assumed | T1 / T3 create if absent; T6 `## Verification` lists the directory with byte sizes. |
| A3 | USO daily OHLC from inception (2006-04-10) is on disk or obtainable via the desk's usual daily source (yfinance, as prior plans used), **split-adjusted** for the 1:8 reverse split of 2020-04-29; the adjusted basis is the one in which S1–S4 and 160 are quoted. | standard data fact / assumed source | T4 `## Data` records source, adjustment, and pull timestamp; Q9. |
| A4 | OVX (CBOE Crude Oil ETF Volatility Index, USO-options-based) history from 2007-05-10 is obtainable and is the IV proxy for modeled premium; no historical USO options chain is on disk. | assumed | T4 `## Premium model` (`PREMIUM:MODELED`); T5 flags every R that depends on it. |
| A5 | The current absolute levels (S1–S4 ≈ 140–175; wall 160) have little or no history in the adjusted series above ~2015, so a backtest of those prices as such has `n` ≈ 0. The testable object is the **rule class**: zones generated walk-forward by PA's rule, walls from UW history. | Planner hypothesis; standard for level-based tests | `## Out of scope` row; T4 `## Zone generation`; T6 `## Caveats`. |
| A6 | `wall 160` is the UW GEX call wall read in the closed plan's cache. It is static for the illustration table; historical walls exist only if UW supplies them (T2). | brief-confirmed / assumed | T1 `## Wall`; T2; C4 `WALL:NA` branch. |
| A7 | UW may hold no historical call-wall series. Then C4 is not backtestable, reads `NA`, and gets a forward paper-journal proposal instead (S4). | unknown | T2 `WALL:NA` literal; T5 `trades_C4.csv` absent with reason; T6 `C4: NA`; Q4. |
| A8 | `AI-up` and `OE reject` are the Price Action Analyst's regime labels. The Planner does not expand the acronyms; PA defines them in price / structure terms (T1) and RA writes a mechanical proxy (T4). The hypothesis under test is that the labels partition call-sale outcomes: sales lose in `AI-up`, hold in `OE reject`. | brief tokens; behaviour is a hypothesis | T1 `## Regime labels`; T4 `## Regime rule`; T5 cross-tables; S1 validation. |
| A9 | Historical FOMC statement dates and BOJ decision dates are public and complete back to 2006; the desk calendar may not reach that far, so web sourcing is permitted **for calendars only**. | calendar fact | T5 `backtests/events.csv` with source URL per row-block; T4 `## Event rule`. |
| A10 | The closed plan's `REPORT.md` carried the Oct 16 165/175 call credit spread as its candidate context. It is used here once, as `C1`'s illustration row. | brief-confirmed ("Oct16 165/175 context only") | S2; `## Out of scope`. |
| A11 | The USO bullish thesis is open (invalidation daily close < 134.34–136.57). The catalog records thesis state in `regime_intent`; the backtest does not depend on the thesis being open, so an invalidation during the plan does not close it — PA issues `pa_level_spec_v2.md` and the illustration table is refreshed. | brief / prior plan | T3 `regime_intent`; Constraints "Versioning". |
| A12 | RA can run Python (pandas) on the desk and pull daily data, as prior desk scripts did (`run_deep.py`, yfinance). | prior-plan precedent | T5 `backtests/run_bt.py`; `## Reproduction`. |
| A13 | No intraday USO data is on disk by default. `timed` in `C3` is read as **time-boxed** (entry at T+1 session after the rejection bar; time stop in sessions), not intraday timing. If PA's rejection rule is 4H and 4H data exists on disk, RA uses it and states so. | Planner reading | T3 `## Definitions`; Q1 (host Sequence wording), Q3. |
| A14 | The post to Dominic is a terse message carrying the `REPORT.md` path and the verdict line, not a paste of the file. | Dominic preference | T6 stop condition. |
| A15 | No MHM involvement is justified: every Must is met from public daily data, PA's spec, the UW cache, and RA's own script. | roster default | `## Out of scope`; T6 `## Compliance`. |

## Context and inputs

Desk facts (from brief and the closed plan; do not re-derive):

- Closed plan `20260914-uso-call-sale`: single-instance insight; Oct 16 165/175 call credit spread as **context only**; PA supply zones and UW GEX cache exist under `/workspace/plans/20260914-uso-call-sale/outputs/`.
- USO bullish thesis **OPEN**; invalidation = daily close under **134.34–136.57**. Dec 150 long call exited Sep 10; desk flat on that call.
- Levels in play: PA supply `S1`–`S4` (four zones above spot, to be issued as a versioned spec) and the UW GEX call wall at **160**.
- Events in the plan window: FOMC Wed 2026-09-16; BOJ 2026-09-17/18. In this plan they are **historical filter columns**, not entry gates.
- Dominic's four numbers: **hit rate, avg R, max DD, n.** Regime filters: `AI-up` vs `OE reject`.

Planner frame — hypotheses for RA and PA to confirm or overturn (not conclusions; each lands in a task):

| # | frame | lands in |
|---|---|---|
| F-a | **Four strategies are two structures × two triggers.** `C1` (CCS) and `C2` (covered) differ in payoff and requirement; `C3` (timed reject) and `C4` (wall-fade) differ in trigger. Writing each as `structure` + `trigger` + `exits` makes the catalog orthogonal and the backtest reusable: `C3` and `C4` default to the `C1` structure. | T3 |
| F-b | **The backtest is of the rule class, not the price.** Absolute 140–175 has no adjusted-basis history (A5). PA's mechanical zone rule, applied walk-forward, generates historical `Sn`-equivalents; the results describe "reject at a PA-class supply zone", which is what the catalog encodes. | T1, T4 |
| F-c | **Premium must be modeled** (A4): Black-Scholes with IV = OVX, no skew, continuous strikes. Hit rate is therefore **path-based** (short strike not breached at a daily close during the hold) and does not depend on the model; avg R and max DD do, and carry `PREMIUM:MODELED`. Dominic reads hit rate as the robust number and R as indicative. | T4, T5 |
| F-d | **Regime is the filter that matters.** Hypothesis: in `AI-up` the supply class fails often enough that no call-sale strategy has positive avg R; in `OE reject` `C1` / `C3` do. If the split does not appear, the regime labels are not a filter for this idea and the REPORT says so in one line. | T5, T6 |
| F-e | **Event filter is a column, not a story.** Expect `EVT:IN` / `EVT:SPAN` to show wider R dispersion and lower hit rate than `EVT:OUT`; whatever the numbers, the REPORT prints the table and one line. | T5, T6 |
| F-f | **`C4` is probably `NA`** unless UW has wall history; a static 160 cannot be backtested. The honest output is a forward journal spec, not a proxy that pretends. | T2, T5, S4 |
| F-g | **`C2` is an overlay** on a hypothetical share position (Dominic holds no shares per the closed plan); its R is overlay P&L ÷ credit and its verdict is about the overlay, not about owning USO. | T3, T4 |
| F-h | **Small n is the likely result** for a strict rejection rule on one instrument. `LOW-N` / `NO-READ` flags keep the REPORT from over-reading; the sensitivity section is limited so it cannot manufacture n. | T5 |

Artifact root: `/workspace/plans/20260914-uso-call-sale-bt/outputs/`

| file | owner | role | Must |
|---|---|---|---|
| `pa_level_spec_v1.md` (+ `screenshots/*.png` optional) | Price Action Analyst | mechanical zone rule; S1–S4 with formation dates; wall confluence; regime labels; historical labels (S1) | M1 |
| `uw_cache_index.md` (+ cache files at UW cache location) | UW | wall history paths + timestamps + fields, or `WALL:NA` | M2 |
| `ra_catalog.md` | Research Analyst | C1–C4 rules tied to S1–S4 / wall 160; current instance illustration | M3 |
| `ra_methods.md` | Research Analyst | data, walk-forward, premium model, metrics, regime + event rules, sample-size and no-search rules | M4 |
| `ra_backtests.md` + `backtests/` (`run_bt.py`, `events.csv`, `trades_C*.csv`, `summary.csv`, `*.png`) | Research Analyst | results per strategy × regime × event × window; flags; sensitivity; reproduction | M5 |
| `REPORT.md` | Research Analyst | decision-complete synthesis; proposals; post | M6 |

Timeline (UTC; ET in parentheses); plan time 2026-09-14 19:32 UTC (15:32 ET). Nothing is due today.

| when | what |
|---|---|
| 2026-09-17 22:00 (Thu 18:00 ET) | Wave 1: T1 PA `pa_level_spec_v1.md` |
| 2026-09-18 22:00 (Fri 18:00 ET) | Wave 2: T2 UW cache + index (optional); T3 RA `ra_catalog.md` |
| 2026-09-21 22:00 (Mon 18:00 ET) | Wave 3: T4 RA `ra_methods.md` |
| 2026-09-23 22:00 (Wed 18:00 ET) | Wave 4: T5 RA `ra_backtests.md` + `backtests/` |
| 2026-09-24 11:30 (Thu 07:30 ET) | Wave 5: T6 RA `REPORT.md` + post |

## Work breakdown

Six tasks, numbered and ordered as the host Sequence. Owners: Price Action Analyst (T1), UW (T2, optional), Research Analyst (T3, T4, T5, T6). No MHM.

| task_id | task | owner | inputs | output | depends_on | effort |
|---|---|---|---|---|---|---|
| T1 | **PA versioned historical level spec.** Write `pa_level_spec_v1.md`: header (`version: 1`, `as_of`, `spot` + timestamp, `ATR14`); `## Rule` — the mechanical zone-identification rule PA uses (timeframe; swing-high definition; zone low / high construction; validity and breach rule; test counting) or `rule: discretionary` plus the proxy PA accepts (Q2); `## Current levels` — exactly `S1`–`S4` with `formation_date` (the session on which the zone first became identifiable under the rule), tests, status, distance in $ and ATR14; `## Wall` — `wall 160` as an external UW level with `confluence: Sn` / `none` (within 1 ATR14); `## Regime labels` — `AI-up` and `OE reject` in price / structure terms (what PA sees on the chart); `## Historical labels` (S1) — ≥ 10 dated past instances of each label; `## Changelog`. Levels only — no fundamentals. Screenshots optional under `outputs/screenshots/`. | Price Action Analyst | USO daily / 4H chart; PA zone method; closed plan's `pa_zones.md` | `/workspace/plans/20260914-uso-call-sale-bt/outputs/pa_level_spec_v1.md` | — | M |
| T2 | **UW optional cache — wall history.** If UW holds historical GEX data for USO: write call wall, put wall, and zero-gamma **by date** as far back as available, plus the current GEX profile, to the UW cache location; write `uw_cache_index.md` with one row per file — path, timestamp, field names, date range. **No values, no exports, no images. Nothing else under `outputs/`.** If no history: `uw_cache_index.md` with the line `WALL:NA — no historical call-wall data` (+ the current-profile row if refreshed). | UW | UW data; UW cache location | UW cache files at their existing location + `/workspace/plans/20260914-uso-call-sale-bt/outputs/uw_cache_index.md` | — | S |
| T3 | **RA strategy catalog.** `ra_catalog.md`: header line `host_sequence:` (Q1); one section per `C1`–`C4` with the thirteen fields of M3, every `trigger` and `exit_level` written against `S1`–`S4` / `wall 160`; `## Definitions` (`timed` = time-boxed per A13; rejection bar; buffer in EM; R unit per strategy; `NEUTRAL` residual); `## Current instance` — one row per strategy mapping the rule onto `pa_level_spec_v1.md` levels and wall 160, `C1` row = Oct 16 165/175 from the closed plan (S2), header `illustration — not a card`; `## Not in catalog` (≤ 4 lines: naked call, diagonal, collar — variants, not strategies here); `proposals only`; `## Sources`. Parameters written here are the pre-registered set for T5. | Research Analyst | T1 spec (or fallback per Soft); closed plan `REPORT.md`; host Sequence text | `/workspace/plans/20260914-uso-call-sale-bt/outputs/ra_catalog.md` | T1 | M |
| T4 | **RA backtest methods.** `ra_methods.md` with the eleven sections of M4: data (USO daily adjusted; split 2020-04-29 1:8; OVX; source + pull timestamp; range); walk-forward rule; zone generation (PA rule or `ZONE:PROXY`); premium model (`PREMIUM:MODELED`: BS, IV = OVX, continuous strikes, r default 0, cost); metrics (R per strategy per F-g, `max_DD_R` on cumulative R by entry date, one open position per strategy); regime rule (mechanical `AI-up` / `OE reject` / `NEUTRAL` with thresholds, mapped to PA's T1 definitions); event rule (calendar sources, `EVT:OUT` / `EVT:IN` / `EVT:SPAN` windows); sample-size rule (`LOW-N` < 20, `NO-READ` < 10); no-search rule (`SENS` ≤ 2 params × ±1 step); windows (full, 5y); `## Sources`. `proposals only`. | Research Analyst | T1 spec; T3 catalog; data availability | `/workspace/plans/20260914-uso-call-sale-bt/outputs/ra_methods.md` | T1, T3 | M |
| T5 | **RA backtests.** Run `backtests/run_bt.py` per `ra_methods.md`: pull data, build `events.csv` (FOMC + BOJ with source), generate zones walk-forward, label regimes and events, simulate `C1`–`C3` (and `C4` if T2 supplied wall history; else `WALL:NA`), write `trades_C*.csv` (one row per trade: entry date, trigger level, regime, event bucket, short / long strike, credit, exit date, exit reason, R) and `summary.csv`. Write `ra_backtests.md`: `## Summary` (strategy × regime × event × window; `n`, `hit_rate`, `avg_R`, `max_DD_R`, `flags`), `## Per-strategy` (headlines, equity-curve PNG path, worst trade, cross-table, S3 extras), `## Sensitivity` (`SENS`), `## Regime proxy validation` (agreement with PA's S1 labels or `na`), `## Reproduction`, `## Sources`. `proposals only`. | Research Analyst | T2 index (optional); T3 catalog; T4 methods; data | `/workspace/plans/20260914-uso-call-sale-bt/outputs/ra_backtests.md` + `/workspace/plans/20260914-uso-call-sale-bt/outputs/backtests/` (`run_bt.py`, `events.csv`, `trades_C1.csv`…`trades_C4.csv`, `summary.csv`, `*.png`) | T2, T3, T4 | L |
| T6 | **RA `REPORT.md` + post.** Sections per M6. `## Verdict`: `C1:`–`C4:` each with exactly one of `EDGE` / `NO-EDGE` / `LOW-N` / `NA` (rule: `EDGE` requires full-sample **and** 5y `avg_R` > 0 with `n` ≥ 20 in the stated regime bucket; `LOW-N` if the qualifying bucket has 10 ≤ `n` < 20; `NA` if not backtestable) plus one line per `EDGE` naming the regime and event bucket. `## Event filter` ≤ 8 lines. `## UW read` ≤ 6 lines or `WALL:NA`. `## Caveats` once. `## Proposals`: numbered, each ending `proposal only`; forward journal spec for `LOW-N` / `NA` strategies (S4). `## Compliance`: no live trade cards; no trade today; no thesis / `risk.md` / routine / skill edits; no UW paste; PA wrote no fundamentals (negative grep result); no MHM; no factor gate; no parameter search. `## Verification`: directory listing with byte sizes, per-md non-trivial result, CSV row counts vs `n`. Post to Dominic: terse, `REPORT.md` path + verdict line; post reference on the last line. | Research Analyst | all files under `outputs/`; T5 | `/workspace/plans/20260914-uso-call-sale-bt/outputs/REPORT.md` | T5 | M |

## Sequence

Planner → desk execution card, matching the host Sequence already issued (T1 → T2 → T3 → T4 → T5 → T6). T2 is optional and runs alongside T3. Deadlines UTC (ET in parentheses). Nothing is due 2026-09-14.

**Wave 1 — PA spec (Thu 2026-09-17)**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 1 (T1) | Price Action Analyst | `/workspace/plans/20260914-uso-call-sale-bt/outputs/pa_level_spec_v1.md` | file exists; header has `version: 1`, `as_of:`, `spot:`, `ATR14:`; `## Rule` present with either a mechanical rule (contains `timeframe`, `swing`, `breach`) or `rule: discretionary` + `proxy:`; `## Current levels` has exactly four rows `S1`…`S4` each with `low` < `high` > `spot` and a `formation_date` ≤ `as_of`; `## Wall` contains `wall 160` and `confluence:`; `## Regime labels` contains `AI-up` and `OE reject`; `## Changelog` present; negative grep for `Hormuz`, `pipeline`, `FOMC`, `BOJ`, `OPEC`, `inventor`, `WTI`, `geo` returns nothing; passes the non-trivial test | 2026-09-17 22:00 (18:00 ET Thu) |

**Wave 2 — optional cache + catalog (Fri 2026-09-18)**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 2 (T2, optional) | UW | UW cache files at their location + `/workspace/plans/20260914-uso-call-sale-bt/outputs/uw_cache_index.md` | index exists; **either** rows for call wall / put wall / zero-gamma by date with path, timestamp, field names, date range, every path existing, no numeric strike / gamma values, no `![`, no code fence; **or** the literal `WALL:NA — no historical call-wall data`; no other UW-authored file under `outputs/` | 2026-09-18 22:00 (18:00 ET Fri) |
| 3 (T3) | Research Analyst | `/workspace/plans/20260914-uso-call-sale-bt/outputs/ra_catalog.md` | header contains `host_sequence:`; headings `## C1 Defined CCS at supply`, `## C2 Covered call at supply`, `## C3 Timed reject-at-supply`, `## C4 Wall-fade`, `## Definitions`, `## Current instance`, `## Not in catalog`, `## Sources`; each `C` section has all thirteen field names of M3; each `trigger` and `exit_level` cell contains one of `S1`, `S2`, `S3`, `S4`, `wall 160`; `## Current instance` contains `illustration — not a card` and, in the `C1` row, `165`, `175`, `Oct 16` (S2); `## Definitions` contains `timed`, `rejection bar`, `buffer`, `NEUTRAL`; `proposals only`; negative grep for card tokens returns nothing; passes the non-trivial test | 2026-09-18 22:00 (18:00 ET Fri) |

**Wave 3 — methods (Mon 2026-09-21)**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 4 (T4) | Research Analyst | `/workspace/plans/20260914-uso-call-sale-bt/outputs/ra_methods.md` | all eleven M4 headings present; `## Data` contains `2020-04-29`, `1:8`, `OVX`, a source, and a pull timestamp; `## Zone generation` cites `pa_level_spec_v1.md` `## Rule` or contains `ZONE:PROXY`; `## Premium model` contains `PREMIUM:MODELED`; `## Regime rule` contains `AI-up`, `OE reject`, `NEUTRAL` each with a numeric threshold; `## Event rule` contains `FOMC`, `BOJ`, `EVT:OUT`, `EVT:IN`, `EVT:SPAN`; `## Sample-size rule` contains `LOW-N` and `NO-READ` with thresholds; `## No-search rule` contains `SENS`; `## Windows` contains `5y`; `proposals only`; passes the non-trivial test | 2026-09-21 22:00 (18:00 ET Mon) |

**Wave 4 — backtests (Wed 2026-09-23)**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 5 (T5) | Research Analyst | `/workspace/plans/20260914-uso-call-sale-bt/outputs/ra_backtests.md` + `outputs/backtests/` | `backtests/run_bt.py`, `backtests/events.csv`, `backtests/summary.csv` exist; `trades_C1.csv`, `trades_C2.csv`, `trades_C3.csv` exist; `trades_C4.csv` exists **or** `ra_backtests.md` contains `C4` + `WALL:NA`; `events.csv` has columns `date`, `event` ∈ {`FOMC`, `BOJ`}, `source`; `## Summary` rows carry `n`, `hit_rate`, `avg_R`, `max_DD_R`, `flags`, with `LOW-N` on every row `n` < 20 and `NO-READ` on every row `n` < 10; each `## Per-strategy` subsection names a PNG path that exists; `## Sensitivity` contains `SENS`; `## Regime proxy validation` present; `## Reproduction` contains a command line and a pull timestamp; every `trades_C*.csv` row count equals the corresponding full-window all-regime `n`; `proposals only`; passes the non-trivial test | 2026-09-23 22:00 (18:00 ET Wed) |

**Wave 5 — REPORT (Thu 2026-09-24)**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 6 (T6) | Research Analyst | `/workspace/plans/20260914-uso-call-sale-bt/outputs/REPORT.md` | all twelve M6 headings present; `## Verdict` contains `C1:`, `C2:`, `C3:`, `C4:` each followed by exactly one of `EDGE` / `NO-EDGE` / `LOW-N` / `NA`, and one bucket line per `EDGE`; `## Event filter` ≤ 8 lines with a table; `## UW read` ≤ 6 lines with a cache path + timestamp or `WALL:NA`, no `![`, no code fence; `## Level spec` contains `pa_level_spec_v1.md` (or the version used); `## Proposals` rows each end `proposal only`; contains `no live trade cards` and `no trade today`; `## Compliance` contains `thesis`, `risk.md`, `paste`, `fundamentals`, `MHM`, `factor gate`, `parameter search`; `## Verification` lists every file under `outputs/` with byte size; negative grep for `GATE:ARM`, `A++`, `qty`, `contracts:`, `ORDER`, `BUY TO`, `SELL TO` returns nothing across `outputs/*.md`; last line is the post reference to Dominic; passes the non-trivial test | 2026-09-24 11:30 (07:30 ET Thu) |

**Plan-level stop:** the plan closes when step 6's stop condition is met. A T1 miss does not block T3 / T4 / T5: the catalog falls back to the closed plan's zones relabelled `S1`–`S4` with `spec: pending v1`, the backtest uses `ZONE:PROXY`, and `REPORT.md` `## Verification` names the miss. A T2 miss or `WALL:NA` makes `C4: NA` and triggers the S4 journal proposal; it does not stall. A thesis invalidation during the plan does not close it (A11). Any live entry, sizing, routine change, bearish structure, or other-instrument test is a new `plan_id` or Dominic's own call.

Owner-side rules for the card: PA writes levels, dates, and regime labels only (negative grep enforced); UW writes to cache + index only, never to Dominic; RA reads the cache and writes its own read; all parameters pre-registered in `ra_catalog.md` / `ra_methods.md` before `run_bt.py` runs; `SENS` never selects the headline; no file outside `outputs/` is created or edited except the UW cache at its own location; `proposals only` in every RA file; `no live trade cards`; no MHM; no SPY factor gate.

## Definition of done

Checkable by listing files and grepping content under `/workspace/plans/20260914-uso-call-sale-bt/outputs/`.

Non-trivial test (every `.md`): ≥ 25 non-blank lines; no `TODO` / `TBD` / `FIXME`; every quoted number has a source in the same section; a `## Sources` section.

- [ ] `pa_level_spec_v1.md` passes the non-trivial test; header contains `version: 1`, `as_of:`, `spot:`, `ATR14:`; `## Current levels` has exactly four rows `S1`–`S4` with `formation_date`; `## Wall` contains `wall 160` and `confluence:`; `## Regime labels` contains `AI-up` and `OE reject`; `## Changelog` present; `grep -iE 'Hormuz|pipeline|FOMC|BOJ|OPEC|inventor|WTI|geo'` returns nothing.
- [ ] `uw_cache_index.md` exists; either lists cache paths (each existing) with timestamps, field names, and date ranges and contains no `![`, no code fence, and no strike-level numeric values — or contains `WALL:NA — no historical call-wall data`; no other file under `outputs/` is authored by UW.
- [ ] `ra_catalog.md` passes the non-trivial test; contains `host_sequence:`, the four `## C` headings, `## Definitions`, `## Current instance`, `## Not in catalog`; every `C` section has the thirteen M3 fields; every `trigger` and `exit_level` contains one of `S1`–`S4` / `wall 160`; contains `illustration — not a card`, `165`, `175`, `Oct 16`, `timed`, `rejection bar`, `NEUTRAL`, `proposals only`.
- [ ] `ra_methods.md` passes the non-trivial test; contains the eleven M4 headings; contains `2020-04-29`, `1:8`, `OVX`, `PREMIUM:MODELED`, `AI-up`, `OE reject`, `NEUTRAL`, `FOMC`, `BOJ`, `EVT:OUT`, `EVT:IN`, `EVT:SPAN`, `LOW-N`, `NO-READ`, `SENS`, `5y`, `proposals only`; contains `pa_level_spec_v1.md` or `ZONE:PROXY`.
- [ ] `backtests/run_bt.py`, `backtests/events.csv`, `backtests/summary.csv`, `backtests/trades_C1.csv`, `trades_C2.csv`, `trades_C3.csv` exist with size > 0; `trades_C4.csv` exists or `ra_backtests.md` contains `WALL:NA`; `events.csv` has a `source` column; at least one `.png` under `backtests/`.
- [ ] `ra_backtests.md` passes the non-trivial test; `## Summary` rows carry `n`, `hit_rate`, `avg_R`, `max_DD_R`, `flags`; every row with `n` < 20 contains `LOW-N`; every row with `n` < 10 contains `NO-READ`; `## Per-strategy`, `## Sensitivity` (`SENS`), `## Regime proxy validation`, `## Reproduction` present; each `trades_C*.csv` row count equals the strategy's full-window all-regime `n`.
- [ ] `REPORT.md` passes the non-trivial test; contains the twelve M6 headings; `## Verdict` has `C1:`, `C2:`, `C3:`, `C4:` each with exactly one of `EDGE` / `NO-EDGE` / `LOW-N` / `NA`; `## Event filter` ≤ 8 lines; `## UW read` ≤ 6 lines, no `![`, no code fence; contains `no live trade cards`, `no trade today`, `pa_level_spec_v`; every `## Proposals` row ends `proposal only`; `## Compliance` contains `thesis`, `risk.md`, `paste`, `fundamentals`, `MHM`, `factor gate`, `parameter search`; `## Verification` lists every file under `outputs/` with a byte size; last line is the post reference to Dominic.
- [ ] `grep -E 'GATE:ARM|A\+\+|qty|contracts:|ORDER|BUY TO|SELL TO' outputs/*.md` returns nothing; every RA `.md` contains `proposals only`.
- [ ] No file outside `outputs/` (thesis file, `risk.md`, any routine or skill, the closed plan's directory) has a modification attributable to this plan; the UW cache at its own location is the only permitted write outside `outputs/`.
- [ ] No artifact references MHM as an owner, the SPY factor gate, or any instrument other than USO (OVX as IV proxy excepted) as a series or candidate; no artifact renumbers T1–T6 or renames the plan.
- [ ] `02_plan.critique.md` in this scratchpad shows PASS on all eight checklist items (Planner).

## Open questions

None blocks Wave 1. Each has one roster owner, a place it is resolved, and a default.

| id | question | owner | resolve in | default if unresolved |
|---|---|---|---|---|
| Q1 | Does the host Sequence's T1–T6 numbering match A1, and does its wording of `timed` (C3) mean time-boxed (A13)? | Research Analyst (holds the host Sequence text) | T3 header `host_sequence:` line | Order as A1; `timed` = time-boxed (entry T+1 session; time stop 10 sessions); if the host differs, RA writes the mapping in the header and Planner issues version 2 of this file, same `plan_id`. |
| Q2 | Is PA's zone rule mechanical enough to generate historical zones walk-forward? | Price Action Analyst | T1 `## Rule` | `rule: discretionary` + the Soft-constraint pivot proxy; RA tags `ZONE:PROXY` in T4 / T5 and the REPORT `## Caveats`. |
| Q3 | Is the rejection bar for C3 defined on daily or 4H bars, and is 4H USO data on disk? | Price Action Analyst (bar), Research Analyst (data) | T1 `## Regime labels` / `## Rule`; T4 `## Data` | Daily; 4H only if PA's rule requires it and the series exists on disk, stated in `## Data`. |
| Q4 | Does UW hold historical call-wall data for USO, and how far back? | UW | T2 `uw_cache_index.md` | `WALL:NA`; C4 reads `NA`; S4 journal proposal. |
| Q5 | Are the default R definitions, cost, overlap rule, and DTE / exit defaults (Soft) acceptable? | Research Analyst | T4 `## Metrics`, `## Premium model` | Defaults stand; any replacement rule is stated where applied and pre-registered before T5. |
| Q6 | Are the default regime-proxy thresholds a fair mechanization of PA's `AI-up` / `OE reject`? | Research Analyst (writes), validated against PA's S1 sample | T4 `## Regime rule`; T5 `## Regime proxy validation` | Defaults stand; agreement with PA's sample reported as a percentage; < 70 % agreement is stated in `## Caveats`, not tuned away. |
| Q7 | Event window [T−2, T+1] sessions for `EVT:IN`; FOMC statement day and BOJ decision day (second day of a two-day meeting) as the anchor dates? | Research Analyst | T4 `## Event rule`; T5 `events.csv` | As stated; calendar sources named per block in `events.csv`. |
| Q8 | C2 R unit: overlay P&L ÷ credit (F-g) or overlay P&L ÷ share risk? | Research Analyst | T4 `## Metrics` | Overlay P&L ÷ credit; the verdict is about the overlay. |
| Q9 | Data source if USO / OVX daily history is not on disk? | Research Analyst | T4 `## Data` | yfinance daily adjusted (as prior desk plans); source and pull timestamp recorded; split 2020-04-29 1:8 verified against the series. |
| Q10 | Does Dominic want the forward paper journal (S4) for `LOW-N` / `NA` strategies, and at what cadence? | Research Analyst (proposes), Dominic (approves) | T6 `## Proposals` | Proposal written with daily post-close cadence through 2026-10-16; `Dominic: approve / decline` closes the section. |

## Changelog

| version | date | brain | change |
|---|---|---|---|
| 1 | 2026-09-14 | fable-5.1 | In-depth formalization of the host Sequence already issued (T1–T6, same order, same owners, `plan_id` unchanged). Six tasks — Price Action Analyst (T1 versioned historical level spec `pa_level_spec_v1.md`: mechanical rule, S1–S4 with formation dates, wall 160 confluence, `AI-up` / `OE reject` labels), UW (T2 optional wall-history cache + index, `WALL:NA` branch), Research Analyst (T3 catalog C1–C4 tied to S1–S4 / wall 160 with illustration table; T4 methods — walk-forward, `PREMIUM:MODELED` via OVX, metrics, regime + event rules, `LOW-N` / `NO-READ`, no-search; T5 backtests `run_bt.py` + CSVs + `ra_backtests.md`; T6 decision-complete `REPORT.md` with per-strategy `EDGE` / `NO-EDGE` / `LOW-N` / `NA` and numbered proposals). Backtest is of the rule class, not the absolute levels (A5). FOMC / BOJ as filter columns (`EVT:OUT` / `IN` / `SPAN`), section ≤ 8 lines. Not for today's execution: first deadline 2026-09-17, `REPORT.md` 2026-09-24 11:30 UTC. Hard: no live trade cards (negative grep), proposals only, named path stops, no thesis / `risk.md` / routine edits, no MHM, no factor gate, no UW paste, no parameter search. Prior closed plan `20260914-uso-call-sale` is context only (Oct 16 165/175 as the C1 illustration). Status `ready`. |
