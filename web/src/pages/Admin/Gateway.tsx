import { useEffect, useState, useCallback } from "react";
import { apiGet, apiPost, apiPut, apiDel } from "../../lib/api";
import { t } from "../../lib/i18n";

interface FilterRule {
  id: string;
  keyword: string;
  match_mode: string;
  severity: string;
  category: string | null;
  description: string | null;
  enabled: boolean;
  detect_count: number;
  block_count: number;
  total_checks: number;
  detect_rate: number;
  block_rate: number;
  created_at: string;
  updated_at: string;
}

interface GatewayStats {
  total_filters: number;
  enabled_filters: number;
  total_detections: number;
  total_blocks: number;
  total_checks: number;
  overall_detect_rate: number;
  overall_block_rate: number;
}

interface LogEntry {
  id: string;
  filter_id: string;
  keyword: string;
  matched_text: string;
  match_mode: string;
  severity: string;
  action_taken: string;
  session_id: string | null;
  model_name: string | null;
  created_at: string;
}

export function GatewayPage() {
  const [filters, setFilters] = useState<FilterRule[]>([]);
  const [stats, setStats] = useState<GatewayStats | null>(null);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [tab, setTab] = useState<"filters" | "logs">("filters");
  const [loading, setLoading] = useState(false);
  const [showAdd, setShowAdd] = useState(false);
  const [editing, setEditing] = useState<FilterRule | null>(null);

  // Form state
  const [form, setForm] = useState({
    keyword: "",
    match_mode: "exact",
    severity: "block",
    category: "",
    description: "",
  });

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [f, s, l] = await Promise.all([
        apiGet<FilterRule[]>("/gateway/filters"),
        apiGet<GatewayStats>("/gateway/stats"),
        apiGet<LogEntry[]>("/gateway/logs?limit=200"),
      ]);
      setFilters(f);
      setStats(s);
      setLogs(l);
    } catch { /* ignore */ }
    setLoading(false);
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleAdd = async () => {
    if (!form.keyword.trim()) return;
    try {
      await apiPost("/gateway/filters", {
        keyword: form.keyword.trim(),
        match_mode: form.match_mode,
        severity: form.severity,
        category: form.category || null,
        description: form.description || null,
      });
      setShowAdd(false);
      setForm({ keyword: "", match_mode: "exact", severity: "block", category: "", description: "" });
      load();
    } catch { /* ignore */ }
  };

  const handleUpdate = async () => {
    if (!editing) return;
    try {
      await apiPut(`/gateway/filters/${editing.id}`, {
        keyword: form.keyword.trim(),
        match_mode: form.match_mode,
        severity: form.severity,
        category: form.category || null,
        description: form.description || null,
      });
      setEditing(null);
      load();
    } catch { /* ignore */ }
  };

  const handleDelete = async (id: string) => {
    if (!confirm(t("gateway.confirmDelete"))) return;
    try {
      await apiDel(`/gateway/filters/${id}`);
      load();
    } catch { /* ignore */ }
  };

  const handleToggle = async (f: FilterRule) => {
    try {
      await apiPut(`/gateway/filters/${f.id}`, { enabled: !f.enabled });
      load();
    } catch { /* ignore */ }
  };

  const handleResetStats = async (id: string) => {
    try {
      await apiPost(`/gateway/filters/${id}/reset-stats`);
      load();
    } catch { /* ignore */ }
  };

  const handleClearLogs = async () => {
    if (!confirm(t("gateway.confirmClearLogs"))) return;
    try {
      await apiDel("/gateway/logs");
      load();
    } catch { /* ignore */ }
  };

  const startEdit = (f: FilterRule) => {
    setForm({
      keyword: f.keyword,
      match_mode: f.match_mode,
      severity: f.severity,
      category: f.category || "",
      description: f.description || "",
    });
    setEditing(f);
    setShowAdd(false);
  };

  const cancelForm = () => {
    setShowAdd(false);
    setEditing(null);
    setForm({ keyword: "", match_mode: "exact", severity: "block", category: "", description: "" });
  };

  const pct = (v: number) => (v * 100).toFixed(1) + "%";

  const severityLabel = (s: string) =>
    s === "block" ? t("gateway.severity.block") :
    s === "warn" ? t("gateway.severity.warn") :
    t("gateway.severity.log");

  const modeLabel = (m: string) =>
    m === "exact" ? t("gateway.mode.exact") :
    m === "regex" ? t("gateway.mode.regex") :
    t("gateway.mode.semantic");

  return (
    <div className="gateway-page">
      <h2>{t("gateway.title")}</h2>
      <p className="gateway-desc">{t("gateway.description")}</p>

      {/* Stats cards */}
      {stats && (
        <div className="gateway-stats">
          <div className="gw-stat-card">
            <div className="gw-stat-num">{stats.total_filters}</div>
            <div className="gw-stat-label">{t("gateway.stats.totalFilters")}</div>
          </div>
          <div className="gw-stat-card">
            <div className="gw-stat-num">{stats.enabled_filters}</div>
            <div className="gw-stat-label">{t("gateway.stats.enabled")}</div>
          </div>
          <div className="gw-stat-card">
            <div className="gw-stat-num">{stats.total_detections}</div>
            <div className="gw-stat-label">{t("gateway.stats.detections")}</div>
          </div>
          <div className="gw-stat-card">
            <div className="gw-stat-num">{stats.total_blocks}</div>
            <div className="gw-stat-label">{t("gateway.stats.blocks")}</div>
          </div>
          <div className="gw-stat-card">
            <div className="gw-stat-num">{pct(stats.overall_detect_rate)}</div>
            <div className="gw-stat-label">{t("gateway.stats.detectRate")}</div>
          </div>
          <div className="gw-stat-card">
            <div className="gw-stat-num">{pct(stats.overall_block_rate)}</div>
            <div className="gw-stat-label">{t("gateway.stats.blockRate")}</div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="gateway-tabs">
        <button className={tab === "filters" ? "active" : ""} onClick={() => setTab("filters")}>
          {t("gateway.tab.filters")}
        </button>
        <button className={tab === "logs" ? "active" : ""} onClick={() => setTab("logs")}>
          {t("gateway.tab.logs")}
        </button>
      </div>

      {/* Filters tab */}
      {tab === "filters" && (
        <div>
          <div className="gateway-toolbar">
            <button className="gw-btn primary" onClick={() => { cancelForm(); setShowAdd(true); }}>
              {t("gateway.add")}
            </button>
          </div>

          {(showAdd || editing) && (
            <div className="gw-form-card">
              <h3>{editing ? t("gateway.editFilter") : t("gateway.newFilter")}</h3>
              <div className="gw-form-grid">
                <label>
                  {t("gateway.form.keyword")}
                  <input
                    value={form.keyword}
                    onChange={(e) => setForm({ ...form, keyword: e.target.value })}
                    placeholder={t("gateway.form.keywordPlaceholder")}
                  />
                </label>
                <label>
                  {t("gateway.form.matchMode")}
                  <select value={form.match_mode} onChange={(e) => setForm({ ...form, match_mode: e.target.value })}>
                    <option value="exact">{t("gateway.mode.exact")}</option>
                    <option value="regex">{t("gateway.mode.regex")}</option>
                    <option value="semantic">{t("gateway.mode.semantic")}</option>
                  </select>
                </label>
                <label>
                  {t("gateway.form.severity")}
                  <select value={form.severity} onChange={(e) => setForm({ ...form, severity: e.target.value })}>
                    <option value="block">{t("gateway.severity.block")}</option>
                    <option value="warn">{t("gateway.severity.warn")}</option>
                    <option value="log">{t("gateway.severity.log")}</option>
                  </select>
                </label>
                <label>
                  {t("gateway.form.category")}
                  <input
                    value={form.category}
                    onChange={(e) => setForm({ ...form, category: e.target.value })}
                    placeholder={t("gateway.form.categoryPlaceholder")}
                  />
                </label>
                <label className="gw-full">
                  {t("gateway.form.description")}
                  <input
                    value={form.description}
                    onChange={(e) => setForm({ ...form, description: e.target.value })}
                    placeholder={t("gateway.form.descriptionPlaceholder")}
                  />
                </label>
              </div>
              <div className="gw-form-actions">
                <button className="gw-btn primary" onClick={editing ? handleUpdate : handleAdd}>
                  {t("gateway.form.save")}
                </button>
                <button className="gw-btn" onClick={cancelForm}>{t("gateway.form.cancel")}</button>
              </div>
            </div>
          )}

          {loading && <p className="gw-loading">{t("gateway.loading")}</p>}

          <table className="gw-table">
            <thead>
              <tr>
                <th>{t("gateway.col.keyword")}</th>
                <th>{t("gateway.col.mode")}</th>
                <th>{t("gateway.col.severity")}</th>
                <th>{t("gateway.col.category")}</th>
                <th>{t("gateway.col.detectCount")}</th>
                <th>{t("gateway.col.detectRate")}</th>
                <th>{t("gateway.col.blockCount")}</th>
                <th>{t("gateway.col.blockRate")}</th>
                <th>{t("gateway.col.enabled")}</th>
                <th>{t("gateway.col.actions")}</th>
              </tr>
            </thead>
            <tbody>
              {filters.length === 0 && (
                <tr><td colSpan={10} className="gw-empty">{t("gateway.empty")}</td></tr>
              )}
              {filters.map((f) => (
                <tr key={f.id} className={!f.enabled ? "gw-disabled" : ""}>
                  <td className="gw-kw">{f.keyword}</td>
                  <td><span className={`gw-badge mode-${f.match_mode}`}>{modeLabel(f.match_mode)}</span></td>
                  <td><span className={`gw-badge sev-${f.severity}`}>{severityLabel(f.severity)}</span></td>
                  <td>{f.category || "-"}</td>
                  <td>{f.detect_count}</td>
                  <td>{pct(f.detect_rate)}</td>
                  <td>{f.block_count}</td>
                  <td>{pct(f.block_rate)}</td>
                  <td>
                    <button className="gw-toggle" onClick={() => handleToggle(f)}>
                      {f.enabled ? "✓" : "✗"}
                    </button>
                  </td>
                  <td className="gw-actions">
                    <button className="gw-btn small" onClick={() => startEdit(f)}>{t("gateway.edit")}</button>
                    <button className="gw-btn small" onClick={() => handleResetStats(f.id)}>{t("gateway.resetStats")}</button>
                    <button className="gw-btn small danger" onClick={() => handleDelete(f.id)}>{t("gateway.delete")}</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Logs tab */}
      {tab === "logs" && (
        <div>
          <div className="gateway-toolbar">
            <button className="gw-btn danger" onClick={handleClearLogs}>{t("gateway.clearLogs")}</button>
          </div>
          {loading && <p className="gw-loading">{t("gateway.loading")}</p>}
          <table className="gw-table">
            <thead>
              <tr>
                <th>{t("gateway.log.time")}</th>
                <th>{t("gateway.col.keyword")}</th>
                <th>{t("gateway.col.mode")}</th>
                <th>{t("gateway.col.severity")}</th>
                <th>{t("gateway.log.action")}</th>
                <th>{t("gateway.log.matchedText")}</th>
                <th>{t("gateway.log.model")}</th>
              </tr>
            </thead>
            <tbody>
              {logs.length === 0 && (
                <tr><td colSpan={7} className="gw-empty">{t("gateway.log.empty")}</td></tr>
              )}
              {logs.map((l) => (
                <tr key={l.id}>
                  <td className="gw-time">{new Date(l.created_at).toLocaleString("zh-CN")}</td>
                  <td className="gw-kw">{l.keyword}</td>
                  <td><span className={`gw-badge mode-${l.match_mode}`}>{modeLabel(l.match_mode)}</span></td>
                  <td><span className={`gw-badge sev-${l.severity}`}>{severityLabel(l.severity)}</span></td>
                  <td><span className={`gw-badge act-${l.action_taken}`}>{l.action_taken === "blocked" ? t("gateway.log.blocked") : l.action_taken === "warned" ? t("gateway.log.warned") : t("gateway.log.logged")}</span></td>
                  <td className="gw-matched">{l.matched_text}</td>
                  <td>{l.model_name || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
