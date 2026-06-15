// App shell: top thread header, optional left/right panes, modal portal.
// Codex-style: single top bar with brand on the left, ThreadHeader centred,
// and a clean right cluster (panel toggle / theme / user).
import { useEffect, useState } from "react";
import { Outlet, useSearchParams } from "react-router-dom";
import { useAuthStore } from "../stores/auth";
import { apiGet } from "../lib/api";
import { LeftPane } from "../components/LeftPane";
import { RightPane } from "../components/RightPane/RightPane";
import { RequestUserInputModal } from "../components/RequestUserInputModal";
import { ComputerUseIndicator } from "../stores/computerUse.tsx";
import { requestUserInput, useUserInputStore } from "../stores/userInput";
import { usePaneStore } from "../stores/tabs";
import { ThreadHeader } from "../components/ThreadHeader";
import { ThemeMenu } from "../components/ThemeMenu";
import { UserMenu } from "../components/UserMenu";
import { Logo } from "../components/Logo";
import { ProgressBar } from "../components/ProgressBar";
import { IconPanelLeft, IconPanelRight } from "../components/Icons";
import { t } from "../lib/i18n";

export function AppLayout() {
  const [leftCollapsed, setLeftCollapsed] = useState(false);
  const setIdentity = useAuthStore((s) => s.setIdentity);
  const clear = useAuthStore((s) => s.clear);
  const username = useAuthStore((s) => s.username);
  const role = useAuthStore((s) => s.role);
  const orgName = useAuthStore((s) => s.orgName);
  const paneOpen = usePaneStore((s) => s.open);
  const paneToggle = usePaneStore((s) => s.toggle);
  const [params] = useSearchParams();
  const sessionId = params.get("session") || null;

  useEffect(() => {
    if (!username) {
      apiGet<any>("/auth/me").then((d) => {
        if (d?.username) setIdentity(d);
        else clear();
      }).catch(() => clear());
    }
  }, [username, setIdentity, clear]);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (!(e.ctrlKey || e.metaKey)) return;
      if (e.key === "b") { e.preventDefault(); setLeftCollapsed((v) => !v); }
      if (e.key === "j") { e.preventDefault(); paneToggle(); }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [paneToggle]);

  // Test hook: let e2e scripts trigger the request-user-input modal from
  // outside React without going through a real fetch event. Only attached
  // when running on localhost so it stays inert in production builds.
  useEffect(() => {
    if (typeof window === "undefined") return;
    if (!window.location.hostname.match(/^(localhost|127\.0\.0\.1)$/)) return;
    (window as any).__gepawTestShowUserInput = (req?: any) => {
      // Fire-and-forget: do NOT return the unresolved `requestUserInput` promise
      // because page.evaluate on the test side would hang waiting for it.
      const payload = req ?? {
        question: t("modal.requestUserInput.title"),
        description: t("modal.requestUserInput.desc"),
        options: [
          { id: "light", label: t("theme.menu.light"), description: "" },
          { id: "dark",  label: t("theme.menu.dark"),  description: "" },
          { id: "auto",  label: t("theme.menu.system"), description: "" },
        ],
        allowFreeText: true,
      };
      // Bypass the async wrapper so the call returns immediately.
      useUserInputStore.getState().enqueue({
        ...payload,
        resolve: () => {},
      });
    };
  }, []);
  // Test hook: simulate the agent runtime writing to memory. In a real
  // build the chat runtime would call this from a "summarize last turn"
  // service. For QA we expose it on window.
  useEffect(() => {
    if (typeof window === "undefined") return;
    if (!window.location.hostname.match(/^(localhost|127\.0\.0\.1)$/)) return;
    (window as any).__gepawTestAgentWriteMemory = async (req?: any) => {
      const { useSettingsStore, makeMemoryId } = await import("../stores/settings");
      const store = useSettingsStore.getState();
      const today = new Date().toISOString().slice(0, 10);
      const kind = req?.kind || "summary";
      if (kind === "topic") {
        const id = makeMemoryId();
        const samples = [
          { title: "用户偏好中文 + 简洁", body: "代理从最近 5 轮对话中观察到用户偏好中文回答、要点先行、不需要寒暄。" },
          { title: "当前项目: GE-paw 控制台改造", body: "代理记录用户当前正在做的事情,涉及弹窗定位、记忆系统、知识库三个模块。" },
          { title: "沟通风格: 工程师对工程师", body: "用户用 `codex`、`qwenpaw`、`minimax agent` 等术语,代理可以以对等身份交流。" },
        ];
        const s = samples[Math.floor(Math.random() * samples.length)];
        store.upsertMemoryTopic({ id, title: s.title, body: s.body, author: "agent", updatedAt: Date.now() });
        return { kind: "topic", id, title: s.title };
      }
      // default: a L2 dated summary of the "last conversation turn"
      const lastEntry = Object.values(store.memory.dated).sort((a, b) => b.updatedAt - a.updatedAt)[0];
      const id = makeMemoryId();
      const samples = [
        `讨论了 GE-paw 控制台中 slash 菜单的定位 bug: 越出视口顶部 145px。已把 <SlashMenu> 移入 .composer-wrap 内部,问题修复。`,
        `用户提出 computer use 不应该弹窗,应该用 codex 风格的边缘蓝光。已重做,改成 cu-halo + 顶栏状态徽章。`,
        `用户提出记忆系统应该由 agent 自行读写,而不是用户手动填表。已重做,记忆现在由代理维护,用户只读 + 审核。`,
      ];
      const s = samples[Math.floor(Math.random() * samples.length)];
      const keywords = ["GE-paw", "审计", kind === "summary" ? "代理" : "总结"];
      store.upsertMemoryEntry({ id, date: today, body: s, topicIds: lastEntry ? [lastEntry.id] : [], keywords, author: "agent", updatedAt: Date.now() });
      // Also update the L0 outline if empty
      if (!store.memory.outline) {
        store.setMemoryOutline("用户正在改造 GE-paw 控制台: 让 chat 内的弹窗定位正确、记忆系统由 agent 自行维护、知识库像文件夹一样可操控。");
      }
      return { kind: "summary", id, date: today };
    };
  }, []);

  function bodyClass() {
    if (leftCollapsed && !paneOpen) return "both-collapsed";
    if (leftCollapsed) return "left-collapsed";
    if (!paneOpen) return "right-collapsed";
    return "";
  }

  return (
    <div className="app-shell">
      <ProgressBar />
      <div className="topbar">
        <div className="topbar-left">
          <button
            type="button"
            className="topbar-icon-btn"
            title={t("topbar.toggleLeft")}
            onClick={() => setLeftCollapsed((v) => !v)}
          >
            <IconPanelLeft size={17} />
          </button>
          <span className="topbar-brand">
            <Logo size={18} />
            <span className="topbar-brand-text">{t("brand.name")}</span>
          </span>
        </div>
        <div className="topbar-center">
          <ThreadHeader sessionId={sessionId} orgName={orgName} role={role} />
        </div>
        <div className="topbar-right">
          {orgName && <span className="topbar-org-pill" title={t("topbar.workspace")}>{orgName}</span>}
          <button
            type="button"
            className="topbar-icon-btn"
            title={t("topbar.toggleRight")}
            onClick={paneToggle}
          >
            <IconPanelRight size={17} />
          </button>
          <ThemeMenu />
          <UserMenu />
        </div>
      </div>
      <div className={"app-body " + bodyClass()}>
        {!leftCollapsed ? <LeftPane /> : <div className="left-pane" style={{ width: "var(--left-w-collapsed)" }} />}
        <div className="center-pane"><Outlet /></div>
        <RightPane />
      </div>
      <RequestUserInputModal />
      <ComputerUseIndicator />
    </div>
  );
}

