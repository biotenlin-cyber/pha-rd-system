export const siteConfig = {
  name: "都佰城",
  fullName: "都佰城新材料科技有限公司",
  tagline: "以 PHA 重塑可持续未来",
  description:
    "都佰城专注于聚羟基脂肪酸酯(PHA)生物可降解材料的研发、生产与应用,助力包装、医疗、农业、3D 打印等行业实现绿色转型。",
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
  { label: "首页", href: "/" },
  { label: "关于我们", href: "/about" },
  { label: "产品与技术", href: "/products" },
  { label: "新闻资讯", href: "/news" },
  { label: "联系我们", href: "/contact" },
];
