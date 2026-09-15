# Plan: Agent context hygiene — inventory + classify standing context per roster agent, hygiene standard (terse · dated · owner · expiry) with hard desk boundaries, per-agent cleanup packets (ORCL/ADBE stand-down echoes out of daily loops, no cross-desk bleed), Planner verify + SUMMARY before/after

```
plan_id: 20260915-agent-context-hygiene
title: Agent context hygiene — inventory + classify standing context per roster agent, hygiene standard (terse · dated · owner · expiry) with hard desk boundaries, per-agent cleanup packets (ORCL/ADBE stand-down echoes out of daily loops, no cross-desk bleed), Planner verify + SUMMARY before/after
requester: Dominic (via Planner)
created: 2026-09-15
status: draft
brain: fable-5.1
depth: in-depth
version: 1
```

> **Execution state at plan time:** Wave 1 is partly done. The Planner has scanned every roster agent and the shared user-memory (seed below); PA has **already scrubbed** its own context and the record is on the desk at `/workspace/plans/20260915-agent-context-hygiene/inputs/PA_seed.md` — **PA is not redone**. Wave 2 is this plan. Approval is pre-given for invent → plan → delegate; Dominic is flagged **only** if a packet would delete anything beyond memory / routine / skill standing lines. Nothing here touches `/workspace/*/reports`. Tuesday 2026-09-15 is a live RTH session; routine and skill edits are held until the 20:00 UTC (16:00 ET) close so no agent's daily loop changes mid-session.

## Goal

Matches the GOAL in the brief. Maintain **terse, correct, live** context across all five roster agents — Planner, Price Action Analyst (PA), Research Analyst (RA), Multi-Horizon Momentum (MHM), UW — and remove context that is **irrelevant, non-terse, incorrect, or closed**.

Trigger: this morning's premarket injected the **finished ORCL/ADBE stand-down** as if it were live, and PA's memory carried **MHM bleed**. Two root causes, both addressed here: (1) closed decisions left as *standing* injections in daily loops; (2) cross-desk items held in the wrong agent's standing memory.

Five musts from the brief:

1. **Inventory** memory / routines / skills / user-memory per agent.
2. **Classify** every item `KEEP` / `ARCHIVE` (one dated log line, then forget standing) / `DELETE` (forget standing, no log).
3. **Hard desk boundaries** — PA ≠ MHM ≠ UW ≠ RA ≠ Planner; an agent's standing memory holds only its own desk.
4. **Standing hygiene standard** — every standing line is terse, dated, owned, and carries an expiry.
5. **Execute cleanup packets** per agent, each agent editing only its own context; **SUMMARY to Dominic before and after**.

Planner scan (seed, from the brief) — the starting inventory this plan completes:

| agent | seed finding | implied class |
|---|---|---|
| PA | scrubbed — see `inputs/PA_seed.md` | done; verify-only in T7 |
| Planner | episode log OK; `uso watch LIVE` keep; **stop echoing stand-downs into new plans** | LOG keep; MEM keep; TEMPLATE line rewrite |
| RA | Sep 10 routines scrubbed; **profile price-rule still names ORCL**; **log carries stand-down "default facts"** injected as standing | MEM/profile rewrite; standing injection forget; log lines stay |
| UW | no quick grep hits; **confirm alerts registry** | verify registry; forget any ORCL/ADBE alert |
| MHM | **confirm no PA DMs** | verify; forget any PA/TV coupling line |
| shared user-mem | no ORCL/ADBE; **keep PA trade prefs** | verify-only; no edits |

## Success criteria

Must (each has exactly one task):

