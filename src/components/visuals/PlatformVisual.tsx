import { cn } from "@/lib/utils";

type Props = {
  className?: string;
  compact?: boolean;
};

// 抽象研发管理平台视觉:仿苹果产品图风格的"设备"展示一个仪表盘 mockup
export function PlatformVisual({ className, compact = false }: Props) {
  const height = compact ? "h-[300px]" : "h-[440px] sm:h-[500px]";

  return (
    <div className={cn("relative w-full mx-auto max-w-4xl", height, className)}>
      <svg viewBox="0 0 900 520" className="w-full h-full" aria-hidden>
        <defs>
          <linearGradient id="device-frame" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#3a3a3c" />
            <stop offset="100%" stopColor="#1c1c1e" />
          </linearGradient>
          <linearGradient id="device-screen" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#fbfbfd" />
            <stop offset="100%" stopColor="#eef0f4" />
          </linearGradient>
          <linearGradient id="bar-blue" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#5ea3ff" />
            <stop offset="100%" stopColor="#0a4cb8" />
          </linearGradient>
          <linearGradient id="bar-pearl" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#d2dcf0" />
            <stop offset="100%" stopColor="#a8b8d6" />
          </linearGradient>
          <filter id="device-shadow" x="-10%" y="-10%" width="120%" height="130%">
            <feGaussianBlur in="SourceAlpha" stdDeviation="14" />
            <feOffset dx="0" dy="22" />
            <feComponentTransfer>
              <feFuncA type="linear" slope="0.22" />
            </feComponentTransfer>
            <feMerge>
              <feMergeNode />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* 设备外壳 (仿 MacBook 屏幕) */}
        <g filter="url(#device-shadow)">
          <rect x="60" y="50" width="780" height="430" rx="22" fill="url(#device-frame)" />
          <rect x="74" y="64" width="752" height="402" rx="14" fill="url(#device-screen)" />
        </g>

        {/* 顶部栏 */}
        <rect x="74" y="64" width="752" height="40" fill="#ffffff" />
        <circle cx="100" cy="84" r="5" fill="#ff5f57" />
        <circle cx="120" cy="84" r="5" fill="#febc2e" />
        <circle cx="140" cy="84" r="5" fill="#28c840" />
        <rect x="370" y="76" width="160" height="16" rx="8" fill="#e5e7ec" />

        {/* 侧边栏 */}
        <rect x="74" y="104" width="160" height="362" fill="#f4f5f8" />
        <rect x="92" y="124" width="124" height="14" rx="3" fill="#0a4cb8" />
        <rect x="92" y="148" width="100" height="10" rx="3" fill="#c4cdde" />
        <rect x="92" y="170" width="118" height="10" rx="3" fill="#c4cdde" />
        <rect x="92" y="192" width="92" height="10" rx="3" fill="#c4cdde" />
        <rect x="92" y="214" width="110" height="10" rx="3" fill="#c4cdde" />
        <rect x="92" y="236" width="84" height="10" rx="3" fill="#c4cdde" />
        <rect x="92" y="258" width="116" height="10" rx="3" fill="#c4cdde" />

        {/* 主区:KPI 卡片 */}
        <g>
          <rect x="254" y="124" width="170" height="80" rx="10" fill="#ffffff" stroke="#e5e7ec" />
          <rect x="270" y="138" width="60" height="9" rx="3" fill="#a8b8d6" />
          <rect x="270" y="158" width="100" height="20" rx="3" fill="#1d1d1f" />
          <rect x="270" y="186" width="130" height="6" rx="3" fill="url(#bar-blue)" />

          <rect x="438" y="124" width="170" height="80" rx="10" fill="#ffffff" stroke="#e5e7ec" />
          <rect x="454" y="138" width="60" height="9" rx="3" fill="#a8b8d6" />
          <rect x="454" y="158" width="80" height="20" rx="3" fill="#1d1d1f" />
          <rect x="454" y="186" width="100" height="6" rx="3" fill="url(#bar-blue)" />

          <rect x="622" y="124" width="190" height="80" rx="10" fill="#ffffff" stroke="#e5e7ec" />
          <rect x="638" y="138" width="60" height="9" rx="3" fill="#a8b8d6" />
          <rect x="638" y="158" width="120" height="20" rx="3" fill="#1d1d1f" />
          <rect x="638" y="186" width="80" height="6" rx="3" fill="url(#bar-blue)" />
        </g>

        {/* 主图表 */}
        <g>
          <rect x="254" y="220" width="354" height="220" rx="10" fill="#ffffff" stroke="#e5e7ec" />
          <rect x="270" y="236" width="100" height="11" rx="3" fill="#1d1d1f" />
          <rect x="270" y="254" width="160" height="8" rx="3" fill="#a8b8d6" />

          {/* 柱状图 */}
          {[0, 1, 2, 3, 4, 5, 6, 7].map((i) => {
            const heights = [70, 100, 88, 130, 115, 150, 132, 170];
            const useBlue = i % 2 === 0;
            return (
              <rect
                key={i}
                x={290 + i * 36}
                y={420 - heights[i]}
                width="22"
                height={heights[i]}
                rx="4"
                fill={useBlue ? "url(#bar-blue)" : "url(#bar-pearl)"}
              />
            );
          })}
        </g>

        {/* 右侧列表 */}
        <g>
          <rect x="622" y="220" width="190" height="220" rx="10" fill="#ffffff" stroke="#e5e7ec" />
          <rect x="638" y="236" width="120" height="11" rx="3" fill="#1d1d1f" />
          {[0, 1, 2, 3, 4].map((i) => (
            <g key={i} transform={`translate(0, ${i * 32})`}>
              <circle cx="650" cy="276" r="6" fill="#0a4cb8" />
              <rect x="664" y="270" width="120" height="7" rx="3" fill="#1d1d1f" />
              <rect x="664" y="282" width="80" height="6" rx="3" fill="#a8b8d6" />
            </g>
          ))}
        </g>
      </svg>
    </div>
  );
}
