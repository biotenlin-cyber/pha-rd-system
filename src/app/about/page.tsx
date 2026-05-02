import type { Metadata } from "next";
import { LinkArrow } from "@/components/apple/LinkArrow";
import { companyIntro } from "@/data/company";

export const metadata: Metadata = {
  title: "关于都佰城",
  description: "了解都佰城的公司背景、愿景使命、发展历程与资质认证。",
};

export default function AboutPage() {
  return (
    <div className="bg-fog">
      <div className="space-y-2">
        {/* Hero */}
        <section className="bg-paper text-ink">
          <div className="mx-auto max-w-4xl px-6 sm:px-8 pt-24 sm:pt-32 pb-20 text-center">
            <div className="text-eyebrow mb-3 fade-up">ABOUT US</div>
            <h1 className="text-display sm:text-hero font-semibold tracking-tight fade-up">
              用合成生物学,
              <br />
              重新定义可持续材料。
            </h1>
            <p className="mt-6 text-lead text-ash max-w-2xl mx-auto fade-up-soft">
              {companyIntro.short}
            </p>
          </div>
        </section>

        {/* Long story */}
        <section className="bg-paper">
          <div className="mx-auto max-w-3xl px-6 sm:px-8 py-20 border-t border-hairline">
            <div className="text-eyebrow text-ink mb-4">OUR STORY</div>
            <h2 className="text-display font-semibold tracking-tight mb-8">
              从一个菌种,长成一座工厂。
            </h2>
            <div className="space-y-6 text-lg leading-[1.7] text-ink/85">
              {companyIntro.long.map((p, i) => (
                <p key={i}>{p}</p>
              ))}
            </div>
          </div>
        </section>

        {/* Stats */}
        <section className="bg-paper">
          <div className="mx-auto max-w-apple px-6 sm:px-8 py-16 grid grid-cols-2 md:grid-cols-4 gap-6 sm:gap-10 border-t border-hairline">
            {companyIntro.stats.map((s) => (
              <div key={s.label} className="text-center">
                <div className="text-section font-semibold text-ink">{s.value}</div>
                <div className="mt-1 text-sm text-smoke">{s.label}</div>
              </div>
            ))}
          </div>
        </section>

        {/* Values */}
        <section className="bg-obsidian text-paper">
          <div className="mx-auto max-w-apple px-6 sm:px-8 py-24">
            <div className="text-center max-w-3xl mx-auto mb-16">
              <div className="text-eyebrow text-white/80 mb-3">VISION · MISSION · VALUES</div>
              <h2 className="text-display font-semibold tracking-tight">
                我们相信,材料能改变世界。
              </h2>
            </div>
            <div className="grid gap-3 md:grid-cols-3">
              {(["vision", "mission", "values"] as const).map((key) => {
                const item = companyIntro[key];
                return (
                  <div key={key} className="rounded-tile bg-coal p-10">
                    <h3 className="text-2xl font-semibold tracking-tight">
                      {item.title}
                    </h3>
                    <p className="mt-4 text-base text-white/75 leading-relaxed">
                      {item.body}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* Timeline */}
        <section id="milestones" className="bg-paper">
          <div className="mx-auto max-w-4xl px-6 sm:px-8 py-24">
            <div className="text-center mb-16">
              <div className="text-eyebrow text-ink mb-3">MILESTONES</div>
              <h2 className="text-display font-semibold tracking-tight">
                十年,一步一个脚印。
              </h2>
            </div>
            <ol className="space-y-10 sm:space-y-12">
              {companyIntro.timeline.map((m) => (
                <li
                  key={m.year}
                  className="grid gap-3 sm:grid-cols-12 sm:gap-8 items-start"
                >
                  <div className="sm:col-span-3">
                    <div className="text-2xl sm:text-3xl font-semibold tracking-tight text-ink">
                      {m.year}
                    </div>
                  </div>
                  <div className="sm:col-span-9 sm:border-l sm:border-hairline sm:pl-8">
                    <h3 className="text-xl font-semibold tracking-tight">
                      {m.title}
                    </h3>
                    <p className="mt-2 text-base text-ash leading-relaxed">{m.desc}</p>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </section>

        {/* Certifications */}
        <section id="certifications" className="bg-fog">
          <div className="mx-auto max-w-apple px-6 sm:px-8 py-24">
            <div className="text-center max-w-3xl mx-auto mb-12">
              <div className="text-eyebrow text-ink mb-3">CERTIFICATIONS</div>
              <h2 className="text-display font-semibold tracking-tight">
                资质 与 认证。
              </h2>
            </div>
            <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {companyIntro.qualifications.map((q) => (
                <li
                  key={q}
                  className="rounded-tile bg-paper px-6 py-5 text-base text-ink"
                >
                  {q}
                </li>
              ))}
            </ul>
          </div>
        </section>

        {/* Platform pointer - 强化系统融合 */}
        <section className="bg-obsidian text-paper">
          <div className="mx-auto max-w-4xl px-6 sm:px-8 py-24 text-center">
            <div className="text-eyebrow text-white/80 mb-3">R&D PLATFORM</div>
            <h2 className="text-display font-semibold tracking-tight">
              我们的研发,跑在自研的平台上。
            </h2>
            <p className="mt-5 text-lead text-white/75 max-w-2xl mx-auto">
              都佰城内部研发依靠 PHA-RD 研发管理平台:把材料数据、产品节点与专利资产装进同一个系统。
            </p>
            <div className="mt-7 flex justify-center">
              <LinkArrow href="/platform" size="lg" className="text-white hover:text-white/85">
                了解 PHA-RD 平台
              </LinkArrow>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
