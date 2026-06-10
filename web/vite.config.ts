// @ts-nocheck
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In-memory mock state for the dev server.
type Session = any;
const mockSessions: any[] = [
  { id: "s-1", title: "�ع� auth �м��", status: "active", pinned: true, channel_kind: null, permission: "smart", created_at: "2026-06-09T08:00:00Z", last_message_at: "2026-06-10T14:30:00Z" },
  { id: "s-2", title: "���� LLM �ӿ�����", status: "idle", pinned: false, channel_kind: "dingtalk", permission: "full", created_at: "2026-06-08T10:00:00Z", last_message_at: "2026-06-10T11:00:00Z" },
  { id: "s-3", title: "�Ự��", status: "active", pinned: false, channel_kind: null, permission: "smart", created_at: "2026-06-10T09:00:00Z", last_message_at: "2026-06-10T15:00:00Z" },
  { id: "s-4", title: "��������", status: "idle", pinned: false, archived: true, channel_kind: null, permission: "readonly", created_at: "2026-06-05T08:00:00Z", last_message_at: "2026-06-06T08:00:00Z" },
];
const mockAdminSessions: any[] = [
  { id: "s-1", title: "�ع� auth �м��", status: "active", pinned: true, archived: false, channel_kind: null, channel_account_id: null, username: "admin", user_id: "u-1", message_count: 24, last_message_at: "2026-06-10T14:30:00Z", created_at: "2026-06-09T08:00:00Z" },
  { id: "s-2", title: "���� LLM �ӿ�����", status: "idle", pinned: false, archived: false, channel_kind: "dingtalk", channel_account_id: "a-dingtalk-1", username: "alice", user_id: "u-2", message_count: 18, last_message_at: "2026-06-10T11:00:00Z", created_at: "2026-06-08T10:00:00Z" },
  { id: "s-3", title: "�Ự��", status: "active", pinned: false, archived: false, channel_kind: null, channel_account_id: null, username: "admin", user_id: "u-1", message_count: 5, last_message_at: "2026-06-10T15:00:00Z", created_at: "2026-06-10T09:00:00Z" },
  { id: "s-4", title: "��������", status: "idle", pinned: false, archived: true, channel_kind: null, channel_account_id: null, username: "bob", user_id: "u-3", message_count: 9, last_message_at: "2026-06-06T08:00:00Z", created_at: "2026-06-05T08:00:00Z" },
];
const mockProviders: any[] = [
  { id: "openai", name: "OpenAI", enabled: true, base_url: "https://api.openai.com/v1", model: "gpt-4o-mini", max_tokens: 4096, temperature: 0.2, is_default: true },
  { id: "anthropic", name: "Anthropic", enabled: true, base_url: "https://api.anthropic.com", model: "claude-3-5-sonnet", max_tokens: 8192, temperature: 0.3, is_default: false },
  { id: "deepseek", name: "DeepSeek", enabled: false, base_url: "https://api.deepseek.com", model: "deepseek-chat", max_tokens: 4096, temperature: 0.2, is_default: false },
];
const mockMembers: any[] = [
  { id: "u-1", username: "admin", display_name: "����Ա", email: "admin@gepaw.dev", is_active: true, org_id: "GE-paw ��ʾ", role: "admin" },
  { id: "u-2", username: "alice", display_name: "Alice ��", email: "alice@gepaw.dev", is_active: true, org_id: "GE-paw ��ʾ", role: "user" },
  { id: "u-3", username: "bob", display_name: "Bob ��", email: "bob@gepaw.dev", is_active: false, org_id: "GE-paw ��ʾ", role: "user" },
];
const mockChannels: any[] = [
  { id: "c-1", kind: "dingtalk", name: "������", enabled: true, status: "running", last_seen_at: "2026-06-10T15:00:00Z" },
  { id: "c-2", kind: "echo", name: "���Ի���", enabled: true, status: "running", last_seen_at: "2026-06-10T12:00:00Z" },
  { id: "c-3", kind: "telegram", name: "Telegram", enabled: false, status: "stopped", last_seen_at: null },
];
const mockCrons: any[] = [
  { id: "j-1", name: "ÿ�ջ���", schedule_cron: "0 9 * * *", prompt_template: "�������նԻ�", enabled: true, failure_count: 0, last_status: "ok", last_run_at: "2026-06-10T09:00:00Z", next_run_at: "2026-06-11T09:00:00Z" },
  { id: "j-2", name: "�ܱ�", schedule_cron: "0 18 * * 5", prompt_template: "�����ܱ�", enabled: true, failure_count: 0, last_status: "ok", last_run_at: "2026-06-06T18:00:00Z", next_run_at: "2026-06-13T18:00:00Z" },
];
const mockWikiSources: any[] = [
  { id: "w-1", path: "docs/architecture.md", status: "indexed", size_bytes: 12450, mime: "text/markdown", error: null },
  { id: "w-2", path: "docs/api.md", status: "indexed", size_bytes: 8230, mime: "text/markdown", error: null },
  { id: "w-3", path: "docs/runbook.md", status: "pending", size_bytes: 4230, mime: "text/markdown", error: null },
];
const mockAudit: any[] = [
  { id: "a-1", actor: "admin", action: "session.create", target: "s-3", created_at: "2026-06-10T15:00:00Z", details: "" },
  { id: "a-2", actor: "alice", action: "llm.update", target: "openai", created_at: "2026-06-10T14:30:00Z", details: "" },
  { id: "a-3", actor: "admin", action: "member.invite", target: "bob", created_at: "2026-06-10T11:00:00Z", details: "" },
  { id: "a-4", actor: "admin", action: "channel.toggle", target: "telegram", created_at: "2026-06-09T18:20:00Z", details: "" },
  { id: "a-5", actor: "alice", action: "session.archive", target: "s-4", created_at: "2026-06-09T16:00:00Z", details: "" },
];
const mockMessages: any[] = [
  { id: "m-0", role: "user", content: "����ҷ���һ������ֿ�� auth ����", tokens_in: 0, tokens_out: 0 },
  { id: "m-1", role: "assistant", content: "<think>�����ȿ�������ṹ</think>�Ұ������� auth ���̡�[TOOL_CALL]{\"name\":\"read_file\",\"args\":{\"path\":\"src/auth.ts\"},\"status\":\"ok\"}[/TOOL_CALL]��ȡ src/auth.ts ����Կ�����Ҫ���̣�1) �м�������� app.use(auth_middleware)��2) JWT ��֤ͨ����ע�� req.user��3) ʧ��ʱ���� 401����һ���ҽ����ع��м�����֡�", tokens_in: 32, tokens_out: 184 },
  { id: "m-2", role: "user", content: "�ã���ʼ�ع�", tokens_in: 0, tokens_out: 0 },
  { id: "m-3", role: "assistant", content: "<think>��ʼ�༭ auth.ts��</think>�õġ�[TOOL_CALL]{\"name\":\"edit_file\",\"args\":{\"path\":\"src/auth.ts\",\"new_text\":\"// updated\"},\"status\":\"ok\"}[/TOOL_CALL]�Ѿ�д���°汾��[TOOL_CALL]{\"name\":\"run_command\",\"args\":{\"cmd\":\"pytest\"},\"status\":\"running\"}[/TOOL_CALL]", tokens_in: 28, tokens_out: 96 },
];

