"""Encode an explicit independent reviewer assertion; never generate automatic approval."""
import argparse
import sys
from .evidence import candidate, artifact_path, atomic_json, stamp

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    ap.add_argument('--reviewer-id', required=True, help='Non-secret opaque reviewer identifier')
    ap.add_argument('--kind', choices=['independent','operator-host'], default='independent')
    ap.add_argument('--decision', choices=['APPROVE_FOR_NEXT_GATE','BLOCKED','INCONCLUSIVE'], required=True)
    ap.add_argument('--findings-count', type=int, required=True)
    ap.add_argument('--review-note', required=True, help='Short finding IDs or reference, not secrets')
    a=ap.parse_args()
    if a.findings_count < 0 or (a.decision == 'APPROVE_FOR_NEXT_GATE' and a.findings_count):
        ap.error('approval requires zero findings')
    if not a.reviewer_id.strip() or not a.review_note.strip(): ap.error('nonempty reviewer id/note required')
    c=candidate()
    if a.kind=='operator-host' and a.decision != 'APPROVE_FOR_NEXT_GATE':
        ap.error('operator-host evidence must be an affirmative qualification review')
    ok=a.decision=='APPROVE_FOR_NEXT_GATE'
    receipt={'schema_version':2,'check':'independent-diff-review','source':'independent-review',
             'status':'passed' if ok else 'blocked', 'exit_code':0 if ok else 2,
             'candidate_unchanged':True,'candidate':c,'reviewer_role':'independent-reviewer',
             'reviewer_id':a.reviewer_id,'review_note':a.review_note,'decision':a.decision,
             'findings_count':a.findings_count, 'started_at_utc':stamp(),'ended_at_utc':stamp()}
    if a.kind=='operator-host':
        receipt.update(check='operator-host-review',source='operator-review', operator_id=a.reviewer_id,decision='QUALIFIED')
    atomic_json(artifact_path(a.output),receipt)
    print(receipt['status'], 'review assertion recorded; reviewer independence not machine-authenticated')
    return 0 if ok else 2
if __name__=='__main__':sys.exit(main())
