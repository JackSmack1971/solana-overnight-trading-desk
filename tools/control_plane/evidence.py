"""Versioned candidate identity and local, explicitly non-cryptographic evidence."""
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from .common import ROOT, BLUEPRINT, digest

EXCLUDES = {'.git', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.tox', '.venv', 'venv', 'artifacts', 'dist', 'build'}

def stamp():
    return datetime.now(timezone.utc).isoformat()

def candidate(root=ROOT):
    """Hash contents and relative paths; includes untracked code, excludes generated evidence.

    Not a Git commit signature. Artifact directories are excluded intentionally.
    """
    root = Path(root).resolve()
    h = hashlib.sha256()
    names = []
    for p in root.rglob('*'):
        if any(part in EXCLUDES for part in p.relative_to(root).parts):
            continue
        if p.is_symlink():
            raise ValueError('candidate contains symlink: '+str(p.relative_to(root)))
        if p.is_file():
            names.append(p)
    for p in sorted(names):
        name = p.relative_to(root).as_posix().encode()
        h.update(len(name).to_bytes(4, 'big')); h.update(name)
        h.update(bytes.fromhex(digest(p)))
    return {'schema_version': 1, 'sha256': h.hexdigest(), 'file_count': len(names),
            'blueprint_sha256': digest(root / BLUEPRINT.relative_to(ROOT))}

def artifact_path(path, root=ROOT, *, must_exist=False):
    root = Path(root).resolve()
    raw = Path(path)
    dest = raw if raw.is_absolute() else root/raw
    base = root/'artifacts/control-plane'
    # Check every pre-existing parent to prevent symlink escapes.
    if dest.is_symlink() or any(parent.is_symlink() for parent in dest.parents if parent != root and parent.is_relative_to(root)):
        raise ValueError('symlink artifact path forbidden')
    resolved = dest.resolve()
    if not resolved.is_relative_to(base.resolve()) or resolved == base.resolve():
        raise ValueError('path must be under artifacts/control-plane/')
    if must_exist and (not resolved.is_file() or resolved.is_symlink()):
        raise ValueError('missing or invalid artifact')
    return resolved

def atomic_json(dest, data):
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=dest.parent, prefix='.tmp-')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as out:
            json.dump(data, out, indent=2, sort_keys=True)
            out.write('\n')
        os.replace(tmp, dest)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def read_receipts(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if isinstance(data, dict): data = data.get('receipts')
    if not isinstance(data, list): raise ValueError('expected receipt list or {receipts: [...]}')
    return data
