// Inline drawer variant of GoalsTab, opened from the composer toolbar.
// Reuses the same zustand-backed goal store so what the user sees here is
// identical to what the right-pane GoalsTab renders, just docked in the
// chat column for fast access during a turn.
import { useState } from "react";
import { useGoalsStore, type Goal, type GoalStatus } from "../stores/goals";
import { IconPlus, IconTrash, IconClose } from "./Icons";
import { t } from "../lib/i18n";

const EMPTY: Goal[] = [];
const STATUSES: GoalStatus[] = ["pending", "in_progress", "done", "failed"];

export function GoalDrawer({ sessionId, onClose }: { sessionId: string; onClose: () => void }) {
  const goals = useGoalsStore((s) => (sessionId ? s.bySession[sessionId] : EMPTY)) || EMPTY;
  const add = useGoalsStore((s) => s.add);
  const update = useGoalsStore((s) => s.update);
  const remove = useGoalsStore((s) => s.remove);
  const [text, setText] = useState("");

  const done = goals.filter((g) => g.status === "done").length;
  const total = goals.length;

  function submit() {
    if (!sessionId) return;
    if (add(sessionId, text)) setText("");
  }

  return (
    <div className="drawer goal-drawer">
      <div className="drawer-head">
        <span className="drawer-title">{t("chat.drawer.goals")}</span>
        <span className="drawer-count">
          {total === 0 ? "" : t("goals.count.label", { done, total })}
        </span>
        <span className="drawer-spacer" />
        <button type="button" className="topbar-icon-btn compact" onClick={onClose} title={t("chat.drawer.close")}>
          <IconClose size={14} />
        </button>
      </div>
      <div className="drawer-body">
        <div className="goals-add">
          <input
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); submit(); } }}
            placeholder={t("goals.addPlaceholder")}
          />
          <button type="button" className="primary" onClick={submit} disabled={!text.trim()} title={t("goals.add")}>
            <IconPlus size={14} />
          </button>
        </div>
        {goals.length === 0 ? (
          <div className="drawer-empty">
            <div className="drawer-empty-title">{t("goals.empty.title")}</div>
            <div className="drawer-empty-hint">{t("goals.empty.hint")}</div>
          </div>
        ) : (
          <ul className="goal-list">
            {goals.map((g) => (
              <li key={g.id} className={"goal-row goal-" + g.status}>
                <select
                  className={"goal-status goal-status-" + g.status}
                  value={g.status}
                  onChange={(e) => update(sessionId, g.id, { status: e.target.value as GoalStatus })}
                >
                  {STATUSES.map((s) => <option key={s} value={s}>{t("goals.status." + s as any)}</option>)}
                </select>
                <span className="goal-text">{g.text}</span>
                <button type="button" className="topbar-icon-btn compact" onClick={() => remove(sessionId, g.id)} title={t("goals.delete")}>
                  <IconTrash size={13} />
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
