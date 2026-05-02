import type { Metadata } from "next";
import Link from "next/link";
import { news } from "@/data/news";
import { formatDate } from "@/lib/utils";

export const metadata: Metadata = {
  title: "Newsroom — 新闻资讯",
  description: "都佰城公司动态、产品发布、行业洞察与媒体报道。",
};

const categoryTones: Record<string, string> = {
  公司动态: "from-[#3a86ff] to-[#0a4cb8]",
  产品发布: "from-[#86868b] to-[#1d1d1f]",
  行业洞察: "from-[#7eb6ff] to-[#3a86ff]",
  媒体报道: "from-[#d2d2d7] to-[#86868b]",
};

export default function NewsPage() {
  const sorted = [...news].sort((a, b) => (a.date < b.date ? 1 : -1));
  const [feature, ...rest] = sorted;

  return (
    <div className="bg-paper">
      {/* Hero - Newsroom 标题区 */}
      <section className="border-b border-hairline">
        <div className="mx-auto max-w-apple px-6 sm:px-8 pt-20 sm:pt-28 pb-12 text-center">
          <div className="text-eyebrow text-ink mb-3 fade-up">NEWSROOM</div>
          <h1 className="text-display sm:text-hero font-semibold tracking-tight fade-up">
            来自都佰城的最新消息。
          </h1>
        </div>
      </section>

      {/* Featured */}
      {feature && (
        <section className="border-b border-hairline">
          <div className="mx-auto max-w-apple px-6 sm:px-8 py-16">
            <Link
              href={`/news/${feature.slug}`}
              className="group block rounded-marble overflow-hidden bg-fog hover:bg-haze transition"
            >
              <div className="grid md:grid-cols-2">
                <div
                  className={`min-h-[280px] sm:min-h-[420px] relative bg-gradient-to-br ${
                    categoryTones[feature.category] ?? "from-fog to-hairline"
                  }`}
                >
                  <div className="absolute top-6 left-6 inline-flex items-center rounded-full bg-white/15 backdrop-blur border border-white/20 px-3 py-1 text-xs text-white">
                    {feature.category}
                  </div>
                </div>
                <div className="p-10 sm:p-14 flex flex-col justify-center">
                  <time className="text-sm text-smoke">{formatDate(feature.date)}</time>
                  <h2 className="mt-3 text-section font-semibold tracking-tight group-hover:text-link transition">
                    {feature.title}
                  </h2>
                  <p className="mt-4 text-base sm:text-lg text-ash leading-relaxed">
                    {feature.excerpt}
                  </p>
                  <span className="mt-6 link-arrow text-base">阅读全文</span>
                </div>
              </div>
            </Link>
          </div>
        </section>
      )}

      {/* List */}
      <section>
        <div className="mx-auto max-w-apple px-6 sm:px-8 py-16">
          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
            {rest.map((n) => (
              <Link
                key={n.slug}
                href={`/news/${n.slug}`}
                className="group rounded-tile overflow-hidden bg-fog hover:bg-haze transition flex flex-col"
              >
                <div
                  className={`h-44 relative bg-gradient-to-br ${
                    categoryTones[n.category] ?? "from-fog to-hairline"
                  }`}
                >
                  <div className="absolute top-4 left-4 inline-flex items-center rounded-full bg-white/15 backdrop-blur border border-white/20 px-2.5 py-1 text-[11px] text-white">
                    {n.category}
                  </div>
                </div>
                <div className="p-7 flex-1 flex flex-col">
                  <time className="text-xs text-smoke">{formatDate(n.date)}</time>
                  <h3 className="mt-2 text-lg font-semibold leading-snug group-hover:text-link transition">
                    {n.title}
                  </h3>
                  <p className="mt-3 text-sm text-ash leading-relaxed line-clamp-3">
                    {n.excerpt}
                  </p>
                  <span className="mt-5 link-arrow text-sm">阅读全文</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
