"""Conservative concurrency planner; no automatic git worktrees/merges."""
import argparse
import json
import sys
from pathlib import PurePosixPath
from .tasks import definitions, statuses, state_at

def conflicts(first, second):
    for a in first['scope']:
        for b in second['scope']:
            a=a.rstrip('/');b=b.rstrip('/')
            if a==b or a.startswith(b+'/') or b.startswith(a+'/'):return True
    return False

def plan(tasks, state, maximum=3):
    if not 1 <= maximum <= 3: raise ValueError('max agents must be 1..3')
    ready=[t for t in statuses(tasks,state) if t['status']=='ready' and not t.get('manual')]
    chosen=[];rejected=[]
    for t in ready:
        if len(chosen)==maximum:rejected.append({'id':t['id'],'reason':'capacity'});continue
        if any(conflicts(t, other) for other in chosen):
            rejected.append({'id':t['id'],'reason':'write-set overlap'});continue
        chosen.append(t)
    return {'parallel_candidates':[t['id'] for t in chosen],'deferred':rejected,
            'notice':'Only a read-only scheduling suggestion. Writers must use isolated worktrees and single-owner integration.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--max',type=int,default=3);a=ap.parse_args()
    try: result=plan(definitions(),state_at(),a.max)
    except ValueError as e:ap.error(str(e))
    print(json.dumps(result,indent=2));return 0
if __name__=='__main__':sys.exit(main())
