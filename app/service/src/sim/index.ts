import type { Queryable } from "../db.js";
import { SimCollector } from "./collector.js";
import { SimMaintenance } from "./maintenance.js";
import { SimPayments } from "./payments.js";
import type { SimTimer } from "./timers.js";
import { SimUtilities } from "./utilities.js";
import { SimVendors } from "./vendors.js";

/** Every imitated system that keeps timers, by name. */
export const timerHandlers: Record<string, (q: Queryable, t: SimTimer) => Promise<void>> = {
  payments: SimPayments.onTimer,
  utilities: SimUtilities.onTimer,
  maintenance: SimMaintenance.onTimer,
  vendors: SimVendors.onTimer,
  collector: SimCollector.onTimer,
};

export { SimCollector } from "./collector.js";
export { SimLedger, seedLedger } from "./ledger.js";
export { SimMail } from "./mail.js";
export { SimMaintenance } from "./maintenance.js";
export { SimPayments } from "./payments.js";
export { readScenario, setScenario } from "./scenarios.js";
export { SimUtilities } from "./utilities.js";
export { SimVendors } from "./vendors.js";
