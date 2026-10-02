import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
S = "NY:ABP 1405"
rows.append(D(S, "new_rule",
  "Once an unclaimed refund is paid to the Comptroller, the former tenant earns no further interest on it; this closes "
  "the deposit-interest account at the payment date.",
  proposed=[R("NY:ABP-1405-no-interest-after-payment", S, "ABP 1405(1)(a)", "former tenant", "may_not",
  "The landlord has paid the former tenant's unclaimed deposit refund (with any 7-103 interest accrued to that date) "
  "to the State Comptroller under ABP 1315 or 1312.",
  "The tenant is entitled to no interest on it from the payment date, whether or not it earned interest before; the "
  "interest-bearing exceptions in 1405(1)(a) cover only bank, insurance and other article 3, 4, 6 and 10 property, not "
  "a 1315 refund. The landlord therefore computes and pays 7-103 interest only up to the payment to the Comptroller.",
  Q(S, "no owner of abandoned property shall be entitled to receive interest on account of such abandoned property from and after the date",
    "whether or not he was entitled to interest on such property prior to such date"),
  "minor", "Step 6.8 unclaimed refund; Step 5.6 interest", dependencies=["NY:ABP-1315(2)", "NY:GOL-7-103(2)-interest-owed"])]))

rows.append(D("NY:ABP 1409", "no_decision",
  "Charges holder publication costs against abandoned property; a 1315 deposit refund carries no holder publication "
  "duty, so nothing is deducted under it."))
rows.append(D("NY:ABP 1411", "no_decision", "The Comptroller's power to waive publication; no landlord or tenant act turns on it."))

S = "NY:ABP 1413"
rows.append(D(S, "new_rule",
  "The landlord's unclaimed-refund report is made under oath; a wilful false oath in it is perjury.",
  proposed=[R("NY:ABP-1413-false-report", S, "ABP 1413", "landlord", "must_not",
  "The landlord files the report of an unclaimed deposit refund with the Comptroller.",
  "A wilful false oath in that report is perjury and punishable as such, in addition to the ABP 1412 penalties.",
  Q(S, "The making of a willful false oath in any report", "punishable as such according to law."),
  "minor", "Step 6.8 unclaimed refund", dependencies=["NY:ABP-1400-1412-reporting"])]))

S = "NY:ABP 1415"
rows.append(D(S, "new_rule",
  "No rule bars the holder from taking service, handling or dormancy charges out of an unclaimed refund; 1415 does, "
  "save deductions under New York law or a specific contract term made in the normal course.",
  proposed=[R("NY:ABP-1415-no-dormancy-charges", S, "ABP 1415", "landlord", "must_not",
  "A former tenant's deposit refund is unclaimed and becomes (or is becoming) abandoned property.",
  "The landlord may not deduct any service, handling or maintenance charge from it, unless the deduction is made under "
  "New York law (for example the certified-mail notice cost ABP 1422 allows) or under a valid contract that expressly "
  "makes the deduction non-refundable and it is taken in the normal course of the landlord's business. A lease clause "
  "creating such a charge on a deposit refund is still subject to GOL 7-103 and 7-108, which allow no administration "
  "charge beyond the 1% interest fee (NY:GOL-7-103(2)-admin-fee).",
  Q(S, "No deduction shall be made for service, handling or maintenance charges", "in the normal course of business of the holder."),
  "major", "Step 6.8 unclaimed refund", dependencies=["NY:ABP-1422", "NY:GOL-7-103(2)-admin-fee"])]))

rows.append(D("NY:ABP 1416", "no_decision",
  "Regulates fee-charging locators who help owners retrieve property already held by the Comptroller; no landlord, "
  "manager or Handoff settlement act turns on it."))

S = "NY:ABP 1419"
rows.append(D(S, "new_rule",
  "Changes what the landlord's unclaimed-refund report must contain for refunds of $20 or less.",
  proposed=[R("NY:ABP-1419-aggregate-small", S, "ABP 1419", "landlord", "may",
  "The landlord reports and delivers unclaimed deposit refunds to the Comptroller and one or more is $20 or less.",
  "Refunds of $20 or less may be reported in the aggregate without the tenant's name, address or other identifying "
  "information; every amount, however small, must still be delivered.",
  Q(S, "need not specify the name, address or other information identifying the owner", "in any amount, to the state comptroller."),
  "minor", "Step 6.8 unclaimed refund", dependencies=["NY:ABP-1315(2)"])]))

