"""Rebuild the package file-hash manifest after deliberate file changes.

Does not alter the canonical blueprint or attest runtime qualification.
"""
from pathlib import Path
import hashlib
import json
from .common import ROOT


def refresh(root=ROOT):
    destination=root/'control-plane/package-manifest.json'
    data=json.loads(destination.read_text(encoding='utf8'))
    files=[p for p in root.rglob('*') if p.is_file() and p!=destination
           and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts
           and '.git' not in p.parts and 'artifacts' not in p.parts]
    data['sha256']={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    destination.write_text(json.dumps(data,indent=2)+'\n',encoding='utf8')
    return len(files)

if __name__=='__main__':
    print('Manifest entries:',refresh())
