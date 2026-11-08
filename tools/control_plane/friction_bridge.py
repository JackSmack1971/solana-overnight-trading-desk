"""Limited friction observations from structured receipts; no raw commands stored."""
import argparse
import json
import sys
from tools.friction.core import record as record_incident
from .evidence import artifact_path

# Explicitly conservative: failed tests are application defects, NOT friction.
# Only environment/runner-blocked receipts can be classified automatically.
def classify(receipt):
    if receipt.get('schema_version')!=2 or receipt.get('source')!='local-command':return None
    if receipt.get('status')!='blocked' or receipt.get('candidate_unchanged') is not True:return None
    if receipt.get('exit_code') is not None:return None
    return {'category':'test-runner','shell':'python','tool':'verification-runner',
            'failure_code':'invocation-blocked','outcome':'unresolved'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--receipt',required=True);ap.add_argument('--db',help='external absolute database path')
    a=ap.parse_args()
    try:
        raw=json.loads(artifact_path(a.receipt,must_exist=True).read_text())
        data=classify(raw)
        if data: result=record_incident(a.db,**data);print(json.dumps(result))
        else:print('SKIP: no permitted friction classification')
    except (OSError,ValueError,json.JSONDecodeError) as e:ap.error(str(e))
    return 0
if __name__=='__main__':sys.exit(main())
