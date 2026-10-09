# UW_tsla_asof.md — TSLA as of Thu 2026-10-08 13:35 ET (UW-20261009-06)
For Planner's blind test (Dominic calibration). Pulled Fri 10/09 13:12–13:16 ET from Unusual Whales, filtered to Oct 8 09:30–13:35 ET.
**As-of discipline:** everything in this file was known by 13:35 ET on Oct 8. No later data is included, and there are no GEX levels from after the cutoff. Lookahead references were kept out of this file on purpose.
Expiry note: the 10/09 expiry was **1DTE** on Oct 8. **There is no Oct 10 expiry** (Saturday); the chain lists 10/09, 10/12, 10/14 and 10/16.

## Summary (as of 13:35)
- **1DTE (10/09) flow at 365–375 was opening,** with vol > OI at most strikes from 367.5 to 375. It was two-sided.
  - Put buying near the level: 370P bought at the ask, $484K (12:53; vol 76,028 vs OI 8,562).
  - Calls sold above it: 372.5C sold at the bid, $453K (10:29; vol 18,874 vs OI 13,078); 367.5C sold at the bid, $308K (vol > OI); 370C sold at the bid, $280K; 375C sold at the bid, $276K. There was also a 372.5C bought at the ask for $287K.
  - The 10/09 377.5P was sold at the bid for $509K (09:37; vol 2,414 vs OI 5,854).
- **13:20–13:35 tape on the 10/09 365–385 strikes:** 6,793 prints, with vol > OI on all the active contracts.
  - 370C: 3,908 contracts (~$1.15M), net sold (2,028 at the bid vs 1,438 at the ask).
  - 370P: 3,076 contracts (~$1.06M), about even.
  - 365P: 4,500 contracts, net sold (2,574 at the bid vs 1,582 at the ask), which is mild support for the level holding.
  - 377.5C: 3,189 contracts, mostly bought at the ask (upside calls bought into the test).
  - Full table below.
- **10/16 flow:** smaller and mixed.
  - 375P bought at the ask, $353K (09:43).
  - 380C at MID, $281K.
  - 370C traded about $100K each both ways from 11:46 to 13:33.
  - 365P sold at the bid, $114K (12:59).
- **OI at the start of Oct 8** (= the 10/07 close, known at the cutoff):
  - 10/09: the heaviest put OI is at 370 (8,562) and 365 (5,276); call OI is stacked at 375–390 (10.8K–15.7K).
  - 10/16: 380 is the big two-sided strike (13,934 calls / 14,691 puts); 370 has 6,983 calls / 8,357 puts.
- **GEX as of 13:35 Oct 8: NO DATA.** UW's historical view of Oct 8 is the end-of-day snapshot (as of 16:00), which is after the cutoff. The intraday exposure chart doesn't give strike-level flip or walls. The OI-based levels could in principle be rebuilt from the Oct 8 OI below plus spot ~370 and IV, but that wasn't attempted.
- **IV per print: NO DATA.** UW's flow table doesn't show IV; its % column is the bid/ask split.

## OI dated 10/08 (start of day; OI reflects the 10/07 close)
| expiry | 365 C / P | 370 C / P | 375 C / P | 380 C / P | 385 C / P | 390 C / P |
|---|---|---|---|---|---|---|
| 10/09 | 2,045 / 5,276 | 4,967 / 8,562 | 10,817 / 3,694 | 11,133 / 3,224 | 11,441 / 2,624 | 15,671 / 668 |
| 10/16 | 4,973 / 4,180 | 6,983 / 8,357 | 5,156 / 5,118 | 13,934 / 14,691 | 9,922 / 1,823 | 7,336 / 4,909 |
These match the OI shown on the Oct 8 flow rows. The earlier days (10/05–10/07) are in the raw oi.md.

