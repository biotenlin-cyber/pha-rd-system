from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundError
from app.models import (
    ApplicationDomain,
    ApplicationScenario,
    GradeScenarioMatch,
    PhaGrade,
    ScenarioExternalLink,
    ScenarioTag,
    Tag,
)


async def list_scenarios(
    db: AsyncSession,
    *,
    domain: str | None = None,
    tags: list[str] | None = None,
    q: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[dict], int]:
    base = (
        select(ApplicationScenario, ApplicationDomain.code.label("domain_code"))
        .join(ApplicationDomain, ApplicationDomain.id == ApplicationScenario.domain_id)
        .where(ApplicationScenario.status == "active")
    )
    if domain:
        base = base.where(ApplicationDomain.code == domain)
    if tags:
        sub = (
            select(ScenarioTag.scenario_id)
            .join(Tag, Tag.id == ScenarioTag.tag_id)
            .where(Tag.slug.in_(tags))
            .group_by(ScenarioTag.scenario_id)
            .having(func.count(func.distinct(Tag.slug)) == len(tags))
        )
        base = base.where(ApplicationScenario.id.in_(sub))
    if q:
        like = f"%{q}%"
        base = base.where(
            (ApplicationScenario.name_zh.ilike(like))
            | (ApplicationScenario.summary.ilike(like))
        )

    total = (await db.execute(select(func.count()).select_from(base.subquery()))).scalar_one()

    stmt = (
        base.order_by(ApplicationScenario.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    rows = (await db.execute(stmt)).all()

    scenario_ids = [s.id for s, _ in rows]
    tags_by_scenario = await _load_tags_for_scenarios(db, scenario_ids)
    top_match_by_scenario = await _load_top_match_grade(db, scenario_ids)

    out: list[dict] = []
    for scenario, domain_code in rows:
        out.append(
            {
                "id": scenario.id,
                "code": scenario.code,
                "name_zh": scenario.name_zh,
                "domain_code": domain_code,
                "summary": scenario.summary,
                "tags": tags_by_scenario.get(scenario.id, []),
                "top_match_grade": top_match_by_scenario.get(scenario.id),
            }
        )
    return out, int(total)


async def _load_tags_for_scenarios(
    db: AsyncSession, scenario_ids: list[int]
) -> dict[int, list[dict]]:
    if not scenario_ids:
        return {}
    stmt = (
        select(ScenarioTag.scenario_id, Tag)
        .join(Tag, Tag.id == ScenarioTag.tag_id)
        .where(ScenarioTag.scenario_id.in_(scenario_ids))
    )
    out: dict[int, list[dict]] = {}
    for sid, tag in (await db.execute(stmt)).all():
        out.setdefault(sid, []).append(
            {
                "id": tag.id,
                "slug": tag.slug,
                "name_zh": tag.name_zh,
                "category": tag.category,
                "color": tag.color,
            }
        )
    return out


async def _load_top_match_grade(
    db: AsyncSession, scenario_ids: list[int]
) -> dict[int, str]:
    if not scenario_ids:
        return {}
    rn = (
        select(
            GradeScenarioMatch.scenario_id,
            GradeScenarioMatch.grade_id,
            func.row_number()
            .over(
                partition_by=GradeScenarioMatch.scenario_id,
                order_by=GradeScenarioMatch.match_score.desc(),
            )
            .label("rn"),
        )
        .where(GradeScenarioMatch.scenario_id.in_(scenario_ids))
        .subquery()
    )
    stmt = (
        select(rn.c.scenario_id, PhaGrade.code)
        .join(PhaGrade, PhaGrade.id == rn.c.grade_id)
        .where(rn.c.rn == 1)
    )
    return {sid: code for sid, code in (await db.execute(stmt)).all()}


async def get_scenario_detail(db: AsyncSession, key: str) -> dict:
    stmt = (
        select(ApplicationScenario, ApplicationDomain.code.label("domain_code"))
        .join(ApplicationDomain, ApplicationDomain.id == ApplicationScenario.domain_id)
        .options(
            selectinload(ApplicationScenario.tag_links).selectinload(ScenarioTag.tag),
            selectinload(ApplicationScenario.matches).selectinload(GradeScenarioMatch.grade),
            selectinload(ApplicationScenario.external_links),
        )
    )
    if key.isdigit():
        stmt = stmt.where(ApplicationScenario.id == int(key))
    else:
        stmt = stmt.where(ApplicationScenario.code == key)
    row = (await db.execute(stmt)).first()
    if row is None:
        raise NotFoundError(f"Scenario '{key}' not found")
    scenario, domain_code = row

    tags = [
        {
            "id": link.tag.id,
            "slug": link.tag.slug,
            "name_zh": link.tag.name_zh,
            "category": link.tag.category,
            "color": link.tag.color,
        }
        for link in scenario.tag_links
    ]
    matches = sorted(
        [
            {
                "grade_id": m.grade_id,
                "grade_code": m.grade.code,
                "grade_name_zh": m.grade.name_zh,
                "match_score": m.match_score,
                "recommendation_level": m.recommendation_level,
                "key_metrics": m.key_metrics or {},
                "rationale": m.rationale,
            }
            for m in scenario.matches
        ],
        key=lambda x: -x["match_score"],
    )
    external_links = [
        {
            "id": link.id,
            "link_type": link.link_type,
            "external_ref": str(link.external_ref),
            "label": link.label,
            "meta": link.meta or {},
        }
        for link in scenario.external_links
    ]

    return {
        "id": scenario.id,
        "domain_id": scenario.domain_id,
        "domain_code": domain_code,
        "code": scenario.code,
        "name_zh": scenario.name_zh,
        "name_en": scenario.name_en,
        "summary": scenario.summary,
        "sub_scenarios": scenario.sub_scenarios or [],
        "technical_requirements": scenario.technical_requirements or {},
        "typical_products": scenario.typical_products or [],
        "market_size_usd": float(scenario.market_size_usd) if scenario.market_size_usd else None,
        "market_year": scenario.market_year,
        "market_notes": scenario.market_notes,
        "status": scenario.status,
        "tags": tags,
        "matches": matches,
        "external_links": external_links,
    }


async def list_scenario_external_links(
    db: AsyncSession, scenario_id: int, link_type: str | None = None
) -> list[dict]:
    stmt = select(ScenarioExternalLink).where(
        ScenarioExternalLink.scenario_id == scenario_id
    )
    if link_type:
        stmt = stmt.where(ScenarioExternalLink.link_type == link_type)
    rows = (await db.execute(stmt)).scalars().all()
    return [
        {
            "id": r.id,
            "link_type": r.link_type,
            "external_ref": str(r.external_ref),
            "label": r.label,
            "meta": r.meta or {},
        }
        for r in rows
    ]
