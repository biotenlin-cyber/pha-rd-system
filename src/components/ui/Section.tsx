import { cn } from "@/lib/utils";
import { Container } from "./Container";

type Props = {
  eyebrow?: string;
  title?: React.ReactNode;
  subtitle?: React.ReactNode;
  align?: "center" | "left";
  className?: string;
  containerClassName?: string;
  children?: React.ReactNode;
  id?: string;
};

export function Section({
  eyebrow,
  title,
  subtitle,
  align = "center",
  className,
  containerClassName,
  children,
  id,
}: Props) {
  const alignClass = align === "center" ? "text-center mx-auto" : "text-left";

  return (
    <section id={id} className={cn("py-16 sm:py-20 lg:py-24", className)}>
      <Container className={containerClassName}>
        {(eyebrow || title || subtitle) && (
          <div className={cn("max-w-2xl mb-12 sm:mb-16", alignClass)}>
            {eyebrow && (
              <div className="text-sm font-medium uppercase tracking-[0.2em] text-accent-500 mb-3">
                {eyebrow}
              </div>
            )}
            {title && (
              <h2 className="text-3xl sm:text-4xl font-semibold text-slate-900 leading-tight">
                {title}
              </h2>
            )}
            {subtitle && (
              <p className="mt-4 text-base sm:text-lg text-slate-600 leading-relaxed">
                {subtitle}
              </p>
            )}
          </div>
        )}
        {children}
      </Container>
    </section>
  );
}