## Gaps and caveats
- Flow lists show only the top 250 by premium per window. For 365–390, coverage is prints of at least ~$83–88K. The 13:20–13:35 file has no premium floor (complete for 10/09 365–385).
- The site's aggregated-trades view was used.
- A few rows in the 13:20–13:35 raw file didn't parse cleanly; they're kept as raw text.
- Opening vs closing for individual prints is inferred from vol > OI only.
- No option quotes (bid/ask) as of 13:35, only the bid-ask shown on each print.
- No GEX and no IV as of the cutoff.

---
# Raw (as-of only)

<!-- prints-1325.md: summary by contract -->
# prints-1325.md — TSLA 10/09/26 expiry, strikes 365-385, 13:20:00-13:35:00 ET Oct 8 (no min premium)
Source: live-options-flow, order=Time, limit=250, URL filters expiry_dates[]=2026-10-09&min_strike=365&max_strike=385&min_premium=0, paged by older_than (24 pages of 250). Raw rows in p_chunk*.json.
Dedup: page boundaries overlapped by 1s; duplicates removed by max-count per identical row string (genuinely identical prints within the same second at a boundary may be undercounted slightly).
IV: NOT shown per print in the flow table (the % column is Chain Bid/Ask side %, not IV). No hover IV captured.
Total prints: 6793 (dedup: at each page boundary the cut-off second is taken only from the next page, which queried older_than=that second+1s, so no loss/duplication expected)


## Summary by contract (13:20-13:35; premium computed = price*size*100)
| strike | C/P | prints | contracts | premium $ | ask sz | bid sz | mid sz | no-side sz | vol at first->last print | OI |
|---|---|---|---|---|---|---|---|---|---|---|
| 365 | C | 62 | 321 | 194,203 | 229 | 88 | 4 | 0 | 4,921->5,241 | 2,045 |
| 365 | P | 924 | 4500 | 694,322 | 1582 | 2574 | 344 | 0 | 26,616->31,115 | 5,276 |
| 367.5 | C | 279 | 1320 | 569,534 | 529 | 570 | 221 | 0 | 3,895->5,205 | 1,393 |
| 367.5 | P | 1117 | 3339 | 785,881 | 1476 | 1524 | 339 | 0 | 37,245->40,574 | 2,599 |
| 370 | C | 780 | 3908 | 1,154,271 | 1438 | 2028 | 442 | 0 | 17,832->21,939 | 4,967 |
| 370 | P | 980 | 3076 | 1,062,485 | 1482 | 1360 | 234 | 0 | 85,261->88,336 | 8,562 |
| 372.5 | C | 636 | 3387 | 652,593 | 1461 | 1656 | 270 | 0 | 52,341->55,758 | 13,078 |
| 372.5 | P | 251 | 845 | 414,242 | 380 | 301 | 164 | 0 | 50,351->51,194 | 3,025 |
| 375 | C | 580 | 2594 | 316,690 | 1254 | 1010 | 330 | 0 | 69,912->72,456 | 10,817 |
| 375 | P | 122 | 845 | 574,884 | 441 | 355 | 49 | 0 | 24,846->25,688 | 3,694 |
| 377.5 | C | 404 | 3189 | 231,781 | 1884 | 1150 | 155 | 0 | 38,820->42,076 | 6,493 |
| 377.5 | P | 36 | 218 | 189,971 | 146 | 71 | 1 | 0 | 7,676->7,893 | 5,854 |
| 380 | C | 350 | 1781 | 77,111 | 627 | 1092 | 62 | 0 | 48,224->50,004 | 11,133 |
| 380 | P | 25 | 44 | 48,066 | 18 | 17 | 9 | 0 | 9,259->9,302 | 3,224 |
| 382.5 | C | 116 | 538 | 13,586 | 196 | 341 | 1 | 0 | 19,002->19,538 | 12,197 |
| 382.5 | P | 4 | 9 | 11,566 | 2 | 7 | 0 | 0 | 748->756 | 2,247 |
| 385 | C | 122 | 428 | 6,614 | 272 | 149 | 7 | 0 | 18,319->18,742 | 11,441 |
| 385 | P | 3 | 9 | 14,421 | 9 | 0 | 0 | 0 | 1,803->1,811 | 2,624 |


