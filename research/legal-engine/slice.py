"""A SAMPLE of 20 atoms from three sections, used to test the method's shape. It is not Stage A and is not
the representation of the law: STAGE_A.md owns the scope and lists what this sample gets wrong (NY 7-107 routing,
NY 7-103 trust and interest, time computation, VA move-in report, applicability, and skipped subsections).

Original description: the move-out deposit settlement chain in NY, CA and VA, atomized in CORDON's
stage format (A: legal meaning; B: clocks and parameters; C: evaluators; D: evidence contracts).

Not a legal product and not legal advice. It exists to test whether the method holds on this domain:
  - every atom carries a verbatim source quote, checked against the saved statute text (fails if not found);
  - rules and standards are typed separately (Nay: rules compile; standards need judgment);
  - dependencies the text does not resolve are recorded as bounded unknowns, never filled.

Sources (retrieved 2026-09-28, saved under sources/):
  NY General Obligations Law 7-108 (nysenate.gov), CA Civil Code 1950.5 (leginfo), VA Code 55.1-1226 (law.lis.virginia.gov).
"""
import datetime as dt
import json
import pathlib
import re

SRC = pathlib.Path(__file__).parent / "sources"
TEXT = {k: re.sub(r"\s+", " ", (SRC / f).read_text()) for k, f in
        {"NY": "NY_GOL_7-108.txt", "CA": "CA_CIV_1950.5.txt", "VA": "VA_55.1-1226.txt"}.items()}

