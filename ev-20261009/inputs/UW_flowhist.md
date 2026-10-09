# UW_flowhist — Unusual Whales inputs for the EV evaluation (job UW-20261009-05)
For Dominic (Planner T2; RA lead). Written Fri 2026-10-09 ~13:10 ET. All times ET.
**Covers:** USO Nov20 150/155C + 150/160C · GOOGL Nov20 355/365C + 360/370C · PLTR Oct16 205/210C · SPY Oct16 778/781C (bull) + 775/767P (bear) · IBIT Nov20 46/49C · TSLA (no spread; context only).
**Read times:** this job 12:53–13:01 ET (chains/flow/GEX/IV 12:53–12:57; contract pages 12:58–12:59; Mr. Whale ~13:00–13:01). Earlier today: IBIT 08:31 + 09:59–10:00 (plans/20261009-btc/uw.md); watchlist UW 10:04–10:07 (OI as of 10/08 close) and 12:10–12:13; gamma check 12:16–12:21. Yesterday: watchlist UW 11:09–11:12, 12:14–12:16, 15:02–15:05; USO 10/08 09:17–09:18 (uw-uso-1008.md).
**Rules:** only numbers from the source files; NO DATA where missing. Sums/differences marked "(sum)"/"(diff)" are my arithmetic on source numbers. The UW tag is my judgement, kept conservative.

## Global caveats
1. **No live bid/ask from UW.** Chain and contract pages show only the bid/ask volume split ("B/A vol %", shown as UW prints it) and fill prices; Mr. Whale returned "NO DATA: bid/ask unavailable" for every leg. Spread liquidity/width can't be scored from UW; debits come from RA/Robinhood (02_plan.md).
2. **Flow lists = top ~250 prints by premium** per query, so each list has a premium floor (stated per ticker: USO ~$134K, GOOGL ~$400K, PLTR ~$379K, SPY today ~$219K, IBIT ~$136K, TSLA ~$807K; Whale SPY 10/01–10/09 list smallest row $377.5K). Smaller prints are invisible.
3. **Opening vs closing is inferred**, not labelled by UW: vol > OI on the print day, and/or the next OI update. "Opened (sold/bought)" = side tag + OI change = inference.
4. **OI dating:** contract-page OI dated D = OI as of D's open (prior close). So the 10/09 "OI chg" reflects 10/08 trading; today's prints show up in Monday's OI.
5. **Whale flow-setup history = NO DATA for all six tickers** (see §4).
6. **Two GEX bases:** Live heatmap = directionalized volume, DTE-limited (setting varies: 10/30/60 DTE, noted per name); Gamma tab = OI, all expiries, no DTE control. Their flips/walls differ; both are shown. Gamma describes dealer hedging (dampen/amplify), not a price forecast.
7. Per-expiry IV term structure not shown by UW (only 30d/90d); implied moves only where the chain gave them.

