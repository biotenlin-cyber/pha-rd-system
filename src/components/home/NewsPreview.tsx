import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Section } from "@/components/ui/Section";
import { news } from "@/data/news";
import { formatDate } from "@/lib/utils";

export function NewsPreview() {
  const latest = [...news]
    .sort((a, b) => (a.date < b.date ? 1 : -1))
    .slice(0, 3);

  return (
    <Section
      eyebrow="NEWS"
      title="最新动态"
      subtitle="持续关注 PHA 材料行业的进展,记录都佰城与客户、伙伴共同成长的脚步。"
      className="bg-tech-soft"
    >
      <div className="grid gap-6 md:grid-cols-3">
        {latest.map((n) => (
          <Link
            key={n.slug}
            href={`/news/${n.slug}`}
            className="group rounded-2xl bg-white border border-slate-200 overflow-hidden hover:border-brand-200 hover:shadow-soft transition flex flex-col"
          >
            <div
              className="h-40 bg-tech-radial relative overflow-hidden"
              aria-hidden
            >
              <div className="absolute inset-0 bg-grid opacity-20 mix-blend-overlay" />
              <div className="absolute top-4 left-4 inline-flex items-center rounded-full bg-white/10 backdrop-blur border border-white/20 px-2.5 py-1 text-xs text-white">
                {n.category}
              </div>
            </div>
            <div className="p-6 flex-1 flex flex-col">
              <time className="text-xs text-slate-500">{formatDate(n.date)}</time>
              <h3 className="mt-2 text-lg font-semibold text-slate-900 leading-snug group-hover:text-brand-900 transition">
                {n.title}
              </h3>
              <p className="mt-3 text-sm leading-relaxed text-slate-600 line-clamp-2">
                {n.excerpt}
              </p>
              <span className="mt-5 inline-flex items-center gap-1 text-sm font-medium text-brand-900">
                阅读全文 <ArrowRight size={14} />
              </span>
            </div>
          </Link>
        ))}
      </div>

      <div className="mt-10 text-center">
        <Link
          href="/news"
          className="inline-flex items-center gap-2 text-sm font-medium text-brand-900 hover:text-brand-700"
        >
          查看全部资讯 <ArrowRight size={16} />
        </Link>
      </div>
    </Section>
  );
}
