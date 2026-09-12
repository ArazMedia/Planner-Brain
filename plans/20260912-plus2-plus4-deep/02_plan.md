# Plan: +2 half-size vs +4-only, disaggregated — SPY-alone and BTC-alone dollar curves, 2016 composition note, turnover, year splits, decision (closeout)

```
plan_id: 20260912-plus2-plus4-deep
title: +2 half-size vs +4-only, disaggregated — SPY-alone and BTC-alone dollar curves, 2016 composition note, turnover, year splits, decision (closeout)
requester: Multi-Horizon Momentum (Dominic via MHM)
created: 2026-09-12
status: ready
brain: fable-5.1
depth: in-depth
version: 2
```

> **Execution state at plan time:** MHM has already produced the core artifacts under the artifact root (charts, note, turnover/year-split tables, `DECISION.md`, `README.md`, `run_deep.py`). This plan is a **closeout sequence**: it maps the confirmed goal onto the files that exist, states which stop conditions are already met, and names the only remaining polish. No re-runs are scheduled. No RA/PA tasks. No `risk.md` edits.

## Goal

Matches the confirmed `01_goals.md` (six items, quoted in the brief). Disaggregate the closed plan `20260912-sheet-vs-research` T5 combined-book result (`/workspace/mhm/research/sheet_vs_research/slice_01_plus2_ev_vs_plus4/`) into **SPY-alone** and **BTC-alone** $9k dollar curves, and answer whether the +2 half-size tier helps enough on each asset alone in the **5y** window to propose a `risk.md` gate change — or only on the combined book / full sample.

1. Separate $9k equity curves: SPY alone and BTC alone; Sheet vs Research; +4-only vs +2/+4; full and 5y as **separate figures** (never only a squeezed full-scale plot).
2. Short 2016 / composition note: BTC yfinance starts 2014-09-17 (n=4377 through 2026-09-10); Sheet first usable ~2014-11; Research first usable ~2015-06 — composition change, not a data bug; vertical BTC-data-start marker on charts; SPY-alone vs BTC-alone panels.
3. Turnover / time-in-market tables by name quantifying more movement after ~2016.
4. Calendar-year splits of the paths.
5. Decision one-pager: does +2 half-size help enough on SPY alone **and** BTC alone in 5y to propose a `risk.md` change — or only on combined book / full sample.
6. Stop at readable charts + decision note; proposals only.

All outputs are **proposals**. Dominic decides anything touching `live_min_abs_score` or `risk.md`.

## Success criteria

Must (each has a task; status is as reported by MHM at plan time and is re-verified by T6 before close):

| id | criterion | checked by | task | status at plan time |
|---|---|---|---|---|
| M1 | Four separate figures exist and are readable: `spy_full_dollars.png`, `spy_5y_dollars.png`, `btc_full_dollars.png`, `btc_5y_dollars.png`; each shows Sheet vs Research and +4-only vs +2/+4 as clearly labelled series or small multiples; the BTC full-window figure carries a vertical BTC-data-start marker | files exist, size > 0; visual check recorded in `REPORT.md` chart index | T1 | MET (verify in T6) |
| M2 | `NOTE_2016_btc.md` explains the ~2016 kink as composition (BTC data start 2014-09-17, n=4377 through 2026-09-10; Sheet first usable ~2014-11; Research first usable ~2015-06), states "not a data bug", points at the SPY-alone vs BTC-alone panels, and passes the non-trivial test (≥ 25 non-blank lines) | file + grep for the five dates/counts + `## Sources` | T2 | PARTIAL — file exists but short; expand |
| M3 | Turnover / time-in-market table **by name** (SPY, BTC) × ruleset × gate × window exists and quantifies more movement after ~2016 | `turnover_tim.csv` columns + a before/after-2016 comparison somewhere on disk | T3 | MET (verify; conditional polish) |
| M4 | Calendar-year splits of the dollar paths exist by name × ruleset × gate, partial years flagged | `year_splits.md` + `year_splits.csv` | T4 | MET (verify) |
| M5 | `DECISION.md` answers, per asset, whether +2 half-size helps in 5y (SPY alone, BTC alone), and separately on combined / full; states the proposal; says "proposals only"; names the Dominic call on `live_min_abs_score`; no `risk.md` edit | file + grep | T5 | MET (verify) |
| M6 | Plan stops at readable charts + decision note. `REPORT.md` is a thin index (chart index, pointers, compliance attestation: no `tv`, no RA/PA, no edits to `risk.md` / `universe.md` / engine / skills, no re-runs beyond the single `run_deep.py` execution) and MHM has posted the terse summary to Dominic | file + post reference | T6 | OPEN |

