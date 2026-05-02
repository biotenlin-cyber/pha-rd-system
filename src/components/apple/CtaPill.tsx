import Link from "next/link";
import { cn } from "@/lib/utils";

type Variant = "filled" | "outline" | "filledLight";

type Props = {
  href: string;
  children: React.ReactNode;
  variant?: Variant;
  className?: string;
};

const variantClass: Record<Variant, string> = {
  filled: "bg-appleBlue text-white hover:bg-appleBlueHover",
  outline: "border border-link text-link hover:bg-link hover:text-white",
  filledLight: "bg-white text-ink hover:bg-fog",
};

export function CtaPill({ href, children, variant = "filled", className }: Props) {
  return (
    <Link
      href={href}
      className={cn(
        "inline-flex items-center justify-center rounded-full px-5 h-10 text-sm font-medium transition",
        variantClass[variant],
        className,
      )}
    >
      {children}
    </Link>
  );
}
