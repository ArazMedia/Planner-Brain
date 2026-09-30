"""Critic data checks (compact). Answers: are the day-1 rows aligned to real after-close prints, do the bars match a
second vendor, and is the day-1 negative open->close drift real (MU specific vs. a general post-print effect)?
Inputs: raw_daily_unadj.csv, raw_earnings_dates.csv, day1_planner.csv, raw_1h.csv, external/ (SEC, Nasdaq, Yahoo panel).
Output: stdout (saved to critic_data_checks_out.txt) and external/panel_day1.csv
"""
import pandas as pd, numpy as np, glob, os
pd.set_option("display.width", 220); pd.set_option("display.max_columns", 40)
d = pd.read_csv("raw_daily_unadj.csv", index_col=0, parse_dates=True)
e = pd.read_csv("raw_earnings_dates.csv"); e["date"] = pd.to_datetime(e["Earnings Date"].str[:10]); e["hour"] = e["Earnings Date"].str[11:13].astype(int)
e = e[e["Reported EPS"].notna()].sort_values("date").reset_index(drop=True)
pl = pd.read_csv("day1_planner.csv", parse_dates=["report_date", "day1"])
sec = pd.read_csv("external/sec_filings_MU.csv", parse_dates=["filingDate", "reportDate"])
sec["acc"] = pd.to_datetime(sec.acceptanceDateTime.str[:19])
k8 = sec[sec.form.str.startswith("8-K")].copy()

print("=== 1. SEC 8-K verification of the 99 yfinance earnings rows (2001-12 .. 2026-06) ===")
rows = []
for _, r in e.iterrows():
    w = k8[(k8.filingDate >= r.date - pd.Timedelta(days=1)) & (k8.filingDate <= r.date + pd.Timedelta(days=2))]
    # prefer item 2.02 (post-2004) else any 8-K in the window
    w202 = w[w["items"].fillna("").str.contains("2.02")]
    m = w202 if len(w202) else w
    if len(m):
        m = m.sort_values("acc").iloc[0]
        rows.append(dict(yf_date=r.date.date(), yf_hour=r.hour, sec_report=m.reportDate.date() if pd.notna(m.reportDate) else None,
                         sec_accepted=m.acc, items=m["items"], same_day=(m.acc.normalize() == r.date), after_close=(m.acc.hour >= 16) if m.acc.normalize() == r.date else None))
    else:
        rows.append(dict(yf_date=r.date.date(), yf_hour=r.hour, sec_report=None, sec_accepted=None, items=None, same_day=False, after_close=None))
v = pd.DataFrame(rows)
print("rows:", len(v), "| 8-K found within [-1,+2]d:", v.sec_accepted.notna().sum(), "| 8-K accepted same day:", v.same_day.sum(),
      "| accepted same day and >=16:00 ET:", (v.after_close == True).sum())
print("Rows whose 8-K was NOT accepted after the close on the yfinance date (need a look):")
print(v[~(v.after_close == True)].to_string())
in_ds = set(pl.report_date.dt.date)
print("\nRows in raw_earnings_dates but NOT in day1_planner.csv:", sorted(set(v.yf_date) - in_ds))

print("\n=== 2. day-1 alignment: day1 must be the next trading day after report_date; volume must spike ===")
idx = d.index
bad = 0
for _, r in pl.iterrows():
    i = idx.get_loc(r.report_date); nxt = idx[i + 1]
    if nxt != r.day1: bad += 1; print("MISALIGNED", r.report_date.date(), r.day1.date(), nxt.date())
print("misaligned rows:", bad, "| day-1 volume / report-day volume: median %.2f, min %.2f (%s)" % (
    (pl.vol_ratio).median(), pl.vol_ratio.min(), pl.loc[pl.vol_ratio.idxmin(), "report_date"].date()))
vr = [d.Volume.iloc[idx.get_loc(r.day1)] / d.Volume.iloc[idx.get_loc(r.report_date)] for _, r in pl.iterrows()]
pl["v1_v0"] = vr; print("day-1 volume < report-day volume on", (pl.v1_v0 < 1).sum(), "rows:", pl[pl.v1_v0 < 1][["report_date", "v1_v0"]].round(2).values.tolist())

print("\n=== 3. Second vendor (Nasdaq.com) vs yfinance, day-1 bars, 2016-10 .. 2026-06 ===")
nq = pd.read_csv("external/nasdaq_mu_daily.csv", index_col=0, parse_dates=True)
sub = pl[pl.day1 >= nq.index.min()]
cmp = []
for _, r in sub.iterrows():
    if r.day1 not in nq.index: cmp.append(dict(day1=r.day1.date(), missing=True)); continue
    q = nq.loc[r.day1]; p = d.loc[r.day1]
    cmp.append(dict(day1=r.day1.date(), dO=(p.Open / q.Open - 1) * 100, dH=(p.High / q.High - 1) * 100, dL=(p.Low / q.Low - 1) * 100, dC=(p.Close / q.Close - 1) * 100, dV=(p.Volume / q.Volume - 1) * 100))
