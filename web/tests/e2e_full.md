# GE-paw E2E 测试报告（2026-06-13）

## 概览
- 目标：验证修复后的 GE-paw 控制台是否可正常启动、路由、登录并访问主要页面。
- 当前状态：页面与样式已修正，Admin 路由与 LLM 配置页已补齐，Vite 开发服务器处于持续启动中（因端口占用冲突，需要保持单一实例运行）。

## 已完成的修复
- `web/src/App.tsx`：恢复完整路由结构，包含 Login、Assistant/QnA、Settings、Admin 子路由。
- `web/src/pages/Admin/LLM.tsx`：补齐导出名称（`AdminLLMPage / LLMConfigPage` 双导出），并引入 `qwenpaw` 式左栏供应商导航 + 右侧配置面板的布局。
- `web/src/styles/global.css`：追加 Admin 布局、LLM 配置页、按钮、Toast、Modal 等样式，统一使用 Codex 深色主题变量。
- 临时索引页 `web/index.debug.html`：已移除，避免干扰 Vite 根路由。

## 端到端覆盖范围（计划）
1. 登录流程：访问 `/login`、提交用户名密码、登录成功跳转。
2. Assistant 页面：会话创建、发送消息、Mock 回复渲染。
3. Admin 页面导航：侧边栏切换 LLM / Members / Channels 等。
4. LLM 配置页：预置供应商列表、API Key 输入、保存/测试/删除交互。
5. Settings 页面：主题切换、语言切换等。
6. 右侧面板：Plan/Goals/RightPane 展开收起。

## 当前阻塞点
- Vite 开发服务器会在 5173 端口被占用时启动失败；当前已有实例保持运行，但 Playwright 测试需要稳定端口。
- Node REPL 未预装 `playwright`，需要在 web 项目或系统环境中安装后才能进行自动化截图/交互。

## 后续行动
1. 保持 Vite 在 `5173` 单实例运行（若端口被占需先释放）。
2. 在 web 项目 `npm i -D playwright @playwright/test` 或使用系统 Python `playwright` 进行自动化。
3. 运行脚本逐页面打开、截图、断言关键元素，补充本报告的执行结果。
4. 使用 Codex 参考截图对比字体、间距、按钮圆角、图标样式，迭代 UI 细节。
5. 汇总 Linear 待办（当前 MCP `linear` 未配置，需要提供可用插件后再补充）。

## 附录：关键文件
- `C:/Users/Admin/Documents/GE-paw/web/src/App.tsx`
- `C:/Users/Admin/Documents/GE-paw/web/src/pages/Admin/LLM.tsx`
- `C:/Users/Admin/Documents/GE-paw/web/src/layouts/AppLayout.tsx`
- `C:/Users/Admin/Documents/GE-paw/web/src/styles/global.css`
- `C:/Users/Admin/Documents/GE-paw/web/vite.config.ts`