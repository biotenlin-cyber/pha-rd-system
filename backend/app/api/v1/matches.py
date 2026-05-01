from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.services import match_service

router = APIRouter()


@router.get("")
async def list_matches(
    grade_id: int | None = None,
    scenario_id: int | None = None,
    min_score: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await match_service.list_matches(
        db, grade_id=grade_id, scenario_id=scenario_id, min_score=min_score
    )
