# VIX-spike long call, hedged: entry, stop, structure (plan dated 2026-11-01)

**Inputs:** `vix_dip_summary.md` (Araz backtest, 69 SPY episodes Sep 1997–Mar 2026), `vix_dip_episodes.csv`, `vix_dip_context_20261101.md` (RA, data as of Fri 10/30 close). Account constraints from RA: ~$8k cash, Level 3, no margin/shorting, CSPs allowed, never holds to expiry. Size and $ risk are Dominic's; nothing here sets them.

**Verified backtest anchors (summary.md):** peak VIX 40–50 and 50+ both won 100% at +120d (worst +1.3 / +13.3). Rule (d) VIX/VIX3M back <1 (2009+, n=29): win 93/76/79 at 20/60/120d, worst +120d −12.5, worst DD before recovery −11.6. First close ≥25: win 53/57/61, worst +120d −42.3. Event peaks won 91% at +120d, bear peaks 48%.

**One-line answer:** do not buy the outright long-dated call *at* the spike. Buy a 90–180 DTE call debit spread at first confirmation (VIX/VIX3M close <1 + price confirmation + classifier ≠ Bear), and convert it to an outright call only when IV has normalized. The only cash-only downside hedge is a long put spread, and at spike IV it costs more than it protects (math in §3); the real hedge is structure choice, staged entry, and a close-basis stop.

---

## 0. Catalyst calendar, hold window 11/2/2026 → ~early Mar 2027 (90–120d)

Supply events first: RA finds none at the index level in the window. Nearest is the **Treasury quarterly refunding 11/4** (coupon sizes vs. 10y 4.98%, 10y TIPS 2.63% on 10/29). Dates not verified in the inputs are marked.

| Date | Event | Status in inputs |
|---|---|---|
| 11/3 Tue | US midterms. WH 10/29: no Iran attack "prior to the midterm elections"; Qatar talks are the counter | RA (ABC via MACRO_REGIME_20261030) |
| 11/4 Wed | Treasury refunding; ISM services | RA, dates unverified |
| 11/6 Fri | Oct payrolls | RA, unverified |
| 11/10 Tue 8:30 | **Oct CPI** (oil pass-through; RA's inflation-channel test) | RA, verified (BLS) |
| 11/17 Tue AMC | **NVDA Q3 FY27** (QQQ/SMH swing factor) | RA, confirmed (NVDA IR 10/28) |
| 11/18 Wed | VIX Nov expiry | RA, verified |
| 11/20 Fri | Nov monthly opex SPY/QQQ | RA |
| 11/26–27 | Thanksgiving close / 1pm early close | RA |
| late Nov | Oct PCE | **verify date** (not in inputs) |
| early Dec | Nov payrolls | **verify date** |
| 12/9 Wed | **FOMC + SEP** (Dec 8–9). Dec hike odds 87.4% on 10/28 [single-source] | RA, verified |
| 12/10 Thu | Nov CPI | RA, verified (BLS) |
| 12/16 / 12/18 | VIX Dec expiry / quad witching + S&P rebalance | RA |
| mid-Jan 2027 | Dec CPI; Q4 bank earnings open the season | **verify date** |
| late Jan 2027 | FOMC | **verify date** |
| late Feb 2027 | NVDA Q4 FY27 | **verify date** |

Hold-window implication: a spike bought this week sits in front of CPI (11/10), NVDA (11/17) and FOMC (12/9). Those are the three dates where the classifier (§1) can flip.

---

## 1. Critique of the event/bear split, and a real-time classifier

The backtest's "event vs bear" uses windows known only afterwards (Mar 2000–Apr 2003, Jul 2007–Jun 2009, Feb–Apr 2020, Jan–Oct 2022), and the summary itself flags that Dec 2021 is labeled event although it "ran straight into the 2022 bear market." The 91%/48% split is therefore a ceiling, not a tradable rule. What *is* knowable at the spike:

**A. Price/vol inputs available on the day (from the CSV, computed here):**

| Real-time condition at the spike close | n | Win +120d | Worst +120d | Med / worst max DD (250d) | Bears in set |
|---|---|---|---|---|---|
| VIX ≥ 40, any drawdown | 15 | 100% | +1.3 | −3.8 / −20.2 | 7 |
| VIX < 40 and SPY < 10% below 52-wk high | 32 | 78% | −12.0 | −5.8 / −40.6 | 3 |
| VIX < 40 and SPY ≥ 10% below 52-wk high | 22 | 55% | −22.2 | −9.3 / −46.4 | 15 |

Read: below VIX 40, "already down ≥10% and spiking again" is where the bear damage lives (15 of 22 were bear episodes). Above 40 the drawdown depth stops mattering. Clustering (number of spikes in the prior 365d) adds little: 2007-08-16 had zero prior spikes and was a bear; the 2021 spikes had 3–4 and were events.

**B. Macro inputs from RA's filter list (thresholds are RA's; "convention, not sourced studies"):**

