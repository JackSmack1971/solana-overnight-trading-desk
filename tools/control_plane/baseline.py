import argparse, json, subprocess, sys
from datetime import datetime, timezone
from .common import ROOT, BLUEPRINT, digest

def git(*args):
    p=subprocess.run(['git',*args],cwd=ROOT,capture_output=True,text=True,timeout=15)
    return {'exit_code':p.returncode,'output':p.stdout[:50000] if p.returncode==0 else '', 'error':p.stderr[:2000] if p.returncode else ''}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',help='Optional JSON output file under artifacts/control-plane/')
    a=ap.parse_args()
    out={'captured_at_utc':datetime.now(timezone.utc).isoformat(),'blueprint_sha256':digest(BLUEPRINT),'head':git('rev-parse','HEAD'),'status':git('status','--porcelain=v1','--untracked-files=all'),'diff_stat':git('diff','--stat'),'staged_diff_stat':git('diff','--cached','--stat')}
    if a.output:
        dest=(ROOT/a.output).resolve();allowed=(ROOT/'artifacts/control-plane').resolve()
        if not dest.is_relative_to(allowed) or dest==allowed:raise SystemExit('output must be under artifacts/control-plane/')
        dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.is_symlink():raise SystemExit('symlink output prohibited')
        import os,tempfile
        fd,tmp=tempfile.mkstemp(dir=dest.parent,prefix='.baseline-')
        try:
            with os.fdopen(fd,'w') as f:json.dump(out,f,indent=2)
            os.replace(tmp,dest)
        finally:
            if os.path.exists(tmp):os.unlink(tmp)
    else:print(json.dumps(out,indent=2))
    return 0 if out['head']['exit_code']==0 else 2
if __name__=='__main__':sys.exit(main())
