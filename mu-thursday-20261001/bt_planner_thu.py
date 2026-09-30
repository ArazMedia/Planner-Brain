"""Planner independent Thursday (day-1) backtest for MU. Proposal/research only.
PRE-DECLARED RULES (fixed before computing P&L; declared after seeing yesterday's 2015+ per-print moves,
so 2001-2015 prints act as the quasi out-of-sample check):
  R0  DAY1-SHORT      : short at day-1 open, any gap, cover at close.  (tests the day-1 intraday drift)
  R1  CONTINUATION    : trade in gap direction open->close, |gap|>=3%.   (R1 fade = -R1)
  R2  FADE-GAP-UP     : short at open if gap >= +3%, cover at close.
  R3  CONT-GAP-DOWN   : short at open if gap <= -3%, cover at close.
  R4  REGIME          : R0 restricted to 20d run-up > +10% at the report close.
  R5  OR60 (hourly)   : 2023-10+ only (yfinance 1h). At 10:30, trade in direction of first-hour candle
                        (close vs open); stop = other side of first-hour range; exit at close. Descriptive.
Stock execution: entry at open (R5: 10:30 close) with 0.10% adverse slippage; exit at close 0.10% slippage;
  hard stop 3% from entry (sensitivity 2/4/none); daily bars can't order H vs L, so if the stop level is touched
  the stop is ASSUMED HIT (conservative), fill = stop + 0.20% slippage.
Options execution (Oct 2 expiry, entered Thu): vertical debit spread, long strike = nearest $5 to entry price
  (ATM), short strike W further OTM in trade direction. Black-Scholes, flat vol (no skew), r=4%.
  T_entry = 2/252 (Thu open -> Fri close, trading-time), exit at Thu close T=1/252; stop exit at T=1.5/252.
  IV: entry post-crush IV base 55% (sens 45/70); exit IV = entry - 3 pts. Costs: each leg pays full half-spread
  on entry and exit (width $0.80 base, $1.20 stress) + $0.05/contract/leg fees.
Historical % moves are applied to a Thursday open of S0 (default 1065).
"""
import pandas as pd, numpy as np, sys
from math import log, sqrt, exp
from math import erf
class norm:
    @staticmethod
    def cdf(x): return 0.5*(1+erf(x/sqrt(2)))
rng=np.random.default_rng(7)
df=pd.read_csv("day1_planner.csv"); df["era"]=np.where(df.year<=2015,"2001-15","2016-26")
S0=1065.0; SLIP=0.001; SSLIP=0.002
def bs(S,K,T,v,cp,r=0.04):
    d1=(log(S/K)+(r+v*v/2)*T)/(v*sqrt(T)); d2=d1-v*sqrt(T)
    return S*norm.cdf(d1)-K*exp(-r*T)*norm.cdf(d2) if cp=="C" else K*exp(-r*T)*norm.cdf(-d2)-S*norm.cdf(-d1)

def stock_trade(row, side, stop=0.03, entry=None, entry_px_pct=0.0, hi=None, lo=None, stop_px=None):
    """returns (ret_pct_of_entry, R_units, exit_kind, exit_px_rel) ; prices relative to open=1"""
    o=1.0+entry_px_pct/100
    H=1+row.hi_from_open_pct/100 if hi is None else hi; L=1+row.lo_from_open_pct/100 if lo is None else lo
    C=1+row.oc_pct/100
    e=o*(1+SLIP*side)
    if stop_px is not None: sp=stop_px
    elif stop is None: sp=None
    else: sp=e*(1-stop*side)
    risk=abs(e-sp)/e if sp is not None else 0.03
    if sp is not None and ((side>0 and L<=sp) or (side<0 and H>=sp)):
        x=sp*(1-SSLIP*side); kind="stop"
    else:
        x=C*(1-SLIP*side); kind="close"
    ret=side*(x/e-1)
    return ret, ret/risk, kind, x

def spread_pnl(side, entry_rel, exit_rel, exit_T, iv=0.55, W=15, width=0.80, S=S0):
    """per-contract $ P&L of a 1-lot vertical debit spread; returns (pnl, max_loss)"""
    Se=S*entry_rel; K1=round(Se/5)*5; K2=K1+W*side; cp="C" if side>0 else "P"
    Te=2/252; ivx=iv-0.03
    deb=bs(Se,K1,Te,iv,cp)-bs(Se,K2,Te,iv,cp); cost_in=width  # 2 legs x half-width
    Sx=S*exit_rel; val=bs(Sx,K1,exit_T,ivx,cp)-bs(Sx,K2,exit_T,ivx,cp); cost_out=width
    fees=4*0.05/100
    paid=deb+cost_in/1; pnl=(val-cost_out/1)-paid-fees
    # width per leg: half-spread per leg = width/2, two legs -> width per side
    return pnl*100, (paid+fees)*100, deb, K1, K2

