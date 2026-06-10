// Codex-style left pane:
//   - New-session button at the top.
//   - Mode links (Assistant / QnA).
//   - Grouped session list (Today / This week / ...) with per-row actions:
//     rename, pin/unpin, archive/unarchive, delete. Actions live in a hover
//     toolbar (visible on hover or focus) plus a context menu (right click).
//   - Admin links (visible to admins) at the bottom.
//
// All session operations are wired through the session store which talks to
// the real backend (or the mock plugin in dev).
import { useEffect, useMemo, useRef, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { apiGet, apiPost, apiDel } from "../lib/api";
import { useAuthStore } from "../stores/auth";
import { useSessionStore, type Session, type PermissionMode } from "../stores/session";
import {
  IconPlus, IconAssistant, IconQnA,
  IconLLM, IconMembers, IconChannels, IconCron, IconTokens, IconSessions, IconWiki, IconAudit,
  IconPin, IconArchive, IconTrash, IconPencil, IconCheck, IconClose, IconChevronDown,
} from "./Icons";
import { t } from "../lib/i18n";

type ApiSession = {
  id: string;
  title: string;
  status: string;
  pinned: boolean;
  archived?: boolean;
  channel_kind: string | null;
  permission: Session["permission"];
  created_at: string | null;
  last_message_at: string | null;
};

const SECTION_LABELS: Record<string, string> = {
  Today: t("left.section.today"),
  "This week": t("left.section.week"),
  "This month": t("left.section.month"),
  Earlier: t("left.section.earlier"),
  Archived: t("left.session.archived"),
};

function groupBy(iso: string | null | undefined, archived: boolean): string {
  if (archived) return "Archived";
  if (!iso) return "Earlier";
  const d = new Date(iso);
  const now = new Date();
  const diff = (now.getTime() - d.getTime()) / 1000;
  if (diff < 86400) return "Today";
  if (diff < 86400 * 7) return "This week";
  if (diff < 86400 * 30) return "This month";
  return "Earlier";
}

export function LeftPane() {
  const [list, setList] = useState<ApiSession[]>([]);
  const [showArchived, setShowArchived] = useState(false);
  const [busy, setBusy] = useState(false);
  const nav = useNavigate();
  const role = useAuthStore((s) => s.role);
  const upsert = useSessionStore((s) => s.upsert);
  const remove = useSessionStore((s) => s.remove);
  const rename = useSessionStore((s) => s.rename);
  const pin = useSessionStore((s) => s.pin);
  const archive = useSessionStore((s) => s.archive);

  async function load() {
    try {
      const rows = await apiGet<ApiSession[]>("/client/sessions");
      setList(rows);
      for (const r of rows) upsert({ ...r });
    } catch { /* ignore */ }
  }
  useEffect(() => { load(); }, []);

  async function newSession() {
    setBusy(true);
    try {
      const s = await apiPost<ApiSession>("/client/sessions", { title: t("left.newSession") });
      upsert({ ...s });
      nav(`/app/assistant?session=${s.id}`);
      load();
    } finally { setBusy(false); }
  }

  const filtered = useMemo(() => {
    return showArchived ? list : list.filter((s) => !s.archived);
  }, [list, showArchived]);

  const grouped = filtered.reduce<Record<string, ApiSession[]>>((acc, s) => {
    const key = groupBy(s.last_message_at, !!s.archived);
    (acc[key] ||= []).push(s);
    return acc;
  }, {});

  const archivedCount = list.filter((s) => s.archived).length;

  async function onPin(s: ApiSession) {
    const next = !s.pinned;
    setList((prev) => prev.map((x) => (x.id === s.id ? { ...x, pinned: next } : x)));
    try { await pin(s.id, next); } catch { setList((prev) => prev.map((x) => (x.id === s.id ? { ...x, pinned: s.pinned } : x))); }
  }

  async function onArchive(s: ApiSession) {
    const next = !s.archived;
    setList((prev) => prev.map((x) => (x.id === s.id ? { ...x, archived: next } : x)));
    try { await archive(s.id, next); } catch { setList((prev) => prev.map((x) => (x.id === s.id ? { ...x, archived: !!s.archived } : x))); }
  }

  async function onDelete(s: ApiSession) {
    if (!confirm(t("left.session.confirmDelete", { title: s.title || t("left.untitled") }))) return;
    setList((prev) => prev.filter((x) => x.id !== s.id));
    remove(s.id);
    try { await apiDel("/client/sessions/" + s.id); } catch { /* reload on failure */ load(); }
  }

  async function onRename(s: ApiSession, next: string) {
    const title = next.trim().slice(0, 200);
    if (!title || title === s.title) return;
    setList((prev) => prev.map((x) => (x.id === s.id ? { ...x, title } : x)));
    try { await rename(s.id, title); } catch { load(); }
  }

  return (
    <div className="left-pane">
      <div className="left-section left-section-actions">
        <button type="button" className="new-thread-btn" onClick={newSession} disabled={busy} title={t("left.newSession")}>
          <IconPlus size={15} />
          <span>{t("left.newSession")}</span>
        </button>
      </div>

      <div className="left-section">
        <NavLink to="/app/assistant" className={({ isActive }) => "left-item" + (isActive ? " active" : "")}>
          <span className="left-item-icon"><IconAssistant size={15} /></span>
          <span>{t("left.mode.assistant")}</span>
        </NavLink>
        <NavLink to="/app/qna" className={({ isActive }) => "left-item" + (isActive ? " active" : "")}>
          <span className="left-item-icon"><IconQnA size={15} /></span>
          <span>{t("left.mode.qna")}</span>
        </NavLink>
      </div>

      {list.length === 0 && (
        <div className="left-section left-section-empty">
          <div className="left-empty-hint">{t("left.empty.threads")}</div>
        </div>
      )}

      {Object.entries(grouped).map(([k, items]) => (
        <div className="left-section" key={k}>
          <div className="left-section-title">{SECTION_LABELS[k] || k}</div>
          {items.map((s) => (
            <SessionRow
              key={s.id}
              session={s}
              onPin={() => onPin(s)}
              onArchive={() => onArchive(s)}
              onDelete={() => onDelete(s)}
              onRename={(next) => onRename(s, next)}
            />
          ))}
        </div>
      ))}

      {archivedCount > 0 && !showArchived && (
        <div className="left-section">
          <button type="button" className="left-show-archived" onClick={() => setShowArchived(true)}>
            <IconArchive size={13} />
            <span>{t("left.session.showArchived")} ({archivedCount})</span>
          </button>
        </div>
      )}
      {showArchived && (
        <div className="left-section">
          <button type="button" className="left-show-archived" onClick={() => setShowArchived(false)}>
            <IconClose size={13} />
            <span>{t("left.session.archived")} ({archivedCount})</span>
          </button>
        </div>
      )}

      {role === "admin" && (
        <div className="left-section left-section-bottom">
          <div className="left-section-title">{t("left.section.admin")}</div>
          <AdminLink to="/admin/llm"      icon={<IconLLM size={15} />}      label={t("left.admin.llm")} />
          <AdminLink to="/admin/members"  icon={<IconMembers size={15} />}  label={t("left.admin.members")} />
          <AdminLink to="/admin/channels" icon={<IconChannels size={15} />} label={t("left.admin.channels")} />
          <AdminLink to="/admin/crons"    icon={<IconCron size={15} />}     label={t("left.admin.crons")} />
          <AdminLink to="/admin/tokens"   icon={<IconTokens size={15} />}   label={t("left.admin.tokens")} />
          <AdminLink to="/admin/sessions" icon={<IconSessions size={15} />} label={t("left.admin.sessions")} />
          <AdminLink to="/admin/wiki"     icon={<IconWiki size={15} />}     label={t("left.admin.wiki")} />
          <AdminLink to="/admin/audit"    icon={<IconAudit size={15} />}    label={t("left.admin.audit")} highlight />
        </div>
      )}
    </div>
  );
}

function AdminLink({ to, icon, label, highlight }: { to: string; icon: React.ReactNode; label: string; highlight?: boolean }) {
  return (
    <NavLink to={to} className={({ isActive }) => "left-item left-item-admin" + (isActive ? " active" : "") + (highlight ? " highlight" : "")} title={label}>
      <span className="left-item-icon">{icon}</span>
      <span>{label}</span>
    </NavLink>
  );
}

function SessionRow({
  session,
  onPin,
  onArchive,
  onDelete,
  onRename,
}: {
  session: ApiSession;
  onPin: () => void;
  onArchive: () => void;
  onDelete: () => void;
  onRename: (next: string) => void;
}) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(session.title);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => { if (editing) inputRef.current?.select(); }, [editing]);
  useEffect(() => { setDraft(session.title); }, [session.title]);

  function commit() {
    setEditing(false);
    if (draft.trim() && draft.trim() !== session.title) onRename(draft);
    else setDraft(session.title);
  }

  return (
    <div className={"left-row" + (session.pinned ? " pinned" : "") + (session.archived ? " archived" : "") + (editing ? " editing" : "")}>
      <NavLink
        to={`/app/assistant?session=${session.id}`}
        className={({ isActive }) => "left-item left-item-session" + (isActive ? " active" : "")}
        title={session.title}
        onDoubleClick={(e) => { e.preventDefault(); setEditing(true); }}
      >
        {editing ? (
          <input
            ref={inputRef}
            className="left-rename-input"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onBlur={commit}
            onKeyDown={(e) => {
              if (e.key === "Enter") { e.preventDefault(); commit(); }
              if (e.key === "Escape") { e.preventDefault(); setDraft(session.title); setEditing(false); }
              e.stopPropagation();
            }}
            onClick={(e) => e.preventDefault()}
            autoFocus
            maxLength={200}
          />
        ) : (
          <>
            {session.pinned && <span className="left-row-pin"><IconPin size={11} /></span>}
            <span className="left-item-text">{session.title || t("left.untitled")}</span>
            {session.channel_kind && <span className="left-item-channel">{session.channel_kind}</span>}
            {session.archived && <span className="left-item-channel">{t("left.session.archived")}</span>}
          </>
        )}
      </NavLink>
      <div className="left-row-actions">
        <button type="button" className="left-row-action" title={session.pinned ? t("left.session.unpin") : t("left.session.pin")} onClick={onPin}>
          <IconPin size={12} />
        </button>
        <button type="button" className="left-row-action" title={session.archived ? t("left.session.unarchive") : t("left.session.archive")} onClick={onArchive}>
          <IconArchive size={12} />
        </button>
        <button type="button" className="left-row-action" title={t("left.session.rename")} onClick={(e) => { e.preventDefault(); setEditing(true); }}>
          <IconPencil size={12} />
        </button>
        <button type="button" className="left-row-action danger" title={t("left.session.delete")} onClick={onDelete}>
          <IconTrash size={12} />
        </button>
      </div>
    </div>
  );
}