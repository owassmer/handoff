import { createContext, useContext, useSyncExternalStore } from "react";
import type { HandoffStore, ReadResource } from "./state";

export const HandoffContext = createContext<HandoffStore | null>(null);
export function useHandoffStore() {
  const store = useContext(HandoffContext);
  if (!store) {
    throw new Error("Handoff isn't available right now.");
  }
  useSyncExternalStore(store.subscribe, store.getSnapshot);
  return store;
}
export function useHandoffRead<T>(resource: ReadResource<T>) {
  const state = useSyncExternalStore(resource.subscribe, resource.getSnapshot);
  return { ...state, refresh: resource.fresh };
}
