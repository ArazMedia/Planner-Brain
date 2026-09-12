# Plan: Independent re-test PDF intake — claim map vs handoff / Plan A / Plan B, engine verification of 2–3 headlines, RA deep pass, decision note (ruleset · gate · stops · sizing, in-sample caveat), ranked §9 opens, decision-complete REPORT

```
plan_id: 20260912-independent-retest
title: Independent re-test PDF intake — claim map vs handoff / Plan A / Plan B, engine verification of 2–3 headlines, RA deep pass, decision note (ruleset · gate · stops · sizing, in-sample caveat), ranked §9 opens, decision-complete REPORT
requester: Multi-Horizon Momentum (Dominic via MHM)
created: 2026-09-12
status: draft
brain: fable-5.1
depth: in-depth
version: 1
```

> **Execution state at plan time:** MHM has staged the artifact root `/workspace/mhm/research/independent_retest_2026-09-12/` with `source.pdf`, `source.txt`, `README.md`, `claim_map.md` (stub), `proposals_stub.md` (stub), and `RA_intake_reply.md` (received, seven items). This plan **fills and completes those files**; it does not create a parallel tree. Wave 1 runs claim map, RA deep pass and engine verification in parallel; `DECISION.md` and `REPORT.md` come last. All outputs are proposals. No task edits `risk.md`, `universe.md`, the engine, or skills.

## Goal

Matches the confirmed `01_goals.md` (six items, quoted in the brief). Take the independent re-test PDF from intake to a **decision-ready desk deep work** package under the artifact root:

1. **Claim map.** Map every PDF claim (headline list below, and especially the §7 handoff section) onto what the desk already has — tonight's SPY/BTC handoff, Plan A (`20260912-sheet-vs-research`), Plan B (`20260912-plus2-plus4-deep`, closed) — tagging each `REPRODUCED` (PDF agrees with an on-disk desk finding), `CORRECTED` (PDF contradicts or refines an on-disk finding), or `NEW` (no desk artifact covers it).
2. **Decision note.** One note covering the four decision axes — **ruleset** (Sheet in force vs Research), **gate** (`live_min_abs_score: 4`, do not loosen BTC to +2), **stops** (PDF: no stop helps), **sizing** (PDF lever: SPY cap 60–80%, BTC 7.5%) — each carrying the §8 **in-sample** caveat; proposals only, Dominic applies.
3. **RA deep pass.** The RA intake (seven items, received) is the starting point; RA deepens it into an execution artifact, refining verdicts only where a cited path supports the change.
4. **Engine verification.** MHM reproduces 2–3 PDF headline numbers with `mhm.py` (read-only use) or documents the delta (data source, start date, cost, lag, window, metric definition) when the number cannot be matched. No parameter search.
5. **Ranked §9 opens.** The PDF's §9 open items are ranked for later `plan_id`s; none is executed in this plan.
6. **`REPORT.md` decision-complete.** Dominic can decide from `REPORT.md` + `DECISION.md` alone. **No** automatic edits to `risk.md`, `universe.md`, engine, or skills.

PDF headlines in scope (from brief): Research > Sheet on SPY; timing ≈ half-SPY return/vol (buys drawdown, not Sharpe); EV concentrated; 2022 drawdown help / 2020 partial; 5y cannot rank; mirror shorts lose; no stop helps; sizing lever SPY cap 60–80%, BTC 7.5%; learned book 11.4% / 1.32 / −12%; §8 is in-sample; §7 handoff — 5y book misaligned, start dates, keep |score|=4, don't loosen BTC +2, 2016 kink OK.

## Success criteria

Must (each has exactly one task):

