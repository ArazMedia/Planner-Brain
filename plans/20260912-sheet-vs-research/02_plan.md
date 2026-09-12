# Plan: Sheet vs Research — decision-ready win map, gap list, and ordered execution

```
plan_id: 20260912-sheet-vs-research
title: Sheet vs Research — decision-ready win map, gap list, and ordered execution
requester: Multi-Horizon Momentum (Dominic via MHM)
created: 2026-09-12
status: draft
brain: fable-5.1
depth: in-depth
version: 1
```

## Goal

Produce a decision-ready **Sheet vs Research** note for Dominic (matches `01_goals.md`, confirmed):

1. Map the regimes / markets / horizons where the **Sheet** ruleset wins vs where **Research** wins, built from backtests and library papers **already on disk**.
2. Produce an explicit, **ranked gap list** limited to gaps that would change a desk decision: `ruleset_in_force`, live gates (`live_min_abs_score`, +4 long-only), or `universe`.
3. Give MHM an **ordered multi-bot execution** with owner, artifact path under `/workspace/mhm/research/sheet_vs_research/`, stop condition, and deadline for every step.
4. **Stop** when Dominic has the note plus a short ranked list of next analyses. This plan is bounded; it is not an open-ended research spiral.

All findings are **proposals only**. Dominic must `apply` any change to ruleset, gates, or universe.

## Success criteria

Must (each has a task; see Work breakdown):

| id | criterion | checked by | task |
|---|---|---|---|
| M1 | `win_map.md` exists with a regime × market × horizon table; every cell either cites an on-disk path (backtest dir, stats file, or library doc) or is explicitly marked `UNMEASURED` | file + grep for `UNMEASURED`/paths | T1 |
| M2 | `RA_period_attribution.md` exists; each hypothesis from RA intake is tested against the 5y calendar using the 5y equity curves and marked `SUPPORTED` / `REFUTED` / `INCONCLUSIVE` | file + verdict tags | T2 |
| M3 | `PA_spy_structure.md` + one chart PNG exist; annotates Sheet (5–42d/MAD) vs Research (21–252d/EWMA) structure for SPY this week from `scores.json`; no recomputed scores | both files exist | T3 |
| M4 | `gap_list.md` exists; gaps ranked; each gap names the desk decision it would change, the measurement needed, the owner who would measure it, effort, and a `THIS_CYCLE: Y/N` flag | file + per-gap fields | T4 |
| M5 | `REPORT.md` exists, terse, contains RA-mandated items (a) live gates, (b) 5y Research > Sheet vs full-sample Sheet BTC edge and neither gated SPY sleeve beats SPY BH, (c) structural Sheet 5–42d/MAD vs Research 21–252d/EWMA with this week's SPY −2 vs +2; ends with ≤5 ranked next analyses; labelled "proposals only"; posted to Dominic | file + posted | T6 |
| M6 | Compliance attestation in `REPORT.md`: MHM never ran `tv`; no edits to `risk.md`, `universe.md`, engine, or skills; no backtest on disk re-run from scratch | attestation section present | T6 |

Should:

| id | criterion | task |
|---|---|---|
| S1 | At most **one** new engine slice run this cycle, and only if `gap_list.md` rank #1 is `THIS_CYCLE: Y` and engine-measurable in one session | T5 |
| S2 | PA dual Strategy Tester explicitly **deferred** with the rationale recorded in `gap_list.md` and `REPORT.md` (not run this cycle) | T4, T6 |

## Out of scope

Deliberately de-scoped, with reason:

| item | why |
|---|---|
| 0DTE / CPI-day tactics | Not a Sheet-vs-Research question; different horizon and instrument set. |
| Earnings names | Universe is SPY, SMH, BTC; single-name event risk is orthogonal to the ruleset comparison. |
| Hormuz / geopolitical day-trades | Discretionary, not systematic; no backtest basis on disk. |
| UW (unusual whales) as a signal | RA de-scoped UW-as-signal; no owner in roster needs it for this plan. |
| Parameter search / optimisation of either ruleset | Would be a new-ruleset project, and risks overfitting; goal is to compare the two rulesets as specified. |
| PA dual Strategy Tester **before** the written win map | Constraint: structure snapshot first; tester is UI-manual (30–60m per symbol × ruleset ≈ 2–4h for SPY+BTC) and cannot change a gate decision before the written map exists. Recorded as a ranked next analysis, not a task. |
| Re-running any backtest already on disk from scratch | Constraint. Only a **new slice** (regime split, lag, +2 vs +4, SMH sleeve) may be run, and only via T5 if it qualifies. |
| Editing `risk.md`, `universe.md`, engine, or skills | Hard constraint. Findings are proposals; Dominic applies. |
| Cash-short P&L as a live consideration | Cash shorts are paper on this desk; shorts appear in the win map only as a labelled paper column. |
| More than one new engine slice, or any slice whose result cannot change `ruleset_in_force` / gates / `universe` this cycle | Anti-spiral rule. |

