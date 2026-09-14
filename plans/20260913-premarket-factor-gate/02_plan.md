# Plan: Premarket factor gate — weekday RTH factor pack F1–F10 beyond EV, `05_factor_gate.md` required before A++ cards arm, PA premarket + RA pre-market-brief + RA sd-plan updated, UW cache-only, Monday live

```
plan_id: 20260913-premarket-factor-gate
title: Premarket factor gate — weekday RTH factor pack F1–F10 beyond EV, 05_factor_gate.md required before A++ cards arm, PA premarket + RA pre-market-brief + RA sd-plan updated, UW cache-only, Monday live
requester: Dominic (session desk, via host Sequence)
created: 2026-09-13
status: ready
brain: fable-5.1
depth: in-depth
version: 1
```

> **Execution state at plan time:** the host Sequence for this work has **already been issued** and is executing tonight (Sunday 2026-09-13 ET). Dominic has authorized PA to update its skills and routines tonight, and the template `FACTOR_GATE.md` is already on the desk at `/workspace/session-desk/templates/FACTOR_GATE.md`. This plan **formalizes** that Sequence — same order (PA skill/routine + template dry-run → RA brief + sd-plan + stats → UW cache → Monday live), same file name (`05_factor_gate.md`), same owners — so the desk has a checkable card and a definition of done. It does not add steps, rename files, or change owners relative to the host Sequence. Nothing here lowers an EV gate.

## Goal

Matches the confirmed goal in the brief. Starting Monday 2026-09-14, every **weekday RTH** session carries a **premarket factor pack beyond EV**: ten factors F1–F10, read before the open by their owners, written into

`/workspace/session-desk/session/YYYY-MM-DD/05_factor_gate.md`

from the desk template. **A++ cards do not arm unless that file exists for today and carries an arm verdict.** Three routines change to make this real:

1. **PA premarket** — produces `05_factor_gate.md` from `templates/FACTOR_GATE.md` and fills the PA-owned factors (F1 regime/structure, F2 volume, F3 distance vs EM, F9 opposing zone).
2. **RA pre-market-brief** — fills the RA-owned factors (F4 base-rate n + setup, F5 UW GEX/DP/flow read **from the UW cache only, never pasted**, F6 event, F7 dual-stop **soft**, F8 IV/RV), with F5 written `na` — not a block — when the UW cache is missing or stale.
3. **RA sd-plan** — reads the gate, writes the F10 verdict (`No A++ / wait` → `GATE:WAIT`), and enforces the **hard rule: missing gate or `GATE:WAIT` → no A++ stored.**

UW's only role is **cache freshness** for F5. MHM is not involved. EV gates are unchanged; the factor pack sits **on top of** EV, it does not replace or loosen it.

Factor list (from the brief; owners fixed):

| id | factor | owner | hard / soft | when missing |
|---|---|---|---|---|
| F1 | regime / structure | PA | hard | gate incomplete → `GATE:WAIT` |
| F2 | volume | PA | hard | gate incomplete → `GATE:WAIT` |
| F3 | distance vs EM | PA | hard | gate incomplete → `GATE:WAIT` |
| F4 | base-rate `n` + setup | Research Analyst | hard | gate incomplete → `GATE:WAIT` |
| F5 | UW GEX / DP / flow | Research Analyst ← UW cache | hard when present; **cache-only, never paste** | UW cache missing/stale → `na`, **does not block** |
| F6 | event | Research Analyst | hard | gate incomplete → `GATE:WAIT` |
| F7 | dual-stop | Research Analyst | **soft** — never flips the verdict | row written `na`; does not block |
| F8 | IV / RV | Research Analyst | hard | gate incomplete → `GATE:WAIT` |
| F9 | opposing zone | PA | hard | gate incomplete → `GATE:WAIT` |
| F10 | No A++ / wait (verdict) | desk — written by the RA sd-plan step; Dominic may force `WAIT` | verdict line `GATE:ARM` / `GATE:WAIT` | file or verdict missing → treated as `GATE:WAIT` |

