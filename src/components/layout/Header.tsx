"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { ChevronRight, Search, X, Menu } from "lucide-react";
import { mainNav, siteConfig } from "@/data/site";
import { cn } from "@/lib/utils";

export function Header() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    setMobileOpen(false);
  }, [pathname]);

  useEffect(() => {
    if (mobileOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [mobileOpen]);

  return (
    <header className="fixed top-9 inset-x-0 z-50 h-11 bg-paper/72 apple-blur border-b border-hairline/60">
      <div className="mx-auto max-w-[1024px] h-full px-4 sm:px-6 flex items-center justify-between text-[13px] text-ink/85">
        <Link
          href="/"
          aria-label={siteConfig.name}
          className="flex items-center gap-1.5 font-medium text-ink"
        >
          <Logo />
          <span className="sr-only">{siteConfig.name}</span>
        </Link>

        <nav className="hidden md:flex items-center gap-7 text-[12.5px]">
          {mainNav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "opacity-80 hover:opacity-100 transition",
                pathname.startsWith(item.href) && "opacity-100",
              )}
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-4 text-ink/85">
          <button
            type="button"
            aria-label="搜索"
            className="hidden md:inline-flex items-center justify-center h-8 w-8 hover:opacity-100 opacity-80 transition"
          >
            <Search size={16} strokeWidth={1.6} />
          </button>
          <button
            type="button"
            className="md:hidden inline-flex items-center justify-center h-8 w-8"
            aria-label={mobileOpen ? "关闭菜单" : "打开菜单"}
            aria-expanded={mobileOpen}
            onClick={() => setMobileOpen((v) => !v)}
          >
            {mobileOpen ? <X size={18} strokeWidth={1.6} /> : <Menu size={18} strokeWidth={1.6} />}
          </button>
        </div>
      </div>

      {mobileOpen && (
        <div className="md:hidden fixed inset-x-0 top-[80px] bottom-0 bg-paper border-t border-hairline overflow-y-auto">
          <nav className="px-6 py-4">
            {mainNav.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="flex items-center justify-between py-4 text-xl font-medium text-ink border-b border-hairline"
              >
                {item.label}
                <ChevronRight size={18} className="text-smoke" />
              </Link>
            ))}
            <div className="mt-6 text-xs text-smoke">
              <Link href="/contact" className="text-link">
                联系我们 ›
              </Link>
            </div>
          </nav>
        </div>
      )}
    </header>
  );
}

function Logo() {
  return (
    <span className="inline-flex items-center gap-1.5">
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        aria-hidden
        className="text-ink"
      >
        {/* 抽象 PHA 分子图标:大圆 + 卫星圆 */}
        <circle cx="12" cy="12" r="6" fill="currentColor" />
        <circle cx="20" cy="6" r="2.4" fill="currentColor" />
        <circle cx="5" cy="19" r="2" fill="currentColor" />
      </svg>
      <span className="text-[13px] tracking-tight font-semibold">都佰城</span>
    </span>
  );
}
