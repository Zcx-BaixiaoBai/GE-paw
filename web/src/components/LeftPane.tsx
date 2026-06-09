import { useEffect, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { apiGet, apiPost } from "../lib/api";
import { useAuthStore } from "../stores/auth";

type Session = { id: string; title: string; pinned?: boolean; channel_kind?: string | null; last_message_at?: string };

export function LeftPane() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const nav = useNavigate();
  const role = useAuthStore((s) => s.role);

  async function load() {
    try { setSessions(await apiGet<Session[]>("/client/sessions")); } catch {}
  }
  useEffect(() => { load(); }, []);

  async function newSession() {
    const s = await apiPost<any>("/client/sessions", { title: "New session" });
    nav(`/app/assistant?session=${s.id}`);
    load();
  }

  const grouped = sessions.reduce<Record<string, Session[]>>((acc, s) => {
    const key = groupBy(s.last_message_at);
    (acc[key] ||= []).push(s);
    return acc;
  }, {});

  return (
    <div className="left-pane">
      <div className="section">
        <button className="primary" style={{ width: "100%" }} onClick={newSession}>+ New session</button>
      </div>
      <div className="section">
        <div className="section-title">Modes</div>
        <NavLink to="/app/assistant" className={({ isActive }) => "item" + (isActive ? " active" : "")}>
          <span>{"💬"}</span><span>Assistant</span>
        </NavLink>
        <NavLink to="/app/qna" className={({ isActive }) => "item" + (isActive ? " active" : "")}>
          <span>{"🔍"}</span><span>Q&amp;A</span>
        </NavLink>
      </div>
      {Object.entries(grouped).map(([k, list]) => (
        <div className="section" key={k}>
          <div className="section-title">{k}</div>
          {list.map((s) => (
            <NavLink key={s.id} to={`/app/assistant?session=${s.id}`}
              className={({ isActive }) => "item" + (isActive ? " active" : "") + (s.pinned ? " pinned" : "")}>
              <span>{s.title || "Untitled"}</span>
              {s.channel_kind && <span className="channel">{s.channel_kind}</span>}
            </NavLink>
          ))}
        </div>
      ))}
      {role === "admin" && (
        <div className="section">
          <div className="section-title">Admin</div>
          <NavLink to="/admin/llm" className={({ isActive }) => "item" + (isActive ? " active" : "")}><span>{"🧠"}</span><span>LLM endpoints</span></NavLink>
          <NavLink to="/admin/members" className={({ isActive }) => "item" + (isActive ? " active" : "")}><span>{"👥"}</span><span>Members</span></NavLink>
          <NavLink to="/admin/channels" className={({ isActive }) => "item" + (isActive ? " active" : "")}><span>{"📡"}</span><span>Channels</span></NavLink>
          <NavLink to="/admin/crons" className={({ isActive }) => "item" + (isActive ? " active" : "")}><span>{"⏰"}</span><span>Cron jobs</span></NavLink>
          <NavLink to="/admin/tokens" className={({ isActive }) => "item" + (isActive ? " active" : "")}><span>{"💰"}</span><span>Tokens</span></NavLink>
          <NavLink to="/admin/sessions" className={({ isActive }) => "item" + (isActive ? " active" : "")}><span>{"📜"}</span><span>Sessions</span></NavLink>
          <NavLink to="/admin/wiki" className={({ isActive }) => "item" + (isActive ? " active" : "")}><span>{"📖"}</span><span>Wiki</span></NavLink>
          <NavLink to="/admin/audit" className={({ isActive }) => "item" + (isActive ? " active" : "")}><span>{"🔍"}</span><span>Audit</span></NavLink>
        </div>
      )}
    </div>
  );
}

function groupBy(iso?: string): string {
  if (!iso) return "Earlier";
  const d = new Date(iso);
  const now = new Date();
  const diff = (now.getTime() - d.getTime()) / 1000;
  if (diff < 86400) return "Today";
  if (diff < 86400 * 7) return "This week";
  if (diff < 86400 * 30) return "This month";
  return "Earlier";
}
