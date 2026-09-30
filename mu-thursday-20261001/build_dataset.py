"""Planner independent MU day-1 (first post-earnings session) dataset.
Inputs: raw_daily_unadj.csv, raw_earnings_dates.csv, raw_1h.csv (yfinance pulls by fetch.py, 2026-09-30 ~00:30 ET).
Output: day1_planner.csv
"""
import pandas as pd, numpy as np
d=pd.read_csv("raw_daily_unadj.csv",index_col=0,parse_dates=True)
e=pd.read_csv("raw_earnings_dates.csv")
e["ts"]=e["Earnings Date"]; e["hour"]=e.ts.str[11:13].astype(int); e["date"]=pd.to_datetime(e.ts.str[:10])
e=e[e["Reported EPS"].notna()].sort_values("date")
h=pd.read_csv("raw_1h.csv"); h["dt"]=pd.to_datetime(h.Datetime.str[:19]); h["day"]=h.dt.dt.normalize()
idx=d.index
rows=[]
for _,r in e.iterrows():
    if r.date not in idx: continue
    i=idx.get_loc(r.date)
    # timing: AMC -> base = report-day close. Check with volume: reaction day should out-volume report day.
    v0,v1=d.Volume.iloc[i],d.Volume.iloc[i+1] if i+1<len(d) else np.nan
    if r.hour==7: continue   # BMO, skip (2002 only)
    timing="AMC" if r.hour>=16 else ("AMC?vol" if v1>v0 else "BMO?vol")
    if timing=="BMO?vol": continue
    if i+2>=len(d) or i<25: continue
    pc=d.Close.iloc[i]; o,hh,l,c=d.Open.iloc[i+1],d.High.iloc[i+1],d.Low.iloc[i+1],d.Close.iloc[i+1]
    c2=d.Close.iloc[i+2]
    gap=o/pc-1
    s=np.sign(gap) if gap!=0 else 1
    row=dict(report_date=r.date.date(),day1=idx[i+1].date(),hour=r.hour,timing=timing,surprise=r["Surprise(%)"],
        prev_close=pc,open=o,high=hh,low=l,close=c,close_d2=c2,
        gap_pct=gap*100,oc_pct=(c/o-1)*100,cc_pct=(c/pc-1)*100,d2_cc_pct=(c2/pc-1)*100,
        hi_from_open_pct=(hh/o-1)*100,lo_from_open_pct=(l/o-1)*100,range_pct=(hh/l-1)*100,
        gap_fill=bool(l<=pc) if gap>0 else bool(hh>=pc),
        continuation=bool(np.sign(c-o)==s),
        mfe_dir_pct=((hh/o-1) if s>0 else (1-l/o))*100,   # favourable excursion in gap direction from open
        mae_dir_pct=((1-l/o) if s>0 else (hh/o-1))*100,   # adverse excursion vs gap direction from open
        close_loc=(c-l)/(hh-l) if hh>l else np.nan,
        runup20_pct=(pc/d.Close.iloc[i-20]-1)*100, runup10_pct=(pc/d.Close.iloc[i-10]-1)*100,
        vol_ratio=v1/d.Volume.iloc[i-20:i].mean(), year=r.date.year)
    # hourly (yfinance 1h, 2023-10-31+): first bar 09:30-10:30 = 60m opening range
    hb=h[h.day==pd.Timestamp(idx[i+1])].sort_values("dt")
    if len(hb)>=6:
        orh,orl=hb.High.iloc[0],hb.Low.iloc[0]; c1030=hb.Close.iloc[0]; rest=hb.iloc[1:]
        row.update(h1_close_pct=(c1030/o-1)*100, h1_high=orh, h1_low=orl, h1_close=c1030,
            or60_break_up=bool((rest.High>orh).any()), or60_break_dn=bool((rest.Low<orl).any()),
            first_break=("up" if (rest.High>orh).idxmax()<(rest.Low<orl).idxmax() else "dn") if (rest.High>orh).any() and (rest.Low<orl).any() else ("up" if (rest.High>orh).any() else ("dn" if (rest.Low<orl).any() else "none")),
            h1_to_close_pct=(c/c1030-1)*100, post1030_hi=rest.High.max(), post1030_lo=rest.Low.min(), h1_dir_confirms_gap=bool(np.sign(c1030-o)==s))
    rows.append(row)
df=pd.DataFrame(rows)
df.to_csv("day1_planner.csv",index=False,float_format="%.4f")
print(len(df), df.report_date.min(), df.report_date.max(), df.timing.value_counts().to_dict(), "hourly rows:",df.h1_close_pct.notna().sum())
