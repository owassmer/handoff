"""Citation normalization shared by match.py and check_register.py (no model; pure code).

parse(text) -> list of (key, number) where key names an instrument family ('GOL', 'RPL', '9 NYCRR', 'ADC',
'RCNY 6', '11 USC', '24 CFR', 'FRBP', ...) and number is the section number in upper case. Parenthesized
subdivisions and comments are dropped first ('GOL 7-108(1-a)(e)' -> ('GOL', '7-108')). A bare number after ',', ';',
'/', 'and' or 'or' inherits the previous prefix ('RPL 440(1), 440-a' -> RPL 440, RPL 440-A). 'A-B' ranges are
expanded for instruments whose section numbers are plain integers ('RPL 215-216', 'STT 304-305').
source_file_cite(path) -> (key, number) from saved-source file names like sources/REVIEW5A_NY_GBL_349.txt.
"""
import re

HY = r"\d+-\d+(?:\.\d+)?"            # 7-108, 20-699.20, 5-1103
PLAIN = r"\d+(?:-[A-Za-z]{1,5})?(?!\d)"  # 235-e, 604-aa, 1801-A
NY = [
    (r"(?:N\.?Y\.?\s+)?(?:GOL|General Obligations Law|Gen\.?\s*Oblig\.?\s*Law)", "GOL", HY, False),
    (r"(?:N\.?Y\.?\s+)?(?:RPAPL|Real Property Actions and Proceedings Law)", "RPAPL", PLAIN, True),
    (r"(?:N\.?Y\.?\s+)?(?:RPL|Real Property Law)", "RPL", PLAIN, True),
    (r"(?:N\.?Y\.?\s+)?(?:MDL|Multiple Dwelling Law)", "MDL", PLAIN, True),
    (r"(?:N\.?Y\.?\s+)?(?:CPLR|Civil Practice Law and Rules)", "CPLR", PLAIN, True),
    (r"(?:N\.?Y\.?\s+)?(?:GBL|General Business Law)", "GBL", PLAIN, True),
    (r"(?:N\.?Y\.?\s+)?(?:Judiciary Law|Jud\.?\s*Law)", "JUD", PLAIN, True),
    (r"(?:N\.?Y\.?\s+)?(?:UCC|Uniform Commercial Code)", "UCC", HY, False),
    (r"(?:N\.?Y\.?\s+)?(?:ABP|Abandoned Property Law)", "ABP", PLAIN, True),
    (r"(?:N\.?Y\.?\s+)?EPTL", "EPTL", r"\d+-\d+\.\d+", False),
    (r"(?:N\.?Y\.?\s+)?(?:Military Law|Mil\.?\s*Law)", "MIL", PLAIN, True),
    (r"(?:N\.?Y\.?\s+)?(?:Executive Law|Exec\.?\s*Law)", "EXEC", PLAIN, True),
    (r"(?:N\.?Y\.?\s+)?(?:LLC Law|Limited Liability Company Law)", "LLC", PLAIN, True),
    (r"(?:N\.?Y\.?\s+)?(?:BCL|Business Corporation Law)", "BCL", PLAIN, True),
    (r"(?:N-?PCL|Not-for-Profit Corporation Law)", "NPCL", PLAIN, True),
    (r"(?:N\.?Y\.?\s+)?(?:GCN|General Construction Law)", "GCN", PLAIN, True),
    (r"(?:N\.?Y\.?\s+)?(?:STT|State Technology Law)", "STT", PLAIN, True),
    (r"(?:N\.?Y\.?\s+)?(?:SSL|Social Services Law)", "SSL", PLAIN, True),
    (r"(?:DCL|Debtor and Creditor Law)", "DCL", PLAIN, True),
    (r"(?:NYC\s+|New York City\s+)?(?:CCA|Civil Court Act)", "CCA", PLAIN, True),
    (r"(?:SCPA|Surrogate.s Court Procedure Act)", "SCPA", PLAIN, True),
    (r"RSC", "9 NYCRR", r"25\d\d\.\d+", False),
    (r"(?:N\.?Y\.?\s+)?(?:MHL|Mental Hygiene Law)", "MHY", r"81\.\d+", False),
    (r"(?:N\.?Y\.?\s+)?(?:Partnership Law)", "PTR", r"\d+(?:-\d+)?(?:-[A-Za-z])?", False),
]
NYC = [
    (r"(?:NYC\s+)?(?:Admin(?:istrative)?\.?\s*Code|ADC|HMC)", "ADC", HY, False),
]
TITLED = [  # prefix with a title number captured as group 1
    (r"(\d+)\s*NYCRR\s*(?:Part\s*|part\s*|§+\s*)?", "{} NYCRR", r"\d+(?:\.\d+[a-z]?(?:-[a-z])?)?", False),
    (r"(\d+)\s*RCNY\s*(?:§+\s*)?", "RCNY {}", HY, False),
    (r"(\d+)\s*U\.?\s?S\.?\s?C\.?\s*(?:§+\s*)?", "{} USC", r"\d+[a-zA-Z]*(?:-\d+[a-zA-Z]?)?(?:\s+note)?", False),
    (r"(\d+)\s*C\.?\s?F\.?\s?R\.?\s*(?:§+\s*|part\s*|Part\s*)?", "{} CFR", r"\d+(?:\.\d+[a-z]?(?:-\d+)?)?", False),
]
FRBP = [(r"(?:FRBP|Fed\.?\s*R\.?\s*Bankr\.?\s*P\.?|Federal Rules? of Bankruptcy Procedure,?\s*(?:Rule)?)", "FRBP", r"\d{4}", False)]
PLAIN_KEYS = {k for _, k, _, p in NY if p}
SEP = r"(?:\s*[,;/]\s*|\s+and\s+|\s+or\s+|\s*,\s*and\s+)+"


