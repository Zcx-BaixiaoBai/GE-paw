// Admin: channel accounts. We follow the qwenpaw-style UX: instead of a
// free-form JSON blob, each channel kind renders a guided form with the
// fields admins actually need to fill in. For wechat/wecom/dingtalk/feishu we
// also expose a one-click QR-code sign-in that walks the user through the
// official scan flow and writes the resulting credentials back to the row.
import { useEffect, useRef, useState } from "react";
import { apiGetArray, apiGet, apiPost, apiDel } from "../../lib/api";
import { IconTrash, IconRefresh } from "../../components/Icons";
import { t } from "../../lib/i18n";

type Ch = {
  id: string; kind: string; name: string; enabled: boolean; status: string;
  last_seen_at?: string | null;
  credentials: Record<string, any>;
};
type StatusResp = { running: string[] };

// Kinds the backend actually supports. Keep in sync with CHANNEL_KINDS.
const KINDS = [
  "telegram", "feishu", "wecom", "wechat", "dingtalk",
  "discord", "matrix", "mattermost", "mqtt", "onebot", "qq", "echo",
];
const QR_KINDS = new Set(["wechat", "wecom", "dingtalk", "feishu"]);

type QrState = {
  phase: "idle" | "loading" | "ready" | "polling" | "done" | "error";
  qrcode_img?: string;
  poll_token?: string;
  last_status?: string;
  credentials?: Record<string, any>;
  message?: string;
};

