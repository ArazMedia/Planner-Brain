# SUMMARY_FOR_ARAZ: EV 10/9 (proposal only; no orders). Ranked by the conservative EV = min(history EV, drift-neutral EV).
Inputs missing at finalize: none. Full detail: /workspace/plans/20261009-ev/outputs/EV.md

1. TSLA Oct16 385/390C | grade B | EV +$40 (+17% of debit $233; drift-neutral +$18) | p(target) 44% (mkt 34%) | WATCH | trigger 15m close >386.82 holding VWAP (fail: 15m close <381, hard 1h <380); RA spread, skip if full > ~$260; CPI inside, ER 10/21 after expiry
2. USO Nov20 150/160C | grade C | EV +$68 (+20% of debit $338; drift-neutral +$12) | p(target) 20% (mkt 10%) | WATCH | trigger daily close >148.07 (fail: daily close <147.12)
3. PLTR Oct16 205/210C | grade B | EV +$3 (+1% of debit $220; drift-neutral +$32) | p(target) 25% (mkt 25%) | SKIP | trigger hold >204.4 (fail: 4h close <204.42; modelled as daily close); target 207.5-210
4. SPY Oct16 778/781C (bull) | grade C | EV +$22 (+13% of debit $165; drift-neutral -$7) | p(target) 49% (mkt 39%) | SKIP | trigger DAILY close >779.27 (RA v2: a 4h/intraday poke is not enough; PA: >1x vol) (fail: close <774.90); CPI 10/14 inside
5. GOOGL Nov20 360/370C | grade D | EV +$65 (+17% of debit $392; drift-neutral -$8) | p(target) 34% (mkt 24%) | SKIP | trigger GOOGL daily close >353.22 (PA native; = GOOG 350.09); fail GOOGL close <341.38; ER + FOMC 10/28 inside
6. IBIT Nov20 46/49C | grade D | EV +$1 (+1% of debit $137; drift-neutral -$9) | p(target) 22% (mkt 20%) | SKIP | trigger 15m close >47.16 w/ BTC >82,714 (stop: close -2.75% = IBIT ~45.53 / BTC 80,526, PA def; setup-invalid 46.25)
7. GOOGL Nov20 355/365C | grade C | EV +$60 (+14% of debit $438; drift-neutral -$10) | p(target) 36% (mkt 26%) | SKIP | trigger GOOGL daily close >353.22 (PA native; = GOOG 350.09); fail GOOGL close <341.38; ER + FOMC 10/28 inside
8. PLTR Nov20 200/210C | grade B | EV -$17 (-4% of debit $490; drift-neutral +$30) | p(target) 10% (mkt 11%) | SKIP | trigger hold >204.4 (fail: 4h close <204.42, modelled as daily close); PLTR ER (Nov 2 or 9) INSIDE expiry
9. USO Nov20 150/155C | grade D | EV +$6 (+3% of debit $192; drift-neutral -$19) | p(target) 21% (mkt 11%) | SKIP | trigger daily close >148.07 (fail: daily close <147.12)
10. SPY Oct16 775/767P (bear) | grade C | EV -$45 (-19% of debit $243; drift-neutral -$3) | p(target) 13% (mkt 21%) | SKIP | trigger DAILY close <774.90 (RA v2) (fail: close >779.27, PA def); CPI 10/14 inside