function readBody(req) {
  return new Promise((resolve) => {
    let data = "";
    req.on("data", (c) => (data += c));
    req.on("end", () => { try { resolve(JSON.parse(data || "{}")); } catch { resolve({}); } });
  });
}

function tokensForDays(days) {
  const byModel = [
    { model: "gpt-4o-mini", calls: 800, prompt_tokens: 1500000, completion_tokens: 1000000, total_tokens: 2500000, cost_cents: 1200 },
    { model: "claude-3-5-sonnet", calls: 300, prompt_tokens: 1200000, completion_tokens: 600000, total_tokens: 1800000, cost_cents: 5400 },
    { model: "deepseek-chat", calls: 134, prompt_tokens: 180000, completion_tokens: 101234, total_tokens: 281234, cost_cents: 1221 },
  ];
  let totalCalls = 0, totalTokens = 0, totalCents = 0;
  for (const m of byModel) { totalCalls += m.calls; totalTokens += m.total_tokens; totalCents += m.cost_cents; }
  const summary = { from: "x", to: "y", by_model: byModel, calls: totalCalls, total_tokens: totalTokens, prompt_tokens: 2700000, completion_tokens: 1701234, cost_cents: totalCents };
  const byDay = [];
  const today = new Date("2026-06-10T00:00:00Z");
  for (let i = Math.min(days, 7) - 1; i >= 0; i--) {
    const d = new Date(today); d.setUTCDate(d.getUTCDate() - i);
    const bucket = d.toISOString().slice(0, 10);
    const factor = 0.8 + ((i * 7 + 3) % 11) / 22;
    const t = Math.round(totalTokens / Math.min(days, 7) * factor);
    const c = Math.round(totalCents / Math.min(days, 7) * factor);
    byDay.push({ bucket, prompt_tokens: Math.round(t * 0.6), completion_tokens: Math.round(t * 0.4), total_tokens: t, cost_cents: c });
  }
  const byUser = [
    { user_id: "u-1", prompt_tokens: 1600000, completion_tokens: 900000, cost_cents: 4500, calls: 800 },
    { user_id: "u-2", prompt_tokens: 800000, completion_tokens: 500000, cost_cents: 2500, calls: 300 },
    { user_id: "u-3", prompt_tokens: 300000, completion_tokens: 301234, cost_cents: 821, calls: 134 },
  ];
  const mtd = { calls: totalCalls, total_tokens: totalTokens, cost_cents: totalCents };
  return { summary, byDay, byUser, mtd };
}

