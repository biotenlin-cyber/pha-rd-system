"""Research-analysis aggregations for patents.

Per PHA expert recommendation, MVP focuses on the 3 chart types that are
informative with ~12 patents:
  1. legal-status distribution (funnel)
  2. domain × grade heatmap
  3. top applicants bar chart
plus year/country/subclass facets for filtering.
"""
from __future__ import annotations

from sqlalchemy import distinct, extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Applicant,
    ApplicationDomain,
    ApplicationScenario,
    Inventor,
    Patent,
    PatentApplicant,
    PatentClassification,
    PatentGrade,
    PatentInventor,
    PatentScenario,
    PhaGrade,
)


async def overview(db: AsyncSession) -> dict:
    total = (await db.execute(select(func.count()).select_from(Patent))).scalar_one()

    by_legal = await _count(
        db,
        select(Patent.legal_status, func.count(Patent.id))
        .group_by(Patent.legal_status)
        .order_by(func.count(Patent.id).desc()),
    )

    by_country = await _count(
        db,
        select(Patent.country_code, func.count(Patent.id))
        .group_by(Patent.country_code)
        .order_by(func.count(Patent.id).desc()),
    )

    by_year_rows = (
        await db.execute(
            select(
                extract("year", Patent.application_date).label("yr"),
                func.count(Patent.id),
            )
            .where(Patent.application_date.is_not(None))
            .group_by("yr")
            .order_by("yr")
        )
    ).all()
    by_year = [
        {"code": str(int(yr)), "count": int(c)}
        for yr, c in by_year_rows
    ]

    by_top_applicant_rows = (
        await db.execute(
            select(Applicant.name_zh, func.count(distinct(PatentApplicant.patent_id)))
            .join(PatentApplicant, PatentApplicant.applicant_id == Applicant.id)
            .group_by(Applicant.id, Applicant.name_zh)
            .order_by(func.count(distinct(PatentApplicant.patent_id)).desc())
            .limit(10)
        )
    ).all()
    by_top_applicant = [
        {"code": name, "count": int(c)} for name, c in by_top_applicant_rows
    ]

    by_top_inventor_rows = (
        await db.execute(
            select(Inventor.name_zh, func.count(distinct(PatentInventor.patent_id)))
            .join(PatentInventor, PatentInventor.inventor_id == Inventor.id)
            .group_by(Inventor.id, Inventor.name_zh)
            .order_by(func.count(distinct(PatentInventor.patent_id)).desc())
            .limit(10)
        )
    ).all()
    by_top_inventor = [
        {"code": name, "count": int(c)} for name, c in by_top_inventor_rows
    ]

    by_subclass_rows = (
        await db.execute(
            select(
                PatentClassification.subclass,
                func.count(distinct(PatentClassification.patent_id)),
            )
            .where(PatentClassification.subclass.is_not(None))
            .group_by(PatentClassification.subclass)
            .order_by(func.count(distinct(PatentClassification.patent_id)).desc())
            .limit(15)
        )
    ).all()
    by_subclass = [
        {"code": code, "count": int(c)} for code, c in by_subclass_rows
    ]

    by_grade_rows = (
        await db.execute(
            select(PhaGrade.code, func.count(distinct(PatentGrade.patent_id)))
            .join(PatentGrade, PatentGrade.grade_id == PhaGrade.id)
            .group_by(PhaGrade.code)
            .order_by(func.count(distinct(PatentGrade.patent_id)).desc())
        )
    ).all()
    by_grade = [{"code": code, "count": int(c)} for code, c in by_grade_rows]

    by_domain_rows = (
        await db.execute(
            select(ApplicationDomain.code, func.count(distinct(PatentScenario.patent_id)))
            .join(ApplicationScenario, ApplicationScenario.domain_id == ApplicationDomain.id)
            .join(PatentScenario, PatentScenario.scenario_id == ApplicationScenario.id)
            .group_by(ApplicationDomain.code)
            .order_by(func.count(distinct(PatentScenario.patent_id)).desc())
        )
    ).all()
    by_domain = [
        {"code": code, "count": int(c)} for code, c in by_domain_rows
    ]

    return {
        "total": int(total),
        "by_legal_status": by_legal,
        "by_country": by_country,
        "by_year": by_year,
        "by_top_applicant": by_top_applicant,
        "by_top_inventor": by_top_inventor,
        "by_subclass": by_subclass,
        "by_grade": by_grade,
        "by_domain": by_domain,
    }


async def domain_grade_heatmap(db: AsyncSession) -> list[dict]:
    """Return matrix rows: {domain, grade, count} for the heatmap chart."""
    rows = (
        await db.execute(
            select(
                ApplicationDomain.code.label("domain"),
                PhaGrade.code.label("grade"),
                func.count(distinct(Patent.id)).label("c"),
            )
            .select_from(Patent)
            .join(PatentScenario, PatentScenario.patent_id == Patent.id)
            .join(ApplicationScenario, ApplicationScenario.id == PatentScenario.scenario_id)
            .join(ApplicationDomain, ApplicationDomain.id == ApplicationScenario.domain_id)
            .join(PatentGrade, PatentGrade.patent_id == Patent.id)
            .join(PhaGrade, PhaGrade.id == PatentGrade.grade_id)
            .group_by(ApplicationDomain.code, PhaGrade.code)
        )
    ).all()
    return [{"domain": d, "grade": g, "count": int(c)} for d, g, c in rows]


async def _count(db: AsyncSession, stmt) -> list[dict]:
    rows = (await db.execute(stmt)).all()
    return [{"code": str(c1), "count": int(c2)} for c1, c2 in rows if c1 is not None]
