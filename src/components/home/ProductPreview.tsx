import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Section } from "@/components/ui/Section";
import { products } from "@/data/products";

export function ProductPreview() {
  const featured = products.slice(0, 3);

  return (
    <Section
      eyebrow="PRODUCTS"
      title="覆盖薄膜、注塑、纤维、改性的产品矩阵"
      subtitle="从通用牌号到定制改性,都佰城为各行业客户提供系统化的 PHA 材料解决方案。"
      className="bg-tech-soft"
    >
      <div className="grid gap-6 md:grid-cols-3">
        {featured.map((p) => (
          <article
            key={p.id}
            className="group rounded-2xl bg-white border border-slate-200 p-6 hover:border-brand-200 hover:shadow-soft transition"
          >
            <div className="flex items-center justify-between">
              <span className="inline-flex items-center rounded-full bg-brand-50 text-brand-900 px-2.5 py-1 text-xs font-medium">
                {p.category}
              </span>
              <span className="text-xs text-slate-500">{p.model}</span>
            </div>
            <h3 className="mt-5 text-xl font-semibold text-slate-900">{p.name}</h3>
            <p className="mt-2 text-sm leading-relaxed text-slate-600 line-clamp-3">
              {p.description}
            </p>
            <ul className="mt-4 space-y-1.5 text-xs text-slate-500">
              {p.features.slice(0, 3).map((f) => (
                <li key={f} className="flex items-start gap-2">
                  <span className="mt-1.5 h-1 w-1 rounded-full bg-accent-500" />
                  <span>{f}</span>
                </li>
              ))}
            </ul>
          </article>
        ))}
      </div>

      <div className="mt-10 text-center">
        <Link
          href="/products"
          className="inline-flex items-center gap-2 text-sm font-medium text-brand-900 hover:text-brand-700"
        >
          查看全部产品 <ArrowRight size={16} />
        </Link>
      </div>
    </Section>
  );
}
