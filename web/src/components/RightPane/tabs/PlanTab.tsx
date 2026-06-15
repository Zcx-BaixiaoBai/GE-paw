// Codex-style plan tab: vertical timeline of the plan steps the assistant
// committed to. Pulls the current session from the URL (?session=) so the
// right pane "just works" without manual entry.
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { apiGet } from "../../../lib/api";
import { t } from "../../../lib/i18n";
import { IconRefresh, IconPlan } from "../../../components/Icons";

type PlanStep = {
  message_id: string;
  tool: string;
  args: Record<string, any>;
  status: string;
  at: string | null;
};
type PlanData = {
  session_id?: string;
  steps: PlanStep[];
  status: "ok" | "empty";
  hint?: string | null;
};
type Props = { data?: { sessionId?: string } };

function toolGlyph(tool: string) {
    if (tool.startsWith("read")) return "📖";
    if (tool.startsWith("edit") || tool.startsWith("write")) return "✏️";
    if (tool.startsWith("run") || tool.startsWith("exec")) return "▶";
    if (tool.startsWith("web") || tool.startsWith("fetch")) return "🌐";
    return "—";
  }

export function PlanTab({ data }: Props) {
  const [params] = useSearchParams();
  const sid = data?.sessionId || params.get("session") || "";
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
      setErr(e?.message || t("plan.failed"));
      setPlan(null);
    } finally { setBusy(false); }
  }
  useEffect(() => { if (sid) load(); }, [sid]);

  return (
    <div className="plan-tab">
      <div className="plan-toolbar">
        <span className="plan-toolbar-title"><IconPlan size={13} /> {t("tab.plan")}</span>
        <span className="plan-toolbar-spacer" />
        <span className="plan-toolbar-sid" title={sid}>{sid || t("plan.sessionPlaceholder")}</span>
        <button className="icon-btn" onClick={load} disabled={busy || !sid} title={t("goals.refresh")}><IconRefresh size={13} /></button>
      </div>
      {err && <div className="plan-err">{err}</div>}
      {!sid && <div className="tab-empty"><div className="tab-empty-title">{t("plan.tabHint")}</div></div>}
      {sid && plan && plan.status === "empty" && (
        <div className="tab-empty">
          <div className="tab-empty-title">{t("plan.empty.title")}</div>\r\n          <div className="tab-empty-hint">{plan.hint || t("plan.empty.hint")}</div>\r\n          <div className="tab-empty-hint">{t("plan.tabHint")}</div>
        </div>
      )}
      {sid && plan && plan.status === "ok" && (
        <div className="plan-list">
          {plan.steps.map((s, i) => (
            <div key={s.message_id + ":" + i} className={"plan-step plan-" + s.status}>
              <div className="plan-step-rail">
                <span className="plan-step-num">{i + 1}</span>
                {i < plan.steps.length - 1 && <span className="plan-step-line" />}
              </div>
              <div className="plan-step-body">
                <div className="plan-step-head">
                  <span className="plan-step-glyph" aria-hidden>{toolGlyph(s.tool)}</span>
                  <span className="plan-tool">{s.tool}</span>
                  <span className={"plan-status plan-status-" + s.status}>{t(("plan.status." + s.status) as any, undefined, s.status)}</span>
                  {s.at && <span className="plan-time">{new Date(s.at).toLocaleTimeString()}</span>}
                </div>
                {Object.keys(s.args || {}).length > 0 && (
                  <pre className="plan-args">{JSON.stringify(s.args, null, 2)}</pre>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
      {sid && !plan && !err && busy && <div className="tab-empty">{t("plan.loading")}</div>}
    </div>
  );
}



