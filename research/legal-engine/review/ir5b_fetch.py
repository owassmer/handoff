"""IR5B: fetch a URL and save its text mechanically as sources/REVIEW5B_<name>.txt; or search CourtListener.

Usage:
  python3 review/ir5b_fetch.py NAME URL          # save page text (refuses to overwrite)
  python3 review/ir5b_fetch.py --search 'QUERY' [court]   # CourtListener v4 search, prints hits
HTML is stripped to text (tags removed, entities unescaped, whitespace collapsed per line).
"""
import datetime
import html
import json
import pathlib
import re
import subprocess
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")


def get(url, timeout=90):
    return subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url], capture_output=True).stdout


def strip(text):
    if "<html" in text.lower() or "<body" in text.lower() or "<div" in text.lower():
        text = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
        text = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>|</h\d>|</li>", "\n", text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = html.unescape(text)
        text = "\n".join(re.sub(r"[ \t ]+", " ", l).strip() for l in text.splitlines())
        text = re.sub(r"\n{3,}", "\n\n", text)
    return text


if sys.argv[1] == "--search":
    q = sys.argv[2]
    court = sys.argv[3] if len(sys.argv) > 3 else "ny nyappdiv nyappterm nysupct nycivct nyfamct nycountyct"
    url = ("https://www.courtlistener.com/api/rest/v4/search/?type=o&q=" + urllib.parse.quote(q)
           + "&court=" + urllib.parse.quote(court))
    raw = get(url, 120)
    try:
        d = json.loads(raw)
    except Exception:
        print(raw[:500])
        sys.exit(1)
    print("count", d.get("count"))
    for r in d.get("results", [])[:20]:
        print("-", r.get("caseName"), "|", r.get("court"), "|", r.get("dateFiled"), "|", r.get("citation"),
              "| https://www.courtlistener.com" + (r.get("absolute_url") or ""))
        for o in r.get("opinions", [])[:1]:
            print("   ", re.sub(r"\s+", " ", o.get("snippet") or "")[:300])
    sys.exit(0)

if sys.argv[1] == "--cap":
    # Harvard Caselaw Access Project static files: --cap NAME reporter volume page
    name, rep, vol, page = sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
    out = ROOT / "sources" / f"REVIEW5B_{name}.txt"
    if out.exists():
        sys.exit(f"exists: {out}")
    meta = json.loads(get(f"https://static.case.law/{rep}/{vol}/CasesMetadata.json", 120))
    hits = [m for m in meta if int(re.sub(r"\D", "", m["first_page"]) or 0) <= page <= int(re.sub(r"\D", "", m["last_page"]) or 0)]
    if not hits:
        sys.exit("no case at that page")
    parts = []
    for m in hits:
        url = f"https://static.case.law/{rep}/{vol}/cases/{m['file_name']}.json"
        c = json.loads(get(url, 120))
        body = c.get("casebody", {})
        txt = [c.get("name", ""), c.get("decision_date", ""), c.get("court", {}).get("name", ""),
               "; ".join(x["cite"] for x in c.get("citations", [])), "", body.get("head_matter", "")]
        for o in body.get("opinions", []):
            txt += ["", f"[{o.get('type')}] {o.get('author') or ''}", o.get("text", "")]
        parts.append(f"CAP URL: {url}\n" + "\n".join(txt))
    hdr = (f"SOURCE: Harvard Caselaw Access Project static files, {rep} {vol} p.{page}\nRETRIEVED: "
           f"{datetime.date.today().isoformat()} by independent reviewer 5B via curl; JSON text saved mechanically.\n\n")
    out.write_text(hdr + "\n\n=====\n\n".join(parts))
    print("saved", out, sum(len(p) for p in parts), [m["name_abbreviation"] for m in hits])
    sys.exit(0)

name, url = sys.argv[1], sys.argv[2]
out = ROOT / "sources" / f"REVIEW5B_{name}.txt"
if out.exists():
    sys.exit(f"exists: {out}")
text = strip(get(url).decode("utf-8", errors="replace"))
if len(text.strip()) < 500:
    sys.exit(f"too short ({len(text)} chars); not saved")
hdr = (f"SOURCE: {url}\nRETRIEVED: {datetime.date.today().isoformat()} by independent reviewer 5B via curl; "
       "HTML stripped mechanically.\n\n")
out.write_text(hdr + text)
print("saved", out, len(text))
