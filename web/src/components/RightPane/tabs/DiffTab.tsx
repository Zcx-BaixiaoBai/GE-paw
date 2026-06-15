import { useEffect, useState } from "react";
import { apiGet } from "../../../lib/api";
import { t } from "../../../lib/i18n";

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
      setErr(e?.message || t("plan.failed"))
      setResult(null);
    } finally { setBusy(false); }
  }

  useEffect(() => { if (!result && !err) run(); /* auto-load on mount */ }, []);

  return (
    <div className="diff-tab">
      <div className="diff-toolbar">
        <label>{t("common.left")}</label>
        <input value={left} onChange={(e) => setLeft(e.target.value)} />
        <label>{t("common.right")}</label>
        <input value={right} onChange={(e) => setRight(e.target.value)} />
        <button className="primary" disabled={busy} onClick={run}>{busy ? t("common.diffing") : t("common.compare")}</button>
      </div>
      {err && <div className="diff-err">{err}</div>}
      {result && (
        <>
          <div className="diff-meta">
            <span className="kbd" title={result.left}>{result.left}</span>
            <span className="diff-vs">{t("common.vs")}</span>
            <span className="kbd" title={result.right}>{result.right}</span>
            <span className="spacer" />
            <span className="kbd">{t("common.similar", { pct: Math.round(result.ratio * 100) })}</span>
          </div>
          <pre className="diff-body">{result.diff || t("common.noDiff")}</pre>
        </>
      )}
      {!result && !err && !busy && <div className="tab-empty">{t("tab.diff.empty")}</div>}
    </div>
  );
}



