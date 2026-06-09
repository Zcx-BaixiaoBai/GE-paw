/**
 * gepaw mascot (same as logo symbol). Used in Hero and Nav.
 */
import { CatPawIcon } from "./CatPawIcon";

interface gepawMascotProps {
  size?: number;
  className?: string;
}

export function gepawMascot({
  size = 80,
  className = "",
}: gepawMascotProps) {
  return <CatPawIcon size={size} className={className} />;
}
