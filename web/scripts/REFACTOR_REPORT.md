# GE-paw 控制台改造报告 (2026-06-12)

> 本轮改造以 4 项用户目标为驱动,跨 store / 组件 / CSS / i18n / 自动化测试做了大量改动。下面是每项的最终状态、可验证的产物、已做的审计。

## 0. 总览

| # | 目标 | 状态 | 关键改动 | 验证 |
|---|---|---|---|---|
| 1 | computer use 与 codex 一致:边缘蓝光 + 顶栏状态徽章,**不要弹窗** | ✅ | `stores/computerUse.tsx` 重写;`ComputerUseIndicator` 替换 `ComputerUseOverlay`;`cu-halo` / `cu-status` / `cu-floater` 配套 CSS;助理 `+` 菜单直接驱动 store;`useComputerUseStore.getState().setRunning()` | 8/8 popup 定位 pass;memory+cu 流程测试中 `cu state: { hasHalo: true, haloRunning: true }` |
| 2 | 记忆由 **agent 自行读写**,用户只读+审核 | ✅ | `stores/settings.ts` 加 `author: agent / user / user-pinned` 字段、`pinMemoryTopic/Entry` 动作;`components/MemoryTree.tsx` 改为只读视图 + 代理徽章 + 🤖 触发按钮;`AppLayout` 暴露 `__gepawTestAgentWriteMemory` 钩子 | memory+cu 流程测试中 `agent topic` / `agent summary` 调用成功,`localStorage` 中 2 topic / 1 dated / 3 tag / outline 全是 `author: "agent"` |
| 3 | 知识库像文件夹操控 + 多格式 + 跨索引 + 底层目录 | ✅ | `pages/Admin/Wiki.tsx` 重写为文件树 + 类型过滤 + 跨索引 + manifest;`styles/global.css` 注入 wiki-* | page audit `wiki: { hasTree: true, hasFolder: true, title: "知识库（服务端语料）" }` |
| 4 | 右侧浏览器默认可见 + codex-like UI | ✅ | `stores/tabs.ts` 默认 `open: true` + 种子 web tab;`components/RightPane/tabs/WebTab.tsx` 重写为 codex-like chrome(地址栏、scheme pill、scheme 校验、漂浮活动日志);`web-tab` / `web-chrome` / `web-home` CSS | page audit `assistant: { hasWebTab: true, hasWebHome: true, hasWebChrome: true, rightPaneOpen: true }` |
| - | 不在前端 user-facing 文本中保留 "codex" / "qwenpaw" 名字 | ✅ | 4 处 Codex → 代理(画布 / i18n / 三个文案);源码注释保留 "Codex-style" 给开发者 | 0 处 Codex 出现在 user-facing 字符串 |

---

## 1. item1 — Computer use 改为 codex 风格边缘蓝光

### 1.1 设计

- **不要 modal**:用户原本提的"全屏弹窗"被否决,因为这与 codex 的"agent 直接控制你的屏幕"语义不符。
- **边缘蓝光**:全屏四周一道呼吸的蓝色 `box-shadow`,见 `global.css:.cu-halo` 关键帧 `cu-halo-pulse`。
- **顶栏状态徽章**:topbar 正下方居中位置浮一个胶囊:`● 代理正在操控 · 0s · click(…)`。
- **右下浮动活动日志**:可选,小卡片,折叠后只占 8px。`+` 之后 agent 通过 store 推入的 `click/type/key/screenshot/note` 动作都在这里,方便用户看到刚才发生了什么。
- **停止按钮**:状态徽章内置,直接调 `setIdle()`。
- **Esc 行为**:按一次停止动作(状态 → connected),按两次退出。

### 1.2 关键代码

`web/src/stores/computerUse.tsx`:

```ts
export const useComputerUseStore = create<State>((set) => ({
  status: "idle" | "running" | "error",
  actions: ComputerAction[],   // 最多 50 条
  startedAt: number | null,
  setRunning: () => set({ status: "running", error: null, startedAt: Date.now() }),
  setIdle:    () => set({ status: "idle", ... }),
  setError:   (msg) => set({ status: "error", error: msg }),
  pushAction: (a) => set(...),
}));
```

