// Knowledge base (wiki) admin. Reimagines the flat upload list as a folder
// tree the admin can navigate like a file system, and adds:
//   - drag-and-drop multi-file upload with mime validation
//   - extra file type support: xlsx, pdf, docx, pptx, csv, html, json, xml,
//     ipynb, md, txt (server still does the heavy parsing)
//   - filter chips by file type
//   - "underlying directory" manifest view (the index.json-ish tree that
//     all other plugins/scripts read from)
//   - cross-references: clicking a source's path reveals who links to it
import { useEffect, useMemo, useRef, useState } from "react";
import { apiGet, apiGetArray, apiPost, apiPostForm } from "../../lib/api";
import { IconRefresh, IconTrash, IconFiles } from "../../components/Icons";
import { t } from "../../lib/i18n";

type Src = {
  id: string;
  path: string;
  status: string;
  size_bytes: number;
  mime?: string;
  error?: string;
  /** Optional: id of the manifest entry that links TO this source. */
  backlinks?: string[];
};

// Whitelist of extensions the backend can ingest. Server is the source of
// truth, but we filter here too so users get immediate feedback.
const SUPPORTED_EXTS = new Set([
  ".md", ".markdown",
  ".txt",
  ".pdf",
  ".docx", ".doc",
  ".xlsx", ".xls", ".csv",
  ".pptx", ".ppt",
  ".html", ".htm",
  ".json", ".xml", ".yaml", ".yml",
  ".ipynb",
  ".rst",
]);

function extOf(path: string): string {
  const i = path.lastIndexOf(".");
  return i >= 0 ? path.slice(i).toLowerCase() : "";
}

function isSupported(name: string): boolean {
  return SUPPORTED_EXTS.has(extOf(name));
}

