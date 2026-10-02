"""Build the Handoff decks as PPTX and PDF from one content module.

Every slide is laid out once, in inches, as a list of primitives (rect, oval, line, text).
The same primitives render to PPTX (python-pptx) and to HTML, which headless Chrome prints to PDF.
Text is measured against the Georgia and Arial font files; any text that does not fit its box stops the build.

Run from research/decks/src:
    uv run --with python-pptx python build_decks.py              # all decks
    uv run --with python-pptx python build_decks.py Handoff_Pitch
"""

import html
import pathlib
import re
import subprocess
import sys

from PIL import ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
from lxml import etree

import content

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# ---------------------------------------------------------------- design tokens
W, H = 13.333, 7.5
ML = 0.75                      # outer margin, left and right
CW = W - 2 * ML                # content width on a 12-column grid
GUT = 0.25
COL = (CW - 11 * GUT) / 12
BOT = 6.55                     # lowest point for body content
SRC_Y = 6.93                   # source line

PAPER, INK, TEXT2, MUTED = "FFFFFF", "15202B", "46505C", "7B8591"
RULE, PANEL, BAR, COUNT = "D9DDE2", "F1F3F5", "B4BCC6", "D3DAE2"
DARK, ONDARK, DARKRULE = "101C2B", "C3CCD7", "2A3A4E"
ACCENT, WHITE = "C2410C", "FFFFFF"
ARROW = "5B6573"

SERIF, SANS = "Georgia", "Arial"
FONT_FILES = {
    (SERIF, False): "/System/Library/Fonts/Supplemental/Georgia.ttf",
    (SERIF, True): "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    (SANS, False): "/System/Library/Fonts/Supplemental/Arial.ttf",
    (SANS, True): "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
}
# type scale (pt): display 64, divider 46, headline 32, big number 60-120, lede 20, body 18-20, label 12, source 10
LH_BODY, LH_HEAD = 1.28, 1.14
TRACK = 0.12                   # letter-spacing for uppercase labels, in em
_fonts = {}


class FitError(Exception):
    pass


# ---------------------------------------------------------------- text measurement

def runs(para):
    """Split '**bold**' markup into (text, bold) runs."""
    return [(p, i % 2 == 1) for i, p in enumerate(re.split(r"\*\*", para)) if p]


def _font(face, bold, size):
    key = (face, bold, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_FILES[(face, bold)], int(round(size * 10)))
    return _fonts[key]


def text_w(s, size, bold=False, face=SANS, track=0.0):
    return (_font(face, bold, size).getlength(s) + len(s) * track * size * 10) / 10 / 72


def prep(paras, size, width, bold=False, face=SANS, track=0.0):
    """Apply ties, then undo any tie whose joined words would not fit the width."""
    out = []
    for p in ([paras] if isinstance(paras, str) else paras):
        p = tie(p)
        toks = p.split(" ")
        fixed = []
        for t in toks:
            if NBSP in t and text_w(t.replace("**", ""), size, bold, face, track) > width * 0.99:
                t = t.replace(NBSP, " ")
            fixed.append(t)
        out.append(" ".join(fixed))
    return out


def para_lines(para, size, width, bold=False, face=SANS, track=0.0):
    """Greedy line count. Browsers and PowerPoint may also break after a hyphen or en dash, so model that."""
    words = []   # (text, bold, space_before)
    for txt, b in runs(para):
        for tok in re.split(r"[ \t\n]+", txt):
            if not tok:
                continue
            parts = re.findall(r"[^-–]+[-–]?|[-–]", tok)
            for j, part in enumerate(parts):
                words.append((part, b or bold, j == 0))
    lines, cur = 1, 0.0
    space = text_w(" ", size, face=face, track=track)
    for tok, b, sb in words:
        ww = text_w(tok, size, b, face, track)
        if ww > width:
            raise FitError(f"word too wide: {tok!r} at {size}pt in {width:.2f}in")
        gap = space if sb else 0.0
        if cur == 0:
            cur = ww
        elif cur + gap + ww <= width:
            cur += gap + ww
        else:
            lines += 1
            cur = ww
    return lines


def text_h(paras, size, width, bold=False, face=SANS, lh=LH_BODY, gap=0, track=0.0):
    paras = prep(paras, size, width, bold, face, track)
    n = sum(para_lines(p, size, width * 0.99, bold, face, track) for p in paras)
    return n * size * lh / 72 + (len(paras) - 1) * gap / 72


def n_lines(paras, size, width, bold=False, face=SANS):
    paras = prep(paras, size, width, bold, face)
    return sum(para_lines(p, size, width * 0.99, bold, face) for p in paras)


def balanced_w(paras, size, w, bold=False, face=SANS):
    """Narrowest width (<= w) with the same line count, so lines come out even and no word sits alone."""
    n = n_lines(paras, size, w, bold, face)
    if n == 1:
        return w
    lo, hi = w * 0.4, w
    for _ in range(18):
        mid = (lo + hi) / 2
        try:
            ok = n_lines(paras, size, mid, bold, face) <= n
        except FitError:
            ok = False
        if ok:
            hi = mid
        else:
            lo = mid
    return min(w, hi + 0.15)


# ---------------------------------------------------------------- typographic ties

NBSP = "\u00a0"


def tie(para):
    """Keep a number with the word after it, and the last two words of a paragraph together (no orphans)."""
    para = re.sub(r"(?<=\d) (?=(?:hours|days|weeks|months|years|of|a|to|units|homes|runs|coats|each|per)\b)",
                  NBSP, para)
    para = re.sub(r"\b(month|day|Day|§|§§|Law|Act|No\.|January|February|March|April|May|June|July|August|"
                  r"September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec) (?=\d)",
                  lambda m: m.group(1) + NBSP, para)
    para = re.sub(r"\b(New) (York)\b", "\\1" + NBSP + "\\2", para)
    para = re.sub(r"(§§?) ", "\\1" + NBSP, para)
    para = re.sub(r" (=|×) ", NBSP + "\\1" + NBSP, para)
    words = para.split(" ")
    if (len(words) >= 4 and NBSP not in words[-1] and len(words[-1].strip(".,;:!?”")) <= 12
            and len(words[-1]) + len(words[-2]) <= 20):
        para = " ".join(words[:-2]) + " " + words[-2] + NBSP + words[-1]
    return para


# ---------------------------------------------------------------- primitives

def T(x, y, w, h, paras, size=18, color=INK, bold=False, face=SANS, align="left", valign="top", gap=0,
      lh=LH_BODY, track=0.0, where=""):
    if isinstance(paras, str):
        paras = [paras]
    paras = prep(paras, size, w, bold, face, track)
    need = text_h(paras, size, w, bold, face, lh, gap, track)
    if need > h + 0.005:
        raise FitError(f"{where}: text needs {need:.2f}in, box {h:.2f}in: {paras[0][:60]!r}")
    if x < -0.001 or y < -0.001 or x + w > W + 0.001 or y + h > H + 0.001:
        raise FitError(f"{where}: box off slide: {paras[0][:40]!r}")
    return dict(k="text", x=x, y=y, w=w, h=h, paras=paras, size=size, color=color, bold=bold, face=face,
                align=align, valign=valign, gap=gap, lh=lh, track=track)


def label(x, y, w, s, color=MUTED, size=12, where="", align="left"):
    """Uppercase, tracked label. One line."""
    s = s.upper()
    h = size * LH_BODY / 72
    return T(x, y, w, h, s, size, color, True, SANS, align=align, track=TRACK, where=where), h


def R(x, y, w, h, fill=None, line=None, lw=1.0, dash=False, radius=0.0):
    return dict(k="rect", x=x, y=y, w=w, h=h, fill=fill, line=line, lw=lw, dash=dash, radius=radius)


def O(x, y, d, fill=None, line=None, lw=1.0):
    return dict(k="oval", x=x, y=y, w=d, h=d, fill=fill, line=line, lw=lw)


