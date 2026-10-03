import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { type JWK, SignJWT, createLocalJWKSet, exportJWK, generateKeyPair } from "jose";
import { CredentialStore } from "../../src/llm/chatgpt/store.js";

export interface Recorded {
  url: string;
  method: string;
  headers: Record<string, string>;
  body: string;
}

type Handler = (req: Recorded) => Response | Promise<Response>;

/** A stand-in for OpenAI's auth and API hosts that records every request it receives. */
export class FakeOpenAI {
  readonly requests: Recorded[] = [];
  private readonly routes: Array<{ match: (r: Recorded) => boolean; handle: Handler }> = [];
  private readonly streams: Array<string | Response> = [];

  on(match: (r: Recorded) => boolean, handle: Handler): this {
    this.routes.push({ match, handle });
    return this;
  }

  /** Queue the next /v1/responses answers: an SSE body, or a whole Response for an error. */
  respond(...answers: Array<string | Response>): this {
    this.streams.push(...answers);
    return this;
  }

  readonly fetch = async (input: string | URL | Request, init?: RequestInit): Promise<Response> => {
    const url = typeof input === "string" ? input : input instanceof URL ? input.toString() : input.url;
    const headers: Record<string, string> = {};
    new Headers(init?.headers).forEach((v, k) => (headers[k] = v));
    const req: Recorded = { url, method: init?.method ?? "GET", headers, body: typeof init?.body === "string" ? init.body : "" };
    this.requests.push(req);
    for (const r of this.routes) if (r.match(req)) return r.handle(req);
    if (url === "https://api.openai.com/v1/responses") {
      const next = this.streams.shift();
      if (next === undefined) throw new Error("no scripted response left");
      return typeof next === "string" ? new Response(next, { status: 200, headers: { "content-type": "text/event-stream", "x-request-id": "req_test" } }) : next;
    }
    throw new Error(`unexpected request to ${url}`);
  };

  form(i: number): Record<string, string> {
    return Object.fromEntries(new URLSearchParams(this.requests[i]!.body));
  }

  bodies(url: string): Array<Record<string, any>> {
    return this.requests.filter((r) => r.url === url).map((r) => JSON.parse(r.body));
  }
}

export function sse(events: Array<Record<string, unknown>>): string {
  return events.map((e, i) => `event: ${e.type}\ndata: ${JSON.stringify({ sequence_number: i, ...e })}\n\n`).join("");
}

/** A completed response stream carrying these output items. */
export function completed(output: Array<Record<string, unknown>>, id = "resp_1"): string {
  return sse([
    { type: "response.created", response: { id, status: "in_progress", output: [] } },
    ...output.map((item, i) => ({ type: "response.output_item.done", output_index: i, item })),
    { type: "response.completed", response: { id, model: "test-model", status: "completed", output, usage: { input_tokens: 100, output_tokens: 20, total_tokens: 120 } } },
  ]);
}

export function fnCall(callId: string, name: string, args: Record<string, unknown>) {
  return { type: "function_call", id: `fc_${callId}`, call_id: callId, name, namespace: "handoff", arguments: JSON.stringify(args), status: "completed" };
}

export function reasoning(id: string) {
  return { type: "reasoning", id, summary: [], encrypted_content: `enc-${id}` };
}

export function message(text: string) {
  return { type: "message", id: "msg_1", role: "assistant", status: "completed", content: [{ type: "output_text", text, annotations: [] }] };
}

/** An OpenAI-like signing key for ID tokens, and its key set. */
export async function testSigner() {
  const { publicKey, privateKey } = await generateKeyPair("RS256", { extractable: true });
  const jwk: JWK = { ...(await exportJWK(publicKey)), kid: "test-key", alg: "RS256", use: "sig" };
  const jwks = createLocalJWKSet({ keys: [jwk] });
  const idToken = (claims: { sub?: string; aud: string; nonce: string; email?: string; iss?: string; expiresIn?: string }) =>
    new SignJWT({ nonce: claims.nonce, email: claims.email ?? "owner@example.com" })
      .setProtectedHeader({ alg: "RS256", kid: "test-key" })
      .setIssuer(claims.iss ?? "https://auth.openai.com")
      .setAudience(claims.aud)
      .setSubject(claims.sub ?? "user-123")
      .setIssuedAt()
      .setExpirationTime(claims.expiresIn ?? "1h")
      .sign(privateKey);
  return { jwks, idToken };
}

/** A credential folder in the system temp directory, outside any repository. */
export async function tempStore(): Promise<{ store: CredentialStore; cleanup: () => Promise<void> }> {
  const dir = await mkdtemp(join(tmpdir(), "handoff-chatgpt-"));
  return { store: new CredentialStore(join(dir, "creds")), cleanup: () => rm(dir, { recursive: true, force: true }) };
}

export function tokenJson(over: Record<string, unknown> = {}): Response {
  return Response.json({
    access_token: "at-1", refresh_token: "rt-1", id_token: "idt", token_type: "Bearer", expires_in: 3600,
    scope: "chatgpt.tokens.use.direct email offline_access openid profile resource.invoke", ...over,
  });
}