## Success criteria

Must (each has exactly one task):

| id | criterion | checked by | task |
|---|---|---|---|
| M1 | PA premarket skill + routine create `05_factor_gate.md` from `/workspace/session-desk/templates/FACTOR_GATE.md` and fill rows F1, F2, F3, F9, each with `read ∈ {PASS, FAIL}`, a `rule` cell stating the threshold applied, and a `source` cell; proven by a **dry-run** file tonight carrying the literal `DRY-RUN` in its header | dry-run file exists; grep `| F1 |`, `| F2 |`, `| F3 |`, `| F9 |` rows with `PASS`/`FAIL`; grep `DRY-RUN` | T1 |
| M2 | RA pre-market-brief fills rows F4, F5, F6, F7, F8 in the same file: F4 carries `n=` and the setup name and cites the on-disk stats path; F5's `source` is a UW **cache path + cache timestamp** (no pasted UW text) or the row reads `na` with reason `cache missing` / `cache stale`; F7 row contains the literal `soft`; proven in the dry-run file | grep rows; grep `n=` in F4; F5 `source` matches a path or row is `na`; F7 contains `soft`; no `paste` in F5 | T2 |
| M3 | RA sd-plan reads today's `05_factor_gate.md`, writes the F10 row with exactly one of `GATE:ARM` / `GATE:WAIT` per the verdict rule, and applies the **hard rule**: if the file is missing, incomplete, dated for another day, marked `DRY-RUN`, or reads `GATE:WAIT`, **zero cards are stored at grade `A++`**; proven by a dry-run in both branches (one forced `WAIT`, one `ARM`) | dry-run sd-plan output for the `WAIT` branch contains `GATE:WAIT` and no `A++` grade; `ARM` branch contains `GATE:ARM`; missing-file branch contains `gate missing` and no `A++` | T3 |
| M4 | UW cache for the session symbols (GEX, DP, flow) is refreshed before the RA brief cutoff Monday with a readable timestamp; UW does **not** paste anything into the brief or the gate | cache files' mtime ≤ cutoff; F5 `source` cell on Monday shows a cache timestamp; no UW-authored text in `05_factor_gate.md` | T4 |
| M5 | Monday 2026-09-14 live: PA premarket writes `/workspace/session-desk/session/2026-09-14/05_factor_gate.md` with header `date: 2026-09-14`, no `DRY-RUN`, rows F1, F2, F3, F9 filled by the PA cutoff | file + grep + mtime | T5 |
| M6 | Monday 2026-09-14 live: RA brief fills F4–F8 in that file by the brief cutoff; RA sd-plan writes F10 and applies the hard rule before RTH open; the sd-plan session output references the gate verdict and contains no `A++` if the verdict is `GATE:WAIT` | file + grep on `05_factor_gate.md` and the sd-plan session output | T6 |

Should:

| id | criterion | task |
|---|---|---|
| S1 | The dry-run file is kept (not deleted) under the Sunday session dir as the reference shape for the routines, and its header states `DRY-RUN — not a live gate` | T1 |
| S2 | F5 row includes cache age in minutes at read time and the `stale` threshold applied, so an `na` is auditable | T2 |
| S3 | sd-plan records held A++ candidates as `A++ candidate — HELD (GATE:WAIT)` (grade field not `A++`) rather than silently dropping them, so Monday's review can see what the gate withheld | T3 |
| S4 | Every EV threshold referenced by sd-plan is byte-identical before and after tonight's edits (diff of the sd-plan routine shows no change to EV values) | T3 |

## Out of scope