def L(x1, y1, x2, y2, color=RULE, lw=1.0, arrow=False, dash=False):
    return dict(k="line", x1=x1, y1=y1, x2=x2, y2=y2, color=color, lw=lw, arrow=arrow, dash=dash)


def check_bottom(y, where, limit=BOT):
    if y > limit + 0.005:
        raise FitError(f"{where}: body runs to {y:.2f}in (limit {limit:.2f})")


# ---------------------------------------------------------------- slide frame

def frame(s, idx, deck):
    """Kicker, headline, optional lede, source line and page number. Returns (elements, body_top)."""
    where = f"{deck['file']} slide {idx}"
    els = []
    if s.get("kicker"):
        e, _ = label(ML, 0.55, 6.0, s["kicker"], ACCENT, 12, where)
        els.append(e)
    if s.get("rail"):
        els += step_rail(s["rail"], where)
    hs = s.get("hsize", 30)
    if not s["title"].endswith((".", "?", "!")):
        s["title"] += "."
    hw = balanced_w(s["title"], hs, s.get("hw", CW * 0.88), face=SERIF)
    hh = text_h(s["title"], hs, hw, face=SERIF, lh=LH_HEAD)
    if n_lines(s["title"], hs, hw, face=SERIF) > 2:
        raise FitError(f"{where}: headline over two lines: {s['title']!r}")
    els.append(T(ML, 0.86, hw, hh, s["title"], hs, INK, face=SERIF, lh=LH_HEAD, where=where))
    y = 0.86 + hh
    if s.get("lede"):
        lw = balanced_w(s["lede"], 20, CW * 0.8)
        lh_ = text_h(s["lede"], 20, lw)
        els.append(T(ML, y + 0.16, lw, lh_, s["lede"], 20, TEXT2, where=where))
        y += 0.16 + lh_
    els += footer(s, idx, deck, where)
    return els, y + 0.42


def footer(s, idx, deck, where, dark=False):
    els = []
    col = "8C99A8" if dark else MUTED
    src = s.get("src")
    if src:
        if not src.startswith("Source"):
            src = ("Sources: " if ";" in src else "Source: ") + src
        fh = text_h(src, 10, CW - 3.2, lh=1.3)
        if fh > 0.37:
            raise FitError(f"{where}: source line over two lines")
        els.append(T(ML, SRC_Y, CW - 3.2, 0.37, src, 10, col, lh=1.3, where=where))
    els.append(T(W - ML - 3.0, SRC_Y, 3.0, 0.2, f"{deck['short']}   {idx}", 10, col, align="right", lh=1.3,
                 where=where))
    return els


def step_rail(rail, where):
    """Small progress indicator for step slides: (current, total)."""
    cur, tot = rail
    d, gap = 0.26, 0.14
    x0 = W - ML - tot * d - (tot - 1) * gap
    els = []
    for i in range(tot):
        x = x0 + i * (d + gap)
        on = i + 1 == cur
        els.append(O(x, 0.5, d, fill=ACCENT if on else None, line=None if on else RULE, lw=1.0))
        els.append(T(x, 0.5, d, d, str(i + 1), 11, WHITE if on else MUTED, True, align="center", valign="middle",
                     lh=1.0, where=where))
    return els


def note_space(s, w=CW):
    if not s.get("note"):
        return BOT
    nh = text_h(s["note"], 20, w - 0.35)
    return BOT - nh - 0.4


def place_note(s, end, where, x=ML, w=CW):
    if not s.get("note"):
        return []
    tw = balanced_w(s["note"], 20, w - 0.35)
    nh = text_h(s["note"], 20, tw)
    top = max(end + 0.4, s.get("note_min_y", 0))
    check_bottom(top + nh, where)
    return [R(x, top + 0.02, 0.05, nh - 0.04, fill=ACCENT),
            T(x + 0.3, top, tw, nh, s["note"], 20, INK, where=where)]


def lede_rows(items, x, y, w, where, size=18, lead_size=None, gap=0.2, rules=True, lead_color=INK,
              text_color=TEXT2):
    """Stacked items separated by hairlines. Each item is 'text' or (lead, text)."""
    els = []
    lead_size = lead_size or size
    for i, it in enumerate(items):
        if i and rules:
            els.append(L(x, y - gap / 2, x + w, y - gap / 2, RULE, 0.75))
        if isinstance(it, (list, tuple)):
            lead, txt = it
            lh_ = text_h(lead, lead_size, w, True)
            els.append(T(x, y, w, lh_, lead, lead_size, lead_color, True, where=where))
            y += lh_ + 0.03
            th = text_h(txt, size, w)
            els.append(T(x, y, w, th, txt, size, text_color, where=where))
            y += th
        else:
            th = text_h(it, size, w)
            els.append(T(x, y, w, th, it, size, INK, where=where))
            y += th
        y += gap
    return els, y - gap


# ---------------------------------------------------------------- layouts

def lay_title(s, idx, deck):
    where = f"{deck['file']} slide {idx}"
    els = [R(ML, 1.95, 0.7, 0.07, fill=ACCENT)]
    e, _ = label(ML, 2.22, 8, s.get("kicker", ""), ONDARK, 13, where)
    els.append(e)
    nw = balanced_w(s["name"], 60, CW * 0.9, face=SERIF)
    nh = text_h(s["name"], 60, nw, face=SERIF, lh=1.08)
    els.append(T(ML, 2.62, nw, nh, s["name"], 60, WHITE, face=SERIF, lh=1.08, where=where))
    lw = balanced_w(s["line"], 22, 8.8)
    lh_ = text_h(s["line"], 22, lw)
    els.append(T(ML, 2.62 + nh + 0.32, lw, lh_, s["line"], 22, ONDARK, where=where))
    check_bottom(2.62 + nh + 0.32 + lh_, where, 6.0)
    els.append(L(ML, 6.45, W - ML, 6.45, DARKRULE, 0.75))
    els.append(T(ML, 6.6, CW, 0.3, s["meta"], 14, ONDARK, where=where))
    return els


def lay_divider(s, idx, deck):
    where = f"{deck['file']} slide {idx}"
    els = [T(ML, 2.3, 3, 0.5, s["num"], 28, ACCENT, True, lh=1.1, where=where)]
    els.append(R(ML, 2.95, 0.7, 0.05, fill=ACCENT))
    nw = balanced_w(s["title"], 46, CW * 0.85, face=SERIF)
    nh = text_h(s["title"], 46, nw, face=SERIF, lh=1.1)
    els.append(T(ML, 3.2, nw, nh, s["title"], 46, WHITE, face=SERIF, lh=1.1, where=where))
    if s.get("line"):
        lw = balanced_w(s["line"], 22, 8.8)
        lh_ = text_h(s["line"], 22, lw)
        els.append(T(ML, 3.2 + nh + 0.3, lw, lh_, s["line"], 22, ONDARK, where=where))
    els += footer(s, idx, deck, where, dark=True)
    return els


def lay_findings(s, idx, deck):
    """Numbered findings in a grid of cells: (lead, text)."""
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    items = s["items"]
    ncol = s.get("ncol", 2)
    gapx = 0.6
    cw = (CW - gapx * (ncol - 1)) / ncol
    rows = [items[i:i + ncol] for i in range(0, len(items), ncol)]
    num_w = 0.62
    for r_i, row in enumerate(rows):
        lead_h = max(text_h(it[0], 20, cw - num_w, True) for it in row)
        body_h = max(text_h(it[1], 18, cw - num_w) for it in row)
        for c_i, it in enumerate(row):
            x = ML + c_i * (cw + gapx)
            n = r_i * ncol + c_i + 1
            els.append(L(x, y, x + cw, y, RULE, 0.75))
            els.append(T(x, y + 0.2, num_w, 0.5, f"{n:02d}", 20, ACCENT, True, where=where))
            els.append(T(x + num_w, y + 0.2, cw - num_w, lead_h, it[0], 20, INK, True, where=where))
            els.append(T(x + num_w, y + 0.2 + lead_h + 0.08, cw - num_w, body_h, it[1], 18, TEXT2, where=where))
        y += 0.2 + lead_h + 0.08 + body_h + 0.35
    end = y - 0.35
    check_bottom(end, where, note_space(s))
    return els + place_note(s, end, where)


