"""Fail-closed gate assertion checks bound to the current working candidate."""
import argparse
import json
import sys
from .common import ROOT, load_json
from .evidence import candidate, artifact_path, read_receipts, atomic_json, stamp

REVIEW = 'independent-diff-review'
OPERATOR = 'operator-host-review'

def evaluate(required, receipts, *, current=None, minimum_tests=None):
    seen = {}
    if len(set(required)) != len(required): return False, 'duplicate check in gate configuration'
    for item in receipts:
        if not isinstance(item, dict) or item.get('schema_version') != 2:
            return False, 'legacy or malformed receipt'
        key = item.get('check')
        if not isinstance(key, str) or key in seen or item.get('status') not in {'passed','failed','blocked','not_run'}:
            return False, 'invalid or duplicate receipt'
        status = item['status']; code = item.get('exit_code')
        if status == 'passed' and (type(code) is not int or code != 0 or item.get('candidate_unchanged') is not True):
            return False, 'invalid passing receipt'
        c = item.get('candidate')
        if not isinstance(c, dict) or not isinstance(c.get('sha256'), str) or len(c['sha256']) != 64:
            return False, 'missing candidate identity'
        if current is not None and (c.get('sha256') != current.get('sha256') or
                                     c.get('blueprint_sha256') != current.get('blueprint_sha256')):
            return False, 'stale or mismatched candidate receipt'
        if key == REVIEW:
            if (item.get('source') != 'independent-review' or item.get('reviewer_role') != 'independent-reviewer'
                or item.get('decision') != 'APPROVE_FOR_NEXT_GATE' or item.get('findings_count') != 0):
                return False, 'independent review evidence missing or invalid'
        elif key == OPERATOR:
            if (item.get('source') != 'operator-review' or not item.get('operator_id')
                or item.get('decision') != 'QUALIFIED'):
                return False, 'host operator review absent or invalid'
        elif item.get('source') != 'local-command':
            return False, 'unknown receipt source'
        minimum = (minimum_tests or {}).get(key, 0)
        if status == 'passed' and minimum and (type(item.get('test_count')) is not int or item['test_count'] < minimum):
            return False, 'zero or insufficient tests for '+key
        seen[key] = item
    missing = [k for k in required if k not in seen or seen[k]['status'] != 'passed']
    return (False, 'missing or nonpassing: '+', '.join(missing)) if missing else (True, 'all required current-candidate receipt assertions passed (not independent authentication)')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gate', required=True); ap.add_argument('--receipts', nargs='+', required=True)
    ap.add_argument('--output', help='optional gate verdict under artifacts/control-plane/')
    a = ap.parse_args()
    config = load_json(ROOT/'control-plane/verification-map.json')
    if a.gate not in config['gates']: ap.error('unknown gate')
    try:
        receipts = []
        for name in a.receipts:
            data = json.loads(artifact_path(name, must_exist=True).read_text())
            receipts.extend(data if isinstance(data, list) else data.get('receipts', [data]) if 'check' not in data else [data])
        now = candidate()
        ok, msg = evaluate(config['gates'][a.gate], receipts, current=now,
                           minimum_tests=config.get('minimum_tests',{}))
        if a.output:
            atomic_json(artifact_path(a.output), {'schema_version': 1, 'gate': a.gate,
                'status': 'passed' if ok else 'blocked', 'candidate': now, 'evaluated_at_utc': stamp(),
                'reason': msg})
    except (ValueError, OSError, json.JSONDecodeError, TypeError) as e: ap.error(str(e))
    print(('PASS: ' if ok else 'BLOCKED: ') + msg)
    return 0 if ok else 2
if __name__ == '__main__': sys.exit(main())
