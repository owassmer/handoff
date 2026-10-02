import { describe, expect, it } from "vitest";
import { HandoffQuote } from "@ontology/sdk";
import { selectedCost, selectedPriceIdentity, validateSelection } from "../proposal.js";
import { WorkspaceStore, proposedWork, seedQuotedWork, selectedWork } from "./workspaceSupport.js";

describe("quoted selection pricing identity", () => {
  function setup(): WorkspaceStore { const store = new WorkspaceStore(); seedQuotedWork(store); return store; }
  it("ignores order and narrative but retains the exact quoted total", () => {
    const store = setup(), quotes = store.all(HandoffQuote), selections = selectedWork();
    const rewritten = selections.map((line) => ({ ...line, scope: `Reviewed: ${line.scope}`, reason: "Same quoted work, clearer explanation." })).reverse();
    expect(selectedPriceIdentity(selections, quotes, "USD")).toBe(selectedPriceIdentity(rewritten, quotes, "USD"));
    expect(selectedCost(rewritten, quotes, "USD")).toBe("20500");
  });
  it("changes identity for an actual source price or currency change", () => {
    const store = setup(), quote = store.all(HandoffQuote)[0]!, selections = selectedWork();
    const initial = selectedPriceIdentity(selections, [quote], "USD");
    store.change(HandoffQuote, quote.quoteId, { linesJson: JSON.stringify([
      { lineId: "clean", description: "Kitchen clean", amountCents: "8001" },
      { lineId: "latch", description: "Adjust latch", amountCents: "12500" },
    ]), totalCents: "20501" });
    expect(selectedPriceIdentity(selections, store.all(HandoffQuote), "USD")).not.toBe(initial);
    store.change(HandoffQuote, quote.quoteId, { currency: "EUR" });
    expect(selectedPriceIdentity(selections, store.all(HandoffQuote), "EUR")).not.toBe(initial);
    expect(() => selectedPriceIdentity(selections, store.all(HandoffQuote), "USD")).toThrow("different currency");
  });
  it("keeps operator-input scope coverage validation strict", () => {
    const store = setup(), draft = { ...proposedWork(), selections: selectedWork() };
    expect(validateSelection(draft, store.all(HandoffQuote))).toBe(draft);
    expect(() => validateSelection({ ...draft, scope: [...draft.scope, "Unquoted roof replacement"] }, store.all(HandoffQuote))).toThrow("reviewed quote selection");
    expect(() => validateSelection({ ...draft, scope: [draft.scope[0]!] }, store.all(HandoffQuote))).toThrow("reviewed quote selection");
  });
  it("rejects duplicate prices, unknown lines and missing offers instead of treating them as free", () => {
    const store = setup(), quotes = store.all(HandoffQuote), selections = selectedWork();
    expect(() => selectedPriceIdentity([...selections, selections[0]!], quotes, "USD")).toThrow("once");
    expect(() => selectedPriceIdentity([{ ...selections[0]!, quoteLineId: "absent" }], quotes, "USD")).toThrow("not in this quote");
    expect(() => selectedPriceIdentity(selections, [], "USD")).toThrow("unavailable");
  });
});
