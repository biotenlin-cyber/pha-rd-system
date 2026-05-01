export type PlatformModule = {
  id: string;
  badge: string;
  title: string;
  subtitle: string;
  description: string;
  capabilities: string[];
};

export const platformOverview = {
  eyebrow: "都佰城研发管理平台",
  title: "一个系统,掌管整个 PHA 研发链。",
  subtitle:
    "从菌种到分子,从配方到专利,从客户样品到批次追溯。都佰城自研的研发管理平台 (PHA-RD) 把材料研发、产品开发与知识产权,装进同一个工作流。",
  stats: [
    { label: "实验记录", value: "12 万+" },
    { label: "在研产品线", value: "32" },
    { label: "管理专利", value: "120+" },
    { label: "协同部门", value: "9" },
  ],
};

export const platformModules: PlatformModule[] = [
  {
    id: "material",
    badge: "Material R&D",
    title: "材料研发管理",
    subtitle: "把每一次实验,变成可检索的知识。",
    description:
      "从菌种文库、发酵参数到改性配方,系统记录每一次实验设计与结果。研发人员可基于结构化字段快速检索历史数据、复用配方、对比批次性能。",
    capabilities: [
      "菌种 / 配方 / 工艺 三维数据模型",
      "实验设计 (DoE) 模板与执行追踪",
      "性能指标自动比对与可视化",
      "批次与原料的全流程溯源",
    ],
  },
  {
    id: "product",
    badge: "Product Pipeline",
    title: "产品开发管理",
    subtitle: "让产品从立项,走到客户的产线。",
    description:
      "围绕客户项目构建端到端管线:从牌号选型、样品试制、客户验证到量产交付。每个节点的责任人、文档与里程碑均可追溯。",
    capabilities: [
      "项目立项与阶段门禁 (Stage-Gate)",
      "样品申请、寄送与反馈闭环",
      "客户测试报告归档",
      "量产 BOM 与工艺包冻结",
    ],
  },
  {
    id: "patent",
    badge: "IP Management",
    title: "知识产权管理",
    subtitle: "把研发成果,牢牢握在手里。",
    description:
      "覆盖技术交底、专利申请、年费维护、海外布局与诉讼应对。系统与研发数据打通,自动从实验记录生成技术交底初稿。",
    capabilities: [
      "技术交底与发明人清单管理",
      "申请进度、年费与状态可视化",
      "PCT / 海外布局多区域跟踪",
      "FTO 检索结果归档与提醒",
    ],
  },
  {
    id: "analytics",
    badge: "Analytics & Collab",
    title: "数据分析与协作",
    subtitle: "决策,从一张共享的看板开始。",
    description:
      "面向研发总监、项目经理与一线工程师的多角色看板,实时呈现项目进展、专利存量、产能利用率等关键指标。支持权限分级的跨部门协作。",
    capabilities: [
      "多角色 BI 看板",
      "项目进展周报自动生成",
      "细粒度权限与外部访客通道",
      "API 与企业微信 / 邮件集成",
    ],
  },
];

export const platformWorkflow = [
  { step: "01", title: "需求洞察", desc: "市场与客户需求录入,转化为研发课题。" },
  { step: "02", title: "实验研发", desc: "结构化记录实验,自动比对性能数据。" },
  { step: "03", title: "样品验证", desc: "向客户寄送样品,闭环收集测试反馈。" },
  { step: "04", title: "知识沉淀", desc: "实验数据 → 技术交底 → 专利申请。" },
  { step: "05", title: "量产交付", desc: "工艺包冻结,进入万吨级工厂量产。" },
];

export const platformDeployment = [
  {
    title: "私有化部署",
    desc: "面向核心研发数据,提供独立私有云或本地化部署方案,内网隔离。",
  },
  {
    title: "国密合规",
    desc: "支持国密算法、等保 2.0 三级要求,满足关键数据合规审计。",
  },
  {
    title: "持续演进",
    desc: "平台由都佰城研发团队持续迭代,新模块按季度发布。",
  },
];
