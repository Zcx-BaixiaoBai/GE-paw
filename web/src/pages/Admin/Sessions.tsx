import { useEffect, useState } from "react";
import { apiGetArray, apiGet, apiPost, apiDel } from "../../lib/api";
import { IconTrash } from "../../components/Icons";
import { t } from "../../lib/i18n";

type S = {
  id: string; title: string; status: string; pinned: boolean; archived: boolean;
  channel_kind?: string | null; channel_account_id?: string | null;
  username?: string; user_id?: string;
  message_count?: number; last_message_at?: string | null; created_at?: string | null;
};

export function AdminSessionsPage() {
  const [list, setList] = useState<S[]>([]);
  const [showAll, setShowAll] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  async function load() {
    try { setList(await apiGetArray<S>(`/admin/sessions?all=` + (showAll ? "1" : "0"))); }
    catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  useEffect(() => { load(); }, [showAll]);
  async function archive(x: S) {
    await apiPost("/admin/sessions/" + x.id + "/archive", {}); load();
  }
  async function remove(x: S) {
    if (!confirm(t("admin.common.confirmDelete", { name: x.title || x.id }))) return;
    await apiDel("/admin/sessions/" + x.id); load();
  }
  return (
    <div className="admin-page">
      <h1>{t("admin.sessions.title")}</h1>
      {err && <div className="admin-card admin-err">{err}</div>}
      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">
          <span>{t("admin.sessions.title")} ({list.length})</span>
          <span className="admin-spacer" />
          <label className="admin-checkbox">
            <input type="checkbox" checked={showAll} onChange={(e) => setShowAll(e.target.checked)} />
            {t("admin.sessions.allChannels")}
          </label>
        </div>
        {list.length === 0 ? (
          <div className="admin-empty">{t("admin.sessions.empty")}</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>{t("admin.sessions.title2")}</th>
                <th>{t("admin.sessions.user")}</th>
                <th>{t("admin.sessions.channel")}</th>
                <th>{t("admin.sessions.messages")}</th>
                <th>{t("admin.sessions.status")}</th>
                <th>{t("admin.sessions.lastActivity")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {list.map((x) => (
                <tr key={x.id}>
                  <td>
                    <strong>{x.title || x.id.slice(0, 8)}</strong>
                    {x.archived && <span className="pill pill-off" style={{ marginLeft: 8 }}>{t("admin.sessions.archived")}</span>}
                  </td>
                  <td>{x.username || x.user_id || t("common.dash")}</td>
                  <td>{x.channel_kind || <span className="admin-hint">{t("admin.sessions.web")}</span>}</td>
                  <td>{x.message_count ?? 0}</td>
                  <td>{x.status}</td>
                  <td>{x.last_message_at ? new Date(x.last_message_at).toLocaleString() : t("common.dash")}</td>
                  <td className="admin-row-action">
                    <button onClick={() => archive(x)}>{t("admin.sessions.archive")}</button>
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




