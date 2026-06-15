// Built-in browser tab. Renders a sandboxed iframe with a codex-style chrome:
// URL bar with scheme pill, back/forward/reload buttons, loading progress,
// external-open, and an empty home state with quick bookmarks.
//
// All URLs are sandboxed (`allow-scripts allow-same-origin allow-forms`).
// http:// is allowed but flagged with a small warning chip. javascript:/data:
// URLs are rejected outright to avoid XSS via the address bar.
import { useEffect, useRef, useState } from "react";
import { t } from "../../../lib/i18n";

type Props = { data?: { initialUrl?: string } };

const QUICK_LINKS: { label: string; url: string; hint: string }[] = [
  { label: "GE-paw 控制台", url: `${typeof window !== "undefined" ? window.location.origin : ""}/app/assistant`, hint: "回到本机控制台" },
  { label: "设置", url: `${typeof window !== "undefined" ? window.location.origin : ""}/app/settings`, hint: "LLM / 通道 / Skill 配置" },
  { label: "管理", url: `${typeof window !== "undefined" ? window.location.origin : ""}/app/settings?tab=members`, hint: "成员 / Token / 审计" },
];

function normalizeUrl(input: string): { ok: true; url: string } | { ok: false; reason: string } {
  const raw = (input || "").trim();
  if (!raw) return { ok: false, reason: "empty" };
  // Reject obviously dangerous schemes.
  const lower = raw.toLowerCase();
  if (/^(javascript|data|vbscript|file):/i.test(lower)) {
    return { ok: false, reason: "scheme-blocked" };
  }
  // If it already has a scheme, use as-is.
  if (/^[a-z][a-z0-9+.-]*:/i.test(raw)) {
    return { ok: true, url: raw };
  }
  // If it starts with //, treat as protocol-relative.
  if (raw.startsWith("//")) return { ok: true, url: "https:" + raw };
  // If it looks like a host, prepend https://.
  if (/^[\w-]+(\.[\w-]+)+/.test(raw) && !raw.includes(" ")) {
    return { ok: true, url: "https://" + raw };
  }
  // Single word: treat as a search via DuckDuckGo.
  if (!/\s/.test(raw)) {
    return { ok: true, url: "https://duckduckgo.com/?q=" + encodeURIComponent(raw) };
  }
  // Multi-word: search.
  return { ok: true, url: "https://duckduckgo.com/?q=" + encodeURIComponent(raw) };
}

function schemeOf(url: string): string {
  const m = url.match(/^([a-z][a-z0-9+.-]*):/i);
  return m ? m[1].toLowerCase() : "https";
}

export function WebTab({ data }: Props) {
  const seed = data?.initialUrl?.trim() || "";
  const [url, setUrl] = useState(seed);
  const [input, setInput] = useState(seed);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<string[]>(seed ? [seed] : []);
  const [hIdx, setHIdx] = useState(seed ? 0 : -1);
  const iframeRef = useRef<HTMLIFrameElement | null>(null);

  // If a parent route passes a new initialUrl after mount, navigate to it.
  useEffect(() => {
    if (data?.initialUrl && data.initialUrl !== url) {
      navigate(data.initialUrl);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data?.initialUrl]);

  function navigate(next: string) {
    const r = normalizeUrl(next);
    if (!r.ok) {
      if (r.reason === "scheme-blocked") setErr("该协议已被沙箱拒绝");
      else if (r.reason === "empty") setErr(null);
      return;
    }
    setErr(null);
    setUrl(r.url);
    setInput(r.url);
    // Truncate forward history.
    const trimmed = history.slice(0, hIdx + 1);
    const next2 = [...trimmed, r.url];
    setHistory(next2);
    setHIdx(next2.length - 1);
    setLoading(true);
  }

  function back() {
    if (hIdx <= 0) return;
    const newIdx = hIdx - 1;
    setHIdx(newIdx);
    const u = history[newIdx];
    setUrl(u);
    setInput(u);
    setLoading(true);
  }
  function forward() {
    if (hIdx >= history.length - 1) return;
    const newIdx = hIdx + 1;
    setHIdx(newIdx);
    const u = history[newIdx];
    setUrl(u);
    setInput(u);
    setLoading(true);
  }
  function reload() {
    if (!url) return;
    // Cache-bust the iframe src to force a reload.
    const u = url + (url.includes("#") ? "" : "#" + Date.now());
    setUrl(u);
    setLoading(true);
  }
  function openExternal() {
    if (!url) return;
    window.open(url, "_blank", "noopener,noreferrer");
  }

  const scheme = url ? schemeOf(url) : "";
  const insecure = url && scheme === "http";

  return (
    <div className="web-tab">
      <div className="web-chrome">
        <div className="web-chrome-row web-chrome-nav">
          <button
            type="button"
            className="web-nav-btn"
            onClick={back}
            disabled={hIdx <= 0}
            title="后退"
            aria-label="后退"
          >
            ‹
          </button>
          <button
            type="button"
            className="web-nav-btn"
            onClick={forward}
            disabled={hIdx >= history.length - 1}
            title="前进"
            aria-label="前进"
          >
            ›
          </button>
          <button type="button" className="web-nav-btn" onClick={reload} disabled={!url} title="刷新" aria-label="刷新">
            ↻
          </button>
        </div>
        <form
          className="web-chrome-row web-chrome-addr"
          onSubmit={(e) => {
            e.preventDefault();
            navigate(input);
          }}
        >
          <span className={"web-scheme" + (insecure ? " warn" : "")}>{scheme || "https"}</span>
          <input
            className="web-url"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t("tab.preview.placeholder") || "输入网址或搜索"}
            spellCheck={false}
            autoCapitalize="off"
            autoCorrect="off"
          />
          <button type="submit" className="web-go" title="前往" aria-label="前往">
            {t("tab.web.go")}
          </button>
        </form>
        <div className="web-chrome-row web-chrome-extras">
          {insecure && <span className="web-warn" title="明文 HTTP 连接">⚠ 不安全</span>}
          {loading && <span className="web-load" aria-label="loading">⟳</span>}
          <button
            type="button"
            className="web-nav-btn"
            onClick={openExternal}
            disabled={!url}
            title="在系统浏览器打开"
            aria-label="在系统浏览器打开"
          >
            ↗
          </button>
        </div>
      </div>
      {err && <div className="web-err">{err}</div>}
      {url ? (
        <iframe
          ref={iframeRef}
          className="web-frame"
          title="web-tab"
          src={url}
          sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
          referrerPolicy="no-referrer"
          onLoad={() => setLoading(false)}
          onError={() => {
            setLoading(false);
            setErr("页面加载失败,可能拒绝了嵌入");
          }}
        />
      ) : (
        <div className="web-home">
          <div className="web-home-title">浏览器</div>
          <div className="web-home-sub">在右侧打开任意 URL,或从下面快速开始</div>
          <div className="web-home-grid">
            {QUICK_LINKS.map((q) => (
              <button
                key={q.url}
                type="button"
                className="web-home-card"
                onClick={() => navigate(q.url)}
              >
                <span className="web-home-card-label">{q.label}</span>
                <span className="web-home-card-hint">{q.hint}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
