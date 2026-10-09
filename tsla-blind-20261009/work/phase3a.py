import json
from fw import *
VARS = [
 ('base (framework as run)', {}),
 ('no mkt+10pp cap', dict(cap=False)),
 ('no drift-neutral min (TAKE ignores EV_B)', dict(driftmin=False)),
 ('intraday stops (5m/15m close < 370.25 or low < 368.04)', dict(stop_mode='intraday')),
 ('no WATCH->SKIP demotion', dict(demote=False)),
 ('1DTE convexity: empirical payoff distribution', dict(convex=True)),
 ('grade gate relaxed to B (RA sens: volume +1 -> +0.70)', dict(grade_override=('B', 0.70))),
 ('ALL toward-flat removed (cap, min, demotion, grade B), daily stops', dict(cap=False, driftmin=False, demote=False, grade_override=('B', 0.70))),
 ('ALL toward-flat removed + intraday stops (honest net)', dict(cap=False, driftmin=False, demote=False, grade_override=('B', 0.70), stop_mode='intraday')),
 ('ALL toward-flat removed + intraday stops + convexity', dict(cap=False, driftmin=False, demote=False, grade_override=('B', 0.70), stop_mode='intraday', convex=True)),
]
out = []
for st in STRUCTS:
    for name, kw in VARS:
        r = evaluate(st, **kw)
        evu = r['ev_cvx'] if kw.get('convex') else r['ev']
        out.append(dict(struct=st.name, var=name, ev=evu, ev_lo=r['ev_lo'], ev_b=r['ev_b'], p_t=r['p']['t'], p_s=r['p']['s'], mkt_t=r['mkt']['t'],
                        capped=r['capped'], verdict=r['verdict'], n_own=r['n_own'], own=r['own'], debit=r['debit']))
json.dump(out, open('phase3a.json', 'w'), indent=1, default=float)
for o in out:
    if o['struct'] in ('Oct9 375/385C', 'Oct9 370/380C', 'Oct9 375C', 'Oct16 375/385C', 'Oct9 370/375C'):
        print(f"{o['struct']:15s} {o['var'][:55]:55s} p_t={o['p_t']:.2f} p_s={o['p_s']:.2f} mkt={o['mkt_t']:.2f} cap={o['capped']!s:5} EV={o['ev']:+5.0f} lo={o['ev_lo']:+5.0f} EVB={o['ev_b']:+5.0f} {o['verdict']}  own={o['own']}")