def _strip(text):
    t = text or ""
    for _ in range(3):
        t = re.sub(r"\([^()]*\)", "", t)
    t = t.replace("§", " ").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", t)


def _specs():
    for pre, key, num, plain in NY + NYC + FRBP:
        yield re.compile(r"(?<![A-Za-z])" + pre + r"\s*(?:art\.\s*[\w-]+\s*,?\s*)?(?:§+\s*)?(" + num + r")"), key, num, plain, False
    for pre, key, num, plain in TITLED:
        yield re.compile(r"(?<![\w.])" + pre + r"(" + num + r")"), key, num, plain, True


SPECS = list(_specs())


def parse(text):
    out = []
    if re.search(r"12\s*U\.?\s?S\.?\s?C\.?\s*(?:§\s*)?5220\s+note|Protecting Tenants at Foreclosure", text or ""):
        out.append(("12 USC", "5220 note"))
    t = _strip(text)
    taken = []
    for rx, key, num, plain, titled in SPECS:
        for m in rx.finditer(t):
            if any(a <= m.start() < b for a, b in taken):
                continue
            k = key.format(m.group(1)) if titled else key
            n = m.group(2) if titled else m.group(1)
            end = m.end()
            nums = [n]
            # range A-B for plain-number instruments
            mr = re.match(r"-(\d+)(?![\d.-])", t[end:])
            if key in PLAIN_KEYS and mr and re.fullmatch(r"\d+", n) and int(mr.group(1)) > int(n) and int(mr.group(1)) - int(n) < 60:
                nums = [f"RANGE:{n}:{mr.group(1)}"]
                end += mr.end()
            cont = re.compile(SEP + r"(" + num + r")(?![\w.])")
            while True:
                mc = cont.match(t, end)
                if not mc:
                    break
                # a continuation must not be the start of another prefix (e.g. '; 7 CFR 3560')
                if re.match(r"\s*(?:U\.?\s?S\.?\s?C|C\.?\s?F\.?\s?R|NYCRR|RCNY)", t[mc.end():]):
                    break
                nums.append(mc.group(1))
                end = mc.end()
            taken.append((m.start(), end))
            for x in nums:
                out.append((k, x.upper().replace(" NOTE", " note")))
    return out


FILEMAP = {"GOL": "GOL", "RPL": "RPL", "RPAPL": "RPAPL", "MDL": "MDL", "CPLR": "CPLR", "GBL": "GBL", "GCN": "GCN",
           "ABP": "ABP", "MIL": "MIL", "CCA": "CCA", "JUD": "JUD", "STT": "STT", "BCL": "BCL", "LLC": "LLC",
           "EXEC": "EXEC", "EXC": "EXEC", "SCPA": "SCPA", "SSL": "SSL", "UCC": "UCC", "EPTL": "EPTL"}


def source_file_cite(path):
    if not path:
        return None
    n = re.sub(r"^.*/", "", path)
    n = re.sub(r"\.txt$", "", n)
    n = re.sub(r"^(REVIEW\d[AB]?_|SWEEP_)", "", n)
    n = re.sub(r"_(nysenate|justia|LII|uscode|ecfr|courtlistener|nycourts|ESIGN|TCPA|VAWA|NYCRR|current|official.*|live.*)$", "", n, flags=re.I)
    m = re.match(r"NY_(\d+)NYCRR_([\d.]+[a-z]?)$", n)
    if m:
        return (f"{m.group(1)} NYCRR", m.group(2).upper())
    m = re.match(r"NY_([A-Z]+)_([\dA-Za-z.\-]+)$", n)
    if m and m.group(1) in FILEMAP:
        return (FILEMAP[m.group(1)], m.group(2).upper())
    m = re.match(r"NYC_ADC_([\d\-.]+)$", n)
    if m:
        return ("ADC", m.group(1).upper())
    m = re.match(r"NYC_RCNY(\d+)_([\d\-.]+)$", n)
    if m:
        return (f"RCNY {m.group(1)}", m.group(2).upper())
    m = re.match(r"US_(\d+)USC_([\dA-Za-z\-]+)$", n)
    if m:
        return (f"{m.group(1)} USC", m.group(2).upper())
    m = re.match(r"US_(\d+)CFR_([\d.]+(?:-\d+)?)$", n)
    if m and "." in m.group(2):
        return (f"{m.group(1)} CFR", m.group(2).upper())
    m = re.match(r"US_FRBP_(\d+)$", n)
    if m:
        return ("FRBP", m.group(1))
    return None


