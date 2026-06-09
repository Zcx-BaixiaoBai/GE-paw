import { useEffect, useState } from "react";
import { apiPost } from "../lib/api";
import { usePaneStore } from "../stores/tabs";

type Citation = { path: string; snippet: string; score: number };
type QnAResult = { answer: string; citations: Citation[]; tokens_in: number; tokens_out: number; latency_ms: number };
type QnAHistory = { id: number; query: string; tokens_in: number; tokens_out: number; latency_ms: number; created_at: string };

export function QnAPage() {
  const [question, setQuestion] = useState("");
  const [busy, setBusy] = useState(false);
  const [last, setLast] = useState<QnAResult | null>(null);
  const [history, setHistory] = useState<QnAHistory[]>([]);
  const addTab = usePaneStore((s) => s.add);

  useEffect(() => {
    addTab({ kind: "files", title: "Wiki files", dataSource: "wiki" });
    addTab({ kind: "web", title: "Wiki preview", data: { initialUrl: "/api/client/wiki/preview?path=wiki" } });
  }, []);

  async function ask() {
    const q = question.trim();
    if (!q || busy) return;
    setBusy(true); setLast(null);
    try {
      const r = await apiPost<QnAResult>("/client/wiki/query", { question: q });
      setLast(r);
      setHistory((h) => [{ id: Date.now(), query: q, tokens_in: r.tokens_in, tokens_out: r.tokens_out, latency_ms: r.latency_ms, created_at: new Date().toISOString() }, ...h].slice(0, 50));
    } catch (e: any) {
      setLast({ answer: "Error: " + (e?.message || "unknown"), citations: [], tokens_in: 0, tokens_out: 0, latency_ms: 0 });
    } finally {
      setBusy(false);
    }
  }

  function openInFiles(c: Citation) {
    addTab({ kind: "files", title: "Wiki - " + c.path, dataSource: "wiki" });
    addTab({ kind: "web", title: "Preview - " + c.path, data: { initialUrl: "/api/client/wiki/preview?path=" + encodeURIComponent(c.path) } });
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", flex: 1, minHeight: 0 }}>
      <div className="chat-area">
        <div style={{ fontSize: 11, color: "var(--fg-muted)", marginBottom: 8 }}>
          <span className="kbd">Q&amp;A</span> Ask about the org wiki corpus. Server-side, no caching.
        </div>
        {last && (
          <div className="chat-msg assistant">
            <div className="role">assistant</div>
            <div className="bubble">{last.answer || "(no answer)"}</div>
            <div className="chat-meta">tokens in {last.tokens_in} / out {last.tokens_out} - {last.latency_ms}ms</div>
          </div>
        )}
        {last && last.citations.length > 0 && (
          <div className="admin-card">
            <div style={{ fontWeight: 600, marginBottom: 6 }}>Citations ({last.citations.length})</div>
            {last.citations.map((c, i) => (
              <div key={i} className="files-row" onClick={() => openInFiles(c)} title="Open in side panel">
                <span className="icon">{"📄"}</span>
                <span className="name">{c.path}</span>
                <span className="size">score {c.score}</span>
              </div>
            ))}
          </div>
        )}
        {history.length > 1 && (
          <div className="admin-card">
            <div style={{ fontWeight: 600, marginBottom: 6 }}>Recent questions</div>
            {history.slice(0, 10).map((h) => (
              <div key={h.id} className="files-row" onClick={() => setQuestion(h.query)}>
                <span className="icon">{"💬"}</span>
                <span className="name">{h.query}</span>
                <span className="size">{new Date(h.created_at).toLocaleTimeString()}</span>
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="composer">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); ask(); } }}
          placeholder="Ask a question (Ctrl+Enter to submit)"
        />
        <button className="primary" disabled={busy || !question.trim()} onClick={ask}>{busy ? "Asking..." : "Ask"}</button>
      </div>
    </div>
  );
}