cmp = pd.DataFrame(cmp)
print("n compared:", len(cmp), "| max |diff| %%: O %.3f H %.3f L %.3f C %.3f | vol max %.1f%%" % (cmp.dO.abs().max(), cmp.dH.abs().max(), cmp.dL.abs().max(), cmp.dC.abs().max(), cmp.dV.abs().max()))
print(cmp[(cmp[["dO", "dH", "dL", "dC"]].abs() > 0.05).any(axis=1)].round(3).to_string())
print("June 2026 bars, yfinance vs Nasdaq (Close):")
j = pd.DataFrame({"yf_close": d.Close["2026-06-18":"2026-06-30"], "nq_close": nq.Close["2026-06-18":"2026-06-30"], "yf_open": d.Open["2026-06-18":"2026-06-30"], "nq_open": nq.Open["2026-06-18":"2026-06-30"], "yf_vol": d.Volume["2026-06-18":"2026-06-30"], "nq_vol": nq.Volume["2026-06-18":"2026-06-30"]})
print(j.round(2).to_string())
print("June 2026 pre-print 8-Ks (news check):"); print(k8[(k8.filingDate >= "2026-06-15") & (k8.filingDate <= "2026-06-30")][["filingDate", "acc", "items"]].to_string())

print("\n=== 4. The skipped 2002-06-25 print (yfinance stamp 07:00 -> treated as BMO and dropped) ===")
i = idx.get_loc(pd.Timestamp("2002-06-25"))
print(d.iloc[i - 1:i + 3][["Open", "High", "Low", "Close", "Volume"]].to_string())
o, h, c = d.Open.iloc[i + 1], d.High.iloc[i + 1], d.Close.iloc[i + 1]
ent = o * 0.999; sp = ent * 1.03; x = sp * 1.002 if h >= sp else c * 1.001; ret = -(x / ent - 1) * 100
print("If included as AMC (day1 = 2002-06-26): gap %.1f%%, oc %.1f%%, R0 short result %.2f%% = %.2fR" % ((o / d.Close.iloc[i] - 1) * 100, (c / o - 1) * 100, ret, ret / 3))
t = pd.read_csv("trades_base.csv"); r0 = t[t.rule == "R0 DAY1-SHORT"].R.values
print("R0 mean R: n=98 %.3f -> n=99 incl. this print %.3f" % (r0.mean(), (r0.sum() + ret / 3) / 99))

print("\n=== 5. Official daily open vs first 1h bar open (fill realism), 11 prints with hourly data ===")
h = pd.read_csv("raw_1h.csv"); h["day"] = pd.to_datetime(h.Datetime.str[:10]); h["hm"] = h.Datetime.str[11:16]
for _, r in pl[pl.h1_close_pct.notna()].iterrows():
    b = h[(h.day == r.day1) & (h.hm == "09:30")]
    if len(b): print(r.day1.date(), "daily open %.2f  1h-bar open %.2f  diff %+.2f%%  (gap %+.1f%%, oc %+.1f%%)" % (r.open, b.Open.iloc[0], (b.Open.iloc[0] / r.open - 1) * 100, r.gap_pct, r.oc_pct))

print("\n=== 6. Is the day-1 open->close drift real? MU raw drift and controls (no costs) ===")
oc = pl.oc_pct
def tt(x): x = np.asarray(x, float); return x.mean(), x.mean() / (x.std(ddof=1) / np.sqrt(len(x))), len(x)
print("MU day-1 oc: mean %+.2f%% t=%.2f n=%d | median %+.2f | share negative %.0f%%" % (*tt(oc), oc.median(), (oc < 0).mean() * 100))
for nm, m in [("gap>0", pl.gap_pct > 0), ("gap<=0", pl.gap_pct <= 0), ("|gap|<3", pl.gap_pct.abs() < 3), ("3<=|gap|<7", (pl.gap_pct.abs() >= 3) & (pl.gap_pct.abs() < 7)), ("|gap|>=7", pl.gap_pct.abs() >= 7), ("gap>=7", pl.gap_pct >= 7), ("gap<=-7", pl.gap_pct <= -7), ("2001-15", pl.year <= 2015), ("2016-26", pl.year >= 2016)]:
    print("  %-11s mean %+.2f%% t=%.2f n=%d" % (nm, *tt(oc[m])))
