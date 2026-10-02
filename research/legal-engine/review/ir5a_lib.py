"""Independent review 5A helpers: whitespace-normalized source reading and anchor-based verbatim quote cutting.

Quotes are cut mechanically from saved source files between a start anchor and an end anchor (both must occur in the
saved text), so nothing is retyped. CLI: python3 review/ir5a_lib.py peek FILE [START] [N]  |  find FILE REGEX [W]
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"


def norm(s):
    s = s.replace(" ", " ").replace("­", "").replace("​", "")
    return re.sub(r"\s+", " ", s).strip()


_cache = {}


def text(source_file):
    p = ROOT / source_file if not str(source_file).startswith("/") else pathlib.Path(source_file)
    if p not in _cache:
        _cache[p] = norm(p.read_text(errors="replace"))
    return _cache[p]


def cut(source_file, start, end=None, maxlen=1200):
    t = text(source_file)
    s = norm(start)
    i = t.find(s)
    if i < 0:
        raise KeyError(f"start anchor not found in {source_file}: {start[:90]!r}")
    if end is None:
        return t[i:i + len(s)]
    e = norm(end)
    j = t.find(e, i)
    if j < 0:
        raise KeyError(f"end anchor not found in {source_file} after start: {end[:90]!r}")
    q = t[i:j + len(e)]
    if len(q) > maxlen:
        raise ValueError(f"quote too long ({len(q)}) in {source_file}: {start[:60]!r}")
    return q


def contains(source_file, quote):
    return norm(quote) in text(source_file)


if __name__ == "__main__":
    cmd, f = sys.argv[1], sys.argv[2]
    f = f if f.startswith("sources/") or f.startswith("/") else "sources/" + f
    t = text(f)
    if cmd == "peek":
        start = sys.argv[3] if len(sys.argv) > 3 else ""
        n = int(sys.argv[4]) if len(sys.argv) > 4 else 1500
        i = t.find(norm(start)) if start else 0
        print(t[max(i, 0):max(i, 0) + n])
    elif cmd == "find":
        w = int(sys.argv[4]) if len(sys.argv) > 4 else 250
        for m in list(re.finditer(sys.argv[3], t, re.I))[:6]:
            print("...", t[max(0, m.start() - w):m.end() + w], "...\n")
