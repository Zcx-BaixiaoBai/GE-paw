import { useEffect, useState } from "react";
import { apiGet, apiPost, apiDel } from "../../lib/api";
import { IconTrash } from "../../components/Icons";
import { t } from "../../lib/i18n";

type Ch = { id: string; kind: string; name: string; enabled: boolean; status: string; last_seen_at?: string | null };
type StatusResp = { running: string[] };

const KINDS = ["telegram", "feishu", "wecom", "dingtalk", "discord", "matrix", "mattermost", "mqtt", "onebot", "qq", "echo"];

export function AdminChannelsPage() {
  const [list, setList] = useState<Ch[]>([]);
  const [status, setStatus] = useState<StatusResp>({ running: [] });
  const [form, setForm] = useState({ kind: "telegram", name: "", credentials: "{}" });
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    try {
      setList(await apiGet<Ch[]>("/admin/channels"));
      setStatus(await apiGet<StatusResp>("/admin/channels/status"));
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  useEffect(() => { load(); }, []);

  async function add() {
    setErr(null);
    let cred: any;
    try { cred = JSON.parse(form.credentials || "{}"); }
    catch { cred = { raw: form.credentials }; }
    try {
      await apiPost("/admin/channels", { kind: form.kind, name: form.name, credentials: cred, enabled: true });
      setForm({ kind: form.kind, name: "", credentials: "{}" });
      load();
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  async function toggle(c: Ch) {
    await apiPost("/admin/channels/" + c.id, { enabled: !c.enabled });
    load();
  }
  async function remove(c: Ch) {
    if (!confirm(t("admin.common.confirmDelete", { name: c.name }))) return;
    await apiDel("/admin/channels/" + c.id);
    load();
  }
  async function reload() {
    setErr(null);
    try {
      const r = await apiPost<{ started: number; running: string[] }>("/admin/channels/reload", {});
      setStatus({ running: r.running });
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  function isRunning(c: Ch) { return status.running.includes(c.kind + ":" + c.id); }

  return (
    <div className="admin-page">
      <h1>{t("admin.channels.title")}</h1>
      {err && <div className="admin-card admin-err">{err}</div>}

      <div className="admin-card">
        <div className="admin-card-title">{t("admin.channels.addTitle")}</div>
        <div className="admin-form">
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.channels.kind")}</span>
            <select value={form.kind} onChange={(e) => setForm({ ...form, kind: e.target.value })}>
              {KINDS.map((k) => <option key={k} value={k}>{k}</option>)}
            </select>
          </label>
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.channels.name")}</span>
            <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="bot-main" />
          </label>
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.channels.credentials")}</span>
            <textarea value={form.credentials} onChange={(e) => setForm({ ...form, credentials: e.target.value })} rows={4} placeholder='{"token":"..."}' />
          </label>
        </div>
        <div className="admin-form-actions">
          <button className="primary" onClick={add} disabled={!form.name}>{t("admin.common.add")}</button>
          <span className="admin-hint">
            {t("admin.channels.hint")}
          </span>
        </div>
      </div>

      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">
          <span>{t("admin.channels.list")}</span>
          <span className="admin-spacer" />
          <button onClick={reload}>{t("admin.channels.reload")}</button>
          <span className="admin-hint">{t("admin.channels.runningCount", { count: status.running.length })}</span>
        </div>
        {list.length === 0 ? (
          <div className="admin-empty">{t("admin.channels.empty")}</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>{t("admin.channels.kind")}</th>
                <th>{t("admin.channels.name")}</th>
                <th>{t("admin.channels.status")}</th>
                <th>{t("admin.channels.enabled")}</th>
                <th>{t("admin.channels.lastSeen")}</th>
                <th>{t("admin.channels.listener")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {list.map((c) => (
                <tr key={c.id}>
                  <td><code className="code-chip">{c.kind}</code></td>
                  <td><strong>{c.name}</strong></td>
                  <td>{c.status}</td>
                  <td>{c.enabled ? <span className="pill pill-ok">{t("admin.channels.enabled")}</span> : <span className="pill pill-off">{t("common.dash")}</span>}</td>
                  <td>{c.last_seen_at ? new Date(c.last_seen_at).toLocaleString() : t("common.dash")}</td>
                  <td>{isRunning(c) ? <span className="pill pill-ok">{t("admin.channels.running")}</span> : <span className="pill pill-off">{t("admin.channels.stopped")}</span>}</td>
                  <td className="admin-row-action">
                    <button onClick={() => toggle(c)}>{c.enabled ? t("admin.channels.enabled") : t("common.dash")}</button>
                    <button className="icon-btn danger" onClick={() => remove(c)} title={t("admin.common.delete")}><IconTrash size={13} /></button>
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