def stats(p, R=None, label=""):
    p=np.asarray(p,float); n=len(p)
    if n==0: return dict(rule=label,n=0)
    bs_=rng.choice(p,(10000,n)).mean(1); lo,hi=np.percentile(bs_,[5,95])
    loo=[np.delete(p,i).mean() for i in range(n)] if n>1 else [np.nan]
    return dict(rule=label,n=n,win=(p>0).mean(),mean=p.mean(),median=np.median(p),ci5=lo,ci95=hi,loo_min=min(loo),loo_max=max(loo),
                p_boot_le0=(bs_<=0).mean())

def run(stop=0.03, iv=0.55, W=15, width=0.80, S=S0, out=True):
    rules={"R0 DAY1-SHORT":lambda r:-1,
           "R1 CONTINUATION |gap|>=3":lambda r:(np.sign(r.gap_pct) if abs(r.gap_pct)>=3 else 0),
           "R1f FADE |gap|>=3":lambda r:(-np.sign(r.gap_pct) if abs(r.gap_pct)>=3 else 0),
           "R2 FADE-GAP-UP >=+3":lambda r:(-1 if r.gap_pct>=3 else 0),
           "R3 CONT-GAP-DOWN <=-3":lambda r:(-1 if r.gap_pct<=-3 else 0),
           "R4 DAY1-SHORT runup20>10":lambda r:(-1 if r.runup20_pct>10 else 0)}
    recs=[]
    for name,f in rules.items():
        for _,r in df.iterrows():
            s=f(r)
            if s==0: continue
            ret,Ru,kind,x=stock_trade(r,s,stop)
            ret_nostop=s*((1+r.oc_pct/100)*(1-SLIP*s)/(1+SLIP*s)-1)
            exT=1.5/252 if kind=="stop" else 1/252
            pnl,ml,deb,K1,K2=spread_pnl(s,1.0,x,exT,iv,W,width,S)
            recs.append(dict(rule=name,report_date=r.report_date,era=r.era,year=r.year,side=s,gap=r.gap_pct,oc=r.oc_pct,
                ret_pct=ret*100,R=Ru,exit=kind,ret_nostop_pct=ret_nostop*100,opt_pnl=pnl,opt_R=pnl/ml,opt_maxloss=ml,opt_debit=deb,K1=K1,K2=K2))
    # R5 hourly
    hsub=df[df.h1_close_pct.notna()]
    for _,r in hsub.iterrows():
        s=1 if r.h1_close_pct>0 else -1
        o=r.open; e_rel=r.h1_close/o
        sp=(r.h1_low/o) if s>0 else (r.h1_high/o)
        # after-10:30 high/low unknown in daily; use the hourly bars
        ret,Ru,kind,x=stock_trade(r,s,None,entry_px_pct=(e_rel-1)*100,stop_px=sp,
            hi=r.post1030_hi/o, lo=r.post1030_lo/o)
        pnl,ml,deb,K1,K2=spread_pnl(s,e_rel,x,1.5/252 if kind=="stop" else 1/252,iv,W,width,S)
        recs.append(dict(rule="R5 OR60 first-hour dir (hourly)",report_date=r.report_date,era=r.era,year=r.year,side=s,gap=r.gap_pct,oc=r.oc_pct,
            ret_pct=ret*100,R=Ru,exit=kind,ret_nostop_pct=s*(r.close/r.h1_close-1)*100,opt_pnl=pnl,opt_R=pnl/ml,opt_maxloss=ml,opt_debit=deb,K1=K1,K2=K2))
    t=pd.DataFrame(recs)
    return t

if __name__=="__main__":
    t=run()
    t.to_csv("trades_base.csv",index=False,float_format="%.4f")
    pd.set_option("display.width",250); pd.set_option("display.max_columns",30)
    rows=[]
    for rule,g in t.groupby("rule",sort=False):
        for cut,gg in [("ALL",g),("2001-15",g[g.era=="2001-15"]),("2016-26",g[g.era=="2016-26"]),("last12",g.tail(12))]:
            s=stats(gg.R.values,label=rule); s.update(cut=cut,stock_ret_mean=gg.ret_pct.mean(),nostop_mean=gg.ret_nostop_pct.mean(),
                stopped=(gg.exit=="stop").mean(),opt_R=gg.opt_R.mean(),opt_usd=gg.opt_pnl.mean())
            if gg.opt_pnl.notna().any():
                so=stats(gg.opt_pnl.dropna().values); s.update(opt_ci5=so["ci5"],opt_ci95=so["ci95"],opt_win=so["win"])
            rows.append(s)
    S=pd.DataFrame(rows)
    print(S[["rule","cut","n","win","mean","ci5","ci95","loo_min","loo_max","p_boot_le0","stock_ret_mean","nostop_mean","stopped","opt_R","opt_usd","opt_ci5","opt_ci95","opt_win"]].round(3).to_string())
    S.to_csv("summary_base.csv",index=False,float_format="%.4f")