| Filter | Event reading | Bear reading |
|---|---|---|
| HY OAS (BAMLH0A0HYM2) | flat/tightening, <~400bp | widening and >400bp heading to 500bp+ |
| CPI | soft, hike odds falling | hot, hawkish dots |
| Fed | able to ease / cut priced | hiking or unable to ease; 10y >5% sustained |
| VIX/VIX3M | back <1 within days | >1 for multiple days |
| VVIX | rolls over from 120–140 while VIX still high | rises with VIX |
| Breadth | Zweig thrust or two 90% up days | repeated 90% down days, no thrust |
| Equity P/C | spikes >0.8–1.0 then fades | low while price falls |
| VIX price action | back inside upper 20d Bollinger / below prior close | new closing highs |

**Classifier rule:** EVENT = price block A is not in the bottom row, HY OAS <400 and not widening, and at least two of {VIX/VIX3M <1, VVIX rolling, breadth thrust or 90% up day, P/C spiked and fading}. BEAR = HY OAS >400 and widening, **or** price block A bottom row + Fed unable to ease, **or** VIX making new closing highs with ratio >1 for 3+ days. Anything else = MIXED (trade it as a bounce, spreads only, shorter hold).

**How it would have read at the time (inputs only):**

| Spike | Price block (CSV) | Macro block | Classifier output | Actual |
|---|---|---|---|---|
| 2021-12-01, VIX 31.1 | SPY −4.1% from high → middle row (event-like) | HY OAS, CPI, hike odds for Dec 2021 **not in inputs**; RA only says it "ran straight into the 2022 bear" | EVENT on price alone; MIXED at best if the Fed/CPI inputs of the time were fed in (verify) | +120d −12.0, max DD −21.6 |
| 2008 (01-22 / 03-17 / 07-15, VIX 31–32 / 28.5) | SPY −16 / −17.6 / −21.5% → bottom row, 2–4 prior spikes | HY OAS values for 2008 **not in inputs**; RA: "repeated VIX spikes of 30–45 each failed" | BEAR from price alone (and the first two 2007 spikes, at −8%, would have passed as EVENT) | +120d −5.2 / −2.1 / −22.2; max DD −42 to −46 |
| 2022 (01-26 / 03-07 / 05-09 / 06-13, VIX 32–36) | −9.3% (middle row, borderline) then −12 / −16 / −21% (bottom row) | HY OAS, CPI prints **not in inputs**; RA: "2022 rates bear," Fed hiking; "VIX never sustained a 40-plus capitulation" | 01-26: MIXED (price event-like, Fed bear); 03-07 onward: BEAR | +120d −8.2 / −2.7 / −1.5 / +9.4; max DD −18.8 / −16 / −11.8 / −6.4 |

**Weakness, stated plainly:** the price block cannot catch the *first* spike of a bear, because the first spike is by definition shallow (2007-08-16 −8.4%, 2007-11-12 −8.2%, 2021-12-01 −4.1%, 2022-01-26 −9.3% all look like events). Only the macro block can, and it is slow (HY OAS 400bp is a lagging line; in the inputs it is 326bp today). The price block also rejects 7 of 22 deep-drawdown spikes that were events (e.g. 2018-12-24 at −19.3%, +120d +25.3). Expect the classifier to be right about the middle of bears and wrong at their start; that is why the entry tiers below require the term-structure confirmation and the stop is thesis-level, not just price-level.

---

## 2. Entry tiers (zones, not lines)

Dominic's method applied: identify the SPY/QQQ *zone* when the spike arrives (prior swing lows, 200d MA area, the spike-day low), set a zone alert, and define the confirmation alert only once price is inside the zone. Confirmation = convergent evidence: 15m breakout over the zone high or a strong 4h close back above the 4h 20MA, momentum/volume, UW flow (call $ premium > put $ premium on SPY/QQQ in session; no numeric threshold is set because none is in the inputs), and news tone. No trigger is placed next to the current price.

