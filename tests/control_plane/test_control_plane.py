import tempfile,unittest
from pathlib import Path
from tools.control_plane.validate import validate
from tools.control_plane.gate import evaluate
from tools.control_plane.common import ROOT
class ControlPlaneTests(unittest.TestCase):
    def test_package(self):self.assertEqual(validate(),[])
    def test_changed_blueprint_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'docs/blueprint').mkdir(parents=True);(root/'docs/blueprint/solana-overnight-trading-desk-blueprint-v2.6-consolidated.md').write_text('tampered')
            self.assertTrue(any('digest' in e for e in validate(root)))
    def receipt(self, check='x', status='passed', exit_code=0):
        from tools.control_plane.evidence import candidate
        return {'schema_version': 2, 'check':check, 'status':status,
                'exit_code':exit_code,'candidate':candidate(), 'candidate_unchanged':True,
                'source':'local-command'}
    def test_gate_rejects_forged_pass(self):
        self.assertFalse(evaluate(['x'],[self.receipt(exit_code=1)])[0])
    def test_gate_rejects_missing(self):self.assertFalse(evaluate(['x'],[])[0])
    def test_gate_rejects_duplicate(self):
        r=self.receipt();self.assertFalse(evaluate(['x'],[r,r])[0])
    def test_gate_pass(self):self.assertTrue(evaluate(['x'],[self.receipt()])[0])
if __name__=='__main__':unittest.main()

class SkillContractTests(unittest.TestCase):
    """Static routing and boundary regressions; not Codex activation tests."""
    def test_skill_routing_metadata_and_core_contract(self):
        expected={
            'desk-task-intake':('baseline','not for'),
            'desk-contracts':('traceability','not for'),
            'desk-implement-slice':('code slice','not for'),
            'desk-reference-parity':('reference harness','not for'),
            'desk-fault-verification':('invariants','not for'),
            'desk-review-gate':('candidate diff','not for'),
            'desk-host-handoff':('WSL2','not for'),
        }
        for name,(trigger,exclusion) in expected.items():
            with self.subTest(skill=name):
                data=(ROOT/'.agents/skills'/name/'SKILL.md').read_text(encoding='utf-8')
                header=data.split('---',2)[1]
                self.assertIn('name: '+name,header)
                self.assertIn(trigger.lower(),header.lower())
                self.assertIn(exclusion,header.lower())
                self.assertIn('blueprint',data.lower())
                self.assertTrue(any(x in data.lower() for x in ('blocked','inconclusive','stop')))
                self.assertNotIn('Use when this workflow is explicitly relevant',data)