## Constraints

Hard (from brief):

- MHM never runs `tv`. Anything TradingView is owned by Price Action Analyst.
- Nothing in this plan changes `/workspace/mhm/risk.md`, `/workspace/mhm/universe.md`, the engine, or skills.
- The library `/workspace/mhm/research/` is the first source. Cite library and on-disk backtests before any web source; web sources are not expected to be needed.
- Every step ends in a **named file path** under `/workspace/mhm/research/sheet_vs_research/`. "MHM says done" is not a stop condition. A stop condition is: file exists **and** is non-trivial (see Definition of done for the non-trivial test).
- Do not redo backtests already on disk. New engine runs only for a genuinely new slice, and only via T5.
- PA structure snapshot **before** any dual Strategy Tester work.
- Owners only from the roster: Planner, Multi-Horizon Momentum (MHM), Research Analyst (RA), Price Action Analyst (PA).
- Dominic preferences: terse; interested in +4 long-only on SPY and BTC; no paper spam. `REPORT.md` and the post to Dominic obey this.
- 5–8 tasks maximum; parallelise only independent tasks.

Soft:

- Deadlines below assume plan approval on 2026-09-12. If approval slips, shift all deadlines by the same offset but keep ordering.
- Effort units: S < 1h, M 1–3h, L half day.

## Assumptions

Each assumption is unconfirmed unless noted; the task that tests or relies on it is named. MHM's early read is stress-tested here, not accepted.

| id | assumption | status | stress test / where handled |
|---|---|---|---|
| A1 | **MHM early read:** Research wins sustained trends and the 5y +4 long-only window. Supported by `spy_btc_plus4_long/5y` (Research ~$14.2k vs Sheet ~$10.3k on $9k). | partially supported — single 5y window, combined SPY+BTC portfolio | T2 tests whether the edge is concentrated in a few sub-periods (2020 recovery, 2023–mid-2024) or broad; T1 splits per asset using `stats_{SPY,BTC}_{sheet,research}.txt`. If the edge sits in ≤2 sub-periods, the win map must say "Research wins in X regimes", not "Research wins". |
| A2 | **MHM early read:** Sheet wins full-sample BTC +4 longs. Supported by `spy_btc_plus4_long/full` (Sheet ~$45k vs Research ~$30k). | unconfirmed at asset level — full-sample figure is combined SPY+BTC | T1 must isolate BTC using `stats_BTC_{sheet,research}.txt`; RA intake frames this as an asset/regime feature (fast catch of discontinuous crypto expansions), not evidence for Sheet on SPY. Win map must not generalise BTC to SPY. |
| A3 | **MHM early read:** Neither gated SPY sleeve beats SPY buy-and-hold over full history. Supported by SPY BH ~$78k vs Sheet ~$45k / Research ~$30k (full) and ~$15.7k vs $14.2k / $10.3k (5y). | supported at portfolio level; SPY-only sleeve comparison not isolated | T1 reports the SPY-only sleeve vs SPY BH if `stats_SPY_*` allow it; otherwise the cell is `UNMEASURED` and becomes a gap candidate. Note the comparison is return-only; ret/vol and drawdown from stats files must be shown alongside, since a gated sleeve is meant to buy drawdown protection, not beat BH on return. |
| A4 | Library `Sanity_Backtest.md` figure (live-set Research ret/vol 0.62 vs Sheet 0.27) is on a universe consistent with the current live set (SPY, SMH, BTC). | unconfirmed — SMH may not be in the sanity set | T1 checks the sanity universe; if SMH is absent, "SMH live sleeve with same filters" is auto-included in the gap list (T4). |
| A5 | Existing backtests use the same lag, cost, and start-date conventions for both rulesets. | unconfirmed | T1 records lag/cost/start-date per backtest dir in a provenance table. If they differ, that is a gap (T4), not something to fix in this plan. |
| A6 | BTC history is shorter than SPY in the "full" runs, so "full-sample" is not the same window per asset. | likely true, unconfirmed | T1 provenance table; win map labels windows explicitly. |
| A7 | The seven library paper analyses plus `00_Combined_Analysis_and_Strategy_Derivation.md`, `MHM_Strategy_Spec.md` §§3–5 and `Sanity_Backtest.md` are sufficient paper evidence; no new web sourcing needed. Papers named by MHM: Moskowitz/Hurst, Levine–Pedersen, CFM/Sepp, Hamill (shorts mostly paper). | assumed | T1 cites library paths; if a claim cannot be grounded in the library, mark `UNMEASURED` rather than fetch from web. |
| A8 | PA can produce a useful SPY structure snapshot without the research-horizon drawings, using `/workspace/mhm/weekly/2026-09-14/scores.json` and the ruleset horizon definitions (Sheet 5–42d/MAD; Research 21–252d/EWMA). | supported by PA intake ("none block structure snapshot") | T3. PA does not recompute scores. |
| A9 | PA screenshots may be low-res thumbnails. | flagged by PA intake | T3 stop condition accepts a low-res PNG if `PA_spy_structure.md` carries the annotations in text. |
| A10 | Dominic's decision surface this cycle is exactly: (i) keep `ruleset_in_force: sheet` vs switch to `research` vs keep sheet and log Research beside; (ii) `live_min_abs_score` 4 vs 2 (this week Research gives SPY +2 / BTC +2 → flat under +4); (iii) whether SMH joins the +4 long-only sleeve. | assumed from desk config and RA intake | T4 ranks gaps only against these three decisions. |
| A11 | The note is not required before the 2026-09-14 gate. Sheet is in force and yields flat SPY/BTC this week regardless; the note informs the following cycle. | assumed (Open question Q4) | Deadlines set for 2026-09-16. |
| A12 | RA intake's recommendation — keep `sheet` in force and log Research beside until Dominic decides — is the default proposal unless T1/T2 evidence contradicts it. | assumed | T6 states the default and any evidence against it. |

