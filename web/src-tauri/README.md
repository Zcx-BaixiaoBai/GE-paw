# GE-paw 桌面壳 (Tauri 2.x)

> 本目录是 GE-paw 控制台的可选桌面壳。它把 `web/dist`（Vite 产物）打包为单文件应用，
> 并以 **sidecar** 模式启动 `gepaw serve`，由 WebView 2 / WKWebView / WebKitGTK 渲染前端。

## 目录结构

```
web/src-tauri/
├── Cargo.toml          # Rust 依赖与 profile
├── tauri.conf.json     # 窗口 / bundle / sidecar 配置
├── build.rs            # tauri_build 入口
├── capabilities/       # Tauri 2.x 权限（默认允许窗口/事件/资源）
│   └── default.json
├── icons/              # 平台图标（默认提供 32x32 占位）
│   └── icon.png
├── binaries/           # sidecar 二进制（Tauri 按目标三元组自动选择）
│   └── README.md
├── src/
│   └── main.rs         # 启动 sidecar → 等端口 → 启 WebView
└── README.md
```

## 构建前置

- Rust 1.77+ 与 `cargo`
- 平台依赖：
  - Windows：WebView2 Runtime（Win11 自带；Win10 需手动安装）
  - macOS：Xcode Command Line Tools
  - Linux：`webkit2gtk-4.1-dev`、`libssl-dev`、`libayatana-appindicator3-dev`
- Node 20+、pnpm（与 `web/` 共用）
- 已有 `gepaw.exe` 编译产物：`.venv/Scripts/gepaw.exe`（开发期直接复用）

## 构建步骤

```bash
# 1) 前端构建产物
cd web
pnpm install
pnpm build                 # 产物写入 web/dist/

# 2) 把 gepaw 复制为 sidecar（Windows 示例）
mkdir -p src-tauri/binaries
cp ../.venv/Scripts/gepaw.exe src-tauri/binaries/gepaw-x86_64-pc-windows-msvc.exe

# Linux:
# cp /path/to/gepaw src-tauri/binaries/gepaw-x86_64-unknown-linux-gnu
# macOS Intel:
# cp /path/to/gepaw src-tauri/binaries/gepaw-x86_64-apple-darwin
# macOS Apple Silicon:
# cp /path/to/gepaw src-tauri/binaries/gepaw-aarch64-apple-darwin

# 3) 装 Tauri CLI 并打包
cargo install tauri-cli --version "^2.0" --locked
cd src-tauri
cargo tauri build           # 发布构建
# 或开发模式：cargo tauri dev
```

## 客户端零落盘（Wiki 路径）

Web Tab 在问答模式下默认通过 `GET /api/client/wiki/preview` 渲染服务端清洗过的 HTML。
为避免 WebView 把任何 wiki 字节落盘，本壳采用三重保险：

1. **后端中间件**：`WikiNoStoreMiddleware` 给 `/api/client/wiki/*` 注入
   `Cache-Control: no-store`，浏览器/ WebView 不会写磁盘缓存。
2. **前端 `queryClient`**：对 wiki 路径显式 `fetch(noStore: true)`。
3. **WebView 启动清理**：`main.rs::clear_webview_data` 在窗口建立后提示
   前端 `caches.keys()` 阶段清掉所有 cache，并把缓存目录打印到 stderr 便于排查。

WebView2 默认数据目录：`%LOCALAPPDATA%\ai.gepaw.desktop\EBWebView\`。
WKWebView 沙箱目录：`(sandbox container)/Library/Caches/ai.gepaw.desktop/`。

## 配置项

`tauri.conf.json` 中可调：

- `app.windows[0].width/height`：默认 1280×800，最小 960×600。
- `app.security.csp`：默认拒绝跨源脚本；前端 fetch 只允许 `self` + `ipc`。
- `bundle.targets`：默认 `all`（按当前平台生成 dmg/nsis/deb/AppImage）。
- `bundle.externalBin`：声明 `gepaw` 为 sidecar；Tauri 2 会按目标三元组补全文件名后缀。

## 已知限制

- v1 不做多语言安装器（NSIS 仅基础包，不含 i18n）；管理员手册见根目录 `README_zh.md`。
- 第一次运行需要 5–10s 等待 sidecar 端口就绪；`READY_TIMEOUT = 30s`。
- macOS GateKeeper：未签名 dev build 需 `xattr -d com.apple.quarantine` 后才能打开。
