"""IR4B: fetch a URL and save its text mechanically as sources/REVIEW4B_<name>.txt.

Usage: python3 review/ir4b_fetch.py NAME URL
HTML is stripped to text (tags removed, entities unescaped, whitespace collapsed per line).
Refuses to overwrite an existing file.
"""
import html
import pathlib
import re
import subprocess
import sys
import datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
name, url = sys.argv[1], sys.argv[2]
out = ROOT / "sources" / f"REVIEW4B_{name}.txt"
if out.exists():
    sys.exit(f"exists: {out}")
raw = subprocess.run(["curl", "-sL", "-m", "60", "-A", "Mozilla/5.0 (research)", url], capture_output=True).stdout
text = raw.decode("utf-8", errors="replace")
if "<html" in text.lower() or "<body" in text.lower():
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
    text = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>|</h\d>", "\n", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = "\n".join(re.sub(r"[ \t ]+", " ", l).strip() for l in text.splitlines())
    text = re.sub(r"\n{3,}", "\n\n", text)
if len(text.strip()) < 500:
    sys.exit(f"too short ({len(text)} chars); not saved")
hdr = f"SOURCE: {url}\nRETRIEVED: {datetime.date.today().isoformat()} by independent reviewer 4B via curl; HTML stripped mechanically.\n\n"
out.write_text(hdr + text)
print("saved", out, len(text))