## 1. Summary (one row per setup)
| Setup | Spread (debit, plan) | Flow at the strikes (open/close, $, side) | GEX vs spread strikes | IVR · IV30 vs RV21 | Min leg OI | Flow-history evidence | UW tag (judgement) |
|---|---|---|---|---|---|---|---|
| USO bull | Nov20 150/155C ($192.50); 150/160C ($337.50) | At legs only 160C ASK $164K 10/06 (opened: OI 2,187→2,676). None ≥~$134K at 150/155. Between the strikes: **Nov 153C short-call build** — 10/07 BID $1.95M + 10/08 BID $1.31M opened as sold; OI 360 (10/06) → 3,573 → 7,154 → 8,954 | Live (60D): CW 154, flip 147.81, PW 147, Amplifying. Gamma tab: **CW 151**, PW 144, Short Γ/Amplifying, magnet 140. Both call walls sit **between 150 long and 155/160 short** | 18.96 (pct 42) · 44.7–45.2% vs 40.2% | 1,490 (155C); 2,699 (160C) | n=0 setup stats (Whale NO DATA). Proxy: USO big dark-pool days n=75 → no edge vs base rate | **−1**: large sold-call OI (8,954) at 153 and both call walls between the strikes = supply under the short strike; no opening ask-side buying at the legs |
| GOOGL bull | Nov20 355/365C ($437.50); 360/370C ($392.50) | No vol>OI at 355–370. 370C two-way: ask $6.11M vs bid $6.40M (sum, 10/01–10/08) + MID $1.4M; OI −2,961 at 10/09 update = **net closing**. 360C ASK $863K / BID $514K (10/02). 355C BID $645K (10/02). 365C none. Nearby: Feb27 345C sold at bid (opened +1,953; again $7.23M BID today) = overwrites | Gamma tab: **CW = magnet = 355 (= long strike of 355/365)**, flip 352.83, PW 350, Long Γ/Dampening. Live (60D): CW 357.5, flip 348.9, PW 347.5, Amplifying. Short strikes 365/370 above both call walls | 54.08 (pct 65) · 35.7% vs 24.3%; earnings 10/28 inside Nov20 | 2,946 (365C); 11,499 (360C) | n=0 setup stats. Proxy: GOOG/GOOGL large-call flow around 7 200DMA test days (4 windows): ask-side buying only after the 9/9–9/11 tests; other windows leaned bid | **0** (lean −): pin/cap at 355–357.5 under the short strikes, 370C closing, call overwrites, rich IV vs RV; offset by positive GOOG net premium and 31K Nov 355C OI (side unknown) |
| PLTR bull | Oct16 205/210C ($220) | OI at 10/09 update up at 205 (+1,127), 210 (+1,929), 215 (+1,370); **today vol > OI at 205/210/215** (19,817/12,618/17,201) = opening, side mixed: 205C BID $1.23M (ML w/ 212.5C MID $463K, vol>OI); 207.5C MID $1.06M + 215C MID $396K (vol>OI); 210C none ≥$379K. 205P BID $450K vol>OI (put sold, opening) | Gamma tab: **CW 210 (= short strike)**, PW = magnet 205 (= long strike), flip 192.95, Long Γ/Dampening. Live (30D, 12:5x): CW 215, PW 190, flip 195.2, Amplifying; 10/16 col: 205 +8,650K, 210 −747K | 49.05 (pct 67) · 57.1–57.4% vs 24.0% (Oct16 chain IV ~42%) | 8,003 (205C) | n=0 setup stats (Whale NO DATA) | **0** (lean +): heavy opening OI at both legs and +$21.25M net premium (12:19), but sides at the legs are mixed/MID, magnet at the long strike and IV rich vs RV |
| SPY bull | Oct16 778/781C ($152) | 778C 10/08 15:58 ASK $648K vol 6,253 > OI 5,765 → OI +569 (opened, bought). 781C 10/02 BID $585K → OI 5,554→8,790 (opened, sold side; inference). Today C780 ASK $278K (vol<OI). OI 10d: 778C 4,651→6,334; 781C 3,825→9,780 | Gamma tab (12:19): **CW = magnet 780 (inside 778/781)**, PW 777, flip 824.02, Dampening. Live: PW 776 (12:56, 10D) / 777 (12:19, 30D); flip 777.19 / 777.56; CW 783 / 787; Amplifying; negative Γ 778–780 (12:19: 778 −6.0B, 779 −659M, 780 −498M) | **9.31** (pct 10) · 12.5% vs 10.0%; 10/16 implied ±0.93% ($7.25) | 6,334 (778C) | n=0 setup stats. Whale 10/01–10/09 SPY Oct16 prints listed (n=20 rows) — not outcome stats | **+1**: cheap IV, magnet/call wall at 780 inside the spread, opening ask-side 778C; caveat 781C OI build looks sold |
| SPY bear | Oct16 775/767P ($170.50) | 775P: 10/08 ASK $618K vol 10,357 > OI 9,812 but OI then **−1,123** (8,689) → net closing; 10/06 cross $885K (no side); 10/05 BID $413K; 10/01 ASK $403K. 767P: no prints in lists; **OI 6,815→9,826 (10d), +1,540 at 10/09 update** | Live PW 776–777 and flip 777.2–777.6 sit just above the 775 long put; positive Γ 775–777 (12:19: +398M/+931M/+1.52B) = dampening support. Summary accel ↓ at **767 (= short put)** | 9.31 · 12.5% vs 10.0% | 8,689 (775P) | n=0 setup stats | **0**: rising 767P OI and cheap IV vs put-wall/positive-gamma support at 775–777 and 775P net closing |
| IBIT bull | Nov20 46/49C (~$138) | **No ask-side opening call buying for 2 days** (10/08 15:02 and 10/09 08:31–12:13 reads). 46C: no prints. 49C: 10/02 ASK $363K, BID $290K; 10/05 ASK $208K (none vol>OI). Nov27 49.5C/52.5C sold at bid today, opening (vol 4,400>21; 5,500>0). Nov 48C/48P crosses opened (side unknown) | Live (60D): flip 46.3 (just above 46 long), **CW 47.5 (below 49 short)**, PW 43, Amplifying. 46 strike not captured; 49 Σ −391K. Gamma tab/magnet: NO DATA | **7.59** (pct 13) · 36.3% vs 38.2% (IV < RV) | 22,023 (46C) | n=0 setup stats | **0** (lean −): no confirming flow, calls sold above spot, CW below short strike; offset by very cheap IV |
| TSLA | No spread (RA to propose) | 10/16 385C vol 22,309 vs OI 10,137 (opening volume), prints two-way: ASK $1.44M (vol>OI) + $1.06M, BID $1.58M (vol>OI). 392.5C ASK $1.08M + $966K, MID $1.08M (vol>OI 1,609). 10/16 400C OI +7,984, 390C +2,980 | Live (60D): **on the flip 381.23** (spot 383.49), PW 380 (64.8M), CW 390 (17.9M); 385 −97.8M, 382.5 −180.5M. Gamma tab (12:1x): CW = magnet 400, flip 382.06, Accel ↓ 370 | 23.74 (pct 28) · 43.0% vs 29.7%; earnings 10/21 AMC (±6.71%), before Nov20 | NO DATA (no legs) | n=0 setup stats | **0**: no spread; flow two-way; IV rich vs RV with earnings inside Nov20 |