Should:

| id | criterion | task | status |
|---|---|---|---|
| S1 | Combined-book figures `combined_full_dollars.png`, `combined_5y_dollars.png` kept as optional context, listed in the chart index, never used as the sole evidence for a per-asset claim | T6 | MET (files exist) |
| S2 | `stats_all.csv` referenced from `DECISION.md` and `REPORT.md` as the numeric source for every dollar figure quoted | T5, T6 | verify |

## Out of scope

| item | why |
|---|---|
| Editing `risk.md` (including `live_min_abs_score` or any half-size tier) | Hard constraint. `DECISION.md` is a proposal; Dominic applies. |
| PA dual Strategy Tester | Not needed to meet any Must; UI-manual; remains on the closed plan's next-analyses list. |
| Any RA or PA task | Default MHM-only plan; every Must is met from MHM artifacts already on disk. |
| Universe changes; SMH / GLD / USO expansion | Different question; per-asset disaggregation here is SPY and BTC only. |
| Parameter search (other score tiers such as +3-only, other half-size fractions, lag or cost sweeps) | Would be a new-ruleset project and risks overfitting the gate to the 5y window. |
| Re-running `run_deep.py` or any engine backtest | Artifacts exist. Only file-level polish is scheduled. If a verification step in T6 finds a defect that needs a re-run, that is a new `plan_id`, not a step here. |
| Re-doing the combined-book T5 slice from `20260912-sheet-vs-research` | Cited as prior context; combined figures here are optional cross-checks only. |
| Open research spiral (more windows, more assets, more regimes) | Plan closes when T6's stop condition is met. |

## Constraints

Hard (from brief):

- MHM never runs `tv`; no TradingView work in this plan (no PA task exists to do it).
- Nothing in this plan changes `/workspace/mhm/risk.md`, `/workspace/mhm/universe.md`, the engine, or skills.
- Every step ends in a **named file path** under `/workspace/mhm/research/sheet_vs_research/plus2_plus4_deep/`. "Already done" is not a stop condition; the stop condition is the file existing and passing its check.
- Non-trivial test for every `.md` artifact: ≥ 25 non-blank lines; no `TODO` / `TBD` / `FIXME`; every quoted number has an on-disk path in the same section; a `## Sources` section. PNG artifacts: size > 0 bytes.
- Full and 5y are **separate figures**; a full-scale plot alone never satisfies a 5y criterion.
- Library `/workspace/mhm/research/` is the first source if any paper is cited (none is required for this plan).
- 5–8 tasks; owners from the roster only; RA/PA not used.
- Deadlines assume start 2026-09-12. Charts already exist; decision note already exists (ahead of the ~2026-09-13 18:00 UTC target). Remaining polish is due 2026-09-12.
- Dominic preferences: terse; no paper spam. `REPORT.md` is a thin index, not a second narrative.

Soft:

- Effort units: S < 1h, M 1–3h. Every remaining step is S.
- If a verification step fails (e.g. a PNG lacks the BTC-start marker), MHM records the failure in `REPORT.md` under `## Verification` rather than silently fixing by re-run; a fix that needs the engine is out of scope (see above). A fix that is pure re-plotting from `stats_all.csv` / existing path data is allowed as polish.