| id | criterion | checked by | task |
|---|---|---|---|
| M1 | `claim_map.md` is filled: one row per PDF headline (all 13 listed in Goal) **plus** one row per §7 handoff item; each row has `tag ∈ {REPRODUCED, CORRECTED, NEW}`, a PDF section reference, and — for `REPRODUCED` / `CORRECTED` — an on-disk desk path (handoff doc, Plan A dir, Plan B dir); `NEW` rows name the later-plan candidate id used in `open_questions_ranked.md` | file; grep tags; every non-`NEW` row has a `/workspace/mhm/...` path | T1 |
| M2 | `DECISION.md` has one section per axis (`## Ruleset`, `## Gate`, `## Stops`, `## Sizing`), each with: PDF finding, desk evidence path(s), RA verdict pointer, engine-verify pointer, **proposal**, and the literal string `in-sample` in `## Sizing`; a `## Dominic decides` section listing at most three options per axis; the string `proposals only`; no instruction to edit `risk.md` | file + grep | T5 |
| M3 | `RA_deep.md` exists; each of the seven intake items is carried forward with a verdict `SUPPORTED` / `REFUTED` / `INCONCLUSIVE`, and every verdict change from `RA_intake_reply.md` cites a path; the six §8 must-caveats from intake item 6 are each expanded into one paragraph of proposed `risk.md` **language** (marked `PROPOSED — not applied`) | file + verdict tags + `PROPOSED — not applied` | T2 |
| M4 | `engine_verify.md` covers **2–3** headlines (fixed set below), each tagged `MATCH` (within stated tolerance), `DELTA` (number differs; cause documented), or `NOT_REPRODUCIBLE` (engine cannot express the PDF construction; reason stated); each has a run spec (ruleset, gate, window, data start, cost, lag, metric definition) and an on-disk CSV or stats path | file + tags + CSV paths | T3 |
| M5 | `open_questions_ranked.md` lists every §9 open item with rank, decision it would change, measurement spec, owner who would measure, effort, `THIS_PLAN: N` for all rows, and a suggested later `plan_id` slug | file + `THIS_PLAN` column all `N` | T4 |
| M6 | `REPORT.md` is decision-complete: `## Verdict` (one paragraph per axis), `## Claim map summary` (counts by tag), `## Engine verification summary`, `## RA deep summary`, `## Ranked opens (top 3)`, `## Compliance` (no `tv`; no PA/UW; no edits to `risk.md` / `universe.md` / engine / skills; engine used read-only), `## Verification` (directory listing with byte sizes; non-trivial-test result per md), `## Sources`; `README.md` indexes every file in the root; post reference to Dominic on the last line | file + headings + post reference | T6 |

Should:

| id | criterion | task |
|---|---|---|
| S1 | `proposals_stub.md` is either absorbed into `DECISION.md` (stub gets a one-line `Superseded by DECISION.md` header) or completed in place with the same four axes — not left as a bare stub | T5 |
| S2 | Optional CSVs `engine_verify_<headline>.csv` sit beside `engine_verify.md` and are referenced from it | T3 |
| S3 | `RA_deep.md` states plainly, in one sentence, that Research timing on SPY is **drawdown conversion, not higher return/vol** (intake item 1) | T2 |

## Out of scope

| item | why |
|---|---|
| Editing `/workspace/mhm/risk.md`, `/workspace/mhm/universe.md`, engine code, or skills | Hard constraint; every output is a proposal. RA writes proposed `risk.md` language as text inside `RA_deep.md` only. |
| PA dual Strategy Tester; any PA task | Not needed to meet any Must; PDF claims are number/logic claims verifiable from disk + engine. Default NO per roster rule. |
| UW (any task) | No Must requires it; default NO. |
| GLD / USO or any new universe member | PDF and desk scope is SPY and BTC. |
| Parameter search (score tiers, stop levels, cap sweeps, lag/cost grids) | The PDF sizing lever is §8 in-sample; sweeping it would compound the in-sample problem. T3 reproduces fixed PDF specs only. |
| Executing any §9 open item | T4 ranks them for later `plan_id`s. |
| Re-doing Plan A / Plan B artifacts | Cited by path as desk evidence; `claim_map.md` maps onto them. |
| Building an engine feature to express a PDF construction the engine lacks | T3 tags `NOT_REPRODUCIBLE` and documents; a build is a new `plan_id`. |
| Web sourcing beyond one public SPY 2022 figure | Library `/workspace/mhm/research/` and on-disk SPY closes are the first source (see A5). |

## Constraints

Hard (from brief):