Do-not-double-count note: price levels/triggers are PA's. The GEX rows above are dealer-positioning facts at the option strikes, not price base rates.

## 2. Per-name detail

### 2.1 USO — Nov20 150/155C, 150/160C (spot $147.57 @12:53)
**Strike table (Nov20 calls; B/A vol % as shown by UW; quote = NO DATA all rows)**
| Strike | OI | OI chg | Vol | Last | IV | B/A vol % |
|---|---|---|---|---|---|---|
| 145 | 880 | −60 | 49 | 11.15 | 46% | 84% |
| **150** | 5,740 | −97 | 78 | 8.00 | 46% | 45% |
| **155** | 1,490 | +13 | 34 | 6.16 | 46% | 82% |
| 158 | 647 | +4 | 7 | 5.80 | 47% | 100% |
| **160** | 2,699 | +84 | 180 | 4.72 | 47% | 48% |
| 165 | 1,566 | +17 | 70 | 3.62 | 48% | 60% |
**10-day OI per leg (10/09 → 09/28, quotes.md):** 150C 5740, 5837, 5581, 5563, 5557, 5454, 5205, 5147, 4989, 4985 (+755 diff, rising; −97 last). 155C 1490, 1477, 1525, 1513, 1270, 1222, 1232, 1234, 1238, 1191 (+299 diff). 160C 2699, 2615, 2676, 2187, 2155, 2074, 1978, 1969, 1949, 1950 (+749 diff; step +489 on 10/07).
**Flow at/near the strikes (top-250, floor ~$134K, 10/01–10/09):**
- 10/06 09:40 160C ASK @3.70, 442, $164K, vol 705 / OI 2,187 → OI 2,676 next update (opened, bought).
- 10/02 13:42 158C BID @6.60, 248, $164K, vol 276 / OI 719.
- 10/01 15:54 145C ASK @13.60, 200, $272K, vol 267 / OI 638. 10/05 09:43 150P ASK $268K (vol 219 / OI 2,033); 10/07 145P ASK $144K.
- **153C short-call build (between the long and short strikes):** 10/06 15:43 cross 3,550 $2.26M vol 3,586 > OI 360; 10/07 15:36 BID 3,350 $1.95M (OI 3,573 → 7,154, +3,581, opened as sold); 10/08 15:18 BID 1,800 $1.31M (OI 7,154 → 8,954, +1,800). Sold-call read = side tag + OI (inference). Same day the 10/16 151C ask buy was a close (OI −2,148).
- Today (10/09): no prints ≥$134K at Nov 145–165; 10/16 150C two-way (BID $301K; ASK $251K/$194K/$176K, OI 5,754); net premium +$0.96M (12:10).
**GEX:** Live (DTE=60, 12:54): Amplifying, flip 147.81, CW 154 (48.8K), PW 147 (3.7M); Σ 155 −767K, 150 −128K, 145 −405K; 11/20 column 155 8.8K, 150 3.2K; 160 outside window (NO DATA). DTE=30 same levels. Gamma tab: Short Γ/Amplifying, net −$20.81K, flip N/A, **CW 151**, PW 144, magnet = short-gamma pocket 140 ($47.16K). Read: CW 151 (Gamma) and 154 (Live) both lie between 150 and 155/160.
**IV:** IVR 18.96 (pct 42; IV pct 30d/1y 19%); IV30 44.7–45.2%; RV21 40.2%; IV 52w 25.8–128.8%; term 30d 44.7% → 90d 43.7% (backwardation); Nov20 chain IV ~46%. Implied moves: 10/14 ±3.13%, 10/16 ±4.04%, 10/21 ±5.15%, 10/23 ±5.71%, 10/30 ±7.29%; Nov20 NO DATA.

