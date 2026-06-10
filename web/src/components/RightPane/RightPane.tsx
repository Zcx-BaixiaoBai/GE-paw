import { useEffect, useRef, useState } from "react";
import { usePaneStore } from "../../stores/tabs";
import { TabRegistry, AllTabKinds, TabKind } from "./registry";

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
          <div className="tab" style={{ color: "var(--fg-faint)", cursor: "default" }}>无标签页</div>
        )}
        {tabs.map((t) => {
          const meta = TabRegistry[t.kind];
          return (
            <div key={t.id} className={"tab" + (t.id === active ? " active" : "")} onClick={() => activate(t.id)} title={meta.hint || meta.title}>
              <span>{meta.icon}</span><span>{t.title}</span>
              <span className="close" onClick={(e) => { e.stopPropagation(); remove(t.id); }}>{"×"}</span>
            </div>
          );
        })}
        <div className="tab-add" ref={menuRef}>
          <button className="icon-btn" title="打开标签页" onClick={() => setMenuOpen((v) => !v)}>{"+"}</button>
          {menuOpen && (
            <div className="tab-menu">
              {AllTabKinds.map((k) => {
                const m = TabRegistry[k];
                return (
                  <button key={k} className="tab-menu-item" onClick={() => openTab(k)} title={m.hint}>
                    <span>{m.icon}</span><span>{m.title}</span>
                    <span className="kbd">{m.available ? "可用" : "即将"}</span>
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </div>
      <div className="tab-body">
        {tabs.length === 0 && <div className="tab-empty">暂无标签页，点击 + 添加。</div>}
        {tabs.map((t) => {
          if (t.id !== active) return null;
          const Comp = TabRegistry[t.kind].component;
          return <Comp key={t.id} data={t.data} />;
        })}
      </div>
    </div>
  );
}


