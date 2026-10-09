# RA appendix: market-implied probabilities (CBOE chain only)
Written 2026-10-09 ~12:56 ET by RA. Script: `scripts/mkt_probs.py`. CSV: `inputs/RA_mkt_probs.csv`.

**Method:**
- P(S_T > K) = N(d2), lognormal, r = 4%, no dividends, using each strike's own CBOE IV (interpolated between listed strikes).
- Spot is the **price embedded in the CBOE delayed chain**.
- T is measured from the chain quote time (CBOE timestamp − 15 min) to 16:00 ET on expiry.
- Chains were pulled 12:47 ET (USO/GOOGL/PLTR/SPY, quotes ≈12:32) and 12:53 ET (IBIT/TSLA, quotes ≈12:38). Files are in `/workspace/plans/20261008-goog-uso-mu-watch/data/1247/`.

**Caveats:**
- These are risk-neutral, **unconditional** (measured from the current price, not from the trigger) and **at expiry**. They are not touch probabilities.
- N(d2) with the strike's own IV ignores the skew slope, so downside-strike probabilities are slightly understated.
- At fair value the spread is worth ≈ mid. Market EV at the full-spread debit ≈ (mid − full) before exit costs. That's the "EV vs mid" column.

| Spread | Spot | Full-spread debit | BE (full spread) | P(max) | P(>BE) profit | P(full loss) | Target p (at expiry) | EV vs mid | Leg OI |
|---|---|---|---|---|---|---|---|---|---|
| USO Nov20 150/155C | 148.05 | $225 | 152.25 | 0.365 | 0.410 | 0.552 | >150.67 0.436; >154 0.381 | −$32.5 | 5,740/1,490 |
| USO Nov20 150/160C | 148.05 | $365 | 153.65 | 0.294 | 0.387 | 0.552 | >154 0.381; >163.49 0.250 | −$27.5 | 5,740/2,699 |
| GOOGL Nov20 355/365C | 354.11 | $460 | 359.60 | 0.391 | 0.440 | 0.516 | >359.98 0.437; >370.89 0.340 | −$22.5 | 31,092/2,946 |
| GOOGL Nov20 360/370C | 354.11 | $420 | 364.20 | 0.347 | 0.398 | 0.563 | >370.89 0.340 | −$27.5 | 11,499/34,302 |
| PLTR Oct16 205/210C | 205.94 | $230 | 207.30 | 0.362 | 0.449 | 0.475 | >207.5 0.442; >210 0.362 | −$10.0 | 8,003/11,407 |
| PLTR Nov20 200/210C | 205.94 | $505 | 205.05 | 0.431 | 0.482 | 0.465 | >210 0.431 | −$15.0 | 12,744/7,776 |
| SPY Oct16 778/781C | 778.11 | $154 | 779.54 | 0.410 | 0.466 | 0.476 | >780 0.448; >781.62 0.386 | −$2.0 | 6,334/9,780 |
| SPY Oct16 775/767P | 778.11 | $172 | 773.28 | 0.172 | 0.317 | 0.630 | <770 0.231; <767 0.172 | −$1.5 | 8,689/9,826 |
| IBIT Nov20 46/49C | 46.82 | $139 | 47.39 | 0.348 | 0.451 | 0.455 | – | −$2.0 | 22,023/26,057 |
| TSLA Oct16 385/390C | 382.795 | $205 | 387.05 | 0.359 | 0.413 | 0.548 | >386.82 0.417; >388.55 0.385; >390 0.359 | −$10.0 | 10,137/10,316 |

**Note on the full-spread debits:**
- The full-spread debits and breakevens here come from the 12:32/12:38 quotes. They differ slightly from `02_plan.md` (mid debits) and the options-prep file.
- USO 150/155 is now $225 full spread vs $192.50 mid.
- IBIT is $139 vs ~$138.
- Planner should use one quote time consistently.
