// Progress store: tracks a single "current run" through the chat / task
// pipeline. Two views into the same state:
//
//   1. Top floating pill (Codex-style): "Context Left 60.2% 397.7K / 1.0M"
//      with a thin progress bar.
//
//   2. Right-pane step list (MiniMax Code-style): ordered steps with
//      pending / running / done / failed states, strikethrough on done.
//
// We don't try to pull real server-side progress yet — the chat endpoint
// is a single POST that returns the reply, not an event stream. Instead
// we drive the steps from the Assistant page lifecycle (send -> thinking
// -> replying -> done) and let the user see what's happening. When the
// backend grows SSE / progress events, just hook the SSE handlers into
// `setSteps` and replace the synthetic advances.

import { create } from "zustand";

export type StepStatus = "pending" | "running" | "done" | "failed";

export type Step = {
  id: string;
  label: string;
  status: StepStatus;
  detail?: string;
  // Optional right-aligned secondary line (e.g. file count, "已编辑 3 个文件")
  hint?: string;
  startedAt?: number;
  finishedAt?: number;
};

export type ProgressState = {
  // Top bar
  running: boolean;
  label: string;            // "Context Left" | "执行中" | "已就绪"
  usedTokens: number;       // rough bytes / tokens used
  maxTokens: number;        // rough bytes / tokens budget (default 1.0M)
  // Right pane
  steps: Step[];
  collapsed: boolean;
  // Actions
  beginRun: (label?: string) => void;
  endRun: () => void;
  setBudget: (used: number, max: number) => void;
  bump: (delta: number) => void;             // quick token bump (incoming chunks)
  setLabel: (label: string) => void;
  pushStep: (s: Omit<Step, "startedAt" | "finishedAt"> & { status?: StepStatus }) => void;
  setStep: (id: string, patch: Partial<Step>) => void;
  markStep: (id: string, status: StepStatus, detail?: string) => void;
  nextStep: () => void;     // running -> done, next pending -> running
  reset: () => void;
  toggleCollapsed: () => void;
};

let _sid = 0;
const sid = () => `s${Date.now().toString(36)}_${(++_sid).toString(36)}`;

export const useProgressStore = create<ProgressState>((set, get) => ({
  running: false,
  label: "已就绪",
  usedTokens: 0,
  maxTokens: 1_000_000,
  steps: [],
  collapsed: false,

  beginRun: (label = "执行中") => set({
    running: true,
    label,
    usedTokens: 0,
    steps: [
      { id: sid(), label: "解析请求", status: "running", startedAt: Date.now() },
      { id: sid(), label: "思考中", status: "pending" },
      { id: sid(), label: "等待响应", status: "pending" },
      { id: sid(), label: "整理结果", status: "pending" },
    ],
  }),

  endRun: () => {
    // Mark any still-pending steps as done so the UI looks settled.
    const now = Date.now();
    set((s) => ({
      running: false,
      label: "已就绪",
      steps: s.steps.map((st) => (st.status === "pending" || st.status === "running")
        ? { ...st, status: "done", finishedAt: now }
        : st),
    }));
  },

  setBudget: (used, max) => set({ usedTokens: used, maxTokens: Math.max(max, 1) }),
  bump: (delta) => set((s) => ({ usedTokens: s.usedTokens + Math.max(0, delta) })),
  setLabel: (label) => set({ label }),

  pushStep: (s) => set((st) => ({
    steps: [...st.steps, {
      id: sid(),
      label: s.label,
      status: s.status ?? "pending",
      detail: s.detail,
      hint: s.hint,
      startedAt: s.status === "running" ? Date.now() : undefined,
    }],
  })),

  setStep: (id, patch) => set((s) => ({
    steps: s.steps.map((st) => (st.id === id ? { ...st, ...patch } : st)),
  })),

  markStep: (id, status, detail) => set((s) => ({
    steps: s.steps.map((st) => {
      if (st.id !== id) return st;
      const now = Date.now();
      return {
        ...st,
        status,
        detail: detail ?? st.detail,
        startedAt: st.startedAt ?? (status === "running" ? now : undefined),
        finishedAt: status === "done" || status === "failed" ? now : st.finishedAt,
      };
    }),
  })),

  nextStep: () => set((s) => {
    const now = Date.now();
    const idx = s.steps.findIndex((st) => st.status === "running");
    const next = s.steps.findIndex((st) => st.status === "pending");
    return {
      steps: s.steps.map((st, i) => {
        if (i === idx && st.status === "running") {
          return { ...st, status: "done", finishedAt: now };
        }
        if (i === next) {
          return { ...st, status: "running", startedAt: now };
        }
        return st;
      }),
    };
  }),

  reset: () => set({
    running: false,
    label: "已就绪",
    usedTokens: 0,
    steps: [],
  }),

  toggleCollapsed: () => set((s) => ({ collapsed: !s.collapsed })),
}));
