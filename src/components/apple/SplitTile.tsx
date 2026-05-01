import { cn } from "@/lib/utils";

type Theme = "light" | "dark" | "fog";

type SplitTileItem = {
  theme?: Theme;
  eyebrow?: string;
  title: React.ReactNode;
  subtitle?: React.ReactNode;
  ctas?: React.ReactNode;
  visual?: React.ReactNode;
};

const themeClass: Record<Theme, string> = {
  light: "bg-paper text-ink",
  dark: "bg-obsidian text-paper",
  fog: "bg-fog text-ink",
};

export function SplitTile({ items }: { items: [SplitTileItem, SplitTileItem] }) {
  return (
    <section className="grid gap-2 md:grid-cols-2 bg-fog">
      {items.map((item, idx) => {
        const theme = item.theme ?? "light";
        const subtitleColor = theme === "dark" ? "text-white/70" : "text-ash";
        const eyebrowColor = theme === "dark" ? "text-white/80" : "text-ink";

        return (
          <div
            key={idx}
            className={cn(
              "relative overflow-hidden flex flex-col min-h-[520px] py-14 px-6 sm:px-10",
              themeClass[theme],
            )}
          >
            <div className="text-center mx-auto max-w-md">
              {item.eyebrow && (
                <div className={cn("text-eyebrow mb-2", eyebrowColor)}>
                  {item.eyebrow}
                </div>
              )}
              <h3 className="text-section font-semibold tracking-tight">
                {item.title}
              </h3>
              {item.subtitle && (
                <p className={cn("mt-3 text-base sm:text-lg", subtitleColor)}>
                  {item.subtitle}
                </p>
              )}
              {item.ctas && (
                <div className="mt-5 flex flex-wrap justify-center gap-x-5 gap-y-2">
                  {item.ctas}
                </div>
              )}
            </div>
            {item.visual && (
              <div className="mt-10 flex-1 flex items-end justify-center w-full">
                {item.visual}
              </div>
            )}
          </div>
        );
      })}
    </section>
  );
}
