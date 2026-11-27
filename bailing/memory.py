"""Explicit local facts. SQLite transactions serialize writers; no platform discovery."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3

CATEGORIES = ('basic', 'family', 'preference', 'topic')

def connect(root):
    directory = root / 'memory' / 'continuity'
    if directory.is_symlink() or (root / 'memory').is_symlink():
        raise ValueError('Refuse symlink memory directory')
    directory.mkdir(exist_ok=True, mode=0o700)
    file = directory / 'facts.sqlite3'
    if file.is_symlink():
        raise ValueError('Refuse symlink fact database')
    db = sqlite3.connect(file, timeout=5)
    db.execute('CREATE TABLE IF NOT EXISTS facts (category TEXT, key TEXT, value TEXT, source TEXT, updated TEXT, PRIMARY KEY(category,key))')
    return db

def update(root, action, category, key, value=None, source=None):
    if action not in ('save', 'forget') or category not in CATEGORIES:
        raise ValueError('Invalid action or category')
    if not isinstance(key, str) or not key.strip() or len(key)>80 or any(ord(c)<32 for c in key):
        raise ValueError('Key must be 1–80 printable characters')
    if action == 'save' and (not isinstance(value,str) or not value.strip() or len(value)>1000 or not isinstance(source,str) or not source.strip() or len(source)>200):
        raise ValueError('Save requires value (1–1000 characters) and source (1–200 characters)')
    db = connect(root)
    try:
        with db:
            if action == 'forget':
                db.execute('DELETE FROM facts WHERE category=? AND key=?', (category,key))
            else:
                db.execute('INSERT OR REPLACE INTO facts VALUES (?,?,?,?,?)', (category,key,value,source,datetime.now(timezone.utc).isoformat()))
    finally:
        db.close()
    return {'ok':True, 'action':action, 'scope':'current fact store only; archives, journals and other indexes are unaffected'}

def snapshot(root, budget=6000, query=None):
    if budget < 1:
        raise ValueError('Budget must be positive')
    db = connect(root)
    try:
        rows = db.execute('SELECT category,key,value,source,updated FROM facts ORDER BY category,key').fetchall()
    finally:
        db.close()
    records = [dict(zip(('category','key','value','source','updated'),r)) for r in rows]
    if query is not None:
        records = [r for r in records if query.casefold() in (r['key']+' '+r['value']).casefold()]
    result = {'evidence':'historical_reference; current user corrections take priority', 'scope':'explicit current facts only', 'records':[], 'omitted':[{'category':r['category'],'key':r['key']} for r in records]}
    def encoded():
        return json.dumps(result,ensure_ascii=False,indent=2)
    if len(encoded())>budget:
        raise ValueError('Budget cannot hold complete omission list')
    for r in records:
        ref={'category':r['category'],'key':r['key']}
        result['omitted'].remove(ref);result['records'].append(r)
        if len(encoded())>budget:
            result['records'].pop();result['omitted'].append(ref)
    return encoded()
