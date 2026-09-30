import pandas as pd, numpy as np, bt_planner_thu as B
from math import sqrt
# generalized spread: placement 'atm' (long at entry) or 'ctr' (strikes straddle entry)
def spread(side, x_rel, exT, iv, W, width, place, S=B.S0):
    Se=S; cp="C" if side>0 else "P"
    if place=="atm": K1=round(Se/5)*5; K2=K1+W*side
    else: mid=round(Se/5)*5; K1=mid-side*W/2; K2=mid+side*W/2
    deb=B.bs(Se,K1,2/252,iv,cp)-B.bs(Se,K2,2/252,iv,cp)
    Sx=S*x_rel; val=B.bs(Sx,K1,exT,iv-0.03,cp)-B.bs(Sx,K2,exT,iv-0.03,cp)
    paid=deb+width+0.002; pnl=(val-width)-paid
    return pnl*100, paid*100
df=B.df
rows=[]
for rule,filt in [("R0",lambda r:True),("R3",lambda r:r.gap_pct<=-3),("R4",lambda r:r.runup20_pct>10)]:
  sub=df[[filt(r) for _,r in df.iterrows()]]
  for place in ["atm","ctr"]:
    for W in [10,15,20]:
      for width in [0.40,0.80,1.20]:   # round-trip cost per side = width (2 legs x half-width)
        for iv in [0.45,0.55,0.70]:
          P=[];ML=[];E=[]
          for _,r in sub.iterrows():
              ret,Ru,kind,x=B.stock_trade(r,-1,0.03)
              p,ml=spread(-1,x,1.5/252 if kind=="stop" else 1/252,iv,W,width,place)
              P.append(p);ML.append(ml);E.append(r.era)
          P=np.array(P);ML=np.array(ML);E=np.array(E)
          rows.append(dict(rule=rule,place=place,W=W,cost_per_side=width,iv=iv,n=len(P),maxloss=ML.mean(),EV_usd=P.mean(),EV_R=(P/ML).mean(),
             EV_R_pre16=(P/ML)[E=="2001-15"].mean(),EV_R_post16=(P/ML)[E=="2016-26"].mean(),win=(P>0).mean()))
G=pd.DataFrame(rows); G.to_csv("grid_options.csv",index=False,float_format="%.4f")
pd.set_option("display.width",200)
print(G[(G.iv==0.55)].round(3).to_string())
print(G.groupby(["rule","place","cost_per_side"]).EV_R.agg(["min","max"]).round(3))