| id | criterion | checked by | task |
|---|---|---|---|
| M1 | One inventory file per agent — `inputs/Planner_inventory.md`, `inputs/RA_inventory.md`, `inputs/UW_inventory.md`, `inputs/MHM_inventory.md`, `inputs/SHARED_usermem_inventory.md` — plus `inputs/PA_seed.md` referenced (not rewritten). Each row: `id`, `item` (verbatim or ≤ 120-char summary), `path`, `type ∈ {MEM, ROUTINE, SKILL, TEMPLATE, USERMEM, LOG}`, `owner`, `dated`, `class`, `action`, `reason`, `xdesk ∈ {Y, N}`. `inputs/INVENTORY.md` consolidates counts per agent × type × class. | files exist; every row has all ten columns filled; `INVENTORY.md` counts equal row counts | T1 |
| M2 | Every inventory row has `class ∈ {KEEP, ARCHIVE, DELETE, DOMINIC}` and a one-line `reason`. `DELETE` / `ARCHIVE` rows have `type ∈ {MEM, ROUTINE, SKILL, TEMPLATE}` only; any proposed removal of another type, or of anything under `/workspace/*/reports`, is `DOMINIC`. Every row with `xdesk = Y` is `ARCHIVE`, `DELETE`, or `KEEP` with `action = pointer` (one-line pointer to the owning desk). Every row mentioning `ORCL` or `ADBE` in a daily loop (`ROUTINE`, `SKILL`, `TEMPLATE`, or `MEM` read by a routine) is `ARCHIVE` or `DELETE`. | grep classes; grep `ORCL`/`ADBE` rows → class column; grep `xdesk = Y` rows → class/action | T1 |
| M3 | `outputs/HYGIENE_STANDARD.md` has a `## Boundaries` section: one row per agent with `owns` and `must not hold standing`, and the three fixed rules verbatim in intent — **MHM = research/backtest only; no PA TV coupling; no PA DMs**; **UW = cache + alerts registry only, no analysis text**; **Planner = plans / episodes / standards, no desk data, no stand-down echoes into new plan templates**. | grep section + five agent rows + `research/backtest only`, `TV`, `DMs` | T2 |
| M4 | `outputs/HYGIENE_STANDARD.md` has `## Standing line format` with the literal format `YYYY-MM-DD \| <owner> \| <item ≤ 120 chars> \| exp:<YYYY-MM-DD or standing>`, `## Rules` (terse, dated, owner, expiry, closed → log not standing, cross-desk → pointer at most, incorrect → forget same day, no symbol in a daily loop unless live in the universe), `## Lifecycle` (close → log line + forget within one session), `## Packet format`, `## DONE format`. | grep headings + format string + rule keywords | T2 |
| M5 | Cleanup packets issued: `outputs/CLEANUP_RA.md`, `outputs/CLEANUP_UW.md`, `outputs/CLEANUP_MHM.md`, `outputs/CLEANUP_Planner.md`, each in the `## Packet format` of the standard, every action row citing an inventory `id`, with `## Do not touch` (reports, logs, user-mem, other desks) and `## Return` (DONE path + deadline). `outputs/SUMMARY.md` `## Before` section written for Dominic: counts per agent × class, one line per `ARCHIVE` / `DELETE` item, `DOMINIC flags: none` or the flagged rows. | files exist; each action row's `id` resolves in the agent's inventory; `## Before` present with `DOMINIC flags:` line | T3 |
| M6 | RA executes `CLEANUP_RA.md`: profile price-rule rewritten symbol-agnostic (no `ORCL`, logic unchanged); stand-down default-fact standing injection forgotten; log entries untouched. `outputs/DONE_RA.md` lists every packet row as `done` / `skipped(<reason>)` / `DOMINIC` with before → after text, and ends with `ORCL: 0 · ADBE: 0 · xdesk: 0` over RA standing files. | file; grep `ORCL`/`ADBE` in RA standing paths from inventory = 0; log paths unchanged (mtime/hash) | T4 |
| M7 | UW executes `CLEANUP_UW.md`: alerts registry read and recorded (path + line count) or `registry: none`; any ORCL/ADBE standing alert forgotten; no UW analysis text in any other desk's standing files. `outputs/DONE_UW.md` per M6 shape. | file; `registry:` line; grep = 0 | T5 |
| M8 | MHM executes `CLEANUP_MHM.md`: `PA DMs: <n>` recorded (default 0); any PA / TV / live-trade coupling line forgotten or archived; MHM standing reads research/backtest only. `outputs/DONE_MHM.md` per M6 shape, ending `PA DMs: 0 · TV: 0 · ORCL: 0 · ADBE: 0`. | file; grep `PA DMs:`; grep `tv`/`tradingview`/`PA` in MHM standing paths = 0 (case-insensitive, whole-word) | T6 |
| M9 | Planner executes `CLEANUP_Planner.md` (`uso watch LIVE` kept verbatim; stand-down echo line removed from the new-plan template; episode log untouched) → `outputs/DONE_Planner.md`; then verifies **all five** agents by grep over every standing path in the inventories (reports and logs excluded) and writes `outputs/SUMMARY.md` `## After` + `## Verification` (grep commands, hit counts, residuals, next review date). | `DONE_Planner.md`; `## After`; `## Verification` shows `ORCL: 0`, `ADBE: 0`, cross-desk `0` for every agent or a named residual with owner | T7 |

Should:

