import { useEffect, useState } from "react";
import { apiGet, apiPost, apiDel } from "../../lib/api";

type LLM = { id: string; name: string; base_url: string; model: string; max_tokens: number; temperature: number; is_default: boolean; enabled: boolean };

export function AdminLLMPage() {
  const [list, setList] = useState<LLM[]>([]);
  const [form, setForm] = useState({ name: "", base_url: "", api_key: "", model: "gpt-4o-mini", max_tokens: 4096, temperature: 0.2, is_default: false });
  const [err, setErr] = useState<string | null>(null);

  async function load() { try { setList(await apiGet<LLM[]>("/admin/llm")); } catch (e: any) { setErr(e?.message || "load failed"); } }
  useEffect(() => { load(); }, []);

  async function add() {
    setErr(null);
    try { await apiPost("/admin/llm", form); setForm({ name: "", base_url: "", api_key: "", model: "gpt-4o-mini", max_tokens: 4096, temperature: 0.2, is_default: false }); load(); }
    catch (e: any) { setErr(e?.message || "create failed"); }
  }

  return (
    <div>
      <h1>LLM endpoints</h1>
      <div className="admin-card">
        <div style={{ fontWeight: 600, marginBottom: 10 }}>Add endpoint (OpenAI-compatible)</div>
        <div className="row"><label>Name</label><input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="main" /></div>
        <div className="row"><label>Base URL</label><input value={form.base_url} onChange={(e) => setForm({ ...form, base_url: e.target.value })} placeholder="https://api.openai.com/v1" /></div>
        <div className="row"><label>API Key</label><input type="password" value={form.api_key} onChange={(e) => setForm({ ...form, api_key: e.target.value })} /></div>
        <div className="row"><label>Model</label><input value={form.model} onChange={(e) => setForm({ ...form, model: e.target.value })} /></div>
        <div className="row"><label>Max tokens</label><input type="number" value={form.max_tokens} onChange={(e) => setForm({ ...form, max_tokens: parseInt(e.target.value) || 4096 })} /></div>
        <div className="row"><label>Temperature</label><input type="number" step="0.1" value={form.temperature} onChange={(e) => setForm({ ...form, temperature: parseFloat(e.target.value) || 0.2 })} /></div>
        <div className="row"><label>Default</label><input type="checkbox" checked={form.is_default} onChange={(e) => setForm({ ...form, is_default: e.target.checked })} /></div>
        <div style={{ marginTop: 8 }}><button className="primary" onClick={add} disabled={!form.name || !form.base_url || !form.api_key || !form.model}>Add</button></div>
        {err && <div style={{ color: "var(--danger)", marginTop: 8 }}>{err}</div>}
      </div>
      <div className="admin-card">
        <div style={{ fontWeight: 600, marginBottom: 10 }}>Existing endpoints</div>
        <table className="admin-table">
          <thead><tr><th>Name</th><th>Base URL</th><th>Model</th><th>Default</th><th>Enabled</th><th></th></tr></thead>
          <tbody>
            {list.length === 0 && <tr><td colSpan={6} style={{ color: "var(--fg-faint)" }}>No endpoints</td></tr>}
            {list.map((e) => (
              <tr key={e.id}>
                <td>{e.name}</td><td>{e.base_url}</td><td>{e.model}</td>
                <td>{e.is_default ? "yes" : ""}</td><td>{e.enabled ? "yes" : "no"}</td>
                <td><button onClick={async () => { await apiDel("/admin/llm/" + e.id); load(); }}>Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
