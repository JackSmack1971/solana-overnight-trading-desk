"""Run one local verification command and record bounded structured evidence.

This is a self-report from the local machine, not independently authenticated proof.
"""
import argparse
import re
import subprocess
import sys
from .common import ROOT
from .evidence import candidate, stamp, artifact_path, atomic_json

TEST_PATTERNS = [re.compile(r'Ran (\d+) tests? in '), re.compile(r'(\d+) passed(?:,|\s|$)')]

def execute(check, argv, timeout=300, *, root=ROOT, minimum_tests=0):
    if not check or not re.fullmatch(r'[a-z][a-z0-9-]{0,63}', check): raise ValueError('invalid check id')
    if not argv or not 1 <= timeout <= 1800: raise ValueError('argv and timeout 1..1800 required')
    before = candidate(root)
    started = stamp()
    count = None
    try:
        p = subprocess.run(argv, cwd=root, timeout=timeout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True, errors='replace')
        code = p.returncode
        # A conservative, bounded parser for unittest/pytest summary formats.
        for pattern in TEST_PATTERNS:
            m = pattern.search(p.stdout[-16000:])
            if m: count = int(m.group(1)); break
        status = 'passed' if code == 0 and (not minimum_tests or (count is not None and count >= minimum_tests)) else 'failed'
    except (OSError, subprocess.TimeoutExpired):
        code = None; status = 'blocked'
    after = candidate(root)
    if before['sha256'] != after['sha256']: status = 'blocked'  # command mutated candidate under test
    return {'schema_version': 2, 'check': check, 'status': status, 'exit_code': code,
            'started_at_utc': started, 'ended_at_utc': stamp(), 'candidate': before,
            'candidate_unchanged': before['sha256'] == after['sha256'],
            'source': 'local-command', 'argv': argv, 'test_count': count,
            'minimum_tests': minimum_tests, 'note': 'Untrusted local execution receipt; output not persisted.'}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--timeout', type=int, default=300)
    ap.add_argument('--minimum-tests', type=int, default=0)
    ap.add_argument('argv', nargs=argparse.REMAINDER)
    a = ap.parse_args()
    argv = a.argv[1:] if a.argv[:1] == ['--'] else a.argv
    if a.minimum_tests < 0: ap.error('minimum-tests must be nonnegative')
    try:
        dest = artifact_path(a.output)
        receipt = execute(a.check, argv, a.timeout, minimum_tests=a.minimum_tests)
        atomic_json(dest, receipt)
    except (ValueError, OSError) as e: ap.error(str(e))
    print(receipt['status'], receipt['exit_code'], 'tests=',receipt['test_count'])
    return 0 if receipt['status'] == 'passed' else 2
if __name__ == '__main__': sys.exit(main())