<!-- flow.md -->
# flow.md — TSLA live options flow, Oct 8 2026 09:30-13:35 ET, sorted by premium, limit 250

Full-window URL (newer_than=1791466200000&older_than=1791480900000) returned 250 rows (limit hit; all dated 10/08, 09:30:32-13:32:05). Cutoff (smallest visible) premium in full window: $162K. Therefore split:
- W1 09:30-11:30 (older_than=1791473400000): 250 rows, all 10/08, 09:30:12-11:29:06, cutoff premium $88K (limit hit again).
- W2 11:30-13:35: 250 rows, all 10/08, 11:30:36-13:34:33, cutoff premium $83K (limit hit again).
=> Lists below are COMPLETE only for prints >= ~$88K (W1) / >= ~$83K (W2); smaller prints are not captured here (see prints-1325.md for complete 13:20-13:35 0DTE). No 10/10/2026 expiry appears in any row (none listed; Saturday). Default UW flow view (aggregated trades on, add_agg_trades=true).
Volume/OI are as displayed on the row at print time. Codes: SL=single leg, ML-O=multileg; AGG*=aggregated, AUTO/SLAN/MLET/MLAT = condition codes.

## W1 09:30-11:30: 10/09 & 10/16 expiry, strikes 365-390
| time | expiry | strike | C/P | side | premium | size | price | bid-ask | spot | volume | OI | vol>OI | code/flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 09:37:29 | 10/09/2026 | 377.5 | P | BID | $509K | 970 | 5.25 | 5.25-5.35 | 374.47 | 2,414 | 5,854 |  | SL AGG* |
| 10:29:19 | 10/09/2026 | 372.5 | C | BID | $453K | 1,277 | 3.55 | 3.45-3.65 | 372.99 | 18,874 | 13,078 | **YES** | SL AGG* |
| 09:43:22 | 10/16/2026 | 375 | P | ASK | $353K | 413 | 8.55 | 8.45-8.60 | 375.30 | 1,380 | 5,118 |  | SL AGG* |
| 10:08:10 | 10/09/2026 | 367.5 | C | BID | $308K | 450 | 6.85 | 6.85-6.95 | 372.97 | 1,602 | 1,393 | **YES** | SL AUTO |
| 09:33:46 | 10/16/2026 | 380 | C | MID | $281K | 450 | 6.25 | 6.25-6.35 | 373.57 | 804 | 13,934 |  | SL AGG* |
| 09:51:09 | 10/09/2026 | 375 | C | BID | $276K | 919 | 3.00 | 2.97-3.10 | 373.67 | 17,657 | 10,817 | **YES** | SL AGG* |
| 09:42:36 | 10/09/2026 | 377.5 | P | NONE | $275K | 520 | 5.29 | 5.15-5.45 | 374.31 | 4,154 | 5,854 |  | SL AGG* |
| 09:40:48 | 10/09/2026 | 377.5 | P | ASK | $239K | 503 | 4.75 | 4.65-4.85 | 375.64 | 3,256 | 5,854 |  | SL AGG* |
| 10:22:41 | 10/09/2026 | 370 | C | BID | $202K | 424 | 4.77 | 4.65-4.80 | 372.44 | 5,996 | 4,967 | **YES** | SL AGG* |
| 09:43:22 | 10/16/2026 | 377.5 | C | ASK | $200K | 247 | 8.10 | 7.95-8.15 | 375.27 | 627 | 1,290 |  | SL AGG* |
| 09:59:29 | 10/09/2026 | 385 | P | BID | $174K | 131 | 13.30 | 13.30-13.35 | 372.05 | 740 | 2,624 |  | SL AGG* |
| 10:23:20 | 10/09/2026 | 372.5 | C | ASK | $170K | 500 | 3.40 | 3.30-3.40 | 372.46 | 16,542 | 13,078 | **YES** | SL AGG* |
| 09:39:06 | 10/09/2026 | 370 | P | BID | $161K | 1,006 | 1.60 | 1.59-1.64 | 375.22 | 10,453 | 8,562 | **YES** | SL AGG* |
| 09:37:28 | 10/09/2026 | 375 | P | BID | $161K | 423 | 3.80 | 3.70-3.95 | 374.73 | 4,121 | 3,694 | **YES** | SL AGG* |
| 10:32:00 | 10/09/2026 | 372.5 | C | ASK | $159K | 453 | 3.50 | 3.45-3.55 | 373.04 | 19,626 | 13,078 | **YES** | SL AGG* |
| 10:23:53 | 10/09/2026 | 372.5 | C | BID | $151K | 464 | 3.25 | 3.20-3.30 | 372.24 | 17,102 | 13,078 | **YES** | SL AGG* |
| 09:30:50 | 10/09/2026 | 375 | P | ASK | $145K | 325 | 4.45 | 4.25-4.50 | 373.98 | 781 | 3,694 |  | SL AGG* |
| 09:54:48 | 10/09/2026 | 367.5 | C | BID | $142K | 219 | 6.50 | 6.45-6.60 | 372.19 | 818 | 1,393 |  | SL AGG* |
| 09:53:43 | 10/09/2026 | 372.5 | P | ASK | $141K | 403 | 3.51 | 3.45-3.60 | 372.34 | 15,242 | 3,025 | **YES** | SL AGG* |
| 09:37:04 | 10/09/2026 | 375 | C | ASK | $141K | 408 | 3.46 | 3.35-3.60 | 374.50 | 4,588 | 10,817 |  | SL AGG* |
| 10:29:18 | 10/09/2026 | 367.5 | C | BID | $139K | 205 | 6.80 | 6.80-7.00 | 372.89 | 1,920 | 1,393 | **YES** | SL AGG* |
| 10:28:23 | 10/09/2026 | 370 | C | ASK | $138K | 284 | 4.85 | 4.75-4.85 | 372.60 | 6,729 | 4,967 | **YES** | SL AGG* |
| 10:41:29 | 10/09/2026 | 370 | C | MID | $123K | 225 | 5.45 | 5.40-5.50 | 373.69 | 7,877 | 4,967 | **YES** | ML-O MLAT |
| 09:30:12 | 10/16/2026 | 375 | P | ASK | $121K | 123 | 9.80 | 9.50-10.00 | 373.45 | 160 | 5,118 |  | SL AGG* |
| 10:42:33 | 10/09/2026 | 385 | P | ASK | $117K | 100 | 11.70 | 11.25-11.90 | 373.78 | 1,028 | 2,624 |  | SL AUTO |
| 10:40:03 | 10/09/2026 | 375 | C | BID | $111K | 409 | 2.71 | 2.69-2.75 | 373.84 | 37,927 | 10,817 | **YES** | SL AGG* |
| 09:52:19 | 10/09/2026 | 367.5 | P | ASK | $109K | 730 | 1.49 | 1.45-1.50 | 372.79 | 8,900 | 2,599 | **YES** | SL AGG* |
| 09:40:42 | 10/09/2026 | 380 | C | ASK | $101K | 504 | 2.01 | 1.96-2.07 | 375.28 | 7,521 | 11,133 |  | SL AGG* |
| 10:33:22 | 10/09/2026 | 370 | C | BID | $101K | 200 | 5.06 | 5.05-5.10 | 373.11 | 7,208 | 4,967 | **YES** | SL AGG* |
| 09:55:12 | 10/09/2026 | 370 | P | BID | $100K | 422 | 2.36 | 2.33-2.41 | 372.55 | 24,264 | 8,562 | **YES** | SL AGG* |
| 09:50:04 | 10/09/2026 | 370 | C | ASK | $99K | 175 | 5.65 | 5.50-5.65 | 373.28 | 2,144 | 4,967 |  | SL AGG* |
| 09:38:24 | 10/09/2026 | 370 | P | BID | $99K | 530 | 1.86 | 1.84-1.90 | 374.42 | 9,206 | 8,562 | **YES** | SL AGG* |
| 09:40:11 | 10/09/2026 | 375 | C | ASK | $98K | 242 | 4.07 | 4.00-4.15 | 375.46 | 8,911 | 10,817 |  | SL AGG* |
| 10:45:21 | 10/09/2026 | 372.5 | P | ASK | $97K | 346 | 2.80 | 2.78-2.84 | 372.91 | 29,485 | 3,025 | **YES** | SL AGG* |
| 10:11:38 | 10/16/2026 | 387.5 | C | BID | $95K | 272 | 3.50 | 3.50-3.55 | 372.27 | 467 | 1,582 |  | SL AUTO |
| 09:31:16 | 10/09/2026 | 375 | P | BID | $94K | 216 | 4.35 | 4.25-4.40 | 373.95 | 1,410 | 3,694 |  | SL AGG* |
| 09:41:01 | 10/09/2026 | 377.5 | C | BID | $89K | 292 | 3.06 | 2.89-3.20 | 375.34 | 5,870 | 6,493 |  | SL AGG* |
| 10:33:58 | 10/09/2026 | 370 | P | BID | $88K | 519 | 1.70 | 1.70-1.73 | 373.32 | 48,641 | 8,562 | **YES** | SL AGG* |

