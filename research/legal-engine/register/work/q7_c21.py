import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:GOL 11-102", N, "Utility liability to state contractors for delaying public works; outside the chain."),
    D("NY:GOL 11-105", N, "Civil liability for shoplifting from mercantile establishments; a rental building is not a mercantile establishment."),
    D("NY:GOL 11-106", N, "Police officers' and firefighters' injury claims against negligent persons; not a settlement claim between landlord and tenant."),
    D("NY:GOL 13-107", N, "Claims pass with transferred bonds; outside the chain (assignment of a lease balance is governed by the stated champerty rule)."),
    D("NY:GOL 15-109", N, "Uniform interpretation of the joint-obligations title; a construction canon that changes no outcome of the stated co-obligor release and payment rules."),
    D("NY:GOL 15-304", N, "Cancellation of record of expired oil, gas and mineral leases; outside the chain."),
    D("NY:GOL 3-109", N, "Payment of wages to minors; outside the chain."),
    D("NY:GOL 3-111", N, "Parent's negligence not imputed to an infant in personal-injury actions; outside the chain."),
    D("NY:GOL 3-303", N, "Prenuptial contracts survive marriage; outside the chain."),
    D("NY:GOL 3-309", N, "Spouses may convey property to each other; outside the chain."),
    D("NY:GOL 5-1101", N, "Agreements to transfer securities not void for want of consideration; outside the chain."),
    D("NY:GOL 5-1115", N, "Grantor's promises in a recordable deed binding without consideration; the chain involves no deed."),
    D("NY:GOL 5-1311", N, "Risk of loss between vendor and purchaser in a contract of sale of realty; a building sale's effect on the tenant's deposit is governed by the stated GOL 7-105 and 7-108(2) rules, and this allocates risk only between seller and buyer."),
    D("NY:GOL 5-1502L", N, "Statutory power of attorney authority over retirement benefits; outside the chain."),
    D("NY:GOL 5-301", N, "Void anti-union employment contracts; outside the chain."),
    D("NY:GOL 5-302", N, "Void digital-replica clauses in performance contracts; outside the chain."),
    D("NY:GOL 5-311", N, "Void spousal agreements to dissolve marriage or waive support; outside the chain."),
    D("NY:GOL 5-322", N, "Void negligence waivers for caterers; outside the chain."),
    D("NY:GOL 5-322.2", N, "Owner identification in building construction contracts; a contracting formality between owner and contractor, not a tenant charge or step."),
    D("NY:GOL 5-322.3", N, "Filing of payment bonds on private improvements over $100,000; outside the chain."),
    D("NY:GOL 5-324", N, "Void indemnities of architects and engineers for design defects; outside the chain."),
    D("NY:GOL 5-326", N, "Void negligence waivers by pools, gyms and places of recreation that charge for use; it governs liability for injury, not any charge, deposit or step in settling a tenancy."),
    D("NY:GOL 5-333", N, "Oil, gas and mineral lease terms; outside the chain."),
    D("NY:GOL 5-334", N, "Enforceability of equity options granted to large mortgage lenders; outside the chain."),
    D("NY:GOL 5-335", N, "Insurer subrogation limits in personal-injury settlements; outside the chain."),
    D("NY:GOL 5-525", N, "Interest on securities brokers' debit balances; outside the chain."),
    D("NY:GOL 5-602", N, "Interest on insurance drafts held in mortgage escrow for owner-occupied homes; a mortgagee's escrow, not a tenant's security deposit."),
    D("NY:GOL 5-705", N, "A grantee is liable on an existing mortgage only if it assumes it in writing; between owner and lender, not the tenancy account."),
]
save(rows)
