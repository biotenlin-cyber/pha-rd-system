import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { news } from "@/data/news";
import { formatDate } from "@/lib/utils";
import { LinkArrow } from "@/components/apple/LinkArrow";
import { JsonLd, articleLd, breadcrumbLd } from "@/components/seo/JsonLd";

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
    <article className="bg-paper">
      <JsonLd data={articleLd(item)} />
      <JsonLd
        data={breadcrumbLd([
          { name: "首页", url: "/" },
          { name: "Newsroom", url: "/news" },
          { name: item.title, url: `/news/${item.slug}` },
        ])}
      />
      {/* Crumbs */}
      <div className="border-b border-hairline">
        <div className="mx-auto max-w-3xl px-6 sm:px-8 py-4 text-sm">
          <Link href="/news" className="text-link hover:text-linkHover">
            ‹ Newsroom
          </Link>
        </div>
      </div>

      {/* Headline */}
      <header className="border-b border-hairline">
        <div className="mx-auto max-w-3xl px-6 sm:px-8 py-16 sm:py-20">
          <div className="text-eyebrow text-link">{item.category}</div>
          <h1 className="mt-4 text-display font-semibold tracking-tight">
            {item.title}
          </h1>
          <div className="mt-6 flex items-center gap-3 text-sm text-smoke">
            <time>{formatDate(item.date)}</time>
            <span>·</span>
            <span>都佰城新闻中心</span>
          </div>
        </div>
      </header>

      {/* Body */}
      <div className="mx-auto max-w-prose2 px-6 sm:px-8 py-16">
        <p className="text-xl leading-[1.6] text-ink/90 font-medium">
          {item.excerpt}
        </p>
        <div className="mt-8 space-y-6 text-lg leading-[1.7] text-ink/85">
          {item.body.map((p, i) => (
            <p key={i}>{p}</p>
          ))}
        </div>

        <hr className="my-16 border-hairline" />

        <div className="text-sm text-smoke">
          <p>
            如需了解更多关于本篇内容的细节,或寻求合作,请通过{" "}
            <Link href="/contact" className="text-link">
              联系我们
            </Link>{" "}
            页面与都佰城团队取得联系。
          </p>
        </div>
      </div>

      {/* Prev / Next */}
      <nav className="bg-fog">
        <div className="mx-auto max-w-apple px-6 sm:px-8 py-16 grid gap-3 md:grid-cols-2">
          {prev ? (
            <Link
              href={`/news/${prev.slug}`}
              className="group rounded-tile bg-paper p-8 hover:bg-haze transition"
            >
              <div className="text-eyebrow text-smoke">‹ 上一篇</div>
              <div className="mt-3 text-lg font-semibold tracking-tight group-hover:text-link line-clamp-2">
                {prev.title}
              </div>
            </Link>
          ) : (
            <div />
          )}
          {next ? (
            <Link
              href={`/news/${next.slug}`}
              className="group rounded-tile bg-paper p-8 hover:bg-haze transition md:text-right"
            >
              <div className="text-eyebrow text-smoke">下一篇 ›</div>
              <div className="mt-3 text-lg font-semibold tracking-tight group-hover:text-link line-clamp-2">
                {next.title}
              </div>
            </Link>
          ) : (
            <div />
          )}
        </div>
      </nav>

      {/* CTA */}
      <section className="bg-paper">
        <div className="mx-auto max-w-apple px-6 sm:px-8 py-20 text-center border-t border-hairline">
          <h2 className="text-display font-semibold tracking-tight">
            想第一时间获得都佰城动态?
          </h2>
          <div className="mt-6 flex justify-center gap-x-6 gap-y-3 flex-wrap">
            <LinkArrow href="/news" size="lg">
              返回 Newsroom
            </LinkArrow>
            <LinkArrow href="/contact" size="lg">
              订阅与媒体联络
            </LinkArrow>
          </div>
        </div>
      </section>
    </article>
  );
}
