"""Fail-closed local task scheduler and durable transition log; never runs Codex itself."""
import argparse
import json
import sys
from pathlib import Path
from .common import ROOT, load_json
from .evidence import artifact_path, atomic_json, candidate, stamp

STATES = {'pending','ready','in_progress','blocked','verified'}
DEFAULT_STATE = 'artifacts/control-plane/tasks-state.json'

def definitions(root=ROOT):
    data=load_json(root/'control-plane/tasks.json')
    if data.get('schema_version') != 1: raise ValueError('invalid task schema')
    tasks=data.get('tasks',[])
    ids=[t['id'] for t in tasks]
    if len(ids)!=len(set(ids)) or not tasks: raise ValueError('duplicate or empty task graph')
    index={t['id']:t for t in tasks}
    for t in tasks:
        if t['id'] in t.get('depends_on',[]) or not set(t.get('depends_on',[])).issubset(index):
            raise ValueError('bad task dependency '+t['id'])
    visited=set(); active=set()
    def visit(key):
        if key in active: raise ValueError('task graph cycle')
        if key in visited: return
        active.add(key)
        for dep in index[key]['depends_on']: visit(dep)
        active.remove(key); visited.add(key)
    for k in ids: visit(k)
    return tasks

def state_at(path=DEFAULT_STATE, *, root=ROOT):
    path=artifact_path(path,root)
    if path.exists():
        state=load_json(path)
        if state.get('schema_version')!=1: raise ValueError('invalid state schema')
    else: state={'schema_version':1,'tasks':{},'history':[]}
    return state

def statuses(tasks, state):
    complete={key for key,value in state['tasks'].items() if value.get('status')=='verified'}
    result=[]
    for task in tasks:
        old=state['tasks'].get(task['id'],{}).get('status','pending')
        eligible=all(key in complete for key in task['depends_on'])
        status='ready' if old=='pending' and eligible else old
        result.append({**task,'status':status,'eligible':eligible})
    return result

def transition(task_id, action, state, tasks, *, gate_verdict=None, root=ROOT, reason=''):
    index={t['id']:t for t in tasks}
    if task_id not in index: raise ValueError('unknown task')
    current={t['id']:t for t in statuses(tasks,state)}[task_id]
    old=current['status']
    transitions={'start':({'ready'},'in_progress'), 'block':({'ready','in_progress','blocked'},'blocked'),
                 'resume':({'blocked'},'in_progress'), 'verify':({'in_progress'},'verified'), 'manual-verify':({'in_progress'},'verified')}
    allowed,new=transitions[action]
    if old not in allowed: raise ValueError(f'illegal transition {old} -> {action}')
    if action in {'start','resume','verify','manual-verify'} and not current['eligible']: raise ValueError('dependencies not verified')
    snapshot=candidate(root)
    if action in {'verify','manual-verify'}:
        if not gate_verdict: raise ValueError('verification gate artifact required')
        verdict=load_json(artifact_path(gate_verdict, root, must_exist=True))
        if (verdict.get('status')!='passed' or verdict.get('gate')!=current['gate']
            or verdict.get('candidate',{}).get('sha256')!=snapshot['sha256']):
            raise ValueError('gate absent, wrong type, or stale')
        if current.get('manual') != (action=='manual-verify'):
            raise ValueError('manual task requires manual-verify; ordinary tasks require verify')
        if action=='manual-verify':
            qualification=load_json(root/'control-plane/client-qualification.json')
            if (qualification.get('status') != 'QUALIFIED' or not qualification.get('effective_permissions_verified')
                or not qualification.get('network_denial_verified') or not qualification.get('subagent_inheritance_verified')):
                raise ValueError('client/host qualification not independently recorded')
    state['tasks'][task_id]={'status':new,'candidate_sha256':snapshot['sha256'], 'updated_at_utc':stamp(), 'reason':reason[:240]}
    state['history'].append({'task':task_id,'action':action,'at_utc':stamp(), 'candidate_sha256':snapshot['sha256']})
    return new

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('action',choices=['status','next','start','block','resume','verify','manual-verify'])
    ap.add_argument('--task');ap.add_argument('--state',default=DEFAULT_STATE)
    ap.add_argument('--gate-verdict');ap.add_argument('--reason',default='')
    a=ap.parse_args()
    try:
        tasks=definitions(); state=state_at(a.state)
        if a.action=='status': print(json.dumps(statuses(tasks,state),indent=2));return 0
        if a.action=='next':
            ready=[t for t in statuses(tasks,state) if t['status']=='ready']
            print(json.dumps(ready,indent=2));return 0 if ready else 2
        if not a.task: ap.error('--task required')
        transition(a.task,a.action,state,tasks,gate_verdict=a.gate_verdict,reason=a.reason)
        atomic_json(artifact_path(a.state),state)
    except (ValueError,OSError,KeyError,json.JSONDecodeError) as e: ap.error(str(e))
    print(a.task, state['tasks'][a.task]['status'])
    return 0
if __name__=='__main__':sys.exit(main())
