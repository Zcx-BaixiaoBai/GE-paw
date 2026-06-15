// Assistant page (Codex-style composer).
// Design notes (6/12 refactor):
//   - The composer is a single rounded card, not a 5-button toolbar + card.
//   - Tool selection is inline (slash menu) and a single "more" (...) button
//     for less-common affordances (computer use, drawer toggles).
//   - Model and permission are tiny pills at the bottom-left of the card;
//     they only surface when relevant, not as a permanent bar.
//   - The drawer toggles (goals/plan) are slash commands (/goals, /plan).
import { useEffect, useRef, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { apiGet, apiPost } from "../lib/api";
import { useSessionStore, type PermissionMode } from "../stores/session";
import { usePaneStore } from "../stores/tabs";
import { AssistantMsg } from "../components/AssistantMsg";
import { GoalDrawer } from "../components/GoalDrawer";
import { PlanDrawer } from "../components/PlanDrawer";
import { ModelSelector } from "../components/ModelSelector";
import { PermissionSelector } from "../components/PermissionSelector";
import { IconSend, IconClose, IconPlus, IconMonitor, IconMore } from "../components/Icons";
import { useComputerUseStore } from "../stores/computerUse.tsx";
import { SlashMenu, type SlashContext } from "../components/SlashMenu";
import { useSettingsStore } from "../stores/settings";
import { useProgressStore } from "../stores/progress";
import { t } from "../lib/i18n";

type Msg = { id?: string; role: "user" | "assistant" | "system"; content: string; tokens_in?: number; tokens_out?: number };

// Tiny "more" overflow menu — mirrors the Codex 3-dot affordance. Hosts
// computer use + drawer toggles so the main composer stays clean.
function ComposerMore({ onOpenGoal, onOpenPlan, onOpenComputerUse, cuEnabled }: {
  onOpenGoal: () => void;
  onOpenPlan: () => void;
  onOpenComputerUse: () => void;
  cuEnabled: boolean;
}) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!open) return;
    const close = (e: MouseEvent) => {
      if (!ref.current?.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, [open]);
  return (
    <div className="composer-more" ref={ref}>
      <button
        type="button"
        className="composer-more-btn"
        title={t("chat.more")}
        aria-label={t("chat.more")}
        onClick={() => setOpen((v) => !v)}
      >
        <IconMore size={14} />
      </button>
      {open && (
        <div className="composer-more-menu" role="menu">
          <button
            type="button"
            className="composer-more-item"
            onClick={() => { setOpen(false); onOpenComputerUse(); }}
            disabled={!cuEnabled}
            title={cuEnabled ? t("composer.plus.computerUseHint") : t("composer.plus.computerUseDisabled")}
          >
            <IconMonitor size={13} />
            <span>{t("composer.plus.computerUse")}</span>
          </button>
          <button type="button" className="composer-more-item" onClick={() => { setOpen(false); onOpenGoal(); }}>
            <span className="composer-more-dot" />
            <span>{t("chat.drawer.goals")}</span>
          </button>
          <button type="button" className="composer-more-item" onClick={() => { setOpen(false); onOpenPlan(); }}>
            <span className="composer-more-dot" />
            <span>{t("chat.drawer.plan")}</span>
          </button>
        </div>
      )}
    </div>
  );
}

