import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { products } from "@/data/products";
import { LinkArrow } from "@/components/apple/LinkArrow";
import { Reveal } from "@/components/apple/Reveal";
import { ProductSubNav } from "@/components/apple/ProductSubNav";
import { SpecTable } from "@/components/apple/SpecTable";
import { CloserLook } from "@/components/apple/CloserLook";
import { DataPillars } from "@/components/apple/DataPillars";
import { ProductVisual } from "@/components/visuals/ProductVisual";
import { JsonLd, productLd, breadcrumbLd } from "@/components/seo/JsonLd";

export function generateStaticParams() {
  return products.map((p) => ({ id: p.id }));
}

type Params = { id: string };

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { id } = await params;
  const p = products.find((x) => x.id === id);
  if (!p) return { title: "产品不存在" };
  return {
    title: `${p.name} ${p.model}`,
    description: p.description,
  };
}

export default async function ProductDetailPage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { id } = await params;
  const p = products.find((x) => x.id === id);
  if (!p) notFound();

  // 同类其他产品(用于底部相关推荐)
  const related = products
    .filter((x) => x.category === p.category && x.id !== p.id)
    .slice(0, 3);

  return (
    <div className="bg-paper">
      <JsonLd data={productLd(p)} />
      <JsonLd
        data={breadcrumbLd([
          { name: "首页", url: "/" },
          { name: "PHA 产品", url: "/products" },
          { name: `${p.name} ${p.model}`, url: `/products/${p.id}` },
        ])}
      />
      <ProductSubNav productName={p.name} productModel={p.model} ctaLabel="申请样品" />

      {/* HERO */}
      <section className="bg-paper">
        <div className="mx-auto max-w-apple px-6 sm:px-8 pt-12 sm:pt-20 pb-8 text-center">
          <div className="text-eyebrow text-ink mb-3 fade-up">
            <span className="text-link">新一代</span>{" "}
            {p.category} · {p.model}
          </div>
          <Reveal>
            <h1 className="text-hero font-semibold tracking-tight max-w-3xl mx-auto">
              {p.tagline}
            </h1>
          </Reveal>
          <Reveal delay={120}>
            <p className="mt-5 text-lead text-ash max-w-2xl mx-auto">
              {p.pageSubtitle}
            </p>
          </Reveal>
          <Reveal delay={200}>
            <div className="mt-7 flex flex-wrap justify-center gap-x-6 gap-y-3">
              <Link
                href="/contact"
                className="inline-flex items-center justify-center h-11 px-6 rounded-full bg-appleBlue text-white text-[15px] font-medium hover:bg-appleBlueHover transition"
              >
                申请样品
              </Link>
              <LinkArrow href="#highlights" size="md">
                了解更多
              </LinkArrow>
            </div>
          </Reveal>
        </div>

        {/* 主视觉 */}
        <div className="mx-auto max-w-apple px-6 sm:px-8 pb-20 sm:pb-28">
          <Reveal>
            <div className="aspect-[16/10] flex items-center justify-center">
              <ProductVisual tone={p.tone} shape={p.shape} className="max-w-2xl" />
            </div>
          </Reveal>
        </div>
      </section>

      {/* HIGHLIGHTS - 4 个数据柱 */}
      <section id="highlights">
        <DataPillars
          eyebrow="PRODUCT HIGHLIGHTS"
          title="关键性能,一眼读懂。"
          pillars={p.pillars}
        />
      </section>

      {/* HERO MOMENT - 黑底大字 */}
      <section className="bg-obsidian text-paper">
        <div className="mx-auto max-w-apple px-6 sm:px-8 py-32 sm:py-40 text-center">
          <Reveal>
            <h2 className="text-hero font-semibold tracking-tight max-w-3xl mx-auto">
              一颗颗粒,
              <br />
              可以走多远?
            </h2>
          </Reveal>
          <Reveal delay={140}>
            <p className="mt-6 text-lg sm:text-xl text-white/75 max-w-2xl mx-auto">
              从万吨级工厂到客户产线,从加工车间到自然环境,{p.model} 的每一克都经历完整的质量与降解验证。
            </p>
          </Reveal>
          <div className="mt-12 flex justify-center">
            <ProductVisual tone={p.tone === "pearl" ? "blue" : p.tone} shape={p.shape} className="max-w-md" />
          </div>
        </div>
      </section>

      {/* CLOSER LOOK */}
      <CloserLook
        title={
          <>
            为 {p.category} 而生,
            <br />
            把每一个细节都想透。
          </>
        }
        items={p.closerLook}
      />

      {/* APPLICATIONS */}
      <section className="bg-fog">
        <div className="mx-auto max-w-apple px-6 sm:px-8 py-24">
          <Reveal>
            <div className="text-center max-w-3xl mx-auto mb-14">
              <div className="text-eyebrow text-ink mb-3">APPLICATIONS</div>
              <h2 className="text-display font-semibold tracking-tight">
                它,正在被用在哪里。
              </h2>
            </div>
          </Reveal>
          <div className="grid gap-3 sm:grid-cols-3">
            {p.applications.map((a, i) => (
              <Reveal key={a} delay={i * 80}>
                <div className="rounded-tile bg-paper p-8 min-h-[180px] flex flex-col">
                  <div className="text-eyebrow text-ink mb-3">
                    APPLICATION {String(i + 1).padStart(2, "0")}
                  </div>
                  <div className="text-section font-semibold tracking-tight mt-auto">
                    {a}
                  </div>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* FEATURES checklist */}
      <section className="bg-paper">
        <div className="mx-auto max-w-apple px-6 sm:px-8 py-24">
          <Reveal>
            <div className="text-center max-w-3xl mx-auto mb-12">
              <div className="text-eyebrow text-ink mb-3">FEATURES</div>
              <h2 className="text-display font-semibold tracking-tight">
                每一项,都直指你的应用难点。
              </h2>
            </div>
          </Reveal>
          <ul className="grid gap-4 sm:grid-cols-2">
            {p.features.map((f, i) => (
              <Reveal key={f} delay={i * 60}>
                <li className="flex items-start gap-3 rounded-tile bg-fog px-6 py-5">
                  <span className="mt-1.5 h-1.5 w-1.5 rounded-full bg-link shrink-0" />
                  <span className="text-base text-ink">{f}</span>
                </li>
              </Reveal>
            ))}
          </ul>
        </div>
      </section>

      {/* SPECS */}
      <section id="specs" className="bg-paper">
        <div className="mx-auto max-w-3xl px-6 sm:px-8 py-24 border-t border-hairline">
          <Reveal>
            <div className="text-eyebrow text-ink mb-3">TECHNICAL SPECIFICATIONS</div>
            <h2 className="text-display font-semibold tracking-tight mb-12">
              {p.model} · 完整规格。
            </h2>
          </Reveal>
          <SpecTable groups={p.specs} />
          <p className="mt-12 text-xs text-smoke">
            * 规格参数为典型值,实际批次以随附检测报告为准。完整 TDS / SDS 可通过{" "}
            <Link href="/contact" className="text-link">
              联系我们
            </Link>{" "}
            索取。
          </p>
        </div>
      </section>

      {/* RELATED */}
      {related.length > 0 && (
        <section className="bg-fog">
          <div className="mx-auto max-w-apple px-6 sm:px-8 py-20">
            <div className="flex items-end justify-between mb-8">
              <h2 className="text-section font-semibold tracking-tight">
                同类型其他 PHA 牌号。
              </h2>
              <LinkArrow href="/products">查看全部</LinkArrow>
            </div>
            <div className="grid gap-3 sm:grid-cols-3">
              {related.map((r) => (
                <Link
                  key={r.id}
                  href={`/products/${r.id}`}
                  className="group rounded-tile bg-paper p-8 hover:bg-haze transition flex flex-col"
                >
                  <div className="aspect-[4/3] flex items-center justify-center">
                    <ProductVisual tone={r.tone} shape={r.shape} />
                  </div>
                  <div className="mt-4 text-eyebrow text-smoke">{r.category}</div>
                  <h3 className="mt-1 text-lg font-semibold tracking-tight">
                    {r.name}
                  </h3>
                  <span className="mt-3 link-arrow text-sm">了解 {r.model}</span>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA */}
      <section className="bg-paper">
        <div className="mx-auto max-w-apple px-6 sm:px-8 py-24 text-center border-t border-hairline">
          <Reveal>
            <h2 className="text-display font-semibold tracking-tight">
              想把 {p.model} 用在您的产品上?
            </h2>
            <p className="mt-4 text-lead text-ash max-w-2xl mx-auto">
              告诉我们应用场景与加工工艺,都佰城应用工程师将为您提供牌号选型与样品支持。
            </p>
            <div className="mt-7 flex flex-wrap justify-center gap-x-6 gap-y-3">
              <Link
                href="/contact"
                className="inline-flex items-center justify-center h-11 px-6 rounded-full bg-appleBlue text-white text-[15px] font-medium hover:bg-appleBlueHover transition"
              >
                申请样品
              </Link>
              <LinkArrow href="/platform" size="md">
                了解 PHA-RD 平台
              </LinkArrow>
            </div>
          </Reveal>
        </div>
      </section>
    </div>
  );
}
