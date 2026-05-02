import Link from "next/link";
import { SplitTile } from "@/components/apple/SplitTile";
import { LinkArrow } from "@/components/apple/LinkArrow";
import { Reveal } from "@/components/apple/Reveal";
import { PHAVisual } from "@/components/visuals/PHAVisual";
import { PlatformVisual } from "@/components/visuals/PlatformVisual";
import { ProductVisual } from "@/components/visuals/ProductVisual";

export default function HomePage() {
  return (
    <div className="bg-fog">
      <div className="space-y-2">
        {/* Tile 1: 品牌主张 - PHA - 巨型 hero */}
        <section className="bg-paper text-ink relative overflow-hidden">
          <div className="mx-auto max-w-apple px-6 sm:px-8 pt-16 sm:pt-24 pb-8 text-center">
            <div className="text-eyebrow text-ink mb-3 fade-up">都佰城 PHA</div>
            <Reveal>
              <h1
                className="font-semibold tracking-tight leading-[0.96] max-w-5xl mx-auto"
                style={{ fontSize: "clamp(3rem, 8.5vw, 8rem)", letterSpacing: "-0.04em" }}
              >
                重塑塑料的未来。
              </h1>
            </Reveal>
            <Reveal delay={80}>
              <p
                className="mt-3 font-semibold tracking-tight text-smoke leading-[0.96]"
                style={{ fontSize: "clamp(2rem, 5.6vw, 5.25rem)", letterSpacing: "-0.035em" }}
              >
                从一颗颗粒开始。
              </p>
            </Reveal>
            <Reveal delay={180}>
              <p className="mt-7 text-lead text-ash max-w-2xl mx-auto">
                自主菌种、万吨级量产、全球认证。一种从自然来,也回归自然的高性能材料。
              </p>
            </Reveal>
            <Reveal delay={260}>
              <div className="mt-7 flex flex-wrap justify-center gap-x-6 gap-y-3">
                <LinkArrow href="/products" size="lg">
                  了解 PHA 产品
                </LinkArrow>
                <LinkArrow href="/contact" size="lg">
                  申请样品
                </LinkArrow>
              </div>
            </Reveal>
          </div>
          <Reveal delay={120}>
            <div className="mx-auto max-w-5xl px-6 sm:px-8 pb-12 sm:pb-20">
              <PHAVisual />
            </div>
          </Reveal>
        </section>

        {/* Tile 2: 都佰城研发管理平台 - 黑底巨型 */}
        <section className="bg-obsidian text-paper relative overflow-hidden">
          <div className="mx-auto max-w-apple px-6 sm:px-8 pt-16 sm:pt-24 pb-8 text-center">
            <div className="text-eyebrow text-white/80 mb-3 fade-up">
              都佰城研发管理平台 · PHA-RD
            </div>
            <Reveal>
              <h2
                className="font-semibold tracking-tight leading-[0.98] max-w-5xl mx-auto"
                style={{ fontSize: "clamp(2.75rem, 7.6vw, 7.25rem)", letterSpacing: "-0.035em" }}
              >
                一个系统,
                <br />
                <span className="text-white/55">掌管整个研发链。</span>
              </h2>
            </Reveal>
            <Reveal delay={120}>
              <p className="mt-7 text-lead text-white/75 max-w-2xl mx-auto">
                材料研发、产品开发、知识产权,装进同一个工作流。让 12 万次实验,变成可检索的资产。
              </p>
            </Reveal>
            <Reveal delay={200}>
              <div className="mt-7 flex flex-wrap justify-center gap-x-6 gap-y-3">
                <LinkArrow
                  href="/platform"
                  size="lg"
                  className="text-white hover:text-white/85"
                >
                  走进平台
                </LinkArrow>
                <LinkArrow
                  href="/contact"
                  size="lg"
                  className="text-white hover:text-white/85"
                >
                  预约演示
                </LinkArrow>
              </div>
            </Reveal>
          </div>
          <Reveal delay={120}>
            <div className="mx-auto max-w-5xl px-6 sm:px-8 pb-12 sm:pb-20">
              <PlatformVisual />
            </div>
          </Reveal>
        </section>

        {/* Tile 3: 双产品 - 薄膜/注塑 */}
        <SplitTile
          items={[
            {
              theme: "light",
              eyebrow: "薄膜级 · DBC-F100",
              title: "高韧性。可堆肥。",
              subtitle: "购物袋、农膜、食品包装,以 PHA 替代一次性塑料。",
              ctas: (
                <>
                  <LinkArrow href="/products/dbc-f100">了解更多</LinkArrow>
                  <LinkArrow href="/contact">申请样品</LinkArrow>
                </>
              ),
              visual: <ProductVisual tone="pearl" shape="film" />,
            },
            {
              theme: "light",
              eyebrow: "注塑级 · DBC-I200",
              title: "通用。耐热。可降解。",
              subtitle: "高流动性 PHA 注塑原料,适用于餐具、容器与电子配件。",
              ctas: (
                <>
                  <LinkArrow href="/products/dbc-i200">了解更多</LinkArrow>
                  <LinkArrow href="/contact">申请样品</LinkArrow>
                </>
              ),
              visual: <ProductVisual tone="blue" shape="pellet" />,
            },
          ]}
        />

        {/* Tile 4: 应用场景 */}
        <SplitTile
          items={[
            {
              theme: "dark",
              eyebrow: "应用 · 包装 / 3D 打印",
              title: "在每一只袋子里,看见可持续。",
              subtitle: "从电商缓冲材料到 3D 打印线材,以 PHA 重塑日常用品的全生命周期。",
              ctas: (
                <LinkArrow href="/products" className="text-white hover:text-white/90">
                  查看应用案例
                </LinkArrow>
              ),
              visual: <ProductVisual tone="midnight" shape="pellet" />,
            },
            {
              theme: "dark",
              eyebrow: "应用 · 医疗 / 农业",
              title: "更友好的材料,与人和土地共处。",
              subtitle: "可吸收医用器械与无微塑料残留的农用地膜,把 PHA 推向严苛场景。",
              ctas: (
                <LinkArrow href="/products" className="text-white hover:text-white/90">
                  查看应用案例
                </LinkArrow>
              ),
              visual: <ProductVisual tone="graphite" shape="fiber" />,
            },
          ]}
        />

        {/* Tile 5: 资讯 + 认证 */}
        <SplitTile
          items={[
            {
              theme: "light",
              eyebrow: "都佰城动态",
              title: "万吨级 PHA 工厂正式投产。",
              subtitle: "盐城智能化工厂全线试车完成,公司进入规模化稳定供货阶段。",
              ctas: <LinkArrow href="/news/10000-ton-plant-online">阅读全文</LinkArrow>,
            },
            {
              theme: "light",
              eyebrow: "全球认证",
              title: "EN13432 / BPI / OK Compost。",
              subtitle: "覆盖工业堆肥、土壤、海洋等多种环境的可降解认证体系。",
              ctas: <LinkArrow href="/about#certifications">查看资质清单</LinkArrow>,
            },
          ]}
        />

        {/* Tile 6: 全站 CTA - apple "Shop and Learn" 风格 */}
        <section className="bg-paper">
          <div className="mx-auto max-w-apple px-6 sm:px-8 py-24 grid gap-3 md:grid-cols-3">
            <Link
              href="/products"
              className="group rounded-marble bg-fog p-10 hover:bg-haze transition flex flex-col"
            >
              <div className="text-eyebrow text-ink mb-3">EXPLORE</div>
              <h3 className="text-section font-semibold tracking-tight">
                浏览全部 PHA 产品。
              </h3>
              <span className="mt-4 link-arrow text-sm">查看产品矩阵</span>
            </Link>
            <Link
              href="/platform"
              className="group rounded-marble bg-fog p-10 hover:bg-haze transition flex flex-col"
            >
              <div className="text-eyebrow text-ink mb-3">PLATFORM</div>
              <h3 className="text-section font-semibold tracking-tight">
                了解 PHA-RD 研发管理平台。
              </h3>
              <span className="mt-4 link-arrow text-sm">走进平台</span>
            </Link>
            <Link
              href="/contact"
              className="group rounded-marble bg-fog p-10 hover:bg-haze transition flex flex-col"
            >
              <div className="text-eyebrow text-ink mb-3">CONTACT</div>
              <h3 className="text-section font-semibold tracking-tight">
                与我们的团队聊聊。
              </h3>
              <span className="mt-4 link-arrow text-sm">申请样品 / 预约演示</span>
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
}
