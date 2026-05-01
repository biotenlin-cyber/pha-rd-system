# pha-rd-system

PHA 材料研发及产品开发与专利管理系统

---

## 都佰城品牌官网 + 研发平台介绍站

本仓库承载都佰城新材料的对外品牌门户与 PHA 研发管理平台 (PHA-RD) 的产品介绍页。整站采用 **Apple 官网风格** 的视觉系统:极简黑白基底、巨型 SF Pro 风格字体、Tile 块组合、标志性 "Learn more →" 链接 CTA 与多列法律 Footer。

### 技术栈

- **框架**:Next.js 15 (App Router, React 19, RSC 优先)
- **语言**:TypeScript
- **样式**:Tailwind CSS v3,Apple 设计 Token (`ink` / `paper` / `fog` / `smoke` / `link`)
- **图标**:lucide-react
- **视觉**:全部产品图采用 SVG 渐变抽象绘制(可后续替换为真实摄影 / 3D 渲染)

### 路由总览

| 路径 | 模块 | 说明 |
| --- | --- | --- |
| `/` | 首页 | 5 段 Tile:PHA 主张 / PHA-RD 平台 / 产品双联 / 应用双联 / 资讯双联 |
| `/products` | 产品 | 按薄膜/注塑/纤维/改性 4 大类分组的产品矩阵 |
| `/platform` | **PHA-RD 平台** | 4 大模块、流水线、部署模式与合规 |
| `/about` | 关于 | 公司故事、数据、价值观、时间线、资质 |
| `/news` | Newsroom | 头条 + 网格列表 |
| `/news/[slug]` | 新闻详情 | 编辑级长文版式 |
| `/contact` | 联系 | 渠道卡片 + 留言表单 + 资源指引 |

### 目录结构

```
src/
├── app/                       # Next.js App Router 入口
│   ├── layout.tsx
│   ├── page.tsx               # 首页 Tile 组合
│   ├── about/page.tsx
│   ├── platform/page.tsx      # 都佰城研发管理平台
│   ├── products/page.tsx
│   ├── news/{page,[slug]/page}.tsx
│   └── contact/page.tsx
├── components/
│   ├── apple/                 # Tile / SplitTile / LinkArrow / CtaPill
│   ├── visuals/               # PHA / Platform / Product 抽象 SVG
│   ├── layout/                # Header (Apple 顶部毛玻璃导航) / Footer
│   └── contact/ContactForm.tsx
├── data/                      # site / company / products / news / platform
└── lib/utils.ts
```

### 设计 Token

| Token | 颜色 | 用途 |
| --- | --- | --- |
| `ink` | `#1d1d1f` | 主文字 |
| `paper` | `#ffffff` | 主背景 |
| `fog` | `#f5f5f7` | 浅灰分区 |
| `haze` | `#fbfbfd` | 卡片 hover 背景 |
| `smoke` | `#86868b` | 副文字 |
| `hairline` | `#d2d2d7` | 分隔线 |
| `link` | `#0071e3` | 主色 / 链接 / CTA |
| `obsidian` | `#000000` | 深色 Tile 背景 |
| `coal` | `#161617` | 深色卡片背景 |

字号采用 Apple 风格的 clamp 流式排版 (`hero` / `display` / `section` / `lead` / `eyebrow`)。

### 本地开发

```bash
npm install
npm run dev      # http://localhost:3000
npm run build
npm run start
npm run lint
```

### 内容维护

- 站点全局 / 导航 → `src/data/site.ts`
- 公司信息 / 历程 / 资质 → `src/data/company.ts`
- 产品矩阵与应用 → `src/data/products.ts`
- 新闻 → `src/data/news.ts`
- 研发管理平台模块 → `src/data/platform.ts`

### 后续扩展建议

- 真实摄影 / 3D 渲染图替换 `components/visuals/*` 抽象 SVG
- 联系表单接入邮件服务 (Resend / SendGrid) 或表单 SaaS
- 接入 CMS (Sanity / Strapi) 管理新闻与产品
- 增加滚动驱动动画 (IntersectionObserver) 进一步贴近 Apple 体感
- 增加多语言 i18n (英文站) / `sitemap.xml` / `robots.txt`
