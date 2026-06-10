// GE-paw flat logo. A stylized paw print rendered as geometric shapes so
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
      {/* Four toe pads (top row) */}
      <circle cx="9" cy="9" r="4.2" fill="currentColor" opacity="0.85" />
      <circle cx="23" cy="9" r="4.2" fill="currentColor" opacity="0.85" />
      <circle cx="5" cy="17" r="3.5" fill="currentColor" opacity="0.75" />
      <circle cx="27" cy="17" r="3.5" fill="currentColor" opacity="0.75" />
      {/* Main pad */}
      <path
        d="M16 14c-5.5 0-9 3.8-9 7.5 0 3 2.4 5.5 5.5 5.5 1.4 0 2.4-.5 3.5-.5s2.1.5 3.5.5c3.1 0 5.5-2.5 5.5-5.5 0-3.7-3.5-7.5-9-7.5z"
        fill="currentColor"
      />
    </svg>
  );
}
