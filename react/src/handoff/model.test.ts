import { describe, expect, it } from "vitest";
import { inbox, lineState, nextVisit } from "./model";
import { workExample } from "./work.test-support";

function booked() {
  const data = workExample();
  const job = data.jobs[0]!;
  Object.assign(job, {
    status: "Scheduled",
    appointmentAt: "2026-09-29T13:00:00Z",
    appointmentEndsAt: "2026-09-29T16:00:00Z",
  });
  data.inspections = [];
  data.invoices = [];
  data.payments = [];
  return { data, job };
}

describe("inbox threads", () => {
  it("files a vendor's reply under its sender, with the order it answers", () => {
    const { data, job } = booked();
    data.messages = [
      {
        id: "order",
        title: "Work order: Condition assessment",
        body: "Please go ahead.",
        recipientPartyId: job.providerPartyId,
        direction: "Outgoing",
        purpose: "Appointment",
        jobId: job.id,
        replyToMessageId: null,
        status: "Sent",
        createdAt: "2026-09-28T08:42:00Z",
      },
      {
        id: "reply",
        title: "Re: Work order: Condition assessment",
        body: "We can start on Tuesday, September 29.",
        senderPartyId: job.providerPartyId,
        recipientPartyId: null,
        direction: "Incoming",
        purpose: "Appointment",
        jobId: job.id,
        replyToMessageId: "order",
        status: "Received",
        createdAt: "2026-09-28T12:42:00Z",
      },
    ];
    const threads = inbox(data);
    expect(threads).toHaveLength(1);
    expect(threads[0]!.partyId).toBe(job.providerPartyId);
    expect(threads[0]!.messages.map((m) => m.id)).toEqual(["order", "reply"]);
  });
});

describe("next visit", () => {
  it("names the next booked visit when every open job has one", () => {
    const { data, job } = booked();
    expect(nextVisit(data)).toMatchObject({ job: job.title, at: "2026-09-29T13:00:00Z" });
  });
  it("is empty while any open job has no visit booked", () => {
    const { data, job } = booked();
    job.appointmentAt = null;
    expect(nextVisit(data)).toBeNull();
  });
});

describe("quote line status", () => {
  it("marks each line ordered, in the proposed plan, or not selected", () => {
    const data = workExample();
    data.workPlan!.selections = data.workPlan!.selections.filter((s) => s.quoteLineId === "handle");
    data.jobs = [
      ...data.jobs,
      {
        ...data.jobs[0]!,
        id: "wall-job",
        quoteId: "offer-oak",
        scope: [
          {
            lineId: "wall",
            description: "Local wall repair",
            amountCents: "80000",
            acceptedScope: "Repair the wall",
          },
        ],
      },
    ];
    expect(lineState(data, "offer-oak", "wall")).toBe("Ordered");
    expect(lineState(data, "offer-oak", "handle")).toBe("In proposed plan");
    data.workPlan!.status = "Accepted";
    expect(lineState(data, "offer-oak", "handle")).toBe("Approved");
    data.workPlan!.selections = [];
    expect(lineState(data, "offer-oak", "handle")).toBe("Not ordered");
  });
});
