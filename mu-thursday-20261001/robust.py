import pandas as pd, numpy as np, bt_planner_thu as B
df=B.df.copy(); rng=np.random.default_rng(11)
out=[]
def r0(stop, slip=0.001, sslip=0.002, sub=None):
    B.SLIP=slip; B.SSLIP=sslip
    d=df if sub is None else sub
    res=[B.stock_trade(r,-1,stop) for _,r in d.iterrows()]
    B.SLIP=0.001; B.SSLIP=0.002
    return np.array([x[0] for x in res])*100, np.array([x[1] for x in res]), np.array([x[2]=="stop" for x in res])
print("== R0 stop sensitivity (slip 0.10%/0.20% stop)")
for st in [0.02,0.03,0.04,0.05,0.06,None]:
    ret,R,stp=r0(st)
    bs=rng.choice(ret,(10000,len(ret))).mean(1)
    print(f"stop={st}: n={len(ret)} mean_ret={ret.mean():.2f}% CI90=({np.percentile(bs,5):.2f},{np.percentile(bs,95):.2f}) meanR={R.mean():.3f} win={np.mean(ret>0):.2f} stopped={stp.mean():.2f} pre16={ret[df.year<=2015].mean():.2f} post16={ret[df.year>2015].mean():.2f}")
print("== R0 slippage stress (3% stop)")
for sl,ss in [(0.001,0.002),(0.002,0.004),(0.003,0.006),(0.005,0.01)]:
    ret,R,stp=r0(0.03,sl,ss); print(f"slip={sl*100:.1f}%/stop {ss*100:.1f}%: mean_ret={ret.mean():.2f}% meanR={R.mean():.3f}")
print("== R0 5-year blocks (3% stop)")
ret,R,stp=r0(0.03)
blk=(df.year//5)*5
for b in sorted(blk.unique()):
    m=blk==b; print(b, m.sum(), f"meanR={R[m].mean():+.3f} ret={ret[m].mean():+.2f}% win={np.mean(ret[m]>0):.2f}")
print("== walk-forward: trade print k only if mean R of all prior prints (min 12) > 0")
wf=[R[k] for k in range(12,len(R)) if R[:k].mean()>0]
print("WF n",len(wf),"meanR",np.mean(wf).round(3),"of",len(R)-12,"eligible")
print("== first half / second half by date")
h=len(R)//2; print("H1",h,R[:h].mean().round(3),"H2",len(R)-h,R[h:].mean().round(3))
print("== by gap direction / run-up")
for nm,m in [("gap>0",df.gap_pct>0),("gap<0",df.gap_pct<=0),("|gap|<3",df.gap_pct.abs()<3),("gap>=3",df.gap_pct>=3),("gap<=-3",df.gap_pct<=-3),("gap>=8",df.gap_pct>=8),("runup20>10",df.runup20_pct>10),("runup20<=10",df.runup20_pct<=10),("runup20>10 & pre16",(df.runup20_pct>10)&(df.year<=2015))]:
    print(f"{nm:18s} n={m.sum():3d} meanR={R[m].mean():+.3f} ret={ret[m].mean():+.2f}% win={np.mean(ret[m]>0):.2f}")
print("== raw open->close drift t-stat, no stop, by era")
for nm,m in [("all",df.year>0),("pre16",df.year<=2015),("post16",df.year>2015)]:
    x=-df.oc_pct[m]; print(nm, m.sum(), f"mean short oc={x.mean():+.2f}% t={x.mean()/(x.std()/np.sqrt(m.sum())):.2f} median={x.median():+.2f}")
print("== hourly subset (n=11): where does the day-1 drift happen?")
hs=df[df.h1_close_pct.notna()][["report_date","gap_pct","h1_close_pct","h1_to_close_pct","oc_pct","first_break"]]
print(hs.round(2).to_string()); print("mean open->10:30",hs.h1_close_pct.mean().round(2),"10:30->close",hs.h1_to_close_pct.mean().round(2),"open->close",hs.oc_pct.mean().round(2))
print("== day-2 context: short day1 open -> day2 close (no stop)")
x=-(df.close_d2/df.open-1)*100; print("mean",x.mean().round(2),"median",x.median().round(2))
