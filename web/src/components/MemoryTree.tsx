// Memory panel: the agent owns the writes, the user owns the read + review.
//
// In qwenpaw's design the agent runtime writes into a layered memory file:
//   L0  outline: a 1-paragraph agent-curated summary of "what the user is about"
//   L1  topics:  short stable facts the agent has picked up (e.g. "uses zh-CN",
//                "prefers concise answers", "currently working on plugin X")
//   L2  dated:   per-day journal entries, written by the agent after each turn
//   tags:       derived keyword index, maintained automatically
//   links:      cross-references the agent has added between entries
//
// The user panel is read-mostly. They can:
//   - see what the agent knows (this view)
//   - pin items they want to keep (so the agent does not age them out)
//   - delete items they disagree with
//   - trigger an "agent summarize" run to ask the agent to refresh a topic
//
// The actual writes happen in `agentMemoryWriter` (mounted by the chat
// runtime). For the local mock we expose a `__gepawTestAgentWriteMemory` hook
// on `window` so QA scripts can simulate the agent writing without a backend.
import { useMemo, useState } from "react";
import {
  useSettingsStore,
  type MemoryEntry,
  type MemoryTopic,
  emptyMemoryEntry,
  makeMemoryId,
} from "../stores/settings";
import { t } from "../lib/i18n";

const ISO_DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

function todayISO(): string {
  return new Date().toISOString().slice(0, 10);
}

function titleOf(entry: MemoryEntry | undefined): string {
  if (!entry) return "?";
  return entry.body.split("\n", 1)[0].slice(0, 80) || entry.date;
}

function authorBadge(entry: MemoryEntry): string {
  // `author` is the agent runtime (or "user-pinned" for items the user
  // explicitly promoted). Older entries (before this field existed) are
  // treated as agent-written.
  if (entry.author === "user-pinned") return "📌 用户置顶";
  if (entry.author === "agent") return "🤖 代理写入";
  if (entry.author === "user") return "✍️ 用户补充";
  return "🤖 代理写入";
}

function authorBadgeTopic(tp: MemoryTopic): string {
  if (tp.author === "user-pinned") return "📌";
  if (tp.author === "user") return "✍️";
  return "🤖";
}

