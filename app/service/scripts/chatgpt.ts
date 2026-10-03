/**
 * Sign in with ChatGPT for Handoff development. Run on the computer whose browser you use:
 *   npm run chatgpt -- login [--label L] [--port N] [--enable-plan]
 *   npm run chatgpt -- status
 *   npm run chatgpt -- models [--label L]
 *   npm run chatgpt -- access-token [--label L] (--clipboard | --stdout)
 *   npm run chatgpt -- export --label L --to FILE      (to move a session to a self-hosted VM over SSH)
 *   npm run chatgpt -- import FILE                     (on the VM; it keeps its own host id)
 *   npm run chatgpt -- logout [--label L]
 * Credentials live in HANDOFF_CHATGPT_HOME or ~/.config/handoff/chatgpt, never in the repository.
 */
import { spawn } from "node:child_process";
import { readFile } from "node:fs/promises";
import { settingsFor } from "../src/agent/models.js";
import { exportAccount, importAccount, login, logout } from "../src/llm/chatgpt/login.js";
import { planEnabled } from "../src/llm/chatgpt/oauth.js";
import { type CredentialRecord, CredentialStore } from "../src/llm/chatgpt/store.js";
import { StoredCredentials } from "../src/llm/chatgpt/tokens.js";

const args = process.argv.slice(2);
const command = args[0];
const flag = (name: string) => args.includes(`--${name}`);
const option = (name: string) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : undefined;
};

const store = CredentialStore.fromEnvironment();
const mask = (id: string) => (id.length > 12 ? `${id.slice(0, 7)}…${id.slice(-4)}` : id);

async function selected(): Promise<string> {
  const label = option("label") ?? (await store.active());
  if (!label) throw new Error("no ChatGPT account is signed in; run `npm run chatgpt -- login`");
  return label;
}

function describe(r: CredentialRecord, active: boolean): string {
  const expires = r.expires_at ? `access token until ${r.expires_at}` : "no access token";
  return `${active ? "*" : " "} ${r.label}  ${r.email ?? "(no email)"}  client ${mask(r.client_id)}  plan usage ${planEnabled(r.scopes) ? "enabled" : "NOT enabled"}  ${expires}  ${r.refresh_token ? "renewable" : "not renewable"}${r.imported_from_host ? "  (imported)" : ""}`;
}

async function main() {
  switch (command) {
    case "login": {
      const port = option("port");
      const result = await login({ store, label: option("label"), port: port ? Number(port) : undefined, enablePlan: flag("enable-plan"), openBrowser: flag("no-browser") ? () => { throw new Error("no browser"); } : undefined });
      console.log(`${result.newRegistration ? "Registered" : "Signed in again as"} ${result.record.label} (${result.record.email ?? "no email"}).`);
      console.log(result.planEnabled
        ? "Permission to use your ChatGPT plan is granted."
        : "Permission to use your ChatGPT plan was NOT granted. Handoff will not run inference on this account; run `login --label " + result.record.label + " --enable-plan` to ask again.");
      break;
    }
    case "status": {
      const host = await store.hostIdentity();
      console.log(`Credential folder: ${store.dir}`);
      console.log(`This host: ${host.ext_agent_host_id}`);
      try {
        const s = settingsFor("coordinator");
        console.log(`Coordinator: ${s.provider} model ${s.model}; paid fallback ${s.allowPaidFallback ? `ALLOWED (${s.fallbackModel})` : "off"}`);
      } catch (e) {
        console.log(`Coordinator: ${e instanceof Error ? e.message : String(e)}`);
      }
      const active = await store.active();
      const accounts = await store.list();
      if (accounts.length === 0) console.log("No ChatGPT accounts saved.");
      for (const r of accounts) console.log(describe(r, r.label === active));
      console.log("Review this app's usage and limits at https://chatgpt.com/settings/usage");
      break;
    }
    case "models": {
      const source = new StoredCredentials(store, { label: await selected() });
      const res = await fetch("https://api.openai.com/v1/models", { headers: { Authorization: (await source.authorization())! } });
      const body = (await res.json()) as { models?: Array<{ slug: string; display_name: string; visibility: string }> };
      if (!res.ok) throw new Error(`model list failed with HTTP ${res.status}`);
      for (const m of (body.models ?? []).filter((m) => m.visibility === "list")) console.log(`${m.slug}\t${m.display_name}`);
      break;
    }
    case "access-token": {
      // For moving a short-lived token into a protected credential setting. Never paste it into a chat.
      const token = (await new StoredCredentials(store, { label: await selected() }).authorization())!.replace(/^Bearer /, "");
      if (flag("clipboard")) {
        const tool = process.platform === "darwin" ? ["pbcopy", []] : ["xclip", ["-selection", "clipboard"]];
        await new Promise<void>((resolve, reject) => {
          const p = spawn(tool[0] as string, tool[1] as string[], { stdio: ["pipe", "ignore", "inherit"] });
          p.once("error", reject);
          p.once("close", (code) => (code === 0 ? resolve() : reject(new Error(`${tool[0]} exited ${code}`))));
          p.stdin.end(token);
        });
        console.error("Access token copied to the clipboard. It expires within an hour.");
      } else if (flag("stdout")) {
        process.stdout.write(token);
      } else {
        throw new Error("choose --clipboard or --stdout; the token is never printed by default");
      }
      break;
    }
    case "export": {
      const to = option("to");
      if (!to) throw new Error("export needs --to FILE");
      await exportAccount(store, await selected(), to);
      console.log(`Wrote ${to} (owner-only). Move it to the VM over SSH, run import there, then delete this copy.`);
      break;
    }
    case "import": {
      const file = args[1];
      if (!file) throw new Error("import needs a FILE");
      const r = await importAccount(store, JSON.parse(await readFile(file, "utf8")) as CredentialRecord);
      console.log(`Imported ${r.label}; this host keeps its own id ${r.ext_agent_host_id}. Delete ${file} now.`);
      break;
    }
    case "logout": {
      const label = await selected();
      const { revoked } = await logout(store, label);
      console.log(revoked ? `Signed out of ${label}; the session was revoked.` : `Signed out of ${label} locally, but remote revocation was not confirmed. You can disconnect Handoff in ChatGPT Settings.`);
      break;
    }
    default:
      console.log("usage: npm run chatgpt -- <login|status|models|access-token|export|import|logout> [options]");
      process.exitCode = command ? 1 : 0;
  }
}

main().catch((e) => {
  console.error(e instanceof Error ? e.message : String(e));
  process.exit(1);
});
