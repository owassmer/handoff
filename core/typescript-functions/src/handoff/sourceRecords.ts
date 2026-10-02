import { sourceDetails } from "./sourceAccess.js";
import type { DeliveryContext, DeliveryRecords } from "./deliveryRecords.js";
import { recordExistingJob, recordInspection, recordInvoice, recordQuote } from "./deliveryRecords.js";
import type { ExistingJob, InspectionReport, SupplierInvoice } from "./deliveryContracts.js";
import type { HandoffDetails } from "./workDetails.js";
import { details, parseDetails, words } from "./values.js";

/** Recognize imported business records without inventing Handoff orders or retroactive approvals. */
export async function recognizeSourceRecord(context: DeliveryContext, world: HandoffDetails, records: DeliveryRecords): Promise<boolean> {
  for (const document of world.documents) {
    if (!document.detailsJson) continue;
    const types = { Quote: "offer", "Job record": "job", Inspection: "report", Invoice: "invoice" } as const;
    const kind = document.kind as keyof typeof types;
    if (!Object.hasOwn(types, kind)) continue;
    const value = sourceDetails(document.detailsJson);
    if (typeof value !== "object" || !value || !Object.hasOwn(value, types[kind])) continue;
    const envelope = details(value, [types[kind]], kind === "Quote" ? ["providerDocumentId", "serviceId", "providerSourceVersion", "sourcePassages"] : [], "Supporting business record");
    const raw = envelope[types[kind]];
    if (typeof raw !== "object" || raw === null || Array.isArray(raw)) continue;
    const input = { ...raw, sourceSystem: document.sourceSystem ?? "Received document", sourceRecordId: kind === "Quote" ? `${document.sourceRecordId ?? document.documentId}:${document.sourceVersion ?? "1"}` : document.sourceRecordId ?? document.documentId, sourceDocumentId: document.documentId };
    if (kind === "Quote" && !records.quotes.some((row) => row.sourceDocumentId === document.documentId)) {
      await recordQuote(context, input); return true;
    }
    if (kind === "Job record" && !records.jobs.some((row) => row.sourceDocumentId === document.documentId)) {
      // Each called boundary validates all fields before making an edit.
      await recordExistingJob(context, input as unknown as ExistingJob); return true;
    }
    if (kind === "Inspection" && !records.inspections.some((row) => row.sourceDocumentId === document.documentId)) {
      await recordInspection(context, input as unknown as InspectionReport); return true;
    }
    if (kind === "Invoice" && !records.invoices.some((row) => row.sourceDocumentId === document.documentId)) {
      await recordInvoice(context, input as unknown as SupplierInvoice); return true;
    }
  }
  return false;
}
