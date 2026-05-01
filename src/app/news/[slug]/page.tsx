import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { news } from "@/data/news";
import { formatDate } from "@/lib/utils";

export function generateStaticParams() {
  return news.map((n) => ({ slug: n.slug }));
}

type Params = { slug: string };

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { slug } = await params;
  const item = news.find((n) => n.slug === slug);
  if (!item) return { title: "新闻不存在" };
  return {
    title: item.title,
    description: item.excerpt,
  };
}

export default async function NewsDetailPage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { slug } = await params;
  const item = news.find((n) => n.slug === slug);
  if (!item) notFound();

  const sorted = [...news].sort((a, b) => (a.date < b.date ? 1 : -1));
  const idx = sorted.findIndex((n) => n.slug === slug);
  const prev = idx > 0 ? sorted[idx - 1] : null;
  const next = idx < sorted.length - 1 ? sorted[idx + 1] : null;

  return (
    <>
      <section className="relative overflow-hidden bg-tech-radial text-white">
        <div
          className="absolute inset-0 bg-grid opacity-20 mix-blend-overlay"
          aria-hidden
        />
        <Container className="relative pt-32 pb-16 sm:pt-40 sm:pb-20" size="narrow">
          <Link
            href="/news"
            className="inline-flex items-center gap-1 text-sm text-white/80 hover:text-white transition"
          >
            <ArrowLeft size={16} /> 返回新闻列表
          </Link>
          <div className="mt-8 inline-flex items-center rounded-full bg-white/10 border border-white/20 px-3 py-1 text-xs text-white/80 backdrop-blur">
            {item.category}
          </div>
          <h1 className="mt-4 text-3xl sm:text-4xl font-semibold leading-tight">
            {item.title}
          </h1>
          <time className="mt-4 inline-block text-sm text-white/70">
            {formatDate(item.date)}
          </time>
        </Container>
      </section>

      <article className="py-16 sm:py-20">
        <Container size="narrow">
          <div className="prose prose-slate max-w-none">
            <p className="text-lg leading-relaxed text-slate-700 border-l-4 border-accent-500 pl-5 bg-tech-soft py-4 rounded-r-lg">
              {item.excerpt}
            </p>
            <div className="mt-8 space-y-5 text-base leading-relaxed text-slate-700">
              {item.body.map((p, i) => (
                <p key={i}>{p}</p>
              ))}
            </div>
          </div>

          <div className="mt-16 pt-8 border-t border-slate-200 grid gap-4 sm:grid-cols-2">
            {prev ? (
              <Link
                href={`/news/${prev.slug}`}
                className="group rounded-xl border border-slate-200 p-5 hover:border-brand-200 hover:shadow-soft transition"
              >
                <div className="text-xs text-slate-500 inline-flex items-center gap-1">
                  <ArrowLeft size={12} /> 上一篇
                </div>
                <div className="mt-2 text-sm font-medium text-slate-900 group-hover:text-brand-900 line-clamp-2">
                  {prev.title}
                </div>
              </Link>
            ) : (
              <div />
            )}
            {next ? (
              <Link
                href={`/news/${next.slug}`}
                className="group rounded-xl border border-slate-200 p-5 hover:border-brand-200 hover:shadow-soft transition sm:text-right"
              >
                <div className="text-xs text-slate-500 inline-flex items-center gap-1 sm:justify-end sm:w-full">
                  下一篇 <ArrowRight size={12} />
                </div>
                <div className="mt-2 text-sm font-medium text-slate-900 group-hover:text-brand-900 line-clamp-2">
                  {next.title}
                </div>
              </Link>
            ) : (
              <div />
            )}
          </div>
        </Container>
      </article>
    </>
  );
}
