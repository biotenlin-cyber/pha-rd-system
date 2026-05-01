export type ProductTone = "blue" | "graphite" | "pearl" | "midnight" | "champagne";
export type ProductShape = "pellet" | "film" | "fiber";

export type SpecGroup = {
  section: string;
  items: { label: string; value: string }[];
};

export type Pillar = { value: string; label: string };

export type Product = {
  id: string;
  name: string;
  model: string;
  category: "薄膜级" | "注塑级" | "纤维级" | "改性级";
  description: string;
  features: string[];
  applications: string[];

  // 详情页扩展
  tagline: string; // hero 主标题:句号,大字
  pageSubtitle: string; // hero 副标题
  pillars: Pillar[]; // 4 张大数据卡
  closerLook: string[]; // "Take a closer look" 段
  tone: ProductTone;
  shape: ProductShape;
  specs: SpecGroup[];
};

export const products: Product[] = [
  {
    id: "dbc-f100",
    name: "高韧性薄膜料",
    model: "DBC-F100",
    category: "薄膜级",
    description:
      "面向购物袋、垃圾袋、食品包装的高韧性 PHA 薄膜原料,具备优异的撕裂强度与可堆肥降解性能。",
    features: ["拉伸强度 ≥ 25 MPa", "断裂伸长率 ≥ 400%", "EN13432 认证", "海洋环境可降解"],
    applications: ["一次性购物袋", "食品级保鲜袋", "农用地膜"],
    tagline: "高韧性。可堆肥。",
    pageSubtitle:
      "为薄膜而生的 PHA 原料,撕裂强度与延展性同时在线,工业堆肥 90 天降解。",
    pillars: [
      { value: "≥25", label: "MPa 拉伸强度" },
      { value: "≥400%", label: "断裂伸长率" },
      { value: "EN13432", label: "工业堆肥认证" },
      { value: "海洋", label: "环境可降解" },
    ],
    closerLook: [
      "自主菌种发酵的高纯 PHA 主链,不依赖石化共聚单体。",
      "改性配方在保留高韧性的同时,提升加工窗口和制袋速度。",
      "在工业堆肥与海洋环境中,可被微生物完全降解为水与二氧化碳。",
    ],
    tone: "pearl",
    shape: "film",
    specs: [
      {
        section: "物理性能",
        items: [
          { label: "外观", value: "乳白色圆柱粒子" },
          { label: "密度", value: "1.24 g/cm³" },
          { label: "熔体流动指数", value: "2.0 — 4.0 g/10min (190°C / 2.16 kg)" },
        ],
      },
      {
        section: "热性能",
        items: [
          { label: "熔点", value: "约 165°C" },
          { label: "玻璃化转变温度", value: "−5°C" },
          { label: "推荐加工温度", value: "150 — 175°C" },
        ],
      },
      {
        section: "机械性能",
        items: [
          { label: "拉伸强度", value: "≥ 25 MPa" },
          { label: "断裂伸长率", value: "≥ 400%" },
          { label: "撕裂强度 (Elmendorf)", value: "≥ 60 g" },
        ],
      },
      {
        section: "降解性能",
        items: [
          { label: "工业堆肥降解", value: "90 天 (EN13432)" },
          { label: "海洋降解", value: "180 — 360 天 (ASTM D6691)" },
          { label: "土壤降解", value: "180 — 360 天" },
        ],
      },
      {
        section: "认证与合规",
        items: [
          { label: "可降解认证", value: "EU EN13432 / US BPI / OK Compost" },
          { label: "食品接触合规", value: "FDA 21 CFR / EU 10/2011" },
          { label: "重金属", value: "符合 RoHS 限值" },
        ],
      },
      {
        section: "包装与运输",
        items: [
          { label: "标准包装", value: "25 kg 内衬铝箔袋 / 牛皮纸外袋" },
          { label: "吨包", value: "500 / 1000 kg 集装袋" },
          { label: "储存", value: "干燥阴凉,远离阳光直射" },
        ],
      },
    ],
  },
  {
    id: "dbc-i200",
    name: "通用注塑料",
    model: "DBC-I200",
    category: "注塑级",
    description:
      "高流动性 PHA 注塑级牌号,适用于餐具、包装容器及消费电子配件,兼顾刚性与韧性。",
    features: ["熔指 12—18 g/10min", "热变形温度 ≥ 110℃", "可食品接触", "可工业堆肥降解"],
    applications: ["可降解餐具", "化妆品瓶盖", "电子产品配件"],
    tagline: "通用。耐热。可降解。",
    pageSubtitle:
      "高流动性 PHA 注塑原料,适配既有注塑机型,无需改造模具即可投产。",
    pillars: [
      { value: "12—18", label: "g/10min 熔指" },
      { value: "≥110°C", label: "热变形温度" },
      { value: "FDA", label: "食品接触合规" },
      { value: "EN13432", label: "工业堆肥认证" },
    ],
    closerLook: [
      "高熔指设计兼顾薄壁制品的填充与冷却效率。",
      "成型周期接近常规聚烯烃,降低产线切换成本。",
      "适配主流注塑机与热流道系统,无需更换设备。",
    ],
    tone: "blue",
    shape: "pellet",
    specs: [
      {
        section: "物理性能",
        items: [
          { label: "外观", value: "象牙白圆柱粒子" },
          { label: "密度", value: "1.25 g/cm³" },
          { label: "熔体流动指数", value: "12 — 18 g/10min (190°C / 2.16 kg)" },
        ],
      },
      {
        section: "热性能",
        items: [
          { label: "熔点", value: "约 168°C" },
          { label: "热变形温度 (HDT)", value: "≥ 110°C @ 0.45 MPa" },
          { label: "推荐成型温度", value: "165 — 185°C" },
        ],
      },
      {
        section: "机械性能",
        items: [
          { label: "拉伸强度", value: "≥ 30 MPa" },
          { label: "弯曲强度", value: "≥ 45 MPa" },
          { label: "缺口冲击", value: "≥ 5 kJ/m²" },
        ],
      },
      {
        section: "降解性能",
        items: [
          { label: "工业堆肥降解", value: "120 天 (EN13432)" },
          { label: "海洋降解", value: "12 — 18 个月" },
        ],
      },
      {
        section: "认证与合规",
        items: [
          { label: "可降解认证", value: "EN13432 / BPI" },
          { label: "食品接触合规", value: "FDA 21 CFR / GB 4806" },
        ],
      },
    ],
  },
  {
    id: "dbc-x300",
    name: "纤维专用料",
    model: "DBC-X300",
    category: "纤维级",
    description:
      "为纺粘 / 熔喷工艺定制的 PHA 纤维原料,可制成无纺布、医用敷料与卫生材料。",
    features: ["纤度 ≤ 2.0 dtex", "高纺丝稳定性", "皮肤亲和性佳", "可生理降解"],
    applications: ["医用敷料", "婴儿尿片", "高端无纺布"],
    tagline: "亲肤。稳定。可生理降解。",
    pageSubtitle: "为纺粘和熔喷工艺定制,适配现有纤维产线,无需更换喷丝板。",
    pillars: [
      { value: "≤2.0", label: "dtex 纤度" },
      { value: "高", label: "纺丝稳定性" },
      { value: "亲肤", label: "皮肤接触友好" },
      { value: "生理", label: "可降解环境" },
    ],
    closerLook: [
      "针对熔喷工艺优化的窄分子量分布,纺丝断丝率显著降低。",
      "纤维表面光滑、吸水性可调,适合医卫与擦拭场景。",
      "与人体生理环境兼容,无重金属、无残留单体。",
    ],
    tone: "graphite",
    shape: "fiber",
    specs: [
      {
        section: "物理性能",
        items: [
          { label: "外观", value: "白色圆柱粒子" },
          { label: "密度", value: "1.23 g/cm³" },
          { label: "熔体流动指数", value: "25 — 35 g/10min" },
        ],
      },
      {
        section: "纤维性能",
        items: [
          { label: "可达纤度", value: "≤ 2.0 dtex" },
          { label: "纺丝速度", value: "1500 — 2500 m/min" },
        ],
      },
      {
        section: "降解性能",
        items: [
          { label: "工业堆肥降解", value: "60 — 90 天" },
          { label: "生理可降解", value: "适用于体内吸收类研究" },
        ],
      },
    ],
  },
  {
    id: "dbc-m400",
    name: "高耐热改性料",
    model: "DBC-M400",
    category: "改性级",
    description:
      "通过共混改性提升耐热性与加工窗口,适合需要短时高温的耐热制品场景。",
    features: ["热变形温度 ≥ 130℃", "高刚性", "良好加工窗口", "可堆肥降解"],
    applications: ["热饮杯盖", "微波餐具", "户外一次性容器"],
    tagline: "为高温场景而生。",
    pageSubtitle:
      "热变形温度突破 130°C,把可降解材料推向热饮、微波与户外场景。",
    pillars: [
      { value: "≥130°C", label: "热变形温度" },
      { value: "高", label: "刚性" },
      { value: "宽", label: "加工窗口" },
      { value: "EN13432", label: "可降解认证" },
    ],
    closerLook: [
      "通过定制晶核改性,显著提升耐热温度而不牺牲降解性。",
      "兼容常规热成型与注塑工艺,降低切换成本。",
      "适用于热饮杯盖、微波餐具、户外一次性容器等场景。",
    ],
    tone: "midnight",
    shape: "pellet",
    specs: [
      {
        section: "物理性能",
        items: [
          { label: "密度", value: "1.27 g/cm³" },
          { label: "熔体流动指数", value: "8 — 12 g/10min" },
        ],
      },
      {
        section: "热性能",
        items: [
          { label: "热变形温度", value: "≥ 130°C @ 0.45 MPa" },
          { label: "维卡软化点", value: "≥ 140°C" },
        ],
      },
      {
        section: "机械性能",
        items: [
          { label: "拉伸强度", value: "≥ 35 MPa" },
          { label: "弯曲模量", value: "≥ 2,800 MPa" },
        ],
      },
    ],
  },
  {
    id: "dbc-3d10",
    name: "3D 打印线材",
    model: "DBC-3D10",
    category: "改性级",
    description:
      "面向 FDM 3D 打印的 PHA 改性线材,打印翘曲率低,层间结合强,绿色无异味。",
    features: ["1.75mm / 2.85mm 线径", "翘曲率低", "可生物降解", "无 VOC 释放"],
    applications: ["创客教育", "工业原型", "可降解模型"],
    tagline: "可降解的 3D 打印,从这里开始。",
    pageSubtitle:
      "为 FDM 3D 打印优化的 PHA 改性线材,翘曲率低、无 VOC、绿色无异味。",
    pillars: [
      { value: "1.75 / 2.85", label: "mm 线径" },
      { value: "极低", label: "翘曲率" },
      { value: "0", label: "VOC 释放" },
      { value: "可降解", label: "环境亲和" },
    ],
    closerLook: [
      "针对 FDM 工艺优化的结晶速率,显著降低翘曲与开裂。",
      "层间结合强度高,打印件可直接用于功能原型。",
      "无 VOC、低气味,适合教育、办公等室内场景。",
    ],
    tone: "blue",
    shape: "fiber",
    specs: [
      {
        section: "线材规格",
        items: [
          { label: "线径", value: "1.75 mm / 2.85 mm" },
          { label: "卷重", value: "0.75 kg / 1.0 kg" },
          { label: "公差", value: "±0.03 mm" },
        ],
      },
      {
        section: "打印参数",
        items: [
          { label: "推荐喷头温度", value: "200 — 220°C" },
          { label: "推荐热床温度", value: "40 — 60°C" },
          { label: "推荐打印速度", value: "30 — 60 mm/s" },
        ],
      },
    ],
  },
  {
    id: "dbc-c500",
    name: "高纯医用级",
    model: "DBC-C500",
    category: "改性级",
    description:
      "符合医用级品控要求的高纯度 PHA 原料,可用于可吸收缝合线、药物缓释载体研究。",
    features: ["重金属低于检测限", "细胞毒性 0 级", "可生理降解", "GMP 级生产环境"],
    applications: ["可吸收缝合线", "组织工程支架", "药物缓释"],
    tagline: "为医疗,设计的纯度。",
    pageSubtitle:
      "GMP 级生产环境下的高纯 PHA,适用于可吸收缝合线、组织工程与药物缓释研究。",
    pillars: [
      { value: "GMP", label: "级生产环境" },
      { value: "0 级", label: "细胞毒性" },
      { value: "<LOD", label: "重金属残留" },
      { value: "生理", label: "可降解" },
    ],
    closerLook: [
      "在 GMP 级洁净厂房中独立生产,与工业级线路完全隔离。",
      "重金属与残留溶剂控制在检测限以下,符合医用原料要求。",
      "已与多家医疗机构开展可吸收缝合线、药物缓释载体合作研究。",
    ],
    tone: "pearl",
    shape: "pellet",
    specs: [
      {
        section: "纯度",
        items: [
          { label: "重金属总量", value: "< 检测限 (LOD)" },
          { label: "残留溶剂", value: "符合 ICH Q3C" },
          { label: "细菌内毒素", value: "符合 USP 标准" },
        ],
      },
      {
        section: "生物学性能",
        items: [
          { label: "细胞毒性", value: "0 级 (ISO 10993-5)" },
          { label: "致敏性", value: "无 (ISO 10993-10)" },
        ],
      },
    ],
  },
  {
    id: "dbc-a600",
    name: "农业地膜专用",
    model: "DBC-A600",
    category: "薄膜级",
    description:
      "针对地膜场景优化的 PHA 牌号,具备良好的耐候性与土壤可控降解周期。",
    features: ["可控降解 90—180 天", "耐候性优异", "无残留塑料颗粒", "兼容现有铺膜设备"],
    applications: ["大田农膜", "果蔬覆盖膜", "苗圃育苗"],
    tagline: "可降解的地膜。无微塑料残留。",
    pageSubtitle:
      "针对农业场景定制的 PHA 牌号,90 — 180 天可控降解,降解后无微塑料残留。",
    pillars: [
      { value: "90—180", label: "天可控降解" },
      { value: "0", label: "微塑料残留" },
      { value: "兼容", label: "现有铺膜设备" },
      { value: "高", label: "耐候性" },
    ],
    closerLook: [
      "通过菌种与改性配方,可实现 90 — 180 天的可调降解周期。",
      "降解后产物为水与二氧化碳,土壤中无任何微塑料颗粒残留。",
      "与现有铺膜设备完全兼容,无需更换农机。",
    ],
    tone: "champagne",
    shape: "film",
    specs: [
      {
        section: "薄膜性能",
        items: [
          { label: "厚度", value: "8 — 15 μm" },
          { label: "拉伸强度", value: "≥ 22 MPa" },
        ],
      },
      {
        section: "降解性能",
        items: [
          { label: "土壤可控降解", value: "90 — 180 天 (可调)" },
          { label: "降解产物", value: "H₂O + CO₂,无微塑料残留" },
        ],
      },
    ],
  },
  {
    id: "dbc-p700",
    name: "高阻隔包装料",
    model: "DBC-P700",
    category: "薄膜级",
    description:
      "通过多层共挤改性提升阻氧、阻水性能,延长食品保鲜期。",
    features: ["氧气透过率低", "可热封", "印刷亲和性佳", "工业堆肥可降解"],
    applications: ["真空食品包装", "高端礼盒内衬", "鲜食外卖"],
    tagline: "高阻隔,延长每一份新鲜。",
    pageSubtitle:
      "多层共挤优化的 PHA 包装料,在保持可降解性的同时,大幅降低氧气透过率。",
    pillars: [
      { value: "极低", label: "氧气透过率" },
      { value: "可热封", label: "包装效率高" },
      { value: "印刷友好", label: "品牌可识别" },
      { value: "可降解", label: "工业堆肥" },
    ],
    closerLook: [
      "通过多层共挤工艺,在 PHA 主基材外覆盖阻隔功能层。",
      "热封性能优异,适配主流包装机,无需特殊改造。",
      "印刷亲和性好,可承载品牌包装的复杂图文。",
    ],
    tone: "graphite",
    shape: "film",
    specs: [
      {
        section: "阻隔性能",
        items: [
          { label: "氧气透过率 (OTR)", value: "< 5 cc/m²·day" },
          { label: "水蒸气透过率 (WVTR)", value: "< 8 g/m²·day" },
        ],
      },
      {
        section: "加工性能",
        items: [
          { label: "热封温度", value: "100 — 120°C" },
          { label: "印刷适应", value: "凹印 / 柔印 / 数字印刷" },
        ],
      },
    ],
  },
];