| item | why |
|---|---|
| **Lowering any EV gate** or re-tuning EV thresholds | Brief de-scope. The factor pack is *beyond* EV. S4 checks the EV values are untouched. |
| **Paste bridge** for UW data (any mechanism where UW output is pasted into a brief, gate, or chat) | Brief de-scope. F5 is cache-only; missing cache → `na`. |
| **MHM** — any task, engine run, or artifact | Brief de-scope. Roster for this plan is PA, Research Analyst, UW. |
| **Non-session symbols** — factors for anything outside the day's session universe | Brief de-scope. F-rows are per session symbol / setup only. |
| Weekend, holiday, or non-RTH gates | Gate is a weekday RTH premarket artifact. The Sunday file is a `DRY-RUN`, never a live gate. |
| Changing factor **definitions** or **owners** relative to the host Sequence | Plan formalizes; owners and F1–F10 are fixed by the brief. |
| Building a factor back-test, scoring model, or weighting scheme over F1–F10 | Verdict rule is a hard-factor AND (see Constraints); any weighting is a new `plan_id` after live data accumulates. |
| Renaming or renumbering session files | `05_factor_gate.md` is fixed; existing `01`–`04` session files are untouched. |
| Automating Dominic's `No A++ today` call | F10 accepts a manual force to `WAIT`; nothing forces `ARM`. |

## Constraints

Hard (from brief and host Sequence):

- Gate file path is exactly `/workspace/session-desk/session/YYYY-MM-DD/05_factor_gate.md`, created from `/workspace/session-desk/templates/FACTOR_GATE.md`. No other name.
- **Hard rule in sd-plan:** missing gate **or** `GATE:WAIT` → **no A++ stored**. "Missing" includes: file absent; any hard row (F1, F2, F3, F4, F6, F8, F9, and F5 unless `na`) blank or `pending`; header `date:` not equal to the session directory date; header contains `DRY-RUN`.
- **Verdict rule (F10):** `GATE:WAIT` if any hard row reads `FAIL` or is missing, or if Dominic has called `No A++ today`; otherwise `GATE:ARM`. F7 (`soft`) never changes the verdict. F5 `na` never changes the verdict.
- **F5 is cache-only, never paste.** The RA reads the UW cache on disk; the `source` cell is a cache path + cache timestamp. No UW screenshots, exports, or copied text enter any session file. UW's task is freshness only.
- **Missing UW = `na`, not block.** Cache absent or older than the stale threshold at read time → F5 `na` with reason; gate proceeds on F1–F4, F6, F8, F9.
- Owners only from {PA, Research Analyst, UW}. UW owns nothing but cache freshness. MHM appears nowhere.
- PA edits its own skills/routines tonight (authorized). RA edits pre-market-brief and sd-plan tonight. Edits to `FACTOR_GATE.md` are **additive only** (a field the routine needs that the template lacks) and logged in the template's own changelog line; anything else goes to Dominic.
- EV gates and their thresholds are not touched.
- Weekday RTH only. Monday 2026-09-14 is the first live session. All cutoffs in UTC with ET in parentheses (EDT = UTC−4).
- Every step ends in a named file path; "PA says done" / "RA says done" is not a stop condition.

Soft:

- Effort units: S < 1h, M 1–3h.
- Stale threshold for the UW cache: default 90 minutes at RA read time (Q3).
- Monday cutoffs (defaults, Q5): UW cache fresh 11:30 UTC (07:30 ET); RA brief rows 12:30 UTC (08:30 ET); PA rows 13:00 UTC (09:00 ET); sd-plan verdict + hard rule 13:15 UTC (09:15 ET); RTH open 13:30 UTC (09:30 ET). A missed cutoff leaves rows blank, which the hard rule reads as `GATE:WAIT` — the failure mode is **no A++**, never an unguarded A++.
- Tonight's dry-run cutoffs: PA by 02:00 UTC 2026-09-14 (22:00 ET Sun); RA by 04:00 UTC (00:00 ET).

## Assumptions

