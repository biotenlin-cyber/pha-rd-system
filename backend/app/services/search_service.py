import time

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ApplicationDomain, ApplicationScenario, PhaGrade, ScenarioTag, Tag


async def search(
    db: AsyncSession,
    *,
    q: str = "",
    domain: str | None = None,
    grade: str | None = None,
    tags: list[str] | None = None,
    types: list[str] | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    start = time.perf_counter()
    types = types or ["scenario", "grade"]
    like = f"%{q}%" if q else None
    similarity_q = q or ""

    hits: list[dict] = []

    if "scenario" in types:
        stmt = (
            select(
                ApplicationScenario.id,
                ApplicationScenario.code,
                ApplicationScenario.name_zh,
                ApplicationScenario.summary,
                ApplicationDomain.code.label("domain_code"),
                func.greatest(
                    func.similarity(ApplicationScenario.name_zh, similarity_q),
                    func.similarity(
                        func.coalesce(ApplicationScenario.summary, ""), similarity_q
                    ),
                ).label("score"),
            )
            .join(ApplicationDomain, ApplicationDomain.id == ApplicationScenario.domain_id)
            .where(ApplicationScenario.status == "active")
        )
        if domain:
            stmt = stmt.where(ApplicationDomain.code == domain)
        if like:
            stmt = stmt.where(
                (ApplicationScenario.name_zh.ilike(like))
                | (ApplicationScenario.summary.ilike(like))
                | (ApplicationScenario.code.ilike(like))
            )
        if tags:
            sub = (
                select(ScenarioTag.scenario_id)
                .join(Tag, Tag.id == ScenarioTag.tag_id)
                .where(Tag.slug.in_(tags))
            )
            stmt = stmt.where(ApplicationScenario.id.in_(sub))
        stmt = stmt.order_by(text("score DESC NULLS LAST"), ApplicationScenario.id)
        for sid, code, name_zh, summary, domain_code, score in (
            await db.execute(stmt)
        ).all():
            hits.append(
                {
                    "type": "scenario",
                    "id": sid,
                    "code": code,
                    "name_zh": name_zh,
                    "snippet": summary,
                    "score": float(score or 0),
                    "domain_code": domain_code,
                }
            )

    if "grade" in types:
        gstmt = select(
            PhaGrade.id,
            PhaGrade.code,
            PhaGrade.name_zh,
            PhaGrade.description,
            func.greatest(
                func.similarity(PhaGrade.name_zh, similarity_q),
                func.similarity(PhaGrade.code, similarity_q),
            ).label("score"),
        ).where(PhaGrade.status == "active")
        if grade:
            gstmt = gstmt.where(PhaGrade.code == grade)
        if like:
            gstmt = gstmt.where(
                (PhaGrade.name_zh.ilike(like))
                | (PhaGrade.code.ilike(like))
                | (PhaGrade.description.ilike(like))
            )
        gstmt = gstmt.order_by(text("score DESC NULLS LAST"), PhaGrade.id)
        for gid, code, name_zh, description, score in (await db.execute(gstmt)).all():
            hits.append(
                {
                    "type": "grade",
                    "id": gid,
                    "code": code,
                    "name_zh": name_zh,
                    "snippet": description,
                    "score": float(score or 0),
                    "domain_code": None,
                }
            )

    hits.sort(key=lambda h: -h["score"])
    total = len(hits)
    offset = (page - 1) * page_size
    paged = hits[offset : offset + page_size]

    facets = await _facets(db, q=q, tags=tags)
    type_counts: dict[str, int] = {}
    for h in hits:
        type_counts[h["type"]] = type_counts.get(h["type"], 0) + 1
    facets["type"] = [{"code": k, "count": v} for k, v in sorted(type_counts.items())]

    took_ms = int((time.perf_counter() - start) * 1000)
    return {
        "meta": {"total": total, "page": page, "page_size": page_size, "took_ms": took_ms},
        "facets": facets,
        "data": paged,
    }


async def _facets(
    db: AsyncSession, *, q: str = "", tags: list[str] | None = None
) -> dict:
    like = f"%{q}%" if q else None

    dstmt = (
        select(ApplicationDomain.code, func.count(ApplicationScenario.id))
        .join(ApplicationScenario, ApplicationScenario.domain_id == ApplicationDomain.id)
        .where(ApplicationScenario.status == "active")
        .group_by(ApplicationDomain.code)
        .order_by(func.count(ApplicationScenario.id).desc())
    )
    if like:
        dstmt = dstmt.where(
            (ApplicationScenario.name_zh.ilike(like))
            | (ApplicationScenario.summary.ilike(like))
        )
    domain_facets = [
        {"code": code, "count": int(c)} for code, c in (await db.execute(dstmt)).all()
    ]

    tstmt = (
        select(Tag.slug, func.count(ScenarioTag.scenario_id))
        .join(ScenarioTag, ScenarioTag.tag_id == Tag.id)
        .group_by(Tag.slug)
        .order_by(func.count(ScenarioTag.scenario_id).desc())
        .limit(20)
    )
    tag_facets = [
        {"code": slug, "count": int(c)} for slug, c in (await db.execute(tstmt)).all()
    ]

    return {"domain": domain_facets, "tag": tag_facets, "type": []}
