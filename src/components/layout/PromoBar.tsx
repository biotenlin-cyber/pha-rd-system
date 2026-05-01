import Link from "next/link";

export function PromoBar() {
  return (
    <div className="fixed top-0 inset-x-0 z-[60] h-9 bg-fog text-ink/85 text-[12px] flex items-center justify-center px-4 border-b border-hairline">
      <p className="truncate">
        都佰城 PHA-RD 平台现已开放预约演示。
        <Link href="/platform" className="ml-2 text-link hover:text-linkHover">
          走进平台 ›
        </Link>
      </p>
    </div>
  );
}