## Assumptions

| id | assumption | status | where handled |
|---|---|---|---|
| A1 | MHM's report of what exists under the artifact root is accurate: four per-asset PNGs, two combined PNGs, `NOTE_2016_btc.md`, `turnover_tim.csv`, `year_splits.csv`, `year_splits.md`, `stats_all.csv`, `DECISION.md`, `README.md`, `run_deep.py`. | reported by MHM, not independently listed by Planner | T6 `## Verification` re-lists the directory with byte sizes. |
| A2 | "+2 half-size" means the same tier definition as the closed plan's slice (`slice_01_plus2_ev_vs_plus4/`): +4 at full size, +2 (and +3) long at half size, nothing below +2; cash shorts paper. | assumed identical; `run_deep.py` is the record | T6 chart index states the tier rule as read from `run_deep.py` / `README.md`; if it differs from slice_01, `DECISION.md` must already say so or T5 polish adds one line. |
| A3 | "SPY alone" / "BTC alone" = the whole $9k run on a single-asset sleeve under the same sizing rules, not the per-asset share of the combined book. | assumed from `run_deep.py` design | T6 states which it is; `DECISION.md` wording must match. |
| A4 | 5y window = trailing five years ending 2026-09-10 (~2021-09-10 → 2026-09-10), consistent with the closed plan's 5y runs. | assumed | T6 chart index records window start/end per figure from `stats_all.csv`. |
| A5 | BTC data facts are as stated in the brief: yfinance start 2014-09-17, n=4377 daily bars through 2026-09-10. Sheet first usable ~2014-11 and Research first usable ~2015-06 are approximate and follow from lookbacks (Sheet 5–42d; Research 21–252d) plus warm-up. | brief-confirmed (BTC start, n); approximate (first-usable) | T2 writes exact first-nonzero-score dates per ruleset if `stats_all.csv` / run output exposes them; otherwise keeps `~` and says why. |
| A6 | The ~2016 kink in combined-book curves is composition (BTC entering, with Research entering later than Sheet) and not a data bug. MHM's `DECISION.md` already states this. | supported by MHM | T2 must show it, not just assert it: point at the SPY-alone full figure (no kink, or a different one) versus the BTC-alone full figure (starts at the marker). T3 quantifies the movement change. |
| A7 | `DECISION.md` conclusions as reported: SPY +2 helps in 5y; BTC +2 hurts slightly in 5y; proposal = do **not** loosen the live gate to +2 on BTC from 5y evidence; SPY +2 is the only sleeve where 5y still helps — Dominic's call before any `live_min_abs_score` change. | reported by MHM | T5 verification greps for the per-asset verdicts and the Dominic-call line; Planner does not re-decide. |
| A8 | Dominic's decision surface is exactly: keep `live_min_abs_score: 4` for both; or add a SPY-only +2 half-size tier; or add +2 half-size for both. Anything else (SMH, tiers other than half, other windows) is out of scope. | assumed | `DECISION.md` should present at most these three options; if it presents more, T5 polish trims to three or labels extras "not proposed". |
| A9 | Turnover/time-in-market "more movement after ~2016" can be shown from `turnover_tim.csv` / `year_splits.csv` as they stand (per-year or pre/post-2016 rows). | unconfirmed — depends on the CSV's window granularity | T3 conditional polish: if no before/after-2016 comparison exists on disk, add a ≤ 6-row table to `REPORT.md` computed from the existing CSVs (no engine run). |
| A10 | The post to Dominic is a short message with the `DECISION.md` and `REPORT.md` paths; it is not a paste of the note. | Dominic preference | T6 stop condition. |

## Context and inputs

Desk gates (unchanged, do not re-derive): ruleset in force = sheet; `live_min_abs_score: 4`; +4 long-only interest on SPY and BTC; cash shorts paper; capital $9k.

Prior context (cite, do not redo):

