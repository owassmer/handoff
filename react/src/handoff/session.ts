import type { PublicOauthClient } from "@osdk/oauth";
import { restartSignIn } from "./signIn";
import type { HandoffStore } from "./state";

type AccessFailure = "signed-out" | "permission" | "connection" | "sign-in-failed";
interface SessionState {
  store?: HandoffStore;
  loading: boolean;
  failed: boolean;
  failure?: AccessFailure;
  activity?: "checking" | "signing-in";
}
function accessFailure(error: unknown): AccessFailure {
  // Platform SDK packages can carry different error-class versions. Inspect only
  // the documented public error fields, never messages, parameters or credentials.
  if (typeof error === "object" && error !== null) {
    if (
      ("errorName" in error && error.errorName === "ApiUsageDenied") ||
      ("statusCode" in error && error.statusCode === 403) ||
      ("errorCode" in error && error.errorCode === "PERMISSION_DENIED")
    ) {
      return "permission";
    }
    if (
      ("statusCode" in error && error.statusCode === 401) ||
      ("errorCode" in error && error.errorCode === "UNAUTHORIZED")
    ) {
      return "signed-out";
    }
  }
  return "connection";
}
/** Identity is read from the signed-in session, never provided to an action by the caller. */
export class HandoffSession {
  private state: SessionState = { loading: true, failed: false, activity: "checking" };
  private store?: HandoffStore;
  private user?: string;
  private listeners = new Set<() => void>();
  private request?: Promise<void>;
  private signInRequest?: Promise<void>;
  private generation = 0;
  constructor(
    private readonly auth: PublicOauthClient,
    private readonly currentUser: () => Promise<string>,
    private readonly createStore: (user: string) => HandoffStore,
  ) {}
  getSnapshot = () => this.state;
  private emit() {
    this.listeners.forEach((fn) => fn());
  }
  private forgetIdentity() {
    this.generation++;
    this.request = undefined;
    this.store?.dispose();
    this.store = undefined;
    this.user = undefined;
  }
  private signedOut = () => {
    if (this.signInRequest) {
      // Explicit reauthorization already hid and cleared the previous identity.
      return;
    }
    this.forgetIdentity();
    this.state = { loading: false, failed: true, failure: "signed-out" };
    this.emit();
  };
  private refreshed = () => {
    void this.verify();
  };
  private signedIn = () => {
    if (this.signInRequest) {
      return;
    }
    // An older identity read must not win after a new sign-in event.
    this.generation++;
    this.request = undefined;
    this.state = { loading: true, failed: false, activity: "checking" };
    void this.verify();
  };
  subscribe = (fn: () => void) => {
    this.listeners.add(fn);
    if (this.listeners.size === 1) {
      this.auth.addEventListener("refresh", this.refreshed);
      this.auth.addEventListener("signIn", this.signedIn);
      this.auth.addEventListener("signOut", this.signedOut);
      void this.verify();
    }
    return () => {
      this.listeners.delete(fn);
      if (!this.listeners.size) {
        this.auth.removeEventListener("refresh", this.refreshed);
        this.auth.removeEventListener("signIn", this.signedIn);
        this.auth.removeEventListener("signOut", this.signedOut);
      }
    };
  };
  signIn = (): Promise<void> => {
    if (this.signInRequest) {
      return this.signInRequest;
    }
    this.forgetIdentity();
    this.state = { loading: true, failed: false, activity: "signing-in" };
    this.signInRequest = Promise.resolve()
      .then(() => restartSignIn(this.auth))
      .then(() => this.checkIdentity())
      .catch(() => {
        this.state = { loading: false, failed: true, failure: "sign-in-failed" };
        this.emit();
      })
      .finally(() => {
        this.signInRequest = undefined;
      });
    this.emit();
    return this.signInRequest;
  };
  verify = (): Promise<void> => this.signInRequest ?? this.checkIdentity();
  private checkIdentity(): Promise<void> {
    if (this.request) {
      return this.request;
    }
    const generation = this.generation;
    // Preserve the mounted work view on an ordinary refresh of the same person.
    this.state = {
      ...this.state,
      loading: true,
      failed: false,
      failure: undefined,
      activity: "checking",
    };
    this.request = Promise.resolve()
      .then(this.currentUser)
      .then((user) => {
        if (generation !== this.generation) {
          return;
        }
        if (!user) {
          throw new Error();
        }
        if (user !== this.user || !this.store) {
          this.store?.dispose();
          this.user = user;
          this.store = this.createStore(user);
        } else {
          void this.store.refresh();
        }
        this.state = { store: this.store, loading: false, failed: false };
      })
      .catch((error: unknown) => {
        if (generation === this.generation) {
          const failure = accessFailure(error);
          if (failure === "permission" || failure === "signed-out") {
            this.store?.dispose();
            this.store = undefined;
            this.user = undefined;
          }
          this.state = { loading: false, failed: true, failure };
        }
      })
      .finally(() => {
        if (generation === this.generation) {
          this.request = undefined;
          this.emit();
        }
      });
    this.emit();
    return this.request;
  }
}