## Context and inputs

Desk state (do not re-derive):

- Live universe: SPY, SMH, BTC · capital $9k · target 10% · cap 100% · `ruleset_in_force: sheet` · `live_min_abs_score: 4` · cash shorts = paper.
- This week (2026-09-14): SPY Sheet −2 / Research +2 · SMH Sheet −2 / Research 0 · BTC Sheet 0 / Research +2 · under +4 long-only → flat SPY/BTC.
- Scores for PA: `/workspace/mhm/weekly/2026-09-14/scores.json`.

Backtests on disk (cite, do not redo):

- GLD+USO: `/workspace/mhm/backtests/2026-09-12/gld_uso/`
- SPY+BTC |score|=4: `/workspace/mhm/backtests/2026-09-12/spy_btc_score4/{full,5y}/`
- SPY+BTC +4 long-only: `/workspace/mhm/backtests/2026-09-12/spy_btc_plus4_long/{full,5y}/` — Full: $9k → Sheet ~$45k, Research ~$30k, SPY BH ~$78k. 5y: Sheet ~$10.3k, Research ~$14.2k, SPY BH ~$15.7k.
- Stats: `/workspace/mhm/ledger/stats_{SPY,BTC,GLD,USO}_{sheet,research}.txt`

Library (first source): `/workspace/mhm/research/` — seven paper analyses; `00_Combined_Analysis_and_Strategy_Derivation.md`; `MHM_Strategy_Spec.md` (§§3–5 relevant); `Sanity_Backtest.md` (Research >> Sheet on equity ETFs; Sheet earns on BTC/TSLA/commodities; live-set Research ret/vol 0.62 vs Sheet 0.27).

Prior context notes: `requests/2026-09-11-gld-uso-context.md`, `requests/2026-09-11-spy-btc-context.md`. No prior Sheet-vs-Research attribution note exists.

Intake received:

