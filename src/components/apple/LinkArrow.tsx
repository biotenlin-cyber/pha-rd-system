import Link from "next/link";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  children: React.ReactNode;
  size?: "sm" | "md" | "lg";
  className?: string;
};

const sizeClass = {
  sm: "text-sm",
  md: "text-base",
  lg: "text-lg",
} as const;

export function LinkArrow({ href, children, size = "md", className }: Props) {
  return (
    <Link href={href} className={cn("link-arrow", sizeClass[size], className)}>
      {children}
    </Link>
  );
}
