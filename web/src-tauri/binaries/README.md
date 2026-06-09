# sidecar 二进制

Tauri 2 会按构建目标三元组查找 `gepaw-<triple>[.exe]`。

| 平台 | 文件名 |
| --- | --- |
| Windows x64 | `gepaw-x86_64-pc-windows-msvc.exe` |
| Linux x64   | `gepaw-x86_64-unknown-linux-gnu` |
| macOS Intel | `gepaw-x86_64-apple-darwin` |
| macOS ARM   | `gepaw-aarch64-apple-darwin` |

生成示例（Windows / PyInstaller 产物 `.venv/Scripts/gepaw.exe`）：

```bash
mkdir -p src-tauri/binaries
cp .venv/Scripts/gepaw.exe src-tauri/binaries/gepaw-x86_64-pc-windows-msvc.exe
```

`tauri build` 之前必须存在对应三元组的文件；`tauri dev` 在开发期会优先
从 `PATH` 或 `src-tauri/binaries/` 找到名为 `gepaw` 的可执行文件。
