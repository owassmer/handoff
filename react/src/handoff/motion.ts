import { type RefObject, useEffect, useLayoutEffect, useRef, useState } from "react";

/** How long an arrival stays marked; matches the highlight fade in handoff.css. */
export const ARRIVAL_MS = 1600;

/** The current time, re-rendering every `ms` while `active`. */
export function useNow(ms: number, active = true): number {
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    if (!active) {
      return undefined;
    }
    setNow(Date.now());
    const timer = setInterval(() => setNow(Date.now()), ms);
    return () => clearInterval(timer);
  }, [ms, active]);
  return now;
}

/**
 * Keys that appeared since the previous render, marked for ARRIVAL_MS. The first set of keys is the page as it
 * loaded, not an arrival, so nothing is marked until the data changes. Keys encode what changed, e.g. a job id plus
 * its stage, so a changed stage reads as an arrival too.
 */
export function useArrivals(keys: readonly string[]): ReadonlySet<string> {
  const previous = useRef<Set<string> | null>(null);
  const [marked, setMarked] = useState<ReadonlySet<string>>(() => new Set());
  const signature = keys.join("\u0000");
  useEffect(() => {
    const current = new Set(keys);
    const before = previous.current;
    previous.current = current;
    if (!before) {
      return undefined;
    }
    const fresh = [...current].filter((key) => !before.has(key));
    if (!fresh.length) {
      return undefined;
    }
    setMarked((prev) => new Set([...prev, ...fresh]));
    const timer = setTimeout(
      () => setMarked((prev) => new Set([...prev].filter((key) => !fresh.includes(key)))),
      ARRIVAL_MS,
    );
    return () => clearTimeout(timer);
    // The signature stands for the key list.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [signature]);
  return marked;
}

/** The time, in ms since page load, that each key was first seen. Used to age a wait the case clock can't measure. */
export function useFirstSeen(key: string | undefined): number | undefined {
  const seen = useRef(new Map<string, number>());
  if (key && !seen.current.has(key)) {
    seen.current.set(key, Date.now());
  }
  return key ? seen.current.get(key) : undefined;
}

/** "in 40 s", "in 3 min". */
export function countdown(ms: number): string {
  const seconds = Math.ceil(ms / 1000);
  return seconds < 60 ? `in ${seconds} s` : `in ${Math.ceil(seconds / 60)} min`;
}

/**
 * Rows that change place glide to their new position instead of jumping (FLIP). Children carry `data-flip` keys.
 * Movement is skipped under reduced motion.
 */
export function useFlip(container: RefObject<HTMLElement | null>, signature: string) {
  const last = useRef(new Map<string, number>());
  useLayoutEffect(() => {
    const root = container.current;
    if (!root) {
      return;
    }
    const reduce =
      typeof window.matchMedia === "function" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const now = new Map<string, number>();
    root.querySelectorAll<HTMLElement>("[data-flip]").forEach((el) => {
      const key = el.dataset.flip!;
      const top = el.getBoundingClientRect().top;
      now.set(key, top);
      const before = last.current.get(key);
      if (!reduce && before !== undefined && before !== top && typeof el.animate === "function") {
        el.animate([{ transform: `translateY(${before - top}px)` }, { transform: "none" }], {
          duration: 220,
          easing: "cubic-bezier(0.2, 0.7, 0.2, 1)",
        });
      }
    });
    last.current = now;
  }, [container, signature]);
}

/** How long a confirmation or update notice stays before closing itself. */
export const TRANSIENT_MS = 10_000;
/**
 * A transient message closes itself after `ms`, but not while the pointer or keyboard focus is on it; leaving restarts
 * the wait (Radix Toast, Sonner). Pass a changing `active` value to restart it for a new message.
 */
export function useAutoDismiss(active: unknown, onDismiss: () => void, ms = TRANSIENT_MS) {
  const [held, setHeld] = useState(false);
  const dismiss = useRef(onDismiss);
  useEffect(() => {
    dismiss.current = onDismiss;
  }, [onDismiss]);
  useEffect(() => {
    if (!active || held) {
      return undefined;
    }
    const timer = setTimeout(() => dismiss.current(), ms);
    return () => clearTimeout(timer);
  }, [active, held, ms]);
  return {
    onMouseEnter: () => setHeld(true),
    onMouseLeave: () => setHeld(false),
    onFocus: () => setHeld(true),
    onBlur: () => setHeld(false),
  };
}
