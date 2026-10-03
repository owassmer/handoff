import type { Collector } from "../adapters/collector.js";
import type { Ledger } from "../adapters/ledger.js";
import type { Mail } from "../adapters/mail.js";
import type { Maintenance } from "../adapters/maintenance.js";
import type { Payments } from "../adapters/payments.js";
import type { UtilityBiller } from "../adapters/utilities.js";
import type { Vendors } from "../adapters/vendors.js";
import type { ActionSpec } from "../gateway.js";
import { adjustCollector, placeWithCollector } from "./collectorActions.js";
import { createWorkOrder } from "./createWorkOrder.js";
import { issueRefund } from "./issueRefund.js";
import { postToLedger } from "./postToLedger.js";
import { requestFinalBills } from "./requestFinalBills.js";
import { sendMessage } from "./sendMessage.js";
import { placeVendorOrder, requestQuote } from "./vendorWork.js";

/** One interface per outside system. A simulated world passes imitations; production passes the real ones. */
export interface Adapters {
  mail: Mail;
  payments: Payments;
  ledger: Ledger;
  utilities: UtilityBiller;
  maintenance: Maintenance;
  vendors: Vendors;
  collector: Collector;
}

export function standardActions(a: Adapters): Array<ActionSpec<any>> {
  return [
    sendMessage(a.mail),
    issueRefund(a.payments),
    postToLedger(a.ledger),
    requestFinalBills(a.utilities),
    createWorkOrder(a.maintenance),
    requestQuote(a.vendors),
    placeVendorOrder(a.vendors),
    placeWithCollector(a.collector),
    adjustCollector(a.collector),
  ];
}
