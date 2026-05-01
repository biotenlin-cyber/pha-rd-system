import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#1d1d1f",
        paper: "#ffffff",
        fog: "#f5f5f7",
        haze: "#fbfbfd",
        smoke: "#86868b",
        ash: "#6e6e73",
        hairline: "#d2d2d7",
        link: "#0071e3",
        linkHover: "#0077ed",
        obsidian: "#000000",
        coal: "#161617",
      },
      fontFamily: {
        sans: [
          '"SF Pro Display"',
          '"SF Pro Text"',
          "-apple-system",
          "BlinkMacSystemFont",
          '"PingFang SC"',
          '"Hiragino Sans GB"',
          '"Microsoft YaHei"',
          "Inter",
          "system-ui",
          "sans-serif",
        ],
        mono: [
          '"SF Mono"',
          "ui-monospace",
          "Menlo",
          "Monaco",
          "Consolas",
          "monospace",
        ],
      },
      fontSize: {
        eyebrow: ["0.8125rem", { lineHeight: "1.2", letterSpacing: "0.01em", fontWeight: "500" }],
        // Apple-grade hero scale (clamps inline at component level when needed)
        hero: ["clamp(2.75rem, 5.6vw, 5.5rem)", { lineHeight: "1.05", letterSpacing: "-0.025em", fontWeight: "600" }],
        display: ["clamp(2rem, 3.6vw, 3.25rem)", { lineHeight: "1.1", letterSpacing: "-0.02em", fontWeight: "600" }],
        section: ["clamp(1.75rem, 2.6vw, 2.25rem)", { lineHeight: "1.15", letterSpacing: "-0.015em", fontWeight: "600" }],
        lead: ["clamp(1.125rem, 1.4vw, 1.375rem)", { lineHeight: "1.35", letterSpacing: "0", fontWeight: "400" }],
      },
      letterSpacing: {
        eyebrow: "0.02em",
        tight2: "-0.025em",
      },
      borderRadius: {
        tile: "1.25rem",
        chunk: "1.5rem",
        marble: "2rem",
      },
      boxShadow: {
        tile: "0 0.5px 1px rgba(0,0,0,0.04), 0 6px 20px rgba(0,0,0,0.05)",
        glow: "0 30px 80px rgba(0, 113, 227, 0.18)",
      },
      maxWidth: {
        prose2: "44rem",
      },
      animation: {
        "fade-up": "fadeUp 700ms cubic-bezier(0.22, 1, 0.36, 1) both",
      },
      keyframes: {
        fadeUp: {
          from: { opacity: "0", transform: "translateY(14px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
