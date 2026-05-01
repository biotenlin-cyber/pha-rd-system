"use client";

import { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

type Props = {
  children: React.ReactNode;
  delay?: number;
  className?: string;
  as?: "div" | "section" | "article" | "li" | "header";
  id?: string;
  /** translateY 起始位移 (px) */
  offset?: number;
  /** 仅触发一次,默认 true */
  once?: boolean;
};

export function Reveal({
  children,
  delay = 0,
  className,
  as: Tag = "div",
  id,
  offset = 24,
  once = true,
}: Props) {
  const ref = useRef<HTMLElement>(null);
  const [shown, setShown] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    if (typeof IntersectionObserver === "undefined") {
      setShown(true);
      return;
    }
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setShown(true);
            if (once) observer.unobserve(entry.target);
          } else if (!once) {
            setShown(false);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" },
    );
    observer.observe(node);
    return () => observer.disconnect();
  }, [once]);

  const style: React.CSSProperties = {
    opacity: shown ? 1 : 0,
    transform: shown ? "translateY(0)" : `translateY(${offset}px)`,
    transition: `opacity 800ms cubic-bezier(0.22, 1, 0.36, 1) ${delay}ms, transform 800ms cubic-bezier(0.22, 1, 0.36, 1) ${delay}ms`,
    willChange: "opacity, transform",
  };

  // 多态标签 ref 类型在 TS 下较难精确表达,使用 any 桥接
  const TagAny = Tag as React.ElementType;
  return (
    <TagAny
      ref={ref}
      id={id}
      className={cn(className)}
      style={style}
    >
      {children}
    </TagAny>
  );
}
