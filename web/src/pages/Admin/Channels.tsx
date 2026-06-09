import { useEffect, useState } from "react";
import { apiGet, apiPost, apiDel, apiPost as _p } from "../../lib/api";

type Ch = { id: string; kind: string; name: string; enabled: boolean; status: string; last_seen_at?: string | null };
type StatusResp = { running: string[] };

const KINDS = ["telegram","feishu","wecom","dingtalk","discord","matrix","mattermost","mqtt","onebot","qq","echo"];

export function AdminChannelsPage() {
  const [list, setList] = useState<Ch[]>([]);
  const [status, setStatus] = useState<StatusResp>({ running: [] });
  const [form, setForm] = useState({ kind: "telegram", name: "", credentials: "{}" });
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    try {
      setList(await apiGet<Ch[]>("/admin/channels"));
      setStatus(await apiGet<StatusResp>("/admin/channels/status"));
    } catch (e: any) { setErr(e?.message || "load failed"); }
  }
  useEffect(() => { load(); }, []);

  async function add() {
    setErr(null);
    let cred: any; try { cred = JSON.parse(form.credentials || "{}"); } catch { cred = { raw: form.credentials }; }
    try {
      await apiPost("/admin/channels", { kind: form.kind, name: form.name, credentials: cred, enabled: true });
      setForm({ kind: form.kind, name: "", credentials: "{}" });
      load();
    } catch (e: any) { setErr(e?.message || "create failed"); }
  }
  async function toggle(c: Ch) {
    await _p("/admin/channels/" + c.id, { enabled: !c.enabled });
    load();
  }
  async function remove(c: Ch) {
    if (!confirm("Delete channel " + c.name + "?")) return;
    await apiDel("/admin/channels/" + c.id);
    load();
  }
  async function reload() {
    setErr(null);
    try {
      const r = await _p<{ started: number; running: string[] }>("/admin/channels/reload", {});
      setStatus({ running: r.running });
    } catch (e: any) { setErr(e?.message || "reload failed"); }
  }
  function isRunning(c: Ch) { return status.running.includes(c.kind + ":" + c.id); }

  return (
    <div>
      <h1>Channels</h1>
      {err && <div className="admin-card" style={{ color: "var(--danger)" }}>{err}</div>}

      <div className="admin-card">
        <div style={{ fontWeight: 600, marginBottom: 10 }}>Add channel</div>
        <div className="row">
          <label>Kind</label>
          <select value={form.kind} onChange={(e) => setForm({ ...form, kind: e.target.value })}>
            {KINDS.map((k) => <option key={k} value={k}>{k}</option>)}
          </select>
        </div>
        <div className="row"><label>Name</label><input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="bot-main" /></div>
        <div className="row"><label>Credentials (JSON)</label><textarea value={form.credentials} onChange={(e) => setForm({ ...form, credentials: e.target.value })} rows={4} placeholder='{"token":"..."}' /></div>
        <button className="primary" onClick={add} disabled={!form.name}>Add</button>
        <span style={{ marginLeft: 8, fontSize: 11, color: "var(--fg-muted)" }}>Tip: use kind <code>echo</code> for in-process testing via <code>POST /api/webhook/echo</code>.</span>
      </div>

      <div className="admin-card">
        <div style={{ display: "flex", alignItems: "center", marginBottom: 10 }}>
          <div style={{ fontWeight: 600 }}>Existing channels</div>
          <span style={{ flex: 1 }} />
          <button onClick={reload}>Reload adapters</button>
          <span style={{ marginLeft: 8, fontSize: 11, color: "var(--fg-muted)" }}>running: {status.running.length}</span>
        </div>
        <table className="admin-table">
          <thead><tr><th>Kind</th><th>Name</th><th>Status</th><th>Enabled</th><th>Last seen</th><th>Listener</th><th></th></tr></thead>
          <tbody>
            {list.length === 0 && <tr><td colSpan={7} style={{ color: "var(--fg-faint)" }}>No channels</td></tr>}
            {list.map((c) => (
              <tr key={c.id}>
                <td><code>{c.kind}</code></td>
                <td><b>{c.name}</b></td>
                <td>{c.status}</td>
                <td>{c.enabled ? "yes" : "no"}</td>
                <td>{c.last_seen_at ? new Date(c.last_seen_at).toLocaleString() : "-"}</td>
                <td>{isRunning(c) ? <span style={{ color: "var(--ok)" }}>running</span> : <span style={{ color: "var(--fg-muted)" }}>stopped</span>}</td>
                <td style={{ whiteSpace: "nowrap" }}>
                  <button onClick={() => toggle(c)}>{c.enabled ? "Disable" : "Enable"}</button>
                  <button onClick={() => remove(c)} style={{ marginLeft: 4, color: "var(--danger)" }}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