rows.append(D("NY:DCL 150", "no_decision",
  "Lets a discharged debtor have a judgment docket marked discharged; the landlord's duty to stop enforcing a "
  "discharged balance is stated by US:11USC524(a)(2), and nothing the landlord does turns on the docket entry."))

S = "NY:DCL 151"
rows.append(D(S, "partial",
  "The bankruptcy stay on setoff is stated (US:11USC362(a)(7)-deposit-is-setoff); DCL 151 supplies the state-law setoff "
  "right itself, on either side's insolvency event, exercisable against a trustee, receiver or levying creditor.",
  ["US:11USC362(a)(7)-deposit-is-setoff", "US:CASE-Strumpf-hold", "NY:CPLR-6401-foreclosure-receiver"], [R(
  "NY:DCL-151-insolvency-setoff", S, "DCL 151", "landlord; tenant", "may",
  "Branch (a): the tenant becomes subject to a bankruptcy petition, assignment for creditors, receivership, "
  "execution, supplementary-proceeding subpoena or order, or attachment, while the landlord owes it a deposit refund "
  "and it owes the landlord a balance. Branch (b): the landlord (owner) becomes subject to one of those events while "
  "it owes the tenant a refund and the tenant owes it rent or charges.",
  "The party owing money may set off what the other owes it against what it owes the other, matured or unmatured, at "
  "or after the event, even though it had not set off before, and may assert the setoff against the trustee, debtor "
  "in possession, assignee, receiver or execution, judgment or attachment creditor and anyone claiming through them. "
  "(a) In the tenant's bankruptcy the right exists but its exercise is stayed until relief is granted "
  "(US:11USC362(a)(7)-deposit-is-setoff, US:CASE-Strumpf-hold); against a tenant's levying creditor or receiver the "
  "landlord applies the deposit to the tenant's balance first and only the remainder is reached. (b) Against an "
  "owner's receiver (including a foreclosure receiver collecting rent) or levying creditor, the tenant may set off "
  "its refund against rent the receiver demands.",
  Q(S, "to set off and apply against any indebtedness, whether matured or unmatured, of such creditor to such debtor",
    "any amount owing from such debtor to such creditor"),
  "critical", "Step 0.5 who is owed the rent; Step 6.7 tenant in bankruptcy",
  dependencies=["US:11USC362(a)(7)-deposit-is-setoff", "NY:CPLR-6401-foreclosure-receiver"])]))

S = "NY:DCL 282"
rows.append(D(S, "partial",
  "The refund payee in the tenant's bankruptcy is stated for chapter 7 as the trustee (US:11USC542-refund-payee); DCL "
  "282(i) lets a New York debtor exempt CPLR 5205 property, which includes a residential security deposit, and "
  "exempted property leaves the estate, so the remainder is then the debtor's. The rule misses this branch.",
  ["US:11USC542-refund-payee"], [R(
  "NY:DCL-282-deposit-exemption-payee", S, "DCL 282(i); CPLR 5205(g); 11 USC 522(l)", "landlord", "must",
  "The former tenant, domiciled in New York, is a chapter 7 debtor and lists its security deposit (or the refund) as "
  "exempt under DCL 282(i) and CPLR 5205(g) (or under the federal list by election, DCL 285), and no objection is "
  "sustained, so the exemption stands.",
  "The refund remainder is exempt property and is paid to the debtor, not the trustee, once the landlord has notice "
  "that the exemption stands; before then the trustee branch of US:11USC542-refund-payee governs. The exemption "
  "decides only who receives the remainder; the landlord's application of the deposit to lawful charges is governed "
  "by US:11USC362(a)(7)-deposit-is-setoff and US:CASE-Strumpf-hold.",
  Q(S, "an individual debtor domiciled in this state may exempt from the property of the estate",
    "under sections fifty-two hundred five and fifty-two hundred six of the civil practice law and rules"),
  "critical", "Step 6.7 tenant in bankruptcy", amends="US:11USC542-refund-payee",
  dependencies=["US:11USC542-refund-payee"],
  construction=[{"source_file": "register/texts/NY_CPLR/5205.txt", "quote": Q("register/texts/NY_CPLR/5205.txt",
                  "Security deposit exemption. Money deposited as security for the rental of real property to be used as the residence of the judgment debtor")},
                {"source_file": "register/texts/US_11USC/522.txt", "quote": Q("register/texts/US_11USC/522.txt",
                  "Unless a party in interest objects, the property claimed as exempt on such list is exempt.")}],
  reasoning="DCL 282(i) imports CPLR 5205 exemptions, and 5205(g) names residential security deposits; 11 USC 522(l) "
            "makes claimed property exempt absent a sustained objection, removing it from what the trustee "
            "administers.")]))