- Every step ends in a **named file path** under `/workspace/mhm/research/independent_retest_2026-09-12/`. "MHM says done" is not a stop condition; the stop condition is the file existing and passing its check.
- Non-trivial test for every `.md` artifact: ≥ 25 non-blank lines; no `TODO` / `TBD` / `FIXME`; every quoted number has an on-disk path in the same section; a `## Sources` section.
- 5–8 tasks; owners only from the roster (MHM, Research Analyst, Planner); PA / UW not used.
- Wave 1 = fill `claim_map.md` + `RA_deep.md` + `engine_verify.md` in parallel; `DECISION.md` and `REPORT.md` last.
- Existing stubs are filled, not replaced by new files with different names. `RA_deep.md` is the one permitted new file for the RA pass (intake reply is preserved as the record — see Q7).
- Engine use is read-only: `mhm.py` is run, not modified.
- Deadlines assume start 2026-09-12; `REPORT.md` target ~2026-09-13 18:00 UTC.
- MHM never runs `tv`.
- Library first: `/workspace/mhm/research/` before any web source.
- Dominic preferences: terse; no paper spam; `REPORT.md` is decision-complete but not a second narrative of the PDF.

Soft:

- Effort units: S < 1h, M 1–3h.
- Engine-verify tolerance: `MATCH` if CAGR within ±1.0pp, Sharpe within ±0.10, max DD within ±2pp of the PDF figure under the PDF's stated construction; otherwise `DELTA` with cause.
- If a Wave 1 file misses its deadline, T5 proceeds with the available files and names the missing one in `## Dominic decides` as an open input; T6 lists it under `## Verification`.

## Assumptions

| id | assumption | status | where handled |
|---|---|---|---|
| A1 | The six staged files exist under the artifact root as MHM reports (`source.pdf`, `source.txt`, `README.md`, `claim_map.md`, `proposals_stub.md`, `RA_intake_reply.md`). Planner cannot list the directory from this scratchpad repo. | reported by MHM | T6 `## Verification` re-lists the directory with byte sizes. |
| A2 | `source.txt` is a faithful text extraction of `source.pdf` with §7, §8, §9 headings recoverable. | assumed | T1 checks first; if §-structure is lost, MHM re-extracts text (allowed; not engine work) and notes it in `claim_map.md` `## Sources`. |
| A3 | `mhm.py` exists at the desk's engine location, runs read-only from the CLI, and supports the Sheet and Research rulesets, the `|score| ≥ 4` gate, full and 5y windows, and per-asset sleeves as used in Plan A / Plan B. | assumed from Plan A/B history | T3 records the exact invocation per headline in `engine_verify.md`; anything unsupported is `NOT_REPRODUCIBLE`. |
| A4 | The learned-book headline `11.4% / 1.32 / −12%` is CAGR / Sharpe / max drawdown of the PDF's §8 sized book (SPY cap 60–80%, BTC 7.5%) over the PDF's full window. | assumed; PDF §8 is the source | T3 reads §8 first and records the metric definitions and window before running; if the engine cannot apply per-asset caps, T3 tags `NOT_REPRODUCIBLE` and shows the nearest uncapped book instead. |
| A5 | The SPY 2022 gap (PDF −19% vs RA "public ~−24–25%") is most likely **definitional**: −19% is close to the 2022 calendar-year price return of SPY, while −24–25% is close to the peak-to-trough close-to-close max drawdown (Jan → Oct 2022). | Planner hypothesis; unconfirmed | T3 computes both figures from the on-disk SPY closes used by the engine and states which one the PDF means; T2 reframes intake item 2 accordingly. Neither figure is called "wrong" until the definition is fixed. |
| A6 | Desk evidence lives at: tonight's SPY/BTC handoff (path known to MHM, Q1), Plan A `/workspace/mhm/research/sheet_vs_research/` (incl. `win_map.md`, `RA_period_attribution.md`, `gap_list.md`, `slice_01_plus2_ev_vs_plus4/`), Plan B `/workspace/mhm/research/sheet_vs_research/plus2_plus4_deep/` (incl. `DECISION.md`, `NOTE_2016_btc.md`, `stats_all.csv`, `year_splits.csv`). | Plan B closed; Plan A artifacts exist per prior plan | T1 cites these paths per row; a missing file makes the row `NEW` with a note, not a re-run. |
| A7 | RA intake verdicts (items 1–7) stand as the baseline; `RA_deep.md` may change a verdict only with a cited on-disk path or the T3 result. | received | T2 stop condition; T6 diff of verdicts intake → deep. |
| A8 | Engine data differ from the PDF's (desk: yfinance daily, BTC from 2014-09-17, n=4377 through 2026-09-10; cost and lag per Plan A provenance). Deltas of a few pp on long-window figures are expected and are documentation, not defects. | brief-confirmed data facts; PDF data source unknown | T3 `DELTA` rows name the suspected cause; no tuning to close the gap. |
| A9 | Decision surface is exactly four axes with at most three options each: ruleset {keep Sheet in force; switch SPY sleeve to Research; run Research as paper shadow}, gate {keep 4 both; SPY-only +2 half-size (Plan B); no change proposed for BTC}, stops {no stop (PDF); keep current desk stop if any; none else}, sizing {no change; adopt PDF caps as **paper** book; defer pending out-of-sample}. | assumed | T5 lists only these; extras labelled `not proposed`. |
| A10 | §7 handoff items — 5y book misaligned, differing start dates, keep |score|=4, don't loosen BTC +2, 2016 kink OK — largely `REPRODUCE` Plan B (`DECISION.md`, `NOTE_2016_btc.md`) and Plan A's demotion of 5y ranking. | expected | T1 confirms per row with a path; any `CORRECTED` in §7 is flagged in `REPORT.md` `## Verdict`. |
| A11 | No PA or UW involvement is justified: every Must is met from PDF text, on-disk artifacts, read-only engine runs, and RA. | roster default | `## Out of scope`; T6 `## Compliance` attests. |
| A12 | The post to Dominic is a terse message with `REPORT.md` and `DECISION.md` paths, not a paste. | Dominic preference | T6 stop condition. |

