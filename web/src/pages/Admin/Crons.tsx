import { useEffect, useState } from "react";
import { apiGet, apiPost, apiDel } from "../../lib/api";
import { IconTrash } from "../../components/Icons";
import { t } from "../../lib/i18n";

type Cron = {
  id: string; name: string; schedule_cron: string; prompt_template: string;
  enabled: boolean; failure_count: number; last_status?: string; last_run_at?: string;
  next_run_at?: string;
};

export function AdminCronsPage() {
  const [list, setList] = useState<Cron[]>([]);
  const [form, setForm] = useState({
    name: "", schedule_cron: "*/5 * * * *",
    prompt_template: "",
  });
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    try { setList(await apiGet<Cron[]>("/admin/crons")); }
    catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  useEffect(() => { load(); }, []);

  async function add() {
    setErr(null);
    try {
      await apiPost("/admin/crons", form);
      setForm({ ...form, name: "" });
      load();
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  async function toggle(c: Cron) {
    await apiPost("/admin/crons/" + c.id, { enabled: !c.enabled });
    load();
  }
  async function remove(c: Cron) {
    if (!confirm(t("admin.common.confirmDelete", { name: c.name }))) return;
    await apiDel("/admin/crons/" + c.id);
    load();
  }

  return (
    <div className="admin-page">
      <h1>{t("admin.crons.title")}</h1>
      {err && <div className="admin-card admin-err">{err}</div>}

      <div className="admin-card">
        <div className="admin-card-title">{t("admin.crons.addTitle")}</div>
        <div className="admin-form">
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.crons.name")}</span>
            <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="daily-status" />
          </label>
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.crons.schedule")}</span>
            <input value={form.schedule_cron} onChange={(e) => setForm({ ...form, schedule_cron: e.target.value })} placeholder="*/5 * * * *" />
          </label>
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.crons.prompt")}</span>
            <textarea value={form.prompt_template} onChange={(e) => setForm({ ...form, prompt_template: e.target.value })} rows={3} />
          </label>
        </div>
        <div className="admin-form-actions">
          <button className="primary" onClick={add} disabled={!form.name || !form.schedule_cron}>{t("admin.common.add")}</button>
          <span className="admin-hint">{t("admin.crons.hint")}</span>
        </div>
      </div>

      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">{t("admin.crons.title")} ({list.length})</div>
        {list.length === 0 ? (
          <div className="admin-empty">{t("admin.crons.empty")}</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>{t("admin.crons.name")}</th>
                <th>{t("admin.crons.schedule")}</th>
                <th>{t("admin.crons.prompt")}</th>
                <th>{t("admin.crons.lastStatus")}</th>
                <th>{t("admin.crons.lastRun")}</th>
                <th>{t("admin.crons.nextRun")}</th>
                <th>{t("admin.crons.failures")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {list.map((c) => (
                <tr key={c.id}>
                  <td><strong>{c.name}</strong></td>
                  <td><code className="code-chip">{c.schedule_cron}</code></td>
                  <td className="admin-clamp" title={c.prompt_template}>{c.prompt_template || t("common.dash")}</td>
                  <td>{c.last_status || t("common.dash")}</td>
                  <td>{c.last_run_at ? new Date(c.last_run_at).toLocaleString() : t("common.dash")}</td>
                  <td>{c.next_run_at ? new Date(c.next_run_at).toLocaleString() : t("common.dash")}</td>
                  <td>{c.failure_count > 0 ? <span className="pill pill-warn">{c.failure_count}</span> : c.failure_count}</td>
                  <td className="admin-row-action">
                    <button onClick={() => toggle(c)}>{c.enabled ? t("admin.crons.disable") : t("admin.crons.enable")}</button>
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
