// @ts-nocheck
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const mockSessions: any[] = [
  { id: "s-1", title: "Fix auth", status: "active", pinned: true, channel_kind: null, permission: "smart", created_at: "2026-06-09T08:00:00Z", last_message_at: "2026-06-10T14:30:00Z" },
  { id: "s-2", title: "Configure LLM", status: "idle", pinned: false, channel_kind: "dingtalk", permission: "full", created_at: "2026-06-08T10:00:00Z", last_message_at: "2026-06-10T11:00:00Z" },
  { id: "s-3", title: "New chat", status: "active", pinned: false, channel_kind: null, permission: "smart", created_at: "2026-06-10T09:00:00Z", last_message_at: "2026-06-10T15:00:00Z" }
];
const mockAdminSessions: any[] = [
  { id: "s-1", title: "Fix auth", status: "active", pinned: true, archived: false, channel_kind: null, channel_account_id: null, username: "admin", user_id: "u-1", message_count: 24, last_message_at: "2026-06-10T14:30:00Z", created_at: "2026-06-09T08:00:00Z" },
  { id: "s-2", title: "Configure LLM", status: "idle", pinned: false, archived: false, channel_kind: "dingtalk", channel_account_id: "a-1", username: "alice", user_id: "u-2", message_count: 18, last_message_at: "2026-06-10T11:00:00Z", created_at: "2026-06-08T10:00:00Z" }
];
const mockProviders: any[] = [
  { id: "openai", name: "OpenAI", enabled: true, base_url: "https://api.openai.com/v1", model: "gpt-4o-mini", max_tokens: 4096, temperature: 0.2, is_default: true }
];
const mockMembers: any[] = [
  { id: "u-1", username: "admin", display_name: "Admin", email: "admin@gepaw.dev", is_active: true, org_id: "GE-paw", role: "admin" }
];
const mockChannels: any[] = [];
const mockCrons: any[] = [];
const mockWikiSources: any[] = [];
const mockAudit: any[] = [];
const sessionMessages: Record<string, any[]> = {
  "s-1": [
    { id: "m-1-1", role: "user", content: "Help me review the auth flow.", tokens_in: 0, tokens_out: 0 },
    { id: "m-1-2", role: "assistant", content: "OK. The auth flow uses JWT.", tokens_in: 120, tokens_out: 86 }
  ],
  "s-2": [
    { id: "m-2-1", role: "user", content: "Configure LLM endpoint parameters.", tokens_in: 0, tokens_out: 0 },
    { id: "m-2-2", role: "assistant", content: "Opening the LLM endpoints page.", tokens_in: 0, tokens_out: 0 }
  ],
  "s-3": [
    { id: "m-3-1", role: "user", content: "Add a WeChat channel.", tokens_in: 0, tokens_out: 0 },
    { id: "m-3-2", role: "assistant", content: "Pick kind=wechat, fill in a name, then QR-scan.", tokens_in: 0, tokens_out: 0 }
  ]
};
const mockCostTable = { overrides: {}, known_models: ["gpt-4o-mini"] };

function readBody(req: any): Promise<any> {
  return new Promise((resolve) => {
    let data = "";
    req.on("data", (chunk: any) => (data += chunk));
    req.on("end", () => {
      if (!data) return resolve({});
      try { resolve(JSON.parse(data)); } catch { resolve({}); }
    });
  });
}

