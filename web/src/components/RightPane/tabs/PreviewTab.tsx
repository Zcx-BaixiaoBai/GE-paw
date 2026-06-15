import { useEffect, useState } from "react";
import { apiGet } from "../../../lib/api";
import { t } from "../../../lib/i18n";

type PreviewData = {
  path: string;
  size: number;
  lines: number;
  words: number;
  headline: string;
  preview_url: string;
  file_url: string;
  snippet: string;
};
type Props = { data?: { path?: string } };

export function PreviewTab({ data }: Props) {
  const [path, setPath] = useState<string>(data?.path || "wiki/overview.md");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [meta, setMeta] = useState<PreviewData | null>(null);

  async function load() {
    setBusy(true); setErr(null);
    try {
      const r = await apiGet<PreviewData>("/client/preview-data?path=" + encodeURIComponent(path));
      setMeta(r);
    } catch (e: any) {
      setErr(e?.message || t("common.error.unknown"))
      setMeta(null);
    } finally { setBusy(false); }
  }
  useEffect(() => { load(); }, [path]);

  return (
    <div className="preview-tab">
      <div className="preview-toolbar">
        <label>{t("common.path")}</label>
        <input value={path} onChange={(e) => setPath(e.target.value)} />
        <button className="primary" disabled={busy} onClick={load}>{busy ? t("common.loading") : t("common.reload")}</button>
      </div>
      {err && <div className="preview-err">{err}</div>}
      {meta && (
        <>
          <div className="preview-meta">
            <div className="preview-headline">{meta.headline}</div>
            <div className="preview-stats">
              <span className="kbd">{meta.path}</span>
              <span>{meta.lines} lines</span>
              <span>{meta.words} words</span>
              <span>{humanSize(meta.size)}</span>
            </div>
          </div>
          <iframe className="preview-frame" src={meta.preview_url} sandbox="allow-same-origin" referrerPolicy="no-referrer" />
        </>
      )}
      {!meta && !err && !busy && <div className="tab-empty">{t("tab.preview.empty")}</div>}
    </div>
  );
}

function humanSize(n: number): string {
  if (n < 1024) return n + " B";
  if (n < 1024 * 1024) return (n / 1024).toFixed(1) + " KB";
  return (n / 1024 / 1024).toFixed(1) + " MB";
}