| id | criterion | task |
|---|---|---|
| S1 | Each `DONE_*.md` carries `standing lines before: <n> / after: <m>` for the agent's `MEM` type, so terseness is measured, not asserted | T4, T5, T6, T7 |
| S2 | `HYGIENE_STANDARD.md` `## Cadence` — one-line weekly self-check per agent (Friday after close) and one Planner grep (Monday premarket); added to each agent as **one** standing line in the standard's format | T2 |
| S3 | `ARCHIVE` lines are written into the **agent's own log** as one dated `closed:` line, never into standing memory; `SUMMARY.md` `## After` indexes their paths | T4, T5, T6, T7 |
| S4 | `INVENTORY.md` records which memory stores the Planner could read directly and which it could not (agent-confirmed rows marked `src: agent`), so the next hygiene pass knows its blind spots | T1 |

## Out of scope

| item | why |
|---|---|
| **Redoing PA** | Brief: PA already scrubbed (`inputs/PA_seed.md`). PA is verified by grep in T7 only; no PA task, no PA edits. |
| **Anything under `/workspace/*/reports`** | Brief constraint. Reports are archives; grep hits there are not failures and never a `DELETE`. |
| Session history dirs (`/workspace/session-desk/session/YYYY-MM-DD/`) and dated log entries | Archives by nature. Only *standing* lines (memory, routine prompts, skill standing lines, session/plan templates) are targets. |
| Rewriting skill or routine **logic** | Only standing lines that echo dead work are edited; thresholds, gates, EV values untouched. |
| Reopening the ORCL/ADBE stand-down decision | Closed for trading context. This plan removes echoes; it does not revisit the decision or add either symbol anywhere. |
| Changes to `uso watch LIVE` or any live trade / watch item | Live context is `KEEP` by definition; S4-style regression check only. |
| Editing shared user-memory | Seed: no ORCL/ADBE; PA trade prefs kept. Verify-only (T1 inventory, T7 grep); any proposed edit is `DOMINIC`. |
| Mass-delete beyond memory / routine / skill / template standing lines | Brief: Dominic flag. Such rows are `DOMINIC`, held, and listed in `SUMMARY.md` `## Before`; nothing in this plan executes them. |
| An automated memory linter or tooling | Later `plan_id` if the manual cadence (S2) proves insufficient. |
| MHM engine, backtest artifacts, research trees | MHM's *standing memory* is in scope; its research outputs are not. |

## Constraints

Hard (from brief):

- **Reports are untouchable.** No packet row may name a path under `/workspace/*/reports`. `DELETE` and `ARCHIVE` are restricted to `type ∈ {MEM, ROUTINE, SKILL, TEMPLATE}`. Anything else proposed for removal → `class = DOMINIC`, row held, listed in `SUMMARY.md` `## Before`; the rest of the packet still executes (Q9).
- **Desk boundaries.** PA ≠ MHM ≠ UW ≠ RA ≠ Planner. A standing line belongs to exactly one desk. Cross-desk lines (`xdesk = Y`) leave the holder's standing memory; if the item is live, the owning desk already holds it (T7 verifies) and the holder keeps at most a one-line pointer.
- **MHM = research/backtest only.** No PA TV coupling, no PA DMs, no live-trade context in MHM standing memory.
- **ORCL/ADBE are closed for trading context.** Neither symbol appears in any standing daily loop (routine prompt, premarket list, price rule, alert, session template) after Wave 3. They may remain in reports and in dated `closed:` log lines.
- **Own-hand edits only.** Each agent forgets / rewrites its own memory, routines, skills. Planner edits only its own context plus the plan artifacts it owns (`HYGIENE_STANDARD.md`, `CLEANUP_*.md`, `SUMMARY.md`, inventories). Planner never writes into another agent's memory.
- **Terse.** Every standing line is one line, ≤ 120 chars, in the standard's format `YYYY-MM-DD | <owner> | <item> | exp:<date|standing>`. Prose paragraphs in standing memory are `DELETE` or rewritten to one line.
- **Approval.** Pre-given for invent → plan → delegate. `SUMMARY.md` `## Before` is **information** to Dominic, not a gate; Wave 3 proceeds unless a `DOMINIC` row exists, in which case only that row waits.
- **Named path stops.** Every step ends in a file at a named path under `/workspace/plans/20260915-agent-context-hygiene/`; "agent says done" is not a stop condition.

Soft:

- Effort units: S < 1h, M 1–3h.
- **No routine / skill edits during RTH.** Wave 3 execution starts at or after 20:00 UTC (16:00 ET) Tuesday 2026-09-15; Wave 4 closes by 02:00 UTC Wednesday 2026-09-16 (22:00 ET Tue) so Wednesday's premarket runs on clean context.
- Standing-line expiry default when none is natural: `exp:standing` plus a `review:` date 30 days out (Q5).
- Archive destination default: the agent's own log, one `closed:` line (Q4).
- `DOMINIC` also triggers when a single packet would forget more than 20 lines or more than half of an agent's `MEM` lines, even if every row is a standing type (Q9 default).

