/** Versioned synthetic-only Phase B configuration. No legal activation. */
import type { SafetyProfile } from "./types.js";

export interface PhaseBSafetyProfile extends SafetyProfile {}

export interface ReviewRuleRelease {
  schemaVersion: string;
  ruleReleaseId: string;
  sourceRuleReleaseId: string;
  codeVersion: string;
  status: string;
  implementationStatus: string;
  legalReviewStatus: string;
  allowLiveUse: boolean;
  allowedOrigins: string[];
  ordinaryPeriodDays: number;
  finalPeriodDays: number;
  timeZone: string;
  interimMoneyPolicy: string;
  missingAddressPolicy: string;
  legalCompletionPolicy: string;
}
