from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.models import Tag
from app.schemas.tag import Tag as TagSchema

router = APIRouter()


@router.get("", response_model=list[TagSchema])
async def list_tags(category: str | None = None, db: AsyncSession = Depends(get_db)):
    stmt = select(Tag).order_by(Tag.id)
    if category:
        stmt = stmt.where(Tag.category == category)
    return list((await db.execute(stmt)).scalars().all())
