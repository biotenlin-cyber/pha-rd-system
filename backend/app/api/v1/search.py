from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.schemas.search import SearchResponse
from app.services import search_service

router = APIRouter()


@router.get("", response_model=SearchResponse)
async def search(
    q: str = "",
    domain: str | None = None,
    grade: str | None = None,
    tags: list[str] | None = Query(None),
    types: list[str] | None = Query(None),
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    return await search_service.search(
        db,
        q=q,
        domain=domain,
        grade=grade,
        tags=tags,
        types=types,
        page=page,
        page_size=page_size,
    )