## Assumptions

| id | assumption | status | where handled |
|---|---|---|---|
| A1 | Each agent's memory, routine prompts, skill files, and session/plan templates exist as files on the desk that the Planner can **read**; the Planner scan in the seed came from such a read. Exact paths are not known to this brain and are **recorded per row in the inventories**, never invented here. | seed-implied | T1 (path column); Q1 |
| A2 | "Forget standing" is an operation only the **owning agent** performs on its own memory; Planner can read but not write others' memory. | brief ("each agent executes own forget") | T4–T7 ownership; Constraints |
| A3 | Shared user-memory is one store; seed says no ORCL/ADBE and PA trade prefs must stay. | seed | T1 `SHARED_usermem_inventory.md` (all `KEEP`); T7 grep; Q7 |
| A4 | `inputs/PA_seed.md` exists at the artifact root and is PA's completed inventory + DONE record in one; it names PA's standing paths so T7 can grep them. | brief | T1 references; T7 verify-only |
| A5 | RA's "profile price-rule" is one standing line (profile / MEM) naming ORCL as an example symbol; it can be rewritten symbol-agnostic (`session symbols`) without changing the rule's logic. | seed | T4; Q3 |
| A6 | RA's "stand-down default facts" are (a) dated log entries — archives, kept — and (b) a standing injection line that a routine reads each morning — the thing that fired this morning. Only (b) is forgotten. | seed + trigger | T1 classification; T4 |
| A7 | UW keeps an alerts registry (file or list) that UW can read and edit; the Planner's quick grep did not cover it. | seed ("confirm alerts registry") | T5; Q2 |
| A8 | MHM's standing memory may carry PA / TV references left from earlier plans (e.g., the `tv` prohibition lines, PA DMs); MHM can enumerate and forget them. | seed ("confirm no PA DMs") | T6; Q6 |
| A9 | The stand-down echo into new plans comes from a Planner **template** line (new-plan or session template), not from the episode log; the log is `KEEP`. | seed | T1; T7 own scrub |
| A10 | Tuesday 2026-09-15 is a live RTH session (EDT, UTC−4); Wednesday 2026-09-16 premarket routines start ≈ 11:00 UTC (07:00 ET). | calendar | Soft constraints; Sequence deadlines |
| A11 | "Fable" in the Sequence is this planning brain; Wave 2 is complete when `02_plan.md` and `02_plan.critique.md` exist and the Planner has produced the standard and packets (T2, T3). | brief | Sequence |
| A12 | Agents can report a `MEM` line count before and after their scrub (S1); if a store cannot be counted, the DONE file says `count: n/a`. | assumed | S1; T4–T7 |

## Context and inputs

Inputs already on the desk:

- `/workspace/plans/20260915-agent-context-hygiene/inputs/PA_seed.md` — PA scrub record (done).
- Planner scan (seed table in `## Goal`).
- Agent stores per A1: memory, routine prompts, skill files, session/plan templates, shared user-memory; paths recorded in T1.

Artifact root: `/workspace/plans/20260915-agent-context-hygiene/`

```
inputs/
  PA_seed.md                    (exists — not rewritten)
  Planner_inventory.md          T1
  RA_inventory.md               T1
  UW_inventory.md               T1
  MHM_inventory.md              T1
  SHARED_usermem_inventory.md   T1
  INVENTORY.md                  T1 (counts + src: planner|agent per store)
outputs/
  HYGIENE_STANDARD.md           T2
  CLEANUP_RA.md                 T3
  CLEANUP_UW.md                 T3
  CLEANUP_MHM.md                T3
  CLEANUP_Planner.md            T3
  SUMMARY.md                    T3 (## Before) → T7 (## After, ## Verification)
  DONE_RA.md                    T4
  DONE_UW.md                    T5
  DONE_MHM.md                   T6
  DONE_Planner.md               T7
```

Inventory row shape (all five `*_inventory.md`):

`| id | item | path | type | owner | dated | class | action | reason | xdesk |`

- `type ∈ {MEM, ROUTINE, SKILL, TEMPLATE, USERMEM, LOG}`; `class ∈ {KEEP, ARCHIVE, DELETE, DOMINIC}`; `action ∈ {none, rewrite, pointer, log+forget, forget, hold}`; `xdesk ∈ {Y, N}`.
- `ARCHIVE` ⇒ `action = log+forget`; `DELETE` ⇒ `forget`; `DOMINIC` ⇒ `hold`; `KEEP` ⇒ `none` / `rewrite` / `pointer`.

