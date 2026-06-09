import { useEffect, useState } from "react";
import { apiGet, apiPost, apiDel } from "../../lib/api";

type S = {
  id: string; title: string; status: string; pinned: boolean; archived: boolean;
  channel_kind?: string | null; channel_account_id?: string | null;
  username?: string; user_id?: string; message_count: number;
  created_at?: string; last_message_at?: string | null;
};

export function AdminSessionsPage() {
  const [list, setList] = useState<S[]>([]);
  const [q, setQ] = useState("");
  const [channel, setChannel] = useState("");
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    try {
      const params = new URLSearchParams();
      if (q) params.set("q", q);
      if (channel) params.set("channel_kind", channel);
      params.set("limit", "200");
      setList(await apiGet<S[]>("/admin/sessions?" + params.toString()));
    } catch (e: any) { setErr(e?.message || "load failed"); }
  }
  useEffect(() => { load(); }, []);
  // re-load on filter changes
  useEffect(() => { load(); }, [q, channel]);

  async function archive(s: S) {
    try { await apiPost("/admin/sessions/" + s.id + "/archive", {}); load(); }
    catch (e: any) { setErr(e?.message || "archive failed"); }
  }
  async function remove(s: S) {
    if (!confirm("Delete session '" + s.title + "' and all its messages?")) return;
    try { await apiDel("/admin/sessions/" + s.id); load(); }
    catch (e: any) { setErr(e?.message || "delete failed"); }
  }

  const channels = Array.from(new Set(list.map((s) => s.channel_kind).filter(Boolean) as string[]));

  return (
    <div>
      <h1>Sessions</h1>
      {err && <div className="admin-card" style={{ color: "var(--danger)" }}>{err}</div>}
      <div className="admin-card" style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Filter by title" style={{ width: 280 }} />
        <select value={channel} onChange={(e) => setChannel(e.target.value)}>
          <option value="">All channels</option>
          {channels.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
        <span style={{ flex: 1 }} />
        <span className="kbd">{list.length} sessions</span>
      </div>
      <div className="admin-card">
        <table className="admin-table">
          <thead><tr>
            <th>Title</th><th>User</th><th>Channel</th><th>Messages</th><th>Status</th><th>Last activity</th><th></th>
          </tr></thead>
          <tbody>
            {list.length === 0 && <tr><td colSpan={7} style={{ color: "var(--fg-faint)" }}>No sessions</td></tr>}
            {list.map((s) => (
              <tr key={s.id}>
                <td><b>{s.title}</b>{s.archived && <span className="kbd" style={{ marginLeft: 6 }}>archived</span>}</td>
                <td>{s.username || "-"}</td>
                <td>{s.channel_kind || <span style={{ color: "var(--fg-muted)" }}>web</span>}</td>
                <td>{s.message_count}</td>
                <td>{s.status}</td>
                <td>{s.last_message_at ? new Date(s.last_message_at).toLocaleString() : "-"}</td>
                <td style={{ whiteSpace: "nowrap" }}>
                  {!s.archived && <button onClick={() => archive(s)}>Archive</button>}
                  <button onClick={() => remove(s)} style={{ marginLeft: 4, color: "var(--danger)" }}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
