# Brief for an independent critic (prepared for a Fable 5.1 cloud agent; NOT launched: no CloudAgent tool in this Planner executor session)
Task: critique Planner's MU day-1 (first session after an after-close earnings print) backtest for overfitting and methodology errors; propose/verify at most 2-3 rule refinements. Write findings to CRITIC_FINDINGS.md.
Data: day1_planner.csv (98 MU prints 2001-12 .. 2026-06; yfinance unadjusted daily + 1h for 2023-10+).
Scripts: build_dataset.py, bt_planner_thu.py (pre-declared rules R0-R5), robust.py, placebo.py, grid.py (options), refine_timestop.py.
Headline to attack: R0 "short at day-1 open, 3% hard stop, cover at close" = +0.33R (+0.99%/trade), n=98, 90% CI +0.14..+0.53R,
both eras positive, walk-forward +0.32R, placebo on non-earnings days -0.06R. Options (Oct 2 put debit spreads) do NOT survive natural fills.
Questions: (1) any look-ahead / survivorship / date errors? (2) is touch=stop conservative enough? (3) is the open print attainable?
(4) is the earnings-day negative intraday drift a known effect (literature) or a yfinance artifact? (5) better defined-risk expression for an $8k account?
