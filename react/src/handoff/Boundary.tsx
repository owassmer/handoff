import { Component, type ReactNode } from "react";
import "./handoff.css";

export class HandoffBoundary extends Component<{ children: ReactNode }, { failed: boolean }> {
  state = { failed: false };
  static getDerivedStateFromError() {
    return { failed: true };
  }
  render() {
    return this.state.failed ? (
      <div className="handoff-app">
        <main className="page">
          <section className="empty" role="alert">
            <h1>Let’s reopen Handoff</h1>
            <p>Something interrupted this page. Reopen it to see the latest saved work.</p>
            <button type="button" className="btn" onClick={() => window.location.reload()}>
              Reopen
            </button>
          </section>
        </main>
      </div>
    ) : (
      this.props.children
    );
  }
}
export function HandoffRouteError() {
  return (
    <div className="handoff-app">
      <main className="page">
        <section className="empty" role="alert">
          <h1>We couldn’t open this page</h1>
          <p>Return to your units and try again.</p>
          <a className="btn" href={import.meta.env.BASE_URL}>
            Back to units
          </a>
        </section>
      </main>
    </div>
  );
}
