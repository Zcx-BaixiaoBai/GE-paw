// Codex-style top bar centre piece. Shows the current session title, lets
// the user rename / pin / archive via a menu. When no session is selected
// we render the brand instead.
import { useEffect, useRef, useState } from "react";
import { useSessionStore } from "../stores/session";
import { IconArchive, IconCheck, IconChevronDown, IconPencil, IconPin, IconShield } from "./Icons";
import { t } from "../lib/i18n";

type Props = {
  sessionId: string | null;
  orgName: string | null;
  role: "admin" | "user" | null;
};

export function ThreadHeader({ sessionId, orgName, role }: Props) {
  const session = useSessionStore((s) => (sessionId ? s.byId[sessionId] : null));
  const rename = useSessionStore((s) => s.rename);
  const pin = useSessionStore((s) => s.pin);
  const archive = useSessionStore((s) => s.archive);
  const load = useSessionStore((s) => s.load);
  const [open, setOpen] = useState(false);
  const [opensUp, setOpensUp] = useState(false);
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => { if (sessionId) load(sessionId).catch(() => null); }, [sessionId, load]);
  useEffect(() => { if (session) setDraft(session.title); }, [session?.title]);

  useEffect(() => {
    if (!open) return;
    const onClick = (e: MouseEvent) => {
      if (!menuRef.current?.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, [open]);

  // Flip the thread-header dropdown upward when the title is near
  // the bottom of the viewport so the menu never spills off-screen.
  useEffect(() => {
    if (!open || !menuRef.current) return;
    const rect = menuRef.current.getBoundingClientRect();
    const spaceBelow = window.innerHeight - rect.bottom;
    setOpensUp(spaceBelow < 220);
  }, [open]);

  useEffect(() => {
    if (editing) inputRef.current?.select();
  }, [editing]);

  async function commitRename() {
    if (!session) return;
    const title = draft.trim();
    if (!title) { setEditing(false); return; }
    try {
      await rename(session.id, title.slice(0, 200));
      setEditing(false);
    } catch (e: any) {
      setErr(e?.message || "rename failed");
      setEditing(false);
    }
  }

  if (!sessionId) {
    return (
      <div className="thread-header empty">
        <span className="thread-title">{t("brand.name")}</span>
        <span className="thread-meta">{t("topbar.workspace")}: {orgName || t("left.untitled")}</span>
      </div>
    );
  }

  const title = session?.title || t("topbar.untitledThread");

  return (
    <div className={"thread-header" + (session?.pinned ? " pinned" : "")}>
      {editing ? (
        <input
          ref={inputRef}
          className="thread-rename-input"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") { e.preventDefault(); commitRename(); }
            if (e.key === "Escape") { e.preventDefault(); setEditing(false); setDraft(session?.title || ""); }
          }}
          onBlur={commitRename}
          maxLength={200}
          placeholder={t("topbar.rename.placeholder")}
        />
      ) : (
        <button type="button" className="thread-title-btn" onClick={() => setOpen((v) => !v)} title={title}>
          <span className="thread-title">{title}</span>
          <span className="thread-caret"><IconChevronDown size={12} /></span>
        </button>
      )}
      {role === "admin" && (
        <span className="thread-role-pill"><IconShield size={10} />{t("topbar.role.admin")}</span>
      )}
      {session?.permission && (
        <span className={"thread-perm-pill thread-perm-" + session.permission}>{t("perm." + session.permission as any)}</span>
      )}
      {err && <span className="thread-err">{err}</span>}

      <div className="dropdown" ref={menuRef}>
        {!editing && (
          <button type="button" className="topbar-icon-btn ghost" onClick={() => setOpen((v) => !v)} title={t("topbar.toggleTheme")} style={{ display: "none" }} />
        )}
        {open && (
          <div className={"dropdown-menu thread-menu" + (opensUp ? " opens-up" : "")} role="menu">
            <button type="button" className="dropdown-item" onClick={() => { setOpen(false); setEditing(true); }}>
              <span className="dropdown-item-icon"><IconPencil size={14} /></span>
              <span className="dropdown-item-text">{t("topbar.rename")}</span>
            </button>
            <button type="button" className="dropdown-item" onClick={async () => { if (!session) return; setOpen(false); try { await pin(session.id, !session.pinned); } catch { /* ignore */ } }}>
              <span className="dropdown-item-icon"><IconPin size={14} /></span>
              <span className="dropdown-item-text">{session?.pinned ? t("topbar.unpin") : t("topbar.pin")}</span>
            </button>
            <button
              type="button"
              className="dropdown-item"
              onClick={async () => {
                if (!session) return;
                setOpen(false);
                try { await archive(session.id, !session.archived); } catch { /* ignore */ }
              }}
            >
              <span className="dropdown-item-icon"><IconArchive size={14} /></span>
              <span className="dropdown-item-text">{session?.archived ? t("topbar.unarchive") : t("topbar.archive")}</span>
            </button>
            {err && <div className="dropdown-sep" />}
            {err && <div className="dropdown-item err"><span className="dropdown-item-text">{err}</span><span className="dropdown-item-check"><IconCheck size={12} /></span></div>}
          </div>
        )}
      </div>
    </div>
  );
}








