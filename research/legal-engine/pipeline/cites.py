"""Citation normalization for match (code only, no model). Generalized from register/tools/cites.py.

Each jurisdiction's profile.json declares how its law is cited, under "citations":
  order            integer; patterns of lower order are tried first (the NY family keeps the legacy order)
  patterns         [{prefix, key, number, plain_range, titled}]
                   prefix: regex for the instrument's name as rules write it ('GOL|General Obligations Law');
                   key: the normalized family key ('GOL'; with titled=true a format such as '{} NYCRR' filled by
                   the prefix's first group); number: 'HY' (7-108, 20-699.20), 'PLAIN' (235-e, 1801-A) or a regex;
                   plain_range: expand integer ranges ('RPL 215-216').
  special          [{regex, emit: [key, number]}]   read on the raw text before subdivisions are dropped
  continuation_stop [regex]  a bare number after ',' is not a continuation when this follows it ('; 7 CFR 3560')
  instrument_map   [{key | key_regex, instrument, lead_from, lead_to, startswith, part, group_in}]
  label_aliases    {section-id label: key}  e.g. 'Judiciary Law' -> 'JUD'
  file_strip       [regex]  removed from source-file names before file_patterns
  file_patterns    [{regex, key, number, key_map, require_dot}]  cite from a saved source file's name
  provision_special [{regex, requires, emit}]  extra citation when the provision matches and names `requires`

The rules the engine applies: parenthesized subdivisions are dropped ('GOL 7-108(1-a)(e)' -> GOL 7-108); a bare
number after ',', ';', '/', 'and' or 'or' inherits the previous prefix; integer ranges are expanded for
plain-numbered instruments; section numbers are upper-cased.
"""
from __future__ import annotations

import re

from . import core

HY = r"\d+-\d+(?:\.\d+)?"
PLAIN = r"\d+(?:-[A-Za-z]{1,5})?(?!\d)"
NUMBERS = {"HY": HY, "PLAIN": PLAIN}
SEP = r"(?:\s*[,;/]\s*|\s+and\s+|\s+or\s+|\s*,\s*and\s+)+"


def _strip(text):
    t = text or ""
    for _ in range(3):
        t = re.sub(r"\([^()]*\)", "", t)
    t = t.replace("§", " ").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", t)


