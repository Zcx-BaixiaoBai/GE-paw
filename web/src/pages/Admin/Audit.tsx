import { useEffect, useState } from "react";
import { apiGet } from "../../lib/api";
import { IconRefresh } from "../../components/Icons";
import { t } from "../../lib/i18n";

type E = { id: number; action: string; target: string; actor: string; created_at: string; details?: string };

export function AdminAuditPage() {
  const [list, setList] = useState<E[]>([]);
  const [err, setErr] = useState<string | null>(null);
  async function load() {
    try { setList(await apiGet<E[]>("/admin/audit")); setErr(null); }
    catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  useEffect(() => { load(); }, []);
  return (
    <div className="admin-page">
      <div className="admin-page-head">
        <h1>{t("admin.audit.title")}</h1>
        <button className="icon-btn" onClick={load} title={t("admin.common.refresh")}><IconRefresh size={14} /></button>
      </div>
      {err && <div className="admin-card admin-err">{err}</div>}
      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">{t("admin.audit.title")} ({list.length})</div>
        {list.length === 0 ? (
          <div className="admin-empty">{t("admin.audit.empty")}</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>{t("admin.audit.when")}</th>
                <th>{t("admin.audit.action")}</th>
                <th>{t("admin.audit.target")}</th>
                <th>{t("admin.audit.actor")}</th>
              </tr>
            </thead>
            <tbody>
              {list.map((e) => (
                <tr key={e.id}>
                  <td className="admin-mono">{new Date(e.created_at).toLocaleString()}</td>
                  <td><code className="code-chip">{e.action}</code></td>
                  <td><code className="code-chip">{e.target}</code></td>
                  <td>{e.actor}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
