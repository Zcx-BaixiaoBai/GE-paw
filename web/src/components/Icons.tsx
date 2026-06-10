// Flat SVG icon set for GE-paw. All icons use currentColor and are 16x16 by
// default. Designed to read clearly at 14-20px, the typical toolbar size.
import type { CSSProperties } from "react";

type IconProps = {
  size?: number;
  className?: string;
  style?: CSSProperties;
};

const wrap = (path: React.ReactNode) => ({ size = 16, className, style }: IconProps) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    width={size}
    height={size}
    className={className}
    style={style}
    fill="none"
    stroke="currentColor"
    strokeWidth={1.7}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden
  >
    {path}
  </svg>
);

export const IconAssistant = wrap(
  <>
    <circle cx="12" cy="12" r="3" />
    <path d="M12 2v3" />
    <path d="M12 19v3" />
    <path d="M2 12h3" />
    <path d="M19 12h3" />
    <path d="M5 5l2 2" />
    <path d="M17 17l2 2" />
    <path d="M5 19l2-2" />
    <path d="M17 7l2-2" />
  </>,
);

export const IconQnA = wrap(
  <>
    <path d="M21 15a3 3 0 0 1-3 3H8l-5 4V6a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3z" />
    <path d="M9 9h6" />
    <path d="M9 13h4" />
  </>,
);

export const IconLLM = wrap(
  <>
    <rect x="4" y="6" width="16" height="12" rx="2" />
    <circle cx="9" cy="12" r="1" fill="currentColor" />
    <circle cx="15" cy="12" r="1" fill="currentColor" />
    <path d="M12 3v3" />
    <path d="M9 18v3" />
    <path d="M15 18v3" />
  </>,
);

export const IconMembers = wrap(
  <>
    <circle cx="9" cy="9" r="3" />
    <circle cx="17" cy="10" r="2.2" />
    <path d="M3 20c.5-3.5 3-5.5 6-5.5s5.5 2 6 5.5" />
    <path d="M14 20c.5-2 1.5-3.5 4-3.5s3.5 1.5 4 3.5" />
  </>,
);

export const IconChannels = wrap(
  <>
    <path d="M3 12c4 0 4-6 8-6s4 6 8 6" />
    <path d="M3 17c4 0 4-4 8-4s4 4 8 4" />
  </>,
);

export const IconCron = wrap(
  <>
    <circle cx="12" cy="13" r="7" />
    <path d="M12 13l3-3" />
    <path d="M9 3h6" />
    <path d="M12 3v3" />
  </>,
);

export const IconTokens = wrap(
  <>
    <circle cx="8" cy="12" r="5" />
    <circle cx="16" cy="12" r="5" />
  </>,
);

export const IconSessions = wrap(
  <>
    <path d="M4 5h13" />
    <path d="M4 12h13" />
    <path d="M4 19h13" />
    <circle cx="20" cy="5" r="1" fill="currentColor" />
    <circle cx="20" cy="12" r="1" fill="currentColor" />
    <circle cx="20" cy="19" r="1" fill="currentColor" />
  </>,
);

export const IconWiki = wrap(
  <>
    <path d="M4 4h11l5 5v11a1 1 0 0 1-1 1H4z" />
    <path d="M15 4v5h5" />
    <path d="M8 13h8" />
    <path d="M8 17h6" />
  </>,
);

export const IconAudit = wrap(
  <>
    <circle cx="11" cy="11" r="6" />
    <path d="M20 20l-4.3-4.3" />
    <path d="M9 11h4" />
  </>,
);

export const IconFiles = wrap(
  <>
    <path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
  </>,
);

export const IconWeb = wrap(
  <>
    <circle cx="12" cy="12" r="9" />
    <path d="M3 12h18" />
    <path d="M12 3a14 14 0 0 1 0 18" />
    <path d="M12 3a14 14 0 0 0 0 18" />
  </>,
);

export const IconDiff = wrap(
  <>
    <path d="M7 4v16" />
    <path d="M17 4v16" />
    <path d="M3 8h4" />
    <path d="M3 12h4" />
    <path d="M3 16h4" />
    <path d="M17 8h4" />
    <path d="M17 12h4" />
    <path d="M17 16h4" />
  </>,
);

export const IconPreview = wrap(
  <>
    <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" />
    <circle cx="12" cy="12" r="3" />
  </>,
);

export const IconPlan = wrap(
  <>
    <path d="M3 6h18" />
    <circle cx="6" cy="6" r="1.6" fill="currentColor" stroke="none" />
    <path d="M3 12h18" />
    <circle cx="14" cy="12" r="1.6" fill="currentColor" stroke="none" />
    <path d="M3 18h18" />
    <circle cx="9" cy="18" r="1.6" fill="currentColor" stroke="none" />
  </>,
);

export const IconGoals = wrap(
  <>
    <circle cx="12" cy="12" r="9" />
    <circle cx="12" cy="12" r="5" />
    <circle cx="12" cy="12" r="1.5" fill="currentColor" stroke="none" />
  </>,
);

