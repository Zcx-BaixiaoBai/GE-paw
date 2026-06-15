import { Outlet, NavLink } from "react-router-dom";
import { t } from "../../lib/i18n";

export function AdminLayout() {
  const links = [
    { to: "/admin/llm", label: t("admin.nav.llm") || "LLM" },
    { to: "/admin/members", label: t("admin.nav.members") || "Members" },
    { to: "/admin/channels", label: t("admin.nav.channels") || "Channels" },
    { to: "/admin/crons", label: t("admin.nav.crons") || "Crons" },
    { to: "/admin/tokens", label: t("admin.nav.tokens") || "Tokens" },
    { to: "/admin/sessions", label: t("admin.nav.sessions") || "Sessions" },
    { to: "/admin/wiki", label: t("admin.nav.wiki") || "Wiki" },
    { to: "/admin/audit", label: t("admin.nav.audit") || "Audit" },
    { to: "/admin/gateway", label: t("admin.nav.gateway") || "\u6a21\u578b\u7f51\u5173" },
  ];

  return (
    <div className="admin-layout">
      <nav className="admin-sidebar">
        {links.map((l) => (
          <NavLink key={l.to} to={l.to} className={({ isActive }) => "admin-nav-link" + (isActive ? " active" : "")}>
            {l.label}
          </NavLink>
        ))}
      </nav>
      <main className="admin-main">
        <Outlet />
      </main>
    </div>
  );
}
