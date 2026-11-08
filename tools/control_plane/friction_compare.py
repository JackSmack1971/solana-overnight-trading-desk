"""Evaluate before/after command outcomes for a friction proposal without mutation.

Evidence is local self-report; a human reviewer still decides whether to apply a fix.
"""
import argparse
import json
import sys
from .evidence import artifact_path, atomic_json, stamp

def compare(before, after):
    if any(r.get('schema_version') != 2 or r.get('source') != 'local-command' for r in (before,after)):
        raise ValueError('expected v2 command receipts')
    if before.get('check') != after.get('check'): raise ValueError('unrelated checks cannot be compared')
    if before.get('candidate',{}).get('sha256') == after.get('candidate',{}).get('sha256'):
        raise ValueError('no candidate change; cannot attribute remediation')
    if before.get('status') != 'blocked' or after.get('status') != 'passed':
        return {'result':'INCONCLUSIVE','reason':'not a blocked-to-passed transition'}
    if after.get('candidate_unchanged') is not True:
        return {'result':'INCONCLUSIVE','reason':'candidate mutated during verification'}
    return {'result':'CANDIDATE_IMPROVEMENT','reason':'Observed blocked-to-passed transition; causality and regression freedom are not established'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--before',required=True);ap.add_argument('--after',required=True);ap.add_argument('--output',required=True)
    a=ap.parse_args()
    try:
        before=json.loads(artifact_path(a.before,must_exist=True).read_text())
        after=json.loads(artifact_path(a.after,must_exist=True).read_text())
        result=compare(before,after)
        atomic_json(artifact_path(a.output),{'schema_version':1,'evaluated_at_utc':stamp(),
                  'check':before.get('check'),'before_candidate':before.get('candidate',{}).get('sha256'),
                  'after_candidate':after.get('candidate',{}).get('sha256'),**result})
    except (ValueError,OSError,json.JSONDecodeError) as e:ap.error(str(e))
    print(result['result'],result['reason']);return 0 if result['result']=='CANDIDATE_IMPROVEMENT' else 2
if __name__=='__main__':sys.exit(main())
