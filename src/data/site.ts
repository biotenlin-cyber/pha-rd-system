export const siteConfig = {
  name: "都佰城",
  fullName: "都佰城新材料科技有限公司",
  tagline: "重塑塑料的未来",
  description:
    "都佰城专注于聚羟基脂肪酸酯(PHA)生物可降解材料的研发、生产与应用,并自主构建了 PHA 研发管理平台,助力包装、医疗、农业、3D 打印等行业实现绿色转型。",
  contact: {
    address: "上海市浦东新区张江高科技园区科苑路 88 号",
    phone: "+86 21 5888-0000",
    email: "contact@dubaicheng.com",
    workingHours: "周一至周五 09:00 — 18:00",
  },
  social: {
    weibo: "#",
    linkedin: "#",
    wechat: "dubaicheng_official",
  },
} as const;

export type NavItem = {
  label: string;
  href: string;
};

export const mainNav: NavItem[] = [
  { label: "产品", href: "/products" },
  { label: "平台", href: "/platform" },
  { label: "关于", href: "/about" },
  { label: "资讯", href: "/news" },
  { label: "联系", href: "/contact" },
];

export const footerNav: { title: string; items: NavItem[] }[] = [
  {
    title: "产品与技术",
    items: [
      { label: "PHA 产品矩阵", href: "/products" },
      { label: "薄膜级", href: "/products#film" },
      { label: "注塑级", href: "/products#injection" },
      { label: "纤维 / 改性级", href: "/products#advanced" },
    ],
  },
  {
    title: "都佰城研发平台",
    items: [
      { label: "平台总览", href: "/platform" },
      { label: "材料研发管理", href: "/platform#material" },
      { label: "产品开发管理", href: "/platform#product" },
      { label: "知识产权管理", href: "/platform#patent" },
    ],
  },
  {
    title: "关于都佰城",
    items: [
      { label: "公司简介", href: "/about" },
      { label: "发展历程", href: "/about#milestones" },
      { label: "资质认证", href: "/about#certifications" },
      { label: "新闻资讯", href: "/news" },
    ],
  },
  {
    title: "支持",
    items: [
      { label: "联系我们", href: "/contact" },
      { label: "样品申请", href: "/contact" },
      { label: "技术合作", href: "/contact" },
      { label: "媒体联络", href: "/contact" },
    ],
  },
];
