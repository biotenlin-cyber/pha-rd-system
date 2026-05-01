# pha-rd-system

PHA 材料研发及产品开发与专利管理系统

---

## 都佰城企业品牌官网

本仓库当前承载 **都佰城新材料科技有限公司** 企业品牌官网,基于 Next.js (App Router) + TypeScript + Tailwind CSS 构建,定位为对外展示 PHA 生物可降解材料业务的官方门户。

### 技术栈

- **框架**:Next.js 15(App Router,React 19)
- **语言**:TypeScript
- **样式**:Tailwind CSS v3 + 自定义科技蓝主题
- **图标**:lucide-react
- **包管理**:npm

### 页面结构

| 路径 | 说明 |
| --- | --- |
| `/` | 首页(Hero、亮点、产品预览、公司简介、最新资讯、CTA) |
| `/about` | 关于我们(简介、愿景使命、发展历程、资质) |
| `/products` | 产品与技术(PHA 介绍、产品矩阵、技术优势、应用场景) |
| `/news` | 新闻列表 |
| `/news/[slug]` | 新闻详情(基于 `src/data/news.ts` 静态生成) |
| `/contact` | 联系我们(联系方式、表单、地图占位) |

### 目录结构

```
src/
├── app/                  # 路由入口(layout / 各页面)
├── components/
│   ├── layout/           # Header / Footer
│   ├── home/             # 首页各区块
│   ├── products/         # 产品卡片
│   ├── contact/          # 联系表单(Client Component)
│   ├── ui/               # 通用基础组件(Container / Section / Button)
│   └── PageHero.tsx      # 内页通用 Hero
├── data/                 # 站点 / 公司 / 产品 / 新闻数据
└── lib/                  # 工具函数
```

### 本地开发

```bash
# 1. 安装依赖
npm install

# 2. 启动开发服务器(默认 http://localhost:3000)
npm run dev

# 3. 生产构建
npm run build

# 4. 启动生产服务器
npm run start

# 5. Lint
npm run lint
```

### 内容维护

- 公司介绍、愿景、历程、资质 → `src/data/company.ts`
- 产品矩阵、技术优势、应用场景 → `src/data/products.ts`
- 新闻列表与正文 → `src/data/news.ts`
- 站点全局信息(站名、导航、联系方式) → `src/data/site.ts`

如需替换占位的图片或对接真实 CMS,可在 `src/data` 中将常量替换为 fetch 调用,或迁移至 Headless CMS。

### 设计系统

- 主色 `brand-900` `#0B3D91`,辅以亮蓝 `accent-500` `#1E90FF` / `accent-400` `#38BDF8`
- 中文字体栈优先使用系统苹方/微软雅黑,英文与数字使用 Inter
- Hero 与 CTA 使用 `bg-tech-radial` 蓝色径向渐变 + 网格纹路
- 卡片统一圆角 `rounded-2xl` + `hover:shadow-soft` 浅阴影

### 后续扩展建议

- 接入真实图片资源(产品图、团队照片、办公环境)替换 SVG 占位
- 联系表单接入邮件服务(Resend、SendGrid)或表单收集 SaaS
- 增加多语言 i18n(英文站)
- 增加 `sitemap.xml` / `robots.txt` 与结构化数据(JSON-LD)
- 接入 CMS(Sanity / Strapi)管理新闻与产品