- **PA:** highest leverage is a SPY structure/regime snapshot on the MHM layout (~15–25m) from `scores.json`, annotating the rulesets MHM names; dual Strategy Tester is ready in principle but UI-manual (~30–60m per symbol × ruleset) and sequenced after the snapshot. Blockers (research-horizon drawings not run; tester CLI weak; low-res screenshots) do not block the snapshot.
- **RA:** Research 5y edge hypotheses — sustained equity bulls / low-turnover grinds (≈2020 recovery; 2023–mid-2024), post-crisis rebounds, moderate vol with persistent trend; equity Research >> Sheet; BTC mixed. Sheet's BTC full-sample edge is a fast catch of discontinuous crypto expansions — an asset/regime feature. Three MUST items for the note: (a) live gates; (b) 5y Research > Sheet vs full-sample Sheet BTC edge and neither gated SPY beats BH; (c) structural Sheet 5–42d/MAD vs Research 21–252d/EWMA (this week SPY −2 vs +2).

Candidate gaps (to be ranked in T4, not all done): regime split by vol/rates/crisis; SPY+BTC correlation when both +4; turnover/cost; lag 1 vs 2; +2 EV>0 vs +4-only; SMH live sleeve same filters; live gate interaction; PA structure when Sheet≠Research; RA period attribution for Research 5y edge.

Artifact root for all execution outputs: `/workspace/mhm/research/sheet_vs_research/`

## Work breakdown

Six tasks. Wave 1 (T1, T2, T3) is independent and runs in parallel. T5 is conditional.

| task_id | task | owner | inputs | output | depends_on | effort |
|---|---|---|---|---|---|---|
| T1 | Write the Sheet vs Research **win map** from existing evidence: regime × market (SPY, SMH, BTC, GLD, USO) × horizon (5y, full) table, long-only vs paper-short columns, per-asset isolation from stats files, provenance table (window, lag, cost per backtest dir), library citations for each claim; `UNMEASURED` where no disk evidence | Multi-Horizon Momentum | backtest dirs `spy_btc_plus4_long/{full,5y}`, `spy_btc_score4/{full,5y}`, `gld_uso/`; `ledger/stats_*`; library `Sanity_Backtest.md`, `MHM_Strategy_Spec.md` §§3–5, `00_Combined_Analysis_and_Strategy_Derivation.md`, seven paper analyses; Assumptions A1–A7 | `/workspace/mhm/research/sheet_vs_research/win_map.md` | — | M |
| T2 | **Period attribution** of the Research 5y edge: test each RA hypothesis (2020 recovery; 2023–mid-2024 grind; post-crisis rebounds; moderate-vol persistent trend) against the calendar using the 5y equity curves; tag each `SUPPORTED` / `REFUTED` / `INCONCLUSIVE`; state which fraction of the 5y Research-minus-Sheet gap sits in the top two sub-periods; context only, no score changes | Research Analyst | `spy_btc_plus4_long/5y/` equity curves and trade logs; `stats_{SPY,BTC}_{sheet,research}.txt`; RA intake hypotheses; `requests/2026-09-11-spy-btc-context.md` | `/workspace/mhm/research/sheet_vs_research/RA_period_attribution.md` | — | M |
| T3 | **SPY structure snapshot** on the MHM TradingView layout for the week of 2026-09-14: mark Sheet horizon (5–42d/MAD) and Research horizon (21–252d/EWMA) structure, explain visually why Sheet reads −2 and Research +2, note SMH (−2 / 0) and BTC (0 / +2) in one line each; do not recompute scores | Price Action Analyst | `/workspace/mhm/weekly/2026-09-14/scores.json`; ruleset horizon definitions from `MHM_Strategy_Spec.md`; PA intake | `/workspace/mhm/research/sheet_vs_research/PA_spy_structure.md` and `/workspace/mhm/research/sheet_vs_research/PA_spy_structure_2026-09-14.png` | — | S |
| T4 | **Ranked gap list**: score every candidate gap against the three desk decisions (A10); for each gap give decision changed, measurement spec, owner who would measure, effort, `THIS_CYCLE: Y/N`; auto-include SMH sleeve if A4 fails and lag/cost if A5 fails; record PA tester as deferred with reason; name the single slice (if any) that T5 should run | Multi-Horizon Momentum | T1 `win_map.md`; T2 `RA_period_attribution.md`; candidate gap list; desk config | `/workspace/mhm/research/sheet_vs_research/gap_list.md` | T1, T2 | S |
| T5 | **Conditional new engine slice** — run **only** if `gap_list.md` rank #1 is `THIS_CYCLE: Y`, engine-measurable in one session, and not already on disk. Expected candidate (pre-ranked by Planner, MHM confirms in T4): `+2 EV>0 vs +4-only` for SPY and BTC long-only under live gates, both rulesets, full and 5y — this is the slice that bears directly on `live_min_abs_score` and this week's flat-vs-long outcome. If the trigger fails, write the skip file instead | Multi-Horizon Momentum | T4 `gap_list.md` rank #1 spec; engine (read-only use, no edits); existing backtest conventions from T1 provenance table | `/workspace/mhm/research/sheet_vs_research/slice_01_<gap_id>/README.md` plus engine CSVs in the same dir — **or** `/workspace/mhm/research/sheet_vs_research/slice_01_SKIPPED.md` stating the failed trigger | T4 | M (or S if skipped) |
| T6 | **REPORT.md synthesis** for Dominic and post: terse; RA MUST items (a)(b)(c); win map summary; top gaps; T5 result or skip; default proposal (A12) and evidence for/against; ≤5 ranked next analyses (PA dual tester included here, not as a task); "proposals only — Dominic must `apply`"; compliance attestation (M6); then post to Dominic | Multi-Horizon Momentum | T1, T2, T3, T4, T5 outputs | `/workspace/mhm/research/sheet_vs_research/REPORT.md` | T3, T4, T5 | S |

