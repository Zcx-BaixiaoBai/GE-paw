// Top floating progress pill (Codex desktop style):
//
//   ┌─────────────────────────────────────────────┐
//   │  Context Left 60.2%   397.7K / 1.0M   ▓▓▓▓▒ │
//   └─────────────────────────────────────────────┘
//
// Sits at the top center, above the page content, regardless of which
// page is active. Auto-hides when nothing is running, so it never adds
// noise to an idle session.
import { useEffect, useState } from "react";
import { useProgressStore } from "../stores/progress";
import { IconClose } from "./Icons";

function formatTokens(n: number): string {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + "M";
  if (n >= 1_000) return (n / 1_000).toFixed(1) + "K";
  return String(n);
}

export function ProgressBar() {
  const running = useProgressStore((s) => s.running);
  const label = useProgressStore((s) => s.label);
  const used = useProgressStore((s) => s.usedTokens);
  const max = useProgressStore((s) => s.maxTokens);
  const toggleCollapsed = useProgressStore((s) => s.toggleCollapsed);
  const collapsed = useProgressStore((s) => s.collapsed);
  const endRun = useProgressStore((s) => s.endRun);

  // Tiny "still alive" simulation when running so the bar moves even
  // without SSE — gives users feedback that the agent is doing work.
  const [bumpSeed, setBumpSeed] = useState(0);
  useEffect(() => {
    if (!running) return;
    const t = setInterval(() => setBumpSeed((v) => v + 1), 400);
    return () => clearInterval(t);
  }, [running]);

  useEffect(() => {
    if (!running) return;
    // Simulate progress while running. Real progress should come from
    // server-side events; this is just enough motion to feel alive.
    const step = Math.max(800, Math.round(max * 0.003));
    useProgressStore.setState((s) => ({ usedTokens: Math.min(s.maxTokens, s.usedTokens + step) }));
  }, [bumpSeed, running, max]);

  if (!running && used === 0) return null;

  const pct = Math.min(100, Math.round((used / max) * 1000) / 10);

  return (
    <div
      className={"progress-bar-floating" + (running ? " running" : " idle") + (collapsed ? " collapsed" : "")}
      role="status"
      aria-live="polite"
    >
      <div className="progress-bar-track">
        <div className="progress-bar-fill" style={{ width: pct + "%" }} />
      </div>
      <div className="progress-bar-row">
        <span className="progress-bar-label">{label}</span>
        <span className="progress-bar-pct">{pct.toFixed(1)}%</span>
        <span className="progress-bar-numbers">
          {formatTokens(used)} / {formatTokens(max)}
        </span>
        {running ? (
          <button
            type="button"
            className="progress-bar-stop"
            onClick={endRun}
            title="结束"
            aria-label="结束"
          >
            <IconClose size={12} />
          </button>
        ) : null}
        <button
          type="button"
          className="progress-bar-toggle"
          onClick={toggleCollapsed}
          title={collapsed ? "展开步骤" : "收起"}
          aria-label={collapsed ? "展开步骤" : "收起"}
        >
          {collapsed ? "▾" : "▴"}
        </button>
      </div>
    </div>
  );
}
