import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { apiGet, apiPost } from "../lib/api";

type Msg = { id?: string; role: "user" | "assistant" | "system"; content: string; tokens_in?: number; tokens_out?: number };

export function AssistantPage() {
  const [params, setParams] = useSearchParams();
  const sessionId = params.get("session") || "";
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [tokens, setTokens] = useState({ in: 0, out: 0 });
  const scroller = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!sessionId) {
      apiPost<any>("/client/sessions", { title: "New session" }).then((s) => setParams({ session: s.id }));
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
      setMessages((m) => [...m, { role: "assistant", content: r.reply || "(no response)" }]);
      setTokens((t) => ({ in: t.in + (r.tokens_in || 0), out: t.out + (r.tokens_out || 0) }));
    } catch (e: any) {
      setMessages((m) => [...m, { role: "system", content: "Error: " + (e?.message || "unknown") }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", flex: 1, minHeight: 0 }}>
      <div className="chat-area" ref={scroller}>
        {messages.length === 0 && <div className="tab-empty">Send a message to start.</div>}
        {messages.map((m, i) => (
          <div key={i} className={"chat-msg " + m.role}>
            <div className="role">{m.role}</div>
            <div className="bubble">{m.content}</div>
          </div>
        ))}
      </div>
      <div className="composer">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); send(); } }}
          placeholder="Type a message (Ctrl+Enter to send)"
        />
        <button className="primary" disabled={busy || !input.trim()} onClick={send}>{busy ? "Sending..." : "Send"}</button>
        <span className="kbd" title="Total tokens this session">in {tokens.in} / out {tokens.out}</span>
      </div>
    </div>
  );
}