def lay_stats(s, idx, deck):
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    st = s["stats"]
    n = len(st)
    gap = 0.4
    cw = (CW - gap * (n - 1)) / n
    ns = s.get("nsize", 54)
    y += 0.1
    nh = max(text_h(it["num"], ns, cw, True, lh=1.05) for it in st)
    lh_ = max(text_h(it["label"], 18, cw - 0.1) for it in st)
    for i, it in enumerate(st):
        x = ML + i * (cw + gap)
        hl = it.get("hl")
        els.append(L(x, y, x + cw, y, RULE, 0.75))
        els.append(R(x, y - 0.02, 0.6, 0.04, fill=ACCENT if hl else INK))
        els.append(T(x, y + 0.28, cw, nh, it["num"], ns, ACCENT if hl else INK, True, lh=1.05, where=where))
        els.append(T(x, y + 0.28 + nh + 0.12, cw - 0.1, lh_, it["label"], 18, TEXT2, where=where))
    end = y + 0.28 + nh + 0.12 + lh_
    check_bottom(end, where, note_space(s))
    return els + place_note(s, end, where)


def lay_bignum(s, idx, deck):
    """One large figure on the left; rule-separated points on the right."""
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    lw = s.get("left_w", 4.3)
    bs = s.get("bsize", 110)
    bh = text_h(s["big"], bs, lw, True, lh=1.0)
    els.append(T(ML - 0.04, y - 0.1, lw, bh, s["big"], bs, ACCENT, True, lh=1.0, where=where))
    ch = text_h(s["caption"], 20, lw - 0.3)
    els.append(T(ML, y - 0.1 + bh + 0.15, lw - 0.3, ch, s["caption"], 20, INK, where=where))
    rx = ML + lw + 0.5
    rw = W - ML - rx
    b, end = lede_rows(s["items"], rx, y, rw, where, 18, 18, 0.26)
    bottom = max(end, y - 0.1 + bh + 0.15 + ch)
    els.append(L(rx - 0.25, y, rx - 0.25, bottom, RULE, 0.75))
    check_bottom(bottom, where, note_space(s))
    return els + b + place_note(s, bottom, where)


def lay_list(s, idx, deck):
    """Rule-separated items, in one or two columns. Items are 'text' or (lead, text)."""
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    items = s["items"]
    ncol = s.get("ncol", 1)
    width = s.get("width", CW * (0.78 if ncol == 1 else 1))
    gapx = 0.6
    cw = (width - gapx * (ncol - 1)) / ncol
    if ncol == 1:
        b, end = lede_rows(items, ML, y, cw, where, 18, 20, 0.28)
        els += b
    else:
        rows = [items[i:i + ncol] for i in range(0, len(items), ncol)]
        for r_i, row in enumerate(rows):
            if r_i:
                y += 0.14
                els.append(L(ML, y, ML + width, y, RULE, 0.75))
                y += 0.14
            hs = [text_h(it, 18, cw) for it in row]
            for c_i, it in enumerate(row):
                els.append(T(ML + c_i * (cw + gapx), y, cw, hs[c_i], it, 18, INK, where=where))
            y += max(hs)
        end = y
    check_bottom(end, where, note_space(s))
    return els + place_note(s, end, where)


def lay_columns(s, idx, deck):
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    cols = s["cols"]
    n = len(cols)
    gap = s.get("gap", 0.45)
    cw = (CW - gap * (n - 1)) / n
    panel = s.get("panel", False)
    pad = 0.25 if panel else 0.0
    iw = cw - 2 * pad
    bsize = s.get("size", 18)
    lab_h = 12 * LH_BODY / 72 if any(c.get("label") for c in cols) else 0
    hd_h = max((text_h(c["head"], 22, iw, face=SERIF, lh=1.2) for c in cols if c.get("head")), default=0)
    pg = s.get("pgap", 10)
    body_h = max(text_h(c.get("body", []), bsize, iw, gap=pg) for c in cols)
    top = y + (0.22 if panel else 0.2)
    yy = top
    if lab_h:
        yy += lab_h + 0.12
    if hd_h:
        yy += hd_h + 0.12
    end = yy + body_h + (0.25 if panel else 0)
    for i, c in enumerate(cols):
        x = ML + i * (cw + gap)
        hl = c.get("hl")
        if panel:
            els.append(R(x, y, cw, end - y, fill=PANEL))
            els.append(R(x, y, cw, 0.05, fill=ACCENT if hl else INK))
        else:
            els.append(L(x, y, x + cw, y, RULE, 0.75))
            els.append(R(x, y - 0.02, 0.6, 0.04, fill=ACCENT if hl else INK))
        cy = top
        if lab_h:
            if c.get("label"):
                e, _ = label(x + pad, cy, iw, c["label"], ACCENT if hl else MUTED, 12, where)
                els.append(e)
            cy += lab_h + 0.12
        if hd_h:
            if c.get("head"):
                els.append(T(x + pad, cy, iw, hd_h, c["head"], 22, INK, face=SERIF, lh=1.2, where=where))
            cy += hd_h + 0.12
        body = c.get("body", [])
        if body:
            bh = text_h(body, bsize, iw, gap=pg)
            els.append(T(x + pad, cy, iw, bh, body, bsize, INK, gap=pg, where=where))
    check_bottom(end, where, note_space(s))
    return els + place_note(s, end, where)


def box_text_color(style):
    if style == "gate_pilot":
        return ACCENT
    return WHITE if style in ("today", "gate", "dark") else INK


def draw_box(x, y, w, h, style, radius=0.06):
    if style == "today" or style == "dark":
        return R(x, y, w, h, fill=INK, radius=radius)
    if style == "gate":
        return R(x, y, w, h, fill=ACCENT, radius=radius)
    if style == "pilot":
        return R(x, y, w, h, fill=WHITE, line=INK, lw=1.25, dash=True, radius=radius)
    if style == "gate_pilot":
        return R(x, y, w, h, fill=WHITE, line=ACCENT, lw=2.0, dash=True, radius=radius)
    return R(x, y, w, h, fill=PANEL, radius=radius)


def lay_flow(s, idx, deck):
    """Rows of boxes joined by arrows. Step style: today (filled), pilot (dashed), gate (accent), plain (panel)."""
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    arrow = s.get("arrow", 0.42)
    size = s.get("size", 18)
    pad = 0.14
    allbw = [(CW - arrow * (len(r["steps"]) - 1)) / len(r["steps"]) for r in s["rows"]]
    bh_all = max(max(text_h(st["t"], size, bw - 2 * pad, True) for st in r["steps"]) + 2 * pad
                 for r, bw in zip(s["rows"], allbw))
    bh_all = max(bh_all, s.get("minh", 0.85))
    for row in s["rows"]:
        steps = row["steps"]
        n = len(steps)
        bw = (CW - arrow * (n - 1)) / n
        if row.get("label"):
            e, lh_ = label(ML, y, CW, row["label"], MUTED, 12, where)
            els.append(e)
            y += lh_ + 0.14
        bh = bh_all
        sub_h = max((text_h(st["sub"], 18, bw - 0.05) for st in steps if st.get("sub")), default=0)
        for i, st in enumerate(steps):
            x = ML + i * (bw + arrow)
            style = st.get("style", row.get("style", "plain"))
            if st.get("gate"):
                style = "gate"
            els.append(draw_box(x, y, bw, bh, style))
            els.append(T(x + pad, y + pad, bw - 2 * pad, bh - 2 * pad, st["t"], size, box_text_color(style), True,
                         align="center", valign="middle", where=where))
            if st.get("sub"):
                els.append(T(x, y + bh + 0.16, bw - 0.05, sub_h, st["sub"], 18, TEXT2, where=where))
            if i < n - 1:
                ax = x + bw + 0.05
                els.append(L(ax, y + bh / 2, ax + arrow - 0.08, y + bh / 2, ARROW, 2.25, arrow=True))
        y += bh + (sub_h + 0.16 if sub_h else 0) + s.get("row_gap", 0.4)
    y -= s.get("row_gap", 0.4)
    if s.get("legend"):   # key sits in the header band, right-aligned with the kicker
        widths = [0.47 + text_w(t, 16) + 0.1 for _, t in s["legend"]]
        x = W - ML - sum(widths) - 0.4 * (len(widths) - 1)
        for (style, text), wd in zip(s["legend"], widths):
            els.append(draw_box(x, 0.55, 0.34, 0.2, style, 0.03))
            els.append(T(x + 0.47, 0.5, wd - 0.47, 0.3, text, 16, TEXT2, where=where))
            x += wd + 0.4
    check_bottom(y, where, note_space(s))
    return els + place_note(s, y, where)


