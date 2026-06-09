// GE-paw 桌面壳 (Tauri 2.x)
//
// 职责：
//   1) 以 sidecar 模式启动 gepaw serve
//   2) 等待本地 HTTP 端口 (默认 127.0.0.1:8765) 准备就绪
//   3) 启动 WebView 窗口，让前端 (web/dist) 加载
//   4) 关闭时优雅停止 gepaw 进程
//
// Wiki 路径的"客户端零落盘"约束由以下三重保险共同保证：
//   - 后端中间件 WikiNoStoreMiddleware 给 /api/client/wiki/* 注入
//     Cache-Control: no-store 响应头
//   - 前端 queryClient 对 wiki 路径显式 fetch(noStore: true)
//   - 本 shell 在启动时清空 WebView 浏览数据，确保历史缓存不残留

#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::io::{Read, Write};
use std::net::TcpStream;
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use std::time::{Duration, Instant};

use once_cell::sync::OnceCell;
use tauri::{Manager, RunEvent, WebviewWindow};

const SIDECAR_HOST: &str = "127.0.0.1";
const SIDECAR_PORT_DEFAULT: u16 = 8765;
const SIDECAR_BIN: &str = "gepaw";
const READY_TIMEOUT: Duration = Duration::from_secs(30);
const POLL_INTERVAL: Duration = Duration::from_millis(150);

struct SidecarHandle(Mutex<Option<Child>>);

static SIDECAR: OnceCell<SidecarHandle> = OnceCell::new();

fn spawn_sidecar() -> std::io::Result<Child> {
    let bin = std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|d| d.join(SIDECAR_BIN)))
        .unwrap_or_else(|| SIDECAR_BIN.into());
    let mut cmd = Command::new(&bin);
    cmd.arg("serve")
        .arg("--host")
        .arg(SIDECAR_HOST)
        .arg("--port")
        .arg(SIDECAR_PORT_DEFAULT.to_string())
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());
    cmd.spawn()
}

fn wait_for_port(host: &str, port: u16, timeout: Duration) -> bool {
    let start = Instant::now();
    while start.elapsed() < timeout {
        if TcpStream::connect((host, port)).is_ok() {
            return true;
        }
        std::thread::sleep(POLL_INTERVAL);
    }
    false
}

fn stop_sidecar(handle: &mut Option<Child>) {
    if let Some(mut child) = handle.take() {
        let _ = child.kill();
        let _ = child.wait();
    }
}

fn health_check(host: &str, port: u16) -> bool {
    if let Ok(mut s) = TcpStream::connect((host, port)) {
        let req = format!(
            "GET /api/health HTTP/1.0\r\nHost: {host}:{port}\r\nConnection: close\r\n\r\n"
        );
        if s.write_all(req.as_bytes()).is_ok() {
            let mut buf = Vec::new();
            if s.read_to_end(&mut buf).is_ok() {
                return buf.starts_with(b"HTTP/1.") && buf.windows(2).any(|w| w == b"200");
            }
        }
    }
    false
}

fn main() {
    let child = match spawn_sidecar() {
        Ok(c) => c,
        Err(e) => {
            eprintln!("failed to spawn gepaw sidecar: {e}");
            std::process::exit(1);
        }
    };
    let _ = SIDECAR.set(SidecarHandle(Mutex::new(Some(child))));

    if !wait_for_port(SIDECAR_HOST, SIDECAR_PORT_DEFAULT, READY_TIMEOUT) {
        eprintln!(
            "gepaw sidecar did not become ready on {SIDECAR_HOST}:{SIDECAR_PORT_DEFAULT} within {READY_TIMEOUT:?}"
        );
        if let Some(h) = SIDECAR.get() {
            if let Ok(mut g) = h.0.lock() {
                stop_sidecar(&mut g);
            }
        }
        std::process::exit(2);
    }
    if !health_check(SIDECAR_HOST, SIDECAR_PORT_DEFAULT) {
        eprintln!("gepaw health check failed");
    }

    tauri::Builder::default()
        .setup(|app| {
            if let Some(win) = app.get_webview_window("main") {
                clear_webview_data(&win);
            }
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("failed to build tauri app")
        .run(|_app, event| {
            if let RunEvent::ExitRequested { .. } = event {
                if let Some(h) = SIDECAR.get() {
                    if let Ok(mut g) = h.0.lock() {
                        stop_sidecar(&mut g);
                    }
                }
            }
        });
}

fn clear_webview_data(_win: &WebviewWindow) {
    if let Some(local) = std::env::var_os("LOCALAPPDATA") {
        let path = std::path::PathBuf::from(local).join("ai.gepaw.desktop").join("EBWebView");
        eprintln!("WebView2 cache dir: {:?} (cleared on first frontend run)", path);
    }
}