### 2.2 GOOGL — Nov20 355/365C, 360/370C (spot $354.33 @12:53)
**Strike table (Nov20 calls; quote NO DATA)**
| Strike | OI | OI chg | Vol | Last | IV | B/A vol % |
|---|---|---|---|---|---|---|
| 350 | 7,490 | −346 | 1,038 | 19.72 | 37% | 56% |
| **355** | 31,092 | +23 | 563 | 17.07 | 36% | 50% |
| **360** | 11,499 | −20 | 962 | 14.60 | 36% | 73% |
| **365** | 2,946 | +159 | 82 | 12.80 | 36% | 51% |
| **370** | 34,302 | −2,961 | 862 | 10.95 | 36% | 53% |
| 375 | 3,246 | +102 | 54 | 9.22 | 36% | 63% |
**10-day OI per leg:** 355C 31092, 31069, 30916, 30724, 30593, 30688, 30232, 30061, 29874, 1873 (+28,001 jump 09/28→09/29 = the 9/28 27,400-lot cross, side NONE; flat since). 360C 11499, 11519, 11172, 11414, 11181, 10370, 10130, 10148, 9803, 9746 (+1,753 diff). 365C 2946, 2787, 2743, 2712, 2682, 2912, 2835, 2840, 2842, 2797 (flat). 370C 34302, 37263, 37273, 33062, 33070, 33630, 33446, 28873, 28668, 37625 (±9K swings; −2,961 at 10/09 update = closing).
**Flow Nov20 350–375 (floor ~$400K):**
- 370C: 10/08 13:34 ASK @8.90 2,276 $2.03M (vol 6,524 / OI 37,263); 10/08 13:33 BID $1.34M + $1.33M; 10/07 ASK $712K; 10/06 15:46–15:48 ASK $1.4M, $954K, $534K + MID $1.4M; 10/01 09:37–09:38 BID $1.49M, $1.31M, $932K + ASK $482K. Ask $6.11M vs bid $6.40M (sum) → OI fell 2,961 after 10/08 = net closing.
- 360C: 10/02 11:17 ASK @11.50 750 $863K (vol 1,149 / OI 10,370); 11:34 BID $514K. OI 10,370 → 11,181 (next update).
- 355C: 10/02 12:47 BID @13.35 483 $645K (vol 1,067 / OI 30,688). 365C: no prints ≥$400K.
- 350C ASK $752K (10/02), BID $695K (10/01). Nearby: 380C 10/05 cross 20,000 $12.8M vol 21,770 > OI 9,031 (paired 435C; 380/435 spread opened, side NONE).
- Overwrites: Feb27 345C sold at bid 10/08 ($2.10M + $2.08M, vol 1,627 > OI 635) → OI +1,953 (opened, sold); sold again 10/09 10:09 BID $7.23M (vol 2,088 / OI 2,588). Also 11/20 380C ASK $324K today.
- Net premium today: GOOGL +$5.48M (10:06) → +$3.57M (12:10); GOOG +$5.87M → +$11.79M.
**GEX:** Gamma tab (12:13 and 12:5x): Long Γ/Dampening, net +$855K, flip 352.83, **CW 355 = magnet ($177K)**, PW 350. Live (DTE=60, 12:5x): Amplifying, flip 348.9, CW 357.5 (23.4M), PW 347.5 (2.9M); Σ 355 −52,320K, 360 +497K, 365 −2,178K, 370 −470K; 11/20 column 355 66.2K, 360 −526K, 365 2.0K, 370 115K. (Live 30D at 12:12: flip 350.67, CW 357.5, PW 350.)
**IV:** IVR 54.08 (pct 65; IV pct 76%); IV30 35.7%; RV21 24.3%; term 30d 35.7% → 90d 32.4% (backwardation); Nov20 chain IV ~36%. **Earnings 10/28, before Nov20.** Implied move: NO DATA.

