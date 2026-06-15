import { create } from "zustand";
import { persist } from "zustand/middleware";

export type TabKind = "files" | "web" | "diff" | "preview" | "plan" | "goals";
export type TabState = {
  id: string;
  kind: TabKind;
  title: string;
  dataSource?: "local" | "wiki";
  data?: Record<string, any>;
};
type PaneState = {
  open: boolean;
  tabs: TabState[];
  active: string | null;
  width: number;
  setOpen: (open: boolean) => void;
  toggle: () => void;
  add: (tab: Omit<TabState, "id">) => string;
  remove: (id: string) => void;
  activate: (id: string) => void;
  setWidth: (w: number) => void;
};
function makeId() { return Math.random().toString(36).slice(2); }

// First-load seed: open the right pane with a built-in browser tab so the
// workspace feels like a codex-style desktop from the first keystroke. Users
// who explicitly collapsed it before will see their `open: false` restored
// from the persisted state, so the seed only fires on a fresh install.
const SEED_TAB: TabState = {
  id: "web-seed",
  kind: "web",
  title: "浏览器",
  data: { initialUrl: "" }, // empty -> WebTab will show its home/empty state
};

export const usePaneStore = create<PaneState>()(
  persist(
    (set, get) => ({
      // Default OPEN so the embedded browser is visible on first launch.
      // The persisted `open` field overrides this for returning users.
      open: true,
      // Seed with a web tab so the browser is the first thing the user sees.
      tabs: [SEED_TAB],
      active: SEED_TAB.id,
      width: 420,
      setOpen: (open) => set({ open }),
      toggle: () => set({ open: !get().open }),
      add: (t) => {
        const id = makeId();
        const tab: TabState = { ...t, id };
        set({ tabs: [...get().tabs, tab], active: id, open: true });
        return id;
      },
      remove: (id) => {
        const tabs = get().tabs.filter((t) => t.id !== id);
        const active = get().active === id ? (tabs[tabs.length - 1]?.id ?? null) : get().active;
        set({ tabs, active });
      },
      activate: (id) => set({ active: id, open: true }),
      setWidth: (width) => set({ width }),
    }),
    {
      name: "gepaw-pane",
      partialize: (s) => ({ tabs: s.tabs, active: s.active, open: s.open, width: s.width }),
      // Returning users keep their saved open/tabs; brand-new users (no entry
      // in localStorage) see the seed above. After the first write the seed
      // is the persisted state, so the default doesn't re-fire.
      merge: (persisted, current) => {
        const p = (persisted as Partial<PaneState>) || {};
        // If the persisted state is empty (first install), keep the seed.
        if (!p.tabs || (Array.isArray(p.tabs) && p.tabs.length === 0)) {
          return { ...current, open: p.open ?? current.open, width: p.width ?? current.width };
        }
        return { ...current, ...p };
      },
    },
  ),
);
