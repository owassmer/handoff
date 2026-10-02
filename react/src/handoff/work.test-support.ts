import type { HandoffWorkspace } from "./contracts";
import { acceptWork, exampleWorkspace } from "./examples.test-support";

/** A completed assessment is not an authorization for the later repair proposal. */
export function workExample(): HandoffWorkspace {
  const base = exampleWorkspace();
  Object.assign(base.workPlan!, {
    title: "Assess the wall and handle",
    scope: ["Inspect the wall and handle"],
    desiredOutcome: "A condition report",
    budgetCents: "10000",
    estimatedCostCents: "8000",
  });
  const data = acceptWork(base);
  data.workPlan = {
    ...exampleWorkspace().workPlan!,
    id: "repair-proposal",
    revision: "1",
    status: "Ready",
    selections: [
      {
        quoteId: "offer-oak",
        quoteLineId: "wall",
        scope: "Repair and finish the kitchen wall",
        reason: "The assessment supports a local repair.",
      },
      {
        quoteId: "offer-oak",
        quoteLineId: "handle",
        scope: "Refit and test the loose door handle",
        reason: "The existing handle can be retained.",
      },
    ],
  };
  data.quotes = [
    {
      id: "offer-oak",
      title: "Quoted repair visit",
      providerPartyId: "provider",
      kind: "Repair",
      status: "Offered",
      currency: "GBP",
      lines: [
        { lineId: "wall", description: "Local wall repair", amountCents: "80000" },
        { lineId: "handle", description: "Refit handle", amountCents: "7500" },
      ],
      totalCents: "87500",
      depositCents: "25000",
      paymentTerms: "Deposit on booking; balance after completion",
      requirements: ["Retain sound fittings"],
      availableFrom: "2026-09-23T10:00:00Z",
      validUntil: "2026-10-01T00:00:00Z",
      sourceDocumentId: "quote",
    },
  ];
  data.jobs = [
    {
      id: "assessment-job",
      title: "Condition assessment",
      kind: "Assessment",
      status: "Complete",
      origin: "Handoff",
      providerPartyId: "provider",
      workPlanId: "work-garden",
      decisionId: "decision-saved",
      quoteId: null,
      scope: [
        {
          lineId: "inspection",
          description: "Inspect",
          acceptedScope: "Inspect the wall and handle",
          amountCents: "8000",
        },
      ],
      committedCents: "8000",
      currency: "GBP",
      appointmentAt: "2026-09-22T10:00:00Z",
      appointmentEndsAt: "2026-09-22T11:00:00Z",
      progressSummary: "Assessment complete; a repair is recommended.",
      verificationInspectionId: "report",
    },
  ];
  data.inspections = [
    {
      id: "report",
      title: "Assessment findings",
      jobId: "assessment-job",
      observerPartyId: "provider",
      purpose: "Check condition",
      observedAt: "2026-09-22T11:00:00Z",
      findings: [
        {
          lineId: "wall",
          result: "Deficient",
          observation: "Small area of damaged plaster",
          method: "Visual examination",
        },
        {
          lineId: "hidden",
          result: "Not checked",
          observation: "Concealed pipework not examined",
          method: "No access",
        },
      ],
      sourceDocumentId: "survey",
    },
  ];
  data.invoices = [
    {
      id: "invoice",
      title: "Assessment invoice",
      jobId: "assessment-job",
      providerPartyId: "provider",
      payerPartyId: "owner",
      status: "Received",
      lines: [{ lineId: "inspection", description: "Condition assessment", amountCents: "8000" }],
      totalCents: "8000",
      currency: "GBP",
      dueAt: "2026-09-30T00:00:00Z",
      sourceDocumentId: "quote",
    },
  ];
  data.funding = [
    {
      id: "fund",
      title: "Work funding",
      ownerPartyId: "owner",
      currency: "GBP",
      confirmedCents: "100000",
      committedOrSpentCents: "8000",
      availableCents: "92000",
      sourceDocumentId: "quote",
    },
  ];
  data.payments = [
    {
      id: "payment",
      title: "Assessment payment",
      jobId: "assessment-job",
      purpose: "Final payment",
      status: "Uncertain",
      amountCents: "8000",
      currency: "GBP",
      requestedAt: "2026-09-22T12:00:00Z",
      observedAt: null,
    },
  ];
  data.parties.push({
    id: "owner",
    name: "Riverton Homes",
    kind: "Owner",
    description: "Work funder",
  });
  data.handoff.physicalProgress = "Repairs proposed";
  data.handoff.financialProgress = "Tenant account remains open";
  data.handoff.revision = "8";
  return data;
}
