import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from bailing.archive import search, render
from bailing.retrieval import retrieve

ROOT = Path(__file__).resolve().parents[1]

class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.archive = self.root / 'memory/archive'
        self.archive.mkdir(parents=True)
        self.first = self.write('2026-01-01-codex-demo.md', '# Synthetic\n\n### user · t1\nreading 社区读书会 45 minutes\n\n### assistant · t2\noutline ready\n')
        self.second = self.write('2026-01-02-hermes-followup.md', '### user · t3\nreading 社区读书会 correction: 30 minutes\n')

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, content):
        p = self.archive / name
        p.write_text(content, encoding='utf-8')
        return p

    def test_sources_and_line_numbers(self):
        result = search('reading', self.root)
        self.assertEqual(len(result['hits']), 2)
        hit = next(h for h in result['hits'] if h['runtime'] == 'codex')
        self.assertEqual(hit['line'], 3)
        self.assertTrue(self.first.read_text().splitlines()[hit['line'] - 1].startswith('### user'))
        self.assertFalse(result['current_facts_verified'])

    def test_combined_filters_and_inclusive_dates(self):
        result = search('读书会', self.root, runtime='hermes', since='2026-01-02', until='2026-01-02', session='follow')
        self.assertEqual(len(result['hits']), 1)
        self.assertIn('30 minutes', result['hits'][0]['text'])
        self.assertEqual(search('reading', self.root, runtime='other')['hits'], [])

    def test_invalid_filters(self):
        for options in [{'since':'2026-02-30'}, {'since':'2026-1-01'}, {'since':'2026-02-01','until':'2026-01-01'}, {'limit':0}, {'limit':51}]:
            with self.subTest(options=options), self.assertRaises(ValueError):
                search('reading', self.root, **options)

    def test_empty_query_and_absent_archive(self):
        self.assertEqual(search('', self.root)['hits'], [])
        with self.assertRaises(ValueError): search('reading', self.root / 'absent')

    def test_unreadable_file_reported_and_other_hit_retained(self):
        from bailing.archive import read_local
        def mocked(path, root):
            if path == self.first: raise OSError(11, 'unavailable')
            return read_local(path, root)
        with patch('bailing.archive.read_local', side_effect=mocked):
            result = search('reading', self.root)
        self.assertEqual(len(result['hits']), 1)
        self.assertEqual(len(result['skipped']), 1)
        self.assertIn('Skipped:', render(result))

    def test_invalid_encoding_filename_and_date_reported(self):
        self.write('bad-name.md', 'reading')
        self.write('2026-02-30-other-demo.md', 'reading')
        (self.archive / '2026-01-03-other-invalid.md').write_bytes(b'\xff')
        self.assertEqual(len(search('reading', self.root)['skipped']), 3)

    def test_links_not_read(self):
        outside = self.root / 'outside'
        outside.mkdir()
        (outside / '2026-01-03-other-secret.md').write_text('secretword')
        (self.archive / 'linked-folder').symlink_to(outside, target_is_directory=True)
        (self.archive / '2026-01-03-other-link.md').symlink_to(outside / '2026-01-03-other-secret.md')
        result = search('secretword', self.root)
        self.assertEqual(result['hits'], [])
        self.assertEqual(len(result['skipped']), 2)
        self.assertNotIn('secretword', render(result))

    def test_archive_root_symlink_rejected(self):
        import shutil
        shutil.rmtree(self.archive)
        self.archive.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError): search('reading', self.root)

    def test_search_does_not_modify_sources(self):
        before = {p.name:p.read_bytes() for p in self.archive.iterdir()}
        search('reading', self.root)
        self.assertEqual(before, {p.name:p.read_bytes() for p in self.archive.iterdir()})

    def test_cli_json(self):
        r = subprocess.run([sys.executable, '-m', 'bailing', 'archive-search', '社区读书会', '--root', 'examples/fictional', '--runtime', 'hermes', '--json'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        result = json.loads(r.stdout)
        self.assertEqual(result['hits'][0]['session'], 'reading-followup')
        self.assertIn('30 minutes', result['hits'][0]['text'])

    def test_deterministic_ties(self):
        self.write('2026-01-04-other-b.md', 'sameword')
        self.write('2026-01-04-other-a.md', 'sameword')
        names = [h['path'] for h in search('sameword', self.root)['hits']]
        self.assertEqual(names, sorted(names))

if __name__ == '__main__': unittest.main()
