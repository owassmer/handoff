# Running Handoff's models on a ChatGPT plan

October 3, 2026. During development, Handoff's agent runs on the user's ChatGPT plan through OpenAI's Sign in with ChatGPT, not on a paid API. This follows OpenAI's guide for open-source and locally hosted apps: <https://developers.openai.com/siwc/token-sharing-open-source>.

> **What this is not.** OpenAI documents this self-serve flow for open-source and locally hosted apps. It does not approve a paid or remotely hosted product. Offering ChatGPT plan usage in Handoff as a commercial, hosted service needs OpenAI's [interest form](https://openai.com/form/sign-in-with-chatgpt-interest/) and whatever agreement follows. Handoff's repository is private and the product is commercial, so whether even development use fits OpenAI's terms is for Owen to confirm.

## Settings

| Variable | Meaning |
|---|---|
| `HANDOFF_MODEL_PROVIDER` | `openai_chatgpt` (default): billed to the ChatGPT plan. `openrouter`: a paid API, chosen explicitly. `HANDOFF_<ROLE>_PROVIDER` overrides it for one role. |
| `HANDOFF_<ROLE>_MODEL` | The model for a role (`COORDINATOR`, `TENANT`, `ANALYST`). For the ChatGPT plan, a slug from `npm run chatgpt -- models`. Model names are never written into code. |
| `HANDOFF_ALLOW_PAID_FALLBACK` | Only the exact value `true` lets a failed ChatGPT plan request retry on OpenRouter with `HANDOFF_<ROLE>_FALLBACK_MODEL`. When it is anything else, including unset, no failure ever falls back to a paid provider. The failures this covers are missing authorization, ineligibility, an exhausted usage limit, and provider errors. |
| `HANDOFF_CHATGPT_AUTH` | Where authorization comes from (see below): `stored` (default), `environment` or `injected`. |
| `HANDOFF_CHATGPT_HOME` | The credential folder for `stored`. Default `~/.config/handoff/chatgpt`. A folder inside a git repository is refused. |
| `HANDOFF_CHATGPT_ACCOUNT` | Which saved account to use, if not the active one. |

Jev is separate: its access, billing and model are unchanged and not configured here.

## Three ways to authorize, kept apart

1. **`stored`: the durable, renewable flow.** Use this on your own computer, or on a self-hosted VM you control.
   - Credentials are saved by the login helper, with owner-only files and atomic writes.
   - They are refreshed near expiry, under a lock, so two processes never spend the same rotating refresh token.
   - Refresh tokens last 30 days and renew on use.
2. **`environment`: an access token from the environment's settings.** Use this for a short test in a cloud session.
   - The token lives in `HANDOFF_CHATGPT_ACCESS_TOKEN`.
   - It cannot be renewed here, and lasts about an hour.
3. **`injected`: the environment's credential proxy adds the `Authorization` header.** The token never enters the session. Handoff sends no `Authorization` header and relies on the proxy to add it for `api.openai.com`.

## Setting up on your Mac (durable)

The sign-in redirects your browser to `http://127.0.0.1:<port>/auth/callback`. That address reaches only the computer running the browser, so this step must run on your Mac, never in a remote session.

```
git clone <the Handoff repository> && cd handoff/app && npm install
cd service
npm run chatgpt -- login          # opens "Continue with ChatGPT" in your browser
npm run chatgpt -- status         # account, plan permission, expiry; never prints tokens
npm run chatgpt -- models         # the model slugs your plan offers
HANDOFF_COORDINATOR_MODEL=<slug> npm run smoke:chatgpt
```

`login` first creates this computer's host ID: a key-thumbprint URI, created once and reused. On a first sign-in it registers Handoff with OpenAI under the name "Handoff" (you can rename it at approval). It then saves the issued client ID with the account. Before saving anything, it checks:
- the ID token's signature, issuer, audience and nonce;
- that the ChatGPT plan permission (`chatgpt.tokens.use.direct`) was actually granted.

If you decline that permission, the sign-in is kept but Handoff will not run inference on it. To ask again, run `npm run chatgpt -- login --label <label> --enable-plan`.

`npm run chatgpt -- logout` revokes the session and then clears the tokens. Usage and per-app limits are at <https://chatgpt.com/settings/usage>. On a Plus plan, the five-hour limit is shared with every other app using the plan.

## Testing from a Claude Code web session

