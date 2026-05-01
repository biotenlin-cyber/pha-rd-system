import type { Metadata } from "next";
import { LinkArrow } from "@/components/apple/LinkArrow";
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

const tonesByCategory: Record<Product["category"], "blue" | "graphite" | "pearl" | "midnight"> = {
  薄膜级: "pearl",
  注塑级: "blue",
  纤维级: "graphite",
  改性级: "midnight",
};

const shapesByCategory: Record<Product["category"], "pellet" | "film" | "fiber"> = {
  薄膜级: "film",
  注塑级: "pellet",
  纤维级: "fiber",
  改性级: "pellet",
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
        {/* Hero */}
        <section className="bg-paper text-ink">
          <div className="mx-auto max-w-6xl px-6 sm:px-8 pt-20 sm:pt-28 pb-20 text-center">
            <div className="text-eyebrow mb-3 fade-up">PHA PRODUCTS</div>
            <h1 className="text-display sm:text-hero font-semibold tracking-tight max-w-4xl mx-auto fade-up">
              一种材料。
              <br />
              <span className="text-smoke">无数种可能。</span>
            </h1>
            <p className="mt-5 text-lead text-ash max-w-2xl mx-auto fade-up-soft">
              从薄膜到注塑,从纤维到高端改性。八款核心牌号,适配你的下一款产品。
            </p>
            <div className="mt-7 flex flex-wrap justify-center gap-x-6 gap-y-3">
              {categories.map((c) => (
                <LinkArrow key={c} href={`#${categoryAnchors[c]}`}>
                  {c}
                </LinkArrow>
              ))}
            </div>
          </div>
        </section>

        {/* Tech advantages */}
        <section className="bg-paper">
          <div className="mx-auto max-w-6xl px-6 sm:px-8 py-20 border-t border-hairline">
            <div className="text-center max-w-3xl mx-auto mb-12">
              <div className="text-eyebrow text-ink mb-3">CORE STRENGTHS</div>
              <h2 className="text-display font-semibold tracking-tight">
                真正自主可控的全链路技术。
              </h2>
            </div>
            <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
              {techAdvantages.map((t) => (
                <div key={t.title} className="rounded-tile bg-fog p-8">
                  <h3 className="text-lg font-semibold">{t.title}</h3>
                  <p className="mt-3 text-base text-ash leading-relaxed">{t.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Product groups */}
        {categories.map((cat, idx) => {
          const tone = tonesByCategory[cat];
          const shape = shapesByCategory[cat];
          const dark = idx % 2 === 1;

          return (
            <section
              key={cat}
              id={categoryAnchors[cat]}
              className={dark ? "bg-obsidian text-paper" : "bg-paper text-ink"}
            >
              <div className="mx-auto max-w-6xl px-6 sm:px-8 py-24">
                <div className="text-center max-w-3xl mx-auto mb-16">
                  <div
                    className={`text-eyebrow mb-3 ${dark ? "text-white/80" : "text-ink"}`}
                  >
                    {cat.toUpperCase()}
                  </div>
                  <h2 className="text-display font-semibold tracking-tight">
                    {cat === "薄膜级" && "高韧性,高包覆。"}
                    {cat === "注塑级" && "高流动,高耐热。"}
                    {cat === "纤维级" && "亲肤,稳定,可生理降解。"}
                    {cat === "改性级" && "为严苛场景而生。"}
                  </h2>
                </div>

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {grouped[cat]?.map((p) => (
                    <article
                      key={p.id}
                      id={p.id}
                      className={`rounded-marble overflow-hidden flex flex-col ${
                        dark ? "bg-coal" : "bg-fog"
                      }`}
                    >
                      <div
                        className={`p-8 flex items-center justify-center min-h-[220px] ${
                          dark ? "bg-obsidian" : "bg-paper"
                        }`}
                      >
                        <ProductVisual tone={tone} shape={shape} />
                      </div>
                      <div className="p-8 flex-1 flex flex-col">
                        <div className="flex items-center justify-between text-xs">
                          <span
                            className={dark ? "text-white/70" : "text-ash"}
                          >
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
                            {p.features.map((f) => (
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

                        <div className="mt-6 pt-5 border-t border-hairline/40">
                          <div
                            className={`text-eyebrow mb-2 ${dark ? "text-white/80" : "text-ink"}`}
                          >
                            APPLICATIONS
                          </div>
                          <div className="flex flex-wrap gap-1.5">
                            {p.applications.map((a) => (
                              <span
                                key={a}
                                className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs ${
                                  dark
                                    ? "bg-white/10 text-white/85"
                                    : "bg-paper text-ink border border-hairline"
                                }`}
                              >
                                {a}
                              </span>
                            ))}
                          </div>
                        </div>

                        <div className="mt-6">
                          <LinkArrow
                            href="/contact"
                            className={dark ? "text-white hover:text-white/85" : ""}
                          >
                            申请样品 / 索取规格书
                          </LinkArrow>
                        </div>
                      </div>
                    </article>
                  ))}
                </div>
              </div>
            </section>
          );
        })}

        {/* Applications */}
        <section className="bg-paper">
          <div className="mx-auto max-w-6xl px-6 sm:px-8 py-24">
            <div className="text-center max-w-3xl mx-auto mb-16">
              <div className="text-eyebrow text-ink mb-3">APPLICATIONS</div>
              <h2 className="text-display font-semibold tracking-tight">
                哪里需要可持续,哪里就有 PHA。
              </h2>
            </div>
            <div className="grid gap-3 md:grid-cols-2">
              {applications.map((a) => (
                <div key={a.title} className="rounded-tile bg-fog p-10">
                  <h3 className="text-section font-semibold tracking-tight">
                    {a.title}
                  </h3>
                  <p className="mt-3 text-base text-ash leading-relaxed">{a.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="bg-fog">
          <div className="mx-auto max-w-6xl px-6 sm:px-8 py-24 text-center">
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
          </div>
        </section>
      </div>
    </div>
  );
}