rows.append(D("NY:DCL 283", "no_decision",
  "Caps the aggregate of CPLR 5205(a) personal-property and annuity exemptions; the security deposit is exempt under "
  "5205(g), outside that cap, so the settlement is unchanged."))
rows.append(D("NY:DCL 284", "no_decision",
  "Opts New York debtors out of the federal 522(d) list subject to DCL 285; who is paid follows the exemption the "
  "debtor actually claims (proposed at DCL 282), not this section."))
rows.append(D("NY:DCL 285", "no_decision",
  "Lets a debtor elect the federal exemption list; the settlement consequence of any exemption of the refund is "
  "stated in the rule proposed at DCL 282."))
rows.append(D("NY:GCN 33", "no_decision", "Notice to a board or body; no settlement notice goes to one."))
rows.append(D("NY:GCN 44-A", "no_decision",
  "A seal on an instrument has no legal effect; no lease, guaranty or release in this chain turns on a seal."))

S = "NY:GCN 53"
rows.append(D(S, "new_rule",
  "Every chain deadline is kept by New York standard time; this decides whether an electronic statement or refund "
  "sent near midnight is on day 14 or day 15.",
  proposed=[R("NY:GCN-53-deadline-clock", S, "GCN 53", "landlord, manager, Handoff", "must",
  "An act in the chain must be performed at or within a time prescribed by law: the 14-day statement and refund, the "
  "RPL 227-b 'midnight of the fifth business day', notices with day or hour limits.",
  "The act is timed by New York standard time (NY:GCN-52-standard-time), not the sender's or a server's time zone. A "
  "statement or refund sent by email or text is provided on the New York calendar day of sending; one sent after "
  "midnight New York time on day 14 is sent on day 15 and late (NY:GOL-7-108(1-a)(e)-forfeiture).",
  Q(S, "Any act required by or in pursuance of law to be performed at or within a prescribed time", "according to the standard time."),
  "critical", "Step 6.3 counting", dependencies=["NY:GCN-20", "NY:ADJ-provide-written-dispatch"])]))

S = "NY:GCN 52"
rows.append(D(S, "new_rule",
  "Defines the New York standard time that GCN 53 applies to every chain deadline.",
  proposed=[R("NY:GCN-52-standard-time", S, "GCN 52(1), (2)", "landlord, manager, Handoff", "must",
  "A chain deadline is computed in clock time (NY:GCN-53-deadline-clock).",
  "New York standard time is that of the 75th meridian west (Eastern Standard Time), advanced one hour during daylight "
  "saving time; courts, public officers and legal proceedings follow it. The daylight-saving dates are those of the "
  "federal Uniform Time Act (second Sunday in March to first Sunday in November), which supersedes the April and "
  "October dates in GCN 52(2).",
  Q(S, "The standard time throughout this state is that of the seventy-fifth meridian of longitude west from Greenwich",
    "shall be regulated thereby."),
  "major", "Step 6.3 counting",
  reasoning="15 U.S.C. 260a fixes the daylight-saving period nationally and supersedes inconsistent state laws; New "
            "York has not exempted itself, so only GCN 52(1)'s zone and the fact of a one-hour advance remain operative.")]))

S = "NY:GCN 93"
rows.append(D(S, "new_rule",
  "Decides point-in-time application wherever a rule in the chain is repealed or sunsets (Good Cause 2034-06-15, "
  "stabilization 2027-03-31, the pre-2019 and pre-2025 deposit texts): rights and liabilities already accrued survive.",
  proposed=[R("NY:GCN-93-repeal-saves-accrued", S, "GCN 93", "landlord; tenant", "may",
  "A statute or part of one that governs the tenancy is repealed or expires (by sunset) after a right accrued, a "
  "liability or forfeiture was incurred, or an act was done under it.",
  "The repeal does not affect that act, right, liability, penalty or forfeiture; it is enjoyed, asserted and enforced "
  "as fully as if the repeal had not taken effect (for example a deposit forfeiture or double-damages liability "
  "incurred under a text later amended, or a Good Cause defense to a non-renewal given before 2034-06-15), unless the "
  "repealing act provides otherwise.",
  Q(S, "The repeal of a statute or part thereof shall not affect or impair any act done", "as if such repeal had not been effected."),
  "major", "Step 0.4 which version applies")]))

