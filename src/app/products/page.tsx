import type { Metadata } from "next";
import Link from "next/link";
import { LinkArrow } from "@/components/apple/LinkArrow";
import { Reveal } from "@/components/apple/Reveal";
import { ProductVisual } from "@/components/visuals/ProductVisual";
import { products, techAdvantages, applications, type Product } from "@/data/products";

export const metadata: Metadata = {
  title: "PHA 产品 — 产品矩阵",
  description:
    "都佰城 PHA 产品矩阵涵盖薄膜级、注塑级、纤维级与改性级牌号,覆盖包装、医疗、农业、3D 打印等应用场景。",
};

const categoryAnchors: Record<Product["category"], string> = {
  薄膜级: "film",
  注塑级: "injection",
  纤维级: "fiber",
  改性级: "advanced",
};

const categoryHero: Record<Product["category"], string> = {
  薄膜级: "高韧性,高包覆。",
  注塑级: "高流动,高耐热。",
  纤维级: "亲肤,稳定,可生理降解。",
  改性级: "为严苛场景而生。",
};

export default function ProductsPage() {
  const grouped = products.reduce<Record<Product["category"], Product[]>>(
    (acc, p) => {
      acc[p.category] = acc[p.category] || [];
      acc[p.category].push(p);
      return acc;
    },
    {} as Record<Product["category"], Product[]>,
  );

  const categories: Product["category"][] = ["薄膜级", "注塑级", "纤维级", "改性级"];

  return (
    <div className="bg-fog">
      <div className="space-y-2">
        {/* HERO */}
        <section className="bg-paper text-ink">
          <div className="mx-auto max-w-6xl px-6 sm:px-8 pt-20 sm:pt-28 pb-20 text-center">
            <div className="text-eyebrow mb-3 fade-up">PHA PRODUCTS</div>
            <Reveal>
              <h1
                className="font-semibold tracking-tight leading-[1.0] max-w-5xl mx-auto"
                style={{ fontSize: "clamp(3rem, 8.5vw, 8rem)", letterSpacing: "-0.035em" }}
              >
                一种材料。
                <br />
                <span className="text-smoke">无数种可能。</span>
              </h1>
            </Reveal>
            <Reveal delay={120}>
              <p className="mt-7 text-lead text-ash max-w-2xl mx-auto">
                从薄膜到注塑,从纤维到高端改性。八款核心牌号,适配你的下一款产品。
              </p>
            </Reveal>
            <Reveal delay={200}>
              <div className="mt-7 flex flex-wrap justify-center gap-x-6 gap-y-3">
                {categories.map((c) => (
                  <LinkArrow key={c} href={`#${categoryAnchors[c]}`}>
                    {c}
                  </LinkArrow>
                ))}
              </div>
            </Reveal>
          </div>
        </section>

        {/* TECH ADVANTAGES */}
        <section className="bg-paper">
          <div className="mx-auto max-w-6xl px-6 sm:px-8 py-20 border-t border-hairline">
            <Reveal>
              <div className="text-center max-w-3xl mx-auto mb-12">
                <div className="text-eyebrow text-ink mb-3">CORE STRENGTHS</div>
                <h2 className="text-display font-semibold tracking-tight">
                  真正自主可控的全链路技术。
                </h2>
              </div>
            </Reveal>
            <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
              {techAdvantages.map((t, i) => (
                <Reveal key={t.title} delay={i * 80}>
                  <div className="rounded-tile bg-fog p-8 h-full">
                    <h3 className="text-lg font-semibold">{t.title}</h3>
                    <p className="mt-3 text-base text-ash leading-relaxed">{t.desc}</p>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* PRODUCT GROUPS */}
        {categories.map((cat, idx) => {
          const dark = idx % 2 === 1;

          return (
            <section
              key={cat}
              id={categoryAnchors[cat]}
              className={dark ? "bg-obsidian text-paper" : "bg-paper text-ink"}
            >
              <div className="mx-auto max-w-6xl px-6 sm:px-8 py-24">
                <Reveal>
                  <div className="text-center max-w-3xl mx-auto mb-16">
                    <div
                      className={`text-eyebrow mb-3 ${dark ? "text-white/80" : "text-ink"}`}
                    >
                      {cat.toUpperCase()}
                    </div>
                    <h2 className="text-display font-semibold tracking-tight">
                      {categoryHero[cat]}
                    </h2>
                  </div>
                </Reveal>

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {grouped[cat]?.map((p, i) => (
                    <Reveal key={p.id} delay={i * 70}>
                      <Link
                        href={`/products/${p.id}`}
                        id={p.id}
                        className={`group rounded-marble overflow-hidden flex flex-col h-full transition ${
                          dark ? "bg-coal hover:bg-[#1f1f21]" : "bg-fog hover:bg-haze"
                        }`}
                      >
                        <div
                          className={`p-8 flex items-center justify-center min-h-[220px] ${
                            dark ? "bg-obsidian" : "bg-paper"
                          }`}
                        >
                          <ProductVisual tone={p.tone} shape={p.shape} />
                        </div>
                        <div className="p-8 flex-1 flex flex-col">
                          <div className="flex items-center justify-between text-xs">
                            <span className={dark ? "text-white/70" : "text-ash"}>
                              {p.category}
                            </span>
                            <span
                              className={`font-mono ${dark ? "text-white/70" : "text-ash"}`}
                            >
                              {p.model}
                            </span>
                          </div>
                          <h3 className="mt-4 text-xl font-semibold tracking-tight">
                            {p.name}
                          </h3>
                          <p
                            className={`mt-2 text-sm leading-relaxed ${dark ? "text-white/75" : "text-ash"}`}
                          >
                            {p.description}
                          </p>

                          <div className="mt-6">
                            <ul className="space-y-2 text-sm">
                              {p.features.slice(0, 3).map((f) => (
                                <li key={f} className="flex items-start gap-2.5">
                                  <span
                                    className={`mt-1.5 h-1 w-1 rounded-full ${
                                      dark ? "bg-white" : "bg-ink"
                                    }`}
                                  />
                                  <span>{f}</span>
                                </li>
                              ))}
                            </ul>
                          </div>

                          <div className="mt-6 pt-5 border-t border-hairline/40 flex items-center justify-between">
                            <span
                              className={`link-arrow text-sm ${dark ? "text-white group-hover:text-white" : ""}`}
                            >
                              了解 {p.model}
                            </span>
                            <span
                              className={`text-xs ${dark ? "text-white/60" : "text-smoke"}`}
                            >
                              查看规格 ›
                            </span>
                          </div>
                        </div>
                      </Link>
                    </Reveal>
                  ))}
                </div>
              </div>
            </section>
          );
        })}

        {/* APPLICATIONS */}
        <section id="applications" className="bg-paper">
          <div className="mx-auto max-w-6xl px-6 sm:px-8 py-24">
            <Reveal>
              <div className="text-center max-w-3xl mx-auto mb-16">
                <div className="text-eyebrow text-ink mb-3">APPLICATIONS</div>
                <h2 className="text-display font-semibold tracking-tight">
                  哪里需要可持续,哪里就有 PHA。
                </h2>
              </div>
            </Reveal>
            <div className="grid gap-3 md:grid-cols-2">
              {applications.map((a, i) => (
                <Reveal key={a.title} delay={i * 80}>
                  <div className="rounded-tile bg-fog p-10 h-full">
                    <h3 className="text-section font-semibold tracking-tight">
                      {a.title}
                    </h3>
                    <p className="mt-3 text-base text-ash leading-relaxed">{a.desc}</p>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="bg-fog">
          <div className="mx-auto max-w-6xl px-6 sm:px-8 py-24 text-center">
            <Reveal>
              <h2 className="text-display font-semibold tracking-tight">
                不确定哪款牌号最合适?
              </h2>
              <p className="mt-4 text-lead text-ash max-w-2xl mx-auto">
                告诉我们您的应用与加工工艺,都佰城应用工程师会推荐最合适的 PHA 牌号与改性方案。
              </p>
              <div className="mt-7 flex flex-wrap justify-center gap-x-6 gap-y-3">
                <LinkArrow href="/contact" size="lg">
                  联系应用工程师
                </LinkArrow>
                <LinkArrow href="/platform" size="lg">
                  了解研发平台
                </LinkArrow>
              </div>
            </Reveal>
          </div>
        </section>
      </div>
    </div>
  );
}
