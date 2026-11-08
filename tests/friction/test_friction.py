import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools.control_plane.common import ROOT
from tools.friction.core import checked_db, clusters, connect, evaluate, fingerprint, propose, record, report

class FrictionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db=Path(self.tmp.name)/'incidents.sqlite3'

    def event(self, **changes):
        values=dict(category='shell-syntax',shell='bash',tool='git',failure_code='invalidFlag',outcome='recovered',recovery_code='useSupportedFlag')
        values.update(changes)
        return record(self.db,**values)

    def test_persistence_and_cluster(self):
        first=self.event(session_ref='sessionA')
        self.event(session_ref='sessionB')
        value=clusters(self.db)
        self.assertEqual(len(value['clusters']),1)
        item=value['clusters'][0]
        self.assertEqual(item['incidents'],2)
        self.assertEqual(item['attributable_sessions'],2)
        self.assertEqual(item['fingerprint'],first['fingerprint'])
        with connect(self.db) as connection:
            self.assertEqual(connection.execute('select count(*) from incidents').fetchone()[0],2)

    def test_session_coverage_not_inferred(self):
        self.event()
        self.event()
        self.assertEqual(clusters(self.db)['clusters'][0]['attributable_sessions'],0)

    def test_invalid_input_cannot_store_secrets_or_paths(self):
        for change in ({'tool':'git --password=secret'},{'failure_code':'/tmp/private'},{'shell':'unknown-system'},
                       {'category':'provider-fault'},{'evidence_sha256':'secret'},{'session_ref':'abc@example.com'},
                       {'client_version':'0.166.0'}):
            with self.subTest(change=change),self.assertRaises(ValueError):self.event(**change)
        self.assertEqual(clusters(self.db,1)['clusters'],[])

    def test_db_cannot_reside_in_repository(self):
        with self.assertRaises(ValueError):checked_db(ROOT/'artifacts/friction.sqlite3')
        with self.assertRaises(ValueError):checked_db(Path('relative.sqlite3'))

    def test_proposal_and_reported_evaluation_do_not_modify_policy(self):
        original=(ROOT/'AGENTS.md').read_bytes()
        fp=self.event()['fingerprint']
        prop=propose(self.db,fingerprint_id=fp,remediation_target='local-script',proposed_fix_code='detectShell')
        self.assertEqual(prop['status'],'CANDIDATE')
        result=evaluate(self.db,proposal_id=prop['proposal_id'],check_code='focusedSuite',exit_code=0,output_sha256='a'*64)
        self.assertEqual(result['outcome'],'REPORTED_PASS')
        proposals=report(self.db)['proposals']
        self.assertEqual(proposals[0]['status'],'CANDIDATE')
        self.assertEqual(proposals[0]['reported_checks'],1)
        self.assertEqual((ROOT/'AGENTS.md').read_bytes(),original)

    def test_unknown_incident_or_proposal_rejected(self):
        with self.assertRaises(ValueError):
            propose(self.db,fingerprint_id='0'*64,remediation_target='agents-guidance',proposed_fix_code='extraLine')
        with self.assertRaises(ValueError):
            evaluate(self.db,proposal_id='00000000-0000-4000-8000-000000000000',check_code='unitSuite',exit_code=0,output_sha256='f'*64)

    def test_cli_end_to_end(self):
        command=[sys.executable,'-m','tools.friction','--db',str(self.db),'record','--category','shell-syntax',
                 '--shell','bash','--tool','git','--failure-code','badFlag','--outcome','unresolved']
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,check=True)
        self.assertEqual(json.loads(result.stdout)['status'],'OBSERVED')
        result=subprocess.run([sys.executable,'-m','tools.friction','--db',str(self.db),'clusters','--minimum','1'],cwd=ROOT,capture_output=True,text=True,check=True)
        self.assertEqual(json.loads(result.stdout)['clusters'][0]['incidents'],1)

    def test_cli_rejects_raw_command(self):
        command=[sys.executable,'-m','tools.friction','--db',str(self.db),'record','--category','shell-syntax',
                 '--shell','bash','--tool','git push https://token@host','--failure-code','badFlag','--outcome','unresolved']
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertNotIn('token@host',result.stderr)
        self.assertFalse(self.db.exists())

    def test_parent_directory_private_on_posix(self):
        if os.name!='posix':self.skipTest('POSIX-only access modes')
        self.event()
        self.assertEqual(self.db.stat().st_mode & 0o777,0o600)
        self.assertEqual(self.db.parent.stat().st_mode & 0o777,0o700)

if __name__=='__main__': unittest.main()