## Sequence

Ordered execution card for MHM (Planner → MHM reply format: owner · artifact path · stop condition · deadline). Deadlines are UTC and assume approval on 2026-09-12.

**Wave 1 — parallel, independent (existing evidence only)**

| step | task | owner | artifact path | stop condition | deadline |
|---|---|---|---|---|---|
| 1a | T1 win map | MHM | `/workspace/mhm/research/sheet_vs_research/win_map.md` | file exists; contains the regime × market × horizon table, a provenance table, ≥1 cited on-disk path per non-`UNMEASURED` cell, and passes the non-trivial test | 2026-09-13 18:00 |
| 1b | T2 period attribution | RA | `/workspace/mhm/research/sheet_vs_research/RA_period_attribution.md` | file exists; every RA hypothesis carries a `SUPPORTED`/`REFUTED`/`INCONCLUSIVE` tag with a date range and a pointer into the 5y backtest dir; passes the non-trivial test | 2026-09-13 18:00 |
| 1c | T3 SPY structure snapshot | PA | `/workspace/mhm/research/sheet_vs_research/PA_spy_structure.md` + `PA_spy_structure_2026-09-14.png` | both files exist; md names both rulesets' horizons and the −2 / +2 reading; PNG non-zero size (low-res acceptable per A9); passes the non-trivial test | 2026-09-13 18:00 |

**Wave 2 — sequential**

| step | task | owner | artifact path | stop condition | deadline |
|---|---|---|---|---|---|
| 2 | T4 gap list | MHM | `/workspace/mhm/research/sheet_vs_research/gap_list.md` | file exists; every gap has decision / measurement / owner / effort / `THIS_CYCLE`; PA tester listed as deferred with reason; rank #1 named with an explicit T5 go / no-go line | 2026-09-14 12:00 |
| 3 | T5 conditional slice | MHM | `/workspace/mhm/research/sheet_vs_research/slice_01_<gap_id>/README.md` + CSVs, **or** `slice_01_SKIPPED.md` | one of the two paths exists; README states window, lag, cost, gate, and the one-line decision implication; no existing backtest re-run | 2026-09-15 18:00 |
| 4 | T6 REPORT + post | MHM | `/workspace/mhm/research/sheet_vs_research/REPORT.md` | file exists; contains (a)(b)(c), ≤5 ranked next analyses, "proposals only", compliance attestation; MHM has posted the terse summary to Dominic with the REPORT path | 2026-09-16 12:00 |

**Plan-level stop:** the plan is complete when step 4's stop condition is met. Any further analysis (including the PA dual Strategy Tester or a second engine slice) requires a new `plan_id`. Wave 1 tasks that miss deadline do not block T4: T4 proceeds with the available files and lists the missing one as a gap.

Owner-side rules restated for the card: MHM never runs `tv` (1c is PA). MHM does not edit `risk.md`, `universe.md`, engine, or skills at any step. RA produces context only, no score changes. PA never computes MHM scores.

## Definition of done

All checkable by listing files and grepping content.

Non-trivial test (applies to every `.md` artifact): ≥ 25 non-blank lines; no `TODO` / `TBD` / `FIXME` strings; every claimed number is accompanied by an on-disk path in the same section; a `## Sources` section listing every path read.

