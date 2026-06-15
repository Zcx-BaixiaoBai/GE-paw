import { Navigate, Route, Routes } from "react-router-dom";
import { LoginPage } from "./pages/Login";
import { AppLayout } from "./layouts/AppLayout";

import { LLMConfigPage } from "./pages/Admin/LLM";
import { ChannelsPage } from "./pages/Admin/Channels";
import { CronsPage } from "./pages/Admin/Crons";
import { MembersPage } from "./pages/Admin/Members";
import { TokensPage } from "./pages/Admin/Tokens";
import { WikiPage } from "./pages/Admin/Wiki";
import { AuditPage } from "./pages/Admin/Audit";
import { SessionsPage } from "./pages/Admin/Sessions";
import { SkillsPage } from "./pages/Admin/Skills";
import { PluginsPage } from "./pages/Admin/Plugins";
import { MCPPage } from "./pages/Admin/MCP";
import { GatewayPage } from "./pages/Admin/Gateway";

import { AssistantPage } from "./pages/Assistant";
import { QnAPage } from "./pages/QnA";
import { SettingsPage } from "./pages/Settings";
import { AdminLayout } from "./pages/Admin/AdminLayout";

export function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<AppLayout />}> 
        <Route index element={<Navigate to="/app/assistant" replace />} />
        <Route path="app/assistant" element={<AssistantPage />} />
        <Route path="app/qna" element={<QnAPage />} />
        <Route path="settings" element={<SettingsPage />} />
        <Route path="admin" element={<AdminLayout />}> 
          <Route index element={<Navigate to="llm" replace />} />
          <Route path="llm" element={<LLMConfigPage />} />
          <Route path="channels" element={<ChannelsPage />} />
          <Route path="crons" element={<CronsPage />} />
          <Route path="members" element={<MembersPage />} />
          <Route path="tokens" element={<TokensPage />} />
          <Route path="wiki" element={<WikiPage />} />
          <Route path="audit" element={<AuditPage />} />
          <Route path="sessions" element={<SessionsPage />} />
          <Route path="skills" element={<SkillsPage />} />
          <Route path="plugins" element={<PluginsPage />} />
          <Route path="mcp" element={<MCPPage />} />
          <Route path="gateway" element={<GatewayPage />} />
        </Route>
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}