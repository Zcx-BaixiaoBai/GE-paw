import { useEffect, useState } from "react";
import { apiGet } from "../../../lib/api";

type DiffData = {
  left: string;
  right: string;
  ratio: number;
  diff: string;
  left_size: number;
  right_size: number;
};
type Props = { data?: { left?: string; right?: string; initialDiff?: DiffData } };

export function DiffTab({ data }: Props) {
  const [left, setLeft] = useState<string>(data?.left || "wiki/overview.md");
  const [right, setRight] = useState<string>(data?.right || "wiki/index.md");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [result, setResult] = useState<DiffData | null>(data?.initialDiff || null);

  useEffect(() => {
    if (data?.left) setLeft(data.left);
    if (data?.right) setRight(data.right);
    if (data?.initialDiff) setResult(data.initialDiff);
  }, [data?.left, data?.right, data?.initialDiff]);

  async function run() {
    setBusy(true); setErr(null);
    try {
      const r = await apiGet<DiffData>("/client/diff?left=" + encodeURIComponent(left) + "&right=" + encodeURIComponent(right));
      setResult(r);
    } catch (e: any) {
      setErr(e?.message || "diff failed");
      setResult(null);
    } finally { setBusy(false); }
  }

  useEffect(() => { if (!result && !err) run(); /* auto-load on mount */ }, []);

  return (
    <div className="diff-tab">
      <div className="diff-toolbar">
        <label>Left</label>
        <input value={left} onChange={(e) => setLeft(e.target.value)} />
        <label>Right</label>
        <input value={right} onChange={(e) => setRight(e.target.value)} />
        <button className="primary" disabled={busy} onClick={run}>{busy ? "Diffing..." : "Compare"}</button>
      </div>
      {err && <div className="diff-err">{err}</div>}
      {result && (
        <>
          <div className="diff-meta">
            <span className="kbd">{result.left}</span>
            <span>vs</span>
            <span className="kbd">{result.right}</span>
            <span className="spacer" />
            <span className="kbd">similarity {Math.round(result.ratio * 100)}%</span>
          </div>
          <pre className="diff-body">{result.diff || "(no differences)"}</pre>
        </>
      )}
      {!result && !err && !busy && <div className="tab-empty">Pick two wiki files to compare.</div>}
    </div>
  );
}
