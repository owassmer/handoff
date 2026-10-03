/**
 * Subscription-only smoke test: one wake of the real coordinator on the simulated case's first moment
 * (October 12, the tenant gives notice), billed to the ChatGPT plan. It refuses to run if a paid
 * provider could be used.
 *
 *   HANDOFF_COORDINATOR_MODEL=<slug from `npm run chatgpt -- models`> npm run smoke:chatgpt
 * With HANDOFF_CHATGPT_AUTH=stored (default), environment (HANDOFF_CHATGPT_ACCESS_TOKEN) or injected.
 */
import { modelFor, settingsFor } from "../src/agent/models.js";
import { coordinatorTurn } from "../src/agent/turn.js";
import { stageNoticeWorld } from "../src/demo/seed.js";
import { ChatGPTPlanError } from "../src/llm/chatgpt/responses.js";
import { tokenSourceFromEnvironment } from "../src/llm/chatgpt/tokens.js";

async function main() {
  const s = settingsFor("coordinator");
  if (s.provider !== "openai_chatgpt") throw new Error(`refusing: the coordinator's provider is ${s.provider}, not openai_chatgpt`);
  if (process.env.HANDOFF_ALLOW_PAID_FALLBACK === "true") throw new Error("refusing: HANDOFF_ALLOW_PAID_FALLBACK is true; this test is subscription-only");
  console.log(`Coordinator: ChatGPT plan, model ${s.model}, ${tokenSourceFromEnvironment().describe()}. Paid fallback off.`);

  const w = await stageNoticeWorld(coordinatorTurn({ model: modelFor("coordinator"), maxSteps: 40 }));
  try {
    const r = await w.runner.runUntilQuiet();
    const [run] = await w.db.query<{ id: string; status: string; error: string | null }>(`select id, status, error from runs order by started_at desc limit 1`);
    console.log(`\nWake: ${run?.status ?? "none"}${run?.error ? ` — ${run.error}` : ""}`);
    for (const m of await w.db.query<{ role: string; content: Record<string, any> }>(`select role, content from run_messages where run_id = $1 order by seq`, [run?.id])) {
      if (m.role === "assistant") {
        for (const c of m.content.toolCalls ?? []) console.log(`  → ${c.name} ${JSON.stringify(c.args)}`);
        if (m.content.text) console.log(`  says: ${m.content.text}`);
      } else if (m.role === "tool") {
        console.log(`  ← ${String(m.content.text).slice(0, 300)}`);
      }
    }
    console.log("\nEmails sent:");
    for (const msg of await w.mail.inbox("tenant-1")) console.log(`  [${msg.subject}] ${msg.body.replace(/\s+/g, " ").slice(0, 400)}`);
    console.log("Wake-ups scheduled:");
    for (const wk of await w.db.query<{ due_at: Date; reason: string }>(`select due_at, reason from wakeups order by due_at`)) console.log(`  ${new Date(wk.due_at).toISOString()} ${wk.reason}`);
    console.log("Decisions proposed:");
    for (const d of await w.db.query<{ kind: string; status: string }>(`select kind, status from decisions where case_id is not null`)) console.log(`  ${d.kind} (${d.status})`);
    if (r.failed.length > 0) process.exitCode = 1;
  } finally {
    await w.close();
  }
}

main().catch((e) => {
  if (e instanceof ChatGPTPlanError) console.error(`ChatGPT plan request failed: ${e.message}`);
  else console.error(e instanceof Error ? e.message : String(e));
  process.exit(1);
});
