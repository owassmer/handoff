import type { Queryable } from "./db.js";

export type Permission = "view" | "work" | "decide" | "configure";

/** Who is asking. Only operators can decide; the agent proposes and acts within what was decided. */
export type Principal =
  | { kind: "operator"; userId: string }
  | { kind: "agent"; runId: string }
  | { kind: "system"; name: string };

export function principalLabel(p: Principal): string {
  switch (p.kind) {
    case "operator": return `operator:${p.userId}`;
    case "agent": return `agent:${p.runId}`;
    case "system": return `system:${p.name}`;
  }
}

export class NotAllowed extends Error {}

export async function requirePermission(q: Queryable, p: Principal, permission: Permission): Promise<string> {
  if (p.kind !== "operator") throw new NotAllowed(`${principalLabel(p)} cannot ${permission}; only an operator can`);
  const [user] = await q.query<{ permissions: Permission[] }>(`select permissions from users where id = $1`, [p.userId]);
  if (!user) throw new NotAllowed(`unknown user ${p.userId}`);
  if (!user.permissions.includes(permission)) throw new NotAllowed(`${p.userId} does not have ${permission} permission`);
  return p.userId;
}
