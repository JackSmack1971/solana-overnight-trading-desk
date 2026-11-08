"""Optional adapter for supported Codex lifecycle hook payloads.

Observational only. Must be wired by a version-qualified plugin hook, never
interpreted as an enforcement mechanism. Does not log tool inputs or outputs.
"""
import json
import sys
from .evidence import artifact_path, atomic_json, stamp

SUPPORTED = {'SessionStart', 'PreToolUse', 'PostToolUse', 'PostToolUseFailure'}

def sanitize(payload):
    if not isinstance(payload,dict): raise ValueError('event must be object')
    event = payload.get('hook_event_name') or payload.get('event')
    if event not in SUPPORTED: raise ValueError('unsupported event')
    return {'schema_version':1,'event':event,'observed_at_utc':stamp(),
            'note':'Advisory observation only; sensitive payload fields discarded.'}

def main():
    # Never embed raw hook payloads in artifacts; caller can omit --output completely.
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output');a=ap.parse_args()
    try:
        data=sanitize(json.load(sys.stdin))
        if a.output: atomic_json(artifact_path(a.output),data)
    except (ValueError,json.JSONDecodeError,OSError) as e:
        print('hook event ignored: '+str(e),file=sys.stderr);return 0 # no disruption to development
    return 0
if __name__=='__main__':sys.exit(main())
