import { useEffect, useState } from "react";
import { apiGet, apiPut, apiDel } from "../../lib/api";
import { t } from "../../lib/i18n";

type ByModel = { model: string; prompt_tokens: number; completion_tokens: number; total_tokens: number; cost_cents: number; calls: number };
type Summary = { from: string; to: string; by_model: ByModel[]; calls: number; total_tokens: number; prompt_tokens: number; completion_tokens: number; cost_cents: number };
type ByDay = { bucket: string; prompt_tokens: number; completion_tokens: number; total_tokens: number; cost_cents: number };
type ByUser = { user_id: string | null; prompt_tokens: number; completion_tokens: number; cost_cents: number; calls: number };
type CostTable = { overrides: Record<string, { prompt: number; completion: number }>; known_models: string[] };

export function AdminTokensPage() {
  const [days, setDays] = useState(7);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [byDay, setByDay] = useState<ByDay[]>([]);
  const [byUser, setByUser] = useState<ByUser[]>([]);
  const [mtd, setMtd] = useState<{ calls: number; total_tokens: number; cost_cents: number } | null>(null);
  const [cost, setCost] = useState<CostTable | null>(null);
  const [overrideForm, setOverrideForm] = useState({ model: "", prompt: "0.15", completion: "0.6" });
  const [err, setErr] = useState<string | null>(null);

  async function loadAll() {
    setErr(null);
    try {
      const [s, d, u, m, c] = await Promise.all([
        apiGet<Summary>("/admin/tokens/summary?days=" + days),
        apiGet<ByDay[]>("/admin/tokens/by-day?days=" + days),
        apiGet<ByUser[]>("/admin/tokens/by-user?days=" + days),
        apiGet<{ calls: number; total_tokens: number; cost_cents: number }>("/admin/tokens/mtd"),
        apiGet<CostTable>("/admin/tokens/cost_table"),
      ]);
      setSummary(s); setByDay(d); setByUser(u); setMtd(m); setCost(c);
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  useEffect(() => { loadAll(); }, [days]);

  async function setOverride() {
    setErr(null);
    try {
      await apiPut("/admin/tokens/cost_table/" + encodeURIComponent(overrideForm.model), {
        prompt: Number(overrideForm.prompt),
        completion: Number(overrideForm.completion),
      });
      setOverrideForm({ model: "", prompt: "0.15", completion: "0.6" });
      loadAll();
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  async function clearOverride(model: string) {
    try { await apiDel("/admin/tokens/cost_table/" + encodeURIComponent(model)); loadAll(); }
    catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }

  const maxDay = Math.max(1, ...byDay.map((d) => d.total_tokens));

  return (
    <div className="admin-page">
      <h1>{t("admin.tokens.title")}</h1>
      {err && <div className="admin-card admin-err">{err}</div>}

      <div className="admin-card">
        <div className="admin-form admin-form-inline">
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.tokens.window")}</span>
            <select value={days} onChange={(e) => setDays(parseInt(e.target.value, 10))}>
              <option value={1}>{t("admin.tokens.last24h")}</option>
              <option value={7}>{t("admin.tokens.last7d")}</option>
              <option value={30}>{t("admin.tokens.last30d")}</option>
              <option value={90}>{t("admin.tokens.last90d")}</option>
            </select>
          </label>
          <span className="admin-spacer" />
          <span className="admin-hint">
            {t("admin.tokens.summary", { calls: summary?.calls ?? 0, tokens: summary?.total_tokens ?? 0, cents: summary?.cost_cents ?? 0 })}
          </span>
        </div>
      </div>

      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">{t("admin.tokens.byModel")}</div>
        {(!summary || summary.by_model.length === 0) ? (
          <div className="admin-empty">{t("admin.tokens.empty")}</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>{t("admin.tokens.title")}</th>
                <th>{t("admin.tokens.calls")}</th>
                <th>{t("admin.tokens.prompt")}</th>
                <th>{t("admin.tokens.completion")}</th>
                <th>{t("admin.tokens.total")}</th>
                <th>{t("admin.tokens.cost")}</th>
              </tr>
            </thead>
            <tbody>
              {summary.by_model.map((m) => (
                <tr key={m.model}>
                  <td className="admin-mono">{m.model}</td>
                  <td>{m.calls}</td>
                  <td>{m.prompt_tokens}</td>
                  <td>{m.completion_tokens}</td>
                  <td>{m.total_tokens}</td>
                  <td>{m.cost_cents}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="admin-card">
        <div className="admin-card-title">{t("admin.tokens.byDay")}</div>
        {byDay.length === 0 ? (
          <div className="admin-empty">{t("admin.tokens.emptyWindow")}</div>
        ) : (
          <>
            <div className="admin-bar-chart">
              {byDay.map((d) => (
                <div key={d.bucket} className="admin-bar" title={d.bucket + " · " + d.total_tokens + " tokens"}
                  style={{ height: Math.max(4, (d.total_tokens / maxDay) * 70) + "px" }} />
              ))}
            </div>
            <div className="admin-bar-axis">
              <span>{byDay[0]?.bucket || ""}</span>
              <span>{byDay[byDay.length - 1]?.bucket || ""}</span>
            </div>
          </>
        )}
      </div>

      <div className="admin-card">
        <div className="admin-card-title">{t("admin.tokens.monthToDate")}</div>
        <div className="admin-metrics">
          <Metric label={t("admin.tokens.calls")} value={mtd?.calls ?? 0} />
          <Metric label={t("admin.tokens.total")} value={mtd?.total_tokens ?? 0} />
          <Metric label={t("admin.tokens.cost")} value={mtd?.cost_cents ?? 0} />
        </div>
      </div>

      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">{t("admin.tokens.costTable")}</div>
        <table className="admin-table">
          <thead>
            <tr>
              <th>{t("admin.tokens.title")}</th>
              <th>{"Prompt / 1k"}</th>
              <th>{"Completion / 1k"}</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <input value={overrideForm.model}
                  onChange={(e) => setOverrideForm({ ...overrideForm, model: e.target.value })}
                  placeholder="model-name" />
              </td>
              <td>
                <input value={overrideForm.prompt}
                  onChange={(e) => setOverrideForm({ ...overrideForm, prompt: e.target.value })}
                  style={{ width: 80 }} />
              </td>
              <td>
                <input value={overrideForm.completion}
                  onChange={(e) => setOverrideForm({ ...overrideForm, completion: e.target.value })}
                  style={{ width: 80 }} />
              </td>
              <td className="admin-row-action">
                <button onClick={setOverride} className="primary">{t("admin.common.save")}</button>
              </td>
            </tr>
            {Object.entries(cost?.overrides || {}).map(([m, q]) => (
              <tr key={m}>
                <td><code className="code-chip">{m}</code></td>
                <td>{q.prompt}</td>
                <td>{q.completion}</td>
                <td className="admin-row-action">
                  <button onClick={() => clearOverride(m)}>{t("admin.common.delete")}</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="admin-hint">
          {t("admin.tokens.knownHint", { models: (cost?.known_models || []).slice(0, 12).join(", ") })}
        </div>
      </div>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="admin-metric">
      <div className="admin-metric-value">{value}</div>
      <div className="admin-metric-label">{label}</div>
    </div>
  );
}
