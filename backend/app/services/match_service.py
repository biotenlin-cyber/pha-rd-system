from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import ApplicationScenario, GradeScenarioMatch, PhaGrade


async def list_matches(
    db: AsyncSession,
    *,
    grade_id: int | None = None,
    scenario_id: int | None = None,
    min_score: int | None = None,
) -> list[dict]:
    stmt = (
        select(GradeScenarioMatch)
        .options(
            selectinload(GradeScenarioMatch.grade),
            selectinload(GradeScenarioMatch.scenario).selectinload(ApplicationScenario.domain),
        )
        .order_by(GradeScenarioMatch.match_score.desc())
    )
    if grade_id is not None:
        stmt = stmt.where(GradeScenarioMatch.grade_id == grade_id)
    if scenario_id is not None:
        stmt = stmt.where(GradeScenarioMatch.scenario_id == scenario_id)
    if min_score is not None:
        stmt = stmt.where(GradeScenarioMatch.match_score >= min_score)

    rows = (await db.execute(stmt)).scalars().all()
    out: list[dict] = []
    for m in rows:
        out.append(
            {
                "id": m.id,
                "grade_id": m.grade_id,
                "grade_code": m.grade.code,
                "grade_name_zh": m.grade.name_zh,
                "scenario_id": m.scenario_id,
                "scenario_code": m.scenario.code,
                "scenario_name_zh": m.scenario.name_zh,
                "domain_code": m.scenario.domain.code,
                "match_score": m.match_score,
                "recommendation_level": m.recommendation_level,
                "key_metrics": m.key_metrics or {},
                "rationale": m.rationale,
            }
        )
    return out


async def recommend_grades_for_scenario(
    db: AsyncSession, scenario_id: int, top: int = 5
) -> list[dict]:
    stmt = (
        select(GradeScenarioMatch, PhaGrade)
        .join(PhaGrade, PhaGrade.id == GradeScenarioMatch.grade_id)
        .where(GradeScenarioMatch.scenario_id == scenario_id)
        .order_by(GradeScenarioMatch.match_score.desc())
        .limit(top)
    )
    out: list[dict] = []
    for match, grade in (await db.execute(stmt)).all():
        out.append(
            {
                "grade_id": grade.id,
                "grade_code": grade.code,
                "grade_name_zh": grade.name_zh,
                "match_score": match.match_score,
                "recommendation_level": match.recommendation_level,
                "key_metrics": match.key_metrics or {},
                "rationale": match.rationale,
            }
        )
    return out
