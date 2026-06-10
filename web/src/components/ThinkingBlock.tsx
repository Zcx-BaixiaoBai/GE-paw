// Codex-style collapsed reasoning block. The assistant's "thinking" is hidden
// behind a single-row summary that the user can click to expand. The
// collapsed row has a continuously pulsing dot (think-pulse) so the user
// can tell the model is still reasoning.
import { useState } from "react";
import { IconChevronDown, IconBot } from "./Icons";
import { t } from "../lib/i18n";

export function ThinkingBlock({ text, durationSec }: { text: string; durationSec?: number }) {
  const [open, setOpen] = useState(false);
  if (!text) return null;
  const summary = durationSec && durationSec > 0
    ? t("chat.thinking.collapsed", { seconds: durationSec.toFixed(1) })
    : t("chat.thinking.label");
  return (
    <div className={"think-block" + (open ? " open" : "")}>
      <button type="button" className="think-head" onClick={() => setOpen((v) => !v)}>
        <span className={"think-caret" + (open ? " open" : "")}><IconChevronDown size={12} /></span>
        <span className="think-orb" aria-hidden><IconBot size={14} /></span>
        <span className="think-label">{summary}</span>
      </button>
      {open && <pre className="think-body">{text}</pre>}
    </div>
  );
}
