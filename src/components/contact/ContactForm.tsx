"use client";

import { useState } from "react";
import { CheckCircle2 } from "lucide-react";

type FormState = {
  name: string;
  company: string;
  email: string;
  phone: string;
  topic: string;
  message: string;
};

const initial: FormState = {
  name: "",
  company: "",
  email: "",
  phone: "",
  topic: "产品咨询",
  message: "",
};

export function ContactForm() {
  const [form, setForm] = useState<FormState>(initial);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const update =
    <K extends keyof FormState>(key: K) =>
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
      setForm((prev) => ({ ...prev, [key]: e.target.value }));
    };

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!form.name.trim() || !form.email.trim() || !form.message.trim()) {
      setError("请填写姓名、邮箱和留言内容。");
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      setError("邮箱格式不正确。");
      return;
    }
    console.info("[ContactForm] submission", form);
    setSubmitted(true);
    setForm(initial);
  };

  if (submitted) {
    return (
      <div className="rounded-marble bg-fog p-12 text-center">
        <div className="mx-auto h-12 w-12 grid place-items-center rounded-full bg-ink text-white">
          <CheckCircle2 size={22} strokeWidth={1.6} />
        </div>
        <h3 className="mt-5 text-2xl font-semibold tracking-tight">
          已收到您的留言。
        </h3>
        <p className="mt-3 text-base text-ash leading-relaxed max-w-md mx-auto">
          感谢您对都佰城的关注。我们的商务团队将在 1—2 个工作日内与您取得联系。
        </p>
        <button
          type="button"
          onClick={() => setSubmitted(false)}
          className="mt-6 link-arrow text-sm"
        >
          再发一条留言
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="space-y-5" noValidate>
      <div className="grid gap-5 sm:grid-cols-2">
        <Field label="姓名" required>
          <input
            type="text"
            value={form.name}
            onChange={update("name")}
            className={inputClass}
            placeholder="您的姓名"
            required
          />
        </Field>
        <Field label="公司">
          <input
            type="text"
            value={form.company}
            onChange={update("company")}
            className={inputClass}
            placeholder="所在公司或机构"
          />
        </Field>
        <Field label="邮箱" required>
          <input
            type="email"
            value={form.email}
            onChange={update("email")}
            className={inputClass}
            placeholder="name@company.com"
            required
          />
        </Field>
        <Field label="电话">
          <input
            type="tel"
            value={form.phone}
            onChange={update("phone")}
            className={inputClass}
            placeholder="(可选)"
          />
        </Field>
      </div>

      <Field label="咨询主题">
        <select value={form.topic} onChange={update("topic")} className={inputClass}>
          <option>产品咨询</option>
          <option>研发平台演示</option>
          <option>样品申请</option>
          <option>技术合作</option>
          <option>媒体联络</option>
          <option>其他</option>
        </select>
      </Field>

      <Field label="留言" required>
        <textarea
          value={form.message}
          onChange={update("message")}
          rows={5}
          className={`${inputClass} resize-y`}
          placeholder="请简要描述您的需求,以便我们更高效地与您沟通。"
          required
        />
      </Field>

      {error && (
        <p className="text-sm text-red-600" role="alert">
          {error}
        </p>
      )}

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pt-3">
        <p className="text-xs text-smoke">
          您提交的信息将仅用于业务联系,我们承诺不会用于其他用途。
        </p>
        <button
          type="submit"
          className="inline-flex items-center justify-center h-11 px-7 rounded-full bg-link text-white text-sm font-medium hover:bg-linkHover transition"
        >
          提交
        </button>
      </div>
    </form>
  );
}

const inputClass =
  "w-full rounded-2xl border border-hairline bg-paper px-4 py-3 text-base text-ink placeholder:text-smoke focus:outline-none focus:border-link focus:ring-4 focus:ring-link/15 transition";

function Field({
  label,
  required,
  children,
}: {
  label: string;
  required?: boolean;
  children: React.ReactNode;
}) {
  return (
    <label className="block">
      <span className="block text-sm font-medium text-ink mb-2">
        {label}
        {required && <span className="text-link ml-0.5">*</span>}
      </span>
      {children}
    </label>
  );
}