| id | assumption | status | where handled |
|---|---|---|---|
| A1 | `/workspace/session-desk/templates/FACTOR_GATE.md` exists and carries a header (`date:`), one row per F1–F10, and a verdict line. Planner cannot list the desk from this scratchpad repo. | brief says assume exists | T1 dry-run is the first read; a missing field is added additively (Constraints) and noted in the dry-run header. |
| A2 | Session directories follow `/workspace/session-desk/session/YYYY-MM-DD/` with numbered files; `05_` is free and `05_factor_gate.md` is the name the host Sequence issued. | brief-confirmed | All paths; no other session file renamed. |
| A3 | The UW cache (GEX, DP, flow per session symbol) lives at a fixed on-disk location known to UW and RA, with file mtimes or an embedded timestamp usable as the freshness stamp. | assumed | T4 refreshes; T2 reads and writes cache path + timestamp into F5 `source`; path recorded there (Q3). |
| A4 | The arm token is `GATE:ARM`; the wait token `GATE:WAIT` is given by the brief. | `WAIT` confirmed; `ARM` assumed | T1 confirms against the template; if the template uses a different arm token, the routines use the template's token and the dry-run header records it (Q1). |
| A5 | Row ownership makes write order irrelevant: PA writes only F1, F2, F3, F9; RA writes only F4–F8; sd-plan writes only F10. Whichever of PA / RA runs first creates the file from the template; the other fills its rows in place. sd-plan always runs last. | design assumption | T1, T2 file-handling rule; Q2. |
| A6 | Thresholds for each factor (what `PASS` means for F1–F9) are the owners' current premarket heuristics, written into the `rule` cell per row so they are auditable; this plan does not set numeric thresholds. | assumed | M1, M2 `rule` cell requirement; Q4. |
| A7 | The Sunday dry-run is written to `/workspace/session-desk/session/2026-09-13/05_factor_gate.md` with `DRY-RUN` in the header; sd-plan's hard rule treats any `DRY-RUN` file as missing, so it can never arm Monday. | design assumption | T1, T3; Q6. |
| A8 | sd-plan already has a card grade field with `A++` as the top grade and an existing session output file under the session dir; this plan changes the storing rule, not the file name. | assumed from brief wording ("A++ cards", "stored") | T3, T6; Q7. |
| A9 | F3 "distance vs EM" uses the expected move PA already computes or reads in its premarket routine; no new data feed is needed. | assumed | T1 `source` cell names where EM came from. |
| A10 | F4 `n` comes from RA's existing stats table extended tonight to expose `n` per setup; no new back-test. | brief ("RA … stats") | T2 output includes the stats path in F4 `source`. |
| A11 | Dominic's `No A++ today` call reaches sd-plan through an existing desk channel (a line in the session dir or a direct instruction to RA); sd-plan writes `GATE:WAIT` with reason `Dominic: No A++`. | assumed | T3 rule; Q8. |
| A12 | Monday 2026-09-14 is a normal US trading day (no holiday); EDT offset UTC−4 applies. | calendar fact | Monday cutoffs. |

## Context and inputs

Desk today: the session desk grades setups into cards; `A++` is the top grade and arms at RTH open subject to the EV gate. Tonight's change inserts a second, factor-based gate **in front of** A++ arming without touching EV.

