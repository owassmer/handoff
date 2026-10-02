import { describe, expect, it } from "vitest";
import { canonical_json } from "../domain/codec.js";
import { projectRequests } from "../lifecycle/requests.js";
import { RequestHarness } from "./phaseDRequestsSupport.js";

describe("withdrawal does not confer new financial authority", () => {
  it("lets the requester withdraw READY intent after their grant is revoked", () => {
    const h = new RequestHarness(); const requestId = h.admit();
    h.request.snapshot.authorityGrants.forEach((grant) => { grant.revoked = true; });
    h.run({ kind: "CANCEL_UNATTEMPTED_REQUEST", payload: { requestId, reason: "Withdraw unattempted intent." } }, { isAdministrator: false });
    expect(projectRequests(h.workflow)[0]?.state).toBe("CANCELLED");
    expect(projectRequests(h.workflow)[0]?.reservedAmountCents).toBe(0);
    expect(h.request.snapshot.moneyEvents).toHaveLength(0);
  });
  it("lets a trusted case administrator withdraw without a financial grant", () => {
    const h = new RequestHarness(); const requestId = h.admit();
    h.request.snapshot.authorityGrants.forEach((grant) => { grant.revoked = true; });
    h.run({ kind: "CANCEL_UNATTEMPTED_REQUEST", payload: { requestId, reason: "Administrator withdrawal." } }, { actorId: "other-admin", isAdministrator: true });
    expect(projectRequests(h.workflow)[0]?.state).toBe("CANCELLED");
  });
  it("does not let an unrelated non-administrator withdraw another request", () => {
    const h = new RequestHarness(); const requestId = h.admit();
    const before = canonical_json(h.workflow);
    expect(() => h.run({ kind: "CANCEL_UNATTEMPTED_REQUEST", payload: { requestId, reason: "Not the requester." } }, { actorId: "unrelated-user", isAdministrator: false })).toThrow(/requester or case administrator/);
    expect(canonical_json(h.workflow)).toBe(before);
  });
  it("does not let even an administrator cancel a potentially attempted instruction", () => {
    const h = new RequestHarness(); const requestId = h.admit(); h.claim(requestId);
    const before = canonical_json(h.workflow);
    expect(() => h.run({ kind: "CANCEL_UNATTEMPTED_REQUEST", payload: { requestId, reason: "Cannot assume no attempt." } }, { actorId: "other-admin", isAdministrator: true })).toThrow(/unattempted READY/);
    expect(canonical_json(h.workflow)).toBe(before);
    expect(projectRequests(h.workflow)[0]?.reservedAmountCents).toBe(600);
  });
});