- Closed plan `20260912-sheet-vs-research`, T5 combined-book slice: `/workspace/mhm/research/sheet_vs_research/slice_01_plus2_ev_vs_plus4/` — Full: Sheet +4 $45k → +2/+4 $72k (+$27k); Research $30k → $45k. 5y: Sheet $10.3k → $11.8k; Research $14.2k → $15.0k. Combined-only; insufficient for a per-asset gate decision, which is why this plan exists.

Artifact root: `/workspace/mhm/research/sheet_vs_research/plus2_plus4_deep/`

Files reported present at plan time (A1):

| file | role | Must |
|---|---|---|
| `spy_full_dollars.png`, `spy_5y_dollars.png` | SPY-alone $9k curves, full and 5y, Sheet vs Research × +4-only vs +2/+4 | M1 |
| `btc_full_dollars.png`, `btc_5y_dollars.png` | BTC-alone $9k curves, full and 5y; full carries BTC-data-start marker | M1 |
| `combined_full_dollars.png`, `combined_5y_dollars.png` | optional combined-book cross-check | S1 |
| `NOTE_2016_btc.md` | composition note (short at plan time) | M2 |
| `turnover_tim.csv` | turnover / time-in-market by name × ruleset × gate × window | M3 |
| `year_splits.csv`, `year_splits.md` | calendar-year splits | M4 |
| `stats_all.csv` | numeric source for all dollar / stat figures | S2 |
| `DECISION.md` | one-pager, already written | M5 |
| `README.md` | run provenance (what `run_deep.py` did, windows, tier rule) | input to T6 |
| `run_deep.py` | the single script that produced everything above; already executed once; **not** re-run | input to T6 |

Not present at plan time: `REPORT.md` (thin index, T6).

Library: `/workspace/mhm/research/` — no paper citation is required by any Must; if MHM cites one in the note, library first.

## Work breakdown

Six tasks. T1, T3, T4, T5 are complete pending verification; T2 and T6 are the only open work. Owner for every task is Multi-Horizon Momentum (MHM). No RA/PA.

