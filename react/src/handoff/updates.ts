import { useEffect, useRef, useState } from "react";
import type { HandoffWorkspace } from "./contracts";

export type UpdateTab = "money" | "messages" | "timeline" | "calendar" | "documents";
export interface Toast {
  text: string;
  more: number;
  tab: UpdateTab;
}
/** Activity that restates the operator's own action; the operator already knows. */
const OWN = ["Message received", "Work plan accepted", "Work plan changed"];
const AGENT = [
  "Handoff progressed",
  "Handoff next step",
  "Work plan ready",
  "Recommendation unavailable",
  "Work can't be ordered",
];

function keysOf(data: HandoffWorkspace): Record<UpdateTab, string[]> {
  return {
    money: [
      ...data.invoices.map((i) => i.id),
      ...data.quotes.map((q) => `${q.id}:${q.status}`),
      ...data.payments.map((p) => `${p.id}:${p.status}`),
    ],
    messages: data.messages
      .filter((m) => m.direction === "Incoming" || m.direction === "Outgoing")
      .map((m) => m.id),
    timeline: data.activity.map((a) => a.id),
    calendar: data.jobs.map((j) => `${j.id}:${j.appointmentAt ?? ""}`),
    documents: data.documents.map((d) => d.id),
  };
}

/**
 * What changed since the last read, for tabs the operator isn't looking at: a dot on each such tab and one toast
 * naming the newest step (Linear/Vercel pattern). Nothing is flagged on the first load.
 */
export function useUpdates(data: HandoffWorkspace | undefined, tab: string) {
  const previous = useRef<Record<UpdateTab, Set<string>> | null>(null);
  const [unseen, setUnseen] = useState<Partial<Record<UpdateTab, boolean>>>({});
  const [toast, setToast] = useState<Toast>();
  useEffect(() => {
    if (!data) {
      return;
    }
    const keys = keysOf(data);
    const before = previous.current;
    previous.current = Object.fromEntries(
      Object.entries(keys).map(([k, v]) => [k, new Set(v)]),
    ) as Record<UpdateTab, Set<string>>;
    if (!before) {
      return;
    }
    const changed = (Object.keys(keys) as UpdateTab[]).filter(
      (k) => k !== tab && keys[k].some((key) => !before[k].has(key)),
    );
    if (changed.length) {
      setUnseen((prev) => ({ ...prev, ...Object.fromEntries(changed.map((k) => [k, true])) }));
    }
    if (tab === "timeline") {
      return;
    }
    const fresh = data.activity
      .filter((a) => !before.timeline.has(a.id) && !OWN.includes(a.title))
      .sort((a, b) => a.at.localeCompare(b.at));
    const newest = fresh[fresh.length - 1];
    if (!newest) {
      return;
    }
    const text = (AGENT.includes(newest.title) ? newest.detail : newest.title) || newest.title;
    setToast((prev) => ({
      text: text.length > 140 ? `${text.slice(0, 137).trimEnd()}…` : text,
      more: (prev ? prev.more + 1 : 0) + fresh.length - 1,
      tab: "timeline",
    }));
  }, [data, tab]);
  useEffect(() => {
    setUnseen((prev) => (prev[tab as UpdateTab] ? { ...prev, [tab]: false } : prev));
    if (tab === "timeline") {
      setToast(undefined);
    }
  }, [tab]);
  return { unseen, toast, dismiss: () => setToast(undefined) };
}
