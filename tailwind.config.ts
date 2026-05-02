import type { Config } from "tailwindcss";

/**
 * 设计 token 单一来源:docs/DESIGN.md
 * 修改本文件后请同步更新 DESIGN.md。
 */
const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // 背景 / 表面
        paper: "#ffffff",
        fog: "#f5f5f7", // Athens Gray - apple.com 标志主灰
        haze: "#fafafc",
        obsidian: "#000000",
        coal: "#161617",

        // 文字阶梯
        ink: "#1d1d1f", // Shark - apple.com 主黑
        ash: "#424245", // 正文次级
        smoke: "#6e6e73", // 三级 / 标签
        silver: "#86868b", // 弱文字

        // 描边
        hairline: "#d2d2d7",

        // 链接 vs 主按钮 - 必须区分
        link: "#0066cc", // 内联文本链接(Science Blue)
        linkHover: "#0077ed",
        appleBlue: "#0071e3", // 主胶囊按钮(Buy / 申请样品)
        appleBlueHover: "#0077ed",
      },
      fontFamily: {
        sans: [
          '"SF Pro Display"',
          '"SF Pro Text"',
          '"SF Pro Icons"',
          "-apple-system",
          "BlinkMacSystemFont",
          '"PingFang SC"',
          '"Hiragino Sans GB"',
          '"Microsoft YaHei"',
          "Helvetica Neue",
          "Helvetica",
          "Arial",
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
        eyebrow: ["0.75rem", { lineHeight: "1.2", letterSpacing: "0.06em", fontWeight: "600" }],
        // 字号阶梯 - 与 apple.com 实测对齐 (DESIGN.md §2)
        mega: ["clamp(3.5rem, 8.5vw, 8rem)", { lineHeight: "1.0", letterSpacing: "-0.035em", fontWeight: "600" }],
        hero: ["clamp(2.75rem, 6.4vw, 6rem)", { lineHeight: "1.04", letterSpacing: "-0.005em", fontWeight: "600" }],
        display: ["clamp(2.25rem, 4.4vw, 3.75rem)", { lineHeight: "1.08", letterSpacing: "-0.003em", fontWeight: "600" }],
        section: ["clamp(1.75rem, 2.8vw, 2.5rem)", { lineHeight: "1.12", letterSpacing: "-0.003em", fontWeight: "600" }],
        lead: ["clamp(1.125rem, 1.4vw, 1.375rem)", { lineHeight: "1.4", letterSpacing: "0", fontWeight: "400" }],
        body: ["1.0625rem", { lineHeight: "1.47", letterSpacing: "-0.022em" }], // 17px - apple.com desktop 正文
      },
      letterSpacing: {
        eyebrow: "0.06em",
        tightHero: "-0.005em",
        tightDisplay: "-0.003em",
      },
      borderRadius: {
        // apple.com 实测圆角阶梯
        button: "9999px",
        image: "1.125rem", // 18px
        tile: "1.375rem", // 22px - 大多数卡片
        marble: "1.75rem", // 28px - 大模块
      },
      boxShadow: {
        tile: "0 0.5px 1px rgba(0,0,0,0.04), 0 6px 20px rgba(0,0,0,0.05)",
        glow: "0 30px 80px rgba(0, 113, 227, 0.18)",
      },
      maxWidth: {
        // apple.com 全站标准容器
        apple: "980px",
        appleWide: "1280px",
        prose2: "44rem",
      },
      transitionTimingFunction: {
        apple: "cubic-bezier(0.22, 1, 0.36, 1)",
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
