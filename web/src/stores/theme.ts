// Codex-style theme toggle. The persisted preference is one of
// "light" / "dark" / "system"; when "system" the UI follows the OS
// prefers-color-scheme setting via a media-query listener.
import { create } from "zustand";
import { persist } from "zustand/middleware";

export type ThemeMode = "light" | "dark" | "system";

type State = {
  mode: ThemeMode;
  setMode: (m: ThemeMode) => void;
  /** Resolved value: "light" or "dark" after applying the system preference. */
  resolved: () => "light" | "dark";
};

function systemPrefersDark(): boolean {
  if (typeof window === "undefined" || !window.matchMedia) return false;
  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

function applyToDom(resolved: "light" | "dark"): void {
  if (typeof document === "undefined") return;
  document.documentElement.dataset.theme = resolved;
}

export const useThemeStore = create<State>()(
  persist(
    (set, get) => ({
      mode: "dark",
      setMode: (m) => {
        set({ mode: m });
        const resolved = m === "system" ? (systemPrefersDark() ? "dark" : "light") : m;
        applyToDom(resolved);
      },
      resolved: () => {
        const m = get().mode;
        return m === "system" ? (systemPrefersDark() ? "dark" : "light") : m;
      },
    }),
    { name: "gepaw-theme" },
  ),
);

// Apply the persisted mode on boot and subscribe to OS changes for "system".
if (typeof window !== "undefined" && window.matchMedia) {
  const mq = window.matchMedia("(prefers-color-scheme: dark)");
  const sync = () => {
    const resolved = useThemeStore.getState().resolved();
    applyToDom(resolved);
  };
  mq.addEventListener("change", sync);
  sync();
}
