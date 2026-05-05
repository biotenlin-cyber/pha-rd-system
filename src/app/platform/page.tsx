import type { Metadata } from "next";
import { Hero } from "@/components/apple/Hero";
import { LinkArrow } from "@/components/apple/LinkArrow";
import { Reveal } from "@/components/apple/Reveal";
import { PlatformVisual } from "@/components/visuals/PlatformVisual";
import {
  platformOverview,
  platformModules,
  platformWorkflow,
  platformDeployment,
} from "@/data/platform";

export const metadata: Metadata = {
  title: "都佰城研发管理平台",
  description:
    "都佰城自研的 PHA-RD 研发管理平台,把材料研发、产品开发与知识产权,装进同一个工作流。",
};

export default function PlatformPage() {
  return (
    <div className="bg-fog">
      <div className="space-y-2">
        {/* Hero */}
        <Hero
          eyebrow={platformOverview.eyebrow}
          size="mega"
          title={platformOverview.title}
          subtitle={platformOverview.subtitle}
          cta={[
            { label: "查看模块", href: "#modules" },
            { label: "预约演示", href: "/contact" },
          ]}
          visual={<PlatformVisual />}
        />

        {/* Stats strip */}
        <section className="bg-paper">
          <div className="mx-auto max-w-apple px-6 sm:px-8 py-12 sm:py-16 grid grid-cols-2 md:grid-cols-4 gap-6 sm:gap-10 border-t border-hairline">
            {platformOverview.stats.map((s) => (
              <div key={s.label} className="text-center">
                <div className="text-section font-semibold text-ink">{s.value}</div>
                <div className="mt-1 text-sm text-smoke">{s.label}</div>
              </div>
            ))}
          </div>
        </section>

        {/* Modules */}
        <section id="modules" className="bg-paper">
          <div className="mx-auto max-w-apple px-6 sm:px-8 py-20 sm:py-28">
            <div className="text-center max-w-3xl mx-auto mb-16">
              <div className="text-eyebrow text-ink mb-3">PLATFORM MODULES</div>
              <h2 className="text-display font-semibold tracking-tight">
                四个核心模块,
                <br />
                覆盖研发的每一英里。
              </h2>
            </div>

            <div className="space-y-3">
              {platformModules.map((m, idx) => (
                <Reveal
                  key={m.id}
                  delay={idx * 60}
                  as="article"
                  id={m.id}
                  className={`rounded-marble overflow-hidden grid md:grid-cols-2 ${
                    idx % 2 === 0 ? "bg-fog" : "bg-coal text-paper"
                  }`}
                >
                  <div className="p-10 sm:p-14 flex flex-col justify-center">
                    <div className={`text-eyebrow mb-3 ${idx % 2 === 0 ? "text-ink" : "text-white/80"}`}>
                      {m.badge}
                    </div>
                    <h3 className="text-section font-semibold tracking-tight">
                      {m.title}
                    </h3>
                    <p className={`mt-2 text-lg ${idx % 2 === 0 ? "text-ash" : "text-white/70"}`}>
                      {m.subtitle}
                    </p>
                    <p className={`mt-5 text-base leading-relaxed ${idx % 2 === 0 ? "text-ink/85" : "text-white/85"}`}>
                      {m.description}
                    </p>
                    <ul className="mt-6 space-y-2 text-[15px]">
                      {m.capabilities.map((c) => (
                        <li key={c} className="flex items-start gap-3">
                          <span
                            className={`mt-2 h-1.5 w-1.5 rounded-full shrink-0 ${
                              idx % 2 === 0 ? "bg-link" : "bg-white"
                            }`}
                          />
                          <span>{c}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div
                    className={`p-10 sm:p-14 flex items-center justify-center ${
                      idx % 2 === 0 ? "bg-paper" : "bg-obsidian"
                    }`}
                  >
                    <ModuleVisual variant={m.id} darkMode={idx % 2 === 1} />
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* Workflow */}
        <section className="bg-obsidian text-paper">
          <div className="mx-auto max-w-apple px-6 sm:px-8 py-24 text-center">
            <Reveal>
              <div className="text-eyebrow text-white/80 mb-3">WORKFLOW</div>
              <h2 className="text-display font-semibold tracking-tight max-w-3xl mx-auto">
                一条流水线,从需求到量产。
              </h2>
            </Reveal>
            <div className="mt-12 grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
              {platformWorkflow.map((w, i) => (
                <Reveal
                  key={w.step}
                  delay={i * 70}
                  className="rounded-tile bg-coal p-6 text-left border border-white/5"
                >
                  <div className="text-eyebrow text-link">{w.step}</div>
                  <h3 className="mt-2 text-lg font-semibold">{w.title}</h3>
                  <p className="mt-2 text-sm text-white/70 leading-relaxed">
                    {w.desc}
                  </p>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* Deployment & Compliance */}
        <section className="bg-paper">
          <div className="mx-auto max-w-apple px-6 sm:px-8 py-24">
            <Reveal>
              <div className="text-center max-w-2xl mx-auto mb-12">
                <div className="text-eyebrow text-ink mb-3">DEPLOYMENT</div>
                <h2 className="text-display font-semibold tracking-tight">
                  安全交付,可控演进。
                </h2>
              </div>
            </Reveal>
            <div className="grid gap-3 md:grid-cols-3">
              {platformDeployment.map((d, i) => (
                <Reveal key={d.title} delay={i * 80} className="rounded-tile bg-fog p-8">
                  <h3 className="text-lg font-semibold">{d.title}</h3>
                  <p className="mt-3 text-base text-ash leading-relaxed">{d.desc}</p>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="bg-fog">
          <div className="mx-auto max-w-apple px-6 sm:px-8 py-24 text-center">
            <h2 className="text-display font-semibold tracking-tight">
              想看一次平台的真实演示?
            </h2>
            <p className="mt-4 text-lead text-ash max-w-2xl mx-auto">
              我们的解决方案工程师会根据您团队的规模与场景,提供一对一演示与试用通道。
            </p>
            <div className="mt-7 flex flex-wrap justify-center gap-x-6 gap-y-3">
              <LinkArrow href="/contact" size="lg">
                预约演示
              </LinkArrow>
              <LinkArrow href="/products" size="lg">
                查看 PHA 产品
              </LinkArrow>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

function ModuleVisual({ variant, darkMode }: { variant: string; darkMode: boolean }) {
  const fg = darkMode ? "#ffffff" : "#1d1d1f";
  const muted = darkMode ? "rgba(255,255,255,0.18)" : "#e5e7ec";
  const accent = "#0071e3";

  return (
    <svg viewBox="0 0 480 360" className="w-full max-w-md aspect-[4/3]" aria-hidden>
      {variant === "material" && (
        <g>
          {[0, 1, 2].map((row) =>
            [0, 1, 2, 3].map((col) => (
              <rect
                key={`${row}-${col}`}
                x={60 + col * 90}
                y={60 + row * 80}
                width="78"
                height="68"
                rx="10"
                fill={muted}
                opacity={(row * 4 + col) % 5 === 0 ? 1 : 0.55}
              />
            )),
          )}
          <rect x={60} y={60} width="78" height="68" rx="10" fill={accent} />
          <rect x={150} y={140} width="78" height="68" rx="10" fill={accent} opacity="0.6" />
          <rect x={330} y={220} width="78" height="68" rx="10" fill={accent} opacity="0.85" />
        </g>
      )}
      {variant === "product" && (
        <g>
          <rect x="40" y="100" width="400" height="6" fill={muted} />
          {[80, 180, 280, 380].map((x, i) => (
            <g key={x}>
              <circle cx={x} cy="103" r="14" fill={i <= 1 ? accent : muted} />
              <text x={x} y="148" textAnchor="middle" fontSize="13" fill={fg} opacity="0.8">
                {["立项", "样品", "验证", "量产"][i]}
              </text>
            </g>
          ))}
          <rect x="40" y="200" width="400" height="60" rx="10" fill={muted} />
          <rect x="40" y="200" width="240" height="60" rx="10" fill={accent} opacity="0.85" />
          <rect x="40" y="280" width="400" height="40" rx="10" fill={muted} />
          <rect x="40" y="280" width="160" height="40" rx="10" fill={accent} opacity="0.6" />
        </g>
      )}
      {variant === "patent" && (
        <g>
          {[0, 1, 2, 3].map((i) => (
            <g key={i} transform={`translate(${40 + i * 100}, 80)`}>
              <rect width="80" height="110" rx="10" fill={muted} />
              <rect x="10" y="14" width="60" height="6" rx="3" fill={fg} opacity="0.65" />
              <rect x="10" y="28" width="40" height="6" rx="3" fill={fg} opacity="0.4" />
              <rect x="10" y="80" width="60" height="14" rx="4" fill={i < 2 ? accent : fg} opacity={i < 2 ? 1 : 0.3} />
            </g>
          ))}
          <text x="240" y="240" textAnchor="middle" fontSize="14" fill={fg} opacity="0.65">
            120+ 专利组合 · PCT / 海外 / 国内
          </text>
        </g>
      )}
      {variant === "analytics" && (
        <g>
          <rect x="40" y="60" width="400" height="40" rx="8" fill={muted} />
          <rect x="40" y="60" width="280" height="40" rx="8" fill={accent} opacity="0.85" />

          {[0, 1, 2, 3, 4, 5, 6].map((i) => {
            const heights = [60, 90, 70, 110, 95, 130, 100];
            return (
              <rect
                key={i}
                x={50 + i * 56}
                y={260 - heights[i]}
                width="34"
                height={heights[i]}
                rx="6"
                fill={i % 2 ? accent : muted}
                opacity={i % 2 ? 0.85 : 1}
              />
            );
          })}
          <rect x="40" y="280" width="400" height="2" fill={muted} />
        </g>
      )}
    </svg>
  );
}
