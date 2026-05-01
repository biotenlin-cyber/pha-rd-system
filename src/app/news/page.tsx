import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { PageHero } from "@/components/PageHero";
import { Container } from "@/components/ui/Container";
import { news } from "@/data/news";
import { formatDate } from "@/lib/utils";

export const metadata: Metadata = {
  title: "新闻资讯",
  description: "都佰城公司动态、产品发布、行业洞察与媒体报道。",
};

export default function NewsPage() {
  const sorted = [...news].sort((a, b) => (a.date < b.date ? 1 : -1));

  return (
    <>
      <PageHero
        eyebrow="NEWS & INSIGHTS"
        title="新闻资讯"
        subtitle="持续关注 PHA 产业的进展与都佰城的发展脚步,分享我们的最新动态、行业洞察与媒体声音。"
      />

      <section className="py-16 sm:py-20">
        <Container>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {sorted.map((n) => (
              <Link
                key={n.slug}
                href={`/news/${n.slug}`}
                className="group rounded-2xl bg-white border border-slate-200 overflow-hidden hover:border-brand-200 hover:shadow-soft transition flex flex-col"
              >
                <div
                  className="h-44 bg-tech-radial relative overflow-hidden"
                  aria-hidden
                >
                  <div className="absolute inset-0 bg-grid opacity-20 mix-blend-overlay" />
                  <div className="absolute top-4 left-4 inline-flex items-center rounded-full bg-white/10 backdrop-blur border border-white/20 px-2.5 py-1 text-xs text-white">
                    {n.category}
                  </div>
                </div>
                <div className="p-6 flex-1 flex flex-col">
                  <time className="text-xs text-slate-500">
                    {formatDate(n.date)}
                  </time>
                  <h3 className="mt-2 text-lg font-semibold text-slate-900 leading-snug group-hover:text-brand-900 transition">
                    {n.title}
                  </h3>
                  <p className="mt-3 text-sm leading-relaxed text-slate-600 line-clamp-3">
                    {n.excerpt}
                  </p>
                  <span className="mt-5 inline-flex items-center gap-1 text-sm font-medium text-brand-900">
                    阅读全文 <ArrowRight size={14} />
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </Container>
      </section>
    </>
  );
}
