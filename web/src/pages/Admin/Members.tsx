import { useEffect, useState } from "react";
import { apiGet, apiPost, apiDel } from "../../lib/api";

type User = { id: string; username: string; display_name: string; email?: string; is_active: boolean };

export function AdminMembersPage() {
  const [list, setList] = useState<User[]>([]);
  const [orgs, setOrgs] = useState<{ id: string; name: string }[]>([]);
  const [form, setForm] = useState({ username: "", display_name: "", password: "", email: "", org_id: "" });

  async function load() {
    const [u, o] = await Promise.all([apiGet<User[]>("/admin/users"), apiGet<{ id: string; name: string }[]>("/admin/orgs")]);
    setList(u); setOrgs(o);
    setForm((f) => ({ ...f, org_id: f.org_id || o[0]?.id || "" }));
  }
  useEffect(() => { load(); }, []);

  async function add() {
    if (!form.username || !form.password || !form.org_id) return;
    await apiPost("/admin/users", { ...form, role: "user" });
    setForm({ username: "", display_name: "", password: "", email: "", org_id: form.org_id });
    load();
  }

  return (
    <div>
      <h1>Members</h1>
      <div className="admin-card">
        <div style={{ fontWeight: 600, marginBottom: 10 }}>Add user</div>
        <div className="row"><label>Username</label><input value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} /></div>
        <div className="row"><label>Display</label><input value={form.display_name} onChange={(e) => setForm({ ...form, display_name: e.target.value })} /></div>
        <div className="row"><label>Email</label><input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></div>
        <div className="row"><label>Password</label><input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></div>
        <div className="row"><label>Org</label>
          <select value={form.org_id} onChange={(e) => setForm({ ...form, org_id: e.target.value })}>
            {orgs.map((o) => <option key={o.id} value={o.id}>{o.name}</option>)}
          </select>
        </div>
        <button className="primary" onClick={add} disabled={!form.username || !form.password}>Add</button>
      </div>
      <div className="admin-card">
        <table className="admin-table">
          <thead><tr><th>Username</th><th>Display</th><th>Email</th><th>Active</th><th></th></tr></thead>
          <tbody>
            {list.length === 0 && <tr><td colSpan={5} style={{ color: "var(--fg-faint)" }}>No users</td></tr>}
            {list.map((u) => (
              <tr key={u.id}>
                <td>{u.username}</td><td>{u.display_name}</td><td>{u.email}</td><td>{u.is_active ? "yes" : "no"}</td>
                <td><button onClick={async () => { await apiDel("/admin/users/" + u.id); load(); }}>Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
