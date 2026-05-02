import { cn } from "@/lib/utils";

type Theme = "light" | "dark" | "fog";

type Props = {
  theme?: Theme;
  eyebrow?: string;
  title: React.ReactNode;
  subtitle?: React.ReactNode;
  ctas?: React.ReactNode;
  visual?: React.ReactNode;
  size?: "hero" | "half";
  align?: "center" | "left";
  className?: string;
};

const themeClass: Record<Theme, string> = {
  light: "bg-paper text-ink",
  dark: "bg-obsidian text-paper",
  fog: "bg-fog text-ink",
};

const sizeClass = {
  hero: "min-h-[680px] sm:min-h-[720px] py-16 sm:py-20",
  half: "min-h-[560px] py-14 sm:py-16",
} as const;

export function Tile({
  theme = "light",
  eyebrow,
  title,
  subtitle,
  ctas,
  visual,
  size = "hero",
  align = "center",
  className,
}: Props) {
  const subtitleColor = theme === "dark" ? "text-white/70" : "text-ash";
  const eyebrowColor = theme === "dark" ? "text-white/80" : "text-ink";

  return (
    <section
      className={cn(
        "relative overflow-hidden flex flex-col",
        themeClass[theme],
        sizeClass[size],
        className,
      )}
    >
      <div
        className={cn(
          "relative z-10 mx-auto w-full max-w-apple px-6 sm:px-8 flex flex-col items-center",
          align === "left" ? "items-start text-left" : "items-center text-center",
        )}
      >
        {eyebrow && (
          <div className={cn("text-eyebrow mb-3", eyebrowColor)}>{eyebrow}</div>
        )}
        <h2 className="text-display sm:text-hero font-semibold tracking-tight max-w-4xl fade-up">
          {title}
        </h2>
        {subtitle && (
          <p
            className={cn(
              "mt-4 text-lead max-w-2xl fade-up-soft",
              subtitleColor,
            )}
          >
            {subtitle}
          </p>
        )}
        {ctas && (
          <div
            className={cn(
              "mt-6 flex flex-wrap gap-x-6 gap-y-3",
              align === "left" ? "justify-start" : "justify-center",
            )}
          >
            {ctas}
          </div>
        )}
      </div>
      {visual && (
        <div className="relative z-0 mt-10 sm:mt-12 flex-1 flex items-end justify-center w-full">
          {visual}
        </div>
      )}
    </section>
  );
}
