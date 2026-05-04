# Bioten™ 博碳 PHA · 设计真理来源

> 适用品牌:**Bioten™ 博碳PHA** — 一个生物基水性 PHA 阻隔涂层平台,面向纸基包装。
> 本文件与都佰城 PHA 项目(`docs/DESIGN.md`)是**两个独立品牌**的设计系统,严禁交叉混用。
> 修改本文件后请同步更新 `public/bioten-preview.html` 与未来落地的 Bioten 站点 token。

---

## 1. 品牌气质定位

> **Bio-material Luxury** — 介于 Apple 产品发布页、材料实验室、奢侈品包装、科学期刊封面 之间。

| 是 | 不是 |
|---|---|
| 洁净、温和、精密、可信、可验证 | 普通环保绿 / SaaS 蓝 |
| 纸纤维 / 透明膜 / 乳液颗粒 / 微观结构 | 大片森林、地球、烟囱、塑料海洋 |
| "Barrier, born from biology." | "环保可降解,绿色未来,守护地球" |
| 数据:Cobb / WVTR / Kit / Repulping pathway | 虚假百分比 (95%、80%、30%) |
| 一层透明膜在纸上工作 | 蓝色水花包裹纸杯 |

---

## 2. Color tokens

### 2.1 Fiber White (背景纸白系统) — 占比 55–65%

| Token | Hex | 用途 |
|---|---|---|
| `fiberWhite` | `#F6F2EA` | 页面主背景 |
| `pulpIvory` | `#ECE5D8` | 纸张纹理 / 次级背景 |
| `mistWhite` | `#F8FAF8` | 卡片内部 / 留白区域 |
| `warmAsh` | `#D8D2C7` | 细线 / 分割 / 纸纤维暗部 |

### 2.2 Bio Carbon (深色系 — 主黑绿)

| Token | Hex | 用途 |
|---|---|---|
| `bioCarbon` | `#17231F` | 主标题 / Logo / 正文重点 |
| `deepChlorophyll` | `#243A32` | 二级标题 / 深色模块 |
| `graphiteGreen` | `#3C4A43` | 正文 / 导航 / 说明文字 |

### 2.3 Mineral Blue (水性科技蓝) — 占比 18–25%

| Token | Hex | 用途 |
|---|---|---|
| `mineralBlue` | `#7FAFC4` | 主视觉水膜 / 乳液流体 |
| `waterborneBlue` | `#A8D3DE` | 渐变 / 透明膜 / 高光 |
| `iceBlue` | `#D9ECF1` | 背景雾化 / 卡片光晕 |
| `technicalBlue` | `#2D6F9F` | **CTA 主按钮** / 数据 / 交互状态 |

### 2.4 Bio Green (生物来源绿) — 占比 3–6%

| Token | Hex | 用途 |
|---|---|---|
| `algaeGreen` | `#6F927C` | 生物来源标签 / 图标 |
| `mossGreen` | `#82976E` | 可持续模块 / 图表辅助 |
| `softLeaf` | `#B8C8A9` | 背景渐变 / 轻量状态 |
| `regenerativeGreen` | `#4E735D` | 重点标签 / 认证信息 |

### 2.5 PHA Amber (高级辅助暖金) — 占比 1–3%

| Token | Hex | 用途 |
|---|---|---|
| `phaAmber` | `#C9A66B` | **重点数据 / 徽章 / 微粒** |
| `fermentationGold` | `#D8C18A` | 原料颗粒 / 轻微高光 |
| `celluloseBeige` | `#BFAF91` | 纸纤维阴影 / 材质层 |
| `softOchre` | `#E8D7AE` | 浅色背景过渡 |

> 比例铁律:绿色和金色都不要大面积使用。**越少越高级。**

---

## 3. 三套可选风格 (按场景调用)

### 方案 A · 温和材料科技风(主推荐 — 官网 / 品牌手册 / 展会主视觉)

```
背景  #F6F2EA
主文字 #17231F
主视觉蓝 #A8D3DE
CTA 蓝 #2D6F9F
生物绿 #6F927C
暖金点缀 #C9A66B
```

### 方案 B · 高端实验室风(技术中心 / TDS 页面 / 投资人材料)

```
背景  #EEF3F2
主文字 #10231F
冷蓝 #BFDCE6
深蓝灰 #315D70
图表绿 #5E7E6A
线条灰 #B9C4C0
```

### 方案 C · 高级包装奢华风(样品盒 / 产品发布 / 展会空间 / 品牌视频)

