"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type Props = {
  productName: string;
  productModel: string;
  ctaHref?: string;
  ctaLabel?: string;
};

export function ProductSubNav({
  productName,
  productModel,
  ctaHref = "/contact",
  ctaLabel = "咨询",
}: Props) {
  const [shown, setShown] = useState(false);

  useEffect(() => {
    const onScroll = () => setShown(window.scrollY > 320);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <div
      aria-hidden={!shown}
      className={`fixed top-[80px] inset-x-0 z-40 h-12 bg-paper/85 apple-blur border-b border-hairline transition-all duration-300 ${
        shown ? "opacity-100 translate-y-0" : "opacity-0 -translate-y-2 pointer-events-none"
      }`}
    >
      <div className="mx-auto max-w-[1024px] h-full px-4 sm:px-6 flex items-center justify-between">
        <div className="flex items-baseline gap-3 min-w-0">
          <span className="text-[15px] font-semibold tracking-tight text-ink truncate">
            {productName}
          </span>
          <span className="text-[12px] font-mono text-smoke shrink-0 hidden sm:inline">
            {productModel}
          </span>
        </div>
        <div className="flex items-center gap-4 text-[13px] shrink-0">
          <Link href="#highlights" className="text-ink/85 hover:text-ink hidden sm:inline">
            产品亮点
          </Link>
          <Link href="#specs" className="text-ink/85 hover:text-ink hidden md:inline">
            规格
          </Link>
          <Link
            href={ctaHref}
            className="inline-flex items-center justify-center h-8 px-4 rounded-full bg-appleBlue text-white text-[13px] font-medium hover:bg-appleBlueHover transition"
          >
            {ctaLabel}
          </Link>
        </div>
      </div>
    </div>
  );
}
