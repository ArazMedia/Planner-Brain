# Placebo: same R0 rule (short open, 3% stop, same costs) on NON-earnings MU days -> checks stop-logic artifacts
import pandas as pd, numpy as np
d=pd.read_csv("raw_daily_unadj.csv",index_col=0,parse_dates=True); d=d["2001-12-01":]
e=pd.read_csv("day1_planner.csv"); ed=set(pd.to_datetime(e.day1))
pc=d.Close.shift(1); gap=(d.Open/pc-1)
SL=0.001; SS=0.002
ent=d.Open*(1-SL); sp=ent*1.03
stopped=d.High>=sp
x=np.where(stopped, sp*(1+SS), d.Close*(1+SL))
ret=-(x/ent-1)*100; R=ret/3
df=pd.DataFrame(dict(ret=ret,R=R,gap=gap*100,stopped=stopped),index=d.index).dropna()
non=df[~df.index.isin(ed)]
for nm,m in [("all non-earnings days",non.gap.abs()>=0),("non-earn |gap|>=3%",non.gap.abs()>=3),("non-earn gap>=3%",non.gap>=3),("non-earn gap<=-3%",non.gap<=-3),("non-earn |gap|>=5%",non.gap.abs()>=5)]:
    s=non[m]; print(f"{nm:24s} n={len(s):5d} meanR={s.R.mean():+.3f} ret={s.ret.mean():+.2f}% stopped={s.stopped.mean():.2f}")
s=df[df.index.isin(ed)]; print(f"{'earnings day-1':24s} n={len(s):5d} meanR={s.R.mean():+.3f} ret={s.ret.mean():+.2f}%")
