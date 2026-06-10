// Top-right user menu: shows username + role, links to admin (when admin)
// and a sign-out action.
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../stores/auth";
import { IconCheck, IconLogout, IconSettings, IconUser, IconShield } from "./Icons";
import { t } from "../lib/i18n";

export function UserMenu() {
  const username = useAuthStore((s) => s.username);
  const role = useAuthStore((s) => s.role);
  const clear = useAuthStore((s) => s.clear);
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const nav = useNavigate();

  useEffect(() => {
    if (!open) return;
    const onClick = (e: MouseEvent) => {
      if (!ref.current?.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, [open]);

  if (!username) return null;
  const initial = username.slice(0, 1).toUpperCase();
  return (
    <div className="dropdown" ref={ref}>
      <button
        type="button"
        className="topbar-icon-btn user-avatar"
        onClick={() => setOpen((v) => !v)}
        title={username}
        aria-label={t("topbar.menu.profile")}
      >
        <span className="user-avatar-text">{initial}</span>
        {role === "admin" && <span className="user-avatar-badge" title={t("topbar.role.admin")}><IconShield size={9} /></span>}
      </button>
      {open && (
        <div className="dropdown-menu user-menu" role="menu">
          <div className="dropdown-header">
            <div className="user-menu-name">{username}</div>
            <div className="user-menu-role">
              {role === "admin" ? t("topbar.role.admin") : t("topbar.role.member")}
            </div>
          </div>
          <button type="button" className="dropdown-item" onClick={() => { setOpen(false); }}>
            <span className="dropdown-item-icon"><IconUser size={14} /></span>
            <span className="dropdown-item-text">{t("topbar.menu.profile")}</span>
          </button>
          {role === "admin" && (
            <button type="button" className="dropdown-item" onClick={() => { setOpen(false); nav("/admin/llm"); }}>
              <span className="dropdown-item-icon"><IconSettings size={14} /></span>
              <span className="dropdown-item-text">{t("topbar.menu.admin")}</span>
            </button>
          )}
          <div className="dropdown-sep" />
          <button
            type="button"
            className="dropdown-item"
            onClick={() => { setOpen(false); clear(); nav("/login"); }}
          >
            <span className="dropdown-item-icon"><IconLogout size={14} /></span>
            <span className="dropdown-item-text">{t("topbar.menu.signout")}</span>
            <span className="dropdown-item-check"><IconCheck size={12} /></span>
          </button>
        </div>
      )}
    </div>
  );
}
