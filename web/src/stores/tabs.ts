import { create } from "zustand";
import { persist } from "zustand/middleware";

export type TabKind = "files" | "web" | "diff" | "preview" | "plan";
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

export const usePaneStore = create<PaneState>()(
  persist(
    (set, get) => ({
      open: false,
      tabs: [],
      active: null,
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
    { name: "gepaw-pane", partialize: (s) => ({ tabs: s.tabs, active: s.active, open: s.open, width: s.width }) },
  ),
);
