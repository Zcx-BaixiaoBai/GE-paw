import { Navigate, Route, Routes } from "react-router-dom";
import { LoginPage } from "./pages/Login";
import { AppLayout } from "./layouts/AppLayout";
import { AssistantPage } from "./pages/Assistant";
import { QnAPage } from "./pages/QnA";
import { AdminLayout } from "./pages/Admin/AdminLayout";
import { AdminLLMPage } from "./pages/Admin/LLM";
import { AdminMembersPage } from "./pages/Admin/Members";
import { AdminChannelsPage } from "./pages/Admin/Channels";
import { AdminCronsPage } from "./pages/Admin/Crons";
import { AdminTokensPage } from "./pages/Admin/Tokens";
import { AdminSessionsPage } from "./pages/Admin/Sessions";
import { AdminWikiPage } from "./pages/Admin/Wiki";
import { AdminAuditPage } from "./pages/Admin/Audit";
import { useAuthStore } from "./stores/auth";

function RequireAuth({ children }: { children: React.ReactNode }) {
  const token = useAuthStore((s) => s.accessToken);
  if (!token) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

function RequireAdmin({ children }: { children: React.ReactNode }) {
  const token = useAuthStore((s) => s.accessToken);
  const role = useAuthStore((s) => s.role);
  if (!token) return <Navigate to="/login" replace />;
  if (role !== "admin") return <Navigate to="/app/assistant" replace />;
  return <>{children}</>;
}

export function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<RequireAuth><AppLayout /></RequireAuth>}>
        <Route index element={<Navigate to="/app/assistant" replace />} />
        <Route path="app/assistant" element={<AssistantPage />} />
        <Route path="app/qna" element={<QnAPage />} />
        <Route path="admin" element={<RequireAdmin><AdminLayout /></RequireAdmin>}>
          <Route index element={<Navigate to="/admin/llm" replace />} />
          <Route path="llm" element={<AdminLLMPage />} />
          <Route path="members" element={<AdminMembersPage />} />
          <Route path="channels" element={<AdminChannelsPage />} />
          <Route path="crons" element={<AdminCronsPage />} />
          <Route path="tokens" element={<AdminTokensPage />} />
          <Route path="sessions" element={<AdminSessionsPage />} />
          <Route path="wiki" element={<AdminWikiPage />} />
          <Route path="audit" element={<AdminAuditPage />} />
        </Route>
      </Route>
    </Routes>
  );
}
