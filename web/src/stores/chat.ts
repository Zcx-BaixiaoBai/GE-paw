// Local-only UI state for the chat page: which inline drawer is open
// and pending composer input. Persisted only for the drawer preference.
import { create } from "zustand";
import { persist } from "zustand/middleware";

export type DrawerKind = "goals" | "plan" | null;

type State = {
  drawer: DrawerKind;
  setDrawer: (k: DrawerKind) => void;
  toggle: (k: Exclude<DrawerKind, null>) => void;
};

export const useChatUiStore = create<State>()(
  persist(
    (set, get) => ({
      drawer: null,
      setDrawer: (k) => set({ drawer: k }),
      toggle: (k) => set({ drawer: get().drawer === k ? null : k }),
    }),
    { name: "gepaw-chat-ui" },
  ),
);
