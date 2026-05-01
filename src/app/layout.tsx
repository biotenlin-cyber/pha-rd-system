import type { Metadata } from "next";
import "./globals.css";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { siteConfig } from "@/data/site";

export const metadata: Metadata = {
  metadataBase: new URL("https://www.dubaicheng.com"),
  title: {
    default: `${siteConfig.name} — ${siteConfig.tagline}`,
    template: `%s — ${siteConfig.name}`,
  },
  description: siteConfig.description,
  keywords: [
    "都佰城",
    "PHA",
    "聚羟基脂肪酸酯",
    "生物可降解材料",
    "可持续材料",
    "生物基材料",
    "研发管理平台",
  ],
  openGraph: {
    type: "website",
    locale: "zh_CN",
    title: `${siteConfig.name} — ${siteConfig.tagline}`,
    description: siteConfig.description,
    siteName: siteConfig.name,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen flex flex-col bg-paper">
        <Header />
        <main className="flex-1 pt-11">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
