// Local-only settings store: persisted via localStorage. Admins configure
// skills/MCP/plugins server-side; this store is for per-user UI preferences,
// including the structured "Memory" tree (L0 outline + dated L1/L2 layers +
// keyword index) that the user requested.
import { create } from "zustand";
import { persist } from "zustand/middleware";

/**
 * Memory is layered to mirror a qwenpaw-style bottom-up + dated journal:
 *   - L0  outline: one-paragraph high-level summary of "who the user is".
 *   - L1  topics:  short bullet topics the user wants the agent to remember.
 *   - L2  dated:   daily journal entries; each date is its own file, so
 *                  older context can age out without rewriting the outline.
 *   - tags:        cross-cutting keyword index pointing into L1/L2 by date.
 *   - links:       explicit cross-references between entries (by id).
 */
export type MemoryLayer = {
  /** L0 outline (markdown). */
  outline: string;
  /** L1 topics; each has stable id so cross-refs can target it. */
  topics: MemoryTopic[];
  /** L2 dated entries keyed by ISO date (yyyy-mm-dd). */
  dated: Record<string, MemoryEntry>;
  /** Keyword index: keyword -> list of entry ids it appears in. */
  tags: MemoryTagIndex;
  /** Cross-references: source id -> list of target ids. */
  links: MemoryLinks;
};

export type MemoryTopic = {
  id: string;
  title: string;
  body: string;
  /** "agent" (default), "user", or "user-pinned" (user-promoted, locked from aging). */
  author: "agent" | "user" | "user-pinned";
  updatedAt: number;
};

export type MemoryEntry = {
  id: string;
  date: string;
  body: string;
  topicIds: string[];
  keywords: string[];
  /** "agent" (default), "user", or "user-pinned" (locked from aging). */
  author: "agent" | "user" | "user-pinned";
  updatedAt: number;
};

export type MemoryTagIndex = Record<string, string[]>;

export type MemoryLinks = Record<string, string[]>;

const EMPTY_MEMORY: MemoryLayer = {
  outline: "",
  topics: [],
  dated: {},
  tags: {},
  links: {},
};

export type Settings = {
  /** Allow launching the Computer Use overlay from the chat "+" menu. */
  computerUseEnabled: boolean;
  setComputerUseEnabled: (v: boolean) => void;
  /** Show full source messages vs assistant-only in the chat stream. */
  showRawMessages: boolean;
  setShowRawMessages: (v: boolean) => void;
  /** Auto-compact long conversations to free the context window. */
  autoCompactEnabled: boolean;
  setAutoCompactEnabled: (v: boolean) => void;
  compactThreshold: number;
  setCompactThreshold: (n: number) => void;
  /** Structured memory tree (qwenpaw-style: outline + topics + dated). */
  memoryEnabled: boolean;
  setMemoryEnabled: (v: boolean) => void;
  memory: MemoryLayer;
  setMemory: (m: MemoryLayer) => void;
  patchMemory: (patch: Partial<MemoryLayer>) => void;
  // Convenience mutators
  setMemoryOutline: (s: string) => void;
  upsertMemoryTopic: (t: MemoryTopic) => void;
  removeMemoryTopic: (id: string) => void;
  pinMemoryTopic: (id: string) => void;
  upsertMemoryEntry: (e: MemoryEntry) => void;
  removeMemoryEntry: (id: string) => void;
  pinMemoryEntry: (id: string) => void;
  addMemoryLink: (fromId: string, toId: string) => void;
  removeMemoryLink: (fromId: string, toId: string) => void;
  rebuildMemoryTagIndex: () => void;
};

function newId() { return Math.random().toString(36).slice(2, 10); }

function indexKeywords(entry: MemoryEntry, idx: MemoryTagIndex) {
  for (const k of entry.keywords) {
    const key = k.trim().toLowerCase();
    if (!key) continue;
    if (!idx[key]) idx[key] = [];
    if (!idx[key].includes(entry.id)) idx[key].push(entry.id);
  }
}

