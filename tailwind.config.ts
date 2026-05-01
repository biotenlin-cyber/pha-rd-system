import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eef4ff",
          100: "#dae6ff",
          200: "#bccfff",
          300: "#8eaeff",
          400: "#5c84ff",
          500: "#365dff",
          600: "#1f3ee0",
          700: "#1a32b8",
          800: "#142a91",
          900: "#0b3d91",
          950: "#081f5c",
        },
        accent: {
          400: "#38bdf8",
          500: "#1e90ff",
          600: "#0c7be0",
        },
      },
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          '"PingFang SC"',
          '"Hiragino Sans GB"',
          '"Microsoft YaHei"',
          "Inter",
          "system-ui",
          "sans-serif",
        ],
      },
      backgroundImage: {
        "tech-radial":
          "radial-gradient(circle at 20% 20%, rgba(56,189,248,0.25), transparent 50%), radial-gradient(circle at 80% 0%, rgba(30,144,255,0.25), transparent 45%), linear-gradient(135deg, #0b3d91 0%, #142a91 60%, #081f5c 100%)",
        "tech-soft":
          "linear-gradient(180deg, #ffffff 0%, #f1f5ff 60%, #e6efff 100%)",
      },
      boxShadow: {
        soft: "0 1px 2px rgba(15, 23, 42, 0.04), 0 8px 24px rgba(15, 23, 42, 0.06)",
      },
    },
  },
  plugins: [],
};

export default config;
