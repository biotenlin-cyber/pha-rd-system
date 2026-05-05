import { Reveal } from "./Reveal";
import { cn } from "@/lib/utils";

export type Pillar = {
  value: string;
  label: string;
};

type Props = {
  eyebrow?: React.ReactNode;
  title?: React.ReactNode;
  pillars: Pillar[];
  /** light = 灰底白卡 / dark = 黑底深卡 */
  tone?: "light" | "dark";
  className?: string;
};

/**
 * 4 数据柱组件 — 用 token 字号(text-display)替代之前 inline clamp。
 * 出现于产品详情页 highlights / 平台 stats 等位置。
 */
export function DataPillars({ eyebrow, title, pillars, tone = "light", className }: Props) {
  const dark = tone === "dark";
  return (
    <section className={cn(dark ? "bg-coal text-white" : "bg-fog text-ink", className)}>
      <div className="mx-auto max-w-apple px-6 sm:px-8 py-20 sm:py-28">
        {(eyebrow || title) && (
          <Reveal>
            <div className="text-center max-w-3xl mx-auto mb-14">
              {eyebrow && (
                <div className={cn("text-eyebrow mb-3", dark ? "text-white/85" : "text-ink")}>
                  {eyebrow}
                </div>
              )}
              {title && (
                <h2 className="text-display font-semibold tracking-tight">{title}</h2>
              )}
            </div>
          </Reveal>
        )}
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {pillars.map((p, i) => (
            <Reveal key={p.label} delay={i * 80}>
              <div
                className={cn(
                  "rounded-tile p-8 h-full text-center flex flex-col items-center justify-center min-h-[180px]",
                  dark ? "bg-obsidian" : "bg-paper",
                )}
              >
                <div
                  className={cn(
                    "text-display font-semibold tracking-tight",
                    dark ? "text-white" : "text-ink",
                  )}
                >
                  {p.value}
                </div>
                <div className={cn("mt-2 text-sm", dark ? "text-white/65" : "text-smoke")}>
                  {p.label}
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