| Tier | VIX zone | Term structure | Classifier | Price confirmation (in zone only) | Action | Backtest support |
|---|---|---|---|---|---|---|
| **Watch** | first close ≥25 (after 20d below) | ratio usually >1 | any | none yet; draw the zone, set zone alerts | **no position** | first close ≥25: win 53/57/61, worst +120d −42.3 |
| **Starter** | 25–40, after the spike high is in | **VIX/VIX3M close <1** after being >1 (rule d), or VIX close below prior close / inside upper band | EVENT or MIXED (not BEAR) | 15m breakout of zone high with volume **or** strong 4h close above 4h 20MA; UW call premium leading; VVIX rolling | **call debit spread** 90–180 DTE (CSP on a cheaper ETF if a strike fits, §3) | rule d: 93/76/79, worst +120d −12.5; back <30 after ≥30: 83/74/69 |
| **Full** | ≥40 | ratio can still be >1 | not BEAR by HY OAS (price block does not matter above 40) | after a down week, first 15m failed breakdown of the zone low or first green 4h close (Man Group: week-1 decline then 3m positive 100%) | call spread or CSP into the spike; convert to outright call when ratio <1 | first close ≥40: 77/92/85, worst +120d −25; peak ≥40: 100% at +120d, n=15 |
| **Add** | normalized: VIX <~20, ratio <~0.9 | contango | EVENT confirmed (breadth thrust or 90% up day; HY OAS flat/tighter) | higher low on 4h, 4h 20MA > 50MA turning up | **outright 120+ DTE call**, delta 0.5–0.6 (RA "normalized" phase) | peak-entry medians +11.7 at 120d; your cost basis is a few % higher than the peak |

Why Starter waits for the ratio: in Mar 2026 the ratio flipped <1 on 3/31 (VIX 25.25, SPY 647.06) two sessions after the 31.05 peak (SPY 630.89). The wait cost +2.56% of spot. In the §3 EXAMPLE call (delta 0.58, vega 0.274/pt), that is ≈1.5 index points of delta given up vs ≈1.6 points of vega saved **if** 180-DTE IV fell point-for-point with the VIX (it falls less; assumption). Roughly a wash on price, and you buy the information that the spike was an event.

---

## 3. Structure comparison, 90–365 DTE, judged on mark-to-market during the hold

**Cash-only feasibility first.** A true collar needs 100 shares; an uncovered short call is not cash-only. The feasible hedged variants are: (c1) long call + long put **spread**, (c2) call spread + put spread, (d) CSP on an ETF where 100 × strike ≤ ~$8k, i.e. **strike ≤ $80** (RA: SPY ~$650+ and QQQ ~$690–720 strikes are "not affordable"; RA names XLK/IWM-class as candidates, prices not in inputs, verify at broker; a generic sub-$80 S&P proxy such as SPLG is the other candidate, verify price). Long call + long single put is cash-only but doubles the long vega, the exact exposure the spike punishes, so it is excluded.

**EXAMPLE (all assumptions stated, Black-Scholes, own calc):** index = 100, r = 4%, no dividends, **180 DTE**, entry on a spike day with 180-DTE IV **35** (front VIX would print higher; term IV rises less, as RA notes VIX3M +7% vs VIX +13% on 10/30). Skew assumed: 100C 35, 110C 33, 95P 39, 85P 43. IV then mean-reverts uniformly to 28 (partial) or **20** (normal). Downside scenario: spot −5% / −10% with IV +8 pts. Scale: at SPY 755.72 (10/30 close) one index point = $7.56, so one contract ≈ 756× the figures.

| Structure | Cost | Δ | Vega /pt | Θ /day | +20d flat, IV20 | +20d +3%, IV20 | +20d +5%, IV20 | +20d +8%, IV20 | +60d +5%, IV20 | +60d +8%, IV20 | +20d −5%, IV43 | +20d −10%, IV43 | ≈ $/contract on SPY |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (a) long 100C | 10.69 | 0.58 | 0.274 | −0.032 | **−43%** | **−25%** | **−12%** | +9% | −21% | +1% | −12% | −34% | ~$8,100 |
| (b) 100/110 call spread | 4.53 | 0.16 | ~0 | −0.003 | −7% | +13% | **+26%** | **+45%** | +24% | +45% | −17% | −33% | ~$3,400 |
| (c1) 100C + 95/85 put spread | 13.54 | 0.46 | 0.323 | −0.033 | −41% | −30% | −22% | −7% | −30% | −15% | **−3%** | **−16%** | ~$10,200 |
| (c2) 100/110 CS + 95/85 PS | 7.37 | 0.04 | 0.049 | −0.004 | −17% | −11% | −6% | +1% | −10% | −1% | +2% | +1% | ~$5,600 |
| (d) CSP 90 strike, IV 44 (premium 6.60) | +6.60 credit | −0.29 | 0.240 | −0.025 | +41% of prem (IV34) | +69% (IV28) | +91% (IV20) | — | +95% (IV20) | — | −44% (IV52) | −87% (IV56) | cash = 100 × strike |