# ---------------------------------------------------------------- Stage A: atoms of legal meaning
# determinacy: RULE (code decides), STANDARD (judgment: agent/Jev reading, operator accepts), MIXED.
ATOMS = [
    # New York
    dict(id="NY:7-108(1-a)(e)", state="NY", actor="landlord", modality="shall", determinacy="RULE",
         effect="Provide an itemized statement of the basis for any amount retained and return the remainder.",
         quote="Within fourteen days after the tenant has vacated the premises, the landlord shall provide the tenant with an itemized statement indicating the basis for the amount of the deposit retained, if any, and shall return any remaining portion of the deposit to the tenant."),
    dict(id="NY:7-108(1-a)(e)-forfeit", state="NY", actor="landlord", modality="consequence", determinacy="RULE",
         effect="Missing the 14-day statement and return forfeits any right to retain. No intent element.",
         quote="If a landlord fails to provide the tenant with the statement and deposit within fourteen days, the landlord shall forfeit any right to retain any portion of the deposit."),
    dict(id="NY:7-108(1-a)(b)", state="NY", actor="landlord", modality="may retain only", determinacy="STANDARD",
         effect="Retention limited to reasonable, itemized costs in four heads; never ordinary wear and tear or a prior tenant's damage.",
         judgment=["reasonable costs", "beyond normal wear and tear", "damage caused by a prior tenant"],
         quote="The landlord may not retain any amount of the deposit for costs relating to ordinary wear and tear of occupancy or damage caused by a prior tenant."),
    dict(id="NY:7-108(1-a)(c)", state="NY", actor="landlord", modality="shall offer", determinacy="MIXED",
         effect="Move-in inspection offer; conditions noted in the signed move-in agreement can never be deducted at move-out.",
         cross_time="move-in record governs move-out deductions",
         quote="Upon the tenant's vacating of the premises, the landlord may not retain any amount of the deposit or advance due to any condition, defect, or damage noted in such agreement."),
    dict(id="NY:7-108(1-a)(d)", state="NY", actor="landlord", modality="shall", determinacy="MIXED",
         effect="Notify of the pre-move-out inspection right; if requested, inspect 1-2 weeks before the end, on 48 hours' notice, itemize, allow cure.",
         judgment=["within a reasonable time after notification"],
         quote="If the tenant requests such an inspection, the inspection shall be made no earlier than two weeks and no later than one week before the end of the tenancy."),
    dict(id="NY:7-108(1-a)(f)", state="NY", actor="landlord", modality="burden", determinacy="RULE",
         effect="In any dispute the landlord bears the burden of proving the retention reasonable.",
         quote="the landlord shall bear the burden of proof as to the reasonableness of the amount retained."),
    dict(id="NY:7-108(1-a)(g)", state="NY", actor="landlord", modality="liability", determinacy="MIXED",
         effect="Actual damages for any violation; punitive up to twice the deposit if willful.",
         judgment=["willfully violated"],
         quote="a person found to have willfully violated this subdivision shall be liable for punitive damages of up to twice the amount of the deposit or advance."),
    # California
    dict(id="CA:1950.5(h)(1)", state="CA", actor="landlord", modality="shall", determinacy="RULE",
         effect="Itemized statement and return of the remainder no later than 21 calendar days after the tenant vacates.",
         quote="No later than 21 calendar days after the tenant has vacated the premises"),
    dict(id="CA:1950.5(h)(2)(D)", state="CA", actor="landlord", modality="shall", determinacy="RULE",
         effect="A repair or cleaning deduction must carry the photographs taken under (g) and a written cost explanation.",
         quote="If a deduction is made for repairs or cleanings allowed by this section, the landlord shall provide photographs taken pursuant to subdivision (g)"),
    dict(id="CA:1950.5(g)(1)", state="CA", actor="landlord", modality="shall", determinacy="RULE",
         effect="Move-in photographs for tenancies beginning on or after 2025-07-01.",
         cross_time="move-in evidence is a precondition of move-out deductions",
         quote="For tenancies that begin on or after July 1, 2025, the landlord shall take photographs of the unit immediately before, or at the inception of, the tenancy."),
    dict(id="CA:1950.5(g)(2)", state="CA", actor="landlord", modality="shall", determinacy="MIXED",
         effect="From 2025-04-01, photographs after possession returns and before repairs, and again after repairs.",
         judgment=["within a reasonable time"],
         quote="Beginning April 1, 2025, the landlord shall take photographs of the unit within a reasonable time after the possession of the unit is returned to the landlord"),
    dict(id="CA:1950.5(h)(3)", state="CA", actor="landlord", modality="may", determinacy="MIXED",
         effect="If repairs or vendor documents are not done within 21 days, deduct a good-faith estimate; complete the documentation within 14 days of finishing.",
         judgment=["cannot reasonably be completed", "good faith estimate"],
         quote="Within 14 calendar days of completing the repair or receiving the documentation, the landlord shall complete the requirements"),
    dict(id="CA:1950.5(h)(4)(A)", state="CA", actor="landlord", modality="exception", determinacy="RULE",
         effect="Documentation duties (h)(2)-(3) do not apply when repair and cleaning deductions total $125 or less (unless requested under (h)(5)).",
         quote="The deductions for repairs and cleaning together do not exceed one hundred twenty-five dollars ($125)."),
    dict(id="CA:1950.5(h)(7)", state="CA", actor="landlord", modality="consequence", determinacy="STANDARD",
         effect="Bad-faith noncompliance with (h) forfeits any claim to the security.",
         judgment=["in bad faith"],
         quote="The landlord shall not be entitled to claim any amount of the security if the landlord, in bad faith, fails to comply with this subdivision."),
    dict(id="CA:1950.5(m)", state="CA", actor="landlord", modality="liability", determinacy="STANDARD",
         effect="Bad-faith retention: statutory damages up to twice the security plus actual damages.",
         judgment=["bad faith"],
         quote="statutory damages of up to twice the amount of the security, in addition to actual damages."),
    # Virginia
    dict(id="VA:55.1-1226(A)", state="VA", actor="landlord", modality="shall", determinacy="RULE",
         effect="Itemized disposition with any amount due within 45 days of termination or vacating, whichever is later.",
         quote="within 45 days after the termination date of the tenancy or the date the tenant vacates the dwelling unit, whichever occurs last."),
    dict(id="VA:55.1-1226(A)-wear", state="VA", actor="landlord", modality="may apply only", determinacy="STANDARD",
         effect="Damages from the tenant's noncompliance, less reasonable wear and tear.",
         judgment=["reasonable wear and tear"],
         quote="the payment of the amount of damages that the landlord has suffered by reason of the tenant's noncompliance with"),
    dict(id="VA:55.1-1226(E)-contractor", state="VA", actor="landlord", modality="may", determinacy="RULE",
         effect="If damages exceed the deposit and need a third-party contractor, notice within 45 days buys 15 more days to itemize.",
         quote="If notice is given as prescribed in this subsection, the landlord shall have an additional 15-day period to provide an itemization of the damages and the cost of repair."),
    dict(id="VA:55.1-1226(E)-willful", state="VA", actor="landlord", modality="consequence", determinacy="STANDARD",
         effect="Willful noncompliance: return of the deposit, actual damages and attorney fees (credited against rent owed).",
         judgment=["willfully fails"],
         quote="If the landlord willfully fails to comply with this section, the court shall order the return of the security deposit to the tenant, together with actual damages and reasonable attorney fees"),
    dict(id="VA:55.1-1226(G)", state="VA", actor="landlord", modality="shall", determinacy="RULE",
         effect="Within 5 days of notice to vacate, tell the tenant of the right to attend; inspect within 72 hours of possession if requested.",
         quote="which must be made within 72 hours of delivery of possession."),
]