### 2.3 PLTR — Oct16 205/210C (spot $205.45 @12:53)
**Strike table (Oct16 calls; 207.5/212.5 exist but not in table; quote NO DATA)**
| Strike | OI | OI chg | Vol | Last | IV | B/A vol % |
|---|---|---|---|---|---|---|
| 200 | 16,883 | −722 | 13,338 | 8.00 | 42% | 50% |
| **205** | 8,003 | +1,127 | 19,817 | 5.10 | 42% | 59% |
| **210** | 11,407 | +1,929 | 12,618 | 2.85 | 41% | 49% |
| 215 | 3,990 | +1,370 | 17,201 | 1.53 | 42% | 38% |
From the 12:18 read: 207.5C OI 2,314 (vol 14,983), 212.5C OI 1,682 (vol 11,254).
**10-day OI per leg:** 205C 8003, 6876, 5603, 4267, 3797, 3723, 4343, 4069, 4025, 2312 (rising every update since 10/02; +5,691 diff). 210C 11407, 9478, 9113, 8895, 8754, 8568, 8224, 7976, 9144, 8585 (+2,822 diff; +1,929 last).
**Flow Oct16 200–215 (floor ~$379K, all 10/09):**
- 09:59 205C BID @2.99 4,097 $1.23M (vol 7,818 / OI 8,003; ML, paired 212.5C MID @1.13 4,097 $463K vol 4,733 > OI 1,682).
- 10:35 207.5C MID @2.66 4,000 $1.06M (vol 6,264 > OI 2,314) with 215C MID @0.99 4,000 $396K (vol 7,172 > OI 3,990).
- 10:07 200C ASK @4.35 1,328 $578K (vol 8,061 / OI 16,883).
- Puts: 09:46 200P ASK $722K (vol>OI); 10:12 200P BID $460K (vol>OI); 12:18 205P BID @4.40 1,023 $450K (vol 5,116 > OI 190 → put sold, opening).
- No 210C prints ≥$379K. Net premium +$21.25M (calls +$12.2M, puts −$9.1M) at 12:19; largest call prints are 0DTE 195C and deep-ITM rolls.
**GEX:** Gamma tab: Long Γ/Dampening, net +$988.6K, flip 192.95, **CW 210 (= short strike)**, **PW = magnet 205 (= long strike)**. Live (DTE=30, 12:5x): Amplifying, flip 195.2, CW 215 (1.3M), PW 190 (1.2M); Σ 205 +1,175K (10/16 +8,650K), 207.5 −3,663K, 210 −2,500K (10/16 −747K), 212.5 −1,401K, 215 +1,322K. (12:18 Live: CW 220, PW 192.5, flip 196.09; negative Γ 202.5 −13.8M.)
**IV:** IVR 49.05 (pct 67; IV pct 74%); IV30 57.1–57.4%; RV21 24.0%; term 30d 57.1% → 90d 50.0% (backwardation); Oct16 chain IV ~42%. Earnings 11/02 (after Oct16). Implied move: NO DATA.

### 2.4 SPY — Oct16 778/781C (bull), 775/767P (bear) (spot 778.30 @12:56)
**Strike table (Oct16; quote NO DATA)**
| Strike | C OI | C OI chg | C Vol | C Last | C IV | C B/A % | P OI | P OI chg | P Vol | P Last | P IV | P B/A % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 764 | 2,485 | 9 | 15 | 14.98 | 13% | 67% | 4,062 | 685 | 1,590 | 0.80 | 12% | 63% |
| **767** | 7,206 | −40 | 119 | 12.54 | 11% | 61% | 9,826 | +1,540 | 1,526 | 1.09 | 11% | 72% |
| 768 | 4,197 | −25 | 76 | 11.83 | 12% | 59% | 16,595 | 290 | 2,623 | 1.26 | 11% | 45% |
| 774 | 4,779 | 746 | 513 | 7.27 | 11% | 44% | 7,573 | 384 | 2,733 | 2.49 | 10% | 50% |
| **775** | 23,112 | 1,116 | 8,117 | 6.51 | 11% | 49% | 8,689 | −1,123 | 5,431 | 2.80 | 10% | 47% |
| 776 | 5,911 | 2,694 | 8,688 | 5.80 | 11% | 56% | 2,471 | 331 | 4,301 | 3.08 | 10% | 55% |
| 777 | 4,269 | 250 | 13,820 | 5.17 | 10% | 56% | 2,135 | −176 | 8,304 | 3.49 | 9% | 54% |
| **778** | 6,334 | 569 | 3,547 | 4.60 | 10% | 46% | 2,151 | −265 | 4,402 | 3.92 | 9% | 48% |
| 779 | 3,070 | −52 | 2,286 | 4.05 | 10% | 48% | 1,364 | −514 | 1,253 | 4.38 | 9% | 67% |
| 780 | 20,909 | 1,985 | 13,922 | 3.54 | 10% | 49% | 6,928 | −592 | 2,434 | 4.89 | 9% | 48% |
| **781** | 9,780 | 355 | 1,435 | 3.05 | 10% | 42% | 917 | −53 | 68 | 5.57 | 9% | 51% |
| 782 | 5,564 | 1,473 | 2,098 | 2.63 | 10% | 56% | 576 | −431 | 70 | 5.91 | 9% | 54% |
**10-day OI per leg:** 778C 6334, 5765, 5875, 5741, 5407, 5226, 5213, 4950, 4890, 4651 (+1,683 diff). 781C 9780, 9425, 9150, 9296, 8790, 5554, 5618, 5528, 3917, 3825 (+5,955 diff; +3,236 step after 10/02). 775P 8689, 9812, 8749, 9084, 7602, 7465, 7178, 7503, 7549, 7641 (+1,048 diff; −1,123 last). 767P 9826, 8286, 7779, 7831, 7419, 7226, 6954, 6671, 6843, 6815 (+3,011 diff; **rising**, +1,540 last).
**Flow — today (floor ~$219K):** 11:09 C775 ASK $279K (vol 6,877 / OI 23,112); 10:58 C780 ASK $278K 868 @3.20 (vol 8,637 / OI 20,909); 09:55 C775 ASK $255K. No 767–775P or 778–781C prints ≥$219K; no vol>OI. Other: 12:19 765P 10/30 MID sweep $3.43M (vol 13,626 / OI 30,156). Net premium +$7.42M (calls −$1.1M, puts −$8.6M) at 12:19.
**Flow — Whale, Oct16 prints 10/01–10/09 (top 20 by premium; at/near the legs):** 10/08 15:58 778C Ask $648,120, 1,964, vol 6,253 / OI 5,765 (vol>OI). 10/02 15:44 781C Bid $585,398, 2,419, vol 4,188 / OI 5,554. 10/02 09:34 780C cross $686,000 (no side); 10/05 15:09 780C Bid $667,500 (vol 9,567 / OI 17,861). 775P: 10/06 13:06 cross $885,000 (vol 9,023 / OI 9,084); 10/08 13:12 Ask $618,000 1,000 (vol 10,357 / OI 9,812, vol>OI); 10/05 10:34 Bid $413,343; 10/01 13:05 Ask $402,840. 10/08 09:41 773P Ask $593,142. 772C repeated (Ask $1,137,500 10/07; Ask $549,000 10/05; Ask $387,100 10/09; Bid $382,200/$381,420 10/07; Bid $377,500 10/08). 770C cross $1.46M 10/01; Bid $632K/$483K 10/05. No 767P rows.
**GEX:** Live 12:56 (DTE=10): Amplifying, flip 777.19, CW 783, **PW 776**, −8.3B per 1% at spot; Σ 780 −1,478,678K, 781 −3,780K, 782 −80,034K. Live 12:19 (30D): flip 777.56, CW 787 (15.1M), **PW 777 (+1.52B)**; positive 777/776/775 (+1.52B/+931M/+398M); negative 778 −6.0B, 779 −659M, 780 −498M. Gamma tab (12:19): Long Γ/Dampening, net +$235.1K, flip 824.02, **CW = magnet 780** ($404.15K), PW 777; Summary ACCEL ↓ **767** ($161.29K).
**IV:** IVR **9.31** (pct 10; 30d 1y pct 6%); IV30 12.5%; RV21 10.0%; contango 30d 12.5% → 90d 14.0%. Implied moves: 10/12 ±0.39%, 10/13 ±0.52%, 10/14 ±0.71% (CPI day per plan), **10/16 ±0.93% ($7.25)**.

