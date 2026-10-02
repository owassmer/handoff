import { createBrowserRouter } from "react-router-dom";
import { OsdkProvider } from "@osdk/react";
import AuthCallback from "@/AuthCallback";
import client from "@/client";
import { HandoffCaseRoute, HandoffListPage, HandoffNotFound } from "@/handoff/App";
import { HandoffRouteError } from "@/handoff/Boundary";
import { CalendarPage } from "@/handoff/Calendar";
import { HandoffConnectionPage } from "@/handoff/Connection";
import { CaseControlsRoute } from "@/handoff/Controls";

export const router = createBrowserRouter(
  [
    {
      element: (
        <OsdkProvider client={client}>
          <HandoffConnectionPage />
        </OsdkProvider>
      ),
      errorElement: <HandoffRouteError />,
      children: [
        { path: "/", element: <HandoffListPage /> },
        { path: "/handoffs/:handoffId", element: <HandoffCaseRoute /> },
        // Admin-only, unlinked: runs Resume handoff back to back for testing.
        { path: "/handoffs/:handoffId/controls", element: <CaseControlsRoute /> },
        { path: "/calendar", element: <CalendarPage /> },
        { path: "*", element: <HandoffNotFound /> },
      ],
    },
    { path: "/auth/callback", element: <AuthCallback />, errorElement: <HandoffRouteError /> },
  ],
  { basename: import.meta.env.BASE_URL },
);
