import { useEffect, useState } from "react";
import { apiGet, apiPost, apiDel } from "../../lib/api";
import { IconTrash } from "../../components/Icons";
import { t } from "../../lib/i18n";

type User = { id: string; username: string; display_name?: string; email?: string; is_active: boolean; org_id?: string; role?: string };

export function AdminMembersPage() {
  const [list, setList] = useState<User[]>([]);
  const [form, setForm] = useState({ username: "", display_name: "", email: "", password: "" });
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    try { setList(await apiGet<User[]>("/admin/members")); }
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

  return (
    <div className="admin-page">
      <h1>{t("admin.members.title")}</h1>
      {err && <div className="admin-card admin-err">{err}</div>}

      <div className="admin-card">
        <div className="admin-card-title">{t("admin.members.addTitle")}</div>
        <div className="admin-form">
          <Field label={t("admin.members.username")}><input value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} /></Field>
          <Field label={t("admin.members.display")}><input value={form.display_name} onChange={(e) => setForm({ ...form, display_name: e.target.value })} /></Field>
          <Field label={t("admin.members.email")}><input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></Field>
          <Field label={t("admin.members.password")}><input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></Field>
        </div>
        <div className="admin-form-actions">
          <button className="primary" onClick={add} disabled={!form.username || !form.password}>{t("admin.common.add")}</button>
        </div>
      </div>

      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">{t("admin.members.title")} ({list.length})</div>
        {list.length === 0 ? (
          <div className="admin-empty">{t("admin.members.empty")}</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>{t("admin.members.username")}</th>
                <th>{t("admin.members.display")}</th>
                <th>{t("admin.members.email")}</th>
                <th>{t("admin.members.org")}</th>
                <th>{t("admin.members.active")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {list.map((u) => (
                <tr key={u.id}>
                  <td><strong>{u.username}</strong>{u.role === "admin" && <span className="pill pill-ok" style={{ marginLeft: 6 }}>admin</span>}</td>
                  <td>{u.display_name || t("common.dash")}</td>
                  <td className="admin-mono">{u.email || t("common.dash")}</td>
                  <td>{u.org_id || t("common.dash")}</td>
                  <td>{u.is_active ? <span className="pill pill-ok">{t("admin.members.active")}</span> : <span className="pill pill-off">{t("common.dash")}</span>}</td>
                  <td className="admin-row-action">
                    <button onClick={() => toggle(u)}>{u.is_active ? t("admin.common.cancel") : t("admin.members.active")}</button>
                    <button className="icon-btn danger" onClick={() => remove(u)} title={t("admin.common.delete")}><IconTrash size={13} /></button>
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
