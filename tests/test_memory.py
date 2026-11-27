import concurrent.futures
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from bailing.memory import update, snapshot

class FactsTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        (self.root/'memory').mkdir()
    def tearDown(self): self.tmp.cleanup()
    def save(self,key='reading',value='paper',source='synthetic:a'):
        return update(self.root,'save','preference',key,value,source)
    def test_correction_and_source(self):
        self.save();self.save(value='digital',source='synthetic:b')
        records=json.loads(snapshot(self.root))['records']
        self.assertEqual(len(records),1);self.assertEqual(records[0]['source'],'synthetic:b')
        self.assertEqual(records[0]['value'],'digital');self.assertTrue(records[0]['updated'])
    def test_forget_scope(self):
        self.save(); archive=self.root/'memory/old.md';archive.write_text('paper')
        result=update(self.root,'forget','preference','reading')
        self.assertEqual(json.loads(snapshot(self.root))['records'],[])
        self.assertEqual(archive.read_text(),'paper');self.assertIn('unaffected',result['scope'])
    def test_budget_and_omissions(self):
        for i in range(4):self.save(str(i),'x'*900)
        data=snapshot(self.root,1000);result=json.loads(data)
        self.assertLessEqual(len(data),1000)
        self.assertEqual(len(result['records'])+len(result['omitted']),4)
        self.assertTrue(result['omitted'])
        with self.assertRaises(ValueError):snapshot(self.root,20)
    def test_concurrent_writers(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda i:self.save(str(i)),range(16)))
        self.assertEqual(len(json.loads(snapshot(self.root,20000))['records']),16)
    def test_corrupt_database_is_not_empty(self):
        d=self.root/'memory/continuity';d.mkdir();p=d/'facts.sqlite3';p.write_bytes(b'broken')
        with self.assertRaises(sqlite3.Error):snapshot(self.root)
        self.assertEqual(p.read_bytes(),b'broken')
    def test_invalid_and_symlink(self):
        with self.assertRaises(ValueError):self.save(source='')
        with self.assertRaises(ValueError):update(self.root,'save','wrong','k','v','s')
        outside=self.root/'outside';outside.mkdir()
        (self.root/'memory/continuity').symlink_to(outside)
        with self.assertRaises(ValueError):self.save()
    def test_search_current_store_only(self):
        self.save();self.assertEqual(len(json.loads(snapshot(self.root,query='PAPER'))['records']),1)
        update(self.root,'forget','preference','reading')
        self.assertEqual(json.loads(snapshot(self.root,query='paper'))['records'],[])
