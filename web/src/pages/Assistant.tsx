// Assistant page (Codex-style composer).
// - ThreadHeader is rendered by AppLayout, not here.
// - A toolbar above the textarea toggles the inline Goals / Plan drawers.
// - The composer is a single rounded card with send / stop actions.
import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { apiGet, apiPost } from "../lib/api";
import { useSessionStore, type PermissionMode } from "../stores/session";
import { usePaneStore } from "../stores/tabs";
import { AssistantMsg } from "../components/AssistantMsg";
import { GoalDrawer } from "../components/GoalDrawer";
import { PlanDrawer } from "../components/PlanDrawer";
import { ModelSelector } from "../components/ModelSelector";
import { PermissionSelector } from "../components/PermissionSelector";
import { IconSend, IconClose, IconGoals, IconPlan } from "../components/Icons";
import { t } from "../lib/i18n";

type Msg = { id?: string; role: "user" | "assistant" | "system"; content: string; tokens_in?: number; tokens_out?: number };

export function AssistantPage() {
  const [params, setParams] = useSearchParams();
  const sessionId = params.get("session") || "";
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [tokens, setTokens] = useState({ in: 0, out: 0 });
  const [showGoals, setShowGoals] = useState(false);
  const [showPlan, setShowPlan] = useState(false);
  const scroller = useRef<HTMLDivElement>(null);
  const taRef = useRef<HTMLTextAreaElement>(null);
  const upsert = useSessionStore((s) => s.upsert);
  const session = useSessionStore((s) => (sessionId ? s.byId[sessionId] : null));
  const setPermission = useSessionStore((s) => s.setPermission);
  const paneOpen = usePaneStore((s) => s.open);

  useEffect(() => {
    if (!sessionId) {
      apiPost<any>("/client/sessions", { title: t("left.newSession") }).then((s) => {
        upsert(s);
        setParams({ session: s.id });
      });
      return;
    }
    apiGet<Msg[]>("/client/sessions/" + sessionId + "/messages").then(setMessages).catch(() => setMessages([]));
  }, [sessionId]);

  useEffect(() => { scroller.current?.scrollTo({ top: 1e9, behavior: "smooth" }); }, [messages]);

  async function send() {
    const text = input.trim();
    if (!text || busy) return;
    setInput("");
    setBusy(true);
    setMessages((m) => [...m, { role: "user", content: text }]);
    try {
      const r = await apiPost<any>("/client/chat", { session_id: sessionId, message: text });
      setMessages((m) => [...m, { role: "assistant", content: r.reply || t("chat.noResponse") }]);
      setTokens((tk) => ({ in: tk.in + (r.tokens_in || 0), out: tk.out + (r.tokens_out || 0) }));
    } catch (e: any) {
      setMessages((m) => [...m, { role: "system", content: t("chat.errorPrefix") + " " + (e?.message || t("error.unknown")) }]);
    } finally {
      setBusy(false);
      taRef.current?.focus();
    }
  }

  function stop() {
    setBusy(false);
  }

  async function changePermission(next: PermissionMode) {
    if (!sessionId) return;
    try { await setPermission(sessionId, next); } catch { /* surface via store */ }
  }

  return (
    <div className="chat-page">
      <div className="chat-area" ref={scroller}>
        {messages.length === 0 ? (
          <div className="chat-welcome">
            <h1 className="chat-welcome-title">{t("chat.welcome.title")}</h1>
            <div className="chat-welcome-sub">{t("chat.welcome.sub")}</div>
            <div className="chat-welcome-hint">{t("chat.welcome.hint")}</div>
          </div>
        ) : (
          messages.map((m, i) => (
            <div key={i} className={"msg msg-" + m.role}>
              <div className="msg-role">{m.role}</div>
              {m.role === "assistant"
                ? <AssistantMsg content={m.content} tokensIn={m.tokens_in} tokensOut={m.tokens_out} />
                : <div className={"msg-bubble msg-bubble-" + m.role}>{m.content}</div>}
            </div>
          ))
        )}
      </div>

      {showGoals && sessionId && (
        <GoalDrawer sessionId={sessionId} onClose={() => setShowGoals(false)} />
      )}
      {showPlan && sessionId && (
        <PlanDrawer sessionId={sessionId} onClose={() => setShowPlan(false)} />
      )}

      <div className="composer-wrap">
        <div className="composer-toolbar">
          <button type="button" className={"composer-tool" + (showGoals ? " active" : "")} onClick={() => setShowGoals((v) => !v)} title={t("chat.drawer.goals")}>
            <IconGoals size={13} />
            <span>{t("chat.drawer.goals")}</span>
          </button>
          <button type="button" className={"composer-tool" + (showPlan ? " active" : "")} onClick={() => setShowPlan((v) => !v)} title={t("chat.drawer.plan")}>
            <IconPlan size={13} />
            <span>{t("chat.drawer.plan")}</span>
          </button>
          <span className="composer-tool-spacer" />
          <ModelSelector />
          <PermissionSelector value={session?.permission ?? null} onChange={changePermission} />
          {paneOpen && null}
        </div>
        <div className="composer">
          <textarea
            ref={taRef}
            className="composer-textarea"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); send(); }
            }}
            placeholder={t("chat.placeholder")}
            rows={1}
          />
          <div className="composer-actions">
            <span className="composer-tool-tokens" title={t("chat.tokensTip")}>
              in {tokens.in} / out {tokens.out}
            </span>
            <span className="composer-actions-spacer" />
            {busy ? (
              <button type="button" className="composer-send" onClick={stop} title={t("chat.stop")}>
                <IconClose size={13} /> {t("chat.stop")}
              </button>
            ) : (
              <button type="button" className="composer-send" disabled={!input.trim()} onClick={send} title={t("chat.send")}>
                <IconSend size={13} /> {t("chat.send")}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