## Context and inputs

Desk gates (unchanged, do not re-derive): ruleset in force = Sheet; `live_min_abs_score: 4`; +4 long-only interest on SPY and BTC; cash shorts paper; capital $9k.

Prior desk work (cite, do not redo):

- **Handoff tonight (SPY/BTC)** — path per Q1; the PDF's §7 is written against it.
- **Plan A** `20260912-sheet-vs-research` — win map, RA period attribution, gap list, and the combined-book slice `slice_01_plus2_ev_vs_plus4/` (Full: Sheet +4 $45k → +2/+4 $72k; Research $30k → $45k. 5y: Sheet $10.3k → $11.8k; Research $14.2k → $15.0k).
- **Plan B** `20260912-plus2-plus4-deep` (closed) — per-asset $9k curves; `DECISION.md` (SPY +2 helps in 5y; BTC +2 hurts slightly; do not loosen BTC gate on 5y evidence); `NOTE_2016_btc.md` (2016 kink = composition, not a data bug).

Artifact root: `/workspace/mhm/research/independent_retest_2026-09-12/`

| file | state at plan time | role | Must |
|---|---|---|---|
| `source.pdf`, `source.txt` | present | the independent re-test; §7 handoff, §8 sizing (in-sample), §9 opens | input to all |
| `README.md` | present (stub) | root index; T6 completes it | M6 |
| `claim_map.md` | present (stub) | T1 fills | M1 |
| `proposals_stub.md` | present (stub) | absorbed by / completed as `DECISION.md` (S1) | M2 |
| `RA_intake_reply.md` | present (received) | RA baseline, seven items, paths listed in item 7 | input to T2, T5 |
| `RA_deep.md` | absent | T2 writes | M3 |
| `engine_verify.md` (+ `engine_verify_*.csv`) | absent | T3 writes | M4 |
| `DECISION.md` | absent | T5 writes | M2 |
| `open_questions_ranked.md` | absent | T4 writes | M5 |
| `REPORT.md` | absent | T6 writes | M6 |

