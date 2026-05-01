import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Container } from "@/components/ui/Container";

export function CTASection() {
  return (
    <section className="py-16 sm:py-20">
      <Container>
        <div className="relative overflow-hidden rounded-3xl bg-tech-radial text-white px-8 py-14 sm:px-14 sm:py-20">
          <div
            className="absolute inset-0 bg-grid opacity-20 mix-blend-overlay"
            aria-hidden
          />
          <div className="relative max-w-2xl">
            <h2 className="text-3xl sm:text-4xl font-semibold leading-tight">
              想为您的产品引入 PHA 材料?
            </h2>
            <p className="mt-4 text-base sm:text-lg text-white/80">
              我们的应用工程师将与您一起,从牌号选型、加工工艺到认证合规,提供全流程支持。
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Button
                href="/contact"
                size="lg"
                variant="primary"
                className="bg-white text-brand-900 hover:bg-brand-50"
              >
                联系我们 <ArrowRight size={18} />
              </Button>
              <Button href="/products" size="lg" variant="ghost">
                浏览产品
              </Button>
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}
