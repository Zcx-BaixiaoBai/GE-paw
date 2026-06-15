// Admin: MCP servers (per-org). Transport is one of "stdio" (subprocess
// command + args) or "http" (a remote SSE/HTTP MCP endpoint). Config is
// stored as a JSON object, but the form below provides guided fields for
// both transports and serialises them on save.
import { useEffect, useState } from "react";
import { apiGetArray, apiGet, apiPost, apiPatch, apiDel } from "../../lib/api";
import { IconTrash } from "../../components/Icons";
import { t } from "../../lib/i18n";

type Mcp = { id: string; name: string; transport: string; config: Record<string, any>; enabled: boolean };

type Form = {
  name: string;
  transport: "stdio" | "http";
  command: string;
  args: string;
  url: string;
  headers: string;
  env: string;
  enabled: boolean;
};

const EMPTY: Form = {
  name: "", transport: "stdio",
  command: "", args: "", url: "", headers: "", env: "",
  enabled: true,
};

function serialise(f: Form): Record<string, any> {
  if (f.transport === "stdio") {
    const args = f.args.split(/\s+/).map((s) => s.trim()).filter(Boolean);
    const env: Record<string, string> = {};
    f.env.split(/\n+/).forEach((line) => {
      const m = line.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$/);
      if (m) env[m[1]] = m[2];
    });
    return { command: f.command.trim(), args, env };
  }
  let headers: Record<string, string> = {};
  try {
    if (f.headers.trim()) headers = JSON.parse(f.headers);
  } catch { headers = { __raw: f.headers }; }
  return { url: f.url.trim(), headers };
}

export function AdminMCPPage() {
  const [list, setList] = useState<Mcp[]>([]);
  const [form, setForm] = useState<Form>({ ...EMPTY });
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    try { setList(await apiGetArray<Mcp>(`/admin/mcp`)); }
    catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  useEffect(() => { load(); }, []);

  async function add() {
    setErr(null);
    try {
      await apiPost("/admin/mcp", { name: form.name, transport: form.transport, config: serialise(form), enabled: form.enabled });
      setForm({ ...EMPTY });
      load();
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  async function toggle(x: Mcp) {
    await apiPatch("/admin/mcp/" + x.id, { enabled: !x.enabled });
    load();
  }
  async function remove(x: Mcp) {
    if (!confirm(t("admin.common.confirmDelete", { name: x.name }))) return;
    await apiDel("/admin/mcp/" + x.id);
    load();
  }

  return (
    <div className="admin-page">
      <h1>{t("admin.mcp.title")}</h1>
      <p className="admin-hint" style={{ marginBottom: 16 }}>{t("admin.mcp.sub")}</p>
      {err && <div className="admin-card admin-err">{err}</div>}

      <div className="admin-card">
        <div className="admin-card-title">{t("admin.mcp.addTitle")}</div>
        <div className="admin-form">
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.mcp.name")}</span>
            <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="mcp-filesystem" />
          </label>
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.mcp.transport")}</span>
            <select value={form.transport} onChange={(e) => setForm({ ...form, transport: e.target.value as Form["transport"] })}>
              <option value="stdio">stdio (本地子进程)</option>
              <option value="http">http (远端 MCP / SSE)</option>
            </select>
          </label>
          {form.transport === "stdio" ? (
            <>
              <label className="admin-field">
                <span className="admin-field-label">{t("admin.mcp.command")}</span>
                <input value={form.command} onChange={(e) => setForm({ ...form, command: e.target.value })} placeholder="npx -y @modelcontextprotocol/server-filesystem" />
              </label>
              <label className="admin-field" style={{ alignItems: "flex-start" }}>
                <span className="admin-field-label">{t("admin.mcp.env")}</span>
                <textarea
                  value={form.env}
                  onChange={(e) => setForm({ ...form, env: e.target.value })}
                  rows={3}
                  style={{ fontFamily: "var(--font-mono)", fontSize: 12 }}
                  placeholder={"API_KEY=xxx\nDEBUG=1"}
                />
              </label>
            </>
          ) : (
            <>
              <label className="admin-field">
                <span className="admin-field-label">{t("admin.mcp.url")}</span>
                <input value={form.url} onChange={(e) => setForm({ ...form, url: e.target.value })} placeholder="https://mcp.example.com/sse" />
              </label>
              <label className="admin-field" style={{ alignItems: "flex-start" }}>
                <span className="admin-field-label">{t("admin.mcp.headers")}</span>
                <textarea
                  value={form.headers}
                  onChange={(e) => setForm({ ...form, headers: e.target.value })}
                  rows={3}
                  style={{ fontFamily: "var(--font-mono)", fontSize: 12 }}
                  placeholder={'{"Authorization": "Bearer ..."}'}
                />
              </label>
            </>
          )}
          <label className="admin-checkbox">
            <input type="checkbox" checked={form.enabled} onChange={(e) => setForm({ ...form, enabled: e.target.checked })} />
            {t("admin.mcp.enabled")}
          </label>
        </div>
        <div className="admin-form-actions">
          <button className="primary" onClick={add} disabled={!form.name}>{t("admin.common.add")}</button>
          <span className="admin-hint">{t("admin.mcp.hint")}</span>
        </div>
      </div>

      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">{t("admin.mcp.list")} ({list.length})</div>
        {list.length === 0 ? (
          <div className="admin-empty">{t("admin.mcp.empty")}</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>{t("admin.mcp.name")}</th>
                <th>{t("admin.mcp.transport")}</th>
                <th>{t("admin.mcp.config")}</th>
                <th>{t("admin.mcp.enabled")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {list.map((x) => (
                <tr key={x.id}>
                  <td><strong>{x.name}</strong></td>
                  <td><code className="code-chip">{x.transport}</code></td>
                  <td className="admin-clamp" title={JSON.stringify(x.config)}>
                    <code className="code-chip">{x.config?.command || x.config?.url || t("common.dash")}</code>
                  </td>
                  <td>
                    <span className={"admin-pill " + (x.enabled ? "admin-pill-on" : "admin-pill-off")}>
                      {x.enabled ? t("admin.mcp.enabledOn") : t("admin.mcp.enabledOff")}
                    </span>
                  </td>
                  <td className="admin-row-action">
                    <button onClick={() => toggle(x)}>{x.enabled ? t("admin.common.disable") : t("admin.common.enable")}</button>
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




