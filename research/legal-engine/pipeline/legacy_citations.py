"""Citation configs for the NY, NYC and US layers, ported pattern for pattern from register/tools/cites.py.
import-legacy writes each into the layer's profile.json under "citations"; tests check that the engine built from
them parses every rule provision exactly as the legacy module does."""

_NY = r"(?:N\.?Y\.?\s+)?"


def _p(prefix, key, number, plain_range):
    return {"prefix": prefix, "key": key, "number": number, "plain_range": plain_range, "titled": False}


NY = {
    "order": 1,
    "patterns": [
        _p(_NY + r"(?:GOL|General Obligations Law|Gen\.?\s*Oblig\.?\s*Law)", "GOL", "HY", False),
        _p(_NY + r"(?:RPAPL|Real Property Actions and Proceedings Law)", "RPAPL", "PLAIN", True),
        _p(_NY + r"(?:RPL|Real Property Law)", "RPL", "PLAIN", True),
        _p(_NY + r"(?:MDL|Multiple Dwelling Law)", "MDL", "PLAIN", True),
        _p(_NY + r"(?:CPLR|Civil Practice Law and Rules)", "CPLR", "PLAIN", True),
        _p(_NY + r"(?:GBL|General Business Law)", "GBL", "PLAIN", True),
        _p(_NY + r"(?:Judiciary Law|Jud\.?\s*Law)", "JUD", "PLAIN", True),
        _p(_NY + r"(?:UCC|Uniform Commercial Code)", "UCC", "HY", False),
        _p(_NY + r"(?:ABP|Abandoned Property Law)", "ABP", "PLAIN", True),
        _p(_NY + r"EPTL", "EPTL", r"\d+-\d+\.\d+", False),
        _p(_NY + r"(?:Military Law|Mil\.?\s*Law)", "MIL", "PLAIN", True),
        _p(_NY + r"(?:Executive Law|Exec\.?\s*Law)", "EXEC", "PLAIN", True),
        _p(_NY + r"(?:LLC Law|Limited Liability Company Law)", "LLC", "PLAIN", True),
        _p(_NY + r"(?:BCL|Business Corporation Law)", "BCL", "PLAIN", True),
        _p(r"(?:N-?PCL|Not-for-Profit Corporation Law)", "NPCL", "PLAIN", True),
        _p(_NY + r"(?:GCN|General Construction Law)", "GCN", "PLAIN", True),
        _p(_NY + r"(?:STT|State Technology Law)", "STT", "PLAIN", True),
        _p(_NY + r"(?:SSL|Social Services Law)", "SSL", "PLAIN", True),
        _p(r"(?:DCL|Debtor and Creditor Law)", "DCL", "PLAIN", True),
        _p(r"(?:NYC\s+|New York City\s+)?(?:CCA|Civil Court Act)", "CCA", "PLAIN", True),
        _p(r"(?:SCPA|Surrogate.s Court Procedure Act)", "SCPA", "PLAIN", True),
        _p(r"RSC", "9 NYCRR", r"25\d\d\.\d+", False),
        _p(_NY + r"(?:MHL|Mental Hygiene Law)", "MHY", r"81\.\d+", False),
        _p(_NY + r"(?:Partnership Law)", "PTR", r"\d+(?:-\d+)?(?:-[A-Za-z])?", False),
        {"prefix": r"(\d+)\s*NYCRR\s*(?:Part\s*|part\s*|§+\s*)?", "key": "{} NYCRR",
         "number": r"\d+(?:\.\d+[a-z]?(?:-[a-z])?)?", "plain_range": False, "titled": True},
    ],
    "continuation_stop": [r"NYCRR"],
    "instrument_map": [{"key": k, "instrument": "NY:" + k} for k in (
        "GOL", "RPL", "RPAPL", "MDL", "CPLR", "GBL", "JUD", "UCC", "ABP", "EPTL", "MIL", "EXEC", "LLC", "BCL", "NPCL",
        "GCN", "STT", "SSL", "DCL", "CCA", "SCPA", "PTR", "MHY")] + [
        {"key_regex": r"^(\d+) NYCRR$", "group_in": ["9", "16", "18", "19", "22", "23"], "instrument": "NY:{1}NYCRR"},
        {"key_regex": r"^(\d+) NYCRR$", "instrument": None}],
    "label_aliases": {"Judiciary Law": "JUD", "Military Law": "MIL", "Executive Law": "EXEC", "LLC Law": "LLC",
                      "N-PCL": "NPCL", "Partnership Law": "PTR", "MHL": "MHY"},
    "file_strip": [r"^(REVIEW\d[AB]?_|SWEEP_)",
                   r"_(nysenate|justia|LII|uscode|ecfr|courtlistener|nycourts|ESIGN|TCPA|VAWA|NYCRR|current|official.*|live.*)$"],
    "file_patterns": [
        {"regex": r"NY_(\d+)NYCRR_([\d.]+[a-z]?)$", "key": "{1} NYCRR", "number": "{2}"},
        {"regex": r"NY_([A-Z]+)_([\dA-Za-z.\-]+)$", "key_map": {
            "GOL": "GOL", "RPL": "RPL", "RPAPL": "RPAPL", "MDL": "MDL", "CPLR": "CPLR", "GBL": "GBL", "GCN": "GCN",
            "ABP": "ABP", "MIL": "MIL", "CCA": "CCA", "JUD": "JUD", "STT": "STT", "BCL": "BCL", "LLC": "LLC",
            "EXEC": "EXEC", "EXC": "EXEC", "SCPA": "SCPA", "SSL": "SSL", "UCC": "UCC", "EPTL": "EPTL"},
         "number": "{2}"},
    ],
}

