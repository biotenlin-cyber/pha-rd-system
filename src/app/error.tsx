"use client";

import Link from "next/link";
import { useEffect } from "react";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="bg-paper">
      <section className="mx-auto max-w-apple px-6 sm:px-8 py-32 sm:py-40 text-center">
        <div className="text-eyebrow text-ink mb-3">SOMETHING WENT WRONG</div>
        <h1 className="text-hero font-semibold tracking-tight text-ink">
          页面加载时遇到问题。
        </h1>
        <p className="mt-5 text-lead text-ash max-w-xl mx-auto">
          可能是临时性错误。请稍后重试,如问题持续存在请通过页面底部联系方式与我们沟通。
        </p>
        <div className="mt-7 flex flex-wrap justify-center gap-x-6 gap-y-3">
          <button
            onClick={reset}
            className="inline-flex items-center justify-center h-11 px-6 rounded-full bg-appleBlue text-white text-[15px] font-medium hover:bg-appleBlueHover transition"
          >
            重新加载
          </button>
          <Link
            href="/"
            className="inline-flex items-center justify-center h-11 px-6 rounded-full border border-hairline text-ink text-[15px] font-medium hover:bg-fog transition"
          >
            返回首页
          </Link>
        </div>
        {error.digest && (
          <p className="mt-12 text-xs text-smoke font-mono">Reference: {error.digest}</p>
        )}
      </section>
    </div>
  );
}
