"""Read-only search of explicitly supplied local Markdown archives."""
from datetime import date
from pathlib import Path
import re
from .retrieval import read_local, terms, rank

NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z][a-z0-9_]*)-(.+)\.md$")
MESSAGE = re.compile(r"^### (?:user|assistant|百灵) · ")

def valid_date(value):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("Dates must use YYYY-MM-DD")
    date.fromisoformat(value)
    return value

def search(query, root, limit=8, runtime=None, since=None, until=None, session=None):
    if not 1 <= limit <= 50:
        raise ValueError("Result limit must be between 1 and 50")
    if since: valid_date(since)
    if until: valid_date(until)
    if since and until and since > until:
        raise ValueError("since must not be later than until")
    archive = root / "memory/archive"
    if archive.is_symlink():
        raise ValueError("Archive directory must not be a symlink")
    if not archive.exists():
        raise ValueError("No memory/archive directory; see docs/ARCHIVE.md")
    if not archive.is_dir() or not archive.resolve().is_relative_to(root.resolve()):
        raise ValueError("Unsafe archive directory")
    docs, skipped, metadata = [], [], {}
    # Do not follow symlink directories. This is not a sandbox against concurrent writers.
    import os
    for folder, dirs, files in os.walk(archive, followlinks=False):
        dirs.sort()
        for name in list(dirs):
            path = Path(folder) / name
            if path.is_symlink():
                skipped.append({"path": str(path.relative_to(root)), "reason": "symlink"})
                dirs.remove(name)
        for name in sorted(files):
            path = Path(folder) / name
            if path.suffix != ".md" or name == "README.md": continue
            relative = str(path.relative_to(root))
            if path.is_symlink():
                skipped.append({"path": relative, "reason": "symlink"}); continue
            match = NAME.fullmatch(name)
            if not match:
                skipped.append({"path": relative, "reason": "unrecognized filename"}); continue
            day, source, identity = match.groups()
            try: valid_date(day)
            except ValueError:
                skipped.append({"path": relative, "reason": "invalid date"}); continue
            if runtime and source != runtime: continue
            if since and day < since: continue
            if until and day > until: continue
            if session and session not in identity: continue
            try: body = read_local(path, root)
            except (OSError, UnicodeError) as exc:
                skipped.append({"path": relative, "reason": type(exc).__name__}); continue
            lines = body.splitlines(keepends=True)
            starts = [i for i, line in enumerate(lines) if MESSAGE.match(line)]
            if not starts or starts[0] != 0: starts.insert(0, 0)
            for begin, end in zip(starts, starts[1:] + [len(lines)]):
                text = "".join(lines[begin:end])
                docs.append((path, begin + 1, text, terms(text)))
            metadata[relative] = {"date": day, "runtime": source, "session": identity}
    hits = rank(docs, query, root, limit)
    for hit in hits: hit.update(metadata[hit["path"]])
    return {"query": query, "scanned": len(docs), "hits": hits, "skipped": skipped,
            "evidence_status": "historical_reference", "current_facts_verified": False,
            "filters": {"runtime": runtime, "since": since, "until": until, "session": session}}

def render(result):
    output = [f"Historical reference only — {len(result['hits'])} hits; {result['scanned']} blocks; {len(result['skipped'])} skipped files/directories."]
    for item in result["hits"]:
        output.append(f"{item['path']}:{item['line']} [{item['runtime']} {item['date']}; session={item['session']}]")
        snippet = " ".join(item["text"].split())
        output.append(snippet[:240] + ("… [excerpt; read source for context]" if len(snippet) > 240 else ""))
    if not result["hits"]:
        output.append("No matching records; this does not prove an event never occurred.")
    for item in result["skipped"]:
        output.append(f"Skipped: {item['path']} ({item['reason']})")
    return "\n".join(output)