function mockApiPlugin() {
  return {
    name: "mock-api",
    configureServer(server: any) {
      server.middlewares.use("/api", async (req: any, res: any) => {
        const url = req.url || "";
        const method = (req.method || "GET").toUpperCase();
        const path = url.split("?")[0];
        const respond = (data: any, status = 200) => {
          res.statusCode = status;
          res.setHeader("content-type", "application/json; charset=utf-8");
          res.end(JSON.stringify(data));
        };
        const body = (method === "GET" || method === "HEAD") ? {} : await readBody(req);

        if (path === "/auth/login" || path === "/auth/login/") {
          if (method !== "POST") return respond({ detail: "no" }, 405);
          const uname = String(body?.username || "").trim();
          if (!uname || !body?.password) return respond({ detail: "missing" }, 400);
          const role = uname.toLowerCase().startsWith("admin") ? "admin" : "user";
          return respond({ access_token: "mock-" + uname, refresh_token: "mock-r-" + uname, role });
        }
        if (path === "/auth/me" || path === "/auth/me/") return respond({ username: "admin", role: "admin", org_id: "o1", org_name: "GE-paw" });
        if (path === "/client/sessions" && method === "GET") return respond(mockSessions);
        if (path === "/client/sessions" && method === "POST") {
          const id = "s-" + Math.random().toString(36).slice(2, 8);
          const now = new Date().toISOString();
          const s = { id, title: body?.title || "New chat", status: "active", pinned: false, channel_kind: null, permission: "smart", created_at: now, last_message_at: now };
          mockSessions.unshift(s);
          if (!sessionMessages[id]) sessionMessages[id] = [];
          return respond(s, 201);
        }
        const csSingle = path.match(/^\/client\/sessions\/([^/]+)$/);
        if (csSingle) {
          const id = csSingle[1];
          const idx = mockSessions.findIndex((x: any) => x.id === id);
          if (method === "GET") return respond(idx >= 0 ? mockSessions[idx] : { id });
          if (method === "DELETE") { if (idx >= 0) mockSessions.splice(idx, 1); return respond({ ok: true }); }
          if (method === "PATCH") { const cur = idx >= 0 ? mockSessions[idx] : { id }; const nxt = Object.assign({}, cur, body, { id }); if (idx >= 0) mockSessions[idx] = nxt; else mockSessions.push(nxt); return respond(nxt); }
        }
        // Per-session messages
        const csMsgs = path.match(/^\/client\/sessions\/([^/]+)\/messages$/);
        if (csMsgs) {
          const sid = csMsgs[1];
          if (!sessionMessages[sid]) sessionMessages[sid] = [];
          return respond(sessionMessages[sid]);
        }
        if (path === "/client/chat" && method === "POST") {
          const sid = body?.session_id || "s-default";
          if (!sessionMessages[sid]) sessionMessages[sid] = [];
          const reply = "Mock reply. Configure real LLM in Settings.";
          sessionMessages[sid].push({ id: "m-u", role: "user", content: body?.message || "" });
          sessionMessages[sid].push({ id: "m-a", role: "assistant", content: reply });
          return respond({ reply });
        }
        if (path === "/client/config") return respond({ llm: { id: "openai", name: "OpenAI", base_url: "https://api.openai.com/v1", model: "gpt-4o-mini" } });
        if (path === "/client/llm/providers" || path === "/client/llm/providers/") return respond(mockProviders.filter((p) => p.enabled !== false));
        if (path === "/client/llm/active" && method === "POST") return respond({ ok: true, active: body?.provider_id });
        if (path === "/client/plan") return respond({ session_id: "s-1", status: "ok", steps: [] });
        if (path === "/admin/llm" || path === "/admin/llm/providers" || path === "/admin/llm/") {
          if (method === "GET") return respond(mockProviders);
          if (method === "POST") { const p = Object.assign({ id: "p-new", enabled: true, is_default: false }, body); mockProviders.push(p); return respond(p, 201); }
        }
        if (path === "/admin/members") return respond(mockMembers);
        if (path === "/admin/channels") return respond(mockChannels);
        if (path === "/admin/channels/status") return respond({ running: [] });
        if (path === "/admin/channels/reload") return respond({ started: 0, running: [] });
        if (path === "/admin/crons") return respond(mockCrons);
        if (path === "/admin/sessions") return respond(mockAdminSessions);
        if (path === "/admin/wiki/sources" || path === "/admin/wiki/sources/") return respond(mockWikiSources);
        if (path === "/admin/wiki/sources/upload") return respond({ id: "w-new" });
        if (path === "/admin/wiki/ingest" || path === "/admin/wiki/compile" || path === "/admin/wiki/reset") return respond({ ok: true });
        if (path === "/admin/wiki") return respond({ sources: mockWikiSources, log: [] });
        if (path === "/admin/audit") return respond(mockAudit);
        if (path === "/admin/tokens/summary") return respond({ calls: 0, total_tokens: 0 });
        if (path === "/admin/tokens/by-day") return respond([]);
        if (path === "/admin/tokens/by-user") return respond([]);
        if (path === "/admin/tokens/mtd") return respond({ calls: 0, total_tokens: 0 });
        if (path === "/admin/tokens/cost_table" || path === "/admin/tokens/cost_table/") return respond(mockCostTable);
        if (path === "/admin/tokens") return respond({});
        if (path === "/admin/skills" || path === "/admin/skills/") return respond([]);
        if (path === "/admin/mcp" || path === "/admin/mcp/") return respond([]);
        if (path === "/admin/plugins" || path === "/admin/plugins/") return respond([]);
        return respond({});
      });
    },
  };
}

export default defineConfig({
  plugins: [react(), mockApiPlugin()],
  server: { host: "0.0.0.0", port: 5173, strictPort: true },
  build: { outDir: "dist", sourcemap: false },
});


