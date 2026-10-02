"""Independent review 4A: fetch a URL with curl, strip HTML mechanically, save under sources/REVIEW4A_<name>.txt.

Usage: python3 review/ir4a_fetch.py NAME URL [--raw]
Never overwrites an existing file. Text is extracted by html.parser (no retyping).
"""
import html
import html.parser
import pathlib
import re
import subprocess
import sys

SRC = pathlib.Path(__file__).resolve().parent.parent / "sources"


class Strip(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1
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


def fetch(url):
    r = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "60", "-A",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
                        url], capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def to_text(raw):
    s = Strip()
    s.feed(raw)
    t = "".join(s.out)
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n\n", t)
    return t.strip()


def main():
    name, url = sys.argv[1], sys.argv[2]
    p = SRC / f"REVIEW4A_{name}.txt"
    if p.exists():
        print("exists", p.name)
        return
    raw = fetch(url)
    text = raw if "--raw" in sys.argv else to_text(raw)
    if len(text) < 500:
        print("too short, not saved", name, len(text))
        return
    p.write_text(f"SOURCE: {url}\nRETRIEVED: 2026-09-29 by independent reviewer 4A via curl; HTML stripped mechanically by review/ir4a_fetch.py\n\n{text}\n")
    print("saved", p.name, len(text))


if __name__ == "__main__":
    main()
