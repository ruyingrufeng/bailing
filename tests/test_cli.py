import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from bailing.retrieval import prepare, retrieve

SOURCE = Path(__file__).resolve().parents[1]

class PublicWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'private'
        self.run_cli('init', str(self.root), '--name', 'River')

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args, ok=True):
        result = subprocess.run([sys.executable, '-m', 'bailing', *args], cwd=SOURCE, text=True, capture_output=True)
        self.assertEqual(result.returncode == 0, ok, result.stderr)
        return result.stdout + result.stderr

    def test_init_refuses_overwrite(self):
        target = self.root / 'GENESIS.md'
        original = target.read_bytes()
        self.run_cli('init', str(self.root), ok=False)
        self.assertEqual(original, target.read_bytes())

    def test_doctor_catches_missing_core(self):
        (self.root / 'core/CONSTITUTION.md').unlink()
        self.run_cli('doctor', '--root', str(self.root), ok=False)

    def test_cross_runtime_record_and_recovery(self):
        (self.root / 'tasks/ACTIVE.md').write_text('# Tasks\n## T1\nReading session: 45 minutes. Date unknown. Next: choose questions.\n')
        self.run_cli('record', '--root', str(self.root), '--runtime', 'codex', 'Outline ready; invitation not sent.')
        output = self.run_cli('context', '--root', str(self.root), '--runtime', 'hermes')
        self.assertIn('Outline ready; invitation not sent.', output)
        self.assertIn('Date unknown', output)
        self.assertIn('Next: choose questions', output)
        self.assertIn('runtime: hermes', output)

    def test_record_escapes_multiline(self):
        self.run_cli('record', '--root', str(self.root), '--runtime', 'other', 'text\n# fake header')
        files = [p for p in (self.root / 'memory/journal').glob('*.md') if p.name != 'README.md']
        self.assertEqual(len(files[0].read_text().splitlines()), 1)

    def test_retrieval_preserves_corrections_and_sources(self):
        (self.root / 'memory/entries/old.md').write_text('# Reading\nDate was Monday.\n## Correction\nDate unknown, verify first.')
        result = retrieve('Reading', self.root, category='memory')
        self.assertEqual(result[0]['path'], 'memory/entries/old.md')
        self.assertIn('Date unknown', result[0]['text'])
        output = prepare('Reading', self.root)
        self.assertIn('historical_reference', output)
        self.assertIn('old.md:1', output)

    def test_missing_match_is_not_denial(self):
        output = prepare('zzunseenwordzz', self.root)
        self.assertIn('没有匹配记录', output)
        self.assertIn('不能据此推断', output)

    def test_symlink_memory_rejected(self):
        outside = Path(self.tmp.name) / 'outside.md'
        outside.write_text('outside private text')
        (self.root / 'memory/entries/link.md').symlink_to(outside)
        output = self.run_cli('context', '--root', str(self.root), '--runtime', 'other', ok=False)
        self.assertNotIn('outside private text', output)

    def test_symlink_journal_rejected(self):
        import datetime
        outside = Path(self.tmp.name) / 'outside.md'
        outside.write_text('unchanged')
        name = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d') + '.md'
        (self.root / 'memory/journal' / name).symlink_to(outside)
        self.run_cli('record', '--root', str(self.root), '--runtime', 'other', 'append', ok=False)
        self.assertEqual(outside.read_text(), 'unchanged')

    def test_private_workspace_git_ignore(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        result = subprocess.run(['git', '-C', str(self.root), 'status', '--porcelain'], capture_output=True, text=True, check=True)
        self.assertEqual(result.stdout.strip(), '?? .gitignore')

    def test_fictional_demo(self):
        output = self.run_cli('prepare', '--root', str(SOURCE / 'examples/fictional'), '社区读书会')
        self.assertIn('TASK-DEMO-001', output)
        self.assertIn('no invitations sent', output)

if __name__ == '__main__':
    unittest.main()
