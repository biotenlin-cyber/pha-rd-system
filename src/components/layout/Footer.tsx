import Link from "next/link";
import { footerNav, siteConfig } from "@/data/site";

export function Footer() {
  return (
    <footer className="bg-fog text-ash">
      <div className="mx-auto max-w-[1024px] px-6 sm:px-8 py-8 text-xs leading-[1.6]">
        <p className="text-ash">
          1. 产品参数与认证情况以最新批次随附技术文件为准。本网站涉及的应用案例仅供示意,实际效果取决于客户具体加工与使用条件。
        </p>
        <p className="mt-3 text-ash">
          2. 都佰城新材料保留对产品规格、工艺、价格等进行调整的权利。如需获取最新技术资料或样品,请通过{" "}
          <Link href="/contact" className="text-link hover:text-linkHover">
            联系我们
          </Link>{" "}
          页面与商务团队取得联系。
        </p>

        <div className="mt-8 border-t border-hairline pt-8 grid gap-8 md:grid-cols-4">
          {footerNav.map((col) => (
            <div key={col.title}>
              <h3 className="text-[12px] font-semibold text-ink mb-3">
                {col.title}
              </h3>
              <ul className="space-y-2">
                {col.items.map((it) => (
                  <li key={it.href + it.label}>
                    <Link
                      href={it.href}
                      className="text-ash hover:text-ink transition"
                    >
                      {it.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-8 border-t border-hairline pt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-ash">
            Copyright © {new Date().getFullYear()} {siteConfig.fullName}. 保留所有权利。
          </p>
          <ul className="flex flex-wrap gap-x-5 gap-y-2 text-ash">
            <li>
              <Link href="#" className="hover:text-ink">
                隐私政策
              </Link>
            </li>
            <li>
              <Link href="#" className="hover:text-ink">
                使用条款
              </Link>
            </li>
            <li>
              <Link href="#" className="hover:text-ink">
                法律声明
              </Link>
            </li>
            <li>
              <span className="text-ash">沪 ICP 备 XXXXXXXX 号</span>
            </li>
          </ul>
        </div>

        <div className="mt-4 text-ash">中国大陆</div>
      </div>
    </footer>
  );
}
