// Admin shell: a sidebar of management sections + a scrollable main pane.
// Same visual rhythm as the Codex app shell so admins don't feel they've
// jumped out of the console.
import { NavLink, Outlet } from "react-router-dom";
import {
  IconAudit, IconChannels, IconCron, IconLLM, IconMembers,
  IconSessions, IconTokens, IconWiki,
} from "../../components/Icons";
import { t } from "../../lib/i18n";

type Item = { to: string; label: string; icon: React.ReactNode };

const ITEMS: Item[] = [
  { to: "/admin/llm",      label: t("left.admin.llm"),      icon: <IconLLM size={14} /> },
  { to: "/admin/members",  label: t("left.admin.members"),  icon: <IconMembers size={14} /> },
  { to: "/admin/channels", label: t("left.admin.channels"), icon: <IconChannels size={14} /> },
  { to: "/admin/crons",    label: t("left.admin.crons"),    icon: <IconCron size={14} /> },
  { to: "/admin/tokens",   label: t("left.admin.tokens"),   icon: <IconTokens size={14} /> },
  { to: "/admin/sessions", label: t("left.admin.sessions"), icon: <IconSessions size={14} /> },
  { to: "/admin/wiki",     label: t("left.admin.wiki"),     icon: <IconWiki size={14} /> },
  { to: "/admin/audit",    label: t("left.admin.audit"),    icon: <IconAudit size={14} /> },
];

export function AdminLayout() {
  return (
    <div className="admin-layout">
      <aside className="admin-side">
        <div className="admin-side-title">{t("left.section.admin")}</div>
        {ITEMS.map((it) => (
          <NavLink
            key={it.to}
            to={it.to}
            className={({ isActive }) => "admin-side-item" + (isActive ? " active" : "")}
          >
            <span className="admin-side-icon">{it.icon}</span>
            <span className="admin-side-label">{it.label}</span>
          </NavLink>
        ))}
      </aside>
      <main className="admin-main"><Outlet /></main>
    </div>
  );
}
