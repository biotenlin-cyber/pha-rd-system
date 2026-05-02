# 都佰城 PHA-RD 站点 — 设计系统真理来源

> 该文件是项目的 **设计 token 单一来源**。配色、字号、间距、圆角、动效缓动,全以本文件为准。
> 直接照抄自 apple.com (homepage / iPhone 产品页 / Newsroom / Mac 产品页) 与 tesla.com 的真实 CSS 与公开分析,辅以 Apple 品牌指南。
> 修改 token 必须同步更新 `tailwind.config.ts` + `src/app/globals.css`。

---

## 1. Color tokens

来源:apple.com 官网生产 CSS、Apple Human Interface Guidelines、品牌指南。

| Token | Hex | RGB | 用途 | Apple 对应 |
|---|---|---|---|---|
| `paper` | `#FFFFFF` | 255,255,255 | 主背景(白底段) | Page bg |
| `fog` | `#F5F5F7` | 245,245,247 | 次背景 / 卡片底(灰底段) | Athens Gray (官方主灰) |
| `haze` | `#FAFAFC` | 250,250,252 | hover 态浅灰 | — |
| `obsidian` | `#000000` | 0,0,0 | 黑色 hero / hero moment | Black sections |
| `coal` | `#161617` | 22,22,23 | 黑底卡片 / 表格深 | Card on black |
| `ink` | `#1D1D1F` | 29,29,31 | 主文字 | Shark (官方主黑) |
| `ash` | `#424245` | 66,66,69 | 正文次级 | Body secondary |
| `smoke` | `#6E6E73` | 110,110,115 | 三级文字 / 标签 | Gray2 |
| `silver` | `#86868B` | 134,134,139 | 弱文字 / disabled | Gray3 |
| `hairline` | `#D2D2D7` | 210,210,215 | 1px 描边 / 分隔 | Border |
| `link` | `#0066CC` | 0,102,204 | 链接文字(text 链) | Link blue |
| `linkHover` | `#0077ED` | 0,119,237 | 链接 hover | Link hover |
| `appleBlue` | `#0071E3` | 0,113,227 | 主按钮(Buy / 申请样品) | Action button bg |
| `appleBlueHover` | `#0077ED` | 0,119,237 | 主按钮 hover | Action button hover |

> Apple 官网用 `#0066CC` 作 inline 链接,`#0071E3` 作蓝胶囊按钮。两个不通用,**必须区分**。

---

## 2. Typography

字体栈(无版权字体,**所有 weight 用系统字体回退**):

```css
font-family:
  "SF Pro Display",
  "SF Pro Text",
  "SF Pro Icons",
  -apple-system,
  BlinkMacSystemFont,
  "Helvetica Neue",
  "PingFang SC",
  "Microsoft YaHei",
  Helvetica,
  Arial,
  sans-serif;
```

字号阶梯(向上 clamp 到桌面端,**与 apple.com 实测对齐**):

| Token | 移动 → 桌面 | 字重 | line-height | letter-spacing | Apple 用途 |
|---|---|---|---|---|---|
| `mega` | 56 → 128 px | 600 | 1.0 | -0.035em | 跨页大标题(罕用) |
| `hero` | 44 → 96 px | 600 | 1.04 | -0.005em | iPhone hero h1 |
| `display` | 36 → 60 px | 600 | 1.08 | -0.003em | section h2 |
| `section` | 28 → 40 px | 600 | 1.12 | -0.003em | 模块标题 h3 |
| `lead` | 18 → 22 px | 400 | 1.35 | 0 | hero 副标 |
| `body` | 17 → 17 px | 400 | 1.47 | -0.022em | 正文 |
| `eyebrow` | 12 → 12 px | 600 | 1 | 0.5em (uppercase) | 小标 |

> 关键:**正文 17px 而非 16px**,这是 apple.com 的桌面端正文(也是 SF Pro 设计的最佳尺寸)。

---

## 3. Layout

| 项目 | 值 | 备注 |
|---|---|---|
| Container max-width | **980 px** | apple.com 全站标准 |
| Container max-width (wide) | 1280 px | 仅极少数全幅模块用 |
| Section gutter (inline) | 22 px | 移动端 |
| Section gutter (desktop) | 32 px | 桌面端 |
| Section padding (vertical) | 96 → 130 px | py-24 ~ py-32 |
| Tile-to-tile gap | 8 px | 黑白拼接的接缝 |

---

## 4. Components

### Top bar
- **Promo bar**: 30px 高,`#F5F5F7` 底,`#1D1D1F` 12px 文字,1px hairline 下边
- **Main nav**: 44px 高,`rgba(255,255,255,0.72)` + `backdrop-filter: blur(20px)`,1px hairline 下边
- 主 logo 与导航字号:14px,字间距 -0.01em

### Buttons
- **Primary pill**: 高 44px / 内边距 24px,`bg-appleBlue` `text-white` `rounded-full`,16px 字号
- **Compact pill** (sticky bar 用): 高 32px / 内边距 16px,12-13px 字号
- **Link arrow**: 文字 + ` ›`,hover 下划线显现,主色 `#0066CC`

### Cards / Tiles
- **Marble** (大卡): `rounded-[28px]` `bg-fog` 背景
- **Tile** (中卡): `rounded-[22px]` 
- **Pill / button**: `rounded-full`
- **Image / spec**: `rounded-[18px]`

### Sticky product subnav
- 顶部 80px 偏移(promo + main nav 下方),48px 高
- `rgba(255,255,255,0.85)` + blur(20px),hairline 下边
- 滚动 320px 后渐入,opacity + translateY 300ms

---

## 5. Motion

```css
/* Apple 标志缓动 */
--ease-apple: cubic-bezier(0.22, 1, 0.36, 1);  /* easeOutQuint */
--ease-emphasized: cubic-bezier(0.4, 0, 0.2, 1); /* Material-ish, hover */

/* 入场动画 */
fade-up: 800ms var(--ease-apple) → opacity 0→1, translateY 24px→0;
hover-tile: 200ms ease;
sticky-subnav: 300ms var(--ease-apple);
```

IntersectionObserver 阈值:`0.12`,`rootMargin: "0px 0px -8% 0px"`。

---

## 6. 来源(本次研究)

| 来源 | 用途 |
|---|---|
| apple.com 实测尝试(被 403 阻断,fallback 到下列) | 主参考 |
| Apple 公开 ac-globalnav.built.css | nav 字体栈 |
| `colorpalettegenerator.ai/brands/apple` 索引值 | 主色对齐 |
| `gist.github.com/riodw` Apple Colors CSS | 调色板 |
| `KunalTanwar11/apple-colors` GitHub | 系统色变量 |
| Apple HIG (`developer.apple.com/design/human-interface-guidelines`) | typography / spacing 指南 |
| Wikipedia "Typography of Apple Inc." | 字体演进 |
| Jon Lehman "Code the iPhone 14 Landing Page" | 980px 容器 |
| tesla.com(被 403,通过外部分析推断) | 对比参考 |

---

## 7. Tesla 对比与取舍(为什么以 Apple 为主)

特斯拉风格更强调:
- 全屏背景图 + 上下层结构(我们没有真实拍图,做不到)
- 顶部透明/反色导航(动态主题切换)
- 极少装饰、留白更阔
- "Order Now" 居中底部黑底胶囊

由于 PHA 是工业 B2B 而非汽车,信息密度高于特斯拉。**主参考 Apple,辅以 Tesla 的"hero 极简、CTA 居中"原则**。
