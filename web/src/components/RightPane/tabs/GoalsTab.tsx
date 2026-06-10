// Codex-style goal tab: per-session checklist with progress ring. The user
// can add, complete, and remove goals; the assistant reads them when
// drafting plans. State persists in localStorage via the goals store.
import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { useGoalsStore, type Goal, type GoalStatus } from "../../../stores/goals";
import { IconGoals, IconPlus, IconRefresh, IconTrash, IconCheck } from "../../../components/Icons";
import { t } from "../../../lib/i18n";

type Props = { data?: { sessionId?: string } };
const EMPTY_GOALS: Goal[] = [];
const STATUSES: GoalStatus[] = ["pending", "in_progress", "done", "failed"];
const statusLabel = (s: GoalStatus) => t(`goals.status.${s}` as any);

export function GoalsTab({ data }: Props) {
  const [params] = useSearchParams();
  const sid = data?.sessionId || params.get("session") || "";
  const goals = useGoalsStore((s) => (sid && s.bySession[sid]) || EMPTY_GOALS);
  const add = useGoalsStore((s) => s.add);
  const update = useGoalsStore((s) => s.update);
  const remove = useGoalsStore((s) => s.remove);
  const [text, setText] = useState("");

  const stats = useMemo(() => {
    const total = goals.length;
    const done = goals.filter((g) => g.status === "done").length;
    const inProgress = goals.filter((g) => g.status === "in_progress").length;
    const pct = total > 0 ? Math.round((done / total) * 100) : 0;
    return { total, done, inProgress, pct };
  }, [goals]);

  function submit() {
    if (!sid || !text.trim()) return;
    add(sid, text);
    setText("");
  }

  return (
    <div className="plan-tab">
      <div className="plan-toolbar">
        <span className="plan-toolbar-title"><IconGoals size={13} /> {t("tab.goals")}</span>
        <span className="plan-toolbar-spacer" />
        <span className="plan-toolbar-sid" title={sid}>{sid || t("plan.sessionPlaceholder")}</span>
        <button className="icon-btn" onClick={() => location.reload()} title={t("goals.refresh")}><IconRefresh size={13} /></button>
      </div>
      {!sid && <div className="tab-empty"><div className="tab-empty-title">{t("goals.tabHint")}</div></div>}
      {sid && (
        <>
          <div className="goal-progress">
            <ProgressRing percent={stats.pct} done={stats.done} total={stats.total} />
            <div className="goal-progress-meta">
              <div className="goal-progress-title">{t("goals.count.label", { done: stats.done, total: stats.total })}</div>
              {stats.inProgress > 0 && (
                <div className="goal-progress-sub">{stats.inProgress} {t("goals.status.in_progress")}</div>
              )}
            </div>
          </div>
          <div className="goals-add">
            <input
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); submit(); } }}
              placeholder={t("goals.addPlaceholder")}
            />
            <button className="primary" onClick={submit} disabled={!text.trim() || !sid} title={t("goals.add")}>
              <IconPlus size={13} />
            </button>
          </div>
          {goals.length === 0 ? (
            <div className="tab-empty">\r\n              <div className="tab-empty-icon"><IconGoals size={26} /></div>\r\n              <div className="tab-empty-title">{t("goals.empty.title")}</div>\r\n              <div className="tab-empty-hint">{t("goals.empty.hint")}</div>\r\n              <div className="tab-empty-hint">{t("goals.tabHint")}</div>\r\n            </div>
          ) : (
            <div className="plan-list">
              {goals.map((g) => (
                <GoalRow
                  key={g.id}
                  goal={g}
                  onStatus={(s) => update(sid, g.id, { status: s })}
                  onRemove={() => remove(sid, g.id)}
                />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}

function ProgressRing({ percent, done, total }: { percent: number; done: number; total: number }) {
  const r = 18;
  const c = 2 * Math.PI * r;
  const dash = (percent / 100) * c;
  return (
    <div className="goal-ring" title={`${done}/${total}`}>
      <svg width="44" height="44" viewBox="0 0 44 44" aria-hidden>
        <circle cx="22" cy="22" r={r} fill="none" stroke="var(--border)" strokeWidth="3" />
        <circle cx="22" cy="22" r={r} fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeDasharray={c} strokeDashoffset={c - dash} transform="rotate(-90 22 22)" style={{ transition: "stroke-dashoffset 320ms ease" }} />
      </svg>
      <span className="goal-ring-text">{percent}%</span>
    </div>
  );
}

function GoalRow({ goal, onStatus, onRemove }: { goal: Goal; onStatus: (s: GoalStatus) => void; onRemove: () => void }) {
  return (
    <div className={"goal-row goal-" + goal.status}>
      <button type="button" className="goal-check" title={statusLabel(goal.status)} onClick={() => onStatus(goal.status === "done" ? "pending" : "done")}>
        <IconCheck size={12} />
      </button>
      <div className="goal-row-body">
        <span className="goal-text">{goal.text}</span>
        <select className={"goal-status goal-status-" + goal.status} value={goal.status} onChange={(e) => onStatus(e.target.value as GoalStatus)} aria-label={t("goals.status.label")}>
          {STATUSES.map((s) => (
            <option key={s} value={s}>{statusLabel(s)}</option>
          ))}
        </select>
      </div>
      <button className="icon-btn" title={t("goals.delete")} onClick={onRemove}><IconTrash size={12} /></button>
    </div>
  );
}
