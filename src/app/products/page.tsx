import type { Metadata } from "next";
import { Package, HeartPulse, Sprout, Boxes } from "lucide-react";
import { PageHero } from "@/components/PageHero";
import { Section } from "@/components/ui/Section";
import { Container } from "@/components/ui/Container";
import { ProductCard } from "@/components/products/ProductCard";
import { products, techAdvantages, applications } from "@/data/products";

export const metadata: Metadata = {
  title: "产品与技术",
  description:
    "都佰城 PHA 产品矩阵涵盖薄膜级、注塑级、纤维级与改性级牌号,覆盖包装、医疗、农业、3D 打印等应用场景。",
};

const iconMap = {
  Package,
  HeartPulse,
  Sprout,
  Boxes,
} as const;

export default function ProductsPage() {
  return (
    <>
      <PageHero
        eyebrow="PRODUCTS & TECHNOLOGY"
        title="产品与技术"
        subtitle="围绕 PHA 这一核心生物可降解材料,我们提供从通用牌号到定制改性的系统化产品组合,服务全球客户的可持续转型。"
      />

      <Section
        eyebrow="WHAT IS PHA"
        title="什么是 PHA?"
        subtitle="聚羟基脂肪酸酯(Polyhydroxyalkanoates)是由微生物发酵合成的天然高分子聚酯,可在土壤、海水、堆肥等多种自然环境中实现完全生物降解,被认为是少数真正意义上的「源于自然、归于自然」的可持续材料。"
      >
        <div className="grid gap-6 md:grid-cols-3">
          {[
            {
              title: "全场景可降解",
              desc: "在土壤、淡水、海水、工业堆肥等多种环境中可被微生物完全降解为水与二氧化碳。",
            },
            {
              title: "生物基来源",
              desc: "由微生物利用糖类、油脂等可再生原料发酵合成,显著降低化石资源消耗。",
            },
            {
              title: "性能多样",
              desc: "通过菌种与工艺调控,可获得从柔韧到刚性、从低熔点到高耐热等多样化性能。",
            },
          ].map((item) => (
            <div
              key={item.title}
              className="rounded-2xl bg-white border border-slate-200 p-6"
            >
              <h3 className="text-lg font-semibold text-slate-900">{item.title}</h3>
              <p className="mt-3 text-sm leading-relaxed text-slate-600">
                {item.desc}
              </p>
            </div>
          ))}
        </div>
      </Section>

      <Section
        eyebrow="PRODUCT MATRIX"
        title="产品矩阵"
        subtitle="从通用薄膜、注塑到高端医用与改性牌号,选择最适合您应用的 PHA 解决方案。"
        className="bg-tech-soft"
      >
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {products.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      </Section>

      <Section eyebrow="TECH ADVANTAGES" title="核心技术优势">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {techAdvantages.map((t) => (
            <div
              key={t.title}
              className="rounded-2xl bg-white border border-slate-200 p-6 hover:shadow-soft transition"
            >
              <h3 className="text-lg font-semibold text-slate-900">{t.title}</h3>
              <p className="mt-3 text-sm leading-relaxed text-slate-600">{t.desc}</p>
            </div>
          ))}
        </div>
      </Section>

      <section className="py-16 sm:py-20 bg-tech-soft">
        <Container>
          <div className="text-center max-w-2xl mx-auto mb-12">
            <div className="text-sm font-medium uppercase tracking-[0.2em] text-accent-500 mb-3">
              APPLICATIONS
            </div>
            <h2 className="text-3xl sm:text-4xl font-semibold text-slate-900">
              应用场景
            </h2>
            <p className="mt-4 text-slate-600">
              PHA 已在多个行业实现规模化应用,持续为客户创造绿色价值。
            </p>
          </div>
          <div className="grid gap-6 md:grid-cols-2">
            {applications.map((a) => {
              const Icon = iconMap[a.icon as keyof typeof iconMap];
              return (
                <div
                  key={a.title}
                  className="flex gap-5 rounded-2xl bg-white border border-slate-200 p-6 hover:shadow-soft transition"
                >
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-brand-50 text-brand-900">
                    {Icon ? <Icon size={22} /> : null}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-slate-900">
                      {a.title}
                    </h3>
                    <p className="mt-2 text-sm leading-relaxed text-slate-600">
                      {a.desc}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </Container>
      </section>
    </>
  );
}
