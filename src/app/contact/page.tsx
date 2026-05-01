import type { Metadata } from "next";
import { Mail, MapPin, Phone, Clock } from "lucide-react";
import { ContactForm } from "@/components/contact/ContactForm";
import { LinkArrow } from "@/components/apple/LinkArrow";
import { siteConfig } from "@/data/site";

export const metadata: Metadata = {
  title: "联系都佰城",
  description: "联系都佰城,获取 PHA 产品资料、平台演示、技术咨询与样品申请。",
};

const channels = [
  {
    icon: Mail,
    title: "商务合作",
    desc: "产品采购、应用开发、长期供货合作。",
    contact: siteConfig.contact.email,
    href: `mailto:${siteConfig.contact.email}`,
  },
  {
    icon: Phone,
    title: "电话咨询",
    desc: "工作日 09:00 — 18:00 由专人接听。",
    contact: siteConfig.contact.phone,
    href: `tel:${siteConfig.contact.phone}`,
  },
  {
    icon: MapPin,
    title: "总部地址",
    desc: "上海张江高科技园区。",
    contact: siteConfig.contact.address,
    href: "#",
  },
  {
    icon: Clock,
    title: "工作时间",
    desc: "周一至周五接待,节假日邮件回复。",
    contact: siteConfig.contact.workingHours,
    href: "#",
  },
];

export default function ContactPage() {
  return (
    <div className="bg-fog">
      <div className="space-y-2">
        {/* Hero */}
        <section className="bg-paper">
          <div className="mx-auto max-w-4xl px-6 sm:px-8 pt-20 sm:pt-28 pb-16 text-center">
            <div className="text-eyebrow text-ink mb-3 fade-up">CONTACT</div>
            <h1 className="text-display sm:text-hero font-semibold tracking-tight fade-up">
              我们,
              <br />
              在听。
            </h1>
            <p className="mt-5 text-lead text-ash max-w-2xl mx-auto fade-up-soft">
              产品咨询、平台演示、样品申请、媒体联络。选择最方便的方式,与都佰城团队建立联系。
            </p>
          </div>
        </section>

        {/* Channels */}
        <section className="bg-paper">
          <div className="mx-auto max-w-6xl px-6 sm:px-8 py-12 border-t border-hairline">
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              {channels.map((c) => (
                <a
                  key={c.title}
                  href={c.href}
                  className="group rounded-tile bg-fog p-7 hover:bg-haze transition flex flex-col"
                >
                  <c.icon size={22} strokeWidth={1.6} className="text-ink" />
                  <h3 className="mt-5 text-lg font-semibold tracking-tight">
                    {c.title}
                  </h3>
                  <p className="mt-2 text-sm text-ash leading-relaxed flex-1">
                    {c.desc}
                  </p>
                  <span className="mt-4 link-arrow text-sm">{c.contact}</span>
                </a>
              ))}
            </div>
          </div>
        </section>

        {/* Form */}
        <section className="bg-paper">
          <div className="mx-auto max-w-3xl px-6 sm:px-8 py-20 border-t border-hairline">
            <div className="text-center mb-12">
              <div className="text-eyebrow text-ink mb-3">SEND A MESSAGE</div>
              <h2 className="text-display font-semibold tracking-tight">
                给我们留言。
              </h2>
              <p className="mt-4 text-lead text-ash max-w-xl mx-auto">
                填写下方表单,我们的商务或技术团队将在 1—2 个工作日内与您取得联系。
              </p>
            </div>
            <ContactForm />
          </div>
        </section>

        {/* Map placeholder + further links */}
        <section className="bg-fog">
          <div className="mx-auto max-w-6xl px-6 sm:px-8 py-20 grid gap-4 lg:grid-cols-2">
            <div className="rounded-tile overflow-hidden bg-paper border border-hairline relative min-h-[320px]">
              <div className="absolute inset-0 flex items-center justify-center text-center px-8">
                <div>
                  <div className="mx-auto h-12 w-12 grid place-items-center rounded-full bg-ink text-white">
                    <MapPin size={20} strokeWidth={1.6} />
                  </div>
                  <p className="mt-5 text-base font-semibold">
                    {siteConfig.contact.address}
                  </p>
                  <p className="mt-1 text-sm text-smoke">
                    地图占位 · 部署时可接入高德 / 百度 / Google Maps 嵌入
                  </p>
                </div>
              </div>
            </div>
            <div className="rounded-tile bg-paper p-10 flex flex-col">
              <div className="text-eyebrow text-ink mb-3">了解更多</div>
              <h3 className="text-section font-semibold tracking-tight">
                先看一眼,再决定怎么聊。
              </h3>
              <p className="mt-4 text-base text-ash leading-relaxed">
                如果您还在评估 PHA 是否适合您的产品,或对都佰城研发管理平台感兴趣,可以先浏览这些资源。
              </p>
              <div className="mt-6 flex flex-col gap-3">
                <LinkArrow href="/products">PHA 产品矩阵</LinkArrow>
                <LinkArrow href="/platform">研发管理平台 PHA-RD</LinkArrow>
                <LinkArrow href="/news">Newsroom 最新动态</LinkArrow>
                <LinkArrow href="/about">关于都佰城</LinkArrow>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