export function AssistantPage() {
  const [params, setParams] = useSearchParams();
  const sessionId = params.get("session") || "";
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [tokens, setTokens] = useState({ in: 0, out: 0 });
  const [showGoals, setShowGoals] = useState(false);
  const [showPlan, setShowPlan] = useState(false);
  const [loadTick, setLoadTick] = useState(0);
  const [slashOpen, setSlashOpen] = useState(false);
  const [slashQuery, setSlashQuery] = useState("");
  const scroller = useRef<HTMLDivElement>(null);
  const taRef = useRef<HTMLTextAreaElement>(null);
  const upsert = useSessionStore((s) => s.upsert);
  const session = useSessionStore((s) => (sessionId ? s.byId[sessionId] : null));
  const setPermission = useSessionStore((s) => s.setPermission);
  const nav = useNavigate();
  const cuEnabled = useSettingsStore((s) => s.computerUseEnabled);

  useEffect(() => {
    setMessages([]);
    setInput("");
    setBusy(false);
    setLoadTick((n) => n + 1);
    if (!sessionId) {
      apiPost<any>("/client/sessions", { title: t("left.newSession") }).then((s) => {
        upsert(s);
        setParams({ session: s.id });
      });
      return;
    }
    apiGet<Msg[]>("/client/sessions/" + sessionId + "/messages")
      .then((rows) => setMessages(Array.isArray(rows) ? rows : []))
      .catch(() => setMessages([]));
  }, [sessionId]);

  useEffect(() => { scroller.current?.scrollTo({ top: 1e9, behavior: "smooth" }); }, [messages]);

  // Auto-grow textarea to its content.
  useEffect(() => {
    const ta = taRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = Math.min(ta.scrollHeight, 220) + "px";
  }, [input]);

  async function newSession() {
    try {
      const s = await apiPost<any>("/client/sessions", { title: t("left.newSession") });
      upsert(s);
      setParams({ session: s.id });
    } catch { /* swallow */ }
  }

  async function runSlashCommand(text: string): Promise<boolean> {
    const m = text.match(/^\/(\w+)/);
    if (!m) return false;
    const cmd = m[1].toLowerCase();
    if (cmd === "new") { await newSession(); return true; }
    if (cmd === "clear") { setInput(""); return true; }
    if (cmd === "settings") { nav("/app/settings"); return true; }
    if (cmd === "goals") { setShowGoals(true); setInput(""); return true; }
    if (cmd === "plan")  { setShowPlan(true);  setInput(""); return true; }
    if (cmd === "cu") {
      if (!cuEnabled) return false;
      useComputerUseStore.getState().setRunning();
      setInput("");
      return true;
    }
    if (cmd === "help") {
      setInput("");
      setMessages((m) => [...m, { role: "system", content: "可用命令: /new /clear /settings /goals /plan /cu /model /perm" }]);
      return true;
    }
    return false;
  }

  async function send() {
    const text = input.trim();
    if (!text || busy) return;
    if (text.startsWith("/") && await runSlashCommand(text)) {
      setInput("");
      setSlashOpen(false);
      return;
    }
    setInput("");
    setBusy(true);
    setMessages((m) => [...m, { role: "user", content: text }]);
    // Drive the global progress store: kick off a run, advance through
    // the synthetic steps, and reflect the actual token delta the
    // server reports in r.tokens_in / r.tokens_out.
    const prog = useProgressStore.getState();
    prog.beginRun("执行中");
    setTimeout(() => useProgressStore.getState().nextStep(), 300);  // 解析 -> 思考
    setTimeout(() => useProgressStore.getState().nextStep(), 900);  // 思考 -> 等待响应
    try {
      const r = await apiPost<any>("/client/chat", { session_id: sessionId, message: text });
      const tin = r.tokens_in || 0;
      const tout = r.tokens_out || 0;
      setMessages((m) => [...m, { role: "assistant", content: r.reply || t("chat.noResponse") }]);
      setTokens((tk) => ({ in: tk.in + tin, out: tk.out + tout }));
      // Reflect the actual server-reported token usage on the progress bar.
      useProgressStore.setState((s) => ({
        usedTokens: s.usedTokens + tin + tout,
      }));
      setTimeout(() => useProgressStore.getState().nextStep(), 200); // 等待响应 -> 整理结果
      setTimeout(() => useProgressStore.getState().endRun(), 600);   // 整理结果 -> 完成
    } catch (e: any) {
      setMessages((m) => [...m, { role: "system", content: t("chat.errorPrefix") + " " + (e?.message || t("error.unknown")) }]);
      useProgressStore.getState().endRun();
    } finally {
      setBusy(false);
      taRef.current?.focus();
    }
  }

  function stop() { setBusy(false); }
  async function changePermission(next: PermissionMode) {
    if (!sessionId) return;
    try { await setPermission(sessionId, next); } catch { /* surface via store */ }
  }

  const canSend = !busy && input.trim().length > 0;

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
            <div key={(m.id ?? "k") + ":" + i} className={"msg msg-" + m.role}>
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
        <SlashMenu
          open={slashOpen}
          query={slashQuery}
          onPick={() => { setSlashOpen(false); setInput(""); }}
          onClose={() => setSlashOpen(false)}
          ctx={{
            navigate: (to) => nav(to),
            createSession: async () => { await newSession(); },
            clearInput: () => setInput(""),
            insertText: (t) => setInput((cur) => (cur ? cur + "\n" + t : t)),
          }}
        />
        <div className="composer-card">
          <textarea
            ref={taRef}
            className="composer-textarea"
            value={input}
            onChange={(e) => {
              const v = e.target.value;
              setInput(v);
              if (v.startsWith("/") && !v.includes(" ")) {
                setSlashOpen(true);
                setSlashQuery(v.slice(1));
              } else {
                setSlashOpen(false);
              }
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); send(); }
            }}
            placeholder={t("chat.placeholder")}
            rows={1}
          />
          <div className="composer-foot">
            <div className="composer-foot-left">
              <ModelSelector />
              <PermissionSelector value={session?.permission ?? null} onChange={changePermission} />
              <span className="composer-tokens" title={t("chat.tokensTip")}>
                in {tokens.in} / out {tokens.out}
              </span>
            </div>
            <div className="composer-foot-right">
              <ComposerMore
                cuEnabled={cuEnabled}
                onOpenComputerUse={() => useComputerUseStore.getState().setRunning()}
                onOpenGoal={() => setShowGoals(true)}
                onOpenPlan={() => setShowPlan(true)}
              />
              <button
                type="button"
                className={"composer-send" + (busy ? " busy" : "") + (canSend ? " ready" : "")}
                onClick={busy ? stop : send}
                disabled={!busy && !canSend}
                title={busy ? t("chat.stop") : t("chat.send")}
                aria-label={busy ? t("chat.stop") : t("chat.send")}
              >
                {busy ? <IconClose size={14} /> : <IconSend size={14} />}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