export function MemoryTree() {
  const memory = useSettingsStore((s) => s.memory);
  const removeTopic = useSettingsStore((s) => s.removeMemoryTopic);
  const pinTopic = useSettingsStore((s) => s.pinMemoryTopic);
  const upsertEntry = useSettingsStore((s) => s.upsertMemoryEntry);
  const removeEntry = useSettingsStore((s) => s.removeMemoryEntry);
  const pinEntry = useSettingsStore((s) => s.pinMemoryEntry);
  const rebuildIndex = useSettingsStore((s) => s.rebuildMemoryTagIndex);

  const [activeDate, setActiveDate] = useState<string>(() => {
    const dates = Object.keys(memory.dated).sort();
    return dates[dates.length - 1] || todayISO();
  });
  const [agentBusy, setAgentBusy] = useState(false);
  const [agentNote, setAgentNote] = useState<string | null>(null);

  const dates = useMemo(
    () => Object.keys(memory.dated).sort((a, b) => b.localeCompare(a)),
    [memory.dated],
  );
  const activeEntry = memory.dated[activeDate];
  const agentCount = useMemo(() => {
    let n = 0;
    for (const e of Object.values(memory.dated)) if (e.author !== "user-pinned" && e.author !== "user") n++;
    for (const t of memory.topics) if (t.author !== "user-pinned" && t.author !== "user") n++;
    return n;
  }, [memory]);

  async function askAgentToSummarize() {
    setAgentBusy(true);
    setAgentNote(null);
    try {
      // In a real build this would call /agent/memory/summarize which would
      // either run a model or stream a structured patch. The test hook
      // `__gepawTestAgentWriteMemory` is a local mock used for QA.
      if (typeof window !== "undefined" && (window as any).__gepawTestAgentWriteMemory) {
        await (window as any).__gepawTestAgentWriteMemory({ kind: "summary" });
        setAgentNote("代理已根据最近会话整理出 1 条 L2 日记。");
      } else {
        // No test hook — manually append a placeholder entry so the user can
        // still see the "agent wrote this" flow.
        const id = makeMemoryId();
        upsertEntry({
          id, date: todayISO(),
          body: "(代理写入) 正在与用户讨论 GE-paw 控制台的弹窗定位和记忆系统改造。",
          topicIds: [], keywords: ["GE-paw", "审计"], author: "agent", updatedAt: Date.now(),
        });
        setAgentNote("代理已写入一条手动摘要(无 test hook 模式)。");
      }
      rebuildIndex();
    } finally {
      setAgentBusy(false);
    }
  }

  async function askAgentToAddTopic() {
    setAgentBusy(true);
    setAgentNote(null);
    try {
      if (typeof window !== "undefined" && (window as any).__gepawTestAgentWriteMemory) {
        await (window as any).__gepawTestAgentWriteMemory({ kind: "topic" });
        setAgentNote("代理已添加 1 个 L1 主题。");
      } else {
        // No test hook — simulate an agent-suggested topic.
        const id = makeMemoryId();
        useSettingsStore.getState().upsertMemoryTopic({
          id, title: "用户偏好简洁回答", body: "代理根据近期对话推断,等用户确认。",
          author: "agent", updatedAt: Date.now(),
        });
        setAgentNote("代理已添加一个建议主题(无 test hook 模式)。");
      }
    } finally {
      setAgentBusy(false);
    }
  }

  return (
    <div className="memory-tree">
      <div className="mem-header">
        <div className="mem-header-stat">
          <span className="mem-stat-num">{Object.keys(memory.dated).length}</span>
          <span className="mem-stat-label">L2 日记</span>
        </div>
        <div className="mem-header-stat">
          <span className="mem-stat-num">{memory.topics.length}</span>
          <span className="mem-stat-label">L1 主题</span>
        </div>
        <div className="mem-header-stat">
          <span className="mem-stat-num">{Object.keys(memory.tags).length}</span>
          <span className="mem-stat-label">关键词</span>
        </div>
        <div className="mem-header-stat">
          <span className="mem-stat-num">{agentCount}</span>
          <span className="mem-stat-label">代理写入</span>
        </div>
        <div className="mem-spacer" />
        <button
          type="button"
          className="mem-agent-btn"
          onClick={askAgentToAddTopic}
          disabled={agentBusy}
          title="让代理根据当前会话自动总结一个稳定主题"
        >
          🤖 + 主题
        </button>
        <button
          type="button"
          className="mem-agent-btn"
          onClick={askAgentToSummarize}
          disabled={agentBusy}
          title="让代理根据最近对话整理今天的 L2 日记"
        >
          🤖 整理今天
        </button>
      </div>
      {agentNote && <div className="mem-agent-note">{agentNote}</div>}

      {/* L0 outline (agent-written; user can pin to lock it) */}
      <div className="mem-layer mem-layer-l0">
        <div className="mem-layer-head">
          <span className="mem-layer-tag">L0</span>
          <span className="mem-layer-title">{t("memory.layer.outline")}</span>
          <span className="mem-author-badge">🤖 代理维护</span>
          <span className="mem-spacer" />
          {memory.outline ? (
            <button
              type="button"
              className="mem-pin"
              onClick={() => useSettingsStore.getState().setMemoryOutline("")}
            >
              解除
            </button>
          ) : null}
        </div>
        {memory.outline ? (
          <div className="mem-outline-readonly">{memory.outline}</div>
        ) : (
          <div className="mem-empty">
            代理会在 L0 写入 1 段总结,描述它理解的"用户是谁、当前在做什么、长期偏好"。
          </div>
        )}
      </div>

      {/* L1 topics (agent-written; user can pin / remove) */}
      <div className="mem-layer mem-layer-l1">
        <div className="mem-layer-head">
          <span className="mem-layer-tag">L1</span>
          <span className="mem-layer-title">{t("memory.layer.topics")}</span>
        </div>
        {memory.topics.length === 0 ? (
          <div className="mem-empty">代理尚未写入 L1 主题。点击右上角"🤖 + 主题"让代理总结一个。</div>
        ) : (
          <ul className="mem-topic-list">
            {memory.topics.map((tp) => (
              <li key={tp.id} className={"mem-topic" + (tp.author === "user-pinned" ? " pinned" : "")}>
                <div className="mem-topic-head">
                  <span className="mem-author-badge">{authorBadgeTopic(tp)}</span>
                  <span className="mem-topic-title">{tp.title || t("memory.topic.untitled")}</span>
                  <span className="mem-spacer" />
                  <button
                    type="button"
                    className="mem-pin"
                    onClick={() => pinTopic(tp.id)}
                    title={tp.author === "user-pinned" ? "取消置顶" : "置顶后代理不会自动老化这条"}
                  >
                    {tp.author === "user-pinned" ? "已置顶" : "置顶"}
                  </button>
                  <button
                    type="button"
                    className="mem-del"
                    onClick={() => removeTopic(tp.id)}
                    title={t("admin.common.delete")}
                  >
                    ×
                  </button>
                </div>
                {tp.body && <div className="mem-topic-body">{tp.body}</div>}
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* L2 dated entries (agent-written; user can pin / remove) */}
      <div className="mem-layer mem-layer-l2">
        <div className="mem-layer-head">
          <span className="mem-layer-tag">L2</span>
          <span className="mem-layer-title">{t("memory.layer.dated")}</span>
        </div>
        <div className="mem-date-row">
          <div className="mem-date-list">
            {dates.length === 0 ? (
              <div className="mem-empty">代理尚未写入日记。点击"🤖 整理今天"让代理根据当前会话写一条。</div>
            ) : (
              dates.map((d) => (
                <button
                  type="button"
                  key={d}
                  className={"mem-date" + (d === activeDate ? " active" : "")}
                  onClick={() => setActiveDate(d)}
                  title={titleOf(memory.dated[d])}
                >
                  {d}
                </button>
              ))
            )}
          </div>
          <div className="mem-date-edit">
            <div className="mem-date-input-static">{activeDate}</div>
            {activeEntry ? (
              <>
                <div className="mem-date-head">
                  <span className="mem-author-badge">{authorBadge(activeEntry)}</span>
                  <span className="mem-spacer" />
                  <button
                    type="button"
                    className="mem-pin"
                    onClick={() => pinEntry(activeEntry.id)}
                    title={activeEntry.author === "user-pinned" ? "取消置顶" : "置顶后代理不会自动老化这条"}
                  >
                    {activeEntry.author === "user-pinned" ? "已置顶" : "置顶"}
                  </button>
                  <button
                    type="button"
                    className="mem-del"
                    onClick={() => {
                      removeEntry(activeEntry.id);
                      const next = dates.filter((d) => d !== activeDate)[0];
                      setActiveDate(next || todayISO());
                    }}
                    title={t("admin.common.delete")}
                  >
                    ×
                  </button>
                </div>
                <pre className="mem-entry-body">{activeEntry.body || "(空)"}</pre>
                {activeEntry.keywords.length > 0 && (
                  <div className="mem-keywords">
                    {activeEntry.keywords.map((k) => (
                      <span key={k} className="mem-kw">{k}</span>
                    ))}
                  </div>
                )}
                {(memory.links[activeEntry.id] || []).length > 0 && (
                  <div className="mem-keywords">
                    {(memory.links[activeEntry.id] || []).map((id) => (
                      <span key={id} className="mem-kw mem-kw-link">
                        ↪ {titleOf(memory.dated[id] || memory.topics.find((tp) => tp.id === id))}
                      </span>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <div className="mem-empty">这一天没有日记。</div>
            )}
          </div>
        </div>
      </div>

      {/* Tag index (derived) */}
      <div className="mem-layer mem-layer-tags">
        <div className="mem-layer-head">
          <span className="mem-layer-tag">tags</span>
          <span className="mem-layer-title">{t("memory.layer.tags")}</span>
        </div>
        {Object.keys(memory.tags).length === 0 ? (
          <div className="mem-empty">给日记加上关键词后会自动汇总到这里(代理会自动维护)。</div>
        ) : (
          <div className="mem-keywords mem-keywords-block">
            {Object.entries(memory.tags).map(([k, ids]) => (
              <span key={k} className="mem-kw mem-kw-static">
                {k} <span className="mem-kw-count">{ids.length}</span>
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// Read-only summary used by the chat surface to show "what the agent knows".
export function MemorySummary() {
  const memory = useSettingsStore((s) => s.memory);
  const enabled = useSettingsStore((s) => s.memoryEnabled);
  if (!enabled) return null;
  const topics = memory.topics.length;
  const dates = Object.keys(memory.dated).length;
  const keywords = Object.keys(memory.tags).length;
  return (
    <div className="memory-summary">
      {memory.outline && <div className="memory-summary-outline">{memory.outline}</div>}
      <div className="memory-summary-stats">
        <span>L0 概览{memory.outline ? "✓" : "—"}</span>
        <span>L1 主题 {topics}</span>
        <span>L2 日记 {dates}</span>
        <span>tag {keywords}</span>
      </div>
    </div>
  );
}
