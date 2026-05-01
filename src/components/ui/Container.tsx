import { cn } from "@/lib/utils";

type Props = React.HTMLAttributes<HTMLDivElement> & {
  size?: "default" | "narrow" | "wide";
};

export function Container({
  size = "default",
  className,
  children,
  ...rest
}: Props) {
  const sizeClass =
    size === "narrow"
      ? "max-w-3xl"
      : size === "wide"
        ? "max-w-7xl"
        : "max-w-6xl";

  return (
    <div className={cn("mx-auto w-full px-4 sm:px-6 lg:px-8", sizeClass, className)} {...rest}>
      {children}
    </div>
  );
}
