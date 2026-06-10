// Codex-style goals store. Goals are user-visible checkpoints that an agent
// commits to and updates as it works through a session. Stored in localStorage
// keyed by session id so they survive reloads without a backend round-trip.
import { create } from "zustand";
import { persist } from "zustand/middleware";

export type GoalStatus = "pending" | "in_progress" | "done" | "failed";

export type Goal = {
  id: string;
  text: string;
  status: GoalStatus;
  createdAt: string;
  updatedAt: string;
};

type State = {
  bySession: Record<string, Goal[]>;
  get: (sessionId: string) => Goal[];
  add: (sessionId: string, text: string) => Goal | null;
  update: (sessionId: string, id: string, patch: Partial<Pick<Goal, "text" | "status">>) => void;
  remove: (sessionId: string, id: string) => void;
  clear: (sessionId: string) => void;
};

function makeId() {
  return Math.random().toString(36).slice(2, 10);
}

export const useGoalsStore = create<State>()(
  persist(
    (set, get) => ({
      bySession: {},
      get: (sessionId) => get().bySession[sessionId] ?? [],
      add: (sessionId, text) => {
        const trimmed = text.trim();
        if (!sessionId || !trimmed) return null;
        const now = new Date().toISOString();
        const goal: Goal = {
          id: makeId(),
          text: trimmed,
          status: "pending",
          createdAt: now,
          updatedAt: now,
        };
        const list = get().bySession[sessionId] ?? [];
        set({ bySession: { ...get().bySession, [sessionId]: [...list, goal] } });
        return goal;
      },
      update: (sessionId, id, patch) => {
        const list = get().bySession[sessionId];
        if (!list) return;
        const next = list.map((g) =>
          g.id === id ? { ...g, ...patch, updatedAt: new Date().toISOString() } : g,
        );
        set({ bySession: { ...get().bySession, [sessionId]: next } });
      },
      remove: (sessionId, id) => {
        const list = get().bySession[sessionId];
        if (!list) return;
        set({
          bySession: {
            ...get().bySession,
            [sessionId]: list.filter((g) => g.id !== id),
          },
        });
      },
      clear: (sessionId) => {
        const { [sessionId]: _, ...rest } = get().bySession;
        set({ bySession: rest });
      },
    }),
    { name: "gepaw-goals" },
  ),
);
