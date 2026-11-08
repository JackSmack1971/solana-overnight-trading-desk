"""python3 -m tools.friction --help"""
import argparse
import json
import sys
from .core import CATEGORIES, RESULTS, SHELLS, TARGETS, checked_db, clusters, evaluate, propose, record, report

def main(argv=None):
    parser=argparse.ArgumentParser(description='Local, structured Solana Desk development friction evidence (no raw logs)')
    parser.add_argument('--db',help='absolute external local SQLite file (default: user state directory)')
    commands=parser.add_subparsers(dest='action',required=True)
    r=commands.add_parser('record',help='record one observed avoidable development friction incident')
    r.add_argument('--category',choices=sorted(CATEGORIES),required=True)
    r.add_argument('--shell',choices=sorted(SHELLS),required=True)
    r.add_argument('--tool',required=True,help='opaque identifier, not a command line')
    r.add_argument('--failure-code',required=True,help='stable code, not stderr')
    r.add_argument('--outcome',choices=sorted(RESULTS),required=True)
    r.add_argument('--recovery-code');r.add_argument('--evidence-sha256')
    r.add_argument('--client-version');r.add_argument('--session-ref')
    c=commands.add_parser('clusters',help='aggregate incidents by exact fingerprint')
    c.add_argument('--minimum',type=int,default=2)
    p=commands.add_parser('propose',help='record a remediation hypothesis, without changing project files')
    p.add_argument('--fingerprint',required=True)
    p.add_argument('--target',choices=sorted(TARGETS),required=True)
    p.add_argument('--fix-code',required=True);p.add_argument('--evidence-sha256')
    e=commands.add_parser('evaluate',help='record a check result, as unverified reported evidence')
    e.add_argument('--proposal-id',required=True);e.add_argument('--check-code',required=True)
    e.add_argument('--exit-code',type=int,required=True);e.add_argument('--output-sha256',required=True)
    commands.add_parser('report',help='inspect proposal states and recorded check counts')
    args=parser.parse_args(argv)
    try:
        checked_db(args.db)
        if args.action=='record':
            result=record(args.db,category=args.category,shell=args.shell,tool=args.tool, failure_code=args.failure_code,
                          outcome=args.outcome,recovery_code=args.recovery_code,evidence_sha256=args.evidence_sha256,
                          client_version=args.client_version,session_ref=args.session_ref)
        elif args.action=='clusters':result=clusters(args.db,args.minimum)
        elif args.action=='propose':result=propose(args.db,fingerprint_id=args.fingerprint,remediation_target=args.target,proposed_fix_code=args.fix_code,evidence_sha256=args.evidence_sha256)
        elif args.action=='evaluate':result=evaluate(args.db,proposal_id=args.proposal_id,check_code=args.check_code,exit_code=args.exit_code,output_sha256=args.output_sha256)
        else:result=report(args.db)
    except (ValueError,OSError,RuntimeError) as err:
        # Avoid leaking arbitrary filesystem paths or raw exception contents in output.
        print(json.dumps({'status':'BLOCKED','error_type':type(err).__name__,'note':'Check local database path and structured field constraints.'}),file=sys.stderr)
        return 2
    print(json.dumps(result,sort_keys=True))
    return 0

if __name__=='__main__':sys.exit(main())
