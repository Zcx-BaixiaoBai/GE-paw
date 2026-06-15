// @ts-nocheck
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In-memory mock state for the dev server so the console can be exercised
// without a running Python backend. Mirrors the shape that the real /api
// endpoints return.
type Session = any;
const mockSessions: any[] = [
  { id: "s-1", title: "修复 auth 相关问题", status: "active", pinned: true, channel_kind: null, permission: "smart", created_at: "2026-06-09T08:00:00Z", last_message_at: "2026-06-10T14:30:00Z" },
  { id: "s-2", title: "配置 LLM 接口参数", status: "idle", pinned: false, channel_kind: "dingtalk", permission: "full", created_at: "2026-06-08T10:00:00Z", last_message_at: "2026-06-10T11:00:00Z" },
  { id: "s-3", title: "新对话", status: "active", pinned: false, channel_kind: null, permission: "smart", created_at: "2026-06-10T09:00:00Z", last_message_at: "2026-06-10T15:00:00Z" },
  { id: "s-4", title: "已归档会话", status: "idle", pinned: false, archived: true, channel_kind: null, permission: "readonly", created_at: "2026-06-05T08:00:00Z", last_message_at: "2026-06-06T08:00:00Z" },
];
const mockAdminSessions: any[] = [
  { id: "s-1", title: "修复 auth 相关问题", status: "active", pinned: true, archived: false, channel_kind: null, channel_account_id: null, username: "admin", user_id: "u-1", message_count: 24, last_message_at: "2026-06-10T14:30:00Z", created_at: "2026-06-09T08:00:00Z" },
  { id: "s-2", title: "配置 LLM 接口参数", status: "idle", pinned: false, archived: false, channel_kind: "dingtalk", channel_account_id: "a-dingtalk-1", username: "alice", user_id: "u-2", message_count: 18, last_message_at: "2026-06-10T11:00:00Z", created_at: "2026-06-08T10:00:00Z" },
  { id: "s-3", title: "新对话", status: "active", pinned: false, archived: false, channel_kind: null, channel_account_id: null, username: "admin", user_id: "u-1", message_count: 5, last_message_at: "2026-06-10T15:00:00Z", created_at: "2026-06-10T09:00:00Z" },
  { id: "s-4", title: "已归档会话", status: "idle", pinned: false, archived: true, channel_kind: null, channel_account_id: null, username: "bob", user_id: "u-3", message_count: 9, last_message_at: "2026-06-06T08:00:00Z", created_at: "2026-06-05T08:00:00Z" },
];
const mockProviders: any[] = [
  { id: "openai", name: "OpenAI", enabled: true, base_url: "https://api.openai.com/v1", model: "gpt-4o-mini", max_tokens: 4096, temperature: 0.2, is_default: true },
  { id: "anthropic", name: "Anthropic", enabled: true, base_url: "https://api.anthropic.com", model: "claude-3-5-sonnet", max_tokens: 8192, temperature: 0.3, is_default: false },
  { id: "deepseek", name: "DeepSeek", enabled: false, base_url: "https://api.deepseek.com", model: "deepseek-chat", max_tokens: 4096, temperature: 0.2, is_default: false },
];
const mockMembers: any[] = [
  { id: "u-1", username: "admin", display_name: "管理员", email: "admin@gepaw.dev", is_active: true, org_id: "GE-paw 演示", role: "admin" },
  { id: "u-2", username: "alice", display_name: "Alice 员工", email: "alice@gepaw.dev", is_active: true, org_id: "GE-paw 演示", role: "user" },
  { id: "u-3", username: "bob", display_name: "Bob 员工", email: "bob@gepaw.dev", is_active: false, org_id: "GE-paw 演示", role: "user" },
];
const mockChannels: any[] = [
  { id: "c-1", kind: "dingtalk", name: "主通道", enabled: true, status: "running", last_seen_at: "2026-06-10T15:00:00Z" },
  { id: "c-2", kind: "echo", name: "回声测试", enabled: true, status: "running", last_seen_at: "2026-06-10T12:00:00Z" },
  { id: "c-3", kind: "telegram", name: "Telegram", enabled: false, status: "stopped", last_seen_at: null },
];
const mockCrons: any[] = [
  { id: "j-1", name: "每日总结", schedule_cron: "0 9 * * *", prompt_template: "生成每日状态报告", enabled: true, failure_count: 0, last_status: "ok", last_run_at: "2026-06-10T09:00:00Z", next_run_at: "2026-06-11T09:00:00Z" },
  { id: "j-2", name: "周报", schedule_cron: "0 18 * * 5", prompt_template: "生成本周工作总结", enabled: true, failure_count: 0, last_status: "ok", last_run_at: "2026-06-06T18:00:00Z", next_run_at: "2026-06-13T18:00:00Z" },
];
const mockWikiSources: any[] = [
  { id: "w-1", path: "docs/architecture.md", status: "indexed", size_bytes: 12450, mime: "text/markdown", error: null },
  { id: "w-2", path: "docs/api.md", status: "indexed", size_bytes: 8230, mime: "text/markdown", error: null },
  { id: "w-3", path: "docs/runbook.md", status: "pending", size_bytes: 4230, mime: "text/markdown", error: null },
];
const mockAudit: any[] = [
  { id: "a-1", actor_id: "u-1", action: "session.create", target: "s-3", ip: "127.0.0.1", created_at: "2026-06-10T15:00:00Z", detail_json: "{\"title\":\"新对话\"}" },
  { id: "a-2", actor_id: "u-2", action: "llm.update", target: "openai", ip: "127.0.0.1", created_at: "2026-06-10T14:30:00Z", detail_json: "{\"model\":\"gpt-4o-mini\"}" },
  { id: "a-3", actor_id: "u-1", action: "member.invite", target: "u-3", ip: "127.0.0.1", created_at: "2026-06-10T11:00:00Z", detail_json: "{\"username\":\"bob\"}" },
  { id: "a-4", actor_id: "u-1", action: "wiki.upload", target: "docs/architecture.md", ip: "127.0.0.1", created_at: "2026-06-10T10:00:00Z", detail_json: null },
  { id: "a-5", actor_id: "u-2", action: "session.delete", target: "s-old", ip: "127.0.0.1", created_at: "2026-06-09T16:00:00Z", detail_json: null },
];
const sessionMessages: Record<string, any[]> = {
  "s-1": [
    { id: "m-1-1", role: "user", content: "帮我看看 auth 模块的认证流程", tokens_in: 0, tokens_out: 0 },
    { id: "m-1-2", role: "assistant", content: "好的，auth 模块使用 JWT，登录后 token 放在 Authorization 头。\n\n关键文件：src/auth.ts。", tokens_in: 120, tokens_out: 86 }
  ],
  "s-2": [
    { id: "m-2-1", role: "user", content: "配置 LLM 接口参数", tokens_in: 0, tokens_out: 0 },
    { id: "m-2-2", role: "assistant", content: "已为你打开 LLM 接口设置页。请填写：\n- 名称\n- Base URL\n- API Key\n- 模型\n\n完成后点击「添加」即可。", tokens_in: 0, tokens_out: 0 }
  ],
  "s-3": [
    { id: "m-3-1", role: "user", content: "在 channel 页里加一个微信通道", tokens_in: 0, tokens_out: 0 },
    { id: "m-3-2", role: "assistant", content: "好的。在通道类型里选 wechat，只需要填名称然后扫二维码完成登录。\n\n不需要 token。", tokens_in: 0, tokens_out: 0 }
  ],
};
const mockMessages: any[] = [];  // backward compat: empty default

  { id: "m-1", role: "user", content: "帮我查一下 wiki 里的认证流程", tokens_in: 0, tokens_out: 0 },
  { id: "m-2", role: "assistant", content: "好的，我已读取 wiki/auth.md。整体流程如下：\n1. 用户提交用户名密码\n2. 服务端验证后签发 JWT\n3. 客户端在 Authorization 头里携带 token\n\n接下来需要我做哪一步？", tokens_in: 120, tokens_out: 86 },
];
const mockCostTable = {
  overrides: { "my-custom-model": { prompt: 0.0005, completion: 0.0015 } },
  known_models: ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-mini", "claude-3-5-sonnet", "claude-3-5-haiku", "claude-opus-4", "deepseek-chat", "deepseek-reasoner", "qwen-plus", "qwen-turbo", "glm-4", "moonshot-v1-128k"],
};

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

