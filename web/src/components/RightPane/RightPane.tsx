import { useEffect, useRef, useState } from "react";
import { usePaneStore } from "../../stores/tabs";
import { TabRegistry, AllTabKinds, TabKind } from "./registry";
import { t } from "../../lib/i18n";
import { IconClose, IconPlus } from "../Icons";

export function RightPane() {
  const { open, tabs, active, remove, activate, add } = usePaneStore();
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (!(e.ctrlKey || e.metaKey) || e.altKey) return;
      if (e.key >= "1" && e.key <= "9") {
        e.preventDefault();
        const idx = parseInt(e.key, 10) - 1;
        if (tabs[idx]) activate(tabs[idx].id);
      }
      if (e.shiftKey && (e.key === "T" || e.key === "t")) {
        e.preventDefault();
        if (active) remove(active);
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [tabs, active, activate, remove]);

  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    }
    if (menuOpen) document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, [menuOpen]);

  if (!open) return <div />;

  function openTab(kind: TabKind) {
    const meta = TabRegistry[kind];
    add({ kind, title: meta.title });
    setMenuOpen(false);
  }

  return (
    <div className="right-pane">
      <div className="tabs-bar">
        {tabs.length === 0 && (
          <div className="tab" style={{ color: "var(--fg-faint)", cursor: "default" }}>{t("tab.none")}</div>
        )}
        {tabs.map((tab) => {
          const meta = TabRegistry[tab.kind];
          return (
            <div key={tab.id} className={"tab" + (tab.id === active ? " active" : "")} onClick={() => activate(tab.id)} title={meta.hint || meta.title}>
              <span>{meta.icon}</span><span>{tab.title}</span>
              <span className="close" onClick={(e) => { e.stopPropagation(); remove(tab.id); }}>{"×"}</span>
            </div>
          );
        })}
        <div className="tab-add" ref={menuRef}>
          <button className="icon-btn" title={t("tab.menu.open")} aria-label={t("tab.menu.open")} onClick={() => setMenuOpen((v) => !v)}><IconPlus size={13} /></button>
          {menuOpen && (
            <div className="tab-menu">
              {AllTabKinds.map((k) => {
                const m = TabRegistry[k];
                return (
                  <button key={k} className="tab-menu-item" onClick={() => openTab(k)} title={m.hint}>
                    <span>{m.icon}</span><span>{m.title}</span>
                    <span className="kbd">{m.available ? t("tab.menu.kbd.live") : t("tab.menu.kbd.soon")}</span>
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </div>
      <div className="tab-body">
        {tabs.length === 0 && <div className="tab-empty">{t("tab.none")}</div>}
        {tabs.map((tab) => {
          if (tab.id !== active) return null;
          const Comp = TabRegistry[tab.kind].component;
          return <Comp key={tab.id} data={tab.data} />;
        })}
      </div>
    </div>
  );
}
