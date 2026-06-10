// Q&A page: ask a question against the org wiki. Server-side retrieval with
// citations that can be opened in the right-pane Files/Web tabs.
import { useEffect, useState } from "react";
import { apiPost } from "../lib/api";
import { usePaneStore } from "../stores/tabs";
import { t } from "../lib/i18n";

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
    addTab({ kind: "files", title: t("tab.files"), dataSource: "wiki" });
    addTab({ kind: "web", title: t("tab.preview"), data: { initialUrl: "/api/client/wiki/preview?path=wiki" } });
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
      setLast({ answer: t("chat.errorPrefix") + " " + (e?.message || t("error.unknown")), citations: [], tokens_in: 0, tokens_out: 0, latency_ms: 0 });
    } finally {
      setBusy(false);
    }
  }

  function openInFiles(c: Citation) {
    addTab({ kind: "files", title: t("tab.files") + " - " + c.path, dataSource: "wiki" });
    addTab({ kind: "web", title: t("tab.preview") + " - " + c.path, data: { initialUrl: "/api/client/wiki/preview?path=" + encodeURIComponent(c.path) } });
  }

  return (
    <div className="chat-page">
      <div className="chat-area">
        <div className="chat-welcome">
          <h1 className="chat-welcome-title">{t("qna.badge")}</h1>
          <div className="chat-welcome-sub">{t("qna.intro")}</div>
        </div>
        {last && (
          <div className="msg msg-assistant">
            <Assistant content={last.answer} tokensIn={last.tokens_in} tokensOut={last.tokens_out} latency={last.latency_ms} />
          </div>
        )}
        {last && last.citations.length > 0 && (
          <div className="admin-card">
            <div className="admin-card-title">{t("qna.citations")} ({last.citations.length})</div>
            {last.citations.map((c, i) => (
              <div key={i} className="files-row" onClick={() => openInFiles(c)} title={t("qna.openInFiles")}>
                <span className="name">{c.path}</span>
                <span className="size">{t("qna.score", { score: c.score })}</span>
              </div>
            ))}
          </div>
        )}
        {history.length > 0 && (
          <div className="admin-card">
            <div className="admin-card-title">{t("qna.recent")}</div>
            {history.slice(0, 10).map((h) => (
              <div key={h.id} className="files-row" onClick={() => setQuestion(h.query)}>
                <span className="name">{h.query}</span>
                <span className="size">{new Date(h.created_at).toLocaleTimeString()}</span>
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="composer-wrap">
        <div className="composer">
          <textarea
            className="composer-textarea"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); ask(); } }}
            placeholder={t("qna.placeholder")}
          />
          <div className="composer-actions">
            <span className="composer-actions-spacer" />
            <button type="button" className="composer-send" disabled={busy || !question.trim()} onClick={ask}>
              {busy ? t("qna.asking") : t("qna.ask")}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function Assistant({ content, tokensIn, tokensOut, latency }: { content: string; tokensIn: number; tokensOut: number; latency: number }) {
  return (
    <>
      <div className="msg-bubble msg-bubble-assistant">{content || t("qna.empty.answer")}</div>
      <div className="msg-meta">in {tokensIn} / out {tokensOut} {"·"} {latency}ms</div>
    </>
  );
}
