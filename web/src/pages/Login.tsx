import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiGet, apiPost } from "../lib/api";
import { useAuthStore } from "../stores/auth";

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
    } catch (e: any) { setErr(e?.message || "login failed"); }
    finally { setBusy(false); }
  }

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={submit}>
        <h1>GE-paw</h1>
        <div className="sub">Sign in to your workspace</div>
        <div className="field">
          <label>Username</label>
          <input value={u} onChange={(e) => setU(e.target.value)} autoFocus />
        </div>
        <div className="field">
          <label>Password</label>
          <input type="password" value={p} onChange={(e) => setP(e.target.value)} />
        </div>
        <div className="actions">
          <button className="primary" type="submit" disabled={busy} style={{ width: "100%" }}>
            {busy ? "Signing in..." : "Sign in"}
          </button>
        </div>
        {err && <div className="err">{err}</div>}
      </form>
    </div>
  );
}
