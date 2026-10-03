import type { Queryable } from "../db.js";
import { SimPayments } from "./payments.js";
import type { SimTimer } from "./timers.js";

/** Every imitated system that keeps timers, by name. */
export const timerHandlers: Record<string, (q: Queryable, t: SimTimer) => Promise<void>> = {
  payments: SimPayments.onTimer,
};

export { SimMail } from "./mail.js";
export { SimPayments } from "./payments.js";
export { setScenario } from "./scenarios.js";
