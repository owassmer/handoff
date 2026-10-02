import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { auth } from "@/client";
import "./handoff/handoff.css";
import { takeReturnRoute } from "./handoff/returnRoute";

function AuthCallback() {
  const [failed, setFailed] = useState(false);
  const navigate = useNavigate();
  const completion = useRef<ReturnType<typeof auth.signIn>>();
  useEffect(() => {
    let active = true;
    // Share completion across repeated effects; consume the return route only once.
    // The SDK also deduplicates a pending signIn. Do not sign out on the callback.
    completion.current ??= Promise.resolve().then(() => auth.signIn());
    void completion.current
      .then(() => {
        if (active) {
          navigate(takeReturnRoute(), { replace: true });
        }
      })
      .catch(() => {
        if (active) {
          setFailed(true);
        }
      });
    return () => {
      active = false;
    };
  }, [navigate]);
  return (
    <div className="handoff-app">
      <main className="hf-main">
        <section className="hf-empty">
          <p className="hf-eyebrow">Handoff</p>
          {failed ? (
            <>
              <h1>We couldn’t finish signing you in</h1>
              <p>Please return to Handoff and try signing in again.</p>
              <button
                type="button"
                className="hf-button"
                onClick={() => navigate(takeReturnRoute(), { replace: true })}
              >
                Return to Handoff
              </button>
            </>
          ) : (
            <p role="status">Signing you in…</p>
          )}
        </section>
      </main>
    </div>
  );
}
export default AuthCallback;
