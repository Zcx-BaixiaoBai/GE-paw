// Admin: cron jobs. We keep the underlying cron expression in sync with the
// UI so admins can either pick a friendly "every 5 minutes / daily at 09:00"
// preset, or paste a raw cron expression when they need precise control.
import { useEffect, useMemo, useState } from "react";
import { apiGetArray, apiGet, apiPost, apiDel } from "../../lib/api";
import { IconTrash } from "../../components/Icons";
import { t } from "../../lib/i18n";

type Cron = {
  id: string; name: string; schedule_cron: string; prompt_template: string;
  enabled: boolean; failure_count: number; last_status?: string;
  last_run_at?: string; next_run_at?: string;
};

type Cadence = "5m" | "15m" | "30m" | "1h" | "daily" | "weekly" | "custom";

function cadenceToCron(c: Cadence, hour: number, minute: number, weekday: number): string {
  switch (c) {
    case "5m":    return "*/5 * * * *";
    case "15m":   return "*/15 * * * *";
    case "30m":   return "*/30 * * * *";
    case "1h":    return "0 * * * *";
    case "daily": return minute + " " + hour + " * * *";
    case "weekly":return minute + " " + hour + " * * " + weekday;
    default:      return "";
  }
}

function cronToCadence(expr: string): { c: Cadence; hour: number; minute: number; weekday: number } {
  const m = expr.trim().match(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)$/);
  if (!m) return { c: "custom", hour: 9, minute: 0, weekday: 1 };
  const mm = m[1], hh = m[2], dow = m[5];
  if (mm === "*/5")  return { c: "5m", hour: 9, minute: 0, weekday: 1 };
  if (mm === "*/15") return { c: "15m", hour: 9, minute: 0, weekday: 1 };
  if (mm === "*/30") return { c: "30m", hour: 9, minute: 0, weekday: 1 };
  if (mm === "0" && hh === "*") return { c: "1h", hour: 9, minute: 0, weekday: 1 };
  if (/^\d+$/.test(mm) && /^\d+$/.test(hh) && dow === "*") {
    return { c: "daily", hour: parseInt(hh, 10), minute: parseInt(mm, 10), weekday: 1 };
  }
  if (/^\d+$/.test(mm) && /^\d+$/.test(hh) && /^\d+$/.test(dow)) {
    return { c: "weekly", hour: parseInt(hh, 10), minute: parseInt(mm, 10), weekday: parseInt(dow, 10) };
  }
  return { c: "custom", hour: parseInt(hh || "9", 10), minute: parseInt(mm || "0", 10), weekday: 1 };
}