CSP row uses its own IV path (44 → 34/28/20 on flat/+3/+5 rallies; 52/56 on −5/−10 declines), shown in each cell. For comparison with IV unchanged at 35: (a) +5% in 20d = +23%; (b) = +17%. The entire difference between a winning and a losing outright call at +5% is the IV path.

**Discussion.**
- (a) Outright call at spike IV: vega 0.274/pt on a 10.69 premium = 2.6% of premium per vol point. A 15-point normalization costs ~38% before delta helps; spot must rally ~7% in 20d just to break even on the mark. In the backtest, +20d medians after a peak are +5.4 (all) and +7.7 (40–50 bucket); the outright call is under water at the median path. Singles are right for fast moves at cheap IV; a spike is the opposite.
- (b) Call debit spread: vega ≈ 0, theta ≈ 0 at entry, delta 0.16 rising as spot approaches the short strike. At +5%/IV20 it is +26% vs −12% for the single. Its cost is the capped upside and low initial delta; at +8% it is +45% while the single is +9%, so the cap does not bind within the hold window at historical median moves. Downside −5% costs −17%, so it also loses less than the single. This is the right instrument for "rich IV, slow-to-medium move."
- (c1) Call + put spread: the "hedge" adds +27% to cost and *adds* vega (0.323 vs 0.274). At −5% it saves 9 points of loss vs the single; at +5%/IV20 it loses 22% instead of 12%. It only pays if a second leg down comes fast and before IV collapses. Use only when the classifier reads MIXED and the thesis still demands long-dated call exposure.
- (c2) Call spread + put spread: delta 0.04; it is a long-strangle-of-spreads, not a directional position. Fails the ask.
- (d) CSP on a ≤$80 ETF: short vega at the spike (the only structure that *earns* the IV crush), +41% of premium in 20d even flat. Risk is directional: −10%/IV56 marks at −87% of premium, and assignment means owning the ETF with cash (fits staged accumulation, per RA). It is a hedge for the call's vega, not for its delta. RA's "cash-secured risk reversal" (CSP + long call) is feasible only on the cheap ETF.

**Recommended sequence (RA's phase table, adopted):** spike peak → CSP on a ≤$80 ETF if a strike fits, otherwise nothing or a small call spread; first confirmation → call spread 90–180 DTE; VIX normalized → outright 120+ DTE call, or convert the spread by buying back the short leg once the short call's IV is at or below the long leg's entry IV. Note the affordability facts: one SPY ATM 180-DTE call ≈ $8.1k and one 10-wide SPY call spread ≈ $3.4k at the EXAMPLE IV, so on SPY only the spread is even possible, and on QQQ it is worse; the long-dated outright call is realistically a QQQ/SPY *OTM* call or a cheaper ETF (sizing Dominic's).

---

## 4. Stops (candle-close basis), invalidation, add rules

