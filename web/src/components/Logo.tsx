// GE-paw flat logo. A stylized code symbol rendered as geometric shapes so
// it scales cleanly at any size and inherits the current text color.
import type { CSSProperties } from "react";

export type LogoProps = {
  size?: number;
  className?: string;
  style?: CSSProperties;
  title?: string;
};

export function Logo({ size = 18, className, style, title }: LogoProps) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 32 32"
      width={size}
      height={size}
      className={className}
      style={style}
      role={title ? "img" : "presentation"}
      aria-label={title}
      aria-hidden={title ? undefined : true}
    >
      {title ? <title>{title}</title> : null}
      {/* Code symbol inspired by Codex */}
      <path
        d="M10.5 6.5L4 16l6.5 9.5M21.5 6.5L28 16l-6.5 9.5M18 4l-4 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
