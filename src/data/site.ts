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

// Apple footer "Shop and Learn" 风格的多列站点地图
export const footerNav: { title: string; items: NavItem[] }[] = [
  {
    title: "选购 PHA 产品",
    items: [
      { label: "薄膜级 DBC-F100", href: "/products/dbc-f100" },
      { label: "注塑级 DBC-I200", href: "/products/dbc-i200" },
      { label: "纤维级 DBC-X300", href: "/products/dbc-x300" },
      { label: "改性级 DBC-M400", href: "/products/dbc-m400" },
      { label: "3D 打印线材 DBC-3D10", href: "/products/dbc-3d10" },
      { label: "全部产品", href: "/products" },
    ],
  },
  {
    title: "应用场景",
    items: [
      { label: "包装", href: "/products#applications" },
      { label: "医疗", href: "/products#applications" },
      { label: "农业", href: "/products#applications" },
      { label: "3D 打印 / 消费品", href: "/products#applications" },
    ],
  },
  {
    title: "都佰城 PHA-RD 平台",
    items: [
      { label: "平台总览", href: "/platform" },
      { label: "材料研发管理", href: "/platform#material" },
      { label: "产品开发管理", href: "/platform#product" },
      { label: "知识产权管理", href: "/platform#patent" },
      { label: "数据分析与协作", href: "/platform#analytics" },
      { label: "预约演示", href: "/contact" },
    ],
  },
  {
    title: "关于都佰城",
    items: [
      { label: "公司简介", href: "/about" },
      { label: "发展历程", href: "/about#milestones" },
      { label: "资质认证", href: "/about#certifications" },
      { label: "Newsroom", href: "/news" },
      { label: "投资者关系", href: "#" },
    ],
  },
  {
    title: "支持与合作",
    items: [
      { label: "样品申请", href: "/contact" },
      { label: "技术合作", href: "/contact" },
      { label: "媒体联络", href: "/contact" },
      { label: "招贤纳士", href: "#" },
      { label: "供应商门户", href: "#" },
    ],
  },
];
