import re, sys
from pathlib import Path
from .common import ROOT, BLUEPRINT, EXPECTED, digest, load_json

def validate(root=ROOT, expected=EXPECTED):
    errors=[]
    bp=root/'docs/blueprint/solana-overnight-trading-desk-blueprint-v2.6-consolidated.md'
    if not bp.is_file() or digest(bp)!=expected: errors.append('blueprint digest mismatch or missing')
    for f in ['AGENTS.md','.codex/config.toml','control-plane/authority.md','control-plane/capabilities.json','control-plane/verification-map.json']:
        if not (root/f).is_file(): errors.append('missing '+f)
    for f in (root/'.agents/skills').glob('*/SKILL.md'):
        s=f.read_text(encoding='utf8')
        m=re.match(r'\A---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n',s)
        if not m or m[1]!=f.parent.name or len(m[1])>64 or len(m[2])>1024: errors.append('invalid skill '+str(f.relative_to(root)))
    if len(list((root/'.agents/skills').glob('*/SKILL.md')))!=8: errors.append('expected eight skills')
    for name in ['capabilities','verification-map','client-qualification']:
        try:
            data=load_json(root/f'control-plane/{name}.json')
            if data.get('schema_version')!=1: errors.append('invalid schema version '+name)
        except (ValueError,OSError) as e: errors.append('invalid JSON '+name+': '+str(e))
    try:
        manifest=load_json(root/'control-plane/package-manifest.json')
        if manifest.get('schema_version')!=1 or not isinstance(manifest.get('sha256'),dict):
            errors.append('invalid package manifest schema')
        else:
            checks=manifest['sha256']
            if not checks: errors.append('empty package manifest')
            for name,expected_digest in checks.items():
                path=root/name
                if (not isinstance(name,str) or name.startswith('/') or '..' in Path(name).parts
                    or not path.resolve().is_relative_to(root.resolve())):
                    errors.append('unsafe package manifest path');continue
                if not path.is_file() or not isinstance(expected_digest,str) or not re.fullmatch('[0-9a-f]{64}',expected_digest) or digest(path)!=expected_digest:
                    errors.append('manifest digest mismatch: '+name)
            actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='package-manifest.json' and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts and '.git' not in p.parts and 'artifacts' not in p.parts}
            if set(checks)!=actual: errors.append('package manifest coverage mismatch')
            required=['AGENTS.md','.agents/skills/desk-friction-intelligence/SKILL.md',
                      'tools/friction/core.py','tools/friction/__main__.py','tools/friction/__init__.py',
                      'docs/control-plane/friction-intelligence.md','tests/friction/test_friction.py']
            for name in required:
                if name not in checks: errors.append('manifest missing entry: '+name)
    except (ValueError,OSError,TypeError) as e:
        errors.append('invalid package manifest: '+type(e).__name__)
    return errors

def main():
    errors=validate()
    for e in errors: print('FAIL:',e)
    if not errors: print('PASS: package structure, skill headers and canonical blueprint digest (not runtime qualification)')
    return bool(errors)
if __name__=='__main__':sys.exit(main())
