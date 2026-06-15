// Codex-style slash command menu. Pops up above the composer when the user
// types `/` at the start of the input, filters as they keep typing, and
// runs the picked command (e.g. `/new` creates a session, `/settings`
// navigates). Arrow keys + Enter to pick; Esc to close.
import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { t } from "../lib/i18n";

export type SlashCommand = {
  id: string;
  labelKey: string;       // i18n key for the command name
  descKey: string;        // i18n key for the description
  run: (ctx: SlashContext) => Promise<void> | void;
};

export type SlashContext = {
  navigate: (to: string) => void;
  createSession: () => Promise<void>;
  clearInput: () => void;
  insertText: (text: string) => void;
};

function defaultCommands(ctx: SlashContext): SlashCommand[] {
  return [
    {
      id: "new",
      labelKey: "slash.new",
      descKey: "slash.new.desc",
      run: async () => { await ctx.createSession(); },
    },
    {
      id: "clear",
      labelKey: "slash.clear",
      descKey: "slash.clear.desc",
      run: () => { ctx.clearInput(); },
    },
    {
      id: "help",
      labelKey: "slash.help",
      descKey: "slash.help.desc",
      run: () => {
        ctx.insertText(
          "可用命令：\n" +
          "/new   新建会话\n" +
          "/clear 清空输入\n" +
          "/settings 打开设置\n" +
          "/model 插入当前模型信息\n" +
          "/perm 切换权限模式\n",
        );
      },
    },
    {
      id: "settings",
      labelKey: "slash.settings",
      descKey: "slash.settings.desc",
      run: () => { ctx.navigate("/app/settings"); },
    },
    {
      id: "model",
      labelKey: "slash.model",
      descKey: "slash.model.desc",
      run: () => {
        // Insert a hint the user can send; the server can echo the active
        // model back. Keep it simple — don't pretend to know the model name.
        ctx.insertText("[查看当前模型：/api/client/config]");
      },
    },
  ];
}

export function SlashMenu({
  open,
  query,
  onPick,
  onClose,
  ctx,
}: {
  open: boolean;
  query: string;
  onPick: () => void;
  onClose: () => void;
  ctx: SlashContext;
}) {
  const navigate = useNavigate();
  const [active, setActive] = useState(0);
  const ref = useRef<HTMLDivElement>(null);

  const cmds = useMemo(
    () => defaultCommands({ ...ctx, navigate }),
    [ctx, navigate],
  );

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return cmds;
    return cmds.filter((c) => {
      const label = (t as any)(c.labelKey).toLowerCase();
      return label.includes(q) || c.id.includes(q);
    });
  }, [cmds, query]);

  useEffect(() => { setActive(0); }, [query, open]);

  useEffect(() => {
    if (!open) return;
    function onKey(e: KeyboardEvent) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setActive((i) => Math.min(i + 1, filtered.length - 1));
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setActive((i) => Math.max(i - 1, 0));
      } else if (e.key === "Enter" || e.key === "Tab") {
        if (filtered[active]) {
          e.preventDefault();
          void filtered[active].run(ctx);
          onPick();
        }
      } else if (e.key === "Escape") {
        e.preventDefault();
        onClose();
      }
    }
    window.addEventListener("keydown", onKey, true);
    return () => window.removeEventListener("keydown", onKey, true);
  }, [open, filtered, active, ctx, onPick, onClose]);

  if (!open) return null;
  return (
    <div className="slash-menu" ref={ref} role="listbox" aria-label={t("slash.menu.title")}>
      <div className="slash-menu-head">{t("slash.menu.title")}</div>
      {filtered.length === 0 ? (
        <div className="slash-menu-empty">{t("slash.menu.empty")}</div>
      ) : (
        filtered.map((c, i) => (
          <button
            key={c.id}
            type="button"
            className={"slash-menu-item" + (i === active ? " active" : "")}
            onMouseEnter={() => setActive(i)}
            onClick={() => { void c.run(ctx); onPick(); }}
            role="option"
            aria-selected={i === active}
          >
            <span className="slash-menu-item-name">/{c.id}</span>
            <span className="slash-menu-item-desc">{(t as any)(c.descKey)}</span>
          </button>
        ))
      )}
    </div>
  );
}
