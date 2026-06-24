# GE-paw Product Requirements Document (PRD)

> **Document owner:** Repository custodian (Codex)
> **Status:** Living document — updated with every major feature, refactor, or roadmap change
> **Source of truth for:** Module scope, acceptance criteria, milestone targets
> **Not authoritative for:** Code-level design (see `docs/CUSTODIANSHIP.md` for that)

---

## Table of Contents

1. [Document Info](#1-document-info)
2. [Background & Goals](#2-background--goals)
3. [Users & Scenarios](#3-users--scenarios)
4. [Scope](#4-scope)
5. [Product Architecture Overview](#5-product-architecture-overview)
6. [Functional Requirements](#6-functional-requirements)
   - 6.1 [Assistant Mode](#61-assistant-mode)
   - 6.2 [Q&A Mode (LLM-wiki)](#62-qa-mode-llm-wiki)
   - 6.3 [Console (Web UI)](#63-console-web-ui)
   - 6.4 [Channels](#64-channels)
   - 6.5 [Skills](#65-skills)
   - 6.6 [MCP](#66-mcp)
   - 6.7 [Plugins](#67-plugins)
   - 6.8 [Multi-Agent](#68-multi-agent)
   - 6.9 [Memory](#69-memory)
   - 6.10 [Heartbeat / Cron](#610-heartbeat--cron)
   - 6.11 [Coding Mode](#611-coding-mode)
   - 6.12 [Workspace](#612-workspace)
   - 6.13 [Admin Console](#613-admin-console)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [Data Model](#8-data-model)
9. [Deployment & Operations](#9-deployment--operations)
10. [Security & Compliance](#10-security--compliance)
11. [Internationalization & Accessibility](#11-internationalization--accessibility)
12. [Telemetry & Observability](#12-telemetry--observability)
13. [Milestones & Version Plan](#13-milestones--version-plan)
14. [Acceptance Criteria Matrix](#14-acceptance-criteria-matrix)
15. [Risks & Dependencies](#15-risks--dependencies)
16. [Glossary](#16-glossary)

---

## 1. Document Info

| Field | Value |
| --- | --- |
| Product | **GE-paw** (fork of gepaw; "GE-paw" branding in this repo) |
| Repository | `https://github.com/Zcx-BaixiaoBai/GE-paw` |
| Upstream | `https://github.com/agentscope-ai/gepaw` (Apache-2.0) |
| License | Apache-2.0 |
| Python | 3.10 – 3.13 |
| Node | 20 LTS |
| Document version | v0.1.0 (initial draft) |
| Last updated | 2026-06-24 |
| Custodian | Codex AI agent (`docs/CUSTODIANSHIP.md`) |
| Related docs | `README.md`, `README_zh.md`, `CONTRIBUTING.md`, `SECURITY.md` |

### Revision history

| Version | Date | Author | Notes |
| --- | --- | --- | --- |
| v0.1.0 | 2026-06-24 | Codex custodian | Initial PRD draft. Mirrors README + Roadmap; sets acceptance criteria for v1.x. |

---

## 2. Background & Goals

### 2.1 Why this fork exists

GE-paw is a personal-AI-assistant platform that started as a fork of `agentscope-ai/gepaw`
(formerly CoPaw, renamed to gepaw 2026-04-12). Two product strands are bundled:

1. **Assistant mode** — long-running `react_agent` ingesting multi-channel messages
   (IM + Web), driven by scheduled tasks (cron), with centralized token accounting
   and audit.
2. **Q&A mode** — team knowledge base, sourced from `md / pdf / docx / html`, ingested
   using the **LLM-wiki** pipeline (borrowed from
   `SamurAIGPT/llm-wiki-agent`, MIT). Original corpora live only on the server;
   client-side never downloads the raw source files.

### 2.2 Goals

| ID | Goal | Measurable target |
| --- | --- | --- |
| G-1 | Unified assistant runtime | All IM + Web channels route through one `react_agent` instance per workspace. |
| G-2 | Controllable team Q&A | Every Q&A answer must cite ≥ 1 source chunk from the local index. |
| G-3 | Local-first data | User corpora, memory, and secrets stay on the user's machine by default. |
| G-4 | Extension without lock-in | Skills / MCP / Plugin can be installed/removed at runtime without restart. |
| G-5 | Multi-tenant admin | Org admins can audit, throttle, and revoke access without code changes. |
| G-6 | International reach | All UI strings i18n-ready (zh-CN / en / ja / ru baseline). |
| G-7 | Zero-config install | A new user goes from `pip install` to first chat in ≤ 5 minutes. |

### 2.3 Non-goals (this PRD)

- **Not** a model-training platform. GE-paw consumes upstream LLMs; it does not fine-tune.
- **Not** a multi-tenant SaaS. Org-level isolation exists but cross-tenant federation is out of scope.
- **Not** a voice-first product. Voice input is supported (Whisper) but speech synthesis is not on the roadmap.

---

## 3. Users & Scenarios

### 3.1 Personas

| Persona | Description | Primary surface |
| --- | --- | --- |
| **P-1 Individual power user** | Runs gepaw locally on macOS / Windows; uses 1-2 IM channels; expects chat + scheduling. | Console (Web) + DingTalk |
| **P-2 Team lead** | Runs gepaw in Docker / on a cloud VM for a 5–20 person team. Needs admin, audit, multi-agent. | Admin Console + DingTalk/Feishu |
| **P-3 Knowledge-base curator** | Owns a team wiki (md / pdf / docx). Watches ingest progress, fixes broken parses. | Admin Console → Wiki tab |
| **P-4 Developer / contributor** | Wants to add a channel, a skill, an MCP. Reads CONTRIBUTING. | GitHub + local dev env |
| **P-5 Enterprise compliance officer** | Reviews security, audit, data-residency claims. | SECURITY.md + audit logs |

### 3.2 Top scenarios

1. **S-1 Quick chat.** Individual user starts gepaw, configures DashScope API key, chats in Web Console, gets a useful answer in ≤ 30 s.
2. **S-2 IM relay.** User sends "帮我整理今天的知乎热榜" in DingTalk. gepaw posts a streaming summary back into the same conversation.
3. **S-3 Scheduled digest.** User sets a daily 09:00 cron that posts a tech-news digest to a Feishu group.
4. **S-4 Team Q&A.** New joiner asks "我们组的报销流程是什么？". gepaw answers with a citation to `wiki/finance/reimbursement.md`.
5. **S-5 Skill install.** Admin clicks "Install" on a community skill; security scan passes; skill appears in the user's picker.
6. **S-6 Multi-agent debate.** Two agents (`planner`, `critic`) collaborate to draft a PR description.
7. **S-7 Audit.** Admin filters audit log by user, sees all messages + token usage in the last 30 days, exports CSV.

---

## 4. Scope

### 4.1 In scope

- Web Console (React 18 + Vite) — three-pane Codex-style layout
- Channels: DingTalk, Feishu, WeChat Work, Telegram, Discord, Tencent Yuanbao
- Backend: FastAPI + `react_agent` runner
- Skills, MCP, Plugins (in-workspace install + scan)
- Multi-agent orchestration (mission-style loop with `prd.json`)
- Memory (long-term + per-thread)
- Heartbeat / Cron
- Admin Console (10 tabs: Audit / Channels / Crons / Gateway / LLM / MCP / Members / Plugins / Sessions / Skills / Tokens / Wiki)
- Q&A / LLM-wiki ingestion (md / pdf / docx / html)
- Docker / pip / script / desktop install paths
- i18n: zh-CN (default) / en / ja / ru
- OAuth 2.1 MCP, Whisper voice input, dynamic upload limit

### 4.2 Out of scope

- Cross-tenant federation
- Model fine-tuning / RLHF tooling
- Voice synthesis (TTS)
- Native mobile apps (PWA only)
- Server-side GPU provisioning / autoscaling (caller's responsibility)

---

## 5. Product Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                         Console (React 18)                     │
│  ┌─────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │  Left Pane  │  │   Main Pane      │  │  Right Pane      │  │
│  │  Threads /  │  │  Assistant /     │  │  Files / Diff /  │  │
│  │  Sessions   │  │  Q&A / Settings  │  │  Preview / Plan  │  │
│  └─────────────┘  └──────────────────┘  └──────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                              │  HTTPS / JWT
┌─────────────────────────────▼──────────────────────────────────┐
│                  FastAPI Backend (gepaw / gepaw)               │
│  routers: assistant │ admin │ client │ gateway │ channels     │
│  ─────────────────────────────────────────────────────────     │
│  react_agent  ─►  tools (skills) ─►  llm_router ─► providers   │
│       │                                                            │
│       ├── heartbeat / cron  ──►  scheduler                            │
│       ├── mission loop     ──►  prd.json (Phase 1)                    │
│       └── ingest (Q&A)     ──►  wiki_index                             │
└────────────────────────────────────────────────────────────────┘
                              │  external APIs
┌─────────────────────────────▼──────────────────────────────────┐
│   Channels (IM) │ LLM Providers │ MCP │ Skills / Plugins store │
└────────────────────────────────────────────────────────────────┘
```

Storage layers:

- **Working dir** (`gepaw_WORKING_DIR`) — runtime DB, agent state, wiki index, skills.
- **Secret dir** (`gepaw_SECRET_DIR`) — encrypted API keys, channel tokens.
- **Backup dir** (`gepaw_BACKUP_DIR`) — versioned archives for rollback.

---

## 6. Functional Requirements

Each subsection follows the same template:

> **FR-X.Y Title**
> *User story* → *Behavior* → *Acceptance criteria* → *Edge cases* → *Out of scope*

### 6.1 Assistant Mode

**FR-6.1.1 New thread**
- *Story:* As P-1, I open Console and start a fresh conversation.
- *Behavior:* Click "+" → left pane shows new thread id; composer is focused; previous thread is paused but preserved.
- *Acceptance:*
  - POST `/api/threads` returns 201 with `thread_id`.
  - Composer is auto-focused within 200 ms of click.
  - Previous threads remain listed with their last-touched timestamp.
- *Edge cases:* localStorage cleared → graceful fallback to server-side list.
- *Out of scope:* thread archival / auto-merge.

**FR-6.1.2 Send message**
- *Story:* As P-1, I type a prompt and hit Enter.
- *Behavior:* User input is queued, sent to `/api/threads/{id}/messages`, stream tokens back into the bubble; abort button appears mid-stream.
- *Acceptance:*
  - Enter sends; Shift+Enter inserts newline.
  - Abort cancels in-flight generation within 1 s.
  - Failed request shows a retry button that reuses the same draft.
- *Edge cases:* network drop → message marked `failed`, draft preserved; reconnect auto-retries once.

**FR-6.1.3 Slash commands**
- *Story:* As P-1, I type `/` to see available commands.
- *Behavior:* Dropdown lists `clear`, `compact`, `model`, `perm`, `skill …`, `cron …`.
- *Acceptance:*
  - `/compact` triggers context compression.
  - `/model llama3` switches the active model for the thread.
  - Unknown slash commands render as plain text.

**FR-6.1.4 Reasoning selector**
- *Story:* As P-1, I pick "low / medium / high" reasoning effort before sending.
- *Behavior:* Dropdown inside composer; persists per thread.
- *Acceptance:*
  - Selection sent as `reasoning_effort` to backend.
  - Backend maps to model-supported effort levels; unknown levels rejected with 400.

**FR-6.1.5 Permission selector**
- *Story:* As P-1, I scope what the agent can touch.
- *Behavior:* Dropdown: `read-only`, `workspace`, `system` (each requires confirm modal on first use).
- *Acceptance:*
  - Inline approval card surfaces whenever a tool call exceeds the granted scope (see FR-6.13.7).

**FR-6.1.6 Inline approval**
- *Story:* As P-1, an agent wants to write a file; I approve / deny inline.
- *Behavior:* Approval card slides in over the message bubble; user clicks ✓ / ✗.
- *Acceptance:*
  - Card disappears after click; agent receives an `approve` / `deny` callback.
  - Timeout (60 s default) auto-denies and surfaces a "denied" badge.

**FR-6.1.7 Tool-call card**
- *Story:* As P-1, I see what tools the agent invoked.
- *Behavior:* Card expands to show args + result; collapses by default.
- *Acceptance:* Click chevron toggles expansion; copy-to-clipboard works for args/result.

### 6.2 Q&A Mode (LLM-wiki)

**FR-6.2.1 Wiki ingest**
- *Story:* As P-3, I point gepaw at `wiki/`, kick off ingest.
- *Behavior:* Walks directory, parses md/pdf/docx/html, splits into chunks, embeds, stores in vector index.
- *Acceptance:*
  - Progress bar (per file) in Admin → Wiki tab.
  - Failed files surface in an error list with reason; success files can be re-indexed.
  - Idempotent: re-ingest updates rather than duplicates.

**FR-6.2.2 Q&A query**
- *Story:* As P-2, I ask a question.
- *Behavior:* top-K chunks retrieved, LLM synthesizes answer with citations.
- *Acceptance:*
  - Every answer shows ≥ 1 inline citation chip.
  - Citations are clickable; opens source preview in right pane.
  - If similarity < threshold, fallback answer: "未找到相关资料" + suggest terms.

**FR-6.2.3 Source preview**
- *Story:* As P-2, I click a citation.
- *Behavior:* Right pane shows the source file's rendered content (md → HTML, pdf → text + page jump).
- *Acceptance:*
  - Raw source files are never exposed; only the rendered/chunked view.
  - PDF preview shows page number alongside chunk.

### 6.3 Console (Web UI)

**FR-6.3.1 Three-pane layout**
- *Story:* As P-1, my screen shows left/middle/right panes that I can resize and collapse.
- *Behavior:* Resize handles, collapse buttons; layout persists in `localStorage`.
- *Acceptance:*
  - On 1280×800 minimum viewport, all panes are visible (no horizontal scroll).
  - Layout state restored on next visit.

**FR-6.3.2 Theming**
- *Story:* As P-1, I toggle dark / light / system theme.
- *Behavior:* Theme menu in top bar; CSS variables swap; transition ≤ 200 ms.
- *Acceptance:* No flash-of-wrong-theme on page load.

**FR-6.3.3 i18n switcher**
- *Story:* As P-1, I switch UI language.
- *Behavior:* Settings → Language; persists per user.
- *Acceptance:* All visible strings come from i18n bundles; missing keys render the English fallback and log a warning.

**FR-6.3.4 Composer states**
- *Behavior:* empty / typing / filled / sending / error / sent.
- *Acceptance:* Each state has a distinct visual cue; transitions animated ≤ 150 ms.

### 6.4 Channels

**FR-6.4.1 Channel abstraction**
- Each channel implements `send`, `receive`, `stream_chunk`, `reply_in_thread` interfaces.
- A new channel = a new module in `src/gepaw/app/channels/<name>/` + a router entry.

**FR-6.4.2 Supported channels (v1.x)**

| Channel | Status | Streaming | Thread reply | Notes |
| --- | --- | --- | --- | --- |
| DingTalk | ✅ Stable | ✅ | ✅ | streaming_enabled config knob |
| Feishu | ✅ Stable | ✅ | ✅ (since v1.1.10) | |
| WeChat Work | ✅ Stable | ⚠️ partial | n/a | text + image |
| Telegram | ✅ Stable | ✅ | ✅ | |
| Discord | ✅ Stable | ✅ | ✅ | |
| Tencent Yuanbao | ✅ (since v1.1.10) | ✅ | ✅ | |

- *Acceptance per channel:*
  - Health check via `/api/channels/<name>/health`.
  - Disabling a channel stops inbound delivery within 60 s.

**FR-6.4.3 Channel config**
- Stored in `secret_dir`; never sent to client.
- Each channel exposes a typed config schema validated server-side on save.

### 6.5 Skills

**FR-6.5.1 Built-in skills**
- Scheduler (cron expression)
- PDF / Office processing
- News digest
- Web search (Tavily)

**FR-6.5.2 Custom skill install**
- *Story:* As P-2, I drop a skill folder into `skills/` or paste a Git URL.
- *Behavior:* gepaw validates the manifest, runs the security scan (FR-10.2), loads.
- *Acceptance:*
  - Skill appears in the picker within 5 s.
  - Uninstall removes it and clears any state.
  - Hot-reload: skill code changes apply without restart.

**FR-6.5.3 Skill manifest schema**
- Required fields: `name`, `version`, `entry`, `permissions[]`, `triggers[]`.
- Optional: `config`, `dependencies`, `homepage`.

### 6.6 MCP

**FR-6.6.1 OAuth 2.1 MCP** (since v1.1.7)
- *Story:* As P-2, I connect a remote MCP server via OAuth.
- *Behavior:* Console walks the user through authorization-code flow, refresh tokens stored in `secret_dir`.
- *Acceptance:* Token refresh happens automatically; failed refresh surfaces a re-authorize banner.

**FR-6.6.2 Local MCP stdio**
- Standard `mcp.json` schema; child process per server.

**FR-6.6.3 MCP health**
- `/api/mcp/<id>/health` returns OK / degraded / down with last-check timestamp.

### 6.7 Plugins

**FR-6.7.1 Plugin distribution**
- Official channel: `plugins/` repo bundles; third-party: install via URL or local file.
- *Acceptance:* Plugin manifest must declare API version compatibility.

**FR-6.7.2 Plugin updates**
- Stable check (every 24 h) on the plugin registry.
- Updates require admin confirmation before applying.

### 6.8 Multi-Agent

**FR-6.8.1 Multiple agents per workspace**
- *Story:* As P-2, I create `planner` and `critic` agents.
- *Behavior:* Each agent has its own system prompt, model, skills; user picks the active one.
- *Acceptance:* Switching agents preserves thread history.

**FR-6.8.2 Mission loop**
- *Story:* As P-2, I dispatch a multi-step task.
- *Behavior:*
  1. **Phase 1 (decompose):** master agent produces `prd.json` (`stories[]`).
  2. **Phase 2 (execute):** workers pick `passes=false` stories, run, mark `passes=true`.
  3. **Phase 3 (review):** reviewer agent audits `prd.json` progress.
- *Acceptance:*
  - `prd.json` schema validation runs before phase 2 starts; failure aborts the loop.
  - Each story's `acceptanceCriteria` is enforced by an explicit test (if provided).
  - Loop is resumable after crash.

**FR-6.8.3 Subagent spawn**
- `spawn_subagent` tool (since v1.1.10) for ephemeral in-workspace sub-agent execution.
- Lifecycle: spawn → run → return result → terminate.

**FR-6.8.4 Group chat** (planned v1.x)
- Multiple agents visible in one thread; each user message fan-outs to all.

### 6.9 Memory

**FR-6.9.1 Long-term memory**
- *Story:* As P-1, the agent remembers my preferences across sessions.
- *Behavior:* Each user turn is summarized into a memory record; retrieval uses semantic search.
- *Acceptance:*
  - User can browse / delete memory entries in Settings.
  - Memory can be exported as JSON.

**FR-6.9.2 Per-thread memory**
- Scoped to a single thread; cleared when the thread is deleted.

**FR-6.9.3 Memory-evolving & proactive**
- Agent reflects after each session; weekly digest of learned preferences surfaced to user.

### 6.10 Heartbeat / Cron

**FR-6.10.1 Cron scheduler**
- UTC-based; crontab syntax; calendar view in Admin → Crons (since v1.1.7).
- *Acceptance:* Calendar highlights runs, failures, and skipped runs.

**FR-6.10.2 Heartbeat**
- Periodic check-in (default 30 min) summarizing new events; delivers to user-chosen channel.

### 6.11 Coding Mode

**FR-6.11.1 Three-panel Web IDE** (since v1.1.9)
- Left: file tree; middle: editor (Monaco); right: chat with selected code.

**FR-6.11.2 LSP integration**
- Python (pyright) out of the box; TS via `tsserver`.

**FR-6.11.3 Workspace versioning**
- Snapshot before destructive tool calls; one-click rollback.

**FR-6.11.4 Runtime**
- Sandbox for executing code in the user's environment.

**FR-6.11.5 Open Directory tab** (since v1.1.10)
- Reference local projects without copying into the workspace.

### 6.12 Workspace

**FR-6.12.1 Subfolder layout** (planned)
- Auto-suggested split: `config/`, `production/`, `scratch/`.

**FR-6.12.2 File access guard**
- Default deny outside `working_dir`; explicit allowlist for system paths (e.g., `~/.gepaw/`).

**FR-6.12.3 Sandbox integration** (in progress)
- For risky tools, run inside a sandbox (Docker or nsjail); logs surfaced in Admin → Audit.

### 6.13 Admin Console

The Admin Console exposes 12 tabs (status = this fork):

| Tab | Purpose | Key endpoints |
| --- | --- | --- |
| Audit | Search & export audit logs | `/api/admin/audit` |
| Channels | Channel enable/disable + per-channel config | `/api/admin/channels/*` |
| Crons | Cron list / calendar | `/api/admin/crons/*` |
| Gateway | Provider routing rules | `/api/admin/gateway/*` |
| LLM | Model providers, key mgmt, test connection | `/api/admin/llm/*` |
| MCP | MCP server list + health | `/api/admin/mcp/*` |
| Members | Org members / roles | `/api/admin/members/*` |
| Plugins | Plugin registry | `/api/admin/plugins/*` |
| Sessions | Active sessions | `/api/admin/sessions/*` |
| Skills | Skill registry | `/api/admin/skills/*` |
| Tokens | Token usage (per-user / per-day / per-model) | `/api/admin/tokens/*` |
| Wiki | Ingest progress + failures | `/api/admin/wiki/*` |

**FR-6.13.1 Admin auth**
- Role-based: `admin`, `operator`, `viewer`.
- 2FA for `admin` role.

**FR-6.13.2 Audit log retention**
- Default 90 days; configurable up to 1 year.

**FR-6.13.3 Token usage view**
- Daily / weekly / monthly breakdown; CSV export; per-model cost calculation.

**FR-6.13.4 Members management**
- Invite by email; assign role; revoke.

**FR-6.13.5 Channels admin**
- Toggle channel; rotate webhook tokens; inspect last-error.

**FR-6.13.6 Cron admin**
- Create / pause / delete cron; see last 100 runs.

**FR-6.13.7 Permission / scope escalation**
- Every admin action that changes user-visible behavior requires justification text.

---

## 7. Non-Functional Requirements

### 7.1 Performance

| Metric | Target |
| --- | --- |
| First chat token (cold cache) | ≤ 3 s p50, ≤ 6 s p95 |
| First chat token (warm) | ≤ 1.5 s p50, ≤ 3 s p95 |
| Console TTI on 4G | ≤ 2.5 s |
| Wiki ingest throughput | ≥ 5 MB/s on NVMe |
| Concurrent active threads per agent | ≥ 32 |

### 7.2 Reliability

- Process restart within 10 s on crash (systemd / Docker restart policy).
- Backup archive created every 6 h; last 7 archives retained.
- RPO ≤ 6 h; RTO ≤ 30 min.

### 7.3 Scalability

- Single-host baseline: 50 concurrent users, 500 threads/day.
- Horizontal scale path: stateless FastAPI behind a load balancer; sticky session for WebSocket.

### 7.4 Maintainability

- Lint: black + ruff for Python; eslint + prettier for TS.
- Type check: mypy strict for `src/gepaw/`; `tsc --noEmit` for `web/`.
- Test pyramid: ≥ 60 % unit, 20 % integration, 20 % e2e.

### 7.5 Portability

- Linux x86_64 / arm64, macOS x86_64 / arm64, Windows 10+.
- Python 3.10 – 3.13; Node 20 LTS.

---

## 8. Data Model

(Selected entities only; full schema lives in code under `src/gepaw/models/`.)

### 8.1 Core entities

- `User` — id, email, role, locale, created_at, last_seen_at.
- `Thread` — id, user_id, title, model, created_at, updated_at, archived_at.
- `Message` — id, thread_id, role (`user` / `assistant` / `tool`), content, tool_calls, token_usage, created_at.
- `Skill` — id, name, version, manifest_json, enabled, permissions, installed_at.
- `MCPServer` — id, name, transport, config (encrypted), health_status.
- `Channel` — id, type, config (encrypted), enabled, last_health_at.
- `Cron` — id, name, schedule, action, last_run_at, last_status.
- `WikiSource` — id, path, sha256, last_indexed_at, status.
- `WikiChunk` — id, source_id, ordinal, content, embedding, metadata.
- `AuditEvent` — id, actor_id, action, target, payload_json, created_at.
- `PRD` — mission-loop id, loop_dir, current_phase, prd_json_path.

### 8.2 Retention

| Entity | Default | Configurable |
| --- | --- | --- |
| `Message` | unbounded | archive after 365 d |
| `AuditEvent` | 90 d | up to 365 d |
| `WikiSource` chunks | while file exists | manual purge |
| Telemetry | 90 d | no |

---

## 9. Deployment & Operations

### 9.1 Install paths (user-facing)

- `pip install gepaw` (PyPI)
- One-line script (macOS / Linux / Windows)
- Docker (Docker Hub + Alibaba ACR)
- Alibaba Cloud ECS one-click
- ModelScope Studio (cloud-hosted)
- Desktop app (Tauri, Windows / macOS) — beta

### 9.2 Local storage layout

```
~/.gepaw/
├── bin/                 # CLI entrypoints
├── working/             # gepaw_WORKING_DIR
│   ├── agents/<id>/
│   ├── skills/
│   ├── mcp/
│   ├── wiki/
│   └── gepaw.db
├── working.secret/      # gepaw_SECRET_DIR (encrypted at rest)
└── working.backups/     # gepaw_BACKUP_DIR
```

### 9.3 Configuration

- Env vars prefixed `gepaw_` (e.g. `gepaw_WORKING_DIR`).
- `.env` file in working dir; secrets never committed (`.gitignore` covers).
- `gepaw init` produces `.env.example`.

### 9.4 Backup & restore

- Automatic archives every 6 h.
- Restore command: `gepaw restore <archive>`.

### 9.5 Upgrade

- In-place upgrade supported across patch + minor versions.
- Major upgrade requires rebuild of frontend (`console/dist`).

---

## 10. Security & Compliance

### 10.1 Threat model (summary)

| Threat | Mitigation |
| --- | --- |
| Prompt injection via skills / docs | Skill security scan; sandboxing of tool calls |
| Data exfiltration to third parties | Local-first default; explicit channel routing |
| Token leakage | Secrets in `secret_dir`, env never logged |
| Privilege escalation via admin actions | Role separation; justification required |
| Supply-chain (skill / plugin) | Manifest signing (planned) |

### 10.2 Skill security scanning

On install, the skill scan checks for:

- Prompt-injection patterns
- Command-injection sinks
- Hardcoded API keys / tokens
- Data-exfiltration attempts (outbound HTTP to non-allowlisted hosts)
- File-system writes outside working dir

A failing scan blocks install and surfaces the reason.

### 10.3 Web authentication

- Optional; `gepaw_AUTH_ENABLED=true` to enable.
- JWT-based; refresh tokens stored in `secret_dir`.

### 10.4 Compliance posture

- Apache-2.0 license.
- Telemetry is opt-in, anonymous, version-once.
- No personal data collected; no file contents uploaded by default.

### 10.5 Vulnerability reporting

Per `SECURITY.md` — Alibaba Security Response Center (ASRC).

---

## 11. Internationalization & Accessibility

### 11.1 Languages

Baseline: `zh-CN` (default), `en`, `ja`, `ru`. Each PR adding a new visible string
must update all four bundles.

### 11.2 Accessibility

- WCAG 2.1 AA target.
- Keyboard nav for all interactive elements.
- Color contrast ≥ 4.5:1 for body text.
- Focus rings visible; `aria-label` on icon-only buttons.

---

## 12. Telemetry & Observability

### 12.1 Anonymous telemetry (opt-in)

Collected at `gepaw init` once per version:

- gepaw version, install method, OS, Python version, CPU arch, GPU availability.

**Not collected:** personal data, files, credentials, IPs.

### 12.2 Server-side metrics

- Per-user / per-thread token usage (token table).
- Per-model latency p50/p95.
- Tool-call success rate.
- Channel delivery rate.

### 12.3 Logging

- Structured JSON logs to `working/logs/`.
- Rotation: daily, retain 14 days.
- Log level configurable per module.

---

## 13. Milestones & Version Plan

| Milestone | Target date | Scope |
| --- | --- | --- |
| **v1.1.11** (this fork's next patch) | 2026-Q3 | Subagent visualization (partial), token-by-day chart polish, gateway i18n parity |
| **v1.2.0** | 2026-Q3 | OAuth in admin, Response API, subagent visualization |
| **v1.3.0** | 2026-Q4 | Workspace subfolder layout, file-access sandbox v1 |
| **v1.4.0** | 2027-Q1 | Group chat, user-selectable context compression |
| **v1.5.0** | 2027-Q2 | gepaw Creator GA, gepaw Insight GA |

Status legend:

- **In Progress** — actively being worked on
- **Planned** — queued or under design
- **Seeking Contributors** — community welcome

---

## 14. Acceptance Criteria Matrix

A change is merge-ready only if **every** row relevant to it is checked.

### 14.1 Code quality

- [ ] `pytest -q` passes locally (≥ 95 % of touched modules have tests).
- [ ] `ruff check src/` clean.
- [ ] `mypy src/gepaw` clean for new/changed files.
- [ ] `cd web && npm run build` succeeds.
- [ ] `cd web && npm run lint` clean for changed files.

### 14.2 Functional

- [ ] New / changed user-visible strings exist in all four i18n bundles.
- [ ] New API endpoints have OpenAPI docstrings + at least 1 happy-path test.
- [ ] New tool calls require permission scope; default-deny.
- [ ] New skill installs trigger the security scan.

### 14.3 Security

- [ ] No secret strings in code or logs.
- [ ] No new outbound HTTP without allowlist.
- [ ] Auth-protected endpoints verify JWT + role.

### 14.4 Operations

- [ ] Backward-compatible DB migrations.
- [ ] Backup still produced; restore tested on a copy.
- [ ] `docs/PRD.md` updated if scope or acceptance criteria changed.

### 14.5 Documentation

- [ ] `CHANGELOG` entry under the unreleased section.
- [ ] README / docs updated for user-visible changes.
- [ ] If deprecation: deprecation note + 1-version grace period.

---

## 15. Risks & Dependencies

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Upstream gepaw drifts | Feature gaps / merge conflicts | Track upstream weekly; rebasing plan |
| LLM provider API changes | Broken chat | Provider adapters isolated; integration tests mock providers |
| Skill supply-chain | Code execution in user env | Scan + sandbox |
| Token cost surprises | Org budget overrun | Token table + per-org cap (planned) |
| Wiki parser edge cases | Ingest failures | Per-format regression tests; manual override path |

External dependencies: DashScope / OpenAI / Anthropic APIs, DingTalk / Feishu
/ Telegram / Discord SDKs, MCP reference servers.

---

## 16. Glossary

| Term | Definition |
| --- | --- |
| **Agent** | A configured runtime combining system prompt, model, skills, and tools. |
| **Channel** | An IM integration (DingTalk, Feishu, etc.). |
| **Cron** | A scheduled task. |
| **Heartbeat** | Periodic agent self-check. |
| **LLM-wiki** | Q&A pipeline from `SamurAIGPT/llm-wiki-agent`. |
| **Mission loop** | Multi-agent task runner using `prd.json`. |
| **MCP** | Model Context Protocol. |
| **Permission scope** | What an agent is allowed to touch (`read-only` / `workspace` / `system`). |
| **PRD (mission)** | Per-loop task list, NOT this document. |
| **Skill** | A reusable capability registered with the agent. |
| **Thread** | A single conversation. |
| **Working dir** | `gepaw_WORKING_DIR`, the on-disk home of agent state. |

---

## Appendix A — Acceptance walkthrough

For each in-flight feature, the custodian opens a Draft PR and ticks the relevant
boxes from §14. When all boxes are checked, the PR is moved out of draft and merged
into `main`.

## Appendix B — Change log for this PRD

- v0.1.0 (2026-06-24) — Initial draft; mirrors README + Roadmap.
