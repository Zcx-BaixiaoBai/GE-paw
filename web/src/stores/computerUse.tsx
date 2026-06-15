// Computer use: a non-blocking indicator. The agent has direct control of the
// user's screen — there is no modal, no popup, no extra window. The user sees:
//   - a pulsing blue glow around the viewport (border halo)
//   - a small status badge in the topbar (e.g. "● 代理正在操控")
//   - an optional small floating activity log (bottom-right) that the user
//     can collapse but cannot fully dismiss while a run is active
//
// The actual screen content is whatever the agent is doing — in a Tauri build
// this would be the live Tauri screenshot / input bridge. In dev/mock we just
// animate the halo + record actions for the activity log.
import { useEffect, useState } from "react";
import { create } from "zustand";
import { t } from "../lib/i18n";

export type ComputerAction =
  | { kind: "screenshot"; at: number }
  | { kind: "click"; at: number; x: number; y: number; button: "left" | "right" | "middle" }
  | { kind: "type"; at: number; text: string }
  | { kind: "key"; at: number; combo: string }
  | { kind: "note"; at: number; text: string };

export type ComputerUseState = "idle" | "running" | "error";

type State = {
  status: ComputerUseState;
  error: string | null;
  actions: ComputerAction[];
  startedAt: number | null;
  lastActionAt: number | null;
  setRunning: () => void;
  setIdle: () => void;
  setError: (msg: string | null) => void;
  pushAction: (a: ComputerAction) => void;
  reset: () => void;
};

export const useComputerUseStore = create<State>((set) => ({
  status: "idle",
  error: null,
  actions: [],
  startedAt: null,
  lastActionAt: null,
  setRunning: () => set({
    status: "running",
    error: null,
    startedAt: Date.now(),
  }),
  setIdle: () => set({
    status: "idle",
    error: null,
    startedAt: null,
    lastActionAt: null,
  }),
  setError: (msg) => set({ status: "error", error: msg }),
  pushAction: (a) =>
    set((prev) => ({
      actions: [a, ...prev.actions].slice(0, 50),
      lastActionAt: Date.now(),
    })),
  reset: () => set({
    status: "idle",
    error: null,
    actions: [],
    startedAt: null,
    lastActionAt: null,
  }),
}));

// Overlay component: a thin "chrome" around the app — the edge halo, the
// topbar status badge, and the optional floating activity log. The agent
// runtime drives `useComputerUseStore`; this component is just the visual.
export function ComputerUseIndicator() {
  const status = useComputerUseStore((s) => s.status);
  const error = useComputerUseStore((s) => s.error);
  const actions = useComputerUseStore((s) => s.actions);
  const startedAt = useComputerUseStore((s) => s.startedAt);
  const setIdle = useComputerUseStore((s) => s.setIdle);
  const [elapsed, setElapsed] = useState(0);
  const [logOpen, setLogOpen] = useState(true);

  useEffect(() => {
    if (status !== "running") {
      setElapsed(0);
      return;
    }
    const t0 = startedAt || Date.now();
    setElapsed(Math.max(0, Math.floor((Date.now() - t0) / 1000)));
    const id = setInterval(() => {
      setElapsed(Math.max(0, Math.floor((Date.now() - t0) / 1000)));
    }, 500);
    return () => clearInterval(id);
  }, [status, startedAt]);

  if (status === "idle") return null;

  const isRunning = status === "running";
  const isError = status === "error";
  const lastAction = actions[0];

  return (
    <>
      {/* Edge halo: a fixed-position ring just inside the viewport. */}
      <div
        className={"cu-halo" + (isRunning ? " cu-halo-running" : "") + (isError ? " cu-halo-error" : "")}
        aria-hidden
      />

      {/* Topbar status pill (rendered via portal so it can sit next to the
          existing topbar-right cluster without disturbing its layout). */}
      <div className="cu-status" role="status" aria-live="polite">
        <span className={"cu-status-dot" + (isRunning ? " on" : "")} />
        {isRunning && (
          <span className="cu-status-text">
            {t("computerUse.running")}
            <span className="cu-status-elapsed"> · {elapsed}s</span>
            {lastAction && (
              <span className="cu-status-action"> · {describeAction(lastAction)}</span>
            )}
          </span>
        )}
        {isError && (
          <span className="cu-status-text cu-status-text-error">
            {t("computerUse.errored")}
            {error && <span className="cu-status-error-detail"> {error}</span>}
          </span>
        )}
        <button
          type="button"
          className="cu-status-stop"
          onClick={() => setIdle()}
          title={t("computerUse.stop")}
        >
          {t("computerUse.stop")}
        </button>
      </div>

      {/* Optional small floating activity log (collapsible). */}
      {isRunning && actions.length > 0 && (
        <div className={"cu-floater" + (logOpen ? "" : " collapsed")}>
          <button
            type="button"
            className="cu-floater-head"
            onClick={() => setLogOpen((v) => !v)}
            aria-expanded={logOpen}
          >
            <span>{t("computerUse.activity")}</span>
            <span className="cu-floater-count">{actions.length}</span>
            <span className="cu-floater-caret">{logOpen ? "▾" : "▸"}</span>
          </button>
          {logOpen && (
            <ul className="cu-floater-list">
              {actions.slice(0, 8).map((a, i) => (
                <li key={i} className={"cu-floater-item cu-floater-" + a.kind}>
                  <span className="cu-floater-kind">{labelOf(a)}</span>
                  <span className="cu-floater-detail">{detailOf(a)}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </>
  );
}

function labelOf(a: ComputerAction): string {
  switch (a.kind) {
    case "screenshot": return t("computerUse.actions.screenshot");
    case "click":      return t("computerUse.actions.click");
    case "type":       return t("computerUse.actions.type");
    case "key":        return t("computerUse.actions.key");
    case "note":       return t("computerUse.actions.note");
  }
}

function detailOf(a: ComputerAction): string {
  switch (a.kind) {
    case "screenshot": return new Date(a.at).toLocaleTimeString();
    case "click":      return `(${a.x}, ${a.y}) · ${a.button}`;
    case "type":       return a.text.length > 32 ? a.text.slice(0, 32) + "…" : a.text;
    case "key":        return a.combo;
    case "note":       return a.text;
  }
}

function describeAction(a: ComputerAction): string {
  if (a.kind === "click") return `click (${a.x}, ${a.y})`;
  if (a.kind === "type")  return `type "${a.text.length > 16 ? a.text.slice(0, 16) + "…" : a.text}"`;
  if (a.kind === "key")   return a.combo;
  if (a.kind === "screenshot") return "screenshot";
  if (a.kind === "note") return a.text;
  return "";
}