export const techAdvantages = [
  {
    title: "自主菌种平台",
    desc: "高产、稳定的工业级 PHA 菌种文库,发酵效率领先行业平均水平 30%。",
  },
  {
    title: "全链路工艺",
    desc: "从底盘菌种到下游提取与改性,全部自主开发,质量端到端可控。",
  },
  {
    title: "万吨级量产",
    desc: "万吨级智能化工厂稳定供货,DCS 控制 + 在线 QC,批次一致性 ≥ 99%。",
  },
  {
    title: "全球认证体系",
    desc: "通过 EN13432、BPI、OK Compost、海洋降解等多项国际认证。",
  },
];

export const applications = [
  {
    title: "包装",
    desc: "购物袋、食品包装、电商缓冲材料,从源头减少一次性塑料污染。",
    icon: "Package",
  },
  {
    title: "医疗",
    desc: "可吸收缝合线、医用敷料与组织工程支架,与人体生理环境友好兼容。",
    icon: "HeartPulse",
  },
  {
    title: "农业",
    desc: "可降解地膜与苗圃用品,降解后无微塑料残留,改善土壤生态。",
    icon: "Sprout",
  },
  {
    title: "3D 打印 & 消费品",
    desc: "PHA 线材与改性料赋能教育、工业原型与高端消费品制造。",
    icon: "Boxes",
  },
];
