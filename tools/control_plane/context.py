"""Create an auditable task-specific brief without losing normative source authority."""
import argparse
import hashlib
import json
import re
import sys
from .common import ROOT, BLUEPRINT
from .tasks import definitions
from .evidence import artifact_path, atomic_json, candidate, stamp

# Reference-only excerpts: exact paragraphs containing matching normative markers.
def compile_brief(task_id, *, root=ROOT, max_chars=14000):
    task=next((t for t in definitions(root) if t['id']==task_id),None)
    if task is None: raise ValueError('unknown task')
    text=(root / BLUEPRINT.relative_to(ROOT)).read_text(encoding='utf8')
    lines=text.splitlines()
    selectors=[x for x in task['requirements'] if re.fullmatch(r'(?:OD-\d{3}|V\d+)',x)]
    extracts=[]; budget=max_chars
    for i,line in enumerate(lines):
        if any(re.search(r'(?<![A-Za-z0-9])'+re.escape(s)+r'(?![A-Za-z0-9])',line) for s in selectors):
            start=max(0,i-2); end=min(len(lines),i+5)
            excerpt='\n'.join(lines[start:end])
            if len(excerpt)>budget: break
            extracts.append({'start_line':start+1,'end_line':end,'text':excerpt})
            budget-=len(excerpt)
    snapshot=candidate(root)
    return {'schema_version':1,'task':task,'candidate':snapshot,'generated_at_utc':stamp(),
            'authoritative_blueprint':str(BLUEPRINT.relative_to(ROOT)),
            'excerpt_policy':'Exact source excerpts are aids, not complete requirements; inspect linked sections and surrounding dependencies.',
            'excerpts':extracts, 'missing_exact_selectors':[s for s in selectors if not any(s in x['text'] for x in extracts)],
            'required_scoped_instructions':['AGENTS.md','tests/AGENTS.md'],
            'caution':'Undecided product/economic/security choices are BLOCKED, not defaults. Do not infer phase completion.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--task',required=True);ap.add_argument('--output',required=True)
    a=ap.parse_args()
    try: result=compile_brief(a.task); atomic_json(artifact_path(a.output),result)
    except (OSError,ValueError) as e:ap.error(str(e))
    print('compiled',a.task,'excerpts',len(result['excerpts']))
    return 0
if __name__=='__main__':sys.exit(main())
