import { Tile } from "@/components/apple/Tile";
import { SplitTile } from "@/components/apple/SplitTile";
import { LinkArrow } from "@/components/apple/LinkArrow";
import { PHAVisual } from "@/components/visuals/PHAVisual";
import { PlatformVisual } from "@/components/visuals/PlatformVisual";
import { ProductVisual } from "@/components/visuals/ProductVisual";

export default function HomePage() {
  return (
    <div className="bg-fog">
      <div className="space-y-2">
        {/* Tile 1: 品牌主张 - PHA */}
        <Tile
          theme="light"
          eyebrow="都佰城 PHA"
          title={
            <>
              重塑塑料的未来。
              <br />
              <span className="text-smoke">从一颗颗粒开始。</span>
            </>
          }
          subtitle="自主菌种、万吨级量产、全球认证。一种从自然来,也回归自然的高性能材料。"
          ctas={
            <>
              <LinkArrow href="/products" size="lg">
                了解 PHA 产品
              </LinkArrow>
              <LinkArrow href="/contact" size="lg">
                申请样品
              </LinkArrow>
            </>
          }
          visual={<PHAVisual />}
        />

        {/* Tile 2: 研发管理平台 - 重点强调 */}
        <Tile
          theme="dark"
          eyebrow="都佰城研发管理平台 · PHA-RD"
          title={
            <>
              一个系统,
              <br />
              掌管整个研发链。
            </>
          }
          subtitle="材料研发、产品开发、知识产权,装进同一个工作流。让 12 万次实验,变成可检索的资产。"
          ctas={
            <>
              <LinkArrow href="/platform" size="lg" className="text-white hover:text-white/90">
                走进平台
              </LinkArrow>
              <LinkArrow href="/contact" size="lg" className="text-white hover:text-white/90">
                预约演示
              </LinkArrow>
            </>
          }
          visual={<PlatformVisual />}
        />

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
                  <LinkArrow href="/products#dbc-f100">了解更多</LinkArrow>
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
                  <LinkArrow href="/products#dbc-i200">了解更多</LinkArrow>
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
              ctas: <LinkArrow href="/products" className="text-white hover:text-white/90">查看应用案例</LinkArrow>,
              visual: <ProductVisual tone="midnight" shape="pellet" />,
            },
            {
              theme: "dark",
              eyebrow: "应用 · 医疗 / 农业",
              title: "更友好的材料,与人和土地共处。",
              subtitle: "可吸收医用器械与无微塑料残留的农用地膜,把 PHA 推向严苛场景。",
              ctas: <LinkArrow href="/products" className="text-white hover:text-white/90">查看应用案例</LinkArrow>,
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
              subtitle: "覆盖工业堆冶、土壤、海洋等多种环境的可降解认证体系。",
              ctas: <LinkArrow href="/about#certifications">查看资质清单</LinkArrow>,
            },
          ]}
        />
      </div>
    </div>
  );
}