# ---------------------------------------------------------------- Stage B: clocks (from the atoms above only)
CLOCKS = {
    "NY": dict(atom="NY:7-108(1-a)(e)", anchor="vacated", days=14, unit="days", extension=None,
               on_expiry="forfeit any right to retain (no intent element)"),
    "CA": dict(atom="CA:1950.5(h)(1)", anchor="vacated", days=21, unit="calendar days",
               extension="good-faith estimate now; documents within 14 calendar days of completion (CA:1950.5(h)(3))",
               on_expiry="forfeiture only on bad faith (h)(7); up to 2x for bad-faith retention (m)"),
    "VA": dict(atom="VA:55.1-1226(A)", anchor="max(termination, vacated)", days=45, unit="days",
               extension="+15 days if contractor notice given within 45 (VA:55.1-1226(E)-contractor)",
               on_expiry="willful: return deposit, actual damages, attorney fees"),
}

# Stage A dependency closure the slice does NOT resolve. Each is a bounded unknown, not a default.
BOUNDED_UNKNOWNS = [
    "Weekend and holiday rollover: whether each state's general computation-of-time statute moves a deadline that "
    "lands on a weekend or holiday (NY General Construction Law, CA Civil Code, VA Code general provisions). Not read.",
    "NY 7-108 has no stated estimate mechanism: how a landlord itemizes repair costs not yet invoiced within 14 days. "
    "The statute requires 'reasonable and itemized costs'; case law not read.",
    "NY 7-108(1-a) exclusions (rent-controlled and rent-stabilized units under the named laws, seasonal units, "
    "owner-occupied co-ops): applicability depends on unit status facts.",
    "Local law: NYC and California cities may add rules (e.g. rent stabilization schemes, local ordinances). Not read.",
    "Delivery and receipt: what counts as 'provide' / 'furnish' / 'given' for each notice (mail, email by agreement).",
]


def check_quotes():
    """Discriminating check: every atom's quote must appear verbatim in its own state's statute text."""
    bad = [a["id"] for a in ATOMS if re.sub(r"\s+", " ", a["quote"]) not in TEXT[a["state"]]]
    # the check must be able to fail: a quote from another state must not be found
    cross = [a["id"] for a in ATOMS if re.sub(r"\s+", " ", a["quote"]) in TEXT[{"NY": "CA", "CA": "VA", "VA": "NY"}[a["state"]]]]
    return bad, cross


# ---------------------------------------------------------------- Stage C: evaluator (calendar days only)
def deadline(state, vacated, termination=None):
    """Raw statutory deadline. Holiday rollover is a bounded unknown and is NOT applied."""
    c = CLOCKS[state]
    anchor = max(vacated, termination) if (state == "VA" and termination) else vacated
    return anchor + dt.timedelta(days=c["days"])


if __name__ == "__main__":
    bad, cross = check_quotes()
    print(f"atoms: {len(ATOMS)}; quotes not found verbatim: {bad}; quotes wrongly found in another state: {cross}")
    kinds = {}
    for a in ATOMS:
        kinds.setdefault(a["state"], {}).setdefault(a["determinacy"], 0)
        kinds[a["state"]][a["determinacy"]] += 1
    print("determinacy by state:", json.dumps(kinds))
    # one case, three states: tenant vacates Wed 30 Sep 2026; VA lease terminates 31 Oct 2026 (vacated early)
    v, term = dt.date(2026, 9, 30), dt.date(2026, 10, 31)
    for s in ("NY", "CA", "VA"):
        d = deadline(s, v, term)
        print(f"{s}: statement due {d:%a %d %b %Y} ({CLOCKS[s]['days']} {CLOCKS[s]['unit']} from {CLOCKS[s]['anchor']}); "
              f"extension: {CLOCKS[s]['extension']}; on expiry: {CLOCKS[s]['on_expiry']}")
    print("bounded unknowns:", len(BOUNDED_UNKNOWNS))
    json.dump({"atoms": ATOMS, "clocks": CLOCKS, "bounded_unknowns": BOUNDED_UNKNOWNS},
              open(pathlib.Path(__file__).parent / "slice.json", "w"), indent=1)
