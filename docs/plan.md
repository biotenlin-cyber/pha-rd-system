# PHA 应用知识库模块 — 实施计划

## Context

仓库 `pha-rd-system` 是一个"PHA 材料研发及产品开发与专利管理系统"，目前只有一个 README，属于全新项目。用户希望先交付**应用知识库模块**作为系统的第一块拼图，目的有三：

1. **沉淀 PHA 新应用价值**——把医疗、可降解包装、农业、海洋、3D 打印、纺织、电子、化妆品、建筑、碳中和等领域的应用场景结构化，形成可检索的领域知识资产。
2. **支撑后续研发决策**——通过"PHA 牌号 ↔ 应用场景"的匹配关系（含关键性能指标与推荐等级），帮助研发人员快速判断"用什么牌号做什么场景"。
3. **预留与专利/项目模块的接口**——为后续模块提供关联钩子，避免后期重写表结构。

技术栈：**Vue 3 + TypeScript + Element Plus**（前端）/ **FastAPI + SQLAlchemy 2.0 (async) + Alembic**（后端）/ **PostgreSQL 15**。交付深度：**全栈 MVP，含初始种子数据**，可本地一键启动演示。

---

## 一、项目骨架（monorepo）

工具选型：后端 `uv` + `ruff` + `pytest` + `pre-commit`；前端 `pnpm` + `vite` + `vue-tsc` + `eslint`。

```
pha-rd-system/
├── docker-compose.yml          # 仅 postgres，前后端裸跑
├── Makefile                    # make up / migrate / seed / dev-be / dev-fe / test
├── .pre-commit-config.yaml
├── backend/
│   ├── pyproject.toml          # uv-managed
│   ├── alembic.ini
│   ├── alembic/versions/0001_init.py
│   ├── app/
│   │   ├── main.py             # FastAPI app factory + CORS + 路由聚合
│   │   ├── core/{config,logging,exceptions}.py
│   │   ├── db/{base,session,deps}.py
│   │   ├── models/             # domain / scenario / grade / match / tag / associations
│   │   ├── schemas/            # pydantic models 镜像
│   │   ├── services/           # 业务层（含 search_service）
│   │   ├── api/v1/             # domains / scenarios / grades / matches / tags / search
│   │   └── utils/text.py
│   ├── scripts/seed.py         # python -m scripts.seed --reset
│   ├── data/seed/*.yaml
│   └── tests/                  # pytest + httpx async client
└── frontend/
    ├── package.json / vite.config.ts (proxy /api → :8000)
    └── src/
        ├── main.ts / App.vue / router/ / stores/ / api/ / types/
        ├── views/              # Home / DomainList / DomainDetail / ScenarioDetail / GradeList / GradeDetail / SearchResults
        ├── components/         # DomainCard / ScenarioCard / GradeCard / MatchTable / PerformanceRadar / FilterSidebar / SearchBar / TagChip / PlaceholderLinks
        ├── composables/{useFilters,useSearch}.ts
        └── styles/element-overrides.scss
```

---

## 二、数据模型（PostgreSQL 15）

通用约定：所有表 `id BIGSERIAL PK` + `created_at`/`updated_at TIMESTAMPTZ DEFAULT now()`；编码字段使用 `CITEXT`；柔性指标使用 `JSONB`。初始迁移启用扩展 `pg_trgm`、`citext`。

### 核心表

- **`application_domains`** — 一级应用领域（医疗/包装/农业…）
  字段：`code (CITEXT UNIQUE)`、`name_zh`、`name_en`、`description`、`icon`、`sort_order`。
- **`application_scenarios`** — 二级应用场景
  字段：`domain_id FK`、`code (UNIQUE, e.g. medical.suture)`、`name_zh/en`、`summary`、`sub_scenarios JSONB`、`technical_requirements JSONB`（降解周期、生物相容性等级、力学/热学指标）、`typical_products JSONB`、`market_size_usd`、`market_year`、`market_notes`、`status`、`search_vector TSVECTOR`。
  索引：`(domain_id)`；GIN(`search_vector`)；GIN(`name_zh gin_trgm_ops`)；GIN(`technical_requirements jsonb_path_ops`)。
- **`pha_grades`** — PHA 牌号库（PHB / PHBV / PHBHHx / P34HB / P3HB4HB / mcl-PHA …）
  字段：`code (UNIQUE)`、`name_zh`、`full_name`、`polymer_family`、关键性能列（`tm_celsius`、`tg_celsius`、`crystallinity_pct`、`elongation_at_break_pct`、`tensile_strength_mpa`、`youngs_modulus_gpa`、`biocompatibility_class`、`degradation_months_soil`、`degradation_months_marine`）、`extra_metrics JSONB`、`typical_processing JSONB`、`search_vector`。