def lay_layers(s, idx, deck):
    """Stacked bands: a label block on the left, what it does on the right."""
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    lw = 3.0
    gap = 0.12
    tx = ML + lw + 0.4
    tw = CW - lw - 0.4
    for band in s["bands"]:
        th = text_h(band["text"], 18, tw - 0.3)
        bh = max(th + 0.3, 0.72)
        style = band.get("style", "dark")
        els.append(draw_box(ML, y, lw, bh, style, 0.04))
        els.append(T(ML + 0.2, y, lw - 0.4, bh, band["name"], 20, box_text_color(style), True, valign="middle",
                     where=where))
        els.append(R(tx - 0.2, y, tw + 0.2, bh, fill=PANEL, radius=0.04))
        els.append(T(tx, y, tw - 0.3, bh, band["text"], 18, INK, valign="middle", where=where))
        y += bh + gap
    y -= gap
    check_bottom(y, where, note_space(s))
    return els + place_note(s, y, where)


def lay_timeline(s, idx, deck):
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    pts = s["points"]
    n = len(pts)
    gap = 0.35
    cw = (CW - gap * (n - 1)) / n
    ly = y + 0.14
    els.append(L(ML + 0.12, ly, ML + (n - 1) * (cw + gap) + 0.12, ly, RULE, 1.5))
    wh = max(text_h(p["when"], 20, cw, True) for p in pts)
    ends = []
    for i, p in enumerate(pts):
        x = ML + i * (cw + gap)
        st = p.get("style", "dark")
        d = 0.24
        if st == "hl":
            els.append(O(x, ly - d / 2, d, fill=ACCENT))
        elif st == "open":
            els.append(O(x, ly - d / 2, d, fill=WHITE, line=INK, lw=1.5))
        else:
            els.append(O(x, ly - d / 2, d, fill=INK))
        els.append(T(x, ly + 0.36, cw, wh, p["when"], 20, ACCENT if st == "hl" else INK, True, where=where))
        yy = ly + 0.36 + wh + 0.1
        th = text_h(p["what"], 18, cw)
        els.append(T(x, yy, cw, th, p["what"], 18, TEXT2, where=where))
        ends.append(yy + th)
    end = max(ends)
    check_bottom(end, where, note_space(s))
    return els + place_note(s, end, where)


def lay_table(s, idx, deck):
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    widths = s["widths"]
    cws = [CW * w / sum(widths) for w in widths]
    INSET = 0.15
    cws = [c - (INSET * 2 / len(cws)) for c in cws]
    xs = [ML + INSET + sum(cws[:i]) for i in range(len(cws))]
    pad = 0.25
    size = s.get("size", 18)
    acc = s.get("accent_col")
    hl_rows = set(s.get("hl_rows", []))
    for h_, x, c in zip(s["head"], xs, cws):
        e, _ = label(x, y, c - pad, h_, MUTED, 12, where)
        els.append(e)
    y += 12 * LH_BODY / 72 + 0.1
    els.append(L(ML, y, W - ML, y, INK, 1.0))
    y += 0.14
    for r_i, row in enumerate(s["rows"]):
        hl = r_i in hl_rows
        rh = max(text_h(cell, size, c - pad, i == 0 or hl) for i, (cell, c) in enumerate(zip(row, cws)))
        if hl:
            els.append(R(ML, y - 0.1, CW, rh + 0.2, fill=PANEL))
            els.append(R(ML, y - 0.1, 0.05, rh + 0.2, fill=ACCENT))
        for i, (cell, x, c) in enumerate(zip(row, xs, cws)):
            bold = i == 0 or (acc is not None and i == acc) or hl
            col = ACCENT if (acc is not None and i == acc) else (INK if i == 0 or hl else TEXT2)
            els.append(T(x, y, c - pad, rh, cell, size, col, bold, where=where))
        y += rh + 0.1
        if r_i < len(s["rows"]) - 1:
            if not hl and (r_i + 1) not in hl_rows:
                els.append(L(ML, y, W - ML, y, RULE, 0.75))
            y += 0.12
    check_bottom(y, where, note_space(s))
    return els + place_note(s, y, where)


def fmt_pct(v):
    return f"{v:g}%"


def lay_bars(s, idx, deck):
    """Horizontal bar charts in one or more panels.

    Panel: title, max, fmt ('pct' | 'usd' | 'bn'), rows of dict(label, v | lo,hi | a,b, hl, text).
    Pairs (a, b) draw two bars per row with a legend: series 0 accent, series 1 neutral.
    """
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    panels = s["panels"]
    n = len(panels)
    gapx = 0.7
    pw = (CW - gapx * (n - 1)) / n
    lab_w = s.get("label_w", 3.4 if n == 1 else 2.35)
    val_w = 1.25
    ends = []
    if s.get("legend"):
        x = ML
        for i, text in enumerate(s["legend"]):
            els.append(R(x, y + 0.06, 0.3, 0.2, fill=ACCENT if i == 0 else BAR))
            tw = text_w(text, 16) + 0.1
            els.append(T(x + 0.42, y, tw, 0.3, text, 16, TEXT2, where=where))
            x += 0.42 + tw + 0.5
        y += 0.55
    for p_i, p in enumerate(panels):
        px = ML + p_i * (pw + gapx)
        yy = y
        if p.get("title"):
            th = text_h(p["title"], 18, pw, True)
            els.append(T(px, yy, pw, th, p["title"], 18, INK, True, where=where))
            yy += th + 0.2
        bx = px + lab_w + 0.15
        bw = pw - lab_w - 0.15 - val_w
        mx = p["max"]
        rows = p["rows"]
        pair = any("a" in r for r in rows)
        bar_h = 0.24 if pair else 0.32
        rgap = s.get("row_gap", 0.3)
        # gridlines
        grid = p.get("grid")
        top = yy
        row_hs = []
        for r in rows:
            lh_ = text_h(r["label"], 18, lab_w, r.get("hl", False))
            bars_h = 2 * bar_h + 0.06 if pair else bar_h
            row_hs.append(max(lh_, bars_h))
        total_h = sum(row_hs) + rgap * (len(rows) - 1)
        if grid:
            for g in grid:
                gx = bx + bw * g / mx
                els.append(L(gx, top - 0.05, gx, top + total_h + 0.05, RULE, 0.75, dash=g != 0))
                gl = p.get("gfmt", fmt_pct)(g)
                els.append(T(gx - 0.5, top + total_h + 0.1, 1.0, 0.24, gl, 13, MUTED, align="center", lh=1.2,
                             where=where))
        for r, rh in zip(rows, row_hs):
            hl = r.get("hl", False)
            lh_ = text_h(r["label"], 18, lab_w, hl)
            els.append(T(px, yy + (rh - lh_) / 2, lab_w, lh_, r["label"], 18, INK, hl, where=where))
            if pair:
                by = yy + (rh - (2 * bar_h + 0.06)) / 2
                for k, key in enumerate(("a", "b")):
                    v = r[key]
                    ww = max(bw * v / mx, 0.03)
                    els.append(R(bx, by, ww, bar_h, fill=ACCENT if k == 0 else BAR))
                    txt = r.get(f"{key}_text", p.get("fmt", fmt_pct)(v))
                    els.append(R(bx + ww + 0.05, by + bar_h / 2 - 0.15, text_w(txt, 16, True) + 0.1, 0.3,
                                 fill=PAPER))
                    els.append(T(bx + ww + 0.1, by + bar_h / 2 - 0.16, val_w + 0.3, 0.32, txt, 16,
                                 ACCENT if k == 0 else TEXT2, True, lh=1.2, valign="middle", where=where))
                    by += bar_h + 0.06
            else:
                by = yy + (rh - bar_h) / 2
                col = ACCENT if hl else BAR
                if "lo" in r:
                    x0 = bx + bw * r["lo"] / mx
                    ww = max(bw * (r["hi"] - r["lo"]) / mx, 0.05)
                    els.append(R(bx, by + bar_h / 2 - 0.01, x0 - bx, 0.02, fill=RULE))
                    els.append(R(x0, by, ww, bar_h, fill=col))
                    end_x = x0 + ww
                else:
                    ww = max(bw * r["v"] / mx, 0.04)
                    els.append(R(bx, by, ww, bar_h, fill=col))
                    end_x = bx + ww
                txt = r.get("text") or p.get("fmt", fmt_pct)(r["v"])
                els.append(R(end_x + 0.06, by + bar_h / 2 - 0.16, text_w(txt, 18, True) + 0.12, 0.32, fill=PAPER))
                els.append(T(end_x + 0.12, by + bar_h / 2 - 0.17, val_w + 0.4, 0.34, txt, 18,
                             ACCENT if hl else INK, True, lh=1.2, valign="middle", where=where))
            yy += rh + rgap
        end = top + total_h + (0.4 if grid else 0)
        ends.append(end)
    end = max(ends)
    check_bottom(end, where, note_space(s))
    return els + place_note(s, end, where)


