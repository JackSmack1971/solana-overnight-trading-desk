import json
import tempfile
import unittest
from pathlib import Path
from tools.control_plane.evidence import candidate, artifact_path, atomic_json
from tools.control_plane.gate import evaluate
from tools.control_plane.record import execute
from tools.control_plane.tasks import definitions, statuses, transition
from tools.control_plane.context import compile_brief
from tools.control_plane.parallel import conflicts, plan
from tools.control_plane.retry import run
from tools.control_plane.hook_event import sanitize
from tools.control_plane.friction_bridge import classify
from tools.control_plane.common import ROOT

class OrchestrationTests(unittest.TestCase):
    def test_candidate_stable_during_evidence_write_and_stale_on_code_change(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'docs/blueprint').mkdir(parents=True)
            (root/'docs/blueprint/solana-overnight-trading-desk-blueprint-v2.6-consolidated.md').write_text('blueprint')
            (root/'code.py').write_text('a')
            a=candidate(root)
            atomic_json(root/'artifacts/control-plane/a.json',{'x':1})
            self.assertEqual(a,candidate(root))
            (root/'code.py').write_text('b')
            self.assertNotEqual(a['sha256'],candidate(root)['sha256'])

    def test_record_to_gate_integration(self):
        r=execute('focused-tests',['python','-m','unittest','discover','-s','tests/friction'],minimum_tests=1)
        self.assertEqual(r['status'],'passed')
        self.assertGreater(r['test_count'],0)
        ok,msg=evaluate(['focused-tests'],[r],current=r['candidate'],minimum_tests={'focused-tests':1})
        self.assertTrue(ok,msg)
        stale={**r,'candidate':{**r['candidate'],'sha256':'0'*64}}
        self.assertFalse(evaluate(['focused-tests'],[stale],current=r['candidate'])[0])
        self.assertFalse(evaluate(['focused-tests'],[r],current=r['candidate'],minimum_tests={'focused-tests':1000})[0])

    def test_duplicate_missing_legacy_review(self):
        c=candidate()
        r={'schema_version':2,'check':'independent-diff-review','status':'passed','exit_code':0,'candidate':c,'candidate_unchanged':True,'source':'local-command'}
        self.assertFalse(evaluate(['independent-diff-review'],[r],current=c)[0])
        self.assertFalse(evaluate(['x'],[{'check':'x','status':'passed','exit_code':0}])[0])
        self.assertFalse(evaluate(['x'],[r,r])[0])

    def test_task_dag_initially_manual(self):
        tasks=definitions();state={'schema_version':1,'tasks':{},'history':[]}
        statuses_by_id={x['id']:x for x in statuses(tasks,state)}
        self.assertEqual(statuses_by_id['P0-baseline']['status'],'ready')
        self.assertEqual(statuses_by_id['P1-contracts']['status'],'pending')
        with self.assertRaises(ValueError):transition('P1-contracts','start',state,tasks)
        transition('P0-baseline','start',state,tasks)
        with self.assertRaises(ValueError):transition('P0-baseline','verify',state,tasks)
        self.assertEqual(len(state['history']),1)

    def test_context_and_parallel(self):
        brief=compile_brief('P1-contracts')
        self.assertIn('blueprint_sha256',brief['candidate'])
        self.assertFalse(conflicts({'scope':['contracts/']},{'scope':['src/']}))
        self.assertTrue(conflicts({'scope':['src/']},{'scope':['src/desk/']}))
        self.assertEqual(plan(definitions(),{'tasks':{},'history':[]})['parallel_candidates'],[])

    def test_retry_refuses_side_effects(self):
        with self.assertRaises(ValueError):run('check',['bash','-c','echo ok'])
        with self.assertRaises(ValueError):run('check',['python','-c','print(1)'])

    def test_hook_redacts_and_friction_skips_test_failures(self):
        observed=sanitize({'event':'PreToolUse','tool_input':{'token':'sensitive'}})
        self.assertNotIn('tool_input',observed)
        self.assertIsNone(classify({'schema_version':2,'source':'local-command','status':'failed','exit_code':1}))

if __name__=='__main__': unittest.main()

class RecoveryTests(unittest.TestCase):
    def test_handoff_no_git_does_not_claim_clean(self):
        from tools.control_plane.handoff import snapshot
        report=snapshot()
        self.assertIn('git_status',report)
        self.assertIn('candidate',report)

    def test_friction_requires_changed_candidate_and_blocked_transition(self):
        from tools.control_plane.friction_compare import compare
        old={'schema_version':2,'source':'local-command','check':'probe','candidate':{'sha256':'a'*64},'status':'blocked'}
        new={**old,'candidate':{'sha256':'b'*64},'status':'passed','candidate_unchanged':True}
        self.assertEqual(compare(old,new)['result'],'CANDIDATE_IMPROVEMENT')
        with self.assertRaises(ValueError): compare(old,{**new,'candidate':old['candidate']})

class DriveTests(unittest.TestCase):
    def test_no_auto_dispatch_when_manual_bootstrap_pending(self):
        from tools.control_plane.drive import choose
        self.assertIsNone(choose(definitions(),{'tasks':{},'history':[]}))

    def test_in_progress_writer_blocks_second_writer(self):
        from tools.control_plane.drive import choose
        state={'tasks':{'P0-baseline':{'status':'verified'},'P1-contracts':{'status':'in_progress'}},'history':[]}
        with self.assertRaises(ValueError): choose(definitions(),state)
