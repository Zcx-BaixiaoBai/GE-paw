// Codex-style permission pill with a dropdown menu. The visible label uses
// the zh-CN i18n keys (perm.full / perm.smart / perm.strict / perm.readonly)
// and the matching icon hint at the severity of the chosen mode.
//
// Selecting a new value calls `onChange` which is expected to PATCH the
// session; we stay presentational here and let the parent own the API call
// (so callers can pass the current session id and wire it through the
// session store).
import { useEffect, useRef, useState } from "react";
import { IconChevronDown, IconLock, IconShield, IconShieldOff } from "./Icons";
import type { PermissionMode } from "../stores/session";
import { t } from "../lib/i18n";

export type PermissionSelectorProps = {
  value: PermissionMode | null;
  onChange: (next: PermissionMode) => void;
  disabled?: boolean;
};

type Item = {
  value: PermissionMode;
  icon: React.ReactNode;
  cls: string;
};

const ICONS: Record<PermissionMode, React.ReactNode> = {
  full: <IconShieldOff size={14} />,
  smart: <IconShield size={14} />,
  strict: <IconLock size={14} />,
  readonly: <IconLock size={14} />,
};

const ORDER: PermissionMode[] = ["full", "smart", "strict", "readonly"];

export function PermissionSelector({ value, onChange, disabled }: PermissionSelectorProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onClick = (e: MouseEvent) => {
      if (!ref.current?.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, [open]);

  const current: PermissionMode = value ?? "smart";

  return (
    <div className="perm-pill" ref={ref}>
      <button
        type="button"
        className={"perm-pill-btn perm-pill-" + current}
        onClick={(e) => { e.preventDefault(); e.stopPropagation(); if (!disabled) setOpen((v) => !v); }}
        disabled={disabled}
        title={t("chat.permission.label")}
      >
        <span className="perm-pill-icon">{ICONS[current]}</span>
        <span className="perm-pill-text">{t("perm." + current as any)}</span>
        <span className="perm-pill-caret"><IconChevronDown size={12} /></span>
      </button>
      {open && (
        <div className="perm-menu" role="menu">
          {ORDER.map((m) => (
            <Item
              key={m}
              value={m}
              active={m === current}
              onPick={(v) => { if (v !== current) onChange(v); setOpen(false); }}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function Item({ value, active, onPick }: { value: PermissionMode; active: boolean; onPick: (v: PermissionMode) => void }) {
  return (
    <button
      type="button"
      role="menuitemradio"
      aria-checked={active}
      className={"perm-menu-item" + (active ? " active" : "")}
      onClick={() => onPick(value)}
    >
      <span className={"perm-menu-icon perm-pill-" + value}>{ICONS[value]}</span>
      <span className="perm-menu-text">
        <span className="perm-menu-title">{t("perm." + value as any)}</span>
        <span className="perm-menu-desc">{t("perm." + value + ".desc" as any)}</span>
      </span>
    </button>
  );
}


