import Link from "next/link";
import { footerNav, siteConfig } from "@/data/site";

/**
 * 把 `#` 死链渲染为不可点击的占位,保留视觉但不污染 SEO/a11y。
 * 真实路径走 next/link。
 */
function FooterLink({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) {
  if (href === "#") {
    return (
      <span
        aria-disabled="true"
        className="text-silver cursor-not-allowed select-none"
        title="即将上线"
      >
        {children}
      </span>
    );
  }
  return (
    <Link
      href={href}
      className="text-ash hover:text-ink hover:underline underline-offset-2 transition"
    >
      {children}
    </Link>
  );
}

export function Footer() {
  return (
    <footer className="bg-fog text-ash">
      <div className="mx-auto max-w-[1024px] px-6 sm:px-8 py-8 text-xs leading-[1.6]">
        {/* 法律说明小字 — 苹果官网式样 */}
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
        <p className="mt-3 text-ash">
          3. 都佰城研发管理平台 (PHA-RD) 为公司内部研发系统,目前面向特邀生态伙伴开放试用,不对公众开放注册。
        </p>

        {/* 多列站点地图 — Shop and Learn 段 */}
        <div className="mt-9 border-t border-hairline pt-9 grid gap-x-6 gap-y-8 md:grid-cols-3 lg:grid-cols-5">
          {footerNav.map((col) => (
            <div key={col.title}>
              <h3 className="text-[12px] font-semibold text-ink mb-3">
                {col.title}
              </h3>
              <ul className="space-y-[6px]">
                {col.items.map((it) => (
                  <li key={it.href + it.label}>
                    <FooterLink href={it.href}>{it.label}</FooterLink>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* 二级聚合段 — 苹果"还有更多购物方式"区 */}
        <div className="mt-9 border-t border-hairline pt-7">
          <p className="text-ash">
            还有更多了解都佰城的方式:{" "}
            <Link href="/contact" className="text-link hover:text-linkHover">
              申请样品
            </Link>
            {"  "}或{"  "}
            <Link href="/platform" className="text-link hover:text-linkHover">
              预约 PHA-RD 平台演示 ›
            </Link>
          </p>
          <p className="mt-2 text-ash">
            想加入我们?
            <span
              aria-disabled="true"
              className="text-silver cursor-not-allowed select-none ml-1"
              title="即将上线"
            >
              招贤纳士
            </span>
            {" "}页面即将上线。
          </p>
        </div>

        {/* 底部版权 + 法律链接 + 地区 */}
        <div className="mt-9 border-t border-hairline pt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-ash">
            Copyright © {new Date().getFullYear()} {siteConfig.fullName}. 保留所有权利。
          </p>
          <ul className="flex flex-wrap gap-x-5 gap-y-2 text-silver">
            <li><span aria-disabled="true" className="cursor-not-allowed">隐私政策</span></li>
            <li><span aria-disabled="true" className="cursor-not-allowed">使用条款</span></li>
            <li><span aria-disabled="true" className="cursor-not-allowed">法律声明</span></li>
            <li><span aria-disabled="true" className="cursor-not-allowed">网站地图</span></li>
            <li><span>沪 ICP 备 XXXXXXXX 号</span></li>
          </ul>
        </div>

        <div className="mt-4 text-ash">中国大陆</div>
      </div>
    </footer>
  );
}
