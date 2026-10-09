"""Synthetic regression cases for recovery boundaries."""
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from bailing.__main__ import context
from bailing.retrieval import prepare

SOURCE = Path(__file__).resolve().parents[1]

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'workspace'
        shutil.copytree(SOURCE / 'templates/individual', self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_summary_order_and_legacy_workspace(self):
        result = context(self.root, 'other')
        self.assertLess(result.index('## Source: state/SELF_MODEL.md'), result.index('## Source: GENESIS.md'))
        (self.root / 'state/SELF_MODEL.md').unlink()
        result = context(self.root, 'other')
        self.assertIn('Skipped source: state/SELF_MODEL.md', result)
        self.assertIn('## Source: GENESIS.md', result)

    def test_optional_invalid_encoding_is_reported(self):
        (self.root / 'memory/entries/bad.md').write_bytes(b'\xff')
        result = context(self.root, 'other')
        self.assertIn('Skipped source: memory/entries/bad.md', result)
        self.assertIn('invalid UTF-8', result)

    def test_optional_permission_error_is_reported(self):
        from bailing.__main__ import read_local
        def reader(path, root):
            if path.name == 'SELF_MODEL.md':
                raise PermissionError(13, 'synthetic denial')
            return read_local(path, root)
        with patch('bailing.__main__.read_local', side_effect=reader):
            self.assertIn('PermissionError (errno=13)', context(self.root, 'other'))

    def test_core_encoding_failure_is_fatal(self):
        (self.root / 'GENESIS.md').write_bytes(b'\xff')
        with self.assertRaises(ValueError):
            context(self.root, 'other')

    def test_budget_keeps_all_omitted_sources_and_small_record(self):
        for i in range(3):
            (self.root / f'memory/entries/long{i}.md').write_text('reading ' * 1000 + '\nCorrection: old claim withdrawn.')
        (self.root / 'tasks/ACTIVE.md').write_text('## Reading\nreading brief task; verify date.')
        result = prepare('reading', self.root, budget=2200, max_block=600)
        self.assertLessEqual(len(result), 2200)
        self.assertIn('brief task', result)
        for i in range(3):
            self.assertIn(f'memory/entries/long{i}.md:1', result)
        self.assertNotIn('old claim withdrawn', result)  # whole record omitted, not cut

    def test_exact_minimum_and_too_small_budget(self):
        (self.root / 'memory/entries/long.md').write_text('reading ' * 100)
        result = prepare('reading', self.root, max_block=1)
        self.assertEqual(result, prepare('reading', self.root, budget=len(result), max_block=1))
        with self.assertRaises(ValueError):
            prepare('reading', self.root, budget=len(result)-1, max_block=1)
        with self.assertRaises(ValueError):
            prepare('reading', self.root, max_block=0)

    def test_rules_are_never_truncated(self):
        (self.root / 'state/BEHAVIOR_RULES.md').write_text('rule ' * 1000)
        with self.assertRaises(ValueError):
            prepare('reading', self.root, budget=500)
