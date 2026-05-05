import Link from "next/link";
import { Reveal } from "./Reveal";
import { LinkArrow } from "./LinkArrow";
import { cn } from "@/lib/utils";

type Cta = {
  label: string;
  href: string;
  /** primary 渲染为蓝胶囊填充按钮(申请样品 / Buy 风格)。默认 false 走 LinkArrow。 */
  primary?: boolean;
};

type Props = {
  eyebrow?: React.ReactNode;
  /** 主标题。允许 ReactNode 以支持 <br/> 与彩色 <span/>。 */
  title: React.ReactNode;
  subtitle?: React.ReactNode;
  cta?: Cta[];
  /** 大视觉,在文字下方居中渲染。 */
  visual?: React.ReactNode;
  /**
   * mega — 跨页大标题(8rem 上限),首页 Tile 用
   * hero — 产品 / 平台 / 关于 hero
   * display — 二级 hero(news 详情、cases 详情)
   * 默认 hero。
   */
  size?: "mega" | "hero" | "display";
  /** light = 白底深字 / dark = 黑底白字 */
  tone?: "light" | "dark";
  /** 默认居中。少数情况(news 详情)用 left。 */
  align?: "center" | "left";
  /** 整段额外 className,例:背景渐变。 */
  className?: string;
  /** 视觉容器 className,默认 max-w-apple px-6 sm:px-8 pb-16 sm:pb-24 */
  visualClassName?: string;
  /** 是否包 <Reveal>,默认 true。 */
  reveal?: boolean;
};

const sizeClass: Record<NonNullable<Props["size"]>, string> = {
  mega: "text-mega",
  hero: "text-hero",
  display: "text-display",
};

/**
 * 全站统一 hero primitive。
 * 强制 max-w-apple(980)、token 字号、tracking-tight,从源头消除 inline clamp / letter-spacing 漂移。
 */
export function Hero({
  eyebrow,
  title,
  subtitle,
  cta,
  visual,
  size = "hero",
  tone = "light",
  align = "center",
  className,
  visualClassName,
  reveal = true,
}: Props) {
  const dark = tone === "dark";
  const eyebrowColor = dark ? "text-white/85" : "text-ink";
  const subtitleColor = dark ? "text-white/75" : "text-ash";
  const titleColor = dark ? "text-white" : "text-ink";

  const W = reveal ? Reveal : Passthrough;

  return (
    <section
      className={cn(
        "relative overflow-hidden",
        dark ? "bg-obsidian text-white" : "bg-paper text-ink",
        className,
      )}
    >
      <div
        className={cn(
          "mx-auto max-w-apple px-6 sm:px-8 pt-16 sm:pt-24 pb-8",
          align === "center" ? "text-center" : "text-left",
        )}
      >
        {eyebrow && (
          <div className={cn("text-eyebrow mb-3 fade-up", eyebrowColor)}>{eyebrow}</div>
        )}

        <W>
          <h1
            className={cn(
              sizeClass[size],
              "font-semibold tracking-tight",
              titleColor,
              align === "center" && "max-w-3xl mx-auto",
            )}
          >
            {title}
          </h1>
        </W>

        {subtitle && (
          <W delay={120}>
            <p
              className={cn(
                "mt-7 text-lead max-w-2xl",
                subtitleColor,
                align === "center" && "mx-auto",
              )}
            >
              {subtitle}
            </p>
          </W>
        )}

        {cta && cta.length > 0 && (
          <W delay={200}>
            <div
              className={cn(
                "mt-7 flex flex-wrap gap-x-6 gap-y-3",
                align === "center" ? "justify-center" : "justify-start",
              )}
            >
              {cta.map((c) =>
                c.primary ? (
                  <Link
                    key={c.href + c.label}
                    href={c.href}
                    className="inline-flex items-center justify-center h-11 px-6 rounded-full bg-appleBlue text-white text-[15px] font-medium hover:bg-appleBlueHover transition"
                  >
                    {c.label}
                  </Link>
                ) : (
                  <LinkArrow
                    key={c.href + c.label}
                    href={c.href}
                    size="lg"
                    className={dark ? "text-white hover:text-white/85" : undefined}
                  >
                    {c.label}
                  </LinkArrow>
                ),
              )}
            </div>
          </W>
        )}
      </div>

      {visual && (
        <W delay={120}>
          <div
            className={cn(
              "mx-auto max-w-apple px-6 sm:px-8 pb-12 sm:pb-20",
              visualClassName,
            )}
          >
            {visual}
          </div>
        </W>
      )}
    </section>
  );
}

function Passthrough({ children }: { children: React.ReactNode; delay?: number }) {
  return <>{children}</>;
}