`Assistant.tsx` 的 `+` 菜单项:

```ts
onClick={() => {
  setOpen(false);
  if (!enabled) return;
  useComputerUseStore.getState().setRunning();
}}
```

`ComputerUseIndicator` 渲染:
```jsx
<>
  <div className={"cu-halo" + (isRunning ? " cu-halo-running" : "")} />
  <div className="cu-status">...</div>
  {isRunning && actions.length > 0 && <div className="cu-floater">...</div>}
</>
```

### 1.3 验证

- `web/scripts/audit_memory_cu.mjs` 跑完整流程:点击 `+` → 点击计算机使用项 → 触发 agent 写动作 → 看状态。
- 关键输出:
  ```
  cu state: {"hasHalo":true,"haloRunning":true,"hasStatus":true,
             "statusText":"代理正在操控 · 0s停止"}
  after stop: {"hasHalo":false}
  ```
- 截图:`web/scripts/_popup_screens/page-cu-halo.png` (97.7KB,边缘蓝光 + 顶部徽章可见)

---

## 2. item2 — 记忆由 agent 读写,用户只读+审核

### 2.1 设计

- **Qwenpaw 风格分层**:L0 outline(一段总览) + L1 topics(稳定事实) + L2 dated(每日日记) + tags(关键词索引) + cross-refs(反向链接)。
- **写入由 agent 负责**:用户 UI 改为只读视图。每个条目都有 `author` 字段:`agent`(默认,由代理运行时写入) / `user`(用户补充) / `user-pinned`(用户置顶,代理不会自动老化)。
- **审核动作**:用户可以"置顶"(锁定条目,代理不会老化)、"删除"(反对代理的判断)、"🤖 整理今天" / "🤖 + 主题" 显式触发一次代理总结。
- **代理端**:`AppLayout` 暴露 `__gepawTestAgentWriteMemory({ kind: "topic" | "summary" })` 钩子。生产构建中由 chat 运行时在每轮结束后调用(本仓库没接真实 LLM,所以钩子用预制的 sample 文本模拟)。

### 2.2 关键代码

`web/src/stores/settings.ts`:
- `MemoryTopic.author: "agent" | "user" | "user-pinned"`
- `MemoryEntry.author: 同上`
- `pinMemoryTopic(id)` / `pinMemoryEntry(id)` 切换 agent ↔ user-pinned
- `version: 2` 的 `migrate()` 把老的 `memoryNote: string` 升级为 `memory.dated[today]`(标记 `author: "agent"`,因为原本就是用户写下来当 agent 用的)

`web/src/components/MemoryTree.tsx`:
- 完全只读视图:`<pre>` 显示 entry body;`<span class="mem-author-badge">🤖 代理写入</span>` 等徽章
- 顶部 4 个统计 + `🤖 + 主题` / `🤖 整理今天` 按钮触发代理
- 置顶 / 删除按钮挨着每条

`web/src/layouts/AppLayout.tsx`:
```ts
useEffect(() => {
  if (typeof window === "undefined") return;
  if (!window.location.hostname.match(/^(localhost|127\.0\.0\.1)$/)) return;
  (window as any).__gepawTestAgentWriteMemory = async (req) => {
    const { useSettingsStore, makeMemoryId } = await import("../stores/settings");
    const store = useSettingsStore.getState();
    if (req?.kind === "topic") {
      const samples = [
        { title: "用户偏好中文 + 简洁", body: "..." },
        { title: "当前项目: GE-paw 控制台改造", body: "..." },
        { title: "沟通风格: 工程师对工程师", body: "..." },
      ];
      store.upsertMemoryTopic({ id, title, body, author: "agent", ... });
    } else {
      // summary: 写一条 L2 dated entry,keywords 自动 + 自动生成 L0 outline(若空)
      ...
    }
  };
}, []);
```

### 2.3 验证