| task_id | task | owner | inputs | output | depends_on | effort |
|---|---|---|---|---|---|---|
| T1 | **Per-asset dollar charts** (DONE). SPY-alone and BTC-alone $9k curves, full and 5y as four separate figures, each with Sheet vs Research and +4-only vs +2/+4 as labelled series or small multiples; BTC-start vertical marker on the full-window BTC figure (and on combined full). Remaining: none unless T6 verification finds a missing marker or label, in which case re-plot from existing path data only | Multi-Horizon Momentum | `run_deep.py` output already on disk; `stats_all.csv` | `/workspace/mhm/research/sheet_vs_research/plus2_plus4_deep/spy_full_dollars.png`, `spy_5y_dollars.png`, `btc_full_dollars.png`, `btc_5y_dollars.png` (+ optional `combined_full_dollars.png`, `combined_5y_dollars.png`) | — | S (done) |
| T2 | **Expand `NOTE_2016_btc.md`** to pass the non-trivial test: BTC yfinance start 2014-09-17, n=4377 through 2026-09-10; Sheet first usable ~2014-11 and Research first usable ~2015-06 (exact dates if available, A5); why Research enters later (252d lookback); what the combined curve is made of before / between / after those dates; "composition change, not a data bug"; pointer to `spy_full_dollars.png` vs `btc_full_dollars.png` showing the kink is BTC-side; one line on what this means for reading the closed plan's combined full-sample numbers; `## Sources` | Multi-Horizon Momentum | existing `NOTE_2016_btc.md`; `stats_all.csv`; `README.md`; T1 figures; brief data facts | `/workspace/mhm/research/sheet_vs_research/plus2_plus4_deep/NOTE_2016_btc.md` | T1 | S |
| T3 | **Turnover / time-in-market by name** (DONE, verify). Confirm `turnover_tim.csv` has rows keyed by name (SPY, BTC) × ruleset × gate × window with turnover and time-in-market columns. Conditional polish (A9): if no before/after-~2016 comparison exists, add a ≤ 6-row table to `REPORT.md` `## Movement after 2016` computed from `turnover_tim.csv` / `year_splits.csv` — no engine run | Multi-Horizon Momentum | `turnover_tim.csv`; `year_splits.csv` | `/workspace/mhm/research/sheet_vs_research/plus2_plus4_deep/turnover_tim.csv` (+ conditional section in `REPORT.md`) | T1 | S (done / conditional) |
| T4 | **Calendar-year splits** (DONE, verify). Confirm `year_splits.md` and `year_splits.csv` give per-year figures by name × ruleset × gate for the dollar paths; partial years (first BTC year, 2026 YTD, 5y start year) flagged; `year_splits.md` passes the non-trivial test | Multi-Horizon Momentum | `year_splits.csv`, `year_splits.md` | `/workspace/mhm/research/sheet_vs_research/plus2_plus4_deep/year_splits.md` and `year_splits.csv` | T1 | S (done) |
| T5 | **Decision one-pager** (DONE, verify). Confirm `DECISION.md` states per-asset 5y verdicts (SPY +2 helps; BTC +2 hurts slightly), the combined / full-sample contrast, the proposal (do not loosen BTC gate from 5y evidence; SPY +2 half-size is the only sleeve where 5y still helps; Dominic's call before `live_min_abs_score`), "proposals only", the at-most-three options of A8, and cites `stats_all.csv` for every dollar figure; passes the non-trivial test. Polish only if a grep in T6 fails | Multi-Horizon Momentum | `DECISION.md`; `stats_all.csv`; T1–T4 outputs | `/workspace/mhm/research/sheet_vs_research/plus2_plus4_deep/DECISION.md` | T1, T3, T4 | S (done) |
| T6 | **`REPORT.md` thin index + verification + post.** Sections: `## Chart index` (each PNG: asset, window, series shown, marker Y/N, byte size); `## Pointers` (DECISION, NOTE, turnover, year splits, stats, README, run_deep); `## Verification` (directory listing with sizes; non-trivial-test result for each md; grep results for the M2 and M5 strings; A2/A3/A4 facts as read from `README.md` / `run_deep.py`); conditional `## Movement after 2016` (T3); `## Compliance` (no `tv`; no RA/PA; no edits to `risk.md` / `universe.md` / engine / skills; `run_deep.py` executed once, not re-run); `## Sources`. Then post the terse summary (DECISION verdict + two paths) to Dominic and record the post reference at the bottom | Multi-Horizon Momentum | all files under the artifact root; T2 expanded note | `/workspace/mhm/research/sheet_vs_research/plus2_plus4_deep/REPORT.md` | T2, T3, T4, T5 | S |

## Sequence

Planner → MHM closeout card. Owner is MHM for every step. Deadlines are UTC; start 2026-09-12. Steps marked **MET** need no action beyond the T6 verification record; steps marked **OPEN** are the remaining work.

**Wave 0 — already executed (verify only, no re-run)**

| step | owner | artifact path | stop condition | deadline UTC | state |
|---|---|---|---|---|---|
| 0a (T1) | MHM | `/workspace/mhm/research/sheet_vs_research/plus2_plus4_deep/spy_full_dollars.png`, `spy_5y_dollars.png`, `btc_full_dollars.png`, `btc_5y_dollars.png` | four files exist, each size > 0; each shows Sheet vs Research and +4-only vs +2/+4 with legible labels; `btc_full_dollars.png` (and `combined_full_dollars.png` if kept) shows a vertical BTC-data-start marker at 2014-09-17; full and 5y are separate files | 2026-09-12 12:00 | MET (record in T6 `## Verification`) |
| 0b (T3) | MHM | `.../plus2_plus4_deep/turnover_tim.csv` | file exists; header includes name, ruleset, gate, window plus turnover and time-in-market columns; rows for SPY and BTC under both rulesets and both gates; a before/after-~2016 comparison exists on disk (here or via T3 conditional section in `REPORT.md`) | 2026-09-12 12:00 | MET / conditional |
| 0c (T4) | MHM | `.../plus2_plus4_deep/year_splits.md` + `year_splits.csv` | both exist; per-year rows by name × ruleset × gate; partial years flagged; md passes the non-trivial test | 2026-09-12 12:00 | MET (verify) |
| 0d (T5) | MHM | `.../plus2_plus4_deep/DECISION.md` | file exists; contains the strings `SPY`, `BTC`, `5y`, `combined`, `full`, `live_min_abs_score`, `proposal`; a per-asset 5y verdict line for each of SPY and BTC; the line that the BTC gate is **not** to be loosened on 5y evidence; the line that the call is Dominic's; no instruction to edit `risk.md`; passes the non-trivial test; cites `stats_all.csv` | 2026-09-12 12:00 | MET (verify) |

**Wave 1 — open polish**

| step | owner | artifact path | stop condition | deadline UTC | state |
|---|---|---|---|---|---|
| 1 (T2) | MHM | `.../plus2_plus4_deep/NOTE_2016_btc.md` | ≥ 25 non-blank lines; contains `2014-09-17`, `4377`, `2026-09-10`, `2014-11`, `2015-06`, `composition`, `not a data bug`; names `spy_full_dollars.png` and `btc_full_dollars.png`; has `## Sources`; no `TODO`/`TBD`/`FIXME` | 2026-09-12 14:00 | OPEN |
| 2 (T6) | MHM | `.../plus2_plus4_deep/REPORT.md` | file exists with `## Chart index` (all six PNGs, sizes, marker Y/N), `## Pointers`, `## Verification` (directory listing; per-md non-trivial result; grep results for step 0d and step 1 strings; A2/A3/A4 facts), `## Compliance`, `## Sources`; conditional `## Movement after 2016` if step 0b needed it; post reference to Dominic on the last line | 2026-09-12 18:00 | OPEN |

**Plan-level stop:** the plan closes when step 2's stop condition is met. If any Wave 0 verification fails in a way that needs `run_deep.py` or the engine to be run again, MHM records the failure in `REPORT.md` `## Verification`, still posts to Dominic, and the fix becomes a new `plan_id`. Pure re-plot or text polish from existing on-disk data is allowed inside this plan.

Owner-side rules for the card: MHM only. No `tv`. No RA/PA hand-offs. No edits to `risk.md`, `universe.md`, engine, or skills. No re-execution of `run_deep.py`.

## Definition of done

Checkable by listing files and grepping content under `/workspace/mhm/research/sheet_vs_research/plus2_plus4_deep/`.

Non-trivial test (every `.md`): ≥ 25 non-blank lines; no `TODO` / `TBD` / `FIXME`; each quoted number has an on-disk path in the same section; a `## Sources` section.

- [ ] `spy_full_dollars.png`, `spy_5y_dollars.png`, `btc_full_dollars.png`, `btc_5y_dollars.png` exist, each size > 0; `REPORT.md` chart index records for each: asset, window (start–end), series shown (Sheet +4, Sheet +2/+4, Research +4, Research +2/+4), marker Y/N; marker = Y for `btc_full_dollars.png`.
- [ ] `NOTE_2016_btc.md` passes the non-trivial test and contains `2014-09-17`, `4377`, `2026-09-10`, `2014-11`, `2015-06`, `composition`, `not a data bug`, `spy_full_dollars.png`, `btc_full_dollars.png`.
- [ ] `turnover_tim.csv` exists; header has name / ruleset / gate / window plus turnover and time-in-market fields; rows for SPY and BTC; a before/after-~2016 comparison exists in the CSV or in `REPORT.md` `## Movement after 2016`.
- [ ] `year_splits.md` passes the non-trivial test; `year_splits.csv` exists; partial years are flagged in the md.
- [ ] `DECISION.md` passes the non-trivial test; contains `live_min_abs_score`, `proposal`, `stats_all.csv`, `SPY`, `BTC`, `5y`, `combined`; contains a per-asset 5y verdict for SPY and for BTC; contains a line that the BTC gate is not loosened on 5y evidence and that the call is Dominic's; contains no instruction to edit `risk.md`.
- [ ] `REPORT.md` passes the non-trivial test; has `## Chart index`, `## Pointers`, `## Verification`, `## Compliance`, `## Sources`; `## Compliance` states: no `tv`; no RA/PA; no edits to `risk.md` / `universe.md` / engine / skills; `run_deep.py` run once, not re-run; last line is the post reference to Dominic.
- [ ] No file under `/workspace/mhm/risk.md`, `/workspace/mhm/universe.md`, the engine, or skills has a modification attributable to this plan.
- [ ] `02_plan.critique.md` in this scratchpad shows PASS on all eight checklist items (Planner).

## Open questions

None blocks Wave 1. Each has an owner from the roster, a place it is resolved, and a default.

| id | question | owner | resolve in | default if unresolved |
|---|---|---|---|---|
| Q1 | Does `run_deep.py` use the identical +2 half-size tier rule as `slice_01_plus2_ev_vs_plus4/` (+2 and +3 at half, +4 full)? | Multi-Horizon Momentum | T6 `## Verification` (read from `run_deep.py` / `README.md`) | State the rule as implemented; if it differs from slice_01, one line in `DECISION.md` says so. No re-run. |
| Q2 | Is "alone" the whole $9k on one asset, or the per-asset share of the combined book? | Multi-Horizon Momentum | T6 `## Verification` | Whole $9k single-asset sleeve; `DECISION.md` wording must match whichever is true. |
| Q3 | Can exact first-usable dates per ruleset (first non-zero BTC score) be read from existing output, replacing `~2014-11` / `~2015-06`? | Multi-Horizon Momentum | T2 | Keep `~` dates with the lookback reasoning; do not run anything to get exact dates. |
| Q4 | Does `turnover_tim.csv` already contain a before/after-~2016 split, or only full / 5y windows? | Multi-Horizon Momentum | T3 (step 0b) | If only full / 5y, add the ≤ 6-row `## Movement after 2016` table to `REPORT.md` from existing CSVs. |
| Q5 | Are the combined PNGs kept or deleted? | Multi-Horizon Momentum | T6 chart index | Keep, labelled "context only — combined book"; never cited for a per-asset claim. |
| Q6 | Is the ~2026-09-13 18:00 UTC decision deadline still relevant now that `DECISION.md` exists? | Planner | this plan (resolved) | Resolved: decision exists; all remaining deadlines are 2026-09-12. |
| Q7 | Should the post to Dominic wait for `REPORT.md`, or go now with `DECISION.md` alone? | Multi-Horizon Momentum | T6 | Post once, after `REPORT.md`, with both paths; if Dominic asks earlier, send the `DECISION.md` path alone and still finish T6. |

## Changelog

| version | date | brain | change |
|---|---|---|---|
| 1 | 2026-09-12 | fable-5.1 | Pre-execution in-depth draft: six MHM-only tasks (charts → note / turnover / year splits → decision → report), Wave 1 charts ASAP, decision by 2026-09-13 18:00 UTC. Superseded before commit. |
| 2 | 2026-09-12 | fable-5.1 | Rewritten as **closeout** after MHM reported the core artifacts complete under `plus2_plus4_deep/`. Same six tasks mapped to real paths; T1/T3/T4/T5 marked MET pending T6 verification; open work reduced to expanding `NOTE_2016_btc.md` (T2) and writing the thin `REPORT.md` index + post (T6). Status `ready`. No RA/PA; no re-runs; no `risk.md` edits. |
