from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.schemas.common import Page, Pagination
from app.schemas.scenario import ExternalLink, ScenarioDetail, ScenarioMatchSummary, ScenarioSummary
from app.services import match_service, scenario_service

router = APIRouter()


@router.get("", response_model=Page[ScenarioSummary])
async def list_scenarios(
    domain: str | None = None,
    q: str | None = None,
    tags: list[str] | None = Query(None),
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    data, total = await scenario_service.list_scenarios(
        db, domain=domain, tags=tags, q=q, page=page, page_size=page_size
    )
    return {"data": data, "meta": Pagination(page=page, page_size=page_size, total=total)}


@router.get("/{key}", response_model=ScenarioDetail)
async def get_scenario(key: str, db: AsyncSession = Depends(get_db)):
    return await scenario_service.get_scenario_detail(db, key)


@router.get("/{key}/matches", response_model=list[ScenarioMatchSummary])
async def get_scenario_matches(key: str, db: AsyncSession = Depends(get_db)):
    detail = await scenario_service.get_scenario_detail(db, key)
    return detail["matches"]


@router.get("/{key}/recommended-grades", response_model=list[ScenarioMatchSummary])
async def get_recommended_grades(
    key: str, top: int = 5, db: AsyncSession = Depends(get_db)
):
    detail = await scenario_service.get_scenario_detail(db, key)
    return await match_service.recommend_grades_for_scenario(db, detail["id"], top=top)


@router.get("/{key}/external-links", response_model=list[ExternalLink])
async def get_external_links(
    key: str,
    type: str | None = None,  # noqa: A002 - query alias
    db: AsyncSession = Depends(get_db),
):
    detail = await scenario_service.get_scenario_detail(db, key)
    return await scenario_service.list_scenario_external_links(db, detail["id"], type)