### 2.5 IBIT — Nov20 46/49C (spot 46.84 @12:56)
**Strike table (Nov20; quote NO DATA)**
| Strike | C OI | C OI chg | C Vol | C Last | C IV | C B/A % | P OI | P OI chg | P Vol | P IV |
|---|---|---|---|---|---|---|---|---|---|---|
| 45 | 27,548 | 61 | 71 | 3.53 | 40% | 54% | 16,260 | −248 | 1,397 | NO DATA (row partial) |
| **46** | 22,023 | −125 | 195 | 2.93 | 39% | 46% | 5,036 | 1,042 | 401 | 36% |
| 47 | 10,687 | 247 | 137 | 2.38 | 39% | 44% | 3,306 | −95 | 412 | 35% |
| 48 | 26,141 | 11,096 | 2,771 | 1.94 | 39% | 46% | 20,889 | 9,347 | 178 | 35% |
| **49** | 26,057 | −384 | 403 | 1.55 | 38% | 54% | 1,246 | −87 | 133 | 34% |
| 50 | 29,558 | 455 | 4,358 | 1.24 | 38% | 49% | 2,489 | 151 | 218 | 34% |
**10-day OI per leg:** 46C 22023, 22148, 22215, 22258, 22319, 22425, 22426, 22441, 22440, 22597 (**flat-to-down**, −574 diff, down in 8 of 9 updates). 49C 26057, 26441, 26820, 26534, 25935, 23775, 23698, 22515, 22473, 22047 (**up** +4,010 diff over 10d; but down the last 2 updates, 26,820 → 26,057). (Whale 13:01 showed 49C vol 863 vs page 403 at 12:59.)
**Flow 11/20 45–50 (floor ~$136K, 10/01–10/09):** 10/08 12:58 48C cross $2.43M + 48P cross $5.43M (vol>OI; both opened, side unknown). 10/02 13:55 48C ASK $1.38M (vol 5,416 / OI 10,193) + 48P BID $1.23M (vol>OI). 49C: 10/02 15:25 ASK $363K (vol 4,446 / OI 23,775); 10/02 13:15 BID $290K; 10/05 15:57 ASK $208K (49C OI 23,775 → 25,935 → 26,534 after these). 50C ASK $465K, $212K, $154K (10/02–10/06). 46C: none; 46P BID $237K 10/08. 10/09 10:37 48C BID $185K. None vol>OI at 46/49.
**Two-day context:** 10/08 15:02 read: all 6 ask-side call prints ≥$100K had vol < OI. 10/09 open (09:30–09:59): two ask calls ≥$100K, neither opened. 10/09 12:10: 4 ask calls ≥$100K, none vol>OI; Nov27 49.5C BID $704K (vol 4,400 > OI 21) and 52.5C BID $451K (5,500 > 0) = calls sold above spot, opening. Net premium −$0.51M (12:11). Bullish exception (opened 10/08): Mar27 60C/70C floor call spread (+18,079/+19,944).
**GEX:** Live (DTE=60): Amplifying, flip 46.3, CW 47.5, PW 43, −3.6M/1% at spot; Σ 50 −1,140K, 49.5 930K, 49 −391K, 48.5 −1,248K, 48 988K, 47.5 2,348K; 46 not captured. Gamma tab/magnet: NO DATA.
**IV:** IVR 7.59 (pct 13); IV30 36.3%; RV21 38.2%; contango 30d 36.2% → 90d 38.4%. Implied move: NO DATA.

