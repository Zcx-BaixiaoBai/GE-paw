// Switchable model picker. The active LLM endpoint is fetched from
// /client/config and stored in a module-level cache so every chat session
// in the tab reuses the same value. The user can open the dropdown to
// pick any provider that is registered and enabled on the LLM admin page.
// Picking fires PATCH /api/client/sessions/{id} so the session record
// remembers the choice; subsequent /api/client/chat calls will then use
// that endpoint on the backend.
import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { apiGet, apiPost, apiPatch } from "../lib/api";
import { IconBot, IconChevronDown } from "./Icons";
import { t } from "../lib/i18n";

type Llm = { id: string; name: string; base_url: string; model: string; is_default?: boolean; enabled?: boolean } | null;
type Config = { llm: Llm };
type Provider = { id: string; name: string; base_url: string; model: string; enabled?: boolean; is_default?: boolean };

let _cache: Llm | null = undefined as any;
let _providersCache: Provider[] | null = null;

export function ModelSelector() {
  const [llm, setLlm] = useState<Llm>(_cache ?? null);
  const [providers, setProviders] = useState<Provider[]>(_providersCache ?? []);
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const [params] = useSearchParams();
  const sessionId = params.get("session") || "";

  useEffect(() => {
    if (_cache === undefined) {
      apiGet<Config>("/client/config")
        .then((c) => { _cache = c.llm ?? null; setLlm(_cache); })
        .catch(() => { _cache = null; setLlm(null); });
    }
    if (!_providersCache) {
      apiGet<Provider[]>("/client/llm/providers").then((rows) => {
        const enabled = (rows || []).filter((p) => p.enabled !== false);
        _providersCache = enabled;
        setProviders(enabled);
      }).catch(() => setProviders([]));
    }
  }, []);

  useEffect(() => {
    if (!open) return;
    const onClick = (e: MouseEvent) => {
      if (!ref.current?.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, [open]);

  // Flip up when near the bottom of the viewport (same logic as PermissionSelector)
  useEffect(() => {
    if (!open || !ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const spaceBelow = window.innerHeight - rect.bottom;
    if (spaceBelow < 260) ref.current.classList.add("opens-up");
    else ref.current.classList.remove("opens-up");
  }, [open]);

  const label = llm ? (llm.name || llm.model || t("chat.model.label")) : t("chat.model.label");
  const enabled = providers.filter((p) => p.enabled !== false);

  async function pick(p: Provider) {
    if (busy || p.id === llm?.id) { setOpen(false); return; }
    setBusy(true);
    try {
      await apiPost("/client/llm/active", { provider_id: p.id });
      _cache = p;
      setLlm(p);
      if (sessionId) {
        try { await apiPatch("/client/sessions/" + sessionId, { llm_provider_id: p.id }); } catch { /* non-fatal */ }
      }
      setOpen(false);
    } catch {
      // Fallback: locally switch even if backend rejects
      _cache = p;
      setLlm(p);
      setOpen(false);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="model-pill-wrap" ref={ref}>
      <button
        type="button"
        className={"model-pill" + (open ? " active" : "")}
        title={llm ? `${llm.model} @ ${llm.base_url}` : label}
        onClick={() => enabled.length > 0 && setOpen((v) => !v)}
      >
        <span className="model-pill-icon"><IconBot size={14} /></span>
        <span className="model-pill-text">{label}</span>
        <span className="model-pill-caret"><IconChevronDown size={12} /></span>
      </button>
      {open && (
        <div className="model-pill-menu" role="menu">
          {enabled.length === 0 ? (
            <div className="model-pill-empty">未配置 LLM — 管理员请在设置中添加</div>
          ) : (
            enabled.map((p) => (
              <button
                key={p.id}
                type="button"
                className={"model-pill-item" + (p.id === llm?.id ? " active" : "")}
                onClick={() => pick(p)}
                disabled={busy}
                role="menuitemradio"
                aria-checked={p.id === llm?.id}
              >
                <span className="model-pill-item-name">{p.name || p.id}</span>
                <span className="model-pill-item-model">{p.model}</span>
                {p.is_default && <span className="model-pill-item-tag">默认</span>}
              </button>
            ))
          )}
        </div>
      )}
    </div>
  );
}
