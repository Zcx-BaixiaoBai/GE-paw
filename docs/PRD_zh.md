# GE-paw 产品需求文档（PRD）

> **文档所有者：** 仓库代管（Codex）
> **状态：** 活文档 —— 随每次重大功能、重构、Roadmap 变更更新
> **以下事项的唯一权威来源：** 模块范围、验收标准、里程碑目标
> **不负责：** 代码级设计（见 `docs/CUSTODIANSHIP.md`）

> **翻译约定：** 描述性文字译为中文；专业术语（API、JWT、MCP、LSP、i18n、PR 等）保留英文。表格、命令、路径、配置项、版本号原样保留。

---

## 目录

1. [文档信息](#1-文档信息)
2. [背景与目标](#2-背景与目标)
3. [用户与场景](#3-用户与场景)
4. [范围](#4-范围)
5. [产品架构总览](#5-产品架构总览)
6. [功能需求](#6-功能需求)
   - 6.1 [Assistant 模式](#61-assistant-模式)
   - 6.2 [Q&A 模式（LLM-wiki）](#62-qa-模式llm-wiki)
   - 6.3 [Console（Web UI）](#63-consoleweb-ui)
   - 6.4 [Channels](#64-channels)
   - 6.5 [Skills](#65-skills)
   - 6.6 [MCP](#66-mcp)
   - 6.7 [Plugins](#67-plugins)
   - 6.8 [Multi-Agent](#68-multi-agent)
   - 6.9 [Memory](#69-memory)
   - 6.10 [Heartbeat / Cron](#610-heartbeat--cron)
   - 6.11 [Coding 模式](#611-coding-模式)
   - 6.12 [Workspace](#612-workspace)
   - 6.13 [Admin Console](#613-admin-console)
7. [非功能需求](#7-非功能需求)
8. [数据模型](#8-数据模型)
9. [部署与运维](#9-部署与运维)
10. [安全与合规](#10-安全与合规)
11. [国际化与无障碍](#11-国际化与无障碍)
12. [遥测与可观测性](#12-遥测与可观测性)
13. [里程碑与版本计划](#13-里程碑与版本计划)
14. [验收标准矩阵](#14-验收标准矩阵)
15. [风险与依赖](#15-风险与依赖)
16. [术语表](#16-术语表)

---

## 1. 文档信息

| 字段 | 值 |
| --- | --- |
| 产品 | **GE-paw**（gepaw 的 fork；本仓库使用 "GE-paw" 品牌） |
| 仓库 | `https://github.com/Zcx-BaixiaoBai/GE-paw` |
| 上游 | `https://github.com/agentscope-ai/gepaw`（Apache-2.0） |
| License | Apache-2.0 |
| Python | 3.10 – 3.13 |
| Node | 20 LTS |
| 文档版本 | v0.1.0（初稿） |
| 最后更新 | 2026-06-24 |
| 代管方 | Codex AI 代理（`docs/CUSTODIANSHIP.md`） |
| 关联文档 | `README.md`、`README_zh.md`、`CONTRIBUTING.md`、`SECURITY.md` |

### 修订历史

| 版本 | 日期 | 作者 | 说明 |
| --- | --- | --- | --- |
| v0.1.0 | 2026-06-24 | Codex 代管 | 初稿。对齐 README + Roadmap；为 v1.x 设定验收标准。 |

---

## 2. 背景与目标

### 2.1 为何要 fork

GE-paw 是一个个人 AI 助手平台，源自 `agentscope-ai/gepaw`（前身 CoPaw，2026-04-12 更名为 gepaw）的 fork。本仓库捆绑两条产品线：

1. **Assistant 模式** —— 长期运行的 `react_agent`，汇聚多渠道消息（IM + Web），由定时任务（cron）驱动，配套集中的 token 计量和审计。
2. **Q&A 模式** —— 团队知识库，数据源为 `md / pdf / docx / html`，通过 **LLM-wiki** 流水线（借用自 `SamurAIGPT/llm-wiki-agent`，MIT 协议）入库。**原始语料只存在于服务端，客户端永不下载源文件。**

### 2.2 目标

| 编号 | 目标 | 可衡量指标 |
| --- | --- | --- |
| G-1 | 统一的 Assistant runtime | 所有 IM + Web 渠道都路由到同一 `react_agent` 实例（按 workspace 划分）。 |
| G-2 | 可控的团队 Q&A | 每条 Q&A 回答必须引用本地索引中 ≥ 1 个 chunk。 |
| G-3 | Local-first | 用户语料、记忆、密钥默认存放在本机。 |
| G-4 | 无锁定扩展 | Skills / MCP / Plugin 支持运行时安装/卸载，无需重启。 |
| G-5 | 多租户管理 | Org admin 可不通过代码变更完成审计、限流、撤销。 |
| G-6 | 国际化 | 所有 UI 文案 i18n 就绪（zh-CN / en / ja / ru 基线）。 |
| G-7 | 零配置安装 | 新用户从 `pip install` 到首次对话 ≤ 5 分钟。 |

### 2.3 非目标（本 PRD 不涵盖）

- **不是**模型训练平台。GE-paw 消费上游 LLM，不做 fine-tune。
- **不是**多租户 SaaS。Org 级隔离已支持，跨租户联邦不在范围内。
- **不是**语音优先产品。语音输入已支持（Whisper），但语音合成不在 Roadmap。

---

## 3. 用户与场景

### 3.1 Personas

| 编号 | Persona | 描述 | 主要入口 |
| --- | --- | --- | --- |
| P-1 | 个人重度用户 | 在 macOS / Windows 本机跑 gepaw，使用 1-2 个 IM 渠道，需要对话 + 定时任务。 | Console（Web）+ DingTalk |
| P-2 | 团队负责人 | 在 Docker / 云 VM 上跑 gepaw，服务 5–20 人团队。需要 admin、审计、多 agent。 | Admin Console + DingTalk / Feishu |
| P-3 | 知识库管理员 | 维护团队 wiki（md / pdf / docx），关注入库进度，修复失败的解析。 | Admin Console → Wiki tab |
| P-4 | 开发者 / 贡献者 | 想新增渠道、Skill、MCP。阅读 CONTRIBUTING。 | GitHub + 本地开发环境 |
| P-5 | 企业合规官 | 审查安全、审计、数据驻留声明。 | `SECURITY.md` + 审计日志 |

### 3.2 关键场景

1. **S-1 快速对话。** 个人用户启动 gepaw，配置 DashScope API key，在 Web Console 对话，≤ 30 s 拿到有用回答。
2. **S-2 IM 中继。** 用户在 DingTalk 发"帮我整理今天的知乎热榜"。gepaw 以流式卡片回复到同一会话。
3. **S-3 定时摘要。** 用户设置每天 09:00 的 cron，把科技早报推送到 Feishu 群。
4. **S-4 团队 Q&A。** 新人问"我们组的报销流程是什么？"。gepaw 给出回答并引用 `wiki/finance/reimbursement.md`。
5. **S-5 Skill 安装。** Admin 在社区 Skill 上点"安装"，安全扫描通过，Skill 出现在用户的选单里。
6. **S-6 多 Agent 协作。** 两个 agent（`planner`、`critic`）协作起草 PR 描述。
7. **S-7 审计。** Admin 按用户过滤审计日志，查看最近 30 天的消息 + token 用量，导出 CSV。

---

## 4. 范围

### 4.1 In scope

- Web Console（React 18 + Vite）—— 三栏 Codex 风格布局
- Channels：DingTalk、Feishu、WeChat Work、Telegram、Discord、Tencent Yuanbao
- Backend：FastAPI + `react_agent` runner
- Skills、MCP、Plugins（workspace 内安装 + 扫描）
- 多 Agent 编排（mission-style loop + `prd.json`）
- Memory（长期 + 单 thread）
- Heartbeat / Cron
- Admin Console（12 个 tab：Audit / Channels / Crons / Gateway / LLM / MCP / Members / Plugins / Sessions / Skills / Tokens / Wiki）
- Q&A / LLM-wiki 入库（md / pdf / docx / html）
- Docker / pip / 脚本 / 桌面安装路径
- i18n：zh-CN（默认）/ en / ja / ru
- OAuth 2.1 MCP、Whisper 语音输入、动态上传上限

### 4.2 Out of scope

- 跨租户联邦
- 模型 fine-tune / RLHF 工具
- 语音合成（TTS）
- 原生移动端 App（仅 PWA）
- 服务端 GPU 供给 / 自动扩缩容（调用方负责）

---

## 5. 产品架构总览

```
┌────────────────────────────────────────────────────────────────┐
│                    Console（React 18 + Vite）                  │
│  ┌─────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │  Left Pane  │  │   Main Pane      │  │  Right Pane      │  │
│  │  Threads /  │  │  Assistant /     │  │  Files / Diff /  │  │
│  │  Sessions   │  │  Q&A / Settings  │  │  Preview / Plan  │  │
│  └─────────────┘  └──────────────────┘  └──────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                              │  HTTPS / JWT
┌─────────────────────────────▼──────────────────────────────────┐
│                  FastAPI Backend（gepaw / gepaw）              │
│  routers: assistant │ admin │ client │ gateway │ channels     │
│  ─────────────────────────────────────────────────────────     │
│  react_agent  ─►  tools（skills） ─►  llm_router ─► providers   │
│       │                                                            │
│       ├── heartbeat / cron  ──►  scheduler                            │
│       ├── mission loop     ──►  prd.json（Phase 1）                    │
│       └── ingest（Q&A）     ──►  wiki_index                             │
└────────────────────────────────────────────────────────────────┘
                              │  外部 API
┌─────────────────────────────▼──────────────────────────────────┐
│   Channels（IM）│ LLM Providers │ MCP │ Skills / Plugins store │
└────────────────────────────────────────────────────────────────┘
```

存储分层：

- **Working dir**（`gepaw_WORKING_DIR`）—— 运行时 DB、agent 状态、wiki 索引、skills。
- **Secret dir**（`gepaw_SECRET_DIR`）—— 加密的 API key、channel token。
- **Backup dir**（`gepaw_BACKUP_DIR`）—— 用于回滚的版本化归档。

---

## 6. 功能需求

每小节统一模板：

> **FR-X.Y 标题**
> *用户故事* → *行为* → *验收标准* → *边界情况* → *Out of scope*

### 6.1 Assistant 模式

**FR-6.1.1 新建 thread**
- *故事：* 作为 P-1，我打开 Console 开启新会话。
- *行为：* 点击 "+" → 左侧出现新 thread id；输入框获得焦点；前一个 thread 暂停但保留。
- *验收：*
  - `POST /api/threads` 返回 201 并携带 `thread_id`。
  - 点击后输入框在 200 ms 内获得焦点。
  - 历史 thread 仍按最后访问时间排序展示。
- *边界：* localStorage 被清空 → 优雅回退到服务端列表。
- *Out of scope：* thread 归档 / 自动合并。

**FR-6.1.2 发送消息**
- *故事：* 作为 P-1，我输入 prompt 后按 Enter。
- *行为：* 用户输入入队，发送至 `/api/threads/{id}/messages`，token 流式回到气泡；生成中途显示"中止"按钮。
- *验收：*
  - Enter 发送；Shift+Enter 换行。
  - 中止按钮可在 1 s 内取消正在进行的生成。
  - 失败请求显示"重试"按钮，复用同一草稿。
- *边界：* 网络中断 → 消息标记为 `failed`，草稿保留；重连后自动重试一次。

**FR-6.1.3 Slash 命令**
- *故事：* 作为 P-1，我输入 `/` 查看可用命令。
- *行为：* 下拉显示 `clear`、`compact`、`model`、`perm`、`skill …`、`cron …`。
- *验收：*
  - `/compact` 触发上下文压缩。
  - `/model llama3` 切换当前 thread 的激活模型。
  - 未知 slash 命令按纯文本渲染。

**FR-6.1.4 Reasoning 选择器**
- *故事：* 作为 P-1，我在发送前选择"low / medium / high"推理力度。
- *行为：* 输入框内嵌下拉；按 thread 持久化。
- *验收：*
  - 选择作为 `reasoning_effort` 发到后端。
  - 后端映射到模型支持的力度等级；不支持的等级以 400 拒绝。

**FR-6.1.5 Permission 选择器**
- *故事：* 作为 P-1，我限定 agent 可触及的范围。
- *行为：* 下拉：`read-only`、`workspace`、`system`（每次首次使用需弹确认）。
- *验收：*
  - 工具调用超出授予范围时弹出 inline approval（见 FR-6.13.7）。

**FR-6.1.6 Inline approval**
- *故事：* 作为 P-1，agent 想写文件时我 inline 批准 / 拒绝。
- *行为：* 审批卡滑入到消息气泡之上；用户点 ✓ / ✗。
- *验收：*
  - 点击后卡片消失；agent 收到 `approve` / `deny` 回调。
  - 超时（默认 60 s）自动拒绝，并显示"已拒绝"徽标。

**FR-6.1.7 Tool-call 卡片**
- *故事：* 作为 P-1，我看到 agent 调用了哪些 tool。
- *行为：* 卡片默认折叠，可展开查看参数 + 结果。
- *验收：* 点击 chevron 切换展开；参数/结果支持复制到剪贴板。

### 6.2 Q&A 模式（LLM-wiki）

**FR-6.2.1 Wiki 入库**
- *故事：* 作为 P-3，我把 gepaw 指向 `wiki/` 目录，启动入库。
- *行为：* 遍历目录，解析 md / pdf / docx / html，分块、embedding、入向量索引。
- *验收：*
  - Admin → Wiki tab 显示按文件的进度条。
  - 失败文件列入错误列表并说明原因；成功文件可重索引。
  - 幂等：重复入库为更新而非重复。

**FR-6.2.2 Q&A 查询**
- *故事：* 作为 P-2，我提问。
- *行为：* top-K chunks 召回，LLM 综合回答并附引用。
- *验收：*
  - 每条回答展示 ≥ 1 个 inline citation chip。
  - Citation 可点击；右侧面板打开源预览。
  - 相似度低于阈值时回退回答："未找到相关资料" + 推荐关键词。

**FR-6.2.3 源预览**
- *故事：* 作为 P-2，我点击 citation。
- *行为：* 右侧面板展示源文件的渲染内容（md → HTML，pdf → 文本 + 页码跳转）。
- *验收：*
  - 永远不暴露原始源文件；只展示渲染 / chunk 视图。
  - PDF 预览在 chunk 旁显示页码。

### 6.3 Console（Web UI）

**FR-6.3.1 三栏布局**
- *故事：* 作为 P-1，屏幕显示左 / 中 / 右三栏，可调尺寸、可折叠。
- *行为：* 拖拽手柄、折叠按钮；布局持久化到 `localStorage`。
- *验收：*
  - 在 1280×800 最小视口下三栏均可见（无横向滚动）。
  - 下次访问恢复布局状态。

**FR-6.3.2 主题**
- *故事：* 作为 P-1，我切换 dark / light / system。
- *行为：* 顶栏主题菜单；CSS 变量切换；过渡 ≤ 200 ms。
- *验收：* 页面加载不出现主题闪烁。

**FR-6.3.3 i18n 切换**
- *故事：* 作为 P-1，我切换界面语言。
- *行为：* Settings → Language；按用户持久化。
- *验收：* 所有可见文案来自 i18n bundle；缺失 key 回退为英文并打 warning。

**FR-6.3.4 Composer 状态**
- *行为：* empty / typing / filled / sending / error / sent。
- *验收：* 每个状态视觉清晰可辨；切换动画 ≤ 150 ms。

### 6.4 Channels

**FR-6.4.1 Channel 抽象**
- 每个 channel 实现 `send`、`receive`、`stream_chunk`、`reply_in_thread` 接口。
- 新增 channel = 新增模块 `src/gepaw/app/channels/<name>/` + router 注册。

**FR-6.4.2 已支持渠道（v1.x）**

| Channel | 状态 | 流式 | Thread reply | 说明 |
| --- | --- | --- | --- | --- |
| DingTalk | ✅ 稳定 | ✅ | ✅ | `streaming_enabled` 配置项 |
| Feishu | ✅ 稳定 | ✅ | ✅（自 v1.1.10）| |
| WeChat Work | ✅ 稳定 | ⚠️ 部分 | n/a | 文本 + 图片 |
| Telegram | ✅ 稳定 | ✅ | ✅ | |
| Discord | ✅ 稳定 | ✅ | ✅ | |
| Tencent Yuanbao | ✅（自 v1.1.10）| ✅ | ✅ | |

- *每渠道验收：*
  - 通过 `/api/channels/<name>/health` 检查健康。
  - 禁用 channel 后 ≤ 60 s 内停止入站投递。

**FR-6.4.3 Channel 配置**
- 存于 `secret_dir`；永不发给客户端。
- 每个 channel 暴露类型化的 config schema，服务端保存时校验。

### 6.5 Skills

**FR-6.5.1 内置 Skills**
- Scheduler（cron 表达式）
- PDF / Office 处理
- News digest
- Web search（Tavily）

**FR-6.5.2 自定义 Skill 安装**
- *故事：* 作为 P-2，我把 Skill 目录丢到 `skills/` 或粘贴 Git URL。
- *行为：* gepaw 校验 manifest，运行安全扫描（FR-10.2），加载。
- *验收：*
  - Skill 在 5 s 内出现在选单中。
  - 卸载后清理状态。
  - 热重载：Skill 代码变更无需重启即可生效。

**FR-6.5.3 Skill manifest schema**
- 必填字段：`name`、`version`、`entry`、`permissions[]`、`triggers[]`。
- 可选：`config`、`dependencies`、`homepage`。

### 6.6 MCP

**FR-6.6.1 OAuth 2.1 MCP**（自 v1.1.7）
- *故事：* 作为 P-2，我通过 OAuth 连接远程 MCP server。
- *行为：* Console 引导用户走 authorization-code 流程，refresh token 存于 `secret_dir`。
- *验收：* token 自动刷新；刷新失败时显示重新授权横幅。

**FR-6.6.2 本地 MCP stdio**
- 标准 `mcp.json` schema；每个 server 一个子进程。

**FR-6.6.3 MCP 健康检查**
- `/api/mcp/<id>/health` 返回 OK / degraded / down 及最后检查时间。

### 6.7 Plugins

**FR-6.7.1 Plugin 分发**
- 官方：`plugins/` 仓库 bundle；第三方：通过 URL 或本地文件安装。
- *验收：* Plugin manifest 必须声明 API version 兼容性。

**FR-6.7.2 Plugin 更新**
- 稳定检查（每 24 h）扫 plugin registry。
- 更新需 admin 确认后才能应用。

### 6.8 Multi-Agent

**FR-6.8.1 每 workspace 多 agent**
- *故事：* 作为 P-2，我创建 `planner` 和 `critic` 两个 agent。
- *行为：* 每个 agent 拥有自己的 system prompt、model、skills；用户选择激活哪一个。
- *验收：* 切换 agent 保留 thread 历史。

**FR-6.8.2 Mission loop**
- *故事：* 作为 P-2，我派发多步任务。
- *行为：*
  1. **Phase 1（分解）：** master agent 生成 `prd.json`（`stories[]`）。
  2. **Phase 2（执行）：** worker 领取 `passes=false` 的 story，执行后标记 `passes=true`。
  3. **Phase 3（审查）：** reviewer agent 审计 `prd.json` 进度。
- *验收：*
  - Phase 2 启动前先校验 `prd.json` schema；失败则中止 loop。
  - 每条 story 的 `acceptanceCriteria` 由显式 test 强制（如有提供）。
  - Loop 在崩溃后可恢复。

**FR-6.8.3 Subagent spawn**
- `spawn_subagent` 工具（自 v1.1.10），用于 workspace 内临时的子 agent 执行。
- 生命周期：spawn → run → 返回结果 → 终止。

**FR-6.8.4 Group chat**（计划中，v1.x）
- 一个 thread 内可见多个 agent；每条用户消息广播给全部 agent。

### 6.9 Memory

**FR-6.9.1 长期记忆**
- *故事：* 作为 P-1，agent 在跨会话间记住我的偏好。
- *行为：* 每轮用户对话摘要为一条 memory 记录；召回走语义检索。
- *验收：*
  - 用户可在 Settings 浏览 / 删除 memory 条目。
  - Memory 可导出为 JSON。

**FR-6.9.2 单 thread 记忆**
- 仅作用于单个 thread；thread 删除时一并清空。

**FR-6.9.3 记忆演进与主动反馈**
- Agent 在每次会话后反思；每周汇总学习到的偏好给用户。

### 6.10 Heartbeat / Cron

**FR-6.10.1 Cron 调度**
- 基于 UTC；crontab 语法；Admin → Crons 提供日历视图（自 v1.1.7）。
- *验收：* 日历高亮显示运行、失败、跳过的实例。

**FR-6.10.2 Heartbeat**
- 周期性自检（默认 30 min），汇总新事件；投递至用户指定的 channel。

### 6.11 Coding 模式

**FR-6.11.1 三面板 Web IDE**（自 v1.1.9）
- 左：文件树；中：编辑器（Monaco）；右：针对选中代码的对话。

**FR-6.11.2 LSP 集成**
- Python（pyright）开箱即用；TS 走 `tsserver`。

**FR-6.11.3 Workspace 版本化**
- 在破坏性工具调用前快照；一键回滚。

**FR-6.11.4 Runtime**
- 在用户环境中执行代码的沙箱。

**FR-6.11.5 Open Directory tab**（自 v1.1.10）
- 引用本地项目，无需 copy 到 workspace。

### 6.12 Workspace

**FR-6.12.1 子目录布局**（计划中）
- 自动建议拆分：`config/`、`production/`、`scratch/`。

**FR-6.12.2 文件访问守卫**
- 默认拒绝 working_dir 之外；系统路径（如 `~/.gepaw/`）需显式 allowlist。

**FR-6.12.3 Sandbox 集成**（进行中）
- 对风险工具，在 sandbox（Docker 或 nsjail）中运行；日志汇入 Admin → Audit。

### 6.13 Admin Console

Admin Console 暴露 12 个 tab（本 fork 当前状态）：

| Tab | 用途 | 关键端点 |
| --- | --- | --- |
| Audit | 检索 & 导出审计日志 | `/api/admin/audit` |
| Channels | Channel 启停 + 单 channel 配置 | `/api/admin/channels/*` |
| Crons | Cron 列表 / 日历 | `/api/admin/crons/*` |
| Gateway | Provider 路由规则 | `/api/admin/gateway/*` |
| LLM | 模型供应商、key 管理、连通性测试 | `/api/admin/llm/*` |
| MCP | MCP server 列表 + 健康检查 | `/api/admin/mcp/*` |
| Members | Org 成员 / 角色 | `/api/admin/members/*` |
| Plugins | Plugin 注册表 | `/api/admin/plugins/*` |
| Sessions | 活跃 session | `/api/admin/sessions/*` |
| Skills | Skill 注册表 | `/api/admin/skills/*` |
| Tokens | Token 用量（按用户 / 按日 / 按模型） | `/api/admin/tokens/*` |
| Wiki | 入库进度 + 失败列表 | `/api/admin/wiki/*` |

**FR-6.13.1 Admin 认证**
- 基于角色：`admin`、`operator`、`viewer`。
- `admin` 角色强制 2FA。

**FR-6.13.2 审计日志保留**
- 默认 90 天；可配置上限 1 年。

**FR-6.13.3 Token 用量视图**
- 日 / 周 / 月 分布；CSV 导出；按模型成本核算。

**FR-6.13.4 成员管理**
- 邮件邀请；分配角色；撤销。

**FR-6.13.5 Channels 管理**
- 启停 channel；轮换 webhook token；查看 last-error。

**FR-6.13.6 Cron 管理**
- 创建 / 暂停 / 删除 cron；查看最近 100 次执行。

**FR-6.13.7 权限 / 范围提升**
- 任何改变用户可见行为的 admin 操作都需要填写理由。

---

## 7. 非功能需求

### 7.1 性能

| 指标 | 目标 |
| --- | --- |
| 首 token（冷缓存） | ≤ 3 s p50，≤ 6 s p95 |
| 首 token（热缓存） | ≤ 1.5 s p50，≤ 3 s p95 |
| Console TTI（4G） | ≤ 2.5 s |
| Wiki 入库吞吐 | ≥ 5 MB/s（NVMe） |
| 单 agent 并发活跃 thread | ≥ 32 |

### 7.2 可靠性

- 进程崩溃后 ≤ 10 s 自动重启（systemd / Docker restart policy）。
- 每 6 h 产生一份 backup archive；保留最近 7 份。
- RPO ≤ 6 h；RTO ≤ 30 min。

### 7.3 可扩展性

- 单机基线：50 并发用户，500 thread / 天。
- 横向扩展路径：FastAPI 无状态部署在 LB 后；WebSocket 用 sticky session。

### 7.4 可维护性

- Lint：Python 走 black + ruff；TS 走 eslint + prettier。
- 类型检查：`src/gepaw/` 走 mypy strict；`web/` 走 `tsc --noEmit`。
- 测试金字塔：≥ 60 % 单元，20 % 集成，20 % E2E。

### 7.5 可移植性

- Linux x86_64 / arm64、macOS x86_64 / arm64、Windows 10+。
- Python 3.10 – 3.13；Node 20 LTS。

---

## 8. 数据模型

（仅列出核心实体；完整 schema 见 `src/gepaw/models/`。）

### 8.1 核心实体

- `User` —— id、email、role、locale、created_at、last_seen_at。
- `Thread` —— id、user_id、title、model、created_at、updated_at、archived_at。
- `Message` —— id、thread_id、role（`user` / `assistant` / `tool`）、content、tool_calls、token_usage、created_at。
- `Skill` —— id、name、version、manifest_json、enabled、permissions、installed_at。
- `MCPServer` —— id、name、transport、config（加密）、health_status。
- `Channel` —— id、type、config（加密）、enabled、last_health_at。
- `Cron` —— id、name、schedule、action、last_run_at、last_status。
- `WikiSource` —— id、path、sha256、last_indexed_at、status。
- `WikiChunk` —— id、source_id、ordinal、content、embedding、metadata。
- `AuditEvent` —— id、actor_id、action、target、payload_json、created_at。
- `PRD` —— mission-loop id、loop_dir、current_phase、prd_json_path。

### 8.2 保留策略

| 实体 | 默认 | 可配置 |
| --- | --- | --- |
| `Message` | 无限 | 365 天后归档 |
| `AuditEvent` | 90 天 | 上限 365 天 |
| `WikiSource` chunks | 文件存在期间 | 手动清理 |
| 遥测 | 90 天 | 否 |

---

## 9. 部署与运维

### 9.1 安装路径（面向用户）

- `pip install gepaw`（PyPI）
- 一行脚本（macOS / Linux / Windows）
- Docker（Docker Hub + Alibaba ACR）
- 阿里云 ECS 一键部署
- ModelScope Studio（云端托管）
- 桌面 App（Tauri，Windows / macOS）—— beta

### 9.2 本地存储布局

```
~/.gepaw/
├── bin/                 # CLI 入口
├── working/             # gepaw_WORKING_DIR
│   ├── agents/<id>/
│   ├── skills/
│   ├── mcp/
│   ├── wiki/
│   └── gepaw.db
├── working.secret/      # gepaw_SECRET_DIR（静态加密）
└── working.backups/     # gepaw_BACKUP_DIR
```

### 9.3 配置

- 环境变量以 `gepaw_` 为前缀（如 `gepaw_WORKING_DIR`）。
- `.env` 文件位于 working dir；密钥永不提交（`.gitignore` 已覆盖）。
- `gepaw init` 生成 `.env.example`。

### 9.4 备份与恢复

- 每 6 h 自动归档。
- 恢复命令：`gepaw restore <archive>`。

### 9.5 升级

- patch + minor 版本支持原地升级。
- major 升级需重新构建前端（`console/dist`）。

---

## 10. 安全与合规

### 10.1 威胁建模（摘要）

| 威胁 | 缓解 |
| --- | --- |
| 通过 Skills / 文档的 Prompt injection | Skill 安全扫描；tool 调用沙箱化 |
| 向第三方数据外泄 | Local-first 默认；显式 channel 路由 |
| Token 泄漏 | 密钥存于 `secret_dir`，环境变量永不记录日志 |
| 通过 admin 操作的权限提升 | 角色分离；需填写理由 |
| 供应链（Skill / Plugin） | Manifest 签名（计划中） |

### 10.2 Skill 安全扫描

安装时扫描以下项：

- Prompt injection 模式
- Command injection sink
- 硬编码 API key / token
- 数据外泄企图（向未 allowlist 的 host 发起的出站 HTTP）
- 在 working dir 之外的文件系统写

扫描失败则阻止安装并显示原因。

### 10.3 Web 认证

- 可选；`gepaw_AUTH_ENABLED=true` 启用。
- 基于 JWT；refresh token 存于 `secret_dir`。

### 10.4 合规姿态

- Apache-2.0 license。
- 遥测为 opt-in、匿名、按版本一次性。
- 不收集个人数据、文件、凭据。

### 10.5 漏洞报告

按 `SECURITY.md` —— Alibaba Security Response Center（ASRC）。

---

## 11. 国际化与无障碍

### 11.1 语言

基线：`zh-CN`（默认）、`en`、`ja`、`ru`。新增可见文案的 PR 必须同步更新四个 bundle。

### 11.2 无障碍

- WCAG 2.1 AA 目标。
- 所有交互元素支持键盘导航。
- 正文文字 color contrast ≥ 4.5:1。
- 焦点环可见；仅图标的按钮带 `aria-label`。

---

## 12. 遥测与可观测性

### 12.1 匿名遥测（opt-in）

在 `gepaw init` 时按版本一次性收集：

- gepaw 版本、安装方式、OS、Python 版本、CPU 架构、GPU 可用性。

**不收集：** 个人数据、文件、凭据、IP。

### 12.2 服务端指标

- 按用户 / 按 thread 的 token 用量（token 表）
- 按模型的 p50 / p95 延迟
- tool-call 成功率
- channel 投递成功率

### 12.3 日志

- 结构化 JSON 日志输出到 `working/logs/`。
- 轮转：按天，保留 14 天。
- 日志级别按模块可配。

---

## 13. 里程碑与版本计划

| 里程碑 | 目标日期 | 范围 |
| --- | --- | --- |
| **v1.1.11**（本 fork 下一 patch） | 2026-Q3 | Subagent visualization（部分）、token-by-day 图表打磨、gateway i18n 补齐 |
| **v1.2.0** | 2026-Q3 | Admin OAuth、Response API、Subagent visualization |
| **v1.3.0** | 2026-Q4 | Workspace 子目录布局、文件访问 sandbox v1 |
| **v1.4.0** | 2027-Q1 | Group chat、用户可选的上下文压缩 |
| **v1.5.0** | 2027-Q2 | gepaw Creator GA、gepaw Insight GA |

状态图例：

- **In Progress** —— 正在开发
- **Planned** —— 排期或设计中
- **Seeking Contributors** —— 欢迎社区贡献

---

## 14. 验收标准矩阵

一项改动要可合并，需勾选所有相关行。

### 14.1 代码质量

- [ ] `pytest -q` 本地通过（涉及模块 ≥ 95 % 有测试覆盖）。
- [ ] `ruff check src/` 干净。
- [ ] `mypy src/gepaw` 对新增 / 修改文件无错误。
- [ ] `cd web && npm run build` 成功。
- [ ] `cd web && npm run lint` 对修改文件无错误。

### 14.2 功能

- [ ] 新增 / 修改的可见文案同步到四个 i18n bundle。
- [ ] 新 API 端点有 OpenAPI docstring + ≥ 1 条 happy-path test。
- [ ] 新 tool call 需要 permission scope；默认拒绝。
- [ ] 新 Skill 安装会触发安全扫描。

### 14.3 安全

- [ ] 代码、日志中无密钥字符串。
- [ ] 无未经 allowlist 的新出站 HTTP。
- [ ] 受保护端点校验 JWT + 角色。

### 14.4 运维

- [ ] 向后兼容的 DB migration。
- [ ] 仍能产出备份；在副本上验证恢复。
- [ ] 若范围或验收标准变化，同步更新 `docs/PRD.md`。

### 14.5 文档

- [ ] `CHANGELOG` 在 unreleased 段落有新增条目。
- [ ] 用户可见的变更同步更新 README / docs。
- [ ] 若涉及弃用：发布弃用说明 + 1 个版本的过渡期。

---

## 15. 风险与依赖

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| 上游 gepaw 漂移 | 功能差距 / 合并冲突 | 每周跟踪上游；制定 rebase 计划 |
| LLM provider API 变更 | 对话失效 | Provider adapter 隔离；集成测试 mock provider |
| Skill 供应链 | 在用户环境执行代码 | 扫描 + sandbox |
| Token 成本失控 | Org 预算超支 | Token 表 + 按 org 上限（计划中） |
| Wiki 解析边缘情况 | 入库失败 | 按格式的回归测试；手动 override 路径 |

外部依赖：DashScope / OpenAI / Anthropic API，DingTalk / Feishu / Telegram / Discord SDK，MCP 参考实现。

---

## 16. 术语表

| 术语 | 定义 |
| --- | --- |
| **Agent** | 由 system prompt、model、skills、tools 组成的运行时配置。 |
| **Channel** | 一个 IM 集成（DingTalk、Feishu 等）。 |
| **Cron** | 一个定时任务。 |
| **Heartbeat** | Agent 的周期性自检。 |
| **LLM-wiki** | `SamurAIGPT/llm-wiki-agent` 的 Q&A 流水线。 |
| **Mission loop** | 使用 `prd.json` 的多 agent 任务执行器。 |
| **MCP** | Model Context Protocol。 |
| **Permission scope** | Agent 允许触及的范围（`read-only` / `workspace` / `system`）。 |
| **PRD（mission）** | 单 loop 的任务清单，**不是**本文档。 |
| **Skill** | 注册到 Agent 的可复用能力。 |
| **Thread** | 一段对话。 |
| **Working dir** | `gepaw_WORKING_DIR`，agent 状态的磁盘家目录。 |

---

## 附录 A —— 验收流程

每个进行中的 feature，代管方开 Draft PR 并勾选 §14 中相关条目。所有条目勾完后，PR 取消 draft 状态合入 `main`。

## 附录 B —— 本 PRD 变更日志

- v0.1.0（2026-06-24）—— 初稿；对齐 README + Roadmap。
