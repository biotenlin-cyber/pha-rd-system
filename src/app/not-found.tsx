import Link from "next/link";
import { LinkArrow } from "@/components/apple/LinkArrow";

export default function NotFound() {
  return (
    <div className="bg-paper">
      <section className="mx-auto max-w-apple px-6 sm:px-8 py-32 sm:py-40 text-center">
        <div className="text-eyebrow text-ink mb-3">ERROR · 404</div>
        <h1 className="text-hero font-semibold tracking-tight text-ink">
          这个页面,不在这里。
        </h1>
        <p className="mt-5 text-lead text-ash max-w-xl mx-auto">
          您访问的链接可能已被移动或不再可用。回到首页继续浏览,或前往产品矩阵。
        </p>
        <div className="mt-7 flex flex-wrap justify-center gap-x-6 gap-y-3">
          <Link
            href="/"
            className="inline-flex items-center justify-center h-11 px-6 rounded-full bg-appleBlue text-white text-[15px] font-medium hover:bg-appleBlueHover transition"
          >
            返回首页
          </Link>
          <LinkArrow href="/products" size="md">
            浏览 PHA 产品
          </LinkArrow>
        </div>
      </section>
    </div>
  );
}