S = "NY:GCN 94"
rows.append(D(S, "new_rule",
  "Companion to GCN 93 for suits pending when a statute in the chain is repealed or sunsets.",
  proposed=[R("NY:GCN-94-pending-actions", S, "GCN 94", "landlord; tenant", "may",
  "A suit or proceeding under a statute in the chain (deposit, Good Cause, stabilization) is pending when that "
  "statute is repealed or expires.",
  "Unless the repealing law provides otherwise, it is prosecuted and defended to final judgment as if the provision "
  "had not been repealed.",
  Q(S, "Unless otherwise specially provided by law, all actions and proceedings", "as they might if such provisions were not so repealed."),
  "minor", "Step 0.4 which version applies; Step 8.10 before suing", dependencies=["NY:GCN-93-repeal-saves-accrued"])]))

S = "NY:GOL 11-104"
rows.append(D(S, "partial",
  "The returned-check fee cap is stated (NY:RPL-238-a(2-a)); 11-104 adds that a residential rent check carries no "
  "statutory bounced-check damages, and sets the conditions for them on any other check.",
  ["NY:RPL-238-a(2-a)", "NY:GOL-5-328(3)(b)"], [R(
  "NY:GOL-11-104-dishonored-check", S, "GOL 11-104(1)-(8)", "landlord", "may",
  "A check the tenant gave the landlord is dishonored for no account or insufficient funds. Branch (a): the check "
  "paid rent for the residential unit. Branch (b): it paid some other amount (a move-out damage or utility balance).",
  "(a) No additional liquidated damages under 11-104; the landlord recovers the face amount and only the returned-check "
  "fee RPL 238-a(2-a) allows. (b) The drawer who knew or should have known the check would bounce is liable for the "
  "face amount plus liquidated damages fixed by the court up to the lesser of twice the face amount or $750 (no "
  "account) or $400 (insufficient funds), only if the landlord posted or gave conspicuous public notice of these "
  "damages, sent the first demand in the statutory English-and-Spanish form by first-class and restricted certified "
  "mail on or after learning of dishonor, sent the second demand by first-class mail on or after the 15th day after "
  "the first was received, and the drawer did not pay within 30 days after the second demand was mailed; defenses "
  "available against a non-holder in due course apply.",
  Q(S, "4. The drawer shall not be liable to the payee for the additional, liquidated damages provided for by this section if:",
    "The drawer gave such check as payment for the rental of residential premises;"),
  "major", "Step 5.2 fees", dependencies=["NY:RPL-238-a(2-a)"],
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S, "6. The additional liquidated damages provided for in this section shall be available only to those persons or entities which post",
                  "imposition of such damages, and provide notice that criminal penalties also may apply.")}],
  reasoning="Subdivision 4(a) excludes rent checks; subdivisions 2, 3, 6 and 7 state the caps and preconditions for "
            "other checks.")]))

S = "NY:GOL 13-101"
rows.append(D(S, "partial",
  "Champerty is stated (NY:JUD-489-champerty) but not the base rule that the lease balance, and the tenant's deposit "
  "claim, are freely transferable and enforceable by the transferee in its own name subject to prior defenses.",
  ["NY:JUD-489-champerty"], [R(
  "NY:GOL-13-101-105-balance-transfer", S, "GOL 13-101, 13-105", "landlord; transferee", "may",
  "The owner transfers (sells or assigns) a former tenant's balance, or the tenant assigns its deposit claim.",
  "The claim is transferable: it is not a personal-injury claim and no New York or federal statute forbids its "
  "transfer. The transferee may enforce it by action, or use it as a defense or counterclaim, in its own name, "
  "subject to every defense and counterclaim the debtor had against the transferor before notice of the transfer "
  "(for example the tenant's deposit claim, forfeiture, or habitability offset) and any it has against the "
  "transferee. Limits: a transfer taken with the intent and primary purpose of suing is champertous "
  "(NY:JUD-489-champerty); a debt buyer needs a DCWP licence (NYC:DCA-debt-buyer) and is a federal debt collector "
  "(US:HANDOFF-config-owns-balance); rent in a transfer is still collected only by a licensed broker where RPL 440 "
  "requires.",
  Q(S, "Any claim or demand can be transferred, except in one of the following cases:", "would contravene public policy."),
  "critical", "Step 8.1b payments and settlements; Step 8.6 licensing", dependencies=["NY:JUD-489-champerty", "NYC:DCA-debt-buyer"],
  construction=[{"source_file": BY_ID["NY:GOL 13-105"]["text_file"], "quote": Q("NY:GOL 13-105",
                  "the transfer thereof passes an interest, which the transferee may enforce by an action or special proceeding",
                  "before notice of the transfer, or against the transferee.")}],
  reasoning="13-101 makes the claim transferable; 13-105 gives the transferee the transferor's position subject to "
            "defenses existing before notice.")]))

