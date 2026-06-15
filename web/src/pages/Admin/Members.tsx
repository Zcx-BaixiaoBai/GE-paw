import { useEffect, useState, useMemo } from "react";
import { apiGetArray, apiGet, apiPost, apiDel } from "../../lib/api";
import { IconTrash, IconCopy, IconRefresh } from "../../components/Icons";
import { t } from "../../lib/i18n";

type User = { 
  id: string; 
  username: string; 
  display_name?: string; 
  email?: string; 
  is_active: boolean; 
  org_id?: string; 
  role?: string;
  created_at?: string;
  last_active_at?: string;
};

export function AdminMembersPage() {
  const [list, setList] = useState<User[]>([]);
  const [form, setForm] = useState({ username: "", display_name: "", email: "", password: "" });
  const [err, setErr] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [inviteCode, setInviteCode] = useState<string | null>(null);
  const [inviteLoading, setInviteLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const filteredList = useMemo(() => {
    if (!search) return list;
    const searchLower = search.toLowerCase();
    return list.filter(u => 
      u.username.toLowerCase().includes(searchLower) ||
      u.display_name?.toLowerCase().includes(searchLower) ||
      u.email?.toLowerCase().includes(searchLower)
    );
  }, [list, search]);

  async function load() {
    try { setList(await apiGetArray<User>(`/admin/members`)); }
    catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  useEffect(() => { load(); }, []);

  async function add() {
    setErr(null);
    try {
      await apiPost("/admin/members", form);
      setForm({ username: "", display_name: "", email: "", password: "" });
      load();
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  async function remove(u: User) {
    if (!confirm(t("admin.common.confirmDelete", { name: u.username }))) return;
    try { await apiDel("/admin/members/" + u.id); load(); }
    catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  async function toggle(u: User) {
    try { await apiPost("/admin/members/" + u.id, { is_active: !u.is_active }); load(); }
    catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  async function updateRole(u: User, role: string) {
    try { await apiPost("/admin/members/" + u.id, { role }); load(); }
    catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  async function generateInviteCode() {
    setInviteLoading(true);
    try {
      const code = await apiGet<{ code: string }>("/admin/invite-code");
      setInviteCode(code.code);
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
    finally { setInviteLoading(false); }
  }
  async function copyInviteCode() {
    if (!inviteCode) return;
    try {
      await navigator.clipboard.writeText(inviteCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }

  function formatDate(dateString?: string) {
    if (!dateString) return t("common.dash");
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    } catch {
      return dateString;
    }
  }

  function formatDateTime(dateString?: string) {
    if (!dateString) return t("common.dash");
    try {
      const date = new Date(dateString);
      return date.toLocaleString();
    } catch {
      return dateString;
    }
  }

  return (
    <div className="admin-page">
      <h1>{t("admin.members.title")}</h1>
      {err && <div className="admin-card admin-err">{err}</div>}

      {/* Invite Code Section */}
      <div className="admin-card">
        <div className="admin-card-title">{t("admin.members.inviteCode")}</div>
        <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
          <div className="admin-input font-mono" style={{ flex: 1, padding: "8px 12px", fontSize: "14px", background: "var(--bg)" }}>
            {inviteCode || t("admin.members.generateInvite")}
          </div>
          <button className="btn-ghost" onClick={copyInviteCode} disabled={!inviteCode}>
            <IconCopy size={14} />
            {copied ? t("common.copied") : t("common.copy")}
          </button>
          <button className="btn-primary" onClick={generateInviteCode} disabled={inviteLoading}>
            <IconRefresh size={14} className={inviteLoading ? "spin" : ""} />
            {t("admin.members.generate")}
          </button>
        </div>
      </div>

      {/* Add Member Section */}
      <div className="admin-card">
        <div className="admin-card-title">{t("admin.members.addTitle")}</div>
        <div className="admin-form">
          <Field label={t("admin.members.username")}><input value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} /></Field>
          <Field label={t("admin.members.display")}><input value={form.display_name} onChange={(e) => setForm({ ...form, display_name: e.target.value })} /></Field>
          <Field label={t("admin.members.email")}><input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></Field>
          <Field label={t("admin.members.password")}><input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></Field>
        </div>
        <div className="admin-form-actions">
          <button className="btn-primary" onClick={add} disabled={!form.username || !form.password}>{t("admin.common.add")}</button>
        </div>
      </div>

      {/* Members List */}
      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">
          <span>{t("admin.members.title")} ({filteredList.length})</span>
          <div className="admin-search">
            <input 
              type="text" 
              placeholder={t("admin.members.search")} 
              value={search} 
              onChange={(e) => setSearch(e.target.value)}
              style={{ marginLeft: "auto", width: "200px", padding: "6px 12px", fontSize: "12px" }}
            />
          </div>
        </div>
        {filteredList.length === 0 ? (
          <div className="admin-empty">{t("admin.members.empty")}</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>{t("admin.members.username")}</th>
                <th>{t("admin.members.display")}</th>
                <th>{t("admin.members.email")}</th>
                <th>{t("admin.members.role")}</th>
                <th>{t("admin.members.createdAt")}</th>
                <th>{t("admin.members.lastActive")}</th>
                <th>{t("admin.members.active")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {filteredList.map((u) => (
                <tr key={u.id}>
                  <td><strong>{u.username}</strong></td>
                  <td>{u.display_name || t("common.dash")}</td>
                  <td className="admin-mono text-muted">{u.email || t("common.dash")}</td>
                  <td>
                    <select 
                      value={u.role || "user"} 
                      onChange={(e) => updateRole(u, e.target.value)}
                      className="admin-select-sm"
                    >
                      <option value="user">User</option>
                      <option value="admin">Admin</option>
                    </select>
                  </td>
                  <td className="admin-mono text-muted">{formatDate(u.created_at)}</td>
                  <td className="admin-mono text-muted">{formatDateTime(u.last_active_at)}</td>
                  <td>
                    {u.is_active ? (
                      <span className="pill pill-ok">Active</span>
                    ) : (
                      <span className="pill pill-off">Inactive</span>
                    )}
                  </td>
                  <td className="admin-row-action">
                    <button className="btn-ghost" onClick={() => toggle(u)}>
                      {u.is_active ? t("admin.common.disable") : t("admin.common.enable")}
                    </button>
                    <button className="btn-ghost btn-danger-ghost" onClick={() => remove(u)} title={t("admin.common.delete")}>
                      <IconTrash size={13} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="admin-field">
      <span className="admin-field-label">{label}</span>
      {children}
    </label>
  );
}