export const IconPlus = wrap(
  <>
    <path d="M12 5v14" />
    <path d="M5 12h14" />
  </>,
);

export const IconClose = wrap(
  <>
    <path d="M6 6l12 12" />
    <path d="M18 6L6 18" />
  </>,
);

export const IconPanelLeft = wrap(
  <>
    <rect x="3" y="4" width="18" height="16" rx="2" />
    <path d="M9 4v16" />
  </>,
);

export const IconPanelRight = wrap(
  <>
    <rect x="3" y="4" width="18" height="16" rx="2" />
    <path d="M15 4v16" />
  </>,
);

export const IconSun = wrap(
  <>
    <circle cx="12" cy="12" r="4" />
    <path d="M12 2v2" />
    <path d="M12 20v2" />
    <path d="M2 12h2" />
    <path d="M20 12h2" />
    <path d="M5 5l1.5 1.5" />
    <path d="M17.5 17.5L19 19" />
    <path d="M5 19l1.5-1.5" />
    <path d="M17.5 6.5L19 5" />
  </>,
);

export const IconMoon = wrap(
  <>
    <path d="M21 13A9 9 0 1 1 11 3a7 7 0 0 0 10 10z" />
  </>,
);

export const IconLogout = wrap(
  <>
    <path d="M10 17l-5-5 5-5" />
    <path d="M5 12h12" />
    <path d="M14 4h5a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-5" />
  </>,
);

export const IconRefresh = wrap(
  <>
    <path d="M21 12a9 9 0 1 1-3-6.7" />
    <path d="M21 4v5h-5" />
  </>,
);

export const IconTrash = wrap(
  <>
    <path d="M4 7h16" />
    <path d="M9 7V4h6v3" />
    <path d="M6 7l1 13a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2l1-13" />
    <path d="M10 11v6" />
    <path d="M14 11v6" />
  </>,
);

export const IconSend = wrap(
  <>
    <path d="M5 12l14-7-7 14-2-6z" />
  </>,
);

// --- Codex-style additions -------------------------------------------------

export const IconChevronDown = wrap(
  <>
    <path d="M6 9l6 6 6-6" />
  </>,
);

export const IconCheck = wrap(
  <>
    <path d="M5 13l4 4L19 7" />
  </>,
);

export const IconLock = wrap(
  <>
    <rect x="5" y="11" width="14" height="9" rx="2" />
    <path d="M8 11V8a4 4 0 0 1 8 0v3" />
  </>,
);

export const IconShield = wrap(
  <>
    <path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z" />
  </>,
);

export const IconShieldOff = wrap(
  <>
    <path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z" />
    <path d="M4 4l16 16" />
  </>,
);

export const IconUser = wrap(
  <>
    <circle cx="12" cy="8" r="4" />
    <path d="M4 21c1-4 4-6 8-6s7 2 8 6" />
  </>,
);

export const IconSettings = wrap(
  <>
    <circle cx="12" cy="12" r="3" />
    <path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3h0a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8v0a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z" />
  </>,
);

export const IconPencil = wrap(
  <>
    <path d="M4 20h4l11-11-4-4L4 16z" />
    <path d="M14 6l4 4" />
  </>,
);

export const IconArchive = wrap(
  <>
    <rect x="3" y="4" width="18" height="4" rx="1" />
    <path d="M5 8v11a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8" />
    <path d="M10 12h4" />
  </>,
);

export const IconPin = wrap(
  <>
    <path d="M14 3l7 7-4 1-3 3-1 4-7-7 4-1 3-3z" />
    <path d="M7 17l-3 3" />
  </>,
);

export const IconBot = wrap(
  <>
    <rect x="4" y="7" width="16" height="12" rx="3" />
    <circle cx="9" cy="13" r="1.2" fill="currentColor" stroke="none" />
    <circle cx="15" cy="13" r="1.2" fill="currentColor" stroke="none" />
    <path d="M12 3v4" />
    <path d="M9 19v2" />
    <path d="M15 19v2" />
  </>,
);

export const IconList = wrap(
  <>
    <path d="M8 6h13" />
    <path d="M8 12h13" />
    <path d="M8 18h13" />
    <circle cx="4" cy="6" r="1" fill="currentColor" stroke="none" />
    <circle cx="4" cy="12" r="1" fill="currentColor" stroke="none" />
    <circle cx="4" cy="18" r="1" fill="currentColor" stroke="none" />
  </>,
);

export const IconHistory = wrap(
  <>
    <path d="M3 12a9 9 0 1 0 3-6.7" />
    <path d="M3 4v5h5" />
    <path d="M12 7v5l3 2" />
  </>,
);

export const IconSidebar = wrap(
  <>
    <rect x="3" y="4" width="18" height="16" rx="2" />
    <path d="M9 4v16" />
  </>,
);