RA intake (received; baseline for T2 and T5): (1) SPY Research edge SUPPORTED; timing = drawdown conversion, not higher return/vol. (2) 2022 narrative SUPPORTED; SPY −19% may be wrong (public ~−24–25%); exact sleeve % INCONCLUSIVE until MHM reproduces. (3) 2020 exit order SUPPORTED; exact DD% INCONCLUSIVE until MHM. (4) Flat 3–6y stretches + EV concentration SUPPORTED as expectation-setting. (5) Demote 5y book ranking SUPPORTED. (6) §8 must-caveats: in-sample sizing; timing ≠ free Sharpe; cash shorts paper + live |score| ≥ 4; no-stop accepts flats; keep Sheet watch; MHM reproduces before any `risk.md` language. (7) Paths in `RA_intake_reply.md`.

Fixed engine-verify set (T3; no more than three, no substitutions without a written reason in `engine_verify.md`):

| id | PDF headline | what to run |
|---|---|---|
| H1 | Learned book 11.4% / 1.32 / −12% (§8) | Sized SPY+BTC book per §8 caps if the engine supports caps; else nearest uncapped Sheet and Research +4 books, full window; tag per tolerance or `NOT_REPRODUCIBLE` |
| H2 | 2022 drawdown help; SPY −19% | SPY sleeve 2022: calendar-year return **and** peak-to-trough max DD for buy-and-hold vs Sheet +4 vs Research +4 (A5); state which definition the PDF uses |
| H3 | 2020 partial exit | SPY (and BTC) sleeve Feb–Apr 2020: exit date order and sleeve DD% for Sheet vs Research vs buy-and-hold |

Library (first source): `/workspace/mhm/research/` — cite before any web figure. The single permitted external figure is the public SPY 2022 return / drawdown for H2, and only if the on-disk closes cannot produce it.

## Work breakdown

Six tasks. Owners: MHM (T1, T3, T4, T5, T6), Research Analyst (T2). No PA / UW.

