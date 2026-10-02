import ReactDOM from "react-dom/client";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { HandoffCaseRoute, HandoffLayout, HandoffListPage } from "@/handoff/App";
import type { Change, HandoffGateway, HandoffWorkspace } from "@/handoff/contracts";
import { readList, readWorkspace } from "@/handoff/contracts";
import "@/handoff/global.css";
import { HandoffContext } from "@/handoff/hooks";
import { HandoffStore } from "@/handoff/state";
import delivery from "./delivery.json";
import live from "./live.json";
import liveList from "./live_list.json";
import w9List from "./w9_list.json";
import w9a from "./w9_plan2.json";
import w9b from "./w9_orders.json";
import w9c from "./w9_repairplan.json";
import w9d from "./w9_stall.json";
import w9e from "./w9_end.json";
const SEQUENCE = [w9a, w9b, w9c, w9d, w9e] as unknown as HandoffWorkspace[];
import { CalendarPage } from "@/handoff/Calendar";
import list from "./list.json";
import plan from "./plan.json";

const state = new URLSearchParams(location.search).get("state") ?? "plan";
let current: HandoffWorkspace = structuredClone((state === "anim" || state === "steps" ? SEQUENCE[0] : state === "live" ? live : state === "delivery" ? delivery : plan) as unknown as HandoffWorkspace);
const ws = current.workspace.id;
const log: Change[] = [];
(window as unknown as { __changes: Change[] }).__changes = log;

const gateway: HandoffGateway = {
  async list() {
    const l = structuredClone(state === "anim" || state === "steps" ? w9List : state === "live" ? liveList : list) as { handoffs: { physicalProgress: string }[] };
    l.handoffs[0].physicalProgress = current.handoff.physicalProgress;
    return readList(JSON.stringify(l), ws);
  },
  async workspace(id) {
    return readWorkspace(JSON.stringify(current), ws, id);
  },
  async receipt(_id, commandId) {
    return { version: "2", commandId, status: "Not found", subjectId: null, kind: null, payloadHash: null, resultRevision: null, at: null };
  },
  async apply(change) {
    log.push(change);
    if (change.kind === "accept" && current.workPlan) {
      const d = structuredClone(delivery) as unknown as HandoffWorkspace;
      current = { ...d, jobs: [], invoices: [], payments: [], agent: { ...d.agent, status: "Arranging work", nextStep: "Commissioning Carroll Stair & Millwork and Feld Architecture." } };
    }
    return "saved";
  },
  async document() {
    return new Blob([await (await fetch("/preview/sample.pdf")).arrayBuffer()], { type: "application/pdf" });
  },
};
const store = new HandoffStore(gateway, window.sessionStorage, "preview", 0);
const router = createBrowserRouter([
  {
    element: (
      <HandoffContext.Provider value={store}>
        <HandoffLayout />
      </HandoffContext.Provider>
    ),
    children: [
      { path: "/preview.html", element: <HandoffListPage /> },
      { path: "/", element: <HandoffListPage /> },
      { path: "/handoffs/:handoffId", element: <HandoffCaseRoute /> },
      { path: "/calendar", element: <CalendarPage /> },
    ],
  },
]);
// ?state=steps reveals the rebuilt case one recorded step at a time: activity, messages and documents up to each step.
const base = SEQUENCE[3]!;
const times = [...new Set(base.activity.map((a) => a.at))].sort();
let cut = times.length - 12;
const upTo = (t: string): HandoffWorkspace => {
  const d = structuredClone(base);
  d.activity = d.activity.filter((a) => a.at <= t);
  d.messages = d.messages.filter((m) => m.createdAt <= t);
  d.payments = d.payments.filter((p) => p.requestedAt <= t);
  return d;
};
if (state === "steps") {
  current = upTo(times[cut]!);
  (window as unknown as { __step: () => void }).__step = () => {
    cut = Math.min(cut + 1, times.length - 1);
    current = upTo(times[cut]!);
    void store.refresh();
  };
}
// ?state=anim replays the rebuilt case's real snapshots, one every 6 s, to review motion.
if (state === "anim") {
  let step = 0;
  (window as unknown as { __step: () => void }).__step = () => {
    step = Math.min(step + 1, SEQUENCE.length - 1);
    current = structuredClone(SEQUENCE[step]!);
    void store.refresh();
  };
}
ReactDOM.createRoot(document.getElementById("root")!).render(<RouterProvider router={router} />);
