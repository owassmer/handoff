"""Independent review 5A: fetch a URL with curl, strip HTML mechanically, save under sources/REVIEW5A_<name>.txt.

Usage:
  python3 review/ir5a_fetch.py NAME URL [--raw] [--pdf]
  python3 review/ir5a_fetch.py --toc URL          (print link list + text of a table-of-contents page; saves nothing)
Never overwrites an existing file. Text is extracted by html.parser (no retyping). --pdf runs pdftotext -layout.
public.law pages are trimmed to the section body (from the page H1 to the 'Location:' footer) mechanically.
"""
import datetime
import html
import html.parser
import pathlib
import re
import subprocess
import sys
import tempfile

SRC = pathlib.Path(__file__).resolve().parent.parent / "sources"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


class Strip(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.links = [], 0, []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1
        if tag == "a":
            self.links.append(dict(attrs).get("href"))
        if tag in ("p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "blockquote", "pre"):
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self.skip = max(0, self.skip - 1)
        if tag in ("p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "blockquote"):
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def fetch_bytes(url, timeout=90):
    r = subprocess.run(["curl", "-sL", "--compressed", "--max-time", str(timeout), "-A", UA, url], capture_output=True)
    return r.stdout


def to_text(raw):
    s = Strip()
    s.feed(raw)
    t = "".join(s.out)
    t = re.sub(r"[ \t\r\f\v ]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n\n", t)
    return t.strip(), s.links


def trim_public_law(t):
    i = t.find("N.Y.\n")
    j = t.find("Location:")
    k = t.find("Original Source:")
    if i >= 0 and j > i:
        body = t[i:j].strip()
        tail = t[k:k + 400].split("Blank Outline")[0].strip() if k >= 0 else ""
        return body + "\n\n" + tail
    return t


def main():
    if sys.argv[1] == "--toc":
        raw = fetch_bytes(sys.argv[2]).decode("utf-8", "replace")
        t, links = to_text(raw)
        for l in links:
            if l and ("section" in l or "article" in l or "title" in l or "part" in l):
                print("LINK", l)
        print(t[:int(sys.argv[3]) if len(sys.argv) > 3 else 6000])
        return
    name, url = sys.argv[1], sys.argv[2]
    p = SRC / f"REVIEW5A_{name}.txt"
    def key(n):
        n = re.sub(r"\.txt$", "", n)
        n = re.sub(r"^(REVIEW\d[AB]?_|SWEEP_)", "", n)
        n = re.sub(r"_(nysenate|justia|LII|uscode|ecfr|courtlistener|nycourts|live.*|official.*)$", "", n, flags=re.I)
        return n.upper()
    dup = [q.name for q in SRC.iterdir() if key(q.name) == key(p.name) and q.name != p.name]
    if dup and "--force" not in sys.argv:
        print("already saved (not refetched):", name, dup)
        return
    if p.exists():
        print("exists", p.name)
        return
    raw = fetch_bytes(url)
    how = "curl"
    if "--pdf" in sys.argv:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(raw)
        text = subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True).stdout.decode("utf-8", "replace")
        how = "curl + pdftotext -layout"
    elif "--cap" in sys.argv:
        import json
        d = json.loads(raw.decode("utf-8", "replace"))
        cb = d.get("casebody", {})
        parts = [d.get("name", ""), "; ".join(c.get("cite", "") for c in d.get("citations", [])), d.get("decision_date", ""),
                 (d.get("court") or {}).get("name", ""), cb.get("head_matter", "")]
        for o in cb.get("opinions", []):
            parts.append(f"[{o.get('type')}] {o.get('author') or ''}\n{o.get('text', '')}")
        text = "\n\n".join(parts)
        how = "curl of the Caselaw Access Project static JSON (case.law, Harvard LIL); casebody text joined mechanically"
    elif "--raw" in sys.argv:
        text = raw.decode("utf-8", "replace")
    else:
        text, _ = to_text(raw.decode("utf-8", "replace"))
        if "public.law" in url:
            text = trim_public_law(text)
            how = "curl of the public.law mirror of the official nysenate.gov text (nysenate.gov is Cloudflare-walled to curl and browser)"
    if len(text) < 400 or "Just a moment" in text[:300]:
        print("too short or blocked, not saved", name, len(text))
        return
    p.write_text(f"SOURCE: {url}\nRETRIEVED: {datetime.date.today().isoformat()} by independent reviewer 5A via {how}; "
                 f"text extracted mechanically by review/ir5a_fetch.py\n\n{text}\n")
    print("saved", p.name, len(text))


if __name__ == "__main__":
    main()