| task_id | task | owner | inputs | output | depends_on | effort |
|---|---|---|---|---|---|---|
| T1 | **Fill `claim_map.md`.** One row per PDF headline (13) and per §7 handoff item; columns: `claim`, `pdf_section`, `tag` (`REPRODUCED` / `CORRECTED` / `NEW`), `desk_path`, `note`, `later_plan_id` (for `NEW`). §7 rows compared against Plan B `DECISION.md` / `NOTE_2016_btc.md` and Plan A 5y demotion (A10). Summary counts by tag at top; `## Sources` | Multi-Horizon Momentum | `source.txt` / `source.pdf`; `claim_map.md` stub; handoff doc (Q1); Plan A dir; Plan B dir; `RA_intake_reply.md` | `/workspace/mhm/research/independent_retest_2026-09-12/claim_map.md` | — | M |
| T2 | **RA deep pass → `RA_deep.md`.** Carry the seven intake items forward with verdict tags; deepen items 1–5 with dated evidence from Plan A `RA_period_attribution.md`, Plan B `year_splits.csv`, and the PDF; reframe item 2 per A5 (definition before "wrong"); expand item 6's six caveats into proposed `risk.md` language, each marked `PROPOSED — not applied`; one plain sentence for S3; `## Sources` | Research Analyst | `RA_intake_reply.md`; `source.txt`; Plan A `RA_period_attribution.md`, `win_map.md`; Plan B `DECISION.md`, `year_splits.csv`, `NOTE_2016_btc.md`; library | `/workspace/mhm/research/independent_retest_2026-09-12/RA_deep.md` | — | M |
| T3 | **Engine verification → `engine_verify.md`.** For H1, H2, H3: read the PDF's construction (metric definitions, window, universe); run `mhm.py` read-only with the closest spec; tag `MATCH` / `DELTA` / `NOT_REPRODUCIBLE` with tolerance and cause; record the exact invocation; write `engine_verify_H1.csv`, `engine_verify_H2.csv`, `engine_verify_H3.csv` where a run happened; H2 includes both 2022 definitions (A5); `## Sources` | Multi-Horizon Momentum | `source.txt` §§6–8; `mhm.py`; on-disk SPY/BTC closes; Plan A provenance (cost, lag); Plan B `stats_all.csv` | `/workspace/mhm/research/independent_retest_2026-09-12/engine_verify.md` (+ `engine_verify_H*.csv`) | — | M |
| T4 | **Rank §9 opens → `open_questions_ranked.md`.** Every §9 item: rank, decision it would change (ruleset / gate / stops / sizing / none), measurement spec, owner who would measure (roster), effort, `THIS_PLAN: N`, suggested later `plan_id` slug; `NEW` rows from `claim_map.md` appended and ranked with them; items needing off-disk data marked `NEEDS_DATA`; `## Sources` | Multi-Horizon Momentum | `source.txt` §9; T1 `claim_map.md`; T3 `engine_verify.md` | `/workspace/mhm/research/independent_retest_2026-09-12/open_questions_ranked.md` | T1, T3 | S |
| T5 | **`DECISION.md`.** Four axis sections (`## Ruleset`, `## Gate`, `## Stops`, `## Sizing`): PDF finding → desk evidence path → RA verdict (T2) → engine result (T3) → proposal; `## Sizing` carries `in-sample` and the H1 tag; `## Dominic decides` with ≤ 3 options per axis (A9); `proposals only`; no `risk.md` edit instruction; absorb or complete `proposals_stub.md` (S1); `## Sources` | Multi-Horizon Momentum | T1 `claim_map.md`; T2 `RA_deep.md`; T3 `engine_verify.md`; `proposals_stub.md`; Plan B `DECISION.md` | `/workspace/mhm/research/independent_retest_2026-09-12/DECISION.md` (+ header line in `proposals_stub.md`) | T1, T2, T3 | M |
| T6 | **`REPORT.md` decision-complete + `README.md` index + post.** Sections per M6; `## Verification` re-lists the root with byte sizes and the non-trivial-test result per md, plus the intake → deep verdict diff (A7); `## Compliance` attests no `tv`, no PA/UW, no edits to `risk.md` / `universe.md` / engine / skills, engine read-only; `README.md` updated to index every file; post terse summary to Dominic with `REPORT.md` + `DECISION.md` paths; post reference on last line | Multi-Horizon Momentum | all files under the root; T4, T5 outputs | `/workspace/mhm/research/independent_retest_2026-09-12/REPORT.md` (+ `README.md`) | T4, T5 | S |

## Sequence

Planner → MHM execution card. Deadlines UTC; start 2026-09-12. Wave 1 steps run in parallel; Wave 2 needs Wave 1 complete (or deadline passed — soft constraint on missing files applies); Wave 3 closes.

**Wave 1 — parallel intake fill**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 1a (T1) | MHM | `/workspace/mhm/research/independent_retest_2026-09-12/claim_map.md` | ≥ 13 headline rows + all §7 rows; every row tagged `REPRODUCED` / `CORRECTED` / `NEW`; every non-`NEW` row has a `/workspace/mhm/` path; `NEW` rows have a `later_plan_id`; tag counts at top; passes the non-trivial test | 2026-09-13 10:00 |
| 1b (T2) | Research Analyst | `/workspace/mhm/research/independent_retest_2026-09-12/RA_deep.md` | seven items each with `SUPPORTED` / `REFUTED` / `INCONCLUSIVE`; any verdict change from intake cites a path; six `PROPOSED — not applied` paragraphs; contains the phrase `drawdown conversion`; item 2 states the 2022 definition question (A5); passes the non-trivial test | 2026-09-13 10:00 |
| 1c (T3) | MHM | `/workspace/mhm/research/independent_retest_2026-09-12/engine_verify.md` (+ `engine_verify_H1.csv`, `engine_verify_H2.csv`, `engine_verify_H3.csv` where run) | H1, H2, H3 each tagged `MATCH` / `DELTA` / `NOT_REPRODUCIBLE`; each has run spec (ruleset, gate, window, data start, cost, lag, metric definitions) and exact `mhm.py` invocation or the reason none was possible; H2 shows both 2022 calendar return and max DD for buy-and-hold, Sheet, Research; every quoted number has a CSV/stats path; passes the non-trivial test | 2026-09-13 10:00 |