- **`grade_scenario_matches`** — 牌号 ↔ 场景多对多（含评分）
  字段：`grade_id FK`、`scenario_id FK`、`match_score SMALLINT (0~100)`、`recommendation_level CHECK(preferred/suitable/marginal/not_recommended)`、`key_metrics JSONB`（生物相容/力学/降解/工艺四项细分）、`rationale TEXT`、`references JSONB`。
  索引：`UNIQUE(grade_id, scenario_id)`；`(scenario_id, match_score DESC)`；`(grade_id, match_score DESC)`。
- **`tags`** + **`scenario_tags`** / **`grade_tags`** — 标签与多对多关联，`category` 区分 property/process/certification/market。

### 预留外部关联（专利/项目）

为避免在父表（`patents` / `projects`）尚未存在时建立硬 FK，使用占位关联表：

- **`scenario_external_links`** / **`grade_external_links`**
  字段：`link_type CHECK('patent'|'project')`、`external_ref UUID`（占位，未来父表的主键）、`label`、`meta JSONB`。
  落地策略：父表上线后通过 `ALTER TABLE … ADD CONSTRAINT … NOT VALID` + `VALIDATE CONSTRAINT` 平滑加 FK，不重写历史数据。

### 中文检索策略

**采用 `simple` + `pg_trgm`**，不依赖 `zhparser`（编译复杂、Docker 镜像维护成本高）。在 `app/core/config.py` 暴露 `SEARCH_BACKEND` 开关，并预留 `0002_enable_zhparser.py` 注释模板供后期切换。排序公式：

```sql
ORDER BY ts_rank(search_vector, plainto_tsquery('simple', :q)) DESC,
         similarity(name_zh, :q) DESC
```

---

## 三、后端 API 设计（前缀 `/api/v1`）

列表统一 `?page=1&page_size=20&sort=`，响应 `{data, meta}`。

| 资源 | 关键端点 |
|---|---|
| 领域 | `GET/POST /domains`、`GET/PATCH/DELETE /domains/{id}` |
| 场景 | `GET/POST /scenarios?domain=&tags=&q=`、`/{id}`、`/{id}/matches`、`/{id}/recommended-grades?top=5`、`/{id}/external-links` |
| 牌号 | `GET/POST /grades?family=&q=`、`/{id}`、`/{id}/matches`、`/{id}/recommended-scenarios?top=5` |
| 匹配 | `GET/POST/PATCH/DELETE /matches?grade_id=&scenario_id=&min_score=` |
| 标签 | `GET/POST /tags?category=`、`POST /scenarios/{id}/tags` |
| 检索 | `GET /search?q=&domain=&grade=&tags=&types=scenario,grade` → `{meta, facets:{domain,tag,type}, data:[{type,id,code,name_zh,snippet,score}]}` |
| 分面 | `GET /facets/scenarios?domain=&tags=` → 侧栏计数 |

Pydantic schemas 一文件一资源（`schemas/{domain,scenario,grade,match,tag,search,common}.py`）；SQLAlchemy 2.0 `Mapped[...]` + `mapped_column`，全 async session；Alembic `0001_init.py` 一次性建表+扩展+索引。

---

## 四、前端页面与组件

### 路由

| 路径 | 视图 |
|---|---|
| `/` | HomeView（领域卡片网格 + 统计 + 热门牌号） |
| `/domains` / `/domains/:code` | DomainListView / DomainDetailView |
| `/scenarios/:code` | ScenarioDetailView（技术要求表 + 市场卡 + MatchTable + PlaceholderLinks） |
| `/grades` / `/grades/:code` | GradeListView / GradeDetailView（含 `PerformanceRadar` echarts 雷达图） |
| `/search?q=` | SearchResultsView（FilterSidebar 分面 + 分组结果） |

### 复用组件
`SearchBar`（debounce）、`DomainCard`、`ScenarioCard`、`GradeCard`、`MatchTable`（el-table + 评分条 + 推荐等级徽章）、`PerformanceRadar`（echarts 模块化导入，仅 RadarChart，gz < 80KB）、`FilterSidebar`、`TagChip`、`PlaceholderLinks`、`Pagination`。

### 状态与 API 层
Pinia stores 一资源一文件（`domain` / `scenario` / `grade` / `search`）；axios 客户端 `api/client.ts` 统一 baseURL、错误拦截、未来鉴权头注入点；Element Plus 通过 `unplugin-auto-import` 按需加载，主题色 `#1f9e6e`（生物降解绿），locale `zh-cn`。

---

## 五、初始种子数据（`scripts/seed.py` + `data/seed/*.yaml`）

加载器：argparse `--reset` / `--only`，按 `code` 幂等 upsert。