class Engine:
    """Citation parser built from one or more jurisdictions' citation configs."""

    def __init__(self, configs):
        configs = sorted(configs, key=lambda c: c.get("order", 100))
        self.specs, self.special, self.stops, self.imap = [], [], [], []
        self.aliases, self.file_strip, self.file_patterns, self.prov_special = {}, [], [], []
        plain, titled = [], []
        for c in configs:
            for p in c.get("patterns", []):
                (titled if p.get("titled") else plain).append(p)
            self.special += [(re.compile(s["regex"]), tuple(s["emit"])) for s in c.get("special", [])]
            self.stops += c.get("continuation_stop", [])
            self.imap += c.get("instrument_map", [])
            self.aliases.update(c.get("label_aliases", {}))
            self.file_strip += c.get("file_strip", [])
            self.file_patterns += c.get("file_patterns", [])
            self.prov_special += c.get("provision_special", [])
        self.plain_keys = {p["key"] for p in plain + titled if p.get("plain_range")}
        for p in plain:
            num = NUMBERS.get(p["number"], p["number"])
            rx = re.compile(r"(?<![A-Za-z])" + p["prefix"] + r"\s*(?:art\.\s*[\w-]+\s*,?\s*)?(?:§+\s*)?(" + num + r")")
            self.specs.append((rx, p["key"], num, False))
        for p in titled:
            num = NUMBERS.get(p["number"], p["number"])
            self.specs.append((re.compile(r"(?<![\w.])" + p["prefix"] + r"(" + num + r")"), p["key"], num, True))
        self.stop_rx = re.compile(r"\s*(?:" + "|".join(self.stops) + r")") if self.stops else None

    def parse(self, text):
        out = []
        for rx, emit in self.special:
            if rx.search(text or ""):
                out.append(emit)
        t = _strip(text)
        taken = []
        for rx, key, num, titled in self.specs:
            for m in rx.finditer(t):
                if any(a <= m.start() < b for a, b in taken):
                    continue
                k = key.format(m.group(1)) if titled else key
                n = m.group(2) if titled else m.group(1)
                end = m.end()
                nums = [n]
                mr = re.match(r"-(\d+)(?![\d.-])", t[end:])
                if key in self.plain_keys and mr and re.fullmatch(r"\d+", n) and int(mr.group(1)) > int(n) \
                        and int(mr.group(1)) - int(n) < 60:
                    nums = [f"RANGE:{n}:{mr.group(1)}"]
                    end += mr.end()
                cont = re.compile(SEP + r"(" + num + r")(?![\w.])")
                while True:
                    mc = cont.match(t, end)
                    if not mc:
                        break
                    if self.stop_rx and self.stop_rx.match(t[mc.end():]):
                        break
                    nums.append(mc.group(1))
                    end = mc.end()
                taken.append((m.start(), end))
                for x in nums:
                    out.append((k, x.upper().replace(" NOTE", " note")))
        return out

    def provision_extra(self, provision, instrument):
        out = []
        for s in self.prov_special:
            if re.search(s["regex"], provision or "", re.I) and s.get("requires", "") in (provision or "") + (instrument or ""):
                out.append(tuple(s["emit"]))
        return out

    def source_file_cite(self, path):
        if not path:
            return None
        n = re.sub(r"^.*/", "", path)
        n = re.sub(r"\.txt$", "", n)
        for rx in self.file_strip:
            n = re.sub(rx, "", n, flags=re.I)
        for fp in self.file_patterns:
            m = re.match(fp["regex"], n)
            if not m:
                continue
            g = [m.group(0)] + list(m.groups())
            if fp.get("key_map") is not None:
                if g[1] not in fp["key_map"]:
                    continue
                key = fp["key_map"][g[1]]
            else:
                key = fp["key"].format(*g)
            if fp.get("require_dot") and "." not in g[fp["require_dot"]]:
                continue
            num = fp["number"].format(*g)
            return (key, num if fp.get("keep_case") else num.upper())
        return None

    def section_key(self, section_id):
        """'NY:GOL 7-108' -> ('GOL', '7-108'); 'NYC:RCNY 6 5-77' -> ('RCNY 6', '5-77'); 'US:12 USC 5220 note'."""
        rest = section_id.split(":", 1)[1]
        if rest.endswith(" note"):
            lab, num = rest[:-5].rsplit(" ", 1)
            num += " note"
        else:
            lab, num = rest.rsplit(" ", 1)
        num = num.split("@")[0].replace("–", "-").replace("—", "-").upper().replace(" NOTE", " note")
        return (self.aliases.get(lab, lab), num)

    def cite_instrument(self, key, num):
        """Registered instrument id for a citation, whether or not its unit is in scope; None if unknown."""
        lead_m = re.match(r"\d+", num or "")
        lead = int(lead_m.group()) if lead_m else -1
        for e in self.imap:
            g = [key]
            if "key" in e and e["key"] != key:
                continue
            if "key_regex" in e:
                m = re.match(e["key_regex"], key)
                if not m:
                    continue
                g = [m.group(0)] + list(m.groups())
                if "group_in" in e and g[1] not in e["group_in"]:
                    continue
            if "lead_from" in e and not (e["lead_from"] <= lead <= e["lead_to"]):
                continue
            if "startswith" in e and not (num or "").upper().startswith(e["startswith"].upper()):
                continue
            if "part" in e and (num or "").split(".")[0] != e["part"]:
                continue
            if e.get("instrument") is None:
                return None
            return e["instrument"].format(*g)
        return None


_cache = {}


def engine(codes_=None):
    """Engine over the given jurisdictions (default: every jurisdiction in the workspace)."""
    codes_ = tuple(codes_ or core.codes())
    key = (str(core.ROOT), codes_, tuple(core.sha256_file(core.jdir(c) / "profile.json") for c in codes_))
    if key not in _cache:
        _cache[key] = Engine([core.profile(c).get("citations", {}) for c in codes_])
    return _cache[key]