1. On your Mac, after `login`, run `npm run chatgpt -- access-token --clipboard`. This copies the access token without printing it, and it expires within an hour.
2. In this environment's settings (the cloud environment menu in the session's title bar, then Edit), add the token. Never paste it into the chat. Two options:
   - **Injected (preferred).** Use this if the API credentials section can attach `Authorization: Bearer <token>` to requests for `api.openai.com`. Then set `HANDOFF_CHATGPT_AUTH=injected`. The token then never enters the session.
   - **Environment variable.** Otherwise, add an environment variable `HANDOFF_CHATGPT_ACCESS_TOKEN` with the token, and set `HANDOFF_CHATGPT_AUTH=environment`.
3. Also set `HANDOFF_COORDINATOR_MODEL=<slug>`. A new session picks up the settings.
4. In the session, run `npm run smoke:chatgpt` from `app/service`.

The command refuses to run if the coordinator's provider is not `openai_chatgpt` or if paid fallback is allowed.

I could not see how this environment's proxy injects credentials from inside the session, so the injected path is built to the general mechanism (no header sent; the proxy adds it) and has not run against a real injected token.

## A self-hosted VM (later)

1. **Sign in on your Mac.** Complete the sign-in there.
2. **Move the session.** Run `npm run chatgpt -- export --label <label> --to <file>`, copy the file to the VM over SSH, then run `npm run chatgpt -- import <file>` there. Delete both copies of the transfer file afterwards.
3. **Leave refreshes to the VM.** The VM keeps its own host ID, and from then on it owns refreshes.

OpenAI notes that host-specific usage attribution and revocation of plan access for transferred sessions are not yet available.

## What is tested, and what still needs your authorization

**Tested here, without network or real credentials.** 43 tests cover:
- **The authorization request:**
  - every documented parameter, for a first registration and for a returning sign-in;
  - PKCE against RFC 7636's published example;
  - redaction of the ID-token hint.
- **The callback:**
  - state checked first;
  - declined consent, an incomplete registration and a mismatched client all refused.
- **The token endpoint:**
  - the exact code-exchange and refresh form fields, with no client secret;
  - classification of unusable refresh tokens.
- **ID-token checks:**
  - signature against a key set;
  - issuer, audience and nonce;
  - expiry;
  - a foreign signing key refused.
- **Plan permission:** honoured only with `chatgpt.tokens.use.direct`.
- **The full login flow:** a simulated browser calls the real loopback listener, covering:
  - a new registration;
  - a returning sign-in that keeps the saved client;
  - a different account refused without replacing anything;
  - permission declined;
  - permission not granted.
- **The credential store:**
  - owner-only folders and files and atomic writes;
  - refusal inside a repository;
  - one stable host ID.
- **Refresh:**
  - the documented request;
  - two "processes" racing a refresh spend the rotating token once;
  - an unusable session cleared while the registration is kept;
  - a temporary failure keeps the credentials;
  - renewal after a 401.
- **Moving and ending sessions:** export and import that keep the VM's host ID, and revocation on sign-out.
- **The Responses transport:**
  - the exact outgoing body: instructions, full history, text/image/file input, the tool namespace, `store: false`, `stream: true`, encrypted reasoning;
  - none of the unsupported fields;
  - exact replay of reasoning, messages and function calls;
  - tool results matched to call IDs;
  - no `Authorization` header in injected mode;
  - one retry after a 401;
  - classification of every documented error, including a usage limit that arrives mid-stream;
  - success only on `response.completed`.
- **Provider selection:** no paid fallback unless explicitly allowed, and never for a programming error.
- **The coordinator through LangGraph** on this transport against a scripted stream.

**Checked against the real API, October 3, with Owen's authorization:**
- Owen signed in on his Mac and placed the access token in this environment's API credentials.
- The proxy injects the header. A request to `GET /v1/models` with no Authorization header from the session returned 200, and the token never entered the session. The account's model list returned `gpt-6-astra`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna` and `gpt-5.5`.
- `npm run smoke:chatgpt` with `gpt-6-astra` completed a full coordinator wake on the plan. Over several model steps the route accepted the namespaced tools, parallel tool calls, tool results returned by call ID, and replayed encrypted reasoning. The gateway refused a message, and the model recovered from a malformed proposal by itself.

**Still untested:**
- a refresh in the stored flow;
- a self-hosted VM import;
- behavior at a usage limit.

An injected access token expires about an hour after it was issued and cannot be renewed in the session. When it does, run `access-token --clipboard` on the Mac again and update the environment's credential.
