import type { ComponentType } from "react";
import { FilesTab } from "./tabs/FilesTab";
import { WebTab } from "./tabs/WebTab";
import { DiffTab } from "./tabs/DiffTab";
import { PreviewTab } from "./tabs/PreviewTab";
import { PlanTab } from "./tabs/PlanTab";

export type TabKind = "files" | "web" | "diff" | "preview" | "plan";

export type TabMeta = {
  title: string;
  icon: string;
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
  files:   { title: "Files",   icon: "📁", component: FilesTab,   available: true,  hint: "Workspace + Wiki tree" },
  web:     { title: "Web",     icon: "🌐", component: WebTab,     available: true,  hint: "Embed any URL (wiki preview supported)" },
  diff:    { title: "Diff",    icon: "🪞", component: DiffTab,    available: true,  hint: "Compare two wiki files" },
  preview: { title: "Preview", icon: "👁", component: PreviewTab, available: true,  hint: "Multi-format wiki preview" },
  plan:    { title: "Plan",    icon: "🧭", component: PlanTab,    available: true,  hint: "Assistant tool-call plan" },
};

export const AllTabKinds: TabKind[] = ["files", "web", "diff", "preview", "plan"];
