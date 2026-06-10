// Renderer for assistant turns. Recognises <think>...</think> and
// [TOOL_CALL]{...}[/TOOL_CALL] markers embedded by the server (or a
// future streaming pipeline) and renders the body using ThinkingBlock /
// ToolCallCard so the chat surface looks like Codex.
import { ThinkingBlock } from "./ThinkingBlock";
import { ToolCallCard, type ToolStatus } from "./ToolCallCard";

type Tool = { name: string; args?: Record<string, any>; result?: any; status: ToolStatus };

export type AssistantParts = {
  text: string;
  thinking?: string;
  tools?: Tool[];
};

const THINK_RE = /<think>([\s\S]*?)<\/think>/g;
const TOOL_RE = /\[TOOL_CALL\]([\s\S]*?)\[\/TOOL_CALL\]/g;

export function parseAssistant(content: string): AssistantParts {
  let text = content || "";
  let thinking: string | undefined;
  const tools: Tool[] = [];

  // Extract thinking blocks first.
  const thinkMatches: string[] = [];
  text = text.replace(THINK_RE, (_m, g1) => { thinkMatches.push(g1.trim()); return ""; });
  if (thinkMatches.length) thinking = thinkMatches.join("\\n\\n");

  // Extract tool call markers.
  text = text.replace(TOOL_RE, (_m, g1) => {
    try {
      const obj = JSON.parse(g1);
      tools.push({
        name: String(obj.name || obj.tool || "tool"),
        args: obj.args || obj.arguments,
        result: obj.result,
        status: (obj.status as ToolStatus) || "ok",
      });
    } catch {
      tools.push({ name: "tool", args: { raw: g1 }, status: "ok" });
    }
    return "";
  });

  return { text: text.trim(), thinking, tools: tools.length ? tools : undefined };
}

export function AssistantMsg({ content, tokensIn, tokensOut }: { content: string; tokensIn?: number; tokensOut?: number }) {
  const parts = parseAssistant(content);
  return (
    <div className="msg-assistant">
      {parts.thinking && <ThinkingBlock text={parts.thinking} />}
      {parts.tools && parts.tools.map((tool, i) => <ToolCallCard key={i} {...tool} />)}
      {parts.text && <div className="msg-bubble msg-bubble-assistant">{parts.text}</div>}
      {(tokensIn || tokensOut) ? <div className="msg-meta">in {tokensIn || 0} / out {tokensOut || 0}</div> : null}
    </div>
  );
}
