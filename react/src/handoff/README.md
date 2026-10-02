# Handoff frontend

React app for property managers running move-outs with Handoff. It reads one workspace through the published
query functions `listHandoffs`, `getHandoffWorkspace` and `getHandoffChange`, and changes it only through the
Actions Send message, Change work plan and Accept work plan.

- `gateway.ts`: the only code that calls Foundry. Exact function versions come from `branchConfig.ts` and the
  `.env.*` files.
- `contracts.ts`: validates every response before the screens see it.
- `state.ts`: reads, drafts, and change confirmation.
- `App.tsx`, `Decision.tsx`, `Work.tsx`, `SidePanel.tsx`, `DocumentDialog.tsx`: the screens. See `INTEGRATION.md`.

Run `npm test`, `npm run typecheck`, `npm run lint` and `npm run build` before a release. A tag publishes the site.
