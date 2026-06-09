import { useEffect, useRef, useState } from "react";
import { apiGet, apiPost, apiPostForm } from "../../lib/api";

type Src = { id: string; path: string; status: string; size_bytes: number; mime?: string; error?: string };

export function AdminWikiPage() {
  const [sources, setSources] = useState<Src[]>([]);
  const [busy, setBusy] = useState(false);
  const [log, setLog] = useState<string[]>([]);
  const fileRef = useRef<HTMLInputElement>(null);

  async function load() { setSources(await apiGet<Src[]>("/admin/wiki/sources")); }
  useEffect(() => { load(); }, []);
  function append(s: string) { setLog((l) => [...l, "[" + new Date().toLocaleTimeString() + "] " + s]); }

  async function upload(file: File) {
    setBusy(true);
    const fd = new FormData(); fd.append("file", file);
    try { const r = await apiPostForm<any>("/admin/wiki/sources/upload", fd); append("uploaded " + r.path); load(); }
    catch (e: any) { append("upload error: " + (e?.message || "unknown")); }
    finally { setBusy(false); }
  }
  async function ingestAll() { setBusy(true); try { const r = await apiPost<any>("/admin/wiki/ingest", {}); append("ingest: " + JSON.stringify(r)); load(); } catch (e: any) { append("ingest error: " + (e?.message || "unknown")); } finally { setBusy(false); } }
  async function compileAll() { setBusy(true); try { const r = await apiPost<any>("/admin/wiki/compile", {}); append("compile: " + JSON.stringify(r)); load(); } catch (e: any) { append("compile error: " + (e?.message || "unknown")); } finally { setBusy(false); } }
  async function reset() { if (!confirm("Wipe all wiki sources and pages?")) return; setBusy(true); try { await apiPost("/admin/wiki/reset", {}); append("reset OK"); load(); } catch (e: any) { append("reset error: " + (e?.message || "unknown")); } finally { setBusy(false); } }

  return (
    <div>
      <h1>Wiki (server-side corpus)</h1>
      <div className="admin-card">
        <div style={{ fontWeight: 600, marginBottom: 10 }}>Upload sources</div>
        <input ref={fileRef} type="file" multiple onChange={(e) => { Array.from(e.target.files || []).forEach(upload); }} disabled={busy} />
        <div style={{ marginTop: 8, display: "flex", gap: 8 }}>
          <button onClick={ingestAll} disabled={busy}>Trigger ingest</button>
          <button onClick={compileAll} disabled={busy}>Compile index</button>
          <button onClick={reset} disabled={busy} style={{ color: "var(--danger)" }}>Reset all</button>
        </div>
        <div style={{ fontSize: 11, color: "var(--fg-muted)", marginTop: 6 }}>All sources are stored on the server. Clients never see raw files.</div>
      </div>
      <div className="admin-card">
        <div style={{ fontWeight: 600, marginBottom: 10 }}>Sources ({sources.length})</div>
        <table className="admin-table">
          <thead><tr><th>Path</th><th>Status</th><th>Size</th><th>Error</th></tr></thead>
          <tbody>
            {sources.length === 0 && <tr><td colSpan={4} style={{ color: "var(--fg-faint)" }}>No sources</td></tr>}
            {sources.map((s) => (
              <tr key={s.id}>
                <td><code>{s.path}</code></td>
                <td>{s.status}</td>
                <td>{(s.size_bytes / 1024).toFixed(1)} KB</td>
                <td style={{ color: "var(--danger)" }}>{s.error || ""}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {log.length > 0 && (
        <div className="admin-card">
          <div style={{ fontWeight: 600, marginBottom: 10 }}>Log</div>
          <pre style={{ maxHeight: 200, fontSize: 11 }}>{log.join(String.fromCharCode(10))}</pre>
        </div>
      )}
    </div>
  );
}