def lay_bars_shared(s, idx, deck):
    """Several measures for the same rows: one label column, one bar column per measure, values at bar ends."""
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    panels = s["panels"]
    n = len(panels)
    lab_w = s.get("label_w", 3.0)
    gapc = 0.5
    x0 = ML + lab_w + 0.3
    colw = (W - ML - x0 - gapc * (n - 1)) / n
    val_w = 0.95
    th = max(text_h(p["title"], 16, colw, True) for p in panels)
    for k, p in enumerate(panels):
        cx = x0 + k * (colw + gapc)
        els.append(T(cx, y, colw, th, p["title"], 16, TEXT2, True, where=where))
    y += th + 0.18
    labels = [r["label"] for r in panels[0]["rows"]]
    bar_h, rgap = 0.3, s.get("row_gap", 0.2)
    rh = max(max(text_h(lb, 18, lab_w, True) for lb in labels), bar_h)
    top = y
    for i, lb in enumerate(labels):
        hl = panels[0]["rows"][i].get("hl", False)
        lh_ = text_h(lb, 18, lab_w, hl)
        els.append(T(ML, y + (rh - lh_) / 2, lab_w, lh_, lb, 18, INK, hl, where=where))
        for k, p in enumerate(panels):
            r = p["rows"][i]
            cx = x0 + k * (colw + gapc)
            bw = colw - val_w
            ww = max(bw * r["v"] / p["max"], 0.04)
            by = y + (rh - bar_h) / 2
            els.append(R(cx, by, ww, bar_h, fill=ACCENT if r.get("hl") else BAR))
            txt = r.get("text") or p.get("fmt", fmt_pct)(r["v"])
            els.append(T(cx + ww + 0.1, by + bar_h / 2 - 0.17, val_w, 0.34, txt, 18, ACCENT if r.get("hl") else INK,
                         True, lh=1.2, valign="middle", where=where))
        y += rh + rgap
    end = y - rgap
    for k in range(n):
        cx = x0 + k * (colw + gapc)
        els.append(L(cx, top - 0.08, cx, end + 0.08, MUTED, 1.0))
    check_bottom(end, where, note_space(s))
    return els + place_note(s, end, where)


def lay_compare(s, idx, deck):
    """Two panels side by side, each with a head and rule-separated points; one may be highlighted."""
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    sides = s["sides"]
    gap = 0.45
    cw = (CW - gap) / 2
    pad = 0.3
    iw = cw - 2 * pad
    hh = max(text_h(sd["head"], 24, iw, face=SERIF, lh=1.2) for sd in sides)
    bodies = []
    for sd in sides:
        _, e = lede_rows(sd["items"], 0, 0, iw, where, 18, 18, 0.22)
        bodies.append(e)
    ph = 0.3 + 12 * LH_BODY / 72 + 0.1 + hh + 0.25 + max(bodies) + 0.3
    for i, sd in enumerate(sides):
        x = ML + i * (cw + gap)
        hl = sd.get("hl")
        els.append(R(x, y, cw, ph, fill=PANEL))
        els.append(R(x, y, cw, 0.06, fill=ACCENT if hl else INK))
        e, lh_ = label(x + pad, y + 0.3, iw, sd["label"], ACCENT if hl else MUTED, 12, where)
        els.append(e)
        els.append(T(x + pad, y + 0.3 + lh_ + 0.1, iw, hh, sd["head"], 24, INK, face=SERIF, lh=1.2, where=where))
        b, _ = lede_rows(sd["items"], x + pad, y + 0.3 + lh_ + 0.1 + hh + 0.25, iw, where, 18, 18, 0.22)
        els += b
    end = y + ph
    check_bottom(end, where, note_space(s))
    return els + place_note(s, end, where)


def lay_lawstep(s, idx, deck):
    """The law on the left (rule-separated points); how Handoff handles it in a panel on the right."""
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    rw = 3.9
    lw_ = CW - rw - 0.55
    e, lh_ = label(ML, y, lw_, s.get("law_label", "What the law requires"), MUTED, 12, where)
    els.append(e)
    b, end = lede_rows(s["items"], ML, y + lh_ + 0.2, lw_, where, 18, 18, 0.24)
    els += b
    rx = W - ML - rw
    pad = 0.3
    hb = s["handoff"] if isinstance(s["handoff"], list) else [s["handoff"]]
    hh = text_h(hb, 18, rw - 2 * pad, gap=10)
    ph = 0.3 + 12 * LH_BODY / 72 + 0.18 + hh + 0.3
    ph = max(ph, end - y)
    els.append(R(rx, y, rw, ph, fill=PANEL))
    els.append(R(rx, y, rw, 0.06, fill=ACCENT))
    e, lh2 = label(rx + pad, y + 0.3, rw - 2 * pad, "How Handoff handles it", ACCENT, 12, where)
    els.append(e)
    els.append(T(rx + pad, y + 0.3 + lh2 + 0.18, rw - 2 * pad, hh, hb, 18, INK, gap=10, where=where))
    bottom = max(end, y + ph)
    check_bottom(bottom, where, note_space(s))
    return els + place_note(s, bottom, where)


def lay_split(s, idx, deck):
    """Two lists: allowed (accent marker) and not allowed (neutral marker)."""
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    sides = s["sides"]
    gap = 0.6
    ws = s.get("widths", [1, 1])
    cws = [(CW - gap) * w / sum(ws) for w in ws]
    x = ML
    ends = []
    for i, (sd, cw) in enumerate(zip(sides, cws)):
        yes = i == 0
        e, lh_ = label(x, y, cw, sd["label"], ACCENT if yes else INK, 12, where)
        els.append(e)
        yy = y + lh_ + 0.12
        els.append(L(x, yy, x + cw, yy, ACCENT if yes else INK, 1.5))
        yy += 0.2
        per_col = sd.get("ncol", 1)
        cgap = 0.4
        icw = (cw - cgap * (per_col - 1)) / per_col
        cy = yy
        its = sd["items"]
        for r0 in range(0, len(its), per_col):
            row = its[r0:r0 + per_col]
            hs = [text_h(it, 18, icw - 0.42) for it in row]
            for c, it in enumerate(row):
                cx = x + c * (icw + cgap)
                mid = cy + 18 * LH_BODY / 72 / 2
                if yes:
                    els.append(O(cx, mid - 0.09, 0.18, fill=ACCENT))
                else:
                    els.append(O(cx, mid - 0.09, 0.18, fill=WHITE, line=INK, lw=1.25))
                    els.append(L(cx + 0.045, mid, cx + 0.135, mid, INK, 1.25))
                els.append(T(cx + 0.42, cy, icw - 0.42, hs[c], it, 18, INK, where=where))
            cy += max(hs) + 0.2
        ends.append(cy - 0.2)
        x += cw + gap
    end = max(ends)
    check_bottom(end, where, note_space(s))
    return els + place_note(s, end, where)


