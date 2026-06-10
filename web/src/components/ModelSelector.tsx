// Read-only pill that shows the active LLM endpoint for the current org.
// Switching models from the UI is out of scope; admins configure endpoints
// on the LLM admin page. We fetch the config once on mount and remember it.
import { useEffect, useState } from "react";
import { apiGet } from "../lib/api";
import { IconBot, IconChevronDown } from "./Icons";
import { t } from "../lib/i18n";

type Llm = { id: string; name: string; base_url: string; model: string } | null;
type Config = { llm: Llm };

let _cache: Llm | null = undefined as any;

export function ModelSelector() {
  const [llm, setLlm] = useState<Llm>(_cache ?? null);
  useEffect(() => {
    if (_cache !== undefined) return;
    apiGet<Config>("/client/config")
      .then((c) => {
        _cache = c.llm ?? null;
        setLlm(_cache);
      })
      .catch(() => {
        _cache = null;
        setLlm(null);
      });
  }, []);

  const label = llm ? (llm.name || llm.model || t("chat.model.label")) : t("chat.model.label");
  return (
    <button type="button" className="model-pill" title={llm ? `${llm.model} @ ${llm.base_url}` : label} disabled>
      <span className="model-pill-icon"><IconBot size={14} /></span>
      <span className="model-pill-text">{label}</span>
      <span className="model-pill-caret"><IconChevronDown size={12} /></span>
    </button>
  );
}