### 2.6 TSLA — context only, no spread yet (spot 383.49 @12:56)
**Oct16 strike table (quote NO DATA)**
| Strike | C OI | C OI chg | C Vol | C Last | C IV | P OI | P OI chg | P Vol | P Last |
|---|---|---|---|---|---|---|---|---|---|
| 370 | 6,791 | −192 | 2,081 | 16.83 | 40% | 8,300 | −57 | 4,934 | 3.05 |
| 375 | 5,879 | 723 | 3,441 | 13.34 | 39% | 4,591 | −527 | 5,307 | 4.50 |
| 380 | 14,124 | 190 | 10,309 | 10.17 | 39% | 14,624 | −67 | 9,309 | 6.40 |
| 385 | 10,137 | 215 | **22,309** | 7.59 | 39% | 1,853 | 30 | 6,759 | 8.85 |
| 390 | 10,316 | 2,980 | 9,699 | 5.55 | 39% | 4,908 | −1 | 3,958 | 11.70 |
| 395 | 4,320 | 190 | 4,339 | 3.98 | 39% | 2,277 | −15 | 670 | 14.85 |
| 400 | 31,253 | 7,984 | 35,773 | 2.80 | 39% | 7,074 | 1 | 142 | 19.00 |
Nov20: 380C OI 5,342 / 390C 2,336 / 400C 13,853; call IV 43–44%. 392.5C not in table (OI 1,609 from flow rows).
**Flow (floor ~$807K, 10/16 & 11/20, 365–405):** 10/09: 385C BID $1.58M (vol 11,030 > OI 10,137), ASK $1.44M 2,000 @7.20 (vol 19,847 > OI, MLAT), ASK $1.06M; 392.5C MID $1.08M, ASK $1.08M, ASK $966K (all vol > OI 1,609); 380C BID $1.09M. Earlier: 10/07 375P ASK $1.7M (vol>OI); 10/05 370C ASK $1.48M (vol>OI); 10/02 11/20 400C BID $2.46M + $1.56M. Also 10/09 11/13 385C ASK $2.5M (vol 2,749 > OI 189, opening). Net premium +$31.39M (12:11).
**GEX:** Live (DTE=60, 12:56): Amplifying, **flip 381.23**, CW 390 (17.9M), PW 380 (64.8M), −181M/1% at spot; Σ 385 −97,793K, 382.5 −180,505K, 390 17,925K, 395 7,233K, 400 −7,647K. 12:11 reads: Live flip 382.21; Gamma tab flip 382.06, CW = magnet 400, PW 380; Summary accel ↓ 370.
**IV:** IVR 23.74 (pct 28); IV30 43.0%; RV21 29.7%; backwardation 30d 43.2% → 90d 40.4%. **Earnings 10/21 AMC, expected move ±6.71%** (after Oct16, before Nov20); 11/06 implied ±8.2%.

## 3. Liquidity (all legs)
| Leg | OI 10/09 | Vol today (page, ~12:58) | Bid / Ask / width |
|---|---|---|---|
| USO 11/20 150C / 155C / 160C | 5,740 / 1,490 / 2,699 | 78 / 34 / 185 | NO DATA (no UW quote; Whale did not return USO) |
| GOOGL 11/20 355C / 360C / 365C / 370C | 31,092 / 11,499 / 2,946 / 34,302 | 564 / 965 / 83 / 865 | NO DATA |
| PLTR 10/16 205C / 210C | 8,003 / 11,407 | 19,870 / 12,681 | NO DATA |
| SPY 10/16 778C / 781C / 775P / 767P | 6,334 / 9,780 / 8,689 / 9,826 | 3,553 / 1,436 / 5,447 / 1,536 | NO DATA |
| IBIT 11/20 46C / 49C | 22,023 / 26,057 | 195 / 403 | NO DATA |
Thinnest leg by both OI and volume: GOOGL 365C (2,946 OI, 83 vol) and USO 155C (1,490 OI, 34 vol).

