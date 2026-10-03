/** The operator's in-house maintenance system. Completion, hours and rate arrive as events. */
export type WorkCategory = "inspection" | "paint" | "cleaning" | "repair" | "other";

export interface WorkOrderRequest {
  caseId: string;
  unitRef: string;
  category: WorkCategory;
  description: string;
}

export interface WorkOrder {
  ref: string;
  status: "open" | "scheduled" | "in_progress" | "completed" | "cancelled";
  scheduledFor: string | null;
  completedAt: string | null;
  technician: string | null;
  hours: number | null;
  hourlyRateCents: number | null;
  materialsCents: number | null;
}

export interface Maintenance {
  createWorkOrder(r: WorkOrderRequest, key: string): Promise<WorkOrder>;
  find(key: string): Promise<WorkOrder | null>;
}
