import { useState } from "react";
type Props = { data?: { initialUrl?: string } };
export function WebTab({ data }: Props) {
  const [url, setUrl] = useState(data?.initialUrl || "about:blank");
  const [input, setInput] = useState(url);
  return (
    <div className="web-tab">
      <form className="addr" onSubmit={(e) => { e.preventDefault(); setUrl(input); }}>
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="https://..." />
        <button type="submit">Go</button>
        <button type="button" onClick={() => setUrl((u) => u + "#" + Date.now())}>{"↻"}</button>
      </form>
      <iframe title="web-tab" src={url} sandbox="allow-scripts allow-same-origin allow-forms" referrerPolicy="no-referrer" />
    </div>
  );
}
