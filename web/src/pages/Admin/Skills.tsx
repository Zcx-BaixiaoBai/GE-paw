// Admin: skills (per-org). The agent runtime only injects skills whose
// row is enabled=True, so this page is the single source of truth for which
// skills are available across every channel and chat session.
import { useEffect, useState } from "react";
import { apiGetArray, apiGet, apiPost, apiPatch, apiDel } from "../../lib/api";
import { IconTrash } from "../../components/Icons";
import { t } from "../../lib/i18n";

type Skill = { id: string; name: string; manifest: Record<string, any>; enabled: boolean };

const EMPTY = { name: "", manifest: "{\n  \"description\": \"\"\n}", enabled: true };

export function AdminSkillsPage() {
  const [list, setList] = useState<Skill[]>([]);
  const [form, setForm] = useState({ ...EMPTY });
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    try { setList(await apiGetArray<Skill>(`/admin/skills`)); }
    catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  useEffect(() => { load(); }, []);

  async function add() {
    setErr(null);
    let manifest: any;
    try { manifest = JSON.parse(form.manifest || "{}"); }
    catch { setErr(t("admin.skills.manifestInvalid")); return; }
    try {
      await apiPost("/admin/skills", { name: form.name, manifest, enabled: form.enabled });
      setForm({ ...EMPTY });
      load();
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  async function toggle(x: Skill) {
    await apiPatch("/admin/skills/" + x.id, { enabled: !x.enabled });
    load();
  }
  async function remove(x: Skill) {
    if (!confirm(t("admin.common.confirmDelete", { name: x.name }))) return;
    await apiDel("/admin/skills/" + x.id);
    load();
  }

  return (
    <div className="admin-page">
      <h1>{t("admin.skills.title")}</h1>
      <p className="admin-hint" style={{ marginBottom: 16 }}>{t("admin.skills.sub")}</p>
      {err && <div className="admin-card admin-err">{err}</div>}

      <div className="admin-card">
        <div className="admin-card-title">{t("admin.skills.addTitle")}</div>
        <div className="admin-form">
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.skills.name")}</span>
            <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="my-skill" />
          </label>
          <label className="admin-field" style={{ alignItems: "flex-start" }}>
            <span className="admin-field-label">{t("admin.skills.manifest")}</span>
            <textarea
              value={form.manifest}
              onChange={(e) => setForm({ ...form, manifest: e.target.value })}
              rows={6}
              style={{ fontFamily: "var(--font-mono)", fontSize: 12 }}
            />
          </label>
          <label className="admin-checkbox">
            <input type="checkbox" checked={form.enabled} onChange={(e) => setForm({ ...form, enabled: e.target.checked })} />
            {t("admin.skills.enabled")}
          </label>
        </div>
        <div className="admin-form-actions">
          <button className="primary" onClick={add} disabled={!form.name}>{t("admin.common.add")}</button>
          <span className="admin-hint">{t("admin.skills.hint")}</span>
        </div>
      </div>

      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">{t("admin.skills.list")} ({list.length})</div>
        {list.length === 0 ? (
          <div className="admin-empty">{t("admin.skills.empty")}</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>{t("admin.skills.name")}</th>
                <th>{t("admin.skills.manifestTitle")}</th>
                <th>{t("admin.skills.enabled")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {list.map((x) => (
                <tr key={x.id}>
                  <td><strong>{x.name}</strong></td>
                  <td className="admin-clamp" title={JSON.stringify(x.manifest)}>
                    <code className="code-chip">{x.manifest?.description || x.manifest?.name || t("common.dash")}</code>
                  </td>
                  <td>
                    <span className={"admin-pill " + (x.enabled ? "admin-pill-on" : "admin-pill-off")}>
                      {x.enabled ? t("admin.skills.enabledOn") : t("admin.skills.enabledOff")}
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




