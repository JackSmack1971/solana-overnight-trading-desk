"""Local-only, structured development-friction records. Not application runtime code."""
import hashlib
from contextlib import contextmanager
import json
import os
import re
import sqlite3
import stat
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from tools.control_plane.common import ROOT

SCHEMA = 1
PROJECT = 'solana-overnight-desk-v2.6'
CATEGORIES = frozenset({'shell-syntax','environment','dependency','tool-discovery','test-runner','git-workflow','agent-coordination','validation-workflow','other-dev-friction'})
SHELLS = frozenset({'bash','zsh','sh','powershell','cmd','python','none','unknown'})
RESULTS = frozenset({'recovered','unresolved','blocked'})
TARGETS = frozenset({'local-script','environment-preflight','skill','agents-guidance','test-fixture','other-development-tool'})
TOKEN = re.compile(r'^[a-zA-Z][a-zA-Z0-9_-]{0,63}$')
HEX64 = re.compile(r'^[0-9a-f]{64}$')


def utcnow():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def check_token(value, name):
    if not isinstance(value, str) or not TOKEN.fullmatch(value):
        raise ValueError(f'{name} must be an opaque 1-64-character identifier (letters, digits, _ or -); no paths or raw messages')
    return value


def check_digest(value, name):
    if value is not None and (not isinstance(value, str) or not HEX64.fullmatch(value)):
        raise ValueError(f'{name} must be a lowercase SHA-256 hex digest')
    return value


def default_db():
    # Do not place the evidence store inside the checkout or any tracked artifact.
    state = os.environ.get('XDG_STATE_HOME')
    base = Path(state).expanduser() if state and Path(state).is_absolute() else Path.home()/'.local'/'state'
    return base/'codex-friction-intelligence'/PROJECT/'incidents.sqlite3'


def checked_db(path=None):
    path = Path(path).expanduser() if path is not None else default_db()
    if not path.is_absolute():
        raise ValueError('database path must be absolute')
    resolved = path.resolve()
    if resolved.is_relative_to(ROOT.resolve()):
        raise ValueError('local evidence database cannot live inside the repository')
    if resolved.exists() and (resolved.is_symlink() or not resolved.is_file()):
        raise ValueError('database target must be a regular file')
    return resolved


def _open_connection(path=None):
    db = checked_db(path)
    db.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name == 'posix':
        os.chmod(db.parent, 0o700)
    connection = sqlite3.connect(db, timeout=10)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute('PRAGMA busy_timeout = 10000')
        connection.execute('PRAGMA journal_mode = WAL')
        connection.executescript('''
        CREATE TABLE IF NOT EXISTS incidents (
          id TEXT PRIMARY KEY, created_utc TEXT NOT NULL, category TEXT NOT NULL,
          shell TEXT NOT NULL, tool TEXT NOT NULL, failure_code TEXT NOT NULL,
          recovery_code TEXT, outcome TEXT NOT NULL, evidence_sha256 TEXT,
          client_version TEXT, session_ref TEXT, fingerprint TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS incident_fingerprint ON incidents(fingerprint);
        CREATE TABLE IF NOT EXISTS proposals (
          id TEXT PRIMARY KEY, created_utc TEXT NOT NULL, fingerprint TEXT NOT NULL,
          remediation_target TEXT NOT NULL, proposed_fix_code TEXT NOT NULL,
          hypothesis_only INTEGER NOT NULL DEFAULT 1, status TEXT NOT NULL DEFAULT 'CANDIDATE',
          evidence_sha256 TEXT
        );
        CREATE TABLE IF NOT EXISTS evaluations (
          id TEXT PRIMARY KEY, proposal_id TEXT NOT NULL REFERENCES proposals(id),
          created_utc TEXT NOT NULL, check_code TEXT NOT NULL,
          exit_code INTEGER NOT NULL, output_sha256 TEXT NOT NULL,
          outcome TEXT NOT NULL
        );
        ''')
        if os.name == 'posix':
            os.chmod(db, stat.S_IRUSR | stat.S_IWUSR)
        connection.execute('PRAGMA foreign_keys=ON')
        return connection
    except BaseException:
        connection.close()
        raise


@contextmanager
def connect(path=None):
    connection = _open_connection(path)
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def fingerprint(category, shell, tool, failure_code):
    payload = json.dumps([category,shell,tool,failure_code],separators=(',',':'))
    return hashlib.sha256(payload.encode()).hexdigest()


