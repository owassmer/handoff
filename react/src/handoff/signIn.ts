import type { PublicOauthClient } from "@osdk/oauth";

/** Only for an explicit sign-in click on a work page, never for the OAuth callback. */
async function signInFromWorkPage(auth: PublicOauthClient) {
  try {
    return await auth.signIn();
  } catch (error) {
    // OAuth 1.14 leaves completed PKCE state until a later attempt consumes it.
    // Away from the callback, this exact failure means the SDK has removed it.
    // Let the SDK start a fresh request once; never clear its storage ourselves.
    if (
      error instanceof Error &&
      error.name === "OperationProcessingError" &&
      error.message === 'response parameter "state" missing'
    ) {
      return auth.signIn();
    }
    throw error;
  }
}

/** Public OAuth methods only: a refresh of the old grant is not a fresh authorization. */
export async function restartSignIn(auth: PublicOauthClient): Promise<void> {
  if (!auth.getTokenOrUndefined()) {
    // May redirect immediately. If it returns, the SDK restored an existing session.
    // The SDK requires an established session before signOut can revoke it.
    await signInFromWorkPage(auth);
  }
  await auth.signOut();
  await signInFromWorkPage(auth);
}
