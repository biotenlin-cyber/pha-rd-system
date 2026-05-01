import { Reveal } from "./Reveal";

type Props = {
  title: React.ReactNode;
  items: string[];
};

// Apple "Take a closer look" 段:大标题 + 三段细分点
export function CloserLook({ title, items }: Props) {
  return (
    <section className="bg-paper">
      <div className="mx-auto max-w-4xl px-6 sm:px-8 py-24 sm:py-32 text-center">
        <div className="text-eyebrow text-ink mb-4">A CLOSER LOOK</div>
        <Reveal>
          <h2 className="text-display sm:text-hero font-semibold tracking-tight">
            {title}
          </h2>
        </Reveal>
        <ul className="mt-12 grid gap-8 sm:grid-cols-3 text-left">
          {items.map((it, i) => (
            <Reveal key={i} delay={i * 80}>
              <li className="text-[16px] leading-[1.6] text-ash border-t border-hairline pt-5">
                <span className="text-eyebrow text-ink mb-2 block">
                  {String(i + 1).padStart(2, "0")}
                </span>
                {it}
              </li>
            </Reveal>
          ))}
        </ul>
      </div>
    </section>
  );
}