export const useSettingsStore = create<Settings>()(
  persist(
    (set, get) => ({
      computerUseEnabled: true,
      setComputerUseEnabled: (v) => set({ computerUseEnabled: v }),
      showRawMessages: false,
      setShowRawMessages: (v) => set({ showRawMessages: v }),
      autoCompactEnabled: true,
      setAutoCompactEnabled: (v) => set({ autoCompactEnabled: v }),
      compactThreshold: 8000,
      setCompactThreshold: (n) => set({ compactThreshold: Math.max(500, Math.min(1000000, n | 0)) }),
      memoryEnabled: false,
      setMemoryEnabled: (v) => set({ memoryEnabled: v }),

      memory: EMPTY_MEMORY,
      setMemory: (m) => set({ memory: m }),
      patchMemory: (patch) => set((s) => ({ memory: { ...s.memory, ...patch } })),

      setMemoryOutline: (s) => set((st) => ({ memory: { ...st.memory, outline: s } })),
      upsertMemoryTopic: (t) =>
        set((st) => {
          const topics = st.memory.topics.filter((x) => x.id !== t.id);
          topics.push({ ...t, author: t.author ?? "agent", updatedAt: Date.now() });
          topics.sort((a, b) => a.title.localeCompare(b.title));
          return { memory: { ...st.memory, topics } };
        }),
      removeMemoryTopic: (id) =>
        set((st) => {
          const topics = st.memory.topics.filter((x) => x.id !== id);
          // Drop dangling topic refs in dated entries.
          const dated: Record<string, MemoryEntry> = {};
          for (const [date, e] of Object.entries(st.memory.dated)) {
            dated[date] = { ...e, topicIds: e.topicIds.filter((tid) => tid !== id) };
          }
          return { memory: { ...st.memory, topics, dated } };
        }),
      pinMemoryTopic: (id) =>
        set((st) => {
          const topics = st.memory.topics.map((x) => x.id === id
            ? { ...x, author: (x.author === "user-pinned" ? "agent" : "user-pinned") as MemoryTopic["author"] }
            : x);
          return { memory: { ...st.memory, topics } };
        }),
      upsertMemoryEntry: (e) => {
        set((st) => {
          const dated = { ...st.memory.dated, [e.date]: { ...e, updatedAt: Date.now() } };
          return { memory: { ...st.memory, dated } };
        });
        // Rebuild the keyword index on every entry upsert.
        get().rebuildMemoryTagIndex();
      },
      removeMemoryEntry: (id) => {
        set((st) => {
          const dated: Record<string, MemoryEntry> = {};
          for (const [date, e] of Object.entries(st.memory.dated)) {
            if (e.id !== id) dated[date] = e;
          }
          // Strip dangling links that pointed at the removed id.
          const links: MemoryLinks = {};
          for (const [from, tos] of Object.entries(st.memory.links)) {
            if (from === id) continue;
            links[from] = tos.filter((x) => x !== id);
          }
          return { memory: { ...st.memory, dated, links } };
        });
        get().rebuildMemoryTagIndex();
      },
      pinMemoryEntry: (id) =>
        set((st) => {
          const dated: Record<string, MemoryEntry> = {};
          for (const [date, e] of Object.entries(st.memory.dated)) {
            if (e.id === id) {
              dated[date] = { ...e, author: (e.author === "user-pinned" ? "agent" : "user-pinned") as MemoryEntry["author"] };
            } else {
              dated[date] = e;
            }
          }
          return { memory: { ...st.memory, dated } };
        }),
      addMemoryLink: (fromId, toId) =>
        set((st) => {
          if (fromId === toId) return st;
          const cur = st.memory.links[fromId] || [];
          if (cur.includes(toId)) return st;
          return { memory: { ...st.memory, links: { ...st.memory.links, [fromId]: [...cur, toId] } } };
        }),
      removeMemoryLink: (fromId, toId) =>
        set((st) => {
          const cur = st.memory.links[fromId] || [];
          if (!cur.includes(toId)) return st;
          const next = cur.filter((x) => x !== toId);
          const links = { ...st.memory.links, [fromId]: next };
          if (next.length === 0) delete links[fromId];
          return { memory: { ...st.memory, links } };
        }),
      rebuildMemoryTagIndex: () =>
        set((st) => {
          const tags: MemoryTagIndex = {};
          for (const e of Object.values(st.memory.dated)) {
            indexKeywords(e, tags);
          }
          return { memory: { ...st.memory, tags } };
        }),
    }),
    {
      name: "gepaw-settings-v1",
      version: 2,
      // Migrate from the legacy single-md memoryNote field.
      migrate: (persisted: any, fromVersion) => {
        if (!persisted || fromVersion < 2) {
          if (persisted && typeof persisted.memoryNote === "string" && persisted.memoryNote) {
            const id = newId();
            const today = new Date().toISOString().slice(0, 10);
            persisted.memory = {
              outline: "",
              topics: [],
              dated: { [today]: { id, date: today, body: persisted.memoryNote, topicIds: [], keywords: [], author: "agent", updatedAt: Date.now() } },
              tags: {},
              links: {},
            };
            delete persisted.memoryNote;
          }
        }
        return persisted as Settings;
      },
    },
  ),
);

// Helpers exported for the UI to render the memory tree.
export function emptyMemoryEntry(date: string): MemoryEntry {
  return { id: newId(), date, body: "", topicIds: [], keywords: [], author: "agent", updatedAt: Date.now() };
}
export function emptyMemoryTopic(): MemoryTopic {
  return { id: newId(), title: "", body: "", author: "agent", updatedAt: Date.now() };
}
export { newId as makeMemoryId };
export { EMPTY_MEMORY };
