# Refinement check (n=11 hourly prints only; LOW CONFIDENCE): R0 short at daily open, 3% stop, exit at time T
import pandas as pd, numpy as np
h=pd.read_csv("raw_1h.csv"); h["day"]=h.Datetime.str[:10]; h["hm"]=h.Datetime.str[11:16]
e=pd.read_csv("day1_planner.csv"); e=e[e.h1_close_pct.notna()]
res={k:[] for k in ["10:30","11:30","12:30","13:30","close"]}
for _,r in e.iterrows():
    b=h[h.day==r.day1].reset_index(drop=True); ent=r.open*(1-0.001); sp=ent*1.03
    for k,nb in [("10:30",1),("11:30",2),("12:30",3),("13:30",4),("close",len(b))]:
        bb=b.iloc[:nb]
        if (bb.High>=sp).any(): x=sp*1.002
        else: x=bb.Close.iloc[-1]*1.001
        res[k].append(-(x/ent-1)*100)
for k,v in res.items(): v=np.array(v); print(f"exit {k:6s} n={len(v)} mean={v.mean():+.2f}% median={np.median(v):+.2f}% win={np.mean(v>0):.2f} R={v.mean()/3:+.2f}")