**Wave 2 — synthesis**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 2a (T4) | MHM | `/workspace/mhm/research/independent_retest_2026-09-12/open_questions_ranked.md` | every §9 item + every `NEW` claim-map row present; columns rank / decision changed / measurement spec / owner / effort / `THIS_PLAN` / later `plan_id` slug; all `THIS_PLAN: N`; `NEEDS_DATA` flagged where applicable; passes the non-trivial test | 2026-09-13 13:00 |
| 2b (T5) | MHM | `/workspace/mhm/research/independent_retest_2026-09-12/DECISION.md` | headings `## Ruleset`, `## Gate`, `## Stops`, `## Sizing`, `## Dominic decides` present; `## Sizing` contains `in-sample` and the H1 tag; contains `proposals only`, `live_min_abs_score`, `RA_deep.md`, `engine_verify.md`; ≤ 3 options per axis; no instruction to edit `risk.md`; `proposals_stub.md` carries `Superseded by DECISION.md` or is completed in place; passes the non-trivial test | 2026-09-13 16:00 |

**Wave 3 — close**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 3 (T6) | MHM | `/workspace/mhm/research/independent_retest_2026-09-12/REPORT.md` (+ `README.md`) | headings `## Verdict`, `## Claim map summary`, `## Engine verification summary`, `## RA deep summary`, `## Ranked opens (top 3)`, `## Compliance`, `## Verification`, `## Sources`; `## Compliance` contains the four attestations (no `tv`; no PA/UW; no edits to `risk.md` / `universe.md` / engine / skills; engine read-only); `## Verification` lists every file in the root with byte size and per-md non-trivial result; `README.md` names every file in the root; last line is the post reference to Dominic; passes the non-trivial test | 2026-09-13 18:00 |

**Plan-level stop:** the plan closes when step 3's stop condition is met. Any §9 item, PA tester, UW pass, universe change, engine build, or parameter sweep is a new `plan_id`. A Wave 1 miss does not block Wave 2: T5 proceeds and names the missing input in `## Dominic decides`; T6 records it in `## Verification`.

Owner-side rules for the card: MHM never runs `tv`; engine read-only; no edits to `risk.md`, `universe.md`, engine, or skills; RA writes proposed language as text only; no new artifact tree — fill the staged files.

## Definition of done

Checkable by listing files and grepping content under `/workspace/mhm/research/independent_retest_2026-09-12/`.

Non-trivial test (every `.md`): ≥ 25 non-blank lines; no `TODO` / `TBD` / `FIXME`; each quoted number has an on-disk path in the same section; a `## Sources` section.

- [ ] `claim_map.md` passes the non-trivial test; ≥ 13 headline rows and all §7 rows; every row contains exactly one of `REPRODUCED`, `CORRECTED`, `NEW`; every `REPRODUCED` / `CORRECTED` row contains a `/workspace/mhm/` path; every `NEW` row contains a `later_plan_id`.
- [ ] `RA_deep.md` passes the non-trivial test; seven items each with one of `SUPPORTED`, `REFUTED`, `INCONCLUSIVE`; six occurrences of `PROPOSED — not applied`; contains `drawdown conversion`; contains `in-sample`.
- [ ] `engine_verify.md` passes the non-trivial test; contains `H1`, `H2`, `H3`, each followed by one of `MATCH`, `DELTA`, `NOT_REPRODUCIBLE`; contains `mhm.py`; for H2 contains both `calendar` and `max DD` (or `max drawdown`) figures for 2022; every CSV named in the file exists with size > 0.
- [ ] `open_questions_ranked.md` passes the non-trivial test; every row has `THIS_PLAN: N`; column headers include `rank`, `decision`, `owner`, `effort`, `plan_id`.
- [ ] `DECISION.md` passes the non-trivial test; contains `## Ruleset`, `## Gate`, `## Stops`, `## Sizing`, `## Dominic decides`, `in-sample`, `proposals only`, `live_min_abs_score`, `RA_deep.md`, `engine_verify.md`; contains no instruction to edit `risk.md`.
- [ ] `proposals_stub.md` first line contains `Superseded by DECISION.md`, **or** the file itself passes the non-trivial test with the four axis headings.
- [ ] `REPORT.md` passes the non-trivial test; contains the eight M6 headings; `## Compliance` contains `tv`, `PA`, `UW`, `risk.md`, `universe.md`, `read-only`; `## Verification` lists every file in the root with a byte size; last line is the post reference to Dominic.
- [ ] `README.md` names every file present in the root.
- [ ] No file under `/workspace/mhm/risk.md`, `/workspace/mhm/universe.md`, the engine, or skills has a modification attributable to this plan.
- [ ] `02_plan.critique.md` in this scratchpad shows PASS on all eight checklist items (Planner).

