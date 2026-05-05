from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.schemas.grade import Grade, GradeDetail, GradeMatchSummary
from app.services import grade_service, patent_service

router = APIRouter()


@router.get("", response_model=list[Grade])
async def list_grades(
    family: str | None = None,
    q: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    grades = await grade_service.list_grades(db, family=family, q=q)
    return [
        {
            "id": g.id,
            "code": g.code,
            "name_zh": g.name_zh,
            "full_name": g.full_name,
            "polymer_family": g.polymer_family,
            "description": g.description,
            "tm_celsius": float(g.tm_celsius) if g.tm_celsius else None,
            "tg_celsius": float(g.tg_celsius) if g.tg_celsius else None,
            "crystallinity_pct": float(g.crystallinity_pct) if g.crystallinity_pct else None,
            "elongation_at_break_pct": float(g.elongation_at_break_pct)
            if g.elongation_at_break_pct
            else None,
            "tensile_strength_mpa": float(g.tensile_strength_mpa)
            if g.tensile_strength_mpa
            else None,
            "youngs_modulus_gpa": float(g.youngs_modulus_gpa) if g.youngs_modulus_gpa else None,
            "biocompatibility_class": g.biocompatibility_class,
            "degradation_months_soil": float(g.degradation_months_soil)
            if g.degradation_months_soil
            else None,
            "degradation_months_marine": float(g.degradation_months_marine)
            if g.degradation_months_marine
            else None,
            "extra_metrics": g.extra_metrics or {},
            "typical_processing": g.typical_processing or [],
            "status": g.status,
        }
        for g in grades
    ]


@router.get("/{key}", response_model=GradeDetail)
async def get_grade(key: str, db: AsyncSession = Depends(get_db)):
    return await grade_service.get_grade_detail(db, key)


@router.get("/{key}/recommended-scenarios", response_model=list[GradeMatchSummary])
async def get_recommended_scenarios(
    key: str, top: int = 5, db: AsyncSession = Depends(get_db)
):
    detail = await grade_service.get_grade_detail(db, key)
    return await grade_service.recommend_scenarios_for_grade(db, detail["id"], top=top)


@router.get("/{key}/patents")
async def get_linked_patents(key: str, db: AsyncSession = Depends(get_db)):
    detail = await grade_service.get_grade_detail(db, key)
    return await patent_service.list_patents_for_grade(db, detail["id"])
