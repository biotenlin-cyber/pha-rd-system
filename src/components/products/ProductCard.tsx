import type { Product } from "@/data/products";

export function ProductCard({ product }: { product: Product }) {
  return (
    <article className="group rounded-2xl bg-white border border-slate-200 p-6 hover:border-brand-200 hover:shadow-soft transition flex flex-col">
      <div className="flex items-center justify-between">
        <span className="inline-flex items-center rounded-full bg-brand-50 text-brand-900 px-2.5 py-1 text-xs font-medium">
          {product.category}
        </span>
        <span className="text-xs font-mono text-slate-500">{product.model}</span>
      </div>
      <h3 className="mt-5 text-xl font-semibold text-slate-900">{product.name}</h3>
      <p className="mt-2 text-sm leading-relaxed text-slate-600">
        {product.description}
      </p>

      <div className="mt-5">
        <div className="text-xs font-medium uppercase tracking-wider text-slate-500 mb-2">
          产品特性
        </div>
        <ul className="space-y-1.5 text-sm text-slate-700">
          {product.features.map((f) => (
            <li key={f} className="flex items-start gap-2">
              <span className="mt-2 h-1 w-1 rounded-full bg-accent-500 shrink-0" />
              <span>{f}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="mt-5 pt-5 border-t border-slate-100">
        <div className="text-xs font-medium uppercase tracking-wider text-slate-500 mb-2">
          典型应用
        </div>
        <div className="flex flex-wrap gap-2">
          {product.applications.map((a) => (
            <span
              key={a}
              className="inline-flex items-center rounded-md bg-slate-100 text-slate-700 px-2 py-1 text-xs"
            >
              {a}
            </span>
          ))}
        </div>
      </div>
    </article>
  );
}