def lay_journey(s, idx, deck):
    """Numbered steps on a line, each with a short name and one line of text."""
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    steps = s["steps"]
    n = len(steps)
    gap = 0.3
    cw = (CW - gap * (n - 1)) / n
    d = 0.56
    cy = y + 0.1
    els.append(L(ML + d / 2, cy + d / 2, ML + (n - 1) * (cw + gap) + d / 2, cy + d / 2, RULE, 1.5))
    nh = max(text_h(st[0], 20, cw, True) for st in steps)
    th = max(text_h(st[1], 18, cw - 0.05) for st in steps)
    for i, (name, txt) in enumerate(steps):
        x = ML + i * (cw + gap)
        els.append(O(x, cy, d, fill=ACCENT if s.get("hl") == i else INK))
        els.append(T(x, cy, d, d, str(i + 1), 20, WHITE, True, align="center", valign="middle", lh=1.0,
                     where=where))
        els.append(T(x, cy + d + 0.3, cw, nh, name, 20, INK, True, where=where))
        els.append(T(x, cy + d + 0.3 + nh + 0.1, cw - 0.05, th, txt, 18, TEXT2, where=where))
    end = cy + d + 0.3 + nh + 0.1 + th
    check_bottom(end, where, note_space(s))
    return els + place_note(s, end, where)


def lay_decision(s, idx, deck):
    """Two yes/no questions in sequence, each with an exit to the right."""
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    qs = s["questions"]
    qw, ew = 5.4, 5.3
    ex = W - ML - ew
    for i, q in enumerate(qs):
        qh = max(text_h(q["q"], 20, qw - 0.5, True) + 0.36, text_h(q["exit"], 18, ew - 0.5) + 0.36, 0.8)
        eh_ = qh
        els.append(R(ML, y, qw, qh, fill=INK, radius=0.05))
        els.append(T(ML + 0.25, y, qw - 0.5, qh, q["q"], 20, WHITE, True, valign="middle", where=where))
        style = q.get("exit_style", "plain")
        els.append(draw_box(ex, y + (qh - eh_) / 2, ew, eh_, style, 0.05))
        els.append(T(ex + 0.25, y + (qh - eh_) / 2, ew - 0.5, eh_, q["exit"], 18, box_text_color(style),
                     valign="middle", where=where))
        els.append(L(ML + qw, y + qh / 2, ex - 0.03, y + qh / 2, ARROW, 2.0, arrow=True))
        els.append(T(ML + qw + 0.25, y + qh / 2 - 0.36, 1.5, 0.3, q.get("exit_label", "Yes"), 16, MUTED, True,
                     lh=1.2, where=where))
        y += qh
        if i < len(qs) - 1:
            els.append(L(ML + 0.6, y, ML + 0.6, y + 0.42, ARROW, 2.0, arrow=True))
            els.append(T(ML + 0.8, y + 0.07, 1.5, 0.3, q.get("next_label", "No"), 16, MUTED, True, lh=1.2,
                         where=where))
            y += 0.45
    if s.get("final"):
        els.append(L(ML + 0.6, y, ML + 0.6, y + 0.42, ARROW, 2.0, arrow=True))
        els.append(T(ML + 0.8, y + 0.07, 1.5, 0.3, qs[-1].get("next_label", "No"), 16, MUTED, True, lh=1.2,
                     where=where))
        y += 0.45
        fh = max(text_h(s["final"], 18, qw - 0.5) + 0.4, 0.7)
        els.append(draw_box(ML, y, qw, fh, "plain", 0.05))
        els.append(T(ML + 0.25, y, qw - 0.5, fh, s["final"], 18, INK, valign="middle", where=where))
        y += fh
    check_bottom(y, where, note_space(s))
    return els + place_note(s, y, where)


