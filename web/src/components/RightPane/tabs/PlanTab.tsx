import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { apiGet } from "../../../lib/api";

type PlanStep = {
  message_id: string;
  tool: string;
  args: Record<string, any>;
  status: string;
  at: string | null;
};
type PlanData = {
  session_id: string;
  steps: PlanStep[];
  status: "ok" | "empty";
  hint: string | null;
};
type Props = { data?: { sessionId?: string } };

export function PlanTab({ data }: Props) {
  const [params] = useSearchParams();
  const initial = data?.sessionId || params.get("session") || "";
  const [sid, setSid] = useState<string>(initial);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [plan, setPlan] = useState<PlanData | null>(null);

  async function load() {
    if (!sid) return;
    setBusy(true); setErr(null);
    try {
      const r = await apiGet<PlanData>("/client/plan?session_id=" + encodeURIComponent(sid));
      setPlan(r);
    } catch (e: any) {
      setErr(e?.message || "plan failed");
      setPlan(null);
    } finally { setBusy(false); }
  }
  useEffect(() => { if (initial) load(); }, [initial]);

  return (
    <div className="plan-tab">
      <div className="plan-toolbar">
        <label>Session</label>
        <input value={sid} onChange={(e) => setSid(e.target.value)} placeholder="session id" />
        <button className="primary" disabled={busy || !sid} onClick={load}>{busy ? "Loading..." : "Load"}</button>
      </div>
      {err && <div className="plan-err">{err}</div>}
      {plan && plan.status === "empty" && (
        <div className="tab-empty">
          <div style={{ fontSize: 14, marginBottom: 8 }}>No plan steps recorded yet.</div>
          <div style={{ fontSize: 12 }}>{plan.hint}</div>
        </div>
      )}
      {plan && plan.status === "ok" && (
        <div className="plan-list">
          {plan.steps.map((s, i) => (
            <div key={s.message_id + ":" + i} className="plan-step">
              <div className="plan-step-head">
                <span className="kbd">{i + 1}</span>
                <span className="plan-tool">{s.tool}</span>
                <span className={"plan-status " + (s.status === "ok" ? "ok" : s.status === "failed" ? "err" : "")}>{s.status}</span>
                {s.at && <span className="plan-time">{new Date(s.at).toLocaleTimeString()}</span>}
              </div>
              <pre className="plan-args">{JSON.stringify(s.args, null, 2)}</pre>
            </div>
          ))}
        </div>
      )}
      {!plan && !err && !busy && <div className="tab-empty">Open this tab from a chat session to see its plan.</div>}
    </div>
  );
}
