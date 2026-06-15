# Computer Use Plugin

Codex 风格的"计算机使用"插件。安装后：

1. 在左侧底部栏会出现"计算机使用"按钮，点击打开全屏浮层。
2. 浮层可以建立连接、显示截图流、回放代理的点击/键入/按键动作。
3. 同时注册四个 agent 工具：`computer_screenshot` / `computer_click` / `computer_type` / `computer_key`，代理可在获得权限后调用。

## 配置

桌面端（推荐）：

```bash
pnpm tauri dev
```

桌面端通过 Tauri 的 `__TAURI_INTERNALS__` 桥接实际截屏与输入事件，工具真正生效。

浏览器端：

```bash
pnpm dev
```

浏览器端插件仍能加载并出现在 UI 中；点击事件会返回 `input_bridge_unavailable`，UI 会显示友好的提示与占位截图，方便演示与无头环境验证。

## 安全

- 任何工具调用都需要会话处于"全量 / 智能"权限模式，且要求用户先在浮层里"连接"。
- 在"严格 / 只读"权限模式下，代理将被拒绝使用计算机使用工具。