def lay_calendar(s, idx, deck):
    """A month grid with marked days, and rule-separated points on the right."""
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    import calendar as _cal
    yr, mo = s["month"]
    cw_, ch_ = 0.78, 0.56
    gx = ML
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, dname in enumerate(days):
        els.append(T(gx + i * cw_, y, cw_, 0.26, dname.upper(), 12, MUTED, True, align="center", track=TRACK,
                     where=where))
    yy = y + 0.36
    marks = s["marks"]            # day -> style: vacated, count, holiday, weekend, due, check
    counts = s.get("counts", {})  # day -> label under the number
    weeks = _cal.Calendar(0).monthdayscalendar(yr, mo)
    for wk in weeks:
        for i, d in enumerate(wk):
            x = gx + i * cw_
            if d == 0:
                continue
            st = marks.get(d)
            fill, line, col = None, None, (MUTED if i >= 5 else INK)
            if st == "vacated":
                fill, col = INK, WHITE
            elif st == "due":
                fill, col = ACCENT, WHITE
            elif st == "count":
                fill, col = COUNT, INK
            elif st == "skip":
                fill, line, col = WHITE, ACCENT, ACCENT
            elif st == "check":
                fill, line, col = WHITE, INK, INK
            if fill or line:
                els.append(R(x + 0.04, yy + 0.04, cw_ - 0.08, ch_ - 0.08, fill=fill, line=line, lw=1.5,
                             dash=st == "skip", radius=0.04))
            els.append(T(x + 0.04, yy + 0.07, cw_ - 0.08, 0.3, str(d), 16, col, st in ("vacated", "due", "skip"),
                         align="center", lh=1.2, where=where))
            if d in counts:
                els.append(T(x + 0.04, yy + 0.31, cw_ - 0.08, 0.22, counts[d], 11, col, align="center", lh=1.2,
                             where=where))
        yy += ch_
    grid_end = yy
    # legend under the grid
    lg_y = grid_end + 0.2
    for k, (st, text) in enumerate(s.get("legend", [])):
        lx = gx + (k % 2) * 2.7
        ly_ = lg_y + (k // 2) * 0.34
        fill = {"vacated": INK, "due": ACCENT, "count": COUNT, "skip": WHITE}[st]
        els.append(R(lx, ly_ + 0.05, 0.26, 0.2, fill=fill, line=ACCENT if st == "skip" else None, lw=1.25,
                     dash=st == "skip", radius=0.03))
        tw = text_w(text, 16) + 0.05
        els.append(T(lx + 0.38, ly_, tw, 0.3, text, 16, TEXT2, lh=1.2, where=where))
    lg_y += 0.34 * ((len(s.get("legend", [])) + 1) // 2 - 1)
    rx = gx + 7 * cw_ + 0.7
    rw = W - ML - rx
    b, end = lede_rows(s["items"], rx, y, rw, where, 18, 18, 0.24)
    els += b
    bottom = max(end, lg_y + 0.3)
    check_bottom(bottom, where, note_space(s))
    return els + place_note(s, bottom, where)


def lay_example(s, idx, deck):
    """Worked example: facts, the rule, the result, joined by arrows."""
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    cols = s["cols"]
    arrow = 0.5
    ws = s.get("widths", [1, 1, 1])
    avail = CW - arrow * (len(cols) - 1)
    cws = [avail * w / sum(ws) for w in ws]
    pad = 0.25
    bodies = [text_h(c["body"], 18, cw - 2 * pad, gap=10) for c, cw in zip(cols, cws)]
    ph = 0.3 + 12 * LH_BODY / 72 + 0.18 + max(bodies) + 0.3
    x = ML
    for i, (c, cw) in enumerate(zip(cols, cws)):
        last = i == len(cols) - 1
        els.append(R(x, y, cw, ph, fill=PANEL))
        els.append(R(x, y, cw, 0.06, fill=ACCENT if last else INK))
        e, lh_ = label(x + pad, y + 0.3, cw - 2 * pad, c["label"], ACCENT if last else MUTED, 12, where)
        els.append(e)
        bh = text_h(c["body"], 18, cw - 2 * pad, gap=10)
        els.append(T(x + pad, y + 0.3 + lh_ + 0.18, cw - 2 * pad, bh, c["body"], 18, INK, gap=10, where=where))
        if not last:
            ax = x + cw + 0.08
            els.append(L(ax, y + ph / 2, ax + arrow - 0.1, y + ph / 2, ARROW, 2.25, arrow=True))
        x += cw + arrow
    end = y + ph
    check_bottom(end, where, note_space(s))
    return els + place_note(s, end, where)


def lay_account(s, idx, deck):
    """One account line, with its four supporting parts below it."""
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    line_h = 0.72
    els.append(R(ML, y, CW, line_h, fill=INK, radius=0.05))
    els.append(T(ML + 0.3, y, CW - 3.0, line_h, s["line"], 22, WHITE, True, valign="middle", where=where))
    els.append(T(W - ML - 2.8, y, 2.5, line_h, s["amount"], 26, WHITE, True, align="right", valign="middle",
                 where=where))
    parts = s["parts"]
    n = len(parts)
    gap = 0.3
    cw = (CW - gap * (n - 1)) / n
    top = y + line_h + 0.4
    pad = 0.22
    bh = max(text_h(p[1], 18, cw - 2 * pad) for p in parts)
    ph = 0.28 + 12 * LH_BODY / 72 + 0.14 + bh + 0.28
    for i, (lab, body) in enumerate(parts):
        x = ML + i * (cw + gap)
        els.append(L(x + cw / 2, y + line_h, x + cw / 2, top, MUTED, 1.25))
        els.append(R(x, top, cw, ph, fill=PANEL))
        els.append(R(x, top, cw, 0.05, fill=ACCENT if i == s.get("hl", 2) else INK))
        e, lh_ = label(x + pad, top + 0.28, cw - 2 * pad, lab, ACCENT if i == s.get("hl", 2) else MUTED, 12, where)
        els.append(e)
        els.append(T(x + pad, top + 0.28 + lh_ + 0.14, cw - 2 * pad, bh, body, 18, INK, where=where))
    end = top + ph
    check_bottom(end, where, note_space(s))
    return els + place_note(s, end, where)


def lay_team(s, idx, deck):
    where = f"{deck['file']} slide {idx}"
    els, y = frame(s, idx, deck)
    people = s["people"]
    gap = 0.6
    cw = (CW - gap * (len(people) - 1)) / len(people)
    y = max(y + 0.2, (y + BOT) / 2 - 1.2)
    for i, p in enumerate(people):
        x = ML + i * (cw + gap)
        els.append(L(x, y, x + cw, y, RULE, 0.75))
        els.append(R(x, y - 0.02, 0.6, 0.04, fill=INK))
        els.append(T(x, y + 0.4, cw, 0.75, p["name"], 40, INK, face=SERIF, lh=1.15, where=where))
        els.append(T(x, y + 1.25, cw, 0.4, p["role"], 22, ACCENT, True, where=where))
        if p.get("text"):
            th = text_h(p["text"], 20, cw - 0.4)
            els.append(T(x, y + 1.85, cw - 0.4, th, p["text"], 20, TEXT2, where=where))
    return els


def lay_closing(s, idx, deck):
    """Dark closing slide: headline, two or three columns, and a closing question."""
    where = f"{deck['file']} slide {idx}"
    els = [R(ML, 0.95, 0.7, 0.07, fill=ACCENT)]
    e, _ = label(ML, 0.55, 6, s.get("kicker", ""), ONDARK, 12, where)
    els.append(e)
    if not s["title"].endswith((".", "?", "!")):
        s["title"] += "."
    hw = balanced_w(s["title"], 38, CW * 0.85, face=SERIF)
    hh = text_h(s["title"], 38, hw, face=SERIF, lh=1.12)
    els.append(T(ML, 1.25, hw, hh, s["title"], 38, WHITE, face=SERIF, lh=1.12, where=where))
    y = 1.25 + hh + 0.6
    cols = s["cols"]
    gap = 0.6
    cw = (CW - gap * (len(cols) - 1)) / len(cols)
    ends = []
    for i, c in enumerate(cols):
        x = ML + i * (cw + gap)
        els.append(L(x, y, x + cw, y, DARKRULE, 0.75))
        e, lh_ = label(x, y + 0.2, cw, c["label"], ONDARK, 12, where)
        els.append(e)
        bh = text_h(c["body"], 20, cw, gap=10)
        els.append(T(x, y + 0.2 + lh_ + 0.15, cw, bh, c["body"], 20, WHITE, gap=10, where=where))
        ends.append(y + 0.2 + lh_ + 0.15 + bh)
    end = max(ends)
    if s.get("question"):
        qh = text_h(s["question"], 26, CW, face=SERIF, lh=1.2)
        top = max(end + 0.7, 5.3)
        els.append(T(ML, top, CW, qh, s["question"], 26, ACCENT_ON_DARK, face=SERIF, lh=1.2, where=where))
        end = top + qh
    check_bottom(end, where, 6.6)
    els += footer(s, idx, deck, where, dark=True)
    return els


ACCENT_ON_DARK = "F08A5D"   # the accent, lightened for contrast on the dark background

LAYOUTS = {
    "title": lay_title, "divider": lay_divider, "findings": lay_findings, "stats": lay_stats,
    "bignum": lay_bignum, "list": lay_list, "columns": lay_columns, "flow": lay_flow, "layers": lay_layers,
    "timeline": lay_timeline, "table": lay_table, "bars": lay_bars, "compare": lay_compare,
    "bars2": lay_bars_shared,
    "lawstep": lay_lawstep, "split": lay_split, "journey": lay_journey, "decision": lay_decision,
    "calendar": lay_calendar, "example": lay_example, "account": lay_account, "team": lay_team,
    "closing": lay_closing,
}
DARK_KINDS = {"title", "divider", "closing"}


# ---------------------------------------------------------------- PPTX renderer

def _strip_style(shape):
    st = shape._element.find(qn("p:style"))
    if st is not None:
        shape._element.remove(st)


def pptx_render(deck, slides_els, path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    blank = prs.slide_layouts[6]
    for s, els in zip(deck["slides"], slides_els):
        sl = prs.slides.add_slide(blank)
        bg = sl.background.fill
        bg.solid()
        bg.fore_color.rgb = RGBColor.from_string(DARK if s["kind"] in DARK_KINDS else PAPER)
        for e in els:
            k = e["k"]
            if k in ("rect", "oval"):
                if k == "rect":
                    kind = MSO_SHAPE.ROUNDED_RECTANGLE if e.get("radius") else MSO_SHAPE.RECTANGLE
                else:
                    kind = MSO_SHAPE.OVAL
                shp = sl.shapes.add_shape(kind, Inches(e["x"]), Inches(e["y"]), Inches(e["w"]), Inches(e["h"]))
                _strip_style(shp)
                if k == "rect" and e.get("radius"):
                    shp.adjustments[0] = min(0.5, e["radius"] / min(e["w"], e["h"]))
                if e.get("fill"):
                    shp.fill.solid()
                    shp.fill.fore_color.rgb = RGBColor.from_string(e["fill"])
                else:
                    shp.fill.background()
                if e.get("line"):
                    shp.line.color.rgb = RGBColor.from_string(e["line"])
                    shp.line.width = Pt(e["lw"])
                    if e.get("dash"):
                        shp.line.dash_style = MSO_LINE.DASH
                else:
                    shp.line.fill.background()
            elif k == "line":
                c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(e["x1"]), Inches(e["y1"]),
                                            Inches(e["x2"]), Inches(e["y2"]))
                _strip_style(c)
                c.line.color.rgb = RGBColor.from_string(e["color"])
                c.line.width = Pt(e["lw"])
                if e.get("dash"):
                    c.line.dash_style = MSO_LINE.DASH
                if e.get("arrow"):
                    ln = c.line._get_or_add_ln()
                    tail = etree.SubElement(ln, qn("a:tailEnd"))
                    tail.set("type", "triangle")
                    tail.set("w", "med")
                    tail.set("len", "med")
            elif k == "text":
                tb = sl.shapes.add_textbox(Inches(e["x"]), Inches(e["y"]), Inches(e["w"]), Inches(e["h"]))
                tf = tb.text_frame
                tf.word_wrap = True
                tf.auto_size = MSO_AUTO_SIZE.NONE
                tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
                tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE,
                                      "bottom": MSO_ANCHOR.BOTTOM}[e["valign"]]
                for i, para in enumerate(e["paras"]):
                    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                    p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER,
                                   "right": PP_ALIGN.RIGHT}[e["align"]]
                    p.line_spacing = Pt(e["size"] * e["lh"])
                    if i < len(e["paras"]) - 1 and e["gap"]:
                        p.space_after = Pt(e["gap"])
                    for txt, b in runs(para):
                        r = p.add_run()
                        r.text = txt
                        f = r.font
                        f.name = e["face"]
                        f.size = Pt(e["size"])
                        f.bold = b or e["bold"]
                        f.color.rgb = RGBColor.from_string(e["color"])
                        if e["track"]:
                            r._r.get_or_add_rPr().set("spc", str(int(round(e["size"] * e["track"] * 100))))
        notes = s.get("notes") or s.get("src")
        if notes:
            sl.notes_slide.notes_text_frame.text = notes
    prs.save(path)


