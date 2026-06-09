import { NavLink, Outlet } from "react-router-dom";
export function AdminLayout() {
  return (
    <div className="admin-layout">
      <div className="admin-side">
        <NavLink to="/admin/llm" className={({ isActive }) => "item" + (isActive ? " active" : "")}>LLM endpoints</NavLink>
        <NavLink to="/admin/members" className={({ isActive }) => "item" + (isActive ? " active" : "")}>Members</NavLink>
        <NavLink to="/admin/channels" className={({ isActive }) => "item" + (isActive ? " active" : "")}>Channels</NavLink>
        <NavLink to="/admin/crons" className={({ isActive }) => "item" + (isActive ? " active" : "")}>Cron jobs</NavLink>
        <NavLink to="/admin/tokens" className={({ isActive }) => "item" + (isActive ? " active" : "")}>Tokens</NavLink>
        <NavLink to="/admin/sessions" className={({ isActive }) => "item" + (isActive ? " active" : "")}>Sessions</NavLink>
        <NavLink to="/admin/wiki" className={({ isActive }) => "item" + (isActive ? " active" : "")}>Wiki</NavLink>
        <NavLink to="/admin/audit" className={({ isActive }) => "item" + (isActive ? " active" : "")}>Audit</NavLink>
      </div>
      <div className="admin-main"><Outlet /></div>
    </div>
  );
}