- [ ] `win_map.md` exists and passes the non-trivial test; contains a table with rows for at least SPY, SMH, BTC and columns for at least 5y and full windows; each cell cites a path or reads `UNMEASURED`; contains a provenance table with window / lag / cost per backtest dir.
- [ ] `RA_period_attribution.md` exists and passes the non-trivial test; each RA hypothesis has one of `SUPPORTED`, `REFUTED`, `INCONCLUSIVE`; states the share of the 5y Research-minus-Sheet gap held by the top two sub-periods.
- [ ] `PA_spy_structure.md` exists and passes the non-trivial test; `PA_spy_structure_2026-09-14.png` exists with size > 0; md contains the strings `5–42d`/`MAD` and `21–252d`/`EWMA` and the readings `−2` and `+2` for SPY.
- [ ] `gap_list.md` exists and passes the non-trivial test; gaps are numbered in rank order; each has `decision:`, `measurement:`, `owner:`, `effort:`, `THIS_CYCLE:` fields; contains a line beginning `T5:` with `GO` or `NO-GO`; lists PA dual tester as `DEFERRED` with reason.
- [ ] Exactly one of `slice_01_<gap_id>/README.md` or `slice_01_SKIPPED.md` exists; if the slice ran, the dir also contains ≥1 CSV and the README states window, lag, cost, gate, and decision implication.
- [ ] `REPORT.md` exists and passes the non-trivial test; contains sections or bullets for (a) live gates, (b) 5y vs full-sample and SPY BH comparison, (c) structural horizon difference with this week's −2 vs +2; ≤5 numbered next analyses; the phrase `proposals only`; a `## Compliance` section stating no `tv` by MHM, no edits to `risk.md`/`universe.md`/engine/skills, no backtest re-run from scratch.
- [ ] MHM has posted the terse summary and REPORT path to Dominic (post reference recorded at the bottom of `REPORT.md`).
- [ ] No file under `/workspace/mhm/risk.md`, `/workspace/mhm/universe.md`, the engine, or skills has a modification time after plan approval attributable to this plan.
- [ ] `02_plan.critique.md` in this scratchpad shows PASS on all eight checklist items (Planner).

## Open questions

Each has an owner and the task where it is resolved. None blocks Wave 1 start.

| id | question | owner | resolve in | default if unresolved |
|---|---|---|---|---|
| Q1 | Do the "full" runs use the same start date for SPY and BTC, or is BTC's window shorter? | Multi-Horizon Momentum | T1 provenance table | Label windows per asset; do not compare across unequal windows without saying so. |
| Q2 | Which signal lag (1 or 2 bars) and cost assumption do the on-disk backtests use, and is it identical for both rulesets? | Multi-Horizon Momentum | T1 provenance table | If unknown or unequal, add "lag/cost parity" to `gap_list.md`; do not re-run. |
| Q3 | Is SMH present in any existing backtest or in the `Sanity_Backtest.md` live set? | Multi-Horizon Momentum | T1 | If absent, SMH sleeve is an auto-gap in T4 with `THIS_CYCLE: N` unless it outranks the +2 vs +4 slice. |
| Q4 | Does Dominic need the note before the 2026-09-14 gate, or is post-gate (2026-09-16) acceptable? | Planner | before Wave 1 start; else A11 stands | Post-gate acceptable; Sheet in force gives flat SPY/BTC this week either way. |
| Q5 | Will PA's PNG be a low-res thumbnail, and if so is text annotation in the md sufficient for Dominic? | Price Action Analyst | T3 | Accept low-res PNG if md carries all annotations (A9). |
| Q6 | Weekly or monthly granularity for period attribution? | Research Analyst | T2 | Monthly buckets on the 5y equity curve, with weekly detail only for the top two sub-periods. |
| Q7 | Should T5's pre-ranked candidate (+2 EV vs +4-only under live gates) be confirmed as rank #1, or does T1/T2 evidence promote a regime split or SMH sleeve above it? | Multi-Horizon Momentum | T4 | Planner's pre-rank stands unless T4 gives a written reason. |

## Changelog

| version | date | brain | change |
|---|---|---|---|
| 1 | 2026-09-12 | fable-5.1 | Initial in-depth draft from brief, PA intake, RA intake, and confirmed `01_goals.md`. Six tasks, two waves, one conditional engine slice, PA tester deferred to next-analyses list. |
