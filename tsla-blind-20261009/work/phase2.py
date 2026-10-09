import json, re
from fw import *
Q = {}
for tag, d in (('10:13', '1029'), ('12:38', '1247')):
    J = json.load(open(f'/workspace/plans/20261008-goog-uso-mu-watch/data/{d}/TSLA.json')); data = J.get('data', J)
    for o in data['options']:
        m = re.match(r'TSLA(\d{6})([CP])(\d{8})', o['option'])
        if m and m.group(2) == 'C': Q[(tag, m.group(1), int(m.group(3)) / 1000)] = (o['bid'], o['ask'])
def real_exit(st, tag):
    lb, la = Q[(tag, st.exp, st.kl)]
    if st.ks:
        sb, sa = Q[(tag, st.exp, st.ks)]; return 100 * (lb - sa), 100 * ((lb + la) / 2 - (sb + sa) / 2)
    return 100 * lb, 100 * (lb + la) / 2
def model_exit(st, S, Trem):
    return 100 * st.value(S, Trem) - st.legs_hs(S, Trem)
rows = []
for st in STRUCTS:
    D0 = st.debit(); Dfull = D0 + st.legs_hs(SPOT, st.T)
    T_close8 = st.T - st.T_inc[0]
    r = dict(name=st.name, debit=D0, debit_full=Dfull)
    r['stop_5m'] = model_exit(st, 369.88, st.T - st.T_inc[0] * (15 / 140))       # 5m close <370.25 at 13:45 -> out ~13:50
    r['close8'] = model_exit(st, 375.00, T_close8)
    r['q1013_bid'], r['q1013_mid'] = real_exit(st, '10:13')
    r['q1238_bid'], r['q1238_mid'] = real_exit(st, '12:38')
    r['hi'] = model_exit(st, 388.55, max(st.T - st.T_inc[0] - (0.25 + 20 / 390) / 252, 0)) if st.exp != '261009' else 100 * st.payoff(388.55) - st.legs_hs(388.55, 1e-6) + (100 * (st.value(388.55, (370 / 390) / 252) - st.payoff(388.55)))
    r['settle_now'] = 100 * st.payoff(383.08) if st.exp == '261009' else None
    rows.append(r)
json.dump(rows, open('phase2.json', 'w'), indent=1)
for r in rows:
    pnl = lambda v: f"{v - r['debit']:+.0f} ({100*(v - r['debit'])/r['debit']:+.0f}%)"
    print(f"{r['name']:17s} D={r['debit']:.0f} stop5m={pnl(r['stop_5m'])} close8={pnl(r['close8'])} 10:13bid={pnl(r['q1013_bid'])} 12:38bid={pnl(r['q1238_bid'])} hi~{pnl(r['hi'])} settle@383.08={pnl(r['settle_now']) if r['settle_now'] is not None else '-'}")