## W2 11:30-13:35: 10/09 & 10/16 expiry, strikes 365-390
| time | expiry | strike | C/P | side | premium | size | price | bid-ask | spot | volume | OI | vol>OI | code/flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 12:53:01 | 10/09/2026 | 370 | P | ASK | $484K | 2,007 | 2.41 | 2.39-2.42 | 371.39 | 76,028 | 8,562 | **YES** | SL AGG* |
| 12:39:41 | 10/09/2026 | 372.5 | C | ASK | $287K | 910 | 3.15 | 3.05-3.15 | 372.72 | 40,308 | 13,078 | **YES** | SL AGG* |
| 11:52:46 | 10/09/2026 | 370 | C | BID | $280K | 650 | 4.30 | 4.30-4.35 | 372.17 | 11,441 | 4,967 | **YES** | SL AGG* |
| 11:37:54 | 10/09/2026 | 372.5 | P | ASK | $263K | 823 | 3.20 | 3.10-3.25 | 372.08 | 37,453 | 3,025 | **YES** | SL AGG* |
| 12:10:57 | 10/09/2026 | 380 | P | ASK | $203K | 248 | 8.20 | 8.00-8.30 | 372.32 | 7,814 | 3,224 | **YES** | SL AGG* |
| 12:10:57 | 10/09/2026 | 372.5 | P | ASK | $158K | 536 | 2.95 | 2.90-2.95 | 372.42 | 40,307 | 3,025 | **YES** | SL AGG* |
| 11:34:03 | 10/09/2026 | 370 | C | MID | $119K | 267 | 4.45 | 4.40-4.50 | 372.20 | 9,970 | 4,967 | **YES** | SL AGG* |
| 13:11:12 | 10/09/2026 | 370 | P | ASK | $118K | 394 | 3.00 | 2.96-3.05 | 370.11 | 82,555 | 8,562 | **YES** | SL AGG* |
| 12:59:21 | 10/16/2026 | 365 | P | BID | $114K | 206 | 5.55 | 5.55-5.65 | 371.36 | 1,034 | 4,180 |  | SL AGG* |
| 12:20:15 | 10/16/2026 | 370 | C | ASK | $105K | 100 | 10.51 | 10.45-10.55 | 373.14 | 3,531 | 6,983 |  | SL SLAN |
| 12:20:37 | 10/16/2026 | 370 | C | BID | $105K | 100 | 10.51 | 10.45-10.60 | 373.21 | 3,631 | 6,983 |  | SL SLAN |
| 11:52:41 | 10/09/2026 | 367.5 | P | ASK | $105K | 852 | 1.23 | 1.22-1.25 | 372.13 | 29,050 | 2,599 | **YES** | SL AGG* |
| 13:11:19 | 10/09/2026 | 385 | P | ASK | $101K | 68 | 14.91 | 14.50-15.20 | 370.08 | 1,802 | 2,624 |  | ML-O MLET |
| 11:47:23 | 10/16/2026 | 370 | C | MID | $100K | 100 | 10.00 | 9.95-10.05 | 372.28 | 3,166 | 6,983 |  | SL AGG* |
| 11:46:57 | 10/16/2026 | 370 | C | ASK | $100K | 100 | 9.98 | 9.90-10.05 | 372.26 | 3,055 | 6,983 |  | SL SLAN |
| 13:33:33 | 10/16/2026 | 370 | C | ASK | $90K | 100 | 9.00 | 8.90-9.00 | 370.07 | 5,132 | 6,983 |  | SL AGG* |
| 13:33:11 | 10/16/2026 | 370 | C | ASK | $89K | 100 | 8.85 | 8.80-8.85 | 369.94 | 5,020 | 6,983 |  | SL AGG* |
| 12:52:28 | 10/09/2026 | 372.5 | C | BID | $84K | 306 | 2.73 | 2.70-2.79 | 371.51 | 42,713 | 13,078 | **YES** | SL AGG* |
| 13:27:02 | 10/09/2026 | 375 | P | ASK | $83K | 111 | 7.51 | 7.45-7.65 | 368.25 | 25,477 | 3,694 | **YES** | SL AGG* |