```
背景  #EFE8D8
深色 #1C2521
膜蓝 #91C2D0
金色 #C5A45E
象牙白 #FAF7EF
深松绿 #2F4B3D
```

---

## 4. Typography

### 英文

| 用途 | 方向 |
|---|---|
| Logo / 大标题 | 高对比衬线:Editorial New / Canela / Didot |
| 正文 / 导航 | 人文无衬线:Suisse / Neue Haas Grotesk / Inter |
| 数据 / 参数 | 等宽:IBM Plex Mono / JetBrains Mono |

### 中文

| 用途 | 方向 |
|---|---|
| 中文标题 | 宋体 / 新宋风 / 高级衬线(刊物气质,而非互联网圆体) |
| 中文正文 | 思源黑体 / 阿里巴巴普惠体 / HarmonyOS Sans |
| 数据标签 | 等宽数字字体 |

---

## 5. 版式铁律

1. **首屏只保留一个强主视觉。** 不要同时出现杯子、叶子、分子、地球、循环箭头、工厂。**只讲"一层膜"。**
2. **标题必须短。** 高级品牌不靠长标题解释自己。
3. **数据不要堆。** 没有验证数据时,写"验证路径"而非虚假百分比。
4. **按钮不要多。** 首屏最多两个。
5. **卡片最多三张。** 高级感来自"少而准"。
6. **绿色不是主角,阻隔膜才是主角。**

---

## 6. 文案库

### 中文主张候选

- 让纸拥有新的阻隔能力。
- 不是多一层塑料,而是一层来自生物的工程膜。
- 从 PHA 乳液到纸基包装阻隔系统。
- 以可验证的材料路径,支持可循环的纸包装升级。
- 看得见的是纸,看不见的是 Bioten。
- 摸得到的是纸,看不见的是 Bioten。

### 英文主张候选

- Barrier, born from biology.
- A living barrier for paper packaging.
- From bio-based emulsion to functional paper.
- Engineered coating systems for circular paper packaging.
- The invisible layer that helps paper perform.

### 反面教材(禁止使用)

- "环保可降解,绿色未来,守护地球。"
- "Excellent resistance to grease, moisture and oxygen." — 太营销,改写成验证路径。

---

## 7. 主视觉 Brief (供设计 / AI prompt)

> 透明膜在纸纤维上"生长"。

- 极薄、半透明、有折射感的膜从纸纤维表面缓慢展开
- 膜的边缘有微弱蓝色折射
- 膜下能看到纸纤维纹理
- 水滴停在膜上没有渗透,呈高接触角
- 油滴呈高接触角被排斥
- 远处有 PHA 微粒悬浮(米金 / 透明白)
- 浅景深 / 微距材料摄影 / 柔和实验室光
- **不是水流,不是塑料片,不是水花包裹**

---

## 8. 关键组件

### 8.1 Material Data Plates (替代普通玻璃卡片)

像极薄实验室玻璃片,带细技术线与简洁参数。**只写"路径",不堆描述。**

```
Card 01    Water Barrier            Cobb / WVTR pathway
Card 02    Grease Resistance        Kit / food-contact route
Card 03    Repulping Design         Fiber recovery validation
Card 04    Bio-based Carbon         ASTM D6866 pathway
```

CSS 规范:

```css
background: rgba(248, 250, 248, 0.52);
border: 1px solid rgba(255, 255, 255, 0.72);
box-shadow:
  0 24px 70px rgba(45, 111, 159, 0.14),
  inset 0 1px 0 rgba(255, 255, 255, 0.72);
backdrop-filter: blur(22px);
```

### 8.2 三档产品体系卡

只通过顶部极细色带区分,文字与卡身保持一致。

| 牌号 | 定位 | 色带 |
|---|---|---|
| Bioten™ Plus | Balanced barrier system — 通用纸基食品包装升级 | `#6F927C` (algaeGreen) |
| Bioten™ Pro | Performance coating system — 高阻隔 / 高涂布效率 / 高热封 | `#2D6F9F` (technicalBlue) |
| Bioten™ Ultra | Circularity-focused system — 高 ESG / 回收路径 / 低碳示范 | `#C9A66B` (phaAmber) |

### 8.3 Technology Diagram — 横向膜层剖面

```
Food / Liquid / Oil
────────────────────
Bioten Barrier Layer
────────────────────
Paper Fiber Substrate
────────────────────
Repulping / Recovery Pathway
```

每层半透明材质,而非复杂分子结构。

### 8.4 CTA 按钮

