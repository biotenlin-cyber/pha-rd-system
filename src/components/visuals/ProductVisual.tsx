import { cn } from "@/lib/utils";

type Tone = "blue" | "graphite" | "pearl" | "midnight" | "champagne";

const toneStops: Record<Tone, { from: string; mid: string; to: string }> = {
  blue: { from: "#9ec5ff", mid: "#3a86ff", to: "#0a4cb8" },
  graphite: { from: "#c8c8cd", mid: "#7d7d82", to: "#1d1d1f" },
  pearl: { from: "#ffffff", mid: "#e8edf5", to: "#b8c3d8" },
  midnight: { from: "#5a6b8a", mid: "#2a3a5e", to: "#0d1428" },
  champagne: { from: "#f6e7c4", mid: "#d6bb83", to: "#8a6d3a" },
};

type Props = {
  tone?: Tone;
  shape?: "pellet" | "film" | "fiber";
  className?: string;
};

// 模拟苹果产品图:大尺寸圆/胶囊形,带柔光与阴影
export function ProductVisual({ tone = "blue", shape = "pellet", className }: Props) {
  const c = toneStops[tone];
  const id = `${tone}-${shape}`;

  return (
    <div className={cn("relative w-full max-w-md mx-auto aspect-[4/3]", className)}>
      <svg viewBox="0 0 600 450" className="w-full h-full" aria-hidden>
        <defs>
          <radialGradient id={`${id}-grad`} cx="35%" cy="28%" r="80%">
            <stop offset="0%" stopColor={c.from} />
            <stop offset="55%" stopColor={c.mid} />
            <stop offset="100%" stopColor={c.to} />
          </radialGradient>
          <filter id={`${id}-shadow`} x="-30%" y="-20%" width="160%" height="160%">
            <feGaussianBlur in="SourceAlpha" stdDeviation="20" />
            <feOffset dx="0" dy="28" />
            <feComponentTransfer>
              <feFuncA type="linear" slope="0.22" />
            </feComponentTransfer>
            <feMerge>
              <feMergeNode />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {shape === "pellet" && (
          <>
            <circle cx="300" cy="240" r="150" fill={`url(#${id}-grad)`} filter={`url(#${id}-shadow)`} />
            <ellipse cx="248" cy="180" rx="48" ry="24" fill="#ffffff" opacity="0.45" />
          </>
        )}
        {shape === "film" && (
          <>
            <rect
              x="100"
              y="120"
              width="400"
              height="240"
              rx="14"
              fill={`url(#${id}-grad)`}
              filter={`url(#${id}-shadow)`}
              transform="rotate(-6 300 240)"
            />
            <ellipse cx="240" cy="190" rx="80" ry="14" fill="#ffffff" opacity="0.35" transform="rotate(-6 300 240)" />
          </>
        )}
        {shape === "fiber" && (
          <>
            {[0, 1, 2, 3, 4].map((i) => (
              <rect
                key={i}
                x={150 + i * 60}
                y="80"
                width="40"
                height="320"
                rx="20"
                fill={`url(#${id}-grad)`}
                filter={`url(#${id}-shadow)`}
                transform={`rotate(${(i - 2) * 4} ${170 + i * 60} 240)`}
              />
            ))}
          </>
        )}
      </svg>
    </div>
  );
}
