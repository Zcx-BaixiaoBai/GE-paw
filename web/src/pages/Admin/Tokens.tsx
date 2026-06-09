import { useEffect, useState } from "react";
import { apiGet, apiPut, apiDel } from "../../lib/api";

type ByModel = { model: string; prompt_tokens: number; completion_tokens: number; total_tokens: number; cost_cents: number; calls: number };
type Summary = { from: string; to: string; by_model: ByModel[]; calls: number; total_tokens: number; prompt_tokens: number; completion_tokens: number; cost_cents: number };
type ByDay = { bucket: string; prompt_tokens: number; completion_tokens: number; total_tokens: number; cost_cents: number };
type ByUser = { user_id: string | null; prompt_tokens: number; completion_tokens: number; cost_cents: number; calls: number };
type CostTable = { overrides: Record<string, { prompt: number; completion: number }>; known_models: string[] };

export function AdminTokensPage() {
  const [days, setDays] = useState(30);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [byDay, setByDay] = useState<ByDay[]>([]);
  const [byUser, setByUser] = useState<ByUser[]>([]);
  const [mtd, setMtd] = useState<{ calls: number; total_tokens: number; cost_cents: number } | null>(null);
  const [cost, setCost] = useState<CostTable | null>(null);
  const [overrideForm, setOverrideForm] = useState({ model: "", prompt: "0", completion: "0" });
  const [err, setErr] = useState<string | null>(null);

  async function loadAll() {
    try {
      const [s, bd, bu, m, c] = await Promise.all([
        apiGet<Summary>("/admin/tokens/summary"),
        apiGet<{ items: ByDay[] }>("/admin/tokens/by_day?days=" + days),
        apiGet<{ items: ByUser[] }>("/admin/tokens/by_user"),
        apiGet<{ calls: number; total_tokens: number; cost_cents: number }>("/admin/tokens/month_to_date"),
        apiGet<CostTable>("/admin/tokens/cost_table"),
      ]);
      setSummary(s);
      setByDay(bd.items);
      setByUser(bu.items);
      setMtd(m);
      setCost(c);
    } catch (e: any) { setErr(e?.message || "load failed"); }
  }
  useEffect(() => { loadAll(); }, [days]);

  async function setOverride() {
    if (!overrideForm.model) return;
    setErr(null);
    try {
      await apiPut("/admin/tokens/cost_table/" + encodeURIComponent(overrideForm.model), {
        prompt_cents_per_1k: parseInt(overrideForm.prompt || "0", 10),
        completion_cents_per_1k: parseInt(overrideForm.completion || "0", 10),
      });
      setOverrideForm({ model: "", prompt: "0", completion: "0" });
      loadAll();
    } catch (e: any) { setErr(e?.message || "set override failed"); }
  }
  async function clearOverride(model: string) {
    try { await apiDel("/admin/tokens/cost_table/" + encodeURIComponent(model)); loadAll(); }
    catch (e: any) { setErr(e?.message || "clear override failed"); }
  }

  const maxDay = Math.max(1, ...byDay.map((d) => d.total_tokens));

  return (
    <div>
      <h1>Token usage</h1>
      {err && <div className="admin-card" style={{ color: "var(--danger)" }}>{err}</div>}

      <div className="admin-card">
        <div className="row">
          <label>Window</label>
          <select value={days} onChange={(e) => setDays(parseInt(e.target.value, 10))}>
            <option value={1}>Last 24h</option>
            <option value={7}>Last 7d</option>
            <option value={30}>Last 30d</option>
            <option value={90}>Last 90d</option>
          </select>
          <span className="kbd" style={{ marginLeft: 12 }}>Total {summary?.calls ?? 0} calls / {summary?.total_tokens ?? 0} tokens / {(summary?.cost_cents ?? 0)} cents</span>
        </div>
      </div>

      <div className="admin-card">
        <div style={{ fontWeight: 600, marginBottom: 10 }}>By model</div>
        <table className="admin-table">
          <thead><tr><th>Model</th><th>Calls</th><th>Prompt</th><th>Completion</th><th>Total</th><th>Cost (cents)</th></tr></thead>
          <tbody>
            {(summary?.by_model || []).length === 0 && <tr><td colSpan={6} style={{ color: "var(--fg-faint)" }}>No usage</td></tr>}
            {(summary?.by_model || []).map((m) => (
              <tr key={m.model}><td>{m.model}</td><td>{m.calls}</td><td>{m.prompt_tokens}</td><td>{m.completion_tokens}</td><td>{m.total_tokens}</td><td>{m.cost_cents}</td></tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="admin-card">
        <div style={{ fontWeight: 600, marginBottom: 10 }}>By day</div>
        {byDay.length === 0 && <div style={{ color: "var(--fg-faint)" }}>No data in window.</div>}
        <div style={{ display: "flex", alignItems: "flex-end", gap: 2, height: 80 }}>
          {byDay.map((d) => (
            <div key={d.bucket} title={d.bucket + " " + d.total_tokens + " tokens"} style={{ flex: 1, background: "var(--accent)", height: Math.max(2, (d.total_tokens / maxDay) * 78) + "px", minWidth: 6 }} />
          ))}
        </div>
        <div style={{ fontSize: 10, color: "var(--fg-muted)", marginTop: 4, display: "flex", justifyContent: "space-between" }}>
          <span>{byDay[0]?.bucket || ""}</span><span>{byDay[byDay.length - 1]?.bucket || ""}</span>
        </div>
      </div>

      <div className="admin-card">
        <div style={{ fontWeight: 600, marginBottom: 10 }}>By user</div>
        <table className="admin-table">
          <thead><tr><th>User</th><th>Calls</th><th>Prompt</th><th>Completion</th><th>Cost (cents)</th></tr></thead>
          <tbody>
            {byUser.length === 0 && <tr><td colSpan={5} style={{ color: "var(--fg-faint)" }}>No usage</td></tr>}
            {byUser.map((u) => (
              <tr key={u.user_id || "anon"}><td>{u.user_id || "(system)"}</td><td>{u.calls}</td><td>{u.prompt_tokens}</td><td>{u.completion_tokens}</td><td>{u.cost_cents}</td></tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="admin-card">
        <div style={{ fontWeight: 600, marginBottom: 10 }}>Month to date</div>
        <div>Calls: <b>{mtd?.calls ?? 0}</b> &middot; Tokens: <b>{mtd?.total_tokens ?? 0}</b> &middot; Cost (cents): <b>{mtd?.cost_cents ?? 0}</b></div>
      </div>

      <div className="admin-card">
        <div style={{ fontWeight: 600, marginBottom: 10 }}>Cost table</div>
        <table className="admin-table">
          <thead><tr><th>Model</th><th>Prompt cents/1k</th><th>Completion cents/1k</th><th></th></tr></thead>
          <tbody>
            <tr>
              <td><input value={overrideForm.model} onChange={(e) => setOverrideForm({ ...overrideForm, model: e.target.value })} placeholder="model-name" /></td>
              <td><input value={overrideForm.prompt} onChange={(e) => setOverrideForm({ ...overrideForm, prompt: e.target.value })} style={{ width: 80 }} /></td>
              <td><input value={overrideForm.completion} onChange={(e) => setOverrideForm({ ...overrideForm, completion: e.target.value })} style={{ width: 80 }} /></td>
              <td><button onClick={setOverride} className="primary">Set override</button></td>
            </tr>
            {Object.entries(cost?.overrides || {}).map(([m, q]) => (
              <tr key={m}>
                <td><code>{m}</code></td><td>{q.prompt}</td><td>{q.completion}</td>
                <td><button onClick={() => clearOverride(m)}>Clear</button></td>
              </tr>
            ))}
          </tbody>
        </table>
        <div style={{ fontSize: 11, color: "var(--fg-muted)", marginTop: 6 }}>Known defaults: {(cost?.known_models || []).slice(0, 12).join(", ")}...</div>
      </div>
    </div>
  );
}
