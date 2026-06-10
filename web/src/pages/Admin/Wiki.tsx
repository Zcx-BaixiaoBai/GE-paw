import { useEffect, useRef, useState } from "react";
import { apiGet, apiPost, apiPostForm } from "../../lib/api";
import { IconRefresh, IconTrash } from "../../components/Icons";
import { t } from "../../lib/i18n";

type Src = { id: string; path: string; status: string; size_bytes: number; mime?: string; error?: string };

export function AdminWikiPage() {
  const [sources, setSources] = useState<Src[]>([]);
  const [busy, setBusy] = useState(false);
  const [log, setLog] = useState<string[]>([]);
  const fileRef = useRef<HTMLInputElement>(null);

  async function load() {
    try { setSources(await apiGet<Src[]>("/admin/wiki/sources")); }
    catch (e: any) { setLog((l) => [...l, "[" + new Date().toLocaleTimeString() + "] " + (e?.message || t("error.unknown"))]); }
  }
  useEffect(() => { load(); }, []);
  function append(s: string) { setLog((l) => [...l, "[" + new Date().toLocaleTimeString() + "] " + s]); }

  async function upload(file: File) {
    setBusy(true);
    const fd = new FormData(); fd.append("file", file);
    try {
      const r = await apiPostForm<any>("/admin/wiki/sources/upload", fd);
      append(t("admin.wiki.logUploaded", { path: r.path }));
      load();
    } catch (e: any) { append(t("admin.wiki.logUploadFailed", { err: e?.message || t("error.unknown") })); }
    finally { setBusy(false); }
  }
  async function ingestAll() {
    setBusy(true);
    try { const r = await apiPost<any>("/admin/wiki/ingest", {}); append(t("admin.wiki.logIngest", { result: JSON.stringify(r) })); load(); }
    catch (e: any) { append(t("admin.wiki.logIngestFailed", { err: e?.message || t("error.unknown") })); }
    finally { setBusy(false); }
  }
  async function compileAll() {
    setBusy(true);
    try { const r = await apiPost<any>("/admin/wiki/compile", {}); append(t("admin.wiki.logCompile", { result: JSON.stringify(r) })); load(); }
    catch (e: any) { append(t("admin.wiki.logCompileFailed", { err: e?.message || t("error.unknown") })); }
    finally { setBusy(false); }
  }
  async function reset() {
    if (!confirm(t("admin.wiki.confirmReset"))) return;
    setBusy(true);
    try { await apiPost("/admin/wiki/reset", {}); append(t("admin.wiki.logReset")); load(); }
    catch (e: any) { append(t("admin.wiki.logResetFailed", { err: e?.message || t("error.unknown") })); }
    finally { setBusy(false); }
  }

  return (
    <div className="admin-page">
      <div className="admin-page-head">
        <h1>{t("admin.wiki.title")}</h1>
        <button type="button" className="icon-btn" title={t("admin.common.refresh")} onClick={load} disabled={busy}><IconRefresh size={14} /></button>
      </div>

      <div className="admin-card">
        <div className="admin-card-title">{t("admin.wiki.upload")}</div>
        <input ref={fileRef} type="file" multiple onChange={(e) => { Array.from(e.target.files || []).forEach(upload); }} disabled={busy} className="admin-file" />
        <div className="admin-form-actions">
          <button onClick={ingestAll} disabled={busy}>{t("admin.wiki.triggerIngest")}</button>
          <button onClick={compileAll} disabled={busy}>{t("admin.wiki.compileIndex")}</button>
          <button onClick={reset} disabled={busy} className="danger">{t("admin.wiki.resetAll")}</button>
        </div>
        <div className="admin-hint">{t("admin.wiki.uploadHint")}</div>
      </div>

      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">{t("admin.wiki.upload")} ({sources.length})</div>
        {sources.length === 0 ? (
          <div className="admin-empty">{t("admin.wiki.empty")}</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>{t("admin.wiki.path")}</th>
                <th>{t("admin.wiki.status")}</th>
                <th>{t("admin.wiki.size")}</th>
                <th>{t("admin.wiki.error")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {sources.map((s) => (
                <tr key={s.id}>
                  <td><code className="code-chip">{s.path}</code></td>
                  <td>{s.status}</td>
                  <td>{(s.size_bytes / 1024).toFixed(1)} KB</td>
                  <td className="admin-err-cell">{s.error || ""}</td>
                  <td className="admin-row-action">
                    <button className="icon-btn danger" title={t("admin.common.delete")} onClick={async () => {
                      try { await apiPost("/admin/wiki/sources/" + s.id + "/delete", {}); load(); }
                      catch (e: any) { setLog((l) => [...l, "[" + new Date().toLocaleTimeString() + "] " + (e?.message || t("error.unknown"))]); }
                    }}><IconTrash size={13} /></button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {log.length > 0 && (
        <div className="admin-card">
          <div className="admin-card-title">{t("admin.wiki.log")}</div>
          <pre className="admin-log">{log.join("\n")}</pre>
        </div>
      )}
    </div>
  );
}