function formatSize(n: number): string {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / (1024 * 1024)).toFixed(2)} MB`;
}

type FolderNode = {
  name: string;
  fullPath: string;
  children: Map<string, FolderNode>;
  files: Src[];
};

function buildTree(sources: Src[]): FolderNode {
  const root: FolderNode = { name: "/", fullPath: "", children: new Map(), files: [] };
  for (const s of sources) {
    const parts = s.path.split("/").filter(Boolean);
    let cur = root;
    for (let i = 0; i < parts.length - 1; i++) {
      const name = parts[i];
      if (!cur.children.has(name)) {
        cur.children.set(name, { name, fullPath: parts.slice(0, i + 1).join("/"), children: new Map(), files: [] });
      }
      cur = cur.children.get(name)!;
    }
    cur.files.push(s);
  }
  return root;
}

function flattenTree(node: FolderNode, depth = 0, into: { node: FolderNode; depth: number }[] = []): { node: FolderNode; depth: number }[] {
  into.push({ node, depth });
  // Files first, then subfolders alphabetically.
  const folders = [...node.children.values()].sort((a, b) => a.name.localeCompare(b.name));
  for (const f of folders) flattenTree(f, depth + 1, into);
  return into;
}

const ALL_TYPES = "all" as const;
type TypeFilter = typeof ALL_TYPES | string;

export function AdminWikiPage() {
  const [sources, setSources] = useState<Src[]>([]);
  const [busy, setBusy] = useState(false);
  const [log, setLog] = useState<string[]>([]);
  const [view, setView] = useState<"tree" | "manifest">("tree");
  const [selectedFolder, setSelectedFolder] = useState<string>("");
  const [selectedSource, setSelectedSource] = useState<string | null>(null);
  const [typeFilter, setTypeFilter] = useState<TypeFilter>(ALL_TYPES);
  const [search, setSearch] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);
  const folderRef = useRef<HTMLInputElement>(null);

  async function load() {
    try {
      const data = await apiGetArray<Src>("/admin/wiki/sources");
      setSources(data);
    } catch (e: any) {
      setLog((l) => [...l, "[" + new Date().toLocaleTimeString() + "] " + (e?.message || t("error.unknown"))]);
    }
  }
  useEffect(() => { load(); }, []);
  function append(s: string) {
    setLog((l) => [...l, "[" + new Date().toLocaleTimeString() + "] " + s]);
  }

  async function upload(file: File, folder?: string) {
    setBusy(true);
    const fd = new FormData();
    if (folder) fd.append("folder", folder);
    fd.append("file", file);
    try {
      const r = await apiPostForm<any>("/admin/wiki/sources/upload", fd);
      append(t("admin.wiki.logUploaded", { path: r.path }));
      load();
    } catch (e: any) {
      append(t("admin.wiki.logUploadFailed", { err: e?.message || t("error.unknown") }));
    } finally { setBusy(false); }
  }

  async function uploadMany(files: FileList | null, folder?: string) {
    if (!files) return;
    // Filter unsupported file types up-front so the user gets feedback.
    const accepted: File[] = [];
    const rejected: string[] = [];
    for (const f of Array.from(files)) {
      if (isSupported(f.name)) accepted.push(f);
      else rejected.push(f.name);
    }
    if (rejected.length) append(`[unsupported] ${rejected.join(", ")}`);
    for (const f of accepted) await upload(f, folder);
  }

  async function ingestAll() {
    setBusy(true);
    try {
      const r = await apiPost<any>("/admin/wiki/ingest", {});
      append(t("admin.wiki.logIngest", { result: JSON.stringify(r) }));
      load();
    } catch (e: any) { append(t("admin.wiki.logIngestFailed", { err: e?.message || t("error.unknown") })); }
    finally { setBusy(false); }
  }
  async function compileAll() {
    setBusy(true);
    try {
      const r = await apiPost<any>("/admin/wiki/compile", {});
      append(t("admin.wiki.logCompile", { result: JSON.stringify(r) }));
      load();
    } catch (e: any) { append(t("admin.wiki.logCompileFailed", { err: e?.message || t("error.unknown") })); }
    finally { setBusy(false); }
  }
  async function reset() {
    if (!confirm(t("admin.wiki.confirmReset"))) return;
    setBusy(true);
    try { await apiPost("/admin/wiki/reset", {}); append(t("admin.wiki.logReset")); load(); }
    catch (e: any) { append(t("admin.wiki.logResetFailed", { err: e?.message || t("error.unknown") })); }
    finally { setBusy(false); }
  }
  async function remove(s: Src) {
    try { await apiPost("/admin/wiki/sources/" + s.id + "/delete", {}); load(); }
    catch (e: any) { setLog((l) => [...l, "[" + new Date().toLocaleTimeString() + "] " + (e?.message || t("error.unknown"))]); }
  }

  const tree = useMemo(() => buildTree(sources), [sources]);
  const flattened = useMemo(() => flattenTree(tree), [tree]);
  const typeCounts = useMemo(() => {
    const m = new Map<string, number>();
    for (const s of sources) {
      const e = extOf(s.path) || "?";
      m.set(e, (m.get(e) || 0) + 1);
    }
    return m;
  }, [sources]);

  // Files visible in the right pane.
  const visibleFiles = useMemo(() => {
    let files = sources;
    if (selectedFolder) {
      files = files.filter((s) => s.path.startsWith(selectedFolder + "/") || s.path === selectedFolder);
    }
    if (typeFilter !== ALL_TYPES) {
      files = files.filter((s) => extOf(s.path) === typeFilter);
    }
    if (search) {
      const q = search.toLowerCase();
      files = files.filter((s) => s.path.toLowerCase().includes(q));
    }
    return files;
  }, [sources, selectedFolder, typeFilter, search]);

  const selected = sources.find((s) => s.id === selectedSource) || null;

  // Build a manifest snapshot (this is what the underlying index.json would
  // look like, given the current sources). The backend should sync to disk.
  const manifest = useMemo(() => {
    const out = {
      version: 1,
      generatedAt: new Date().toISOString(),
      sourceCount: sources.length,
      folders: [...tree.children.values()].map((f) => ({ name: f.name, fullPath: f.fullPath, fileCount: countFiles(f) })),
      types: Object.fromEntries(typeCounts),
      keywords: [] as string[],
      crossRefs: sources.flatMap((s) => (s.backlinks || []).map((b) => ({ from: b, to: s.path }))),
    };
    return out;
  }, [tree, sources, typeCounts]);

  return (
    <div className="admin-page wiki-page">
      <div className="admin-page-head">
        <h1>{t("admin.wiki.title")}</h1>
        <div className="wiki-tabs">
          <button type="button" className={"wiki-tab" + (view === "tree" ? " active" : "")} onClick={() => setView("tree")}>{t("wiki.tab.tree")}</button>
          <button type="button" className={"wiki-tab" + (view === "manifest" ? " active" : "")} onClick={() => setView("manifest")}>{t("wiki.tab.manifest")}</button>
        </div>
        <span className="admin-spacer" />
        <button type="button" className="icon-btn" title={t("admin.common.refresh")} onClick={load} disabled={busy}><IconRefresh size={14} /></button>
      </div>

      <div className="admin-card">
        <div className="admin-card-title">{t("admin.wiki.upload")}</div>
        <div
          className="wiki-dropzone"
          onDragOver={(e) => { e.preventDefault(); e.dataTransfer.dropEffect = "copy"; }}
          onDrop={(e) => {
            e.preventDefault();
            if (e.dataTransfer.files?.length) {
              uploadMany(e.dataTransfer.files, selectedFolder || undefined);
            }
          }}
        >
          <div className="wiki-dropzone-icon">⤴</div>
          <div className="wiki-dropzone-text">将文件拖到此处，或</div>
          <div className="wiki-dropzone-actions">
            {/* Hidden native inputs, triggered by styled buttons. */}
            <input
              ref={fileRef}
              type="file"
              multiple
              style={{ display: "none" }}
              onChange={(e) => { uploadMany(e.target.files, selectedFolder || undefined); e.target.value = ""; }}
              disabled={busy}
              accept={[...SUPPORTED_EXTS].join(",")}
            />
            <input
              ref={folderRef}
              type="file"
              style={{ display: "none" }}
              // @ts-ignore - webkitdirectory is a real attribute
              webkitdirectory=""
              directory=""
              multiple
              onChange={(e) => { uploadMany(e.dataTransfer ? e.dataTransfer.files : e.target.files); e.target.value = ""; }}
              disabled={busy}
            />
            <button type="button" className="btn-secondary" onClick={() => fileRef.current?.click()} disabled={busy}>
              选择文件
            </button>
            <button type="button" className="btn-ghost" onClick={() => folderRef.current?.click()} disabled={busy}>
              选择文件夹
            </button>
          </div>
          <div className="admin-hint wiki-upload-hint">
            {t("admin.wiki.uploadHint")} · 支持 md / pdf / docx / xlsx / pptx / csv / json / ipynb 等 {SUPPORTED_EXTS.size} 种格式
          </div>
        </div>
        <div className="wiki-toolbar">
          <button onClick={ingestAll} disabled={busy} className="btn-secondary">{t("admin.wiki.triggerIngest")}</button>
          <button onClick={compileAll} disabled={busy} className="btn-secondary">{t("admin.wiki.compileIndex")}</button>
          <button onClick={reset} disabled={busy} className="btn-ghost btn-danger-ghost">{t("admin.wiki.resetAll")}</button>
        </div>
      </div>

      {view === "tree" ? (
        <div className="wiki-tree-layout">
          <aside className="wiki-tree-pane">
            <div className="wiki-tree-pane-head">
              <span>{t("wiki.folders")}</span>
              <span className="wiki-count">{sources.length}</span>
            </div>
            <button
              type="button"
              className={"wiki-folder" + (!selectedFolder ? " active" : "")}
              onClick={() => setSelectedFolder("")}
            >
              <span className="wiki-folder-icon">⌂</span>
              <span>{t("wiki.folder.root")}</span>
            </button>
            {flattened.filter((x) => x.depth > 0 || x.node.files.length > 0).map(({ node, depth }) => {
              const fileCount = countFiles(node);
              if (fileCount === 0) return null;
              return (
                <button
                  type="button"
                  key={node.fullPath}
                  className={"wiki-folder" + (selectedFolder === node.fullPath ? " active" : "")}
                  onClick={() => setSelectedFolder(node.fullPath)}
                  style={{ paddingLeft: 8 + depth * 12 }}
                >
                  <span className="wiki-folder-icon">▸</span>
                  <span className="wiki-folder-name">{node.name}</span>
                  <span className="wiki-folder-count">{fileCount}</span>
                </button>
              );
            })}
          </aside>
          <section className="wiki-files-pane">
            <div className="wiki-files-head">
              <div className="wiki-files-filter">
                <button type="button" className={"wiki-type" + (typeFilter === ALL_TYPES ? " active" : "")} onClick={() => setTypeFilter(ALL_TYPES)}>
                  全部 <span className="wiki-type-count">{sources.length}</span>
                </button>
                {[...typeCounts.entries()].sort((a, b) => b[1] - a[1]).map(([ext, n]) => (
                  <button type="button" key={ext} className={"wiki-type" + (typeFilter === ext ? " active" : "")} onClick={() => setTypeFilter(ext)}>
                    {ext} <span className="wiki-type-count">{n}</span>
                  </button>
                ))}
              </div>
              <input
                className="wiki-search"
                placeholder={t("wiki.search.placeholder")}
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            {visibleFiles.length === 0 ? (
              <div className="admin-empty">{t("admin.wiki.empty")}</div>
            ) : (
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>{t("admin.wiki.path")}</th>
                    <th>{t("admin.wiki.status")}</th>
                    <th>{t("admin.wiki.size")}</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {visibleFiles.map((s) => (
                    <tr key={s.id} className={selectedSource === s.id ? "active" : ""} onClick={() => setSelectedSource(s.id)}>
                      <td>
                        <code className="code-chip">
                          <IconFiles size={11} /> {s.path}
                        </code>
                        <span className={"wiki-ext wiki-ext-" + (extOf(s.path).replace(".", "") || "unknown")}>{extOf(s.path) || "?"}</span>
                      </td>
                      <td>{s.status}</td>
                      <td>{formatSize(s.size_bytes)}</td>
                      <td className="admin-row-action">
                        <button className="icon-btn danger" title={t("admin.common.delete")} onClick={(e) => { e.stopPropagation(); remove(s); }}><IconTrash size={13} /></button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            {selected && (
              <div className="wiki-detail">
                <div className="wiki-detail-head">
                  <code className="code-chip">{selected.path}</code>
                  <span className="wiki-detail-meta">
                    {selected.mime || extOf(selected.path) || "?"} · {formatSize(selected.size_bytes)} · {selected.status}
                  </span>
                </div>
                {selected.error && <div className="wiki-detail-error">{selected.error}</div>}
                {(selected.backlinks || []).length > 0 && (
                  <div className="wiki-detail-section">
                    <div className="wiki-detail-section-title">{t("wiki.backlinks")}</div>
                    <ul className="wiki-backlinks">
                      {(selected.backlinks || []).map((b) => (
                        <li key={b}>
                          <button type="button" className="link-btn" onClick={() => setSelectedSource(b)}>{b}</button>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                <div className="wiki-detail-section">
                  <div className="wiki-detail-section-title">{t("wiki.detail.crossref")}</div>
                  <p className="wiki-detail-hint">{t("wiki.detail.crossrefHint")}</p>
                </div>
              </div>
            )}
          </section>
        </div>
      ) : (
        <div className="admin-card">
          <div className="admin-card-title">{t("wiki.manifest.title")}</div>
          <p className="admin-hint">{t("wiki.manifest.hint")}</p>
          <pre className="admin-log wiki-manifest">{JSON.stringify(manifest, null, 2)}</pre>
        </div>
      )}

      {log.length > 0 && (
        <div className="admin-card">
          <div className="admin-card-title">{t("admin.wiki.log")}</div>
          <pre className="admin-log">{log.join("\n")}</pre>
        </div>
      )}
    </div>
  );
}

function countFiles(n: FolderNode): number {
  return n.files.length + [...n.children.values()].reduce((sum, c) => sum + countFiles(c), 0);
}
