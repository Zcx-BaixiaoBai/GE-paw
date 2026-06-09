import { useEffect, useState } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { useAuthStore } from "../stores/auth";
import { apiGet } from "../lib/api";
import { LeftPane } from "../components/LeftPane";
import { RightPane } from "../components/RightPane/RightPane";
import { usePaneStore } from "../stores/tabs";

export function AppLayout() {
  const [leftCollapsed, setLeftCollapsed] = useState(false);
  const setIdentity = useAuthStore((s) => s.setIdentity);
  const clear = useAuthStore((s) => s.clear);
  const username = useAuthStore((s) => s.username);
  const role = useAuthStore((s) => s.role);
  const orgName = useAuthStore((s) => s.orgName);
  const paneOpen = usePaneStore((s) => s.open);
  const paneToggle = usePaneStore((s) => s.toggle);
  const nav = useNavigate();
  const [theme, setTheme] = useState(localStorage.getItem("gepaw-theme") || "light");

  useEffect(() => {
    if (!username) {
      apiGet<any>("/auth/me").then((d) => {
        if (d?.username) setIdentity(d);
        else clear();
      }).catch(() => clear());
    }
  }, [username, setIdentity, clear]);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("gepaw-theme", theme);
  }, [theme]);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (!(e.ctrlKey || e.metaKey)) return;
      if (e.key === "b") { e.preventDefault(); setLeftCollapsed((v) => !v); }
      if (e.key === "j") { e.preventDefault(); paneToggle(); }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [paneToggle]);

  function bodyClass() {
    if (leftCollapsed && !paneOpen) return "both-collapsed";
    if (leftCollapsed) return "left-collapsed";
    if (!paneOpen) return "right-collapsed";
    return "";
  }

  return (
    <div className="app-shell">
      <div className="topbar">
        <span className="brand">GE-paw</span>
        <span className="pill">{orgName || "org"}</span>
        {role === "admin" && <span className="pill" style={{ color: "var(--accent)" }}>admin</span>}
        <span className="spacer" />
        {username && <span>{username}</span>}
        <button className="icon-btn" title="Toggle left pane (Ctrl+B)" onClick={() => setLeftCollapsed((v) => !v)}>{"☰"}</button>
        <button className="icon-btn" title="Toggle right pane (Ctrl+J)" onClick={paneToggle}>{"⧉"}</button>
        <button className="icon-btn" title="Toggle theme" onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>{theme === "dark" ? "☀" : "☽"}</button>
        <button className="icon-btn" title="Logout" onClick={() => { clear(); nav("/login"); }}>{"⏻"}</button>
      </div>
      <div className={"app-body " + bodyClass()}>
        {!leftCollapsed ? <LeftPane /> : <div className="left-pane" style={{ width: "var(--left-w-collapsed)" }} />}
        <div className="center-pane"><Outlet /></div>
        <RightPane />
      </div>
    </div>
  );
}
