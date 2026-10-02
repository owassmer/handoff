import { Suspense } from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router-dom";
import { HandoffBoundary } from "@/handoff/Boundary";
import { router } from "@/router";
import "./handoff/global.css";

const rootElement = document.getElementById("root");
if (!rootElement) {
  throw new Error("Handoff couldn’t open. Please reopen the page.");
}

ReactDOM.createRoot(rootElement).render(
  <HandoffBoundary>
    <Suspense
      fallback={
        <div className="loading" role="status">
          Opening Handoff…
        </div>
      }
    >
      <RouterProvider router={router} />
    </Suspense>
  </HandoffBoundary>,
);
