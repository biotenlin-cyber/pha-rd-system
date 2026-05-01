# pha-rd-system

PHA 材料研发及产品开发与专利管理系统。

当前已交付：**应用知识库模块（MVP）**——结构化沉淀 PHA 在医疗、可降解包装、农业、海洋、3D 打印、纺织、电子、化妆品、建筑、碳中和等领域的应用场景，以及 PHB / PHBV / PHBHHx / P34HB / P3HB4HB / mcl-PHA 等牌号的性能指标与场景匹配关系。

## 模块能力

1. **应用场景分类库**：领域 → 子场景 → 技术要求（降解周期、生物相容性、力学指标）+ 典型产品 + 市场规模。
2. **牌号-场景匹配**：含 0–100 评分（生物相容 30 + 力学 30 + 降解 20 + 工艺 20）与推荐等级。
3. **检索与筛选**：领域/牌号/标签/全文检索（PostgreSQL `simple` + `pg_trgm`）。
4. **专利/项目预留接口**：占位关联表，父表上线后通过 `NOT VALID` + `VALIDATE CONSTRAINT` 平滑加 FK。

## 技术栈

- 后端：Python 3.11+ / FastAPI / SQLAlchemy 2.0 (async) / Alembic / Pydantic v2 / PostgreSQL 15
- 前端：Vue 3 + TypeScript + Vite + Element Plus + Pinia + ECharts
- 工具链：uv / ruff / pytest / pnpm / vue-tsc / pre-commit

## 本地开发

需要 Docker、Python 3.11+、`uv`、Node 20+、`pnpm`。

```bash
make up                # 启动 postgres
make install-be        # uv sync
make migrate           # alembic upgrade head
make seed              # 灌入种子数据
make dev-be            # 后端 :8000

# 另一终端
make install-fe
make dev-fe            # 前端 :5173
```

打开 <http://localhost:5173/> 验证：10 个领域卡片、`medical.suture` 场景、`PHBHHx` 牌号雷达图、搜索"缝合"。

## 目录

```
backend/         FastAPI + SQLAlchemy 2.0 + Alembic
frontend/        Vue 3 + Element Plus
docker-compose.yml  仅 Postgres
Makefile         一键命令
docs/plan.md     实施计划全文
```