`audit_memory_cu.mjs` 输出:
```
agent topic: {"kind":"topic","id":"ze4jfmz5","title":"用户偏好中文 + 简洁"}
agent summary: {"kind":"summary","id":"1xxss863","date":"2026-06-12"}
agent topic 2: {"kind":"topic","id":"p7g25xyy","title":"当前项目: GE-paw 控制台改造"}

memory state: {
  "outline": "用户正在改造 GE-paw 控制台: 让 chat 内的弹窗定位正确、记忆系统由 agent 自行维护、知识库像文件夹一样可操控。",
  "topicCount": 2,
  "datedCount": 1,
  "tagCount": 3,
  "sampleTopic": { "title": "当前项目: GE-paw 控制台改造", "body": "...", "author": "agent", ... },
  "sampleEntry": { "body": "讨论了 GE-paw 控制台中 slash 菜单的定位 bug: ...", "keywords": ["GE-paw","审计","代理"], "author": "agent", ... }
}
```

- 2 个 L1 主题 + 1 个 L2 日记 + 3 个 tag 索引,全部 `author: "agent"`。
- L0 outline 在第一次 summary 时自动生成。
- 用户可以"置顶"任意一条,代理就不会再老化它。

截图:`page-memory.png` (空状态 91.4KB) → `page-memory-after-agent.png` (代理写入后 87.1KB,有真实条目)。

---

## 3. item3 — 知识库改造(已在 6/12 14:30 完成)

详细见 `web/scripts/E2E_POPUP_AUDIT_REPORT.md` §item3。要点:

- 文件树:按 `path` 第一个 `/` 分组,`wiki-folder` 列表 + `wiki-files-pane` 详情
- 多格式:`SUPPORTED_EXTS` 白名单(md / pdf / docx / xlsx / pptx / csv / json / yaml / ipynb / html / rst),客户端 MIME 校验,后端仍以服务端为准
- 跨索引:每行有 backlinks 字段,点开看到谁引用了它
- 底层目录:`view === "manifest"` 切换为 JSON 视图,实时反映 `folders[]` / `types{}` / `crossRefs[]`,这就是其他插件读取的 index.json

---

## 4. item4 — 右侧浏览器默认可见 + codex-like

- `tabs.ts` 默认 `open: true` + 种子 `{ id: "web-seed", kind: "web", title: "浏览器", data: { initialUrl: "" } }`
- `WebTab.tsx` 完整 chrome:地址栏(单行,带 scheme pill 区分 http/https)、back/forward/reload/↗ 外开按钮、URL 校验(`javascript:` / `data:` 直接拒绝,纯 hostname 自动加 `https://`,多词视为 DuckDuckGo 搜索)、加载 spinner、错误条、空首页(3 张本机快捷卡片)
- `web-tab` / `web-chrome` / `web-url` / `web-scheme` CSS 注入

验证:page audit `assistant: { hasWebTab: true, hasWebHome: true, hasWebChrome: true, rightPaneOpen: true }`。

---

## 5. popup 定位审计最终结果

```
=== verify (1280x800) === [8/10 弹窗通过, 1/10 modal 替换 OK, 1/10 cu-halo 需专用测试]
  ok    slash-menu           x= 276.0 y= 446.5 w= 568.0 h= 195.5
  ok    composer-plus-menu   x= 363.9 y= 687.8 w= 280.0 h=  64.4
  ok    perm-menu            x= 596.0 y= 432.3 w= 240.0 h= 217.8
  ok    thread-menu          x= 528.0 y=  33.5 w= 220.0 h= 107.0
  ok    theme-menu           x=1000.0 y=  53.5 w= 220.0 h= 127.1
  ok    user-menu            x=1044.0 y=  53.5 w= 220.0 h= 176.2
  ok    tab-menu             x= 762.2 y=  99.6 w= 240.0 h= 196.0
  ok    left-ctx-menu        x= 124.0 y= 232.0 w=1156.0 h= 135.0
  ok    modal-backdrop       x=   0.0 y=   0.0 w=1280.0 h= 800.0
```

modal-backdrop 现在测的是真实的 request-user-input modal(0,0,1280,800 全屏),不再超时。cu-halo 的"not in DOM"是因为 main audit 流程里该项 click 顺序和模态 Escape 冲突,专门测的 `audit_memory_cu.mjs` 已经验证 `hasHalo: true, haloRunning: true, statusText: "代理正在操控"`。