## 4. Flow-setup history
**UW/Mr. Whale could not produce setup-history stats for any of the six tickers.** Whale's reason (USO): "The available tools lack a two-year daily USO opening ask-side call premium, volume, and OI series needed to calculate the 90th percentile, breakout-day selection, and forward returns." For GOOGL/PLTR/SPY/IBIT/TSLA: "complete two-year daily opening ask-side call premium, volume, and OI history unavailable"; every count, hit rate, median return and base rate = NO DATA. **n = 0 for all setups.**

Closest real evidence from past files (partial substitutes only):
| Evidence | Source | n | Finding | Caveats |
|---|---|---|---|---|
| GOOG/GOOGL large call flow vs 200DMA tests, 8/24–10/07 | plans/20261008-goog-uso-mu-watch/uw-goog-flow-trend.md | 7 test days in 4 windows (32 sessions) | Ask-side directional calls ≥$500K were heavy only after the 9/9–9/11 tests ($16.6M/22 prints 9/11, $24.9M/20 on 9/14 vs $5.3M/day outside windows). After the 9/1–2, 9/23 and 10/1 tests large calls leaned bid (ask $17.4M/$18.8M/$16.8M vs bid $23.2M/$29.4M/$37.6M). Biggest Nov structures (370/440C 9/08; 355/420C roll 9/28; 380/435C 10/05) opened next to tests, side mostly NONE | Describes flow, **not forward returns**; test levels from a brief; prints ≥$500K only; multi-leg sides ambiguous; all-UW sources. Different trigger (200DMA test, ~338) from today's 350.09 breakout |
| USO big dark-pool days vs forward returns, 2024-10-01 to 2026-10-06 | plans/20261008-goog-uso-mu-watch/uw-uso-dp-history.md | 75 day events (65 with 20d window); base 506 days | **No edge vs base rate:** median 1/5/20d +0.19%/−0.21%/+2.13% vs base +0.09%/+0.29%/+1.16%; 2026-only events +6.30% vs base +8.53% at 20d; permutation shares 0.19–0.75 (no signal). Hold/revisit ≈ chance (held 5d 26% vs 31% expected) | Sampled prints with changing $ floors; event counts skew to 2026 (59/75); price returns came from Yahoo/yfinance in that job (not UW); dark-pool, not options flow |
| USO 10/07 prints opened as sold calls | plans/20261008-goog-uso-mu-watch/uw-uso-1008.md | 1 episode | Nov 153C BID 3,350 opened (OI 3,573 → 7,154); 10/16 151C ask buy closed (−2,148); Jan27 200C (+457), Nov 130C (+278), Jan27 146C (+126) opened as sold = overwriting/supply above spot | Side+OI inference; one episode, no outcome stats. Build continued to 8,954 (10/09) |

## 5. Gaps
- Bid/ask/mid/width: NO DATA for every leg (UW pages show no live quote; Whale returned NO DATA, errored once).
- Setup-history stats: NO DATA for all six (Whale lacks 2y daily ask-side premium/vol/OI series).
- Flow lists cut at top ~250 by premium (per-ticker floors above); SPY today-only list in the part file (10/01–10/08 from Whale's top-20 only).
- Opening/closing for today's prints unknown until Monday's OI update (except vol>OI).
- Gamma tab/magnet not read in this job for SPY/IBIT/TSLA (SPY and TSLA Gamma-tab levels from the 12:1x reads; IBIT NO DATA). Gamma tab has no DTE control.
- GEX strikes not captured: USO 160; SPY 767–779 at 12:56 (12:19 read covers 769–790); IBIT 46; TSLA 370.
- Implied move to the spread expiry: NO DATA for USO Nov20, GOOGL, PLTR, IBIT; only SPY 10/16 (±0.93%) and TSLA earnings (±6.71%) / 11/06 (±8.2%).
- Per-expiry IV beyond 30d/90d: NO DATA.
- USO contract-page volume/OI not returned by Whale (page OI used). GOOGL 370C OI history has ±9K swings; GOOGL 355C 09/28 OI 1,873 then 29,874 (cross).
- IBIT 45 row partial (put IV missing); PLTR 207.5/212.5 not in the part-file table (12:18 OI used).
- TSLA: no spread defined, so no leg OI/GEX-vs-strike read.

Raw part files copied to inputs/uw_raw/ (source: /workspace/uw/tmp/UW-20261009-05/).
