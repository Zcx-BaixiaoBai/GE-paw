// App shell: top thread header, optional left/right panes, modal portal.
// Codex-style: single top bar with brand on the left, ThreadHeader centred,
// and a clean right cluster (panel toggle / theme / user).
import { useEffect, useState } from "react";
import { Outlet, useSearchParams } from "react-router-dom";
import { useAuthStore } from "../stores/auth";
import { apiGet } from "../lib/api";
import { LeftPane } from "../components/LeftPane";
import { RightPane } from "../components/RightPane/RightPane";
import { RequestUserInputModal } from "../components/RequestUserInputModal";
import { requestUserInput } from "../stores/userInput";
import { usePaneStore } from "../stores/tabs";
import { ThreadHeader } from "../components/ThreadHeader";
import { ThemeMenu } from "../components/ThemeMenu";
import { UserMenu } from "../components/UserMenu";
import { Logo } from "../components/Logo";
import { IconPanelLeft, IconPanelRight } from "../components/Icons";
import { t } from "../lib/i18n";

export function AppLayout() {
  const [leftCollapsed, setLeftCollapsed] = useState(false);
  const setIdentity = useAuthStore((s) => s.setIdentity);
  const clear = useAuthStore((s) => s.clear);
  const username = useAuthStore((s) => s.username);
  const role = useAuthStore((s) => s.role);
  const orgName = useAuthStore((s) => s.orgName);
  const paneOpen = usePaneStore((s) => s.open);
  const paneToggle = usePaneStore((s) => s.toggle);
  const [params] = useSearchParams();
  const sessionId = params.get("session") || null;

  useEffect(() => {
    if (!username) {
      apiGet<any>("/auth/me").then((d) => {
        if (d?.username) setIdentity(d);
        else clear();
      }).catch(() => clear());
    }
  }, [username, setIdentity, clear]);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (!(e.ctrlKey || e.metaKey)) return;
      if (e.key === "b") { e.preventDefault(); setLeftCollapsed((v) => !v); }
      if (e.key === "j") { e.preventDefault(); paneToggle(); }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [paneToggle]);

  // Test hook: let e2e scripts trigger the request-user-input modal from
  // outside React without going through a real fetch event. Only attached
  // when running on localhost so it stays inert in production builds.
  useEffect(() => {
    if (typeof window === "undefined") return;
    if (!window.location.hostname.match(/^(localhost|127\.0\.0\.1)$/)) return;
    (window as any).__gepawTestShowUserInput = (req?: any) =>
      requestUserInput(
        req ?? {
          question: t("modal.requestUserInput.title"),
          description: t("modal.requestUserInput.desc"),
          options: [
            { id: "light", label: t("theme.menu.light"), description: "" },
            { id: "dark",  label: t("theme.menu.dark"),  description: "" },
            { id: "auto",  label: t("theme.menu.system"), description: "" },
          ],
          allowFreeText: true,
        },
      );
  }, []);

  function bodyClass() {
    if (leftCollapsed && !paneOpen) return "both-collapsed";
    if (leftCollapsed) return "left-collapsed";
    if (!paneOpen) return "right-collapsed";
    return "";
  }

  return (
    <div className="app-shell">
      <div className="topbar">
        <div className="topbar-left">
          <button
            type="button"
            className="topbar-icon-btn"
            title={t("topbar.toggleLeft")}
            onClick={() => setLeftCollapsed((v) => !v)}
          >
            <IconPanelLeft size={16} />
          </button>
          <span className="topbar-brand">
            <Logo size={18} />
            <span className="topbar-brand-text">{t("brand.name")}</span>
          </span>
        </div>
        <div className="topbar-center">
          <ThreadHeader sessionId={sessionId} orgName={orgName} role={role} />
        </div>
        <div className="topbar-right">
          {orgName && <span className="topbar-org-pill" title={t("topbar.workspace")}>{orgName}</span>}
          <button
            type="button"
            className="topbar-icon-btn"
            title={t("topbar.toggleRight")}
            onClick={paneToggle}
          >
            <IconPanelRight size={16} />
          </button>
          <ThemeMenu />
          <UserMenu />
        </div>
      </div>
      <div className={"app-body " + bodyClass()}>
        {!leftCollapsed ? <LeftPane /> : <div className="left-pane" style={{ width: "var(--left-w-collapsed)" }} />}
        <div className="center-pane"><Outlet /></div>
        <RightPane />
      </div>
      <RequestUserInputModal />
    </div>
  );
}
