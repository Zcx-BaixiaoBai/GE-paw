import { useEffect, useState } from "react";
import { apiGet } from "../../lib/api";

type E = { id: number; action: string; target: string; actor: string; created_at: string; details?: string };

export function AdminAuditPage() {
  const [list, setList] = useState<E[]>([]);
  useEffect(() => { apiGet<E[]>("/admin/audit").then(setList).catch(() => setList([])); }, []);
  return (
    <div>
      <h1>Audit log</h1>
      <div className="admin-card">
        <table className="admin-table">
          <thead><tr><th>When</th><th>Action</th><th>Target</th><th>Actor</th></tr></thead>
          <tbody>
            {list.length === 0 && <tr><td colSpan={4} style={{ color: "var(--fg-faint)" }}>No entries</td></tr>}
            {list.map((e) => (
              <tr key={e.id}>
                <td>{new Date(e.created_at).toLocaleString()}</td>
                <td><code>{e.action}</code></td>
                <td><code>{e.target}</code></td>
                <td>{e.actor}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