Timeline (UTC; ET in parentheses):

| when | what |
|---|---|
| 2026-09-15 ≤ 18:00 (14:00 ET) | T1 inventories complete |
| ≤ 19:00 (15:00 ET) | T2 `HYGIENE_STANDARD.md` |
| ≤ 20:00 (16:00 ET, close) | T3 packets + `SUMMARY.md` `## Before` → Dominic |
| 20:00–23:00 (16:00–19:00 ET) | T4 RA, T5 UW, T6 MHM execute; T7 Planner own scrub |
| ≤ 2026-09-16 02:00 (22:00 ET Tue) | T7 verify + `SUMMARY.md` `## After` → Dominic |
| 2026-09-16 ≈ 11:00 (07:00 ET) | Wednesday premarket runs on clean context (not a plan step) |

## Work breakdown

Seven tasks. Owners: Planner (T1, T2, T3, T7), Research Analyst (T4), UW (T5), Multi-Horizon Momentum (T6). PA has no task (done).

| task_id | task | owner | inputs | output | depends_on | effort |
|---|---|---|---|---|---|---|
| T1 | **Finish inventories + classify.** For Planner, RA, UW, MHM, shared user-mem: list every standing item (MEM, ROUTINE, SKILL, TEMPLATE, USERMEM) and the log stores (LOG) with path, owner, date; classify each `KEEP` / `ARCHIVE` / `DELETE` / `DOMINIC` with a one-line reason; mark cross-desk `xdesk`. Rows the Planner cannot read (UW alerts registry, MHM DMs) are entered as `src: agent`, class `KEEP?` pending confirmation in the agent's packet. Reference `PA_seed.md`; do not rewrite it. Consolidate counts. | Planner | Planner scan (seed); agent stores per A1; `inputs/PA_seed.md` | `inputs/Planner_inventory.md`, `inputs/RA_inventory.md`, `inputs/UW_inventory.md`, `inputs/MHM_inventory.md`, `inputs/SHARED_usermem_inventory.md`, `inputs/INVENTORY.md` | — | M |
| T2 | **Hygiene standard + boundaries.** Write the standing-line format, rules, lifecycle, boundaries table (five agents: owns / must not hold standing, with the MHM, UW, Planner fixed rules), cadence (S2), packet format, DONE format. One page; no prose beyond one line per rule. | Planner | brief constraints; T1 (which failure modes actually occurred) | `outputs/HYGIENE_STANDARD.md` | T1 | S |
| T3 | **Cleanup packets + SUMMARY before.** One packet per agent (RA, UW, MHM, Planner) in the standard's packet format: action rows citing inventory `id`, before text, required after text, `## Do not touch`, `## Return` (DONE path, deadline 23:00 UTC). Write `SUMMARY.md` `## Before`: counts per agent × class, one line per `ARCHIVE` / `DELETE`, `DOMINIC flags:` line, untouched list. Deliver to Dominic; delegate packets to agents at 20:00 UTC. | Planner | T1 inventories; T2 standard | `outputs/CLEANUP_RA.md`, `outputs/CLEANUP_UW.md`, `outputs/CLEANUP_MHM.md`, `outputs/CLEANUP_Planner.md`, `outputs/SUMMARY.md` (`## Before`) | T1, T2 | S |
| T4 | **RA executes packet.** Rewrite profile price-rule symbol-agnostic (no ORCL; logic unchanged); forget the stand-down default-fact standing injection; write one `closed:` log line for the stand-down (ARCHIVE); confirm Sep 10 routine scrub holds (no ORCL/ADBE in routine prompts); leave log entries and reports untouched. Record before → after per row. | Research Analyst | `outputs/CLEANUP_RA.md`; `inputs/RA_inventory.md`; `HYGIENE_STANDARD.md` | `outputs/DONE_RA.md` (+ RA's own memory / profile / routine files at their existing paths, listed in the DONE file) | T3 | S |
| T5 | **UW executes packet.** Read the alerts registry; record `registry: <path> · lines: <n>` or `registry: none`; forget any ORCL / ADBE standing alert (ARCHIVE line if it carried a decision, else DELETE); confirm no UW analysis text sits in another desk's standing files; confirm UW standing memory is cache + registry only. | UW | `outputs/CLEANUP_UW.md`; `inputs/UW_inventory.md`; alerts registry (A7) | `outputs/DONE_UW.md` (+ UW registry / memory at existing paths, listed) | T3 | S |
| T6 | **MHM executes packet.** Enumerate PA DMs and any PA / TV / live-trade coupling lines in MHM standing memory; record `PA DMs: <n>`; forget or archive each; confirm MHM standing reads research/backtest only; nothing ORCL/ADBE. | Multi-Horizon Momentum | `outputs/CLEANUP_MHM.md`; `inputs/MHM_inventory.md` | `outputs/DONE_MHM.md` (+ MHM memory at existing paths, listed) | T3 | S |
| T7 | **Planner own scrub + verify + SUMMARY after.** (a) Execute `CLEANUP_Planner.md`: keep `uso watch LIVE` verbatim; remove the stand-down echo line from the new-plan / session template; keep episode log; write `DONE_Planner.md`. (b) After T4–T6 DONE files land (or at 23:00 UTC), grep every standing path listed in all five inventories + `PA_seed.md` — excluding `/workspace/*/reports` and LOG paths — for `ORCL`, `ADBE`, `stand-down`/`stand down`, and per-desk cross terms (PA files: `MHM`, `backtest`; MHM files: `PA`, `TV`, `tradingview`, `DM`; UW files: analysis terms; RA files: `TV`, `MHM engine`). Write `## After` (per agent: done / skipped / DOMINIC, archive line paths, S1 counts) and `## Verification` (commands, hit counts, residuals with owner, next review date). Deliver to Dominic. | Planner | `outputs/CLEANUP_Planner.md`; `DONE_RA.md`, `DONE_UW.md`, `DONE_MHM.md`; all inventories; `PA_seed.md` | `outputs/DONE_Planner.md`; `outputs/SUMMARY.md` (`## After`, `## Verification`) | T3, T4, T5, T6 | M |

## Sequence

Planner → desk execution card. Deadlines UTC (ET in parentheses). Wave 1 finishes the inventory; Wave 2 is this plan plus the Planner's standard and packets; Wave 3 is own-hand execution after the close; Wave 4 is verification and the after-summary.

**Wave 1 — Tuesday 2026-09-15, during RTH (read-only): finish inventories**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 1a (T1) | Planner | `inputs/Planner_inventory.md`, `inputs/RA_inventory.md`, `inputs/UW_inventory.md`, `inputs/MHM_inventory.md`, `inputs/SHARED_usermem_inventory.md`, `inputs/INVENTORY.md` | six files exist; every row has ten columns filled; no `class` outside {`KEEP`, `ARCHIVE`, `DELETE`, `DOMINIC`, `KEEP?`}; `KEEP?` only on `src: agent` rows; every `ORCL` / `ADBE` row of type `ROUTINE` / `SKILL` / `TEMPLATE` / routine-read `MEM` is `ARCHIVE` or `DELETE`; every `xdesk = Y` row is `ARCHIVE` / `DELETE` / `KEEP`+`pointer`; no `DELETE` / `ARCHIVE` on `LOG` / `USERMEM` / reports paths; `INVENTORY.md` counts match; `PA_seed.md` referenced by path, unchanged (mtime) | 18:00 (14:00 ET) |

**Wave 2 — Tuesday, pre-close: plan (done) + standard + packets + SUMMARY before**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 2a (plan, not a task) | Planner (drafted by Fable) | `plans/20260915-agent-context-hygiene/02_plan.md`, `02_plan.critique.md` (scratchpad) → pasted by Planner to `/workspace/plans/20260915-agent-context-hygiene/` | both files exist at the desk path; critique shows 8/8 PASS; `status: draft` until Planner review, then `ready` in the Changelog | 19:00 (15:00 ET) |
| 2b (T2) | Planner | `outputs/HYGIENE_STANDARD.md` | headings `## Standing line format`, `## Rules`, `## Lifecycle`, `## Boundaries`, `## Cadence`, `## Packet format`, `## DONE format` present; format string literal present; five agent rows in Boundaries; strings `research/backtest only`, `TV`, `DMs`, `cache`, `stand-down` present; file ≤ 120 lines | 19:00 (15:00 ET) |
| 2c (T3) | Planner | `outputs/CLEANUP_RA.md`, `outputs/CLEANUP_UW.md`, `outputs/CLEANUP_MHM.md`, `outputs/CLEANUP_Planner.md`, `outputs/SUMMARY.md` | four packets exist; every action row's `id` resolves in that agent's inventory; each packet has `## Do not touch` naming `/workspace/*/reports`, logs, user-mem, other desks, and `## Return` naming its `DONE_*.md` path and `23:00 UTC`; `SUMMARY.md` has `## Before` with per-agent × class counts, one line per `ARCHIVE` / `DELETE`, and a `DOMINIC flags:` line (`none` or row ids); packets delegated at 20:00 UTC, not before | 20:00 (16:00 ET) |

**Wave 3 — Tuesday after close: own-hand execution**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 3a (T4) | Research Analyst | `outputs/DONE_RA.md` | every `CLEANUP_RA.md` row marked `done` / `skipped(<reason>)` / `DOMINIC`; price-rule row shows before (contains `ORCL`) → after (no `ORCL`, same rule logic); stand-down injection row `done` with the forgotten line quoted; one `closed:` log line path given; `standing lines before: n / after: m` (S1); last line `ORCL: 0 · ADBE: 0 · xdesk: 0`; lists RA standing paths edited | 23:00 (19:00 ET) |
| 3b (T5) | UW | `outputs/DONE_UW.md` | `registry: <path> · lines: <n>` or `registry: none`; each ORCL / ADBE alert row `done` or `none found`; line `other-desk files touched: 0`; S1 counts; last line `ORCL: 0 · ADBE: 0 · xdesk: 0` | 23:00 (19:00 ET) |
| 3c (T6) | Multi-Horizon Momentum | `outputs/DONE_MHM.md` | `PA DMs: <n>` line; each coupling row `done` with the forgotten line quoted or `none found`; S1 counts; last line `PA DMs: 0 · TV: 0 · ORCL: 0 · ADBE: 0` | 23:00 (19:00 ET) |
| 3d (T7a) | Planner | `outputs/DONE_Planner.md` | `uso watch LIVE` row `KEEP` with the line quoted verbatim before and after (identical); template echo row `done` with before → after; episode log row `KEEP`, path unchanged; S1 counts; last line `ORCL: 0 · ADBE: 0 · stand-down echoes: 0` | 23:00 (19:00 ET) |

**Wave 4 — Tuesday night: verify + SUMMARY after**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 4a (T7b) | Planner | `outputs/SUMMARY.md` (`## After`, `## Verification`) | `## After` has one block per agent (PA from `PA_seed.md`, verify-only) with done / skipped / DOMINIC counts, archive line paths, S1 counts; `## Verification` lists each grep command with hit count over standing paths (reports and LOG excluded): `ORCL 0`, `ADBE 0`, `stand-down 0`, cross-desk `0` per agent — or a named residual with owner and date; `next review:` date present; a missing DONE file at 23:00 UTC is recorded as `not returned` with the agent named, not silently skipped | 2026-09-16 02:00 (22:00 ET Tue) |

**Plan-level stop:** the plan closes when 4a's stop condition is met. Residuals named in `## Verification` become one standing line each in the owner's memory in the standard's format with `exp:` ≤ 7 days, and are re-grepped at the first S2 Monday check. A Wave 3 miss by any agent does not block the others; the after-summary names the miss. Nothing in any wave removes a file under `/workspace/*/reports`.

Owner-side rules for the card: own-hand edits only; reports untouchable; `DELETE`/`ARCHIVE` on standing types only; `DOMINIC` rows held, everything else proceeds; no routine/skill edits before 20:00 UTC; terse one-line standing format; ORCL/ADBE out of every daily loop; MHM research/backtest only; PA not redone.

## Definition of done

Checkable by listing files and grepping content under `/workspace/plans/20260915-agent-context-hygiene/` and the standing paths named in the inventories.

- [ ] `inputs/Planner_inventory.md`, `inputs/RA_inventory.md`, `inputs/UW_inventory.md`, `inputs/MHM_inventory.md`, `inputs/SHARED_usermem_inventory.md`, `inputs/INVENTORY.md` exist; every row has ten filled columns; `class` values only `KEEP` / `ARCHIVE` / `DELETE` / `DOMINIC` (no `KEEP?` remaining after Wave 3); no `DELETE` / `ARCHIVE` row has `type` `LOG` or `USERMEM` or a path containing `/reports/`.
- [ ] `inputs/PA_seed.md` unchanged (mtime before plan start).
- [ ] `outputs/HYGIENE_STANDARD.md` exists with the seven headings, the literal format string `YYYY-MM-DD | <owner> | <item ≤ 120 chars> | exp:<YYYY-MM-DD or standing>`, five Boundaries rows, and the strings `research/backtest only`, `TV`, `DMs`; ≤ 120 lines.
- [ ] `outputs/CLEANUP_RA.md`, `outputs/CLEANUP_UW.md`, `outputs/CLEANUP_MHM.md`, `outputs/CLEANUP_Planner.md` exist; every action `id` resolves; each has `## Do not touch` and `## Return`; no path under `/workspace/*/reports` appears in any action row.
- [ ] `outputs/SUMMARY.md` has `## Before` (with `DOMINIC flags:`), `## After`, `## Verification`, `next review:`.
- [ ] `outputs/DONE_RA.md`, `outputs/DONE_UW.md`, `outputs/DONE_MHM.md`, `outputs/DONE_Planner.md` exist with every packet row marked and the required last line; `DONE_UW.md` has `registry:`; `DONE_MHM.md` has `PA DMs:`; `DONE_Planner.md` quotes `uso watch LIVE` identical before/after.
- [ ] grep over all standing paths from the inventories + `PA_seed.md` (excluding `/reports/` and LOG paths): `ORCL` = 0, `ADBE` = 0, `stand-down` / `stand down` = 0; MHM standing: `PA`, `TV`, `tradingview`, `DM` = 0 (whole-word, case-insensitive); PA standing: `MHM`, `backtest` = 0 — or each residual named in `## Verification` with owner and expiry.
- [ ] Every standing `MEM` line in the four executed agents matches the standard's format (date · owner · item · `exp:`) — or is listed as a residual.
- [ ] No file under `/workspace/*/reports` deleted or modified (mtime sweep in `## Verification`).
- [ ] No TODO / TBD / FIXME in any output file.
- [ ] `02_plan.critique.md` in this scratchpad shows PASS on all eight checklist items (Planner).

## Open questions

None blocks Wave 1. Each has one roster owner, a place it is resolved, and a default.

| id | question | owner | resolve in | default if unresolved |
|---|---|---|---|---|
| Q1 | Exact on-disk roots for each agent's memory / routines / skills / templates? | Planner | T1 `path` column | As found by the Planner scan; recorded per row; nothing invented in this plan. |
| Q2 | Does the UW alerts registry hold ORCL / ADBE standing alerts, and where is it? | UW | T5 `registry:` line | If unreadable: `registry: none` recorded, nothing deleted, residual for Planner grep. |
| Q3 | RA price-rule rewrite: symbol-agnostic (`session symbols`) or name current live symbols? | Research Analyst | T4 before → after row | Symbol-agnostic; logic unchanged; no symbol list hard-coded in standing memory. |
| Q4 | Archive destination: agent's own log or a central archive file? | Planner | T2 `## Lifecycle` | Agent's own log, one dated `closed:` line; `SUMMARY.md` `## After` indexes the paths. |
| Q5 | Expiry for standing lines with no natural end (trade prefs, uso watch)? | Planner | T2 `## Rules` | `exp:standing` + `review:` 30 days out. |
| Q6 | Does MHM hold any PA DMs or TV coupling lines? | Multi-Horizon Momentum | T6 `PA DMs:` line | Expected 0; if > 0, forget each and quote it in `DONE_MHM.md`. |
| Q7 | May any shared user-mem line be edited in this plan? | Planner | T1 `SHARED_usermem_inventory.md`; T7 grep | No — all `KEEP`; any proposed edit is `DOMINIC`. |
| Q8 | Weekly cadence day for the self-check (S2)? | Planner | T2 `## Cadence` | Agents: Friday after close; Planner grep: Monday premarket. |
| Q9 | Does a `DOMINIC` row hold the whole packet or only that row? What counts as "mass-delete"? | Planner | T3 packets; `SUMMARY.md` `## Before` | Only the row is held; mass-delete = any non-standing type, or > 20 lines, or > 50% of an agent's `MEM` lines in one packet. |
| Q10 | Do PA's standing paths appear in `PA_seed.md` so T7 can grep them without a PA task? | Planner | T1 (reference row) | If absent, Planner greps PA's roots from the Q1 scan and notes `PA paths: from scan` in `## Verification`. |

## Changelog

| version | date | brain | change |
|---|---|---|---|
| 1 | 2026-09-15 | fable-5.1 | In-depth plan from the brief. Seven tasks — Planner (T1 inventories + classification; T2 hygiene standard + boundaries; T3 packets + SUMMARY before; T7 own scrub + verify + SUMMARY after), Research Analyst (T4), UW (T5), Multi-Horizon Momentum (T6); PA no task (already scrubbed, verify-only). Classes `KEEP` / `ARCHIVE` / `DELETE` / `DOMINIC`; `DELETE`/`ARCHIVE` restricted to MEM / ROUTINE / SKILL / TEMPLATE; reports untouchable; own-hand edits only; ORCL/ADBE out of every daily loop; MHM research/backtest only. Wave 1 read-only during RTH; Wave 3 after 20:00 UTC close; Wave 4 by 02:00 UTC 2026-09-16. Status `draft` — Planner review before paste. |
