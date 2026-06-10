import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiGet, apiPost } from "../lib/api";
import { useAuthStore } from "../stores/auth";
import { t } from "../lib/i18n";
import { Logo } from "../components/Logo";

export function LoginPage() {
  const [u, setU] = useState("admin");
  const [p, setP] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const setTokens = useAuthStore((s) => s.setTokens);
  const setIdentity = useAuthStore((s) => s.setIdentity);
  const nav = useNavigate();

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true); setErr(null);
    try {
      const r = await apiPost<any>("/auth/login", { username: u, password: p });
      setTokens(r.access_token, r.refresh_token);
      const me = await apiGet<any>("/auth/me");
      if (me?.username) setIdentity(me);
      nav("/app/assistant");
    } catch (e: any) { setErr(e?.message || t("login.failed")); }
    finally { setBusy(false); }
  }

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={submit}>
        <div className="login-brand">
          <Logo size={28} />
          <h1>{t("login.title")}</h1>
        </div>
        <div className="sub">{t("login.subtitle")}</div>
        <div className="field">
          <label>{t("login.username")}</label>
          <input value={u} onChange={(e) => setU(e.target.value)} autoFocus />
        </div>
        <div className="field">
          <label>{t("login.password")}</label>
          <input type="password" value={p} onChange={(e) => setP(e.target.value)} />
        </div>
        <div className="actions">
          <button className="primary" type="submit" disabled={busy} style={{ width: "100%" }}>
            {busy ? t("login.submitting") : t("login.submit")}
          </button>
        </div>
        {err && <div className="err">{err}</div>}
      </form>
    </div>
  );
}
