import Link from "next/link";
import { Mail, MapPin, Phone, Clock } from "lucide-react";
import { mainNav, siteConfig } from "@/data/site";

export function Footer() {
  return (
    <footer className="bg-slate-950 text-slate-300">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid gap-10 lg:grid-cols-12">
          <div className="lg:col-span-5">
            <div className="flex items-center gap-2">
              <span className="grid h-9 w-9 place-items-center rounded-xl bg-white text-brand-900 font-semibold">
                都
              </span>
              <span className="flex flex-col leading-tight">
                <span className="text-base font-semibold text-white">
                  {siteConfig.fullName}
                </span>
                <span className="text-[11px] text-slate-400">DUBAICHENG NEW MATERIAL</span>
              </span>
            </div>
            <p className="mt-5 text-sm leading-relaxed text-slate-400 max-w-md">
              {siteConfig.description}
            </p>
          </div>

          <div className="lg:col-span-3">
            <h3 className="text-sm font-semibold text-white mb-4">站点导航</h3>
            <ul className="space-y-2 text-sm">
              {mainNav.map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className="text-slate-400 hover:text-white transition"
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div className="lg:col-span-4">
            <h3 className="text-sm font-semibold text-white mb-4">联系我们</h3>
            <ul className="space-y-3 text-sm text-slate-400">
              <li className="flex gap-3">
                <MapPin size={16} className="mt-0.5 shrink-0 text-accent-400" />
                <span>{siteConfig.contact.address}</span>
              </li>
              <li className="flex gap-3">
                <Phone size={16} className="mt-0.5 shrink-0 text-accent-400" />
                <span>{siteConfig.contact.phone}</span>
              </li>
              <li className="flex gap-3">
                <Mail size={16} className="mt-0.5 shrink-0 text-accent-400" />
                <a
                  href={`mailto:${siteConfig.contact.email}`}
                  className="hover:text-white transition"
                >
                  {siteConfig.contact.email}
                </a>
              </li>
              <li className="flex gap-3">
                <Clock size={16} className="mt-0.5 shrink-0 text-accent-400" />
                <span>{siteConfig.contact.workingHours}</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-white/10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 text-xs text-slate-500">
          <span>
            © {new Date().getFullYear()} {siteConfig.fullName}. All rights reserved.
          </span>
          <span>沪 ICP 备 XXXXXXXX 号</span>
        </div>
      </div>
    </footer>
  );
}
