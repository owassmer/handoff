import { useEffect, useRef } from "react";
import type { HandoffWorkspace } from "./contracts";
import { shortTime } from "./format";
import { useHandoffStore } from "./hooks";
import { replyExpected } from "./model";
import { useArrivals, useFirstSeen, useNow } from "./motion";
import { conversationThread } from "./view";

/** After this long without a reply, say plainly that it comes with Handoff's next step. */
const REPLY_WAIT_MS = 120_000;

function Conversation({
  data,
  stale,
  focus,
}: {
  data: HandoffWorkspace;
  stale: boolean;
  focus: number;
}) {
  const store = useHandoffStore();
  const id = data.handoff.id;
  const input = useRef<HTMLTextAreaElement>(null);
  const end = useRef<HTMLDivElement>(null);
  const draft = store.messageDraft(id);
  const pending = store.pending(id);
  const busy = store.isSending(id) || Boolean(pending);
  const stalePlan =
    draft && (draft.planId !== data.workPlan?.id || draft.revision !== data.workPlan?.revision);
  const thread = conversationThread(data);
  const arrived = useArrivals(thread.map((m) => m.id));
  // Intercom/Slack pattern: sending, then sent, then a typing indicator until the saved reply replaces it.
  const lastMine = [...thread].reverse().find((m) => m.who === "You");
  const waiting = !busy && replyExpected(data);
  const since = useFirstSeen(waiting ? lastMine?.id : undefined);
  const now = useNow(5000, waiting);
  const late = waiting && since !== undefined && now - since > REPLY_WAIT_MS;
  const sendingText = busy ? draft?.value.trim() : undefined;
  const sending = Boolean(sendingText);
  useEffect(() => {
    if (focus) {
      input.current?.focus();
    }
  }, [focus]);
  useEffect(() => {
    end.current?.scrollIntoView?.({ block: "end" });
  }, [thread.length, waiting, sending]);
  return (
    <>
      <div className="panel">
        <div className="thread">
          {thread.map((m) => (
            <div
              className={`bubble${m.who === "You" ? " me" : ""}${arrived.has(m.id) ? " arrive" : ""}`}
              key={m.id}
            >
              <div className="meta">
                {m.who} · {shortTime(m.at)}
                {waiting && m.id === lastMine?.id && " · Sent"}
              </div>
              <div className="body">{m.body}</div>
            </div>
          ))}
          {sendingText && (
            <div className="bubble me sending">
              <div className="meta">You · Sending…</div>
              <div className="body">{sendingText}</div>
            </div>
          )}
          {waiting && (
            <div className="bubble typing" role="status">
              <div className="meta">Handoff</div>
              {late ? (
                <div className="body faint">Handoff will answer after its next step.</div>
              ) : (
                <div className="body">
                  <span className="dots" aria-hidden="true">
                    <i />
                    <i />
                    <i />
                  </span>
                  <span className="sr-only">Handoff is replying</span>
                </div>
              )}
            </div>
          )}
          {!thread.length && (
            <p className="faint">Ask a question or describe a change. Handoff answers here.</p>
          )}
          <div ref={end} />
        </div>
      </div>
      <form
        className="composer"
        onSubmit={(e) => {
          e.preventDefault();
          void store.sendMessage(data);
        }}
      >
        <label className="sr-only" htmlFor="composer">
          Message Handoff
        </label>
        <textarea
          id="composer"
          ref={input}
          className="textarea"
          placeholder="Ask Handoff or describe a change to the plan"
          value={draft?.value ?? ""}
          disabled={!data.permissions.canWork || busy}
          onChange={(e) => store.editMessage(data, e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
              e.preventDefault();
              void store.sendMessage(data);
            }
          }}
        />
        <div className="composer-row">
          <span className="faint" style={{ fontSize: 12 }}>
            {busy && !sendingText
              ? "Sending…"
              : stalePlan
                ? "The plan changed. Review it before sending."
                : ""}
          </span>
          {stalePlan ? (
            <button type="button" className="btn" onClick={() => store.reviewMessage(data)}>
              I’ve reviewed it
            </button>
          ) : (
            <button
              type="submit"
              className="btn primary"
              disabled={!draft?.value.trim() || busy || stale || !data.permissions.canWork}
            >
              Send
            </button>
          )}
        </div>
      </form>
    </>
  );
}

/** Ask Handoff stays beside every tab, and collapses to a rail; the draft is kept in the store. */
export function ChatDock({
  data,
  stale,
  focus,
  collapsed,
  onToggle,
}: {
  data: HandoffWorkspace;
  stale: boolean;
  focus: number;
  collapsed: boolean;
  onToggle(): void;
}) {
  if (collapsed) {
    return (
      <aside className="dock collapsed" aria-label="Ask Handoff">
        <button type="button" className="dock-rail" onClick={onToggle} aria-expanded="false">
          Ask Handoff
        </button>
      </aside>
    );
  }
  return (
    <aside className="dock" aria-label="Ask Handoff">
      <div className="dock-head">
        <h2>Ask Handoff</h2>
        <button type="button" className="btn quiet" onClick={onToggle} aria-expanded="true">
          Hide
        </button>
      </div>
      <Conversation data={data} stale={stale} focus={focus} />
    </aside>
  );
}
