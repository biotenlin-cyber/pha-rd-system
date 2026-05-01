import type { Metadata } from "next";
import { Compass, Target, Heart, BadgeCheck } from "lucide-react";
import { PageHero } from "@/components/PageHero";
import { Section } from "@/components/ui/Section";
import { Container } from "@/components/ui/Container";
import { companyIntro } from "@/data/company";

export const metadata: Metadata = {
  title: "关于我们",
  description: "了解都佰城的公司背景、愿景使命、发展历程与资质认证。",
};

const valueIcons = {
  vision: Compass,
  mission: Target,
  values: Heart,
} as const;

export default function AboutPage() {
  return (
    <>
      <PageHero
        eyebrow="ABOUT US"
        title="关于都佰城"
        subtitle="一家以 PHA 为核心的合成生物学新材料企业,致力于为全球客户提供高性能、全生物降解的可持续材料解决方案。"
      />

      <Section
        eyebrow="OUR STORY"
        title="公司简介"
        subtitle="自 2015 年创立以来,都佰城始终聚焦于 PHA 这一具有完整生物可降解性的高性能材料。"
      >
        <div className="grid gap-12 lg:grid-cols-12">
          <div className="lg:col-span-7 space-y-5 text-base leading-relaxed text-slate-700">
            {companyIntro.long.map((p, i) => (
              <p key={i}>{p}</p>
            ))}
          </div>
          <div className="lg:col-span-5">
            <div className="rounded-2xl border border-slate-200 bg-tech-soft p-8">
              <div className="grid grid-cols-2 gap-6">
                {companyIntro.stats.map((s) => (
                  <div key={s.label}>
                    <div className="text-3xl font-semibold text-brand-900">
                      {s.value}
                    </div>
                    <div className="mt-1 text-xs text-slate-500">{s.label}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </Section>

      <Section
        eyebrow="VISION & MISSION"
        title="愿景 · 使命 · 价值观"
        className="bg-tech-soft"
      >
        <div className="grid gap-6 md:grid-cols-3">
          {(["vision", "mission", "values"] as const).map((key) => {
            const item = companyIntro[key];
            const Icon = valueIcons[key];
            return (
              <div
                key={key}
                className="rounded-2xl bg-white border border-slate-200 p-8 hover:shadow-soft transition"
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50 text-brand-900">
                  <Icon size={22} />
                </div>
                <h3 className="mt-5 text-xl font-semibold text-slate-900">
                  {item.title}
                </h3>
                <p className="mt-3 text-sm leading-relaxed text-slate-600">
                  {item.body}
                </p>
              </div>
            );
          })}
        </div>
      </Section>

      <Section eyebrow="MILESTONES" title="发展历程">
        <div className="relative max-w-3xl mx-auto">
          <div
            className="absolute left-3 sm:left-1/2 top-0 bottom-0 w-px bg-slate-200 -translate-x-px"
            aria-hidden
          />
          <ul className="space-y-10">
            {companyIntro.timeline.map((m, idx) => (
              <li
                key={m.year}
                className="relative pl-10 sm:pl-0 sm:grid sm:grid-cols-2 sm:gap-12 sm:items-center"
              >
                <div
                  className={
                    idx % 2 === 0 ? "sm:text-right sm:pr-12" : "sm:order-2 sm:pl-12"
                  }
                >
                  <div className="text-sm font-medium text-accent-500 mb-1">
                    {m.year}
                  </div>
                  <h3 className="text-lg font-semibold text-slate-900">
                    {m.title}
                  </h3>
                  <p className="mt-2 text-sm text-slate-600 leading-relaxed">
                    {m.desc}
                  </p>
                </div>
                <div
                  className={`absolute left-0 sm:left-1/2 top-1.5 h-3 w-3 rounded-full bg-brand-900 ring-4 ring-white -translate-x-1/2`}
                  aria-hidden
                />
              </li>
            ))}
          </ul>
        </div>
      </Section>

      <section className="py-16 sm:py-20 bg-tech-soft">
        <Container>
          <div className="text-center max-w-2xl mx-auto mb-12">
            <div className="text-sm font-medium uppercase tracking-[0.2em] text-accent-500 mb-3">
              CERTIFICATIONS
            </div>
            <h2 className="text-3xl sm:text-4xl font-semibold text-slate-900">
              资质与认证
            </h2>
          </div>
          <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 max-w-4xl mx-auto">
            {companyIntro.qualifications.map((q) => (
              <li
                key={q}
                className="flex items-start gap-3 rounded-xl bg-white border border-slate-200 px-5 py-4"
              >
                <BadgeCheck size={20} className="mt-0.5 text-accent-500 shrink-0" />
                <span className="text-sm text-slate-700">{q}</span>
              </li>
            ))}
          </ul>
        </Container>
      </section>
    </>
  );
}
