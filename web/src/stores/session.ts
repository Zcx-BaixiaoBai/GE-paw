// Per-session UI state. We mirror what the server returns and stay
// optimistic: when the user picks a permission we update locally first,
// then PATCH /api/client/sessions/{id} to persist. A failure rolls back.
import { create } from "zustand";
import { apiGet, apiPatch, apiDel } from "../lib/api";

export type PermissionMode = "full" | "smart" | "strict" | "readonly";

export type Session = {
  id: string;
  title: string;
  status: string;
  pinned: boolean;
  archived?: boolean;
  channel_kind: string | null;
  permission: PermissionMode | null;
  created_at: string | null;
  last_message_at: string | null;
};

type State = {
  byId: Record<string, Session>;
  load: (id: string) => Promise<Session | null>;
  setPermission: (id: string, mode: PermissionMode | null) => Promise<void>;
  rename: (id: string, title: string) => Promise<void>;
  pin: (id: string, pinned: boolean) => Promise<void>;
  archive: (id: string, archived: boolean) => Promise<void>;
  remove: (id: string) => Promise<void>;
  upsert: (s: Session) => void;
};

export const useSessionStore = create<State>((set, get) => ({
  byId: {},
  load: async (id) => {
    try {
      const cached = get().byId[id];
      if (cached) return cached;
      const s = await apiGet<Session>(`/client/sessions/${id}`);
      set({ byId: { ...get().byId, [id]: s } });
      return s;
    } catch {
      return null;
    }
  },
  setPermission: async (id, mode) => {
    const prev = get().byId[id];
    const optimistic: Session | undefined = prev
      ? { ...prev, permission: mode }
      : undefined;
    if (optimistic) set({ byId: { ...get().byId, [id]: optimistic } });
    try {
      const fresh = await apiPatch<Session>(`/client/sessions/${id}`, { permission: mode });
      set({ byId: { ...get().byId, [id]: fresh } });
    } catch (e) {
      if (prev) set({ byId: { ...get().byId, [id]: prev } });
      throw e;
    }
  },
  rename: async (id, title) => {
    const prev = get().byId[id];
    if (prev) set({ byId: { ...get().byId, [id]: { ...prev, title } } });
    try {
      const fresh = await apiPatch<Session>(`/client/sessions/${id}`, { title });
      set({ byId: { ...get().byId, [id]: fresh } });
    } catch (e) {
      if (prev) set({ byId: { ...get().byId, [id]: prev } });
      throw e;
    }
  },
  pin: async (id, pinned) => {
    const prev = get().byId[id];
    if (prev) set({ byId: { ...get().byId, [id]: { ...prev, pinned } } });
    try {
      const fresh = await apiPatch<Session>(`/client/sessions/${id}`, { pinned });
      set({ byId: { ...get().byId, [id]: fresh } });
    } catch (e) {
      if (prev) set({ byId: { ...get().byId, [id]: prev } });
      throw e;
    }
  },
  archive: async (id, archived) => {
    const prev = get().byId[id];
    if (prev) set({ byId: { ...get().byId, [id]: { ...prev, archived } } });
    try {
      const fresh = await apiPatch<Session>(`/client/sessions/${id}`, { archived });
      set({ byId: { ...get().byId, [id]: fresh } });
    } catch (e) {
      if (prev) set({ byId: { ...get().byId, [id]: prev } });
      throw e;
    }
  },
  remove: async (id) => {
    const prev = get().byId[id];
    const next = { ...get().byId };
    delete next[id];
    set({ byId: next });
    try {
      await apiDel(`/client/sessions/${id}`);
    } catch (e) {
      if (prev) set({ byId: { ...get().byId, [id]: prev } });
      throw e;
    }
  },
  upsert: (s) => set({ byId: { ...get().byId, [s.id]: s } }),
}));