import type { ComponentType } from "react";
import { FilesTab } from "./tabs/FilesTab";
import { WebTab } from "./tabs/WebTab";
import { DiffTab } from "./tabs/DiffTab";
import { PreviewTab } from "./tabs/PreviewTab";
import { PlanTab } from "./tabs/PlanTab";
import { GoalsTab } from "./tabs/GoalsTab";
import {
  IconFiles,
  IconWeb,
  IconDiff,
  IconPreview,
  IconPlan,
  IconGoals,
} from "../Icons";
import { t } from "../../lib/i18n";

export type TabKind = "files" | "web" | "diff" | "preview" | "plan" | "goals";

export type TabMeta = {
  title: string;
  icon: React.ReactNode;
  component: ComponentType<any>;
  /**
   * v1 availability:
   *   - true  : wired to a live backend endpoint; the tab is fully functional.
   *   - false : skeleton in place, endpoint reserved, will be filled in later.
   */
  available: boolean;
  hint?: string;
};

export const TabRegistry: Record<TabKind, TabMeta> = {
  files:   { title: t("tab.files"),   icon: <IconFiles size={14} />,   component: FilesTab,   available: true,  hint: t("tab.files.hint") },
  web:     { title: t("tab.web"),     icon: <IconWeb size={14} />,     component: WebTab,     available: true,  hint: t("tab.web.hint") },
  diff:    { title: t("tab.diff"),    icon: <IconDiff size={14} />,    component: DiffTab,    available: true,  hint: t("tab.diff.hint") },
  preview: { title: t("tab.preview"), icon: <IconPreview size={14} />, component: PreviewTab, available: true,  hint: t("tab.preview.hint") },
  plan:    { title: t("tab.plan"),    icon: <IconPlan size={14} />,    component: PlanTab,    available: true,  hint: t("tab.plan.hint") },
  goals:   { title: t("tab.goals"),   icon: <IconGoals size={14} />,   component: GoalsTab,   available: true,  hint: t("tab.goals.hint") },
};

export const AllTabKinds: TabKind[] = ["files", "web", "diff", "preview", "plan", "goals"];
