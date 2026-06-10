// Inline drawer that shows the current session's recorded plan steps.
// Fetches the same /client/plan payload that the right-pane PlanTab uses,
// and re-polls every 5s while open so a long-running agent updates land.
import { useEffect, useState } from "react";
import { apiGet } from "../lib/api";
import { IconClose, IconRefresh } from "./Icons";
import { t } from "../lib/i18n";

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

export function PlanDrawer({ sessionId, onClose }: { sessionId: string; onClose: () => void }) {
  const [data, setData] = useState<PlanData | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function load() {
    if (!sessionId) return;
    setLoading(true); setErr(null);
    try {
      const r = await apiGet<PlanData>("/client/plan?session_id=" + encodeURIComponent(sessionId));
      setData(r);
    } catch (e: any) {
      setErr(e?.message || t("plan.failed"));
    } finally { setLoading(false); }
  }

  useEffect(() => {
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, [sessionId]);

  return (
    <div className="drawer plan-drawer">
      <div className="drawer-head">
        <span className="drawer-title">{t("chat.drawer.plan")}</span>
        <span className="drawer-count">
          {data && data.status === "ok" ? `${data.steps.length}` : ""}
        </span>
        <span className="drawer-spacer" />
        <button type="button" className="topbar-icon-btn compact" onClick={load} title={t("goals.refresh")} disabled={loading}>
          <IconRefresh size={13} />
        </button>
        <button type="button" className="topbar-icon-btn compact" onClick={onClose} title={t("chat.drawer.close")}>
          <IconClose size={14} />
        </button>
      </div>
      <div className="drawer-body">
        {err && <div className="drawer-err">{err}</div>}
        {data && data.status === "empty" && (
          <div className="drawer-empty">
            <div className="drawer-empty-title">{t("plan.empty.title")}</div>
            <div className="drawer-empty-hint">{data.hint || t("plan.empty.hint")}</div>
          </div>
        )}
        {data && data.status === "ok" && (
          <ul className="plan-list">
            {data.steps.map((s, i) => (
              <li key={s.message_id + ":" + i} className="plan-step">
                <div className="plan-step-head">
                  <span className="kbd">{i + 1}</span>
                  <span className="plan-tool">{s.tool}</span>
                  <span className={"plan-status " + (s.status === "ok" ? "ok" : s.status === "failed" ? "err" : "")}>{s.status}</span>
                  {s.at && <span className="plan-time">{new Date(s.at).toLocaleTimeString()}</span>}
                </div>
                <pre className="plan-args">{JSON.stringify(s.args, null, 2)}</pre>
              </li>
            ))}
          </ul>
        )}
        {!data && !err && <div className="drawer-empty">{loading ? t("plan.loading") : t("plan.tabHint")}</div>}
      </div>
    </div>
  );
}
