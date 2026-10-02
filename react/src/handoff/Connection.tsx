import { useState, useSyncExternalStore } from "react";
import { Admin } from "@osdk/foundry";
import { useOsdkClient } from "@osdk/react";
import { auth, ontologyRid } from "../client";
import { HandoffHeader, HandoffLayout } from "./App";
import { handoffDeployment } from "./branchConfig";
import {
  HANDOFF_BRANCH,
  type HandoffConnection,
  createHandoffGateway,
  isConnected,
} from "./gateway";
import { HandoffContext } from "./hooks";
import { rememberReturnRoute } from "./returnRoute";
import { HandoffSession } from "./session";
import { HandoffStore } from "./state";

const connection: HandoffConnection = {
  ontologyRid,
  ...handoffDeployment,
};
function browserStorage(): Storage | undefined {
  try {
    return window.sessionStorage;
  } catch {
    return undefined;
  }
}
function SignedInHandoff() {
  const client = useOsdkClient();
  const [session] = useState(
    () =>
      new HandoffSession(
        auth,
        async () => {
          rememberReturnRoute();
          // Used only to isolate local drafts. The backend binds the actor on every query and action.
          const user = await Admin.Users.getCurrent(client);
          return user.id;
        },
        (user) =>
          new HandoffStore(
            createHandoffGateway(client, connection),
            browserStorage(),
            `handoff.changes:${connection.ontologyRid}:${HANDOFF_BRANCH ?? "main"}:${connection.workspaceId}:${user}`,
          ),
      ),
  );
  const state = useSyncExternalStore(session.subscribe, session.getSnapshot);
  if (state.store) {
    return (
      <HandoffContext.Provider value={state.store}>
        <HandoffLayout />
      </HandoffContext.Provider>
    );
  }
  return (
    <div className="handoff-app">
      <HandoffHeader />
      <main className="page">
        <section className="empty" aria-busy={state.loading}>
          <h1>
            {state.failure === "permission"
              ? "Handoff needs access"
              : "Let’s get you back to your work"}
          </h1>
          {state.loading ? (
            <p role="status">
              {state.activity === "signing-in" ? "Opening sign-in…" : "Checking your access…"}
            </p>
          ) : (
            <p role="alert">
              {state.failure === "permission"
                ? "You’re signed in, but this app doesn’t have the access it needs. Ask your team to check access for Handoff, then try again. Signing in repeatedly won’t resolve missing access."
                : state.failure === "signed-out"
                  ? "Please sign in to return to your units."
                  : state.failure === "sign-in-failed"
                    ? "We couldn’t open sign-in. Check your connection and try signing in again. If this keeps happening, ask your team for help."
                    : "We couldn’t check your access. Check your connection and try again. If this keeps happening, ask your team for help."}
            </p>
          )}
          <div className="actions">
            <button
              type="button"
              className="btn primary"
              disabled={state.loading}
              onClick={() => {
                rememberReturnRoute();
                void session.signIn();
              }}
            >
              Sign in
            </button>
            <button
              type="button"
              className="btn"
              disabled={state.loading}
              onClick={() => {
                void session.verify();
              }}
            >
              Try again
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}
export function HandoffConnectionPage() {
  if (!isConnected(connection)) {
    return (
      <div className="handoff-app">
        <HandoffHeader />
        <main className="page">
          <section className="empty">
            <h1>Handoff isn’t available yet</h1>
            <p>
              Your team is finishing the connection to this workspace. Please check back shortly.
            </p>
            <button type="button" className="btn" onClick={() => window.location.reload()}>
              Check again
            </button>
          </section>
        </main>
      </div>
    );
  }
  return <SignedInHandoff />;
}