| 类型 | 样式 |
|---|---|
| 主 | `bg: #2D6F9F` / `color: #F8FAF8` / `hover: #1F5F88` |
| 次 | `bg: rgba(255,255,255,.54)` / `border: 1px solid rgba(23,35,31,.12)` / `color: #17231F` / `backdrop-filter: blur(16px)` |

---

## 9. 首屏背景配方

```css
background:
  radial-gradient(circle at 72% 35%, rgba(168, 211, 222, 0.45), transparent 34%),
  radial-gradient(circle at 28% 72%, rgba(201, 166, 107, 0.16), transparent 28%),
  linear-gradient(135deg, #F6F2EA 0%, #EEF4F3 48%, #DDEBF0 100%);
```

纸白 + 雾蓝 + 暖金三层光,比单一蓝白高级。

---

## 10. 影像风格清单

### 不建议

大片森林 / 手捧地球 / 绿色叶子背景 / 工厂烟囱对比 / 塑料垃圾海洋 / 过度水花 / 过度分子结构 / 过度蓝色发光科技线

### 建议

纸纤维微距 / 透明膜边缘 / 水滴接触角 / 涂布线微观 / 纸杯边缘剖面 / 半透明乳液颗粒 / 柔和实验室光 / 极简白底样品摄影 / 高级材料包装盒

---

## 11. 站点信息架构(建议)

```
/                           Hero · Barrier, born from biology.
/technology                 PHA emulsion → coating → barrier → circularity 四步
/performance                Performance Matrix (Cobb / Kit / WVTR / Heat Seal / Repulp / Food)
/applications               Paper cups / bowls / trays / bags / coated paper / custom
/products                   Bioten Plus / Pro / Ultra 三档体系
/verification               TDS · SDS · Trial Guide · Application Notes · Reports
/sustainability             Bio-based carbon · Repulping · Circular pathway
/about                      Bioten 团队 · 工厂 · 资质
/contact                    Start a Coating Trial
```

---

## 12. 与都佰城 PHA 的关系

待定。两种品牌锁定方案:

- **A · 同公司不同子品牌**:`Bioten™ 博碳PHA × 都佰城` — 在 Bioten 的关于页 / footer 引用都佰城 PHA 作为原料端母品牌
- **B · 完全独立品牌**:不在 Bioten 站点出现都佰城名

> 建议在落地前由商务确认,本设计文档先按 B 方案执行(完全独立),保留未来切到 A 的可能。

---

## 13. AI 视觉生成 Prompt(可直接复用)

```
Create a premium homepage hero concept for Bioten™ 博碳PHA, a bio-based
waterborne PHA barrier coating platform for paper packaging. The design
should feel like high-end material science, not a generic eco website.
Use a refined palette of paper ivory, mineral blue, bio-carbon green,
and subtle PHA amber. Avoid bright green, plastic-like blue, and overused
environmental symbols.

Hero visual: a cinematic macro material scene showing a thin translucent
bio-based barrier film forming over a textured paper fiber surface or
paper cup cross-section. The film should look ultra-thin, elegant, slightly
refractive, and waterborne — not like a water splash. Show subtle suspended
PHA emulsion particles, soft paper fibers, a water droplet resting on the
coated surface, and a small oil droplet being repelled. Use shallow depth
of field, soft laboratory lighting, premium material texture, and calm
motion energy.

Layout: left side editorial typography with the headline "Barrier, born
from biology." and supporting text "Bio-based waterborne coating systems
for paper packaging." Add two refined pill buttons: "Start a Coating Trial"
and "View Technology". Top navigation should be minimal and thin: Solutions,
Technology, Applications, Sustainability, Resources.

Add three minimal translucent material data plates, not generic glass cards.
Each card should look like a thin lab glass plate with subtle technical
lines and concise labels:
1. Water / Grease Barrier
2. Heat-sealable Coating
3. Repulping Design

Background: warm paper-white gradient with soft mineral-blue haze and very
subtle oversized BIOTEN typography in the back. Premium, restrained, clean,
scientific, elegant, Apple-like, material-lab aesthetic, high-end B2B brand
design.
```

---

## 14. 评判清单 (上线前必过)

- [ ] 颜色不鲜艳,但层次丰富(纸白 / 雾蓝 / 暖金三层)
- [ ] 主视觉不复杂,但材料逻辑准确(只一层膜在纸上工作)
- [ ] 文案不喊口号,每句话都可验证(写路径,不写百分比)
- [ ] 玻璃卡片不模板化,而是 Material Data Plates
- [ ] 绿色不是主角,阻隔膜才是主角
- [ ] 首屏只两个按钮
- [ ] 中文标题带宋体气质,不像互联网官网