def record(db=None, *, category, shell, tool, failure_code, outcome, recovery_code=None,
           evidence_sha256=None, client_version=None, session_ref=None):
    if category not in CATEGORIES: raise ValueError('unknown friction category')
    if shell not in SHELLS: raise ValueError('unknown shell')
    if outcome not in RESULTS: raise ValueError('unknown outcome')
    for k,v in [('tool',tool),('failure_code',failure_code)]: check_token(v,k)
    for k,v in [('recovery_code',recovery_code),('client_version',client_version),('session_ref',session_ref)]:
        if v is not None: check_token(v,k)
    check_digest(evidence_sha256,'evidence_sha256')
    key = fingerprint(category,shell,tool,failure_code)
    ident = str(uuid.uuid4())
    with connect(db) as c:
        c.execute('''INSERT INTO incidents VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                  (ident,utcnow(),category,shell,tool,failure_code,recovery_code,outcome,evidence_sha256,client_version,session_ref,key))
    return {'incident_id':ident,'fingerprint':key,'status':'OBSERVED'}


def clusters(db=None, minimum=2):
    if not isinstance(minimum,int) or not 1<=minimum<=100000: raise ValueError('minimum outside supported range')
    with connect(db) as c:
        rows=c.execute('''SELECT fingerprint, category, shell, tool, failure_code,
                    COUNT(*) AS incidents, COUNT(DISTINCT session_ref) AS attributable_sessions,
                    SUM(outcome='recovered') AS recovered,
                    MAX(created_utc) AS most_recent_utc
                    FROM incidents GROUP BY fingerprint HAVING COUNT(*)>=?
                    ORDER BY incidents DESC, most_recent_utc DESC, fingerprint ASC LIMIT 100''',(minimum,)).fetchall()
    return {'clusters':[dict(r) for r in rows], 'notice':'Counts are local incident records, not proven independent sessions or verified causes. Session coverage may be incomplete.'}


def propose(db=None, *, fingerprint_id, remediation_target, proposed_fix_code, evidence_sha256=None):
    check_digest(fingerprint_id,'fingerprint')
    if remediation_target not in TARGETS: raise ValueError('invalid remediation target')
    check_token(proposed_fix_code,'proposed_fix_code')
    check_digest(evidence_sha256,'evidence_sha256')
    ident=str(uuid.uuid4())
    with connect(db) as c:
        n=c.execute('SELECT COUNT(*) FROM incidents WHERE fingerprint=?',(fingerprint_id,)).fetchone()[0]
        if n==0:raise ValueError('proposal fingerprint has no recorded incident')
        c.execute('INSERT INTO proposals (id, created_utc, fingerprint, remediation_target, proposed_fix_code, evidence_sha256) VALUES (?,?,?,?,?,?)',
                  (ident,utcnow(),fingerprint_id,remediation_target,proposed_fix_code,evidence_sha256))
    return {'proposal_id':ident,'status':'CANDIDATE','incident_count':n,'note':'Hypothesis only; no policy change or permission granted.'}


def evaluate(db=None, *, proposal_id, check_code, exit_code, output_sha256):
    # This stores *reported* execution evidence only. It does not run or independently attest tests.
    try:uuid.UUID(proposal_id)
    except (ValueError,TypeError):raise ValueError('invalid proposal ID') from None
    check_token(check_code,'check_code')
    check_digest(output_sha256,'output_sha256')
    if not isinstance(exit_code,int) or isinstance(exit_code,bool) or not 0<=exit_code<=255:
        raise ValueError('invalid process exit code')
    ident=str(uuid.uuid4())
    with connect(db) as c:
        if not c.execute('SELECT 1 FROM proposals WHERE id=?',(proposal_id,)).fetchone():
            raise ValueError('unknown proposal ID')
        c.execute('INSERT INTO evaluations VALUES (?,?,?,?,?,?,?)',
                  (ident,proposal_id,utcnow(),check_code,exit_code,output_sha256,'REPORTED_PASS' if exit_code==0 else 'REPORTED_FAIL'))
    return {'evaluation_id':ident,'outcome':'REPORTED_PASS' if exit_code==0 else 'REPORTED_FAIL',
            'note':'Self-reported result; requires independent verification and owner approval. No automatic promotion.'}


def report(db=None):
    with connect(db) as c:
        incidents=c.execute('SELECT COUNT(*) FROM incidents').fetchone()[0]
        proposals=[dict(r) for r in c.execute('''SELECT p.id, p.fingerprint, p.remediation_target,
           p.proposed_fix_code, p.status, COUNT(e.id) AS reported_checks,
           SUM(CASE WHEN e.outcome='REPORTED_FAIL' THEN 1 ELSE 0 END) AS reported_failures
           FROM proposals p LEFT JOIN evaluations e ON e.proposal_id=p.id
           GROUP BY p.id ORDER BY p.created_utc DESC LIMIT 100''').fetchall()]
    return {'recorded_incidents':incidents,'proposals':proposals,'notice':'No proposal is approved or automatically applied by this subsystem.'}