| 文件 | 数量 | 内容要点 |
|---|---|---|
| `domains.yaml` | 10 | medical / packaging / agriculture / marine / 3d_printing / textile / electronics / cosmetics / construction / carbon_neutral |
| `scenarios.yaml` | ~30 | 每领域 ~3 个；含 `technical_requirements`（降解周期、ISO10993、力学下限）、`typical_products`、`market_size_usd` |
| `grades.yaml` | 6 | PHB / PHBV / PHBHHx / P34HB / P3HB4HB / mcl-PHA，含 Tm/Tg/结晶度/断裂伸长/拉伸强度/降解月数 |
| `tags.yaml` | ~20 | 分类 property / process / certification(FDA/CE/ISO10993/EN13432/ASTM-D6400) / market |
| `matches.yaml` | ~50 | 每牌号 ~8 条；评分采用 `生物相容30+力学30+降解20+工艺20=100` 评分细则，存入 `key_metrics` |

`data/seed/README.md` 记录评分细则与数据来源（datasheet / 综述 / 专利）。

---

## 六、关键文件清单（按依赖顺序）

```
pha-rd-system/docker-compose.yml
backend/pyproject.toml
backend/alembic/versions/0001_init.py
backend/app/main.py
backend/app/core/config.py
backend/app/db/session.py
backend/app/models/{domain,scenario,grade,match,tag,associations}.py
backend/app/api/v1/{__init__,domains,scenarios,grades,matches,tags,search}.py
backend/app/services/search_service.py
backend/scripts/seed.py
backend/data/seed/{domains,scenarios,grades,matches,tags}.yaml
frontend/package.json
frontend/vite.config.ts
frontend/src/main.ts
frontend/src/router/index.ts
frontend/src/api/client.ts
frontend/src/views/{HomeView,DomainDetailView,ScenarioDetailView,GradeDetailView,SearchResultsView}.vue
frontend/src/components/{MatchTable,PerformanceRadar,FilterSidebar,SearchBar}.vue
```

---

## 七、本地开发与端到端验证

### 启动命令
```bash
docker compose up -d postgres
cd backend && uv sync && cp .env.example .env
uv run alembic upgrade head
uv run python -m scripts.seed --reset
uv run uvicorn app.main:app --reload --port 8000
# 另一终端
cd frontend && pnpm install && cp .env.example .env && pnpm dev
```
或一键 `make up && make migrate && make seed && make dev-be` / `make dev-fe`。

### 验证清单（每条都要走通）
1. `GET /healthz` 返回 `{"status":"ok"}`。
2. `GET /api/v1/domains` 返回 10 条。
3. `GET /api/v1/search?q=可吸收&types=scenario` 命中 `medical.suture`。
4. 浏览器打开 `http://localhost:5173/`，渲染 10 张领域卡片。
5. 点击「医疗」→ 显示 ≥3 个场景卡片。
6. 进入 `medical.suture` → `MatchTable` 中 `PHBHHx` 排在首位。
7. 进入 `/grades/PHBHHx` → 性能雷达图渲染，匹配场景列表显示。
8. 顶部搜索「缝合」→ 搜索结果页含 scenario + grade 分组、左侧分面计数正确。
9. `pytest` 通过；`pnpm vue-tsc --noEmit` 无类型错误。

---

## 八、风险与权衡

- **中文检索**：`pg_trgm` 仅满足百级数据规模，长尾多字 query 召回有限。已预留 `SEARCH_BACKEND` 开关与 `zhparser` 迁移模板，规模上来后切换。
- **专利/项目占位 FK**：`external_ref UUID` 短期失去引用完整性。父表上线后用 `NOT VALID` + `VALIDATE CONSTRAINT` 升级为真 FK，期间增加孤儿记录夜检任务。
- **鉴权**：MVP 不做。`api/client.ts` 已为 `Authorization` 头预留注入点，后续接 `fastapi-users` / 自建 JWT。
- **匹配评分主观性**：50 条匹配是最容易"拍脑袋"的环节，必须把 30+30+20+20 评分细则写进 `data/seed/README.md`，并在 `key_metrics` 落库。
- **JSONB 灵活性 vs 类型**：前端通过 `frontend/src/types/models.ts` 与 Pydantic schema 同步保证类型；写入侧 Pydantic 校验拒绝脏数据。
- **Docker 化范围**：仅容器化 Postgres，前后端裸跑保留热重载体验；部署时再补 Dockerfile。
- **echarts 体积**：`PerformanceRadar` 使用 `echarts/core` 模块化导入，仅引 `RadarChart`，gz 控制在 ~80KB。

---

## 九、后续可扩展点（不在本期实施）

- 专利模块：上线 `patents` 父表 + Alembic 加 FK，复用 `scenario_external_links` / `grade_external_links`。
- 项目模块：同上。
- 鉴权与 RBAC：`fastapi-users` + `users` / `roles` 表。
- 中文分词升级：`zhparser` 或迁移到 Elasticsearch / Meilisearch。
- 指标可视化：基于 `match_score` 做"牌号雷达 vs 场景需求"的差距热力图。
