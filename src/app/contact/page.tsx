import type { Metadata } from "next";
import { Mail, MapPin, Phone, Clock, MessageSquareText } from "lucide-react";
import { PageHero } from "@/components/PageHero";
import { Container } from "@/components/ui/Container";
import { ContactForm } from "@/components/contact/ContactForm";
import { siteConfig } from "@/data/site";

export const metadata: Metadata = {
  title: "联系我们",
  description: "联系都佰城,获取 PHA 产品资料、技术咨询与样品申请。",
};

const contactCards = [
  {
    icon: MapPin,
    title: "公司地址",
    body: siteConfig.contact.address,
  },
  {
    icon: Phone,
    title: "联系电话",
    body: siteConfig.contact.phone,
  },
  {
    icon: Mail,
    title: "电子邮箱",
    body: siteConfig.contact.email,
  },
  {
    icon: Clock,
    title: "工作时间",
    body: siteConfig.contact.workingHours,
  },
];

export default function ContactPage() {
  return (
    <>
      <PageHero
        eyebrow="CONTACT"
        title="联系我们"
        subtitle="无论是产品选型、技术合作还是样品申请,我们都期待与您建立联系。"
      />

      <section className="py-16 sm:py-20">
        <Container>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {contactCards.map((c) => (
              <div
                key={c.title}
                className="rounded-2xl bg-white border border-slate-200 p-6 hover:shadow-soft transition"
              >
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-brand-50 text-brand-900">
                  <c.icon size={20} />
                </div>
                <h3 className="mt-5 text-sm font-medium text-slate-500">
                  {c.title}
                </h3>
                <p className="mt-1 text-base font-semibold text-slate-900 break-words">
                  {c.body}
                </p>
              </div>
            ))}
          </div>
        </Container>
      </section>

      <section className="pb-20">
        <Container>
          <div className="grid gap-10 lg:grid-cols-12">
            <div className="lg:col-span-5">
              <div className="text-sm font-medium uppercase tracking-[0.2em] text-accent-500 mb-3">
                LEAVE A MESSAGE
              </div>
              <h2 className="text-3xl sm:text-4xl font-semibold text-slate-900 leading-tight">
                给我们留言
              </h2>
              <p className="mt-5 text-base text-slate-600 leading-relaxed">
                请填写右侧表单,我们的商务或技术团队将在 1—2 个工作日内与您取得联系。
              </p>

              <div className="mt-8 rounded-2xl bg-tech-soft border border-slate-200 p-6">
                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white text-brand-900 border border-slate-200 shrink-0">
                    <MessageSquareText size={18} />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-slate-900">
                      微信公众号
                    </h3>
                    <p className="mt-1 text-sm text-slate-600">
                      关注 「{siteConfig.social.wechat}」,获取最新行业资讯与产品动态。
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="lg:col-span-7">
              <ContactForm />
            </div>
          </div>
        </Container>
      </section>

      <section className="pb-20">
        <Container>
          <div
            className="relative h-72 sm:h-96 rounded-2xl overflow-hidden border border-slate-200 bg-tech-soft"
            aria-label="公司地址示意地图"
          >
            <div className="absolute inset-0 bg-grid opacity-50" aria-hidden />
            <div className="absolute inset-0 flex items-center justify-center text-center px-6">
              <div>
                <div className="mx-auto h-12 w-12 grid place-items-center rounded-full bg-brand-900 text-white shadow-soft">
                  <MapPin size={20} />
                </div>
                <p className="mt-4 text-base font-semibold text-slate-900">
                  {siteConfig.contact.address}
                </p>
                <p className="mt-1 text-sm text-slate-500">
                  地图占位 · 实际部署时可接入高德 / 百度 / Google 地图嵌入
                </p>
              </div>
            </div>
          </div>
        </Container>
      </section>
    </>
  );
}
