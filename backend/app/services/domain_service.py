from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models import ApplicationDomain, ApplicationScenario


async def list_domains(db: AsyncSession) -> list[dict]:
    counts = (
        select(
            ApplicationScenario.domain_id,
            func.count(ApplicationScenario.id).label("scenario_count"),
        )
        .group_by(ApplicationScenario.domain_id)
        .subquery()
    )
    stmt = (
        select(ApplicationDomain, func.coalesce(counts.c.scenario_count, 0))
        .outerjoin(counts, counts.c.domain_id == ApplicationDomain.id)
        .order_by(ApplicationDomain.sort_order, ApplicationDomain.id)
    )
    result = await db.execute(stmt)
    out: list[dict] = []
    for domain, count in result.all():
        out.append(
            {
                "id": domain.id,
                "code": domain.code,
                "name_zh": domain.name_zh,
                "name_en": domain.name_en,
                "description": domain.description,
                "icon": domain.icon,
                "sort_order": domain.sort_order,
                "scenario_count": int(count),
            }
        )
    return out


async def get_domain_by_code_or_id(db: AsyncSession, key: str) -> ApplicationDomain:
    stmt = select(ApplicationDomain)
    if key.isdigit():
        stmt = stmt.where(ApplicationDomain.id == int(key))
    else:
        stmt = stmt.where(ApplicationDomain.code == key)
    obj = (await db.execute(stmt)).scalar_one_or_none()
    if obj is None:
        raise NotFoundError(f"Domain '{key}' not found")
    return obj
