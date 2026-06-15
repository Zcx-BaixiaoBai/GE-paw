// Codex-style settings page. Lives under /app/settings so it shares the
// chat shell (left pane + top bar). Hosts the user-facing preferences plus
// all admin sections (LLM, members, channels, crons, skills, MCP, plugins,
// tokens, sessions, wiki, audit) — the user asked for everything in one
// place, so the standalone /admin/* tree was removed.
import { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useSettingsStore } from "../stores/settings";
import { MemoryTree } from "../components/MemoryTree";
import { useAuthStore } from "../stores/auth";
import {
  IconAudit, IconChannels, IconCron, IconLLM, IconMembers,
  IconSessions, IconTokens, IconWiki, IconMonitor, IconPlus,
  IconSettings,
} from "../components/Icons";
import { t } from "../lib/i18n";
import { AdminLLMPage } from "./Admin/LLM";
import { AdminMembersPage } from "./Admin/Members";
import { AdminChannelsPage } from "./Admin/Channels";
import { AdminCronsPage } from "./Admin/Crons";
import { AdminTokensPage } from "./Admin/Tokens";
import { AdminSessionsPage } from "./Admin/Sessions";
import { AdminWikiPage } from "./Admin/Wiki";
import { AdminAuditPage } from "./Admin/Audit";
import { AdminSkillsPage } from "./Admin/Skills";
import { AdminMCPPage } from "./Admin/MCP";
import { AdminPluginsPage } from "./Admin/Plugins";

type TabId = "general" | "llm" | "members" | "channels" | "crons"
  | "tokens" | "sessions" | "wiki" | "skills" | "mcp" | "plugins" | "audit";

type Tab = { id: TabId; label: string; icon: React.ReactNode; adminOnly?: boolean };

const TABS: Tab[] = [
  { id: "general",  label: "通用",     icon: <IconSettings size={14} /> },
  { id: "llm",      label: "LLM 接口", icon: <IconLLM size={14} />,      adminOnly: true },
  { id: "members",  label: "成员",     icon: <IconMembers size={14} />,  adminOnly: true },
  { id: "channels", label: "通道",     icon: <IconChannels size={14} />, adminOnly: true },
  { id: "crons",    label: "定时任务", icon: <IconCron size={14} />,     adminOnly: true },
  { id: "tokens",   label: "Token",    icon: <IconTokens size={14} />,   adminOnly: true },
  { id: "sessions", label: "会话",     icon: <IconSessions size={14} />, adminOnly: true },
  { id: "wiki",     label: "知识库",   icon: <IconWiki size={14} />,     adminOnly: true },
  { id: "skills",   label: "Skill",    icon: <IconMonitor size={14} />,  adminOnly: true },
  { id: "mcp",      label: "MCP",      icon: <IconMonitor size={14} />,  adminOnly: true },
  { id: "plugins",  label: "Plugin",   icon: <IconPlus size={14} />,     adminOnly: true },
  { id: "audit",    label: "审计",     icon: <IconAudit size={14} />,    adminOnly: true },
];

function Section({ title, hint, children }: { title: string; hint?: string; children: React.ReactNode }) {
  return (
    <div className="admin-card">
      <div className="admin-card-title">{title}</div>
      {hint && <div className="admin-hint" style={{ marginBottom: 10 }}>{hint}</div>}
      {children}
    </div>
  );
}

function Toggle({ checked, onChange, label, desc }: {
  checked: boolean; onChange: (v: boolean) => void; label: string; desc?: string;
}) {
  return (
    <label className="settings-row">
      <div className="settings-row-text">
        <div className="settings-row-label">{label}</div>
        {desc && <div className="settings-row-desc">{desc}</div>}
      </div>
      <span
        className={"settings-switch" + (checked ? " on" : "")}
        role="switch"
        aria-checked={checked}
        onClick={() => onChange(!checked)}
        onKeyDown={(e) => {
          if (e.key === " " || e.key === "Enter") { e.preventDefault(); onChange(!checked); }
        }}
        tabIndex={0}
      >
        <span className="settings-switch-knob" />
      </span>
    </label>
  );
}

