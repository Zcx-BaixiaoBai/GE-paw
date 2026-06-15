// Right-pane "Progress" tab (MiniMax Code style).
//
// A vertical list of steps with a leading status indicator. The leading
// indicator follows the same conventions we use elsewhere on the page:
//   pending  -> hollow ring
//   running  -> small filled ring with a slow pulse
//   done     -> muted check inside a faint ring
//   failed   -> red ring with !
//
// Done steps are dimmed and the label is struck through so the eye is
// pulled to whatever is currently running. The list is intentionally
// minimal — no card backgrounds, no progress bars per step. The bar at
// the top of the page is the place for aggregate progress; this is the
// place for the human-readable log.

import { useProgressStore, type Step, type StepStatus } from "../../../stores/progress";
import { IconClose } from "../../../components/Icons";

function statusIcon(status: StepStatus) {
  if (status === "done") {
    return (
      <svg viewBox="0 0 16 16" width="14" height="14" aria-hidden>
        <circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" strokeWidth="1.2" opacity="0.35" />
        <path d="M4.8 8.3 L7 10.5 L11.4 6" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    );
  }
  if (status === "running") {
    return (
      <svg viewBox="0 0 16 16" width="14" height="14" aria-hidden>
        <circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" strokeWidth="1.2" className="step-pulse" />
      </svg>
    );
  }
  if (status === "failed") {
    return (
      <svg viewBox="0 0 16 16" width="14" height="14" aria-hidden>
        <circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" strokeWidth="1.2" />
        <path d="M8 5 V9 M8 11 V11.4" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
      </svg>
    );
  }
  // pending
  return (
    <svg viewBox="0 0 16 16" width="14" height="14" aria-hidden>
      <circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" strokeWidth="1.2" opacity="0.25" />
    </svg>
  );
}

function StepRow({ step, idx }: { step: Step; idx: number }) {
  return (
    <li
      className={
        "progress-step" +
        (step.status === "done" ? " is-done" : "") +
        (step.status === "running" ? " is-running" : "") +
        (step.status === "failed" ? " is-failed" : "")
      }
    >
      <span className="progress-step-icon">{statusIcon(step.status)}</span>
      <div className="progress-step-body">
        <div className="progress-step-label">
          <span className="progress-step-num">{idx + 1}.</span>
          <span>{step.label}</span>
          {step.hint ? <span className="progress-step-hint">{step.hint}</span> : null}
        </div>
        {step.detail ? <div className="progress-step-detail">{step.detail}</div> : null}
      </div>
    </li>
  );
}

export function ProgressTab() {
  const steps = useProgressStore((s) => s.steps);
  const running = useProgressStore((s) => s.running);
  const used = useProgressStore((s) => s.usedTokens);
  const max = useProgressStore((s) => s.maxTokens);
  const reset = useProgressStore((s) => s.reset);
  const endRun = useProgressStore((s) => s.endRun);
  const pushStep = useProgressStore((s) => s.pushStep);

  const pct = max > 0 ? Math.min(100, Math.round((used / max) * 1000) / 10) : 0;
  const doneCount = steps.filter((s) => s.status === "done").length;
  const totalCount = steps.length;

  return (
    <div className="progress-tab">
      <div className="progress-tab-head">
        <div className="progress-tab-head-row">
          <span className="progress-tab-title">进度</span>
          <span className="progress-tab-counts">{doneCount} / {totalCount}</span>
        </div>
        <div className="progress-tab-bar">
          <div className="progress-tab-bar-fill" style={{ width: pct + "%" }} />
        </div>
        <div className="progress-tab-meta">
          <span>{pct.toFixed(1)}%</span>
          <span className="progress-tab-meta-sep">·</span>
          <span>{used.toLocaleString()} / {max.toLocaleString()} tokens</span>
        </div>
      </div>

      {steps.length === 0 ? (
        <div className="progress-tab-empty">
          <div className="progress-tab-empty-text">暂无任务进度</div>
          <div className="progress-tab-empty-hint">在主聊天区发送消息后，任务进度会出现在这里。</div>
          <div className="progress-tab-empty-actions">
            <button
              type="button"
              className="btn-secondary"
              onClick={() => {
                pushStep({ label: "示例步骤", status: "pending" });
                pushStep({ label: "另一个步骤", status: "pending" });
              }}
            >
              插入示例
            </button>
          </div>
        </div>
      ) : (
        <ol className="progress-step-list">
          {steps.map((s, i) => <StepRow key={s.id} step={s} idx={i} />)}
        </ol>
      )}

      <div className="progress-tab-foot">
        {running ? (
          <button type="button" className="btn-secondary" onClick={endRun}>
            结束任务
          </button>
        ) : (
          <button type="button" className="btn-ghost" onClick={reset}>
            <IconClose size={12} /> 清空
          </button>
        )}
      </div>
    </div>
  );
}
