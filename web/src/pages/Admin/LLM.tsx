import { useEffect, useState } from "react";
import { apiGet, apiPost, apiDel } from "../../lib/api";
import { IconTrash } from "../../components/Icons";
import { t } from "../../lib/i18n";

type LLM = { id: string; name: string; base_url: string; model: string; max_tokens: number; temperature: number; is_default: boolean; enabled: boolean };

const EMPTY = { name: "", base_url: "https://api.openai.com/v1", api_key: "", model: "gpt-4o-mini", max_tokens: 4096, temperature: 0.2 };

export function AdminLLMPage() {
  const [list, setList] = useState<LLM[]>([]);
  const [form, setForm] = useState({ ...EMPTY });
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    try { setList(await apiGet<LLM[]>("/admin/llm")); }
    catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  useEffect(() => { load(); }, []);

  async function add() {
    setErr(null);
    try {
      await apiPost("/admin/llm", { ...form, max_tokens: Number(form.max_tokens), temperature: Number(form.temperature), is_default: false });
      setForm({ ...EMPTY });
      load();
    } catch (e: any) { setErr(e?.message || t("error.unknown")); }
  }
  async function remove(x: LLM) {
    if (!confirm(t("admin.common.confirmDelete", { name: x.name }))) return;
    await apiDel("/admin/llm/" + x.id);
    load();
  }

  return (
    <div className="admin-page">
      <h1>{t("admin.llm.title")}</h1>
      {err && <div className="admin-card admin-err">{err}</div>}

      <div className="admin-card">
        <div className="admin-card-title">{t("admin.llm.addTitle")}</div>
        <div className="admin-form">
          <Field label={t("admin.llm.name")}><input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></Field>
          <Field label={t("admin.llm.baseUrl")}><input value={form.base_url} onChange={(e) => setForm({ ...form, base_url: e.target.value })} /></Field>
          <Field label={t("admin.llm.apiKey")}><input type="password" value={form.api_key} onChange={(e) => setForm({ ...form, api_key: e.target.value })} /></Field>
          <Field label={t("admin.llm.model")}><input value={form.model} onChange={(e) => setForm({ ...form, model: e.target.value })} /></Field>
          <Field label={t("admin.llm.maxTokens")}><input type="number" value={form.max_tokens} onChange={(e) => setForm({ ...form, max_tokens: Number(e.target.value) })} /></Field>
          <Field label={t("admin.llm.temperature")}><input type="number" step="0.1" value={form.temperature} onChange={(e) => setForm({ ...form, temperature: Number(e.target.value) })} /></Field>
        </div>
        <div className="admin-form-actions">
          <button className="primary" onClick={add} disabled={!form.name || !form.base_url}>{t("admin.common.add")}</button>
        </div>
      </div>

      <div className="admin-card admin-card-flush">
        <div className="admin-card-title admin-card-title-bar">{t("admin.llm.list")}</div>
        {list.length === 0 ? (
          <div className="admin-empty">{t("admin.llm.empty")}</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>{t("admin.llm.name")}</th>
                <th>{t("admin.llm.baseUrl")}</th>
                <th>{t("admin.llm.model")}</th>
                <th>{t("admin.llm.isDefault")}</th>
                <th>{t("admin.llm.enabled")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {list.map((x) => (
                <tr key={x.id}>
                  <td><strong>{x.name}</strong></td>
                  <td className="admin-mono">{x.base_url}</td>
                  <td className="admin-mono">{x.model}</td>
                  <td>{x.is_default ? <span className="pill pill-ok">{t("admin.llm.isDefault")}</span> : <span className="pill pill-off">{t("common.dash")}</span>}</td>
                  <td>{x.enabled ? <span className="pill pill-ok">{t("admin.llm.enabled")}</span> : <span className="pill pill-off">{t("common.dash")}</span>}</td>
                  <td className="admin-row-action"><button className="icon-btn danger" onClick={() => remove(x)} title={t("admin.common.delete")}><IconTrash size={13} /></button></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="admin-field">
      <span className="admin-field-label">{label}</span>
      {children}
    </label>
  );
}
