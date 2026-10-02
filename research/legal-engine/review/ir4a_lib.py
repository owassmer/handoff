"""Independent review 4A helpers: whitespace-normalized source reading and anchor-based verbatim quote extraction.

Quotes are cut mechanically from saved source files between a start anchor and an end anchor, so nothing is retyped.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


_cache = {}


def text(source_file):
    p = ROOT / source_file if not str(source_file).startswith("/") else pathlib.Path(source_file)
    if p not in _cache:
        _cache[p] = norm(p.read_text(errors="replace"))
    return _cache[p]


def cut(source_file, start, end=None, maxlen=900):
    """Return the normalized span of source_file from the first `start` to the end of the first `end` after it."""
    t = text(source_file)
    s, e = norm(start), norm(end) if end else None
    i = t.find(s)
    if i < 0:
        raise KeyError(f"start anchor not found in {source_file}: {start[:80]!r}")
    if e is None:
        return t[i:i + len(s)]
    j = t.find(e, i + len(s) - min(len(s), len(e)))
    if j < 0:
        raise KeyError(f"end anchor not found in {source_file} after start: {end[:80]!r}")
    q = t[i:j + len(e)]
    if len(q) > maxlen:
        raise ValueError(f"quote too long ({len(q)}) in {source_file}: {start[:60]!r}")
    return q


def contains(source_file, quote):
    return norm(quote) in text(source_file)
