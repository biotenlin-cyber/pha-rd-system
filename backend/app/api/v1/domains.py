from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.schemas.domain import Domain
from app.services import domain_service

router = APIRouter()


@router.get("", response_model=list[Domain])
async def list_domains(db: AsyncSession = Depends(get_db)):
    return await domain_service.list_domains(db)


@router.get("/{key}", response_model=Domain)
async def get_domain(key: str, db: AsyncSession = Depends(get_db)):
    domain = await domain_service.get_domain_by_code_or_id(db, key)
    domains = await domain_service.list_domains(db)
    for d in domains:
        if d["id"] == domain.id:
            return d
    return {
        "id": domain.id,
        "code": domain.code,
        "name_zh": domain.name_zh,
        "name_en": domain.name_en,
        "description": domain.description,
        "icon": domain.icon,
        "sort_order": domain.sort_order,
        "scenario_count": 0,
    }