## Open questions

None blocks Wave 1. Each has one roster owner, a place it is resolved, and a default.

| id | question | owner | resolve in | default if unresolved |
|---|---|---|---|---|
| Q1 | Exact path of tonight's SPY/BTC handoff document that §7 is written against? | Multi-Horizon Momentum | T1 `## Sources` | Cite the path MHM used when staging the root; if none exists as a file, §7 rows map to Plan A / Plan B paths and `claim_map.md` says the handoff was verbal. |
| Q2 | Is the PDF's SPY 2022 −19% a calendar-year return or a peak-to-trough drawdown (A5)? | Multi-Horizon Momentum | T3 H2 | Report both from on-disk closes; label the PDF figure `DELTA — definitional` if it matches one and not the other. |
| Q3 | Can `mhm.py` apply per-asset caps (SPY 60–80%, BTC 7.5%) for H1 without modification? | Multi-Horizon Momentum | T3 H1 | If not, `NOT_REPRODUCIBLE` for the sized figure; show nearest uncapped books; no engine edit. |
| Q4 | Which window and ruleset does the PDF's "learned book" use (A4)? | Multi-Horizon Momentum | T3 (read §8 before running) | Use the PDF's stated window; if unstated, full window from BTC data start 2014-09-17 and say so. |
| Q5 | Is `proposals_stub.md` folded into `DECISION.md` or completed in place (S1)? | Multi-Horizon Momentum | T5 | Fold; leave stub with the `Superseded by DECISION.md` header. |
| Q6 | Which §9 opens need data not on disk, and should any be pre-approved as the next `plan_id`? | Planner | after T4, on reading `open_questions_ranked.md` | Rank only; mark `NEEDS_DATA`; no pre-approval in this plan. |
| Q7 | Is the RA pass a new `RA_deep.md` or an in-place expansion of `RA_intake_reply.md`? | Research Analyst | T2 | New `RA_deep.md`; intake reply untouched as the received record. |
| Q8 | Does the desk currently run any stop that the `## Stops` axis must compare against? | Multi-Horizon Momentum | T5 `## Stops` | State the current desk rule as read from `risk.md` (read-only); if none, the axis proposes "confirm no stop, note flats accepted". |
| Q9 | Post to Dominic after `REPORT.md` only, or earlier with `DECISION.md`? | Multi-Horizon Momentum | T6 | Once, after `REPORT.md`, with both paths; if asked earlier, send `DECISION.md` path and still finish T6. |

## Changelog

| version | date | brain | change |
|---|---|---|---|
| 1 | 2026-09-12 | fable-5.1 | In-depth draft. Six tasks (five MHM, one RA) mapped onto the staged root: fill `claim_map.md`; `RA_deep.md` from intake; `engine_verify.md` on fixed H1–H3 with definitional check for SPY 2022; `open_questions_ranked.md` for §9; `DECISION.md` on four axes with in-sample caveat absorbing `proposals_stub.md`; decision-complete `REPORT.md` + `README.md` index + post. Wave 1 parallel by 2026-09-13 10:00 UTC; `REPORT.md` by 2026-09-13 18:00 UTC. No PA/UW; no `risk.md` / universe / engine / skills edits; no parameter search. |
