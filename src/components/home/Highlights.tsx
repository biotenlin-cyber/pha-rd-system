import { FlaskConical, Factory, ShieldCheck, Globe2 } from "lucide-react";
import { Section } from "@/components/ui/Section";

const items = [
  {
    icon: FlaskConical,
    title: "自主研发",
    desc: "从底盘菌种到改性配方,全链路自研,核心技术安全可控。",
  },
  {
    icon: Factory,
    title: "规模化生产",
    desc: "万吨级智能化工厂稳定供货,批次一致性 ≥ 99%。",
  },
  {
    icon: ShieldCheck,
    title: "专利布局",
    desc: "覆盖菌种、工艺、改性的 120+ 专利组合,技术壁垒扎实。",
  },
  {
    icon: Globe2,
    title: "全球客户",
    desc: "服务全球 30+ 品牌客户,出口欧美、日韩与东南亚。",
  },
];

export function Highlights() {
  return (
    <Section
      eyebrow="WHY DUBAICHENG"
      title="为什么选择都佰城"
      subtitle="围绕 PHA 这一核心材料,我们以技术深度与产业化能力,持续为客户创造长期价值。"
    >
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {items.map(({ icon: Icon, title, desc }) => (
          <div
            key={title}
            className="group rounded-2xl bg-white p-6 border border-slate-200 hover:border-brand-200 hover:shadow-soft transition"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50 text-brand-900 group-hover:bg-brand-900 group-hover:text-white transition">
              <Icon size={22} />
            </div>
            <h3 className="mt-5 text-lg font-semibold text-slate-900">{title}</h3>
            <p className="mt-2 text-sm leading-relaxed text-slate-600">{desc}</p>
          </div>
        ))}
      </div>
    </Section>
  );
}
