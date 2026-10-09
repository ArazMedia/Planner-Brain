import json, collections, statistics as stt
from calib import *
BASES = [s for s in STRUCTS if s.name in ('Oct9 375C', 'Oct9 370/375C', 'Oct9 370/380C', 'Oct9 375/385C', 'Oct12 370/380C', 'Oct16 375/385C')]
VARS = [('framework as run (grade C, daily stops)', dict(grade='C')),
        ('math-only (grade B assumed), daily stops', dict(grade='B')),
        ('grade B, intraday stops', dict(grade='B', stop_mode='intraday')),
        ('grade B, no cap/min/demotion, daily stops', dict(grade='B', cap=False, driftmin=False, demote=False)),
        ('grade B, no cap/min/demotion, intraday stops', dict(grade='B', cap=False, driftmin=False, demote=False, stop_mode='intraday'))]
OUT = {}
for mode in ('expanding', 'loo'):
    for vn, kw in VARS:
        rows = run_calib(BASES, mode=mode, **kw)
        c = collections.Counter(r['verdict'] for r in rows)
        def agg(v):
            R = [r for r in rows if r['verdict'] == v]
            if not R: return None
            return dict(n=len(R), win=sum(r['real'] > 0 for r in R) / len(R), mean_real=stt.mean(r['real'] for r in R),
                        mean_real_pct=stt.mean(r['real'] / r['debit'] for r in R), mean_ev=stt.mean(r['ev'] for r in R))
        allR = dict(n=len(rows), win=sum(r['real'] > 0 for r in rows) / len(rows), mean_real=stt.mean(r['real'] for r in rows),
                    mean_real_pct=stt.mean(r['real'] / r['debit'] for r in rows))
        per = {}
        for b in BASES:
            R = [r for r in rows if r['struct'] == b.name]
            if R: per[b.name] = dict(n=len(R), verdicts=dict(collections.Counter(r['verdict'] for r in R)), win=sum(r['real'] > 0 for r in R) / len(R),
                                     mean_real=stt.mean(r['real'] for r in R), mean_pct=stt.mean(r['real'] / r['debit'] for r in R),
                                     skip_right=sum(1 for r in R if r['verdict'] == 'SKIP' and r['real'] <= 0), skip_wrong=sum(1 for r in R if r['verdict'] == 'SKIP' and r['real'] > 0))
        OUT[f'{mode}|{vn}'] = dict(counts=dict(c), TAKE=agg('TAKE'), WATCH=agg('WATCH'), SKIP=agg('SKIP'), ALL=allR, per=per,
                                   skip_right=sum(1 for r in rows if r['verdict'] == 'SKIP' and r['real'] <= 0),
                                   skip_wrong=sum(1 for r in rows if r['verdict'] == 'SKIP' and r['real'] > 0),
                                   n_events=len({r['day'] for r in rows}))
        o = OUT[f'{mode}|{vn}']
        print(mode, vn, o['counts'], 'events', o['n_events'], 'SKIP right/wrong', o['skip_right'], o['skip_wrong'],
              'TAKE', o['TAKE'] and {k: round(v, 2) for k, v in o['TAKE'].items()}, 'WATCH', o['WATCH'] and {k: round(v, 2) for k, v in o['WATCH'].items()},
              'ALL', {k: round(v, 2) for k, v in allR.items()})
json.dump(OUT, open('phase3c.json', 'w'), indent=1, default=float)
