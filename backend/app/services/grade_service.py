from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundError
from app.models import (
    ApplicationDomain,
    ApplicationScenario,
    GradeScenarioMatch,
    PhaGrade,
)


async def list_grades(
    db: AsyncSession,
    *,
    family: str | None = None,
    q: str | None = None,
) -> list[PhaGrade]:
    stmt = select(PhaGrade).where(PhaGrade.status == "active").order_by(PhaGrade.id)
    if family:
        stmt = stmt.where(PhaGrade.polymer_family == family)
    if q:
        like = f"%{q}%"
        stmt = stmt.where((PhaGrade.name_zh.ilike(like)) | (PhaGrade.code.ilike(like)))
    return list((await db.execute(stmt)).scalars().all())


async def get_grade_detail(db: AsyncSession, key: str) -> dict:
    stmt = select(PhaGrade).options(
        selectinload(PhaGrade.matches)
        .selectinload(GradeScenarioMatch.scenario)
        .selectinload(ApplicationScenario.domain)
    )
    if key.isdigit():
        stmt = stmt.where(PhaGrade.id == int(key))
    else:
        stmt = stmt.where(PhaGrade.code == key)
    grade = (await db.execute(stmt)).scalar_one_or_none()
    if grade is None:
        raise NotFoundError(f"Grade '{key}' not found")

    matches = sorted(
        [
            {
                "scenario_id": m.scenario_id,
                "scenario_code": m.scenario.code,
                "scenario_name_zh": m.scenario.name_zh,
                "domain_code": m.scenario.domain.code,
                "match_score": m.match_score,
                "recommendation_level": m.recommendation_level,
                "key_metrics": m.key_metrics or {},
                "rationale": m.rationale,
            }
            for m in grade.matches
        ],
        key=lambda x: -x["match_score"],
    )

    return {
        "id": grade.id,
        "code": grade.code,
        "name_zh": grade.name_zh,
        "full_name": grade.full_name,
        "polymer_family": grade.polymer_family,
        "description": grade.description,
        "tm_celsius": _f(grade.tm_celsius),
        "tg_celsius": _f(grade.tg_celsius),
        "crystallinity_pct": _f(grade.crystallinity_pct),
        "elongation_at_break_pct": _f(grade.elongation_at_break_pct),
        "tensile_strength_mpa": _f(grade.tensile_strength_mpa),
        "youngs_modulus_gpa": _f(grade.youngs_modulus_gpa),
        "biocompatibility_class": grade.biocompatibility_class,
        "degradation_months_soil": _f(grade.degradation_months_soil),
        "degradation_months_marine": _f(grade.degradation_months_marine),
        "extra_metrics": grade.extra_metrics or {},
        "typical_processing": grade.typical_processing or [],
        "status": grade.status,
        "matches": matches,
    }


def _f(v) -> float | None:
    return float(v) if v is not None else None


async def recommend_scenarios_for_grade(
    db: AsyncSession, grade_id: int, top: int = 5
) -> list[dict]:
    stmt = (
        select(GradeScenarioMatch, ApplicationScenario, ApplicationDomain.code)
        .join(ApplicationScenario, ApplicationScenario.id == GradeScenarioMatch.scenario_id)
        .join(ApplicationDomain, ApplicationDomain.id == ApplicationScenario.domain_id)
        .where(GradeScenarioMatch.grade_id == grade_id)
        .order_by(GradeScenarioMatch.match_score.desc())
        .limit(top)
    )
    out: list[dict] = []
    for match, scenario, domain_code in (await db.execute(stmt)).all():
        out.append(
            {
                "scenario_id": scenario.id,
                "scenario_code": scenario.code,
                "scenario_name_zh": scenario.name_zh,
                "domain_code": domain_code,
                "match_score": match.match_score,
                "recommendation_level": match.recommendation_level,
                "key_metrics": match.key_metrics or {},
                "rationale": match.rationale,
            }
        )
    return out
