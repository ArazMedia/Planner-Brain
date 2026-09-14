# Plan: USO call-sale insight — covered vs naked vs call credit spread against the open bullish thesis, strike/expiry candidates off PA supply zones + UW GEX cache, IV/skew read, kill list, FOMC/BOJ window handling, optional standing watch; proposals only, REPORT by Tue 07:30 ET

```
plan_id: 20260914-uso-call-sale
title: USO call-sale insight — covered vs naked vs call credit spread against the open bullish thesis, strike/expiry candidates off PA supply zones + UW GEX cache, IV/skew read, kill list, FOMC/BOJ window handling, optional standing watch; proposals only, REPORT by Tue 07:30 ET
requester: Dominic (via Research Analyst)
created: 2026-09-14
status: draft
brain: fable-5.1
depth: in-depth
version: 1
```

> **Execution state at plan time:** Planner has **already sent** intake questions to the Price Action Analyst (supply zones + screenshots) and to UW (GEX / DP / flow / OI cache for USO). This plan sequences around those two artifacts: Wave 1 waits for them (and runs the Research Analyst's independent reads in parallel), Wave 2 turns them into strike/expiry candidates and a kill list, Wave 3 is the RA synthesis `REPORT.md`. Everything produced is **insight + proposals**. No task edits the USO thesis, `risk.md`, any routine, or any skill. The optional standing watch (T7) is a **proposal document**, not a routine change.

## Goal

Dominic wants a direct answer on **selling calls on USO** while the desk's USO bullish thesis is **open** (invalidation: daily close under 134.34–136.57). The motive is yield / overextension — WTI ~103+ intraday today, oil and geo hot (pipeline shut; Hormuz diplomacy postponed), the Dec 150 long call already exited Sep 10 for +$762, desk now flat on that call. The tension is obvious and is the point of the work: a short call is upside exposure sold against a thesis that says upside. The deliverable is not a lecture about that tension; it is the set of **structures and paths** that make a call sale coherent with the thesis, the levels and expiries that make it concrete, and the named conditions that kill it.

Eight things must be in the RA `REPORT.md`, each traceable to a task:

1. **Call-sale vs thesis** — covered vs naked vs call credit spread; **when each is the path** (keyed on shares held, account type, thesis state, distance to supply, IV/skew, event window). Defined-risk language preferred wherever naked is cash-account awkward.
2. **Strike / expiry candidates** — a short table, each row with expiry, short strike (and long strike for the spread), delta, credit, max loss, distance to the referenced PA zone, buffer in expected moves, yield on collateral.
3. **IV / skew read** — IV30, IV rank / percentile, IV vs realized, term structure across Sep 18 / Oct 16 / Nov 20 / Dec 18, 25Δ call-vs-put skew, OVX context; verdict token.
4. **PA supply zones as short-call reference levels** — PA-owned; zones above spot with distance in $ and ATR; screenshots; PA writes no fundamentals.
5. **UW GEX / flow / OI** — UW caches; RA reads the cache and writes its own read with cache path + timestamp; **never pasted** to Dominic.
6. **What kills the idea** — named kill conditions K1–K10 with the signal owner and the check, plus the post-entry management rule (close / roll) stated as a path, not a warning.
7. **Event-window handling** — FOMC Wednesday 2026-09-16, BOJ 2026-09-17/18, EIA Wednesday, Sep 18 monthly opex; entry paths `ENTER-PRE` / `ENTER-BETWEEN` / `ENTER-POST` / `NO-ENTRY`; Sep 18 expiry excluded as a sale candidate.
8. **Optional standing watch** — if the REPORT's verdict is "not now, but conditions could form," a one-page watch proposal (cadence, checks, GO/HOLD token, file path) for Dominic to approve.

## Success criteria

Must (each has exactly one task):

| id | criterion | checked by | task |
|---|---|---|---|
| M1 | `pa_zones.md` exists with ≥ 2 supply zones **above spot** (each: `zone_id`, timeframe, low, high, type, distance from spot in $ and in ATR14, times tested, screenshot path) plus a restated invalidation row `134.34–136.57`, spot + timestamp of the read, ATR14 value, and PA's own overextension read (distance from 20EMA in ATR); screenshots exist under `outputs/screenshots/`; the file contains **no fundamentals tokens** (`Hormuz`, `pipeline`, `FOMC`, `BOJ`, `OPEC`, `inventor`, `WTI`, `geo`) | file + grep rows; `ls outputs/screenshots/`; negative grep | T1 |
| M2 | UW cache for USO (GEX by strike for Oct 16, Nov 20 and all-expiry aggregate incl. net GEX sign, call wall, put wall, zero-gamma; DP prints last 5 sessions; flow last 5 sessions incl. net call premium and sweeps at strikes above spot; OI by strike for Oct 16 / Nov 20) is fresh at the UW cache location, and `uw_cache_index.md` lists **paths + timestamps + field names only** — no values, no exports, no images; UW writes nothing else under `outputs/` | index file; each listed path exists with mtime ≤ cutoff; index has no numeric strike/gamma values | T2 |
| M3 | `ra_iv_skew.md` carries IV30, IV rank and IV percentile (252d), IV30 / RV20 ratio, ATM IV per expiry (Sep 18, Oct 2, Oct 9, Oct 16, Nov 20, Dec 18), 25Δ risk reversal (call IV − put IV) for Oct 16 and Nov 20, OVX level and 20d change, expected move (1σ) to Oct 16 and Nov 20 in $, and a verdict line with exactly one of `VOL:SELL-FAVORABLE` / `VOL:NEUTRAL` / `VOL:SELL-UNFAVORABLE` with the rule applied | file + grep tokens; each number carries a source (chain read timestamp or on-disk path) | T3 |
| M4 | `ra_structure.md` has one section per structure (`## Covered call`, `## Naked call`, `## Call credit spread`) each stating: thesis relationship (aligned / neutral-tactical / opposed), what it needs (shares / margin level / nothing), when it is **the path** (decision table), how it is managed (close / roll rule), and the cash-account substitute where relevant; a `## Path decision table` keyed on shares × account × thesis state × distance-to-zone × vol verdict; a `## Event window` section with FOMC / BOJ / EIA / opex timestamps in UTC + ET, the four entry tokens defined, Sep 18 excluded as a sale expiry with reason, and the USD channel stated in ≤ 3 lines; `proposals only` present; no instruction to edit the thesis or `risk.md` | file + headings + grep | T4 |
| M5 | `ra_candidates_kills.md` has `## Candidates` (≥ 3 rows, ≤ 6; columns: `id`, `structure`, `expiry`, `short`, `long`, `Δ`, `credit`, `max_loss`, `zone_ref`, `dist_$`, `buffer_EM`, `yield`, `gex_ref`; every `zone_ref` is a `zone_id` from `pa_zones.md` or `na`; every `gex_ref` cites a cache path from `uw_cache_index.md` or `na`) and `## Kills` (K1–K10 each with signal owner, check, current state `ARMED` / `CLEAR` / `na`, and the value that set it); one `## Management` section with the close / roll rule as a path; `## Sources` | file + grep; cross-check `zone_id`s against T1; cross-check cache paths against T2 | T5 |
| M6 | `REPORT.md` is decision-complete: `## Verdict` (one paragraph; exactly one of `PATH:COVERED` / `PATH:SPREAD` / `PATH:NAKED` / `PATH:NONE`; exactly one of `ENTER-PRE` / `ENTER-BETWEEN` / `ENTER-POST` / `NO-ENTRY`; exactly one of `WATCH:RECOMMEND` / `WATCH:NO`), `## Structure paths`, `## Candidates`, `## IV/skew read`, `## PA zones` (zone table + screenshot paths), `## UW read` (RA prose ≤ 8 lines + cache path + timestamp; no image, no code block, no UW export), `## Kills`, `## Event window`, `## Watch`, `## Compliance`, `## Verification`, `## Sources`; last line is the post reference to Dominic | file + headings + token counts + post reference | T6 |

Should:

| id | criterion | task |
|---|---|---|
| S1 | `ra_structure.md` includes a `## Variants` note (≤ 6 lines) on the two adjacent structures Dominic may ask about — collar (if shares) and diagonal / re-bought long call + short near call — stating for each whether it is a candidate in this plan (`not a candidate — variant only`) | T4 |
| S2 | `ra_candidates_kills.md` shows for each candidate whether the short strike sits at or above 150 (the strike the thesis just paid for) and flags any candidate below it with `BELOW-150` | T5 |
| S3 | `REPORT.md` `## Verdict` names the single best candidate `id` from T5 (or states `none` and the K-ids that killed all), so Dominic reads one row | T6 |
| S4 | `watch_proposal.md` (if written) is executable as-is by RA from the next session: every check is a K-id from T5 with its threshold, the file path pattern is fixed, and the approval line for Dominic is the last line | T7 |

## Out of scope

| item | why |
|---|---|
| **MHM** — any task, engine run, or artifact | Brief de-scope. Roster for this plan is Research Analyst, Price Action Analyst, UW. |
| **Session-desk SPY factor gate** (`05_factor_gate.md`, F1–F10) | Brief de-scope. This is a single-name options insight, not a session card. |
| **Pasting Mr. Whale (UW output) to Dominic** — screenshots, exports, verbatim blocks | Brief: cache; never paste. UW writes to the cache and the index only; RA writes its own read. |
| **Editing the USO thesis file, `risk.md`, any routine or skill** | Brief: no auto risk.md / thesis apply — insight + proposals. T7 is a proposal document; Dominic approves before any routine changes. |
| **Sizing** (contracts, % of capital) | Dominic's call. RA states credit, max loss, and yield per unit only. |
| **Position management after entry beyond the stated close / roll path** | Management rule is stated once in T5 as a path; ongoing management is the watch (T7, optional) or a new `plan_id`. |
| **A bearish USO thesis** or any trade premised on thesis invalidation | If the daily close < 134.34 before the REPORT, the premise (sale *against an open bullish thesis*) is gone; T6 writes `PATH:NONE — thesis invalidated; re-scope` and the plan closes. A bearish structure is a new `plan_id`. |
| **Rewriting unrelated routines** | Only if the watch is recommended, and then only as a proposal in T7. |
| **Other oil names** (XLE, XOP, CL futures, BNO, USL) | Insight is USO-specific; PA zones and UW cache are for USO only. |
| **Web sourcing** beyond confirming public event times (FOMC, BOJ, EIA) if not on the desk calendar | Desk and chain first; no external research articles. |

## Constraints

Hard (from brief):

- Every step ends in a **named file path** under `/workspace/plans/20260914-uso-call-sale/outputs/` (UW cache files sit at the UW cache location and are named by path in `outputs/uw_cache_index.md`). "RA says done" / "PA sent screenshots" is not a stop condition.
- **No auto apply.** No task edits the thesis file, `risk.md`, any routine, or any skill. Every output carries `proposals only`. T7 (if run) writes a proposal file whose last line is an approval line for Dominic.
- **UW cache; never paste.** UW writes only to its cache location and to `outputs/uw_cache_index.md` (paths, timestamps, field names). RA reads the cache and writes its own read with cache path + timestamp. `REPORT.md` `## UW read` contains no image, no code block, no UW export text. Missing or stale cache → `gex_ref: na` and the UW-dependent kills (K5, K6) read `na`; it does not block the REPORT.
- **PA never writes fundamentals.** `pa_zones.md` is levels, structure, distance, screenshots. Negative grep in M1 enforces it.
- **Defined-risk preference.** Where the account is cash (A4 default), the naked path is written as unavailable and the call credit spread (or a wide spread) is the substitute; the structure memo says so in the naked section itself.
- Owners only from {Research Analyst, Price Action Analyst, UW}. Planner owns the critique line in the DoD. Dominic decides.
- 5–8 tasks (this plan: 7, with T7 optional). Deadlines assume start 2026-09-14; `REPORT.md` target 2026-09-15 11:30 UTC (07:30 ET Tue) — before Tuesday RTH and a day before FOMC, so Dominic can choose the entry path with the event window ahead of him.
- Library / desk citations only where an on-disk note is actually relevant (USO / oil thesis file, any desk options or overwriting note). No citation for its own sake.
- Non-trivial test for every `.md` artifact: ≥ 25 non-blank lines; no `TODO` / `TBD` / `FIXME`; every quoted number has a source in the same section (chain read timestamp, cache path, screenshot path, or thesis file path); a `## Sources` section.

Soft:

- Effort units: S < 1h, M 1–3h.
- Default thresholds (Q4; RA may replace with a stated rule): buffer to short strike ≥ 0.5 × EM to expiry (target ≥ 1.0 × EM); short-strike delta band 0.15–0.30; spread width $5 default ($2.50 only if the chain is $1-increment liquid at those strikes); spread credit ≥ 1/3 of width; IV rank ≥ 40 or IV30/RV20 ≥ 1.10 for `VOL:SELL-FAVORABLE`; 25Δ RR ≥ 0 (calls at least as rich as puts) for the skew leg of the verdict.
- Expected move: EM ≈ spot × ATM IV(expiry) × √(DTE / 365), computed by RA from the chain at read time.
- If a Wave 1 file misses its deadline, T5 proceeds with the available files and writes `na` in the dependent cells; T6 lists the missing input under `## Verification` and the verdict may not be `PATH:*` other than `PATH:NONE` if `pa_zones.md` is missing (no reference level → no sale candidate).
- Cutoffs in UTC with ET in parentheses (EDT = UTC−4).

## Assumptions

| id | assumption | status | where handled |
|---|---|---|---|
| A1 | `/workspace/plans/20260914-uso-call-sale/outputs/` exists or is created by the first writer (PA or RA); `outputs/screenshots/` by PA. Planner cannot list the desk from this scratchpad repo. | assumed | T1 / T3 create if absent; T6 `## Verification` lists the directory with byte sizes. |
| A2 | At plan time USO's last daily close is above 136.57 — the thesis is open, as the brief states. | brief-confirmed | T1 records spot + timestamp; T6 checks the Mon 2026-09-14 close against 134.34 before writing `## Verdict` (K9). |
| A3 | The UW cache location for USO is known to UW and RA and exposes a file mtime or embedded timestamp RA can cite. | assumed (same as prior plans) | T2 surfaces the path in `uw_cache_index.md`; Q3. |
| A4 | Dominic holds **no USO shares** and the account in question is **cash** (the brief's "naked is cash-account awkward"). Options approval permits defined-risk spreads. | assumed from brief wording | T4 writes the path table for all cells but marks the default row; Q1 to Dominic via RA; default → spread is the default path, covered path shown as "requires shares (buy-write)". |
| A5 | The USO bullish thesis lives in a desk file whose path RA knows, and it may carry an upside target within the Oct / Nov window. | unknown | T4 cites the path or writes `thesis file: none — thesis as stated in brief (invalidation 134.34–136.57)`; Q2. Any target below a candidate short strike arms K2. |
| A6 | USO listed expiries include Sep 18 (monthly), Sep 25, Oct 2, Oct 9 (weeklies), Oct 16, Nov 20, Dec 18 (monthlies); strikes in $1 / $2.50 / $5 increments around spot; Oct 16 is the most liquid non-front monthly. | calendar fact / assumed liquidity | T3 confirms from the chain; T5 picks widths per Q6. |
| A7 | Event times: FOMC statement Wed 2026-09-16 18:00 UTC (14:00 ET), presser 18:30 UTC; EIA Weekly Petroleum Status Report Wed 2026-09-16 14:30 UTC (10:30 ET); API Tue 2026-09-15 20:30 UTC (16:30 ET); BOJ decision Fri 2026-09-18 ~02:30–03:30 UTC (Thu 22:30–23:30 ET), governor presser ~06:30 UTC (02:30 ET Fri); Sep monthly opex Fri 2026-09-18 20:00 UTC close. | standard schedule; RA confirms | T4 `## Event window`; Q5. |
| A8 | Both scheduled events have a **USD channel into oil** that points the same way for a call seller: a dovish FOMC or a hawkish BOJ weakens USD and bids oil. Combined with the geo tape, upside risk is asymmetric against short calls through the window. | Planner hypothesis | T4 states it in ≤ 3 lines; it is the reason `ENTER-POST` is the default entry token (Q5), not a lecture. |
| A9 | The Dec 150 strike is a meaningful reference: it is the level the thesis just paid for and monetized. A short strike **below 150** inside the thesis window is selling a level the desk's own view said would trade. | Planner hypothesis | S2 flags `BELOW-150`; T5 explains any such candidate in its row. |
| A10 | In a geo-driven oil spike, USO's call wing is often at least as rich as the put wing (positive or flat 25Δ risk reversal) and front-month IV sits above Oct / Nov (inverted term). If true, selling Oct / Nov calls above a supply zone sells the rich wing without holding front-week gamma through FOMC / BOJ. If false (puts richer), the call sale is selling the cheap wing and the vol verdict says so. | Planner hypothesis | T3 reads and tags; K4. |
| A11 | UW's GEX call wall (largest positive net gamma strike above spot) is the natural confluence check for the PA zone: a short strike at or above both is the candidate shape; spot trading above the call wall, negative net GEX, or a wall migrating higher over 3 sessions is a momentum regime that kills the sale. | Planner hypothesis; standard GEX reading | T5 `gex_ref` per candidate; K5. |
| A12 | PA has chart access and screenshot tooling that writes files under `outputs/screenshots/`. | assumed | T1 stop condition names the files. |
| A13 | The post to Dominic is a terse message carrying the `REPORT.md` path and the one-line verdict, not a paste of the file. | Dominic preference | T6 stop condition. |
| A14 | No MHM involvement is justified: every Must is met from the chain, PA levels, the UW cache, and RA. | roster default | `## Out of scope`; T6 `## Compliance` attests. |

## Context and inputs

Desk facts (from brief; do not re-derive):

- USO bullish thesis **OPEN**; invalidation = daily close under **134.34–136.57**.
- Dec 150 long call **exited Sep 10 for +$762**; desk now **flat** on that call. No long USO option leg remains to "cover" a short call.
- Oil / geo hot: pipeline shut; Hormuz diplomacy postponed; **WTI ~103+** earlier today (2026-09-14).
- Events: **FOMC Wednesday 2026-09-16**; **BOJ 2026-09-17/18**. Oil-specific: EIA Wednesday; API Tuesday. **Sep 18 is monthly opex.**
- Account posture for this idea: cash-account awkward for naked (A4) → defined-risk language preferred.

Planner frame — hypotheses for RA to confirm or overturn (not conclusions; each lands in a task):

| # | frame | lands in |
|---|---|---|
| F-a | **Three structures, three thesis relationships.** Covered call / buy-write = *thesis-aligned* (long shares, capped upside — the only call sale that agrees with a bullish thesis). Call credit spread = *neutral-tactical* (fade the overextension above supply with defined risk; thesis stays open underneath). Naked call = *opposed* (undefined upside exposure sold against an upside thesis; margin-only; unavailable in cash). "When each is the path" is therefore mostly a function of **shares held** and **account type**, with distance-to-zone and vol deciding *whether* rather than *which*. | T4 |
| F-b | **The spread is the default path** under A4 (no shares, cash): short strike at/above the nearest PA supply zone with ≥ 0.5–1 EM buffer and at/above the UW call wall; long strike $5 higher; Oct 16 expiry; credit ≥ 1/3 width. A wide spread ($10–15) is the cash-account stand-in for naked exposure if Dominic wants more premium. | T4, T5 |
| F-c | **Expiry ladder.** Sep 18: excluded (4 DTE through FOMC + BOJ + opex; gamma, not yield). Oct 2 / Oct 9: short post-event cycles, thinner premium. **Oct 16: primary** (~32 DTE, past both events, theta sweet spot, liquid). Nov 20: secondary if the zone is higher or vol richer. Dec 18: avoid — same expiry as the exited long; shorting Dec calls is the most direct conflict with the thesis's own horizon. | T3, T5 |
| F-d | **Strike anchor ≥ 150** unless PA's zone and the skew argue otherwise (A9). | T5, S2 |
| F-e | **Vol edge lives in the call wing and the front-month inversion** (A10). If the RR is negative at Oct 16, the sale is the cheap wing → `VOL:SELL-UNFAVORABLE` regardless of IV rank. | T3 |
| F-f | **GEX confluence** (A11): candidate short strike ≥ max(PA zone top + buffer, UW call wall). | T5 |
| F-g | **Event handling is a default of `ENTER-POST`** (Fri 2026-09-18 ≥ 13:30 UTC after BOJ, or Mon 2026-09-21), with `ENTER-BETWEEN` (Thu 2026-09-17 RTH, post-FOMC pre-BOJ) as the only pre-BOJ path and only if every K reads `CLEAR`. `ENTER-PRE` (Mon / Tue) is written but not defaulted. Post-event IV crush costs premium; the USD channel (A8) and geo tape make the gap risk one-sided. | T4 |
| F-h | **Kills are named, not lectured.** K1 no zone within 1.5 EM; K2 thesis target below short strike; K3 vol thin; K4 puts richer than calls; K5 GEX momentum regime; K6 call buying / sweeps above spot; K7 credit < 1/3 width; K8 entry inside the event window when path is `ENTER-POST`; K9 daily close < 134.34 (premise gone); K10 post-entry: daily close above short strike → close or roll up/out (path, one line). | T5 |
| F-i | **Watch** is recommended only if the REPORT's verdict is `NO-ENTRY` / `PATH:NONE` with ≥ 1 kill that can clear on its own (K1 as price moves into a zone, K3 / K4 as vol shifts, K5 / K6 as flow turns, K8 as the window passes). If every kill is structural (no shares + cash + thesis target above every sensible strike), `WATCH:NO`. | T6, T7 |

Artifact root: `/workspace/plans/20260914-uso-call-sale/outputs/`

| file | owner | role | Must |
|---|---|---|---|
| `pa_zones.md` + `screenshots/*.png` | Price Action Analyst | supply zones above spot; invalidation restated; ATR; overextension read | M1 |
| `uw_cache_index.md` (+ cache files at UW cache location) | UW | paths + timestamps + field names; no values | M2 |
| `ra_iv_skew.md` | Research Analyst | vol read; verdict token; EM per expiry | M3 |
| `ra_structure.md` | Research Analyst | structures, path decision table, event window, variants (S1) | M4 |
| `ra_candidates_kills.md` | Research Analyst | strike / expiry table; K1–K10; management path | M5 |
| `REPORT.md` | Research Analyst | decision-complete synthesis + post | M6 |
| `watch_proposal.md` (optional) | Research Analyst | standing watch proposal; approval line | S4 |

Timeline (UTC; ET in parentheses); plan time 2026-09-14 19:21 UTC (15:21 ET), RTH close 20:00 UTC:

| when | what |
|---|---|
| 2026-09-15 00:00 (Mon 20:00 ET) | Wave 1: T1 PA zones; T2 UW cache + index |
| 2026-09-15 00:30 (Mon 20:30 ET) | Wave 1: T3 RA IV/skew; T4 RA structure + event window |
| 2026-09-15 03:00 (Mon 23:00 ET) | Wave 2: T5 candidates + kills |
| 2026-09-15 11:30 (Tue 07:30 ET) | Wave 3: T6 `REPORT.md` + post |
| 2026-09-15 13:00 (Tue 09:00 ET) | Wave 3: T7 `watch_proposal.md` — only if `WATCH:RECOMMEND` |
| 2026-09-16 13:30 → 2026-09-18 13:30 | event window (FOMC Wed 18:00; EIA Wed 14:30; BOJ Fri ~02:30–03:30; opex Fri) — `ENTER-POST` opens at Fri 13:30 |

## Work breakdown

Seven tasks. Owners: Price Action Analyst (T1), UW (T2), Research Analyst (T3, T4, T5, T6, T7). T7 is optional and conditional on T6's watch token. No MHM.

| task_id | task | owner | inputs | output | depends_on | effort |
|---|---|---|---|---|---|---|
| T1 | **PA supply zones + screenshots.** Daily and 4H (weekly if one sits within reach) supply zones **above spot**: `zone_id`, timeframe, low, high, type (swing high / prior supply / measured move / round-number confluence), distance from spot in $ and in ATR14, times tested, screenshot path. Restate invalidation `134.34–136.57` as one row (type `invalidation`). Record spot + read timestamp, ATR14, and PA's overextension read (distance from 20EMA in ATR, and whether the last 3 daily bars closed outside the upper band of PA's usual channel). Levels only — no fundamentals. Answer the intake questions already sent. | Price Action Analyst | USO daily / 4H chart; PA's zone method; intake questions from Planner | `/workspace/plans/20260914-uso-call-sale/outputs/pa_zones.md` + `/workspace/plans/20260914-uso-call-sale/outputs/screenshots/*.png` | — | S |
| T2 | **UW cache for USO + index.** Refresh the USO cache: GEX by strike for Oct 16, Nov 20, and all-expiry aggregate (net GEX sign, call wall, put wall, zero-gamma); DP prints last 5 sessions; flow last 5 sessions (net call premium bought vs sold; sweeps ≥ UW's usual notable threshold at strikes above spot in Oct / Nov); OI by strike Oct 16 / Nov 20. Write `uw_cache_index.md`: one row per cache file — path, timestamp, field names. **No values, no exports, no images. Nothing else under `outputs/`.** Answer the intake questions already sent. | UW | UW data; UW cache location (A3); intake questions from Planner | UW cache files at their existing location + `/workspace/plans/20260914-uso-call-sale/outputs/uw_cache_index.md` | — | S |
| T3 | **RA IV / skew read.** From the chain at or after the Mon close: IV30; IV rank + IV percentile (252d); RV20 and IV30 / RV20; ATM IV per expiry (Sep 18, Oct 2, Oct 9, Oct 16, Nov 20, Dec 18) with the term shape named (`inverted` / `flat` / `upward`); 25Δ RR for Oct 16 and Nov 20; OVX level + 20d change; EM (1σ) to Oct 16 and Nov 20 in $. Verdict line with the rule applied and exactly one of `VOL:SELL-FAVORABLE` / `VOL:NEUTRAL` / `VOL:SELL-UNFAVORABLE` (defaults in Constraints). Confirm the expiry list (A6). `## Sources` with read timestamps. | Research Analyst | option chain; OVX; RV from on-disk closes | `/workspace/plans/20260914-uso-call-sale/outputs/ra_iv_skew.md` | — | M |
| T4 | **RA structure memo + event window.** `## Covered call`, `## Naked call`, `## Call credit spread` — thesis relationship, requirements, when it is the path, management path (close / roll), cash-account substitute. `## Path decision table` keyed on shares × account × thesis state × distance-to-zone × vol verdict, with the A4 default row marked. `## Event window`: A7 timestamps (UTC + ET), the four entry tokens defined with their windows, Sep 18 excluded as a sale expiry with reason, USD channel in ≤ 3 lines (A8), default token per F-g. `## Variants` (S1). Cite the thesis file by path or write `thesis file: none` (A5); state any upside target inside the Oct / Nov window. `proposals only`. `## Sources`. | Research Analyst | brief facts; thesis file (Q2); desk calendar; A4 / Q1 | `/workspace/plans/20260914-uso-call-sale/outputs/ra_structure.md` | — | M |
| T5 | **RA candidates + kills.** `## Candidates` (3–6 rows; columns per M5): spread rows on Oct 16 (primary) and Nov 20 (secondary) with short strike ≥ max(zone top + buffer, call wall), long = short + width; one covered-call row marked `requires shares`; one wide-spread row as the naked stand-in; each row's `zone_ref` → a T1 `zone_id`, `gex_ref` → a T2 cache path; `buffer_EM` from T3's EM; `yield` = credit / (width − credit) for spreads, premium / spot annualized for covered. S2 `BELOW-150` flag. `## Kills`: K1–K10 as F-h, each with signal owner (PA / UW cache via RA / RA), the check, `ARMED` / `CLEAR` / `na`, and the value read. `## Management`: one path — on a daily close above the short strike: close, or roll up and out to the next zone / Nov 20; on a daily close < 134.34: K9 — the sale's premise is gone; RA states the default (close the short leg with the thesis) as a proposal. `## Sources`. | Research Analyst | T1 `pa_zones.md`; T2 cache via `uw_cache_index.md`; T3 `ra_iv_skew.md`; T4 `ra_structure.md`; chain | `/workspace/plans/20260914-uso-call-sale/outputs/ra_candidates_kills.md` | T1, T2, T3, T4 | M |
| T6 | **RA `REPORT.md` + post.** Sections per M6. `## Verdict`: one paragraph, three tokens, best candidate `id` or `none` + K-ids (S3); check the Mon close against 134.34 first (K9 / A2). `## UW read`: RA prose ≤ 8 lines + cache path + timestamp; no paste. `## Compliance`: no thesis / `risk.md` / routine / skill edits; no UW paste; PA wrote no fundamentals (negative grep result); no MHM; no factor gate. `## Verification`: directory listing with byte sizes and per-md non-trivial result; missing Wave 1 inputs named. `## Watch`: `WATCH:RECOMMEND` / `WATCH:NO` with the clearable K-ids. Post to Dominic: terse, `REPORT.md` path + verdict line; post reference on the last line. | Research Analyst | all files under `outputs/`; T5 | `/workspace/plans/20260914-uso-call-sale/outputs/REPORT.md` | T5 | S |
| T7 | **Optional — standing watch proposal.** Only if T6 reads `WATCH:RECOMMEND`. One page: purpose; cadence (default daily post-close through 2026-10-16 or thesis invalidation, whichever first); checks = the clearable K-ids with thresholds; inputs (PA zone refresh cadence — default weekly Fri into a versioned `pa_zones.md`; UW cache daily cutoff; RA chain read); output line `WATCH:GO` / `WATCH:HOLD <K-ids>` into `outputs/watch/YYYY-MM-DD.md`; who runs it (RA) and what it does **not** do (no orders, no thesis edits). Last line: `Dominic: approve / decline`. `## Sources`. | Research Analyst | T6 `REPORT.md`; T5 kills | `/workspace/plans/20260914-uso-call-sale/outputs/watch_proposal.md` | T6 | S |

## Sequence

Planner → desk execution card. PA and UW have their intake questions already; their steps are 1a and 1b. RA's independent reads (1c, 1d) run in parallel so that Wave 2 starts the moment the PA / UW files land. Deadlines UTC (ET in parentheses).

**Wave 1 — parallel inputs (tonight, Mon 2026-09-14 ET)**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 1a (T1) | Price Action Analyst | `/workspace/plans/20260914-uso-call-sale/outputs/pa_zones.md` + `outputs/screenshots/*.png` | file exists; ≥ 2 rows with `zone_id` and low < high, both above the recorded spot; one row `134.34–136.57` typed `invalidation`; spot + timestamp, `ATR14`, `20EMA` distance present; every zone row names a screenshot path that exists; negative grep for `Hormuz`, `pipeline`, `FOMC`, `BOJ`, `OPEC`, `inventor`, `WTI`, `geo` returns nothing; passes the non-trivial test | 2026-09-15 00:00 (20:00 ET Mon) |
| 1b (T2) | UW | UW cache files at their location + `/workspace/plans/20260914-uso-call-sale/outputs/uw_cache_index.md` | index exists; rows for GEX (Oct 16, Nov 20, aggregate), DP, flow, OI (Oct 16, Nov 20); every path listed exists with mtime ≤ 00:00 UTC; index contains no numeric strike / gamma / premium values, no image, no code block; no other UW-authored file under `outputs/` | 2026-09-15 00:00 (20:00 ET Mon) |
| 1c (T3) | Research Analyst | `/workspace/plans/20260914-uso-call-sale/outputs/ra_iv_skew.md` | contains `IV30`, `IV rank`, `IV percentile`, `RV20`, ATM IV rows for all six expiries, `25Δ` (or `25-delta`) RR for Oct 16 and Nov 20, `OVX`, `EM` for Oct 16 and Nov 20, a term-shape token, and exactly one `VOL:` token with the rule stated; every number has a read timestamp; passes the non-trivial test | 2026-09-15 00:30 (20:30 ET Mon) |
| 1d (T4) | Research Analyst | `/workspace/plans/20260914-uso-call-sale/outputs/ra_structure.md` | headings `## Covered call`, `## Naked call`, `## Call credit spread`, `## Path decision table`, `## Event window`, `## Variants`, `## Sources`; `## Naked call` contains `cash` and names the spread substitute; `## Event window` contains `FOMC`, `BOJ`, `EIA`, `opex`, all four `ENTER-` / `NO-ENTRY` tokens, `Sep 18` + `excluded`, and a default token; thesis file path or `thesis file: none`; `proposals only`; no instruction to edit the thesis or `risk.md`; passes the non-trivial test | 2026-09-15 00:30 (20:30 ET Mon) |

**Wave 2 — candidates and kills**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 2 (T5) | Research Analyst | `/workspace/plans/20260914-uso-call-sale/outputs/ra_candidates_kills.md` | `## Candidates` has 3–6 rows with all M5 columns; every `zone_ref` matches a `zone_id` in `pa_zones.md` or is `na`; every `gex_ref` matches a path in `uw_cache_index.md` or is `na`; `BELOW-150` flag applied where due; `## Kills` has rows `K1`…`K10` each with owner, check, one of `ARMED` / `CLEAR` / `na`, and the value read; `## Management` present with `close` and `roll`; `## Sources`; passes the non-trivial test | 2026-09-15 03:00 (23:00 ET Mon) |

**Wave 3 — synthesis and optional watch**

| step | owner | artifact path | stop condition | deadline UTC |
|---|---|---|---|---|
| 3a (T6) | Research Analyst | `/workspace/plans/20260914-uso-call-sale/outputs/REPORT.md` | all twelve M6 headings present; `## Verdict` contains exactly one `PATH:` token, exactly one entry token, exactly one `WATCH:` token, and a candidate `id` or `none`; `## UW read` ≤ 8 lines of prose + a cache path + timestamp, no `![`, no code fence; `## Compliance` contains `thesis`, `risk.md`, `paste`, `fundamentals`, `MHM`, `factor gate`; `## Verification` lists every file under `outputs/` with byte size and per-md non-trivial result; last line is the post reference to Dominic; passes the non-trivial test | 2026-09-15 11:30 (07:30 ET Tue) |
| 3b (T7, optional) | Research Analyst | `/workspace/plans/20260914-uso-call-sale/outputs/watch_proposal.md` | written **only if** `REPORT.md` contains `WATCH:RECOMMEND`; contains cadence, end condition (`2026-10-16` or `134.34`), every check as a `K` id with threshold, output pattern `outputs/watch/YYYY-MM-DD.md`, tokens `WATCH:GO` / `WATCH:HOLD`, the phrase `no orders`; last line `Dominic: approve / decline`; passes the non-trivial test. If `WATCH:NO`, this step is skipped and `REPORT.md` `## Watch` states why. | 2026-09-15 13:00 (09:00 ET Tue) |

**Plan-level stop:** the plan closes when 3a's stop condition is met and either 3b's stop condition is met or `REPORT.md` reads `WATCH:NO`. A Wave 1 miss does not block Wave 2: T5 writes `na` in dependent cells and T6 names the missing input; if `pa_zones.md` is missing, `## Verdict` is `PATH:NONE` (no reference level). If the Mon 2026-09-14 daily close is < 134.34, T6 writes `PATH:NONE — thesis invalidated; re-scope` and the plan closes without T7. Any bearish structure, sizing decision, routine change, or trade in another oil name is a new `plan_id` or Dominic's own call.

Owner-side rules for the card: PA writes levels only (negative grep enforced); UW writes to cache + index only, never to Dominic; RA reads the cache and writes its own read; no file outside `outputs/` is created or edited except the UW cache at its own location; `proposals only` in every RA file; no MHM; no SPY factor gate; naked path written as unavailable under a cash account with the spread as substitute.

## Definition of done

Checkable by listing files and grepping content under `/workspace/plans/20260914-uso-call-sale/outputs/`.

Non-trivial test (every `.md`): ≥ 25 non-blank lines; no `TODO` / `TBD` / `FIXME`; every quoted number has a source in the same section; a `## Sources` section.

- [ ] `pa_zones.md` passes the non-trivial test; ≥ 2 zone rows with `zone_id`; one row containing `134.34` and `136.57` typed `invalidation`; contains `ATR14` and `20EMA`; every screenshot path named exists under `outputs/screenshots/` with size > 0; `grep -iE 'Hormuz|pipeline|FOMC|BOJ|OPEC|inventor|WTI|geo'` returns nothing.
- [ ] `uw_cache_index.md` exists; rows for `GEX`, `DP`, `flow`, `OI`; every path listed exists with mtime ≤ 2026-09-15 00:00 UTC; the file contains no `![`, no code fence, and no strike-level numeric values; no other file under `outputs/` is authored by UW.
- [ ] `ra_iv_skew.md` passes the non-trivial test; contains `IV30`, `IV rank`, `IV percentile`, `RV20`, `OVX`, `EM`, the six expiry dates, `25Δ` or `25-delta`, one term-shape token from {`inverted`, `flat`, `upward`}, and exactly one `VOL:` token.
- [ ] `ra_structure.md` passes the non-trivial test; contains `## Covered call`, `## Naked call`, `## Call credit spread`, `## Path decision table`, `## Event window`, `## Variants`; `## Naked call` contains `cash`; `## Event window` contains `FOMC`, `BOJ`, `EIA`, `opex`, `ENTER-PRE`, `ENTER-BETWEEN`, `ENTER-POST`, `NO-ENTRY`, `Sep 18`, `excluded`; contains `proposals only`; contains either a thesis file path or `thesis file: none`; contains no instruction to edit the thesis or `risk.md`.
- [ ] `ra_candidates_kills.md` passes the non-trivial test; `## Candidates` has 3–6 rows; every `zone_ref` value appears as a `zone_id` in `pa_zones.md` or is `na`; every `gex_ref` value appears as a path in `uw_cache_index.md` or is `na`; `## Kills` contains `K1` … `K10` each followed by one of `ARMED` / `CLEAR` / `na`; `## Management` contains `close` and `roll`.
- [ ] `REPORT.md` passes the non-trivial test; contains the twelve M6 headings; exactly one of `PATH:COVERED` / `PATH:SPREAD` / `PATH:NAKED` / `PATH:NONE`; exactly one of `ENTER-PRE` / `ENTER-BETWEEN` / `ENTER-POST` / `NO-ENTRY`; exactly one of `WATCH:RECOMMEND` / `WATCH:NO`; `## UW read` has no `![` and no code fence and contains a cache path + timestamp; `## Compliance` contains `thesis`, `risk.md`, `paste`, `fundamentals`, `MHM`, `factor gate`; `## Verification` lists every file under `outputs/` with a byte size; last line is the post reference to Dominic.
- [ ] If `REPORT.md` contains `WATCH:RECOMMEND`: `watch_proposal.md` passes the non-trivial test and contains `K` ids with thresholds, `outputs/watch/YYYY-MM-DD.md`, `WATCH:GO`, `WATCH:HOLD`, `no orders`, and last line `Dominic: approve / decline`. If `WATCH:NO`: `watch_proposal.md` does not exist and `REPORT.md` `## Watch` states the reason.
- [ ] No file outside `outputs/` (thesis file, `risk.md`, any routine or skill) has a modification attributable to this plan; the UW cache at its own location is the only permitted write outside `outputs/`.
- [ ] No artifact references MHM as an owner, the SPY factor gate, or any oil name other than USO as a trade candidate.
- [ ] `02_plan.critique.md` in this scratchpad shows PASS on all eight checklist items (Planner).

## Open questions

None blocks Wave 1. Each has one roster owner, a place it is resolved, and a default.

| id | question | owner | resolve in | default if unresolved |
|---|---|---|---|---|
| Q1 | Does Dominic hold USO shares, is the account cash-only, and are defined-risk spreads permitted? | Research Analyst (asks Dominic) | T4 `## Path decision table` default row | No shares; cash; spreads permitted → spread is the default path; covered path written as `requires shares (buy-write)`; naked written as unavailable with the wide spread as substitute. |
| Q2 | Path of the USO thesis file, and does it carry an upside target inside the Oct / Nov window? | Research Analyst | T4 (path cited) → T5 K2 | `thesis file: none — thesis as stated in brief`; K2 reads `na`; candidates anchored ≥ 150 (A9). |
| Q3 | Exact UW cache path for USO and the staleness threshold RA applies? | UW (path), Research Analyst (threshold) | T2 index; T5 `gex_ref` | Path as UW reports; stale = older than the Mon 2026-09-14 close → K5 / K6 `na`. |
| Q4 | Default thresholds (buffer ≥ 0.5 EM target 1.0; Δ 0.15–0.30; credit ≥ 1/3 width; IVR ≥ 40 or IV/RV ≥ 1.10; RR ≥ 0) acceptable? | Research Analyst | T3 verdict rule; T5 K3 / K4 / K7 | Defaults stand; RA states any replacement rule in the file where it is applied. |
| Q5 | Is any pre-BOJ entry (`ENTER-PRE`, `ENTER-BETWEEN`) acceptable to Dominic, or is `ENTER-POST` a hard wait? | Research Analyst (asks Dominic) | T4 `## Event window` default; T6 `## Verdict` | `ENTER-POST` default; `ENTER-BETWEEN` only if every K is `CLEAR`; `ENTER-PRE` written, not defaulted. |
| Q6 | Spread width $5 or $2.50, given chain liquidity at the candidate strikes? | Research Analyst | T5 `## Candidates` | $5; $2.50 only if $1-increment strikes show tight markets at read time, stated per row. |
| Q7 | If the watch is recommended: cadence (daily post-close vs premarket) and PA's zone refresh cadence? | Research Analyst (proposes), Dominic (approves) | T7 | Daily post-close; PA refresh weekly Fri; ends 2026-10-16 or on thesis invalidation. |
| Q8 | Does PA's zone set include a weekly-timeframe zone if one sits within 1.5 EM, or daily / 4H only? | Price Action Analyst | T1 | Daily + 4H; weekly added only if within reach and labelled `W`. |
| Q9 | Should the diagonal (re-buy a long-dated call, sell a near call) be a candidate row or a variant only? | Research Analyst | T4 `## Variants` | Variant only — the desk just exited its long call; re-buying to "cover" a sale is a different thesis action and would be Dominic's call, not a candidate here. |
| Q10 | Which of K1–K10 does RA treat as **clearable** (drives `WATCH:RECOMMEND`) vs structural? | Research Analyst | T6 `## Watch` | Clearable: K1, K3, K4, K5, K6, K8; structural: K2 (unless the thesis target moves), K7 (chain-dependent, semi-clearable), K9 (terminal). |

## Changelog

| version | date | brain | change |
|---|---|---|---|
| 1 | 2026-09-14 | fable-5.1 | In-depth draft. Seven tasks — Price Action Analyst (T1 zones + screenshots, levels only), UW (T2 cache + index, never paste), Research Analyst (T3 IV/skew read; T4 structure memo + event window; T5 candidates + K1–K10 kills + management path; T6 decision-complete `REPORT.md` + post; T7 optional watch proposal). Wave 1 parallel by 2026-09-15 00:00–00:30 UTC; Wave 2 by 03:00 UTC; `REPORT.md` by 11:30 UTC (07:30 ET Tue), ahead of FOMC Wed 2026-09-16 and BOJ 2026-09-17/18. Planner frame: covered = thesis-aligned, spread = neutral-tactical default under a cash account, naked = opposed / unavailable; Oct 16 primary expiry, Sep 18 excluded, Dec 18 avoided; strike ≥ max(PA zone top + buffer, UW call wall), anchored ≥ 150; `ENTER-POST` default. All outputs proposals; no thesis / `risk.md` / routine edits. De-scoped: MHM, SPY factor gate, pasting UW to Dominic, sizing, bearish thesis, other oil names. Status `draft`. |
