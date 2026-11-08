"""Bounded retry for explicitly transient, read-only verification commands.

Never retries arbitrary failed implementation commands or external side effects.
"""
import argparse
import json
import sys
from .record import execute
from .evidence import artifact_path, atomic_json, candidate, stamp

ALLOWLIST = {'python','python3','pytest'}

def run(check, argv, attempts=2, timeout=90, minimum_tests=0):
    if not 1<=attempts<=3: raise ValueError('attempts must be 1..3')
    if not argv or argv[0].split('/')[-1] not in ALLOWLIST: raise ValueError('only allowlisted local test executables may be retried')
    if argv[0].split('/')[-1] in ('python','python3') and (len(argv)<3 or argv[1:3] not in [['-m','unittest'],['-m','pytest']]):
        raise ValueError('only unittest and pytest module invocation permitted')
    results=[]
    for _ in range(attempts):
        receipt=execute(check,argv,timeout,minimum_tests=minimum_tests)
        results.append(receipt)
        if receipt['status']=='passed': break
        # Don't retry deterministic test failures or mutation of candidate.
        if receipt['status'] != 'blocked' or not receipt['candidate_unchanged']: break
    return {'schema_version':1,'check':check,'attempts':results,'final':results[-1],
            'note':'Blocked transient execution attempts are retried only; failing test assertions do not receive blind retries.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',required=True);ap.add_argument('--output',required=True)
    ap.add_argument('--attempts',type=int,default=2);ap.add_argument('--timeout',type=int,default=90)
    ap.add_argument('--minimum-tests',type=int,default=0);ap.add_argument('argv',nargs=argparse.REMAINDER)
    a=ap.parse_args();argv=a.argv[1:] if a.argv[:1]==['--'] else a.argv
    try: obj=run(a.check,argv,a.attempts,a.timeout,a.minimum_tests);atomic_json(artifact_path(a.output),obj)
    except (OSError,ValueError) as e:ap.error(str(e))
    print(obj['final']['status'],'attempts',len(obj['attempts']))
    return 0 if obj['final']['status']=='passed' else 2
if __name__=='__main__':sys.exit(main())
