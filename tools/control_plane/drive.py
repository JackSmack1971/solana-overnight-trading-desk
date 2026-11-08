"""Conservative Codex CLI handoff for the next eligible implementation task.

Opt-in subprocess runner. Does not grant permissions, certify Codex support,
commit changes, auto-approve independent review, or promote gate state.
"""
import argparse
import json
import shutil
import subprocess
import sys
from .tasks import definitions, state_at, statuses, transition, DEFAULT_STATE
from .context import compile_brief
from .evidence import artifact_path, atomic_json, stamp


def choose(tasks, state):
    active=[t for t in statuses(tasks,state) if t['status']=='in_progress']
    if active: raise ValueError('in-progress tasks exist; resume/review before dispatching new writer')
    available=[t for t in statuses(tasks,state) if t['status']=='ready' and not t['manual']]
    return available[0] if available else None

def prompt(task):
    return ('You are working inside the Solana Desk project with root and scoped AGENTS.md. '
            'Before editing, inspect Git status and actual diffs, read the canonical blueprint and relevant tests. '
            'Implement only this smallest authorized slice; do not invent economic decisions or permission changes. '
            'Task: '+task['id']+' — '+task['description']+'. '
            'Read control-plane/tasks.json and docs/control-plane/orchestration-v1.1.md. '
            'Begin with a narrow task context using python3 -m tools.control_plane.context --task '+task['id']+
            ' --output artifacts/control-plane/'+task['id']+'-context.json. '
            'If the phase is too broad, complete only one contract-backed slice, report work remaining, and DO NOT mark the phase verified. '
            'Run focused and required tests. Record actual checks with tools.control_plane.record; '
            'get an independent review and current gate verdict before requesting verification. '
            'Never fabricate human review evidence, promote phase state from prose, or attempt any live trading operation. '
            'Stop on new undecided product/economic/security decisions. '
            'Report changed files, exact tests, blockers, and next eligible action.')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--execute',action='store_true', help='explicitly invoke installed codex exec')
    ap.add_argument('--timeout',type=int,default=1800)
    ap.add_argument('--state',default=DEFAULT_STATE)
    ap.add_argument('--task')
    args=ap.parse_args()
    if args.timeout<60 or args.timeout>7200:ap.error('timeout range 60..7200')
    try:
        tasks=definitions();state=state_at(args.state)
        selected=choose(tasks,state)
        if args.task and (not selected or args.task!=selected['id']):
            raise ValueError('task is not next eligible or another task is in progress')
        if selected is None:
            print('BLOCKED: no eligible non-manual task; inspect tasks next or manual gate')
            return 2
        plan={'task_id':selected['id'],'prompt':prompt(selected),'command':['codex','exec','<task-specific-prompt>'],
              'permissions':'inherited from local Codex config and CLI invocation; no override provided'}
        if not args.execute:
            print(json.dumps(plan,indent=2))
            return 0
        if shutil.which('codex') is None: raise ValueError('codex executable not found; no execution performed')
        # The agent is an implementation writer. Gate verification is a separate stage.
        transition(selected['id'],'start',state,tasks)
        atomic_json(artifact_path(args.state),state)
        started=stamp()
        try:
            outcome=subprocess.run(['codex','exec',plan['prompt']],timeout=args.timeout,
                                   stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=False)
            code=outcome.returncode
        except (OSError,subprocess.TimeoutExpired):code=None
        result={'schema_version':1,'task_id':selected['id'],'started_at_utc':started,
                'ended_at_utc':stamp(),'exit_code':code,'state':'in_progress',
                'note':'Agent execution ended; candidate unverified. Inspect diff, test receipts and independent reviewer decision.'}
        atomic_json(artifact_path('artifacts/control-plane/last-drive.json'),result)
        print(json.dumps(result,indent=2))
        return 0 if code==0 else 2
    except (ValueError,OSError,KeyError) as e:ap.error(str(e))
if __name__=='__main__':sys.exit(main())
