import { Container } from "@/components/ui/Container";

type Props = {
  eyebrow?: string;
  title: string;
  subtitle?: string;
};

export function PageHero({ eyebrow, title, subtitle }: Props) {
  return (
    <section className="relative overflow-hidden bg-tech-radial text-white">
      <div
        className="absolute inset-0 bg-grid opacity-20 mix-blend-overlay"
        aria-hidden
      />
      <Container className="relative pt-32 pb-16 sm:pt-40 sm:pb-20">
        <div className="max-w-3xl">
          {eyebrow && (
            <div className="text-sm font-medium uppercase tracking-[0.2em] text-accent-400">
              {eyebrow}
            </div>
          )}
          <h1 className="mt-3 text-4xl sm:text-5xl font-semibold leading-tight tracking-tight">
            {title}
          </h1>
          {subtitle && (
            <p className="mt-5 text-base sm:text-lg text-white/80 leading-relaxed max-w-2xl">
              {subtitle}
            </p>
          )}
        </div>
      </Container>
    </section>
  );
}
