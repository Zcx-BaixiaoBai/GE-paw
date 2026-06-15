// Audit log: filterable table of recent privileged actions. Pulls the
// /api/admin/audit endpoint (which returns actor_id rather than a
// username) and lets the admin drill into the JSON detail blob.
import { Fragment, useEffect, useMemo, useState } from "react";
import { apiGetArray } from "../../lib/api";
import { IconRefresh, IconChevronDown, IconClose } from "../../components/Icons";
import { t } from "../../lib/i18n";

type E = {
  id: number;
  action: string;
  actor_id: string | null;
  target: string | null;
  detail_json: string | null;
  ip: string | null;
  created_at: string;
};

type TimeRange = "1h" | "today" | "week" | "month" | "";

export function AdminAuditPage() {
  const [list, setList] = useState<E[]>([]);
  const [err, setErr] = useState<string | null>(null);
  const [actionFilter, setActionFilter] = useState<string>("");
  const [timeRange, setTimeRange] = useState<TimeRange>("");
  const [openId, setOpenId] = useState<number | null>(null);

  async function load() {
    try {
      let url = "/admin/audit";
      const params = new URLSearchParams();
      
      if (actionFilter) {
        params.append("action", actionFilter);
      }
      if (timeRange) {
        params.append("time_range", timeRange);
      }
      
      if (params.toString()) {
        url += "?" + params.toString();
      }
      
      setList(await apiGetArray<E>(url));
      setErr(null);
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  useEffect(() => { load(); }, [actionFilter, timeRange]);

  const actions = useMemo(() => {
    const set = new Set<string>();
    list.forEach((x) => set.add(x.action));
    return Array.from(set).sort();
  }, [list]);

  function fmt(json: string | null): string {
    if (!json) return "";
    try { return JSON.stringify(JSON.parse(json), null, 2); } catch { return json; }
  }

  function formatDateTime(dateString: string) {
    try {
      const date = new Date(dateString);
      return date.toLocaleString();
    } catch {
      return dateString;
    }
  }

  return (
    <div className="admin-page">
      <div className="admin-page-head">
        <h1>{t("admin.audit.title")}</h1>
        <span className="admin-hint text-muted">{t("admin.audit.emptyHint")}</span>
        <span className="admin-spacer" />
        
        {/* Action Filter */}
        <select
          className="admin-select"
          value={actionFilter}
          onChange={(e) => setActionFilter(e.target.value)}
          title={t("admin.audit.filter.action")}
        >
          <option value="">{t("admin.audit.filter.all")}</option>
          {actions.map((a) => <option key={a} value={a}>{a}</option>)}
        </select>
        
        {/* Time Range Filter */}
        <select
          className="admin-select"
          value={timeRange}
          onChange={(e) => setTimeRange(e.target.value as TimeRange)}
          title="Time Range"
        >
          <option value="">All Time</option>
          <option value="1h">Last 1 Hour</option>
          <option value="today">Today</option>
          <option value="week">This Week</option>
          <option value="month">This Month</option>
        </select>
        
        <button className="btn-ghost" onClick={load} title={t("admin.common.refresh")}>
          <IconRefresh size={14} />
        </button>
      </div>
      
      {err && <div className="admin-card admin-err">{err}</div>}
      
      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">
          <span>{t("admin.audit.title")} ({list.length})</span>
          {actionFilter && (
            <span className="admin-filter-pill">
              {actionFilter}
              <button 
                className="admin-filter-clear" 
                onClick={() => setActionFilter("")} 
                title={t("common.cancel")}
              >
                <IconClose size={10} />
              </button>
            </span>
          )}
          {timeRange && (
            <span className="admin-filter-pill" style={{ marginLeft: "8px" }}>
              {timeRange === "1h" ? "Last 1 Hour" : 
               timeRange === "today" ? "Today" : 
               timeRange === "week" ? "This Week" : 
               timeRange === "month" ? "This Month" : ""}
              <button 
                className="admin-filter-clear" 
                onClick={() => setTimeRange("")} 
                title="Clear time filter"
              >
                <IconClose size={10} />
              </button>
            </span>
          )}
        </div>
        {list.length === 0 ? (
          <div className="admin-empty">{t("admin.audit.empty")}</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th style={{ width: 32 }}></th>
                <th>{t("admin.audit.when")}</th>
                <th>{t("admin.audit.action")}</th>
                <th>{t("admin.audit.target")}</th>
                <th>{t("admin.audit.actor")}</th>
                <th>{t("admin.audit.ip")}</th>
              </tr>
            </thead>
            <tbody>
              {list.map((e) => {
                const open = openId === e.id;
                return (
                  <Fragment key={e.id}>
                    <tr 
                      className={"audit-row" + (open ? " open" : "")} 
                      onClick={() => setOpenId(open ? null : e.id)}
                    >
                      <td className="audit-caret">
                        <IconChevronDown size={12} />
                      </td>
                      <td className="admin-mono text-muted">{formatDateTime(e.created_at)}</td>
                      <td><code className="code-chip code-chip-action">{e.action}</code></td>
                      <td className="admin-clamp" title={e.target || ""}>
                        <code className="code-chip">{e.target || "¡ª"}</code>
                      </td>
                      <td className="admin-mono">{e.actor_id || "¡ª"}</td>
                      <td className="admin-mono font-mono">{e.ip || "¡ª"}</td>
                    </tr>
                    {open && (
                      <tr className="audit-detail">
                        <td colSpan={6}>
                          <pre className="admin-log">{fmt(e.detail_json) || "(ÎÞÏêÇé)"}</pre>
                        </td>
                      </tr>
                    )}
                  </Fragment>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
