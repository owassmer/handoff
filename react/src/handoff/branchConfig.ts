/** The approved persistent Demo uses Main. Omit the branch parameter; never fall back from a missing branch. */
export const HANDOFF_BRANCH: string | undefined = undefined;

/** Deployment settings only; people, budgets and progress always come from the server. */
export const handoffDeployment = {
  workspaceId: import.meta.env.VITE_HANDOFF_WORKSPACE_ID,
  functionVersion: import.meta.env.VITE_HANDOFF_FUNCTION_VERSION,
  actionFunctionVersion: import.meta.env.VITE_HANDOFF_ACTION_FUNCTION_VERSION,
  changeFunctionRid: import.meta.env.VITE_HANDOFF_CHANGE_FUNCTION_RID,
  acceptFunctionRid: import.meta.env.VITE_HANDOFF_ACCEPT_FUNCTION_RID,
  messageFunctionRid: import.meta.env.VITE_HANDOFF_MESSAGE_FUNCTION_RID,
};
