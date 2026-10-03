/**
 * Sign in with ChatGPT, ChatGPT plan usage for open-source and locally hosted apps.
 * Source: https://developers.openai.com/siwc/token-sharing-open-source (read October 3, 2026).
 *
 * This self-serve flow is documented for open-source and locally hosted apps. Offering ChatGPT plan
 * usage in a paid or remotely hosted app needs OpenAI's interest form; this code is for development.
 */
export const OPENAI_AUTH = {
  issuer: "https://auth.openai.com",
  authorizeEndpoint: "https://auth.openai.com/api/accounts/authorize",
  tokenEndpoint: "https://auth.openai.com/api/accounts/oauth/token",
  discovery: "https://auth.openai.com/.well-known/openid-configuration",
  jwksUri: "https://auth.openai.com/.well-known/jwks.json",
} as const;

/** The resource the tokens are for, and the API they are sent to. */
export const API_RESOURCE = "https://api.openai.com/v1";

/** The first-time registration entrypoint. Never saved, never used for token exchange. */
export const DYNAMIC_CLIENT = "dynamic_agent_client";

/** The scope that permits using the user's ChatGPT plan. A valid ID token alone does not. */
export const PLAN_SCOPE = "chatgpt.tokens.use.direct";

export const REQUESTED_SCOPES = ["openid", "profile", "email", "offline_access", "resource.invoke", PLAN_SCOPE] as const;

/** Display name offered at first registration; the user may edit it. Used consistently across installations. */
export const AGENT_NAME = "Handoff";

/** Loopback callback. Only the port may vary between sign-ins; scheme, host and path never do. */
export const CALLBACK_HOST = "127.0.0.1";
export const CALLBACK_PATH = "/auth/callback";
export const DEFAULT_CALLBACK_PORT = 1455;

/** Codes meaning a refresh token can no longer be used and the user must sign in again. */
export const UNUSABLE_REFRESH_CODES = new Set([
  "invalid_grant", "invalid_refresh_token", "token_expired", "refresh_token_expired", "refresh_token_invalidated", "refresh_token_reused",
]);