allday = (d.Close / d.Open - 1) * 100; dd = d["2001-12-01":]
ed1 = set(pl.day1); day2 = set(idx[idx.get_loc(x) + 1] for x in pl.day1)
non = dd[~dd.index.isin(ed1)]; ocn = (non.Close / non.Open - 1) * 100; gapn = (non.Open / non.Close.shift(1) - 1) * 100
print("MU all non-earnings days oc: mean %+.3f%% t=%.2f n=%d" % tt(ocn.dropna()))
print("MU non-earnings |gap|>=3%% days oc: mean %+.2f%% t=%.2f n=%d" % tt(ocn[gapn.abs() >= 3].dropna()))
print("MU non-earnings |gap|>=7%% days oc: mean %+.2f%% t=%.2f n=%d" % tt(ocn[gapn.abs() >= 7].dropna()))
d2 = dd[dd.index.isin(day2)]; print("MU day-2 (second session after print) oc: mean %+.2f%% t=%.2f n=%d" % tt(((d2.Close / d2.Open - 1) * 100)))
print("MU day-1 open->day2 close (2-session) short drift: mean %+.2f%%" % (-(pl.close_d2 / pl.open - 1) * 100).mean())

print("\n=== 7. Peer panel: after-close 8-K item 2.02 prints (SEC acceptance >= 16:00 ET, same day), day-1 open->close ===")
def panel_day1(sym):
    f = pd.read_csv(f"external/sec_filings_{sym}.csv", parse_dates=["filingDate", "reportDate"])
    f = f[f.form.str.startswith("8-K") & f["items"].fillna("").str.contains("2.02")].copy()
    f["acc"] = pd.to_datetime(f.acceptanceDateTime.str[:19]); f = f[f.acc.dt.hour >= 16]
    f = f[f.acc.dt.normalize() == f.reportDate]              # unambiguous same-day after-close release
    px = pd.read_csv(f"external/yahoo_{sym}_daily.csv", index_col=0, parse_dates=True)
    sp = pd.read_csv(f"external/yahoo_{sym}_splits.csv", index_col=0, parse_dates=True)
    out = []
    for dt_ in sorted(set(f.reportDate)):
        if dt_ not in px.index: continue
        i = px.index.get_loc(dt_)
        if i + 1 >= len(px): continue
        if len(sp) and any((sp.index > dt_) & (sp.index <= px.index[i + 1])): continue  # split on day 1
        pc, o, hi, c = px.Close.iloc[i], px.Open.iloc[i + 1], px.High.iloc[i + 1], px.Close.iloc[i + 1]
        ent = o * 0.999; stp = ent * 1.03; x = stp * 1.002 if hi >= stp else c * 1.001
        out.append(dict(sym=sym, report=dt_.date(), day1=px.index[i + 1].date(), gap=(o / pc - 1) * 100, oc=(c / o - 1) * 100, r0_ret=-(x / ent - 1) * 100, stopped=hi >= stp, v1_v0=px.Volume.iloc[i + 1] / max(px.Volume.iloc[i], 1)))
    return pd.DataFrame(out)
P = []
for fp in sorted(glob.glob("external/yahoo_*_daily.csv")):
    sym = os.path.basename(fp)[6:-10]
    if sym == "MU": continue
    try: P.append(panel_day1(sym))
    except Exception as ex: print(sym, "failed", ex)
P = pd.concat(P, ignore_index=True); P = P[P.v1_v0 > 1.0]  # keep prints where the next session actually reacted
P.to_csv("external/panel_day1.csv", index=False)
g = P.groupby("sym").agg(n=("oc", "size"), mean_oc=("oc", "mean"), t_oc=("oc", lambda x: x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))), r0_ret=("r0_ret", "mean"), r0_R=("r0_ret", lambda x: x.mean() / 3), stopped=("stopped", "mean"), first=("report", "min"))
print(g.round(2).sort_values("mean_oc").to_string())
print("PANEL pooled: n=%d mean oc %+.2f%% t=%.2f | R0-style short (3%% stop, costs) %+.2f%%/trade = %+.3fR | share of 19 names with negative mean oc: %d" % (
    len(P), P.oc.mean(), P.oc.mean() / (P.oc.std(ddof=1) / np.sqrt(len(P))), P.r0_ret.mean(), P.r0_ret.mean() / 3, (g.mean_oc < 0).sum()))
for nm, m in [("|gap|<3", P.gap.abs() < 3), ("3<=|gap|<7", (P.gap.abs() >= 3) & (P.gap.abs() < 7)), ("|gap|>=7", P.gap.abs() >= 7), ("gap>=7", P.gap >= 7), ("gap<=-7", P.gap <= -7), ("2004-15", pd.to_datetime(P.report).dt.year <= 2015), ("2016-26", pd.to_datetime(P.report).dt.year >= 2016)]:
    print("  %-11s mean oc %+.2f%% t=%.2f n=%d | R0-style %+.2f%%" % (nm, *tt(P.oc[m]), P.r0_ret[m].mean()))