def section_key(section_id):
    """'NY:GOL 7-108' -> ('GOL', '7-108'); 'NYC:RCNY 6 5-77' -> ('RCNY 6', '5-77'); 'US:12 USC 5220 note'."""
    j, rest = section_id.split(":", 1)
    if rest.endswith(" note"):
        lab, num = rest[:-5].rsplit(" ", 1)
        num += " note"
    else:
        lab, num = rest.rsplit(" ", 1)
    num = num.split("@")[0].replace("\u2013", "-").replace("\u2014", "-").upper().replace(" NOTE", " note")
    lab = {"Judiciary Law": "JUD", "Military Law": "MIL", "Executive Law": "EXEC", "LLC Law": "LLC", "N-PCL": "NPCL",
           "Partnership Law": "PTR", "MHL": "MHY"}.get(lab, lab)
    return (lab, num)


def cite_instrument(key, num):
    """Instrument id for a citation (whether or not its unit is in scope); None if the instrument is not registered."""
    ny = {"GOL", "RPL", "RPAPL", "MDL", "CPLR", "GBL", "JUD", "UCC", "ABP", "EPTL", "MIL", "EXEC", "LLC", "BCL", "NPCL",
          "GCN", "STT", "SSL", "DCL", "CCA", "SCPA", "PTR", "MHY"}
    if key in ny:
        return f"NY:{key}"
    m = re.match(r"(\d+) NYCRR$", key)
    if m:
        return f"NY:{m.group(1)}NYCRR" if m.group(1) in ("9", "16", "18", "19", "22", "23") else None
    if key == "ADC":
        return "NYC:ADC"
    if key.startswith("RCNY"):
        return "NYC:RCNY"
    if key == "FRBP":
        return "US:FRBP"
    m = re.match(r"(\d+) USC$", key)
    if m:
        t = m.group(1)
        lead = int(re.match(r"\d+", num).group()) if re.match(r"\d+", num) else -1
        if t == "11":
            return "US:11USC"
        if t == "15" and 1601 <= lead <= 1693:
            return "US:15USC-ch41"
        if t == "15" and 7001 <= lead <= 7031:
            return "US:15USC-ch96"
        if t == "42" and 3601 <= lead <= 3631:
            return "US:42USC-ch45"
        if t == "50" and 3901 <= lead <= 4043:
            return "US:50USC-ch50"
        if t == "47" and num.upper().startswith("227"):
            return "US:47USC227"
        if t == "26" and 6031 <= lead <= 6060:
            return "US:26USC-6041-6050"
        if t == "26" and lead == 166:
            return "US:26USC166"
        if t == "12" and num.startswith("5220"):
            return "US:12USC5220note"
        if t == "12" and 5481 <= lead <= 5603:
            return "US:12USC5481"
        if t == "34" and 12491 <= lead <= 12496:
            return "US:34USC-VAWA"
        return None
    m = re.match(r"(\d+) CFR$", key)
    if m:
        part = num.split(".")[0]
        iid = {"12": {"1006": "US:12CFR1006", "1022": "US:12CFR1022", "1005": "US:12CFR1005"},
               "24": {"100": "US:24CFR100", "982": "US:24CFR982", "5": "US:24CFR5", "966": "US:24CFR966",
                      "960": "US:24CFR960", "880": "US:24CFR880", "881": "US:24CFR881", "882": "US:24CFR882",
                      "883": "US:24CFR883", "884": "US:24CFR884", "886": "US:24CFR886", "891": "US:24CFR891",
                      "983": "US:24CFR983", "92": "US:24CFR92"},
               "47": {"64": "US:47CFR64L"}, "16": {"682": "US:16CFR682"}, "26": {"1": "US:26CFR1-info"}, "7": {"3560": "US:7CFR3560"}}
        return iid.get(m.group(1), {}).get(part)
    return None


if __name__ == "__main__":
    import sys
    for s in sys.argv[1:]:
        print(s, "->", parse(s))