NYC = {
    "order": 2,
    "patterns": [
        _p(r"(?:NYC\s+)?(?:Admin(?:istrative)?\.?\s*Code|ADC|HMC)", "ADC", "HY", False),
        {"prefix": r"(\d+)\s*RCNY\s*(?:§+\s*)?", "key": "RCNY {}", "number": "HY", "plain_range": False,
         "titled": True},
    ],
    "continuation_stop": [r"RCNY"],
    "instrument_map": [{"key": "ADC", "instrument": "NYC:ADC"}, {"key_regex": r"^RCNY", "instrument": "NYC:RCNY"}],
    "file_patterns": [
        {"regex": r"NYC_ADC_([\d\-.]+)$", "key": "ADC", "number": "{1}"},
        {"regex": r"NYC_RCNY(\d+)_([\d\-.]+)$", "key": "RCNY {1}", "number": "{2}"},
    ],
}

_USC_RANGES = [("15", 1601, 1693, "US:15USC-ch41"), ("15", 7001, 7031, "US:15USC-ch96"),
               ("42", 3601, 3631, "US:42USC-ch45"), ("50", 3901, 4043, "US:50USC-ch50")]
US = {
    "order": 3,
    "patterns": [
        _p(r"(?:FRBP|Fed\.?\s*R\.?\s*Bankr\.?\s*P\.?|Federal Rules? of Bankruptcy Procedure,?\s*(?:Rule)?)", "FRBP",
           r"\d{4}", False),
        {"prefix": r"(\d+)\s*U\.?\s?S\.?\s?C\.?\s*(?:§+\s*)?", "key": "{} USC",
         "number": r"\d+[a-zA-Z]*(?:-\d+[a-zA-Z]?)?(?:\s+note)?", "plain_range": False, "titled": True},
        {"prefix": r"(\d+)\s*C\.?\s?F\.?\s?R\.?\s*(?:§+\s*|part\s*|Part\s*)?", "key": "{} CFR",
         "number": r"\d+(?:\.\d+[a-z]?(?:-\d+)?)?", "plain_range": False, "titled": True},
    ],
    "special": [{"regex": r"12\s*U\.?\s?S\.?\s?C\.?\s*(?:§\s*)?5220\s+note|Protecting Tenants at Foreclosure",
                 "emit": ["12 USC", "5220 note"]}],
    "continuation_stop": [r"U\.?\s?S\.?\s?C", r"C\.?\s?F\.?\s?R"],
    "provision_special": [{"regex": r"\bcomments?\s+\d", "requires": "1006",
                           "emit": ["12 CFR", "SUPPLEMENT_I_TO_PART_1006"]}],
    "instrument_map": [{"key": "FRBP", "instrument": "US:FRBP"}, {"key": "11 USC", "instrument": "US:11USC"}]
    + [{"key": f"{t} USC", "lead_from": a, "lead_to": b, "instrument": i} for t, a, b, i in _USC_RANGES]
    + [{"key": "47 USC", "startswith": "227", "instrument": "US:47USC227"},
       {"key": "26 USC", "lead_from": 6031, "lead_to": 6060, "instrument": "US:26USC-6041-6050"},
       {"key": "26 USC", "lead_from": 166, "lead_to": 166, "instrument": "US:26USC166"},
       {"key": "12 USC", "startswith": "5220", "instrument": "US:12USC5220note"},
       {"key": "12 USC", "lead_from": 5481, "lead_to": 5603, "instrument": "US:12USC5481"},
       {"key": "34 USC", "lead_from": 12491, "lead_to": 12496, "instrument": "US:34USC-VAWA"}]
    + [{"key": f"{t} CFR", "part": p, "instrument": i} for t, p, i in (
        ("12", "1006", "US:12CFR1006"), ("12", "1022", "US:12CFR1022"), ("12", "1005", "US:12CFR1005"),
        ("24", "100", "US:24CFR100"), ("24", "982", "US:24CFR982"), ("24", "5", "US:24CFR5"),
        ("24", "966", "US:24CFR966"), ("24", "960", "US:24CFR960"), ("24", "880", "US:24CFR880"),
        ("24", "881", "US:24CFR881"), ("24", "882", "US:24CFR882"), ("24", "883", "US:24CFR883"),
        ("24", "884", "US:24CFR884"), ("24", "886", "US:24CFR886"), ("24", "891", "US:24CFR891"),
        ("24", "983", "US:24CFR983"), ("24", "92", "US:24CFR92"), ("47", "64", "US:47CFR64L"),
        ("26", "1", "US:26CFR1-info"), ("7", "3560", "US:7CFR3560"), ("16", "682", "US:16CFR682"))],
    "file_patterns": [
        {"regex": r"US_(\d+)USC_([\dA-Za-z\-]+)$", "key": "{1} USC", "number": "{2}"},
        {"regex": r"US_(\d+)CFR_([\d.]+(?:-\d+)?)$", "key": "{1} CFR", "number": "{2}", "require_dot": 2},
        {"regex": r"US_FRBP_(\d+)$", "key": "FRBP", "number": "{1}"},
    ],
}

CONFIGS = {"NY": NY, "NYC": NYC, "US": US}
