import type { Mail } from "../adapters/mail.js";
import type { Payments } from "../adapters/payments.js";
import type { ActionSpec } from "../gateway.js";
import { issueRefund } from "./issueRefund.js";
import { sendMessage } from "./sendMessage.js";

export interface Adapters {
  mail: Mail;
  payments: Payments;
}

export function standardActions(a: Adapters): Array<ActionSpec<any>> {
  return [sendMessage(a.mail), issueRefund(a.payments)];
}
