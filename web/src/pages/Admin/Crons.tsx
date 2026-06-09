import { useEffect, useState } from "react";
import { apiGet, apiPost, apiDel, apiPost as _apiPost } from "../../lib/api";

type Cron = {
  id: string; name: string; schedule_cron: string; prompt_template: string;
  enabled: boolean; failure_count: number; last_status?: string; last_run_at?: string;
  next_run_at?: string;
};

export function AdminCronsPage() {
  const [list, setList] = useState<Cron[]>([]);
  const [form, setForm] = useState({
    name: "", schedule_cron: "*/5 * * * *",
    prompt_template: "Generate a short daily status report based on the org wiki overview.",
  });
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    try { setList(await apiGet<Cron[]>("/admin/crons")); }
    catch (e: any) { setErr(e?.message || "load failed"); }
  }
  useEffect(() => { load(); }, []);

  async function add() {
    setErr(null);
    try {
      await apiPost("/admin/crons", form);
      setForm({ ...form, name: "" });
      load();
    } catch (e: any) { setErr(e?.message || "create failed"); }
  }
  async function toggle(c: Cron) {
    await _apiPost("/admin/crons/" + c.id, { enabled: !c.enabled });
    load();
  }
  async function remove(c: Cron) {
    if (!confirm("Delete cron " + c.name + "?")) return;
    await apiDel("/admin/crons/" + c.id);
    load();
  }

  return (
    <div>
      <h1>Cron jobs</h1>
      {err && <div className="admin-card" style={{ color: "var(--danger)" }}>{err}</div>}
      <div className="admin-card">
        <div style={{ fontWeight: 600, marginBottom: 10 }}>Add job</div>
        <div className="row"><label>Name</label><input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="daily-status" /></div>
        <div className="row"><label>Schedule (cron)</label><input value={form.schedule_cron} onChange={(e) => setForm({ ...form, schedule_cron: e.target.value })} placeholder="*/5 * * * *" /></div>
        <div className="row"><label>Prompt template</label><textarea value={form.prompt_template} onChange={(e) => setForm({ ...form, prompt_template: e.target.value })} rows={3} /></div>
        <button className="primary" onClick={add} disabled={!form.name || !form.schedule_cron}>Add</button>
        <div style={{ fontSize: 11, color: "var(--fg-muted)", marginTop: 6 }}>Output is logged to cron_run and counted in token_usage_log. 3 consecutive failures auto-disable the job.</div>
      </div>
      <div className="admin-card">
        <table className="admin-table">
          <thead><tr><th>Name</th><th>Schedule</th><th>Prompt</th><th>Last status</th><th>Last run</th><th>Next run</th><th>Failures</th><th></th></tr></thead>
          <tbody>
            {list.length === 0 && <tr><td colSpan={8} style={{ color: "var(--fg-faint)" }}>No cron jobs</td></tr>}
            {list.map((c) => (
              <tr key={c.id}>
                <td><b>{c.name}</b></td>
                <td><code>{c.schedule_cron}</code></td>
                <td style={{ maxWidth: 280, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }} title={c.prompt_template}>{c.prompt_template}</td>
                <td>{c.last_status || "-"}</td>
                <td>{c.last_run_at ? new Date(c.last_run_at).toLocaleString() : "-"}</td>
                <td>{c.next_run_at ? new Date(c.next_run_at).toLocaleString() : "-"}</td>
                <td>{c.failure_count}</td>
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
