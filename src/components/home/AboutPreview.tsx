import { ArrowRight, Leaf } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { companyIntro } from "@/data/company";

export function AboutPreview() {
  return (
    <section className="py-16 sm:py-20 lg:py-24">
      <Container>
        <div className="grid gap-12 lg:grid-cols-12 items-center">
          <div className="lg:col-span-6">
            <div className="text-sm font-medium uppercase tracking-[0.2em] text-accent-500 mb-3">
              ABOUT US
            </div>
            <h2 className="text-3xl sm:text-4xl font-semibold text-slate-900 leading-tight">
              用合成生物学 <br className="hidden sm:block" />
              重新定义可持续材料
            </h2>
            <p className="mt-6 text-base sm:text-lg text-slate-600 leading-relaxed">
              {companyIntro.short}
            </p>
            <a
              href="/about"
              className="mt-8 inline-flex items-center gap-2 text-sm font-medium text-brand-900 hover:text-brand-700"
            >
              了解都佰城 <ArrowRight size={16} />
            </a>
          </div>

          <div className="lg:col-span-6">
            <div className="relative rounded-3xl bg-tech-radial p-8 sm:p-10 text-white overflow-hidden">
              <div
                className="absolute inset-0 bg-grid opacity-20 mix-blend-overlay"
                aria-hidden
              />
              <div className="relative">
                <div className="inline-flex items-center justify-center h-12 w-12 rounded-2xl bg-white/10 border border-white/20">
                  <Leaf size={22} className="text-accent-400" />
                </div>
                <div className="mt-8 grid grid-cols-2 gap-6">
                  {companyIntro.stats.map((s) => (
                    <div key={s.label}>
                      <div className="text-3xl sm:text-4xl font-semibold">
                        {s.value}
                      </div>
                      <div className="mt-2 text-xs sm:text-sm text-white/70">
                        {s.label}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}