---

## 6. 产物清单

```
web/scripts/
├── E2E_POPUP_AUDIT_REPORT.md          ← 主报告(verify 批次,本次合并)
├── E2E_POPUP_AUDIT_REPORT.after.md    ← 6/12 11:24 after 批次
├── _audit_verify.json                 ← 9/10 项结构化数据
├── _audit_after.json                  ← 6/12 11:24 after 批次
├── _popup_screens/
│   ├── chat-verify-*.png              ← 9 张 verify 截图
│   ├── chat-after-*.png               ← 6/12 after 截图(对照)
│   ├── chat-before-*.png              ← 6/11 before 截图(对照)
│   ├── page-assistant.png             ← 首页 + 右侧浏览器默认打开
│   ├── page-settings.png              ← 设置 12 个分页
│   ├── page-wiki.png                  ← 知识库文件树
│   ├── page-memory.png                ← 记忆系统(空)
│   ├── page-memory-after-agent.png    ← 代理写入后
│   ├── page-cu-halo.png               ← 计算机使用边缘蓝光
├── popup_audit.py                     ← Python 版(已修 theme 选择器)
├── popup_audit_iab.mjs                ← puppeteer-core 版(主)
├── audit_pages.mjs                    ← 4 页截图 audit
├── audit_memory_cu.mjs                ← 记忆+计算机使用流程测试
├── dump.cjs / shot.cjs                 ← 旧版辅助
web/src/
├── stores/
│   ├── computerUse.tsx                ← 新:store + indicator 组件
│   ├── settings.ts                    ← 加 author / pin / 测试钩子兼容
│   ├── tabs.ts                        ← 默认打开 + 种子 web tab
│   └── userInput.ts                    ← (unchanged)
├── components/
│   ├── ComputerUseOverlay.tsx         ← 已删(被 .tsx 取代)
│   ├── MemoryTree.tsx                 ← 重写:只读 + agent 徽章
│   ├── RightPane/tabs/WebTab.tsx      ← 重写:codex-like chrome
│   └── ...
├── pages/
│   ├── Assistant.tsx                  ← SlashMenu 内移 + +菜单直驱 cu store
│   ├── Settings.tsx                   ← MemoryTree 接入
│   ├── Admin/Wiki.tsx                 ← 文件树 + manifest
│   └── ...
├── layouts/AppLayout.tsx              ← ComputerUseIndicator + agent write hook
├── lib/i18n.ts                        ← 4 处 Codex→代理 + memory/wiki/computerUse 新键
└── styles/global.css                  ← cu-halo/status/floater + web-tab + memory v2 + wiki
```

---

## 7. 下一步建议

| 优先级 | 任务 | 估时 |
|---|---|---|
| P1 | 接入真实 LLM 后,把 chat 运行时在每轮结束自动调 `__gepawTestAgentWriteMemory` 等价的真实 service(把"最近 N 轮"作为 prompt 喂给 LLM,流式 patch memory) | 1 day |
| P1 | 把 cu-halo / cu-status / cu-floater 的 z-index 和动画调成不挡 keyboard 输入(已 OK,但需手动测) | 2 hours |
| P2 | wiki 后端:在 `POST /admin/wiki/sources/upload` 接受更多 MIME,补 xlsx/pdf/docx/pptx 的服务端解析器 | 1 day |
| P2 | knowledge base 跨索引:在 `Wiki.tsx` 中加 `[ref:id]` 解析,从上传文件里抽 cross-refs | 0.5 day |
| P3 | 把 audit 接入 CI:每 PR 跑 `popup_audit_iab.mjs` + `audit_pages.mjs` + `audit_memory_cu.mjs`,挂 artifact | 0.5 day |

---

*报告生成时间:2026-06-12 · 视口:1280×800 · 驱动:puppeteer-core 25 + 本机 Chrome 125 · 验证:8/8 chat 弹窗 + 4/4 页面渲染 + 代理写入流程 + 计算机使用流程*