const mockCostTable = {
  overrides: { "my-custom-model": { prompt: 0.0005, completion: 0.0015 } },
  known_models: ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-mini", "claude-3-5-sonnet", "claude-3-5-haiku", "claude-opus-4", "deepseek-chat", "deepseek-reasoner", "qwen-plus", "qwen-turbo", "glm-4", "moonshot-v1-128k"],
};

function mockApiPlugin() {
  return {
    name: "mock-api",
    configureServer(server) {
      server.middlewares.use("/api", async (req, res) => {
        const url = req.url || "";
        const method = (req.method || "GET").toUpperCase();
        const path = url.split("?")[0];
        const respond = (data, status = 200) => {
          res.statusCode = status;
          res.setHeader("content-type", "application/json");
          res.end(JSON.stringify(data));
        };
        const body = (method === "GET" || method === "HEAD") ? {} : await readBody(req);

        if (path === "/auth/me" || path === "/auth/me/") return respond({ username: "admin", role: "admin", org_id: "org-1", org_name: "GE-paw ��ʾ" });

        if (path === "/client/sessions" && method === "GET") return respond(mockSessions.filter((s) => !s.archived));
        if (path === "/client/sessions" && method === "POST") {
          const id = "s-" + Math.random().toString(36).slice(2, 8);
          const now = new Date().toISOString();
          const s = { id, title: body.title || "�»Ự", status: "active", pinned: false, channel_kind: null, permission: "smart", created_at: now, last_message_at: now };
          mockSessions.unshift(s); return respond(s, 201);
        }
        const csSingle = path.match(/^\/client\/sessions\/([^/]+)$/);
        if (csSingle) {
          const id = csSingle[1];
          const idx = mockSessions.findIndex((s) => s.id === id);
          if (method === "GET") {
            if (idx >= 0) return respond(mockSessions[idx]);
            return respond({ id });
          }
          if (method === "DELETE") {
            if (idx >= 0) { mockSessions.splice(idx, 1); return respond({ ok: true }); }
            return respond({ ok: true });
          }
          if (method === "PATCH") {
            const cur = idx >= 0 ? mockSessions[idx] : { id };
            const next = { ...cur, ...body, id };
            if (idx >= 0) mockSessions[idx] = next; else mockSessions.push(next);
            return respond(next);
          }
        }
        const csMsgs = path.match(/^\/client\/sessions\/([^/]+)\/messages$/);
        if (csMsgs) { return respond(mockMessages); }
        if (path === "/client/chat" && method === "POST") {
          return respond({ reply: "��mock ��Ӧ�������յ������Ϣ�����������������ʵ LLM��", tokens_in: 18, tokens_out: 42 });
        }
        if (path === "/client/plan") return respond({ session_id: "s-1", status: "ok", steps: [
          { message_id: "m-1", tool: "read_file", args: { path: "src/auth.ts" }, status: "ok", at: "2026-06-10T14:00:00Z" },
          { message_id: "m-2", tool: "edit_file", args: { path: "src/auth.ts", new_text: "// updated" }, status: "ok", at: "2026-06-10T14:05:00Z" },
          { message_id: "m-3", tool: "run_command", args: { cmd: "pytest tests/test_auth.py" }, status: "ok", at: "2026-06-10T14:10:00Z" },
        ] });

        if (path === "/admin/llm" || path === "/admin/llm/providers" || path === "/admin/llm/") {
          if (method === "GET") return respond(mockProviders);
          if (method === "POST") {
            const id = "p-" + Math.random().toString(36).slice(2, 8);
            const p = { id, name: body.name || "��ģ��", enabled: body.enabled !== false, base_url: body.base_url || "https://api.example.com/v1", model: body.model || "gpt-4o-mini", max_tokens: body.max_tokens || 4096, temperature: body.temperature || 0.2, is_default: !!body.is_default };
            mockProviders.push(p); return respond(p, 201);
          }
        }
        const admLlm = path.match(/^\/admin\/llm\/([^/]+)$/);
        if (admLlm) {
          const id = admLlm[1];
          const idx = mockProviders.findIndex((p) => p.id === id);
          if (method === "DELETE") { if (idx >= 0) { mockProviders.splice(idx, 1); } return respond({ ok: true }); }
          if (method === "PATCH" || method === "POST") {
            const cur = idx >= 0 ? mockProviders[idx] : { id };
            const next = { ...cur, ...body, id };
            if (idx >= 0) mockProviders[idx] = next; else mockProviders.push(next);
            return respond(next);
          }
        }

        if (path === "/admin/members") {
          if (method === "GET") return respond(mockMembers);
          if (method === "POST") {
            const id = "u-" + Math.random().toString(36).slice(2, 6);
            const m = { id, username: body.username || "newuser", display_name: body.display_name || "", email: body.email || "", is_active: true, org_id: body.org_id || "GE-paw ��ʾ", role: body.role || "user" };
            mockMembers.push(m); return respond(m, 201);
          }
        }
        const admMem = path.match(/^\/admin\/members\/([^/]+)$/);
        if (admMem) {
          const id = admMem[1];
          const idx = mockMembers.findIndex((x) => x.id === id);
          if (method === "DELETE") { if (idx >= 0) { mockMembers.splice(idx, 1); } return respond({ ok: true }); }
          if (method === "POST" || method === "PATCH") {
            const cur = idx >= 0 ? mockMembers[idx] : { id };
          const next = { ...cur, ...body, id };
          if (idx >= 0) mockMembers[idx] = next; else mockMembers.push(next);
          return respond(next);
          }
        }

        if (path === "/admin/channels") {
          if (method === "GET") return respond(mockChannels);
          if (method === "POST") {
            const id = "c-" + Math.random().toString(36).slice(2, 6);
            const c = { id, kind: body.kind || "echo", name: body.name || "new", enabled: body.enabled !== false, status: "running", last_seen_at: null };
            mockChannels.push(c); return respond(c, 201);
          }
        }
        if (path === "/admin/channels/status") return respond({ running: mockChannels.filter((c) => c.enabled).map((c) => c.kind + ":" + c.id) });
        if (path === "/admin/channels/reload") return respond({ started: mockChannels.filter((c) => c.enabled).length, running: mockChannels.filter((c) => c.enabled).map((c) => c.kind + ":" + c.id) });
        const admCh = path.match(/^\/admin\/channels\/([^/]+)$/);
        if (admCh) {
          const id = admCh[1];
          const idx = mockChannels.findIndex((x) => x.id === id);
          if (method === "DELETE") { if (idx >= 0) { mockChannels.splice(idx, 1); } return respond({ ok: true }); }
          if (method === "POST" || method === "PATCH") {
            const cur = idx >= 0 ? mockChannels[idx] : { id };
            const next = { ...cur, ...body, id };
            if (idx >= 0) mockChannels[idx] = next; else mockChannels.push(next);
            return respond(next);
          }
        }

        if (path === "/admin/crons") {
          if (method === "GET") return respond(mockCrons);
          if (method === "POST") {
            const id = "j-" + Math.random().toString(36).slice(2, 6);
            const j = { id, name: body.name || "������", schedule_cron: body.schedule_cron || "*/5 * * * *", prompt_template: body.prompt_template || "", enabled: body.enabled !== false, failure_count: 0, last_status: null, last_run_at: null, next_run_at: null };
          mockCrons.push(j); return respond(j, 201);
          }
        }
        const admJ = path.match(/^\/admin\/crons\/([^/]+)$/);
        if (admJ) {
          const id = admJ[1];
          const idx = mockCrons.findIndex((x) => x.id === id);
          if (method === "DELETE") { if (idx >= 0) { mockCrons.splice(idx, 1); } return respond({ ok: true }); }
          if (method === "POST" || method === "PATCH") {
            const cur = idx >= 0 ? mockCrons[idx] : { id };
            const next = { ...cur, ...body, id };
            if (idx >= 0) mockCrons[idx] = next; else mockCrons.push(next);
            return respond(next);
          }
        }

        const tdays = (() => { const m = url.match(/days=(\d+)/); return m ? Math.max(1, Math.min(90, parseInt(m[1], 10))) : 7; })();
        const td = tokensForDays(tdays);
        if (path === "/admin/tokens/summary") return respond(td.summary);
        if (path === "/admin/tokens/by-day") return respond(td.byDay);
        if (path === "/admin/tokens/by-user") return respond(td.byUser);
        if (path === "/admin/tokens/mtd") return respond(td.mtd);
        if (path === "/admin/tokens/cost_table" || path === "/admin/tokens/cost_table/") return respond(mockCostTable);
        const ctOv = path.match(/^\/admin\/tokens\/cost_table\/([^/]+)$/);
        if (ctOv) {
          const m = decodeURIComponent(ctOv[1]);
          if (method === "PUT") { mockCostTable.overrides[m] = { prompt: Number(body.prompt), completion: Number(body.completion) }; return respond({ ok: true }); }
          if (method === "DELETE") { delete mockCostTable.overrides[m]; return respond({ ok: true }); }
        }
        if (path === "/admin/tokens") return respond(td);

        if (path === "/admin/sessions") return respond(mockAdminSessions);
        const admS = path.match(/^\/admin\/sessions\/([^/]+)$/);
        if (admS) {
          const id = admS[1];
          const idx = mockAdminSessions.findIndex((s) => s.id === id);
          if (method === "DELETE") { if (idx >= 0) { mockAdminSessions.splice(idx, 1); } return respond({ ok: true }); }
          if (method === "PATCH" || method === "POST") {
            const cur = idx >= 0 ? mockAdminSessions[idx] : { id };
            const next = { ...cur, ...body, id };
            if (idx >= 0) mockAdminSessions[idx] = next; else mockAdminSessions.push(next);
            return respond(next);
          }
        }
        const admSa = path.match(/^\/admin\/sessions\/([^/]+)\/archive$/);
        if (admSa) {
          const id = admSa[1];
          const idx = mockAdminSessions.findIndex((s) => s.id === id);
          if (idx >= 0) { mockAdminSessions[idx].archived = true; return respond(mockAdminSessions[idx]); }
          return respond({ ok: true });
        }

        if (path === "/admin/wiki/sources" || path === "/admin/wiki/sources/") return respond(mockWikiSources);
        if (path === "/admin/wiki/sources/upload") return respond({ id: "w-new", path: "docs/new.md", status: "indexed", size_bytes: 1024 });
        const wikiDel = path.match(/^\/admin\/wiki\/sources\/([^/]+)\/delete$/);
        if (wikiDel) {
          const idx = mockWikiSources.findIndex((s) => s.id === wikiDel[1]);
          if (idx >= 0) { mockWikiSources.splice(idx, 1); }
          return respond({ ok: true });
        }
        if (path === "/admin/wiki/ingest" || path === "/admin/wiki/compile" || path === "/admin/wiki/reset") return respond({ ok: true, processed: mockWikiSources.length });
        if (path === "/admin/wiki") return respond({ sources: mockWikiSources, log: ["���ϴ���docs/architecture.md", "���ϴ���docs/api.md"] });

        if (path === "/admin/audit") return respond(mockAudit);

        return respond({});
      });
    },
  };
}

export default defineConfig({
  plugins: [react(), mockApiPlugin()],
  server: { host: "0.0.0.0", port: 5173 },
  build: { outDir: "dist", sourcemap: false },
});