## Top 10 TSLA prints by premium, full window 09:30-13:35
| time | expiry | strike | C/P | side | premium | size | price | bid-ask | spot | volume | OI | vol>OI | code/flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 12:56:56 | 01/21/2028 | 300 | C | ASK | $2.43M | 199 | 122.30 | 121.90-122.30 | 371.24 | 206 | 4,749 |  | SL AUTO |
| 11:02:07 | 11/20/2026 | 350 | C | BID | $1.06M | 300 | 35.33 | 35.00-35.75 | 372.65 | 317 | 16,966 |  | SL AGG* |
| 09:40:03 | 06/17/2027 | 490 | C | ASK | $1.05M | 425 | 24.80 | 24.25-24.80 | 375.28 | 425 | 1,913 |  | SL AGG* |
| 13:04:03 | 11/20/2026 | 350 | C | ASK | $1.02M | 300 | 33.88 | 33.50-34.10 | 370.68 | 651 | 16,966 |  | SL AGG* |
| 09:36:01 | 01/19/2029 | 330 | P | BID | $1M | 168 | 59.79 | 59.10-60.80 | 373.36 | 168 | 314 |  | ML-O MLET |
| 12:25:44 | 10/23/2026 | 380 | C | BID | $998K | 815 | 12.25 | 12.25-12.35 | 373.21 | 1,065 | 2,405 |  | SL AGG* |
| 09:36:01 | 01/19/2029 | 320 | P | ASK | $926K | 168 | 55.14 | 54.10-55.90 | 373.36 | 213 | 128 | **YES** | ML-O MLET |
| 09:56:40 | 10/12/2026 | 370 | P | ASK | $778K | 2,191 | 3.55 | 3.40-3.55 | 372.49 | 3,335 | 1,355 | **YES** | SL AGG* |
| 12:17:11 | 12/18/2026 | 370 | C | ASK | $672K | 231 | 29.10 | 28.80-29.55 | 372.73 | 415 | 3,875 |  | SL AGG* |
| 11:41:01 | 10/09/2026 | 160 | C | BID | $658K | 31 | 212.30 | 211.75-213.30 | 371.98 | 122 | 0 | **YES** | ML-O MLAT |

