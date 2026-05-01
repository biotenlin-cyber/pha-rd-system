import type { SpecGroup } from "@/data/products";

type Props = {
  groups: SpecGroup[];
};

// Apple style:细 hairline 分隔的 label / value 对照
export function SpecTable({ groups }: Props) {
  return (
    <div className="space-y-12">
      {groups.map((group) => (
        <section key={group.section}>
          <h3 className="text-[18px] sm:text-xl font-semibold tracking-tight text-ink border-b border-hairline pb-3">
            {group.section}
          </h3>
          <dl>
            {group.items.map((item) => (
              <div
                key={item.label}
                className="grid grid-cols-1 sm:grid-cols-12 gap-2 sm:gap-6 py-4 border-b border-hairline/70"
              >
                <dt className="sm:col-span-4 text-[15px] text-ink font-medium">
                  {item.label}
                </dt>
                <dd className="sm:col-span-8 text-[15px] text-ash leading-relaxed">
                  {item.value}
                </dd>
              </div>
            ))}
          </dl>
        </section>
      ))}
    </div>
  );
}