export function AdminChannelsPage() {
  const [list, setList] = useState<Ch[]>([]);
  const [status, setStatus] = useState<StatusResp>({ running: [] });
  const [form, setForm] = useState<{ kind: string; name: string; credentials: Record<string, string> }>(
    { kind: "telegram", name: "", credentials: {} },
  );
  const [err, setErr] = useState<string | null>(null);
  const [qr, setQr] = useState<QrState>({ phase: "idle" });
  const pollRef = useRef<number | null>(null);

  async function load() {
    try {
      setList(await apiGetArray<Ch>(`/admin/channels`));
      setStatus(await apiGet<StatusResp>("/admin/channels/status"));
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  useEffect(() => { load(); }, []);
  useEffect(() => () => { if (pollRef.current) window.clearInterval(pollRef.current); }, []);

  function setCred(k: string, v: string) {
    setForm((f) => ({ ...f, credentials: { ...f.credentials, [k]: v } }));
  }

  function kindDefaults(kind: string): Record<string, string> {
    switch (kind) {
      case "telegram": return { bot_token: "" };
      case "feishu":   return { app_id: "", app_secret: "" };
      case "wecom":    return { bot_id: "", secret: "" };
      case "wechat":   return {};
      case "dingtalk": return { client_id: "", client_secret: "" };
      case "qq":       return { app_id: "", app_secret: "" };
      case "discord":  return { bot_token: "" };
      case "matrix":   return { homeserver: "", access_token: "" };
      case "mattermost": return { url: "", token: "" };
      case "mqtt":     return { host: "", port: "1883", username: "", password: "", topic: "" };
      case "onebot":   return { url: "", access_token: "" };
      case "echo":     return {};
      default:         return {};
    }
  }

  function changeKind(kind: string) {
    setForm({ kind, name: form.name, credentials: kindDefaults(kind) });
  }

  async function add() {
    setErr(null);
    const cleaned: Record<string, any> = {};
    for (const [k, v] of Object.entries(form.credentials)) {
      if (v !== "") cleaned[k] = v;
    }
    try {
      await apiPost("/admin/channels", { kind: form.kind, name: form.name, credentials: cleaned, enabled: true });
      setForm({ kind: form.kind, name: "", credentials: kindDefaults(form.kind) });
      load();
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  async function toggle(c: Ch) { await apiPost("/admin/channels/" + c.id, { enabled: !c.enabled }); load(); }
  async function remove(c: Ch) {
    if (!confirm(t("admin.common.confirmDelete", { name: c.name }))) return;
    await apiDel("/admin/channels/" + c.id);
    load();
  }
  async function reload() {
    setErr(null);
    try {
      const r = await apiPost<{ started: number; running: string[] }>("/admin/channels/reload", {});
      setStatus({ running: r.running });
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  function isRunning(c: Ch) { return status.running.includes(c.kind + ":" + c.id); }

  async function startQrLogin() {
    if (!form.name) {
      setErr(t("admin.channels.qr.needName"));
      return;
    }
    setErr(null);
    setQr({ phase: "loading" });
    try {
      const r = await apiGet<{ qrcode_img: string; poll_token: string }>(
        "/config/channels/" + form.kind + "/qrcode",
      );
      setQr({ phase: "ready", qrcode_img: r.qrcode_img, poll_token: r.poll_token });
    } catch (e: any) {
      setQr({ phase: "error", message: e?.message || t("error.unknown") });
    }
  }

  function startPolling() {
    if (qr.phase !== "ready") return;
    setQr({ phase: "polling", qrcode_img: qr.qrcode_img, poll_token: qr.poll_token, last_status: "pending" });
    const tick = async () => {
      if (qr.phase !== "ready" && qr.phase !== "polling") return;
      const token = (qr as any).poll_token;
      try {
        const r = await apiGet<{ status: string; credentials?: Record<string, any> }>(
          "/config/channels/" + form.kind + "/qrcode/status?token=" + encodeURIComponent(token),
        );
        if (r.status === "ok" || r.status === "done") {
          if (pollRef.current) { window.clearInterval(pollRef.current); pollRef.current = null; }
          setQr({ phase: "done", credentials: r.credentials || {} });
        } else {
          setQr({ phase: "polling", qrcode_img: qr.qrcode_img, poll_token: token, last_status: r.status });
        }
      } catch (e: any) {
        if (pollRef.current) { window.clearInterval(pollRef.current); pollRef.current = null; }
        setQr({ phase: "error", message: e?.message || t("error.unknown") });
      }
    };
    tick();
    pollRef.current = window.setInterval(tick, 2000);
  }

  function applyQrCredentials() {
    if (qr.phase !== "done") return;
    setForm((f) => ({
      ...f,
      credentials: { ...f.credentials, ...(qr as any).credentials },
    }));
    setQr({ phase: "idle" });
  }

  const fields = form.kind in {
    telegram: 1, feishu: 1, wecom: 1, dingtalk: 1, qq: 1, discord: 1,
    matrix: 1, mattermost: 1, mqtt: 1, onebot: 1, echo: 1, wechat: 1,
  } ? kindDefaults(form.kind) : {};

  return (
    <div className="admin-page">
      <h1>{t("admin.channels.title")}</h1>
      <p className="admin-hint" style={{ marginBottom: 16 }}>{t("admin.channels.sub")}</p>
      {err && <div className="admin-card admin-err">{err}</div>}

      <div className="admin-card">
        <div className="admin-card-title">{t("admin.channels.addTitle")}</div>
        <div className="admin-form">
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.channels.kind")}</span>
            <select value={form.kind} onChange={(e) => changeKind(e.target.value)}>
              {KINDS.map((k) => <option key={k} value={k}>{k}</option>)}
            </select>
          </label>
          <label className="admin-field">
            <span className="admin-field-label">{t("admin.channels.name")}</span>
            <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="bot-main" />
          </label>
          {Object.keys(fields).length > 0 && (
            <div className="admin-form-group">
              <div className="admin-field-group-title">{t("admin.channels.credentials")}</div>
              {Object.entries(fields).map(([k, _]) => (
                <label className="admin-field" key={k}>
                  <span className="admin-field-label">{k}</span>
                  <input
                    type={k.includes("token") || k.includes("secret") || k.includes("password") || k.includes("key") ? "password" : "text"}
                    value={(form.credentials[k] ?? "") as string}
                    onChange={(e) => setCred(k, e.target.value)}
                    placeholder={k}
                  />
                </label>
              ))}
            </div>
          )}
        </div>

        {QR_KINDS.has(form.kind) && (
          <div className="qr-block">
            <div className="qr-block-title">{t("admin.channels.qr.title")}</div>
            <div className="qr-block-hint">{t("admin.channels.qr.hint")}</div>
            {qr.phase === "idle" && (
              <button className="primary" onClick={startQrLogin} disabled={!form.name}>
                {t("admin.channels.qr.start")}
              </button>
            )}
            {qr.phase === "loading" && <div className="qr-block-hint">{t("admin.channels.qr.loading")}</div>}
            {(qr.phase === "ready" || qr.phase === "polling") && (
              <div className="qr-stage">
                <img className="qr-img" src={qr.qrcode_img} alt="qrcode" />
                <div className="qr-side">
                  <div className="qr-side-status">{t("admin.channels.qr.scan")}</div>
                  {qr.phase === "ready" ? (
                    <button className="primary" onClick={startPolling}>{t("admin.channels.qr.scanned")}</button>
                  ) : (
                    <div className="qr-side-poll">{t("admin.channels.qr.polling", { status: qr.last_status ?? "" })}</div>
                  )}
                  <button onClick={() => { if (pollRef.current) window.clearInterval(pollRef.current); setQr({ phase: "idle" }); }}>
                    {t("common.cancel")}
                  </button>
                </div>
              </div>
            )}
            {qr.phase === "done" && (
              <div className="qr-done">
                <div className="qr-done-title">{t("admin.channels.qr.done")}</div>
                <pre className="qr-done-pre">{JSON.stringify((qr as any).credentials, null, 2)}</pre>
                <button className="primary" onClick={applyQrCredentials}>{t("admin.channels.qr.apply")}</button>
              </div>
            )}
            {qr.phase === "error" && (
              <div className="admin-err">
                {t("admin.channels.qr.error", { message: (qr as any).message })}
                <button onClick={() => setQr({ phase: "idle" })} style={{ marginLeft: 8 }}>
                  <IconRefresh size={11} /> {t("admin.channels.qr.retry")}
                </button>
              </div>
            )}
          </div>
        )}

        <div className="admin-form-actions">
          <button className="primary" onClick={add} disabled={!form.name}>{t("admin.common.add")}</button>
          <span className="admin-hint">{t("admin.channels.hint")}</span>
        </div>
      </div>

      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">
          <span>{t("admin.channels.list")}</span>
          <span className="admin-spacer" />
          <button onClick={reload}>{t("admin.channels.reload")}</button>
          <span className="admin-hint">{t("admin.channels.runningCount", { count: status.running.length })}</span>
        </div>
        {list.length === 0 ? (
          <div className="admin-empty">{t("admin.channels.empty")}</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>{t("admin.channels.kind")}</th>
                <th>{t("admin.channels.name")}</th>
                <th>{t("admin.channels.status")}</th>
                <th>{t("admin.channels.enabled")}</th>
                <th>{t("admin.channels.lastSeen")}</th>
                <th>{t("admin.channels.listener")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {list.map((c) => (
                <tr key={c.id}>
                  <td><code className="code-chip">{c.kind}</code></td>
                  <td><strong>{c.name}</strong></td>
                  <td>{c.status}</td>
                  <td>{c.enabled ? <span className="pill pill-ok">{t("admin.channels.enabled")}</span> : <span className="pill pill-off">{t("common.dash")}</span>}</td>
                  <td>{c.last_seen_at ? new Date(c.last_seen_at).toLocaleString() : t("common.dash")}</td>
                  <td>{isRunning(c) ? <span className="pill pill-ok">{t("admin.channels.running")}</span> : <span className="pill pill-off">{t("admin.channels.stopped")}</span>}</td>
                  <td className="admin-row-action">
                    <button onClick={() => toggle(c)}>{c.enabled ? t("admin.common.disable") : t("admin.common.enable")}</button>
                    <button className="icon-btn danger" onClick={() => remove(c)} title={t("admin.common.delete")}><IconTrash size={13} /></button>
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




