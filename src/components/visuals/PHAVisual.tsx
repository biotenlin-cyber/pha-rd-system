import { cn } from "@/lib/utils";

type Props = {
  size?: "lg" | "md" | "sm";
  theme?: "light" | "dark";
  className?: string;
};

// 抽象 PHA 颗粒视觉:大颗粒 + 卫星颗粒 + 柔和阴影,模拟苹果产品近景
export function PHAVisual({ size = "lg", theme = "light", className }: Props) {
  const dimension =
    size === "lg" ? "h-[440px] sm:h-[520px]" : size === "md" ? "h-[320px]" : "h-[220px]";

  const isDark = theme === "dark";

  return (
    <div className={cn("relative w-full mx-auto max-w-3xl", dimension, className)}>
      <svg
        viewBox="0 0 800 520"
        className="w-full h-full"
        aria-hidden
      >
        <defs>
          <radialGradient id="pha-main" cx="35%" cy="30%" r="80%">
            <stop offset="0%" stopColor={isDark ? "#f5f5f7" : "#ffffff"} />
            <stop offset="50%" stopColor={isDark ? "#d2d2d7" : "#e8eef9"} />
            <stop offset="100%" stopColor={isDark ? "#86868b" : "#9bb3d8"} />
          </radialGradient>
          <radialGradient id="pha-blue" cx="30%" cy="25%" r="75%">
            <stop offset="0%" stopColor="#7eb6ff" />
            <stop offset="60%" stopColor="#3a86ff" />
            <stop offset="100%" stopColor="#0a4cb8" />
          </radialGradient>
          <radialGradient id="pha-pearl" cx="35%" cy="30%" r="75%">
            <stop offset="0%" stopColor="#ffffff" />
            <stop offset="60%" stopColor="#f1f5fb" />
            <stop offset="100%" stopColor="#c8d4e8" />
          </radialGradient>
          <filter id="pha-shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur in="SourceAlpha" stdDeviation="16" />
            <feOffset dx="0" dy="20" />
            <feComponentTransfer>
              <feFuncA type="linear" slope="0.25" />
            </feComponentTransfer>
            <feMerge>
              <feMergeNode />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* 大颗粒 - 主体 */}
        <circle cx="400" cy="280" r="170" fill="url(#pha-main)" filter="url(#pha-shadow)" />

        {/* 高光 */}
        <ellipse cx="350" cy="220" rx="55" ry="30" fill="#ffffff" opacity="0.5" />

        {/* 卫星颗粒 */}
        <circle cx="180" cy="200" r="62" fill="url(#pha-blue)" filter="url(#pha-shadow)" />
        <ellipse cx="160" cy="180" rx="20" ry="12" fill="#ffffff" opacity="0.4" />

        <circle cx="640" cy="180" r="48" fill="url(#pha-pearl)" filter="url(#pha-shadow)" />
        <ellipse cx="625" cy="165" rx="14" ry="8" fill="#ffffff" opacity="0.6" />

        <circle cx="660" cy="360" r="78" fill="url(#pha-main)" filter="url(#pha-shadow)" />
        <ellipse cx="630" cy="320" rx="24" ry="14" fill="#ffffff" opacity="0.5" />

        <circle cx="160" cy="380" r="42" fill="url(#pha-blue)" filter="url(#pha-shadow)" />
        <ellipse cx="148" cy="368" rx="13" ry="7" fill="#ffffff" opacity="0.4" />

        <circle cx="280" cy="430" r="32" fill="url(#pha-pearl)" filter="url(#pha-shadow)" />
        <circle cx="520" cy="120" r="26" fill="url(#pha-pearl)" filter="url(#pha-shadow)" />
      </svg>
    </div>
  );
}
