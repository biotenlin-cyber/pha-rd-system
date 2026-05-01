export type Product = {
  id: string;
  name: string;
  model: string;
  category: "薄膜级" | "注塑级" | "纤维级" | "改性级";
  description: string;
  features: string[];
  applications: string[];
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