Existing routines touched (paths are the desk's existing skill/routine files; this plan does not rename them):

| routine | owner | change | proof |
|---|---|---|---|
| PA premarket skill + routine | PA | create `05_factor_gate.md` from template; fill F1, F2, F3, F9 with `read`, `rule`, `source` | dry-run file tonight; live file Monday |
| RA pre-market-brief | Research Analyst | fill F4–F8 in `05_factor_gate.md`; F5 cache-only with `na` rule; F7 `soft` | dry-run file tonight; live file Monday |
| RA stats | Research Analyst | expose `n` per setup for F4 | F4 `source` path resolves; row carries `n=` |
| RA sd-plan | Research Analyst | read gate; write F10; hard rule; `HELD` note (S3) | dry-run both branches tonight; live Monday |
| UW cache | UW | fresh by 11:30 UTC Monday; freshness only | mtime; F5 `source` timestamp |

Gate file shape (per template; the dry-run confirms):

- Header: `date: YYYY-MM-DD`, `session: RTH`, `mode: LIVE | DRY-RUN`, `template: /workspace/session-desk/templates/FACTOR_GATE.md`.
- Table: one row per F1–F10 with columns `id`, `factor`, `owner`, `read` (`PASS` / `FAIL` / `na`), `rule`, `value`, `source`, `note`; F7's `read` cell carries `soft`.
- Verdict line: F10 row `read` = `GATE:ARM` or `GATE:WAIT`, with `reason` listing the failing/missing hard rows or `Dominic: No A++`.
- Footer: `## Sources` — paths only (stats file, UW cache files, PA chart/level source).

Inputs already on the desk: `templates/FACTOR_GATE.md` (A1); session symbol list for the day; PA levels / EM; RA stats table; UW cache (A3); EV gate as-is.

Timeline (UTC; ET in parentheses):

| when | what |
|---|---|
| 2026-09-14 00:00–02:00 (Sun 20:00–22:00 ET) | T1 PA skill/routine edit + dry-run |
| 02:00–04:00 (22:00–00:00 ET) | T2 RA brief + stats; T3 RA sd-plan; both dry-run against the T1 file |
| 2026-09-14 ≤ 11:30 (≤ 07:30 ET) | T4 UW cache fresh |
| 11:30–12:30 (07:30–08:30 ET) | T6 step: RA brief fills F4–F8 live |
| ≤ 13:00 (≤ 09:00 ET) | T5 PA fills F1, F2, F3, F9 live |
| ≤ 13:15 (≤ 09:15 ET) | T6 step: sd-plan writes F10, applies hard rule |
| 13:30 (09:30 ET) | RTH open — A++ arms only on `GATE:ARM` |

## Work breakdown

Six tasks. Owners: PA (T1, T5), Research Analyst (T2, T3, T6), UW (T4). No MHM.

| task_id | task | owner | inputs | output | depends_on | effort |
|---|---|---|---|---|---|---|
| T1 | **PA premarket skill/routine + template dry-run.** Update the PA premarket skill and routine to: create `05_factor_gate.md` from the template if absent (else open it); fill F1 regime/structure, F2 volume, F3 distance vs EM, F9 opposing zone with `read`, `rule`, `value`, `source`; write header `date:` and `mode:`; never touch F4–F8 or F10. Run once tonight as a `DRY-RUN` into the Sunday session dir. Additive template fixes only, logged. | PA | `/workspace/session-desk/templates/FACTOR_GATE.md`; PA premarket skill + routine; Sunday levels / EM as sample data | `/workspace/session-desk/session/2026-09-13/05_factor_gate.md` (header `mode: DRY-RUN`) + updated PA skill/routine files (existing paths, listed in the dry-run header) | — | M |
| T2 | **RA pre-market-brief + stats.** Update the brief routine to fill F4 base-rate (`n=`, setup, stats path), F5 UW GEX/DP/flow **from cache only** (`source` = cache path + timestamp; `na` + reason if missing or older than the stale threshold), F6 event, F7 dual-stop tagged `soft`, F8 IV/RV; create the file from the template if PA has not yet (A5); never touch F1–F3, F9, F10. Extend the RA stats table to expose `n` per setup. Dry-run into the T1 file. | Research Analyst | T1 dry-run file (row shape); RA stats table; UW cache (A3); event calendar; IV/RV source | same dry-run file with F4–F8 filled + updated brief routine + stats table (existing paths; stats path in F4 `source`) | T1 | M |
| T3 | **RA sd-plan hard rule.** Update sd-plan to: locate today's `05_factor_gate.md` by session date; validate header (`date:` matches dir; `mode:` not `DRY-RUN`); check all hard rows present; compute F10 per the verdict rule; write the F10 row with `GATE:ARM` / `GATE:WAIT` + reason; if missing / incomplete / `WAIT` → store no card at `A++`, record candidates as `A++ candidate — HELD (GATE:WAIT)` (S3); leave EV values untouched (S4). Dry-run three branches against copies of the T1/T2 file: forced `WAIT`, forced `ARM`, file absent. | Research Analyst | T1/T2 dry-run file; sd-plan routine; existing sd-plan session output format (A8) | updated sd-plan routine (existing path) + dry-run evidence appended to the Sunday file under `## sd-plan dry-run` (three branch results with the literal outcome strings) | T1 | M |
| T4 | **UW cache freshness for Monday.** Refresh GEX, DP, and flow cache for the session symbols before 11:30 UTC (07:30 ET) Monday; ensure each cache file exposes a timestamp RA can read; **write nothing** into the brief or gate. | UW | session symbol list; UW cache location (A3) | UW cache files at their existing path, mtime ≤ 11:30 UTC 2026-09-14 (path + timestamp surfaced in F5 `source` by T6) | — | S |
| T5 | **Monday live — PA rows.** Run the updated PA premarket routine live: create `/workspace/session-desk/session/2026-09-14/05_factor_gate.md` from the template (or open it if RA created it first), header `date: 2026-09-14`, `mode: LIVE`; fill F1, F2, F3, F9 by 13:00 UTC (09:00 ET). | PA | T1 routine; Monday levels, EM, premarket volume | `/workspace/session-desk/session/2026-09-14/05_factor_gate.md` (F1, F2, F3, F9 rows) | T1 | S |
| T6 | **Monday live — RA rows, verdict, hard rule.** Run the updated brief: fill F4–F8 by 12:30 UTC (08:30 ET), F5 from the T4 cache or `na`. Run the updated sd-plan by 13:15 UTC (09:15 ET): write F10, apply the hard rule, store cards accordingly; sd-plan session output references the gate verdict. | Research Analyst | T2 brief routine; T3 sd-plan routine; T4 cache; T5 file | `/workspace/session-desk/session/2026-09-14/05_factor_gate.md` (F4–F8, F10 rows) + sd-plan session output under `/workspace/session-desk/session/2026-09-14/` (existing file name, A8) | T2, T3, T4, T5 | S |

## Sequence

Planner → desk execution card, matching the host Sequence already issued (PA skill/routine + template dry-run → RA brief + sd-plan + stats → UW cache → Monday live). Deadlines UTC (ET in parentheses). Wave 0 is tonight; Wave 1 is Monday premarket; the plan closes at RTH open.

**Wave 0 — tonight (Sunday 2026-09-13 ET): routines + dry-run**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 0a (T1) | PA | `/workspace/session-desk/session/2026-09-13/05_factor_gate.md` | file exists; header has `date: 2026-09-13`, `mode: DRY-RUN`, `template: /workspace/session-desk/templates/FACTOR_GATE.md`, and the paths of the edited PA skill/routine files; rows `F1`, `F2`, `F3`, `F9` each have `read` ∈ {`PASS`, `FAIL`}, a non-empty `rule`, a non-empty `source`; rows F4–F8, F10 untouched (template placeholders); any additive template edit is named in the header | 2026-09-14 02:00 (22:00 ET Sun) |
| 0b (T2) | Research Analyst | same file (F4–F8) + RA stats table at its existing path | rows `F4`–`F8` filled; `F4` contains `n=` and a stats path that exists; `F5` `source` is a cache path + timestamp **or** `read` = `na` with `cache missing` / `cache stale` and age; `F7` `read` cell contains `soft`; no pasted UW text anywhere in the file; the file's `## Sources` lists the stats path and the cache path (or states `UW cache: none`) | 2026-09-14 04:00 (00:00 ET) |
| 0c (T3) | Research Analyst | same file, section `## sd-plan dry-run` + sd-plan routine at its existing path | three branch lines present: `WAIT branch: GATE:WAIT — A++ stored: 0 — HELD: <k>`; `ARM branch: GATE:ARM — A++ eligible`; `MISSING branch: gate missing — A++ stored: 0`; sd-plan routine diff shows no change to any EV threshold value (S4); the routine rejects `mode: DRY-RUN` files as missing | 2026-09-14 04:00 (00:00 ET) |

**Wave 1 — Monday 2026-09-14 premarket: live**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 1a (T4) | UW | UW cache files at their existing path | GEX, DP, flow present for every session symbol; each file mtime (or embedded timestamp) ≤ 11:30 UTC 2026-09-14; UW has written nothing under `/workspace/session-desk/session/2026-09-14/` | 11:30 (07:30 ET) |
| 1b (T6, brief) | Research Analyst | `/workspace/session-desk/session/2026-09-14/05_factor_gate.md` (F4–F8) | rows F4–F8 filled per 0b's conditions; F5 `source` shows the 1a cache timestamp or `na` with reason | 12:30 (08:30 ET) |
| 1c (T5) | PA | `/workspace/session-desk/session/2026-09-14/05_factor_gate.md` (F1, F2, F3, F9) | header `date: 2026-09-14`, `mode: LIVE`; rows F1, F2, F3, F9 filled per 0a's conditions | 13:00 (09:00 ET) |
| 1d (T6, sd-plan) | Research Analyst | same file (F10) + sd-plan session output under `/workspace/session-desk/session/2026-09-14/` | F10 row has exactly one of `GATE:ARM` / `GATE:WAIT` with a reason; sd-plan output contains the same token; if `GATE:WAIT` (or any row missing at 13:15), the output contains no card at grade `A++` and lists held candidates as `HELD (GATE:WAIT)` | 13:15 (09:15 ET) |

**Plan-level stop:** the plan closes when 1d's stop condition is met at or before 13:30 UTC (09:30 ET) Monday 2026-09-14. From Tuesday the gate is a routine, not a plan step. A Wave 0 miss does not loosen anything: sd-plan without an updated routine cannot read a gate, and the brief's rule is that **no gate → no A++** — the desk trades at most A+ until the gate is in place. A Wave 1 miss (any cutoff) resolves to `GATE:WAIT` by the hard rule.

Owner-side rules for the card: F5 cache-only, never paste; F7 soft; missing UW = `na`, not block; no EV threshold changes; session symbols only; `05_factor_gate.md` is the only new session file; MHM not involved; only Dominic can call `No A++ today`, and nothing can force `ARM`.

## Definition of done

Checkable by listing files and grepping content under `/workspace/session-desk/`.

- [ ] `/workspace/session-desk/session/2026-09-13/05_factor_gate.md` exists; header contains `mode: DRY-RUN` and `template: /workspace/session-desk/templates/FACTOR_GATE.md`; rows `| F1 |` … `| F10 |` all present; F1, F2, F3, F9 `read` ∈ {`PASS`, `FAIL`}; F4 contains `n=`; F5 `source` contains a path or `read` = `na`; F7 contains `soft`; no `TODO` / `TBD` / `FIXME`; no string `paste`; `## Sources` present.
- [ ] Same file has section `## sd-plan dry-run` with three lines containing respectively `GATE:WAIT` + `A++ stored: 0`, `GATE:ARM`, and `gate missing` + `A++ stored: 0`.
- [ ] PA premarket skill + routine files named in the dry-run header exist and reference `05_factor_gate.md` and `FACTOR_GATE.md`.
- [ ] RA pre-market-brief routine references `05_factor_gate.md`, `na`, and the UW cache path; RA sd-plan routine references `05_factor_gate.md`, `GATE:WAIT`, `DRY-RUN`, and contains the hard rule (no `A++` when missing / `WAIT`); a diff of sd-plan against its pre-edit version shows no EV threshold value changed.
- [ ] `/workspace/session-desk/templates/FACTOR_GATE.md` has at most additive changes, each named in the dry-run header.
- [ ] UW cache files for every Monday session symbol have mtime (or embedded timestamp) ≤ 2026-09-14 11:30 UTC; no file under `/workspace/session-desk/session/2026-09-14/` is authored by UW.
- [ ] `/workspace/session-desk/session/2026-09-14/05_factor_gate.md` exists; header `date: 2026-09-14`, `mode: LIVE`, no `DRY-RUN`; rows F1–F9 filled per M1/M2; F10 `read` is exactly one of `GATE:ARM` / `GATE:WAIT` with a reason; file mtime ≤ 13:15 UTC.
- [ ] sd-plan session output for 2026-09-14 contains the same `GATE:` token as F10; if `GATE:WAIT`, it contains no card at grade `A++` and, where candidates existed, the string `HELD (GATE:WAIT)`.
- [ ] No EV gate value changed; no file created for a non-session symbol; no MHM artifact referenced.
- [ ] `02_plan.critique.md` in this scratchpad shows PASS on all eight checklist items (Planner).

## Open questions

None blocks Wave 0. Each has one roster owner, a place it is resolved, and a default.

| id | question | owner | resolve in | default if unresolved |
|---|---|---|---|---|
| Q1 | Does `FACTOR_GATE.md` already define the arm token, and is it `GATE:ARM`? | PA | T1 dry-run header | Use the template's token; if none, `GATE:ARM`, added additively and logged. |
| Q2 | When both PA and RA find no file, who creates it from the template? | PA | T1 / T2 routines | Whichever runs first creates; the other opens in place; each writes only its own rows (A5). |
| Q3 | Exact UW cache path and the stale threshold for F5? | UW (path), Research Analyst (threshold) | T4 (path surfaced), T2 (threshold in F5 `rule`) | Path as UW reports it; stale = older than 90 min at RA read time → `na`. |
| Q4 | Numeric `PASS` thresholds for F1–F9? | PA (F1, F2, F3, F9), Research Analyst (F4–F8) | `rule` cell per row, tonight | Owners' current premarket heuristics, stated per row; no threshold set by this plan; revisit after live weeks as a new `plan_id`. |
| Q5 | Monday cutoffs as defaulted (11:30 / 12:30 / 13:00 / 13:15 UTC) acceptable to all three owners? | Research Analyst | T3 sd-plan (encodes the 13:15 read) | Defaults stand; a missed cutoff resolves to `GATE:WAIT`. |
| Q6 | Dry-run location: Sunday session dir `2026-09-13` (default) or elsewhere? | PA | T1 | Sunday dir with `mode: DRY-RUN`; sd-plan rejects `DRY-RUN` as missing. |
| Q7 | Name of the existing sd-plan session output file that stores cards (this plan does not rename it)? | Research Analyst | T3 `## sd-plan dry-run` line | Keep the existing name; the dry-run section states it. |
| Q8 | Channel for Dominic's `No A++ today` call into sd-plan? | Research Analyst | T3 | A line Dominic (or RA on Dominic's instruction) writes into `05_factor_gate.md` F10 `note`: `Dominic: No A++` → `GATE:WAIT`. |
| Q9 | Does F5 `FAIL` (cache present, flow strongly opposing) block like other hard factors? | Research Analyst | T2 F5 `rule` cell | Yes — `FAIL` blocks; only `na` (missing/stale cache) is non-blocking, per brief. |
| Q10 | Is F6 `event` a `FAIL` for any scheduled high-impact event inside RTH, or only within a window around the entry? | Research Analyst | T2 F6 `rule` cell | RA's current brief convention, stated in the `rule` cell. |

## Changelog

| version | date | brain | change |
|---|---|---|---|
| 1 | 2026-09-13 | fable-5.1 | In-depth formalization of the already-executing host Sequence. Six tasks — PA (T1 skill/routine + template dry-run; T5 Monday PA rows), Research Analyst (T2 brief + stats; T3 sd-plan hard rule; T6 Monday RA rows + verdict), UW (T4 cache freshness only). Factor pack F1–F10 with fixed owners; F7 soft; F5 cache-only, never paste, `na` when missing; F10 verdict `GATE:ARM` / `GATE:WAIT`; hard rule missing gate or `GATE:WAIT` → no A++ stored. File `05_factor_gate.md` under `/workspace/session-desk/session/YYYY-MM-DD/` from `templates/FACTOR_GATE.md`. Wave 0 dry-run tonight (Sunday dir, `DRY-RUN`); Wave 1 Monday 2026-09-14 live, closes at 13:30 UTC. De-scoped: EV gate lowering, paste bridge, MHM, non-session symbols. Status `ready` — Dominic has authorized execution. |
