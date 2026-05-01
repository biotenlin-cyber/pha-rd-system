import { ArrowRight, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Container } from "@/components/ui/Container";
import { siteConfig } from "@/data/site";

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-tech-radial text-white">
      <div
        className="absolute inset-0 bg-grid opacity-20 mix-blend-overlay"
        aria-hidden
      />
      <div
        className="absolute -top-40 -left-40 w-[480px] h-[480px] rounded-full bg-accent-500/20 blur-3xl"
        aria-hidden
      />
      <div
        className="absolute -bottom-40 right-0 w-[520px] h-[520px] rounded-full bg-accent-400/20 blur-3xl"
        aria-hidden
      />

      <Container className="relative pt-36 pb-24 sm:pt-44 sm:pb-32 lg:pt-52 lg:pb-40">
        <div className="max-w-3xl">
          <div className="inline-flex items-center gap-2 rounded-full bg-white/10 border border-white/20 px-3 py-1 text-xs text-white/80 backdrop-blur">
            <Sparkles size={14} className="text-accent-400" />
            <span>专注 PHA 生物可降解材料 · 自主研发</span>
          </div>
          <h1 className="mt-6 text-4xl sm:text-5xl lg:text-6xl font-semibold leading-[1.1] tracking-tight">
            {siteConfig.tagline.split(" ").map((part, idx) => (
              <span key={idx} className={idx === 1 ? "text-accent-400" : ""}>
                {part}
                {idx === 0 ? " " : ""}
              </span>
            ))}
          </h1>
          <p className="mt-6 text-lg sm:text-xl text-white/80 leading-relaxed max-w-2xl">
            {siteConfig.description}
          </p>
          <div className="mt-10 flex flex-wrap gap-3">
            <Button href="/products" size="lg" variant="primary" className="bg-white text-brand-900 hover:bg-brand-50">
              了解产品 <ArrowRight size={18} />
            </Button>
            <Button href="/contact" size="lg" variant="ghost">
              联系我们
            </Button>
          </div>
        </div>

        <div className="mt-16 grid grid-cols-2 sm:grid-cols-4 gap-6 sm:gap-8 max-w-3xl">
          {[
            { label: "万吨级产能", value: "10,000 t" },
            { label: "授权及在审专利", value: "120+" },
            { label: "全球客户", value: "30+" },
            { label: "国际认证", value: "EN13432 / BPI" },
          ].map((item) => (
            <div key={item.label}>
              <div className="text-2xl sm:text-3xl font-semibold text-white">
                {item.value}
              </div>
              <div className="mt-1 text-xs sm:text-sm text-white/60">{item.label}</div>
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
}