<!-- oi.md -->
# oi.md — TSLA OI dated 10/08/2026 (start of day = 10/07 close settlement), from contract pages
Source: https://unusualwhales.com/flow/option_chains?chain=<OCC> ("Historical Volume / OI" table; chain page links redirect here). Format: OI (day change vs prior row).
ONLY OI recorded. The 10/08 row on these pages also shows full-day 10/08 volume/close/avg/premium — that is LOOKAHEAD (after 13:35) and was deliberately NOT recorded. 10/09 rows not recorded.
Cross-check: 10/08 OI values match the OI shown on Oct 8 flow rows (e.g. 370C 4,967; 370P 8,562; 375C 10,817; 380C 16-Oct 13,934). No 10/10/2026 expiry is listed on the chain (expiries: 10/09, 10/12, 10/14, 10/16...).

| expiry | strike | C/P | OI 10/08 | OI 10/07 | OI 10/06 | OI 10/05 |
|---|---|---|---|---|---|---|
| 10/09 | 365 | C | 2,045 (-112) | 2,157 | 2,215 | 2,427 |
| 10/09 | 365 | P | 5,276 (+1,378) | 3,898 | 3,920 | 2,284 |
| 10/09 | 370 | C | 4,967 (-377) | 5,344 | 4,693 | 4,061 |
| 10/09 | 370 | P | 8,562 (+2,139) | 6,423 | 5,996 | 3,873 |
| 10/09 | 375 | C | 10,817 (+2,359) | 8,458 | 8,666 | 7,698 |
| 10/09 | 375 | P | 3,694 (+497) | 3,197 | 2,216 | 1,148 |
| 10/09 | 380 | C | 11,133 (+3,559) | 7,574 | 7,080 | 5,918 |
| 10/09 | 380 | P | 3,224 (-114) | 3,338 | 2,598 | 945 |
| 10/09 | 385 | C | 11,441 (+2,615) | 8,826 | 7,500 | 7,643 |
| 10/09 | 385 | P | 2,624 (+1,192) | 1,432 | 677 | 286 |
| 10/09 | 390 | C | 15,671 (+2,217) | 13,454 | 11,342 | 9,145 |
| 10/09 | 390 | P | 668 (-46) | 714 | 378 | 280 |
| 10/16 | 365 | C | 4,973 (+76) | 4,897 | 5,068 | 5,021 |
| 10/16 | 365 | P | 4,180 (-255) | 4,435 | 4,265 | 3,875 |
| 10/16 | 370 | C | 6,983 (-93) | 7,076 | 7,125 | 6,832 |
| 10/16 | 370 | P | 8,357 (-234) | 8,591 | 7,548 | 7,573 |
| 10/16 | 375 | C | 5,156 (+205) | 4,951 | 5,090 | 5,278 |
| 10/16 | 375 | P | 5,118 (+1,541) | 3,577 | 3,598 | 3,249 |
| 10/16 | 380 | C | 13,934 (+959) | 12,975 | 12,686 | 11,917 |
| 10/16 | 380 | P | 14,691 (+464) | 14,227 | 13,545 | 11,815 |
| 10/16 | 385 | C | 9,922 (+2,003) | 7,919 | 7,375 | 3,972 |
| 10/16 | 385 | P | 1,823 (-29) | 1,852 | 1,606 | 1,587 |
| 10/16 | 390 | C | 7,336 (+9) | 7,327 | 6,915 | 5,827 |
| 10/16 | 390 | P | 4,909 (+532) | 4,377 | 4,350 | 4,374 |