| Layer | Rule | Why |
|---|---|---|
| Price stop, Starter | **4h close** below the zone low (spike-day low) after the 15m/4h confirmation fired | the confirmation is the thesis; its failure is the exit |
| Price stop, Full/Add | **daily close** below the spike low | VIX ≥40 entries had median max DD −3.8 and worst −20.2; a daily close under the low is outside the historical path of winners |
| Vol stop | VIX/VIX3M closes back **>1 for 2 consecutive days** after the <1 trigger, or VIX makes a **new closing high** after entry | rule d assumed the inversion was over; RA: "stays above 1 for multiple days" = bear warning |
| Credit stop | HY OAS >400bp and widening (RA's line) at any time in the hold | converts every spike into "a rally to sell" (RA) |
| Macro stop | hot Oct CPI (11/10) with Dec hike odds rising, or hawkish 12/9 dots | inflation → Fed → credit channel confirmed; RA: hold off on calls until FOMC |
| Classifier flip | any BEAR condition in §1 | exit spreads at the mark; do not average |
| Time stop | Call spread not above entry mark by the first of {+20d, next scheduled catalyst} | +20d median after peak is +5.4; a flat mark after 20d says the move is not the historical one |

**Add rules (not size):** add only after (i) ratio <0.9 and VIX inside its 20d band, (ii) a higher low on the 4h and a strong 4h close above the prior swing, (iii) HY OAS flat or tighter than at entry, (iv) a breadth thrust or 90% up day has printed. Never add while ratio >1 or before CPI/FOMC within 2 sessions. Add in the *next* structure (spread → outright call), not more of the same spread. Never add to recover a mark-to-market loss.

---

## 5. Application: Iran-strike spike, week of Nov 2, 2026

**Current facts (RA, 10/30 close unless noted):** VIX 19.42 (intraday high 23.93), VIX3M 20.78, ratio 0.935 (contango), VIX9D 19.25, VXN 28.50, VVIX 106.43 (intraday 124.06), SKEW 149.76, RV10 27.95% > VIX, HY OAS 326bp (+14bp/1m), IG 89bp, WTI $103.37, 10y 4.98%, Dec hike odds 87.4% [single-source], equity P/C 0.59, SPX P/C 1.54, breadth narrowing with no thrust, SPY 755.72 (−3.0% from the 10/6 record 779.09), QQQ −3.5% and SMH −7% on 10/30. Strike signaled for after the 11/3 midterms; Qatar talks are the counter. RA's pre-spike classification: AI-capex/tech repricing with a scheduled geopolitical tail; "not a buyable spike" as of 10/30.

**Classifier reading if a strike produces VIX high-20s to 30s with ratio >1 [RA inference]:**
- Price block: SPY −3% from high → middle row (event-like), VIX <40.
- Credit: 326bp → Event.
- Fed/inflation: 87.4% Dec hike, WTI >$100, 10y 4.98%, RV > IV → Bear-leaning.
- Output: **MIXED**, the 2022-02/03 Ukraine analog (RA: fast V, then the rates bear resumed). Trade it as a bounce, not a bottom.

**Tier application:**
- Day 1–2 of the spike: **Watch** only. Draw the SPY/QQQ zone (spike-day low, nearby 200d MA; levels not in inputs). Do not chase VIX 19→25; first close ≥25 is the coin-flip entry (53%, −42 tail).
- **Starter** only when ratio closes <1 and price confirms inside the zone (15m breakout or strong 4h close), and only if HY OAS is still <400 and not widening and VVIX is rolling. Structure: call debit spread 90–180 DTE on SPY/QQQ (QQQ/SMH is where the vol is: VXN 28.5), or a CSP on a ≤$80 ETF if a strike fits. Prefer the spread to expire after 12/9 so the mark survives the FOMC without front-month theta.
- **Full** only if VIX ≥40; the price block then stops mattering and only HY OAS can veto.
- **Add/convert to outright call** only after RA's event-V flips: oil <$90, CPI soft on 11/10 with hike odds collapsing, ratio <0.9 with a Zweig thrust or 90% up day, NVDA beat-and-raise on 11/17.

**Watch first, in order:** (1) oil, because the Fed/credit channel runs through it; (2) VIX/VIX3M daily close; (3) HY OAS daily (FRED, 1-day lag); (4) VVIX vs VIX; (5) equity P/C moving from 0.59 toward ≥0.8–1.0 and fading (put capitulation absent today); (6) UW call vs put $ premium on SPY/QQQ once price is in the zone.

**Skip conditions:** no strike or a Qatar deal (no spike, no trade); VIX stuck 25–30 with the ratio never >1 (no capitulation, no edge); ratio >1 for 3+ days with new VIX closing highs; HY OAS through 400bp and widening; hot CPI on 11/10 before confirmation has fired (RA: stand down until 12/9); 10y sustained above 5%; breadth printing repeated 90% down days with no thrust.

---

## Open questions for Dominic
1. Which ≤$80 ETF(s) will you accept for the CSP leg, and have you checked at the broker that one strike fits the cash after the spread's debit?
2. Hold horizon for the call leg: is the exit "VIX normalized / +20d / next catalyst" (this plan) or a target on SPY/QQQ?
3. Underlying for the spread: SPY (lower vol, cheaper IV) or QQQ (where the stress is, VXN 28.5, but higher dollar cost)?
4. Do you want the HY OAS 400bp line as a hard exit, or only as a no-add line given FRED's one-day lag?
5. Should a hot Oct CPI on 11/10 cancel the whole setup until 12/9, as RA proposes, or only block the Add tier?
