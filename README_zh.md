<div align="center">

# GE-paw

[![License](https://img.shields.io/badge/license-Apache%202.0-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20~%20%3C3.14-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18-61dafb.svg)](https://react.dev/)

GE-paw 是一个面向团队使用的多租户智能体平台，源自 [QwenPaw](https://github.com/agentscope-ai/QwenPaw)（Apache-2.0）并叠加 [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent)（MIT）的 **LLM-wiki** 思路。

GE-paw 提供两条产品线：

- **助手模式**：会话管理、多频道接入（飞书 / 钉钉 / 企业微信 / Telegram / Discord 等）、定时任务 (cron)、Token 用量计量、Skill / MCP / Plugin 注入。
- **问答模式**：把团队文档（md / pdf / docx / html …）整编成可检索的本地知识库，对话带引用；**语料全部托管在服务端，客户端进程零落盘**。

终端用户登录后看到的是一致的 **Codex 风格三栏界面**：左侧会话导航、中部当前模式内容、右侧可折叠多 Tab 容器（Files / Web，预留 Diff / Preview / Plan）。所有 LLM 端点、Skill、MCP、Plugin、Channel、Cron 由组织管理员统一配置，**终端用户不可自配**。

</div>

---

## 目录

- [产品定位](#产品定位)
- [架构总览](#架构总览)
- [快速开始](#快速开始)
- [管理员操作手册](#管理员操作手册)
- [问答模式与客户端零落盘](#问答模式与客户端零落盘)
- [安全合规](#安全合规)
- [部署](#部署)
- [项目结构](#项目结构)
- [测试](#测试)
- [许可证](#许可证)

## 产品定位

GE-paw 解决两个问题：

1. **统一的助手运行时**：多渠道消息（IM / Web）汇总到同一个 react_agent；定时任务、token 计量、审计集中可观测。
2. **可控的团队问答**：把团队知识库（产品文档、Wiki、流程）以「llm-wiki」风格整编，提问得到带来源引用的回答，**且所有原始语料只在服务端存在**——避免多端同步和客户端泄密。

后端完全自托管，**LLM 仅支持 OpenAI 兼容协议**（v1 强制），指向任意兼容端点即可。

## 架构总览

```
[Browser / Tauri / IM channel]                [Admin browser]
        |                                              |
        | /api/client/*              /api/admin/*       |
        v                                              v
                  +---------------------------------+
                  |   gepaw serve  (FastAPI)        |
                  |   - routers: auth/admin/client  |
                  |   - APScheduler (cron)          |
                  |   - Channel listeners           |
                  +---------------------------------+
                          |              |
                          v              v
               [data/gepaw.db]   [data/orgs/<id>/wiki/]
               (SQLite / PG)     raw / wiki / graph
                          |
                          v
                  [External LLM endpoint]   (OpenAI compatible)
```

详细分层、Wiki 流水线、前端三栏设计见 `docs/architecture.md`。

## 快速开始

### 1. 准备环境

- Python 3.10–3.13（推荐 3.12）
- Node.js 20+（仅在重新构建前端时需要）
- Windows / macOS / Linux

### 2. 安装后端

```bash
git clone <your-gepaw-fork-url> gepaw
cd gepaw
python -m venv .venv
.venv/Scripts/activate           # Windows
# source .venv/bin/activate      # macOS / Linux
pip install -e .
```

### 3. 初始化

```bash
python -m gepaw init --username admin --password "YourStrongPass" --org-name "Default"
```

CLI 会自动生成一个 `GEPAW_SECRET_KEY`（Fernet 主密钥）并写入 `.env`。

### 4. 启动

```bash
python -m gepaw serve --host 0.0.0.0 --port 8765
```

打开 http://127.0.0.1:8765/ ，使用上面创建的 admin 账号登录。

### 5. 启用 Web 控制台

如果是从源码全新 clone，需要先构建前端 dist：

```bash
cd web
npm install --ignore-scripts     # 避免 esbuild postinstall 触发 native 编译
npm run build
cd ..
python -m gepaw serve --port 8765
```

`web/dist/` 会被 FastAPI 通过 `StaticFiles` 托管。生产部署请改用 `docker compose`（见下文）。

## 管理员操作手册

### 配置 LLM 端点

`/admin/llm` → Add endpoint

- Name：标识符（org 内唯一）
- Base URL：`https://api.openai.com/v1` 或任意 OpenAI 兼容端点
- API Key：服务端用 Fernet 加密落库，前端不返回明文
- Model：模型 ID（gpt-4o-mini / qwen-plus / deepseek-chat …）
- Default：是否组织默认

未配置任何端点时，问答模式走 stub 提示，便于本地调试。

### 启用频道

`/admin/channels` → 选 kind (telegram / feishu / wecom / dingtalk / discord / matrix / mattermost / mqtt / onebot / qq / imessage / sip / voice / wechat / xiaoyi / yuanbao) → 填凭据。服务启动时只会加载 settings.toml 与 `channel_account` 表的并集。

### 调度 cron

`/admin/crons` → 表达式 (croniter 5/6 字段) → 目标（写入指定会话 / 推送到 IM / 仅审计）。连续 3 次失败自动禁用并写 `audit_log`。

### Skill / MCP / Plugin

`/admin/skills` `/admin/mcp` `/admin/plugins` 三处分别维护。客户端 `/api/client/config` 仅下发 `enabled=True` 的项。

### Wiki 语料管理

`/admin/wiki` 页：

- 上传 md / txt / pdf / docx / pptx / xlsx / html / csv / json，URL 走 `trafilatura`。
- 触发「批量 ingest」：服务端读源文件 → 落 `data/orgs/<id>/wiki/raw/` → 写 `wiki_source` 记录。
- 「Compile index」：基于已 ingest 的源重新生成 `wiki/index.md` / `wiki/overview.md`。
- 「Lint」：孤立页面与 broken 引用检测。
- 「Reset」：清空当前 org 的全部语料 + DB 记录。

## 问答模式与客户端零落盘

**核心约束**：所有 wiki 资产（`raw/`、`wiki/`、`graph/`、源文件、查询日志）只存在于服务端磁盘。客户端进程、浏览器、Tauri 沙箱**不存任何 wiki 文件副本**、不做持久化缓存、Service Worker 不预缓存 wiki 路径。

为保证这一约束：

| 层       | 措施 |
|----------|------|
| 后端     | `/api/client/wiki/*` 强制注入 `Cache-Control: no-store`（`WikiNoStoreMiddleware`） |
| 后端     | 客户端只读 `wiki/` 子树；`raw/` 和 `graph/` 在 `_safe_subpath` 中显式拒绝 |
| 后端     | 客户端路径越权（`..` / 跨 org）返回 403 / 404 |
| 前端     | React Query / SWR 仅做内存缓存；`zustand persist` 只持久化 `auth.token` + `tabs` UI 状态 |
| 前端     | 切换组织 / 语料时主动 `invalidateQueries` + 清空 Web Tab iframe |
| Tauri    | WebView 的 HTTP 缓存对 wiki 路径设 `no-store`；不下载源文件到 `app_data_dir` |
| 文档     | Wiki 后端存储抽象为 `WikiStore`，v1 实现 `FilesystemWikiStore`，v2 可替换为 S3/OSS |

`Cache-Control: no-store` 由 FastAPI 中间件统一注入到 `/api/client/wiki` 和 `/api/admin/wiki` 的响应。

## 安全合规

- 敏感字段（API Key、Channel 凭据）统一用 `cryptography.Fernet` 加密，主密钥 `GEPAW_SECRET_KEY`。
- 管理员与普通用户通过 JWT 区分：access 15 min，refresh 7 d（可吊销，落 `refresh_token` 表）。
- 所有 admin 端点走 `require_admin`，跨组织访问会被自动 403。
- Wiki 预览渲染用 `markdown` + `bleach` 白名单；Web Tab iframe `sandbox="allow-scripts allow-same-origin allow-forms"`。
- 完整审计：`audit_log` 表记录所有 admin 写入（LLM/Skill/MCP/Plugin/Channel/Cron/Wiki/Reset），可在 `/admin/audit` 查询。

## 部署

### 单进程开发模式

```bash
python -m gepaw serve --port 8765
```

### Docker Compose（推荐）

```bash
cp deploy/.env.example deploy/.env
# 修 deploy/.env，至少改 GEPAW_SECRET_KEY / GEPAW_ADMIN_PASSWORD
docker compose up -d --build
# 初始化（首次部署）
docker compose exec api python -m gepaw init \
    --username admin --password "YourStrongPass" --org-name Default
# 访问
# http://127.0.0.1:8080      # Web 控制台
# http://127.0.0.1:8080/api/health
```

切到 Postgres：把 `docker-compose.yml` 的 `db:` 段打开，并在 `deploy/.env` 设置 `GEPAW_DATABASE_URL`。

### Tauri 桌面壳

v1 未包含。计划：把 `gepaw serve` 打成 sidecar，WebView 加载 `http://127.0.0.1:8765/`；WebView HTTP 缓存对 `/api/client/wiki/*` 强制 `no-store`，禁止下载源文件到 `app_data_dir`。

## 项目结构

```
gepaw/
+- src/gepaw/
|  +- app/
|  |  +- _app.py            FastAPI 入口 + lifespan + middleware
|  |  +- settings.py        pydantic-settings, env 前缀 GEPAW_
|  |  +- db.py              SQLAlchemy 2.x 同步引擎 + WAL/FK pragma
|  |  +- cors.py            CORS + WikiNoStoreMiddleware
|  |  +- deps.py            Principal + require_user/require_admin + JWT 解码
|  |  +- audit.py           write_audit(...)
|  |  +- scheduler.py       APScheduler (cron 触发 / heartbeat)
|  |  +- routers/
|  |     +- auth.py         /api/auth/{login,refresh,logout,me}
|  |     +- admin.py        /api/admin/* (orgs/users/llm/skills/mcp/plugins/channels/crons/tokens/sessions/wiki/audit)
|  |     +- client.py       /api/client/* (config/sessions/messages/chat/stream/wiki/fs)
|  +- models/               identity / llm / assistant / wiki / audit
|  +- security/             crypto (Fernet) / passwords (bcrypt) / jwt
|  +- token_usage/          record_usage + manager (by_day/by_user/by_model) + cost_table
|  +- channels/             base / manager / registry / access_control + kinds/echo (IM bridges)
|  +- routers/webhook.py    POST /api/webhook/<kind>  (external IM callbacks)
|  +- wiki/
|  |  +- store.py           WikiStore 抽象 + FilesystemWikiStore
|  |  +- pipeline.py        ingest / compile / lint / query
|  |  +- llm_client.py      OpenAI 兼容 + stub
|  |  +- markitdown_adapter.py
|  +- cli/main.py           gepaw init / serve / health
|  +- constant.py
+- web/                     React 18 + Vite + TypeScript (Codex 风格)
|  +- src/
|  |  +- layouts/AppLayout.tsx           三栏布局
|  |  +- components/RightPane/           右侧多 Tab 容器
|  |  +- components/RightPane/tabs/      FilesTab / WebTab / DiffTab / PreviewTab / PlanTab
|  |  +- pages/{Login,Assistant,QnA}/
|  |  +- pages/Admin/                    LLM / Members / Channels / Crons / Tokens / Sessions / Wiki / Audit
|  |  +- stores/{auth,tabs}.ts           zustand
|  |  +- lib/api.ts                      fetch 封装 (Cache-Control: no-store)
+- deploy/
|  +- Dockerfile
|  +- nginx.conf
|  +- .env.example
+- tests/                   单元测试
+- scripts/smoke.py         端到端冒烟
+- docs/architecture.md
+- docker-compose.yml
+- pyproject.toml
```

## Token 计量与成本跟踪

每一次 LLM 调用都会被 `gepaw.token_usage.record_usage` 拦截并写入 `token_usage_log`，无论调用来自：
- 助手聊天（/api/client/chat, /api/client/chat/stream）
- Cron 定时任务（每次 _execute_cron）
- 渠道消息（telegram/feishu/...）
- 问答模式（/api/client/wiki/query）

管理员可在 Web 控制台 → Tokens 看到：
- /api/admin/tokens/summary：按模型聚合
- /api/admin/tokens/by_day：最近 N 天每日趋势
- /api/admin/tokens/by_user：按用户用量排名
- /api/admin/tokens/month_to_date：当前自然月累计
- /api/admin/tokens/cost_table：默认 + 自定义费率（每千 token 美分）
- /api/admin/tokens/cost_table/{model}（PUT/DELETE）：覆盖或清除某模型费率

费率默认覆盖 gpt-4o / gpt-4o-mini / o1 / o3-mini / claude-3-5-sonnet 等常见模型；未知模型返回 0 cost。

## 测试

```bash
# 单元测试
pytest tests/ -v

# 端到端冒烟（需先启动 gepaw serve）
python scripts/smoke.py           # login → LLM → skill/mcp/plugin → wiki 上传/口语化
python scripts/smoke_token.py     # token_usage 落库 + 成本报表
python scripts/smoke_channel.py   # 渠道：创建 echo 账号 → webhook 注入 → 会话落库 + token_usage
```

冒烟脚本会跑：

1. 管理员登录 → 配 LLM → 上传 md → 触发批量 ingest → 编译 → lint。
2. 客户端拉 `/api/client/config` → 拉 `/api/client/wiki/tree` → 跑 `/api/client/wiki/query`。
3. 断言：raw / graph 子树 403；`..` 路径 403；stub 模式返回提示。

## 许可证

主代码 Apache-2.0（继承自 QwenPaw）。`llm-wiki-agent` 部分保留 MIT，已在 `NOTICE` / `THIRD_PARTY` 中声明。

---

[English README](README.md) | [架构文档](docs/architecture.md)
