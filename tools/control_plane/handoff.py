"""Durable restart snapshot. Read-only collection of Git and task state."""
import argparse
import json
import subprocess
import sys
from .common import ROOT
from .evidence import candidate, artifact_path, atomic_json, stamp
from .tasks import definitions, state_at, statuses

def git(*argv):
    try:
        p=subprocess.run(['git',*argv],cwd=ROOT,timeout=15,capture_output=True,text=True)
        # No filenames/diff content persisted in handoff; keep only status summary.
        return {'available':p.returncode==0, 'exit_code':p.returncode,
                'entry_count':len(p.stdout.splitlines()) if p.returncode==0 else None}
    except (OSError,subprocess.TimeoutExpired):return {'available':False,'exit_code':None,'entry_count':None}

def snapshot():
    state=state_at(); tasks=statuses(definitions(),state)
    return {'schema_version':1,'captured_at_utc':stamp(),'candidate':candidate(),
            'git_status':git('status','--porcelain=v1','--untracked-files=all'),
            'git_worktrees':git('worktree','list','--porcelain'),
            'task_status':[{'id':t['id'],'status':t['status'],'eligible':t['eligible']} for t in tasks],
            'next_eligible':[t['id'] for t in tasks if t['status']=='ready'],
            'cautions':['Re-inspect actual Git diffs before edits','Existing gate evidence may be stale',
                        'No automatic retry of non-idempotent actions','Unverified host remains unqualified']}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
    try: data=snapshot();atomic_json(artifact_path(a.output),data)
    except (ValueError,OSError) as e:ap.error(str(e))
    print('handoff captured; git baseline', 'present' if data['git_status']['available'] else 'UNAVAILABLE')
    return 0
if __name__=='__main__':sys.exit(main())