function GeneralPane() {
  const computerUseEnabled = useSettingsStore((s) => s.computerUseEnabled);
  const setComputerUseEnabled = useSettingsStore((s) => s.setComputerUseEnabled);
  const showRawMessages = useSettingsStore((s) => s.showRawMessages);
  const setShowRawMessages = useSettingsStore((s) => s.setShowRawMessages);
  const autoCompactEnabled = useSettingsStore((s) => s.autoCompactEnabled);
  const setAutoCompactEnabled = useSettingsStore((s) => s.setAutoCompactEnabled);
  const compactThreshold = useSettingsStore((s) => s.compactThreshold);
  const setCompactThreshold = useSettingsStore((s) => s.setCompactThreshold);
  const memoryEnabled = useSettingsStore((s) => s.memoryEnabled);
  const setMemoryEnabled = useSettingsStore((s) => s.setMemoryEnabled);
  return (
    <>
      <Section title={t("settings.computerUse.title")} hint={t("settings.computerUse.desc")}>
        <Toggle
          checked={computerUseEnabled}
          onChange={setComputerUseEnabled}
          label={t("settings.computerUse.label")}
          desc={t("settings.computerUse.detail")}
        />
        {computerUseEnabled && (
          <div className="settings-helper">
            <IconMonitor size={14} />
            <span>{t("settings.computerUse.helper")}</span>
          </div>
        )}
      </Section>
      <Section title={t("settings.chat.title")}>
        <Toggle
          checked={showRawMessages}
          onChange={setShowRawMessages}
          label={t("settings.chat.showRaw")}
          desc={t("settings.chat.showRawDesc")}
        />
      </Section>
      <Section title={t("settings.compact.title")} hint={t("settings.compact.desc")}>
        <Toggle
          checked={autoCompactEnabled}
          onChange={setAutoCompactEnabled}
          label={t("settings.compact.enabled")}
          desc={t("settings.compact.thresholdDesc")}
        />
        <label className="settings-row">
          <div className="settings-row-text">
            <div className="settings-row-label">{t("settings.compact.threshold")}</div>
          </div>
          <input
            className="settings-threshold-input"
            type="number"
            min={500}
            max={1000000}
            step={500}
            value={compactThreshold}
            onChange={(e) => setCompactThreshold(parseInt(e.target.value, 10) || 8000)}
            disabled={!autoCompactEnabled}
            style={{ width: 120, textAlign: "right" }}
          />
        </label>
      </Section>
      <Section title={t("settings.memory.title")} hint={t("settings.memory.desc")}>
        <Toggle
          checked={memoryEnabled}
          onChange={setMemoryEnabled}
          label={t("settings.memory.enabled")}
        />
        {memoryEnabled && <MemoryTree />}
      </Section>
      <Section title={t("settings.about.title")}>
        <div className="admin-hint">{t("settings.about.note")}</div>
      </Section>
    </>
  );
}

export function SettingsPage() {
  const [params, setParams] = useSearchParams();
  const role = useAuthStore((s) => s.role);
  const isAdmin = role === "admin";
  const tabs = useMemo(() => TABS.filter((t) => isAdmin || !t.adminOnly), [isAdmin]);
  const requested = (params.get("tab") as TabId | null) || "general";
  const initial: TabId = tabs.some((t) => t.id === requested) ? requested : "general";
  const [tab, setTab] = useState<TabId>(initial);
  const nav = useNavigate();

  useEffect(() => {
    if (tab !== (params.get("tab") as TabId | null)) {
      const next = new URLSearchParams(params);
      if (tab === "general") next.delete("tab"); else next.set("tab", tab);
      setParams(next, { replace: true });
    }
  }, [tab]);

  useEffect(() => {
    if (!tabs.some((t) => t.id === tab)) setTab("general");
  }, [tabs, tab]);

  function renderPane() {
    switch (tab) {
      case "general":  return <GeneralPane />;
      case "llm":      return <AdminLLMPage />;
      case "members":  return <AdminMembersPage />;
      case "channels": return <AdminChannelsPage />;
      case "crons":    return <AdminCronsPage />;
      case "tokens":   return <AdminTokensPage />;
      case "sessions": return <AdminSessionsPage />;
      case "wiki":     return <AdminWikiPage />;
      case "skills":   return <AdminSkillsPage />;
      case "mcp":      return <AdminMCPPage />;
      case "plugins":  return <AdminPluginsPage />;
      case "audit":    return <AdminAuditPage />;
    }
  }

  return (
    <div className="chat-page settings-page">
      <div className="settings-shell">
        <aside className="settings-side">
          <div className="settings-side-title">设置</div>
          {tabs.map((it) => (
            <button
              key={it.id}
              type="button"
              className={"settings-side-item" + (tab === it.id ? " active" : "")}
              onClick={() => setTab(it.id)}
            >
              <span className="settings-side-icon">{it.icon}</span>
              <span className="settings-side-label">{it.label}</span>
            </button>
          ))}
        </aside>
        <main className="settings-main">
          {tab === "general" ? (
            <>
              <h1 style={{ fontSize: 22, marginBottom: 4 }}>{t("settings.title")}</h1>
              <p className="admin-hint" style={{ marginBottom: 18 }}>{t("settings.sub")}</p>
              {renderPane()}
            </>
          ) : (
            <div className="admin-page">{renderPane()}</div>
          )}
        </main>
      </div>
    </div>
  );
}
