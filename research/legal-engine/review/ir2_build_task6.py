"""Independent review 2, task 6: first-round verdicts, written only after tasks 1-5 were saved.
Run from research/legal-engine:  python3 review/ir2_build_task6.py  (then ir2_render.py, ir2_verify.py)
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "review/independent_review_2.json"
d = json.loads(P.read_text())

d["first_round"] = [
    {"id": "R1-01", "verdict": "correct and complete",
     "reason": "CPLR 5001/5004 rules, the NML contract-rate rule and the 238-a cap on lease interest are applied and match the text; 2% for natural persons, 9% for companies. S9760 (R2-02) would add 'whether contingent or absolute' to 5004(b) and changes nothing for rent."},
    {"id": "R1-02", "verdict": "correct and complete",
     "reason": "NY:GOL-5-905 matches the statute (15-30 days, personal or registered/certified service); walk 3.1 and C6 state it."},
    {"id": "R1-03", "verdict": "correct and complete",
     "reason": "Two-branch payee rule rests on 7-103(1) as words of severance and Lasky for the joint branch; Holmes is no longer cited for the split."},
    {"id": "R1-04", "verdict": "correct and complete",
     "reason": "US:11USC542-refund-payee applies 541(a)(1), 542(b)-(c) and 1306(b); walk 6.7 and C15 pay the trustee in chapter 7 and the debtor in chapter 13."},
    {"id": "R1-05", "verdict": "correct but incomplete",
     "reason": "The city registration duty and discretionary stay are right for a non-owner-occupied one- or two-family house, but for a multiple dwelling MDL 325(2) bars recovery of rent until registration (R2-03), and the related MDL 302 certificate-of-occupancy bar was missed by both rounds (R2-01)."},
    {"id": "R1-06", "verdict": "correct but incomplete",
     "reason": "Covered-unit rule (RPL 212, 215) is right; the applied exemption list omits the 245%-of-FMR high-rent exemption (RPL 214(15)), the one most likely to reach a market-rate NYC unit, and three others (R2-04). The first-round correct-rule text had the same omission."},
    {"id": "R1-07", "verdict": "correct and complete",
     "reason": "NYC:HMC-27-2013(a) added; walk 1.5 and 5.3 now condition the 3-year cycle and records on a multiple dwelling."},
    {"id": "R1-08", "verdict": "correct and complete",
     "reason": "Walk 2.5 now says silence is consent and only an election to terminate or an unreasonable refusal ends the lease (RPL 236 text)."},
    {"id": "R1-09", "verdict": "correct and complete",
     "reason": "Cap reaches deposit plus rent paid ahead for a later period; first month's rent is not an advance; AG guide supports."},
    {"id": "R1-10", "verdict": "over-corrected",
     "reason": "The wording fix is right for mistake of law, but the walk now leads with 'knew or should have known' and ties it to every managed account while dropping the rule's 'more than inadvertence or accident' limb, so an inadvertent miss by a manager reads as willful (R2-05). I reject the first round's confirmation that knew-or-should-have-known is the whole meaning: Karole, which the rule adopts, starts from 'not merely negligent'."},
    {"id": "R1-11", "verdict": "correct and complete",
     "reason": "C3 now separates the emailed statement from a refund paid by a method that reaches the tenant within the 14 days."},
    {"id": "R1-12", "verdict": "correct and complete",
     "reason": "Phone limb now rests on Bogom-Shanon (text is writing) plus Pickens; I accept the adjudication."},
    {"id": "R1-13", "verdict": "correct but incomplete",
     "reason": "NY:CPLR-3215(g)(3) states the mailing, but not 3215(g)(3)(iii), which excludes the small claims part (R2-11)."},
    {"id": "R1-14", "verdict": "correct and complete",
     "reason": "CCA 1809(1), 1801-A(b), 1803-A(b) rules match the text; walk 8.10 states them."},
    {"id": "R1-15", "verdict": "correct and complete",
     "reason": "The 17 rules are in the deferred list with one kept sentence each (29-H does not apply; no distress in New York); they remain in the files."},
    {"id": "R1-16", "verdict": "correct and complete",
     "reason": "The 'lighter authority' section and 'No appellate court' sentence are gone from the walk; 8.1 states the controlling authority."},
    {"id": "R1-17", "verdict": "correct and complete",
     "reason": "Gelbart, RPL 235-b, GCN 35, Mabe and Van Rensselaer now point to official or CourtListener copies. New review-1 sources introduced their own provenance slip (HPD source_url, R2-12)."},
]
d["overlap"] = (
    "Overlap with the first round: R2-03 extends R1-05; R2-04 extends R1-06; R2-05 reverses the emphasis of R1-10 and "
    "rejects part of the first round's confirmation of the willfulness standard; R2-11 completes R1-13; R2-12 is a "
    "provenance slip in sources added for R1-05. New in this round: R2-01 (MDL 302 certificate of occupancy), R2-02 "
    "(S9760, passed both houses after the first-round sources were read), R2-06 (liquidated damages and lease-break "
    "charges), R2-07 (rent a deposit may cover after an early departure), R2-08 (RPL 232), R2-09 (ABP 1422), R2-10 "
    "(23 NYCRR Part 1), R2-13 (walk alignment). First-round findings I would reject on the merits: none; R1-10 was "
    "right to narrow the mistake-of-law sentence, but its supporting confirmation overstated the standard.")
P.write_text(json.dumps(d, indent=1, ensure_ascii=False))
print("first_round", len(d["first_round"]))