function tokensForDays(days: number) {
  // Synthesise plausible token-usage numbers so the admin pages have data.
  const totalCalls = 80 + days * 35;
  const totalTokens = 240000 + days * 110000;
  const totalCents = 350 + days * 220;
  const summary = {
    from: new Date(Date.now() - days * 86400e3).toISOString(),
    to: new Date().toISOString(),
    by_model: [
      { model: "gpt-4o-mini", prompt_tokens: 120000, completion_tokens: 88000, total_tokens: 208000, cost_cents: 145, calls: 156 },
      { model: "claude-3-5-sonnet", prompt_tokens: 60000, completion_tokens: 42000, total_tokens: 102000, cost_cents: 482, calls: 78 },
      { model: "deepseek-chat", prompt_tokens: 90000, completion_tokens: 71000, total_tokens: 161000, cost_cents: 86, calls: 64 },
    ],
    calls: totalCalls,
    total_tokens: totalTokens,
    prompt_tokens: 270000,
    completion_tokens: 201000,
    cost_cents: totalCents,
  };
  const byDay: any[] = [];
  for (let i = days - 1; i >= 0; i--) {
    const d = new Date(Date.now() - i * 86400e3);
    byDay.push({
      bucket: d.toISOString().slice(0, 10),
      prompt_tokens: 12000 + Math.round(Math.random() * 8000),
      completion_tokens: 8000 + Math.round(Math.random() * 6000),
      total_tokens: 20000 + Math.round(Math.random() * 14000),
      cost_cents: 18 + Math.round(Math.random() * 22),
    });
  }
  const byUser = [
    { user_id: "u-1", prompt_tokens: 180000, completion_tokens: 120000, cost_cents: 432, calls: 168 },
    { user_id: "u-2", prompt_tokens: 95000, completion_tokens: 70000, cost_cents: 198, calls: 94 },
    { user_id: "u-3", prompt_tokens: 30000, completion_tokens: 30123, cost_cents: 82, calls: 13 },
  ];
  const mtd = { calls: totalCalls, total_tokens: totalTokens, cost_cents: totalCents };
  return { summary, byDay, byUser, mtd };
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

        // --- Auth -----------------------------------------------------------------
        if (path === "/auth/login" || path === "/auth/login/") {
          if (method !== "POST") return respond({ detail: "method not allowed" }, 405);
          // Dev mock: any non-empty username/password is accepted. The role is
          // inferred from the username so admin/admin logs in as admin.
          const uname = String(body?.username || "").trim();
          const pwd = String(body?.password || "");
          if (!uname || !pwd) return respond({ detail: "缺少用户名或密码" }, 400);
          const role = uname.toLowerCase().startsWith("admin") ? "admin" : "user";
          return respond({
            access_token: "mock-access-" + uname,
            refresh_token: "mock-refresh-" + uname,
            role,
          });
        }
        if (path === "/auth/refresh" || path === "/auth/refresh/") {
          return respond({
            access_token: "mock-access-refreshed",
            refresh_token: "mock-refresh-refreshed",
          });
        }
        if (path === "/auth/me" || path === "/auth/me/") {
          // The mock identity is a stable admin; the real backend would read
          // the bearer token to look up the user.
          return respond({ username: "admin", role: "admin", org_id: "org-1", org_name: "GE-paw 演示" });
        }

        // --- Client sessions -----------------------------------------------------
        if (path === "/client/sessions" && method === "GET") return respond(mockSessions.filter((s) => !s.archived));
        if (path === "/client/sessions" && method === "POST") {
          const id = "s-" + Math.random().toString(36).slice(2, 8);
          const now = new Date().toISOString();
          const s = { id, title: body.title || "新会话", status: "active", pinned: false, channel_kind: null, permission: "smart", created_at: now, last_message_at: now };
          mockSessions.unshift(s);
          return respond(s, 201);
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
            if (idx >= 0) mockSessions.splice(idx, 1);
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
        if (csMsgs) {
          const sid = csMsgs[1];
          if (!sessionMessages[sid]) sessionMessages[sid] = [];
          return respond(sessionMessages[sid]);
        }
        const csAddMsg = path.match(/^\/client\/sessions\/([^/]+)\/messages$/);
        // (handled above)
        if (path === "/client/chat" && method === "POST") {
          return respond({ reply: "这是 mock 响应。您发送了消息，请连接真实 LLM。", tokens_in: 18, tokens_out: 42 });
        }
        if (path === "/client/plan") return respond({
          session_id: "s-1",
          status: "ok",
          steps: [
            { message_id: "m-1", tool: "read_file", args: { path: "src/auth.ts" }, status: "ok", at: "2026-06-10T14:00:00Z" },
            { message_id: "m-2", tool: "edit_file", args: { path: "src/auth.ts", new_text: "// updated" }, status: "ok", at: "2026-06-10T14:05:00Z" },
            { message_id: "m-3", tool: "run_command", args: { cmd: "pytest tests/test_auth.py" }, status: "ok", at: "2026-06-10T14:10:00Z" },
          ],
        });
        if (path === "/client/preview-data") return respond({
          path: body?.path || "wiki/overview.md",
          size: 12450,
          lines: 240,
          words: 1820,
          headline: "GE-paw 知识库概览",
          preview_url: "about:blank",
          file_url: "about:blank",
          snippet: "GE-paw 是一个多租户智能代理平台，支持助手模式与知识问答模式。",
        });
        if (path === "/client/diff") return respond({
          left: "wiki/overview.md", right: "wiki/index.md", ratio: 0.82, diff: "@@ -1,3 +1,3 @@\n-# 概览\n+# 首页\n\n欢迎使用 GE-paw 知识库。", left_size: 12450, right_size: 8230,
        });
        if (path === "/client/fs/list") return respond({ items: [
          { name: "docs", path: "docs", type: "dir", size: 0, mtime: Date.now() },
          { name: "src", path: "src", type: "dir", size: 0, mtime: Date.now() },
          { name: "README.md", path: "README.md", type: "file", size: 4320, mtime: Date.now() },
        ] });
        if (path === "/client/wiki/tree") return respond({ items: [
          { name: "overview.md", path: "wiki/overview.md", type: "file", size: 12450, mtime: Date.now() },
          { name: "index.md", path: "wiki/index.md", type: "file", size: 8230, mtime: Date.now() },
          { name: "api.md", path: "wiki/api.md", type: "file", size: 5300, mtime: Date.now() },
        ] });
        if (path === "/client/config") return respond({
          llm: { id: "openai", name: "OpenAI", base_url: "https://api.openai.com/v1", model: "gpt-4o-mini" },
        });
        if (path === "/client/wiki/query" && method === "POST") return respond({
          answer: "GE-paw 的认证流程包括：用户登录、令牌签发、权限校验。",
          citations: [
            { path: "wiki/auth.md", snippet: "JWT 令牌用于无状态认证...", score: 0.91 },
            { path: "wiki/security.md", snippet: "权限按角色划分...", score: 0.78 },
          ],
          tokens_in: 120, tokens_out: 88, latency_ms: 312,
        });
        if (path === "/client/wiki/preview" || path.startsWith("/client/wiki/preview")) return respond({ html: "<p>GE-paw 知识库预览（mock）</p>" });

        // --- Admin LLM -----------------------------------------------------------
        if (path === "/admin/llm" || path === "/admin/llm/providers" || path === "/admin/llm/") {
          if (method === "GET") return respond(mockProviders);
          if (method === "POST") {
            const id = "p-" + Math.random().toString(36).slice(2, 8);
            const p = { id, name: body.name || "新模型", enabled: body.enabled !== false, base_url: body.base_url || "https://api.example.com/v1", model: body.model || "gpt-4o-mini", max_tokens: body.max_tokens || 4096, temperature: body.temperature || 0.2, is_default: !!body.is_default };
            mockProviders.push(p);
            return respond(p, 201);
          }
        }
        const admLlm = path.match(/^\/admin\/llm\/([^/]+)$/);
        if (admLlm) {
          const id = admLlm[1];
          const idx = mockProviders.findIndex((p) => p.id === id);
          if (method === "DELETE") { if (idx >= 0) mockProviders.splice(idx, 1); return respond({ ok: true }); }
          if (method === "PATCH" || method === "POST") {
            const cur = idx >= 0 ? mockProviders[idx] : { id };
            const next = { ...cur, ...body, id };
            if (idx >= 0) mockProviders[idx] = next; else mockProviders.push(next);
            return respond(next);
          }
        }

        // --- Admin members -------------------------------------------------------
        if (path === "/admin/members") {
          if (method === "GET") return respond(mockMembers);
          if (method === "POST") {
            const id = "u-" + Math.random().toString(36).slice(2, 6);
            const m = { id, username: body.username || "newuser", display_name: body.display_name || "", email: body.email || "", is_active: true, org_id: body.org_id || "GE-paw 演示", role: body.role || "user" };
            mockMembers.push(m);
            return respond(m, 201);
          }
        }
        const admMem = path.match(/^\/admin\/members\/([^/]+)$/);
        if (admMem) {
          const id = admMem[1];
          const idx = mockMembers.findIndex((x) => x.id === id);
          if (method === "DELETE") { if (idx >= 0) mockMembers.splice(idx, 1); return respond({ ok: true }); }
          if (method === "POST" || method === "PATCH") {
            const cur = idx >= 0 ? mockMembers[idx] : { id };
            const next = { ...cur, ...body, id };
            if (idx >= 0) mockMembers[idx] = next; else mockMembers.push(next);
            return respond(next);
          }
        }

        // --- Admin channels ------------------------------------------------------
        if (path === "/admin/channels") {
          if (method === "GET") return respond(mockChannels);
          if (method === "POST") {
            const id = "c-" + Math.random().toString(36).slice(2, 6);
            const c = { id, kind: body.kind || "echo", name: body.name || "新通道", enabled: body.enabled !== false, status: "running", last_seen_at: null };
            mockChannels.push(c);
            return respond(c, 201);
          }
        }
        if (path === "/admin/channels/status") return respond({ running: mockChannels.filter((c) => c.enabled).map((c) => c.kind + ":" + c.id) });
        if (path === "/admin/channels/reload") return respond({ started: mockChannels.filter((c) => c.enabled).length, running: mockChannels.filter((c) => c.enabled).map((c) => c.kind + ":" + c.id) });
        const admCh = path.match(/^\/admin\/channels\/([^/]+)$/);
        if (admCh) {
          const id = admCh[1];
          const idx = mockChannels.findIndex((x) => x.id === id);
          if (method === "DELETE") { if (idx >= 0) mockChannels.splice(idx, 1); return respond({ ok: true }); }
          if (method === "POST" || method === "PATCH") {
            const cur = idx >= 0 ? mockChannels[idx] : { id };
            const next = { ...cur, ...body, id };
            if (idx >= 0) mockChannels[idx] = next; else mockChannels.push(next);
            return respond(next);
          }
        }

        // --- Admin crons ---------------------------------------------------------
        if (path === "/admin/crons") {
          if (method === "GET") return respond(mockCrons);
          if (method === "POST") {
            const id = "j-" + Math.random().toString(36).slice(2, 6);
            const j = { id, name: body.name || "新任务", schedule_cron: body.schedule_cron || "*/5 * * * *", prompt_template: body.prompt_template || "", enabled: body.enabled !== false, failure_count: 0, last_status: null, last_run_at: null, next_run_at: null };
            mockCrons.push(j);
            return respond(j, 201);
          }
        }
        const admJ = path.match(/^\/admin\/crons\/([^/]+)$/);
        if (admJ) {
          const id = admJ[1];
          const idx = mockCrons.findIndex((x) => x.id === id);
          if (method === "DELETE") { if (idx >= 0) mockCrons.splice(idx, 1); return respond({ ok: true }); }
          if (method === "POST" || method === "PATCH") {
            const cur = idx >= 0 ? mockCrons[idx] : { id };
            const next = { ...cur, ...body, id };
            if (idx >= 0) mockCrons[idx] = next; else mockCrons.push(next);
            return respond(next);
          }
        }

        // --- Admin tokens --------------------------------------------------------
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

        // --- Admin sessions ------------------------------------------------------
        if (path === "/admin/sessions") {
          const showAll = url.includes("all=1");
          return respond(showAll ? mockAdminSessions : mockAdminSessions.filter((s) => !s.archived));
        }
        const admS = path.match(/^\/admin\/sessions\/([^/]+)$/);
        if (admS) {
          const id = admS[1];
          const idx = mockAdminSessions.findIndex((s) => s.id === id);
          if (method === "DELETE") { if (idx >= 0) mockAdminSessions.splice(idx, 1); return respond({ ok: true }); }
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

        // --- Admin wiki ----------------------------------------------------------
        if (path === "/admin/wiki/sources" || path === "/admin/wiki/sources/") return respond(mockWikiSources);
        if (path === "/admin/wiki/sources/upload") return respond({ id: "w-new", path: "docs/new.md", status: "indexed", size_bytes: 1024 });
        const wikiDel = path.match(/^\/admin\/wiki\/sources\/([^/]+)\/delete$/);
        if (wikiDel) {
          const idx = mockWikiSources.findIndex((s) => s.id === wikiDel[1]);
          if (idx >= 0) mockWikiSources.splice(idx, 1);
          return respond({ ok: true });
        }
        if (path === "/admin/wiki/ingest" || path === "/admin/wiki/compile" || path === "/admin/wiki/reset") return respond({ ok: true, processed: mockWikiSources.length });
        if (path === "/admin/wiki") return respond({ sources: mockWikiSources, log: ["已导入：docs/architecture.md", "已导入：docs/api.md"] });

        // --- Admin audit ---------------------------------------------------------
        if (path === "/admin/audit") {
          const m = url.match(/action=([^&]+)/);
          const wanted = m ? decodeURIComponent(m[1]) : "";
          const rows = wanted ? mockAudit.filter((x) => x.action === wanted) : mockAudit;
          return respond(rows);
        }

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
