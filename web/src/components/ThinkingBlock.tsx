// Codex-style collapsed reasoning block. The assistant'\''s "thinking" is hidden
// behind a single-row summary that the user can click to expand. While the
// model is still reasoning the row shows a continuously pulsing orb; once
// reasoning finishes it transitions to a settled "已思考 Ns" summary.
import { useEffect, useState } from "react";
import { IconChevronDown, IconBot } from "./Icons";
import { t } from "../lib/i18n";

export function ThinkingBlock({ text, durationSec, streaming }: { text: string; durationSec?: number; streaming?: boolean }) {
  const [open, setOpen] = useState(false);
  const [tick, setTick] = useState(0);

  // While streaming, the row keeps a live timer so the user can see how
  // long the model has been thinking. Once the model finishes we freeze
  // on the final duration (or the value the server sent).
  useEffect(() => {
    if (!streaming) return;
    const id = setInterval(() => setTick((n) => n + 1), 200);
    return () => clearInterval(id);
  }, [streaming]);

  if (!text) return null;
  const seconds = streaming ? tick * 0.2 : (durationSec && durationSec > 0 ? durationSec.toFixed(1) : null);
  const summary = seconds
    ? t("chat.thinking.collapsed", { seconds: Number(seconds).toFixed(1) })
    : t("chat.thinking.label");

  return (
    <div className={"think-block" + (open ? " open" : "") + (streaming ? " streaming" : "")}>
      <button type="button" className="think-head" onClick={() => setOpen((v) => !v)} aria-expanded={open}>
        <span className={"think-caret" + (open ? " open" : "")}><IconChevronDown size={12} /></span>
        <span className="think-orb" aria-hidden><IconBot size={14} /></span>
        <span className="think-label">{summary}</span>
        {streaming && <span className="think-stream-pill" aria-hidden />}
      </button>
      {open && <pre className="think-body">{text}</pre>}
    </div>
  );
}