# ---------------------------------------------------------------- HTML / PDF renderer

PX = 96  # svg px per inch


def html_render(deck, slides_els, path):
    parts = ["""<!doctype html><html><head><meta charset="utf-8"><style>
@page { size: 13.333in 7.5in; margin: 0 }
html, body { margin: 0; padding: 0 }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; box-sizing: border-box }
.s { position: relative; width: 13.333in; height: 7.5in; overflow: hidden; break-after: page }
.s:last-child { break-after: auto }
.t { position: absolute; display: flex; flex-direction: column; font-kerning: normal }
.t p { margin: 0 }
svg { position: absolute; left: 0; top: 0 }
</style></head><body>"""]
    for s, els in zip(deck["slides"], slides_els):
        bg = DARK if s["kind"] in DARK_KINDS else PAPER
        svg = [f'<svg width="13.333in" height="7.5in" viewBox="0 0 {W * PX:.1f} {H * PX:.1f}">'
               '<defs>'
               f'<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
               f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#{ARROW}"/></marker></defs>']
        texts = []
        for e in els:
            k = e["k"]
            if k == "rect":
                fill = f'#{e["fill"]}' if e.get("fill") else "none"
                stroke = f'stroke="#{e["line"]}" stroke-width="{e["lw"] * PX / 72:.2f}"' if e.get("line") else ""
                dash = ' stroke-dasharray="6,4"' if e.get("dash") else ""
                rr = e.get("radius", 0) * PX
                svg.append(f'<rect x="{e["x"] * PX:.2f}" y="{e["y"] * PX:.2f}" width="{e["w"] * PX:.2f}" '
                           f'height="{e["h"] * PX:.2f}" rx="{rr:.2f}" fill="{fill}" {stroke}{dash}/>')
            elif k == "oval":
                r = e["w"] * PX / 2
                fill = f'#{e["fill"]}' if e.get("fill") else "none"
                stroke = f'stroke="#{e["line"]}" stroke-width="{e["lw"] * PX / 72:.2f}"' if e.get("line") else ""
                svg.append(f'<circle cx="{e["x"] * PX + r:.2f}" cy="{e["y"] * PX + r:.2f}" r="{r:.2f}" '
                           f'fill="{fill}" {stroke}/>')
            elif k == "line":
                dash = ' stroke-dasharray="6,4"' if e.get("dash") else ""
                mk = ' marker-end="url(#ah)"' if e.get("arrow") else ""
                svg.append(f'<line x1="{e["x1"] * PX:.2f}" y1="{e["y1"] * PX:.2f}" x2="{e["x2"] * PX:.2f}" '
                           f'y2="{e["y2"] * PX:.2f}" stroke="#{e["color"]}" '
                           f'stroke-width="{e["lw"] * PX / 72:.2f}"{dash}{mk}/>')
            elif k == "text":
                jc = {"top": "flex-start", "middle": "center", "bottom": "flex-end"}[e["valign"]]
                ps = []
                for i, para in enumerate(e["paras"]):
                    inner = "".join(
                        f"<b>{html.escape(t)}</b>" if (b and not e["bold"]) else html.escape(t)
                        for t, b in runs(para))
                    mb = f"margin-bottom:{e['gap']}pt;" if i < len(e["paras"]) - 1 and e["gap"] else ""
                    ps.append(f'<p style="{mb}">{inner}</p>')
                fam = "Georgia, serif" if e["face"] == SERIF else "Arial, Helvetica, sans-serif"
                trk = f"letter-spacing:{e['track']}em;" if e["track"] else ""
                style = (f'left:{e["x"]}in;top:{e["y"]}in;width:{e["w"]}in;height:{e["h"]}in;font-family:{fam};'
                         f'font-size:{e["size"]}pt;line-height:{e["size"] * e["lh"]:.2f}pt;color:#{e["color"]};'
                         f'font-weight:{"700" if e["bold"] else "400"};text-align:{e["align"]};{trk}'
                         f'justify-content:{jc}')
                texts.append(f'<div class="t" style="{style}">{"".join(ps)}</div>')
        svg.append("</svg>")
        parts.append(f'<section class="s" style="background:#{bg}">' + "".join(svg) + "".join(texts) +
                     "</section>")
    parts.append("</body></html>")
    path.write_text("".join(parts), encoding="utf-8")


def pdf_render(html_path, pdf_path):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}", html_path.as_uri()],
                   check=True, capture_output=True, timeout=120)


# ---------------------------------------------------------------- main

def layout(name):
    deck = content.DECKS[name]
    deck = dict(deck, file=name)
    return deck, [LAYOUTS[s["kind"]](s, i, deck) for i, s in enumerate(deck["slides"], 1)]


def build(name):
    deck, slides_els = layout(name)
    pptx_render(deck, slides_els, OUT / f"{name}.pptx")
    html_path = HERE / "html" / f"{name}.html"
    html_path.parent.mkdir(exist_ok=True)
    html_render(deck, slides_els, html_path)
    pdf_render(html_path, OUT / f"{name}.pdf")
    print(f"{name}: {len(slides_els)} slides")
    return len(slides_els)


if __name__ == "__main__":
    args = sys.argv[1:]
    check_only = "--check" in args
    names = [a for a in args if not a.startswith("--")] or list(content.DECKS)
    errors = []
    for n in names:
        try:
            if check_only:
                deck = dict(content.DECKS[n], file=n)
                bad = 0
                for i, sl in enumerate(deck["slides"], 1):
                    try:
                        LAYOUTS[sl["kind"]](sl, i, deck)
                    except FitError as ex:
                        bad += 1
                        errors.append(f"{n}: {ex}")
                print(f"{n}: {len(deck['slides'])} slides, {bad} failing")
            else:
                build(n)
        except FitError as ex:
            errors.append(f"{n}: {ex}")
    for e in errors:
        print("FIT ERROR", e)
    sys.exit(1 if errors else 0)
