// Codex-style theme menu: light / dark / system. Persists via the theme store.
import { useEffect, useRef, useState } from "react";
import { useThemeStore, type ThemeMode } from "../stores/theme";
import { IconCheck, IconMoon, IconSun } from "./Icons";
import { t } from "../lib/i18n";

const OPTIONS: { value: ThemeMode; label: string; icon: React.ReactNode }[] = [
  { value: "light", label: t("theme.menu.light"), icon: <IconSun size={14} /> },
  { value: "dark", label: t("theme.menu.dark"), icon: <IconMoon size={14} /> },
  { value: "system", label: t("theme.menu.system"), icon: <IconCheck size={14} /> },
];

export function ThemeMenu({ compact = false }: { compact?: boolean }) {
  const mode = useThemeStore((s) => s.mode);
  const setMode = useThemeStore((s) => s.setMode);
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onClick = (e: MouseEvent) => {
      if (!ref.current?.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, [open]);

  const current = OPTIONS.find((o) => o.value === mode) ?? OPTIONS[1];

  return (
    <div className="dropdown" ref={ref}>
      <button
        type="button"
        className={"topbar-icon-btn" + (compact ? " compact" : "")}
        onClick={() => setOpen((v) => !v)}
        title={t("topbar.toggleTheme")}
      >
        {current.icon}
      </button>
      {open && (
        <div className="dropdown-menu theme-menu" role="menu">
          <div className="dropdown-title">{t("theme.menu.title")}</div>
          {OPTIONS.map((o) => (
            <button
              key={o.value}
              type="button"
              className={"dropdown-item" + (o.value === mode ? " active" : "")}
              onClick={() => { setMode(o.value); setOpen(false); }}
              role="menuitemradio"
              aria-checked={o.value === mode}
            >
              <span className="dropdown-item-icon">{o.icon}</span>
              <span className="dropdown-item-text">{o.label}</span>
              {o.value === mode && <span className="dropdown-item-check"><IconCheck size={12} /></span>}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
