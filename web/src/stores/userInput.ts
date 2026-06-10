// Codex-style "request user input" modal queue. The agent runtime calls
// `requestUserInput(...)` (directly or via a server event) which enqueues a
// modal that the user must dismiss before the agent can continue. Only one
// modal is shown at a time; the queue is preserved across navigations.
import { create } from "zustand";

export type UserInputOption = {
  id: string;
  label: string;
  description?: string;
};

export type PendingUserInput = {
  id: string;
  question: string;
  description?: string;
  options: UserInputOption[];
  allowFreeText: boolean;
  resolve: (value: { optionId: string | null; freeText: string | null }) => void;
};

type State = {
  queue: PendingUserInput[];
  current: PendingUserInput | null;
  enqueue: (req: Omit<PendingUserInput, "id" | "resolve"> & { resolve?: PendingUserInput["resolve"] }) => string;
  dismiss: (value: { optionId: string | null; freeText: string | null }) => void;
};

function makeId() {
  return Math.random().toString(36).slice(2, 10);
}

export const useUserInputStore = create<State>((set, get) => ({
  queue: [],
  current: null,
  enqueue: (req) => {
    const id = makeId();
    const item: PendingUserInput = {
      id,
      question: req.question,
      description: req.description,
      options: req.options,
      allowFreeText: req.allowFreeText ?? true,
      resolve: req.resolve ?? (() => undefined),
    };
    const queue = [...get().queue, item];
    set({
      queue,
      current: get().current ?? item,
    });
    return id;
  },
  dismiss: (value) => {
    const cur = get().current;
    if (!cur) return;
    try { cur.resolve(value); } catch { /* swallow */ }
    const rest = get().queue.filter((q) => q.id !== cur.id);
    set({ queue: rest, current: rest[0] ?? null });
  },
}));

// Convenience helper for non-React callers (e.g. fetch error handlers that
// need a one-shot confirmation from the user).
export function requestUserInput(
  req: Omit<PendingUserInput, "id" | "resolve">,
): Promise<{ optionId: string | null; freeText: string | null }> {
  return new Promise((resolve) => {
    useUserInputStore.getState().enqueue({ ...req, resolve });
  });
}