rows.append(D("NY:GOL 13-105", "partial",
  "Its effect (transferee enforces in its own name, subject to defenses before notice) is proposed jointly with 13-101 "
  "as NY:GOL-13-101-105-balance-transfer; champerty limits are stated.",
  ["NY:JUD-489-champerty"], [R(
  "NY:GOL-13-105-notice-of-transfer", "NY:GOL 13-105", "GOL 13-105", "landlord; transferee", "must",
  "A former tenant's balance has been transferred and the tenant pays, settles with, or acquires a defense against "
  "the original landlord before it receives notice of the transfer.",
  "Those payments, settlements and defenses bind the transferee; defenses the tenant acquires against the landlord "
  "after notice do not. The transferee therefore gives the tenant written notice of the transfer before collecting, "
  "and the landlord credits any payment it receives after the transfer to the transferee.",
  Q("NY:GOL 13-105", "subject to any defense or counter-claim, existing against the transferrer, before notice of the transfer"),
  "major", "Step 8.1b payments and settlements", dependencies=["NY:GOL-13-101-105-balance-transfer"])]))

S = "NY:GOL 13-103"
rows.append(D(S, "new_rule",
  "A money judgment against the former tenant may be assigned, which changes who may enforce it.",
  proposed=[R("NY:GOL-13-103-judgment-transfer", S, "GOL 13-103", "landlord; transferee", "may",
  "The landlord holds a money judgment against the former tenant and transfers it.",
  "The judgment is transferable and the transferee enforces it. If the judgment is vacated or reversed, the transfer "
  "carries the underlying claim only if that claim was transferable before judgment (it is: "
  "NY:GOL-13-101-105-balance-transfer). A transferor who did not acknowledge its signature must do so on request of "
  "the assignee, a later assignee or the judgment debtor, on payment of the officer's fees.",
  Q(S, "A judgment for a sum of money, or directing the payment of a sum of money, recovered upon any cause of action, may be transferred",
    "unless the latter was transferable before the judgment was recovered."),
  "minor", "Step 8.12 after judgment", dependencies=["NY:GOL-13-101-105-balance-transfer"])]))

S = "NY:GOL 15-102"
rows.append(D(S, "partial",
  "Release of one co-tenant is stated (NY:GOL-15-104-105-cotenant-release); 15-102 adds that a judgment against one or "
  "some co-tenants does not discharge a co-tenant or guarantor who was not a party.",
  ["NY:GOL-15-104-105-cotenant-release"], [R(
  "NY:GOL-15-102-judgment-not-discharge", S, "GOL 15-102", "landlord", "may",
  "The lease balance is owed by several co-tenants (jointly, or jointly and severally) or with a guarantor, and the "
  "landlord obtains a judgment against only some of them.",
  "The judgment does not discharge any co-obligor who was not a party to that suit; the landlord may still sue the "
  "others, crediting what it actually collects so that it recovers the balance only once.",
  Q(S, "A judgment against one or more of several obligors", "who was not a party to the proceeding wherein the judgment was rendered."),
  "major", "Step 8 collecting a balance", dependencies=["NY:GOL-15-104-105-cotenant-release"])]))

S = "NY:GOL 15-101"
rows.append(D(S, "partial",
  "Defines the reach of GOL title 15 (releases and co-obligors), on which NY:GOL-15-104-105-cotenant-release depends: "
  "it covers contract obligations only, not tort liability.",
  ["NY:GOL-15-104-105-cotenant-release"], [R(
  "NY:GOL-15-101-contract-only", S, "GOL 15-101", "landlord", "must",
  "The landlord applies a GOL title 15 rule (release of one co-obligor, judgment against some, death of a joint "
  "obligor) to a balance.",
  "Those rules reach only obligations and obligors in contract (the lease, a guaranty); they do not reach a person "
  "liable only in tort (a non-party guest who damaged the unit), whose release is governed by the tort rules. "
  "'Several obligors' means obligors severally bound for the same performance.",
  Q(S, "“obligation” does not include a liability in tort", "for the same performance."),
  "minor", "Step 8.1b payments and settlements", dependencies=["NY:GOL-15-104-105-cotenant-release"])]))

rows.append(D("NY:GCN 50", "no_decision", "Gregorian calendar and New Year's Day; no chain deadline turns on it beyond GCN 20 counting."))
rows.append(D("NY:GCN 51", "no_decision", "Defines night time; no chain act is limited to or barred at night by a rule in scope."))

save(rows)
