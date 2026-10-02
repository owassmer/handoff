from q2_lib import *

MECH = "in-suit litigation mechanics (conference, discovery, deposition, calendar, motion or trial practice) that change no amount, deadline, precondition or payee in settling the account or deciding to pursue it."
nd = lambda sid, what: D(sid, "no_decision", what + "; " + MECH)
rows = [
    nd("NY:22 NYCRR 202.10", "Remote appearance and adjournment of conferences"),
    nd("NY:22 NYCRR 202.15", "Videotaped depositions"),
    nd("NY:22 NYCRR 202.20-b", "Limits on number and length of depositions"),
    nd("NY:22 NYCRR 202.20-d", "Depositions of entities"),
    nd("NY:22 NYCRR 202.20-e", "Adherence to discovery schedules"),
    nd("NY:22 NYCRR 202.20-f", "Resolution of disclosure disputes"),
    nd("NY:22 NYCRR 202.20-h", "Pre-trial memoranda and exhibit books"),
    nd("NY:22 NYCRR 202.20-j", "Electronically stored information guidelines in discovery"),
    nd("NY:22 NYCRR 202.22", "Individual-assignment calendars"),
    nd("NY:22 NYCRR 202.23", "Staggered court appearances"),
    nd("NY:22 NYCRR 202.26", "Settlement and pretrial conferences in Supreme Court"),
    nd("NY:22 NYCRR 202.29", "Settlement conference before another justice"),
    nd("NY:22 NYCRR 202.37", "Scheduling trial witnesses"),
    D("NY:22 NYCRR 202.4", "no_decision", "County Court judges may hear Supreme Court ex parte and settlement applications when no Supreme Court term sits; outside New York City and adds no step."),
    nd("NY:22 NYCRR 202.42", "Bifurcated personal-injury trials"),
    nd("NY:22 NYCRR 202.45", "Rescheduling after a mistrial or new-trial order"),
    D("NY:22 NYCRR 202.47", "no_decision", "The county clerk's receipt stub for transcripts of judgment; clerk mechanics (docketing by transcript is at proposed NY:CPLR-5018-docketing)."),
    D("NY:22 NYCRR 202.53", "no_decision", "Trust accountings by testamentary and deed trustees; not a claim in the chain."),
    D("NY:22 NYCRR 202.59", "no_decision", "Tax assessment review outside New York City; not a claim in the chain."),
    D("NY:22 NYCRR 202.65", "no_decision", "Torrens title registration and court-directed real estate sales; not a claim in the chain."),
    nd("NY:22 NYCRR 202.8-a", "Form of motion papers"),
    nd("NY:22 NYCRR 202.8-b", "Word limits on motion papers (effective until 2025-07-07)"),
    nd("NY:22 NYCRR 202.8-c", "Sur-reply papers"),
    D("NY:22 NYCRR 208.1", "no_decision", "Scope, waiver and definitions of the Civil Court rules; no rule of this chain depends on it beyond the rules it introduces."),
    nd("NY:22 NYCRR 208.12", "Videotaped depositions in Civil Court"),
    nd("NY:22 NYCRR 208.15", "Calendar placement of actions transferred from Supreme Court"),
    nd("NY:22 NYCRR 208.17", "Notice of trial and certificate of readiness in Civil Court"),
    D("NY:22 NYCRR 208.23", "no_decision", "Calls of the reserve, ready and general calendars; the default and dismissal consequences for an absent party are those of the calendar-default rule (proposed NY:22NYCRR-208.14-calendar-default)."),
    nd("NY:22 NYCRR 208.5", "Submission of papers to the judge"),
    D("NY:CCA 2103-A", "no_decision", "Authorizes a Civil Court e-filing program; the filing and service consequences are at proposed NY:22NYCRR-208.4a-efiling."),
]
write(rows)
