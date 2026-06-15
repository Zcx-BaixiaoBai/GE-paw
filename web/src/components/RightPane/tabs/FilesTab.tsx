import { useEffect, useState, useCallback } from "react";
import { apiGet } from "../../../lib/api";
import { t } from "../../../lib/i18n";

type FsItem = { name: string; path: string; type: "dir" | "file"; size: number; mtime: number };
type Props = { data?: { dataSource?: "local" | "wiki" } };

export function FilesTab({ data }: Props) {
  const dataSource = data?.dataSource || "local";
  const [path, setPath] = useState(dataSource === "wiki" ? "wiki" : ".");
  const [items, setItems] = useState<FsItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true); setErr(null);
    try {
      if (dataSource === "wiki") {
        const r = await apiGet<{ items: FsItem[] }>("/client/wiki/tree?path=" + encodeURIComponent(path), true);
        setItems(r.items);
      } else {
        const r = await apiGet<{ items: FsItem[] }>("/client/fs/list?path=" + encodeURIComponent(path));
        setItems(r.items);
      }
    } catch (e: any) { setErr(e?.message || "load error"); setItems([]); }
    finally { setLoading(false); }
  }, [path, dataSource]);

  useEffect(() => { load(); }, [load]);

  function go(p: string) { setPath(p); }
  function up() {
    if (dataSource === "wiki") {
      if (path === "wiki") return;
      const parts = path.split("/").filter(Boolean);
      parts.pop();
      setPath(parts.join("/") || "wiki");
    } else {
      if (path === "." || path === "") return;
      const parts = path.split("/").filter(Boolean);
      parts.pop();
      setPath(parts.join("/") || ".");
    }
  }

  const crumbs = (dataSource === "wiki" ? path : ".").split("/").filter(Boolean);

  return (
    <div className="files-tab">
      <div className="breadcrumb">
        <span className="crumb" onClick={() => go(dataSource === "wiki" ? "wiki" : ".")}>{dataSource === "wiki" ? t("tab.wiki") : t("tab.workspace")}</span>
        {crumbs.slice(dataSource === "wiki" ? 1 : 0).map((c, i, arr) => {
          const target = (dataSource === "wiki" ? "wiki/" : "") + arr.slice(0, i + 1).join("/");
          const isLast = i === arr.length - 1;
          return (
            <span key={i} style={{ display: "contents" }}>
              <span className="sep">/</span>
              <span className="crumb" onClick={() => !isLast && go(target)} style={{ fontWeight: isLast ? 600 : 400 }}>{c}</span>
            </span>
          );
        })}
        <span style={{ flex: 1 }} />
        <span className="kbd">{dataSource === "wiki" ? t("tab.wiki") : t("tab.workspace")}</span>
        <button className="icon-btn" onClick={up} title={t("common.up")} aria-label={t("common.up")}>{"↑"}</button>
        <button className="icon-btn" onClick={load} title={t("common.refresh")} aria-label={t("common.refresh")}>{"↻"}</button>
      </div>
      {err && <div style={{ padding: 12, color: "var(--danger)" }}>{err}</div>}
      {loading && <div className="tab-loading">{t("common.loading")}</div>}
      <div className="files-list">
        {items.length === 0 && !loading && !err && <div className="tab-empty">{t("common.emptyList")}</div>}
        {items.map((it) => (
          <div key={it.path} className="files-row" onDoubleClick={() => it.type === "dir" && go(it.path)}>
            <span className="icon">{it.type === "dir" ? "📁" : "📄"}</span>
            <span className="name">{it.name}</span>
            <span className="size">{it.type === "file" ? humanSize(it.size) : ""}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function humanSize(n: number) {
  if (n < 1024) return n + " B";
  if (n < 1024 * 1024) return (n / 1024).toFixed(1) + " KB";
  return (n / 1024 / 1024).toFixed(1) + " MB";
}



