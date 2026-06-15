import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\Admin\Documents\GE-paw\web\vite.config.ts'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the data section boundaries
data_start = content.index('const mockSessions: any[] = [')
msg_start = content.index('const mockMessages: any[]')

# Get everything before data and after data
before = content[:data_start]
after_data = content[msg_start:]

# Find the mockAudit end (just before mockMessages)
audit_end = content.index('];', content.index('const mockAudit: any[]'))
audit_end = audit_end + 2  # include ];
between_data_and_msg = content[audit_end:msg_start]

# Build clean data section
clean_data = '''const mockSessions: any[] = [
  { id: "s-1", title: "\u4fEE\u590D auth \u76F8\u5173\u95EE\u9898", status: "active", pinned: true, channel_kind: null, permission: "smart", created_at: "2026-06-09T08:00:00Z", last_message_at: "2026-06-10T14:30:00Z" },
  { id: "s-2", title: "\u914D\u7F6E LLM \u63A5\u53E3\u53C2\u6570", status: "idle", pinned: false, channel_kind: "dingtalk", permission: "full", created_at: "2026-06-08T10:00:00Z", last_message_at: "2026-06-10T11:00:00Z" },
  { id: "s-3", title: "\u65B0\u5BF9\u8BDD", status: "active", pinned: false, channel_kind: null, permission: "smart", created_at: "2026-06-10T09:00:00Z", last_message_at: "2026-06-10T15:00:00Z" },
  { id: "s-4", title: "\u5DF2\u5F52\u6863\u4F1A\u8BDD", status: "idle", pinned: false, archived: true, channel_kind: null, permission: "readonly", created_at: "2026-06-05T08:00:00Z", last_message_at: "2026-06-06T08:00:00Z" },
];
const mockAdminSessions: any[] = [
  { id: "s-1", title: "\u4FEE\u590D auth \u76F8\u5173\u95EE\u9898", status: "active", pinned: true, archived: false, channel_kind: null, channel_account_id: null, username: "admin", user_id: "u-1", message_count: 24, last_message_at: "2026-06-10T14:30:00Z", created_at: "2026-06-09T08:00:00Z" },
  { id: "s-2", title: "\u914D\u7F6E LLM \u63A5\u53E3\u53C2\u6570", status: "idle", pinned: false, archived: false, channel_kind: "dingtalk", channel_account_id: "a-dingtalk-1", username: "alice", user_id: "u-2", message_count: 18, last_message_at: "2026-06-10T11:00:00Z", created_at: "2026-06-08T10:00:00Z" },
  { id: "s-3", title: "\u65B0\u5BF9\u8BDD", status: "active", pinned: false, archived: false, channel_kind: null, channel_account_id: null, username: "admin", user_id: "u-1", message_count: 5, last_message_at: "2026-06-10T15:00:00Z", created_at: "2026-06-10T09:00:00Z" },
  { id: "s-4", title: "\u5DF2\u5F52\u6863\u4F1A\u8BDD", status: "idle", pinned: false, archived: true, channel_kind: null, channel_account_id: null, username: "bob", user_id: "u-3", message_count: 9, last_message_at: "2026-06-06T08:00:00Z", created_at: "2026-06-05T08:00:00Z" },
];
const mockProviders: any[] = [
  { id: "openai", name: "OpenAI", enabled: true, base_url: "https://api.openai.com/v1", model: "gpt-4o-mini", max_tokens: 4096, temperature: 0.2, is_default: true },
  { id: "anthropic", name: "Anthropic", enabled: true, base_url: "https://api.anthropic.com", model: "claude-3-5-sonnet", max_tokens: 8192, temperature: 0.3, is_default: false },
  { id: "deepseek", name: "DeepSeek", enabled: false, base_url: "https://api.deepseek.com", model: "deepseek-chat", max_tokens: 4096, temperature: 0.2, is_default: false },
];
const mockMembers: any[] = [
  { id: "u-1", username: "admin", display_name: "\u7BA1\u7406\u5458", email: "admin@gepaw.dev", is_active: true, org_id: "GE-paw \u6F14\u793A", role: "admin" },
  { id: "u-2", username: "alice", display_name: "Alice \u5F20", email: "alice@gepaw.dev", is_active: true, org_id: "GE-paw \u6F14\u793A", role: "user" },
  { id: "u-3", username: "bob", display_name: "Bob \u674E", email: "bob@gepaw.dev", is_active: false, org_id: "GE-paw \u6F14\u793A", role: "user" },
];
const mockChannels: any[] = [
  { id: "c-1", kind: "dingtalk", name: "\u4E3B\u901A\u9053", enabled: true, status: "running", last_seen_at: "2026-06-10T15:00:00Z" },
  { id: "c-2", kind: "echo", name: "\u56DE\u58F0\u6D4B\u8BD5", enabled: true, status: "running", last_seen_at: "2026-06-10T12:00:00Z" },
  { id: "c-3", kind: "telegram", name: "Telegram", enabled: false, status: "stopped", last_seen_at: null },
];
const mockCrons: any[] = [
  { id: "j-1", name: "\u6BCF\u65E5\u603B\u7ED3", schedule_cron: "0 9 * * *", prompt_template: "\u751F\u6210\u6BCF\u65E5\u72B6\u6001\u6458\u8981", enabled: true, failure_count: 0, last_status: "ok", last_run_at: "2026-06-10T09:00:00Z", next_run_at: "2026-06-11T09:00:00Z" },
  { id: "j-2", name: "\u5468\u62A5", schedule_cron: "0 18 * * 5", prompt_template: "\u751F\u6210\u672C\u5468\u5DE5\u4F5C\u603B\u7ED3", enabled: true, failure_count: 0, last_status: "ok", last_run_at: "2026-06-06T18:00:00Z", next_run_at: "2026-06-13T18:00:00Z" },
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
'''

# Also fix garbled strings in the plugin function (after msg_start)
# Fix new session title
after_data = re.sub(r'body\.title \|\| "[^"]*"', 'body.title || "\u65B0\u4F1A\u8BDD"', after_data)
# Fix chat reply
after_data = re.sub(r'reply: "[^"]*"', 'reply: "\u8FD9\u662F mock \u54CD\u5E94\u3002\u60A8\u53D1\u9001\u4E86\u6D88\u606F\uFF0C\u8BF7\u8FDE\u63A5\u771F\u5B9E LLM\u3002"', after_data)
# Fix new provider name
after_data = re.sub(r'name: body\.name \|\| "[^"]*"(?=.*enabled)', 'name: body.name || "\u65B0\u6A21\u578B"', after_data)
# Fix new cron name
after_data = re.sub(r'name: body\.name \|\| "[^"]*"(?=.*schedule)', 'name: body.name || "\u65B0\u4EFB\u52A1"', after_data)
# Fix wiki log entries
after_data = re.sub(r'"[^"]*\ufffd[^"]*docs/architecture\.md"', '"\u5DF2\u5BFC\u5165\uFF1Adocs/architecture.md"', after_data)
after_data = re.sub(r'"[^"]*\ufffd[^"]*docs/api\.md"', '"\u5DF2\u5BFC\u5165\uFF1Adocs/api.md"', after_data)

result = before + clean_data + after_data

with open(path, 'w', encoding='utf-8') as f:
    f.write(result)

print('Fixed vite.config.ts')
print('U+FFFD count after fix:', result.count('\ufffd'))
print('File length:', len(result))