export function AdminCronsPage() {
  const [list, setList] = useState<Cron[]>([]);
  const [form, setForm] = useState<{ name: string; cadence: Cadence; hour: number; minute: number; weekday: number; raw: string; prompt: string }>({
    name: "", cadence: "5m", hour: 9, minute: 0, weekday: 1, raw: "", prompt: "",
  });
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    try { setList(await apiGetArray<Cron>(`/admin/crons`)); }
    catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  useEffect(() => { load(); }, []);

  const computedCron = useMemo(() => {
    if (form.cadence === "custom") return form.raw.trim();
    return cadenceToCron(form.cadence, form.hour, form.minute, form.weekday);
  }, [form]);

  async function add() {
    setErr(null);
    if (!form.name) { setErr(t("admin.crons.needName")); return; }
    if (!computedCron) { setErr(t("admin.crons.needSchedule")); return; }
    try {
      await apiPost("/admin/crons", { name: form.name, schedule_cron: computedCron, prompt_template: form.prompt });
      setForm({ ...form, name: "", prompt: "" });
      load();
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  async function toggle(c: Cron) { await apiPost("/admin/crons/" + c.id, { enabled: !c.enabled }); load(); }
  async function remove(c: Cron) {
    if (!confirm(t("admin.common.confirmDelete", { name: c.name }))) return;
    await apiDel("/admin/crons/" + c.id);
    load();
  }
  function edit(c: Cron) {
    const x = cronToCadence(c.schedule_cron);
    setForm({ name: c.name, cadence: x.c, hour: x.hour, minute: x.minute, weekday: x.weekday, raw: c.schedule_cron, prompt: c.prompt_template });
  }

  return (
    <div className="admin-page">
      <h1>{t("admin.crons.title")}</h1>
      <p className="admin-hint" style={{ marginBottom: 16 }}>{t("admin.crons.sub")}</p>
      {err && <div className="admin-card admin-err">{err}</div>}

      <div className="admin-card">
        <div className="admin-card-title">{t("admin.crons.addTitle")}</div>
        <div className="admin-form">
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.crons.name")}</span>
            <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="daily-status" />
          </label>
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.crons.cadence")}</span>
            <select value={form.cadence} onChange={(e) => setForm({ ...form, cadence: e.target.value as Cadence })}>
              <option value="5m">{t("admin.crons.cadence.5m")}</option>
              <option value="15m">{t("admin.crons.cadence.15m")}</option>
              <option value="30m">{t("admin.crons.cadence.30m")}</option>
              <option value="1h">{t("admin.crons.cadence.1h")}</option>
              <option value="daily">{t("admin.crons.cadence.daily")}</option>
              <option value="weekly">{t("admin.crons.cadence.weekly")}</option>
              <option value="custom">{t("admin.crons.cadence.custom")}</option>
            </select>
          </label>
          {(form.cadence === "daily" || form.cadence === "weekly") && (
            <>
              <label className="admin-field">
                <span className="admin-field-label">{t("admin.crons.time")}</span>
                <input
                  type="time"
                  value={String(form.hour).padStart(2, "0") + ":" + String(form.minute).padStart(2, "0")}
                  onChange={(e) => {
                    const parts = e.target.value.split(":");
                    const hh = parseInt(parts[0], 10) || 0;
                    const mm = parseInt(parts[1], 10) || 0;
                    setForm({ ...form, hour: hh, minute: mm });
                  }}
                />
              </label>
              {form.cadence === "weekly" && (
                <label className="admin-field">
                  <span className="admin-field-label">{t("admin.crons.weekday")}</span>
                  <select value={form.weekday} onChange={(e) => setForm({ ...form, weekday: parseInt(e.target.value, 10) })}>
                    {[0,1,2,3,4,5,6].map((d) => <option key={d} value={d}>{t("admin.crons.weekday." + d as any)}</option>)}
                  </select>
                </label>
              )}
            </>
          )}
          {form.cadence === "custom" && (
            <label className="admin-field">
              <span className="admin-field-label">{t("admin.crons.schedule")}</span>
              <input value={form.raw} onChange={(e) => setForm({ ...form, raw: e.target.value })} placeholder="*/5 * * * *" />
            </label>
          )}
          <label className="admin-field" style={{ alignItems: "flex-start" }}>
            <span className="admin-field-label">{t("admin.crons.prompt")}</span>
            <textarea value={form.prompt} onChange={(e) => setForm({ ...form, prompt: e.target.value })} rows={3} />
          </label>
          <div className="admin-hint">
            {t("admin.crons.preview")} <code className="code-chip">{computedCron || "-"}</code>
          </div>
        </div>
        <div className="admin-form-actions">
          <button className="primary" onClick={add}>{t("admin.common.add")}</button>
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
                  <td>
                    <button className="link-btn" onClick={() => edit(c)}><strong>{c.name}</strong></button>
                  </td>
                  <td><code className="code-chip">{c.schedule_cron}</code></td>
                  <td className="admin-clamp" title={c.prompt_template}>{c.prompt_template || t("common.dash")}</td>
                  <td>{c.last_status || t("common.dash")}</td>
                  <td>{c.last_run_at ? new Date(c.last_run_at).toLocaleString() : t("common.dash")}</td>
                  <td>{c.next_run_at ? new Date(c.next_run_at).toLocaleString() : t("common.dash")}</td>
                  <td>{c.failure_count > 0 ? <span className="pill pill-warn">{c.failure_count}</span> : c.failure_count}</td>
                  <td className="admin-row-action">
                    <button onClick={() => toggle(c)}>{c.enabled ? t("admin.common.disable") : t("admin.common.enable")}</button>
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






