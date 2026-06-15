// Admin: plugins (per-org). Plugins are third-party integrations that the
// agent can call alongside skills/MCP. The form captures a JSON manifest so
// admins can configure them in the same unified console.
import { useEffect, useState } from "react";
import { apiGetArray, apiGet, apiPost, apiPatch, apiDel } from "../../lib/api";
import { IconTrash } from "../../components/Icons";
import { t } from "../../lib/i18n";

type Plugin = { id: string; name: string; manifest: Record<string, any>; enabled: boolean };

const EMPTY = { name: "", manifest: "{\n  \"entry\": \"\"\n}", enabled: true };

export function AdminPluginsPage() {
  const [list, setList] = useState<Plugin[]>([]);
  const [form, setForm] = useState({ ...EMPTY });
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    try { setList(await apiGetArray<Plugin>(`/admin/plugins`)); }
    catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  useEffect(() => { load(); }, []);

  async function add() {
    setErr(null);
    let manifest: any;
    try { manifest = JSON.parse(form.manifest || "{}"); }
    catch { setErr(t("admin.plugins.manifestInvalid")); return; }
    try {
      await apiPost("/admin/plugins", { name: form.name, manifest, enabled: form.enabled });
      setForm({ ...EMPTY });
      load();
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  async function toggle(x: Plugin) {
    await apiPatch("/admin/plugins/" + x.id, { enabled: !x.enabled });
    load();
  }
  async function remove(x: Plugin) {
    if (!confirm(t("admin.common.confirmDelete", { name: x.name }))) return;
    await apiDel("/admin/plugins/" + x.id);
    load();
  }

  return (
    <div className="admin-page">
      <h1>{t("admin.plugins.title")}</h1>
      <p className="admin-hint" style={{ marginBottom: 16 }}>{t("admin.plugins.sub")}</p>
      {err && <div className="admin-card admin-err">{err}</div>}

      <div className="admin-card">
        <div className="admin-card-title">{t("admin.plugins.addTitle")}</div>
        <div className="admin-form">
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.plugins.name")}</span>
            <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="my-plugin" />
          </label>
          <label className="admin-field" style={{ alignItems: "flex-start" }}>
            <span className="admin-field-label">{t("admin.plugins.manifest")}</span>
            <textarea
              value={form.manifest}
              onChange={(e) => setForm({ ...form, manifest: e.target.value })}
              rows={6}
              style={{ fontFamily: "var(--font-mono)", fontSize: 12 }}
            />
          </label>
          <label className="admin-checkbox">
            <input type="checkbox" checked={form.enabled} onChange={(e) => setForm({ ...form, enabled: e.target.checked })} />
            {t("admin.plugins.enabled")}
          </label>
        </div>
        <div className="admin-form-actions">
          <button className="primary" onClick={add} disabled={!form.name}>{t("admin.common.add")}</button>
          <span className="admin-hint">{t("admin.plugins.hint")}</span>
        </div>
      </div>

      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">{t("admin.plugins.list")} ({list.length})</div>
        {list.length === 0 ? (
          <div className="admin-empty">{t("admin.plugins.empty")}</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>{t("admin.plugins.name")}</th>
                <th>{t("admin.plugins.manifestTitle")}</th>
                <th>{t("admin.plugins.enabled")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {list.map((x) => (
                <tr key={x.id}>
                  <td><strong>{x.name}</strong></td>
                  <td className="admin-clamp" title={JSON.stringify(x.manifest)}>
                    <code className="code-chip">{x.manifest?.entry || x.manifest?.name || t("common.dash")}</code>
                  </td>
                  <td>
                    <span className={"admin-pill " + (x.enabled ? "admin-pill-on" : "admin-pill-off")}>
                      {x.enabled ? t("admin.plugins.enabledOn") : t("admin.plugins.enabledOff")}
                    </span>
                  </td>
                  <td className="admin-row-action">
                    <button onClick={() => toggle(x)}>{x.enabled ? t("admin.common.disable") : t("admin.common.enable")}</button>
                    <button className="icon-btn danger" onClick={() => remove(x)} title={t("admin.common.delete")}><IconTrash size={13} /></button>
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




